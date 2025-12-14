# app.py
import streamlit as st
import pandas as pd
import numpy as np
from model import optimize_prices

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="ParkWise Watertown – Dynamic Parking Pricing Advisor",
    layout="wide",
)

# ---------------- SESSION STATE ----------------
if "df_out" not in st.session_state:
    st.session_state["df_out"] = None

# ---------------- TITLE ----------------
st.title("ParkWise Watertown – Dynamic Parking Pricing Advisor")

st.markdown(
    """
This prescriptive analytics tool recommends **optimal hourly parking prices** by **zone** and **time block**
to balance **revenue** and a **target occupancy** (default 85%).

**Input requirements (aggregated CSV):**
- `zone`
- `time_block`
- `capacity`
- `baseline_price`
- `baseline_demand`
"""
)

st.markdown("---")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Configuration")

uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

st.sidebar.markdown("### Pricing Controls")
occ_target = st.sidebar.slider("Target occupancy", 0.50, 0.95, 0.85, 0.01)
p_min = st.sidebar.number_input("Minimum price ($/hr)", 0.0, 10.0, 0.5, 0.25)
p_max = st.sidebar.number_input("Maximum price ($/hr)", 0.0, 10.0, 3.0, 0.25)

st.sidebar.markdown("### Model Parameters")
beta = st.sidebar.slider("Price sensitivity (β)", 0.0, 1.0, 0.30, 0.05)
lam = st.sidebar.slider("Penalty weight (λ)", 1.0, 50.0, 10.0, 1.0)

run_btn = st.sidebar.button("Run optimization", type="primary")
clear_btn = st.sidebar.button("Clear results")

# ---------------- HELPERS ----------------
REQUIRED_COLS = {"zone", "time_block", "capacity", "baseline_price", "baseline_demand"}


def load_csv_safely(file):
    """
    Try UTF-8 first, then fallback to latin-1 to avoid UnicodeDecodeError.
    """
    try:
        file.seek(0)
        df = pd.read_csv(file)
        return df, "utf-8"
    except UnicodeDecodeError:
        file.seek(0)
        df = pd.read_csv(file, encoding="latin-1")
        return df, "latin-1"


def action_label(delta, tol=0.05):
    if delta > tol:
        return "Increase price"
    if delta < -tol:
        return "Decrease price"
    return "Keep price"


def clamp01(x):
    return np.clip(x, 0.0, 1.0)


# ---------------- MAIN ----------------
if clear_btn:
    st.session_state["df_out"] = None
    st.success("Results cleared. Run optimization again when ready.")

if uploaded_file is None:
    st.info("Upload a CSV file in the sidebar to begin.")
    st.stop()

# Load file
try:
    df, enc_used = load_csv_safely(uploaded_file)
except Exception as e:
    st.error(f"Could not read CSV file. Details: {e}")
    st.stop()

st.caption(f"File loaded with encoding: **{enc_used}**")

# Validate columns
missing = REQUIRED_COLS - set(df.columns)
if missing:
    st.error(
        f"Missing required columns: {', '.join(sorted(missing))}. "
        "Please upload a file with all required columns."
    )
    st.stop()

# ---------------- RUN OPTIMIZATION ----------------
if run_btn:
    with st.spinner("Running optimization model..."):
        try:
            df_out = optimize_prices(
                df,
                occ_target=occ_target,
                p_min=p_min,
                p_max=p_max,
                beta=beta,
                lam=lam,
            )
            st.session_state["df_out"] = df_out
        except Exception as e:
            st.error(f"Error while running optimization: {e}")
            st.stop()

    st.success("Optimization completed. Open the Summary / Decision Table tabs to view recommendations.")

# Tabs
tab1, tab2, tab3 = st.tabs(["1) Summary", "2) Decision Table", "3) Model Notes"])

# ---------------- TAB 1: SUMMARY ----------------
with tab1:
    st.subheader("Input preview")
    c1, c2 = st.columns(2)
    c1.metric("Rows", f"{len(df):,}")
    c2.metric("Columns", f"{len(df.columns):,}")
    st.dataframe(df.head(20), use_container_width=True)

    st.markdown("---")
    st.subheader("Optimization status")

    if st.session_state["df_out"] is None:
        st.info("Click **Run optimization** in the sidebar to generate recommendations.")
        st.stop()

    df_out = st.session_state["df_out"].copy()

    # Ensure occupancy is interpretable (0..1) even if upstream scale is messy
    df_out["predicted_occupancy_clipped"] = clamp01(df_out["predicted_occupancy"].astype(float))

    st.success("Optimization completed. Review recommendations below.")

    # Key Metrics
    total_rev = float(df_out["expected_revenue"].sum())
    avg_occ = float(df_out["predicted_occupancy_clipped"].mean())
    n_blocks = int(len(df_out))

    k1, k2, k3 = st.columns(3)
    k1.metric("Total Expected Revenue ($)", f"{total_rev:,.2f}")
    k2.metric("Average Predicted Occupancy", f"{avg_occ*100:.2f}%")
    k3.metric("Number of Zone–Time Blocks", f"{n_blocks:,}")

    # Executive Recommendation
    st.markdown("### Executive Recommendation")

    df_r = df_out.copy()
    df_r["price_change"] = df_r["recommended_price"] - df_r["baseline_price"]
    df_r["action"] = df_r["price_change"].apply(action_label)

    # Data scale warning (use unclipped to detect if it's exploding)
    high_rate = float((df_r["predicted_occupancy"] >= 1.0).mean())
    if high_rate > 0.50:
        st.warning(
            "Many blocks exceed 100% predicted occupancy before clipping. "
            "This usually means `baseline_demand` and `capacity` are not on the same scale "
            "(e.g., demand is aggregated across a different unit than capacity). "
            "Occupancy is clipped for interpretability; relative pricing actions remain useful."
        )

    top_up = df_r.sort_values("price_change", ascending=False).head(3)
    top_down = df_r.sort_values("price_change", ascending=True).head(3)

    st.markdown(
        f"""
**Decision:** apply the recommended hourly price for each zone–time block.

- **Target occupancy:** {occ_target*100:.0f}%  
- **Average predicted occupancy (clipped):** {avg_occ*100:.1f}%  
- **Total expected revenue:** ${total_rev:,.0f}
"""
    )

    st.markdown("**Biggest increases (top 3):**")
    for _, row in top_up.iterrows():
        st.write(
            f"- {row['zone']} ({row['time_block']}): "
            f"+${row['price_change']:.2f} → ${row['recommended_price']:.2f}"
        )

    st.markdown("**Biggest decreases (top 3):**")
    for _, row in top_down.iterrows():
        st.write(
            f"- {row['zone']} ({row['time_block']}): "
            f"${row['price_change']:.2f} → ${row['recommended_price']:.2f}"
        )

    st.markdown("---")
    st.subheader("Charts (zone-level summary)")

    rev_by_zone = df_out.groupby("zone")["expected_revenue"].sum().sort_values(ascending=False)
    occ_by_zone = (
        df_out.groupby("zone")["predicted_occupancy_clipped"].mean().sort_values(ascending=False)
    )

    a, b = st.columns(2)
    with a:
        st.write("Revenue by Zone")
        st.bar_chart(rev_by_zone)
    with b:
        st.write("Occupancy by Zone (clipped 0–100%)")
        st.bar_chart(occ_by_zone)

# ---------------- TAB 2: DECISION TABLE ----------------
with tab2:
    st.subheader("Decision Table (what to do)")

    if st.session_state["df_out"] is None:
        st.info("Run optimization first to generate the decision table.")
        st.stop()

    df_out = st.session_state["df_out"].copy()
    df_out["predicted_occupancy_clipped"] = clamp01(df_out["predicted_occupancy"].astype(float))

    df_out["price_change"] = df_out["recommended_price"] - df_out["baseline_price"]
    df_out["action"] = df_out["price_change"].apply(action_label)

    cols = [
        "zone",
        "time_block",
        "capacity",
        "baseline_price",
        "recommended_price",
        "price_change",
        "action",
        "predicted_occupancy_clipped",
        "expected_revenue",
    ]

    df_show = df_out[cols].sort_values(["zone", "time_block"]).copy()
    df_show = df_show.rename(columns={"predicted_occupancy_clipped": "predicted_occupancy"})

    st.dataframe(df_show, use_container_width=True)

    st.download_button(
        "Download results as CSV",
        data=df_show.to_csv(index=False).encode("utf-8"),
        file_name="pricing_recommendations.csv",
        mime="text/csv",
    )

# ---------------- TAB 3: MODEL NOTES ----------------
with tab3:
    st.subheader("Model notes (simple, decision-focused)")

    st.markdown(
        """
**Prescriptive structure**
- **Decision variable:** hourly price per zone–time block
- **Objective:** maximize expected revenue while staying close to the target occupancy
- **Constraints:** price bounds → `[min price, max price]`

**Key assumptions**
- Demand responds to price using a simple sensitivity parameter (**beta**).
- Occupancy is computed from predicted demand and capacity.
- Occupancy shown in the dashboard is **clipped to 0–100%** for interpretability.

**Interpretation**
- If many blocks exceed 100% occupancy before clipping, the dataset likely has scale differences
  between demand and capacity due to aggregation.
- The tool is most useful for consistent pricing recommendations across zones and time blocks.
"""
    )
