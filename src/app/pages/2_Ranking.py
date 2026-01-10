import streamlit as st
import pandas as pd

PROC = "Dataset/processed"
FC = f"{PROC}/forecast"


@st.cache_data
def load_forecast():
    df_future = pd.read_parquet(f"{FC}/future_forecast.parquet")
    return df_future


def ranking_page():
    st.title("🔮 Mobility Hotspot Forecast (Top Districts +3 Month)")

    df = load_forecast()

    # -------------------------
    # Sidebar filters
    # -------------------------
    state_list = ["All India"] + sorted(df['state'].unique())
    sel_state = st.selectbox("Select State (Optional):", state_list)

    scale = st.radio(
        "Scale:",
        ["Absolute", "Per Capita"],
        horizontal=True
    )

    # Filter by state if selected
    if sel_state != "All India":
        df = df[df['state'] == sel_state]

    # -------------------------
    # Prepare metrics
    # -------------------------
    if scale == "Absolute":
        df['metric_mov'] = df['pred_mov_3m']
        df['metric_std'] = df['pred_std_3m']
    else:
        df['metric_mov'] = df['pred_mov_3m'] / df['pop_adult'].replace(0,1)
        df['metric_std'] = df['pred_std_3m'] / df['pop_adult'].replace(0,1)

    # -------------------------
    # Ranking logic
    # -------------------------
    df_mov = df.sort_values('metric_mov', ascending=False).head(10)
    df_std = df.sort_values('metric_std', ascending=False).head(10)

    # -------------------------
    # Display Tabs
    # -------------------------
    tabs = st.tabs([
        "🚚 Movement Migration Hotspots",
        "🎓 Student Mobility Hotspots"
    ])

    with tabs[0]:
        st.subheader("Top Districts Forecasted for Movement Growth (+3m)")
        st.dataframe(
            df_mov[['state','district','metric_mov','pred_mov_3m','pop_adult']].reset_index(drop=True)
        )

    with tabs[1]:
        st.subheader("Top Districts Forecasted for Student Mobility (+3m)")
        st.dataframe(
            df_std[['state','district','metric_std','pred_std_3m','pop_adult']].reset_index(drop=True)
        )


if __name__ == "__main__":
    ranking_page()
