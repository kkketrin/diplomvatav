"""Multicriteria analysis: normalization, weighted scores, TOPSIS, sensitivity."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .config import (
    CRITERIA,
    MAXIMIZE_CRITERIA,
    MINIMIZE_CRITERIA,
    PAYMENT_MODELS,
    RANDOM_SEED,
    SCENARIO_WEIGHTS,
    SENSITIVITY_ITERATIONS,
)


def normalize_decision_matrix(decision_matrix: pd.DataFrame) -> pd.DataFrame:
    """Normalize criteria to [0, 1], where 1 is always the best value."""
    normalized = decision_matrix[["payment_model", "payment_model_bg"]].copy()

    for criterion in CRITERIA:
        values = decision_matrix[criterion].astype(float)
        min_value = values.min()
        max_value = values.max()

        if np.isclose(max_value, min_value):
            normalized[criterion] = 1.0
        elif criterion in MAXIMIZE_CRITERIA:
            normalized[criterion] = (values - min_value) / (max_value - min_value)
        elif criterion in MINIMIZE_CRITERIA:
            normalized[criterion] = (max_value - values) / (max_value - min_value)
        else:
            raise ValueError(f"Unknown criterion direction: {criterion}")

    normalized[CRITERIA] = normalized[CRITERIA].round(6)
    return normalized


def _weights_to_array(weights: dict[str, float]) -> np.ndarray:
    """Convert a weight dictionary to an array ordered by CRITERIA."""
    weight_sum = sum(weights.values())
    if not np.isclose(weight_sum, 1.0):
        raise ValueError(f"Scenario weights must sum to 1, got {weight_sum}")
    return np.array([weights[criterion] for criterion in CRITERIA], dtype=float)


def calculate_weighted_scores(normalized_matrix: pd.DataFrame) -> pd.DataFrame:
    """Calculate weighted-sum scores for all scenarios."""
    values = normalized_matrix[CRITERIA].to_numpy(dtype=float)
    rows: list[dict] = []

    for scenario_name, weights in SCENARIO_WEIGHTS.items():
        weight_array = _weights_to_array(weights)
        scores = values @ weight_array

        scenario_df = normalized_matrix[["payment_model", "payment_model_bg"]].copy()
        scenario_df["scenario"] = scenario_name
        scenario_df["score"] = scores
        scenario_df["rank"] = scenario_df["score"].rank(ascending=False, method="min").astype(int)
        scenario_df = scenario_df.sort_values(["scenario", "rank", "payment_model"]).reset_index(drop=True)
        rows.extend(scenario_df.to_dict(orient="records"))

    result = pd.DataFrame(rows)
    result["score"] = result["score"].round(6)
    return result[["scenario", "payment_model", "payment_model_bg", "score", "rank"]]


def calculate_topsis(
    normalized_matrix: pd.DataFrame,
    scenario: str = "balanced",
) -> pd.DataFrame:
    """Apply the TOPSIS method to normalized criteria.

    The normalized matrix already has a beneficial direction for every criterion:
    higher values are better. Therefore, the ideal best solution is the maximum
    value by column and the ideal worst solution is the minimum value by column.
    """
    if scenario not in SCENARIO_WEIGHTS:
        raise KeyError(f"Unknown scenario: {scenario}")

    values = normalized_matrix[CRITERIA].to_numpy(dtype=float)
    weights = _weights_to_array(SCENARIO_WEIGHTS[scenario])
    weighted = values * weights

    ideal_best = weighted.max(axis=0)
    ideal_worst = weighted.min(axis=0)

    distance_best = np.linalg.norm(weighted - ideal_best, axis=1)
    distance_worst = np.linalg.norm(weighted - ideal_worst, axis=1)
    coefficient = distance_worst / (distance_best + distance_worst)

    result = normalized_matrix[["payment_model", "payment_model_bg"]].copy()
    result["scenario"] = scenario
    result["distance_to_best"] = distance_best
    result["distance_to_worst"] = distance_worst
    result["topsis_score"] = coefficient
    result["rank"] = result["topsis_score"].rank(ascending=False, method="min").astype(int)
    result = result.sort_values(["rank", "payment_model"]).reset_index(drop=True)

    numeric_cols = ["distance_to_best", "distance_to_worst", "topsis_score"]
    result[numeric_cols] = result[numeric_cols].round(6)
    return result


def run_sensitivity_analysis(
    normalized_matrix: pd.DataFrame,
    n_iterations: int = SENSITIVITY_ITERATIONS,
    random_seed: int = RANDOM_SEED,
) -> pd.DataFrame:
    """Test ranking stability under many random weight combinations."""
    rng = np.random.default_rng(random_seed)
    values = normalized_matrix[CRITERIA].to_numpy(dtype=float)
    model_keys = normalized_matrix["payment_model"].to_list()

    first_place_counts = {model_key: 0 for model_key in model_keys}
    average_scores = {model_key: [] for model_key in model_keys}

    for _ in range(n_iterations):
        weights = rng.dirichlet(np.ones(len(CRITERIA)))
        scores = values @ weights
        best_index = int(np.argmax(scores))
        first_place_counts[model_keys[best_index]] += 1

        for model_key, score in zip(model_keys, scores):
            average_scores[model_key].append(float(score))

    rows = []
    for model_key in model_keys:
        rows.append(
            {
                "payment_model": model_key,
                "payment_model_bg": PAYMENT_MODELS[model_key]["label_bg"],
                "first_place_count": first_place_counts[model_key],
                "first_place_share": first_place_counts[model_key] / n_iterations,
                "average_random_score": float(np.mean(average_scores[model_key])),
            }
        )

    result = pd.DataFrame(rows)
    result = result.sort_values(
        ["first_place_count", "average_random_score"], ascending=False
    ).reset_index(drop=True)
    result["first_place_share"] = result["first_place_share"].round(6)
    result["average_random_score"] = result["average_random_score"].round(6)
    return result


def save_table(df: pd.DataFrame, output_path) -> None:
    """Save a table to CSV with UTF-8 BOM."""
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
