# Conrad Kleykamp

Folder containing my work for Challenge #2. Please scroll through this readme to view an overview of each of my submissions.

Current submission count: 3

---

## **Submission #1: Initial EDA (Country, Language, Time)**

### Overview

This notebook contains the initial exploratory data analysis for identifying suitable countries to analyze seasonal patterns that influence farmer question patterns.

### Approach

**Data Loading & Preparation**
- Loaded data from Parquet format
- Parsed datetime fields using ISO8601 format to handle mixed precision timestamps
- Grouped data by country code to assess volume and language distributions

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
- pandas >= 2.2.3
- numpy >= 1.26.4
- matplotlib >= 3.6.0
- seaborn >= 0.12.2

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
- Loaded data from Parquet format
- Parsed datetime fields using ISO8601 format to handle mixed precision timestamps

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
- pandas >= 2.2.3
- numpy >= 1.26.4
- matplotlib >= 3.6.0
- seaborn >= 0.12.2

### Results
- Peak WeFarm platform engagement from late 2018 to early 2019 with monthly volumes exceeding 500,000
- Post 2020 decline in question volume, suggesting gradual decrease in platform engagement
- **High activity period**: August-December (>690K questions/month) spanning late Harvest 1 through Short Rains planting season
- **Peak months**: August (921K) and November (942K)
- **Low activity period**: January-February (355K-335K) during Harvest 2 season
- **Short rains dominance**: Secondary planting season (Oct-Dec) generated ~2.5M questions, exceeding primary planting / Long Rains season (Mar-May) at ~1.7M questions
- **Agricultural calendar alignment**: Question patterns closely track Kenya's dual rainy seasons, with farmers demonstrating highest information needs during pre-planting preparation and the secondary planting period rather than the main growing season.

<img width="4378" height="3392" alt="image" src="https://github.com/user-attachments/assets/d92de2a4-6d69-4a9f-826b-b0a04ae6ac66" />

---

## **Submission #3: Kenya Seasonal/Temporal Word Analysis**

### Overview

This notebook contains an analysis of word frequency across different temporal ranges (Kenya agricultural season, standard meteorological season, month. This analysis uncovers dominant words that appear more frequently in Kenyan farmer questionnaires. 

### Approach

**Data Loading & Preparation**
- Loaded dataset previously generated from second submission (see above)
- 7.5 Kenya English language questions

**Natural Language Processing**
- Extracted words using regex tokenization (3+ character alphabetic tokens, lowercase)
- Applied NLTK stopwords corpus (English) supplemented with custom agricultural terms
- Total stop words filtered: 223

**Temporal Frequency Calculation**
- Built word frequency distributions for three temporal groupings using Counter objects

**Top Word Identification**
- Extracted top 20 words per temporal period, filtering words appearing more than 75 times
- Calculated two metrics per word: (1) frequency per 1,000 questions for normalized comparison, and (2) percentage of total filtered words for relative importance within each period

**Visualization**
- Generated a three-panel stacked heatmap showing the top 15 most frequent words (per 1000 questions) across all temporal groups
- Applied RdYlGn_r color palette for optimal contrast across frequency ranges

### Dependencies
- pandas >= 2.2.3
- numpy >= 1.26.4
- matplotlib >= 3.6.0
- seaborn >= 0.12.2
- nltk >= 3.9.2
  
### Results
**Dominant Agricultural Terms**
- Core agricultural vocabulary remains consistent across all temporal groupings
- "plant" and "maize" consistently constitute the top 2 words across all temporal periods
- Both terms exhibit their highest frequencies during the Transition agricultural season (Sep): "plant" 183.3 per 1K, "maize" 216.4 per 1K

**Ranking of Agricultural/Animal Products**
- Most common agricultural/animal products ranked by average frequency across Kenya agricultural seasons (highest to lowest):
  - Maize
  - Cow
  - Beans
  - Tomatoes
  - Chicken
  - Potatoes
  - Dairy
  - Chicks

**Maize Patterns**
- Exhibits highest frequencies during September (216.4 per 1K) and October (284.7 per 1K)
- Suggests farmers prepare for/plant maize most frequently during Transition period (Sep) into beginning of Short Rains/secondary planting season (Oct)
- Maintains consistently high frequency (>105.0 per 1K) across all agricultural seasons, indicating year-round cultivation with multiple planting/harvest cycles

**Cow Patterns**
- Third most frequent word overall across all temporal groupings
- Highest frequency in December (143.1 per 1K), followed by Short Rains/secondary planting season (102.1 per 1K)

**Other Notable Findings**
- "cow" and "dairy" share synchronized frequency increases, peaking during December/Short Rains season, suggesting farmers prepare to sell or produce dairy products during this period
- "tomatoes" exhibits singular upward spike during August (96.1 per 1K), indicating harvest activity at end of Harvest 1 period (Jun-Aug)

<img width="3796" height="5472" alt="image" src="https://github.com/user-attachments/assets/b73e00c5-3845-4e7c-952e-a31ba48c04b0" />
