--This file creates the main dataset used in Tableau for the analysis
  
COPY (
 select org_idx, question_id, question_user_id, question_content, question_topic_clean as question_topic
 , question_sent::date as question_sent, question_user_country_code
 , financial_subcategory
 , financial_theme_condensed as matched_keyword
 , financial_flag
from questions_deduped 
) TO 'C:\Users\enaho\Downloads\cleaned_question_data_streamlined.csv' (FORMAT CSV, HEADER TRUE);
