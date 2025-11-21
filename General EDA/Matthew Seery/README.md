# Predicting Values For Missing Topics

## Purpose
To fill in the missing values for question_topic that account for less than 20% of all records in the dataset. 

## Method
- Use a transforner block algorithm to test the model on train/validation datasets
- Assess performance on test dataset
- Use model to make predictions for those records with a missing value for 'question_topic'

## Jupyter Notebooks Explanation
- data_wrangling_new_features.ipynb was used to remove non-alphanumeric characters except single spaces from 'question_content' plus add some additional features/columns
- dataset_partition.ipynb was used to partion the dataset between records with and without a value for 'question_topic'
  NB: This notebook also includes other partitions which I may use later
- estimate_missing_topic.ipynb was used train a model using the dataset with valid 'question_topic' and then use the model to predicit values where they are missing

## Results
On the test dataset the model was 82.7% accurate

## Further Work
I am aware that within the missing values there are questions that do not appear to relate to the existing 148 labels in 'question_topic'. However, there are still questions in this dataset that relate to the given topics,

I want to look further into how well the model is predicting the missing values.


