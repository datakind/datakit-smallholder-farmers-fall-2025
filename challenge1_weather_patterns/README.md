# Challenge 1: Weather Patterns and Farmer Questions

## Overview

This analysis investigates how weather patterns affect the types and volumes of questions farmers ask on the Producers Direct platform. By correlating weather events (rainfall, temperature extremes, drought, heat waves) with question patterns across Kenya, Uganda, and Tanzania from 2015-2022, we aim to provide actionable insights for proactive information delivery.

## Goal

Understand how weather patterns affect the types of questions farmers ask, enabling Producers Direct to anticipate farmer needs and deliver timely, relevant information.

## Research Questions

### Primary Questions
1. **How do question volumes or topics change during specific weather conditions (rain, heat, drought)?**
2. **Can we predict the kinds of questions likely to appear given a weather forecast?**
3. **Are certain crops or regions more sensitive to weather-driven question patterns?**

### Key Hypotheses
- **H1**: Pest-related questions increase 1-2 weeks after heavy rainfall (due to increased humidity)
- **H2**: Water/irrigation questions spike during drought periods
- **H3**: Crop stress questions increase during heat waves
- **H4**: Planting questions peak 2-4 weeks before rainy seasons
- **H5**: Arid regions show stronger weather-question correlations than humid regions

## Data Sources

### 1. WeFarm Dataset (Producers Direct Legacy Data)
- **Size**: 7.6M+ questions, 17.2M+ responses
- **Time Period**: 2015-2022
- **Languages**: Swahili, Luganda, Nyn, English
- **Geographic Coverage**: Kenya, Uganda, Tanzania
- **Access**: Via DataKind Slack channel

### 2. Weather Data

#### Primary: NASA POWER API
- **Parameters**: Temperature (min/max/avg), Precipitation, Humidity, Wind Speed
- **Resolution**: Daily, 0.5° x 0.625° (~50 km)
- **Coverage**: 1981-present (using 2015-2022)
- **Access**: Free API, no authentication required
- **Documentation**: https://power.larc.nasa.gov/docs/

#### Supplementary: CHIRPS (Climate Hazards Group InfraRed Precipitation with Station data)
- **Parameters**: Rainfall
- **Resolution**: Daily, 0.05° (~5.5 km)
- **Coverage**: 1981-present
- **Use**: High-resolution rainfall validation

#### Context: ARC2 (African Rainfall Climatology Version 2)
- **Parameters**: Rainfall
- **Resolution**: Monthly, 0.1° (~11 km)
- **Coverage**: 1983-present
- **Use**: Regional rainfall patterns

## Methodology

### Phase 1: Data Collection and Preparation
1. Access WeFarm dataset from DataKind Slack
2. Download weather data using NASA POWER API for Kenya, Uganda, Tanzania (2015-2022)
3. Clean and preprocess both datasets
4. Align timestamps and geographic locations

### Phase 2: Exploratory Data Analysis
1. Visualize question volumes over time
2. Visualize weather patterns over time
3. Identify seasonal patterns and trends
4. Categorize questions by topic (pests, water, planting, harvest, crop stress)

### Phase 3: Correlation Analysis
1. Calculate correlations between weather variables and question volumes
2. Perform lag correlation analysis (0-28 days)
3. Conduct event-based analysis (droughts, heavy rainfall, heat waves)
4. Statistical significance testing

### Phase 4: Visualization and Reporting
1. Create time series visualizations
2. Generate correlation heatmaps
3. Produce event impact comparisons
4. Write comprehensive analysis report

### Phase 5: Predictive Modeling (Stretch Goal)
1. Feature engineering (weather features, lag features, temporal features)
2. Train machine learning models (Random Forest, XGBoost)
3. Evaluate model performance
4. Demonstrate forecast capability

## Project Structure

```
challenge1_weather_patterns/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── data/
│   ├── raw/                          # Raw data files
│   │   ├── wefarm_questions.csv      # Original question data
│   │   ├── weather_kenya.csv         # Kenya weather data
│   │   ├── weather_uganda.csv        # Uganda weather data
│   │   └── weather_tanzania.csv      # Tanzania weather data
│   └── processed/                    # Processed data files
│       ├── questions_daily.csv       # Daily aggregated questions
│       ├── weather_daily.csv         # Daily weather data
│       └── merged_data.csv           # Merged questions + weather
├── notebooks/
│   ├── 01_data_collection.ipynb      # Download and collect data
│   ├── 02_data_preprocessing.ipynb   # Clean and prepare data
│   ├── 03_exploratory_analysis.ipynb # EDA and visualizations
│   ├── 04_correlation_analysis.ipynb # Statistical analysis
│   └── 05_visualization.ipynb        # Final visualizations
├── scripts/
│   ├── download_weather_data.py      # Automated weather data download
│   ├── preprocess_questions.py       # Question data preprocessing
│   ├── calculate_correlations.py     # Correlation calculations
│   └── create_visualizations.py      # Visualization generation
├── visualizations/
│   ├── question_volume_timeseries.png
│   ├── weather_patterns.png
│   ├── correlation_heatmap.png
│   ├── lag_correlation.png
│   ├── event_impact.png
│   └── ...
└── report/
    └── weather_patterns_analysis_report.md  # Final analysis report
```

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Internet connection (for API access)

### Installation

1. **Clone the repository**
```bash
cd /home/ubuntu/datakit-smallholder-farmers-fall-2025/challenge1_weather_patterns
```

2. **Install dependencies**
```bash
pip3 install -r requirements.txt
```

3. **Download WeFarm dataset**
- Join DataKind Slack channel
- Download dataset from provided link
- Place in `data/raw/wefarm_questions.csv`

## Usage

### Quick Start

1. **Download weather data**
```bash
python3 scripts/download_weather_data.py
```

2. **Preprocess question data**
```bash
python3 scripts/preprocess_questions.py
```

3. **Run exploratory analysis**
```bash
jupyter notebook notebooks/03_exploratory_analysis.ipynb
```

4. **Calculate correlations**
```bash
python3 scripts/calculate_correlations.py
```

5. **Generate visualizations**
```bash
python3 scripts/create_visualizations.py
```

### Step-by-Step Workflow

#### Step 1: Data Collection
Run the data collection notebook to download weather data from NASA POWER API:
```bash
jupyter notebook notebooks/01_data_collection.ipynb
```

This will:
- Download daily weather data for Kenya, Uganda, Tanzania (2015-2022)
- Save raw data to `data/raw/`
- Validate data quality

#### Step 2: Data Preprocessing
Run the preprocessing notebook to clean and prepare data:
```bash
jupyter notebook notebooks/02_data_preprocessing.ipynb
```

This will:
- Clean question data (remove duplicates, parse timestamps)
- Categorize questions by topic using keywords
- Aggregate questions by day/week/month
- Align weather data with question timestamps
- Save processed data to `data/processed/`

#### Step 3: Exploratory Analysis
Run the exploratory analysis notebook:
```bash
jupyter notebook notebooks/03_exploratory_analysis.ipynb
```

This will:
- Visualize question volumes over time
- Visualize weather patterns over time
- Identify seasonal patterns
- Create initial correlation plots

#### Step 4: Correlation Analysis
Run the correlation analysis notebook:
```bash
jupyter notebook notebooks/04_correlation_analysis.ipynb
```

This will:
- Calculate Pearson correlations
- Perform lag correlation analysis
- Conduct event-based analysis
- Statistical significance testing
- Generate correlation heatmaps

#### Step 5: Final Visualizations
Run the visualization notebook to create publication-quality plots:
```bash
jupyter notebook notebooks/05_visualization.ipynb
```

This will:
- Create all final visualizations
- Save high-resolution images to `visualizations/`
- Generate summary dashboard

## Expected Deliverables

### 1. Analysis Report
- **File**: `report/weather_patterns_analysis_report.md`
- **Length**: 8-12 pages
- **Content**: Executive summary, methodology, findings, recommendations

### 2. Visualizations (8-10 high-quality plots)
- Question volume time series
- Weather patterns time series
- Dual-axis plots (questions vs weather)
- Correlation heatmaps
- Lag correlation plots
- Event impact comparisons
- Seasonal patterns
- Regional comparisons

### 3. Code and Notebooks
- Fully documented Jupyter notebooks
- Reusable Python scripts
- Clean, commented code

### 4. Key Insights Document
- 1-2 page summary of top findings
- Actionable recommendations for Producers Direct

### 5. Predictive Model (Stretch Goal)
- Trained model file
- Model evaluation report
- Feature importance analysis

## Key Findings (To Be Completed)

_This section will be populated after analysis is complete._

### Top Correlations Discovered
1. TBD
2. TBD
3. TBD

### Optimal Lag Periods
- Rainfall → Pest questions: TBD days
- Drought → Water questions: TBD days
- Temperature → Crop stress: TBD days

### Regional Variations
- Kenya: TBD
- Uganda: TBD
- Tanzania: TBD

### Recommendations for Producers Direct
1. TBD
2. TBD
3. TBD

## Timeline

- **Day 1 (4 hours)**: Data collection and initial exploration
- **Day 2 (4 hours)**: Data preprocessing and topic categorization
- **Day 3 (4 hours)**: Correlation analysis and statistical testing
- **Day 4 (2-3 hours)**: Report writing and documentation
- **Day 5 (Optional, 3-4 hours)**: Predictive modeling

**Total Estimated Time**: 8-12 hours (core) + 3-4 hours (stretch goal)

## Dependencies

See `requirements.txt` for full list. Key packages:
- pandas: Data manipulation
- numpy: Numerical operations
- matplotlib: Visualization
- seaborn: Statistical visualization
- requests: API calls
- scipy: Statistical testing
- statsmodels: Time series analysis
- scikit-learn: Machine learning (optional)

## Contributing

This is part of the DataKind Producers Direct DataKit Challenge. Contributions and collaboration are welcome!

### How to Contribute
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request
5. Share on DataKind Slack

### Questions or Collaboration
- Post in DataKind Slack channel
- Tag @hwilner for questions about this analysis

## License

This project is part of the DataKind Producers Direct DataKit Challenge. Please refer to the main repository for licensing information.

## Acknowledgments

- **DataKind** for organizing the DataKit Challenge
- **Producers Direct** for providing the dataset
- **NASA POWER** for free weather data API
- **CHIRPS** and **ARC2** for supplementary rainfall data

## Contact

- **Contributor**: hwilner
- **GitHub**: https://github.com/hwilner
- **DataKind Slack**: @hwilner

## References

### Data Sources
1. NASA POWER API: https://power.larc.nasa.gov/
2. CHIRPS: https://www.chc.ucsb.edu/data/chirps
3. ARC2: https://www.icpac.net/data-center/arc2/

### Methodology References
1. Gebrechorkos et al. (2019). "Long-term trends in rainfall and temperature using high-resolution climate datasets in East Africa." Scientific Reports.
2. Ongoma & Chen (2017). "Temporal and spatial variability of temperature and precipitation over East Africa from 1951 to 2010." Meteorology and Atmospheric Physics.

---

**Last Updated**: November 5, 2025  
**Status**: In Progress  
**Version**: 1.0
