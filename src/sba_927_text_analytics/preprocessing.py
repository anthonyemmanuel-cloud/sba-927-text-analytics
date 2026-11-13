"""
Requirements 1 and 2: Text Data Processing.

    1. Tokenization and preprocessing:
         load the dataset -> remove noise -> lowercase -> tokenize
         -> remove punctuation -> remove stop words
    2. Stemming and lemmatization of the preprocessed tokens.
"""

import re
import string
from pathlib import Path

from nltk import pos_tag
from nltk.corpus import stopwords, wordnet
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize

# The project folder (two levels up from this file: src/sba_927_text_analytics/)
PROJECT_FOLDER = Path(__file__).resolve().parents[2]
DATASET_PATH = PROJECT_FOLDER / "data" / "SBA927.txt"


# ---------------------------------------------------------------
# Load the dataset
# ---------------------------------------------------------------
def load_dataset(file_path=DATASET_PATH):
    # Read the file and keep one entry per line, skipping blank lines
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.read().splitlines()
    return [line.strip() for line in lines if line.strip()]


# ---------------------------------------------------------------
# Requirement 1: Clean the text data
# ---------------------------------------------------------------
def clean_text(text):
    # Remove noise:
    # 1. Join acronyms like "V.I.K.I." into "VIKI" so the name isn't lost
    #    (otherwise the dots split it and isalpha() throws it away).
    text = re.sub(
        r"\b(?:[A-Za-z]\.){2,}",
        lambda match: match.group(0).replace(".", ""),
        text,
    )
    # 2. Replace special symbols (anything that is not a letter, number,
    #    space, or common punctuation) with a space.
    text = re.sub(r"[^A-Za-z0-9\s.,!?'\"():;-]", " ", text)
    # 3. Collapse extra whitespace (tabs, double spaces) into one space.
    text = re.sub(r"\s+", " ", text).strip()
    return text


def preprocess_steps(text):
    # Show EVERY cleaning step separately (useful for the report).
    stop_words = set(stopwords.words("english"))
    punctuation = set(string.punctuation)

    cleaned = clean_text(text)                                   # remove noise
    lowercased = cleaned.lower()                                 # normalize
    tokens = word_tokenize(lowercased)                           # tokenize
    no_punctuation = [t for t in tokens if t not in punctuation and t.isalpha()]  # remove punctuation
    no_stop_words = [t for t in no_punctuation if t not in stop_words]            # remove stop words

    return {
        "original": text,
        "cleaned": cleaned,
        "lowercased": lowercased,
        "tokens": tokens,
        "no_punctuation": no_punctuation,
        "no_stop_words": no_stop_words,
    }


def tokenize_and_preprocess(text):
    # The lab's function, with noise removal added at the start.
    return preprocess_steps(text)["no_stop_words"]


# ---------------------------------------------------------------
# Requirement 2: Stemming and lemmatization
# ---------------------------------------------------------------
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()


def stem_and_lemmatize(tokens):
    # The lab's version: the lemmatizer treats every word as a NOUN.
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return stemmed_tokens, lemmatized_tokens


def to_wordnet_pos(treebank_tag):
    # Convert a POS tag like 'VBZ' into the format WordNet understands.
    if treebank_tag.startswith("J"):
        return wordnet.ADJ
    if treebank_tag.startswith("V"):
        return wordnet.VERB
    if treebank_tag.startswith("R"):
        return wordnet.ADV
    return wordnet.NOUN


def pos_aware_lemmatize(text):
    # Improvement: tell the lemmatizer each word's part of speech,
    # so verbs are handled too ("investigates" -> "investigate").
    # We tag the words INSIDE their sentence (before removing stop words),
    # because a tagger needs the surrounding words to guess correctly.
    stop_words = set(stopwords.words("english"))
    words = preprocess_steps(text)["no_punctuation"]
    return [
        lemmatizer.lemmatize(word, to_wordnet_pos(tag))
        for word, tag in pos_tag(words)
        if word not in stop_words
    ]