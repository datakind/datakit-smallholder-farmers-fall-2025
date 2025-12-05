The files in this folder are divided into two main sections.

### financial inclusion keyword filter and text classifier

Included are 3 scripts (FI_Claude_label_subset.py, FI_SVM_predictions.py, FI_keywords.py) and 2 short dictionaries (topics_convert.json, corr_all_dcts...) for,
* filtering the raw raw_dataset_producers_direct.csv file by keywords relevant to financial inclusion, which out of about 2.8M unique English language questions produced about 237K unique rows
* performing text classification on the questions in the 237K rows, producing 7 classes of questions, explained in the FI_Claude_label_subset.py code comments

Topic modeling and manual review of a small subsample of questions were used to generate 7 financial-inclusion question classes (loans, pricing, ...) Anthropic's Claude was used to classify a small (4K) subset of the 237K questions into the 7 categories. Various NLP classifier schemes were trained on the Claude-labeled subset. After trying naive Bayes (75% accuracy), SVM linear (80% accuracy), SVM rbf (81% accuracy), and fine-tuning two BERT models on a Colab notebook (82-83% accuracy), the SVM rbf was settled on for a balance between accuracy and speed. The SVM rbf's predictions were recorded on the remaining 233K unlabeled instances.

### data analysis notebook

An informal report is included in the Jupyter notebook file FI_analysis_final.ipynb. Overall, the raw time series data is highly oscillatory, on approximately a monthly basis, making interpretations on planting/harvesting seasonality difficult. Market and pricing questions dominated the financial inclusion topics.
