"""
Generate heatmap data for NYC 311 analysis website
Creates borough complaint profiles and temporal heatmaps
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path

# Load the dataset
data_path = Path(__file__).parent.parent / "data" / "raw" / "311_service_requests.csv"
df = pd.read_csv(data_path)

# Ensure Created Date is datetime
df['Created Date'] = pd.to_datetime(df['Created Date'])

# ===== BOROUGH-SPECIFIC COMPLAINT PROFILES =====
borough_complaints = {}
for borough in df['Borough'].unique():
    borough_data = df[df['Borough'] == borough]
    top_complaints = borough_data['Complaint Type'].value_counts().head(5)
    borough_complaints[borough] = {
        'complaints': top_complaints.to_dict(),
        'percentages': (top_complaints / len(borough_data) * 100).round(1).to_dict(),
        'total': len(borough_data)
    }

# ===== TEMPORAL HEATMAP DATA (Complaint Type x Month) =====
df['Month'] = df['Created Date'].dt.month
df['Month_Name'] = df['Created Date'].dt.month_name()

# Create matrix: rows = complaint types, columns = months
months = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']
complaint_types = df['Complaint Type'].value_counts().head(10).index.tolist()

temporal_matrix = []
for complaint_type in complaint_types:
    row = []
    complaint_data = df[df['Complaint Type'] == complaint_type]
    for month in range(1, 13):
        count = len(complaint_data[complaint_data['Month'] == month])
        row.append(count)
    temporal_matrix.append({
        'complaint_type': complaint_type,
        'monthly_values': row
    })

# ===== GEOGRAPHIC HEATMAP DATA (Community Board Level) =====
# Normalize complaints by population estimates for community boards
community_board_stats = []
for cb in df['Community Board'].unique():
    cb_data = df[df['Community Board'] == cb]
    community_board_stats.append({
        'community_board': int(cb),
        'total_complaints': len(cb_data),
        'top_complaint': cb_data['Complaint Type'].value_counts().index[0],
        'avg_resolution_days': cb_data['Days to Close'].mean().round(1),
        'resolution_std': cb_data['Days to Close'].std().round(1)
    })

community_board_stats = sorted(community_board_stats, key=lambda x: x['total_complaints'], reverse=True)

# ===== GEOGRAPHIC DISTRIBUTION WITH COORDINATES =====
geo_data = []
for idx, row in df.iterrows():
    geo_data.append({
        'lat': row['Latitude'],
        'lon': row['Longitude'],
        'complaint_type': row['Complaint Type'],
        'borough': row['Borough'],
        'resolution_days': row['Days to Close']
    })

# Save all data as JSON
output_dir = Path(__file__).parent.parent / "data" / "processed" / "heatmaps"
output_dir.mkdir(parents=True, exist_ok=True)

# Save borough profiles
with open(output_dir / "borough_profiles.json", "w") as f:
    json.dump(borough_complaints, f, indent=2)

# Save temporal heatmap
with open(output_dir / "temporal_heatmap.json", "w") as f:
    json.dump(temporal_matrix, f, indent=2)

# Save community board stats
with open(output_dir / "community_board_stats.json", "w") as f:
    json.dump(community_board_stats[:50], f, indent=2)  # Top 50

# Save geographic data (sample for performance)
geo_sample = geo_data[::10]  # Every 10th record to reduce file size
with open(output_dir / "geographic_data.json", "w") as f:
    json.dump(geo_sample, f, indent=2)

print("✓ Borough profiles generated")
print("✓ Temporal heatmap data generated")
print("✓ Community board statistics generated")
print("✓ Geographic data generated")
print(f"\nAll data saved to: {output_dir}")
