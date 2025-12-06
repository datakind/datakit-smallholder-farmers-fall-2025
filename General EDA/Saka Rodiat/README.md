Exploratory Data Analysis of the Producers Direct Smallholder Farmers Dataset

Author: Saka Rodiat Opeyemi

Introduction

This project presents an exploratory data analysis (EDA) of the Producers Direct dataset, which contains questions and responses submitted by smallholder farmers across East Africa. The primary objective of this analysis is to identify patterns in farmer inquiries, understand their information needs, examine linguistic and geographic distributions, and derive insights that may support improved decision-making and knowledge dissemination for farmer communities.

Research Objectives

The analysis focuses on the following research questions:

What are the top ten most common question topics among farmers?

Which languages are predominantly used when asking questions?

From which countries do the users asking questions originate?

Are there observable patterns in user activity and response status?

What insights can be derived to inform support strategies for smallholder farmers?

Data and Methods
Data Source

The analysis is based on the farm_data.csv dataset obtained from Producers Direct. Given the size of the dataset (~20 million records), the CSV file was converted into Parquet format to enable efficient querying and processing.

Tools and Technologies

Programming Language: Python 3.x

Libraries: pandas, numpy, matplotlib, seaborn, duckdb

Environment: Jupyter Notebook

DuckDB was employed for efficient querying due to its strong performance with large datasets.

Analytical Approach

The analysis followed these steps:

Data loading and inspection

Cleaning and preprocessing

Visual exploration of key variables

Interpretation of patterns and insights

Use of Generative AI

Generative AI (ChatGPT) was used to support the analysis process by:

Decoding errors and explaining their causes

Suggesting the correct code syntax

Providing coding guidance and workflow suggestions

Human Oversight

All analyses, visual outputs, interpretations, and conclusions were produced and validated manually.

## Files in this submission

wefarm_data_eda.ipynb** – Jupyter Notebook containing the EDA analysis.
-Wefarm_data_sample.csv** – Sample dataset used in the notebook.
README.md** – This file describing the submission.

## How to run the notebook

1. Make sure you have pandas installed: pip install pandas.
2. Open wefarm_data_eda.ipynb in Jupyter Notebook or Jupyter Lab.
3. The notebook loads the sample CSV ('Wefarm_data_sample.csv') automatically and performs exploratory data analysis.

Results and Findings
Question Topics

The most frequently asked question topics were maize, followed by cattle and chicken. The least common topics within the top ten were goat and pig.

Languages Used for Questions

English was the most widely used language, followed by Swahili, Nyanja, and Luganda, reflecting linguistic diversity within the farmer community.

Geographic Distribution of Users

Most users originated from Kenya, with significant representation from Uganda and Tanzania, which aligns with the regions where Producers Direct operates.

Response User Status

The majority of responses were categorized as live, followed by statuses such as zombie, destroyed, and blocked, indicating varying levels of user activity and engagement.

Visualizations

The notebook includes visualizations such as:

Bar charts of question languages

Distribution of user country codes

Response user status distribution

Top 10 most common question topics

These visualizations support the identification of key trends within the dataset.

Limitations

The large dataset required optimization steps such as Parquet conversion.


Conclusion

This exploratory analysis provides insight into the communication patterns, information needs, and engagement behaviors of smallholder farmers across East Africa. Understanding these patterns can help organizations refine their support strategies and develop more targeted interventions.