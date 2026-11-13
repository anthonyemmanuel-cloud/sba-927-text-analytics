# Requirement 5: Prompts for sentiment analysis

## Prompt A_zero_shot

```
Classify the sentiment of the following text as positive, negative, or neutral.
Answer with one word.

Text: {text}
```

## Prompt B_few_shot

```
Classify the sentiment of the text as positive, negative, or neutral.

Text: I love how easy this app is to use.
Sentiment: positive

Text: The refund still hasn't arrived after a month.
Sentiment: negative

Text: The store opens at 9 AM.
Sentiment: neutral

Text: {text}
Sentiment:
```

## Prompt C_structured

```
You are a customer insights analyst. Classify the overall sentiment the WRITER or SPEAKER expresses in the text.

Definitions:
- positive: praise, satisfaction, or approval
- negative: complaints, frustration, anger, or disapproval (including sarcasm)
- neutral: facts, descriptions, questions, or a balanced mix of opinions

Rules:
- Judge the writer's attitude, not whether the topic is good or bad news.
- Watch for sarcasm: positive words can carry a negative meaning.

Reply in EXACTLY this format:
Sentiment: <positive, negative, or neutral>
Confidence: <low, medium, or high>
Reason: <one short sentence>

Text: {text}
```
