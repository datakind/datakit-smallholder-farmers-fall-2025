# Stephanie Lang - Translation Runyankole Analysis

## Overview
A key element of a text message-based peer-networking system is the ability to communicate effectively, and for the members to get the information they're looking for rapidly, and reliably. Machine translation facilitates broader interaction across different smallholder language groups; and facilitates complete message data analysis, across languages and geographies. This analysis project shows that free open source machine translation is possible with minimal infrastructure, however much more training data is required to make such a solution feasible for business application.

## Research Questions
- Question 1: Given that Runyankole is a low-resource language, how well can machine learning models perform in the task of language translation?
- Question 2: Hw can existing datasets be improved to provide better model performance?
- Question 3: Can open source software, and CPU handle such large datasets for traning machine learning models locally, on a laptop, for example, with 32GB RAM.

## Methodology

### Data Sources
- SALT "text_all" parquet files: processed for sequence-to-sequence predictive model. [https://huggingface.co/datasets/Sunbird/salt](https://huggingface.co/datasets/Sunbird/salt)
- VOS Runyankole_manual.pdf: manually processed for curating a word/phrase list to append to the SALT dataset; and processed for sequence-to-sequence predictive model. [https://western-uganda.net/resources/runyankole_manual.pdf](https://western-uganda.net/resources/runyankole_manual.pdf)

### Approach
1. **Step 1**: WeFarm data loading and filtering
2. **Step 2**: Nyn messages dataset data preprocessing
3. **Step 3**: Nyn dataset reshaping
4. **Step 4**: Nyn natural language processing, topic analyses, and visualizations
5. **Step 5**: SALT data loading and filtering
6. **Step 6**: Sequence-to-sequence recurrent neural network model building
7. **Step 7**: Sequence-to-sequence model training, prediction, and performance evaluation
8. **Step 8**: Sequence-to-sequence transformer model building
9. **Step 9**: Sequence-to-sequence transformer training, prediction, and performance evaluation
10. **Step 10**: Sequence-to-sequence transformer 
11. **Step 11**: Training dataset expansion and data preprocessing
12. **Step 12**: Sequence-to-sequence transformer training, prediction, and performance evaluation
13. **Step 13**: WeFarm Nyn messages machine Translation - in progress
14. **Step 14**: Topic modelling and Latent Dirichlet Allocation (LDA) - incomplete

### Tools and Technologies
- **Programming Language**: R
- **Key Libraries**: tidyverse, keras, tensorflow, reticulate, tfdatasets, magrittr, arrow, duckdb, sparklyr, rmarkdown, knitr
- **GenAI Tools Used**: Duck.AI free (GPT-5 Mini) used in initial EDA for manual translation of specific frequent Runyankole terms.
- **Other Tools**: Notepad++ v8.8.7, WSL2, Ubuntu 24.04.3 LTS, R version 4.5.2 (2025-10-31), Renv Version 1.1.5, RStudio Server 2025.09.2+418 (Cucumberleaf Sunflower) for Ubuntu Jammy, Python 3.12.12, openjdk version 1.8.0_472, Microsoft Excel 2010 Student License

## Use of Generative AI

### Tools Used
- **Duck AI GPT-5 Mini**: Used for manually translating selected frequent Runyankole terms during initial EDA, when the term wasn't found in the pdf manual.

### Human Review Process
- The manual translations mentioned above could not be verified against any official sources, or Runyankole speakers.

### AI-Assisted vs. Human-Created
- **AI-Assisted**: manual translation from EDA frequent Runyankole terms list.
- **Human-Created**: all data collection, code, and analysis.

## Key Findings

### Finding 1: It is possible to train ML models with low-resource language datasets, using minimal computing resources
The RMarkdown project files demonstrate that open source software, and CPU can be utilised for training models for machine translation.

**Implications for Producers Direct:**
- Machine translation can be implemented with minimal costs, and infrastructure
- In-house data scientists should be appointed to collate datasets

### Finding 2: Expanding available public datasets with manually collated word/phrase lists improves model performance
Description of the finding, supported by data and visualizations.

**Implications for Producers Direct:**
- With the help of local residents, who speak the low-resource languages fluently. Producers Direct could advance natural language processing capability for theirs, and their partners' expanded use cases.

## Visualizations

### Frequent Runyankole Terms
![unnamed-chunk-19-1.png](../SBLANG-NLP/challenge0-translation-nlp-eda-nyn_files/figure-html/unnamed-chunk-19-1.png)

![nyn_freq_terms.jpg](nyn_freq_terms.jpg)

**Interpretation**: These bar graphs show the frequency of Runyankole terms in all the messages, both questions, and responses. There's many messages about livestock, such as cows, goats, chickens, and pigs; and some about agriculture, such as beans, coffee beans, and tomatoes; with some other topics such as medicine, and meetings/gatherings. There's cultural significance in the prevalence of a respectful form of address.

| | Runyankole | English | Citation | Part-of-speech | Singular or Plural | Top rank
---|---|---|---|---|---|---|
25 | kandi | and, again, moreover | manual | conjunction |  | 1
46 | nimbuza | """Nimbuza"" is Luganda slang for a small, informal gathering or hangout — often used to mean a casual meeting with friends, a short party, or chilling together." | GPT-5 mini | noun |  | 2
49 | ninyenda | I want | manual | enda (verb) |  | 3
18 | enkoko | hen(s), fowl(s) | manual |  |  | 4
52 | nyine | I have | manual | ine (verb) |  | 5
58 | omubazi | "Drug; medicine; ointment" | manual | noun |  | 6
19 | ente | cow | manual | noun |  | 7
20 | enyanya | tomato | manual | noun | singular | 8
12 | ebihimba | bean | manual | noun | plural | 9
15 | embuzi | goat | manual | noun |  | 10
60 | omwani | Coffee bean | manual |  | singular | 11
37 | mwebare | thank you | manual |  | plural | 12
67 | zingahi | How much? | manual |  |  | 13
16 | empunu | pig | y'empunu-pork-manual |  |  | 14
33 | mubaziki | "In Ugandan Luganda, ""mubaziki"" (often spelled ""mubazike"") is a polite form of address meaning ""my respected one"" or ""sir/ma'am"" used when speaking to someone of higher status or to show respect. It combines the possessive ""muba-"" (you/respected) with a respectful suffix; usage varies by region and context." | GPT-5 mini |  |  | 15
51 | nkoreki | "In Uganda, ""nkoreki"" (also spelled ""nkoleki""/""nkoleky"") is a Runyankore/Runyankole adjective meaning ""from Nkore"" or ""related to Nkore"" — i.e., something or someone belonging to the Nkore (Ankole) region/people." | GPT-5 mini |  |  | 16
22 | hati | Now, today | manual | adverb |  | 17
66 | zangye | Mine | manual |  | plural | 18
48 | ninye | I | Ryangye-manual-My/mine |  |  | 19
27 | kuhinga | "To cultivate; do gardening" | manual |  |  | 20

> [!NOTE]
> Refer to the data sources in this readme for details regarding the "manual", and "GPT-5 mini" citations.

### Sequence-to-Sequence RNN Model Training
[seq2seq_rnn.html](seq2seq_rnn.html)

[seq2seq_rnn_plus_vocab.html](seq2seq_rnn_plus_vocab.html)

**Interpretation**: These graphs show the RNN model training metrics before, and after the vocabulary size variable was increased from 1000 to 15000. The model accuracy decreased from 48.9% to 40%, however a more apropriate metric, such as BLEU should be calculated.

### Transformer Model Training
[transformer.html](transformer.html)

[transformer_expanded.html](transformer_expanded.html)

**Interpretation**: This graph shows the transformer model training metrics, before, and after expanding the training dataset with the manually collated word/phrase list from the manual pdf. There's an increase in accuracy from 58.7% to 70.5%, however as stated above, a BLEU score would be more appropriate for model evaluation, and comparison. Unfortunately, the increase in validation loss indicates overfitting, which should be corrected, for example, by adjusting the network's layers.

## Limitations and Challenges

### Data Limitations
- Runyankole is a low-resource language, because there's few publicly available datasets, and resources for training translation ML models, which results in limited vocabulary, and poor contextual training.
- Geographical data are omitted/unavailable for all the messages, limiting spatial data analysis
- Some responses were either aggregated by the system, or answered by a system-selected group of recipients to answer, which cannot be explicitly identified, and may influence analysis results, for example, system-generated topics frequencies

### Methodological Limitations
- Assumptions made
- Simplifications required
- Alternative approaches not explored

### Technical Challenges
- Computational constraints
- Translation accuracy issues
- Other technical hurdles

## Next Steps and Recommendations

### For Further Analysis
1. **Recommendation 1**: Continue expanding the word/phrase list and retrain the transformer model with a larger vocabulary
2. **Recommendation 2**: Fine-tune the transformer model, and calculate BLEU scores for each model
3. **Recommendation 3**: Reuse the project for Luganda, and Swahili, which were found to have more public training datasets, and online resources.
4. **Recommendation 4**: Conduct topic modelling across English, and translated datasets, for example, LDA, or clustering based on Association Rules.

### For Producers Direct
1. **Action 1**: After the fourth recommendation is completed, the data should be joined to geographical data for spatial analysis.
2. **Action 2**: After action 1, the data are ready for further analysis using public datasets from the national offices' of statistics, e.g. Uganda Bureau of Statistics "Monthly_rainfall_for_selected_centres_(mm),_2014_–_2020.xlsx", "Crop_production_for_selected_Food_Crops,_2015-2021_(MT) (1).xlsx". Spatial analysis is recommended for predictive analytics, such as climate change.
3. **Action 3**: Partnership with local organisations, such as the Makerere University, to jointly advance low-resource language models, such as the SALT project, which would benefit both parties

## Files in This Contribution

```
SBLANG-NLP/
├── readme.md (this file)
├── challenge0-translation-model-nyn.Rmd
├── challenge0-translation-nlp-eda-nyn.Rmd
├── challenge0-translation-nlp-eda-nyn_files
│   └── figure-html/
│        └── unnamed-chunk-19-1.png
├── nyn_freq_terms.tiff
├── readme.md
├── seq2seq_rnn.html
├── seq2seq_rnn_plus_vocab.html
├── top_terms_nyn.csv
├── top_terms_nyn.xlsx
└── transformer.html

```

## How to Run This Analysis

### Prerequisites

> [!NOTE]
> This project has been tested on 64 bit Windows 11. All other versions are listed earlier in this README.

#### Windows 11 Environment Setup
- Install Git, and set up the security prerequisites in the official GitHub docs.
- Install WSL2
- Install Ubuntu
- Install R
- Install R Studio Server
- Install Java (if using Spark)
- Install Python and add the configuration to your shell file, for example: 

```
sudo vim ~/.bashrc
```


```
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - bash)"

eval "$(pyenv virtualenv-init -)"
```

- Create a new project from this DataKit Event source code repository, and paste the repo URL.
- Git Clone the SALT repository
- Initialise Renv in RStudio Project Settings
- Install package according to the versions in this README, for example:

```
renv::install.packages("tidyverse")
```


### Running the Analysis
- Update file paths for your own environment.
- Run each code chunk as required.

> [!NOTE]
> Some steps are optional, and require additional refactoring, which may improve computation performance.

- Optionally, render knitr output (html) by clicking the "Knit" button.

## References and Resources

### Academic Papers
= [Machine Translation For African Languages: Community Creation Of Datasets And Models In Uganda](https://openreview.net/pdf?id=BK-z5qzEU-9). Benjamin Akera, Jonathan Mukiibi, Lydia Sanyu Naggayi, Claire Babirye, Isaac Owomugisha, Solomon Nsumba, Joyce Nakatumba-Nabende, Engineer Bainomugisha, Ernest Mwebaze, John Quinn. 3rd Workshop on African Natural Language Processing, 2022. 

### Datasets
- Sunbird African Language Technology (SALT) subset text-all dataset [https://huggingface.co/datasets/Sunbird/salt](https://huggingface.co/datasets/Sunbird/salt)
- VSO Mbarara volunteer manual "runyankole_manual.pdf" 

### Tools and Libraries
- tidyverse 2.0.0 [https://tidyverse.tidyverse.org](https://tidyverse.tidyverse.org)
- keras 2.16.0 [https://tensorflow.rstudio.com/](https://tensorflow.rstudio.com/)
- tensorflow 2.20.0 [https://github.com/rstudio/tensorflow](https://github.com/rstudio/tensorflow)
- reticulate 1.44.1 [https://rstudio.github.io/reticulate/](https://rstudio.github.io/reticulate/)
- tfdatasets 2.18.0 [https://github.com/rstudio/tfdatasets](https://github.com/rstudio/tfdatasets)
- magrittr 2.0.4 [https://magrittr.tidyverse.org](https://magrittr.tidyverse.org)
- arrow 22.0.0 [https://arrow.apache.org/docs/r/](https://arrow.apache.org/docs/r/)
- duckdb 1.2.1 [https://r.duckdb.org/](https://r.duckdb.org/)
- sparklyr 1.9.3 [https://spark.posit.co/](https://spark.posit.co/)
- rmarkdown 2.30 [https://pkgs.rstudio.com/rmarkdown/](https://pkgs.rstudio.com/rmarkdown/)
- knitr 1.50 [https://yihui.org/knitr](https://yihui.org/knitr)

## Contact and Collaboration

**Author**: Stephanie Lang
**GitHub**: [@SBLANG](https://github.com/SBLANG/)

**Collaboration Welcome**: 
- Open to feedback and suggestions
- Happy to collaborate on related analyses
- Available to answer questions about this approach

## Acknowledgments

- Inspired by works of François Chollet, J.J. Allaire, and Tomasz Kalinowski.

---

**Last Updated**: 6 December 2025
**Status**: [Needs Review]
