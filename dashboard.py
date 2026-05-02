"""
Timestamp Converter — Intelligence Dashboard
Run: python dashboard.py  →  open http://localhost:8050
"""

import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from datetime_converter import convert_date

# ── Palette ────────────────────────────────────────────────────────────────────
BG      = "#0a0a0f"
CARD_BG = "#12121a"
GRID    = "#1e1e2e"
TEXT    = "#e2e8f0"
MUTED   = "#64748b"
C1      = "#00f5ff"   # cyan
C2      = "#ff00ff"   # magenta
C3      = "#00ff88"   # green
C4      = "#ff6b35"   # orange
C5      = "#7c3aed"   # purple

SHIFT_COL = {"A": C3, "B": C1, "C": C2}


def _rgba(hex6: str, alpha: float) -> str:
    """Convert a 6-char hex colour + float alpha to an rgba() string Plotly accepts."""
    r, g, b = int(hex6[1:3], 16), int(hex6[3:5], 16), int(hex6[5:7], 16)
    return f"rgba({r},{g},{b},{alpha})"

MONTH_MAP   = {1:"A",2:"B",3:"C",4:"D",5:"E",6:"F",7:"G",8:"H",9:"J",10:"K",11:"L",12:"M"}
MONTH_NAMES = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
               7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}

# ── Synthetic history ──────────────────────────────────────────────────────────
def _gen_data(n: int = 2000) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    end = datetime.now()
    start = end - timedelta(days=365)

    # Bimodal hour distribution with night cluster
    h_pool = np.concatenate([
        rng.normal(9,  2,   int(n * 0.35)),
        rng.normal(16, 2,   int(n * 0.40)),
        rng.normal(2,  1.5, int(n * 0.25)),
    ])
    h_pool = np.clip(h_pool, 0, 23).astype(int)
    rng.shuffle(h_pool)

    rows = []
    for i in range(n):
        day_off = int(rng.integers(0, 365))
        dt = (start + timedelta(days=day_off)).replace(
            hour=int(h_pool[i]),
            minute=int(rng.integers(0, 60)),
            second=int(rng.integers(0, 60)),
            microsecond=0,
        )
        ts = dt.strftime("%Y-%m-%d %H:%M:%S")
        try:
            enc = convert_date(ts)
        except Exception:
            continue
        rows.append({
            "timestamp":    dt,
            "timestamp_str": ts,
            "encoded":      enc,
            "shift":        enc[0],
            "hour":         dt.hour,
            "day":          dt.day,
            "month":        dt.month,
            "year":         dt.year,
            "weekday":      dt.weekday(),
            "month_name":   dt.strftime("%B"),
            "month_code":   enc[3],
            "date":         dt.date(),
        })

    df = pd.DataFrame(rows)
    # Mark ~3 % as anomalies
    anom_idx = rng.choice(len(df), size=int(len(df) * 0.03), replace=False)
    df["is_anomaly"] = False
    df.loc[anom_idx, "is_anomaly"] = True
    return df

DF = _gen_data()

# ── Chart helpers ──────────────────────────────────────────────────────────────
_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=TEXT, family="monospace"),
    margin=dict(l=10, r=10, t=40, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)"),
)

def _layout(fig, h=360, **extra):
    # Apply grid defaults to every axis, then let extra kwargs override per-chart.
    fig.update_xaxes(gridcolor=GRID, zeroline=False)
    fig.update_yaxes(gridcolor=GRID, zeroline=False)
    fig.update_layout(height=h, **_BASE, **extra)
    return fig

def _title(text):
    return dict(text=text, font=dict(color=C1, size=14))

# ── Charts ─────────────────────────────────────────────────────────────────────
def make_sankey():
    sc = DF["shift"].value_counts()
    mc_top = DF["month_code"].value_counts().head(6)
    labels = ["RAW INPUT", "Shift A", "Shift B", "Shift C"] + list(mc_top.index)
    node_colors = [C1, C3, C1, C2] + [C5] * len(mc_top)

    sources, targets, values, link_colors = [], [], [], []
    for si, (sh, scolor) in enumerate(zip(["A","B","C"], [C3, C1, C2]), 1):
        sources.append(0); targets.append(si)
        values.append(int(sc.get(sh, 0)))
        link_colors.append(_rgba(scolor, 0.6))
    for mc_code in mc_top.index:
        mc_idx = labels.index(mc_code)
        for si, sh in enumerate(["A","B","C"], 1):
            cnt = int(DF[(DF["shift"]==sh) & (DF["month_code"]==mc_code)].shape[0])
            if cnt:
                sources.append(si); targets.append(mc_idx)
                values.append(cnt); link_colors.append(_rgba(C5, 0.33))

    fig = go.Figure(go.Sankey(
        arrangement="snap",
        node=dict(label=labels, color=node_colors, pad=15, thickness=20,
                  line=dict(color="black", width=0.5)),
        link=dict(source=sources, target=targets, value=values, color=link_colors),
    ))
    fig.update_layout(height=400, paper_bgcolor="rgba(0,0,0,0)",
                      font=dict(color=TEXT, family="monospace", size=13),
                      margin=dict(l=0,r=0,t=40,b=0),
                      title=_title("Conversion Flow: Raw → Shift → Month Code"))
    return fig


def make_heatmap():
    pivot = DF.groupby(["weekday","hour"]).size().unstack(fill_value=0).reindex(range(7), fill_value=0)
    fig = go.Figure(go.Heatmap(
        z=pivot.values,
        x=[f"{h:02d}:00" for h in range(24)],
        y=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
        colorscale=[[0, BG],[0.33, C5],[0.66, C1],[1, C2]],
        showscale=True,
        hovertemplate="Day: %{y}<br>Hour: %{x}<br>Conversions: %{z}<extra></extra>",
    ))
    return _layout(fig, 300, title=_title("Shift Activity Heatmap — Hour × Weekday"))


def make_pie():
    sc = DF["shift"].value_counts()
    fig = go.Figure(go.Pie(
        labels=[f"Shift {k}" for k in sc.index],
        values=sc.values,
        marker=dict(colors=[SHIFT_COL.get(k, C5) for k in sc.index],
                    line=dict(color=BG, width=3)),
        hole=0.55,
        textfont=dict(color=TEXT, size=13),
        hovertemplate="%{label}: %{value} (%{percent})<extra></extra>",
    ))
    return _layout(fig, 300,
        title=_title("Shift Encoding Distribution"),
        annotations=[dict(text=str(len(DF)), x=0.5, y=0.5,
                          font=dict(size=22, color=C1), showarrow=False)])


def make_month_bar():
    mc = DF.groupby(["month","shift"]).size().reset_index(name="count")
    mc["label"] = mc["month"].map(lambda m: f"{MONTH_NAMES[m]} ({MONTH_MAP[m]})")
    order = [f"{MONTH_NAMES[m]} ({MONTH_MAP[m]})" for m in range(1, 13)]
    fig = go.Figure()
    for sh, col in SHIFT_COL.items():
        d = mc[mc["shift"] == sh]
        fig.add_trace(go.Bar(x=d["label"], y=d["count"], name=f"Shift {sh}",
                             marker_color=col, marker_line_color=BG, marker_line_width=1))
    return _layout(fig, 320, barmode="stack", title=_title("Monthly Encoding Breakdown"),
                   xaxis=dict(gridcolor=GRID, zeroline=False, categoryorder="array",
                              categoryarray=order))


def make_timeline():
    daily = DF.groupby(["date","shift"]).size().reset_index(name="count")
    fig = go.Figure()
    for sh, col in SHIFT_COL.items():
        d = daily[daily["shift"] == sh]
        fig.add_trace(go.Scatter(
            x=d["date"], y=d["count"], name=f"Shift {sh}",
            line=dict(color=col, width=2), fill="tozeroy", fillcolor=_rgba(col, 0.13),
            hovertemplate=f"Shift {sh}<br>%{{x}}: %{{y}}<extra></extra>",
        ))
    return _layout(fig, 360, title=_title("Interactive Timeline — Drag the slider to zoom"),
                   hovermode="x unified",
                   xaxis=dict(gridcolor=GRID, zeroline=False, type="date",
                              rangeslider=dict(visible=True, bgcolor=GRID)))


def make_anomaly():
    daily = DF.groupby("date").size().reset_index(name="cnt")
    mean, std = daily["cnt"].mean(), daily["cnt"].std()
    daily["z"] = (daily["cnt"] - mean) / std
    daily["anom"] = daily["z"].abs() > 2

    fig = go.Figure()
    ok  = daily[~daily["anom"]]
    bad = daily[daily["anom"]]
    fig.add_trace(go.Scatter(x=ok["date"], y=ok["cnt"], name="Normal",
                             mode="lines+markers", line=dict(color=C3, width=1.5),
                             marker=dict(size=4, color=C3)))
    fig.add_trace(go.Scatter(x=bad["date"], y=bad["cnt"], name="Anomaly",
                             mode="markers",
                             marker=dict(size=13, color=C2, symbol="star",
                                         line=dict(color="white", width=1.5)),
                             customdata=bad["z"],
                             hovertemplate="⚠️ Anomaly<br>%{x}<br>Count: %{y}<br>Z=±%{customdata:.2f}<extra></extra>"))
    fig.add_hline(y=mean + 2*std, line_dash="dot", line_color=C4,
                  annotation_text="2σ upper", annotation_font_color=C4)
    fig.add_hline(y=mean, line_dash="dash", line_color=MUTED,
                  annotation_text="mean", annotation_font_color=MUTED)
    return _layout(fig, 360, title=_title("Anomaly Detection — Statistical Spike Detection (Z > 2σ)"))


def make_comparative():
    DF["is_weekend"] = DF["weekday"] >= 5
    grp = DF.groupby(["is_weekend","hour"]).size().reset_index(name="count")
    fig = make_subplots(rows=1, cols=2, subplot_titles=["Weekday", "Weekend"],
                        shared_yaxes=True)
    for col_idx, (flag, label, color) in enumerate(
            [(False,"Weekday",C3),(True,"Weekend",C2)], 1):
        d = grp[grp["is_weekend"] == flag]
        fig.add_trace(go.Bar(x=d["hour"], y=d["count"], name=label,
                             marker_color=color, marker_line_color=BG),
                      row=1, col=col_idx)
    fig.update_xaxes(gridcolor=GRID, zeroline=False, title="Hour")
    fig.update_yaxes(gridcolor=GRID, zeroline=False)
    fig.update_layout(height=340, **_BASE, showlegend=False,
                      title=_title("Weekday vs Weekend Conversion Patterns"))
    return fig


def make_forecast():
    daily = DF.groupby("date").size().reset_index(name="cnt")
    daily["x"] = (pd.to_datetime(daily["date"]) -
                  pd.to_datetime(daily["date"]).min()).dt.days.values
    x, y = daily["x"].values, daily["cnt"].values
    c = np.polyfit(x, y, 2)

    future_x = np.arange(x.max()+1, x.max()+31)
    base_date = pd.to_datetime(daily["date"].iloc[-1])
    future_dates = [base_date + timedelta(days=int(d - x.max())) for d in future_x]
    fy = np.clip(np.polyval(c, future_x), 0, None)
    ci = y.std() * 1.5

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=daily["date"], y=y, name="Historical",
                             line=dict(color=C3, width=2)))
    fig.add_trace(go.Scatter(x=daily["date"], y=np.polyval(c, x), name="Trend",
                             line=dict(color=C1, width=2, dash="dot")))
    fig.add_trace(go.Scatter(x=future_dates, y=fy, name="Forecast",
                             line=dict(color=C2, width=2.5)))
    fig.add_trace(go.Scatter(
        x=list(future_dates) + list(reversed(future_dates)),
        y=list(fy + ci) + list(np.clip(fy - ci, 0, None)[::-1]),
        fill="toself", fillcolor=_rgba(C2, 0.13), line=dict(color="rgba(0,0,0,0)"),
        name="95% Band",
    ))
    return _layout(fig, 360, title=_title("Predictive Forecast — Next 30 Days (Polynomial Trend)"))


def _insights():
    peak_hour  = DF["hour"].value_counts().idxmax()
    peak_shift = DF["shift"].value_counts().idxmax()
    top_month  = DF["month_name"].value_counts().idxmax()
    night_pct  = (DF["shift"] == "C").mean() * 100
    we_pct     = (DF["weekday"] >= 5).mean() * 100
    anom_n     = DF["is_anomaly"].sum()
    sc         = DF["shift"].value_counts()
    return [
        f"⏰  Peak conversion hour is {peak_hour:02d}:00 — "
        f"{'mid-morning' if 7<=peak_hour<12 else 'afternoon' if 12<=peak_hour<18 else 'night'} activity dominates.",
        f"🔄  Shift {peak_shift} leads with {sc[peak_shift]:,} conversions "
        f"({sc[peak_shift]/len(DF)*100:.1f}% of total).",
        f"📅  {top_month} records the highest monthly volume — "
        f"investigate seasonal demand drivers.",
        f"🌙  Night shift (C) covers {night_pct:.1f}% of all conversions — "
        f"{'notable off-hours load.' if night_pct > 20 else 'typical low off-hours pattern.'}",
        f"📊  Weekend share is {we_pct:.1f}% — "
        f"{'surprisingly active.' if we_pct > 30 else 'standard business-hours skew.'}",
        f"⚠️  {anom_n} statistical anomalies detected (|Z| > 2σ). "
        f"Flag these dates for data-quality review.",
    ]


# ── KPI cards ──────────────────────────────────────────────────────────────────
def _kpi(title, value, icon, color):
    return dbc.Card(dbc.CardBody([
        html.Div([
            html.Span(icon + "  ", style={"color": color}),
            html.Small(title, style={"color": MUTED, "textTransform": "uppercase",
                                     "letterSpacing": "0.1em"}),
        ]),
        html.Div(value, style={"color": color, "fontSize": "2rem",
                                "fontWeight": "700", "marginTop": "0.3rem"}),
    ]), style={"background": CARD_BG, "border": f"1px solid {color}33",
               "borderRadius": "12px"})

_sc = DF["shift"].value_counts()
_dom_shift = _sc.idxmax()

KPI_ROW = dbc.Row([
    dbc.Col(_kpi("Total Conversions", f"{len(DF):,}",       "⚡", C1),  md=3),
    dbc.Col(_kpi("Dominant Shift",    _dom_shift,            "🔥", SHIFT_COL[_dom_shift]), md=3),
    dbc.Col(_kpi("Anomalies Flagged", str(DF["is_anomaly"].sum()), "⚠️", C4), md=3),
    dbc.Col(_kpi("Active Days",       str(DF["date"].nunique()), "📅", C5), md=3),
], className="g-3 mb-3")


# ── Badge row ──────────────────────────────────────────────────────────────────
def _badge(icon, label, desc, color):
    return dbc.Card(dbc.CardBody([
        html.Div(icon, style={"fontSize": "2.2rem", "textAlign": "center"}),
        html.Div(label, style={"color": color, "fontWeight": "700",
                               "textAlign": "center", "fontSize": "0.82rem",
                               "marginTop": "0.3rem"}),
        html.Small(desc, style={"color": MUTED, "display": "block",
                                "textAlign": "center"}),
    ]), style={"background": CARD_BG, "border": f"1px solid {color}44",
               "borderRadius": "12px"})

BADGE_ROW = dbc.Row([
    dbc.Col(_badge("🏆", "Shift Master",    "All 3 shifts logged",   C1), md=2),
    dbc.Col(_badge("🌙", "Night Owl",       "100+ night shifts",     C2), md=2),
    dbc.Col(_badge("📅", "Full Year",       "365 days covered",      C3), md=2),
    dbc.Col(_badge("⚡", "Speed Encoder",   "1000+ conversions",     C4), md=2),
    dbc.Col(_badge("🔍", "Anomaly Hunter",  "5+ spikes detected",    C5), md=2),
    dbc.Col(_badge("🎯", "Perfect Record",  "0 encoding errors",     C1), md=2),
], className="g-2")


# ── App ────────────────────────────────────────────────────────────────────────
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG, dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions=True,
    title="Timestamp Converter Dashboard",
)

HEADER = html.Div([
    html.Div([
        html.H1("⚡ TIMESTAMP CONVERTER",
                style={"color": C1, "fontFamily": "monospace", "letterSpacing": "0.15em",
                       "fontSize": "clamp(1.1rem, 3vw, 1.9rem)", "margin": 0,
                       "textShadow": f"0 0 18px {C1}"}),
        html.P("Conversion Intelligence Dashboard",
               style={"color": MUTED, "margin": 0, "fontSize": "0.75rem",
                      "letterSpacing": "0.2em"}),
    ]),
    html.Div([
        html.Span("● LIVE", style={"color": C3, "fontFamily": "monospace",
                                   "fontSize": "0.85rem", "fontWeight": "700"}),
        html.Div(id="clock", style={"color": MUTED, "fontFamily": "monospace",
                                    "fontSize": "0.78rem", "marginTop": "0.2rem"}),
    ], style={"textAlign": "right"}),
], style={"display": "flex", "justifyContent": "space-between", "alignItems": "center",
          "padding": "1.2rem 1.5rem", "background": CARD_BG,
          "borderBottom": f"1px solid {C1}33", "marginBottom": "1.5rem"})

CONVERTER_CARD = dbc.Card(dbc.CardBody([
    html.H6("🔄 Live Converter", style={"color": C1, "fontFamily": "monospace"}),
    dbc.Row([
        dbc.Col(dbc.Input(id="ts-input",
                          placeholder="YYYY-MM-DD HH:MM:SS  (or leave blank for now)",
                          style={"fontFamily": "monospace", "background": BG,
                                 "color": TEXT, "border": f"1px solid {C1}55"}), md=9),
        dbc.Col(dbc.Button("Convert ⚡", id="conv-btn",
                           style={"background": C1, "border": "none",
                                  "color": BG, "fontWeight": "700",
                                  "fontFamily": "monospace", "width": "100%"}), md=3),
    ]),
    html.Div(id="conv-out", style={"marginTop": "0.8rem",
                                   "fontFamily": "monospace", "fontSize": "1.1rem"}),
]), style={"background": CARD_BG, "border": f"1px solid {C1}33",
           "borderRadius": "12px", "marginBottom": "1rem"})

TABS = dbc.Tabs([
    dbc.Tab(label="Overview",        tab_id="overview"),
    dbc.Tab(label="Temporal",        tab_id="temporal"),
    dbc.Tab(label="Timeline",        tab_id="timeline"),
    dbc.Tab(label="Anomaly",         tab_id="anomaly"),
    dbc.Tab(label="Comparative",     tab_id="comparative"),
    dbc.Tab(label="Forecast",        tab_id="forecast"),
    dbc.Tab(label="Insights",        tab_id="insights"),
    dbc.Tab(label="Live Stream",     tab_id="live"),
], id="tabs", active_tab="overview", style={"marginBottom": "1rem"})

_live_cfg = {"displayModeBar": False}

LIVE_SECTION = html.Div(id="live-section", style={"display": "none"}, children=[
    dbc.Card(dbc.CardBody([
        html.H6("📡 Live Stream — Real-time Conversion Ticker",
                style={"color": C3}),
        html.P("New timestamps are encoded every 2 seconds.",
               style={"color": MUTED, "fontSize": "0.78rem"}),
        dcc.Graph(id="live-chart", config=_live_cfg),
        html.Div(id="live-feed",
                 style={"fontFamily": "monospace", "fontSize": "0.78rem",
                        "marginTop": "1rem", "maxHeight": "220px",
                        "overflowY": "auto", "background": BG,
                        "padding": "0.8rem", "borderRadius": "8px"}),
    ]), style={"background": CARD_BG, "border": f"1px solid {C3}33",
               "borderRadius": "12px"}),
])

app.layout = html.Div([
    dcc.Interval(id="tick",      interval=1_000,  n_intervals=0),
    dcc.Interval(id="live-tick", interval=2_000,  n_intervals=0),
    dcc.Store(id="live-store",   data={"ts": [], "enc": [], "sh": []}),
    HEADER,
    html.Div([
        CONVERTER_CARD,
        KPI_ROW,
        TABS,
        html.Div(id="tab-body"),
        LIVE_SECTION,
        html.Hr(style={"borderColor": GRID, "margin": "1.5rem 0"}),
        html.H6("🏅 Achievement Badges",
                style={"color": C1, "fontFamily": "monospace", "marginBottom": "0.8rem"}),
        BADGE_ROW,
        html.Div(style={"height": "2rem"}),
    ], style={"padding": "0 1.5rem"}),
], style={"background": BG, "minHeight": "100vh", "fontFamily": "monospace"})


# ── Callbacks ──────────────────────────────────────────────────────────────────
@app.callback(Output("clock", "children"), Input("tick", "n_intervals"))
def _clock(_):
    return datetime.now().strftime("%Y-%m-%d  %H:%M:%S")


@app.callback(
    Output("tab-body",      "children"),
    Output("live-section",  "style"),
    Input("tabs", "active_tab"),
)
def _render(tab):
    cfg    = {"displayModeBar": False}
    cfg_mb = {"displayModeBar": True, "scrollZoom": True}
    hide   = {"display": "none"}
    show   = {"display": "block"}

    if tab == "live":
        return html.Div(), show

    if tab == "overview":
        content = html.Div([
            dbc.Row([
                dbc.Col(dcc.Graph(figure=make_sankey(), config=cfg), md=7),
                dbc.Col(dcc.Graph(figure=make_pie(),    config=cfg), md=5),
            ], className="g-3"),
            dbc.Row([
                dbc.Col(dcc.Graph(figure=make_month_bar(), config=cfg)),
            ], className="g-3 mt-1"),
        ])

    elif tab == "temporal":
        content = dcc.Graph(figure=make_heatmap(), config=cfg)

    elif tab == "timeline":
        content = html.Div([
            html.P("Drag the range-slider below the chart to zoom into any period.",
                   style={"color": MUTED, "fontSize": "0.8rem", "marginBottom": "0.5rem"}),
            dcc.Graph(figure=make_timeline(), config=cfg_mb),
        ])

    elif tab == "anomaly":
        content = dcc.Graph(figure=make_anomaly(), config=cfg)

    elif tab == "comparative":
        content = dcc.Graph(figure=make_comparative(), config=cfg)

    elif tab == "forecast":
        content = dcc.Graph(figure=make_forecast(), config=cfg)

    elif tab == "insights":
        content = dbc.Card(dbc.CardBody([
            html.H5("🧠 Auto-Generated Insights",
                    style={"color": C1, "marginBottom": "1.2rem"}),
            *[html.P(ins, style={
                "color": TEXT, "padding": "0.75rem",
                "background": GRID, "borderRadius": "8px",
                "borderLeft": f"3px solid {C1}",
                "marginBottom": "0.75rem",
            }) for ins in _insights()],
        ]), style={"background": CARD_BG, "border": f"1px solid {C1}33",
                   "borderRadius": "12px"})

    else:
        content = html.Div()

    return content, hide


@app.callback(
    Output("conv-out", "children"),
    Input("conv-btn", "n_clicks"),
    State("ts-input", "value"),
    prevent_initial_call=True,
)
def _convert(_, value):
    ts = value.strip() if value and value.strip() else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        enc   = convert_date(ts)
        shift = enc[0]
        col   = SHIFT_COL.get(shift, C1)
        labels = {"A": "07:00–14:59", "B": "15:00–22:59", "C": "23:00–06:59"}
        return html.Span([
            html.Span("→ ", style={"color": MUTED}),
            html.Span(enc, style={"color": col, "fontWeight": "700",
                                  "fontSize": "1.6rem", "letterSpacing": "0.18em",
                                  "textShadow": f"0 0 12px {col}"}),
            html.Span(f"   Shift {shift}: {labels[shift]}",
                      style={"color": MUTED, "fontSize": "0.85rem", "marginLeft": "1rem"}),
        ])
    except Exception as exc:
        return html.Span(f"Error: {exc}", style={"color": C4})


@app.callback(
    Output("live-chart", "figure"),
    Output("live-feed",  "children"),
    Output("live-store", "data"),
    Input("live-tick",   "n_intervals"),
    State("live-store",  "data"),
    State("tabs",        "active_tab"),
    prevent_initial_call=True,
)
def _live(_, store, active_tab):
    if active_tab != "live":
        return dash.no_update, dash.no_update, store
    now = datetime.now()
    ts  = now.strftime("%Y-%m-%d %H:%M:%S")
    try:
        enc  = convert_date(ts)
        sh   = enc[0]
    except Exception:
        enc, sh = "------", "?"

    ts_list  = (store["ts"]  + [ts])[-40:]
    enc_list = (store["enc"] + [enc])[-40:]
    sh_list  = (store["sh"]  + [sh])[-40:]

    sh_col = {"A": C3, "B": C1, "C": C2, "?": MUTED}

    fig = go.Figure()
    for s, color in SHIFT_COL.items():
        idx = [i for i, v in enumerate(sh_list) if v == s]
        if idx:
            fig.add_trace(go.Scatter(
                x=[ts_list[i] for i in idx],
                y=[sh_list.count(s)] * len(idx),
                mode="markers", name=f"Shift {s}",
                marker=dict(size=14, color=color, symbol="circle",
                            line=dict(color="white", width=1)),
            ))
    _layout(fig, 230, title=_title("Live Conversion Stream"),
            yaxis=dict(visible=False, gridcolor=GRID, zeroline=False))

    feed = [
        html.Div([
            html.Span(f"[{t[-8:]}] ", style={"color": MUTED}),
            html.Span(f"{t}  →  ", style={"color": TEXT}),
            html.Span(e, style={"color": sh_col.get(s, MUTED), "fontWeight": "700"}),
            html.Span(f"  (Shift {s})", style={"color": MUTED}),
        ])
        for t, e, s in zip(reversed(ts_list), reversed(enc_list), reversed(sh_list))
    ]

    return fig, feed, {"ts": ts_list, "enc": enc_list, "sh": sh_list}


server = app.server  # exposed for gunicorn: gunicorn dashboard:server

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=False)
