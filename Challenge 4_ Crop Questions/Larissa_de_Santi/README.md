# Crop Questions Analysis - Unsupervised Clustering

This project was done for Challenge 4 and focuses on applying unsupervised learning techniques to group a multilingual dataset of farmer questions into distinct topic clusters.

## Approach

The initial strategy involved an **unsupervised learning pipeline** on a sample of the full 7.6M+ multilingual question dataset.

1.  **Data Preparation:** A sample of 50,000 unique questions was extracted, duplicates were removed, and `NaN` content was cleaned.
2.  **Embedding Generation:** The `paraphrase-multilingual-mpnet-base-v2` model from `sentence-transformers` was used to generate **semantic embeddings** for the question text. This model is chosen for its ability to handle multiple languages.
3.  **Dimensionality Reduction:** **UMAP** (Uniform Manifold Approximation and Projection) was applied to the high-dimensional embeddings to reduce the data to 2 dimensions for visualization.
4.  **Clustering:** **K-Means clustering (K=3)** was applied to the full-dimensional embeddings to partition the questions into three topic groups.

## 📉 Key Results & Insights

The K-Means clustering, set to `K=3`, did not effectively group questions by topic. Instead, the primary clustering factor was **language**.

### Cluster Inspection

The language distribution across the three largest clusters confirms the challenge of cross-lingual clustering:

| Cluster ID | Size (Questions) | Dominant Language | Language Mix Summary |
| :---: | :---: | :---: | :--- |
| **1** | 7,197 | Swahili (`swa`) | Primarily Swahili (59.7%) and Nyanja (`nyn`) (31.9%) |
| **0** | 4,573 | English (`eng`) | Overwhelmingly English (98.0%) |
| **2** | 4,116 | English (`eng`) | Overwhelmingly English (98.5%) |

* **Observation:** The multilingual nature of the input text seems to dominate the semantic space, causing the model to group by language before topic when clustering the whole dataset. Clusters 0 and 2, which are heavily English, likely contain two different English topics, while Cluster 1 captures the majority of low-resource languages (Swahili and Nyanja).

### New Strategy

Based on this result, the strategy will be **shifted to monolingual clustering** on the English subset to establish reliable topic labels. This approach will allow for better topic separation within a single language before attempting to align low-resource languages to these derived topics.


## 🛠️ Dependencies

This analysis requires the following Python libraries:

* **`pandas`**: For data manipulation and cleaning.
* **`sentence-transformers`**: Specifically the `paraphrase-multilingual-mpnet-base-v2` model for embedding generation.
* **`scikit-learn`**: For the `KMeans` clustering algorithm.
* **`umap` / `umap-learn`**: For dimensionality reduction and visualization preparation.
* **`matplotlib` / `seaborn`**: For data visualization.
