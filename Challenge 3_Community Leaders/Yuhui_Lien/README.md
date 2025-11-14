# 📄 README.md: Agricultural Terminology Extraction (agricultural_terms_from_wiki.ipynb)

### 1. Executive Summary

This notebook, `agricultural_terms_from_wiki.ipynb`, is dedicated to **extracting a comprehensive glossary of agricultural terms** from a public Wikipedia source. The methodology employs the `requests` library for robust web page retrieval (including the use of a standard `User-Agent` header) and `BeautifulSoup` for efficient HTML parsing. The goal is to generate a clean, machine-readable list of terminology for use in other data science or NLP applications, such as enhancing keyword dictionaries for farmer question classification.

### Key Findings:

- **Successfully extracted 856 unique agricultural terms** from the specified Wikipedia glossary page.
- The extraction process targets the `<dt>` (definition term) HTML tag within the main body content, ensuring accurate capture of glossary entries.
- The extracted terms were cleaned (e.g., removing reference brackets `[]` and newline characters) and saved to a structured CSV file (`agricultural_terms.csv`).

---

### 2. Data

| Feature | Description | Status |
|--------|-------------|--------|
| **Source URL** | `https://en.wikipedia.org/wiki/Glossary_of_agriculture` | Used |
| **Data Extracted** | Agricultural Terms (List of Strings) | Processed |
| **Final Output** | `agricultural_terms.csv` | Created |
| **Data Size** | **856** unique terms | Extracted |

---

### 3. Methodology: Wikipedia Glossary Extraction (Web Scraping)

The process is broken down into three key steps:

#### A. Download and Request Handling

- **Library:** `requests`
- **Method:** `requests.get(url, headers=headers)`
- A standard `User-Agent` header was passed in the request to mimic a web browser and prevent potential blocking.
- Error handling (`response.raise_for_status()`) was implemented to detect and report issues with fetching the URL.

#### B. HTML Parsing

- **Library:** `BeautifulSoup`
- **Goal:** Convert the raw HTML content into a searchable object.

#### C. Extraction and Cleaning

- **Target Tag:** The function specifically looks for the `<dt>` tag inside the main content body (`id='bodyContent'`), as this tag typically holds the definition term in a Wikipedia glossary list.
- **Cleaning:**
    1. Extracts the raw text (`dt_tag.get_text()`).
    2. Removes any text following a newline character.
    3. Removes citation brackets (e.g., `[1]`, `[2]`) from the term.
- **Output:** The clean terms are stored in a Pandas DataFrame and exported to a CSV file.

### Core Python Code Snippet

```python
def extract_glossary_terms(url):
    # ... (header setup) ...
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    body_content = soup.find(id='bodyContent')
    
    if body_content:
        for dt_tag in body_content.find_all('dt'):
            term = dt_tag.get_text().strip()
            # Basic cleaning
            term_clean = term.split('\n')[0].split('[')[0].strip()
            # ... (append to list) ...
    return glossary_terms