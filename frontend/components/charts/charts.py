"""
EquiLens AI – Plotly Financial Charts Component
===============================================
Generates interactive, publication-quality Plotly figures with dark terminal styling.
"""

import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Any, Optional
import pandas as pd

# Standard Plotly dark layout template
DARK_THEME_LAYOUT = dict(
    paper_bgcolor="#111827",
    plot_bgcolor="#0b0f19",
    font=dict(color="#9ca3af", family="system-ui, sans-serif", size=12),
    xaxis=dict(gridcolor="#1f2937", zerolinecolor="#374151"),
    yaxis=dict(gridcolor="#1f2937", zerolinecolor="#374151"),
    margin=dict(l=40, r=40, t=40, b=40),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)


def create_price_candlestick_chart(df: pd.DataFrame, company_name: str = "") -> go.Figure:
    fig = go.Figure()
    if df.empty or "close" not in df.columns:
        fig.add_annotation(text="No Price History Available", showarrow=False, font=dict(color="#9ca3af", size=14))
        fig.update_layout(**DARK_THEME_LAYOUT)
        return fig

    # Check for OHLC
    if all(col in df.columns for col in ["open", "high", "low", "close"]):
        fig.add_trace(
            go.Candlestick(
                x=df["date"],
                open=df["open"],
                high=df["high"],
                low=df["low"],
                close=df["close"],
                name="OHLC",
                increasing_line_color="#10b981",
                decreasing_line_color="#f43f5e",
            )
        )
    else:
        fig.add_trace(
            go.Scatter(
                x=df["date"],
                y=df["close"],
                mode="lines",
                line=dict(color="#38bdf8", width=2),
                name="Close Price",
            )
        )

    fig.update_layout(
        **DARK_THEME_LAYOUT,
        title=f"{company_name} Price Action",
        xaxis_title="Date",
        yaxis_title="Price (₹)",
        xaxis_rangeslider_visible=False,
    )
    return fig


def create_revenue_ebitda_trend_chart(metrics: List[Dict[str, Any]]) -> go.Figure:
    fig = go.Figure()
    if not metrics:
        fig.add_annotation(text="No Financial Performance Data", showarrow=False, font=dict(color="#9ca3af", size=14))
        fig.update_layout(**DARK_THEME_LAYOUT)
        return fig

    df = pd.DataFrame(metrics)
    # Sort by financial_year
    if "financial_year" in df.columns:
        df = df.sort_values(by="financial_year")
        x_axis = df["financial_year"]
    elif "period_end" in df.columns:
        df = df.sort_values(by="period_end")
        x_axis = df["period_end"]
    else:
        x_axis = list(range(len(df)))

    if "revenue" in df.columns:
        fig.add_trace(go.Bar(x=x_axis, y=df["revenue"], name="Revenue (₹ Cr)", marker_color="#3b82f6"))
    if "ebitda" in df.columns:
        fig.add_trace(go.Bar(x=x_axis, y=df["ebitda"], name="EBITDA (₹ Cr)", marker_color="#10b981"))
    if "net_profit" in df.columns:
        fig.add_trace(go.Bar(x=x_axis, y=df["net_profit"], name="PAT (₹ Cr)", marker_color="#818cf8"))

    fig.update_layout(
        **DARK_THEME_LAYOUT,
        barmode="group",
        title="Revenue, EBITDA & PAT Multi-Year Trend",
        xaxis_title="Reporting Period",
        yaxis_title="₹ Crores",
    )
    return fig


def create_forecast_fan_chart(
    historical_dates: List[str],
    historical_values: List[float],
    forecast_dates: List[str],
    base_case: List[float],
    bull_case: List[float],
    bear_case: List[float],
    metric_label: str = "Revenue (₹ Cr)",
) -> go.Figure:
    fig = go.Figure()

    # Historical Line
    if historical_dates and historical_values:
        fig.add_trace(
            go.Scatter(
                x=historical_dates,
                y=historical_values,
                mode="lines+markers",
                name="Historical",
                line=dict(color="#38bdf8", width=3),
                marker=dict(size=6),
            )
        )
        # Connect last historical to first forecast
        conn_x = [historical_dates[-1], forecast_dates[0]]
        conn_base = [historical_values[-1], base_case[0]]
        fig.add_trace(
            go.Scatter(
                x=conn_x,
                y=conn_base,
                mode="lines",
                showlegend=False,
                line=dict(color="#3b82f6", width=2, dash="dot"),
            )
        )

    # Bull Case (Upper Bound)
    fig.add_trace(
        go.Scatter(
            x=forecast_dates,
            y=bull_case,
            mode="lines",
            name="Bull Case (+1σ)",
            line=dict(color="#10b981", width=2, dash="dash"),
        )
    )

    # Base Case (Central Forecast)
    fig.add_trace(
        go.Scatter(
            x=forecast_dates,
            y=base_case,
            mode="lines+markers",
            name="Base Forecast",
            line=dict(color="#3b82f6", width=3),
            marker=dict(size=7),
        )
    )

    # Bear Case (Lower Bound) & Area Fill
    fig.add_trace(
        go.Scatter(
            x=forecast_dates,
            y=bear_case,
            mode="lines",
            name="Bear Case (-1σ)",
            line=dict(color="#f43f5e", width=2, dash="dash"),
            fill="tonexty",
            fillcolor="rgba(59, 130, 246, 0.12)",
        )
    )

    fig.update_layout(
        **DARK_THEME_LAYOUT,
        title=f"Econometric Forecast Trajectory & Scenario Bands: {metric_label}",
        xaxis_title="Period",
        yaxis_title=metric_label,
    )
    return fig


def create_sentiment_donut_chart(sentiment_counts: Dict[str, int]) -> go.Figure:
    labels = list(sentiment_counts.keys())
    values = list(sentiment_counts.values())
    colors = {
        "Positive": "#10b981",
        "Neutral": "#64748b",
        "Negative": "#f43f5e",
    }
    marker_colors = [colors.get(lbl, "#38bdf8") for lbl in labels]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.55,
                marker=dict(colors=marker_colors),
                textinfo="label+percent",
            )
        ]
    )
    fig.update_layout(
        **DARK_THEME_LAYOUT,
        title="Market News Sentiment Distribution",
        showlegend=False,
    )
    return fig

