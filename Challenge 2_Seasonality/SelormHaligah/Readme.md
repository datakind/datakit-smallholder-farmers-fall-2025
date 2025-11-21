# Selorm Haligah- Seasonality Analysis

## Overview
This project details an analysis conducted in collaboration with DataKind and Producers Direct to understand smallholder farmers and the challenges they face in order to design, build  better tools,  information services and policies that directly improve productivity,  income and climate resilience. For the purpose of this task, the idea was to draw insights from seasonality patterns and its impact on agricultural practices. Specifically, the analysis focused on mapping the farming calendar based on question data, trends and year to year shifts in patterns.

## Research Questions
- Question 1: Can we map the farming calendar (planting, growing, harvesting) based on question data
- Question 2: Do seasonal patterns change over time
- Question 3: Is there an association between question data and farming season?
--------
## Methodology
 ### Data Collection
Data was provided by DataKind via Producers Direct. The data size was 7GB, comprising of information on Kenya, Tanzania, Uganda and gb, as well as different languages. However, for the purpose of this study only English data was considered for analysis
### Data Cleaning
Pandas was used to handle data manipulation, by breaking the data into manageable chunks. It was also discovered there were duplicates in the data. Nonetheless, these were not deleted from the dataset, based on these assumptions; 
1. Famers could have asked the same questions but could have been from different regions 
2. Similar questions could garner different responses and so deleting them would not give us a 
clear representation of the dataset. 
Date columns were also formatted for standardization purposes.
### Data Analysis
Focus was placed on unique question ID’s to understand the seasonal patterns in the dataset. NLP techniques of lemmatization and tokenization were induced with NLTK and combined with fuzzy matching using FuzzyWuzzy to account for word variation and typos in the “question content” column. This allowed for the matching of key question words to the general farming season of the respective regions. The final results were then merged to the full dataset on question ID’s.
### Statistical Testing
A chi-squared test of independence was also performed to validate whether indeed the questions farmers asked were associated with the current farming season they were in. Generative AI gave the idea to encode the data using a MultiLabelBinarizer to expand and flatten compound farming season questions.
###  Visualizations 
Power BI was used to visualize the results and present the insights clearly

### Tools and Technologies
- **Programming Language**: Python 3.
- **Key Libraries**: pandas, scikit-learn, NLTK, fuzzywuzzy, numpy
- **GenAI Tools Used**: ChatGPT
- **Other Tools**: Jupyter Notebook, Power BI

## Use of Generative AI

### Tools Used
- **ChatGPT**: gave the idea to encode the data using a MultiLabelBinarizer to expand and flatten compound farming season questions.

## Key Findings
### Finding 1: Trend Analysis
There was sharp jump in the number of questions being asked in 2019, followed by a sharp and further steady decline from then till 2022 and beyond. Generally, there has been a steady decline in the trend of questions being asked from year to year.  With the exception of general questions, there was a consensual sharp rise in the number of planting, growing and harvesting questions and a steady decline from then onwards. For general questions there has always been a decline in the number being asked.
**Implications for Producers Direct:**
- How this finding can be used
- What actions it suggests

###  Chi Squared Test of Independence
In testing for association between the questions being asked and the associated season being asked in, for Kenya, the p values for planting, growing, harvesting and general questions were all below the significant level of 0.05 therefore we rejected the null hypothesis that the independent variable (farmer question) is independent of the expected variable (general agricultural season). There is therefore an association between the questions being asked by farmers and the associated agricultural season
**Implications for Producers Direct:**
- How this finding can be used
- What actions it suggests

### Visualizations
#### Region of Focus -Kenya

There were a total of 7.12 million questions asked in the English dataset for Kenya out of which 1.64 million were unique. After matching, the seasons identified were planting, growing and harvesting, with some farmers asking different combinations of questions. Some questions were general and did not relate to the farming season. Such question revolved around animal farming or other agricultural issues. General questions were the most questions asked in the dataset with a total of 5.26 million questions. Planting questions were the second most asked questions in the dataset, representing 1.58 million and growing questions representing 218 thousand questions. Harvesting questions accounted for 13 thousand questions. The remaining questions were a combination of planting and growing, planting and harvesting, harvesting and growing or planting, harvesting and growing questions. Proportionately, General questions accounted for 73.9% of total questions asked, planting and growing accounted for 25.9% and harvesting 0.2%. Averagely, April recorded the highest questions, with general questions proportionately being the most with 71.9%, while October recorded the least questions being recorded with general questions also proportionately being the most with 73.3%.


-----
### Methodological Limitations
- Assumptions made
- Simplifications required
- Alternative approaches not explored
------
### Technical Challenges
- Computational constraints
------
## Next Steps and Recommendations

### For Further Analysis
1.  replicate on the different regions to enable region to region comparison of results.
------

## How to Run This Analysis

### Prerequisites
```bash
pip install pandas numpy scikit-learn, fuzzywuzzy, nltk
```

### Running the Analysis
```bash
Start Jupyter Notebook
Run
Run the Power BI dashboard
Save the data ke_analysis_for_vis
Run Kenya Data Analysis.pbix
```
------
### Dependencies
- pandas 2.3.1
- numpy <= 1.26.4
- NLTK < = 3.9.2

**Collaboration Welcome**: 
- Open to feedback and suggestions
- Happy to collaborate on related analyses
- Available to answer questions about this approach
