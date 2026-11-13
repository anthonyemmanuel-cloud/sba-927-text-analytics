"""
SBA 927: Business Text Analytics with Natural Language Processing
Student: Anthony Emmanuel

Runs every requirement of the assessment and saves the results as Markdown
tables in the results/ folder (ready to copy into the report).

How to run (from the project folder):
    uv run sba-927-text-analytics                      # everything
    uv run sba-927-text-analytics --part preprocess    # Requirements 1-2
    uv run sba-927-text-analytics --part ner           # Requirements 3-4
    uv run sba-927-text-analytics --part sentiment     # Requirements 5-6 (needs GROQ_API_KEY)
    uv run sba-927-text-analytics --part pretrained    # Requirement 7 (downloads models)
"""

import argparse
import time
from pathlib import Path

from sba_927_text_analytics import ner_pos, preprocessing, pretrained, sentiment
from sba_927_text_analytics.nltk_setup import ensure_nltk_resources

PROJECT_FOLDER = Path(__file__).resolve().parents[2]
RESULTS_FOLDER = PROJECT_FOLDER / "results"


# ---------------------------------------------------------------
# Helpers for saving results
# ---------------------------------------------------------------
def md_table(headers, rows):
    # Build a Markdown table: | a | b |
    def clean(cell):
        return str(cell).replace("|", "\\|").replace("\n", " ")

    lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    lines += ["| " + " | ".join(clean(cell) for cell in row) + " |" for row in rows]
    return "\n".join(lines)


def save(filename, title, sections):
    RESULTS_FOLDER.mkdir(exist_ok=True)
    path = RESULTS_FOLDER / filename
    path.write_text(f"# {title}\n\n" + "\n\n".join(sections) + "\n", encoding="utf-8")
    print(f"Saved: results/{filename}")


def short(items, limit=12):
    # Show at most `limit` items so tables stay readable
    items = list(items)
    return ", ".join(map(str, items[:limit])) + (" ..." if len(items) > limit else "")


# ---------------------------------------------------------------
# Requirements 1 and 2
# ---------------------------------------------------------------
def run_preprocessing(dataset):
    print("\n=== Requirements 1-2: Tokenization, preprocessing, stemming, lemmatization ===")
    steps = [preprocessing.preprocess_steps(text) for text in dataset]
    processed_dataset = [step["no_stop_words"] for step in steps]

    # Step-by-step examples: line 1 (quote with a contraction) and line 5 (acronym V.I.K.I.)
    example_sections = []
    for number in (1, 5):
        example = steps[number - 1]
        example_sections.append(f"## Step-by-step example (line {number})")
        example_sections.append(md_table(["Step", "Result"], [
            ["Original", example["original"]],
            ["1. Remove noise", example["cleaned"]],
            ["2. Lowercase", example["lowercased"]],
            ["3. Tokenize", example["tokens"]],
            ["4. Remove punctuation", example["no_punctuation"]],
            ["5. Remove stop words", example["no_stop_words"]],
        ]))

    # Before and after for every line
    rows = []
    for number, (text, tokens) in enumerate(zip(dataset, processed_dataset), start=1):
        rows.append([number, text, tokens, f"{len(steps[number - 1]['tokens'])} -> {len(tokens)}"])
        print(f"Text {number}: {tokens}")

    # Stemming and lemmatization
    stem_rows, difference_rows = [], []
    for number, (text, tokens) in enumerate(zip(dataset, processed_dataset), start=1):
        stemmed, lemmatized = preprocessing.stem_and_lemmatize(tokens)
        pos_lemmas = preprocessing.pos_aware_lemmatize(text)
        stem_rows.append([number, tokens, stemmed, lemmatized, pos_lemmas])
        for word, stem, lemma, pos_lemma in zip(tokens, stemmed, lemmatized, pos_lemmas):
            if len({word, stem, lemma, pos_lemma}) > 1:
                difference_rows.append([word, stem, lemma, pos_lemma])

    unique_differences = list(dict.fromkeys(tuple(row) for row in difference_rows))
    save("01_preprocessing.md", "Requirement 1: Tokenization and preprocessing", [
        *example_sections,
        "## All lines", md_table(["#", "Original text", "Processed tokens", "Tokens before -> after"], rows),
    ])
    save("02_stemming_lemmatization.md", "Requirement 2: Stemming and lemmatization", [
        md_table(["#", "Tokens", "Stemmed (Porter)", "Lemmatized (lab version)", "Lemmatized (POS-aware)"], stem_rows),
        "## Words where the methods disagree",
        md_table(["Word", "Stem", "Lemma (noun only)", "Lemma (POS-aware)"], unique_differences),
    ])
    print(f"Words where stemming/lemmatization differ: {len(unique_differences)}")


# ---------------------------------------------------------------
# Requirements 3 and 4
# ---------------------------------------------------------------
def run_ner_pos(dataset):
    print("\n=== Requirements 3-4: Named Entity Recognition and POS tagging ===")
    ner_results_dataset = [ner_pos.named_entity_recognition(text) for text in dataset]
    pos_tags_dataset = [ner_pos.pos_tagging(text) for text in dataset]

    for number, ner_results in enumerate(ner_results_dataset, start=1):
        print(f"Named Entities in Text {number}: {ner_results}")

    entity_counts = ner_pos.count_entities(ner_results_dataset)
    pos_counts = ner_pos.count_pos_groups(pos_tags_dataset)

    save("03_named_entities.md", "Requirement 3: Named Entity Recognition (NLTK)", [
        md_table(["#", "Text", "Named entities (entity, label)"],
                 [[n, text, ents or "(none found)"] for n, (text, ents) in enumerate(zip(dataset, ner_results_dataset), start=1)]),
        "## Entity counts",
        md_table(["Entity", "Label", "Times found"], [[e, label, c] for (e, label), c in entity_counts.most_common()]),
    ])
    save("04_pos_tags.md", "Requirement 4: Part-of-Speech tagging (NLTK)", [
        md_table(["#", "POS tags (word, tag)"], [[n, tags] for n, tags in enumerate(pos_tags_dataset, start=1)]),
        "## Word types across the dataset",
        md_table(["Word type", "Count"], pos_counts.most_common()),
    ])
    print(f"Most common word types: {pos_counts.most_common(4)}")


# ---------------------------------------------------------------
# Requirements 5 and 6
# ---------------------------------------------------------------
def score_rows(name, golds, predictions):
    scores = sentiment.evaluate(golds, predictions)
    return [name, f"{scores['correct']}/{scores['total']}", f"{scores['accuracy']:.0%}", f"{scores['macro_f1']:.2f}"]


def run_sentiment(dataset):
    print("\n=== Requirements 5-6: Sentiment analysis with prompts ===")
    samples = sentiment.build_samples(dataset)
    golds = [s["gold"] for s in samples]

    llm = sentiment.create_llm()
    chains = sentiment.build_sentiment_chains(llm)
    start = time.perf_counter()
    results = sentiment.run_prompts(chains, samples)
    seconds = time.perf_counter() - start

    analyzer = sentiment.SentimentIntensityAnalyzer()
    vader = [sentiment.vader_label(s["text"], analyzer) for s in samples]

    # Requirement 5: save the prompts themselves
    save("05_sentiment_prompts.md", "Requirement 5: Prompts for sentiment analysis", [
        f"## Prompt {name}\n\n```\n{prompt.template}\n```" for name, prompt in sentiment.PROMPTS.items()
    ])

    # Requirement 6: results for every sample, and scores
    detail_rows = []
    for i, s in enumerate(samples):
        row = [s["id"], s["text"], s["gold"]]
        row += [results[name][i][0] for name in sentiment.PROMPTS]
        row.append(vader[i])
        detail_rows.append(row)

    def correct_in(prefix, predictions):
        # How many were right among the dataset lines (D) or business samples (B)?
        pairs = [(g, p) for s, g, p in zip(samples, golds, predictions) if s["id"].startswith(prefix)]
        return f"{sum(g == p for g, p in pairs)}/{len(pairs)}"

    summary = []
    for name in sentiment.PROMPTS:
        predictions = [label for label, _ in results[name]]
        summary.append(score_rows(f"Prompt {name}", golds, predictions)
                       + [correct_in("D", predictions), correct_in("B", predictions)])
    summary.append(score_rows("VADER (rule-based baseline)", golds, vader)
                   + [correct_in("D", vader), correct_in("B", vader)])

    def accuracy_of(name):
        return sentiment.evaluate(golds, [label for label, _ in results[name]])["accuracy"]

    best = max(sentiment.PROMPTS, key=accuracy_of)  # the prompt with the highest accuracy
    per_label = sentiment.evaluate(golds, [label for label, _ in results[best]])["per_label"]

    raw_rows = [[s["id"], raw] for s, (_, raw) in zip(samples, results["C_structured"])]
    mistakes = [[s["id"], s["text"], s["gold"], results[best][i][0], s["note"]]
                for i, s in enumerate(samples) if results[best][i][0] != s["gold"]]

    save("06_sentiment_results.md", "Requirement 6: Sentiment analysis results", [
        f"Model: `{sentiment.MODEL_NAME}` (Groq), temperature 0. Total time: {seconds:.1f} seconds.",
        "## Scores (overall, SBA927 dataset only, business samples only)",
        md_table(["Method", "Correct", "Accuracy", "Macro F1", "Dataset (12)", "Business (7)"], summary),
        f"## Precision / recall / F1 per label (best prompt: {best})",
        md_table(["Label", "Precision", "Recall", "F1", "Support"],
                 [[label, f"{v['precision']:.2f}", f"{v['recall']:.2f}", f"{v['f1']:.2f}", v["support"]]
                  for label, v in per_label.items()]),
        "## Every sample",
        md_table(["ID", "Text", "Correct label"] + [f"Prompt {n}" for n in sentiment.PROMPTS] + ["VADER"], detail_rows),
        f"## Mistakes made by the best prompt ({best})",
        md_table(["ID", "Text", "Correct", "Predicted", "Why it is tricky"], mistakes) if mistakes else "No mistakes.",
        "## Full answers from Prompt C (with confidence and reason)",
        md_table(["ID", "Model answer"], raw_rows),
        "## Labeling notes (why each correct label was chosen)",
        md_table(["ID", "Correct label", "Reason"], [[s["id"], s["gold"], s["note"]] for s in samples]),
    ])
    for row in summary:
        print(f"{row[0]}: {row[1]} correct ({row[2]})")


# ---------------------------------------------------------------
# Requirement 7
# ---------------------------------------------------------------
def run_pretrained(dataset):
    print("\n=== Requirement 7: Pre-trained language models ===")
    samples = sentiment.build_samples(dataset)
    golds = [s["gold"] for s in samples]
    texts = [s["text"] for s in samples]

    # spaCy vs NLTK for NER and POS
    nlp = pretrained.load_spacy()
    spacy_rows, pos_rows = [], []
    for number, text in enumerate(dataset, start=1):
        result = pretrained.spacy_analysis(nlp, text)
        nltk_entities = ner_pos.named_entity_recognition(text)
        spacy_rows.append([number, text, nltk_entities or "(none)", result["entities"] or "(none)"])
        pos_rows.append([number, short(result["pos"], 10)])
        print(f"Text {number} spaCy entities: {result['entities']}")

    # Hugging Face subword tokenization vs NLTK word tokenization
    tokenizer = pretrained.load_hf_tokenizer()
    token_rows = []
    for text in dataset[:4]:
        token_rows.append([text, preprocessing.word_tokenize(text), pretrained.hf_tokenize(tokenizer, text)])

    # Hugging Face sentiment models vs the correct labels
    classifiers = pretrained.load_hf_sentiment_pipelines()
    hf_results = {name: pretrained.hf_sentiment(clf, texts) for name, clf in classifiers.items()}
    detail_rows = [[s["id"], s["text"], s["gold"]] + [f"{hf_results[n][i][0]} ({hf_results[n][i][1]})" for n in hf_results]
                   for i, s in enumerate(samples)]
    summary = [score_rows(name, golds, [label for label, _ in hf_results[name]]) for name in hf_results]

    save("07_pretrained_models.md", "Requirement 7: Pre-trained language models", [
        "## NER: NLTK (rule/statistics based) vs spaCy (pre-trained model)",
        md_table(["#", "Text", "NLTK entities", "spaCy entities"], spacy_rows),
        "## POS tags from spaCy (first 10 words)",
        md_table(["#", "POS tags (word, universal tag)"], pos_rows),
        "## Tokenization: NLTK words vs Hugging Face subwords (DistilBERT)",
        md_table(["Text", "NLTK word_tokenize", "DistilBERT tokenizer"], token_rows),
        "## Sentiment: Hugging Face models vs the correct labels",
        md_table(["Model", "Correct", "Accuracy", "Macro F1"], summary),
        md_table(["ID", "Text", "Correct label"] + list(hf_results), detail_rows),
    ])
    for row in summary:
        print(f"{row[0]}: {row[1]} correct ({row[2]})")


# ---------------------------------------------------------------
# main(): the "front door" of the app
# ---------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="SBA 927 business text analytics")
    parser.add_argument("--part", choices=["all", "preprocess", "ner", "sentiment", "pretrained"], default="all")
    part = parser.parse_args().part

    ensure_nltk_resources()
    dataset = preprocessing.load_dataset()
    print(f"Loaded {len(dataset)} lines from data/SBA927.txt")

    if part in ("all", "preprocess"):
        run_preprocessing(dataset)
    if part in ("all", "ner"):
        run_ner_pos(dataset)
    if part in ("all", "sentiment"):
        run_sentiment(dataset)
    if part in ("all", "pretrained"):
        run_pretrained(dataset)


if __name__ == "__main__":
    main()