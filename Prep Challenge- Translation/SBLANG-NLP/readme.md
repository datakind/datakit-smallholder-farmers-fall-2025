---
title: "Prep Challenge0- Translation- Nyankore"
author: "SBLANG"
date: "2025-11-14"
output: 
  html_document:
    toc: TRUE
    toc_float: TRUE
    code_folding: hide
    number_Sections: TRUE
---

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE)
```

# Setup

```{r}

# Import packages
suppressPackageStartupMessages(library('tidyverse'))
suppressPackageStartupMessages(library('keras'))
suppressPackageStartupMessages(library('tm'))


```


# Data Preparation
## Load data

```{r}

# Import csv

messages <- read.csv('C://tmp/DK/b0cd514b-b9cc-4972-a0c2-c91726e6d825.csv', sep = ',', quote = '"', header = TRUE, fileEncoding = 'UTF-8')


```


```{r}

head(messages)

```


## Transform data
### Extract dataset for Nyankore
Limit computation to Nyankore questions or answers only.


```{r}

messages_nyn <- messages %>%
  filter(question_language == 'nyn' | response_language == 'nyn')

```

```{r}

messages_eng <- messages %>%
  filter(question_language == 'eng' | response_language == 'eng')

```

```{r}

messages_swa <- messages %>%
  filter(question_language == 'swa' | response_language == 'swa')

```


```{r}

messages_nyn_filt <- messages_nyn %>%
  select(question_content, question_topic, response_content, response_topic)

```

```{r}

messages_nyn_filt <- messages_nyn_filt %>%
  mutate(row_id = row_number())

```

```{r}

messages_nyn_q <- messages_nyn_filt %>%
  select(question_content, question_topic) %>%
  mutate(content_type = as.factor('q'))

```

```{r}

messages_nyn_a <- messages_nyn_filt %>%
  select(response_content, response_topic) %>%
  mutate(content_type = as.factor('a'))

```


### Reshape data
Focus only on message content for text frequency analysis. Combine questions and answers, and categorise by type.

```{r}

messages_nyn_qa <- rbind(messages_nyn_q, messages_nyn_q)

```

```{r}

messages_nyn_qa <- messages_nyn_qa %>%
  mutate(content = question_content, ... = NULL) %>%
  mutate(topic = question_topic, ... = NULL) %>%
  mutate(type = as.factor(content_type), ... = NULL) %>%
  select(content, topic, type)
head(messages_nyn_qa)


```

### Create corpus

```{r}

# Generate volatile corpus.
corp_nyn <- VCorpus(VectorSource(messages_nyn_qa$content))
head(corp_nyn)

```

### Create Document Term Matrix (DTM)
Create DTM without English-specific processing.

```{r}

# Remove punctuation, and limit to terms larger than 4 characters.
dtm <- DocumentTermMatrix(corp_nyn, control = list(removePunctuation = TRUE, wordLengths = c(4, 999), stopwords = FALSE, removeNumbers = FALSE, stemming = FALSE, bounds = list(global = c(5, Inf))))

```


```{r}

# View sample from document term matrix.
inspect(dtm[1:10, 0:65])

```

### Remove sparse terms

```{r}

dtms <- removeSparseTerms(dtm, 0.99)
dim(dtm)
dim(dtms)

```


## Exploratory Data Analysis
### Identify top terms

```{r}

# Obtain top Nyankore terms from non-sparse matrix, and optionally view counts (occurences) per term.
top_terms_nyn <- dtms[[6]]
head(top_terms_nyn)
# view(as.matrix(dtms))

```


```{r}

# Sum non-sparse term occurences.
freq <- colSums(as.matrix(dtms))
length(freq)
freq[head(order(freq), 66)]

```

### Data Visualization
Visualize highest frequency terms in Nyankore messages content.


```{r}

# Create bar plot of top Nyankore terms.
plt <- barplot(freq[tail(order(freq), 20)], axes = T, cex.names = 0.65, horiz = F, col = c("gray"))

# Write plot to tiff file.
tiff('./nyn_freq_terms.tiff', width = 1024, height = 768, bg = 'white', pointsize = 13, antialias = 'cleartype', compression = 'none')
plot(1:10)
rect(1,5,3,7, col = 'white')
plt <- barplot(freq[tail(order(freq), 20)], axes = T, cex.names = 0.65, horiz = F, col = c("gray"))
dev.off()


```

### Clustering
Preliminary EDA by applying arbitrary clustering.


```{r}

# Create 10 k-means clusters.
kmeans10 <- kmeans(dtms, 10)
kw_with_cluster <- as.data.frame(cbind(messages_nyn_qa, Cluster = kmeans10$cluster))
cluster1 <- subset(kw_with_cluster, subset = Cluster == 1)
cluster2 <- subset(kw_with_cluster, subset = Cluster == 2)
cluster3 <- subset(kw_with_cluster, subset = Cluster == 3)
cluster4 <- subset(kw_with_cluster, subset = Cluster == 4)
cluster5 <- subset(kw_with_cluster, subset = Cluster == 5)
cluster6 <- subset(kw_with_cluster, subset = Cluster == 6)
cluster7 <- subset(kw_with_cluster, subset = Cluster == 7)
cluster8 <- subset(kw_with_cluster, subset = Cluster == 8)
cluster9 <- subset(kw_with_cluster, subset = Cluster == 9)
cluster10 <- subset(kw_with_cluster, subset = Cluster == 10)


```


```{r}

# View cluster 10 results.
head(cluster10,30)


```

### Data Analysis
Analyse highest frequency topics per cluster, limited to 10.


```{r}

# View top 10 terms per cluster, along with counts.
tail(sort(table(cluster1$topic)), 10)
tail(sort(table(cluster2$topic)), 10)
tail(sort(table(cluster3$topic)), 10)
tail(sort(table(cluster4$topic)), 10)
tail(sort(table(cluster5$topic)), 10)
tail(sort(table(cluster6$topic)), 10)
tail(sort(table(cluster7$topic)), 10)
tail(sort(table(cluster8$topic)), 10)
tail(sort(table(cluster9$topic)), 10)
tail(sort(table(cluster10$topic)), 10)


```


### Output results
Write csv files for further processing and analysis.


```{r}

# Export top terms in Nyankore messages.
write.csv(top_terms_nyn$Terms, 
          file = './top_terms_nyn.csv',
          row.names = F)

```


```{r}

# Export all Nyankore messages with row numbers, and columns for content, topic, and type (q or a).
write.csv(messages_nyn_qa, 
          file = './messages_nyn.csv',
          row.names = T)

```

```{r}

#Export non-sparse document term matrix of Nyankore terms.
write.csv(dtm[[6]]$Terms, 
          file = './dtms_nyn.csv',
          row.names = F)

```

# Preliminary Results
Data analysis shows the below top 20 out of 67 terms, including English translation, source cited, parts-of-speech, singular or plural, and rank. The full list of terms is ![here](/top_nyn_terms.xlsx).

 | Runyankole | English | Citation | Part-of-speech | Singular or Plural | Top rank
25 | kandi | and, again, moreover | manual | conjunction |  | 1
46 | nimbuza | """Nimbuza"" is Luganda slang for a small, informal gathering or hangout — often used to mean a casual meeting with friends, a short party, or chilling together." | GPT-5 mini | noun |  | 2
49 | ninyenda | I want | manual | enda (verb) |  | 3
18 | enkoko | hen(s), fowl(s) | manual |  |  | 4
52 | nyine | I have | manual | ine (verb) |  | 5
58 | omubazi | "Drug; medicine;
ointment" | manual | noun |  | 6
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

# Next steps
Curation of word and phrase list for training, and model creation for translation.