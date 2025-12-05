# KEMBAI - Smallholder Farmer Data Analysis

## Overview
This analysis explores a large dataset of questions from smallholder farmers to identify key trends, topics, and languages. The goal is to extract actionable insights that can help Producers Direct better understand and serve the needs of these farmers. The analysis covers data exploration, cleaning, keyword extraction, and visualization, with a focus on financial inclusion and crop-related questions.

## Research Questions
- What are the most common languages used by the farmers?
- Who are the most active users in the dataset?
- What are the most frequently discussed topics, particularly concerning crops and finance?
- How can we segment the data to analyze specific areas of interest like financial inclusion or crop issues?

## Methodology

### Data Sources
- The primary dataset contains 21,541,705 rows of farmer questions and related metadata, loaded from `b0cd514b-b9cc-4972-a0c2-c91726e6d825.csv`.
- All the output and extracted data from the current code will be [in this link](https://drive.google.com/drive/folders/1Jm2esR6ONe6x3UT_4heDsm6-18sXgXUl?usp=sharing)

### Approach
1.  **Data Loading and Optimization**: The original CSV was loaded using PySpark in a Google Colab environment. To improve performance, the dataset was immediately converted to the more efficient Parquet format.
2.  **Data Cleaning and Preprocessing**: Over 630,000 fully duplicate rows were removed, resulting in a cleaned dataset of approximately 20.9 million rows.
3.  **Language-based Partitioning**: The cleaned data was partitioned into separate files based on the `question_language` column, creating distinct datasets for English (`eng`), Swahili (`swa`), Nyankole (`nyn`), and Luganda (`lug`).
4.  **Text Normalization and NLP**: For the English and Luganda datasets, a text processing pipeline was applied, which included:
    *   Converting text to lowercase.
    *   Removing punctuation and special characters.
    *   **Tokenization**: Splitting text into individual words.
    *   **Stop Word Removal**: Filtering out common, low-value words using a custom-defined list.
5.  **Keyword Analysis**: A specific list of financial keywords (e.g., 'loan', 'price', 'income') was used to identify and tag relevant conversations within the English dataset.
6.  **Visualization**: Generated a line chart using Plotly and Matplotlib showing the monthly trends of financial keyword mentions to understand the seasonality of these topics.

### Tools and Technologies
-   **Programming Language**: Python
-   **Key Libraries**:
    -   `PySpark`: For large-scale, distributed data manipulation and analysis.
    -   `Pandas` & `Dask`: For initial data exploration and handling.
    -   `Matplotlib` & `Seaborn`: For static data visualizations.
    -   `Plotly`: For creating interactive time-series charts.
-   **GenAI Tools Used**:
    -   **ChatGPT**: Assisted in writing and debugging PySpark code for keyword counting and library usage.
    -   **Gemini CLI**: Used for initial local data exploration, extracting keyword lists, and consolidating project documentation.
-   **Other Tools**: Google Colab (for its free RAM, GPU, and processing power), Google Drive (for data storage).

## Use of Generative AI

### Tools Used
-   **ChatGPT**: Used for generating Python code to perform keyword extraction and counting.
-   **Gemini CLI**: Used to explore the data within the local environment, perform initial keyword extraction, and consolidate all the work steps from different sources into a single documentation file.

### Human Review Process
-   All AI-generated code was reviewed, tested, and modified by a human to meet specific project requirements.
-   AI-generated summaries and insights were validated against the data to ensure accuracy.

### AI-Assisted vs. Human-Created
-   **AI-Assisted**: Learning new libraries, generating boilerplate/redundant code, writing and structuring documentation.
-   **Human-Created**: Project planning, high-level innovation, code review and testing, final project structure, and prompt engineering.

## Key Findings

### Finding 1: Language and Data Overview
The dataset is multilingual, with English (55.6%) and Swahili (30.09%) being the dominant languages. A significant number of questions (3.77%) were unanswered, and 2.94% of the rows were duplicates, which were removed during preprocessing.

**Implications for Producers Direct:**
-   Engagement strategies should be tailored to at least English and Swahili speakers.
-   The presence of other languages like Nyankole (5.37%) and Luganda (3.2%) indicates a need for multilingual support.

### Finding 2: Top Topics of Interest
The most common topics discussed by farmers include plant, maize, beans, and soil. This highlights the primary areas of focus for their agricultural activities.

**Implications for Producers Direct:**
-   Resources and support can be prioritized around these key topics to meet the most immediate needs of the farmers.

### Finding 3: Seasonality of Financial Topics
The analysis of financial keywords in the English dataset revealed trends in when farmers discuss financial matters. Visualizations show peaks and troughs in conversations about terms like "price," "loan," and "income" throughout the year.

**Implications for Producers Direct:**
-   These dashboards can be used to time the launch of targeted financial literacy programs or advisory services to coincide with periods of high interest.

## Visualizations

### Financial Keyword Trends by Month
Note: A line chart was generated using Plotly showing the count of financial keywords per month for all years.

**Interpretation**: This visualization tracks the volume of financial-related questions throughout the year. For example, a peak in questions about "price" before a harvest season could inform when to provide market price information.

## Limitations and Challenges

### Data Limitations
-   The keyword analysis was primarily focused on English-language data due to the challenges of translation.
-   A small percentage of data (2.2%) had a NULL language field.

### Methodological Limitations
-   The keyword extraction was based on a predefined list of English words, which may not capture the full context or nuances of questions in other languages.
-   No forecasting or predictive modeling was performed.

### Technical Challenges
-   The large size of the dataset required the use of PySpark and Google Colab to manage memory and processing effectively.
-   Some Spark jobs failed or were interrupted, indicating the computational intensity of the tasks.

## Next Steps and Recommendations

### For Further Analysis
1.  **Translate All Data**: Use open-source models to translate all non-English questions to create a complete, unified dataset for a more holistic analysis.
2.  **Develop Forecasting Models**: Create forecasting models to predict trends in farmer questions or agricultural issues.
3.  **Build an Interactive Dashboard**: Develop a comprehensive, interactive dashboard that allows for dynamic exploration of the entire dataset.

### For Producers Direct
1.  **Invest in Translation**: Support the translation of farmer questions to gain a more inclusive understanding of all farmer needs.
2.  **Develop Targeted Content**: Use the insights on top topics and their seasonality to create relevant and timely content, resources, and advisory services.
3.  **Enhance Multilingual Support**: Expand support services to cover the primary languages identified in the analysis.

## Files in This Contribution



## How to Run This Analysis

### Prerequisites
- A Google Account for Google Colab and Google Drive.
- Required Python libraries (run `!pip install pyspark plotly` in a notebook):
  - `pyspark`
  - `plotly`
  - `pandas`
  - `matplotlib`
  - `seaborn`

### Running the Analysis
The analysis is contained within the two Jupyter Notebooks in the `Codes/` directory. They are designed to be run in a Google Colab environment.
1.  Upload the dataset to your Google Drive.
2.  Open the notebooks in Google Colab.
3.  Update the file paths in the notebooks to point to the location of your data in Google Drive.
4.  Run the cells sequentially.

## Contact and Collaboration

**Author**: Amr Abd-Alkrim, Bashir Alsuty, and Emad Abubakar
**GitHub**: 3mrdev, bashiralsuty, EMAD77
**Slack**: Amr Abd-Alkrim, Bashir Alsuty, emad

---

**Last Updated**: 2025-12-05
**Status**: Complete