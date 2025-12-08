# [Beatrice Liu] - [Challenge 4 - Crop Questions] Analysis -- ** incomplete **

## Overview
Created bi-, tri-, and quad-grams and interactive visualizations for English questions by Kenyan farmers on top 5 topics -  cattle, tomato, maize, chickens, none -  to discern most common questions; these can be used by Producers Direct to create FAQ for smallholder farmers.  Sadly, I can't figure out how to display the interactive graphs here, but they are saved in the network_graphs folder.

## Research Questions
- What insights can be gleaned from Crop-specific and Crop-Independent Questions?  


## Methodology: detailed explanation in the Jupyter Notebooks

### Data Sources
- Producers Direct Dataset
- Swahili stopword and verb lemmatization files  

### Approach /  Notebook overviews describe steps in greater detail - see 'Q4.Ngrams.Jupyter.Notebooks.pdf' for list of notebooks and running order
1. **Step 1**: Data loading and initial exploration
2. **Step 2**: Data cleaning and preprocessing
3. **Step 3**: Data segmentation into smallers datasets for analysis: unique questions asked by farmers in 4 countries
4. **Step 4**: Visualization and interpretation
 

### Output Files and Visualizations
- Cleaned data files and interactive visualizations can be found in [google drive folder](https://drive.google.com/drive/folders/1tpwqTqoFfZCWvDvncJjaSbzzua0Y6Q_i?usp=sharing)
- Note:  visualizations are uploaded to github in 'network_graphs' folder
- N-gram frequency graphs can be found in individual notebooks; the PNG files created cropped out the text 


### Tools and Technologies
- **Programming Language**: Python 3.13.5 
- **Key Libraries**: pandas, numpy, matplotlib, nltk, deep-language... - full list is in the notebooks
- **GenAI Tools Used**: ChatGPT, Anaconda Toolbox
- **Other Tools**: Jupyter Notebook


### Tools Used
- **ChatGPT**: Used for generating code for natural language processing functions in English, translating Swahili tokens into English
- **Anaconda Toolbox**: Used for generating interactive network graphs

### Human Review Process
- All AI-generated code was reviewed and tested for accuracy
- AI-generated insights were validated against the data
- Modified AI suggestions in the following ways: coding errors


## Key Findings: 

### Finding 1: [Translating from Swahili is a major roadblock]
- Created bi-, tri-, grams- to cut down on # of characters that needed to be translated
- Tri-grams from Swahili questions are similar to English ones...
- but need *better* lemmatization, normalizing tools, Swahili corpus, and translator.  


### Additional Findings:  Refer to 'farmers.pptx'
Description of the finding, supported by data and visualizations.


## Visualizations

### [Visualization 1 Title]
![Visualization 1](visualizations/viz1.png)

**Interpretation**: What this visualization shows and why it matters.

### [Visualization 2 Title]
![Visualization 2](visualizations/viz2.png)

**Interpretation**: What this visualization shows and why it matters.

## Limitations and Challenges

### Data Limitations
- Missing data issues:  gender, location other than country
- Data quality concerns: vague data dictionary
- Sample size or coverage limitations:  

### Methodological Limitations
- Assumptions made: dropped 'blocked' and 'destroyed' users
- Simplifications required
- Alternative approaches not explored

### Technical Challenges
- Computational constraints
- Translation accuracy issues - YES, need Wwahili NL processor trained on agricultural terms
- Other technical hurdles - 



## Files in This Contribution

```
Bliu_analysis/
├── README.md (this file)
├── notebooks/
│   ├── question_preprocess.ipynb
│   ├── kenya_q_eng.ipynb
│   └── kenya_q_swa.ipynb
│   └── nlp_swa.ipynb
│   └── translate.ipynb
│   └── nlp_eng.ipynb
│   └── nlp_eng_q_notopic.ipynb
│   └── nlp_eng_cattle.ipynb
│   └── nlp_eng_chicken.ipynb
│   └── nlp_eng_maize.ipynb
│   └── nlp_eng_maize.ipynb
├── 10 interactive visualizations/
│   ├── *xx*bigram_eng_ken_*topic*_network.html
│── static directed network visualizations/
│   └── top40trigrams_ken_eng_network.png
│   └── top40bigrams_ken_eng_network.png
│   └── top40bigrams_ken_eng_Notopic_network.png
│   └── top40trigrams_ken_eng_network.png
├── results - *work in progress*/
│   ├── summary_statistics.csv
│   └── findings.md
└── translated n-grams from swahili to english data/ 
    └── ken_240quadgrams_swa2eng.txt
    └── ken_500bigrams_swa2eng.txt
    └── ken_500trigrams_swa2eng.txt
```

### How to Run This Analysis -- *I have no clue, did everything in Jupyter*


### Open and run notebooks in order: refer to 'Q4.Ngrams.Jupyter.Notebooks.pdf' 

```


### Contact and Collaboration

**Author**: [Beatrice Liu]
**GitHub**: @bl1412
 

---

**Last Updated**: [Date]
**Status**: [Analysis Complete, but Findings Summary is WIP]
