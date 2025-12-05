'''

for classifying 'clean_text' row of financial inclusion keyword filtered
data (237K rows)

this trains on the Claude-labeled ~4.4K rows, each labeled with 1 of
7 possible classes by Claude, then using a SVM w/ rbf kernel (also tried
naive Bayes and linear SVM); accuracy was about 81%, with the 
confusion matrix showing good precision/recall for all but the
'mon' and 'msc' categories (msc was "out of class" and probably
difficult for the model(s))

after the model is trained, it predicts classes for the remaining
~233K rows of financial inclusion data

there is a 'topics_convert' file used--this is just a simple
dictionary, with plant and animal topics pulled from raw dataset's
'topic' column--so a few hundred crop names and animal types--these
were pluralized with TextBlob .pluralize, then made into a 
dictionary for 'flattening' plant and livestock names to 'product'--
this may help in keeping the classifier focused on important 
words in the strings (could also remove all of the crop/animal
as stop words) 

other notes:
() stopwords were restricted to a very small set, which seemed to
improve classifier accuracy
() both 1- and 2-grams were used, which seemed to improve accuracy--
for example 'how much' could be important for classifying pricing
questions

'''


import pandas as pd

import json

from dotenv import load_dotenv
load_dotenv()

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.svm import SVC


pd.set_option('display.max_columns', None)   # to show full dataframe
# when printing--will display all columns
pd.set_option('display.max_colwidth', None)   # to display full column 
# content (for strings)

pathname = "DataKind_farmers/"
fi_filename = 'FI_claude_class.csv'
conv_file = 'topics_convert.json'  # see header comment for what this is

num_labels = 7   # how many labels total for classification

# these are the expected class labels from Claude
claude_classes = ['pce','mkt','sta','pft','lon','mny','msc']

df_class = pd.read_csv(pathname+fi_filename)
with open(pathname+conv_file, 'r') as file:
  plant_animal_flat_conv = json.load(file)

# dictionary for "flattening" plant and animal names
plant_animal_flat_conv = {}
conv_file = 'topics_convert.json'
if conv_file != '':
    with open(pathname+conv_file, 'r') as file:
        plant_animal_flat_conv = json.load(file)
# flatten conversions even more--flatten plurals (plants->plant etc)
plant_animal_flat_conv = {key:value if value != 'plants' else
                          'plant' for key,value in
                          plant_animal_flat_conv.items()}
plant_animal_flat_conv = {key:value if value != 'animals' else
                          'animal' for key,value in
                          plant_animal_flat_conv.items()}
# completely flatten to "product"
plant_animal_flat_conv = {key:'product' for key,value in
                          plant_animal_flat_conv.items()}

def flatten_pl_an(text):
  # takes text string and uses flattening dictionary re plant/animal refs
  return ' '.join([word if word not in plant_animal_flat_conv
                 else plant_animal_flat_conv[word]
                 for word in text.split()])

df_class['clean_text'] = df_class['clean_text'].apply(flatten_pl_an)

# pull the ~smallish subset with class labels:
df_labeled = df_class.loc[~pd.isna(df_class['class'])]
# set aside remaining, unlabeled instances for later
df_remainder = df_class.loc[pd.isna(df_class['class'])][['org_idx','clean_text','class']]

# remove duplicate strings for training:
df_labeled = df_labeled[['clean_text','class']].copy()
df_labeled = df_labeled.groupby('clean_text').nth(0)

XX, yy = df_labeled['clean_text'], df_labeled['class']

stop_words_list = ['in','the','of','to','for','and']  # these are 
# a custom stopword list--removing the usual full 'english' set of
# stopwords seemed too restrictive--small words (like 'how' or 'what')
# could make a big difference in classifier accuracy for strings
# this short / simple

# create pipeline with desired classifier
# for SVC classifier on multiclass, the default is one-v-rest; 
# SVM rbf parameters optimized from earlier grid search:
text_clf = Pipeline([
    ('vect',TfidfVectorizer(ngram_range=(1,2),stop_words=
                        stop_words_list)),
    ('clf',SVC(C=500, class_weight='balanced',gamma=0.001,kernel='rbf')),
    ])

text_clf.fit(XX,yy)

yy_predict = text_clf.predict(df_remainder['clean_text'])

df_remainder['class'] = yy_predict

print(df_remainder.head(5))

df_out = df_remainder.drop(columns=['clean_text'])  # only save org_idx alongside
# class
df_out['predicted'] = True   # boolean to indicate which labels came
# from prediction (eg SVM) and which from "manual" labeling

# concat with "hand labeled" (Claude) rows:
df_labeled = df_class.loc[~pd.isna(df_class['class'])].copy()
df_labeled['predicted'] = False
df_labeled = df_labeled[['org_idx','class','predicted']]

df_fin = pd.concat([df_out,df_labeled],axis=0)

# should be True:
print(set(df_fin['org_idx'])==set(df_class['org_idx']))

df_fin.to_csv(pathname+'FI_SVM_rbf_predicts.csv')

