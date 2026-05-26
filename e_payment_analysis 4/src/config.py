"""Configuration for the comparative analysis of electronic payment models.

The values are synthetic and illustrative. They are used to demonstrate the
methodology from the diploma work, not to describe real bank tariffs.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# General settings
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
TABLES_DIR = OUTPUT_DIR / "tables"
FIGURES_DIR = OUTPUT_DIR / "figures"

N_TRANSACTIONS = 5_000
RANDOM_SEED = 42
SENSITIVITY_ITERATIONS = 1_000

# ---------------------------------------------------------------------------
# Payment models
# ---------------------------------------------------------------------------
# Technical key -> Bulgarian display name and model parameters.
# Cost formula:
#   cost = fixed_fee + percent_fee * amount
#          + cross_border_fee * is_cross_border
#          + currency_conversion_fee * amount * has_currency_conversion
# Latency formula:
#   latency = base_latency + load_sensitivity * load + random noise
PAYMENT_MODELS = {
    "card_payment": {
        "label_bg": "Картово плащане",
        "fixed_fee": 0.10,
        "percent_fee": 0.018,
        "cross_border_fee": 0.20,
        "currency_conversion_fee": 0.012,
        "base_latency": 3.0,
        "latency_noise": 0.35,
        "load_sensitivity": 0.60,
        "failure_probability": 0.025,
        "base_risk": 0.035,
        "loss_given_default": 0.45,
        "cross_border_probability": 0.14,
        "conversion_probability": 0.35,
        "availability": 0.980,
        "scalability": 0.900,
        "user_convenience": 0.950,
        "regulatory_compatibility": 0.900,
    },
    "bank_transfer": {
        "label_bg": "Банков превод",
        "fixed_fee": 0.45,
        "percent_fee": 0.003,
        "cross_border_fee": 0.35,
        "currency_conversion_fee": 0.010,
        "base_latency": 10.0,
        "latency_noise": 0.90,
        "load_sensitivity": 1.20,
        "failure_probability": 0.015,
        "base_risk": 0.015,
        "loss_given_default": 0.35,
        "cross_border_probability": 0.10,
        "conversion_probability": 0.30,
        "availability": 0.970,
        "scalability": 0.760,
        "user_convenience": 0.650,
        "regulatory_compatibility": 0.950,
    },
    "instant_payment": {
        "label_bg": "Незабавно плащане",
        "fixed_fee": 0.20,
        "percent_fee": 0.006,
        "cross_border_fee": 0.15,
        "currency_conversion_fee": 0.007,
        "base_latency": 2.0,
        "latency_noise": 0.25,
        "load_sensitivity": 0.45,
        "failure_probability": 0.018,
        "base_risk": 0.020,
        "loss_given_default": 0.35,
        "cross_border_probability": 0.08,
        "conversion_probability": 0.20,
        "availability": 0.985,
        "scalability": 0.880,
        "user_convenience": 0.850,
        "regulatory_compatibility": 0.930,
    },
    "e_wallet": {
        "label_bg": "Електронен портфейл",
        "fixed_fee": 0.12,
        "percent_fee": 0.014,
        "cross_border_fee": 0.18,
        "currency_conversion_fee": 0.015,
        "base_latency": 2.5,
        "latency_noise": 0.30,
        "load_sensitivity": 0.50,
        "failure_probability": 0.020,
        "base_risk": 0.025,
        "loss_given_default": 0.40,
        "cross_border_probability": 0.22,
        "conversion_probability": 0.50,
        "availability": 0.975,
        "scalability": 0.860,
        "user_convenience": 0.920,
        "regulatory_compatibility": 0.850,
    },
    "open_banking": {
        "label_bg": "Open Banking плащане",
        "fixed_fee": 0.18,
        "percent_fee": 0.005,
        "cross_border_fee": 0.12,
        "currency_conversion_fee": 0.006,
        "base_latency": 4.0,
        "latency_noise": 0.50,
        "load_sensitivity": 0.80,
        "failure_probability": 0.030,
        "base_risk": 0.030,
        "loss_given_default": 0.38,
        "cross_border_probability": 0.12,
        "conversion_probability": 0.25,
        "availability": 0.960,
        "scalability": 0.820,
        "user_convenience": 0.800,
        "regulatory_compatibility": 0.940,
    },
}

MODEL_PROBABILITIES = {
    "card_payment": 0.30,
    "bank_transfer": 0.22,
    "instant_payment": 0.18,
    "e_wallet": 0.20,
    "open_banking": 0.10,
}

# ---------------------------------------------------------------------------
# Criteria
# ---------------------------------------------------------------------------
CRITERIA = [
    "average_cost",
    "average_latency",
    "failure_rate",
    "risk_probability",
    "availability",
    "scalability",
    "user_convenience",
    "regulatory_compatibility",
]

CRITERIA_LABELS_BG = {
    "average_cost": "Средна цена",
    "average_latency": "Средно време",
    "failure_rate": "Вероятност за отказ",
    "risk_probability": "Риск",
    "availability": "Наличност",
    "scalability": "Мащабируемост",
    "user_convenience": "Потребителско удобство",
    "regulatory_compatibility": "Регулаторна съвместимост",
}

MINIMIZE_CRITERIA = [
    "average_cost",
    "average_latency",
    "failure_rate",
    "risk_probability",
]

MAXIMIZE_CRITERIA = [
    "availability",
    "scalability",
    "user_convenience",
    "regulatory_compatibility",
]

# ---------------------------------------------------------------------------
# Scenario weights
# ---------------------------------------------------------------------------
# In every scenario the weights sum to 1.
SCENARIO_WEIGHTS = {
    "balanced": {
        "average_cost": 0.125,
        "average_latency": 0.125,
        "failure_rate": 0.125,
        "risk_probability": 0.125,
        "availability": 0.125,
        "scalability": 0.125,
        "user_convenience": 0.125,
        "regulatory_compatibility": 0.125,
    },
    "consumer": {
        "average_cost": 0.100,
        "average_latency": 0.180,
        "failure_rate": 0.120,
        "risk_probability": 0.150,
        "availability": 0.100,
        "scalability": 0.050,
        "user_convenience": 0.250,
        "regulatory_compatibility": 0.050,
    },
    "merchant": {
        "average_cost": 0.250,
        "average_latency": 0.100,
        "failure_rate": 0.200,
        "risk_probability": 0.100,
        "availability": 0.100,
        "scalability": 0.100,
        "user_convenience": 0.050,
        "regulatory_compatibility": 0.100,
    },
    "infrastructure": {
        "average_cost": 0.080,
        "average_latency": 0.120,
        "failure_rate": 0.150,
        "risk_probability": 0.150,
        "availability": 0.200,
        "scalability": 0.200,
        "user_convenience": 0.030,
        "regulatory_compatibility": 0.070,
    },
    "security_regulation": {
        "average_cost": 0.050,
        "average_latency": 0.050,
        "failure_rate": 0.150,
        "risk_probability": 0.300,
        "availability": 0.100,
        "scalability": 0.050,
        "user_convenience": 0.050,
        "regulatory_compatibility": 0.250,
    },
}

SCENARIO_LABELS_BG = {
    "balanced": "Балансиран сценарий",
    "consumer": "Потребителски сценарий",
    "merchant": "Търговски сценарий",
    "infrastructure": "Инфраструктурен сценарий",
    "security_regulation": "Сигурност и регулация",
}
