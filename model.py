# model.py
import numpy as np
import pandas as pd
from scipy.optimize import minimize


REQUIRED_COLUMNS = [
    "zone",
    "time_block",
    "capacity",
    "baseline_price",
    "baseline_demand",
]


def validate_input_df(df: pd.DataFrame) -> None:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def optimize_prices(
    df: pd.DataFrame,
    occ_target: float = 0.85,
    p_min: float = 0.5,
    p_max: float = 3.0,
    beta: float = 0.3,
    lam: float = 10.0,
) -> pd.DataFrame:

    validate_input_df(df)

    df = df.copy()
    df["capacity"] = pd.to_numeric(df["capacity"], errors="coerce")
    df["baseline_price"] = pd.to_numeric(df["baseline_price"], errors="coerce")
    df["baseline_demand"] = pd.to_numeric(df["baseline_demand"], errors="coerce")
    df = df.dropna(subset=["capacity", "baseline_price", "baseline_demand"])

    cap = df["capacity"].values.astype(float)
    P0 = df["baseline_price"].values.astype(float)
    D0 = df["baseline_demand"].values.astype(float)

    if len(df) == 0:
        raise ValueError("No valid rows after cleaning.")

    x0 = np.clip(P0, p_min, p_max)
    P0_safe = P0 + 1e-6
    cap_safe = cap + 1e-6

    def objective(p):
        demand = np.maximum(0.0, D0 * (1 - beta * (p - P0_safe) / P0_safe))
        occ = demand / cap_safe
        revenue = p * demand
        penalty = np.sum((occ - occ_target)**2)
        return -np.sum(revenue) + lam * penalty

    bounds = [(p_min, p_max)] * len(df)
    result = minimize(objective, x0, bounds=bounds, method="L-BFGS-B")

    p_opt = result.x
    demand_opt = np.maximum(0.0, D0 * (1 - beta * (p_opt - P0_safe) / P0_safe))
    occ_opt = demand_opt / cap_safe
    revenue_opt = p_opt * demand_opt

    df_out = df.copy()
    df_out["recommended_price"] = p_opt
    df_out["predicted_demand"] = demand_opt
    df_out["predicted_occupancy"] = occ_opt
    df_out["expected_revenue"] = revenue_opt

    return df_out
