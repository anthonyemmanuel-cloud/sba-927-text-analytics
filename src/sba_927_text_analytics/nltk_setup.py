"""
Make sure the NLTK data files we need are on this computer.

NLTK keeps its "data" (word lists, trained taggers, etc.) separate from the
code. Each resource only needs to be downloaded ONCE. This module checks first
and downloads only what is missing (instructor tip: check before downloading).

Note: the lab PDF uses the OLD resource names ('punkt',
'averaged_perceptron_tagger', 'maxent_ne_chunker'). NLTK 3.9+ renamed them,
so this project uses the NEW names below.
"""

import nltk

# resource name -> where NLTK stores it
NLTK_RESOURCES = {
    "punkt_tab": "tokenizers/punkt_tab",                            # splits text into sentences/words
    "stopwords": "corpora/stopwords",                               # list of common words (the, and, is)
    "wordnet": "corpora/wordnet",                                   # dictionary used by the lemmatizer
    "averaged_perceptron_tagger_eng": "taggers/averaged_perceptron_tagger_eng",  # POS tagger
    "maxent_ne_chunker_tab": "chunkers/maxent_ne_chunker_tab",      # named entity recognizer
    "words": "corpora/words",                                       # English word list used by NER
    "vader_lexicon": "sentiment/vader_lexicon.zip",                 # rule-based sentiment word list
}


def is_downloaded(path):
    # Some resources (like wordnet) stay inside a .zip file after downloading,
    # so look for the folder AND for the .zip version.
    for candidate in (path, path + ".zip"):
        try:
            nltk.data.find(candidate)
            return True
        except LookupError:
            pass
    return False


def ensure_nltk_resources():
    for name, path in NLTK_RESOURCES.items():
        if not is_downloaded(path):  # already downloaded? then skip it
            print(f"Downloading NLTK resource: {name}")
            nltk.download(name, quiet=True)