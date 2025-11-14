# Ruben Vermaak - Producers Direct Climate Sensitivity Analysis

## Overview

This analysis investigates the relationship between smallholder farmer questions received by Producers Direct and localized climate variables (maximum temperature, precipitation, and humidity) in **Kenya (KEN), Uganda (UGA), and Tanzania (TZA)**. The primary goal is to move beyond general seasonal trends to identify **specific crops and regions most sensitive to climate stress**, thereby providing an evidence base for targeted, preventative farmer support and content development.

## Research Questions

* **Question 1:** Which country-specific agricultural topics show the highest statistical correlation with extreme weather conditions (heat, drought, high humidity)?
* **Question 2:** What patterns exist in question volume across the agricultural calendar that link to specific climate crises?
* **Question 3:** What targeted, actionable strategies can Producers Direct implement to proactively address climate-driven farmer needs?

---

## Methodology

### Data Sources
* **Producers Direct Questions Dataset:** Source of farmer questions, date sent, topic, and country code.
* **Weather Data (GCM/ERA5-derived):** Monthly averages for $tasmax$ (maximum temperature), $pr$ (precipitation), and $hurs$ (relative humidity).
* **External Data:** General farming season guides for East Africa (used for post-analysis validation).

### Documenting Local Preprocessing & Optimization

* **File Conversion:** The raw producer data (questions) and the cleaned weather data were both imported and converted locally to the **Apache Parquet format**. This was essential for reducing file size and optimizing performance.
* **Data Transformation:** The raw weather data was transformed locally from its original long format into a usable, standardized monthly structure (`YYYY-MM`) before being merged and uploaded.

### Approach
* **Data Loading & Cleaning:** Data was loaded from **BigQuery** (where final cleaning steps like country code standardization and topic normalization were executed via SQL) and merged on `country_code` and `YYYY-MM`.
* **Analysis Techniques:** **Pearson Correlation Coefficients (R-values)** were calculated by country to quantify relationships. Topics were then ranked by their exposure to the most sensitive climate driver.
* **Validation:** Seasonal plots were generated to align question peaks with critical farming periods (planting, harvest) to verify climate-driven causality.

### Tools and Technologies
* **Programming Language:** Python 3.x
* **Key Libraries:** `pandas`, `matplotlib`, `seaborn`, `google-cloud-bigquery`.
* **Other Tools:** Google Colab Notebook.

### Use of Generative AI
* **Tools Used:** Gemini (Google's AI model).
* **Human Review Process:** All AI-generated code was reviewed, tested, and validated against statistical proof and external agricultural knowledge.
* **AI-Assisted:** Initial code structure for data loading/merging, optimizing visualization functions, iterative debugging, and drafting the report summaries.
* **Human-Created:** All analysis logic, interpretation of visualizations, validation, and final strategic conclusions.

---

## Key Findings & Strategic Implications

### Finding 1: Climate Sensitivity is Localized and Drives Opposite Crises

| Country | Primary Climate Driver | R-value | Strategic Focus |
| :--- | :--- | :--- | :--- |
| **TZA (Tanzania)** | **Heat Stress ($tasmax$)** | $+0.1096$ | Heat Mitigation for Staples and Forage. |
| **KEN (Kenya)** | **Humidity Stress ($hurs$)** | $+0.0503$ | Disease Prevention for High-Value Horticulture. |
| **UGA (Uganda)** | **Extreme Moisture ($hurs$/$pr$)** | $+0.0621$ | Waterlogging/Root Disease Solutions. |

**Implication:** Content must be **hyper-localized** based on the dominant stressor. A general drought alert is insufficient; TZA needs heat/drought solutions, while KEN/UGA need fungal disease prevention.

### Finding 2: Two Distinct Crisis Peaks Define the Farmer Support Calendar

The seasonal question volume validates two major crisis periods that require separate intervention strategies:

* **Planting Season Crisis (March–May Peak):** Driven by high moisture, leading to disease and water management questions (KEN/UGA).
* **Harvest/Dry Season Crisis (August & November Peaks):** Driven by secondary planting and post-harvest issues.
    * **August Peak:** Primarily driven by post-harvest storage pests and the onset of the dry season (feed scarcity).
    * **November Peak:** Driven by the Short Rains secondary planting season, leading to another, smaller peak of moisture-related questions.

**Implication:** A **dual content calendar** is necessary: one for the primary Planting Crisis and one for the Harvest/Storage and Secondary Planting phases (Aug/Nov).

---

## Visualizations

### Question Volume by Month: Seasonal Validation

*Interpretation:* This visualization aligns question volume spikes with the East African agricultural calendar, confirming that farmers seek help during all critical, high-risk periods (planting, harvest, and secondary planting).
![view](Challenge 1 _Weather Patterns/Ruben Vermaak/Question Volum vs. Average Temperature by topic.png)

### Question Volume vs. Avg. Max Temperature ($tasmax$)
*Interpretation:* Shows how questions about key topics like **Maize, Cattle, and Cereal** cluster in the months with the highest average temperatures, confirming their universal vulnerability to heat stress across all countries.


---

## Next Steps and Recommendations

### For Producers Direct (Actionable Strategy)
1.  **Targeted Alert System:** Immediately implement a country-specific alert strategy: **Heat Alerts for TZA; Fungal Disease Alerts for KEN/UGA.**
2.  **Content Prioritization:** Prioritize content development for **Maize** (the universal crisis crop) and **Leafy Greens/Horticulture** (the key humidity victims).
3.  **August & November Campaigns:** Launch targeted digital campaigns during the **July–August** period (post-harvest storage) and the **October–November** period (secondary planting advice).

### For Further Analysis (Future Work)
1.  **Acquire Granular Data:** Integrate **daily weather data**, especially Soil Moisture and Evapotranspiration, for a more accurate predictor of short-term stress.
2.  **Predictive Modeling:** Build a time-series model to forecast peak question volume for the most sensitive topics.

---

## Files in This Contribution

* Challenge 1 - Identifying patterns in weather and agriculture_ruben_vermaak
* README.

## Contact and Collaboration

* **Author:** Ruben Vermaak
* **GitHub:** @Rpvermaak
* **Collaboration Welcome:** Open to feedback and suggestions.
* **Last Updated:** 14 Nov 2025
**Status:** Complete
