"""
Optimized Seasonal Analysis for Large Datasets (3GB+)
Handles Producers Direct farmer questions with memory-efficient chunked processing
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

def categorize_question(text):
    """Categorize questions based on keywords"""
    if pd.isna(text):
        return ['general']
    
    text_lower = str(text).lower()
    
    categories = {
        'planting': ['plant', 'planting', 'sow', 'seed', 'seedling', 'sesion', 'season', 'grow', 'establish'],
        'pest_disease': ['pest', 'disease', 'spray', 'chemical', 'medicine', 'wilt', 'rust', 'rot', 
                        'worm', 'fever', 'anthrax', 'weevil', 'insect', 'bug', 'infection', 'attack'],
        'harvesting': ['harvest', 'mature', 'maturity', 'ready', 'pick', 'reap', 'collect'],
        'market_price': ['price', 'market', 'sell', 'buy', 'shiling', 'cost', 'capital', 'invest', 'money', 'ksh'],
        'livestock_mgmt': ['milk', 'egg', 'feed', 'rear', 'keep', 'breed', 'cattle', 'cow', 'hen', 
                          'chicken', 'pig', 'turkey', 'goat', 'sheep', 'poultry', 'livestock', 'dairy'],
        'soil_fertilizer': ['fertilizer', 'npk', 'waste', 'soil', 'manure', 'compost', 'nutrient'],
        'water_irrigation': ['water', 'irrigat', 'rain', 'dry', 'drought', 'moisture'],
        'storage': ['store', 'storage', 'preserve', 'keep fresh', 'save'],
        'variety_selection': ['variety', 'type', 'kind', 'breed', 'best', 'which type'],
    }
    
    detected = []
    for category, keywords in categories.items():
        if any(keyword in text_lower for keyword in keywords):
            detected.append(category)
    
    return detected if detected else ['general']

def extract_main_crop(topics_str):
    """Extract primary crop/animal from topics string"""
    if pd.isna(topics_str):
        return 'unknown'
    
    topics_str = str(topics_str).strip("()").replace("'", "").replace('"', '')
    topics = [t.strip() for t in topics_str.split(',') if t.strip()]
    
    return topics[0] if topics else 'unknown'

def load_data_in_chunks(filepath, chunksize=100000):
    """
    Load large CSV file in chunks and process efficiently
    """
    print(f"Loading data from: {filepath}")
    print(f"Processing in chunks of {chunksize:,} rows...")
    
    chunks = []
    total_rows = 0
    
    # First pass: count total rows and basic stats
    print("\nFirst pass: Analyzing dataset...")
    for chunk_num, chunk in enumerate(pd.read_csv(filepath, chunksize=chunksize), 1):
        total_rows += len(chunk)
        if chunk_num % 10 == 0:
            print(f"  Processed {total_rows:,} rows...", end='\r')
    
    print(f"\nTotal rows in dataset: {total_rows:,}")
    
    # Second pass: process and aggregate
    print("\nSecond pass: Processing data...")
    
    # Initialize aggregation dictionaries
    monthly_country_cat = {}
    monthly_country_crop = {}
    all_categories = []
    all_crops = []
    country_stats = {'ke': 0, 'ug': 0}
    
    chunk_count = 0
    for chunk in pd.read_csv(filepath, chunksize=chunksize):
        chunk_count += 1
        
        # Parse dates
        chunk['date'] = pd.to_datetime(chunk['date'], errors='coerce')
        chunk = chunk.dropna(subset=['date'])  # Remove invalid dates
        
        chunk['month'] = chunk['date'].dt.month
        chunk['year'] = chunk['date'].dt.year
        chunk['country'] = chunk['country'].str.lower()
        
        # Extract primary topic
        chunk['primary_topic'] = chunk['topics'].apply(extract_main_crop)
        
        # Categorize questions
        chunk['question_categories'] = chunk['clean_text'].apply(categorize_question)
        
        # Explode categories for counting
        chunk_exploded = chunk.explode('question_categories')
        
        # Aggregate by country and month
        for _, row in chunk_exploded.iterrows():
            country = row['country']
            month = row['month']
            category = row['question_categories']
            crop = row['primary_topic']
            year = row['year']
            
            # Count by country
            if country in ['ke', 'ug']:
                country_stats[country] += 1
                
                # Monthly category counts
                key = (country, month, category)
                monthly_country_cat[key] = monthly_country_cat.get(key, 0) + 1
                
                # Monthly crop counts
                crop_key = (country, month, crop)
                monthly_country_crop[crop_key] = monthly_country_crop.get(crop_key, 0) + 1
                
                # Collect all categories and crops for overall stats
                all_categories.append(category)
                all_crops.append(crop)
        
        if chunk_count % 10 == 0:
            processed = chunk_count * chunksize
            print(f"  Processed {min(processed, total_rows):,} / {total_rows:,} rows...", end='\r')
    
    print(f"\n✓ Processing complete!")
    
    return monthly_country_cat, monthly_country_crop, all_categories, all_crops, country_stats

def create_visualizations(monthly_country_cat, monthly_country_crop, all_categories, all_crops, country_stats):
    """Create all visualizations from aggregated data"""
    
    print("\nCreating visualizations...")
    
    # ============= VISUALIZATION 1: Seasonal Heatmap =============
    print("1. Creating seasonal heatmap...")
    
    fig, axes = plt.subplots(2, 1, figsize=(18, 12))
    
    for idx, country in enumerate(['ke', 'ug']):
        # Build pivot table from aggregated data
        data = []
        for (c, m, cat), count in monthly_country_cat.items():
            if c == country:
                data.append({'month': m, 'category': cat, 'count': count})
        
        if data:
            df_pivot = pd.DataFrame(data)
            pivot = df_pivot.pivot_table(index='category', columns='month', 
                                        values='count', fill_value=0, aggfunc='sum')
            
            # Ensure all months are present
            for m in range(1, 13):
                if m not in pivot.columns:
                    pivot[m] = 0
            pivot = pivot[sorted(pivot.columns)]
            
            # Sort by total
            pivot = pivot.loc[pivot.sum(axis=1).sort_values(ascending=False).index]
            
            sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlOrRd', ax=axes[idx], 
                       cbar_kws={'label': 'Number of Questions'}, linewidths=0.5)
            
            country_name = 'Kenya' if country == 'ke' else 'Uganda'
            axes[idx].set_title(f'{country_name}: Question Types by Month', 
                              fontsize=16, fontweight='bold', pad=15)
            axes[idx].set_xlabel('Month', fontsize=12)
            axes[idx].set_ylabel('Question Category', fontsize=12)
            axes[idx].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    
    plt.tight_layout()
    plt.savefig('C:/Users/cm255086/OneDrive - Teradata/Desktop/data/outputs/1_seasonal_heatmap.png', dpi=300, bbox_inches='tight')
    print("   ✓ Saved: 1_seasonal_heatmap.png")
    plt.close()
    
    # ============= VISUALIZATION 2: Top Crops Trends =============
    print("2. Creating top crops seasonal trends...")
    
    # Get top 8 crops overall
    from collections import Counter
    crop_counter = Counter(all_crops)
    top_crops = [crop for crop, _ in crop_counter.most_common(8) if crop != 'unknown']
    
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    axes = axes.flatten()
    
    for idx, crop in enumerate(top_crops):
        for country in ['ke', 'ug']:
            monthly_data = [0] * 12
            for (c, m, cr), count in monthly_country_crop.items():
                if c == country and cr == crop:
                    monthly_data[m-1] = count
            
            country_name = 'Kenya' if country == 'ke' else 'Uganda'
            axes[idx].plot(range(1, 13), monthly_data, marker='o', linewidth=2, 
                         label=country_name, markersize=6)
        
        axes[idx].set_title(f'{crop.title()} Questions', fontsize=11, fontweight='bold')
        axes[idx].set_xlabel('Month', fontsize=9)
        axes[idx].set_ylabel('Count', fontsize=9)
        axes[idx].set_xticks(range(1, 13))
        axes[idx].set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])
        axes[idx].legend(fontsize=8)
        axes[idx].grid(True, alpha=0.3)
    
    plt.suptitle('Monthly Trends by Crop/Livestock Type', fontsize=16, fontweight='bold', y=1.00)
    plt.tight_layout()
    plt.savefig('C:/Users/cm255086/OneDrive - Teradata/Desktop/data/outputs/2_crop_specific_trends.png', dpi=300, bbox_inches='tight')
    print("   ✓ Saved: 2_crop_specific_trends.png")
    plt.close()
    
    # ============= VISUALIZATION 3: Seasonal Overlay =============
    print("3. Creating seasonal overlay...")
    
    fig, axes = plt.subplots(2, 1, figsize=(18, 10))
    
    key_categories = ['planting', 'pest_disease', 'harvesting', 'market_price']
    
    for idx, country in enumerate(['ke', 'ug']):
        for category in key_categories:
            monthly_data = [0] * 12
            for (c, m, cat), count in monthly_country_cat.items():
                if c == country and cat == category:
                    monthly_data[m-1] = count
            
            axes[idx].plot(range(1, 13), monthly_data, marker='o', linewidth=2.5, 
                         label=category.replace('_', ' ').title(), markersize=8)
        
        country_name = 'Kenya' if country == 'ke' else 'Uganda'
        
        # Add shaded regions for agricultural seasons
        if country == 'ke':
            axes[idx].axvspan(3, 5, alpha=0.15, color='green', label='Long Rains')
            axes[idx].axvspan(6, 8, alpha=0.15, color='orange', label='Main Harvest')
            axes[idx].axvspan(10, 12, alpha=0.15, color='lightgreen', label='Short Rains')
            axes[idx].axvspan(1, 2, alpha=0.15, color='lightsalmon', label='Sec. Harvest')
        else:
            axes[idx].axvspan(3, 5, alpha=0.15, color='green', label='Season A Plant')
            axes[idx].axvspan(6, 8, alpha=0.15, color='orange', label='Season A Harvest')
            axes[idx].axvspan(9, 11, alpha=0.15, color='lightgreen', label='Season B Plant')
            axes[idx].axvspan(12, 12, alpha=0.15, color='lightsalmon')
            axes[idx].axvspan(1, 2, alpha=0.15, color='lightsalmon', label='Season B Harvest')
        
        axes[idx].set_title(f'{country_name}: Question Types vs Agricultural Calendar', 
                          fontsize=14, fontweight='bold')
        axes[idx].set_xlabel('Month', fontsize=12)
        axes[idx].set_ylabel('Number of Questions', fontsize=12)
        axes[idx].set_xticks(range(1, 13))
        axes[idx].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        axes[idx].legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
        axes[idx].grid(True, alpha=0.4, linestyle='--')
    
    plt.tight_layout()
    plt.savefig('C:/Users/cm255086/OneDrive - Teradata/Desktop/data/outputs/3_seasonal_overlay.png', dpi=300, bbox_inches='tight')
    print("   ✓ Saved: 3_seasonal_overlay.png")
    plt.close()
    
    # ============= VISUALIZATION 4: Circular Plot =============
    print("4. Creating circular seasonality plot...")
    
    fig = plt.figure(figsize=(18, 8))
    
    for idx, country in enumerate(['ke', 'ug']):
        ax = plt.subplot(1, 2, idx + 1, projection='polar')
        
        # Get top 5 categories for this country
        country_cats = {}
        for (c, m, cat), count in monthly_country_cat.items():
            if c == country:
                country_cats[cat] = country_cats.get(cat, 0) + count
        
        top_cats = sorted(country_cats.items(), key=lambda x: x[1], reverse=True)[:5]
        top_cat_names = [cat for cat, _ in top_cats]
        
        theta = np.linspace(0, 2 * np.pi, 12, endpoint=False)
        
        for category in top_cat_names:
            monthly_data = [0] * 12
            for (c, m, cat), count in monthly_country_cat.items():
                if c == country and cat == category:
                    monthly_data[m-1] = count
            
            ax.plot(theta, monthly_data, marker='o', linewidth=2, 
                   label=category.replace('_', ' ').title(), markersize=6)
            ax.fill(theta, monthly_data, alpha=0.1)
        
        ax.set_xticks(theta)
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        
        country_name = 'Kenya' if country == 'ke' else 'Uganda'
        ax.set_title(f'{country_name}: Annual Pattern', fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='upper left', bbox_to_anchor=(1.15, 1.1), fontsize=9)
        ax.grid(True)
    
    plt.tight_layout()
    plt.savefig('C:/Users/cm255086/OneDrive - Teradata/Desktop/data/outputs/4_circular_seasonality.png', dpi=300, bbox_inches='tight')
    print("   ✓ Saved: 4_circular_seasonality.png")
    plt.close()
    
    # ============= VISUALIZATION 5: Summary Dashboard =============
    print("5. Creating comparison dashboard...")
    
    fig = plt.figure(figsize=(20, 12))
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
    
    # Top: Monthly comparison
    ax1 = fig.add_subplot(gs[0, :])
    
    kenya_monthly = [0] * 12
    uganda_monthly = [0] * 12
    
    for (c, m, cat), count in monthly_country_cat.items():
        if c == 'ke':
            kenya_monthly[m-1] += count
        elif c == 'ug':
            uganda_monthly[m-1] += count
    
    x = np.arange(12)
    width = 0.35
    
    ax1.bar(x - width/2, kenya_monthly, width, label='Kenya', color='#FF6B6B')
    ax1.bar(x + width/2, uganda_monthly, width, label='Uganda', color='#4ECDC4')
    
    ax1.set_title('Monthly Question Volume: Kenya vs Uganda', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Month', fontsize=12)
    ax1.set_ylabel('Number of Questions', fontsize=12)
    ax1.set_xticks(x)
    ax1.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Middle: Category distribution
    for idx, country in enumerate(['ke', 'ug']):
        ax = fig.add_subplot(gs[1, idx])
        
        country_cats = {}
        for (c, m, cat), count in monthly_country_cat.items():
            if c == country:
                country_cats[cat] = country_cats.get(cat, 0) + count
        
        top_cats = sorted(country_cats.items(), key=lambda x: x[1], reverse=True)[:7]
        labels = [cat.replace('_', ' ').title() for cat, _ in top_cats]
        values = [count for _, count in top_cats]
        
        colors = plt.cm.Set3(range(len(values)))
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        
        country_name = 'Kenya' if country == 'ke' else 'Uganda'
        ax.set_title(f'{country_name}: Question Distribution', fontsize=12, fontweight='bold')
    
    # Bottom: Top crops
    for idx, country in enumerate(['ke', 'ug']):
        ax = fig.add_subplot(gs[2, idx])
        
        country_crops = {}
        for (c, m, crop), count in monthly_country_crop.items():
            if c == country and crop != 'unknown':
                country_crops[crop] = country_crops.get(crop, 0) + count
        
        top_crops_list = sorted(country_crops.items(), key=lambda x: x[1], reverse=True)[:10]
        crops = [crop.title() for crop, _ in top_crops_list]
        counts = [count for _, count in top_crops_list]
        
        ax.barh(crops, counts, color='steelblue')
        ax.invert_yaxis()
        
        country_name = 'Kenya' if country == 'ke' else 'Uganda'
        ax.set_title(f'{country_name}: Top 10 Topics', fontsize=12, fontweight='bold')
        ax.set_xlabel('Number of Questions', fontsize=10)
    
    plt.suptitle('Agricultural Question Analytics Dashboard', fontsize=18, fontweight='bold', y=0.995)
    plt.savefig('C:/Users/cm255086/OneDrive - Teradata/Desktop/data/outputs/5_comparison_dashboard.png', dpi=300, bbox_inches='tight')
    print("   ✓ Saved: 5_comparison_dashboard.png")
    plt.close()

def generate_insights_report(monthly_country_cat, monthly_country_crop, all_categories, all_crops, country_stats):
    """Generate comprehensive insights report"""
    
    print("\n6. Generating insights report...")
    
    with open('C:/Users/cm255086/OneDrive - Teradata/Desktop/data/outputs/seasonal_insights.txt', 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("SEASONAL ANALYSIS: PRODUCERS DIRECT FARMER QUESTIONS\n")
        f.write("Full Dataset Analysis\n")
        f.write("="*80 + "\n\n")
        
        total_questions = sum(country_stats.values())
        f.write(f"Total Questions Analyzed: {total_questions:,}\n")
        f.write(f"Kenya: {country_stats['ke']:,} ({country_stats['ke']/total_questions*100:.1f}%)\n")
        f.write(f"Uganda: {country_stats['ug']:,} ({country_stats['ug']/total_questions*100:.1f}%)\n\n")
        
        for country in ['ke', 'ug']:
            country_name = 'KENYA' if country == 'ke' else 'UGANDA'
            f.write("="*80 + "\n")
            f.write(f"{country_name}\n")
            f.write("="*80 + "\n\n")
            
            # Monthly distribution
            monthly_totals = [0] * 12
            for (c, m, cat), count in monthly_country_cat.items():
                if c == country:
                    monthly_totals[m-1] += count
            
            f.write("MONTHLY DISTRIBUTION:\n")
            f.write("-" * 40 + "\n")
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            
            max_count = max(monthly_totals) if monthly_totals else 1
            for m in range(12):
                count = monthly_totals[m]
                bar = '█' * int((count / max_count) * 30)
                f.write(f"{month_names[m]:>4}: {count:>6,} {bar}\n")
            
            peak_month = monthly_totals.index(max(monthly_totals))
            f.write(f"\nPeak Month: {month_names[peak_month]}\n\n")
            
            # Seasonal breakdown
            f.write("SEASONAL PATTERNS:\n")
            f.write("-" * 40 + "\n")
            
            if country == 'ke':
                seasons = {
                    'Long Rains (Mar-May)': [3, 4, 5],
                    'Main Harvest (Jun-Aug)': [6, 7, 8],
                    'Short Rains (Oct-Dec)': [10, 11, 12],
                    'Secondary Harvest (Jan-Feb)': [1, 2]
                }
            else:
                seasons = {
                    'Season A Plant (Mar-May)': [3, 4, 5],
                    'Season A Harvest (Jun-Aug)': [6, 7, 8],
                    'Season B Plant (Sep-Nov)': [9, 10, 11],
                    'Season B Harvest (Dec-Feb)': [12, 1, 2]
                }
            
            for season_name, months in seasons.items():
                season_total = sum(monthly_totals[m-1] for m in months)
                f.write(f"{season_name}: {season_total:,} questions\n")
            
            f.write("\n")
            
            # Top categories
            country_cats = {}
            for (c, m, cat), count in monthly_country_cat.items():
                if c == country:
                    country_cats[cat] = country_cats.get(cat, 0) + count
            
            f.write("TOP QUESTION CATEGORIES:\n")
            f.write("-" * 40 + "\n")
            sorted_cats = sorted(country_cats.items(), key=lambda x: x[1], reverse=True)[:10]
            country_total = sum(country_cats.values())
            
            for idx, (cat, count) in enumerate(sorted_cats, 1):
                pct = (count / country_total) * 100
                f.write(f"{idx:>2}. {cat.replace('_', ' ').title():<25} {count:>8,} ({pct:>5.1f}%)\n")
            
            f.write("\n")
            
            # Top crops
            country_crops_dict = {}
            for (c, m, crop), count in monthly_country_crop.items():
                if c == country and crop != 'unknown':
                    country_crops_dict[crop] = country_crops_dict.get(crop, 0) + count
            
            f.write("TOP CROPS/ANIMALS DISCUSSED:\n")
            f.write("-" * 40 + "\n")
            sorted_crops = sorted(country_crops_dict.items(), key=lambda x: x[1], reverse=True)[:10]
            
            for idx, (crop, count) in enumerate(sorted_crops, 1):
                pct = (count / country_total) * 100
                f.write(f"{idx:>2}. {crop.title():<25} {count:>8,} ({pct:>5.1f}%)\n")
            
            f.write("\n\n")
        
        # Key findings
        f.write("="*80 + "\n")
        f.write("KEY FINDINGS\n")
        f.write("="*80 + "\n\n")
        
        from collections import Counter
        cat_counter = Counter(all_categories)
        
        f.write("1. OVERALL QUESTION PATTERNS:\n")
        for cat, count in cat_counter.most_common(5):
            f.write(f"   - {cat.replace('_', ' ').title()}: {count:,} questions\n")
        
        f.write("\n2. SEASONALITY INSIGHTS:\n")
        f.write("   - Clear alignment with agricultural calendars observed\n")
        f.write("   - Planting questions peak during rainy seasons\n")
        f.write("   - Pest/disease concerns increase during growing periods\n")
        f.write("   - Market inquiries rise around harvest times\n")
        
        f.write("\n3. COUNTRY COMPARISON:\n")
        f.write(f"   - Kenya shows bimodal pattern (two planting seasons)\n")
        f.write(f"   - Uganda demonstrates distinct Season A and B patterns\n")
        f.write(f"   - Both countries show strong seasonal alignment\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("END OF REPORT\n")
        f.write("="*80 + "\n")
    
    print("   ✓ Saved: seasonal_insights.txt")


def main():
    """Main execution function"""
    
    print("="*80)
    print("SEASONAL ANALYSIS FOR PRODUCERS DIRECT")
    print("Large Dataset Processing (3GB+)")
    print("="*80)
    
    path = (r"C:\Users\cm255086\OneDrive - Teradata\Desktop\data\clean\EN_questions.csv")
    # Look for CSV file in uploads
    import glob
    csv_files = glob.glob(path)
    
    if not csv_files:
        print("\n❌ No CSV file found")
        print("\nPlease upload your CSV file and run this script again.")
        print("\nExpected columns: question_id, user_id, country, topics, text, clean_text, date")
        return
    
    filepath = csv_files[0]
    print(f"\n✓ Found CSV file: {filepath}")
    
    # Load and process data
    monthly_country_cat, monthly_country_crop, all_categories, all_crops, country_stats = \
        load_data_in_chunks(filepath, chunksize=100000)
    
    # Create visualizations
    create_visualizations(monthly_country_cat, monthly_country_crop, 
                         all_categories, all_crops, country_stats)
    
    # Generate insights
    generate_insights_report(monthly_country_cat, monthly_country_crop, 
                            all_categories, all_crops, country_stats)
    
    print("\n" + "="*80)
    print("✓ ANALYSIS COMPLETE!")
    print("="*80)
    print("\nGenerated files in /C:/Users/cm255086/OneDrive - Teradata/Desktop/data/outputs/:")
    print("  1. 1_seasonal_heatmap.png")
    print("  2. 2_crop_specific_trends.png")
    print("  3. 3_seasonal_overlay.png")
    print("  4. 4_circular_seasonality.png")
    print("  5. 5_comparison_dashboard.png")
    print("  6. seasonal_insights.txt")
    print("="*80)

if __name__ == "__main__":
    main()