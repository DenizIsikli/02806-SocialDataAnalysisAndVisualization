"""
Process raw 311 real data into all required CSVs.
- Renames API columns to names expected by generate_images.py and generate_interactive_charts.py
- Computes Days to Close
- Creates complaint_analysis, borough_analysis, monthly_volume, yearly_trends
- Monthly volume uses REAL API totals (not equal-sample counts) to preserve seasonal variation
"""
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).parent.parent
RAW_DIR  = PROJECT_ROOT / 'data' / 'raw'
PROC_DIR = PROJECT_ROOT / 'data' / 'processed'
PROC_DIR.mkdir(parents=True, exist_ok=True)

print("Loading raw data ...")
df = pd.read_csv(RAW_DIR / '311_service_requests.csv', low_memory=False)
print(f"  {len(df):,} rows loaded")

# ── 1. Rename columns to match downstream scripts ─────────────
df = df.rename(columns={
    'unique_key':      'Unique ID',
    'created_date':    'Created Date',
    'closed_date':     'Closed Date',
    'complaint_type':  'Complaint Type',
    'descriptor':      'Descriptor',
    'borough':         'Borough',
    'status':          'Status',
    'latitude':        'Latitude',
    'longitude':       'Longitude',
    'community_board': 'Community Board',
})

# ── 2. Parse dates & compute Days to Close ────────────────────
df['Created Date'] = pd.to_datetime(df['Created Date'], errors='coerce')
df['Closed Date']  = pd.to_datetime(df['Closed Date'],  errors='coerce')
df['Days to Close'] = (df['Closed Date'] - df['Created Date']).dt.days
# Clip: negative (data error) → NaN; >365 days → NaN for averages
df.loc[df['Days to Close'] < 0, 'Days to Close'] = np.nan
df.loc[df['Days to Close'] > 365, 'Days to Close'] = np.nan

# ── 3. Remove unspecified borough ─────────────────────────────
df = df[~df['Borough'].str.upper().isin(['UNSPECIFIED', ''])]

print(f"  {len(df):,} rows after filtering unspecified borough")

# ── 4. Save processed raw CSV (column names now match scripts) ─
df.to_csv(RAW_DIR / '311_service_requests.csv', index=False)
print("  Saved processed raw CSV with renamed columns + Days to Close")

# ── 5. complaint_analysis.csv ─────────────────────────────────
print("\nBuilding complaint_analysis.csv ...")
ca = df.groupby('Complaint Type').agg(
    Count    =('Unique ID', 'count'),
    Avg_Days =('Days to Close', 'mean'),
    Open_Cases=('Status', lambda x: (x.str.lower() != 'closed').sum()),
).reset_index()
ca['Avg Days'] = ca['Avg_Days'].round(1)
ca['% Open']   = (ca['Open_Cases'] / ca['Count'] * 100).round(1)
ca = ca.rename(columns={'Open_Cases': 'Open Cases'})
ca = ca[['Complaint Type', 'Count', 'Avg Days', 'Open Cases', '% Open']]
ca = ca.sort_values('Count', ascending=False).reset_index(drop=True)
ca.to_csv(PROC_DIR / 'complaint_analysis.csv', index=False)
print(ca.head(10).to_string())

# ── 6. borough_analysis.csv ───────────────────────────────────
print("\nBuilding borough_analysis.csv ...")
BORO_TITLE = {
    'MANHATTAN':     'Manhattan',
    'BROOKLYN':      'Brooklyn',
    'QUEENS':        'Queens',
    'BRONX':         'Bronx',
    'STATEN ISLAND': 'Staten Island',
}
df['Borough_title'] = df['Borough'].str.upper().map(BORO_TITLE)
df_boro = df[df['Borough_title'].notna()]

ba = df_boro.groupby('Borough_title').agg(
    Total_Complaints =('Unique ID', 'count'),
    Avg_Days         =('Days to Close', 'mean'),
    Median_Days      =('Days to Close', 'median'),
    Open_Cases       =('Status', lambda x: (x.str.lower() != 'closed').sum()),
).reset_index()
ba = ba.rename(columns={
    'Borough_title':   'Borough',
    'Total_Complaints':'Total Complaints',
    'Avg_Days':        'Avg Days to Close',
    'Median_Days':     'Median Days',
    'Open_Cases':      'Open Cases',
})
ba['Avg Days to Close'] = ba['Avg Days to Close'].round(1)
ba['Median Days']       = ba['Median Days'].round(1)
ba.to_csv(PROC_DIR / 'borough_analysis.csv', index=False)
print(ba.to_string())

# ── 7. monthly_volume.csv (REAL API totals, not sampled counts) ─
print("\nBuilding monthly_volume.csv from real API totals ...")
real_monthly = {
    '2020-01': 195231, '2020-02': 173162, '2020-03': 179779, '2020-04': 159114,
    '2020-05': 234308, '2020-06': 313305, '2020-07': 316553, '2020-08': 348463,
    '2020-09': 287851, '2020-10': 269520, '2020-11': 233596, '2020-12': 231142,
    '2021-01': 228039, '2021-02': 195978, '2021-03': 249960, '2021-04': 241648,
    '2021-05': 274411, '2021-06': 301378, '2021-07': 303152, '2021-08': 282244,
    '2021-09': 317507, '2021-10': 308312, '2021-11': 269689, '2021-12': 248564,
    '2022-01': 279281, '2022-02': 244234, '2022-03': 251933, '2022-04': 236083,
    '2022-05': 276664, '2022-06': 271730, '2022-07': 294474, '2022-08': 269234,
    '2022-09': 272054, '2022-10': 267072, '2022-11': 246539, '2022-12': 260662,
    '2023-01': 242173, '2023-02': 225002, '2023-03': 251716, '2023-04': 247496,
    '2023-05': 280932, '2023-06': 267168, '2023-07': 289329, '2023-08': 282757,
    '2023-09': 283517, '2023-10': 302769, '2023-11': 280046, '2023-12': 271817,
    '2024-01': 287186, '2024-02': 240436, '2024-03': 266604, '2024-04': 267565,
    '2024-05': 283982, '2024-06': 306200, '2024-07': 298936, '2024-08': 284823,
    '2024-09': 306770, '2024-10': 306803, '2024-11': 293516, '2024-12': 313949,
    '2025-01': 348179, '2025-02': 255364, '2025-03': 281220, '2025-04': 272550,
    '2025-05': 295057, '2025-06': 306436, '2025-07': 315863, '2025-08': 304014,
    '2025-09': 302684, '2025-10': 336612, '2025-11': 304905, '2025-12': 332104,
}
mv = pd.DataFrame(list(real_monthly.items()), columns=['Date', 'Count'])
mv.to_csv(PROC_DIR / 'monthly_volume.csv', index=False)
print(f"  Saved {len(mv)} months of real volume data")

# Also compute seasonal stats
mv['month_num'] = mv['Date'].str[5:7].astype(int)
winter_avg = mv[mv['month_num'].isin([12,1,2])]['Count'].mean()
summer_avg = mv[mv['month_num'].isin([6,7,8])]['Count'].mean()
fall_avg   = mv[mv['month_num'].isin([9,10,11])]['Count'].mean()
spring_avg = mv[mv['month_num'].isin([3,4,5])]['Count'].mean()
print(f"  Seasonal averages — Winter: {winter_avg:,.0f}  Spring: {spring_avg:,.0f}  Summer: {summer_avg:,.0f}  Fall: {fall_avg:,.0f}")
print(f"  Summer vs Winter: +{(summer_avg-winter_avg)/winter_avg*100:.0f}%")

# ── 8. yearly_trends.csv ──────────────────────────────────────
print("\nBuilding yearly_trends.csv ...")
df['Year'] = df['Created Date'].dt.year
yt = df.groupby('Year').agg(
    Annual_Complaints     =('Unique ID', 'count'),
    Avg_Resolution        =('Days to Close', 'mean'),
    Open_Cases            =('Status', lambda x: (x.str.lower() != 'closed').sum()),
).reset_index()
yt['Avg Resolution (days)'] = yt['Avg_Resolution'].round(2)
yt = yt.rename(columns={
    'Annual_Complaints': 'Annual Complaints',
    'Open_Cases':        'Open Cases',
})
yt = yt[['Year', 'Annual Complaints', 'Avg Resolution (days)', 'Open Cases']]
yt.to_csv(PROC_DIR / 'yearly_trends.csv', index=False)
print(yt.to_string())

print("\nAll processed CSVs written to", PROC_DIR)
