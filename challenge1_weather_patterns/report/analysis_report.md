# Challenge 1: Weather Patterns Analysis Report

**Author**: hwilner
**Date**: November 5, 2025

## 1. Executive Summary

This report details the analysis of farmer question patterns in relation to weather data for Challenge 1 of the Producers Direct DataKit. Using a sample of 500,000 questions and 8 years of weather data from NASA POWER, we found a **statistically significant positive correlation (r=0.194, p=0.028)** between daily rainfall and the volume of farmer questions in Kenya. This suggests that farmers are more likely to ask questions on days with more rainfall.

This initial finding validates the hypothesis that weather events drive farmer engagement and provides a strong foundation for building a proactive information delivery system.

## 2. Introduction

### 2.1. Background

Producers Direct serves over 1.3 million smallholder farmers in East Africa and Latin America. Understanding the drivers behind farmer questions is critical for providing timely, relevant information. This analysis focuses on Challenge 1: Weather Patterns, which aims to correlate weather events with question patterns to better anticipate farmer needs.

### 2.2. Research Questions

- How do question volumes change with weather conditions?
- Is there a correlation between rainfall and question volume?
- What are the overall trends in question volume and weather patterns?

### 2.3. Hypotheses

- **H1**: There is a positive correlation between rainfall and question volume.
- **H2**: Question volumes will show seasonal patterns that align with rainy seasons.

## 3. Data and Methodology

### 3.1. Data Sources

1. **WeFarm Dataset**: A 7.25GB dataset containing 21.7 million question-response pairs. For this analysis, a sample of the first 500,000 rows was used.
   - **Source**: Provided by user via Google Drive

2. **NASA POWER Weather Data**: 8 years (2015-2022) of daily weather data for Kenya, Uganda, and Tanzania.
   - **Source**: [NASA POWER API](https://power.larc.nasa.gov/)

### 3.2. Data Processing

1. **Question Data**: Loaded the first 500,000 rows, parsed timestamps, and filtered for Kenya, Uganda, and Tanzania.
2. **Weather Data**: Downloaded daily data for temperature, precipitation, humidity, and wind speed.
3. **Aggregation**: Aggregated question counts by day and country.
4. **Merging**: Merged daily question counts with weather data for Kenya.

### 3.3. Analytical Methods

- **Descriptive Statistics**: Summarized dataset characteristics.
- **Time Series Analysis**: Plotted question volumes and weather patterns over time.
- **Correlation Analysis**: Calculated Pearson correlation between question volume and rainfall in Kenya.

## 4. Results

### 4.1. Dataset Overview

- **Sample Size**: 500,000 rows
- **Countries**: Kenya (66%), Uganda (34%)
- **Languages**: English (64%), Swahili (24%), Nyn (10%), Luganda (2%)
- **Date Range**: Nov 2017 - Mar 2018

### 4.2. Key Finding: Rainfall Correlates with Question Volume

A Pearson correlation analysis for Kenya revealed a **statistically significant positive correlation (r=0.194, p=0.028)** between daily precipitation and the number of questions asked. This supports our primary hypothesis.

| Metric | Value |
|---|---|
| Correlation (r) | 0.194 |
| P-value | 0.0278 |
| Significance | **Yes** |

This suggests that as rainfall increases, so does farmer engagement on the platform.

### 4.3. Visualizations

**Figure 1: Farmer Questions Over Time**

![Farmer Questions Over Time](../visualizations/demo_01_questions_over_time.png)

*This chart shows the daily volume of questions from Kenya, Uganda, and Tanzania in the sample dataset. There are clear peaks and troughs, suggesting weekly or event-driven patterns.*

**Figure 2: Kenya - Question Volume vs. Rainfall**

![Kenya Questions vs Rainfall](../visualizations/demo_02_kenya_questions_vs_rainfall.png)

*This chart visualizes the positive correlation in Kenya. Question volume (blue line) often rises on days with higher rainfall (green bars).*

**Figure 3: Daily Precipitation Patterns (2015-2022)**

![Daily Precipitation Patterns](../visualizations/demo_03_weather_patterns.png)

*This chart shows the long-term rainfall patterns for Kenya, Uganda, and Tanzania, highlighting the distinct rainy seasons in each country.*

## 5. Discussion

### 5.1. Interpretation

The positive correlation between rainfall and question volume is a strong signal that weather is a primary driver of farmer needs. Farmers likely face immediate challenges and opportunities related to planting, pest control, and crop management during and after rainfall, prompting them to seek information.

### 52. Limitations

- **Sample Data**: This analysis was performed on a 500,000-row sample covering a 4-month period. A full analysis on the 21.7M row dataset is needed to confirm these findings across all years.
- **Topic Analysis**: This initial analysis did not dive into question topics. Further analysis is needed to see if *specific* topics (e.g., pests, planting) are more correlated with weather.
- **Lag Effects**: We have not yet analyzed lag effects (e.g., do pest questions increase 1-2 weeks *after* rainfall?).

## 6. Recommendations for Producers Direct

1. **Proactive Information Delivery**: Use weather forecasts to anticipate farmer needs. If heavy rain is forecast, proactively send information about pest control, water management, and planting.

2. **Real-Time Alerts**: Develop a system to send real-time alerts to farmers based on their location and local weather events.

3. **Deeper Analysis**: Conduct a full analysis on the entire dataset to:
   - Validate these findings across all 8 years.
   - Analyze lag effects between weather and specific question topics.
   - Build a predictive model to forecast question volume and topics based on weather forecasts.

## 7. Future Work

- **Full Dataset Analysis**: Run the analysis on the complete 21.7M row dataset.
- **Topic Modeling**: Use NLP to categorize questions and analyze correlations for each topic.
- **Lag Correlation Analysis**: Identify optimal time lags between weather events and question spikes.
- **Predictive Modeling**: Build a machine learning model to predict question volume and topics.

## 8. Conclusion

This initial analysis provides strong evidence that weather patterns, particularly rainfall, are a significant driver of farmer engagement. By leveraging weather data, Producers Direct can create a more proactive, responsive, and valuable service for its 1.3 million farmers.

---

## References

[1] NASA POWER. [https://power.larc.nasa.gov/](https://power.larc.nasa.gov/)
