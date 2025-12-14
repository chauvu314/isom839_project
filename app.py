# app.py
import streamlit as st
import pandas as pd
from model import optimize_prices

# --- Streamlit Page Config ---
st.set_page_config(
    page_title="ParkWise Watertown – Dynamic Parking Pricing Advisor",
    layout="wide",
)

# --- Title & Intro ---
st.title("🚗 ParkWise Watertown – Dynamic Parking Pricing Advisor")

st.markdown(
    """
This tool helps you explore **dynamic pricing scenarios** for Watertown parking.

Upload an aggregated CSV with at least these columns:

- `zone`
- `time_block`
- `capacity`
- `baseline_price`
- `baseline_demand`
"""
)

st.markdown("---")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Configuration")

uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

st.sidebar.markdown("### Pricing Controls")

occ_target = st.sidebar.slider("Target occupancy", 0.50, 0.95, 0.85, 0.01)
p_min = st.sidebar.number_input("Minimum price ($/hr)", 0.0, 10.0, 0.5, 0.25)
p_max = st.sidebar.number_input("Maximum price ($/hr)", 0.0, 10.0, 3.0, 0.25)

st.sidebar.markdown("### Model Parameters")

beta = st.sidebar.slider("Price sensitivity (β)", 0.0, 1.0, 0.30, 0.05)
lam = st.sidebar.slider("Penalty weight (λ)", 1.0, 50.0, 10.0, 1.0)

run_btn = st.sidebar.button("Run optimization")

# ---------------- HELPERS ----------------
REQUIRED_COLS = {"zone", "time_block", "capacity", "baseline_price", "baseline_demand"}


def load_csv_safely(file):
    """
    Try to read as UTF-8 first.
    If it fails, fall back to latin-1 to avoid UnicodeDecodeError.
    """
    # Try UTF-8
    try:
        file.seek(0)
        df = pd.read_csv(file)
        return df, "utf-8"
    except UnicodeDecodeError:
        pass

    # Fallback to latin-1
    file.seek(0)
    df = pd.read_csv(file, encoding="latin-1")
    return df, "latin-1"


# ---------------- MAIN PAGE ----------------

if uploaded_file is None:
    st.info("⬅️ Upload a CSV file in the sidebar to begin.")
    st.stop()

# Read and preview input file with safer encoding handling
try:
    df, enc_used = load_csv_safely(uploaded_file)
except Exception as e:
    st.error(f"Could not read CSV file. Details: {e}")
    st.stop()

st.caption(f"File loaded with encoding: **{enc_used}**")
st.subheader("📥 Input data preview")

# Basic shape + preview
c1, c2 = st.columns(2)
c1.metric("Rows", f"{len(df):,}")
c2.metric("Columns", f"{len(df.columns):,}")

st.dataframe(df.head(20), use_container_width=True)

# Validate required columns
missing = REQUIRED_COLS - set(df.columns)
if missing:
    st.error(
        f"Missing required columns: {', '.join(sorted(missing))}. "
        "Please upload a file with all required columns."
    )
    st.stop()

st.markdown("---")

# Tabs for structure
tab_input, tab_results = st.tabs(["📊 Input summary", "🧠 Optimization results"])

with tab_input:
    st.markdown("#### Column summary")
    st.write(df.describe(include="all").transpose())

with tab_results:
    st.markdown("Click **Run optimization** in the sidebar to generate results.")

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
        except Exception as e:
            st.error(f"Error while running optimization: {e}")
            st.stop()

    st.success("Optimization completed.")

    # --- Metrics ---
    st.subheader("📈 Key Metrics")

    total_rev = df_out["expected_revenue"].sum()
    avg_occ = df_out["predicted_occupancy"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Expected Revenue ($)", f"{total_rev:,.2f}")
    col2.metric("Average Predicted Occupancy", f"{avg_occ:.2%}")
    col3.metric("Number of Zone–Time Blocks", f"{len(df_out):,}")

    # --- Full Table ---
    st.markdown("### 🔍 Full Optimization Table")
    st.dataframe(df_out, use_container_width=True)

    # --- Charts ---
    st.markdown("### 🗺️ Revenue & Occupancy by Zone")

    if "zone" in df_out.columns:
        rev_by_zone = df_out.groupby("zone")["expected_revenue"].sum().sort_values(
            ascending=False
        )
        occ_by_zone = (
            df_out.groupby("zone")["predicted_occupancy"].mean().sort_values()
        )

        colA, colB = st.columns(2)

        with colA:
            st.write("**Revenue by Zone**")
            st.bar_chart(rev_by_zone)

        with colB:
            st.write("**Occupancy by Zone**")
            st.bar_chart(occ_by_zone)
    else:
        st.warning("Missing 'zone' column, cannot generate charts.")
