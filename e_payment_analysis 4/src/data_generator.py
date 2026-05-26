"""Synthetic transaction generation.

The generator creates artificial transactions for the five electronic payment
models. The data are suitable for demonstrating the mathematical methodology
from the diploma work without using real personal or financial information.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .config import MODEL_PROBABILITIES, PAYMENT_MODELS, RANDOM_SEED


def generate_amount(rng: np.random.Generator) -> float:
    """Generate a positive payment amount.

    A lognormal distribution is used because transaction values are often
    right-skewed: many smaller payments and fewer large ones.
    """
    amount = rng.lognormal(mean=3.5, sigma=0.85)
    return round(float(np.clip(amount, 5.0, 1_500.0)), 2)


def calculate_cost(
    amount: float,
    model_params: dict,
    is_cross_border: bool,
    has_currency_conversion: bool,
) -> float:
    """Calculate the transaction cost using a simplified tariff formula."""
    cost = (
        model_params["fixed_fee"]
        + model_params["percent_fee"] * amount
        + model_params["cross_border_fee"] * int(is_cross_border)
        + model_params["currency_conversion_fee"] * amount * int(has_currency_conversion)
    )
    return round(float(max(cost, 0.0)), 4)


def calculate_latency(
    model_params: dict,
    rng: np.random.Generator,
) -> float:
    """Calculate processing time in conditional time units."""
    load = rng.beta(a=2.0, b=5.0)
    noise = rng.normal(loc=0.0, scale=model_params["latency_noise"])
    latency = model_params["base_latency"] + model_params["load_sensitivity"] * load + noise
    return round(float(max(latency, 0.1)), 4)


def calculate_risk_probability(
    amount: float,
    model_params: dict,
    is_cross_border: bool,
    has_currency_conversion: bool,
    rng: np.random.Generator,
) -> float:
    """Calculate a synthetic risk probability between 0 and 1."""
    amount_factor = min(amount / 1_500.0, 1.0) * 0.025
    cross_border_factor = 0.012 if is_cross_border else 0.0
    conversion_factor = 0.010 if has_currency_conversion else 0.0
    noise = rng.normal(loc=0.0, scale=0.004)
    risk = model_params["base_risk"] + amount_factor + cross_border_factor + conversion_factor + noise
    return round(float(np.clip(risk, 0.001, 0.999)), 5)


def generate_transactions(
    n_transactions: int,
    random_seed: int = RANDOM_SEED,
) -> pd.DataFrame:
    """Generate a dataframe with synthetic transactions."""
    rng = np.random.default_rng(random_seed)
    model_keys = list(MODEL_PROBABILITIES.keys())
    model_probs = np.array([MODEL_PROBABILITIES[key] for key in model_keys], dtype=float)
    model_probs = model_probs / model_probs.sum()

    rows: list[dict] = []

    for transaction_id in range(1, n_transactions + 1):
        model_key = str(rng.choice(model_keys, p=model_probs))
        params = PAYMENT_MODELS[model_key]

        amount = generate_amount(rng)
        is_cross_border = bool(rng.random() < params["cross_border_probability"])
        has_currency_conversion = bool(
            is_cross_border and rng.random() < params["conversion_probability"]
        )

        cost = calculate_cost(amount, params, is_cross_border, has_currency_conversion)
        latency = calculate_latency(params, rng)
        is_failed = bool(rng.random() < params["failure_probability"])
        risk_probability = calculate_risk_probability(
            amount, params, is_cross_border, has_currency_conversion, rng
        )
        expected_loss = round(
            float(risk_probability * params["loss_given_default"] * amount), 4
        )

        rows.append(
            {
                "transaction_id": transaction_id,
                "payment_model": model_key,
                "payment_model_bg": params["label_bg"],
                "amount": amount,
                "is_cross_border": is_cross_border,
                "has_currency_conversion": has_currency_conversion,
                "cost": cost,
                "latency": latency,
                "is_failed": is_failed,
                "risk_probability": risk_probability,
                "expected_loss": expected_loss,
                "status": "failed" if is_failed else "success",
            }
        )

    return pd.DataFrame(rows)


def save_transactions(df: pd.DataFrame, output_path) -> None:
    """Save generated transactions to CSV."""
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
