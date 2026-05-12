"""
NYC 311 Service Requests - Static Image Generation
Professional, restrained palette: dark charcoal + brick red only
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

try:
    PROJECT_ROOT = Path(__file__).parent.parent
except Exception:
    PROJECT_ROOT = Path.cwd()

DATA_RAW = PROJECT_ROOT / 'data' / 'raw'
DATA_PROCESSED = PROJECT_ROOT / 'data' / 'processed'
IMAGES_DIR = PROJECT_ROOT / 'images'
os.makedirs(IMAGES_DIR, exist_ok=True)

plt.style.use('default')

NAVY  = '#1c2836'
RED   = '#b5431e'
GRAY  = '#606470'
LG    = '#e0e3e8'   # light grid color

def clean_axes(ax, spines=('top', 'right')):
    for s in spines:
        ax.spines[s].set_visible(False)
    ax.spines['left'].set_color(LG)
    ax.spines['bottom'].set_color(LG)
    ax.tick_params(colors=GRAY, labelsize=10)

print("=" * 60)
print("NYC 311 - Image Generation")
print("=" * 60)

print("\n[1] Loading data...")
df = pd.read_csv(DATA_RAW / '311_service_requests.csv')
complaint_analysis = pd.read_csv(DATA_PROCESSED / 'complaint_analysis.csv')
borough_analysis   = pd.read_csv(DATA_PROCESSED / 'borough_analysis.csv')
monthly_volume     = pd.read_csv(DATA_PROCESSED / 'monthly_volume.csv')
df['Created Date'] = pd.to_datetime(df['Created Date'], errors='coerce')
print(f"Loaded {len(df):,} records")

# ── 1. TOP COMPLAINTS ────────────────────────────────────────
print("\n[2] top_complaints.png")
fig, ax = plt.subplots(figsize=(12, 6), facecolor='white')

top = complaint_analysis.head(6)[['Complaint Type', 'Count']].copy()
top['pct'] = (top['Count'] / complaint_analysis['Count'].sum() * 100).round(1)

# Shorten long labels for the axis
LABEL_MAP = {
    'Request Large Bulky Item Collection': 'Bulky Item Pickup',
    'Noise - Street/Sidewalk': 'Noise – Street',
    'UNSANITARY CONDITION': 'Unsanitary Cond.',
}
top['Label'] = top['Complaint Type'].map(lambda x: LABEL_MAP.get(x, x))

bar_colors = [RED] + [NAVY] * (len(top) - 1)
bars = ax.bar(range(len(top)), top['Count'].values,
              color=bar_colors, alpha=0.92, edgecolor='white', linewidth=0.5)

for bar, pct in zip(bars, top['pct'].values):
    ax.text(bar.get_x() + bar.get_width() / 2., bar.get_height() + 400,
            f'{pct:.1f}%', ha='center', va='bottom',
            fontsize=11, fontweight='bold', color=NAVY)

ax.set_xticks(range(len(top)))
ax.set_xticklabels(top['Label'].values, rotation=30, ha='right')
ax.set_ylabel('Number of Complaints', fontsize=12, color=GRAY)
ax.set_title('Noise and Parking Dominate — Heat/Hot Water is the Top Infrastructure Complaint',
             fontsize=13, fontweight='bold', color=NAVY, pad=18)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))
ax.grid(axis='y', alpha=0.35, linestyle='-', color=LG, linewidth=0.8)
ax.set_axisbelow(True)
clean_axes(ax)
plt.tight_layout()
plt.savefig(IMAGES_DIR / 'top_complaints.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("  OK top_complaints.png")

# ── 2. BOROUGH CLEVELAND DOT PLOT ────────────────────────────────────────
print("\n[3] borough_chart.png")
fig, ax = plt.subplots(figsize=(12, 5), facecolor='white')

bor        = borough_analysis.sort_values('Total Complaints', ascending=True).reset_index(drop=True)
y_pos      = list(range(len(bor)))
total_city = bor['Total Complaints'].sum()
mean_val   = bor['Total Complaints'].mean()

for i, row in bor.iterrows():
    ax.hlines(i, 0, row['Total Complaints'],
              color=LG, linewidth=2.5, zorder=1)

dot_colors = [RED if b == bor['Borough'].iloc[-1] else NAVY for b in bor['Borough']]
ax.scatter(bor['Total Complaints'].values, y_pos,
           c=dot_colors, s=160, zorder=3, edgecolor='white', linewidth=1.5)

for i, row in bor.iterrows():
    total    = int(row['Total Complaints'])
    pct      = total / total_city * 100
    avg_days = row['Avg Days to Close']
    open_n   = int(row['Open Cases'])
    ax.text(total + 220, i,
            f"{total:,}  ·  {pct:.0f}% of city  ·  {avg_days:.0f} d avg  ·  {open_n:,} open",
            va='center', ha='left', fontsize=9.5, color=GRAY)

ax.axvline(mean_val, color=GRAY, linewidth=1, linestyle='--', alpha=0.5, zorder=2)
ax.text(mean_val + 100, len(bor) - 0.55, f'avg  {mean_val:,.0f}',
        fontsize=8.5, color=GRAY, va='top', ha='left')

ax.set_yticks(y_pos)
ax.set_yticklabels(bor['Borough'].values, fontsize=11, color=NAVY)
ax.set_xlabel('Number of Complaints (2020–2025)', fontsize=11, color=GRAY)
ax.set_title('Brooklyn Leads in Volume — Resolution Times Consistent Across All Boroughs',
             fontsize=13, fontweight='bold', color=NAVY, pad=18)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))
ax.set_xlim(-300, bor['Total Complaints'].max() * 2.15)
ax.grid(axis='x', alpha=0.3, linestyle='-', color=LG, linewidth=0.8)
ax.set_axisbelow(True)
clean_axes(ax)
plt.tight_layout()
plt.savefig(IMAGES_DIR / 'borough_chart.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("  OK borough_chart.png")

# ── 3. DUAL-AXIS: VOLUME + RESOLUTION TIME ──────────────────
print("\n[4] dual_axis_chart.png")
monthly_res = df.groupby(df['Created Date'].dt.to_period('M')).agg(
    Count   =('Unique ID' if 'Unique ID' in df.columns else df.columns[0], 'count'),
    AvgDays =('Days to Close', 'mean')
).reset_index()
monthly_res.columns = ['Period', 'Count', 'AvgDays']
monthly_res['Date'] = monthly_res['Period'].dt.to_timestamp()
monthly_res = monthly_res.sort_values('Date').reset_index(drop=True)

fig, ax1 = plt.subplots(figsize=(14, 6), facecolor='white')

ax1.plot(monthly_res['Date'], monthly_res['Count'],
         color=NAVY, linewidth=2, marker='o', markersize=3.5,
         label='Monthly complaints')
ax1.set_ylabel('Monthly Complaints', fontsize=12, color=NAVY)
ax1.tick_params(axis='y', labelcolor=NAVY, labelsize=10)
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))

ax2 = ax1.twinx()
ax2.plot(monthly_res['Date'], monthly_res['AvgDays'],
         color=RED, linewidth=2, linestyle='--', marker='s', markersize=4,
         label='Avg resolution (days)', alpha=0.85)
ax2.set_ylabel('Avg Days to Close', fontsize=12, color=RED)
ax2.tick_params(axis='y', labelcolor=RED, labelsize=10)
ax2.set_ylim(monthly_res['AvgDays'].min() * 0.85, monthly_res['AvgDays'].max() * 1.15)

covid_s = pd.to_datetime('2020-03-01')
covid_e = pd.to_datetime('2021-06-01')
ax1.axvspan(covid_s, covid_e, alpha=0.08, color=RED)
ax1.axvline(covid_s, color=RED, linewidth=0.8, linestyle='--', alpha=0.55)
ax1.text(covid_s, monthly_res['Count'].max() * 0.97,
         '  COVID-19', fontsize=9, color=RED, va='top')

l1, la1 = ax1.get_legend_handles_labels()
l2, la2 = ax2.get_legend_handles_labels()
ax1.legend(l1 + l2, la1 + la2, loc='upper left', fontsize=10, frameon=False)

ax1.set_title('Volume Varies Seasonally; Resolution Time Stays Flat Through Everything',
              fontsize=13, fontweight='bold', color=NAVY, pad=18)
ax1.set_xlabel('', fontsize=12, color=GRAY)
ax1.grid(axis='y', alpha=0.2, linestyle='-', color=LG, linewidth=0.8)
ax1.set_axisbelow(True)
ax1.spines['top'].set_visible(False)
ax1.spines['left'].set_color(NAVY)
ax1.spines['bottom'].set_color(LG)

# Show quarterly ticks with month + year labels
ax1.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax1.tick_params(axis='x', colors=GRAY, labelsize=9, rotation=40)
plt.setp(ax1.xaxis.get_majorticklabels(), ha='right')

for s in ['top', 'left', 'bottom']:
    ax2.spines[s].set_visible(False)
ax2.spines['right'].set_color(RED)
# Force integer day ticks on right axis
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0f}d'))

plt.tight_layout()
plt.savefig(IMAGES_DIR / 'dual_axis_chart.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("  OK dual_axis_chart.png")

print("\n" + "=" * 60)
print("ALL IMAGES GENERATED")
print(f"Output: {IMAGES_DIR}")
print("=" * 60)
