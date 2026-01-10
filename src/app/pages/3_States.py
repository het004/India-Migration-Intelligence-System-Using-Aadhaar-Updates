import streamlit as st
import pandas as pd
import plotly.graph_objects as go

PROC = "Dataset/processed"
FC = f"{PROC}/forecast"


@st.cache_data
def load_data():
    df_month = pd.read_parquet(f"{PROC}/monthly.parquet")
    df_future = pd.read_parquet(f"{FC}/future_forecast.parquet")
    return df_month, df_future


def states_page():
    st.title("🌍 State-Level Mobility Comparison")

    df_month, df_future = load_data()

    # -------------------------
    # User controls
    # -------------------------
    metric = st.radio(
        "Metric:",
        ["Movement", "Student Mobility"],
        horizontal=True
    )

    scale = st.radio(
        "Scale:",
        ["Absolute", "Per Capita"],
        horizontal=True
    )

    states = sorted(df_month['state'].unique())
    selected_states = st.multiselect(
        "Select States for Comparison:",
        states,
        default=states[:4]  # pick first 4 as default
    )

    if not selected_states:
        st.warning("Please select at least one state.")
        return

    # -------------------------
    # State mean time-series
    # -------------------------
    df_series = df_month[df_month['state'].isin(selected_states)]
    grp = df_series.groupby(['state','month_index']).agg({
        'movement_index':'mean',
        'student_ratio':'mean',
        'pop_adult':'mean'
    }).reset_index()

    # -------------------------
    # Future forecast snapshot
    # -------------------------
    df_snap = df_future[df_future['state'].isin(selected_states)].copy()

    if scale == "Absolute":
        df_snap['metric_mov'] = df_snap['pred_mov_3m']
        df_snap['metric_std'] = df_snap['pred_std_3m']
    else:
        df_snap['metric_mov'] = df_snap['pred_mov_3m'] / df_snap['pop_adult'].replace(0,1)
        df_snap['metric_std'] = df_snap['pred_std_3m'] / df_snap['pop_adult'].replace(0,1)

    # -------------------------
    # Tabs
    # -------------------------
    tab1, tab2 = st.tabs([
        "📈 Time-Series (State Mean)",
        "📊 Future Snapshot (Ranking)"
    ])

    # -------------------------
    # Tab-1 Time Series Plot
    # -------------------------
    with tab1:
        title = "State Mean Movement" if metric=="Movement" else "State Mean Student Mobility"
        fig = go.Figure()

        for stt in selected_states:
            d = grp[grp['state']==stt]
            if metric == "Movement":
                y = d['movement_index']
                if scale == "Per Capita":
                    y = y / d['pop_adult'].replace(0,1)
            else:
                y = d['student_ratio']

            fig.add_trace(go.Scatter(
                x=d['month_index'],
                y=y,
                mode='lines+markers',
                name=stt
            ))

        fig.update_layout(
            title=title,
            xaxis_title="Month Index (2025)",
            height=550,
            template="plotly_white",
            legend=dict(orientation="h")
        )

        st.plotly_chart(fig, use_container_width=True)

    # -------------------------
    # Tab-2 Snapshot Ranking
    # -------------------------
    with tab2:
        st.subheader("State-Level Snapshot (+3 month forecast)")

        if metric=="Movement":
            df_rank = df_snap.groupby('state')['metric_mov'].mean().reset_index()
            df_rank = df_rank.sort_values('metric_mov', ascending=False)
            df_rank.columns = ['State','Movement Forecast (+3m)']
        else:
            df_rank = df_snap.groupby('state')['metric_std'].mean().reset_index()
            df_rank = df_rank.sort_values('metric_std', ascending=False)
            df_rank.columns = ['State','Student Mobility Forecast (+3m)']

        st.dataframe(df_rank.reset_index(drop=True))


if __name__ == "__main__":
    states_page()
