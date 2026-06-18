"""
SpaceX Falcon 9 Landing Prediction — Interactive Dashboard
===========================================================
Run:  python dashboard.py
Open: http://127.0.0.1:8050
"""

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# ── Data ──────────────────────────────────────────────────────────────────────
df = pd.read_csv("spacex_launch_dash.csv")

# Derived columns
df["Result"] = df["class"].map({0: "Failure", 1: "Success"})

payload_min = int(df["Payload Mass (kg)"].min())
payload_max = int(df["Payload Mass (kg)"].max())

# Dropdown options
site_options = [{"label": "All Launch Sites", "value": "ALL"}] + [
    {"label": site, "value": site}
    for site in sorted(df["Launch Site"].unique())
]

# Colour palette
PALETTE = {
    "Success": "#4C9BE8",
    "Failure": "#E8694C",
}

PIE_COLORS = ["#4C9BE8", "#E8694C", "#F0B429", "#68D391"]

# ── App ───────────────────────────────────────────────────────────────────────
app = Dash(__name__, title="SpaceX Dashboard")

app.layout = html.Div(
    style={"fontFamily": "Segoe UI, Arial, sans-serif", "maxWidth": "1100px",
           "margin": "0 auto", "padding": "20px"},
    children=[
        # Header
        html.H1(
            "🚀 SpaceX Falcon 9 Launch Dashboard",
            style={"textAlign": "center", "color": "#1a3a5c", "marginBottom": "4px"},
        ),
        html.P(
            "Explore launch outcomes, payload ranges, and booster performance across sites.",
            style={"textAlign": "center", "color": "#555", "marginBottom": "24px"},
        ),

        # ── Controls ──
        html.Div(
            style={"display": "flex", "gap": "40px", "alignItems": "flex-start",
                   "flexWrap": "wrap", "marginBottom": "24px"},
            children=[
                html.Div(
                    style={"flex": "1", "minWidth": "260px"},
                    children=[
                        html.Label("Launch Site", style={"fontWeight": "bold"}),
                        dcc.Dropdown(
                            id="site-filter",
                            options=site_options,
                            value="ALL",
                            clearable=False,
                            style={"marginTop": "6px"},
                        ),
                    ],
                ),
                html.Div(
                    style={"flex": "2", "minWidth": "300px"},
                    children=[
                        html.Label("Payload Mass Range (kg)",
                                   style={"fontWeight": "bold"}),
                        dcc.RangeSlider(
                            id="payload-filter",
                            min=0,
                            max=10000,
                            step=500,
                            marks={i: f"{i:,}" for i in range(0, 11000, 2500)},
                            value=[payload_min, payload_max],
                            tooltip={"placement": "bottom", "always_visible": True},
                        ),
                    ],
                ),
            ],
        ),

        # ── Charts row ──
        html.Div(
            style={"display": "flex", "gap": "24px", "flexWrap": "wrap"},
            children=[
                html.Div(
                    style={"flex": "1", "minWidth": "320px",
                           "background": "#f9f9f9", "borderRadius": "10px",
                           "padding": "12px", "boxShadow": "0 1px 4px rgba(0,0,0,.1)"},
                    children=[dcc.Graph(id="pie-chart", config={"displayModeBar": False})],
                ),
                html.Div(
                    style={"flex": "2", "minWidth": "420px",
                           "background": "#f9f9f9", "borderRadius": "10px",
                           "padding": "12px", "boxShadow": "0 1px 4px rgba(0,0,0,.1)"},
                    children=[dcc.Graph(id="scatter-chart")],
                ),
            ],
        ),

        # Footer
        html.P(
            "Data: SpaceX API & IBM Skills Network  •  Coursera Applied Data Science Capstone",
            style={"textAlign": "center", "color": "#aaa", "marginTop": "32px",
                   "fontSize": "12px"},
        ),
    ],
)


# ── Callbacks ─────────────────────────────────────────────────────────────────

@app.callback(
    Output("pie-chart", "figure"),
    Input("site-filter", "value"),
)
def update_pie(selected_site):
    if selected_site == "ALL":
        successes = df[df["class"] == 1]
        fig = px.pie(
            successes,
            names="Launch Site",
            title="Successful Launches by Site",
            color_discrete_sequence=PIE_COLORS,
            hole=0.35,
        )
        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            marker=dict(line=dict(color="#fff", width=2)),
            hovertemplate="%{label}<br>Launches: %{value}<extra></extra>",
        )
    else:
        site_df = df[df["Launch Site"] == selected_site]
        counts = site_df["Result"].value_counts().reset_index()
        counts.columns = ["Result", "Count"]
        fig = px.pie(
            counts,
            names="Result",
            values="Count",
            title=f"Outcome Distribution — {selected_site}",
            color="Result",
            color_discrete_map=PALETTE,
            hole=0.35,
        )
        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            marker=dict(line=dict(color="#fff", width=2)),
            hovertemplate="%{label}: %{value}<extra></extra>",
        )

    fig.update_layout(
        margin=dict(t=50, b=10, l=10, r=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


@app.callback(
    Output("scatter-chart", "figure"),
    Input("site-filter", "value"),
    Input("payload-filter", "value"),
)
def update_scatter(selected_site, payload_range):
    lo, hi = payload_range
    filtered = df[df["Payload Mass (kg)"].between(lo, hi)]

    if selected_site != "ALL":
        filtered = filtered[filtered["Launch Site"] == selected_site]

    site_label = "All Sites" if selected_site == "ALL" else selected_site

    fig = px.scatter(
        filtered,
        x="Payload Mass (kg)",
        y="class",
        color="Booster Version Category",
        symbol="Result",
        symbol_map={"Success": "circle", "Failure": "x"},
        opacity=0.75,
        title=f"Payload vs Landing Outcome — {site_label}",
        labels={"class": "Landed (1=Yes, 0=No)"},
        hover_data=["Launch Site", "Result", "Booster Version Category"],
    )
    fig.update_layout(
        yaxis=dict(tickvals=[0, 1], ticktext=["Failure", "Success"]),
        legend=dict(title="Booster"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=50, b=10, l=10, r=10),
    )
    fig.update_xaxes(showgrid=True, gridcolor="#e0e0e0")
    fig.update_yaxes(showgrid=True, gridcolor="#e0e0e0")
    return fig


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)
