"""
Sample Data Analysis Script for DataKind Producers Direct Challenge

This script provides a template for analyzing the WeFarm dataset.
Adjust paths, column names, and analysis logic based on actual data structure.

Author: hwilner
Date: November 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set visualization style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

class WeFarmAnalyzer:
    """
    A class to analyze WeFarm farmer questions and responses data.
    """
    
    def __init__(self, questions_path, responses_path=None):
        """
        Initialize the analyzer with data paths.
        
        Args:
            questions_path (str): Path to questions dataset
            responses_path (str): Path to responses dataset (optional)
        """
        self.questions_path = questions_path
        self.responses_path = responses_path
        self.questions_df = None
        self.responses_df = None
        
    def load_data(self):
        """Load the datasets."""
        print("Loading data...")
        try:
            self.questions_df = pd.read_csv(self.questions_path)
            print(f"Loaded {len(self.questions_df)} questions")
            
            if self.responses_path:
                self.responses_df = pd.read_csv(self.responses_path)
                print(f"Loaded {len(self.responses_df)} responses")
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
        return True
    
    def explore_data(self):
        """Perform initial data exploration."""
        print("\n" + "="*80)
        print("DATA EXPLORATION")
        print("="*80)
        
        print("\nQuestions Dataset:")
        print(f"Shape: {self.questions_df.shape}")
        print(f"\nColumns: {list(self.questions_df.columns)}")
        print(f"\nData types:\n{self.questions_df.dtypes}")
        print(f"\nMissing values:\n{self.questions_df.isnull().sum()}")
        print(f"\nFirst few rows:\n{self.questions_df.head()}")
        
        if self.responses_df is not None:
            print("\n" + "-"*80)
            print("Responses Dataset:")
            print(f"Shape: {self.responses_df.shape}")
            print(f"\nColumns: {list(self.responses_df.columns)}")
    
    def analyze_languages(self, language_col='language'):
        """Analyze language distribution."""
        if language_col not in self.questions_df.columns:
            print(f"Warning: Column '{language_col}' not found")
            return
        
        print("\n" + "="*80)
        print("LANGUAGE ANALYSIS")
        print("="*80)
        
        language_counts = self.questions_df[language_col].value_counts()
        print("\nQuestions by language:")
        print(language_counts)
        
        # Visualize
        plt.figure(figsize=(10, 6))
        language_counts.plot(kind='bar', color='steelblue')
        plt.title('Distribution of Questions by Language', fontsize=14, fontweight='bold')
        plt.xlabel('Language', fontsize=12)
        plt.ylabel('Number of Questions', fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('language_distribution.png', dpi=300, bbox_inches='tight')
        print("\nSaved visualization: language_distribution.png")
        plt.show()
    
    def analyze_temporal_patterns(self, date_col='date'):
        """Analyze temporal patterns in questions."""
        if date_col not in self.questions_df.columns:
            print(f"Warning: Column '{date_col}' not found")
            return
        
        print("\n" + "="*80)
        print("TEMPORAL ANALYSIS")
        print("="*80)
        
        # Convert to datetime
        self.questions_df[date_col] = pd.to_datetime(self.questions_df[date_col])
        
        # Extract temporal features
        self.questions_df['year'] = self.questions_df[date_col].dt.year
        self.questions_df['month'] = self.questions_df[date_col].dt.month
        self.questions_df['year_month'] = self.questions_df[date_col].dt.to_period('M')
        
        # Questions over time
        questions_by_month = self.questions_df.groupby('year_month').size()
        
        print(f"\nDate range: {self.questions_df[date_col].min()} to {self.questions_df[date_col].max()}")
        print(f"Total months: {len(questions_by_month)}")
        
        # Visualize
        plt.figure(figsize=(14, 6))
        questions_by_month.plot(color='darkgreen')
        plt.title('Questions Over Time', fontsize=14, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Number of Questions', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('questions_over_time.png', dpi=300, bbox_inches='tight')
        print("\nSaved visualization: questions_over_time.png")
        plt.show()
        
        # Seasonality analysis
        monthly_avg = self.questions_df.groupby('month').size()
        
        plt.figure(figsize=(10, 6))
        monthly_avg.plot(kind='bar', color='coral')
        plt.title('Average Questions by Month (Seasonality)', fontsize=14, fontweight='bold')
        plt.xlabel('Month', fontsize=12)
        plt.ylabel('Number of Questions', fontsize=12)
        plt.xticks(range(12), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=45)
        plt.tight_layout()
        plt.savefig('seasonality.png', dpi=300, bbox_inches='tight')
        print("Saved visualization: seasonality.png")
        plt.show()
    
    def extract_keywords(self, text_col='question_text', top_n=20):
        """Extract and visualize top keywords."""
        if text_col not in self.questions_df.columns:
            print(f"Warning: Column '{text_col}' not found")
            return
        
        print("\n" + "="*80)
        print("KEYWORD ANALYSIS")
        print("="*80)
        
        from collections import Counter
        import re
        
        # Simple stopwords (expand as needed)
        stopwords = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 
                        'to', 'for', 'of', 'with', 'is', 'are', 'was', 'were'])
        
        # Extract all words
        all_words = []
        for text in self.questions_df[text_col].dropna():
            words = re.findall(r'\b\w+\b', str(text).lower())
            words = [w for w in words if w not in stopwords and len(w) > 3]
            all_words.extend(words)
        
        # Count and get top keywords
        word_counts = Counter(all_words)
        top_keywords = word_counts.most_common(top_n)
        
        print(f"\nTop {top_n} keywords:")
        for word, count in top_keywords:
            print(f"  {word}: {count}")
        
        # Visualize
        keywords_df = pd.DataFrame(top_keywords, columns=['Keyword', 'Count'])
        
        plt.figure(figsize=(10, 8))
        plt.barh(keywords_df['Keyword'], keywords_df['Count'], color='teal')
        plt.xlabel('Frequency', fontsize=12)
        plt.title(f'Top {top_n} Keywords in Questions', fontsize=14, fontweight='bold')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig('top_keywords.png', dpi=300, bbox_inches='tight')
        print("\nSaved visualization: top_keywords.png")
        plt.show()
        
        return keywords_df
    
    def generate_summary_report(self):
        """Generate a summary report of key statistics."""
        print("\n" + "="*80)
        print("SUMMARY REPORT")
        print("="*80)
        
        report = {
            'Total Questions': len(self.questions_df),
            'Date Range': f"{self.questions_df['date'].min()} to {self.questions_df['date'].max()}" if 'date' in self.questions_df.columns else 'N/A',
            'Languages': self.questions_df['language'].nunique() if 'language' in self.questions_df.columns else 'N/A',
            'Missing Values': self.questions_df.isnull().sum().sum(),
        }
        
        if self.responses_df is not None:
            report['Total Responses'] = len(self.responses_df)
        
        for key, value in report.items():
            print(f"{key}: {value}")
        
        return report


def main():
    """Main execution function."""
    print("DataKind Producers Direct - WeFarm Data Analysis")
    print("="*80)
    
    # Initialize analyzer (adjust paths as needed)
    # analyzer = WeFarmAnalyzer('path/to/questions.csv', 'path/to/responses.csv')
    
    # For demonstration, using placeholder
    print("\nNote: Update the data paths in the script to run the analysis")
    print("Example usage:")
    print("  analyzer = WeFarmAnalyzer('questions.csv', 'responses.csv')")
    print("  analyzer.load_data()")
    print("  analyzer.explore_data()")
    print("  analyzer.analyze_languages()")
    print("  analyzer.analyze_temporal_patterns()")
    print("  analyzer.extract_keywords()")
    print("  analyzer.generate_summary_report()")


if __name__ == "__main__":
    main()
