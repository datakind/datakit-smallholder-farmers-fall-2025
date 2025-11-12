#!/usr/bin/env python3
"""
Challenge 1: Weather Patterns - Full Analysis

This script performs the complete analysis correlating weather patterns with farmer questions.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats
from datetime import datetime
import json

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Paths
script_dir = Path(__file__).parent
project_dir = script_dir.parent
data_dir = project_dir / "data"
viz_dir = project_dir / "visualizations"
viz_dir.mkdir(exist_ok=True)

print("="*70)
print("CHALLENGE 1: WEATHER PATTERNS ANALYSIS")
print("="*70)

# ============================================================================
# STEP 1: Load and Process Question Data
# ============================================================================
print("\n[1/6] Loading question data...")
df = pd.read_csv(data_dir / "raw" / "wefarm_dataset.csv")
print(f"Loaded {len(df):,} question-response pairs")

# Parse timestamps
df['question_date'] = pd.to_datetime(df['question_sent'])
df['question_year'] = df['question_date'].dt.year
df['question_month'] = df['question_date'].dt.month
df['question_day'] = df['question_date'].dt.date

print(f"Date range: {df['question_date'].min()} to {df['question_date'].max()}")

# Filter to countries with weather data
df = df[df['question_user_country_code'].isin(['ke', 'ug', 'tz'])]
print(f"Filtered to Kenya/Uganda/Tanzania: {len(df):,} rows")

# ============================================================================
# STEP 2: Aggregate Questions by Day and Country
# ============================================================================
print("\n[2/6] Aggregating questions by day and country...")

# Daily aggregation
daily_questions = df.groupby(['question_day', 'question_user_country_code']).agg({
    'question_id': 'count'
}).rename(columns={'question_id': 'question_count'}).reset_index()

print(f"Created daily aggregation: {len(daily_questions)} day-country combinations")

# Topic-based aggregation (if topics exist)
if 'question_topic' in df.columns:
    # Get top topics
    top_topics = df['question_topic'].value_counts().head(10).index.tolist()
    
    # Create topic columns
    for topic in top_topics:
        topic_col = f'topic_{topic}'
        daily_topic = df[df['question_topic'] == topic].groupby(
            ['question_day', 'question_user_country_code']
        ).size().reset_index(name=topic_col)
        
        daily_questions = daily_questions.merge(
            daily_topic, 
            on=['question_day', 'question_user_country_code'],
            how='left'
        )
        daily_questions[topic_col] = daily_questions[topic_col].fillna(0)
    
    print(f"Added {len(top_topics)} topic columns")

# Save processed data
output_file = data_dir / "processed" / "questions_daily_by_country.csv"
output_file.parent.mkdir(parents=True, exist_ok=True)
daily_questions.to_csv(output_file, index=False)
print(f"Saved to: {output_file}")

# ============================================================================
# STEP 3: Load Weather Data
# ============================================================================
print("\n[3/6] Loading weather data...")

weather_data = {}
country_map = {'kenya': 'ke', 'uganda': 'ug', 'tanzania': 'tz'}

for country_name, country_code in country_map.items():
    weather_file = data_dir / "raw" / f"weather_{country_name}.csv"
    if weather_file.exists():
        df_weather = pd.read_csv(weather_file, index_col=0, parse_dates=True)
        df_weather['country_code'] = country_code
        df_weather['date'] = df_weather.index.date
        weather_data[country_code] = df_weather
        print(f"  {country_name.upper()}: {len(df_weather)} days")

# ============================================================================
# STEP 4: Merge Questions and Weather Data
# ============================================================================
print("\n[4/6] Merging questions with weather data...")

merged_data = []
for country_code, df_weather in weather_data.items():
    # Get questions for this country
    country_questions = daily_questions[
        daily_questions['question_user_country_code'] == country_code
    ].copy()
    
    # Merge with weather
    country_questions['question_day'] = pd.to_datetime(country_questions['question_day'])
    df_weather_reset = df_weather.reset_index()
    df_weather_reset['date'] = pd.to_datetime(df_weather_reset['date'])
    
    merged = country_questions.merge(
        df_weather_reset,
        left_on='question_day',
        right_on='date',
        how='inner'
    )
    
    merged_data.append(merged)
    print(f"  {country_code.upper()}: {len(merged)} matched days")

merged_df = pd.concat(merged_data, ignore_index=True)
print(f"Total merged records: {len(merged_df)}")

# Save merged data
merged_output = data_dir / "processed" / "questions_weather_merged.csv"
merged_df.to_csv(merged_output, index=False)
print(f"Saved merged data to: {merged_output}")

# ============================================================================
# STEP 5: Calculate Correlations
# ============================================================================
print("\n[5/6] Calculating correlations...")

weather_vars = ['T2M', 'T2M_MAX', 'T2M_MIN', 'PRECTOTCORR', 'RH2M', 'WS2M']
question_vars = ['question_count']

# Add topic columns if they exist
topic_cols = [col for col in merged_df.columns if col.startswith('topic_')]
question_vars.extend(topic_cols)

correlations = {}
for q_var in question_vars:
    correlations[q_var] = {}
    for w_var in weather_vars:
        if q_var in merged_df.columns and w_var in merged_df.columns:
            valid_data = merged_df[[q_var, w_var]].dropna()
            if len(valid_data) > 10:
                corr, p_val = stats.pearsonr(valid_data[q_var], valid_data[w_var])
                correlations[q_var][w_var] = {
                    'correlation': float(corr),
                    'p_value': float(p_val),
                    'significant': p_val < 0.05,
                    'n': len(valid_data)
                }

# Save correlations
corr_output = data_dir / "processed" / "correlations.json"
with open(corr_output, 'w') as f:
    json.dump(correlations, f, indent=2)
print(f"Saved correlations to: {corr_output}")

# Print top correlations
print("\nTop Correlations:")
all_corrs = []
for q_var, w_corrs in correlations.items():
    for w_var, stats_dict in w_corrs.items():
        all_corrs.append((
            q_var, w_var, 
            stats_dict['correlation'], 
            stats_dict['p_value'],
            stats_dict['significant']
        ))

all_corrs.sort(key=lambda x: abs(x[2]), reverse=True)
for i, (q_var, w_var, corr, p_val, sig) in enumerate(all_corrs[:10], 1):
    sig_marker = "***" if sig else ""
    print(f"  {i}. {q_var} vs {w_var}: r={corr:.3f} (p={p_val:.4f}) {sig_marker}")

# ============================================================================
# STEP 6: Create Visualizations
# ============================================================================
print("\n[6/6] Creating visualizations...")

# Viz 1: Questions over time
plt.figure(figsize=(14, 6))
for country_code in ['ke', 'ug', 'tz']:
    country_data = daily_questions[
        daily_questions['question_user_country_code'] == country_code
    ].sort_values('question_day')
    plt.plot(country_data['question_day'], 
             country_data['question_count'],
             label=country_code.upper(), alpha=0.7)

plt.xlabel('Date')
plt.ylabel('Question Count')
plt.title('Farmer Questions Over Time by Country')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(viz_dir / '01_questions_over_time.png', dpi=300, bbox_inches='tight')
print("  ✓ Created: 01_questions_over_time.png")
plt.close()

# Viz 2: Weather patterns
fig, axes = plt.subplots(3, 1, figsize=(14, 10))
for idx, (country_name, country_code) in enumerate(country_map.items()):
    if country_code in weather_data:
        df_weather = weather_data[country_code]
        axes[idx].plot(df_weather.index, df_weather['PRECTOTCORR'], 
                      color='blue', alpha=0.6)
        axes[idx].set_title(f'{country_name.upper()}: Daily Precipitation')
        axes[idx].set_ylabel('Rainfall (mm/day)')
        if idx == 2:
            axes[idx].set_xlabel('Date')

plt.tight_layout()
plt.savefig(viz_dir / '02_weather_patterns.png', dpi=300, bbox_inches='tight')
print("  ✓ Created: 02_weather_patterns.png")
plt.close()

# Viz 3: Correlation heatmap
if len(correlations) > 0:
    # Create correlation matrix
    corr_matrix = pd.DataFrame()
    for q_var in question_vars[:5]:  # Top 5 question variables
        if q_var in correlations:
            corr_row = {w_var: correlations[q_var][w_var]['correlation'] 
                       for w_var in weather_vars 
                       if w_var in correlations[q_var]}
            corr_matrix = pd.concat([corr_matrix, pd.DataFrame([corr_row])], ignore_index=True)
    
    if not corr_matrix.empty:
        corr_matrix.index = question_vars[:len(corr_matrix)]
        
        plt.figure(figsize=(10, 6))
        sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm', 
                   center=0, cbar_kws={'label': 'Correlation Coefficient'})
        plt.title('Weather-Question Correlation Matrix')
        plt.tight_layout()
        plt.savefig(viz_dir / '03_correlation_heatmap.png', dpi=300, bbox_inches='tight')
        print("  ✓ Created: 03_correlation_heatmap.png")
        plt.close()

# Viz 4: Questions vs Rainfall (Kenya)
if 'ke' in weather_data:
    kenya_merged = merged_df[merged_df['question_user_country_code'] == 'ke'].sort_values('question_day')
    
    fig, ax1 = plt.subplots(figsize=(14, 6))
    
    ax1.plot(kenya_merged['question_day'], kenya_merged['question_count'], 
            color='blue', label='Questions', alpha=0.7)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Question Count', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    
    ax2 = ax1.twinx()
    ax2.bar(kenya_merged['question_day'], kenya_merged['PRECTOTCORR'], 
           color='green', alpha=0.3, width=1, label='Rainfall')
    ax2.set_ylabel('Rainfall (mm/day)', color='green')
    ax2.tick_params(axis='y', labelcolor='green')
    
    plt.title('Kenya: Question Volume vs Rainfall')
    plt.tight_layout()
    plt.savefig(viz_dir / '04_kenya_questions_vs_rainfall.png', dpi=300, bbox_inches='tight')
    print("  ✓ Created: 04_kenya_questions_vs_rainfall.png")
    plt.close()

print("\n" + "="*70)
print("✓ ANALYSIS COMPLETE!")
print("="*70)
print(f"\nResults saved to:")
print(f"  - Data: {data_dir / 'processed'}")
print(f"  - Visualizations: {viz_dir}")
print("\nNext steps:")
print("  1. Review visualizations")
print("  2. Check correlation results")
print("  3. Write analysis report")
print("  4. Push to GitHub")
print("="*70)
