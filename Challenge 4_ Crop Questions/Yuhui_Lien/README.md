# Yu-hui Lien

## challenge-4-crop-questions-traditional method.ipynb

## 1. Executive Summary

This notebook involves text data cleaning and preprocessing applied to 11.5M rows of English farmer questions, and then utilizes a Prioritized Lexical Classification approach to categorize general questions into predefined business concepts (e.g., Pest & Disease, Market & Finance).

The classification relies on finding keywords in the question text based on a **hierarchical priority structure**, ensuring consistency with business rules.

### Key Findings:

- The lexical approach provides rapid and interpretable topic assignments based on explicit keyword rules.
- This method requires meticulous maintenance of the keyword dictionary to remain effective.
- Preliminary results show an imbalance, with **66% Specific Questions** and **34% General Questions**.

## 2. Data

| Feature | Description | Status |
|--------|-------------|--------|
| **Source Data** | `parquet` file (Kaggle) | Loaded |
| **Target Column** | `question_content_cleaned` | Used |
| **Data Size** | ~11.5M rows | Processed |
| **Time Span** | Long-term dataset | Categorized |

## 3. Methodology: Prioritized Lexical Classification

The approach ensures high-priority topics (like immediate risks) are detected first.

### A. Data Preprocessing

- Basic cleaning: lowercasing, punctuation removal  
- Goal: maximize keyword match accuracy

### B. Prioritized Keyword Matching

Questions assigned to the **first matched category** using the priority order below:

1. **Immediate Action / Risk**  
2. **Foundational Management**  
3. **Farming Technique**  
4. **Conceptual**  
5. **Administrative / Vague**

### C. Tuning for Robustness

- Keyword dictionary requires regular updates.
- Unmatched questions → labeled **Unclassified**.

## 4. Results and Visualization

![Overall Topic Proportion](https://raw.githubusercontent.com/yhlien1221/datakit-smallholder-farmers-fall-2025/main/Challenge%204_%20Crop%20Questions/Yuhui_Lien/pictures/topic_proportion_overall.png)

![Topic proportion trend](https://github.com/yhlien1221/datakit-smallholder-farmers-fall-2025/blob/main/Challenge%204_%20Crop%20Questions/Yuhui_Lien/pictures/topic_proportion_trend.png)

![Distribution of general question into subtopics](https://github.com/yhlien1221/datakit-smallholder-farmers-fall-2025/blob/main/Challenge%204_%20Crop%20Questions/Yuhui_Lien/pictures/general_topic_breakdown_final_corrected.png)

### A. Topic Distribution (Overall)

Specific Questions: 66%  
General Questions: 34%

### B. Topic Distribution by Time

Convergence between categories observed around Aug–Sep 2021.

### C. Subtopic Breakdown for General Questions

- Unclassified/Other/Vague: **34.8%**  
- Farming Technique: **28.7%**  
- Concept & Definition: **15.5%**  
- Soil & Water Management: **6.9%**

## 5. Conclusion and Next Steps

Lexical classification is fast, interpretable, and effective for initial categorization, but maintaining the keyword dictionary is challenging.

### Output Columns:

- `question_content_cleaned`
- `broad_topic`

### Next Steps:

1. **Enhance Subtopic Classification with BERTopic**  
2. Improve classification of Unclassified questions.

---

# challenge-4-crop-questions-transformer.ipynb

## 1. Executive Summary

This project categorizes **~100k rows of English farmer questions** using **Guided BERTopic**, addressing stability problems from standard clustering.

Key improvements include deep text cleaning and semi-supervised clustering using business-defined seed topics.

### Key Findings:

- High-volume data requires strong filtering (`min_topic_size=1000`).
- Seed topics successfully distinguish ambiguous concepts (e.g., poultry vs. planting).

## 2. Data

| Feature | Description | Status |
|--------|-------------|--------|
| **Source Data** | parquet | Loaded |
| **Target Column** | `question_content_cleaned` | Used |
| **Data Size** | 100k+ rows | Processed |

## 3. Methodology: Guided BERTopic and Optimization

### A. Deep Preprocessing

Custom cleaning solved issues like `poutry → poultry`.

- Replacements using `replacement_map`
- `CountVectorizer` with custom stopwords  
- `min_df=0.001` to remove noise

### B. Guided Clustering

Seed topics enforce business logic:

1. Market & Finance  
2. Pest & Disease  
3. Livestock  
4. Farming Technique  

### C. Hyperparameter Tuning

| Parameter | Purpose | Value | Reason |
|----------|---------|-------|--------|
| `min_topic_size` | HDBSCAN | 1000 | Prevent noisy micro-topics |
| `n_neighbors` | UMAP | 75 | More stable embedding |
| `n_components` | UMAP | 5 | Simplify structure |

## 4. Results and Visualization
![Subtopic Classification of General Questions using BERTopic](https://github.com/yhlien1221/datakit-smallholder-farmers-fall-2025/blob/main/Challenge%204_%20Crop%20Questions/Yuhui_Lien/pictures/bertopic_overall_distribution_full_label_final.png)

### A. Subtopic Classification of General Questions using BERTopic

This BERTopic distribution chart suggests that the current model parameters still require further optimization to achieve a balanced and coherent classification. The most notable issue is the dominant presence of generic and vague clusters, such as the 'what_where_you_how' topic at 17.3%, which indicates the model is failing to create highly specific or actionable groups. Furthermore, the top four topics account for over two-thirds of the data, with several categories being overly broad (e.g., 'animal_milk_animals_what' at 16.1%), preventing a clear, fine-grained understanding of the underlying farmer concerns. This imbalance signals the need for refining hyperparameters or utilizing a more restrictive set of seed topics.


### Key Output Columns:

- `BERTopic_Topic_ID`
- `BERTopic_Label`
- `Topic_Key_Label`

### Next Steps:

1. Run full dataset (3M rows)  
2. Visualize hierarchical structure 
Optimize Clustering Parameters: Refine BERTopic hyperparameters (e.g., min_topic_size, UMAP settings) to reduce the volume of vague or overly broad clusters and improve the specificity of subtopic assignments. 


<<<<<<< HEAD
## Challenge 4: Crop Question Analysis: Analyzing Farmer Demand, Community Supply, and Knowledge Gaps
=======
## Challenge 4: Crop Question Analysis: Analyzing Farmer Demand, Community Supply, and Knowledge Gaps (challenge-4-crop-questions-Analyzing-Farmer-Demand-Community-Supply-and- Knowledge-Gaps.ipynb)
>>>>>>> c6d1eaefaf26b1ce26f014545fc8090ed0bfd1a4

## 1. Executive Summary


### Key Findings: 📊

---

#### 1. Supply-Demand Mismatch and Critical Gaps (The Mismatch)

* **Critical Knowledge Gap (High-Volume/Low-Supply):** High-frequency, common farmer questions about **tomato** (Demand Volume Rank 6) and **crop** (Demand Volume Rank 7) are not represented in the "Supply Detail Top 10." This suggests that the detail and comprehensiveness of community knowledge supply are **significantly insufficient** relative to the high, recurring demand for these universal topics, potentially leading to repeated queries.
* **Balanced but High-Volume Response (Banana):** The topic **banana** shows high demand (Rank 9) but is also accompanied by relatively high Supply Detail (Rank 10). This indicates that while the questions are frequent, the community has strong, detailed knowledge-sharing members who are responding comprehensively.

---

#### 2. Demand Patterns (Farmer Questioning Behavior)

* **Dominant Demand (Repetitiveness):** **General Topic** (Rank 1), **cattle** (Rank 2), and **maize** (Rank 3) account for the largest volume of questions (Report A). This clearly identifies the most common and widespread agricultural and livestock challenges faced by the community.
* **Specialized Questioning Behavior (Specificity):** Farmers asking about niche crops like **peach** (Rank 1), **pear** (Rank 2), and $\text{setaria}$ (Rank 3) formulate the most complex and detailed questions (Report B). This behavior suggests that **askers must provide extensive context** to their peers in these niche areas, where established community knowledge may be sparse, to elicit a helpful response.

---

#### 3. Supply Patterns (Community Knowledge Flow)

* **High-Quality Knowledge Supply (High-Detail):** The longest and most detailed answers (high Supply Detail score) are concentrated on specialized topics such as $\text{rye}$ (Rank 1) and $\text{pigeon-pea}$ (Rank 2) (Report C). This demonstrates the existence of **passionate and highly experienced farmers** in these niche domains who are willing to share comprehensive, practical knowledge.
* **Non-Cattle Livestock Supply:** Topics related to non-cattle animals, specifically **bee** (Rank 4) and **poultry** (Rank 5), show strong Supply Detail, indicating a robust knowledge-sharing culture within these specific livestock sub-communities.


---

## 2. Data

| Column Used | Description | Purpose in Analysis |
| :--- | :--- | :--- |
| `question_topic` | Pre-existing classification of the question's subject (e.g., maize, poultry). | Primary grouping variable for all cross-analyses. |
| `question_content_cleaned` | Cleaned text of the farmer's question. | Used to derive **Demand Complexity** ($\text{Specificity Score}$). |
| `response_content_cleaned` | Answer provided by the community. | Used to derive **Supply Detail** ($\text{Response Score}$). |

---

## 3. Methodology

The core of the analysis is a **Supply-Demand Mismatch Model** built on three key quantifiable metrics:

### 3.1 Feature Engineering (Quantification)
To allow for direct comparison, we used **Min-Max Normalization** to scale all metrics to a uniform $[0, 1]$ range.

* **Demand Volume (Report A):** Raw count of questions per topic.
* **Demand Complexity Score (Report B):** Calculated by normalizing the raw **Question Length** (word count) for *each individual question*, then taking the average score per topic. (Higher score = more detailed demand).
* **Supply Detail Score (Report C):** Calculated by normalizing the raw **Answer Length** (word count) for *each individual response*, then taking the average score per topic. (Higher score = more detailed supply).


### 3.2 Cross-Topic Analysis
Metrics were aggregated using `df.groupby('question_topic').agg()`. The analysis focused on identifying patterns where **Demand Complexity $\ne$ Supply Detail**.

---

## 4. Results and Visualization

The following reports quantify the relationship between farmer necessity and platform content flow.

### Report A: Demand Volume (Question Repetitiveness)
![report_a_repetitiveness_seaborn](https://github.com/yhlien1221/datakit-smallholder-farmers-fall-2025/blob/main/Challenge%204_%20Crop%20Questions/Yuhui_Lien/pictures/report_a_repetitiveness_seaborn.png)
**Figure 1:** Total Demand Volume by Topic.

* **Takeaway:** The top 4 topics represent the highest consumption of system capacity.

### Report B: Demand Complexity Ranking
![report_b_demand_specificity_seaborn](https://github.com/yhlien1221/datakit-smallholder-farmers-fall-2025/blob/main/Challenge%204_%20Crop%20Questions/Yuhui_Lien/pictures/report_b_demand_specificity_seaborn.png)
**Figure 2:** Ranking of Topics by Average Farmer Question Complexity.

* **Takeaway:** Farmer effort is highest for niche crops ($\text{peach}, \text{pear}$), indicating these specialized subjects require maximum user input for proper context.

### Report C: Knowledge Supply Detail Ranking
![report_c_supply_detail_seaborn](https://github.com/yhlien1221/datakit-smallholder-farmers-fall-2025/blob/main/Challenge%204_%20Crop%20Questions/Yuhui_Lien/pictures/report_c_supply_detail_seaborn.png)
**Figure 3:** Ranking of Topics by Average Answer Detail (Supply).

* **Takeaway:** The system's resource allocation for detail is highest for topics driven by **knowledge scarcity** ($\text{rye}, \text{pigeon-pea}$).

---

### Next Steps:

<<<<<<< HEAD
1. **Knowledge Quality Assessment (BERTopic)**: Implement BERTopic to analyze community response content, shifting the focus from mere answer length to knowledge focus and quality to precisely identify true information gaps.
=======
1. **Knowledge Quality Assessment (TF-IDF)**: The initial assessment of knowledge quality, shifting focus from mere answer length to semantic depth, has been completed using the Group-wise TF-IDF model.



## Semantic Knowledge Gap Analysis: Quantifying Farmer Demand vs. Supply Detail (challenge-4-crop-questions-tfidf.ipynb)

## 1. Executive Summary

This analysis moves beyond simple keyword matching to quantify the semantic difference between the complexity of farmers' questions and the detail of provided answers. By using **TF-IDF (Semantic Weighting)**, we precisely identify the most critical knowledge gaps in the system.

## Data and Parameters:
The original English dataset is approximately **11.5M** records, but the TF-IDF analysis was performed on a **5 million record sample** of the question/response data set。 The final gap score is heavily weighted towards semantic depth: **Semantic Score (70%)** and **Word Count Score (30%)**


### Key Findings: 

---

#### 1. Critical Knowledge Gap (Semantic Risk)

* **Highest Risk Topics (Low Volume/High Gap):** The most severe gaps are found in low-volume, niche crops: **purple-vetch** ($\text{Gap} \approx 0.0281$), **blackberry** ($\text{Gap} \approx 0.0179$), **rye** ($\text{Gap} \approx 0.0096$), and **mulberry** ($\text{Gap} \approx 0.0089$).
* **Severe Mismatch:** For the top-ranking topic, **purple-vetch**, the **Demand Complexity** ($\approx 0.0531$) is over twice the **Supply Detail** ($\approx 0.0250$). This confirms that farmers are asking highly specific, technical questions using rare terms, but the community's supply lacks the equivalent specialized depth, leading to high unmet semantic need. This demands specialized content creation rather than volume-based solutions.

#### 2. High-Volume, Low-Risk Topics (Foundational Coverage)

* **Balanced Demand/Supply:** High-impact topics such as **General\_Topic**, **cattle**, and **maize** (visible as the largest points on the prioritization matrix) have relatively low semantic gap scores (near or below the $\text{Avg Gap}$ line ($\approx -0.0062$)).
* *Insight:* Despite high volume, the existing knowledge base is adequately broad or foundational to address the complexity of demand, suggesting high-volume repetition, not a fundamental semantic information gap.

#### 3. Knowledge Surplus (Effective Supply)

* **Negative Gaps:** A few topics, including **caliandra** ($\text{Gap} \approx -0.0028$) and **parsley** ($\text{Gap} \approx -0.0024$), exhibit a negative.
* *Insight:* This indicates a knowledge **surplus**. The average **Supply Detail** for these topics is significantly higher than the average **Demand Complexity**, suggesting a strong culture of detailed and comprehensive sharing by experts within these specific sub-communities.

---

## 2. Data

| Column Used | Description | Purpose in Analysis |
| :--- | :--- | :--- |
| `question_topic` | Pre-existing classification of the question's subject (e.g., maize, poultry). | Primary grouping variable for all cross-analyses. |
| `question_content_cleaned` | Cleaned text of the farmer's question. | Used to derive **Demand Complexity** ($\text{Specificity Score}$). |
| `response_content_cleaned` | Answer provided by the community. | Used to derive **Supply Detail** ($\text{Response Score}$). |

---

## 3. Methodology

The core of the analysis is a **Supply-Demand Mismatch Model** built on three key quantifiable metrics:

### 3.1 Feature Engineering (Quantification)
To allow for direct comparison, we used **Min-Max Normalization** to scale all metrics to a uniform $[0, 1]$ range.

* **Question Length Score (Foundational Coverage):** Normalized word count for question content.
* **Answer Length Score (Foundational Coverage):** Normalized word count for response content.

### 3.2 Feature Engineering: Semantic Scoring (Group-wise TF-IDF)
To better capture the specialized depth of conversation within each topic, **TF-IDF was calculated *separately* for each `question_topic` group**. This ensures word importance (IDF) is relative to the topic's own corpus, not the entire 5 million record dataset.

* **Semantic Demand Score:** The average TF-IDF score (measuring specialized depth) for the question content within its topic group.
* **Semantic Supply Score:** The average TF-IDF score (measuring specialized depth) for the response content within its topic group.


### 3.3 Weighted Scoring and Gap Calculation

The model calculates a final weighted score for Supply and determines the Mismatch Gap:

#### Average Demand Complexity
`Average_Demand_Complexity = (Normalized_Question_Length * WEIGHT_COUNT) + (Semantic_Demand_Score * WEIGHT_SEMANTIC)`

#### Average Supply Detail
`Average_Supply_Detail = (Normalized_Answer_Length * WEIGHT_COUNT) + (Semantic_Supply_Score * WEIGHT_SEMANTIC)`

#### Knowledge Gap Score
`Knowledge_Gap_Score = Average_Demand_Complexity - Average_Supply_Detail`



---

## 4. Results and Visualization

The four charts provide a complete diagnostic view, moving from basic frequency to complex risk assessment.

### Report A: Demand Volume Ranking (Frequency)
![Top 10 Question Topics by Demand Volume](https://github.com/yhlien1221/datakit-smallholder-farmers-fall-2025/blob/main/Challenge%204_%20Crop%20Questions/Yuhui_Lien/pictures/top_10_question_volume_report.png)

* **Takeaway:** The top 4 topics represent the highest consumption of system capacity.

### Report B: Knowledge Gap Ranking (Top 15 Unmet Demand)
![Knowledge Gap Ranking Report](https://github.com/yhlien1221/datakit-smallholder-farmers-fall-2025/blob/main/Challenge%204_%20Crop%20Questions/Yuhui_Lien/pictures/1_gap_ranking_report.png)

* **Takeaway:** The highest unmet demand is concentrated in niche crop topics like **purple-vetch** and **blackberry**, which require immediate content focus to address deep semantic deficiencies.

### Report C: Semantic Mismatch: Supply vs. Demand
![Semantic Mismatch Comparison Chart](https://github.com/yhlien1221/datakit-smallholder-farmers-fall-2025/blob/main/Challenge%204_%20Crop%20Questions/Yuhui_Lien/pictures/2_supply_demand_mismatch_labeled.png)

* **Takeaway:** For the top gaps, the **Demand (Complexity)** score significantly exceeds the **Supply (Detail)** score, confirming a severe lack of specialized, high-quality answers relative to the technicality of the questions. The largest gap (**purple-vetch**) shows a Demand score ($\approx 0.0531$) more than double its Supply score ($\approx 0.0250$).

### Figure 4: Prioritization Matrix (Volume vs. Gap)
![Prioritization Matrix: Volume vs. Semantic Gap](https://github.com/yhlien1221/datakit-smallholder-farmers-fall-2025/blob/main/Challenge%204_%20Crop%20Questions/Yuhui_Lien/pictures/3_priority_matrix_labeled_seaborn.png)

* **Takeaway:** This matrix identifies the **Top-Left Quadrant** as the primary risk zone, where low-volume (low impact) topics like **purple-vetch** and **blackberry** carry the highest **semantic risk** ($\text{Y-axis}$). This clarifies that resource allocation should prioritize **content quality and specialization** over simply increasing volume for high-frequency (low-risk) general topics.

---

### Next Steps:

1.  **Actionable Content Strategy:** Use the insights from the Prioritization Matrix to guide specialized content creation for the high-gap, low-volume topics.
2.  **Knowledge Quality Assessment (BERTopic)**: Implement BERTopic to analyze community response content, shifting the focus from mere answer length to knowledge focus and quality to precisely identify true information gaps.
>>>>>>> c6d1eaefaf26b1ce26f014545fc8090ed0bfd1a4
