"""
Requirements 3 and 4: Named Entity Recognition (NER) and Part-of-Speech (POS) tagging.

Both run on the ORIGINAL sentences (not the preprocessed tokens), because they
need capital letters, punctuation and word order to work well.
"""

from collections import Counter

from nltk import ne_chunk, pos_tag
from nltk.tokenize import sent_tokenize, word_tokenize


# ---------------------------------------------------------------
# Requirement 3: Named Entity Recognition (NER)
# ---------------------------------------------------------------
def tokenize_into_sentences(text):
    return sent_tokenize(text)


def part_of_speech_tagging(sentences):
    return [pos_tag(word_tokenize(sentence)) for sentence in sentences]


def extract_named_entities(pos_tagged_sentences):
    named_entities = []
    for sentence in pos_tagged_sentences:
        tree = ne_chunk(sentence)
        for subtree in tree:
            if hasattr(subtree, "label"):  # this piece of the tree is a named entity
                entity = " ".join(word for word, tag in subtree.leaves())
                named_entities.append((entity, subtree.label()))
    return named_entities


def named_entity_recognition(text):
    sentences = tokenize_into_sentences(text)
    pos_tags = part_of_speech_tagging(sentences)
    return extract_named_entities(pos_tags)


# ---------------------------------------------------------------
# Requirement 4: Part-of-Speech (POS) tagging
# ---------------------------------------------------------------
def pos_tagging(text):
    pos_tags = []
    for sentence in sent_tokenize(text):
        pos_tags.extend(pos_tag(word_tokenize(sentence)))
    return pos_tags


# Plain-English names for the most common POS tags
POS_GROUPS = {
    "NN": "Noun", "NNS": "Noun", "NNP": "Proper noun", "NNPS": "Proper noun",
    "VB": "Verb", "VBD": "Verb", "VBG": "Verb", "VBN": "Verb", "VBP": "Verb", "VBZ": "Verb",
    "JJ": "Adjective", "JJR": "Adjective", "JJS": "Adjective",
    "RB": "Adverb", "RBR": "Adverb", "RBS": "Adverb",
    "PRP": "Pronoun", "PRP$": "Pronoun",
    "DT": "Determiner", "IN": "Preposition", "CC": "Conjunction",
}


def count_pos_groups(pos_tags_dataset):
    # Count nouns, verbs, adjectives... across the whole dataset
    counts = Counter()
    for pos_tags in pos_tags_dataset:
        for word, tag in pos_tags:
            if word.isalpha():  # skip punctuation
                counts[POS_GROUPS.get(tag, "Other")] += 1
    return counts


def count_entities(ner_results_dataset):
    # How often each entity (name, place...) appears, with its label
    return Counter(entity for ner_results in ner_results_dataset for entity in ner_results)