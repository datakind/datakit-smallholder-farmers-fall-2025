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
On the test dataset the model was 90.27% accurate.

## Suggestions For Further Work
Amongst the values within 'question_topic' are some that are more generic than others. These include 'plant', 'animal', 'poultry', 'bird', 'grass', 'crop', 'vegetable', and 'tree'.

'plant' from 'question_topic' had a very poor accuracy rate despite the high number of records in the train and test dataset. In at least some cases, another more specific label, as used for other records, might have been a more accurate and descriptive topic. Making such changes could potentially improve the accuracy of the model further.

