"""Visualization utilities for tables and figures used in the analysis."""

from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

from .config import (
    CRITERIA,
    CRITERIA_LABELS_BG,
    FIGURES_DIR,
    PAYMENT_MODELS,
    SCENARIO_LABELS_BG,
)


def _save_current_figure(filename: str) -> None:
    """Save the current matplotlib figure and close it."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    output_path = FIGURES_DIR / filename
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


def plot_bar(
    df: pd.DataFrame,
    value_column: str,
    title: str,
    ylabel: str,
    filename: str,
    sort_ascending: bool | None = None,
) -> None:
    """Create a simple bar chart by payment model."""
    plot_df = df.copy()
    if sort_ascending is not None:
        plot_df = plot_df.sort_values(value_column, ascending=sort_ascending)

    plt.figure(figsize=(9, 5))
    plt.bar(plot_df["payment_model_bg"], plot_df[value_column])
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel("Платежен модел")
    plt.xticks(rotation=25, ha="right")
    _save_current_figure(filename)


def plot_basic_metric_charts(aggregated_metrics: pd.DataFrame) -> None:
    """Create charts for basic aggregated indicators."""
    plot_bar(
        aggregated_metrics,
        "average_cost",
        "Сравнение по средна цена",
        "Средна цена",
        "average_cost_by_model.png",
        sort_ascending=True,
    )
    plot_bar(
        aggregated_metrics,
        "average_latency",
        "Сравнение по средно време за обработка",
        "Средно време (условни единици)",
        "average_latency_by_model.png",
        sort_ascending=True,
    )
    plot_bar(
        aggregated_metrics,
        "failure_rate",
        "Сравнение по вероятност за отказ",
        "Дял на отказаните транзакции",
        "failure_rate_by_model.png",
        sort_ascending=True,
    )
    plot_bar(
        aggregated_metrics,
        "risk_probability",
        "Сравнение по среден риск",
        "Средна рискова оценка",
        "risk_probability_by_model.png",
        sort_ascending=True,
    )
    plot_bar(
        aggregated_metrics,
        "expected_loss",
        "Сравнение по очаквана загуба",
        "Средна очаквана загуба",
        "expected_loss_by_model.png",
        sort_ascending=True,
    )


def plot_normalized_heatmap(normalized_matrix: pd.DataFrame) -> None:
    """Create a heatmap of the normalized decision matrix."""
    values = normalized_matrix[CRITERIA].to_numpy(dtype=float)
    row_labels = normalized_matrix["payment_model_bg"].to_list()
    col_labels = [CRITERIA_LABELS_BG[col] for col in CRITERIA]

    plt.figure(figsize=(11, 5.5))
    plt.imshow(values, aspect="auto")
    plt.colorbar(label="Нормализирана стойност")
    plt.xticks(np.arange(len(col_labels)), col_labels, rotation=35, ha="right")
    plt.yticks(np.arange(len(row_labels)), row_labels)
    plt.title("Нормализирана матрица на решенията")

    for i in range(values.shape[0]):
        for j in range(values.shape[1]):
            plt.text(j, i, f"{values[i, j]:.2f}", ha="center", va="center")

    _save_current_figure("normalized_matrix_heatmap.png")


def plot_scenario_scores(scenario_scores: pd.DataFrame) -> None:
    """Create a grouped chart with scores by scenario."""
    pivot = scenario_scores.pivot(
        index="payment_model_bg", columns="scenario", values="score"
    )
    pivot = pivot.rename(columns=SCENARIO_LABELS_BG)

    plt.figure(figsize=(11, 6))
    x = np.arange(len(pivot.index))
    width = 0.16

    for idx, column in enumerate(pivot.columns):
        offset = (idx - (len(pivot.columns) - 1) / 2) * width
        plt.bar(x + offset, pivot[column], width, label=column)

    plt.title("Сценарийно класиране на платежните модели")
    plt.ylabel("Обща оценка")
    plt.xlabel("Платежен модел")
    plt.xticks(x, pivot.index, rotation=25, ha="right")
    plt.legend(fontsize=8)
    _save_current_figure("scenario_scores.png")


def plot_balanced_ranking(scenario_scores: pd.DataFrame) -> None:
    """Create a ranking chart for the balanced scenario."""
    balanced = scenario_scores[scenario_scores["scenario"] == "balanced"].sort_values(
        "score", ascending=False
    )
    plot_bar(
        balanced,
        "score",
        "Класиране при балансиран сценарий",
        "Обща оценка",
        "balanced_ranking.png",
        sort_ascending=False,
    )


def plot_sensitivity_results(sensitivity_results: pd.DataFrame) -> None:
    """Create a chart showing first-place frequency in sensitivity analysis."""
    plot_bar(
        sensitivity_results,
        "first_place_share",
        "Анализ на чувствителността",
        "Дял на първо място",
        "sensitivity_first_place.png",
        sort_ascending=False,
    )


def plot_payment_infrastructure_graph() -> None:
    """Create a simplified graph of the payment infrastructure."""
    graph = nx.DiGraph()
    edges = [
        ("Клиент", "Търговец"),
        ("Търговец", "Платежен процесор"),
        ("Платежен процесор", "Банка / картова схема"),
        ("Банка / картова схема", "Банка на получателя"),
        ("Банка на получателя", "Получател"),
        ("Клиент", "Електронен портфейл"),
        ("Електронен портфейл", "Търговец"),
        ("Клиент", "Платежен инициатор"),
        ("Платежен инициатор", "Банка на клиента"),
        ("Банка на клиента", "Получател"),
    ]
    graph.add_edges_from(edges)

    plt.figure(figsize=(11, 6))
    pos = nx.spring_layout(graph, seed=42, k=0.9)
    nx.draw_networkx_nodes(graph, pos, node_size=2400)
    nx.draw_networkx_edges(graph, pos, arrows=True, arrowsize=18, width=1.5)
    nx.draw_networkx_labels(graph, pos, font_size=8)
    plt.title("Опростен графов модел на платежната инфраструктура")
    plt.axis("off")
    _save_current_figure("payment_infrastructure_graph.png")


def create_all_figures(
    aggregated_metrics: pd.DataFrame,
    normalized_matrix: pd.DataFrame,
    scenario_scores: pd.DataFrame,
    sensitivity_results: pd.DataFrame,
) -> None:
    """Create all figures used in the numerical analysis."""
    plot_basic_metric_charts(aggregated_metrics)
    plot_normalized_heatmap(normalized_matrix)
    plot_scenario_scores(scenario_scores)
    plot_balanced_ranking(scenario_scores)
    plot_sensitivity_results(sensitivity_results)
    plot_payment_infrastructure_graph()
