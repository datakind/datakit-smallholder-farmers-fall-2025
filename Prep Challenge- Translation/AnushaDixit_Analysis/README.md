# Bridging Languages: Translating Farmer Conversations

This project focuses on translating farmer questions from Swahili, Luganda, and Runyankole (Nyn) into clear, usable English to enable better data-driven insights for agricultural support platforms like Producers Direct.
The pipeline cleans, translates, and analyzes farmer messages to build a glossary of key agricultural terms and support topic modeling and cluster analysis.

## Project Overview
- Developed a translation workflow for underrepresented African languages using open-source models.
- Handled edge cases where English text appeared as missing (NaN) in translation outputs.
- Cleaned and tokenized translated text to extract frequent agricultural terms.
- Generated a Farmer Glossary highlighting commonly discussed topics like crops, livestock, and farming practices.

## Tech Stack

- Python, Pandas, Regex, NLTK, Transformers / NLLB Models
- Libraries: transformers, pandas, nltk, re, collections.Counter

## Outputs

- translated_en: English translations of farmer questions
- translated_clean: Cleaned version for text analysis
- farmer_glossary: Top keywords and frequencies
- Build a topic model using LDA on translated text
- Expand the glossary with semantic clustering for similar agricultural terms
