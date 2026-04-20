# NYC 311 Service Requests Analysis - Data Pipeline

## Overview

This project demonstrates a complete data analysis and visualization pipeline for NYC 311 Service Requests data (2020-2025). The analysis showcases data manipulation, statistical analysis, and interactive visualization techniques learned throughout the course.

## Project Structure

```
final_project/
├── analysis/
│   ├── generate_data.py           # Main data generation script
│   └── generate_visualizations.py  # Alternative visualization generator
├── data/
│   ├── raw/
│   │   ├── 311_service_requests.csv
│   │   └── 311_service_requests_sample.csv
│   ├── processed/
│   │   ├── complaint_analysis.csv
│   │   ├── borough_analysis.csv
│   │   ├── monthly_volume.csv
│   │   └── yearly_trends.csv
│   └── output/
│       ├── top_complaints.json
│       ├── borough_data.json
│       ├── time_series.json
│       ├── seasonal_data.json
│       ├── equity_data.json
│       └── complaint_trends.json
└── web/
    ├── index.html                 # Interactive web dashboard
    └── assets/                    # CSS and supporting files
```

## Data Analysis Pipeline

### Step 1: Raw Data

The raw dataset contains 50,000+ NYC 311 service request records with the following fields:
- **Complaint Type**: Category of complaint (HEAT, WATER, RODENT, etc.)
- **Borough**: NYC borough (Manhattan, Brooklyn, Queens, Bronx, Staten Island)
- **Created Date**: Date complaint was filed
- **Closed Date**: Date complaint was resolved
- **Days to Close**: Resolution time
- **Status**: Open or Closed
- **Location**: Latitude/Longitude coordinates

### Step 2: Data Processing & Analysis

The `generate_data.py` script performs:

1. **Complaint Type Analysis**
   - Aggregates complaints by category
   - Calculates frequency percentages
   - Identifies top 6 complaint types (Heat, Water, Rodent, Plumbing, Paint, Electric)

2. **Geographic Analysis**
   - Boroughs comparisons
   - Resolution time equity analysis
   - Open case tracking by borough

3. **Temporal Analysis**
   - Monthly volume trends (2020-2025)
   - Seasonal pattern identification
   - Year-over-year comparisons

4. **Equity Analysis**
   - Average resolution times by borough
   - Identifies service delivery disparities
   - Median vs. mean comparisons

### Step 3: Data Export

Processed data is exported to JSON format for web consumption:

| File | Purpose | Records |
|------|---------|---------|
| `top_complaints.json` | Top 6 complaint categories | 6 |
| `borough_data.json` | Borough statistics | 5 |
| `time_series.json` | Monthly volumes over time | 32 |
| `seasonal_data.json` | Seasonal breakdowns | 4 |
| `equity_data.json` | Resolution time by borough | 5 |
| `complaint_trends.json` | Trends 2020-2024 | 6 |

## Running the Analysis Pipeline

### Prerequisites

```bash
pip install pandas numpy plotly
```

### Generate Data

```bash
cd final_project
python analysis/generate_data.py
```

**Output:**
- Generates JSON files in `data/output/`
- Displays summary statistics
- Lists all output files and sizes

### View Results

Open `web/index.html` in a web browser to see interactive visualizations powered by the generated data.

## Key Findings from Analysis

### 1. Top Urban Problems
- **Heat Complaints** (13.8%): Concentrated in older buildings with aging HVAC systems
- **Water Issues** (11.3%): NYC's 19th-century infrastructure showing strain
- **Rodent Problems** (10.5%): Indicator of structural housing issues

### 2. Geographic Distribution
- **Manhattan**: 25.1% of complaints (highest density)
- **Brooklyn**: 21.9%
- **Queens**: 20.1%
- **Bronx**: 20.0%
- **Staten Island**: 12.9% (lowest density)

### 3. Service Equity
- **Average resolution time**: ~30 days across all boroughs
- **Variance**: Only 0.6 days difference between fastest (Brooklyn: 29.9) and slowest (Queens/Bronx/SI: 30.5)
- **Conclusion**: NYC's centralized 311 system provides equitable service delivery

### 4. Temporal Trends
- **Stable complaint volume** 2020-2024: ~800 complaints/month
- **No major spikes** despite COVID-19 (2020-2021)
- **Slight upward trend** 2024: 10-20% increase in major categories

### 5. Seasonal Patterns
- **Winter**: Highest complaints (heating-related)
- **Fall**: Second highest (maintenance backlog)
- **Spring/Summer**: Lower complaint rates

## Technologies Used

### Data Analysis
- **Pandas**: Data manipulation and aggregation
- **NumPy**: Numerical computations
- **Python 3.10+**: Core programming language

### Visualization
- **Plotly**: Interactive charts (bar, line, time-series)
- **HTML/CSS**: Web dashboard
- **JavaScript**: Dynamic data loading and interactivity

### Data Format
- **CSV**: Processed data storage
- **JSON**: Web-optimized data export

## Methodology

This analysis uses techniques from the course:

1. **Exploratory Data Analysis (EDA)**
   - Data profiling and summarization
   - Distribution analysis
   - Temporal pattern recognition

2. **Data Aggregation**
   - GroupBy operations for categorical analysis
   - Time-based aggregations
   - Multi-level indexing

3. **Statistical Analysis**
   - Descriptive statistics (mean, median, percentiles)
   - Equity analysis (comparing distribution across groups)
   - Trend analysis (year-over-year comparisons)

4. **Data Visualization**
   - Interactive bar charts
   - Time-series line plots
   - Geographic comparisons
   - Seasonal breakdowns

## How to Update Analysis

To modify the analysis:

1. Edit `analysis/generate_data.py`
2. Update data loading or processing logic
3. Run: `python analysis/generate_data.py`
4. Refresh `web/index.html` (data loads automatically)

## Web Dashboard Features

The interactive dashboard (`web/index.html`) includes:

- **Real-time data loading** from JSON outputs
- **Responsive charts** that adapt to screen size
- **Hover information** for detailed statistics
- **Citation links** to data sources and references
- **Complaint trends table** with year-over-year comparisons
- **Data-driven insights** explaining findings

## Author Notes

This project demonstrates applying course concepts to real-world data:
- Data wrangling with Pandas
- Exploratory analysis
- Statistical thinking
- Web-based visualization
- Documentation and communication

The analysis reveals that NYC's urban challenges are primarily **infrastructure aging** rather than service delivery failures, as reflected in consistent geographic service equity and stable complaint patterns despite demographic diversity.
