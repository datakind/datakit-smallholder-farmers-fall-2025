## Yu-hui Lien
## Submission - 1

```
## Challenge-4-crop-questions-traditional method.ipynb

## 1. Executive Summary

This project utilizes a **Prioritized Lexical Classification** approach to categorize 11.5M rows of **English** farmer questions into predefined business concepts (e.g., Pest & Disease, Market & Finance).

**The classification relies on finding keywords in the question text based on a hierarchical priority structure, ensuring consistency with predefined business rules.**

**Key Findings:**

* The Lexical approach provides rapid, interpretable topic assignments based on explicit keyword rules.

* This method requires meticulous maintenance of the keyword dictionary to remain effective against non-standard text.

* Preliminary results show a clear imbalance, with 66% being Specific Questions and roughly 34% being General Questions.


## 2. Data

| Feature | Description | Status |
| :--- | :--- | :--- |
| **Source Data** | `parquet` file in the Kaggle context) | Loaded |
| **Target Column** | `question_content_cleaned` | Used for matching |
| **Data Size** | Approx. 11.5M rows | Processed |
| **Time Span** | Long-term data analyzed | Categorized |

## 3. Methodology: Prioritized Lexical Classification

The classification relies on a hierarchical, rule-based approach to ensure high-priority topics (like immediate risks) are classified first, minimizing ambiguity.

### A. Data Preprocessing

* **Action:** Basic cleaning steps (lowercasing, punctuation removal) were performed on the raw text.

* **Goal:** Maximize keyword matching effectiveness.

### B. Prioritized Keyword Matching

Questions were classified based on a strict priority order. The question is assigned to the **first** category whose keyword is matched.

**Keyword Categories and Priority Order:**

1. **IMMEDIATE ACTION/RISK** (e.g., Pest & Disease, Market & Finance)

2. **FOUNDATIONAL MANAGEMENT** (e.g., Soil & Water Management)

3. **FARMING TECHNIQUE** (General Actions)

4. **CONCEPTUAL** (Definitions/Explanations)

5. **ADMINISTRATIVE/VAGUE** (Junk/Unclassified)

### C. Tuning for Robustness

* **Keyword Maintenance:** Regular review and expansion of the keyword dictionary is necessary to maintain high accuracy across non-standard text.

* **Fallback:** Questions not matching any defined keyword are assigned to the 'Unclassified' category.

## 4. Results and Visualization

![Overall Topic Proportion](https://raw.githubusercontent.com/yhlien1221/datakit-smallholder-farmers-fall-2025/main/Challenge%204_%20Crop%20Questions/Yuhui_Lien/pictures/topic_proportion_overall.png)

![Topic proportion trend](https://github.com/yhlien1221/datakit-smallholder-farmers-fall-2025/blob/main/Challenge%204_%20Crop%20Questions/Yuhui_Lien/pictures/topic_proportion_trend.png)

![Distribution of general question into subtopics](https://github.com/yhlien1221/datakit-smallholder-farmers-fall-2025/blob/main/Challenge%204_%20Crop%20Questions/Yuhui_Lien/pictures/general_topic_breakdown_final_corrected.png)


### A. Topic Distribution (Overall)

* Preliminary results show a clear imbalance, with 66% being Specific Questions and roughly 34% being General Questions.

### B. Topic Distribution by Time (Monthly)

The line chart shows that while Specific Questions generally dominate, I observed a distinct convergence between August 2021 and September 2021.

### C. Distribution of general question into subtopics

This bar chart reveals that the majority of inquiries fall into just two areas: Unclassified/Other/Vague (34.8%) and Farming Technique (28.7%). The remaining topics, such as "Concept & Definition" (15.5%) and "Soil & Water Management" (6.9%), constitute smaller proportions of the total general questions

## 5. Conclusion and Next Steps

The traditional Lexical Classification method provides a fast and robust initial categorization layer. Its high interpretability makes it ideal for immediate business reporting and dashboard visualization; **however, maintaining and updating the comprehensive list of keywords and phrases necessary for this method can be challenging.**

**The final output contains the following essential columns:**

* `question_content_cleaned`

* `broad_topic` (The final Lexical Category)

**Next Steps:**

1. **Enhance Subtopic Classification with BERTopic**: Apply the Transformer-based BERTopic model to refine the classification of general questions into subtopics, focusing particularly on improving the accuracy and coverage of questions currently labeled as 'Unclassified' by the lexical method.



# Submission - 2

# Project: Guided Topic Modeling for Smallholder Farmer Questions (Challenge 4)
 
## 1. Executive Summary
 
This project aims to categorize and analyze **100,000+ farmer questions** using **Guided BERTopic** (Bidirectional Encoder Representations from Transformers for Topic Modeling) to understand key areas of concern (e.g., pests, market, technique).
 
Initial attempts with standard clustering were unstable due to the large volume of data and non-standard English phrases. By implementing a **deep cleaning pipeline** and **Guided Clustering**, we achieved stable, coherent topics categorized by predefined business concepts (e.g., Market & Finance, Livestock, Farming Technique).
 
**Key Findings:**
 
* The high volume of data necessitates stringent noise filtering (`min_topic_size=1000`).
 
* The use of **Seed Topics** successfully directed the model to separate ambiguous concepts like 'Poultry' from general 'Planting Technique'.
 
* Visualizations confirmed stable topic distribution across the three-day data collection period.
 
## 2. Data
 
| Feature | Description | Status |
| :--- | :--- | :--- |
| **Source Data** | `general_question_list (1).csv` (or `.parquet` file in the Kaggle context) | Loaded |
| **Target Column** | `question_content_cleaned` | Used for modeling |
| **Data Size** | Approx. 100,000+ rows (Scaled up from 1,000 for final run) | Processed |
| **Time Span** | Extremely short (e.g., 3 days: 2017-11-22 to 2017-11-24) | Analyzed |
 
## 3. Methodology: Guided BERTopic and Optimization
 
The primary challenge was the instability of clustering at high volumes due to non-standard English. We implemented the following solutions:
 
### A. Deep Preprocessing
 
To solve the misclassification of words like `poutry` (classified as `cabbages`), a custom deep cleaning function was applied **before** embedding generation:
 
* **Action:** Created a `replacement_map` to normalize common misspellings (`poutry` -> `poultry`, `j` -> `i`, `hw` -> `how`).
 
* **Vectorizer:** Used `CountVectorizer` with a custom English stopword list to preserve key instructional words like "how" and "do", which are essential for identifying 'Technique' topics. (`min_df=0.001` was applied to filter low-frequency noise).
 
### B. Guided Clustering (Semi-Supervised)
 
We enforced business logic into the model by using a `seed_topic_list`, preventing the model from randomly grouping critical concepts.
 
**Key Seed Categories:**
 
1. **Market & Finance:** `['market', 'price', 'cost', ...]`
 
2. **Pest & Disease:** `['pest', 'disease', 'spray', ...]`
 
3. **Livestock:** `['pigs', 'cow', 'poultry', ...]` (Crucial for separating animals from plants)
 
4. **Farming Technique:** `['plant', 'grow', 'method', 'way', ...]`
 
### C. Hyperparameter Tuning for Volume
 
To ensure coherent clustering across 100,000 documents, the following parameters were significantly tightened:
 
| Parameter | Function | Value | Rationale |
| :--- | :--- | :--- | :--- |
| **`min_topic_size`** | HDBSCAN Clustering | 1000 | Drastically increased to eliminate small, fragmented, or noisy topics common in large datasets. |
| **`n_neighbors` (UMAP)** | UMAP Dimensionality Reduction | 75 | Increased to create a smoother, more continuous embedding space, improving clustering stability. |
| **`n_components` (UMAP)** | UMAP Dimensionality Reduction | 5 | Reduced the embedding space complexity for better HDBSCAN performance. |
 
## 4. Results and Visualization
 
The final model yielded stable and meaningful topics.
 
### A. Topic Distribution (Overall)
 
This visualization shows the volume of questions for each topic, using the full `BERTopic_Label`.
 
### B. Topic Distribution by Time (Daily/Seasonal)
 
Due to the extremely short time span of the test data (3 days), the 'seasonal' analysis was performed on a **daily basis**.
 
* **Observation:** Analysis of the $2017-11-22$ to $2017-11-24$ period shows shifts in farmer focus over time (e.g., initial peak of general questions followed by specialization in specific crop techniques).
 
## 5. Conclusion and Next Steps
 
The Guided BERTopic pipeline successfully solved the challenge of unstable clustering and misclassification caused by non-standard text in a high-volume setting.
 
**The final output contains the following essential columns for further analysis:**
 
* `BERTopic_Topic_ID`
 
* `BERTopic_Label` (Full Topic Name)
 
* `Topic_Key_Label` (Simplified 1-2 word tag)
 
**Next Steps:**
 
1. **Full Dataset Run:** Execute the finalized code on the full 3 million rows (expected runtime: 6-10 hours on GPU).
 
2. **Topic Hierarchy:** Utilize `topic_model.visualize_hierarchy()` to group the 14-20 discovered themes into the 7 primary business concepts (Market, Pest, Technique, Livestock). 