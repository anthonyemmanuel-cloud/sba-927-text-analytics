"""
Requirements 5 and 6: Sentiment analysis with prompts, and evaluating the results.

    5. Create prompts that ask a language model whether a text is
       positive, negative, or neutral.
    6. Run the prompts on sample sentences, compare the answers with the
       correct labels, and measure how accurate and effective they are.

We also run VADER (a rule-based tool from NLTK) as a simple baseline,
so we can see whether the language model actually does better.
"""

import os
import re
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from nltk.sentiment import SentimentIntensityAnalyzer

PROJECT_FOLDER = Path(__file__).resolve().parents[2]
MODEL_NAME = "openai/gpt-oss-20b"
LABELS = ["positive", "negative", "neutral"]


# ---------------------------------------------------------------
# Labeled sample sentences ("gold" labels = the answer we expect)
# ---------------------------------------------------------------
# 1) The 12 lines of the SBA927 dataset. Most are plot descriptions, so many
#    are NEUTRAL. Some are hard on purpose (sarcasm, mixed opinions).
DATASET_LABELS = [
    ("negative", "Sarcastic, frustrated tone ('I told you so' isn't enough)."),
    ("neutral", "Plot summary; 'threat' describes the story, not an opinion."),
    ("neutral", "Reports that fans disagree; no opinion of its own."),
    ("neutral", "A confident statement, but not positive or negative."),
    ("negative", "Describes a 'sinister' plan."),
    ("positive", "Viewers 'appreciate' the film."),
    ("neutral", "A line of dialogue with no clear feeling."),
    ("neutral", "Describes a character's role."),
    ("neutral", "Raises a question; no opinion."),
    ("negative", "An angry denial of murder."),
    ("neutral", "Describes the investigation."),
    ("neutral", "Mixed: some viewers like the ending, others speculate."),
]

# 2) Business-style customer feedback (this lab is about BUSINESS text).
BUSINESS_SAMPLES = [
    ("The checkout was fast and the support team fixed my issue in minutes.", "positive", "Clear praise."),
    ("My package arrived two weeks late and nobody answered my emails.", "negative", "Clear complaint."),
    ("The order was delivered on Tuesday.", "neutral", "Just a fact."),
    ("Great, another update that deletes all my settings. Just what I needed.", "negative", "Sarcasm: positive words, negative meaning."),
    ("Customer service was rude and unhelpful.", "negative", "Clear complaint."),
    ("Best purchase I've made this year!", "positive", "Clear praise."),
    ("The product works as described.", "neutral", "Factual; meets expectations."),
]


def build_samples(dataset):
    # Combine the dataset lines and the business samples into one labeled list
    if len(dataset) != len(DATASET_LABELS):
        raise ValueError(f"Expected {len(DATASET_LABELS)} dataset lines, found {len(dataset)}. Check data/SBA927.txt.")
    samples = []
    for number, (text, (gold, note)) in enumerate(zip(dataset, DATASET_LABELS), start=1):
        samples.append({"id": f"D{number}", "source": "SBA927 dataset", "text": text, "gold": gold, "note": note})
    for number, (text, gold, note) in enumerate(BUSINESS_SAMPLES, start=1):
        samples.append({"id": f"B{number}", "source": "Customer feedback", "text": text, "gold": gold, "note": note})
    return samples


# ---------------------------------------------------------------
# Requirement 5: Prompts for sentiment analysis
# Three prompts, from simple to detailed, so we can compare them.
# ---------------------------------------------------------------
PROMPTS = {
    # Prompt A: zero-shot = just ask, no examples
    "A_zero_shot": PromptTemplate.from_template(
        "Classify the sentiment of the following text as positive, negative, or neutral.\n"
        "Answer with one word.\n\n"
        "Text: {text}"
    ),
    # Prompt B: few-shot = give a few solved examples first
    "B_few_shot": PromptTemplate.from_template(
        "Classify the sentiment of the text as positive, negative, or neutral.\n\n"
        "Text: I love how easy this app is to use.\nSentiment: positive\n\n"
        "Text: The refund still hasn't arrived after a month.\nSentiment: negative\n\n"
        "Text: The store opens at 9 AM.\nSentiment: neutral\n\n"
        "Text: {text}\nSentiment:"
    ),
    # Prompt C: role + clear definitions + rules for hard cases + exact output format
    "C_structured": PromptTemplate.from_template(
        "You are a customer insights analyst. Classify the overall sentiment the WRITER "
        "or SPEAKER expresses in the text.\n\n"
        "Definitions:\n"
        "- positive: praise, satisfaction, or approval\n"
        "- negative: complaints, frustration, anger, or disapproval (including sarcasm)\n"
        "- neutral: facts, descriptions, questions, or a balanced mix of opinions\n\n"
        "Rules:\n"
        "- Judge the writer's attitude, not whether the topic is good or bad news.\n"
        "- Watch for sarcasm: positive words can carry a negative meaning.\n\n"
        "Reply in EXACTLY this format:\n"
        "Sentiment: <positive, negative, or neutral>\n"
        "Confidence: <low, medium, or high>\n"
        "Reason: <one short sentence>\n\n"
        "Text: {text}"
    ),
}


def create_llm():
    # Load the Groq API key from .env (never put the key in the code!)
    load_dotenv(PROJECT_FOLDER / ".env")
    if not os.getenv("GROQ_API_KEY"):
        raise SystemExit(
            "Missing GROQ_API_KEY. Create a file named .env in the project "
            "folder containing: GROQ_API_KEY=your-key-here"
        )
    from langchain_groq import ChatGroq  # imported here so tests don't need it

    # temperature=0 -> consistent answers; max_retries=5 -> wait and retry on rate limits;
    # reasoning_effort="low" -> faster, fewer tokens
    return ChatGroq(model=MODEL_NAME, temperature=0, max_retries=5, reasoning_effort="low")


def build_sentiment_chains(llm):
    # One chain per prompt: prompt -> LLM -> plain text
    return {name: prompt | llm | StrOutputParser() for name, prompt in PROMPTS.items()}


def parse_label(response):
    # Pull "positive"/"negative"/"neutral" out of the model's answer.
    text = response.lower()
    match = re.search(r"sentiment:\s*(positive|negative|neutral)", text)  # Prompt C format
    if match:
        return match.group(1)
    match = re.search(r"\b(positive|negative|neutral)\b", text)          # first label word
    return match.group(1) if match else "unknown"


def run_prompts(chains, samples):
    # Run every prompt on every sample. Returns {prompt_name: [(label, raw_answer), ...]}
    results = {}
    for name, chain in chains.items():
        print(f"Running prompt {name} on {len(samples)} samples...")
        answers = []
        for sample in samples:
            raw = chain.invoke({"text": sample["text"]}).strip()
            answers.append((parse_label(raw), raw))
        results[name] = answers
    return results


# ---------------------------------------------------------------
# Baseline: VADER (rule-based, no AI model)
# ---------------------------------------------------------------
def vader_label(text, analyzer=None):
    analyzer = analyzer or SentimentIntensityAnalyzer()
    compound = analyzer.polarity_scores(text)["compound"]  # score from -1 to +1
    if compound >= 0.05:
        return "positive"
    if compound <= -0.05:
        return "negative"
    return "neutral"


# ---------------------------------------------------------------
# Requirement 6: Measuring accuracy
# ---------------------------------------------------------------
def evaluate(golds, predictions):
    # Accuracy plus precision, recall and F1 for each label.
    #   precision: when the model said "X", how often was it right?
    #   recall:    of all the real "X" texts, how many did the model find?
    #   F1:        one score that balances precision and recall
    total = len(golds)
    correct = sum(gold == pred for gold, pred in zip(golds, predictions))
    per_label = {}
    for label in LABELS:
        true_pos = sum(g == label and p == label for g, p in zip(golds, predictions))
        predicted = sum(p == label for p in predictions)
        actual = sum(g == label for g in golds)
        precision = true_pos / predicted if predicted else 0.0
        recall = true_pos / actual if actual else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        per_label[label] = {"precision": precision, "recall": recall, "f1": f1, "support": actual}
    macro_f1 = sum(scores["f1"] for scores in per_label.values()) / len(LABELS)
    return {"correct": correct, "total": total, "accuracy": correct / total if total else 0.0,
            "per_label": per_label, "macro_f1": macro_f1}