#!/usr/bin/env python3
"""
Challenge 4: Crop-Specific vs General Questions
Option B: LLM-based Classification (Groq + Hugging Face Fallback)

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
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

print("="*80)
print("Challenge 4: Option B - LLM-based Classification")
print("="*80)

# Check for Groq API key
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
USE_GROQ = GROQ_API_KEY is not None

if USE_GROQ:
    print("\n✅ Groq API key found - using Groq for classification")
    try:
        from groq import Groq
        groq_client = Groq(api_key=GROQ_API_KEY)
        print("✅ Groq client initialized")
    except ImportError:
        print("⚠️  Groq library not installed, installing...")
        os.system("pip3 install -q groq")
        from groq import Groq
        groq_client = Groq(api_key=GROQ_API_KEY)
        print("✅ Groq client initialized")
else:
    print("\n⚠️  No Groq API key found - using Hugging Face fallback")
    print("Installing transformers...")
    os.system("pip3 install -q transformers torch")
    from transformers import pipeline
    print("Loading Hugging Face model (this may take a moment)...")
    # Use a lightweight model for classification
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    print("✅ Hugging Face model loaded")

# Load data (smaller sample for LLM due to cost/time)
print("\nLoading WeFarm dataset...")
SAMPLE_SIZE = 1000  # Adjust based on available resources
df = pd.read_csv('/home/ubuntu/datakit-smallholder-farmers-fall-2025/challenge2_seasonality/data/raw/wefarm_dataset.csv', nrows=SAMPLE_SIZE)
print(f"Loaded {len(df):,} questions for LLM classification")

def classify_with_groq(text):
    """Classify using Groq API"""
    if pd.isna(text):
        return {'classification': 'unknown', 'confidence': 0, 'crops': [], 'topics': []}
    
    try:
        # Truncate text to avoid token limits
        text_truncated = str(text)[:500]
        
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Fast and accurate
            messages=[
                {
                    "role": "system",
                    "content": """You are an agricultural expert. Classify farming questions into categories.
                    
Respond ONLY with valid JSON in this exact format:
{
  "classification": "crop_specific" or "general" or "mixed",
  "confidence": 0.0 to 1.0,
  "crops": ["list", "of", "crops"],
  "topics": ["list", "of", "topics"]
}

Definitions:
- crop_specific: Question about a specific crop or animal (e.g., "How do I grow maize?")
- general: General farming advice not tied to specific crops (e.g., "How do I improve soil fertility?")
- mixed: Question mentions specific crops but asks general advice (e.g., "What fertilizer for my maize and beans?")"""
                },
                {
                    "role": "user",
                    "content": f"Classify this question: {text_truncated}"
                }
            ],
            temperature=0,
            max_tokens=200
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # Parse JSON response
        import re
        # Extract JSON from response (in case there's extra text)
        json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
        else:
            result = json.loads(result_text)
        
        return result
        
    except Exception as e:
        print(f"Error with Groq: {e}")
        return {'classification': 'error', 'confidence': 0, 'crops': [], 'topics': []}

def classify_with_huggingface(text):
    """Classify using Hugging Face zero-shot classification"""
    if pd.isna(text):
        return {'classification': 'unknown', 'confidence': 0, 'crops': [], 'topics': []}
    
    try:
        # Truncate text
        text_truncated = str(text)[:500]
        
        # Define candidate labels
        candidate_labels = ["crop-specific farming question", "general farming advice", "mixed farming question"]
        
        result = classifier(text_truncated, candidate_labels)
        
        # Map to our classification scheme
        label_map = {
            "crop-specific farming question": "crop_specific",
            "general farming advice": "general",
            "mixed farming question": "mixed"
        }
        
        classification = label_map[result['labels'][0]]
        confidence = result['scores'][0]
        
        # Simple keyword extraction for crops (since HF doesn't do this automatically)
        crop_keywords = ['maize', 'corn', 'tomato', 'chicken', 'cattle', 'cow', 'pig', 'goat', 
                        'bean', 'cassava', 'potato', 'rice', 'wheat', 'coffee', 'tea', 'banana']
        crops = [crop for crop in crop_keywords if crop in text_truncated.lower()]
        
        return {
            'classification': classification,
            'confidence': confidence,
            'crops': crops,
            'topics': []
        }
        
    except Exception as e:
        print(f"Error with Hugging Face: {e}")
        return {'classification': 'error', 'confidence': 0, 'crops': [], 'topics': []}

# Classify all questions
print("\nClassifying questions with LLM...")
print(f"Method: {'Groq API' if USE_GROQ else 'Hugging Face (local)'}")
start_time = time.time()

classify_func = classify_with_groq if USE_GROQ else classify_with_huggingface

results = []
for idx, text in enumerate(df['question_content']):
    if idx % 100 == 0:
        elapsed = time.time() - start_time
        rate = idx / elapsed if elapsed > 0 else 0
        print(f"  Progress: {idx}/{len(df)} ({idx/len(df)*100:.1f}%) - {rate:.1f} questions/sec")
    
    result = classify_func(text)
    results.append(result)

classification_time = time.time() - start_time

df['classification'] = [r['classification'] for r in results]
df['confidence'] = [r['confidence'] for r in results]
df['specific_crops'] = [r['crops'] for r in results]
df['topics'] = [r.get('topics', []) for r in results]

print(f"\n✅ Classification complete in {classification_time:.2f} seconds")
print(f"   Speed: {len(df)/classification_time:.1f} questions/second")

# Calculate statistics
print("\n" + "="*80)
print("CLASSIFICATION RESULTS")
print("="*80)

classification_counts = df['classification'].value_counts()
print("\nOverall Distribution:")
for cat, count in classification_counts.items():
    pct = count / len(df) * 100
    print(f"  {cat:15s}: {count:7,} ({pct:5.1f}%)")

# Average confidence
avg_confidence = df[df['classification'] != 'error']['confidence'].mean()
print(f"\nAverage Confidence: {avg_confidence:.2%}")

# Analyze by country
if 'question_user_country_code' in df.columns:
    print("\nDistribution by Country:")
    country_classification = pd.crosstab(df['question_user_country_code'], df['classification'], normalize='index') * 100
    print(country_classification.round(1))

# Find most common crops mentioned
all_crops_mentioned = [crop for crops in df['specific_crops'] if crops for crop in crops]
crop_counter = Counter(all_crops_mentioned)
if crop_counter:
    print(f"\nTop {min(20, len(crop_counter))} Most Mentioned Crops:")
    for crop, count in crop_counter.most_common(20):
        print(f"  {crop:15s}: {count:6,} mentions")

# ============================================================================
# VISUALIZATIONS
# ============================================================================

print("\nCreating visualizations...")

# Visualization 1: Overall Distribution
fig, ax = plt.subplots(figsize=(10, 6))
classification_counts.plot(kind='bar', ax=ax, color=['#9b59b6', '#3498db', '#e74c3c', '#95a5a6', '#34495e'])
ax.set_title(f'Challenge 4 Option B: Question Classification Distribution\n(LLM-based: {"Groq" if USE_GROQ else "Hugging Face"})', fontsize=14, fontweight='bold')
ax.set_xlabel('Classification Category', fontsize=12)
ax.set_ylabel('Number of Questions', fontsize=12)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
plt.tight_layout()
plt.savefig('/home/ubuntu/datakit-smallholder-farmers-fall-2025/challenge4_crop_classification/visualizations/option_b/viz1_overall_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# Visualization 2: Confidence Distribution
fig, ax = plt.subplots(figsize=(10, 6))
df[df['classification'] != 'error']['confidence'].hist(bins=20, ax=ax, color='#9b59b6', edgecolor='black')
ax.set_title(f'Challenge 4 Option B: Classification Confidence Distribution\n(LLM-based: {"Groq" if USE_GROQ else "Hugging Face"})', fontsize=14, fontweight='bold')
ax.set_xlabel('Confidence Score', fontsize=12)
ax.set_ylabel('Number of Questions', fontsize=12)
ax.axvline(avg_confidence, color='red', linestyle='--', linewidth=2, label=f'Mean: {avg_confidence:.2%}')
ax.legend()
plt.tight_layout()
plt.savefig('/home/ubuntu/datakit-smallholder-farmers-fall-2025/challenge4_crop_classification/visualizations/option_b/viz2_confidence_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# Visualization 3: Top Crops (if available)
if crop_counter:
    fig, ax = plt.subplots(figsize=(12, 8))
    top_crops = crop_counter.most_common(min(20, len(crop_counter)))
    if top_crops:
        crops, counts = zip(*top_crops)
        ax.barh(range(len(crops)), counts, color='#8e44ad')
        ax.set_yticks(range(len(crops)))
        ax.set_yticklabels(crops)
        ax.set_xlabel('Number of Mentions', fontsize=12)
        ax.set_title(f'Challenge 4 Option B: Top {len(crops)} Most Mentioned Crops\n(LLM-based: {"Groq" if USE_GROQ else "Hugging Face"})', fontsize=14, fontweight='bold')
        ax.invert_yaxis()
        plt.tight_layout()
        plt.savefig('/home/ubuntu/datakit-smallholder-farmers-fall-2025/challenge4_crop_classification/visualizations/option_b/viz3_top_crops.png', dpi=300, bbox_inches='tight')
        plt.close()

print("✅ Visualizations saved")

# ============================================================================
# SAVE RESULTS
# ============================================================================

print("\nSaving results...")

# Save classified data
output_df = df[['question_content', 'classification', 'confidence', 'specific_crops', 'topics']]
if 'question_user_country_code' in df.columns:
    output_df['country'] = df['question_user_country_code']
if 'question_language' in df.columns:
    output_df['language'] = df['question_language']

output_df.to_csv('/home/ubuntu/datakit-smallholder-farmers-fall-2025/challenge4_crop_classification/data/processed/option_b_llm_classified.csv', index=False)

# Save summary statistics
summary_stats = {
    'method': 'Groq API' if USE_GROQ else 'Hugging Face (local)',
    'model': 'llama-3.3-70b-versatile' if USE_GROQ else 'facebook/bart-large-mnli',
    'total_questions': len(df),
    'classification_time_seconds': classification_time,
    'speed_questions_per_second': len(df) / classification_time,
    'average_confidence': float(avg_confidence),
    'classification_distribution': {k: int(v) for k, v in classification_counts.items()},
    'classification_percentages': {k: float(v / len(df) * 100) for k, v in classification_counts.items()},
    'top_crops': dict(crop_counter.most_common(20)) if crop_counter else {},
    'estimated_cost_usd': 0 if not USE_GROQ else len(df) * 0.0001  # Rough estimate
}

with open('/home/ubuntu/datakit-smallholder-farmers-fall-2025/challenge4_crop_classification/data/processed/option_b_summary_stats.json', 'w') as f:
    json.dump(summary_stats, f, indent=2)

print("✅ Results saved")

print("\n" + "="*80)
print("OPTION B: LLM-BASED CLASSIFICATION - COMPLETE")
print("="*80)
print(f"\nMethod: {'Groq API' if USE_GROQ else 'Hugging Face (local)'}")
print(f"Total questions analyzed: {len(df):,}")
print(f"Classification time: {classification_time:.2f} seconds")
print(f"Speed: {len(df)/classification_time:.1f} questions/second")
print(f"Average confidence: {avg_confidence:.2%}")
if USE_GROQ:
    estimated_cost = len(df) * 0.0001
    print(f"Estimated cost: ${estimated_cost:.4f}")
else:
    print(f"Cost: $0 (local model)")

print("\nKey Findings:")
for cat, count in classification_counts.items():
    pct = count / len(df) * 100
    print(f"  - {cat}: {count:,} ({pct:.1f}%)")

if crop_counter:
    top_3 = [crop for crop, _ in crop_counter.most_common(3)]
    print(f"\nTop 3 crops: {', '.join(top_3)}")
