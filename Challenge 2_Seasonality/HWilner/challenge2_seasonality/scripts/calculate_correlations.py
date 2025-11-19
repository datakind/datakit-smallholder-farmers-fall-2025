#!/usr/bin/env python3
"""
Calculate Weather-Question Correlations

This script calculates correlations between weather variables and question patterns:
- Pearson correlations
- Lag correlations (0-28 days)
- Event-based analysis
- Statistical significance testing

Usage:
    python3 calculate_correlations.py
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats
from scipy.signal import correlate
import json

def load_data(processed_dir):
    """Load processed question and weather data"""
    print("Loading processed data...")
    
    # Load daily question data
    questions_file = processed_dir / "questions_daily.csv"
    if not questions_file.exists():
        print(f"Error: {questions_file} not found")
        print("Please run preprocess_questions.py first")
        return None, None
    
    questions_df = pd.read_csv(questions_file, index_col=0, parse_dates=True)
    print(f"Loaded {len(questions_df)} days of question data")
    
    # Load weather data (combine all countries)
    raw_dir = processed_dir.parent / "raw"
    weather_files = list(raw_dir.glob("weather_*.csv"))
    
    if not weather_files:
        print(f"Error: No weather files found in {raw_dir}")
        print("Please run download_weather_data.py first")
        return None, None
    
    weather_dfs = []
    for file in weather_files:
        if 'metadata' not in file.name:
            country = file.stem.replace('weather_', '')
            df = pd.read_csv(file, index_col=0, parse_dates=True)
            df['country'] = country
            weather_dfs.append(df)
            print(f"Loaded weather data for {country}: {len(df)} days")
    
    weather_df = pd.concat(weather_dfs)
    
    return questions_df, weather_df

def calculate_pearson_correlation(questions_df, weather_df):
    """Calculate Pearson correlation between weather and questions"""
    print("\nCalculating Pearson correlations...")
    
    # Merge data on date
    merged = questions_df.join(weather_df, how='inner')
    
    # Weather variables
    weather_vars = ['T2M', 'T2M_MAX', 'T2M_MIN', 'PRECTOTCORR', 'RH2M', 'WS2M']
    
    # Question variables
    question_vars = ['question_count'] + [col for col in questions_df.columns 
                                          if col.endswith('_count')]
    
    # Calculate correlations
    correlations = {}
    for q_var in question_vars:
        correlations[q_var] = {}
        for w_var in weather_vars:
            if q_var in merged.columns and w_var in merged.columns:
                # Remove NaN values
                valid_data = merged[[q_var, w_var]].dropna()
                
                if len(valid_data) > 0:
                    corr, p_value = stats.pearsonr(valid_data[q_var], valid_data[w_var])
                    correlations[q_var][w_var] = {
                        'correlation': corr,
                        'p_value': p_value,
                        'significant': p_value < 0.05,
                        'n': len(valid_data)
                    }
    
    return correlations

def calculate_lag_correlation(questions_df, weather_df, max_lag=28):
    """Calculate lag correlations"""
    print(f"\nCalculating lag correlations (max lag: {max_lag} days)...")
    
    # Ensure data is sorted by date
    questions_df = questions_df.sort_index()
    weather_df = weather_df.sort_index()
    
    # Get common date range
    start_date = max(questions_df.index.min(), weather_df.index.min())
    end_date = min(questions_df.index.max(), weather_df.index.max())
    
    # Filter to common range
    questions_df = questions_df[start_date:end_date]
    weather_df = weather_df[start_date:end_date]
    
    weather_vars = ['T2M', 'PRECTOTCORR', 'RH2M']
    question_vars = ['question_count'] + [col for col in questions_df.columns 
                                          if col.endswith('_count')]
    
    lag_correlations = {}
    
    for q_var in question_vars:
        lag_correlations[q_var] = {}
        
        for w_var in weather_vars:
            if q_var in questions_df.columns and w_var in weather_df.columns:
                # Get aligned data
                q_data = questions_df[q_var].fillna(0).values
                w_data = weather_df[w_var].fillna(method='ffill').values
                
                # Calculate correlation for each lag
                lags = range(0, max_lag + 1)
                correlations = []
                p_values = []
                
                for lag in lags:
                    if lag == 0:
                        q_subset = q_data
                        w_subset = w_data
                    else:
                        q_subset = q_data[lag:]
                        w_subset = w_data[:-lag]
                    
                    if len(q_subset) > 0 and len(w_subset) > 0:
                        corr, p_val = stats.pearsonr(q_subset, w_subset)
                        correlations.append(corr)
                        p_values.append(p_val)
                    else:
                        correlations.append(np.nan)
                        p_values.append(np.nan)
                
                # Find optimal lag (highest absolute correlation)
                abs_corrs = [abs(c) if not np.isnan(c) else 0 for c in correlations]
                optimal_lag = lags[np.argmax(abs_corrs)]
                
                lag_correlations[q_var][w_var] = {
                    'lags': list(lags),
                    'correlations': correlations,
                    'p_values': p_values,
                    'optimal_lag': optimal_lag,
                    'optimal_correlation': correlations[optimal_lag],
                    'optimal_p_value': p_values[optimal_lag]
                }
    
    return lag_correlations

def identify_weather_events(weather_df):
    """Identify extreme weather events"""
    print("\nIdentifying weather events...")
    
    events = {
        'heavy_rain': [],
        'drought': [],
        'heat_wave': [],
        'cold_spell': []
    }
    
    # Heavy rainfall: >50mm in a day
    if 'PRECTOTCORR' in weather_df.columns:
        heavy_rain = weather_df[weather_df['PRECTOTCORR'] > 50]
        events['heavy_rain'] = heavy_rain.index.tolist()
        print(f"Heavy rainfall events: {len(events['heavy_rain'])}")
    
    # Drought: <10mm over 30 days
    if 'PRECTOTCORR' in weather_df.columns:
        rainfall_30d = weather_df['PRECTOTCORR'].rolling(window=30).sum()
        drought = weather_df[rainfall_30d < 10]
        events['drought'] = drought.index.tolist()
        print(f"Drought periods: {len(events['drought'])}")
    
    # Heat wave: T_max > 35°C for 3+ consecutive days
    if 'T2M_MAX' in weather_df.columns:
        hot_days = weather_df['T2M_MAX'] > 35
        # Find consecutive sequences
        heat_wave_dates = []
        consecutive = 0
        for date, is_hot in hot_days.items():
            if is_hot:
                consecutive += 1
                if consecutive >= 3:
                    heat_wave_dates.append(date)
            else:
                consecutive = 0
        events['heat_wave'] = heat_wave_dates
        print(f"Heat wave days: {len(events['heat_wave'])}")
    
    # Cold spell: T_min < 10°C for 3+ consecutive days
    if 'T2M_MIN' in weather_df.columns:
        cold_days = weather_df['T2M_MIN'] < 10
        cold_spell_dates = []
        consecutive = 0
        for date, is_cold in cold_days.items():
            if is_cold:
                consecutive += 1
                if consecutive >= 3:
                    cold_spell_dates.append(date)
            else:
                consecutive = 0
        events['cold_spell'] = cold_spell_dates
        print(f"Cold spell days: {len(events['cold_spell'])}")
    
    return events

def analyze_event_impact(questions_df, events, window_days=7):
    """Analyze question patterns during weather events"""
    print(f"\nAnalyzing event impact (±{window_days} days window)...")
    
    impact_analysis = {}
    
    for event_type, event_dates in events.items():
        if not event_dates:
            continue
        
        impact_analysis[event_type] = {}
        
        # Get question counts during events
        event_questions = []
        before_questions = []
        after_questions = []
        
        for event_date in event_dates:
            # During event
            if event_date in questions_df.index:
                event_questions.append(questions_df.loc[event_date, 'question_count'])
            
            # Before event
            before_date = event_date - pd.Timedelta(days=window_days)
            if before_date in questions_df.index:
                before_questions.append(questions_df.loc[before_date, 'question_count'])
            
            # After event
            after_date = event_date + pd.Timedelta(days=window_days)
            if after_date in questions_df.index:
                after_questions.append(questions_df.loc[after_date, 'question_count'])
        
        # Calculate statistics
        if event_questions:
            impact_analysis[event_type]['during'] = {
                'mean': np.mean(event_questions),
                'std': np.std(event_questions),
                'count': len(event_questions)
            }
        
        if before_questions:
            impact_analysis[event_type]['before'] = {
                'mean': np.mean(before_questions),
                'std': np.std(before_questions),
                'count': len(before_questions)
            }
        
        if after_questions:
            impact_analysis[event_type]['after'] = {
                'mean': np.mean(after_questions),
                'std': np.std(after_questions),
                'count': len(after_questions)
            }
        
        # Statistical test (t-test)
        if event_questions and before_questions:
            t_stat, p_value = stats.ttest_ind(event_questions, before_questions)
            impact_analysis[event_type]['ttest_before'] = {
                't_statistic': t_stat,
                'p_value': p_value,
                'significant': p_value < 0.05
            }
        
        print(f"{event_type}: {len(event_dates)} events analyzed")
    
    return impact_analysis

def main():
    """Main correlation analysis function"""
    print("="*60)
    print("Weather-Question Correlation Analysis")
    print("="*60)
    
    # Set up paths
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    processed_dir = project_dir / "data" / "processed"
    
    # Load data
    questions_df, weather_df = load_data(processed_dir)
    
    if questions_df is None or weather_df is None:
        print("\n⚠ Cannot proceed without data.")
        return
    
    # Calculate Pearson correlations
    pearson_corr = calculate_pearson_correlation(questions_df, weather_df)
    
    # Calculate lag correlations
    lag_corr = calculate_lag_correlation(questions_df, weather_df)
    
    # Identify weather events
    events = identify_weather_events(weather_df)
    
    # Analyze event impact
    event_impact = analyze_event_impact(questions_df, events)
    
    # Save results
    results = {
        'pearson_correlations': pearson_corr,
        'lag_correlations': lag_corr,
        'weather_events': {k: len(v) for k, v in events.items()},
        'event_impact': event_impact,
        'analysis_timestamp': pd.Timestamp.now().isoformat()
    }
    
    # Convert numpy types to native Python types for JSON serialization
    def convert_to_serializable(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        return obj
    
    # Deep conversion
    import json
    results_json = json.loads(json.dumps(results, default=convert_to_serializable))
    
    output_file = processed_dir / "correlation_results.json"
    with open(output_file, 'w') as f:
        json.dump(results_json, f, indent=2)
    
    print(f"\n✓ Results saved to: {output_file}")
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print("\nTop Pearson Correlations:")
    # Find top correlations
    all_corrs = []
    for q_var, weather_corrs in pearson_corr.items():
        for w_var, stats_dict in weather_corrs.items():
            all_corrs.append((
                q_var, w_var, 
                stats_dict['correlation'], 
                stats_dict['p_value'],
                stats_dict['significant']
            ))
    
    # Sort by absolute correlation
    all_corrs.sort(key=lambda x: abs(x[2]), reverse=True)
    
    for i, (q_var, w_var, corr, p_val, sig) in enumerate(all_corrs[:10], 1):
        sig_marker = "***" if sig else ""
        print(f"{i}. {q_var} vs {w_var}: r={corr:.3f} (p={p_val:.4f}) {sig_marker}")
    
    print("\n" + "="*60)
    print("✓ Correlation analysis complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Review correlation results")
    print("2. Create visualizations: python3 scripts/create_visualizations.py")
    print("3. Write analysis report")
    print("="*60)

if __name__ == "__main__":
    main()
