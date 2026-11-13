# Business Text Analytics with NLP

**SBA 927: Business Text Analytics: Natural Language Processing Techniques**
Per Scholas AI Prompt Engineering (2026-CAX-255) · Anthony Emmanuel

## What this project does

This project analyzes the text in `data/SBA927.txt` (12 lines about the movie *I, Robot*) plus 7 sample customer-feedback sentences, using the main NLP techniques a business data analyst needs:

| Requirement | Technique | Tool |
|---|---|---|
| 1 | Load the data, remove noise, lowercase, tokenize, remove punctuation and stop words | NLTK |
| 2 | Stemming (Porter) and lemmatization (WordNet, plus a POS-aware version) | NLTK |
| 3 | Named Entity Recognition (people, places, organizations) | NLTK |
| 4 | Part-of-Speech tagging (nouns, verbs, adjectives...) | NLTK |
| 5 | Three sentiment-analysis prompts: zero-shot, few-shot, structured | LangChain + Groq |
| 6 | Run the prompts on 19 labeled sentences and measure accuracy, precision, recall and F1, compared with a rule-based baseline (VADER) | LangChain + Groq, NLTK |
| 7 | Pre-trained models for tokenization, NER, POS and sentiment | spaCy, Hugging Face Transformers |

Every result is saved as a Markdown table in the `results/` folder.

## Project structure

```
data/SBA927.txt                   the dataset
src/sba_927_text_analytics/
    nltk_setup.py                 checks for NLTK data and downloads only what is missing
    preprocessing.py              Requirements 1-2
    ner_pos.py                    Requirements 3-4
    sentiment.py                  Requirements 5-6
    pretrained.py                 Requirement 7
    main.py                       runs everything and saves the results
tests/test_text_analytics.py      automated tests
results/                          output tables (created when you run the program)
```

## Updates from the lab PDF

| Lab PDF | This project | Why |
|---|---|---|
| `nltk.download('punkt')`, `'averaged_perceptron_tagger'`, `'maxent_ne_chunker'` | `punkt_tab`, `averaged_perceptron_tagger_eng`, `maxent_ne_chunker_tab` | NLTK 3.9+ renamed these resources; the old names cause `LookupError` |
| Downloads every time | Checks first, downloads only what is missing | Faster, and works offline after the first run |
| No noise-removal code | `clean_text()` removes special symbols and extra spaces, and keeps acronyms like V.I.K.I. | The requirements ask for noise removal |
| Lemmatizer treats every word as a noun | Added a POS-aware lemmatizer | "investigates" becomes "investigate" only when the lemmatizer knows it is a verb |
| Google Colab / Replit | VS Code + uv | The course setup; also allowed by the lab |

## How to install

```bash
uv sync
```

## How to set up the API key (for Requirements 5-6)

1. Get a free key at https://console.groq.com.
2. `cp .env.example .env`, then put your key in `.env`.

`.env` is in `.gitignore`, so it is never uploaded.

## How to run

```bash
uv run sba-927-text-analytics                      # everything
uv run sba-927-text-analytics --part preprocess    # Requirements 1-2
uv run sba-927-text-analytics --part ner           # Requirements 3-4
uv run sba-927-text-analytics --part sentiment     # Requirements 5-6 (needs the API key)
uv run sba-927-text-analytics --part pretrained    # Requirement 7 (downloads models the first time)
```

## How to run the tests

```bash
uv run pytest
```

The sentiment tests use a fake language model, so no API key or internet is needed.

## My results (real run, November 12, 2026)

### Sentiment analysis (19 labeled sentences)

| Method | Correct | Accuracy | Macro F1 | Dataset (12) | Business (7) |
|---|---|---|---|---|---|
| Prompt A: zero-shot | 15/19 | 79% | 0.78 | 9/12 | 6/7 |
| Prompt B: few-shot | 16/19 | 84% | 0.84 | 10/12 | 6/7 |
| Prompt C: structured | 16/19 | 84% | 0.80 | 10/12 | 6/7 |
| Twitter-RoBERTa (Hugging Face) | 14/19 | 74% | | | |
| VADER (rule-based baseline) | 8/19 | 42% | 0.39 | 3/12 | 5/7 |
| DistilBERT SST-2 (Hugging Face) | 6/19 | 32% | | | |

Prompts used `openai/gpt-oss-20b` on Groq at temperature 0.

### Key findings

- **Stop-word removal deletes negation.** "Sonny: I did not murder him!" becomes `['sonny', 'murder']`, so sentiment analysis must use the original text.
- **The POS-aware lemmatizer fixes verbs** ("investigates" to "investigate", "told" to "tell"); stemming creates non-words and wrong roots ("detective" to "detect").
- **NLTK NER relies on capital letters:** it labeled "Robot" (a movie title) as a PERSON and Sonny as a place (GPE) in one sentence. spaCy was more consistent but labeled "AI" and "V.I.K.I." as places.
- **The language-model prompts doubled VADER's accuracy** and caught sarcasm ("Great, another update that deletes all my settings") that VADER called positive.
- **The structured prompt fixed the hardest cases** (sarcasm in D1, anger in D10) but over-corrected on two others, so it tied with few-shot.
- **DistilBERT SST-2 has no neutral label,** so it could reach at most 9/19 on data that is mostly neutral: choose a model whose labels match the question.
- **All three prompts disagreed with my label for "The product works as described."** Correct labels are judgment calls; a second labeler would improve the evaluation.