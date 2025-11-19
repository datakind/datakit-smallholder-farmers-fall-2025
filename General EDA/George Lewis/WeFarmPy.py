import pandas as pd
import numpy as np
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
import warnings
from matplotlib import pyplot as plt
warnings.filterwarnings('ignore')

class DataCleaning:
    """
    This class provides a clean, reproducible pipeline for:
    - Standardising country codes (ISO 3166-1 alpha-3)
    - Parsing all datetime fields with timezone handling
    - Extracting temporal features (year, month, day, hour, season)
    """
    
    # ISO 3166-1 alpha-3 country code mapping
    COUNTRY_CODE_MAP = {
        'ke': 'KEN',  # Kenya
        'ug': 'UGA',  # Uganda
        'tz': 'TZA',  # Tanzania
    }
    
    # Language code standardization
    LANGUAGE_CODE_MAP = {
        'eng': 'English',
        'swa': 'Swahili',
        'lug': 'Luganda',
        'nyn': 'Runyankore-Rukiga'
    }
    
    # Farming seasons by country (for context enrichment)
    FARMING_SEASONS = {
        'KEN': {
            'long_rains': (3, 5),      # March-May (main planting)
            'short_rains': (10, 12),   # October-December (secondary)
            'harvest_1': (6, 8),       # June-August
            'harvest_2': (1, 2),       # January-February
        },
        'UGA': {
            'season_a_plant': (3, 5),  # March-May
            'season_a_harvest': (6, 8), # June-August
            'season_b_plant': (9, 11),  # September-November
            'season_b_harvest': (12, 2), # December-February
        },
        'TZA': {
            'masika_rains': (3, 5),    # March-May (main)
            'vuli_rains': (10, 12),    # October-December (some regions)
            'harvest': (6, 8),         # June-August
        }
    }
    
    def __init__(self, verbose: bool = True):
        """
        Initialize data processor
        
        Args:
            verbose: Whether to print processing steps
        """
        self.verbose = verbose
        self.processing_log = []
        
    def _log(self, message: str):
        """Log processing step"""
        self.processing_log.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
        if self.verbose:
            print(message)
    
    def _standardize_country_codes(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert country codes to ISO 3166-1 alpha-3 format
        
        Args:
            df: Input dataframe
            
        Returns:
            DataFrame with standardized country codes
        """
        self._log("Standardizing country codes to ISO 3166-1 alpha-3...")
        
        country_cols = [col for col in df.columns if 'country_code' in col]
        
        for col in country_cols:
            original_values = df[col].value_counts()
            df[col] = df[col].map(self.COUNTRY_CODE_MAP).fillna(df[col])
            new_values = df[col].value_counts()
            
            if self.verbose:
                print(f"  {col}:")
                print(f"    Before: {dict(original_values)}")
                print(f"    After:  {dict(new_values)}")
        
        return df
    
    def _parse_datetime_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Parse all datetime columns with proper timezone handling
        
        Args:
            df: Input dataframe
            
        Returns:
            DataFrame with parsed datetime columns
        """
        self._log("Parsing datetime columns...")
        
        # Identify datetime columns
        datetime_cols = [col for col in df.columns 
                        if any(x in col for x in ['sent', 'created_at', 'dob'])]
        
        for col in datetime_cols:
            try:
                # Parse with UTC timezone awareness
                df[col] = pd.to_datetime(df[col], utc=True, errors='coerce',format='mixed')
                
                non_null_count = df[col].notna().sum()
                null_count = df[col].isna().sum()
                
                if non_null_count > 0:
                    date_range = f"{df[col].min()} to {df[col].max()}"
                else:
                    date_range = "No valid dates"
                
                if self.verbose:
                    print(f"  {col}:")
                    print(f"    Valid: {non_null_count:,} | Null: {null_count:,}")
                    print(f"    Range: {date_range}")
                    
            except Exception as e:
                self._log(f"  Warning: Failed to parse {col}: {str(e)}")
        
        return df
    
    def _add_temporal_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract temporal features from datetime columns
        
        Args:
            df: Input dataframe
            
        Returns:
            DataFrame with additional temporal feature columns
        """
        self._log("Extracting temporal features...")
        
        # Question temporal features
        if 'question_sent' in df.columns and pd.api.types.is_datetime64_any_dtype(df['question_sent']):
            df['question_year'] = df['question_sent'].dt.year
            df['question_month'] = df['question_sent'].dt.month
            df['question_day'] = df['question_sent'].dt.day
            df['question_hour'] = df['question_sent'].dt.hour
            df['q_hour_local'] = (df['question_sent']
                                          .dt.tz_convert('Africa/Nairobi')
                                          .dt.hour)
            df['question_dayofweek'] = df['question_sent'].dt.dayofweek
            df['question_quarter'] = df['question_sent'].dt.quarter
            
            # Create year-month period for time series
            df['question_year_month'] = df['question_sent'].dt.to_period('M')
            
            if self.verbose:
                print(f"  Added temporal features for questions")
        
        # Response temporal features
        if 'response_sent' in df.columns and pd.api.types.is_datetime64_any_dtype(df['response_sent']):
            df['response_year'] = df['response_sent'].dt.year
            df['response_month'] = df['response_sent'].dt.month
            df['response_day'] = df['response_sent'].dt.day
            df['response_hour'] = df['response_sent'].dt.hour
            df['r_hour_local'] = (df['response_sent']
                                  .dt.tz_convert('Africa/Nairobi')
                                  .dt.hour)
            df['response_dayofweek'] = df['response_sent'].dt.dayofweek
            
            # Calculate response time (if both timestamps valid)
            df['response_time_hours'] = (
                (df['response_sent'] - df['question_sent']).dt.total_seconds() / 3600
            )
            
            if self.verbose:
                print(f"  Added temporal features for responses")
                valid_response_times = df['response_time_hours'].dropna()
                if len(valid_response_times) > 0:
                    print(f"    Response time: median={valid_response_times.median():.1f}h, "
                          f"mean={valid_response_times.mean():.1f}h")
        
        return df
    
    def _add_farming_season_context(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add farming season context based on country and month
        
        Args:
            df: Input dataframe
            
        Returns:
            DataFrame with farming season indicators
        """
        self._log("Adding farming season context...")
        
        if 'question_month' not in df.columns or 'question_user_country_code' not in df.columns:
            self._log("  Skipping: Required columns not found")
            return df
        
        def get_season(row):
            """Determine farming season for a given row"""
            country = row.get('question_user_country_code')
            month = row.get('question_month')
            
            if pd.isna(country) or pd.isna(month):
                return None
            
            if country not in self.FARMING_SEASONS:
                return None
            
            seasons = self.FARMING_SEASONS[country]
            active_seasons = []
            
            for season_name, (start_month, end_month) in seasons.items():
                # Handle seasons that span year boundary
                if start_month <= end_month:
                    if start_month <= month <= end_month:
                        active_seasons.append(season_name)
                else:  # Wraps around year (e.g., Dec-Feb)
                    if month >= start_month or month <= end_month:
                        active_seasons.append(season_name)
            
            return ','.join(active_seasons) if active_seasons else 'off_season'
        
        df['farming_season'] = df.apply(get_season, axis=1)
        
        if self.verbose:
            season_counts = df['farming_season'].value_counts()
            print(f"  Farming season distribution:")
            for season, count in season_counts.head(5).items():
                print(f"    {season}: {count:,}")
        
        return df
    
    def _add_standardized_season(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add standardized season labels (rainy/harvest) across countries
        """
        if 'question_month' not in df.columns or 'question_user_country_code' not in df.columns:
            return df

        def get_standardized_season(row):
            """Map to standardized rainy/harvest seasons"""
            country = row.get('question_user_country_code')
            month = row.get('question_month')

            if pd.isna(country) or pd.isna(month):
                return None

            # Standardized season mapping
            # Rainy = planting seasons
            # Harvest = harvest seasons

            if country == 'KEN':
                if 3 <= month <= 5:  # Long rains
                    return 'rainy_main'
                elif 10 <= month <= 12:  # Short rains
                    return 'rainy_secondary'
                elif 6 <= month <= 8:  # Harvest 1
                    return 'harvest_main'
                elif month in [1, 2]:  # Harvest 2
                    return 'harvest_secondary'

            elif country == 'UGA':
                if 3 <= month <= 5:  # Season A plant
                    return 'rainy_main'
                elif 9 <= month <= 11:  # Season B plant
                    return 'rainy_secondary'
                elif 6 <= month <= 8:  # Season A harvest
                    return 'harvest_main'
                elif month in [12, 1, 2]:  # Season B harvest
                    return 'harvest_secondary'

            elif country == 'TZA':
                if 3 <= month <= 5:  # Masika rains
                    return 'rainy_main'
                elif 10 <= month <= 12:  # Vuli rains
                    return 'rainy_secondary'
                elif 6 <= month <= 8:  # Harvest
                    return 'harvest_main'

            return 'off_season'

        df['season_standardized'] = df.apply(get_standardized_season, axis=1)

        if self.verbose:
            season_counts = df['season_standardized'].value_counts()
            print(f"  Standardized seasons:")
            for season, count in season_counts.items():
                print(f"    {season}: {count:,}")

        return df
    
    def _compute_data_completeness(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add data completeness metrics per row
        
        Args:
            df: Input dataframe
            
        Returns:
            DataFrame with completeness metrics
        """
        self._log("Computing data completeness metrics...")
        
        # Core fields completeness
        core_fields = [
            'question_content', 'question_language', 'question_user_country_code',
            'response_content', 'response_language'
        ]
        
        available_core = [f for f in core_fields if f in df.columns]
        df['core_fields_complete_pct'] = (
            df[available_core].notna().sum(axis=1) / len(available_core) * 100
        )
        
        # User metadata completeness
        user_metadata_fields = [
            'question_user_gender', 'question_user_dob',
            'response_user_gender', 'response_user_dob'
        ]
        
        available_metadata = [f for f in user_metadata_fields if f in df.columns]
        if available_metadata:
            df['user_metadata_complete_pct'] = (
                df[available_metadata].notna().sum(axis=1) / len(available_metadata) * 100
            )
        
        # Has topic labels
        if 'question_topic' in df.columns:
            df['has_question_topic'] = df['question_topic'].notna()
        
        if 'response_topic' in df.columns:
            df['has_response_topic'] = df['response_topic'].notna()
        
        if self.verbose:
            print(f"  Core fields completeness: {df['core_fields_complete_pct'].mean():.1f}% avg")
            if 'user_metadata_complete_pct' in df.columns:
                print(f"  User metadata completeness: {df['user_metadata_complete_pct'].mean():.1f}% avg")
        
        return df
    
    def _add_text_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract text-based features (length, word count, etc.)
        
        Args:
            df: Input dataframe
            
        Returns:
            DataFrame with text features
        """
        self._log("Extracting text features...")
        
        if 'question_content' in df.columns:
            df['question_length_chars'] = df['question_content'].fillna('').str.len()
            df['question_word_count'] = df['question_content'].fillna('').str.split().str.len()
            
            if self.verbose:
                print(f"  Question length: median={df['question_length_chars'].median():.0f} chars, "
                      f"mean={df['question_length_chars'].mean():.0f} chars")
        
        if 'response_content' in df.columns:
            df['response_length_chars'] = df['response_content'].fillna('').str.len()
            df['response_word_count'] = df['response_content'].fillna('').str.split().str.len()
            
            if self.verbose:
                print(f"  Response length: median={df['response_length_chars'].median():.0f} chars, "
                      f"mean={df['response_length_chars'].mean():.0f} chars")
        
        return df
    
    def _standardize_language_codes(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add human-readable language names
        
        Args:
            df: Input dataframe
            
        Returns:
            DataFrame with language name columns
        """
        self._log("Adding language names...")
        
        lang_cols = [col for col in df.columns if 'language' in col and col.endswith('language')]
        
        for col in lang_cols:
            name_col = col.replace('language', 'language_name')
            df[name_col] = df[col].map(self.LANGUAGE_CODE_MAP).fillna(df[col])
            
            if self.verbose:
                print(f"  {col} -> {name_col}")
        
        return df
    
    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Main processing pipeline
        
        Args:
            df: Raw input dataframe
            
        Returns:
            Cleaned and enriched dataframe
        """
        self._log(f"Starting data processing pipeline on {len(df):,} rows...")
        self._log("="*80)
        
        # Create copy to avoid modifying original
        df_clean = df.copy()
        
        # Remove unnamed index column if present
        if 'Unnamed: 0' in df_clean.columns:
            df_clean = df_clean.drop(columns=['Unnamed: 0'])
        
        # Execute pipeline
        df_clean = self._parse_datetime_columns(df_clean)
        df_clean = self._standardize_country_codes(df_clean)
        df_clean = self._standardize_language_codes(df_clean)
        df_clean = self._add_temporal_features(df_clean)
        df_clean = self._add_farming_season_context(df_clean)
        df_clean = self._add_standardized_season(df_clean)
        df_clean = self._add_text_features(df_clean)
        df_clean = self._compute_data_completeness(df_clean)
        
        # Rename columns to more readable format
        rename_map = {
            # Core IDs - keep as is, they're fine
            'question_id': 'q_id',
            'response_id': 'r_id',
            'question_user_id': 'q_user_id',
            'response_user_id': 'r_user_id',

            # Content
            'question_content': 'q_text',
            'response_content': 'r_text',
            'question_topic': 'q_topic',
            'response_topic': 'r_topic',

            # Languages
            'question_language': 'q_lang_code',
            'response_language': 'r_lang_code',
            'question_language_name': 'q_language',
            'response_language_name': 'r_language',

            # Timestamps
            'question_sent': 'q_datetime',
            'response_sent': 'r_datetime',
            'question_user_created_at': 'q_user_joined',
            'response_user_created_at': 'r_user_joined',
            'question_user_dob': 'q_user_dob',
            'response_user_dob': 'r_user_dob',

            # User attributes
            'question_user_type': 'q_user_type',
            'question_user_status': 'q_user_status',
            'question_user_country_code': 'q_country',
            'question_user_gender': 'q_gender',
            'response_user_type': 'r_user_type',
            'response_user_status': 'r_user_status',
            'response_user_country_code': 'r_country',
            'response_user_gender': 'r_gender',

            # Temporal features
            'question_year': 'q_year',
            'question_month': 'q_month',
            'question_day': 'q_day',
            'question_hour': 'q_hour',
            'question_dayofweek': 'q_weekday',
            'question_quarter': 'q_quarter',
            'question_year_month': 'q_year_month',
            'response_year': 'r_year',
            'response_month': 'r_month',
            'response_day': 'r_day',
            'response_hour': 'r_hour',
            'response_dayofweek': 'r_weekday',
            'response_time_hours': 'response_time_hrs',

            # Context
            'farming_season': 'season',
            'season_standardized':'season_std',

            # Text features
            'question_length_chars': 'q_chars',
            'question_word_count': 'q_words',
            'response_length_chars': 'r_chars',
            'response_word_count': 'r_words',

            # Quality metrics
            'core_fields_complete_pct': 'completeness_pct',
            'user_metadata_complete_pct': 'metadata_pct',
            'has_question_topic': 'has_q_topic',
            'has_response_topic': 'has_r_topic',
        }

        df_clean = df_clean.rename(columns=rename_map)
        
        # filter out gb country
        df_clean = df_clean[df_clean['q_country']!='gb'][df_clean['r_country']!='gb']

        self._log("="*80)
        self._log(f"Processing complete! Output: {len(df_clean):,} rows, "
                 f"{len(df_clean.columns)} columns (+{len(df_clean.columns) - len(df.columns)} added)")
        
        return df_clean
    
    
class EDA:
    ''' Exploratory visualisation of cleaned dataset '''
    def plot_temporal_overview(df: pd.DataFrame, 
                               figsize: tuple = (15, 10)) -> plt.Figure:
        """
        Create comprehensive temporal analysis visualization
        
        Args:
            df: Processed dataframe
            figsize: Figure size
            
        Returns:
            Matplotlib figure
        """
        fig, axes = plt.subplots(3, 2, figsize=figsize)
        fig.suptitle('Temporal Analysis Overview', fontsize=16, fontweight='bold')
        
        # 1. Questions over time (time series)
        if 'q_year_month' in df.columns:
            ax = axes[0, 0]
            questions_by_month = df.groupby('q_year_month').size()
            questions_by_month.plot(ax=ax, color='#2ecc71', linewidth=2)
            ax.set_title('Questions Over Time', fontweight='bold')
            ax.set_xlabel('Date')
            ax.set_ylabel('Number of Questions')
            ax.grid(True, alpha=0.3)
            
            # Manually set xlim with padding
            dates = questions_by_month.index.to_timestamp()
            padding = pd.Timedelta(days=30)  # 15 days padding
            ax.set_xlim(dates.min() - padding, dates.max() + padding)
        
        # 2. Questions by year
        if 'q_year' in df.columns:
            ax = axes[0, 1]
            year_counts = df['q_year'].value_counts().sort_index()
            ax.bar(year_counts.index, year_counts.values, color='#3498db', alpha=0.7)
            ax.set_title('Questions by Year', fontweight='bold')
            ax.set_xlabel('Year')
            ax.set_ylabel('Count')
            ax.grid(True, alpha=0.3, axis='y')
            
            # Manually set xlim with padding
            ax.set_xlim(year_counts.index.min() - 1, year_counts.index.max() + 1)
        
        # 3. Seasonality (by month)
        if 'q_month' in df.columns:
            ax = axes[1, 0]
            month_counts = df['q_month'].value_counts().sort_index()
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            ax.bar(range(1, 13), [month_counts.get(i, 0) for i in range(1, 13)],
                  color='#e74c3c', alpha=0.7)
            ax.set_title('Seasonality (Questions by Month)', fontweight='bold')
            ax.set_xlabel('Month')
            ax.set_ylabel('Count')
            ax.set_xticks(range(1, 13))
            ax.set_xticklabels(month_names, rotation=45)
            ax.grid(True, alpha=0.3, axis='y')
        
        # 4. Hour of day distribution
        if 'q_hour' in df.columns:
            ax = axes[1, 1]
            hour_counts = df['q_hour_local'].value_counts().sort_index()
            ax.plot(hour_counts.index, hour_counts.values, marker='o', 
                   color='#9b59b6', linewidth=2, markersize=6)
            ax.set_title('Activity by Hour of Day', fontweight='bold')
            ax.set_xlabel('Hour (24h)')
            ax.set_ylabel('Count')
            ax.set_xticks(range(0, 24, 3))
            ax.grid(True, alpha=0.3)
        
        # 5. Day of week distribution
        if 'q_weekday' in df.columns:
            ax = axes[2, 0]
            dow_counts = df['q_weekday'].value_counts().sort_index()
            dow_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            ax.bar(range(7), [dow_counts.get(i, 0) for i in range(7)],
                  color='#1abc9c', alpha=0.7)
            ax.set_title('Activity by Day of Week', fontweight='bold')
            ax.set_xlabel('Day')
            ax.set_ylabel('Count')
            ax.set_xticks(range(7))
            ax.set_xticklabels(dow_names)
            ax.grid(True, alpha=0.3, axis='y')
        
        # 6. Response time distribution
        if 'response_time_hrs' in df.columns:
            ax = axes[2, 1]
            response_times = df['response_time_hrs'].dropna()
            if len(response_times) > 0:
                # Convert hours to days
                response_times_days = response_times / 24

                # Create log-spaced bins for better distribution
                bins = np.logspace(np.log10(response_times_days.min() + 0.01), 
                                  np.log10(response_times_days.max()), 
                                  30)

                # Plot histogram
                ax.hist(response_times_days, bins=bins,
                       color='#f39c12', alpha=0.7, edgecolor='black')
                ax.set_title('Response Time Distribution', fontweight='bold')
                ax.set_xlabel('Number of days for response')
                ax.set_ylabel('Count')
                ax.set_xscale('log')  # Log scale makes the uneven bins look even
                ax.grid(True, alpha=0.3, axis='y')

                # Add median line
                median_days = response_times_days.median()
                ax.axvline(median_days, color='red', linestyle='--', 
                          linewidth=2, label=f'Median: {median_days:.1f} days')
                ax.legend()
        
        plt.tight_layout()
        return fig
    
    def plot_geographic_overview(df: pd.DataFrame,
                             figsize: tuple = (18, 12)) -> plt.Figure:
        """
        Create geographic distribution visualization

        Args:
            df: Processed dataframe
            figsize: Figure size

        Returns:
            Matplotlib figure
        """
        from adjustText import adjust_text

        fig = plt.figure(figsize=figsize)
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

        fig.suptitle('Geographic Analysis Overview', fontsize=16, fontweight='bold')

        # 1. Questions by country
        if 'q_country' in df.columns:
            ax = fig.add_subplot(gs[0, 0])
            country_counts = df['q_country'].value_counts()
            colors = plt.cm.Set3(range(len(country_counts)))
            ax.bar(country_counts.index, country_counts.values, color=colors, alpha=0.8)
            ax.set_title('Questions by Country', fontweight='bold')
            ax.set_ylabel('Count')
            ax.grid(True, alpha=0.3, axis='y')

            # Add percentage labels
            for i, (country, count) in enumerate(country_counts.items()):
                pct = count / len(df) * 100
                ax.text(i, count, f'{pct:.1f}%', ha='center', va='bottom')

        # 2. Responses by country
        if 'r_country' in df.columns:
            ax = fig.add_subplot(gs[0, 1])
            country_counts = df['r_country'].value_counts()
            colors = plt.cm.Set3(range(len(country_counts)))
            ax.bar(country_counts.index, country_counts.values, color=colors, alpha=0.8)
            ax.set_title('Responses by Country', fontweight='bold')
            ax.set_ylabel('Count')
            ax.grid(True, alpha=0.3, axis='y')

        # 3. Standardized seasonal distribution
        if 'season_std' in df.columns and 'q_country' in df.columns:
            ax = fig.add_subplot(gs[1, :])  # Full width

            season_country = pd.crosstab(df['season_std'], df['q_country'])
            season_country_pct = season_country.div(season_country.sum(axis=0), axis=1) * 100

            season_order = ['rainy_main', 'rainy_secondary', 'harvest_main', 'harvest_secondary', 'off_season']
            season_labels = ['Main Rainy\n(Planting)', 'Secondary Rainy\n(Planting)', 
                             'Main Harvest', 'Secondary Harvest', 'Off Season']

            countries_list = season_country_pct.columns.tolist()
            n_countries = len(countries_list)

            x = np.arange(len(season_order))
            width = 0.25
            offsets = np.linspace(-(n_countries-1)*width/2, (n_countries-1)*width/2, n_countries)

            for i, country in enumerate(countries_list):
                percentages = [season_country_pct.loc[season, country] 
                               if season in season_country_pct.index else 0 
                               for season in season_order]

                bars = ax.bar(x + offsets[i], percentages, width, 
                              label=f'{country} (n={season_country[country].sum():.0f})',
                              color=f'C{i}', alpha=0.8, edgecolor='black', linewidth=1.5)

                for bar, pct in zip(bars, percentages):
                    if pct > 2:
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                               f'{pct:.1f}%', ha='center', va='bottom', 
                               fontsize=8, fontweight='bold')

            ax.set_xlabel('Season Type', fontsize=11, fontweight='bold')
            ax.set_ylabel('% of Questions', fontsize=11, fontweight='bold')
            ax.set_title('Standardized Seasonal Distribution by Country', fontweight='bold', fontsize=12)
            ax.set_xticks(x)
            ax.set_xticklabels(season_labels, fontsize=10)
            ax.legend(loc='upper right', fontsize=10, framealpha=0.95)
            ax.grid(True, alpha=0.3, axis='y', linestyle='--', linewidth=0.5)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

        # 4. Topic flow across countries (Sankey-style with adjustText)
        if 'q_topic' in df.columns and 'q_country' in df.columns:
            ax = fig.add_subplot(gs[2, :])  # Full width

            # Get topic percentages by country
            topic_country = pd.crosstab(df['q_topic'], df['q_country'])
            topic_country_pct = topic_country.div(topic_country.sum(axis=0), axis=1) * 100

            # Get top 10 per country
            top_per_country = {}
            countries = topic_country_pct.columns
            for country in countries:
                top_per_country[country] = topic_country_pct[country].nlargest(10)

            # Union of all top topics
            all_top_topics = set()
            for topics in top_per_country.values():
                all_top_topics.update(topics.index)

            # Create data matrix
            topic_data = {}
            for topic in all_top_topics:
                topic_data[topic] = [topic_country_pct.loc[topic, c] if topic in topic_country_pct.index else 0 
                                     for c in countries]

            # Sort by total prevalence
            topic_data = dict(sorted(topic_data.items(), key=lambda x: sum(x[1]), reverse=True))

            countries_list = list(countries)
            x_positions = range(len(countries_list))

            # Plot lines and collect text objects for adjustment
            texts = []

            for topic, y_values in topic_data.items():
                in_top_10 = [topic in top_per_country[c].index for c in countries_list]
                num_top_10 = sum(in_top_10)

                if num_top_10 >= 3:
                    alpha, linewidth, color = 0.9, 2.5, 'C0'
                elif num_top_10 >= 2:
                    alpha, linewidth, color = 0.7, 2, 'C1'
                elif num_top_10 == 1:
                    alpha, linewidth, color = 0.5, 1.5, 'C2'
                else:
                    alpha, linewidth, color = 0.15, 0.5, 'gray'

                ax.plot(x_positions, y_values, 'o-', 
                       alpha=alpha, linewidth=linewidth, color=color, 
                       markersize=6, markeredgecolor='white', markeredgewidth=1)

                # Create text labels (will be adjusted later)
                for i, (country, y_val, is_top) in enumerate(zip(countries_list, y_values, in_top_10)):
                    if is_top:
                        bbox_props = dict(boxstyle='round,pad=0.3', facecolor='white', 
                                        edgecolor='black', linewidth=1, alpha=0.95)

                        text = ax.text(i, y_val, f'{topic}\n{y_val:.1f}%', 
                                      fontsize=7, fontweight='bold', ha='center', va='center',
                                      bbox=bbox_props, zorder=10)
                        texts.append(text)

            # Adjust text positions to avoid overlap
            adjust_text(texts, ax=ax,
                       arrowprops=dict(arrowstyle='->', color='gray', lw=0.5, alpha=0.5),
                       expand_points=(5, 1),
                       expand_text=(1.2, 1.2),
                       force_points=(0.5, 0.5),
                       force_text=(0.5, 0.5))

            ax.set_xticks(x_positions)
            ax.set_xticklabels([f'{c}\n(n={topic_country[c].sum():.0f})' 
                                for c in countries_list], fontsize=11, fontweight='bold')
            ax.set_ylabel('% of Questions', fontsize=11, fontweight='bold')
            ax.set_title('Topic Flow Across Countries (Top 10 per country)', fontweight='bold', fontsize=12)
            ax.set_xlim(-0.5, len(countries_list) - 0.5)
            ax.grid(True, alpha=0.3, axis='y', linestyle='--', linewidth=0.5)

            # Legend
            from matplotlib.lines import Line2D
            legend_elements = [
                Line2D([0], [0], color='C0', linewidth=2.5, label='Top 10 in 3+ countries'),
                Line2D([0], [0], color='C1', linewidth=2, label='Top 10 in 2 countries'),
                Line2D([0], [0], color='C2', linewidth=1.5, label='Top 10 in 1 country'),
            ]
            ax.legend(handles=legend_elements, loc='upper left', fontsize=9, framealpha=0.95)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

        plt.tight_layout()
        return fig
    
    def plot_linguistic_overview(df: pd.DataFrame,
                             figsize: tuple = (16, 10)) -> plt.Figure:
        """
        Create linguistic distribution visualization
        Args:
            df: Processed dataframe
            figsize: Figure size
        Returns:
            Matplotlib figure
        """
        fig = plt.figure(figsize=figsize)
        gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

        fig.suptitle('Linguistic Analysis Overview', fontsize=16, fontweight='bold')

        # 1. Questions by language (pie chart)
        if 'q_language' in df.columns:
            ax = fig.add_subplot(gs[0, 0])
            lang_counts = df['q_language'].value_counts()

            # Create pie chart
            colors = plt.cm.Set2(range(len(lang_counts)))
            wedges, texts, autotexts = ax.pie(lang_counts.values, 
                                               labels=lang_counts.index,
                                               autopct='%1.1f%%',
                                               colors=colors,
                                               startangle=90)
            ax.set_title('Questions by Language', fontweight='bold')

            # Make percentage text bold
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')

        # 2. Language match between questions and responses
        if 'q_language' in df.columns and 'r_language' in df.columns:
            ax = fig.add_subplot(gs[0, 1])

            # Check if languages match
            df_temp = df.copy()
            df_temp['lang_match'] = (df_temp['q_language'] == 
                                     df_temp['r_language'])
            match_counts = df_temp['lang_match'].value_counts()

            colors = ['#2ecc71', '#e74c3c']
            ax.bar(range(len(match_counts)), match_counts.values, 
                  color=colors[:len(match_counts)], alpha=0.7)
            ax.set_title('Question-Response Language Match', fontweight='bold')
            ax.set_xticks(range(len(match_counts)))
            ax.set_xticklabels(['Match' if x else 'Mismatch' 
                               for x in match_counts.index])
            ax.set_ylabel('Count')
            ax.grid(True, alpha=0.3, axis='y')

            # Add percentage labels
            for i, count in enumerate(match_counts.values):
                pct = count / match_counts.sum() * 100
                ax.text(i, count, f'{pct:.1f}%', ha='center', va='bottom')

        # 3. Language distribution by country (stacked bar chart)
        if 'q_language' in df.columns and 'q_country' in df.columns:
            ax = fig.add_subplot(gs[1, :])  # Full width bottom row

            # Create crosstab of language by country
            lang_country = pd.crosstab(df['q_language'], df['q_country'])

            # Convert to percentages (% within each country)
            lang_country_pct = lang_country.div(lang_country.sum(axis=0), axis=1) * 100

            # Transpose so countries are on x-axis
            lang_country_pct_T = lang_country_pct.T

            # Plot stacked bars
            lang_country_pct_T.plot(kind='bar', stacked=True, ax=ax, 
                                    colormap='Set3', width=0.7, 
                                    edgecolor='black', linewidth=1.5)

            # Styling
            ax.set_title('Language Distribution by Country', fontweight='bold', fontsize=13)
            ax.set_xlabel('Country', fontsize=11, fontweight='bold')
            ax.set_ylabel('% of Questions', fontsize=11, fontweight='bold')
            ax.set_xticklabels(ax.get_xticklabels(), rotation=0, fontsize=10)
            ax.set_ylim(0, 100)
            ax.grid(True, alpha=0.3, axis='y', linestyle='--', linewidth=0.5)

            # Add country totals to x-labels
            new_labels = [f'{country}\n(n={lang_country[country].sum():.0f})' 
                          for country in lang_country_pct_T.index]
            ax.set_xticklabels(new_labels, rotation=0, fontsize=10)

            # Legend
            ax.legend(title='Language', bbox_to_anchor=(1.02, 1), loc='upper left', 
                     fontsize=9, title_fontsize=10, framealpha=0.95, edgecolor='black')

            # Add percentage labels on segments (if > 5%)
            for i, country in enumerate(lang_country_pct_T.index):
                cumsum = 0
                for language in lang_country_pct_T.columns:
                    pct = lang_country_pct_T.loc[country, language]
                    if pct > 5:  # Only label if > 5%
                        ax.text(i, cumsum + pct/2, f'{pct:.1f}%', 
                               ha='center', va='center', fontsize=8, 
                               fontweight='bold', color='white',
                               bbox=dict(boxstyle='round,pad=0.3', facecolor='black', 
                                       alpha=0.3, edgecolor='none'))
                    cumsum += pct

            # Clean up spines
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

        plt.tight_layout()
        return fig
    
    def plot_user_overview(df: pd.DataFrame,
                      figsize: tuple = (18, 10)) -> plt.Figure:
        """
        Create user behavior visualization

        Args:
            df: Processed dataframe
            figsize: Figure size

        Returns:
            Matplotlib figure
        """
        from scipy.stats import pearsonr
        from datetime import datetime

        fig = plt.figure(figsize=figsize)
        gs = fig.add_gridspec(2, 4, hspace=0.3, wspace=0.3)

        fig.suptitle('User Behavior Overview', fontsize=16, fontweight='bold')

        # 1. User status distribution (questions)
        if 'q_user_status' in df.columns:
            ax = fig.add_subplot(gs[0, 0])
            status_counts = df['q_user_status'].value_counts()
            colors = plt.cm.Set1(range(len(status_counts)))
            ax.bar(status_counts.index, status_counts.values, 
                  color=colors, alpha=0.7)
            ax.set_title('Question User Status', fontweight='bold')
            ax.set_ylabel('Count')
            ax.grid(True, alpha=0.3, axis='y')

            # Add percentage labels
            for i, (status, count) in enumerate(status_counts.items()):
                pct = count / len(df) * 100
                ax.text(i, count, f'{pct:.1f}%', ha='center', va='bottom')

        # 2. Gender distribution (if available)
        if 'q_gender' in df.columns:
            ax = fig.add_subplot(gs[0, 1])
            gender_counts = df['q_gender'].value_counts()

            if len(gender_counts) > 0:
                colors = plt.cm.Pastel1(range(len(gender_counts)))
                wedges, texts, autotexts = ax.pie(gender_counts.values,
                                                   labels=gender_counts.index,
                                                   autopct='%1.1f%%',
                                                   colors=colors,
                                                   startangle=90)
                ax.set_title('Gender Distribution (Question Users)', fontweight='bold')

                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
            else:
                ax.text(0.5, 0.5, 'No gender data available', 
                       ha='center', va='center', transform=ax.transAxes)

        # 3. User age distribution (from DOB)
        if 'q_user_dob' in df.columns:
            ax = fig.add_subplot(gs[0, 2])

            # Calculate age from DOB
            df_temp = df.copy()
            current_year = datetime.now().year
            df_temp['age'] = current_year - pd.to_datetime(df_temp['q_user_dob'], errors='coerce').dt.year

            # Filter reasonable ages (15-90)
            ages = df_temp['age'][(df_temp['age'] >= 15) & (df_temp['age'] <= 90)].dropna()

            if len(ages) > 0:
                # Histogram
                ax.hist(ages, bins=20, color='#3498db', alpha=0.7, edgecolor='black')
                ax.set_title(f'Age Distribution (n={len(ages):,})', fontweight='bold')
                ax.set_xlabel('Age (years)')
                ax.set_ylabel('Count')
                ax.grid(True, alpha=0.3, axis='y')

                # Add median line and stats
                median_age = ages.median()
                ax.axvline(median_age, color='red', linestyle='--', 
                          linewidth=2, label=f'Median: {median_age:.0f}')

                # Add stats text
                stats_text = (f"Mean: {ages.mean():.1f}\n"
                             f"Median: {median_age:.0f}\n"
                             f"Range: {ages.min():.0f}-{ages.max():.0f}")
                ax.text(0.95, 0.95, stats_text, transform=ax.transAxes,
                       verticalalignment='top', horizontalalignment='right',
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))
                ax.legend(loc='upper left')
            else:
                ax.text(0.5, 0.5, 'No age data available', 
                       ha='center', va='center', transform=ax.transAxes)

        # 4. User activity distribution
        if 'q_user_id' in df.columns:
            ax = fig.add_subplot(gs[0, 3])

            # Questions per user
            user_activity = df.groupby('q_user_id').size()

            # Histogram of activity
            ax.hist(user_activity.values, bins=min(30, len(user_activity)), 
                   color='#9b59b6', alpha=0.7, edgecolor='black')
            ax.set_title('Questions per User Distribution', fontweight='bold')
            ax.set_xlabel('Number of Questions')
            ax.set_ylabel('Number of Users')
            ax.grid(True, alpha=0.3, axis='y')
            ax.set_yscale('log')

            # Add stats text
            stats_text = (f"Mean: {user_activity.mean():.1f}\n"
                         f"Median: {user_activity.median():.1f}\n"
                         f"Max: {user_activity.max()}")
            ax.text(0.95, 0.95, stats_text, transform=ax.transAxes,
                   verticalalignment='top', horizontalalignment='right',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        # 5. Text length distribution
        if 'q_chars' in df.columns:
            ax = fig.add_subplot(gs[1, 0])

            lengths = df['q_chars'].dropna()

            # Histogram
            ax.hist(lengths, bins=30, color='#e67e22', alpha=0.7, edgecolor='black')
            ax.set_title('Question Length Distribution', fontweight='bold')
            ax.set_xlabel('Characters')
            ax.set_ylabel('Count')
            ax.grid(True, alpha=0.3, axis='y')

            # Add median line
            median_val = lengths.median()
            ax.axvline(median_val, color='red', linestyle='--', 
                      linewidth=2, label=f'Median: {median_val:.0f}')
            ax.legend()

        # 6. Question vs Response Length Correlation (hexbin)
        if 'q_chars' in df.columns and 'r_chars' in df.columns:
            ax = fig.add_subplot(gs[1, 1:])  # Span 3 columns

            data = df[['q_chars', 'r_chars']].dropna()

            if len(data) > 0:
                # Hexbin plot (shows density)
                hexbin = ax.hexbin(data['q_chars'], data['r_chars'], 
                                  gridsize=50, cmap='YlOrRd', mincnt=1,
                                  edgecolors='black', linewidths=0.2)

                # Colorbar
                cb = plt.colorbar(hexbin, ax=ax, label='Count')

                # Add regression line
                z = np.polyfit(data['q_chars'], data['r_chars'], 1)
                p = np.poly1d(z)
                x_line = np.linspace(data['q_chars'].min(), data['q_chars'].max(), 100)
                ax.plot(x_line, p(x_line), "blue", linewidth=3, 
                       label='Linear fit', linestyle='--')

                # Calculate correlation
                corr, pval = pearsonr(data['q_chars'], data['r_chars'])

                # Add correlation text
                textstr = f'Pearson r = {corr:.3f}\np < 0.001' if pval < 0.001 else f'Pearson r = {corr:.3f}\np = {pval:.3f}'
                props = dict(boxstyle='round', facecolor='white', alpha=0.95, 
                            edgecolor='black', linewidth=2)
                ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=12,
                       verticalalignment='top', bbox=props, fontweight='bold')

                # Add sample size
                ax.text(0.95, 0.05, f'n = {len(data):,}', transform=ax.transAxes,
                       fontsize=10, ha='right', va='bottom',
                       bbox=dict(boxstyle='round', facecolor='white', alpha=0.95, 
                               edgecolor='black'))

                # Styling
                ax.set_xlabel('Question Length (characters)', fontsize=11, fontweight='bold')
                ax.set_ylabel('Response Length (characters)', fontsize=11, fontweight='bold')
                ax.set_title('Correlation: Question vs Response Length', 
                            fontsize=12, fontweight='bold')
                ax.legend(loc='lower right', fontsize=10, framealpha=0.95, 
                         edgecolor='black')

        plt.tight_layout()
        return fig
    
    def plot_data_quality(df: pd.DataFrame,
                         figsize: tuple = (14, 6)) -> plt.Figure:
        """
        Create data quality visualization
        
        Args:
            df: Processed dataframe
            figsize: Figure size
            
        Returns:
            Matplotlib figure
        """
        fig, axes = plt.subplots(1, 2, figsize=figsize)
        fig.suptitle('Data Quality Overview', fontsize=16, fontweight='bold')
        
        # 1. Missing data by column
        ax = axes[0]
        
        # Calculate missing percentages
        missing_pct = (df.isnull().sum() / len(df) * 100).sort_values(ascending=False)
        missing_pct = missing_pct[missing_pct > 0].head(15)
        
        if len(missing_pct) > 0:
            colors = ['#e74c3c' if x > 50 else '#f39c12' if x > 20 else '#2ecc71' 
                     for x in missing_pct.values]
            
            ax.barh(range(len(missing_pct)), missing_pct.values, color=colors, alpha=0.7)
            ax.set_yticks(range(len(missing_pct)))
            ax.set_yticklabels(missing_pct.index)
            ax.set_title('Top 15 Columns with Missing Data', fontweight='bold')
            ax.set_xlabel('Missing (%)')
            ax.grid(True, alpha=0.3, axis='x')
            ax.invert_yaxis()
            
            # Add value labels
            for i, v in enumerate(missing_pct.values):
                ax.text(v, i, f' {v:.1f}%', va='center')
        
        # 2. Completeness score distribution
        ax = axes[1]
        
        if 'completeness_pct' in df.columns:
            completeness = df['completeness_pct']
            
            # Histogram
            ax.hist(completeness, bins=20, color='#16a085', alpha=0.7, edgecolor='black')
            ax.set_title('Core Fields Completeness Distribution', fontweight='bold')
            ax.set_xlabel('Completeness (%)')
            ax.set_ylabel('Count')
            ax.grid(True, alpha=0.3, axis='y')
            
            # Add stats
            stats_text = (f"Mean: {completeness.mean():.1f}%\n"
                         f"Median: {completeness.median():.1f}%")
            ax.text(0.05, 0.95, stats_text, transform=ax.transAxes,
                   verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()

        return fig