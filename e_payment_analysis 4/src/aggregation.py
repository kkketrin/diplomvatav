"""Aggregation of synthetic transaction data by payment model."""

from __future__ import annotations

import pandas as pd

from .config import CRITERIA, PAYMENT_MODELS


def aggregate_metrics(transactions: pd.DataFrame) -> pd.DataFrame:
    """Calculate average indicators for every payment model."""
    grouped = transactions.groupby("payment_model", as_index=False).agg(
        payment_model_bg=("payment_model_bg", "first"),
        transaction_count=("transaction_id", "count"),
        average_amount=("amount", "mean"),
        average_cost=("cost", "mean"),
        average_latency=("latency", "mean"),
        failure_rate=("is_failed", "mean"),
        risk_probability=("risk_probability", "mean"),
        expected_loss=("expected_loss", "mean"),
    )

    static_rows = []
    for model_key, params in PAYMENT_MODELS.items():
        static_rows.append(
            {
                "payment_model": model_key,
                "availability": params["availability"],
                "scalability": params["scalability"],
                "user_convenience": params["user_convenience"],
                "regulatory_compatibility": params["regulatory_compatibility"],
            }
        )

    static_df = pd.DataFrame(static_rows)
    result = grouped.merge(static_df, on="payment_model", how="left")

    numeric_cols = result.select_dtypes(include="number").columns
    result[numeric_cols] = result[numeric_cols].round(6)

    # Keep the same order as in the configuration.
    order = list(PAYMENT_MODELS.keys())
    result["_order"] = result["payment_model"].apply(order.index)
    result = result.sort_values("_order").drop(columns="_order").reset_index(drop=True)
    return result


def create_decision_matrix(aggregated_metrics: pd.DataFrame) -> pd.DataFrame:
    """Create the decision matrix used for normalization and ranking."""
    columns = ["payment_model", "payment_model_bg"] + CRITERIA
    return aggregated_metrics[columns].copy()


def save_table(df: pd.DataFrame, output_path) -> None:
    """Save a table to CSV with UTF-8 BOM for comfortable Excel opening."""
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
