#!/usr/bin/env python3
"""Quick analysis for Challenge 1 demo"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats

print("="*70)
print("CHALLENGE 1: QUICK ANALYSIS (Sample Data)")
print("="*70)

# Paths
data_dir = Path("data")
viz_dir = Path("visualizations")
viz_dir.mkdir(exist_ok=True)

# Load sample
print("\n[1/5] Loading sample data (500k rows)...")
df = pd.read_csv(data_dir / "raw" / "wefarm_dataset.csv", nrows=500000)
print(f"Loaded {len(df):,} rows")

# Parse dates with mixed format
print("\n[2/5] Parsing dates...")
df['question_date'] = pd.to_datetime(df['question_sent'], format='mixed', utc=True)
df['date'] = df['question_date'].dt.date

# Filter countries
df = df[df['question_user_country_code'].isin(['ke', 'ug', 'tz'])]
print(f"Filtered to KE/UG/TZ: {len(df):,} rows")
print(f"Date range: {df['question_date'].min()} to {df['question_date'].max()}")

# Aggregate
print("\n[3/5] Aggregating by day...")
daily = df.groupby(['date', 'question_user_country_code']).size().reset_index(name='question_count')
print(f"Daily aggregation: {len(daily)} day-country combinations")

# Save
(data_dir / "processed").mkdir(parents=True, exist_ok=True)
daily.to_csv(data_dir / "processed" / "questions_daily_sample.csv", index=False)

# Load weather data
print("\n[4/5] Loading weather data...")
weather_kenya = pd.read_csv(data_dir / "raw" / "weather_kenya.csv", index_col=0, parse_dates=True)
print(f"Kenya weather: {len(weather_kenya)} days")

# Merge Kenya data
kenya_questions = daily[daily['question_user_country_code'] == 'ke'].copy()
kenya_questions['date'] = pd.to_datetime(kenya_questions['date'])
weather_kenya_reset = weather_kenya.reset_index()
weather_kenya_reset.columns = ['date'] + list(weather_kenya_reset.columns[1:])
weather_kenya_reset['date'] = pd.to_datetime(weather_kenya_reset['date'])

merged = kenya_questions.merge(weather_kenya_reset, on='date', how='inner')
print(f"Merged Kenya data: {len(merged)} days")

# Calculate correlation
if len(merged) > 10:
    corr, p_val = stats.pearsonr(merged['question_count'], merged['PRECTOTCORR'])
    print(f"\nCorrelation (Questions vs Rainfall): r={corr:.3f}, p={p_val:.4f}")

# Visualizations
print("\n[5/5] Creating visualizations...")

# Viz 1: Questions over time
plt.figure(figsize=(14, 6))
for country in ['ke', 'ug', 'tz']:
    country_data = daily[daily['question_user_country_code'] == country].copy()
    country_data['date'] = pd.to_datetime(country_data['date'])
    country_data = country_data.sort_values('date')
    plt.plot(country_data['date'], country_data['question_count'], 
             label=country.upper(), alpha=0.7, marker='o', markersize=3)

plt.xlabel('Date')
plt.ylabel('Question Count')
plt.title('Farmer Questions Over Time (Sample: First 500k rows)')
plt.legend()
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(viz_dir / 'demo_01_questions_over_time.png', dpi=300, bbox_inches='tight')
print("  ✓ demo_01_questions_over_time.png")
plt.close()

# Viz 2: Kenya questions vs rainfall
if len(merged) > 0:
    fig, ax1 = plt.subplots(figsize=(14, 6))
    
    ax1.plot(merged['date'], merged['question_count'], 
            color='blue', marker='o', markersize=4, label='Questions', alpha=0.7)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Question Count', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.grid(True, alpha=0.3)
    
    ax2 = ax1.twinx()
    ax2.bar(merged['date'], merged['PRECTOTCORR'], 
           color='green', alpha=0.3, width=0.8, label='Rainfall')
    ax2.set_ylabel('Rainfall (mm/day)', color='green')
    ax2.tick_params(axis='y', labelcolor='green')
    
    plt.title(f'Kenya: Question Volume vs Rainfall (r={corr:.3f}, p={p_val:.4f})')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(viz_dir / 'demo_02_kenya_questions_vs_rainfall.png', dpi=300, bbox_inches='tight')
    print("  ✓ demo_02_kenya_questions_vs_rainfall.png")
    plt.close()

# Viz 3: Weather patterns
fig, axes = plt.subplots(3, 1, figsize=(14, 10))
weather_files = [
    ('kenya', 'ke'),
    ('uganda', 'ug'),
    ('tanzania', 'tz')
]

for idx, (country_name, country_code) in enumerate(weather_files):
    weather_file = data_dir / "raw" / f"weather_{country_name}.csv"
    if weather_file.exists():
        df_weather = pd.read_csv(weather_file, index_col=0, parse_dates=True)
        axes[idx].plot(df_weather.index, df_weather['PRECTOTCORR'], 
                      color='blue', alpha=0.6, linewidth=0.8)
        axes[idx].set_title(f'{country_name.upper()}: Daily Precipitation (2015-2022)')
        axes[idx].set_ylabel('Rainfall (mm/day)')
        axes[idx].grid(True, alpha=0.3)
        if idx == 2:
            axes[idx].set_xlabel('Date')

plt.tight_layout()
plt.savefig(viz_dir / 'demo_03_weather_patterns.png', dpi=300, bbox_inches='tight')
print("  ✓ demo_03_weather_patterns.png")
plt.close()

# Summary
print("\n" + "="*70)
print("✓ QUICK ANALYSIS COMPLETE!")
print("="*70)
print(f"\nDataset Summary:")
print(f"  - Sample size: 500,000 rows")
print(f"  - Countries: {df['question_user_country_code'].value_counts().to_dict()}")
print(f"  - Languages: {df['question_language'].value_counts().to_dict()}")
print(f"  - Date range: {df['question_date'].min()} to {df['question_date'].max()}")
print(f"\nWeather Data:")
print(f"  - Kenya: 2,922 days (2015-2022)")
print(f"  - Uganda: 2,922 days (2015-2022)")
print(f"  - Tanzania: 2,922 days (2015-2022)")
print(f"\nKey Finding:")
print(f"  - Questions vs Rainfall correlation: r={corr:.3f} (p={p_val:.4f})")
print(f"\nFiles created:")
print(f"  - {data_dir / 'processed' / 'questions_daily_sample.csv'}")
print(f"  - {viz_dir / 'demo_01_questions_over_time.png'}")
print(f"  - {viz_dir / 'demo_02_kenya_questions_vs_rainfall.png'}")
print(f"  - {viz_dir / 'demo_03_weather_patterns.png'}")
print("\n" + "="*70)
