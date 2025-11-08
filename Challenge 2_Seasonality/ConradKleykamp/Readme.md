# Conrad Kleykamp

Folder containing my work for Challenge #2.

---

## Submission #1: Initial EDA (Country, Language, Time)

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

