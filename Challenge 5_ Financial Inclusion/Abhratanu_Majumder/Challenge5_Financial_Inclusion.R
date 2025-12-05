



questions <- readr::read_csv(
  "C:/Users/am488/Downloads/Datakind_Data.csv",
  n_max = 1000000
)


library(tidyverse)
library(janitor)
library(textclean)
library(lubridate)
library(tidytext)
library(stringr)
library(purrr)


questions <- questions %>% clean_names()
glimpse(questions)

questions <- questions %>%
  mutate(
    question_text_clean = question_content %>%
      replace_non_ascii() %>%
      tolower() %>%
      str_squish()
  )

fin_terms <- c(
  "loan", "loans", "credit", "borrow", "debt", "microfinance",
  "market", "price", "prices", "sell", "selling", "buy", "cost",
  "income", "profit", "earn", "money",
  "saving", "savings", "sacco", "cooperative", "coop"
)


questions <- questions %>%
  mutate(
    is_financial = str_detect(
      question_text_clean,
      str_c(fin_terms, collapse = "|")
    )
  )

questions %>% 
  count(is_financial) %>%
  mutate(prop = n / sum(n))

questions <- questions %>%
  mutate(
    year = year(question_sent),
    month = month(question_sent),
    month_name = month(question_sent, label = TRUE, abbr = TRUE)
  )



monthly_financial <- questions %>%
  filter(is_financial) %>%
  count(
    question_user_country_code,
    year,
    month,
    month_name,
    name = "n_fin"
  )

library(ggplot2)

ggplot(monthly_financial,
       aes(x = month_name, y = n_fin,
           group = year, colour = factor(year))) +
  geom_line(linewidth = 1.2) +
  geom_point(size = 3) +
  facet_wrap(~ question_user_country_code, scales = "free_y") +
  scale_colour_brewer(palette = "Dark2") +
  labs(
    title = "Seasonal Trends in Financial Questions",
    subtitle = "Financial-related questions by month, year, and country",
    x = "Month",
    y = "Number of Financial Questions",
    colour = "Year"
  ) +
  theme_minimal(base_size = 14) +
  theme(
    plot.title = element_text(face = "bold", size = 16),
    axis.text.x = element_text(angle = 45, hjust = 1),
    strip.text = element_text(face = "bold")
  )


fin_words <- questions %>%
  filter(is_financial) %>%
  unnest_tokens(word, question_text_clean) %>%
  anti_join(stop_words, by = "word") %>%
  count(word, sort = TRUE)

head(fin_words, 20)


categories <- list(
  market  = c("market", "price", "prices", "sell", "selling", "buy", "buyer", "cost"),
  credit  = c("loan", "loans", "credit", "borrow", "debt", "microfinance"),
  savings = c("saving", "savings", "sacco", "cooperative", "coop"),
  income  = c("income", "profit", "earn", "earning", "money")
)

assign_fin_category <- function(text) {
  text <- tolower(text)
  
  if (str_detect(text, str_c(categories$market,  collapse = "|"))) return("market_prices")
  if (str_detect(text, str_c(categories$credit,  collapse = "|"))) return("credit_loans")
  if (str_detect(text, str_c(categories$savings, collapse = "|"))) return("savings_coops")
  if (str_detect(text, str_c(categories$income,  collapse = "|"))) return("income_profit")
  
  return("other_financial")
}


questions <- questions %>%
  mutate(
    fin_category = if_else(
      is_financial,
      purrr::map_chr(question_text_clean, assign_fin_category),
      NA_character_
    )
  )


questions %>%
  filter(is_financial) %>%
  count(fin_category, sort = TRUE)


install.packages("wordcloud")
library(wordcloud)
library(RColorBrewer)


market_words <- questions %>%
  filter(fin_category == "market_prices") %>%
  unnest_tokens(word, question_text_clean) %>%
  anti_join(stop_words, by = "word") %>%
  count(word, sort = TRUE)

wordcloud(
  words = market_words$word,
  freq = market_words$n,
  max.words = 200,
  colors = brewer.pal(8, "Dark2")
)



income_words <- questions %>%
  filter(fin_category == "income_profit") %>%
  unnest_tokens(word, question_text_clean) %>%
  anti_join(stop_words, by = "word") %>%
  count(word, sort = TRUE)

wordcloud(
  words = income_words$word,
  freq = income_words$n,
  max.words = 200,
  colors = brewer.pal(8, "Dark2")
)


credit_words <- questions %>%
  filter(fin_category == "credit_loans") %>%
  unnest_tokens(word, question_text_clean) %>%
  anti_join(stop_words, by = "word") %>%
  count(word, sort = TRUE)

wordcloud(
  words = credit_words$word,
  freq = credit_words$n,
  max.words = 200,
  colors = brewer.pal(8, "Dark2")
)



savings_words <- questions %>%
  filter(fin_category == "savings_coops") %>%
  unnest_tokens(word, question_text_clean) %>%
  anti_join(stop_words, by = "word") %>%
  count(word, sort = TRUE)

wordcloud(
  words = savings_words$word,
  freq = savings_words$n,
  max.words = 300,
  colors = brewer.pal(8, "Dark2")
)



fin_country_category <- questions %>%
  filter(is_financial) %>%
  count(question_user_country_code, fin_category, sort = TRUE)

fin_country_category



ggplot(fin_country_category,
       aes(x = question_user_country_code, y = n, fill = fin_category)) +
  geom_col(position = "dodge") +
  labs(
    title = "Financial Question Categories by Country",
    x = "Country",
    y = "Count",
    fill = "Financial Category"
  ) +
  theme_minimal()


fin_by_crop <- questions %>%
  filter(is_financial, !is.na(question_topic)) %>%
  count(question_topic, sort = TRUE)

head(fin_by_crop, 20)


library(ggplot2)
library(viridis)

unique_topics <- questions %>%
  filter(!is.na(question_topic)) %>%
  distinct(question_topic) %>%
  arrange(question_topic)

unique_topics

animal_terms <- c(
  "bee", "camel", "cattle", "chicken", "fish",
  "goat", "pig", "poultry", "rabbit", "sheep",
  "turkey", "tilapia"
)

non_crop_terms <- c(
  "acacia", "bamboo", "eucalyptus",   # trees
  "nightshade", "black-nightshade",   # weeds
  "caliandra", "collard-greens",       # general categories
  "plant", "crop", "tree", "vegetable" # generic
)

remove_list <- c(animal_terms, non_crop_terms)

clean_crop_topics <- crop_topics[!(crop_topics %in% remove_list)]

clean_crop_topics




questions_clean_crops <- questions %>%
  filter(is_financial) %>%                      # keep only financial questions
  filter(question_topic %in% clean_crop_topics) # keep only real crops

fin_by_crop_clean <- questions_clean_crops %>%
  count(question_topic, sort = TRUE)


head(fin_by_crop_clean, 20)

library(ggplot2)
library(viridis)

top_crops_clean <- fin_by_crop_clean %>% 
  slice_max(n, n = 20)  # Top 20 crops

ggplot(top_crops_clean,
       aes(x = reorder(question_topic, n), 
           y = n, 
           fill = n)) +
  geom_col() +
  scale_fill_viridis(option = "C", direction = -1) +
  coord_flip() +
  labs(
    title = "Top Crops Mentioned in Financial Questions (Cleaned Crop List)",
    x = "Crop",
    y = "Financial Question Count",
    fill = "Count"
  ) +
  theme_minimal(base_size = 14) +
  theme(plot.title = element_text(face = "bold"))

fin_by_crop_category <- questions %>%
  filter(is_financial, question_topic %in% clean_crop_topics) %>%
  count(question_topic, fin_category, sort = TRUE)


top10 <- fin_by_crop_clean %>%
  slice_max(n, n = 10) %>%
  pull(question_topic)

fin_by_crop_top10 <- fin_by_crop_category %>%
  filter(question_topic %in% top10)

ggplot(fin_by_crop_top10,
       aes(x = fin_category, y = question_topic, size = n, colour = fin_category)) +
  geom_point(alpha = 0.85) +
  scale_size(range = c(4, 18)) +
  scale_colour_brewer(palette = "Dark2") +
  labs(
    title = "Financial Question Categories for Top 10 Crops",
    x = "Financial Category",
    y = "Crop",
    size = "Count"
  ) +
  theme_minimal(base_size = 14) +
  theme(
    axis.text.y = element_text(size = 12),
    legend.position = "right"
  )



ggplot(fin_by_crop_top10,
       aes(x = fin_category, y = n, fill = fin_category)) +
  geom_col() +
  facet_wrap(~ question_topic, scales = "free_y") +
  scale_fill_brewer(palette = "Dark2") +
  labs(
    title = "Financial Question Types for Each Top Crop",
    x = "Category",
    y = "Count"
  ) +
  theme_minimal(base_size = 14) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))


# Seasonality
ggplot(monthly_trends,
       aes(x = month_name, y = prop, group = fin_category, colour = fin_category)) +
  
  geom_line(linewidth = 1.8, alpha = 0.9) +
  geom_point(size = 4, stroke = 0.5) +
  
  facet_wrap(~ question_user_country_code, scales = "free_y") +
  
  scale_y_continuous(labels = scales::percent_format(accuracy = 1)) +
  scale_colour_brewer(palette = "Dark2") +
  
  labs(
    title = "Seasonality of Financial Question Types",
    subtitle = "Share of each financial category across months, by country",
    x = "Month",
    y = "Share of Financial Questions",
    colour = "Financial Category"
  ) +
  
  theme_minimal(base_size = 15) +
  theme(
    plot.title = element_text(face = "bold", size = 20),
    plot.subtitle = element_text(size = 14, margin = margin(b = 10)),
    axis.text.x = element_text(angle = 45, hjust = 1, size = 12),
    axis.text.y = element_text(size = 12),
    strip.background = element_rect(fill = "#f2f2f2", colour = NA),
    strip.text = element_text(face = "bold", size = 14),
    legend.position = "bottom"
  )


# Top Financial Terms by Category (Top 8 per category)

library(tidytext)
library(forcats)
library(ggplot2)
library(dplyr)

# Create word counts per category
category_words <- questions %>%
  filter(is_financial) %>%
  unnest_tokens(word, question_text_clean) %>%
  anti_join(stop_words, by = "word") %>%
  count(fin_category, word, sort = TRUE)

# Choose top 8 terms per category
top_terms_by_category <- category_words %>%
  group_by(fin_category) %>%
  slice_max(n, n = 8) %>%
  ungroup()

# Plot
ggplot(top_terms_by_category,
       aes(x = fct_reorder(word, n), y = n, fill = fin_category)) +
  geom_col(show.legend = FALSE) +
  coord_flip() +
  facet_wrap(~ fin_category, scales = "free_y") +
  scale_fill_brewer(palette = "Dark2") +
  labs(
    title = "Top Financial Terms Within Each Financial Category",
    subtitle = "Top 8 frequently used terms per financial category",
    x = "Term",
    y = "Frequency"
  ) +
  theme_minimal(base_size = 14) +
  theme(
    plot.title = element_text(face = "bold", size = 18),
    strip.text = element_text(face = "bold"),
    axis.text.y = element_text(size = 12)
  )

questions_clean_crops <- questions %>%
  filter(is_financial) %>%
  filter(question_topic %in% clean_crop_topics)


# Count occurrences for valid crops
crop_freq <- questions_clean_crops %>%
  count(question_topic, sort = TRUE)

# Select top 15
top_15_crops <- crop_freq %>%
  slice_max(n, n = 15) %>%
  pull(question_topic)

# Count occurrences for valid crops
crop_freq <- questions_clean_crops %>%
  count(question_topic, sort = TRUE)

# Select top 15
top_15_crops <- crop_freq %>%
  slice_max(n, n = 15) %>%
  pull(question_topic)

fin_crop_matrix <- questions_clean_crops %>%
  filter(question_topic %in% top_15_crops) %>%
  count(question_topic, fin_category, sort = TRUE)

library(ggplot2)

ggplot(fin_crop_matrix,
       aes(x = fin_category, y = question_topic, fill = n)) +
  geom_tile(color = "white", linewidth = 0.8) +
  scale_fill_distiller(palette = "YlOrRd", direction = 1) +
  labs(
    title = "Financial Questions by Crop and Financial Category",
    subtitle = "Top 15 most frequently mentioned crops (financial questions only)",
    x = "Financial Category",
    y = "Crop",
    fill = "Count"
  ) +
  theme_minimal(base_size = 15) +
  theme(
    plot.title = element_text(face = "bold", size = 18),
    strip.text = element_text(face = "bold"),
    axis.text.x = element_text(angle = 45, hjust = 1),
    panel.grid = element_blank()
  )












model_data <- questions %>%
  select(question_text_clean, is_financial) %>%
  filter(!is.na(question_text_clean))

table(model_data$is_financial)


set.seed(123)

train_index <- sample(nrow(model_data), 0.8 * nrow(model_data))

train_data <- model_data[train_index, ]
test_data  <- model_data[-train_index, ]

nrow(train_data)
nrow(test_data)
head(train_data)



install.packages("text2vec")
library(text2vec)


it_train <- itoken(
  train_data$question_text_clean,
  tokenizer = word_tokenizer,
  progressbar = TRUE
)

vocab <- create_vocabulary(it_train)
vocab <- prune_vocabulary(vocab, term_count_min = 5)  # remove very rare words


vectorizer <- vocab_vectorizer(vocab)


dtm_train <- create_dtm(it_train, vectorizer)

it_test <- itoken(
  test_data$question_text_clean,
  tokenizer = word_tokenizer,
  progressbar = TRUE
)

dtm_test <- create_dtm(it_test, vectorizer)

dim(dtm_train)
dim(dtm_test)


y_train <- as.numeric(train_data$is_financial)
y_test  <- as.numeric(test_data$is_financial)

table(y_train)
table(y_test)


library(glmnet)

glmnet_model <- cv.glmnet(
  x = dtm_train,
  y = y_train,
  family = "binomial",
  alpha = 1,     # LASSO
  nfolds = 5,
  type.measure = "class"
)

