<div align="center">

# ⚡ Timestamp Converter

**A production-ready timestamp encoding utility with an interactive intelligence dashboard**

[![Python](https://img.shields.io/badge/Python-3.7%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Dash](https://img.shields.io/badge/Dash-2.14%2B-008DE4?style=flat-square&logo=plotly&logoColor=white)](https://dash.plotly.com)
[![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-3F4F75?style=flat-square&logo=plotly&logoColor=white)](https://plotly.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Render](https://img.shields.io/badge/Deploy-Render-46E3B7?style=flat-square&logo=render&logoColor=white)](https://render.com)

</div>

---

## Overview

Timestamp Converter encodes datetime strings into compact 6-character codes that capture **shift**, **day**, **month**, and **year** — making temporal data instantly readable at a glance.

On top of the encoding engine, the project ships a full **Plotly Dash intelligence dashboard** with real-time conversion, animated charts, anomaly detection, forecasting, and a live stream mode.

---

## Encoding Format

Every timestamp produces a 6-character code:

```
B  15  G  19
│   │   │   └─ Year (last 2 digits)
│   │   └───── Month letter (A–M, skipping I)
│   └───────── Day of month (zero-padded)
└───────────── Shift letter (A / B / C)
```

### Shift Mapping

| Shift | Hours | Description |
|-------|-------|-------------|
| **A** | 07:00 – 14:59 | Morning / Day shift |
| **B** | 15:00 – 22:59 | Afternoon / Evening shift |
| **C** | 23:00 – 06:59 | Night shift |

### Month Mapping

| Month | Code | Month | Code | Month | Code |
|-------|------|-------|------|-------|------|
| January | A | May | E | September | J |
| February | B | June | F | October | K |
| March | C | July | G | November | L |
| April | D | August | H | December | M |

> **Note:** The letter `I` is intentionally skipped to avoid visual ambiguity with `1`.

### Examples

| Input Timestamp | Output | Breakdown |
|-----------------|--------|-----------|
| `2019-07-15 22:03:16` | `B15G19` | Shift B · Day 15 · Jul (G) · 2019 |
| `2015-01-05 07:00:01` | `A05A15` | Shift A · Day 05 · Jan (A) · 2015 |
| `2021-05-02 11:20:01` | `A02E21` | Shift A · Day 02 · May (E) · 2021 |
| `2023-12-25 23:30:00` | `C25M23` | Shift C · Day 25 · Dec (M) · 2023 |

---

## Installation

### Prerequisites

- Python 3.7 or higher
- pip

### Clone & Install

```bash
git clone https://github.com/MpiloG29/timestamp-converter-project.git
cd timestamp-converter-project
pip install -r requirements.txt
```

---

## Usage

### As a Python Library

```python
from datetime_converter import convert_date

# Single conversion
result = convert_date("2019-07-15 22:03:16")
print(result)  # → B15G19

# Current time
from datetime import datetime
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(convert_date(now))
```

### Interactive CLI Tool

```bash
python interactive_test.py
```

Enter any timestamp at the prompt, type `now` to encode the current time, or `quit` to exit.

### Dashboard

```bash
python dashboard.py
```

Then open [http://localhost:8050](http://localhost:8050) in your browser.

---

## Dashboard

The intelligence dashboard gives you a full visual breakdown of conversion patterns across 8 tabs:

| Tab | What you see |
|-----|-------------|
| **Overview** | Animated Sankey flow (Raw → Shift → Month Code), shift distribution donut, stacked monthly bar chart |
| **Temporal** | Hour × weekday activity heatmap with neon colour scale |
| **Timeline** | Draggable range-slider area chart — zoom into any date range |
| **Anomaly** | Z-score spike detection (flags days beyond ±2σ) with star markers |
| **Comparative** | Side-by-side weekday vs weekend hourly patterns |
| **Forecast** | Polynomial trend line + 30-day forward forecast with confidence band |
| **Insights** | Auto-generated narrative summaries derived from real data patterns |
| **Live Stream** | Real-time encoding ticker — new conversion every 2 seconds |

**Always visible:** live clock, KPI cards, instant converter input, and achievement badges.

---

## Project Structure

```
timestamp-converter-project/
│
├── datetime_converter.py     # Core encoding logic
├── dashboard.py              # Plotly Dash dashboard (8 tabs)
│
├── interactive_test.py       # CLI interactive converter
├── demo_usage.py             # Printed demo with examples
├── example.py                # Minimal usage example
│
├── test_convert_date.py      # pytest unit tests
├── edge_cases_test.py        # Boundary & edge case validation
│
├── requirements.txt          # Python dependencies
├── Procfile                  # Gunicorn entry point (Render / Heroku)
├── render.yaml               # Render deployment config
└── setup.py                  # Package metadata
```

---

## Testing

```bash
# Run the full test suite
pytest test_convert_date.py -v

# Run edge case validation
python edge_cases_test.py

# Run the demo
python demo_usage.py
```

---

## Deployment

The project is pre-configured for **Render** (zero-config deploy).

### Deploy to Render

1. Fork or clone this repository to your GitHub account
2. Go to [render.com](https://render.com) → **New → Web Service**
3. Connect your GitHub repo
4. Render auto-detects `render.yaml` and fills in all settings
5. Click **Deploy**

The `render.yaml` pins Python 3.12, installs dependencies, and starts gunicorn automatically.

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8050` | Port the server listens on (set automatically by Render) |

### Manual / Self-hosted

```bash
gunicorn dashboard:server
```

Or with an explicit port:

```bash
PORT=8080 gunicorn dashboard:server
```

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `dash` | Web framework for the dashboard |
| `plotly` | Interactive chart library |
| `dash-bootstrap-components` | Layout and styling components |
| `pandas` | Data manipulation |
| `numpy` | Numerical operations and synthetic data generation |
| `gunicorn` | Production WSGI server |
| `pytest` | Test runner |

---

## License

This project is licensed under the MIT License.
