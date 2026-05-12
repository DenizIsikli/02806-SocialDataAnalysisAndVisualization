"""
Fetch ~1,008,000 real NYC 311 records sampled evenly across every month 2020-2025.
Strategy: 14,000 records per month × 72 months = 1,008,000 records.
This avoids seasonal bias from yearly-first-N sampling.
Outputs: final_project/data/raw/311_service_requests.csv
"""
import urllib.request, urllib.parse, sys, time, calendar
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).parent.parent
OUT_CSV = PROJECT_ROOT / 'data' / 'raw' / '311_service_requests.csv'

BASE_URL = 'https://data.cityofnewyork.us/resource/erm2-nwe9.csv'
COLS = 'unique_key,created_date,closed_date,complaint_type,descriptor,borough,status,latitude,longitude,community_board'

PER_MONTH = 14_000

# Build month list: Jan 2020 through Dec 2025
months = []
for year in range(2020, 2026):
    for month in range(1, 13):
        last_day = calendar.monthrange(year, month)[1]
        start = f'{year}-{month:02d}-01'
        if month == 12:
            end = f'{year+1}-01-01'
        else:
            end = f'{year}-{month+1:02d}-01'
        months.append((start, end))

def fetch_month(start, end):
    where = f'created_date >= "{start}T00:00:00" AND created_date < "{end}T00:00:00"'
    params = urllib.parse.urlencode({
        '$select': COLS,
        '$where':  where,
        '$order':  'created_date ASC',
        '$limit':  PER_MONTH,
        '$offset': 0,
    })
    url = BASE_URL + '?' + params
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return r.read().decode('utf-8')
        except Exception as e:
            print(f"  Retry {attempt+1}/3: {e}")
            time.sleep(5)
    raise RuntimeError(f"Failed for {start}")

print(f"Fetching ~{PER_MONTH:,} records/month across {len(months)} months (2020-2025)...")
print(f"Target: ~{PER_MONTH * len(months):,} records\n")

total = 0
header_written = False

with open(OUT_CSV, 'w', newline='', encoding='utf-8') as fout:
    for (start, end) in months:
        t0 = time.time()
        raw = fetch_month(start, end)
        lines = raw.strip().splitlines()
        n = max(0, len(lines) - 1)
        if not header_written and len(lines) > 0:
            fout.write(lines[0] + '\n')
            header_written = True
        for line in lines[1:]:
            fout.write(line + '\n')
        total += n
        elapsed = time.time() - t0
        print(f"  {start}  got={n:,}  total={total:,}  ({elapsed:.1f}s)")

print(f"\nDone. {total:,} rows written to {OUT_CSV}")
