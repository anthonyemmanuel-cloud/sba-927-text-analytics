"""
Requirement 7: Experiment with pre-trained language models.

A pre-trained model has already learned from huge amounts of text, so we
can use it right away without training it ourselves.

    spaCy (en_core_web_sm)         -> tokenization, POS tagging, NER
    Hugging Face Transformers:
      - DistilBERT tokenizer       -> how modern models split words ("subwords")
      - DistilBERT SST-2           -> sentiment (positive/negative ONLY)
      - Twitter-RoBERTa sentiment  -> sentiment (positive/negative/neutral)

The Hugging Face models download automatically the first time (a few hundred MB).
"""

SPACY_MODEL = "en_core_web_sm"
HF_TOKENIZER_MODEL = "distilbert/distilbert-base-uncased"
HF_SENTIMENT_MODELS = {
    "distilbert_sst2": "distilbert/distilbert-base-uncased-finetuned-sst-2-english",
    "twitter_roberta": "cardiffnlp/twitter-roberta-base-sentiment-latest",
}


# ---------------------------------------------------------------
# spaCy: tokenization, POS tagging and NER in one step
# ---------------------------------------------------------------
def load_spacy():
    import spacy  # imported here so the rest of the program loads quickly

    return spacy.load(SPACY_MODEL)


def spacy_analysis(nlp, text):
    doc = nlp(text)  # spaCy reads the whole text once and fills in everything
    return {
        "tokens": [token.text for token in doc],
        "pos": [(token.text, token.pos_) for token in doc if not token.is_punct],
        "entities": [(ent.text, ent.label_) for ent in doc.ents],
    }


# ---------------------------------------------------------------
# Hugging Face: subword tokenization
# ---------------------------------------------------------------
def load_hf_tokenizer():
    from transformers import AutoTokenizer

    return AutoTokenizer.from_pretrained(HF_TOKENIZER_MODEL)


def hf_tokenize(tokenizer, text):
    # Rare words get split into pieces; "##" means "this piece continues the word"
    return tokenizer.tokenize(text)


# ---------------------------------------------------------------
# Hugging Face: sentiment analysis
# ---------------------------------------------------------------
def load_hf_sentiment_pipelines():
    from transformers import pipeline

    return {name: pipeline("sentiment-analysis", model=model) for name, model in HF_SENTIMENT_MODELS.items()}


def hf_sentiment(classifier, texts):
    # Returns (label, score) for each text, with labels in lowercase
    # (e.g. "POSITIVE" -> "positive"). score = how sure the model is (0 to 1).
    outputs = classifier(texts)
    return [(output["label"].lower(), round(output["score"], 3)) for output in outputs]