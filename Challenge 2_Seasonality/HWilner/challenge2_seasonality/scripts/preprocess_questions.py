#!/usr/bin/env python3
"""
Preprocess WeFarm Question Data

This script preprocesses the WeFarm question dataset for analysis:
- Cleans and validates data
- Parses timestamps
- Categorizes questions by topic using keywords
- Aggregates questions by time period
- Prepares data for correlation analysis

Usage:
    python3 preprocess_questions.py
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import re
import json

# Topic keywords for categorization
TOPIC_KEYWORDS = {
    'pest': [
        'pest', 'insect', 'bug', 'aphid', 'caterpillar', 'worm', 'beetle',
        'locust', 'grasshopper', 'termite', 'ant', 'fly', 'wadudu', 'mende',
        'infestation', 'attack', 'damage', 'control', 'spray', 'pesticide'
    ],
    'disease': [
        'disease', 'fungus', 'blight', 'wilt', 'rot', 'mold', 'virus',
        'bacterial', 'infection', 'ugonjwa', 'obulwadde', 'sick', 'dying'
    ],
    'water': [
        'water', 'irrigation', 'drought', 'dry', 'watering', 'rain',
        'rainfall', 'moisture', 'maji', 'amazzi', 'ukame', 'ekyeya'
    ],
    'planting': [
        'plant', 'planting', 'seed', 'sowing', 'germination', 'nursery',
        'transplant', 'spacing', 'panda', 'mbegu', 'ensigo', 'okusimba'
    ],
    'harvest': [
        'harvest', 'harvesting', 'mature', 'maturity', 'ready', 'ripe',
        'yield', 'production', 'mavuno', 'okukungula', 'amakungula'
    ],
    'fertilizer': [
        'fertilizer', 'manure', 'compost', 'nutrient', 'nitrogen', 'phosphorus',
        'potassium', 'npk', 'mbolea', 'obugimusa', 'feeding', 'application'
    ],
    'soil': [
        'soil', 'land', 'earth', 'ground', 'udongo', 'ettaka', 'ph',
        'fertility', 'preparation', 'tillage', 'plowing'
    ],
    'crop_stress': [
        'wilting', 'yellowing', 'drying', 'stunted', 'weak', 'poor growth',
        'stress', 'struggling', 'not growing', 'dying', 'brown', 'curling'
    ],
    'weather': [
        'weather', 'climate', 'temperature', 'heat', 'cold', 'frost',
        'sun', 'shade', 'wind', 'hali ya hewa', 'embeera y\'obudde'
    ],
    'market': [
        'market', 'price', 'sell', 'selling', 'buyer', 'trade', 'soko',
        'akatale', 'profit', 'income', 'value'
    ]
}

def load_question_data(file_path):
    """
    Load WeFarm question data
    
    Args:
        file_path (Path): Path to question data CSV
    
    Returns:
        pandas.DataFrame: Loaded question data
    """
    print(f"Loading question data from: {file_path}")
    
    # Try to load the file
    # Note: Adjust column names based on actual dataset structure
    try:
        df = pd.read_csv(file_path)
        print(f"Loaded {len(df)} questions")
        print(f"Columns: {df.columns.tolist()}")
        return df
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        print("\nPlease download the WeFarm dataset and place it in:")
        print(f"  {file_path}")
        print("\nTo get the dataset:")
        print("  1. Join the DataKind Slack channel")
        print("  2. Find the dataset link in the channel")
        print("  3. Download and save to the path above")
        return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def clean_data(df):
    """
    Clean and validate question data
    
    Args:
        df (pandas.DataFrame): Raw question data
    
    Returns:
        pandas.DataFrame: Cleaned data
    """
    print("\nCleaning data...")
    initial_count = len(df)
    
    # Remove duplicates
    df = df.drop_duplicates()
    print(f"Removed {initial_count - len(df)} duplicates")
    
    # Remove rows with missing critical fields
    # Note: Adjust based on actual column names
    critical_fields = ['timestamp', 'question_text']  # Update as needed
    for field in critical_fields:
        if field in df.columns:
            before = len(df)
            df = df.dropna(subset=[field])
            removed = before - len(df)
            if removed > 0:
                print(f"Removed {removed} rows with missing {field}")
    
    print(f"Final count: {len(df)} questions")
    return df

def parse_timestamps(df, timestamp_column='timestamp'):
    """
    Parse timestamps to datetime
    
    Args:
        df (pandas.DataFrame): Question data
        timestamp_column (str): Name of timestamp column
    
    Returns:
        pandas.DataFrame: Data with parsed timestamps
    """
    print(f"\nParsing timestamps from column: {timestamp_column}")
    
    if timestamp_column not in df.columns:
        print(f"Warning: Column '{timestamp_column}' not found")
        print(f"Available columns: {df.columns.tolist()}")
        print("Please update the script with the correct column name")
        return df
    
    # Try to parse timestamps
    try:
        df['datetime'] = pd.to_datetime(df[timestamp_column])
        
        # Extract date components
        df['date'] = df['datetime'].dt.date
        df['year'] = df['datetime'].dt.year
        df['month'] = df['datetime'].dt.month
        df['day'] = df['datetime'].dt.day
        df['week'] = df['datetime'].dt.isocalendar().week
        df['day_of_year'] = df['datetime'].dt.dayofyear
        
        print(f"Date range: {df['datetime'].min()} to {df['datetime'].max()}")
        print(f"Years: {sorted(df['year'].unique())}")
        
        return df
    except Exception as e:
        print(f"Error parsing timestamps: {e}")
        return df

def categorize_questions(df, text_column='question_text'):
    """
    Categorize questions by topic using keyword matching
    
    Args:
        df (pandas.DataFrame): Question data
        text_column (str): Name of question text column
    
    Returns:
        pandas.DataFrame: Data with topic categories
    """
    print(f"\nCategorizing questions by topic...")
    
    if text_column not in df.columns:
        print(f"Warning: Column '{text_column}' not found")
        print(f"Available columns: {df.columns.tolist()}")
        print("Please update the script with the correct column name")
        return df
    
    # Initialize topic columns
    for topic in TOPIC_KEYWORDS.keys():
        df[f'topic_{topic}'] = False
    
    # Categorize based on keywords
    for topic, keywords in TOPIC_KEYWORDS.items():
        pattern = '|'.join(keywords)
        df[f'topic_{topic}'] = df[text_column].str.contains(
            pattern, case=False, na=False, regex=True
        )
    
    # Count questions per topic
    print("\nQuestions per topic:")
    for topic in TOPIC_KEYWORDS.keys():
        count = df[f'topic_{topic}'].sum()
        percentage = (count / len(df)) * 100
        print(f"  {topic}: {count} ({percentage:.1f}%)")
    
    # Identify uncategorized questions
    topic_cols = [f'topic_{topic}' for topic in TOPIC_KEYWORDS.keys()]
    df['has_topic'] = df[topic_cols].any(axis=1)
    uncategorized = (~df['has_topic']).sum()
    print(f"\nUncategorized: {uncategorized} ({(uncategorized/len(df))*100:.1f}%)")
    
    return df

def aggregate_by_time(df):
    """
    Aggregate questions by time period
    
    Args:
        df (pandas.DataFrame): Question data with datetime
    
    Returns:
        dict: Dictionary of aggregated dataframes
    """
    print("\nAggregating questions by time period...")
    
    if 'datetime' not in df.columns:
        print("Error: 'datetime' column not found. Run parse_timestamps first.")
        return {}
    
    aggregated = {}
    
    # Daily aggregation
    daily = df.groupby(df['datetime'].dt.date).agg({
        'datetime': 'count'  # Count questions per day
    }).rename(columns={'datetime': 'question_count'})
    
    # Add topic counts
    topic_cols = [col for col in df.columns if col.startswith('topic_')]
    for col in topic_cols:
        topic_name = col.replace('topic_', '')
        daily[f'{topic_name}_count'] = df.groupby(df['datetime'].dt.date)[col].sum()
    
    aggregated['daily'] = daily
    print(f"Daily: {len(daily)} days")
    
    # Weekly aggregation
    weekly = df.groupby(df['datetime'].dt.to_period('W')).agg({
        'datetime': 'count'
    }).rename(columns={'datetime': 'question_count'})
    
    for col in topic_cols:
        topic_name = col.replace('topic_', '')
        weekly[f'{topic_name}_count'] = df.groupby(
            df['datetime'].dt.to_period('W')
        )[col].sum()
    
    aggregated['weekly'] = weekly
    print(f"Weekly: {len(weekly)} weeks")
    
    # Monthly aggregation
    monthly = df.groupby(df['datetime'].dt.to_period('M')).agg({
        'datetime': 'count'
    }).rename(columns={'datetime': 'question_count'})
    
    for col in topic_cols:
        topic_name = col.replace('topic_', '')
        monthly[f'{topic_name}_count'] = df.groupby(
            df['datetime'].dt.to_period('M')
        )[col].sum()
    
    aggregated['monthly'] = monthly
    print(f"Monthly: {len(monthly)} months")
    
    return aggregated

def main():
    """Main preprocessing function"""
    print("="*60)
    print("WeFarm Question Data Preprocessing")
    print("="*60)
    
    # Set up paths
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    raw_dir = project_dir / "data" / "raw"
    processed_dir = project_dir / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    # Input file (adjust name as needed)
    input_file = raw_dir / "wefarm_questions.csv"
    
    # Load data
    df = load_question_data(input_file)
    
    if df is None:
        print("\n⚠ Cannot proceed without data file.")
        print("Please download the dataset and try again.")
        return
    
    # Clean data
    df = clean_data(df)
    
    # Parse timestamps
    df = parse_timestamps(df)
    
    # Categorize questions
    df = categorize_questions(df)
    
    # Save processed full dataset
    output_file = processed_dir / "questions_processed.csv"
    df.to_csv(output_file, index=False)
    print(f"\nSaved processed data to: {output_file}")
    
    # Aggregate by time
    aggregated = aggregate_by_time(df)
    
    # Save aggregated data
    for period, agg_df in aggregated.items():
        agg_file = processed_dir / f"questions_{period}.csv"
        agg_df.to_csv(agg_file)
        print(f"Saved {period} aggregation to: {agg_file}")
    
    # Save metadata
    metadata = {
        'preprocessing_timestamp': datetime.now().isoformat(),
        'total_questions': len(df),
        'date_range': {
            'start': str(df['datetime'].min()) if 'datetime' in df.columns else None,
            'end': str(df['datetime'].max()) if 'datetime' in df.columns else None
        },
        'topics': {topic: int(df[f'topic_{topic}'].sum()) 
                   for topic in TOPIC_KEYWORDS.keys() if f'topic_{topic}' in df.columns},
        'aggregations': {period: len(agg_df) for period, agg_df in aggregated.items()}
    }
    
    metadata_file = processed_dir / "preprocessing_metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"Saved metadata to: {metadata_file}")
    
    print("\n" + "="*60)
    print("✓ Preprocessing complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Review processed data files")
    print("2. Run: python3 scripts/download_weather_data.py (if not done yet)")
    print("3. Start analysis: jupyter notebook notebooks/03_exploratory_analysis.ipynb")
    print("="*60)

if __name__ == "__main__":
    main()
