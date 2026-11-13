"""
Automated tests for the SBA 927 text analytics project.

They check the NLP steps on small examples where we KNOW the right answer.
The language-model tests use a FAKE model, so they run without internet
or an API key.

Run them with:
    uv run pytest
"""

import pytest
from langchain_core.language_models.fake_chat_models import FakeListChatModel

from sba_927_text_analytics import ner_pos, preprocessing, pretrained, sentiment
from sba_927_text_analytics.nltk_setup import ensure_nltk_resources


@pytest.fixture(scope="session", autouse=True)
def nltk_data():
    # Download any missing NLTK data once, before the tests run
    ensure_nltk_resources()


# ---------- Requirement 1: loading and cleaning ----------

def test_dataset_has_12_lines():
    dataset = preprocessing.load_dataset()
    assert len(dataset) == 12
    assert dataset[0].startswith('"Detective Spooner')


def test_clean_text_removes_noise():
    assert preprocessing.clean_text("Great   product!!  @#$ 10/10") == "Great product!! 10 10"


def test_clean_text_keeps_acronyms():
    assert preprocessing.clean_text("V.I.K.I. serves") == "VIKI serves"


def test_preprocessing_lowercases_and_removes_stop_words_and_punctuation():
    tokens = preprocessing.tokenize_and_preprocess("The Robots ARE coming, and they are FAST!")
    assert tokens == ["robots", "coming", "fast"]


def test_stop_word_removal_also_removes_negation():
    # Important finding: "not" is a stop word, so the meaning flips
    assert preprocessing.tokenize_and_preprocess("Sonny: I did not murder him!") == ["sonny", "murder"]


# ---------- Requirement 2: stemming and lemmatization ----------

def test_stemming_and_lemmatization():
    stemmed, lemmatized = preprocessing.stem_and_lemmatize(["robots", "investigates", "eagerly"])
    assert stemmed == ["robot", "investig", "eagerli"]       # stems can be non-words
    assert lemmatized == ["robot", "investigates", "eagerly"]  # lemmas are real words


def test_pos_aware_lemmatization_handles_verbs():
    lemmas = preprocessing.pos_aware_lemmatize("Detective Spooner investigates the crime.")
    assert lemmas == ["detective", "spooner", "investigate", "crime"]


# ---------- Requirements 3 and 4: NER and POS ----------

def test_ner_finds_a_person():
    entities = ner_pos.named_entity_recognition("Dr. Susan Calvin plays a crucial role.")
    assert ("Susan Calvin", "PERSON") in entities


def test_pos_tagging_labels_words():
    tags = dict(ner_pos.pos_tagging("Sonny becomes a key figure."))
    assert tags["Sonny"] == "NNP"   # proper noun
    assert tags["becomes"] == "VBZ"  # verb


def test_count_pos_groups_skips_punctuation():
    counts = ner_pos.count_pos_groups([[("Sonny", "NNP"), ("runs", "VBZ"), ("!", ".")]])
    assert counts == {"Proper noun": 1, "Verb": 1}


# ---------- Requirements 5 and 6: sentiment prompts ----------

def test_samples_have_valid_labels():
    samples = sentiment.build_samples(preprocessing.load_dataset())
    assert len(samples) == 19  # 12 dataset lines + 7 business samples
    assert all(s["gold"] in sentiment.LABELS for s in samples)


def test_every_prompt_has_a_text_blank():
    for prompt in sentiment.PROMPTS.values():
        assert prompt.input_variables == ["text"]


@pytest.mark.parametrize("answer, expected", [
    ("Positive", "positive"),
    ("Sentiment: negative\nConfidence: high\nReason: The customer is angry.", "negative"),
    ("The sentiment is neutral.", "neutral"),
    ("I am not sure.", "unknown"),
])
def test_parse_label(answer, expected):
    assert sentiment.parse_label(answer) == expected


def test_sentiment_chains_with_fake_model():
    fake_llm = FakeListChatModel(responses=["positive", "negative", "Sentiment: neutral\nConfidence: high\nReason: A fact."])
    chains = sentiment.build_sentiment_chains(fake_llm)
    samples = [{"text": "Some text"}]
    results = sentiment.run_prompts(chains, samples)
    assert [results[name][0][0] for name in sentiment.PROMPTS] == ["positive", "negative", "neutral"]


def test_evaluate_scores():
    scores = sentiment.evaluate(["positive", "negative", "neutral", "neutral"],
                                ["positive", "neutral", "neutral", "neutral"])
    assert scores["correct"] == 3
    assert scores["accuracy"] == 0.75
    assert scores["per_label"]["neutral"]["recall"] == 1.0
    assert scores["per_label"]["negative"]["recall"] == 0.0


def test_vader_baseline():
    assert sentiment.vader_label("Best purchase I've made this year!") == "positive"
    assert sentiment.vader_label("Customer service was rude and unhelpful.") == "negative"


# ---------- Requirement 7: pre-trained models ----------

def test_spacy_finds_entities_and_pos():
    nlp = pretrained.load_spacy()
    result = pretrained.spacy_analysis(nlp, "Dr. Susan Calvin works in Chicago.")
    assert ("Susan Calvin", "PERSON") in result["entities"]
    assert ("works", "VERB") in result["pos"]


def test_hf_sentiment_formats_labels():
    def fake_classifier(texts):
        return [{"label": "POSITIVE", "score": 0.99871} for _ in texts]

    assert pretrained.hf_sentiment(fake_classifier, ["Great!"]) == [("positive", 0.999)]