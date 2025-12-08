# Predicting Values For Missing Topics / Challenge 2 Seasonality

## Purpose
To investigate any trends between seasonality and the type of questions asked. 

## Steps
- Clean data and create additional columns by breaking the date of the question out to 'year', 'month' and day of the week.
- Partition the data between datasets with a valid entry for 'question_topic' and one where the 'question_topic' is missing.
- Use model to make predictions for those records with a missing value for 'question_topic'
- Include 2 different methods for relabelling some of the existing values for 'question_topic' to a topic more specific and thus accurate
- Create barplots to examine any trends between seasonality (months) and questions asked as represented by 'question_topic'

## Jupyter Notebooks Explanation
- data_wrangling_new_features.ipynb was used to remove non-alphanumeric characters except single spaces from 'question_content' plus add some additional features/columns
- relabel_question_topic.ipynb was used to perform 2 different methods for relabelling existing 'question_topic' values with a more specific label
- estimate_missing_topic_no_relabel.ipynb was used to make predictions for the rows with missing values for 'question_topic'
- estimate_missing_topic_with_relabel_v1.ipynb uses the first method of relabelling data to make predictions for the rows with missing values for 'question_topic'
- estimate_missing_topic_with_relabel_v2.ipynb uses the second method of relabelling data to make predictions for the rows with missing values for 'question_topic'
- challenge_2_seasonality_animals_vs_plants.ipynb groups all question topics into either animals or plants to compare if there are any seasonal trends and if the trend differs between animals and plants
- challenge_2_seasonality_top5_topics.ipynb compares the trends for the top 5 most commonly asked type of question over different years for each country and before any relabelling has been performed
- challenge_2_seasonality_top5_topics.ipynb compares the trends for the top 5 most commonly asked type of question over different years for each country after relabelling version 2 has been performed

## Results
### Estimating Predicted Values
The original dataset, before any relabelling was performed, was trained and tested with a prediction accuracy of 90.27% accurate.
Of the 2 methods used for relabelling existing 'question_topic', version 2 gave the best improvement in predicting with an accuracy around 92.18%.

## Suggestions For Further Work
Reduce the 148 different question topics into a smaller number of categories so that better comparisons can be made.
Relabelling can be further improved by adding more alternative values for each topic such as common spelling mistakes.
