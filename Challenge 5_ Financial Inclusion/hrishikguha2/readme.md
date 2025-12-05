Producers Direct: Farmer Needs Prioritization Analysis

Project Summary

This project's goal was to transform raw, multilingual farmer questions into actionable strategic insights for Producers Direct. By combining Machine Translation, Semantic Clustering, Large Language Model (LLM) classification, and a custom Severity Scoring metric, we prioritized farmer needs based on two factors: Frequency (how often a need occurs) and Urgency (how critical the need is, especially if financial).

The final output is a ranked list of clusters, identifying the most critical informational and financial opportunities for strategic investment and product development.

🚀 Stage 1: Data Preparation & Multilingual Translation

The initial dataset contained raw farmer questions across several East African languages (Swahili, Luganda, Nyankore). These were cleaned and translated to enable consistent analysis.

Language Filtering (FastText): The raw dataset was processed using the FastText language identification model (lid.176.bin). This step efficiently filtered down the massive dataset to only include questions written in the target languages: Swahili (sw), Luganda (lg), and Nyankore (nyn).

Machine Translation (Helsinki-NLP): The filtered questions were translated into English using the state-of-the-art multilingual neural machine translation (NMT) model (Helsinki-NLP/opus-mt-mul-en). This created the question_content_en column, ensuring all subsequent semantic analysis was performed on a unified English corpus.
The notebook is [here](https://www.kaggle.com/code/hrishikguha/notebook9e8a5166f1)

🧠 Stage 2: Thematic Clustering (HDBSCAN with GPU Acceleration)

Once the data was translated, I performed unsupervised machine learning to group similar questions into thematic clusters.

Semantic Embedding (Sentence Transformers): The translated English questions were converted into high-dimensional numerical vectors (embeddings) using the all-MiniLM-L6-v2 Sentence Transformer model. These embeddings capture the meaning of the question content.

GPU Acceleration (RAPIDS cuML): RAPIDS cuML was used to significantly accelerate the clustering process on a GPU.

Why cuML: For a dataset of this scale, generating embeddings and calculating the high-dimensional distances necessary for clustering is computationally intensive. Using the cuML implementation of UMAP and HDBSCAN drastically reduced the processing time from hours (on CPU) to minutes (on GPU), making the pipeline feasible for large-scale data.

Clustering (HDBSCAN): Hierarchical Density-Based Spatial Clustering of Applications with Noise (HDBSCAN) was applied to the embeddings.

HDBSCAN automatically determined the optimal number of clusters based on data density.

It assigned a cluster_id to each question, effectively grouping all questions about "maize pest control" or "loan repayment schedules" together.

A special cluster ID (-1) was used for noise/outliers, and another (-999, the Virtual Cluster) was created to merge all small, low-frequency clusters for a single consolidated analysis.

🔍 Stage 3: Financial Intent Mapping (Gemini API)

To understand the strategic implication of each cluster, we used the Gemini API to classify the core need represented by the most frequent questions in each cluster.

Cluster Summarization: For each large cluster (and the Virtual Cluster -999), a sample of the most representative questions was extracted.

LLM Classification: The Gemini API (gemini-2.5-flash-preview-09-2025) was instructed with a system prompt to act as an analyst and classify the need of the cluster into a predefined financial taxonomy (e.g., Working Capital, Risk Mitigation, None/Information Need).

Output Generation: The LLM output two key fields for each cluster:

financialNeed: The primary category of the problem.

productOpportunity: A specific, proposed solution (e.g., "Short-term micro-loan," or "Localized digital advice").

📊 Stage 4: Strategic Prioritization & Severity Scoring

The final stage combined the results of Stages 2 and 3 into a single, actionable score to rank clusters by strategic importance.

Severity Weighting: Each financialNeed category was assigned a numerical weight (0.0 to 1.0) based on its strategic urgency (e.g., Working Capital was weighted higher than a general Information Need).

Frequency Calculation: The percentage of total questions represented by each cluster (cluster_frequency) was calculated.

Severity Score: The final score was calculated using the formula:

Severity Score = Cluster Frequency times Severity Weight

Reporting: The clusters were sorted by the Severity Score. The strategic_report_generator.py script produced two key artifacts:

Text Report (top_priority_clusters_report.txt): A ranked list of the top clusters, detailing their size, primary need, and the specific Strategic Opportunity (the product/service hypothesis) derived from the LLM classification.

Visualization (severity_score_bar_chart.png): A bar chart visually representing the top clusters, allowing executives to quickly identify which needs carry the highest combined risk/opportunity profile.

This pipeline is an attempt at aiding a focus of development efforts where farmer demand (frequency) and financial urgency (severity) are highest.
