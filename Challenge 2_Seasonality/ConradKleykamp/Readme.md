# Conrad Kleykamp

Folder containing my work for Challenge #2. Please scroll through this readme to view an overview of each of my submissions.

Current submission count: 2

---

## **Submission #1: Initial EDA (Country, Language, Time)**

### Overview

This notebook contains the initial exploratory data analysis for identifying suitable countries to analyze seasonal patterns that influence farmer question patterns.

### Approach

**Data Loading & Preparation**
- Loading data from Parquet format
- Parsing datetime fields using ISO8601 format to handle mixed precision timestamps
- Grouping data by country code to assess volume and language distributions

**Country Selection Criteria**
- English prevalence: >70% English language questions
- Question volume: >100,000 questions for statistical robustness
- Temporal coverage: >3 years to capture seasonal patterns

**Analysis Components**
- Country-level statistics: Question volumes, language distributions, temporal coverage
- Temporal analysis: Monthly question volume trends by country
- Language composition: English vs. non-English question proportions
- Visual comparisons: Six panel visualization stack

### Dependencies
- pandas >= 1.5.0
- numpy >= 1.23.0
- matplotlib >= 3.6.0
- seaborn >= 0.12.0

### Results
- Kenya (KE): 9.76M questions, 77.0% English, 4.6 years (2017-2022)
- Uganda (UG): 6.31M questions, 70.7% English, 3.8 years (2017-2021)
- Tanzania (TZ): 4.23M questions, 0.00% English 3.8 years (2017-2021)
- Great Britain (GB): 316 questions, 100% English, 3.5 years (2017-2021)

<img width="1318" height="1940" alt="image" src="https://github.com/user-attachments/assets/fa5dbd94-6927-499f-a236-6fd0a51bb065" />

---

## **Submission #2: Kenya Seasonality/Temporal Question Volume**

### Overview

This notebook contains an exploratory data analysis of Kenya farmer question volume (English questions) across years, months, and meteorological/agricultural seasons. This provides a basic understanding of the distribution of Kenya questions across planting and harvesting seasons. The next step will involve drilling down to word categories/topics and attempt to uncover more precise seasonal patterns.

### Approach

**Data Loading & Preparation**
- Loading data from Parquet format
- Parsing datetime fields using ISO8601 format to handle mixed precision timestamps

**Preprocessing & Feature Engineering**
- Isolated 9.76M Kenya questions from 20.3M total questions across 4 countries, then filtered to 7.5M English questions (77% of Kenya total, 37% of grand total)
- Added temporal variables (e.g. year, month, quarter, day of year) and boolean indicators for agricultural seasons.
- Generated standard meteorological seasons (Southern Hemisphere) and Kenya-specific agricultural seasons aligned with climate patterns (provided by DataKind)

**Analysis Components**
- Question Volume Over Time
- Questions by Month (All Years Combined)
- Questions by Standard Meteorological Season
- Questions by Kenya Agricultural Season
- Visualizations: Four panel visualization stack

### Dependencies
- pandas >= 1.5.0
- numpy >= 1.23.0
- matplotlib >= 3.6.0
- seaborn >= 0.12.0

### Results
- Peak WeFarm platform engagement from late 2018 to early 2019 with monthly volumes exceeding 500,000
- Post 2020 decline in question volume, suggesting gradual decrease in platform engagement
- **High activity period**: August-December (>690K questions/month) spanning late Harvest 1 through Short Rains planting season
- **Peak months**: August (921K) and November (942K)
- **Low activity period**: January-February (355K-335K) during Harvest 2 season
- **Short rains dominance**: Secondary planting season (Oct-Dec) generated ~2.5M questions, exceeding primary planting / Long Rains season (Mar-May) at ~1.7M questions
- **Agricultural calendar alignment**: Question patterns closely track Kenya's dual rainy seasons, with farmers demonstrating highest information needs during pre-planting preparation and the secondary planting period rather than the main growing season.

<img width="4378" height="3392" alt="image" src="https://github.com/user-attachments/assets/d92de2a4-6d69-4a9f-826b-b0a04ae6ac66" />

