# **Watertown Parking Pricing Advisor**  
*A prescriptive analytics web application for optimizing parking prices across zones and time blocks.*

---

## Overview

Watertown Parking Pricing Advisor is a dynamic pricing tool built as the final project for **ISOM 839 – Prescriptive Analytics**.

The application enables users to:

- Upload aggregated parking demand data  
- Adjust occupancy targets and pricing ranges  
- Run an optimization model  
- Receive recommended prices, predicted occupancy, and expected revenue  
- Visualize outcomes by zone  

This project demonstrates prescriptive analytics by transforming data into **actionable pricing recommendations**, not just descriptive charts.

---

## Problem Statement

Parking demand in Watertown varies widely across:

- different street zones  
- time of day  
- baseline demand levels  

Using one fixed price leads to:

- overcrowding in high-demand blocks  
- underutilization in low-demand blocks  
- inefficient revenue performance  
- difficulty achieving the **85% healthy occupancy** standard  

A data-driven pricing tool is needed to recommend **optimal prices by zone and time block**.

---

## Solution

This project provides a **Streamlit web app + optimization engine** that:

1. Accepts aggregated parking data  
2. Applies a simple demand-response model  
3. Runs an optimization using SciPy  
4. Produces optimal prices, occupancy predictions, and revenue estimates  
5. Visualizes results with interactive charts  

This is a fully working **prescriptive analytics product**, suitable for demonstration or deployment.

---

## How the Model Works

### **Demand Function**
```
D(p) = D0 * (1 - beta * (p - p0) / p0)
```

Where:  
- D0 = baseline demand  
- p0 = baseline price  
- beta = price sensitivity  

### **Revenue**
```
Revenue = p * D(p)
```

### **Penalty Term**
```
Penalty = lambda * (occupancy - occupancy_target)^2
```

### **Final Objective Minimized**
```
Objective = -Revenue + Penalty
```

The optimizer finds the price that **maximizes expected revenue** while keeping predicted occupancy **close to the target level** (default 85%).

---

## App Features

### ✔ Upload data  
The CSV must include:

- zone  
- time_block  
- capacity  
- baseline_price  
- baseline_demand  

### ✔ Configure optimization  
- target occupancy  
- minimum and maximum price  
- price sensitivity (beta)  
- penalty weight (lambda)  

### Outputs  
- recommended_price  
- predicted_demand  
- predicted_occupancy  
- expected_revenue  

### ✔ Visualizations  
- Revenue by zone  
- Occupancy by zone  
- Full optimization result table  

---

## Project Structure

```
watertown-pricing-advisor/
│
├── app.py                 # Streamlit UI
├── model.py               # Optimization logic
├── sample_parking_agg.csv # Example dataset
├── requirements.txt       # Dependencies
└── README.md
```

---

## Input Data Format

Example:

| zone          | time_block | capacity | baseline_price | baseline_demand |
|---------------|-----------|----------|----------------|-----------------|
| Main St East  | 8-11      | 20       | 1.00           | 3541            |

This file must be **aggregated**, not raw transaction-level data.

---

## How to Run Locally

### **1. Install dependencies**
```
pip install -r requirements.txt
```

### **2. Launch the application**
```
streamlit run app.py
```

### **3. Upload CSV → adjust settings → run optimization**

---

## Deployment (Streamlit Cloud)

1. Push this repository to GitHub  
2. Visit https://share.streamlit.io  
3. Connect your GitHub repo  
4. Select `app.py` as the entry point  
5. Deploy  

You will receive a public URL to share with your professor or employers.

---

## Loom Demo Outline (3–5 min)

Suggested structure:

1. Introduce parking pricing problem  
2. Explain app purpose and logic  
3. Demo: upload → set parameters → run  
4. Show results: prices, revenue, occupancy  
5. Describe future enhancements  

---

## Future Enhancements

- Learn beta from historical behavioral data  
- Add weather or event-based demand adjustments  
- Time-series demand forecasting  
- Multi-objective optimization (revenue, equity, turnover)  
- Export recommendations as PDF or Excel  

---

## Author

**Crystal Vu**  
MSBA Candidate – Suffolk University  
ISOM 839 – Prescriptive Analytics  
