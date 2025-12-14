# Watertown Parking Pricing Advisor
A prescriptive analytics web application for optimizing parking prices across zones and time blocks.

---

## Overview

Watertown Parking Pricing Advisor is a dynamic pricing tool built as the final project for **ISOM 839 – Prescriptive Analytics**.

The application enables users to:

- Upload aggregated parking demand data  
- Adjust occupancy targets and pricing ranges  
- Run an optimization model  
- Receive recommended prices, predicted occupancy, and expected revenue  
- Review clear pricing actions through a decision table  
- Visualize outcomes by zone  

This project demonstrates **prescriptive analytics** by transforming data into **actionable pricing recommendations**, rather than only descriptive charts or forecasts.

---

## Problem Statement

Parking demand in Watertown varies widely across:

- different street zones  
- time of day  
- baseline demand levels  

Using one fixed parking price leads to:

- overcrowding in high-demand blocks  
- underutilization in low-demand blocks  
- inefficient revenue performance  
- difficulty achieving the recommended **85% healthy occupancy** standard  

A data-driven pricing tool is needed to recommend **optimal prices by zone and time block**, while explicitly balancing revenue and occupancy goals.

---

## Solution

This project provides a **Streamlit web application combined with an optimization engine** that:

1. Accepts aggregated parking demand data  
2. Applies a simple price–demand response model  
3. Solves a constrained optimization problem using SciPy  
4. Produces recommended prices, predicted occupancy, and expected revenue  
5. Presents results as **decision-oriented outputs**, not just visual summaries  

The result is a fully working **prescriptive analytics decision-support system**, suitable for demonstration or further extension.

---

## Prescriptive Analytics Framework

### Decision Variable
- Hourly parking price for each **zone–time block**

### Objective
- Maximize expected revenue  
- While keeping predicted occupancy close to a target level (default 85%)

### Constraints
- Minimum and maximum allowable prices

The application directly answers the question:

**“What hourly price should be charged for each zone and time block?”**

---

## How the Model Works

### Demand Function
# Watertown Parking Pricing Advisor
A prescriptive analytics web application for optimizing parking prices across zones and time blocks.

---

## Overview

Watertown Parking Pricing Advisor is a dynamic pricing tool built as the final project for **ISOM 839 – Prescriptive Analytics**.

The application enables users to:

- Upload aggregated parking demand data  
- Adjust occupancy targets and pricing ranges  
- Run an optimization model  
- Receive recommended prices, predicted occupancy, and expected revenue  
- Review clear pricing actions through a decision table  
- Visualize outcomes by zone  

This project demonstrates **prescriptive analytics** by transforming data into **actionable pricing recommendations**, rather than only descriptive charts or forecasts.

---

## Problem Statement

Parking demand in Watertown varies widely across:

- different street zones  
- time of day  
- baseline demand levels  

Using one fixed parking price leads to:

- overcrowding in high-demand blocks  
- underutilization in low-demand blocks  
- inefficient revenue performance  
- difficulty achieving the recommended **85% healthy occupancy** standard  

A data-driven pricing tool is needed to recommend **optimal prices by zone and time block**, while explicitly balancing revenue and occupancy goals.

---

## Solution

This project provides a **Streamlit web application combined with an optimization engine** that:

1. Accepts aggregated parking demand data  
2. Applies a simple price–demand response model  
3. Solves a constrained optimization problem using SciPy  
4. Produces recommended prices, predicted occupancy, and expected revenue  
5. Presents results as **decision-oriented outputs**, not just visual summaries  

The result is a fully working **prescriptive analytics decision-support system**, suitable for demonstration or further extension.

---

## Prescriptive Analytics Framework

### Decision Variable
- Hourly parking price for each **zone–time block**

### Objective
- Maximize expected revenue  
- While keeping predicted occupancy close to a target level (default 85%)

### Constraints
- Minimum and maximum allowable prices

The application directly answers the question:

**“What hourly price should be charged for each zone and time block?”**

---

## How the Model Works

### Demand Function
# Watertown Parking Pricing Advisor
A prescriptive analytics web application for optimizing parking prices across zones and time blocks.

---

## Overview

Watertown Parking Pricing Advisor is a dynamic pricing tool built as the final project for **ISOM 839 – Prescriptive Analytics**.

The application enables users to:

- Upload aggregated parking demand data  
- Adjust occupancy targets and pricing ranges  
- Run an optimization model  
- Receive recommended prices, predicted occupancy, and expected revenue  
- Review clear pricing actions through a decision table  
- Visualize outcomes by zone  

This project demonstrates **prescriptive analytics** by transforming data into **actionable pricing recommendations**, rather than only descriptive charts or forecasts.

---

## Problem Statement

Parking demand in Watertown varies widely across:

- different street zones  
- time of day  
- baseline demand levels  

Using one fixed parking price leads to:

- overcrowding in high-demand blocks  
- underutilization in low-demand blocks  
- inefficient revenue performance  
- difficulty achieving the recommended **85% healthy occupancy** standard  

A data-driven pricing tool is needed to recommend **optimal prices by zone and time block**, while explicitly balancing revenue and occupancy goals.

---

## Solution

This project provides a **Streamlit web application combined with an optimization engine** that:

1. Accepts aggregated parking demand data  
2. Applies a simple price–demand response model  
3. Solves a constrained optimization problem using SciPy  
4. Produces recommended prices, predicted occupancy, and expected revenue  
5. Presents results as **decision-oriented outputs**, not just visual summaries  

The result is a fully working **prescriptive analytics decision-support system**, suitable for demonstration or further extension.

---

## Prescriptive Analytics Framework

### Decision Variable
- Hourly parking price for each **zone–time block**

### Objective
- Maximize expected revenue  
- While keeping predicted occupancy close to a target level (default 85%)

### Constraints
- Minimum and maximum allowable prices

The application directly answers the question:

**“What hourly price should be charged for each zone and time block?”**

---

## How the Model Works

### Demand Function
D(p) = D0 * (1 - beta * (p - p0) / p0)

Where:
- `D0` = baseline demand  
- `p0` = baseline price  
- `beta` = price sensitivity  

### Revenue
Revenue = p * D(p)

### Occupancy
Occupancy = D(p) / Capacity

Occupancy displayed in the dashboard is **clipped to the range 0–100%** for interpretability.

### Penalty Term
Penalty = lambda * (occupancy - occupancy_target)^2

### Final Objective Minimized
Objective = -Revenue + Penalty

The optimizer selects prices that balance revenue maximization with adherence to the target occupancy level.

---

## App Features
Link APP: https://isom839project-ebysau75c5isizc4x2ad8a.streamlit.app

### Data Upload
The CSV file must include the following **aggregated** fields:

- `zone`  
- `time_block`  
- `capacity`  
- `baseline_price`  
- `baseline_demand`  

### Configuration Controls
Users can adjust:

- target occupancy  
- minimum and maximum price bounds  
- price sensitivity (`beta`)  
- penalty weight (`lambda`)  

### Output Tabs

#### 1) Summary
- Input preview and dataset diagnostics  
- Key metrics:
  - total expected revenue  
  - average predicted occupancy  
  - number of zone–time blocks  
- **Executive Recommendation**, translating model output into pricing actions  
- Zone-level revenue and occupancy charts  

#### 2) Decision Table
- Action-oriented table including:
  - baseline price  
  - recommended price  
  - price change  
  - action label (increase / decrease / keep)  
  - predicted occupancy  
  - expected revenue  
- Downloadable CSV of recommendations  

#### 3) Model Notes
- Prescriptive structure  
- Key assumptions  
- Interpretation guidance and limitations  

### Usability
- Results persist across tab switches using session state  
- “Clear results” button allows users to reset and rerun scenarios  

---

## Data Interpretation Notes

If many zone–time blocks exceed **100% predicted occupancy before clipping**, this indicates that `baseline_demand` and `capacity` are likely on different scales due to aggregation (for example, demand aggregated over longer periods than capacity).

In such cases:

- Occupancy is clipped for interpretability  
- Recommendations should be interpreted as **directional pricing actions** (increase vs. decrease), rather than precise occupancy forecasts  

The tool is most useful for **consistent pricing comparisons across zones and time blocks under a fixed objective function**.

---

## Project Structure


The optimizer selects prices that balance revenue maximization with adherence to the target occupancy level.

---

## App Features

### Data Upload
The CSV file must include the following **aggregated** fields:

- `zone`  
- `time_block`  
- `capacity`  
- `baseline_price`  
- `baseline_demand`  

### Configuration Controls
Users can adjust:

- target occupancy  
- minimum and maximum price bounds  
- price sensitivity (`beta`)  
- penalty weight (`lambda`)  

### Output Tabs

#### 1) Summary
- Input preview and dataset diagnostics  
- Key metrics:
  - total expected revenue  
  - average predicted occupancy  
  - number of zone–time blocks  
- **Executive Recommendation**, translating model output into pricing actions  
- Zone-level revenue and occupancy charts  

#### 2) Decision Table
- Action-oriented table including:
  - baseline price  
  - recommended price  
  - price change  
  - action label (increase / decrease / keep)  
  - predicted occupancy  
  - expected revenue  
- Downloadable CSV of recommendations  

#### 3) Model Notes
- Prescriptive structure  
- Key assumptions  
- Interpretation guidance and limitations  

### Usability
- Results persist across tab switches using session state  
- “Clear results” button allows users to reset and rerun scenarios  

---

## Data Interpretation Notes

If many zone–time blocks exceed **100% predicted occupancy before clipping**, this indicates that `baseline_demand` and `capacity` are likely on different scales due to aggregation (for example, demand aggregated over longer periods than capacity).

In such cases:

- Occupancy is clipped for interpretability  
- Recommendations should be interpreted as **directional pricing actions** (increase vs. decrease), rather than precise occupancy forecasts  

The tool is most useful for **consistent pricing comparisons across zones and time blocks under a fixed objective function**.

---

## Project Structure
watertown-pricing-advisor/
│
├── app.py # Streamlit UI
├── model.py # Optimization logic
├── sample_parking_agg.csv # Example aggregated dataset
├── requirements.txt # Dependencies
└── README.md


---

## Input Data Format

Example:

| zone         | time_block | capacity | baseline_price | baseline_demand |
|--------------|-----------|----------|----------------|-----------------|
| Main St East | 8–11      | 20       | 1.00           | 3541            |

The input file must be **aggregated**, not raw transaction-level data.

---

## How to Run Locally

### 1. Install dependencies
pip install -r requirements.txt

### 2. Launch the application

streamlit run app.py


### 3. Upload CSV → adjust parameters → run optimization

---

## Loom Demo Outline (3–5 minutes)

1. Introduce the parking pricing problem  
2. Explain the prescriptive objective and decision variable  
3. Demonstrate CSV upload and parameter configuration  
4. Run the optimization model  
5. Interpret the Summary and Decision Table outputs
   
Link: https://www.loom.com/share/d7c98151227040d5b715ef867fd863bf
---

## Future Enhancements

- Estimate price sensitivity from historical behavioral data  
- Normalize demand to hourly units automatically  
- Incorporate weather or event-based demand effects  
- Support multi-objective optimization (revenue, equity, turnover)  
- Export recommendations to PDF or Excel reports  

---

## Author

**Crystal Vu**  
MSBA Candidate – Suffolk University  
ISOM 839 – Prescriptive Analytics
