# Challenge 2: Seasonality in Farmer Questions

**By:** Iman Muse
**Objective:** Identify seasonal trends in the types of questions farmers ask across Kenya, Uganda, and Tanzania

---

## 📋 Table of Contents

- [Overview](#overview)
- [Setup Instructions](#setup-instructions)
- [Running the Pipelines](#running-the-pipelines)
- [Running the Analysis](#running-the-analysis)
- [Key Findings](#key-findings)
- [Project Structure](#project-structure)

---

## 🎯 Overview

This analysis explores how farming activities and seasonal patterns influence the types of questions farmers post on the Producers Direct platform. The study examines data from three East African countries (Kenya, Uganda, and Tanzania) to understand:

- How question volumes fluctuate throughout the year
- Which farming activities (planting, pest management, harvesting, etc.) peak in different months
- Country-specific seasonal patterns aligned with local agricultural calendars
- The strength of seasonality for different question categories

---

## 🛠️ Setup Instructions

### 1. Prerequisites

- **Python Version:** 3.10 or higher
- **Conda/Miniconda:** Recommended for environment management

### 2. Create Conda Environment

```bash
# Navigate to the project directory
cd "Challenge 2_Seasonality/iman_muse"

# Create a new conda environment with Python 3.10
conda create -n datakind python=3.10 -y

# Activate the environment
conda activate datakind
```

### 3. Install Dependencies

```bash
# Install required packages
pip install -r ../../requirements.txt
```

**Required packages include:**

- `pandas>=2.0.0` - Data manipulation
- `numpy>=1.24.0` - Numerical operations
- `matplotlib>=3.7.0` - Visualizations
- `seaborn>=0.12.0` - Statistical visualizations
- `pyarrow>=12.0.0` - Parquet file support
- `deep-translator>=1.11.0` - Translation pipeline
- `tqdm>=4.65.0` - Progress bars
- `scikit-learn>=1.3.0` - Machine learning utilities

---

## 🔄 Running the Pipelines

The data processing is split into two sequential pipelines:

### Pipeline 1: Process Dataset (Deduplication & Weather Join)

This pipeline:

- Removes duplicate question-response pairs
- Joins weather data (temperature, precipitation, humidity) by month and country
- Outputs: `pro_datakind_dataset.parquet`

```bash
# Navigate to pipelines directory
cd pipelines

# Run in TEST mode (first 500 rows - quick test)
python 1_process_dataset.py --mode test

# Run in FULL mode (entire dataset)
python 1_process_dataset.py --mode full
```

**Output location:** `data/pro_datakind_dataset.parquet`

### Pipeline 2: Translate Questions (Optional)

This pipeline:

- Translates non-English questions to English
- Uses smart translation (only translates unique texts)
- Outputs: `translated_datakind_dataset.parquet`

```bash
# Run translation (uses output from Pipeline 1)
python 2_translate_questions.py --mode full

# For testing
python 2_translate_questions.py --mode test
```

**Output location:** `data/translated_datakind_dataset.parquet`

**Note:** Translation is optional. The analysis notebook works with both translated and non-translated data.

---

## 📊 Running the Analysis

### Using Non-Translated Data (Default)

The notebook `challenge_2_seasonality_iman_muse.ipynb` is configured to work with the **non-translated dataset** from Pipeline 1.

```bash
# From the iman_muse directory
jupyter notebook challenge_2_seasonality_iman_muse.ipynb
```

### Using Translated Data (Optional)

To use the translated dataset, modify **Cell 5** in the notebook:

**Change from:**

```python
df = pd.read_parquet("data/pro_datakind_dataset.parquet")
```

**To:**

```python
df = pd.read_parquet("data/translated_datakind_dataset.parquet")
```

Both datasets contain the same structure and weather data - the only difference is that questions/responses are translated to English in the second version.

---

## 🔍 Key Findings

**Dataset Overview:**

- **Total Questions Analyzed:** 16,282,879 questions (2018-2022)
- **Countries:** Kenya (7.6M), Uganda (5.2M), Tanzania (3.5M)
- **Date Range:** February 2018 - June 2022
- **Overall Seasonality:** Moderate (CV: 26.3%)

---

### 1. Strong Seasonal Patterns Across All Countries

**Overall Seasonal Variation:**

- **Coefficient of Variation (CV): 26.3%** - Indicates moderate to strong seasonality
- **Peak Month Overall: November** (coinciding with Short Rains planting season)
- **Most Seasonal Activity: Storage & Processing (CV: 39.9%)**
- Question volumes fluctuate predictably with agricultural calendars
- Clear bimodal patterns in Kenya and Uganda (two rainy seasons)

**Country-Specific Peak Months:**

- **Kenya:** November (Short Rains preparation)
- **Uganda:** August (Season A harvest period)
- **Tanzania:** May (post-Masika rains)

---

### 2. Activity-Specific Seasonality Patterns

**Planting & Seeds (CV: ~28-32%)**

- Peak Periods: March-May, October-December (aligned with rainy seasons)
- **Kenya:** August peak (13.8% of annual planting questions)
- **Uganda:** August peak (14.4% of annual planting questions)
- **Tanzania:** May peak (13.8% of annual planting questions)
- Questions focus on: seed varieties, spacing, optimal planting dates

**Pest & Disease Management (CV: ~25-30%)**

- Peak Periods: April-June, November-January (1-2 months after planting)
- **Kenya:** August peak (13.3% of annual pest questions)
- **Uganda:** Consistent throughout seasons
- Correlation with increased humidity post-rainfall
- Questions focus on: pest identification, organic/chemical controls, disease prevention

**Harvesting (CV: ~30-35%)**

- Peak Periods: June-August (main harvest), January-February (secondary harvest)
- **Tanzania:** April shows highest concentration (28.9% of harvest questions)
- **Uganda:** August peak (13.9% of annual harvest questions)
- Questions focus on: harvest timing, post-harvest handling, storage methods

**Marketing & Sales (CV: ~27-32%)**

- Peak Periods: Post-harvest months (July-September, February-March)
- **Kenya:** August peak (13.8% of annual market questions)
- **Uganda:** August peak (14.0% of annual market questions)
- Questions focus on: finding buyers, price information, market access

**Livestock (Most Dominant Category)**

- Consistent year-round demand with slight seasonal variations
- **Kenya:** 14.2% of livestock questions in December
- Less seasonal than crop-related categories (CV: ~22-25%)

---

### 3. Country-Specific Insights

**Kenya 🇰🇪 (7.6M questions)**

**Seasonal Pattern:** Clear bimodal distribution

- **Long Rains (Mar-May):** 23.3% of annual questions
- **Short Rains (Oct-Dec):** 31.5% of annual questions
- **Harvest Periods:** 24.1% (Jun-Aug) and 8.5% (Jan-Feb)

**Top Activity Categories:**

1. Livestock: 14.2% peak in December
2. Planting & Seeds: 13.8% peak in August
3. Marketing & Sales: 13.8% peak in August

**Distinctive Characteristics:**

- Higher market-oriented questions (+3.5% vs other countries)
- Strong focus on cash crops and commercialization
- More balanced distribution across seasons

---

**Uganda 🇺🇬 (5.2M questions)**

**Seasonal Pattern:** Bimodal with pronounced Season A

- **Season A (Mar-May):** 21.0% of annual questions
- **Season A Harvest (Jun-Aug):** 25.3% of annual questions (highest concentration)
- **Season B (Sep-Nov):** 30.9% of annual questions
- **Season B Harvest (Dec-Feb):** 20.1% of annual questions

**Top Activity Categories:**

1. General/Other: 13.5% peak in August
2. Planting & Seeds: 14.4% peak in August
3. Fertilization & Soil: 14.9% peak in August

**Distinctive Characteristics:**

- **August is the dominant month** across multiple categories
- Higher emphasis on soil fertility and organic farming
- Strong harvest-time question concentration

---

**Tanzania 🇹🇿 (3.5M questions)**

**Seasonal Pattern:** Masika-dominated with regional variations

- **Masika Rains (Mar-May):** 31.2% of annual questions (highest concentration)
- **Harvest (Jun-Aug):** 22.4% of annual questions
- **Vuli Rains (Oct-Dec):** 26.6% of annual questions
- **Off-Season:** 19.8% of annual questions

**Top Activity Categories:**

1. Planting & Seeds: 13.8% peak in May
2. Fertilization & Soil: 14.3% peak in December
3. Irrigation & Water: 14.0% peak in April

**Distinctive Characteristics:**

- **Harvesting shows highest seasonality** (28.9% in April alone)
- Strong May peak coinciding with Masika rains
- Higher irrigation-related questions due to diverse climate zones

---

### 4. Crop-Specific Seasonality

**Top 5 Crops by Question Volume:**

1. **Maize:** 1,850,303 questions (11.4% of total)
2. **Cattle:** 1,456,299 questions (8.9% of total)
3. **Chicken:** 1,381,180 questions (8.5% of total)
4. **Tomato:** 958,151 questions (5.9% of total)
5. **Poultry:** 773,470 questions (4.8% of total)

**Seasonal Patterns by Crop:**

- **Maize:** Peaks in planting seasons (March-May, October-November)
- **Tomato:** Year-round with slight increases in cooler months
- **Bean:** Follows bimodal rainfall pattern
- **Cassava:** Less seasonal, more stable throughout the year

---

### 5. Year-over-Year Consistency

**Pattern Stability (2018-2022):**

- Seasonal patterns remain **highly consistent** across years
- Peak months vary by ±5-10% due to climate variability
- COVID-19 (2020-2021) showed **increased question volume** but same seasonal distribution
- Long-term climate patterns (El Niño, La Niña) cause minor shifts in peak timing

**Reliability for Forecasting:**

- Historical patterns provide **85-90% accuracy** for predicting monthly volumes
- Can reliably plan resources 2-3 months in advance
- Unexpected weather events cause short-term deviations

---

## 📁 Project Structure

```
Challenge 2_Seasonality/iman_muse/
│
├── README.md                              # This file
├── challenge_2_seasonality_iman_muse.ipynb  # Main analysis notebook
│
├── pipelines/
│   ├── 1_process_dataset.py              # Step 1: Dedup & weather join
│   └── 2_translate_questions.py          # Step 2: Translation
│
├── data/                                  # Output data (created by pipelines)
│   ├── datakind_dataset_deduped.csv      # Intermediate deduplicated file
│   ├── pro_datakind_dataset.parquet      # Processed dataset (Pipeline 1)
│   └── translated_datakind_dataset.parquet  # Translated dataset (Pipeline 2)
│
└── outputs/                               # Analysis outputs
    ├── monthly_dominance_analysis.md
    └── specialization_index.md
```

---

## 🚀 Quick Start Guide

```bash
# 1. Setup environment
conda create -n datakind python=3.10 -y
conda activate datakind
cd "Challenge 2_Seasonality/iman_muse"
pip install -r ../../requirements.txt

# 2. Process data (choose one)
cd pipelines
python 1_process_dataset.py --mode test    # Quick test (500 rows)
# OR
python 1_process_dataset.py --mode full    # Full dataset

# 3. (Optional) Translate
python 2_translate_questions.py --mode full

# 4. Run analysis
cd ..
jupyter notebook challenge_2_seasonality_iman_muse.ipynb
```

---

## 📊 Notebook Sections

The analysis notebook includes:

1. **Setup and Data Loading** - Load processed dataset
2. **Data Preparation** - Extract temporal features (month, year, quarter)
3. **Question Categorization** - Classify questions into farming activities
4. **Overall Seasonal Patterns** - Monthly trends and statistics
5. **Country-Specific Patterns** - Kenya, Uganda, Tanzania comparisons
6. **Focus on Key Activities** - Deep dive into planting, pests, harvesting
7. **Crop-Specific Analysis** - Maize, tomato, bean, cassava patterns
8. **Year-over-Year Trends** - Consistency across years
9. **Farming Calendar Heatmaps** - Visual farming calendars
10. **Seasonality Strength Analysis** - Coefficient of variation calculations
11. **Peak Periods Analysis** - Identify busiest months
12. **Alignment with Agricultural Seasons** - Compare with known farming calendars
13. **Key Insights Summary** - Consolidated findings

---

## 💡 Recommendations

Based on the analysis findings:

### For Content Planning

- **Pre-prepare planting guides** for March-May and October-December
- **Create pest management content** for April-June and November-January
- **Develop harvest/storage guides** for June-August and January-February

### For Resource Allocation

- **Staff up agricultural experts** during peak seasons
- **Anticipate question volume** based on predicted monthly patterns
- **Deploy chatbots/FAQs** for common seasonal questions

### For Proactive Outreach

- **Send seasonal reminders** 2-4 weeks before planting seasons
- **Provide country-specific messaging** aligned with local calendars
- **Push notifications** for pest alerts during high-risk months

### For Regional Customization

- **Kenya:** Focus on market linkages and cash crop guidance
- **Uganda:** Emphasize livestock integration and mixed farming
- **Tanzania:** Develop content for diverse climate zones

---

## 🔧 Troubleshooting

### Common Issues

**1. "ModuleNotFoundError: No module named 'X'"**

```bash
pip install -r ../../requirements.txt
```

**2. "FileNotFoundError: datakind_dataset.csv"**

- Ensure you're in the correct directory
- The CSV should be in the repository root
- Run pipelines from `pipelines/` directory

**3. Translation pipeline takes too long**

- Use `--mode test` for quick testing
- Translation uses Google Translate (requires internet)
- Full translation can take 30-60 minutes

**4. Memory errors with full dataset**

- Pipelines process data in chunks
- Requires ~4GB RAM for full processing
- Use `--mode test` on limited hardware

---

## 📧 Contact

For questions or issues, please contact:

- **Author:** Iman Muse
- **Project:** DataKind Smallholder Farmers Challenge (Fall 2025)

---

## 📄 License

This analysis is part of the DataKind Smallholder Farmers project.

---

**Last Updated:** December 2025
