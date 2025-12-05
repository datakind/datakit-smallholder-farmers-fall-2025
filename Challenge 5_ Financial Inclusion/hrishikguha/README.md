# Financial Needs Analysis via Semantic Clustering
Feel free to point out any of the many mistakes I'm sure I've made.
This project uses multi-lingual embeddings, cosine similarity scoring, and k-means clustering to explore the financial aspect of questions asked in the dataset. 
Since the raw dataset was over 7 GB, I processed it in batches using Polars, writing intermediate results to 101 small Parquet files so we could scale analysis without loading everything into memory at once. 
 
In the first notebook, 10 of these files were imported, making up about 2 million rows, which seemed like a comfortable number for initial analysis. The first notebook imported the 10 parquet files, made use of the embedder "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2" for each question, and concatenated the parts. Then some target phrases were defined and the embeddings were generated for the same. The cosine similarity scores were then calculated, in batches to preserve memory. The results are saved to all_10_parts_scored.parquet.
The first notebook is on Kaggle [here](https://www.kaggle.com/code/hrishikguha/wefarm-embedding-similarity-scoring) and "all_10_parts_scored.parquet" can be downloaded from the output section.

In the second notebook, the all_10_parts_scored.parquet file is used. The proportion of financial questions are calculated, along with some aggregated measures for the confidence scores. The method discovered 1520 (~1%) financial questions, proportionally seeming small but still a lot for just 1/10th of the data. Then we proceed to clustering, after using the elbow method and silouhette score for arriving at the number of clusters. K-means clustering with k=8 is applied. The clusters are mapped back, and the major themes in the financial subset of questions are explored.

The cluster themes go as follows: "Saving", "Loans", "Cash Crops", "Government assistance, grants and subisidies", "Earnings from Farm", "Managing Farm Finance", "Farm Inputs", and generic questions about which farming and poultry uses are the best.

A pdf version with the output as I saw it, along with the code notebook(sans-output) is uploaded here. In order to run the code, a manual data upload is needed:

1.  Visit the **Kaggle Notebook Link** and go to the **Output** section.
2.  **Download** the `all_10_parts_scored.parquet` file.
3.  Open the `02_Thematic_Analysis.ipynb` notebook in Google Colab.
4.  Upload the downloaded 1.08 GB file into your Colab session's root directory before running the analysis cells.
Or alternatively use a Kaggle API token.


Another idea is to use joeddav/xlm-roberta-large-xnli which is a multi-language NLI for zero-shot classification. Or maybe once the #challenge0 work is complete, a more refined approach can be taken. Feel free to point out any of the many mistakes I'm sure I've made.
