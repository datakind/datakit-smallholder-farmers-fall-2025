#!/usr/bin/env python3
"""
Challenge 4: Crop-Specific vs General Questions
Option A: Traditional NLP Approach (Keyword-based Classification)

Author: hwilner
Date: November 6, 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import time
import json

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

print("="*80)
print("Challenge 4: Option A - Traditional NLP Classification")
print("="*80)

# Load data
print("\nLoading WeFarm dataset...")
df = pd.read_csv('/home/ubuntu/datakit-smallholder-farmers-fall-2025/challenge2_seasonality/data/raw/wefarm_dataset.csv', nrows=500000)
print(f"Loaded {len(df):,} questions")

# Define comprehensive keyword lists
CROP_KEYWORDS = {
    'cereals': ['maize', 'corn', 'rice', 'wheat', 'millet', 'sorghum', 'barley', 'oats'],
    'vegetables': ['tomato', 'cabbage', 'onion', 'carrot', 'kale', 'spinach', 'pepper', 'eggplant', 'cucumber'],
    'tubers': ['potato', 'cassava', 'yam', 'sweet potato'],
    'legumes': ['bean', 'pea', 'lentil', 'groundnut', 'peanut', 'soybean'],
    'fruits': ['banana', 'plantain', 'mango', 'papaya', 'avocado', 'orange', 'pineapple'],
    'cash_crops': ['coffee', 'tea', 'cotton', 'tobacco', 'sugarcane'],
    'livestock': ['chicken', 'cattle', 'cow', 'pig', 'goat', 'sheep', 'duck', 'turkey', 'rabbit'],
    'poultry': ['poultry', 'hen', 'rooster', 'chick', 'egg', 'broiler', 'layer'],
    'aquaculture': ['fish', 'tilapia', 'catfish', 'pond']
}

GENERAL_KEYWORDS = {
    'soil': ['soil', 'erosion', 'fertility', 'compost', 'manure', 'organic matter'],
    'weather': ['weather', 'rain', 'rainfall', 'drought', 'climate', 'temperature', 'season'],
    'water': ['water', 'irrigation', 'watering', 'moisture', 'drainage'],
    'pests': ['pest', 'insect', 'bug', 'aphid', 'worm', 'beetle'],
    'diseases': ['disease', 'fungus', 'blight', 'rot', 'wilt', 'virus'],
    'weeds': ['weed', 'grass', 'invasive'],
    'fertilizer': ['fertilizer', 'fertiliser', 'nutrient', 'npk', 'nitrogen', 'phosphorus', 'potassium'],
    'farming_practices': ['planting', 'harvest', 'harvesting', 'pruning', 'mulching', 'spacing', 'rotation'],
    'general_advice': ['farming', 'agriculture', 'crop', 'farm', 'grow', 'cultivate']
}

# Flatten keyword lists
all_crop_keywords = [kw for category in CROP_KEYWORDS.values() for kw in category]
all_general_keywords = [kw for category in GENERAL_KEYWORDS.values() for kw in category]

def classify_question(text):
    """
    Classify question as crop_specific, general, mixed, or unknown
    Returns: (classification, crop_matches, general_matches, specific_crops)
    """
    if pd.isna(text):
        return 'unknown', 0, 0, []
    
    text_lower = str(text).lower()
    
    # Find crop matches
    crop_matches = []
    for category, keywords in CROP_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                crop_matches.append((keyword, category))
    
    # Find general topic matches
    general_matches = []
    for category, keywords in GENERAL_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                general_matches.append((keyword, category))
    
    # Classification logic
    crop_count = len(crop_matches)
    general_count = len(general_matches)
    
    if crop_count > 0 and general_count == 0:
        classification = 'crop_specific'
    elif general_count > 0 and crop_count == 0:
        classification = 'general'
    elif crop_count > 0 and general_count > 0:
        classification = 'mixed'
    else:
        classification = 'unknown'
    
    specific_crops = list(set([crop for crop, _ in crop_matches]))
    
    return classification, crop_count, general_count, specific_crops

# Classify all questions
print("\nClassifying questions...")
start_time = time.time()

results = df['question_content'].apply(lambda x: classify_question(x))
df['classification'] = results.apply(lambda x: x[0])
df['crop_match_count'] = results.apply(lambda x: x[1])
df['general_match_count'] = results.apply(lambda x: x[2])
df['specific_crops'] = results.apply(lambda x: x[3])

classification_time = time.time() - start_time

print(f"✅ Classification complete in {classification_time:.2f} seconds")
print(f"   Speed: {len(df)/classification_time:,.0f} questions/second")

# Calculate statistics
print("\n" + "="*80)
print("CLASSIFICATION RESULTS")
print("="*80)

classification_counts = df['classification'].value_counts()
print("\nOverall Distribution:")
for cat, count in classification_counts.items():
    pct = count / len(df) * 100
    print(f"  {cat:15s}: {count:7,} ({pct:5.1f}%)")

# Analyze by country
print("\nDistribution by Country:")
country_classification = pd.crosstab(df['question_user_country_code'], df['classification'], normalize='index') * 100
print(country_classification.round(1))

# Analyze by language
print("\nDistribution by Language:")
language_classification = pd.crosstab(df['question_language'], df['classification'], normalize='index') * 100
print(language_classification.round(1))

# Find most common crops mentioned
all_crops_mentioned = [crop for crops in df['specific_crops'] if crops for crop in crops]
crop_counter = Counter(all_crops_mentioned)
print("\nTop 20 Most Mentioned Crops:")
for crop, count in crop_counter.most_common(20):
    print(f"  {crop:15s}: {count:6,} mentions")

# ============================================================================
# VISUALIZATIONS
# ============================================================================

print("\nCreating visualizations...")

# Visualization 1: Overall Distribution
fig, ax = plt.subplots(figsize=(10, 6))
classification_counts.plot(kind='bar', ax=ax, color=['#2ecc71', '#3498db', '#e74c3c', '#95a5a6'])
ax.set_title('Challenge 4 Option A: Question Classification Distribution\n(Traditional NLP)', fontsize=14, fontweight='bold')
ax.set_xlabel('Classification Category', fontsize=12)
ax.set_ylabel('Number of Questions', fontsize=12)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
plt.tight_layout()
plt.savefig('/home/ubuntu/datakit-smallholder-farmers-fall-2025/challenge4_crop_classification/visualizations/option_a/viz1_overall_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# Visualization 2: Distribution by Country
fig, ax = plt.subplots(figsize=(12, 6))
country_classification.plot(kind='bar', stacked=True, ax=ax, color=['#2ecc71', '#3498db', '#e74c3c', '#95a5a6'])
ax.set_title('Challenge 4 Option A: Classification by Country\n(Traditional NLP)', fontsize=14, fontweight='bold')
ax.set_xlabel('Country', fontsize=12)
ax.set_ylabel('Percentage of Questions', fontsize=12)
ax.legend(title='Classification', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
plt.tight_layout()
plt.savefig('/home/ubuntu/datakit-smallholder-farmers-fall-2025/challenge4_crop_classification/visualizations/option_a/viz2_by_country.png', dpi=300, bbox_inches='tight')
plt.close()

# Visualization 3: Top Crops Mentioned
fig, ax = plt.subplots(figsize=(12, 8))
top_crops = crop_counter.most_common(20)
crops, counts = zip(*top_crops)
ax.barh(range(len(crops)), counts, color='#27ae60')
ax.set_yticks(range(len(crops)))
ax.set_yticklabels(crops)
ax.set_xlabel('Number of Mentions', fontsize=12)
ax.set_title('Challenge 4 Option A: Top 20 Most Mentioned Crops\n(Traditional NLP)', fontsize=14, fontweight='bold')
ax.invert_yaxis()
plt.tight_layout()
plt.savefig('/home/ubuntu/datakit-smallholder-farmers-fall-2025/challenge4_crop_classification/visualizations/option_a/viz3_top_crops.png', dpi=300, bbox_inches='tight')
plt.close()

# Visualization 4: Crop Categories Distribution
crop_category_counts = Counter()
for crops in df[df['classification'].isin(['crop_specific', 'mixed'])]['specific_crops']:
    for crop in crops:
        for category, keywords in CROP_KEYWORDS.items():
            if crop in keywords:
                crop_category_counts[category] += 1
                break

fig, ax = plt.subplots(figsize=(10, 6))
categories = list(crop_category_counts.keys())
counts = [crop_category_counts[cat] for cat in categories]
ax.bar(categories, counts, color='#3498db')
ax.set_title('Challenge 4 Option A: Crop Category Distribution\n(Traditional NLP)', fontsize=14, fontweight='bold')
ax.set_xlabel('Crop Category', fontsize=12)
ax.set_ylabel('Number of Mentions', fontsize=12)
ax.set_xticklabels(categories, rotation=45, ha='right')
plt.tight_layout()
plt.savefig('/home/ubuntu/datakit-smallholder-farmers-fall-2025/challenge4_crop_classification/visualizations/option_a/viz4_crop_categories.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ Visualizations saved")

# ============================================================================
# SAVE RESULTS
# ============================================================================

print("\nSaving results...")

# Save classified data (sample)
output_sample = df[['question_content', 'classification', 'specific_crops', 'question_user_country_code', 'question_language']].head(10000)
output_sample.to_csv('/home/ubuntu/datakit-smallholder-farmers-fall-2025/challenge4_crop_classification/data/processed/option_a_sample_classified.csv', index=False)

# Save summary statistics
summary_stats = {
    'total_questions': len(df),
    'classification_time_seconds': classification_time,
    'speed_questions_per_second': len(df) / classification_time,
    'classification_distribution': classification_counts.to_dict(),
    'classification_percentages': (classification_counts / len(df) * 100).to_dict(),
    'top_20_crops': dict(crop_counter.most_common(20)),
    'crop_category_distribution': dict(crop_category_counts),
    'by_country': country_classification.to_dict(),
    'by_language': language_classification.to_dict()
}

with open('/home/ubuntu/datakit-smallholder-farmers-fall-2025/challenge4_crop_classification/data/processed/option_a_summary_stats.json', 'w') as f:
    json.dump(summary_stats, f, indent=2)

print("✅ Results saved")

print("\n" + "="*80)
print("OPTION A: TRADITIONAL NLP - COMPLETE")
print("="*80)
print(f"\nTotal questions analyzed: {len(df):,}")
print(f"Classification time: {classification_time:.2f} seconds")
print(f"Speed: {len(df)/classification_time:,.0f} questions/second")
print(f"Cost: $0 (free)")
print("\nKey Findings:")
print(f"  - Crop-specific questions: {classification_counts.get('crop_specific', 0):,} ({classification_counts.get('crop_specific', 0)/len(df)*100:.1f}%)")
print(f"  - General questions: {classification_counts.get('general', 0):,} ({classification_counts.get('general', 0)/len(df)*100:.1f}%)")
print(f"  - Mixed questions: {classification_counts.get('mixed', 0):,} ({classification_counts.get('mixed', 0)/len(df)*100:.1f}%)")
print(f"  - Unknown questions: {classification_counts.get('unknown', 0):,} ({classification_counts.get('unknown', 0)/len(df)*100:.1f}%)")
print(f"\nTop 3 crops: {', '.join([crop for crop, _ in crop_counter.most_common(3)])}")
