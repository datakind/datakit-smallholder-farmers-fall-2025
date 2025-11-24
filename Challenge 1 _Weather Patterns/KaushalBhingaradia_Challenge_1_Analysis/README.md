# Challenge 1 – Weather & Agriculture Patterns

## Goal

Understand how weather patterns affect the types of questions farmers ask on the Producers Direct platform.

---

## Data Used

* Producers Direct questions dataset (had to use a smaller portion on some parts like LDA as it was too large for my system)
* Seasonal mapping based on East African weather patterns

  * **Hot Dry**: Jan–Feb
  * **Long Rains**: Mar–May
  * **Dry**: Jun–Sep
  * **Short Rains**: Oct–Dec

---

## Key Insights

### 1. Question Categories

* Most questions fall into the **Other** category (72%).
* **Planting** is the most common defined category.
* **Weather_damage** is the least common (only 0.1%).

### 2. Seasonal Patterns

* Most questions are asked during the **Dry Season** and **Short Rains**.
* The **Hot Dry season** has the fewest questions overall.
* Regardless of season, **“Other” remains the dominant category**.

### 3. Monthly Trends

* **Highest activity months**: November and August
* **Lowest activity month**: February
* Question activity peaked in **2019**, then dropped and has mostly flatlined since 2022.

### 4. Weekly Patterns

* Most questions are asked on **Thursdays**.
* The fewest questions are asked on **Sundays**.

### 5. Geographic Trends

* Most questions come from **Kenya**.
* The fewest questions come from **GB (Great Britain)**.

### 6. Language Distribution

* Most common language: **English**
* Least common language: **Luganda (Lug)**

### 7. Topic & Keyword Insights

From topic modeling, the highest-weighted words include:

* **poultry**
* **banana**
* **plant**
* **jibu**
* **kuku**

This suggests heavy engagement with poultry farming and crop-related questions.

---

## Summary of Weather & Question Patterns

* Dry season accounts for the largest share of questions (**33.9%**).
* Hot dry season has the lowest share (**11.2%**).
* November is the most active month (2,355,975 questions).
* February is the least active month (1,099,469 questions).

Category breakdown:

* Other: 72.0%
* Planting: 12.5%
* Harvesting: 4.4%
* Drought: 3.3%
* Disease: 3.3%
* Pest: 2.5%
* Soil: 1.8%
* Weather Damage: 0.1%

---

## What I Learned

* Farmer questions **do show strong seasonal and temporal patterns**.
* Even with weather changes, many questions are broad and fall into the **Other** category.
* Seasonal shifts affect *when* farmers ask, but not strongly *what category dominates*.
* Activity trends suggest platform engagement peaked earlier (2019) and has stabilized at a lower level since.

---

## Recommended Actions

1. **Content Planning by Season**
   Create and highlight content before high-activity seasons like Short Rains and Dry Season.

2. **Improve Category Classification**
   Since most questions are labeled “Other”, refining the classification model could unlock more useful insights.

3. **Target High-Activity Periods**
   Increase engagement efforts around **August** and **November** when farmers are most active.

4. **Regional Focus**
   Since Kenya dominates, consider tailored features or content for Kenyan farmers while also growing outreach in underrepresented regions.

5. **Language Expansion**
   Support more local languages beyond English to increase access for non-English speakers.

---

## 🤖 Use of Generative AI

This project used **Claude 4.5 Sonnet** and **ChatGPT 5.1** to speed up my workflow. They helped me:

* Organize and clean up analysis code faster
* Improve and simplify visualizations
* Help quickly summarize findings into clear insights and recommendations based on my analysis, observations, and my understandings.
* Draft and refine this README quickly

All results and interpretations were reviewed and finalized by me.

---

## 🗂️ Files in This Submission

* **`challenge_1_weather.ipynb`**: Complete Jupyter Notebook with analysis code, visualizations, and inline insights
* **`README.md`**: This comprehensive documentation of methodology and findings

---

**Author: Kaushal Bhingaradia**
**Date:** November 23, 2025
