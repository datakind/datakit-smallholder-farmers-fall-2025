#!/usr/bin/env python3
"""
Explore WeFarm Dataset

Quick exploration of the dataset to understand structure and prepare for analysis.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

# Paths
script_dir = Path(__file__).parent
project_dir = script_dir.parent
data_file = project_dir / "data" / "raw" / "wefarm_dataset.csv"

print("="*60)
print("WeFarm Dataset Exploration")
print("="*60)

# Load a sample first to understand the data
print("\nLoading sample (first 100,000 rows)...")
df_sample = pd.read_csv(data_file, nrows=100000)

print(f"\nDataset shape: {df_sample.shape}")
print(f"Columns: {len(df_sample.columns)}")

print("\n" + "="*60)
print("COLUMN INFORMATION")
print("="*60)
print(df_sample.dtypes)

print("\n" + "="*60)
print("MISSING VALUES")
print("="*60)
print(df_sample.isnull().sum())

print("\n" + "="*60)
print("QUESTION LANGUAGES")
print("="*60)
print(df_sample['question_language'].value_counts())

print("\n" + "="*60)
print("COUNTRIES")
print("="*60)
print(df_sample['question_user_country_code'].value_counts())

print("\n" + "="*60)
print("DATE RANGE")
print("="*60)
df_sample['question_sent_dt'] = pd.to_datetime(df_sample['question_sent'])
print(f"Earliest question: {df_sample['question_sent_dt'].min()}")
print(f"Latest question: {df_sample['question_sent_dt'].max()}")

print("\n" + "="*60)
print("SAMPLE QUESTIONS")
print("="*60)
for i, row in df_sample.head(5).iterrows():
    print(f"\nQuestion {i+1}:")
    print(f"  Language: {row['question_language']}")
    print(f"  Country: {row['question_user_country_code']}")
    print(f"  Date: {row['question_sent']}")
    print(f"  Topic: {row['question_topic']}")
    print(f"  Content: {row['question_content'][:100]}...")

print("\n" + "="*60)
print("TOPICS DISTRIBUTION")
print("="*60)
topic_counts = df_sample['question_topic'].value_counts()
print(topic_counts.head(20))

print("\n" + "="*60)
print("✓ Exploration complete!")
print("="*60)
