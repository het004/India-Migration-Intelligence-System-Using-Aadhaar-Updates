import streamlit as st
import pandas as pd
import plotly.graph_objects as go

PROC = "Dataset/processed"
FC = f"{PROC}/forecast"


@st.cache_data
def load_data():
    df_month = pd.read_parquet(f"{PROC}/monthly.parquet")
    df_hist = pd.read_parquet(f"{FC}/historical_predictions.parquet")
    df_future = pd.read_parquet(f"{FC}/future_forecast.parquet")
    return df_month, df_hist, df_future


def explorer():
    st.title("📍 District Mobility Explorer")

    df_month, df_hist, df_future = load_data()

    # -------------------------
    # Sidebar controls
    # -------------------------
    states = sorted(df_month['state'].unique())
    state = st.selectbox("Select State:", states)

    districts = sorted(df_month[df_month['state']==state]['district'].unique())
    district = st.selectbox("Select District:", districts)

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

    # -------------------------
    # Filter district + compute state mean
    # -------------------------
    d1 = df_hist[(df_hist['state']==state) & (df_hist['district']==district)]
    d2 = df_month[df_month['state']==state]

    # State mean by month_index
    state_grp = d2.groupby('month_index').agg({
        'movement_index':'mean',
        'student_ratio':'mean',
        'pop_adult':'mean'
    }).reset_index()

    # -------------------------
    # Future predictions for district
    # -------------------------
    df_fut = df_future[(df_future['state']==state) & (df_future['district']==district)]

    # -------------------------
    # Build time series traces
    # -------------------------
    fig = go.Figure()

    # District Actual + Predicted
    if metric == "Movement":
        y_true = d1['movement_index']
        y_pred = d1['pred_mov']
        y_future = df_fut['pred_mov_3m']
        title = "Movement Index (+3 month forecast)"

        if scale == "Per Capita":
            y_true = d1['movement_index'] / d1['pop_adult'].replace(0,1)
            y_pred = d1['pred_mov'] / d1['pop_adult'].replace(0,1)
            y_future = df_fut['pred_mov_3m'] / df_fut['pop_adult'].replace(0,1)

        # actual
        fig.add_trace(go.Scatter(
            x=d1['month_index'], y=y_true,
            mode='lines+markers',
            name=f"{district} (Actual)"
        ))

        # predicted (historical)
        fig.add_trace(go.Scatter(
            x=d1['month_index'], y=y_pred,
            mode='lines+markers',
            name=f"{district} (Predicted)"
        ))

        # forecast future
        fig.add_trace(go.Scatter(
            x=df_fut['month_index'] + 3,
            y=y_future,
            mode='markers',
            marker=dict(size=10, symbol='diamond'),
            name=f"{district} (Forecast +3m)"
        ))

    else:  # Student Mobility
        y_true = d1['student_ratio']
        y_pred = d1['pred_std']
        y_future = df_fut['pred_std_3m']
        title = "Student Mobility Ratio (+3 month forecast)"

        # absolute vs per-capita irrelevant for ratio, so no transformation

        fig.add_trace(go.Scatter(
            x=d1['month_index'], y=y_true,
            mode='lines+markers',
            name=f"{district} (Actual)"
        ))

        fig.add_trace(go.Scatter(
            x=d1['month_index'], y=y_pred,
            mode='lines+markers',
            name=f"{district} (Predicted)"
        ))

        fig.add_trace(go.Scatter(
            x=df_fut['month_index'] + 3,
            y=y_future,
            mode='markers',
            marker=dict(size=10, symbol='diamond'),
            name=f"{district} (Forecast +3m)"
        ))

    # -------------------------
    # Add State Mean Comparison
    # -------------------------
    if metric == "Movement":
        y_state = state_grp['movement_index']
        if scale == "Per Capita":
            y_state = y_state / state_grp['pop_adult'].replace(0,1)

        fig.add_trace(go.Scatter(
            x=state_grp['month_index'], y=y_state,
            mode='lines',
            line=dict(dash='dash'),
            name=f"{state} (State Mean)"
        ))
    else:
        fig.add_trace(go.Scatter(
            x=state_grp['month_index'], y=state_grp['student_ratio'],
            mode='lines',
            line=dict(dash='dash'),
            name=f"{state} (State Mean)"
        ))

    fig.update_layout(
        title=title,
        xaxis_title="Month Index (2025)",
        height=550,
        template="plotly_white",
        legend=dict(orientation="h")
    )

    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    explorer()
