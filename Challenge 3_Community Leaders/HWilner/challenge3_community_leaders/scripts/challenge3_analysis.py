#!/usr/bin/env python3
"""
Challenge 3: Identifying Community Leaders
Analyzes the WeFarm dataset to discover leader farmers who consistently provide valuable support.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("CHALLENGE 3: IDENTIFYING COMMUNITY LEADERS")
print("=" * 80)

# Load dataset (using larger sample for better analysis)
print("\n📊 Loading dataset...")
df = pd.read_csv('/home/ubuntu/datakit-smallholder-farmers-fall-2025/challenge2_seasonality/data/raw/wefarm_dataset.csv', 
                 nrows=500000)  # 500k sample

print(f"✅ Loaded {len(df):,} rows")
print(f"   Date range: {df['question_sent'].min()} to {df['question_sent'].max()}")

# =============================================================================
# 1. IDENTIFY TOP CONTRIBUTORS (LEADERS)
# =============================================================================

print("\n" + "=" * 80)
print("1. IDENTIFYING TOP CONTRIBUTORS")
print("=" * 80)

# Count responses per user
response_counts = df['response_user_id'].value_counts()

print(f"\n📈 Response Statistics:")
print(f"   Total unique responders: {df['response_user_id'].nunique():,}")
print(f"   Total responses: {len(df):,}")
print(f"   Average responses per user: {len(df) / df['response_user_id'].nunique():.1f}")
print(f"   Median responses per user: {response_counts.median():.0f}")

# Top 50 contributors
top_contributors = response_counts.head(50)

print(f"\n🏆 TOP 10 CONTRIBUTORS:")
for rank, (user_id, count) in enumerate(top_contributors.head(10).items(), 1):
    percentage = (count / len(df)) * 100
    print(f"   {rank:2d}. User {user_id}: {count:,} responses ({percentage:.2f}%)")

# =============================================================================
# 2. CALCULATE LEADERSHIP METRICS
# =============================================================================

print("\n" + "=" * 80)
print("2. LEADERSHIP METRICS")
print("=" * 80)

# For each responder, calculate metrics
leader_metrics = []

for user_id in top_contributors.head(50).index:
    user_responses = df[df['response_user_id'] == user_id]
    
    # Basic metrics
    num_responses = len(user_responses)
    
    # Response quality (length as proxy)
    avg_response_length = user_responses['response_content'].str.len().mean()
    
    # Topic diversity
    topics = user_responses['response_topic'].dropna()
    unique_topics = topics.nunique()
    most_common_topic = topics.mode()[0] if len(topics) > 0 else None
    
    # Geographic reach
    countries = user_responses['response_user_country_code'].dropna()
    unique_countries = countries.nunique()
    primary_country = countries.mode()[0] if len(countries) > 0 else None
    
    # Unique question askers helped
    unique_askers_helped = user_responses['question_user_id'].nunique()
    
    # User info
    user_info = user_responses.iloc[0]
    
    leader_metrics.append({
        'user_id': user_id,
        'total_responses': num_responses,
        'avg_response_length': avg_response_length,
        'unique_topics': unique_topics,
        'primary_topic': most_common_topic,
        'unique_countries': unique_countries,
        'primary_country': primary_country,
        'unique_askers_helped': unique_askers_helped,
        'user_gender': user_info['response_user_gender'],
        'user_country': user_info['response_user_country_code']
    })

leaders_df = pd.DataFrame(leader_metrics)

print("\n📊 Leadership Metrics Summary:")
print(f"   Average response length: {leaders_df['avg_response_length'].mean():.0f} characters")
print(f"   Average topic diversity: {leaders_df['unique_topics'].mean():.1f} topics per leader")
print(f"   Average farmers helped: {leaders_df['unique_askers_helped'].mean():.0f} unique askers")

# =============================================================================
# 3. ANALYZE PATTERNS
# =============================================================================

print("\n" + "=" * 80)
print("3. LEADER PATTERNS")
print("=" * 80)

# Topic specialization
print("\n📚 Topic Specialization:")
topic_counts = leaders_df['primary_topic'].value_counts().head(10)
for topic, count in topic_counts.items():
    print(f"   {topic}: {count} leaders")

# Geographic patterns
print("\n🌍 Geographic Distribution:")
country_counts = leaders_df['primary_country'].value_counts()
for country, count in country_counts.items():
    print(f"   {country}: {count} leaders")

# Gender distribution
print("\n👥 Gender Distribution:")
gender_counts = leaders_df['user_gender'].value_counts()
for gender, count in gender_counts.items():
    print(f"   {gender}: {count} leaders")

# =============================================================================
# 4. IDENTIFY REPEAT QUESTIONS (TRUST ISSUES)
# =============================================================================

print("\n" + "=" * 80)
print("4. REPEAT QUESTIONS ANALYSIS")
print("=" * 80)

# Find users who ask multiple similar questions
question_counts = df.groupby('question_user_id').agg({
    'question_id': 'count',
    'question_topic': lambda x: x.mode()[0] if len(x.mode()) > 0 else None
}).rename(columns={'question_id': 'num_questions'})

repeat_askers = question_counts[question_counts['num_questions'] > 5].sort_values('num_questions', ascending=False)

print(f"\n🔄 Repeat Question Patterns:")
print(f"   Users asking 5+ questions: {len(repeat_askers):,}")
print(f"   Average questions per repeat user: {repeat_askers['num_questions'].mean():.1f}")

print(f"\n   Top 10 Repeat Askers:")
for rank, (user_id, row) in enumerate(repeat_askers.head(10).iterrows(), 1):
    print(f"   {rank:2d}. User {user_id}: {row['num_questions']} questions (topic: {row['question_topic']})")

# =============================================================================
# 5. SAVE RESULTS
# =============================================================================

print("\n" + "=" * 80)
print("5. SAVING RESULTS")
print("=" * 80)

# Save leaderboard
leaders_df.to_csv('/home/ubuntu/challenge3_leaderboard.csv', index=False)
print(f"✅ Saved leaderboard to challenge3_leaderboard.csv")

# Save summary statistics
summary = {
    'total_responders': df['response_user_id'].nunique(),
    'total_responses': len(df),
    'top_50_response_share': (top_contributors.head(50).sum() / len(df)) * 100,
    'avg_response_length': leaders_df['avg_response_length'].mean(),
    'avg_topics_per_leader': leaders_df['unique_topics'].mean(),
    'avg_farmers_helped': leaders_df['unique_askers_helped'].mean(),
    'repeat_askers_5plus': len(repeat_askers)
}

with open('/home/ubuntu/challenge3_summary.txt', 'w') as f:
    f.write("CHALLENGE 3: COMMUNITY LEADERS - SUMMARY\n")
    f.write("=" * 60 + "\n\n")
    for key, value in summary.items():
        f.write(f"{key}: {value}\n")

print(f"✅ Saved summary to challenge3_summary.txt")

# =============================================================================
# 6. CREATE VISUALIZATIONS
# =============================================================================

print("\n" + "=" * 80)
print("6. CREATING VISUALIZATIONS")
print("=" * 80)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Visualization 1: Top 20 Contributors
fig, ax = plt.subplots(figsize=(12, 8))
top_20 = leaders_df.head(20).sort_values('total_responses')
ax.barh(range(len(top_20)), top_20['total_responses'], color='steelblue')
ax.set_yticks(range(len(top_20)))
ax.set_yticklabels([f"User {uid}" for uid in top_20['user_id']])
ax.set_xlabel('Number of Responses', fontsize=12)
ax.set_title('Top 20 Community Leaders by Response Count', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)

# Add value labels
for i, v in enumerate(top_20['total_responses']):
    ax.text(v + 10, i, f'{v:,}', va='center', fontsize=9)

plt.tight_layout()
plt.savefig('/home/ubuntu/challenge3_viz1_top_contributors.png', dpi=300, bbox_inches='tight')
print("✅ Created visualization 1: Top Contributors")
plt.close()

# Visualization 2: Topic Specialization
fig, ax = plt.subplots(figsize=(10, 6))
topic_data = leaders_df['primary_topic'].value_counts().head(10)
ax.bar(range(len(topic_data)), topic_data.values, color='coral')
ax.set_xticks(range(len(topic_data)))
ax.set_xticklabels(topic_data.index, rotation=45, ha='right')
ax.set_ylabel('Number of Leaders', fontsize=12)
ax.set_title('Leader Specialization by Topic', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

# Add value labels
for i, v in enumerate(topic_data.values):
    ax.text(i, v + 0.5, str(v), ha='center', fontsize=10)

plt.tight_layout()
plt.savefig('/home/ubuntu/challenge3_viz2_topic_specialization.png', dpi=300, bbox_inches='tight')
print("✅ Created visualization 2: Topic Specialization")
plt.close()

# Visualization 3: Response Quality Distribution
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Response length distribution
ax1.hist(leaders_df['avg_response_length'], bins=20, color='mediumseagreen', edgecolor='black', alpha=0.7)
ax1.axvline(leaders_df['avg_response_length'].mean(), color='red', linestyle='--', linewidth=2, label='Mean')
ax1.set_xlabel('Average Response Length (characters)', fontsize=11)
ax1.set_ylabel('Number of Leaders', fontsize=11)
ax1.set_title('Response Quality: Length Distribution', fontsize=13, fontweight='bold')
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

# Farmers helped distribution
ax2.hist(leaders_df['unique_askers_helped'], bins=20, color='mediumpurple', edgecolor='black', alpha=0.7)
ax2.axvline(leaders_df['unique_askers_helped'].mean(), color='red', linestyle='--', linewidth=2, label='Mean')
ax2.set_xlabel('Unique Farmers Helped', fontsize=11)
ax2.set_ylabel('Number of Leaders', fontsize=11)
ax2.set_title('Community Impact: Farmers Helped', fontsize=13, fontweight='bold')
ax2.legend()
ax2.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('/home/ubuntu/challenge3_viz3_quality_metrics.png', dpi=300, bbox_inches='tight')
print("✅ Created visualization 3: Quality Metrics")
plt.close()

print("\n" + "=" * 80)
print("✅ ANALYSIS COMPLETE!")
print("=" * 80)
print("\nGenerated files:")
print("  - challenge3_leaderboard.csv")
print("  - challenge3_summary.txt")
print("  - challenge3_viz1_top_contributors.png")
print("  - challenge3_viz2_topic_specialization.png")
print("  - challenge3_viz3_quality_metrics.png")
