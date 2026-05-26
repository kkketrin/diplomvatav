# Comparative Analysis of Electronic Payment Models

This project contains a Python implementation for a diploma work on the topic
**"Сравнителен анализ на модели за електронни плащания"**.

The code generates synthetic transaction data, aggregates indicators by payment
model, builds a decision matrix, normalizes the criteria, calculates rankings
under different scenarios, applies TOPSIS, performs sensitivity analysis and
creates charts.

## Project structure

```text
e_payment_analysis/
├── run_analysis.py
├── requirements.txt
├── README.md
├── src/
│   ├── config.py
│   ├── data_generator.py
│   ├── aggregation.py
│   ├── multicriteria.py
│   ├── visualization.py
│   └── main.py
├── notebooks/
│   └── electronic_payments_simulation.ipynb
├── data/
└── outputs/
    ├── tables/
    └── figures/
```

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python run_analysis.py
```

## Main outputs

Tables:

- `data/synthetic_transactions.csv`
- `outputs/tables/aggregated_metrics.csv`
- `outputs/tables/decision_matrix.csv`
- `outputs/tables/normalized_matrix.csv`
- `outputs/tables/scenario_scores.csv`
- `outputs/tables/topsis_balanced.csv`
- `outputs/tables/sensitivity_first_place.csv`

Figures:

- `outputs/figures/average_cost_by_model.png`
- `outputs/figures/average_latency_by_model.png`
- `outputs/figures/failure_rate_by_model.png`
- `outputs/figures/risk_probability_by_model.png`
- `outputs/figures/expected_loss_by_model.png`
- `outputs/figures/normalized_matrix_heatmap.png`
- `outputs/figures/scenario_scores.png`
- `outputs/figures/balanced_ranking.png`
- `outputs/figures/sensitivity_first_place.png`
- `outputs/figures/payment_infrastructure_graph.png`

## Note

The data and parameters are synthetic and illustrative. They are suitable for
demonstrating the methodology, but they should not be interpreted as real bank
fees, real processing times, or real risk values.
