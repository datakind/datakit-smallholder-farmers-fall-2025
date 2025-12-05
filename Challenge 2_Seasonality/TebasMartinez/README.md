# Challenge 2 - Seasonality
<<<<<<< HEAD
## Running `Data Cleaning.ipynb`
To run the data cleaning code in the notebook, you'll need to add the Producers Direct dataset file originally provided in the [DataKit](https://docs.google.com/document/d/1jKTmb8R5GlM9uqQkB5fXd37o2bdX17JKB36mK-NqWFE/edit?usp=sharing) under `data/raw/pd_dataset.csv`.
=======
## Overview
Seasonality analysis of WeFarm dataset as suggested in Challenge 2 of the [Producers Direct DataKit Brief](https://docs.google.com/document/d/1jKTmb8R5GlM9uqQkB5fXd37o2bdX17JKB36mK-NqWFE/edit?tab=t.0).

## Data Source
### WeFarm Dataset
Dataset provided by Producers Direct through DataKind's [DataKit](https://docs.google.com/document/d/1jKTmb8R5GlM9uqQkB5fXd37o2bdX17JKB36mK-NqWFE/edit?tab=t.0) with 7 years questions & answers shared through the [WeFarm](https://join.wefarm.com/) SMS platform. Some characteristics of the initial dataset are:
- 20.304.843 rows, each of them representing a question-answer pair.
- 24 columns, including information about the question and answer (id, date, language, message text, topic) and the users (id, user type, status, country, gender, date of birth, account creation date).
- Four languages: English, Swahili, Luganda, and Nyn.
- Three countries: Kenya, Uganda, Tanzania.

## Methodology
### Data Cleaning
- Created a pandas dataframe including only data from questions in English, excluding answers.
- Cleaned null values and duplicates.
- Grouped topics in tuples. In the original dataset, the topic column includes only one topic, so when a question had more than one topic assigned, this question repeated in multiple rows with topic being the only value changing. I grouped all topics per question in tuples in a 'topics' columns.
- Generated question type column.
- Edited column names and reordered.
- Added farming season columns based on the descriptions provided in the [brief](https://docs.google.com/document/d/1jKTmb8R5GlM9uqQkB5fXd37o2bdX17JKB36mK-NqWFE/edit?tab=t.0).
- Filtered countries. Since Tanzania had only 2 questions after cleaning, it was filtered out.
- Exported dataframes to .csv

After the cleaning process, the characteristics of the dataframe are:
- 2.218.481 rows, each representing a question in English.
- 9 columns (question_id, user_id, country, topics, question_type, text, clean_text, date, season).
- Coutries: Kenya and Uganda.

### Univariate Exploratory Data Analysis
- Understanding distributions in the clean dataframe:
   - Questions per country.
   - Questions per season.
   - Most asked topics.
   - Questions per question type.

### Bivariate Exploratory Data Analysis
- Question types per season.
- Question types over time.

## AI use disclaimer
Deepseek was used to generate the dictionary with question types (categories) in `Data Cleaning.ipynb`

## Distributions
[![Questions per country](images/questions_per_country.jpg)]()

[![Questions per season in Kenya](images/questions_per_season_kenya.jpg)]()
[![Questions per season in Uganda](images/questions_per_season_uganda.jpg)]()

[![Question type distribution](images/question_type_distribution.jpg)]()

## Key Insights
[![Question types per season in Kenya](images/types_per_season_kenya.jpg)]()
[![Question types per season in Uganda](images/types_per_season_uganda.jpg)]()

[![Question types over time](images/types_over_time.jpg)]()
[![Question types over time in Kenya](images/types_over_time_kenya.jpg)]()
[![Question types over time in Uganda](images/types_over_time_uganda.jpg)]()

## Running this directory
To run the code in the `Data Cleaning.ipynb` notebook, the Producers Direct dataset file originally provided in the [DataKit](https://docs.google.com/document/d/1jKTmb8R5GlM9uqQkB5fXd37o2bdX17JKB36mK-NqWFE/edit?usp=sharing) must be added under `data/raw/pd_dataset.csv`. All remaining data files needed for the next steps are generated through that notebook.
>>>>>>> c6d1eaefaf26b1ce26f014545fc8090ed0bfd1a4
