"""Main pipeline for the electronic payment model analysis."""

from __future__ import annotations

from .aggregation import aggregate_metrics, create_decision_matrix, save_table
from .config import DATA_DIR, N_TRANSACTIONS, RANDOM_SEED, TABLES_DIR
from .data_generator import generate_transactions, save_transactions
from .multicriteria import (
    calculate_topsis,
    calculate_weighted_scores,
    normalize_decision_matrix,
    run_sensitivity_analysis,
    save_table as save_multicriteria_table,
)
from .visualization import create_all_figures


def ensure_directories() -> None:
    """Create all required output folders."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)


def run_pipeline() -> dict[str, object]:
    """Run the full simulation and analysis pipeline."""
    ensure_directories()

    transactions = generate_transactions(N_TRANSACTIONS, RANDOM_SEED)
    save_transactions(transactions, DATA_DIR / "synthetic_transactions.csv")

    aggregated_metrics = aggregate_metrics(transactions)
    save_table(aggregated_metrics, TABLES_DIR / "aggregated_metrics.csv")

    decision_matrix = create_decision_matrix(aggregated_metrics)
    save_table(decision_matrix, TABLES_DIR / "decision_matrix.csv")

    normalized_matrix = normalize_decision_matrix(decision_matrix)
    save_multicriteria_table(normalized_matrix, TABLES_DIR / "normalized_matrix.csv")

    scenario_scores = calculate_weighted_scores(normalized_matrix)
    save_multicriteria_table(scenario_scores, TABLES_DIR / "scenario_scores.csv")

    topsis_balanced = calculate_topsis(normalized_matrix, scenario="balanced")
    save_multicriteria_table(topsis_balanced, TABLES_DIR / "topsis_balanced.csv")

    sensitivity_results = run_sensitivity_analysis(normalized_matrix)
    save_multicriteria_table(
        sensitivity_results, TABLES_DIR / "sensitivity_first_place.csv"
    )

    create_all_figures(
        aggregated_metrics,
        normalized_matrix,
        scenario_scores,
        sensitivity_results,
    )

    return {
        "transactions": transactions,
        "aggregated_metrics": aggregated_metrics,
        "decision_matrix": decision_matrix,
        "normalized_matrix": normalized_matrix,
        "scenario_scores": scenario_scores,
        "topsis_balanced": topsis_balanced,
        "sensitivity_results": sensitivity_results,
    }


def main() -> None:
    """Entry point used by run_analysis.py."""
    results = run_pipeline()
    print("Analysis completed successfully.")
    print(f"Generated transactions: {len(results['transactions'])}")
    print("Tables saved to: outputs/tables")
    print("Figures saved to: outputs/figures")


if __name__ == "__main__":
    main()
