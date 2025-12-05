<<<<<<< HEAD
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
=======
# Larissa de Santi - Challenge 4: Crop Questions Analysis

## Overview
This analysis addresses Challenge 4 by developing a monolingual clustering pipeline to establish topic categories for a large multilingual question dataset. The primary goal is to transform raw farmer questions into actionable insights by classifying them as "Crop-Specific" (production, pest, disease) or "General/Livelihood" (livestock, market, noise).

## Research Questions
- Question 1: What are the primary semantic categories of the questions?
- Question 2: What proportion of the unique questions are Crop-Specific versus General?
  
## Methodology

### Data Source
- producers_direct_dataset.csv

### Approach
1. Translation: All multilingual questions (Swahili, Luganda, Nyanja, etc.) were unified by translation into English. This was done using the translation pipeline developed in Challenge 0 by Anusha Dixit.
2. Embedding: The unified English text was converted into 768-dimensional numerical vectors (embeddings) using the paraphrase-multilingual-mpnet-base-v2 model.
3. Clustering: K-Means clustering (with K=7) was applied to the unified English embeddings to perform topic discovery.
4. Dimensionality Reduction and Visualization: UMAP was used to reduce the high-dimensional embeddings to 2D coordinates for visual interpretation of the clusters and binary categories (crop-specific or general).

### Tools and Technologies
- **Programming Language**: Python 3.11.9
- **Key Libraries**: pandas, numpy, matplotlib, seaborn, scikit-learn, umap, wordcloud, sentence_transformer, transformers
- **GenAI Tool Used**: Gemini Flash 2.5
- **Other Tools**: Jupyter Notebook

## Use of Generative AI

### Tools Used
- **Gemini Flash 2.5**: Used to generate the UMAP reduction framework and configure all visualization plots.

### Human Review Process
- All AI-generated code was reviewed and tested for accuracy
- AI-generated insights were validated against the data
- Modified AI suggestions in the following ways: Inserting code to save the translated dataset and embeddings.

### AI-Assisted vs. Human-Created
- **AI-Assisted**: UMAP framework, visualization plot configuration, and code review support.
- **Human-Created**: All analytical logic (monolingual pipeline design, K-Means application, UMAP parameters), organization, interpretation, and conclusions.

## Key Findings

### Finding 1: Seven core topic clusters
The iterative K-Means clustering analysis successfully identified K=7 as the optimal solution for generating topic labels from the translated question data. This configuration and the translation pipeline effectively overcame the initial problem of language-based grouping that occurred when using cross-lingual models on the multilingual dataset. 

**Implications for Producers Direct:**
The seven semantic clusters, categorized into five agricultural topics (three General/Livelihood and two Crop-Specific), establish a coherent structure for prioritizing content based on farmers' specific needs.

| Cluster ID | Inferred Topic Label | Core Content Focus | Binary Classification |
| :---: | :--- | :--- | :--- |
| **0** | Crop Production & Planting | Seeking **seeds**, ideal **seasons**, general cultivation, and raising seedlings (e.g., coconut, tomatoes, coffee) | Crop-Specific |
| **5** | Crop Management & Pest/Disease | Controlling **pests** (**army worm**), treating **plant diseases** (banana wilt, coffee diseases), and managing chemical inputs (NPK/fertilizers) | Crop-Specific |
| **4** | Livestock & Dairy | Management of cows, maximizing **milk yield**, general cattle health | General |
| **3** | Poultry & Swine Management | Questions about **chickens**, chicks, pigs, and treatment of small animals | General |
| **1** | Market, Business & Location | Inquiries on product pricing, market access/logistics, finding offices/stores, and local geography | General |
| **6** | Noise (Repetitive / Low-Context) | Repetitive phrases and general low-context noise | Noise |
| **2** | Noise (Poor Nyanja Translation) | Unintelligible text, fragmentation (due to low-resource language translation) | Noise |

### Finding 2: Proportion between question categories
The final binary classification shows a clear division in farmer interest:
* Crop-Specific: 35.31% of the questions (Clusters 0 and 5).
* General/Livelihood: 64.69% of questions (Clusters 1, 2, 3, 4, 6).

**Implications for Producers Direct:**
This concentration of questions in General/Livelihood topics (livestock, markets, etc.) suggests that farmers' immediate concerns extend beyond core crop production. This data should inform a strategy to expand and target support for diversified income streams.

## Visualizations

### Clustering
![Clustering](visualizations/viz1.png)

**Interpretation**: The UMAP and clustering process successfully identified meaningful semantic categories despite the initial multilingual challenge, providing a clear foundation for further analysis and targeted support for farmers.

### Word Cloud
![WordCloud](visualizations/viz2.png)

**Interpretation**: The word clouds provide intuitive visual representations of the most frequent and central themes within each of the five identified agricultural clusters (excluding noise). This visualization is crucial for validating the cluster labels (e.g., verifying that "seeds" and "grow" dominate the Production cluster).

## Limitations and Challenges

### Data Limitations
- Data quality concerns: The Nyanja (Nyn) language subset contains unreliable data due to poor translation quality for this low-resource language, resulting in an "unintelligible text" cluster.
- Sample size or coverage limitations: The analysis used a sample of 10,000 rows (3,265 unique questions), meaning the final proportions may not perfectly reflect the entire raw dataset.

### Methodological Limitations
- K-Value Simplification: The K-Means algorithm requires defining K (the number of clusters) upfront. K=7 was chosen through iterative analysis, but this approach simplifies the complex, continuous nature of topic spaces.
- Subjective Interpretation: The final assignment of labels (e.g., "Poultry," "Market") and the binary classification ("Crop-Specific" vs. "General") required manual interpretation of top questions, which introduces a degree of subjectivity.

### Technical Challenges
- Computational constraints: The sequential translation process for Swahili, Luganda, and Nyanja using the Hugging Face pipeline was the most time-consuming step of the workflow.
- Translation accuracy: Low-resource languages like Nyanja posed a significant hurdle, leading to a dedicated "Noise" cluster in the results.

## Next Steps and Recommendations

### For Further Analysis
Perform human validation on the Nyanja (Nyn) cluster (Cluster 2) to ensure the integrity of the final "General" question proportion and inform trustworthy strategic decisions.

### For Producers Direct
1. **Action 1**: Strategically shift content and resource allocation to prioritize high-demand General/Livelihood topics (Livestock, Market Access, Business), reflecting the majority of farmer concerns.
2. **Action 2**: Develop targeted educational content for the top General/Livelihood clusters (e.g., specific modules on maximizing milk yield, swine fever treatment, or digital market pricing).
3. **Action 3**: Invest in human validation by engaging local Nyanja/Luganda speakers to interpret the "Noise" cluster (Cluster 2).

## Files in This Contribution

```
Larissa_de_Santi/
├── README.md (this file)
├── notebooks/
│   ├── larissa_de_santi_v1.ipynb
│   └── larissa_de_santi_v2.ipynb
├── visualizations/
│   ├── viz1.png
│   └── viz2.png
```

## How to Run This Analysis

### Prerequisites
The analysis requires the raw data file (`producers_direct_dataset.csv`) to be present and the installation of several specialized Python libraries:
```bash
pip install pandas numpy matplotlib seaborn jupyter scikit-learn umap-learn sentence-transformers transformers wordcloud tqdm
```

### Running the Analysis
```bash
# Navigate to the notebooks folder
cd notebooks/

# Start Jupyter Notebook
jupyter notebook

# Open and run the file:
larissa_de_santi_v2.ipynb
```

## Contact and Collaboration
* Author: Larissa de Santi
* GitHub: @larisanti
* E-mail: desantilarissa@gmail.com

*I am open to feedback and available to answer questions about this approach.*

## Acknowledgments
Built upon work by Anusha Dixit on the translation pipeline in Challenge 0.

---

**Last Updated**: November 25, 2025
**Status**: Complete
>>>>>>> c6d1eaefaf26b1ce26f014545fc8090ed0bfd1a4
