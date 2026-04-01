"""
dashboard.py
Generates an interactive HTML dashboard from analysis outputs.
"""
import pandas as pd
import json
import os

# Load reports
summary = json.load(open("reports/summary.json"))
supplier = pd.read_csv("reports/supplier_otd_scorecard.csv")
carriers = pd.read_csv("reports/carrier_delay_analysis.csv")
reasons = pd.read_csv("reports/delay_root_causes.csv")
monthly = pd.read_csv("reports/monthly_shipment_trends.csv")
warehouse = pd.read_csv("reports/warehouse_volume.csv")

def status_badge(status):
    colors = {"CRITICAL": "#e74c3c", "AT RISK": "#f39c12", "HEALTHY": "#27ae60"}
    return f'<span style="background:{colors.get(status,"#aaa")};color:white;padding:3px 10px;border-radius:12px;font-size:12px;font-weight:bold">{status}</span>'

def build_table(df, highlight_col=None):
    rows = ""
    for _, row in df.iterrows():
        cells = ""
        for col in df.columns:
            val = row[col]
            if col == highlight_col:
                cells += f"<td>{status_badge(val)}</td>"
            else:
                cells += f"<td>{val}</td>"
        rows += f"<tr>{cells}</tr>"
    headers = "".join(f"<th>{c.replace('_',' ').title()}</th>" for c in df.columns)
    return f"<table><thead><tr>{headers}</tr></thead><tbody>{rows}</tbody></table>"

monthly_labels = [str(m) for m in monthly["month"].tolist()]
monthly_values = monthly["shipments"].tolist()
otd_values = monthly["on_time_pct"].tolist()

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Supply Chain Operations Dashboard</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Segoe UI', sans-serif; background: #f0f2f5; color: #222; }}
  header {{ background: #1a1a2e; color: white; padding: 28px 40px; }}
  header h1 {{ font-size: 24px; font-weight: 700; }}
  header p {{ font-size: 13px; color: #aaa; margin-top: 4px; }}
  .kpi-row {{ display: flex; gap: 20px; padding: 28px 40px 0; flex-wrap: wrap; }}
  .kpi {{ background: white; border-radius: 10px; padding: 20px 28px; flex: 1; min-width: 160px;
           box-shadow: 0 2px 8px rgba(0,0,0,0.07); border-top: 4px solid #5b4395; }}
  .kpi .val {{ font-size: 32px; font-weight: 700; color: #1a1a2e; }}
  .kpi .lbl {{ font-size: 12px; color: #777; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.5px; }}
  .section {{ background: white; border-radius: 10px; margin: 24px 40px 0;
              padding: 24px 28px; box-shadow: 0 2px 8px rgba(0,0,0,0.07); }}
  .section h2 {{ font-size: 15px; font-weight: 700; color: #1a1a2e; margin-bottom: 16px;
                 padding-left: 10px; border-left: 4px solid #5b4395; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th {{ background: #f8f8fc; text-align: left; padding: 10px 12px; color: #555;
        font-weight: 600; border-bottom: 2px solid #eee; }}
  td {{ padding: 10px 12px; border-bottom: 1px solid #f0f0f0; }}
  tr:hover td {{ background: #fafafa; }}
  .chart-wrap {{ position: relative; height: 220px; }}
  canvas {{ width: 100% !important; }}
  .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin: 24px 40px 0; }}
  .two-col .section {{ margin: 0; }}
  footer {{ text-align: center; padding: 32px; color: #aaa; font-size: 12px; }}
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
</head>
<body>

<header>
  <h1>Supply Chain Operations Analytics Dashboard</h1>
  <p>Operations Data & Analytics Program &nbsp;|&nbsp; Versuni Supply Chain Excellence</p>
</header>

<div class="kpi-row">
  <div class="kpi"><div class="val">{summary['total_orders']:,}</div><div class="lbl">Total Orders</div></div>
  <div class="kpi"><div class="val">{summary['overall_otd_pct']}%</div><div class="lbl">On-Time Delivery</div></div>
  <div class="kpi"><div class="val">{len(summary['critical_suppliers'])}</div><div class="lbl">Critical Suppliers</div></div>
  <div class="kpi"><div class="val">{summary['stockout_risk_count']}</div><div class="lbl">Stockout Risk Cases</div></div>
  <div class="kpi"><div class="val">{summary['total_spend']}</div><div class="lbl">Total Spend</div></div>
</div>

<div class="section">
  <h2>Monthly Shipment Volume & On-Time Delivery Trend</h2>
  <div class="chart-wrap">
    <canvas id="monthlyChart"></canvas>
  </div>
</div>

<div class="two-col">
  <div class="section">
    <h2>Supplier On-Time Delivery Scorecard</h2>
    {build_table(supplier, highlight_col="status")}
  </div>
  <div class="section">
    <h2>Delay Root Cause Analysis</h2>
    {build_table(reasons)}
  </div>
</div>

<div class="two-col">
  <div class="section">
    <h2>Carrier Delay Performance</h2>
    {build_table(carriers)}
  </div>
  <div class="section">
    <h2>Warehouse Inbound Volume</h2>
    {build_table(warehouse)}
  </div>
</div>

<footer>Supply Chain Operations Analytics Pipeline &nbsp;|&nbsp; Built with Python &middot; pandas &middot; SQL Analytics &middot; Chart.js</footer>

<script>
const ctx = document.getElementById('monthlyChart').getContext('2d');
new Chart(ctx, {{
  type: 'bar',
  data: {{
    labels: {monthly_labels},
    datasets: [
      {{
        label: 'Shipments',
        data: {monthly_values},
        backgroundColor: 'rgba(91,67,149,0.75)',
        borderRadius: 6,
        yAxisID: 'y'
      }},
      {{
        label: 'On-Time %',
        data: {otd_values},
        type: 'line',
        borderColor: '#27ae60',
        backgroundColor: 'rgba(39,174,96,0.1)',
        tension: 0.4,
        fill: true,
        yAxisID: 'y1'
      }}
    ]
  }},
  options: {{
    responsive: true,
    maintainAspectRatio: false,
    plugins: {{ legend: {{ position: 'top' }} }},
    scales: {{
      y: {{ title: {{ display: true, text: 'Shipments' }}, beginAtZero: true }},
      y1: {{ position: 'right', title: {{ display: true, text: 'OTD %' }}, min: 60, max: 100,
              grid: {{ drawOnChartArea: false }} }}
    }}
  }}
}});
</script>
</body>
</html>"""

os.makedirs("reports", exist_ok=True)
with open("reports/dashboard.html", "w") as f:
    f.write(html)
print("Dashboard saved to reports/dashboard.html")
