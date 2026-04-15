# NYC 311 Service Requests: 1-Minute Concept Video
## Part A - Concept Video Script

---

## VIDEO SCRIPT (60 seconds)

### [0-5 seconds] OPENING - The Problem
**VISUAL**: Title card on purple background: "What Bothers New Yorkers?"  
**NARRATION**: "Every day, thousands of New Yorkers file 311 complaints—reporting everything from broken heating to rodent infestations to broken streets. But what problems matter most? And does the city treat all neighborhoods fairly?"

### [5-15 seconds] THE DATA
**VISUAL**: Bar chart showing top 3 complaints (HEAT 13.5%, WATER 11%, RODENT 10.3%)  
**NARRATION**: "We analyzed 50,000 complaints from across New York City. Heat, water, and rodent problems dominate—accounting for one-third of ALL complaints. These issues reveal infrastructure challenges facing the entire city."

### [15-30 seconds] GEOGRAPHIC PATTERNS
**VISUAL**: Borough comparison chart (Manhattan 25%, Brooklyn 22%, Queens 20%, Bronx 20%, Staten Island 13%)  
**NARRATION**: "But geographic patterns tell an important story. Manhattan reports the most complaints—but not because it has more problems. It has the highest population density. More importantly, we found something remarkable about equity..."

### [30-45 seconds] EQUITY FINDING
**VISUAL**: Resolution time chart by borough (nearly flat line across all 5 boroughs, all ~30 days)  
**NARRATION**: "NYC resolves complaints at nearly the same speed in every borough—about 30 days on average. This suggests fair resource allocation. Wealthy neighborhoods don't get faster service than low-income areas."

### [45-60 seconds] THE OPPORTUNITY
**VISUAL**: Time series showing stable complaint volume over 5 years  
**NARRATION**: "This data shows NYC's urban challenges stay steady—not worsening. But it also reveals where to invest: upgrade heating systems, manage pests, fix water infrastructure. By understanding what residents complain about, cities can build better."

---

## VISUALIZATION MOCKUPS

### Visual 1: Title Slide
```
┌──────────────────────────────────────┐
│                                      │
│   What Bothers New Yorkers?         │
│                                      │
│   NYC 311 Service Requests Analysis │
│   50,000 Complaints | 5 Years       │
│                                      │
└──────────────────────────────────────┘
```

### Visual 2: Top Complaints Bar Chart
```
Complaint Type Frequency (%)
┌────────────────────────────────┐
│ HEAT        ████████████ 13.5% │
│ WATER       ██████████ 11.0%   │
│ RODENT      ██████████ 10.3%   │
│ PLUMBING    ████████ 9.0%      │
│ PAINT       ████████ 9.0%      │
└────────────────────────────────┘
Key Insight: Top 3 = 34.8% of all complaints
```

### Visual 3: Borough Comparison
```
Complaints by Borough
┌─────────────────────────────┐
│ MANHATTAN    ████████ 25%   │
│ BROOKLYN     ██████ 22%     │
│ QUEENS       ██████ 20%     │
│ BRONX        ██████ 20%     │
│ STATEN IS.   ████ 13%       │
└─────────────────────────────┘
```

### Visual 4: Equity Finding (FLAT LINE)
```
Average Days to Close by Borough
Days │
30.5 ├─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
30.0 ├ Q-B-L-M-S ← Nearly identical!
29.5 └─────────────────────────────────
     Bronx Queens Brooklyn Manhattan SI
```

### Visual 5: Trend Over Time (STABLE)
```
Monthly Complaints 2020-2025
800 ├     ╱╲    ╱╲     ╱╲
700 ├    ╱  ╲  ╱  ╲   ╱  ╲
600 ├────────────────────────
    └─────────────────────────
    2020   2022   2024  2025
    
Key: Stable trend = City managing well
```

---

## GENRE & NARRATIVE STRUCTURE

### What Genre is This?
**Answer**: "Data-Driven, Exploratory Narrative with Explanatory Elements"

### Why Is This Genre Right?
1. **Data-Driven** (Segel & Heer)
   - Story emerges FROM the data patterns
   - Central question: "What does 311 data reveal?"
   - Visualizations show actual statistics, not illustrations

2. **Exploratory Structure**
   - Viewers discover insights alongside us
   - Shows data in progressive layers
   - Builds from simple facts to complex insights

3. **Explanatory Elements**
   - Not just showing data; explaining what it MEANS
   - "More complaints ≠ more problems (it's population density)"
   - "Equal resolution times = fair city governance"

4. **Actionable Insights**
   - Ends with "Here's where to invest"
   - Viewers leave understanding what THIS DATA MEANS for NYC

---

## PRELIMINARY DATA ANALYSIS SUMMARY

### Data Size & Scope
- **Total Records**: 50,000 representative complaints
- **Time Period**: 2020-2025 (5 years, 1,916 days)
- **Geographic Coverage**: All 5 NYC boroughs + 514 community boards
- **Variables**: 10 key fields (date, type, location, status, resolution time, etc.)
- **Data Quality**: 0 missing values - excellent quality

### Distribution Patterns
- **Complaint Types**: 16 categories
  - Top 3 (Heat, Water, Rodent) = 34.8% of all complaints
  - Remaining 13 types = 65.2%
  - Shows concentration in infrastructure issues
  
- **Geographic Distribution**:
  - Manhattan: 25.1% (12,534 complaints)
  - Brooklyn: 21.9% (10,960 complaints)
  - Queens: 20.1% (10,060 complaints)
  - Bronx: 20.0% (10,020 complaints)
  - Staten Island: 12.9% (6,426 complaints)
  - Difference: 12% between highest and lowest
  
- **Temporal Distribution**:
  - Stable year-round (~9,500 complaints/year)
  - Winter spike: 13,680 complaints (28% more than fall)
  - Summer lows: ~11,670 complaints (lowest season)

### Key Statistical Findings
- **Resolution Time**: Average 30.3 days, Median 21 days
  - Range: 1 to 376 days
  - Standard Deviation: 30 days (high variability)
  
- **Status Distribution**:
  - Closed: 64.6% (32,319 complaints)
  - Open: 20.2% (10,086 complaints)
  - In Progress: 15.2% (7,595 complaints)

- **Equity Metrics**:
  - Borough with fastest resolution: Brooklyn (29.9 days mean)
  - Borough with slowest resolution: Bronx/Queens/Staten Island (30.5 days mean)
  - Difference: 0.6 days (no meaningful disparity)

### Seasonal Breakdown
- **Winter** (Dec-Feb): 13,680 complaints (27.4%)
  - Peak: Heat complaints (winter heating demand)
  - Water issues (pipes freeze)
  
- **Spring** (Mar-May): 11,575 complaints (23.2%)
  - Moderate complaint levels
  
- **Summer** (Jun-Aug): 11,670 complaints (23.3%)
  - Lowest season (except fall)
  - AC-related complaints instead of heating
  
- **Fall** (Sep-Nov): 12,995 complaints (26.0%)
  - Rise as heating season approaches

### Why These Stats Matter
1. **Heat dominance** → City needs heating system upgrades
2. **Stable trends** → Urban condition not deteriorating
3. **Fair resolution times** → No geographic bias detected
4. **Seasonal predictability** → City can plan staffing seasonally
5. **Data quality** → Findings are trustworthy

---

## WHY THIS APPROACH WORKS

**Problem Solved**: Viewers understand what 311 data reveals AND why it matters
**Surprising Finding**: Fair service across boroughs (good news about NYC governance)
**Actionable**: City leaders know where to invest resources
**Accessible**: No technical jargon; works for any audience
**Memorable**: Clean narrative arc with clear beginning/middle/end
