"""
NYC 311 - Interactive Charts
1. Borough comparison grouped bar — darker theme colors (borough_comparison.html)
2. Time series with seasonal shading (time_series_interactive.html)
3. Temporal heatmap with year slider starting at 2020 (temporal_heatmap_interactive.html)
4. Borough choropleth map with metric dropdown (geo_heatmap.html)
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

try:
    PROJECT_ROOT = Path(__file__).parent.parent
except Exception:
    PROJECT_ROOT = Path.cwd()

DATA_RAW   = PROJECT_ROOT / 'data' / 'raw'
CHARTS_DIR = PROJECT_ROOT / 'charts'
CHARTS_DIR.mkdir(exist_ok=True)

NAVY = '#1c2836'
RED  = '#b5431e'

print("=" * 60)
print("NYC 311 - Interactive Charts")
print("=" * 60)

print("\n[1] Loading data...")
df = pd.read_csv(DATA_RAW / '311_service_requests.csv')
df['Created Date'] = pd.to_datetime(df['Created Date'], errors='coerce')
df['Year']  = df['Created Date'].dt.year
df['Month'] = df['Created Date'].dt.month
print(f"  Loaded {len(df):,} records")

# ── 1. BOROUGH COMPARISON (grouped bar, darker theme colors) ──
print("\n[2] borough_comparison.html (darker theme, vertical inside text)")

BORO_NORM = {
    'MANHATTAN': 'Manhattan', 'BROOKLYN': 'Brooklyn',
    'QUEENS': 'Queens', 'BRONX': 'Bronx', 'STATEN ISLAND': 'Staten Island',
}
df['Borough_title'] = df['Borough'].str.upper().map(BORO_NORM).fillna(df['Borough'])
boroughs_sorted_bc  = sorted(df['Borough_title'].dropna().unique())

CT_LIST        = ['Illegal Parking', 'Noise - Residential', 'HEAT/HOT WATER']
CT_COLORS_DARK = ['#b5431e', '#1c2836', '#1a4a78']

fig_bc = go.Figure()
for i, ct in enumerate(CT_LIST):
    pcts   = []
    counts = []
    for b in boroughs_sorted_bc:
        bdf      = df[df['Borough_title'] == b]
        ct_count = int((bdf['Complaint Type'] == ct).sum())
        pcts.append(round(ct_count / len(bdf) * 100, 1) if len(bdf) > 0 else 0)
        counts.append(ct_count)
    fig_bc.add_trace(go.Bar(
        name=ct, x=boroughs_sorted_bc, y=pcts,
        text=[f'{p:.1f}%' for p in pcts],
        textposition='inside',
        textangle=-90,
        textfont=dict(size=11, color='white', family='Arial'),
        marker_color=CT_COLORS_DARK[i],
        marker_line_color='white', marker_line_width=0.5,
        customdata=counts,
        hovertemplate='<b>%{x}</b><br>%{fullData.name}: %{y:.1f}% (%{customdata:,} complaints)<extra></extra>',
    ))

fig_bc.update_layout(
    title=dict(
        text='Parking, Noise & Heat — How the Top Complaints Vary by Borough',
        font=dict(size=15, color=NAVY, family='Georgia, serif'),
        x=0.01,
    ),
    barmode='group',
    xaxis_title='Borough',
    yaxis_title='% of Borough Total Complaints',
    font=dict(family='Arial, sans-serif', size=12),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                font=dict(size=12)),
    plot_bgcolor='white',
    paper_bgcolor='white',
    yaxis=dict(gridcolor='rgba(0,0,0,0.08)', tickfont=dict(color=NAVY, size=11)),
    xaxis=dict(tickfont=dict(color=NAVY, size=11)),
    height=480,
    margin=dict(l=70, r=20, t=70, b=60),
)
fig_bc.write_html(
    CHARTS_DIR / 'borough_comparison.html',
    include_plotlyjs='cdn',
    full_html=True,
)
print("  OK borough_comparison.html")

# ── 2. TIME SERIES WITH SEASONAL SHADING ─────────────────────
print("\n[3] time_series_interactive.html (with seasonal shading)")

# Use real monthly totals (not equal-sample counts) for accurate seasonal variation
DATA_PROC = PROJECT_ROOT / 'data' / 'processed'
monthly = pd.read_csv(DATA_PROC / 'monthly_volume.csv')
monthly['Date'] = pd.to_datetime(monthly['Date'] + '-01')
monthly = monthly.sort_values('Date').reset_index(drop=True)

fig_ts = go.Figure()

# Winter shading (Dec–Feb) for each year in the dataset
winters = [
    ('2019-12-01', '2020-03-01'),
    ('2020-12-01', '2021-03-01'),
    ('2021-12-01', '2022-03-01'),
    ('2022-12-01', '2023-03-01'),
    ('2023-12-01', '2024-03-01'),
    ('2024-12-01', '2025-03-01'),
]
for i, (ws, we) in enumerate(winters):
    fig_ts.add_shape(
        type='rect', x0=ws, x1=we, y0=0, y1=1,
        xref='x', yref='paper',
        fillcolor='rgba(181,67,30,0.09)', line_width=0, layer='below',
    )

# Single "Winter" label on the first winter band
fig_ts.add_annotation(
    x='2020-01-01', y=0.96, xref='x', yref='paper',
    text='Winter', showarrow=False,
    font=dict(size=9, color=RED, family='Arial'),
    xanchor='center', yanchor='top',
)

# COVID shading
fig_ts.add_shape(
    type='rect', x0='2020-03-01', x1='2021-07-01', y0=0, y1=1,
    xref='x', yref='paper',
    fillcolor='rgba(100,100,100,0.07)', line_width=0, layer='below',
)
fig_ts.add_annotation(
    x='2020-11-01', y=0.83, xref='x', yref='paper',
    text='COVID-19 period', showarrow=False,
    font=dict(size=9, color='#888', family='Arial'),
    xanchor='center', yanchor='top',
)

# Main complaint volume line
fig_ts.add_trace(go.Scatter(
    x=monthly['Date'], y=monthly['Count'],
    mode='lines+markers',
    name='Monthly Complaints',
    line=dict(color=NAVY, width=2.5),
    marker=dict(size=4),
    hovertemplate='<b>%{x|%B %Y}</b>: %{y:,} complaints<extra></extra>',
))

# Compute seasonal stats for annotation
summer_avg = monthly[monthly['Date'].dt.month.isin([6, 7, 8])]['Count'].mean()
winter_avg = monthly[monthly['Date'].dt.month.isin([12, 1, 2])]['Count'].mean()
pct_above  = (summer_avg - winter_avg) / winter_avg * 100

fig_ts.update_layout(
    title=dict(
        text='Monthly Complaint Volume (2020–2025)',
        font=dict(size=15, color=NAVY, family='Georgia, serif'),
        x=0.01,
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    font=dict(family='Arial, sans-serif', color='#333'),
    xaxis=dict(
        title='',
        tickfont=dict(size=11, color=NAVY),
        gridcolor='rgba(0,0,0,0.06)',
        tickformat='%b %Y',
    ),
    yaxis=dict(
        title='Monthly Complaints',
        tickfont=dict(size=11, color=NAVY),
        gridcolor='rgba(0,0,0,0.08)',
        tickformat=',',
    ),
    hovermode='x unified',
    height=420,
    margin=dict(l=70, r=20, t=55, b=60),
    legend=dict(orientation='h', y=-0.2, x=0.01, font=dict(size=11)),
    annotations=[
        dict(
            x=0.99, y=0.99, xref='paper', yref='paper',
            text=f'Summer avg: +{pct_above:.0f}% above winter baseline',
            showarrow=False,
            font=dict(size=10, color=RED, family='Arial'),
            xanchor='right', yanchor='top',
            bgcolor='rgba(255,255,255,0.85)',
            borderpad=4,
        ),
    ],
)

fig_ts.write_html(
    CHARTS_DIR / 'time_series_interactive.html',
    include_plotlyjs='cdn',
    full_html=True,
)
print("  OK time_series_interactive.html")

# ── 2. TEMPORAL HEATMAP WITH YEAR SLIDER (starts at 2020) ────
print("\n[4] temporal_heatmap_interactive.html (year slider, starts 2020)")

top_types = df['Complaint Type'].value_counts().head(8).index.tolist()
years     = sorted(df['Year'].dropna().astype(int).unique())
months    = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def year_matrix(yr):
    sub = df[df['Year'] == yr]
    return [
        [int(len(sub[(sub['Complaint Type'] == ct) & (sub['Month'] == m)]))
         for m in range(1, 13)]
        for ct in top_types
    ]


# Build one frame per year; each frame also updates the chart title
frames = []
for yr in years:
    mat = year_matrix(yr)
    frames.append(go.Frame(
        data=[go.Heatmap(
            z=mat,
            x=months,
            y=top_types,
            colorscale='Blues',
            showscale=True,
            colorbar=dict(title='Complaints', tickfont=dict(size=10)),
            text=[[str(v) for v in row] for row in mat],
            texttemplate='%{text}',
            textfont=dict(size=9),
            hovertemplate='%{y}<br>%{x}: %{z} complaints<extra></extra>',
            zmin=0,
        )],
        layout=go.Layout(
            title=dict(text=f'When Do Different Problems Peak? — {yr}'),
        ),
        name=str(yr),
    ))

# Start at 2020
start_idx = years.index(2020) if 2020 in years else 0
init_mat  = year_matrix(years[start_idx])

slider_steps = [
    dict(
        args=[[str(yr)], dict(frame=dict(duration=400, redraw=True), mode='immediate')],
        label=str(yr),
        method='animate',
    )
    for yr in years
]

fig_hm = go.Figure(
    data=[go.Heatmap(
        z=init_mat,
        x=months,
        y=top_types,
        colorscale='Blues',
        showscale=True,
        colorbar=dict(title='Complaints', tickfont=dict(size=10)),
        text=[[str(v) for v in row] for row in init_mat],
        texttemplate='%{text}',
        textfont=dict(size=9),
        hovertemplate='%{y}<br>%{x}: %{z} complaints<extra></extra>',
        zmin=0,
    )],
    frames=frames,
)

fig_hm.update_layout(
    title=dict(
        text=f'When Do Different Problems Peak? — {years[start_idx]}',
        font=dict(size=15, color=NAVY, family='Georgia, serif'),
        x=0.01,
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=140, r=20, t=60, b=120),
    font=dict(family='Arial, sans-serif', color='#333'),
    xaxis=dict(title='Month', tickfont=dict(size=11, color=NAVY)),
    yaxis=dict(title='', tickfont=dict(size=11, color=NAVY, family='Arial Black')),
    sliders=[dict(
        active=start_idx,
        currentvalue=dict(prefix='Year: ', font=dict(size=13, color=NAVY)),
        pad=dict(t=50, b=10),
        steps=slider_steps,
        bgcolor='#f0f0f0',
        bordercolor='#ccc',
        tickcolor=NAVY,
    )],
    updatemenus=[dict(
        type='buttons',
        showactive=False,
        y=0,
        x=1.05,
        xanchor='right',
        yanchor='top',
        buttons=[
            dict(label='Play', method='animate',
                 args=[None, dict(frame=dict(duration=800, redraw=True),
                                  fromcurrent=True, mode='immediate')]),
            dict(label='Pause', method='animate',
                 args=[[None], dict(frame=dict(duration=0, redraw=False),
                                    mode='immediate')]),
        ],
    )],
    height=480,
)

fig_hm.write_html(
    CHARTS_DIR / 'temporal_heatmap_interactive.html',
    include_plotlyjs='cdn',
    full_html=True,
)
print("  OK temporal_heatmap_interactive.html")

# ── 3. BOROUGH CHOROPLETH ─────────────────────────────────────
print("\n[5] geo_heatmap.html (Plotly choropleth by borough)")

# Borough name mapping: data UPPERCASE → GeoJSON TitleCase
BORO_MAP = {
    'MANHATTAN':     'Manhattan',
    'BROOKLYN':      'Brooklyn',
    'QUEENS':        'Queens',
    'BRONX':         'Bronx',
    'STATEN ISLAND': 'Staten Island',
}

df['borough_title'] = df['Borough'].str.upper().map(BORO_MAP)

# Total complaints per borough
counts = df['borough_title'].value_counts().reset_index()
counts.columns = ['borough', 'total']

# Average resolution time per borough
res = df.groupby('borough_title')['Days to Close'].mean().round(1).reset_index()
res.columns = ['borough', 'avg_days']
counts = counts.merge(res, on='borough', how='left')

# Heat/Hot Water complaints per borough
heat_ct = (
    df[df['Complaint Type'] == 'HEAT/HOT WATER']
    .groupby('borough_title')
    .size()
    .reset_index(name='heat_count')
)
heat_ct.columns = ['borough', 'heat_count']
counts = counts.merge(heat_ct, on='borough', how='left').fillna(0)

# Fetch NYC borough boundaries from Plotly's stable US-counties dataset
# NYC FIPS codes: Bronx=36005, Brooklyn(Kings)=36047, Manhattan(NY)=36061,
#                 Queens=36081, Staten Island(Richmond)=36085
BOROUGH_FIPS = {
    'Manhattan':     '36061',
    'Brooklyn':      '36047',
    'Queens':        '36081',
    'Bronx':         '36005',
    'Staten Island': '36085',
}
FIPS_TO_BORO = {v: k for k, v in BOROUGH_FIPS.items()}

GEO_URL = (
    'https://raw.githubusercontent.com/plotly/datasets/master/'
    'geojson-counties-fips.json'
)
borough_geojson = None
try:
    resp = requests.get(GEO_URL, timeout=20)
    resp.raise_for_status()
    all_counties = resp.json()
    nyc_fips = set(BOROUGH_FIPS.values())
    nyc_features = [f for f in all_counties['features'] if f['id'] in nyc_fips]
    for f in nyc_features:
        f['properties']['BoroName'] = FIPS_TO_BORO[f['id']]
    borough_geojson = {'type': 'FeatureCollection', 'features': nyc_features}
    print(f"  Fetched NYC borough GeoJSON ({len(nyc_features)} features)")
except Exception as e:
    print(f"  GeoJSON fetch failed ({e}); falling back to bubble map")

if borough_geojson:
    # Three metrics available via dropdown
    metrics = [
        ('total',      'Total Complaints (2020–2025)', 'Blues',   ',d'),
        ('heat_count', 'Heat/Hot Water Complaints (2020–2025)', 'Oranges', ',d'),
        ('avg_days',   'Avg. Resolution Time (days)',  'Greens',  '.1f'),
    ]

    traces = []
    for col, label, cscale, fmt in metrics:
        traces.append(go.Choroplethmapbox(
            geojson=borough_geojson,
            locations=counts['borough'],
            z=counts[col],
            featureidkey='properties.BoroName',
            colorscale=cscale,
            zmin=0,
            zmax=counts[col].max(),
            text=counts['borough'],
            customdata=counts[col],
            hovertemplate=(
                '<b>%{text}</b><br>'
                f'{label}: %{{customdata:{fmt}}}<extra></extra>'
            ),
            showscale=True,
            colorbar=dict(
                title=dict(text=label, font=dict(size=11, color=NAVY)),
                tickfont=dict(size=10, color=NAVY),
                len=0.75,
            ),
            visible=False,
            marker_opacity=0.78,
            marker_line_width=1,
            marker_line_color='white',
        ))
    traces[0].visible = True

    buttons = []
    for i, (_, label, _, _) in enumerate(metrics):
        vis = [j == i for j in range(len(metrics))]
        buttons.append(dict(
            label=label,
            method='update',
            args=[{'visible': vis},
                  {'title.text': f'NYC 311 — {label}'}],
        ))

    fig_ch = go.Figure(data=traces)
    fig_ch.update_layout(
        title=dict(
            text=f'NYC 311 — {metrics[0][1]}',
            font=dict(size=15, color=NAVY, family='Georgia, serif'),
            x=0.01,
        ),
        mapbox_style='carto-positron',
        mapbox_zoom=9,
        mapbox_center={'lat': 40.72, 'lon': -74.00},
        margin=dict(l=0, r=0, t=55, b=10),
        paper_bgcolor='white',
        height=500,
        updatemenus=[dict(
            type='dropdown',
            direction='down',
            x=0.99, y=0.99,
            xanchor='right', yanchor='top',
            showactive=True,
            bgcolor='white',
            bordercolor='#ccc',
            font=dict(size=12, color=NAVY),
            buttons=buttons,
        )],
    )
    fig_ch.write_html(
        CHARTS_DIR / 'geo_heatmap.html',
        include_plotlyjs='cdn',
        full_html=True,
    )
    print("  OK geo_heatmap.html (choropleth)")

else:
    # Fallback: proportional bubble map on borough centroids
    centroids = {
        'Manhattan':    (40.7831, -73.9712),
        'Brooklyn':     (40.6501, -73.9496),
        'Queens':       (40.7282, -73.7949),
        'Bronx':        (40.8448, -73.8648),
        'Staten Island': (40.5795, -74.1502),
    }
    counts['lat'] = counts['borough'].map(lambda b: centroids.get(b, (0, 0))[0])
    counts['lon'] = counts['borough'].map(lambda b: centroids.get(b, (0, 0))[1])

    fig_ch = go.Figure(go.Scattermapbox(
        lat=counts['lat'], lon=counts['lon'],
        text=counts['borough'],
        customdata=counts['total'],
        mode='markers',
        marker=dict(
            size=counts['total'] / counts['total'].max() * 60 + 20,
            color=counts['total'],
            colorscale='Blues',
            showscale=True,
            colorbar=dict(title='Complaints'),
        ),
        hovertemplate='<b>%{text}</b><br>Complaints: %{customdata:,}<extra></extra>',
    ))
    fig_ch.update_layout(
        mapbox_style='carto-positron',
        mapbox_zoom=9,
        mapbox_center={'lat': 40.72, 'lon': -74.00},
        margin=dict(l=0, r=0, t=55, b=10),
        height=500,
        title=dict(
            text='NYC 311 Complaints by Borough',
            font=dict(size=15, color=NAVY, family='Georgia, serif'),
            x=0.01,
        ),
        paper_bgcolor='white',
    )
    fig_ch.write_html(
        CHARTS_DIR / 'geo_heatmap.html',
        include_plotlyjs='cdn',
        full_html=True,
    )
    print("  OK geo_heatmap.html (bubble fallback)")

# ── 5. TOP COMPLAINTS INTERACTIVE (hoverable bar) ────────────
print("\n[6] top_complaints_interactive.html")

complaint_analysis = pd.read_csv(DATA_PROC / 'complaint_analysis.csv')
top6 = complaint_analysis.head(6).copy()

LABEL_MAP = {
    'Request Large Bulky Item Collection': 'Bulky Item Pickup',
    'Noise - Street/Sidewalk': 'Noise – Street',
    'UNSANITARY CONDITION': 'Unsanitary Cond.',
}
top6['Label'] = top6['Complaint Type'].map(lambda x: LABEL_MAP.get(x, x))
top6['pct'] = (top6['Count'] / complaint_analysis['Count'].sum() * 100).round(2)

bar_colors = [RED] + [NAVY] * (len(top6) - 1)

fig_tc = go.Figure(go.Bar(
    x=top6['Label'],
    y=top6['Count'],
    marker_color=bar_colors,
    marker_line_color='white',
    marker_line_width=0.5,
    text=[f'{p:.1f}%' for p in top6['pct']],
    textposition='outside',
    textfont=dict(size=12, color=NAVY, family='Arial'),
    customdata=top6[['Count', 'pct']].values,
    hovertemplate=(
        '<b>%{x}</b><br>'
        'Complaints: <b>%{customdata[0]:,}</b><br>'
        'Share of all calls: <b>%{customdata[1]:.2f}%</b>'
        '<extra></extra>'
    ),
))
fig_tc.update_layout(
    title=dict(
        text='Noise and Parking Dominate — Heat/Hot Water is the Top Infrastructure Complaint',
        font=dict(size=14, color=NAVY, family='Georgia, serif'),
        x=0.01,
    ),
    yaxis=dict(
        title='Number of Complaints',
        tickformat=',',
        gridcolor='rgba(0,0,0,0.07)',
        tickfont=dict(color=NAVY, size=11),
        title_font=dict(color='#606470', size=12),
    ),
    xaxis=dict(tickfont=dict(color=NAVY, size=11)),
    paper_bgcolor='white',
    plot_bgcolor='white',
    height=500,
    margin=dict(l=80, r=20, t=100, b=80),
    showlegend=False,
)
fig_tc.write_html(
    CHARTS_DIR / 'top_complaints_interactive.html',
    include_plotlyjs='cdn',
    full_html=True,
)
print("  OK top_complaints_interactive.html")

# ── 6. DUAL-AXIS INTERACTIVE (real monthly totals + sample avg_days) ──
print("\n[7] dual_axis_interactive.html")

monthly_vol = pd.read_csv(DATA_PROC / 'monthly_volume.csv')
monthly_vol['Date'] = pd.to_datetime(monthly_vol['Date'] + '-01')

monthly_days_da = (
    df.groupby(df['Created Date'].dt.to_period('M'))['Days to Close']
    .mean()
    .reset_index()
)
monthly_days_da.columns = ['Period', 'AvgDays']
monthly_days_da['Date'] = monthly_days_da['Period'].dt.to_timestamp()

monthly_da = monthly_vol.merge(monthly_days_da[['Date', 'AvgDays']], on='Date', how='left')
monthly_da = monthly_da.sort_values('Date').reset_index(drop=True)

fig_da = go.Figure()

fig_da.add_shape(
    type='rect', x0='2020-03-01', x1='2021-07-01', y0=0, y1=1,
    xref='x', yref='paper',
    fillcolor='rgba(100,100,100,0.07)', line_width=0, layer='below',
)
fig_da.add_annotation(
    x='2020-11-01', y=0.97, xref='x', yref='paper',
    text='COVID-19 period', showarrow=False,
    font=dict(size=9, color='#888', family='Arial'),
    xanchor='center', yanchor='top',
)

fig_da.add_trace(go.Scatter(
    x=monthly_da['Date'],
    y=monthly_da['Count'],
    name='Monthly Complaints',
    mode='lines+markers',
    line=dict(color=NAVY, width=2.5),
    marker=dict(size=4),
    yaxis='y1',
    hovertemplate='<b>%{x|%B %Y}</b><br>Complaints: %{y:,}<extra></extra>',
))

fig_da.add_trace(go.Scatter(
    x=monthly_da['Date'],
    y=monthly_da['AvgDays'].round(1),
    name='Avg Resolution (days)',
    mode='lines+markers',
    line=dict(color=RED, width=2, dash='dash'),
    marker=dict(size=4, symbol='square'),
    yaxis='y2',
    hovertemplate='<b>%{x|%B %Y}</b><br>Avg resolution: %{y:.1f} days<extra></extra>',
))

fig_da.update_layout(
    title=dict(
        text='Volume Varies Seasonally; Resolution Time Stays Flat Through Everything',
        font=dict(size=14, color=NAVY, family='Georgia, serif'),
        x=0.01,
    ),
    yaxis=dict(
        title=dict(text='Monthly Complaints', font=dict(color=NAVY, size=12)),
        tickformat=',',
        tickfont=dict(color=NAVY, size=11),
        gridcolor='rgba(0,0,0,0.07)',
        side='left',
    ),
    yaxis2=dict(
        title=dict(text='Avg Days to Close', font=dict(color=RED, size=12)),
        overlaying='y',
        side='right',
        tickfont=dict(color=RED, size=11),
        showgrid=False,
        tickformat='.0f',
        range=[
            monthly_da['AvgDays'].min() * 0.85,
            monthly_da['AvgDays'].max() * 1.15,
        ],
    ),
    legend=dict(
        orientation='h', x=0.01, y=1.02, xanchor='left', yanchor='bottom',
        font=dict(size=11),
    ),
    hovermode='x unified',
    paper_bgcolor='white',
    plot_bgcolor='white',
    height=420,
    margin=dict(l=80, r=80, t=70, b=60),
)
fig_da.write_html(
    CHARTS_DIR / 'dual_axis_interactive.html',
    include_plotlyjs='cdn',
    full_html=True,
)
print("  OK dual_axis_interactive.html")

# ── 7. ANIMATED DENSITY HEATMAP BY YEAR ───────────────────────
print("\n[8] density_heatmap_animated.html")

import plotly.express as px

df_ll = df[df['Latitude'].notna() & df['Longitude'].notna()].copy()
df_ll['Year'] = df_ll['Created Date'].dt.year.astype(int)

sampled_parts = []
for yr in sorted(df_ll['Year'].unique()):
    yr_sub = df_ll[df_ll['Year'] == yr].sample(
        min(8000, len(df_ll[df_ll['Year'] == yr])), random_state=42
    )
    sampled_parts.append(yr_sub)
df_density = pd.concat(sampled_parts, ignore_index=True)
df_density['Year'] = df_density['Year'].astype(str)
df_density['Borough'] = df_density['Borough'].fillna('Unknown')

fig_density = px.density_mapbox(
    df_density,
    lat='Latitude',
    lon='Longitude',
    animation_frame='Year',
    hover_name='Complaint Type',
    hover_data={'Latitude': False, 'Longitude': False, 'Year': False, 'Borough': True},
    radius=5,
    color_continuous_scale=px.colors.sequential.Inferno,
    opacity=0.75,
)
fig_density.update_layout(
    title=dict(
        text='Where Complaints Cluster — Animated by Year (2020–2025)',
        font=dict(size=15, color=NAVY, family='Georgia, serif'),
        x=0.01,
    ),
    mapbox_style='carto-positron',
    mapbox_zoom=9.5,
    mapbox_center={'lat': 40.7128, 'lon': -74.0060},
    coloraxis_showscale=False,
    height=580,
    margin=dict(l=0, r=0, t=60, b=0),
    paper_bgcolor='white',
    font=dict(family='Arial, sans-serif'),
)
fig_density.write_html(
    CHARTS_DIR / 'density_heatmap_animated.html',
    include_plotlyjs='cdn',
    full_html=True,
)
print("  OK density_heatmap_animated.html")

print("\n" + "=" * 60)
print("ALL INTERACTIVE CHARTS GENERATED")
print(f"Output: {CHARTS_DIR}")
print("=" * 60)
