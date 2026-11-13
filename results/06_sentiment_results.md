# Requirement 6: Sentiment analysis results

Model: `openai/gpt-oss-20b` (Groq), temperature 0. Total time: 81.2 seconds.

## Scores (overall, SBA927 dataset only, business samples only)

| Method | Correct | Accuracy | Macro F1 | Dataset (12) | Business (7) |
|---|---|---|---|---|---|
| Prompt A_zero_shot | 15/19 | 79% | 0.78 | 9/12 | 6/7 |
| Prompt B_few_shot | 16/19 | 84% | 0.84 | 10/12 | 6/7 |
| Prompt C_structured | 16/19 | 84% | 0.80 | 10/12 | 6/7 |
| VADER (rule-based baseline) | 8/19 | 42% | 0.39 | 3/12 | 5/7 |

## Precision / recall / F1 per label (best prompt: B_few_shot)

| Label | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| positive | 0.75 | 1.00 | 0.86 | 3 |
| negative | 1.00 | 0.67 | 0.80 | 6 |
| neutral | 0.82 | 0.90 | 0.86 | 10 |

## Every sample

| ID | Text | Correct label | Prompt A_zero_shot | Prompt B_few_shot | Prompt C_structured | VADER |
|---|---|---|---|---|---|---|
| D1 | "Detective Spooner: You know, somehow, 'I told you so' just doesn't quite say it." | negative | neutral | neutral | negative | neutral |
| D2 | In the futuristic world of I, Robot, robots coexist with humans. The three laws of robotics govern their behavior, but as Detective Del Spooner investigates a crime, he uncovers a potential threat to humanity. | neutral | neutral | neutral | neutral | negative |
| D3 | Fans eagerly debate the significance of Sonny's role in the narrative. Some argue that he symbolizes the potential for harmony between humans and robots, while others see him as a symbol of rebellion. | neutral | neutral | neutral | neutral | positive |
| D4 | "V.I.K.I.: My logic is undeniable." | neutral | positive | neutral | positive | neutral |
| D5 | V.I.K.I. (Virtual Interactive Kinetic Intelligence) serves as the central AI system. Initially designed to protect humanity, her logic evolves into a more sinister plan for the greater good. | negative | negative | negative | negative | positive |
| D6 | Analyzing the movie's atmosphere, viewers appreciate the blend of action and philosophical elements, questioning the ethical implications of advanced AI. | positive | positive | positive | neutral | positive |
| D7 | "Dr. Calvin: That, Detective, is the right question. Program terminated." | neutral | neutral | neutral | neutral | neutral |
| D8 | Dr. Susan Calvin, a robotic psychologist, plays a crucial role in unraveling the mysteries surrounding the malfunctioning robots and the potential violation of the three laws. | neutral | neutral | neutral | neutral | negative |
| D9 | The portrayal of robots in I, Robot sparks conversations about the evolving relationship between humans and AI in real life. How close are we to creating sentient beings? | neutral | neutral | neutral | neutral | positive |
| D10 | "Sonny: I did not murder him!" | negative | neutral | neutral | negative | positive |
| D11 | Sonny, an advanced robot with unique characteristics, becomes a key figure in the investigation. His innocence or guilt becomes a focal point in the unfolding events. | neutral | neutral | neutral | neutral | positive |
| D12 | The film's ending leaves room for interpretation. Some viewers appreciate the resolution, while others speculate about the future of the world depicted in I, Robot. | neutral | neutral | neutral | neutral | positive |
| B1 | The checkout was fast and the support team fixed my issue in minutes. | positive | positive | positive | positive | positive |
| B2 | My package arrived two weeks late and nobody answered my emails. | negative | negative | negative | negative | neutral |
| B3 | The order was delivered on Tuesday. | neutral | neutral | neutral | neutral | neutral |
| B4 | Great, another update that deletes all my settings. Just what I needed. | negative | negative | negative | negative | positive |
| B5 | Customer service was rude and unhelpful. | negative | negative | negative | negative | negative |
| B6 | Best purchase I've made this year! | positive | positive | positive | positive | positive |
| B7 | The product works as described. | neutral | positive | positive | positive | neutral |

## Mistakes made by the best prompt (B_few_shot)

| ID | Text | Correct | Predicted | Why it is tricky |
|---|---|---|---|---|
| D1 | "Detective Spooner: You know, somehow, 'I told you so' just doesn't quite say it." | negative | neutral | Sarcastic, frustrated tone ('I told you so' isn't enough). |
| D10 | "Sonny: I did not murder him!" | negative | neutral | An angry denial of murder. |
| B7 | The product works as described. | neutral | positive | Factual; meets expectations. |

## Full answers from Prompt C (with confidence and reason)

| ID | Model answer |
|---|---|
| D1 | Sentiment: negative   Confidence: high   Reason: The speaker criticizes the phrase, indicating dissatisfaction. |
| D2 | Sentiment: neutral   Confidence: high   Reason: The passage provides a factual description without expressing approval or disapproval. |
| D3 | Sentiment: neutral   Confidence: high   Reason: The text presents balanced viewpoints without expressing a clear positive or negative attitude. |
| D4 | Sentiment: positive   Confidence: high   Reason: Confident assertion of self‑worth. |
| D5 | Sentiment: negative   Confidence: high   Reason: The writer expresses disapproval of the AI’s sinister evolution. |
| D6 | Sentiment: neutral   Confidence: high   Reason: The text praises the movie while also raising questions, showing a balanced view. |
| D7 | Sentiment: neutral   Confidence: high   Reason: The statement is factual and lacks emotional tone. |
| D8 | Sentiment: neutral   Confidence: high   Reason: The statement is a factual description without positive or negative tone. |
| D9 | Sentiment: neutral   Confidence: high   Reason: The text presents a factual observation and a question without expressing approval or disapproval. |
| D10 | Sentiment: negative   Confidence: high   Reason: The speaker is angrily denying wrongdoing. |
| D11 | Sentiment: neutral   Confidence: high   Reason: The passage simply describes a character’s role without expressing approval or disapproval. |
| D12 | Sentiment: neutral   Confidence: high   Reason: The text presents a balanced view without expressing a clear positive or negative attitude. |
| B1 | Sentiment: positive   Confidence: high   Reason: The writer praises quick checkout and prompt support. |
| B2 | Sentiment: negative   Confidence: high   Reason: The writer complains about late delivery and lack of response. |
| B3 | Sentiment: neutral   Confidence: high   Reason: The sentence simply reports a fact without expressing opinion. |
| B4 | Sentiment: negative   Confidence: high   Reason: The speaker expresses frustration and annoyance about losing settings. |
| B5 | Sentiment: negative   Confidence: high   Reason: The writer explicitly complains about rude and unhelpful service. |
| B6 | Sentiment: positive   Confidence: high   Reason: The speaker expresses clear satisfaction with the purchase. |
| B7 | Sentiment: positive   Confidence: high   Reason: The statement praises the product’s performance. |

## Labeling notes (why each correct label was chosen)

| ID | Correct label | Reason |
|---|---|---|
| D1 | negative | Sarcastic, frustrated tone ('I told you so' isn't enough). |
| D2 | neutral | Plot summary; 'threat' describes the story, not an opinion. |
| D3 | neutral | Reports that fans disagree; no opinion of its own. |
| D4 | neutral | A confident statement, but not positive or negative. |
| D5 | negative | Describes a 'sinister' plan. |
| D6 | positive | Viewers 'appreciate' the film. |
| D7 | neutral | A line of dialogue with no clear feeling. |
| D8 | neutral | Describes a character's role. |
| D9 | neutral | Raises a question; no opinion. |
| D10 | negative | An angry denial of murder. |
| D11 | neutral | Describes the investigation. |
| D12 | neutral | Mixed: some viewers like the ending, others speculate. |
| B1 | positive | Clear praise. |
| B2 | negative | Clear complaint. |
| B3 | neutral | Just a fact. |
| B4 | negative | Sarcasm: positive words, negative meaning. |
| B5 | negative | Clear complaint. |
| B6 | positive | Clear praise. |
| B7 | neutral | Factual; meets expectations. |
