# 🚚 Supply Chain Operations Analytics Pipeline

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-green?style=flat&logo=pandas)
![ChartJS](https://img.shields.io/badge/Chart.js-Interactive-pink?style=flat)
![Domain](https://img.shields.io/badge/Domain-Supply%20Chain%20Excellence-orange?style=flat)
![Orders](https://img.shields.io/badge/Orders%20Analysed-500-blue?style=flat)
![KPIs](https://img.shields.io/badge/KPIs%20Computed-7-purple?style=flat)

> **End-to-end supply chain operations analytics — order tracking · delivery performance · supplier scorecards · delay root cause analysis · inventory stockout risk monitoring**

---

## 🧠 Why I Built This

Supply chain excellence teams spend a significant amount of time pulling data from multiple systems, cleaning it and assembling it into reports that answer the same questions every week. Which suppliers are underperforming? Where are delays concentrating? Which warehouses are at risk of stockout?

This pipeline automates that entire workflow — from raw order and inventory data through to a fully populated operations dashboard — so the team can focus on acting on the insights rather than producing them.

---

## 📊 Results at a Glance

| Metric | Value |
|---|---|
| 📦 Orders analysed | 500 |
| 🏭 Suppliers tracked | 5 |
| 🏪 Warehouses monitored | 5 (Amsterdam · Brussels · Frankfurt · Paris · Rotterdam) |
| 🚛 Carriers tracked | 5 (DHL · DB Schenker · DSV · FedEx · UPS) |
| 📅 Period covered | Jan 2024 – Dec 2024 |
| ✅ Overall on-time delivery | 73.2% |
| 🔴 Critical suppliers | 2 (SupplierB · SupplierC) |
| 🟡 At-risk suppliers | 3 (SupplierA · SupplierD · SupplierE) |
| ⚠️ Stockout risk events | 5 |
| 💰 Total spend tracked | €16.2M |
| 📉 Top delay root cause | Bad weather (36.8%) |

---

## 🔍 Key Findings

### 📉 Finding 1 — Bad Weather is the Leading Delay Driver
Bad weather accounts for 36.8% of all delayed shipments — the single largest root cause, ahead of warehouse capacity issues, customs clearance and carrier delay which each account for roughly 21%. This points to a need for weather-resilient routing and pre-emptive buffer stock in exposed lanes rather than purely a carrier performance problem.

### 📦 Finding 2 — Irons are the Highest Stockout Risk Category
Stockout risk events are concentrated in the Irons category across Amsterdam, Brussels and Frankfurt. Rotterdam shows risk in Blenders. All 5 stockout events occurred in a single month each — suggesting periodic demand spikes rather than a chronic reorder point problem. Safety stock thresholds for these category-location combinations need recalibration.

### 🔴 Finding 3 — No Supplier is Performing at Target
Overall on-time delivery sits at 73.2% — below the 85% AT RISK threshold for every single supplier in the network. SupplierB and SupplierC are in CRITICAL territory at 67.6% and 67.7% respectively. This is not a supplier-specific problem — it indicates a systemic issue in the supply network that requires network-level intervention rather than individual supplier reviews.

---

## 🏗️ Architecture

```
generate_data.py
  ├── 500 simulated order records with shipment tracking data
  └── Monthly inventory levels by warehouse and product category
          │
          ▼
analysis.py
  ├── On-time delivery rate overall and by supplier
  ├── Supplier performance scorecard with risk rating
  ├── Carrier delay analysis by volume and average delay
  ├── Delay root cause frequency distribution
  ├── Monthly shipment trend with OTD overlay
  └── Inventory stockout risk by warehouse and category
          │
          ▼
dashboard.py
  └── Interactive HTML dashboard with Chart.js visualisations
          │
          ▼
reports/
  ├── dashboard.html                     ← open this
  ├── supplier_otd_scorecard.csv
  ├── carrier_delay_analysis.csv
  ├── delay_root_causes.csv
  ├── supplier_performance_scorecard.csv
  ├── monthly_shipment_trends.csv
  ├── inventory_stockout_risk.csv
  └── summary.json
```

---

## 📐 KPIs Computed

| KPI | Description | Audience |
|---|---|---|
| On-Time Delivery Rate | % of orders within promised lead time | Operations manager |
| Supplier Scorecard | OTD %, avg delay, total spend, risk tier | Procurement team |
| Carrier Delay Analysis | Avg delay days and volume per carrier | Logistics manager |
| Delay Root Cause | Frequency of customs / weather / carrier / capacity | Supply chain analyst |
| Monthly Shipment Trends | Volume and OTD % by month | Planning team |
| Inventory Stockout Risk | Months below safety threshold by location | Warehouse manager |
| Warehouse Inbound Volume | Orders and units received per DC | DC manager |

---

## 🚦 Supplier Risk Classification

| Tier | OTD Threshold | Action |
|---|---|---|
| 🔴 CRITICAL | Below 70% | Immediate escalation and review |
| 🟡 AT RISK | 70% – 85% | Active monitoring and improvement plan |
| 🟢 HEALTHY | Above 85% | Performing within targets |

---

## 📂 Project Structure

```
supply-chain-ops-analytics/
│
├── 📁 data/
│   ├── orders.csv          # 500 order and shipment tracking records
│   └── inventory.csv       # Monthly inventory by warehouse and category
│
├── 📁 src/
│   ├── generate_data.py    # Synthetic dataset generation
│   ├── analysis.py         # Core KPI computation pipeline
│   └── dashboard.py        # HTML dashboard generator
│
├── 📁 reports/
│   ├── dashboard.html               ← open this in browser
│   ├── supplier_otd_scorecard.csv
│   ├── carrier_delay_analysis.csv
│   ├── delay_root_causes.csv
│   ├── supplier_performance_scorecard.csv
│   ├── monthly_shipment_trends.csv
│   ├── inventory_stockout_risk.csv
│   └── summary.json
│
└── README.md
```

---

## 🚀 How to Run

```bash
pip install pandas numpy
python3 src/generate_data.py
python3 src/analysis.py
python3 src/dashboard.py
```

Then open `reports/dashboard.html` in your browser.

---

## 🔗 Related Project

This project works alongside the [Supplier Performance Analytics](https://github.com/pavansri8886/supplier-performance-analytics) repo, which extends the supplier scorecard with 12-month trend analysis, risk flagging, lane heatmaps and cold chain monitoring across 25 real-named European suppliers and 4,054 orders.

Together they form a complete supply chain analytics layer:

| This repo | Supplier Performance Analytics |
|---|---|
| End-to-end ops pipeline | Deep supplier trend analysis |
| Order tracking + inventory | 12-month monthly trends |
| Root cause classification | Lane heatmap by country |
| Stockout risk detection | Cold chain risk flagging |
| Summary JSON for downstream | Management dashboard |

---

## 🔭 What I Would Build Next

The natural next step is connecting the root cause classifier to a real-time alerting layer — when carrier delay exceeds a threshold on a specific lane, trigger an automatic notification to the logistics manager rather than surfacing it in the next weekly report. The stockout risk model would also benefit from incorporating demand forecasting so it flags risk before stock falls below safety level rather than after.

---

## 👤 Author

**Pavan Kumar Naganaboina**
MSc Data Management & AI — ECE Paris 2025–2026

[![LinkedIn](https://img.shields.io/badge/LinkedIn-pavankumarn01-blue?style=flat&logo=linkedin)](https://linkedin.com/in/pavankumarn01)
[![GitHub](https://img.shields.io/badge/GitHub-pavansri8886-black?style=flat&logo=github)](https://github.com/pavansri8886)

---

> *Built to demonstrate end-to-end supply chain analytics — from raw operational data through KPI computation, root cause analysis and management-ready reporting. Relevant to Supply Chain Excellence teams working on operational visibility, process efficiency and data-driven decision support.*
