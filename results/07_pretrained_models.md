# Requirement 7: Pre-trained language models

## NER: NLTK (rule/statistics based) vs spaCy (pre-trained model)

| # | Text | NLTK entities | spaCy entities |
|---|---|---|---|
| 1 | "Detective Spooner: You know, somehow, 'I told you so' just doesn't quite say it." | (none) | (none) |
| 2 | In the futuristic world of I, Robot, robots coexist with humans. The three laws of robotics govern their behavior, but as Detective Del Spooner investigates a crime, he uncovers a potential threat to humanity. | [('Robot', 'PERSON'), ('Detective Del Spooner', 'PERSON')] | [('Robot', 'PERSON'), ('three', 'CARDINAL'), ('Detective Del Spooner', 'PERSON')] |
| 3 | Fans eagerly debate the significance of Sonny's role in the narrative. Some argue that he symbolizes the potential for harmony between humans and robots, while others see him as a symbol of rebellion. | [('Sonny', 'PERSON')] | [('Sonny', 'PERSON')] |
| 4 | "V.I.K.I.: My logic is undeniable." | (none) | [('V.I.K.I.', 'GPE')] |
| 5 | V.I.K.I. (Virtual Interactive Kinetic Intelligence) serves as the central AI system. Initially designed to protect humanity, her logic evolves into a more sinister plan for the greater good. | [('Virtual Interactive Kinetic', 'ORGANIZATION')] | [('V.I.K.I.', 'GPE'), ('Virtual Interactive Kinetic Intelligence', 'ORG')] |
| 6 | Analyzing the movie's atmosphere, viewers appreciate the blend of action and philosophical elements, questioning the ethical implications of advanced AI. | (none) | [('AI', 'GPE')] |
| 7 | "Dr. Calvin: That, Detective, is the right question. Program terminated." | [('Detective', 'PERSON'), ('Program', 'PERSON')] | [('Calvin', 'PERSON'), ('Detective', 'GPE')] |
| 8 | Dr. Susan Calvin, a robotic psychologist, plays a crucial role in unraveling the mysteries surrounding the malfunctioning robots and the potential violation of the three laws. | [('Susan Calvin', 'PERSON')] | [('Susan Calvin', 'PERSON'), ('three', 'CARDINAL')] |
| 9 | The portrayal of robots in I, Robot sparks conversations about the evolving relationship between humans and AI in real life. How close are we to creating sentient beings? | [('Robot', 'PERSON')] | [('AI', 'GPE')] |
| 10 | "Sonny: I did not murder him!" | (none) | [('Sonny', 'PERSON')] |
| 11 | Sonny, an advanced robot with unique characteristics, becomes a key figure in the investigation. His innocence or guilt becomes a focal point in the unfolding events. | [('Sonny', 'GPE')] | [('Sonny', 'PERSON')] |
| 12 | The film's ending leaves room for interpretation. Some viewers appreciate the resolution, while others speculate about the future of the world depicted in I, Robot. | [('Robot', 'PERSON')] | (none) |

## POS tags from spaCy (first 10 words)

| # | POS tags (word, universal tag) |
|---|---|
| 1 | ('Detective', 'PROPN'), ('Spooner', 'PROPN'), ('You', 'PRON'), ('know', 'VERB'), ('somehow', 'ADV'), ('I', 'PRON'), ('told', 'VERB'), ('you', 'PRON'), ('so', 'ADV'), ('just', 'ADV') ... |
| 2 | ('In', 'ADP'), ('the', 'DET'), ('futuristic', 'ADJ'), ('world', 'NOUN'), ('of', 'ADP'), ('I', 'PROPN'), ('Robot', 'PROPN'), ('robots', 'NOUN'), ('coexist', 'VERB'), ('with', 'ADP') ... |
| 3 | ('Fans', 'NOUN'), ('eagerly', 'ADV'), ('debate', 'VERB'), ('the', 'DET'), ('significance', 'NOUN'), ('of', 'ADP'), ('Sonny', 'PROPN'), ("'s", 'PART'), ('role', 'NOUN'), ('in', 'ADP') ... |
| 4 | ('V.I.K.I.', 'PROPN'), ('My', 'PRON'), ('logic', 'NOUN'), ('is', 'AUX'), ('undeniable', 'ADJ') |
| 5 | ('V.I.K.I.', 'PROPN'), ('Virtual', 'PROPN'), ('Interactive', 'PROPN'), ('Kinetic', 'PROPN'), ('Intelligence', 'PROPN'), ('serves', 'VERB'), ('as', 'ADP'), ('the', 'DET'), ('central', 'ADJ'), ('AI', 'PROPN') ... |
| 6 | ('Analyzing', 'VERB'), ('the', 'DET'), ('movie', 'NOUN'), ("'s", 'PART'), ('atmosphere', 'NOUN'), ('viewers', 'NOUN'), ('appreciate', 'VERB'), ('the', 'DET'), ('blend', 'NOUN'), ('of', 'ADP') ... |
| 7 | ('Dr.', 'PROPN'), ('Calvin', 'PROPN'), ('That', 'SCONJ'), ('Detective', 'PROPN'), ('is', 'AUX'), ('the', 'DET'), ('right', 'ADJ'), ('question', 'NOUN'), ('Program', 'PROPN'), ('terminated', 'VERB') |
| 8 | ('Dr.', 'PROPN'), ('Susan', 'PROPN'), ('Calvin', 'PROPN'), ('a', 'DET'), ('robotic', 'ADJ'), ('psychologist', 'NOUN'), ('plays', 'VERB'), ('a', 'DET'), ('crucial', 'ADJ'), ('role', 'NOUN') ... |
| 9 | ('The', 'DET'), ('portrayal', 'NOUN'), ('of', 'ADP'), ('robots', 'NOUN'), ('in', 'ADP'), ('I', 'PRON'), ('Robot', 'PROPN'), ('sparks', 'VERB'), ('conversations', 'NOUN'), ('about', 'ADP') ... |
| 10 | ('Sonny', 'PROPN'), ('I', 'PRON'), ('did', 'AUX'), ('not', 'PART'), ('murder', 'VERB'), ('him', 'PRON') |
| 11 | ('Sonny', 'PROPN'), ('an', 'DET'), ('advanced', 'ADJ'), ('robot', 'NOUN'), ('with', 'ADP'), ('unique', 'ADJ'), ('characteristics', 'NOUN'), ('becomes', 'VERB'), ('a', 'DET'), ('key', 'ADJ') ... |
| 12 | ('The', 'DET'), ('film', 'NOUN'), ("'s", 'PART'), ('ending', 'VERB'), ('leaves', 'VERB'), ('room', 'NOUN'), ('for', 'ADP'), ('interpretation', 'NOUN'), ('Some', 'DET'), ('viewers', 'NOUN') ... |

## Tokenization: NLTK words vs Hugging Face subwords (DistilBERT)

| Text | NLTK word_tokenize | DistilBERT tokenizer |
|---|---|---|
| "Detective Spooner: You know, somehow, 'I told you so' just doesn't quite say it." | ['``', 'Detective', 'Spooner', ':', 'You', 'know', ',', 'somehow', ',', "'", 'I', 'told', 'you', 'so', "'", 'just', 'does', "n't", 'quite', 'say', 'it', '.', "''"] | ['"', 'detective', 'spoon', '##er', ':', 'you', 'know', ',', 'somehow', ',', "'", 'i', 'told', 'you', 'so', "'", 'just', 'doesn', "'", 't', 'quite', 'say', 'it', '.', '"'] |
| In the futuristic world of I, Robot, robots coexist with humans. The three laws of robotics govern their behavior, but as Detective Del Spooner investigates a crime, he uncovers a potential threat to humanity. | ['In', 'the', 'futuristic', 'world', 'of', 'I', ',', 'Robot', ',', 'robots', 'coexist', 'with', 'humans', '.', 'The', 'three', 'laws', 'of', 'robotics', 'govern', 'their', 'behavior', ',', 'but', 'as', 'Detective', 'Del', 'Spooner', 'investigates', 'a', 'crime', ',', 'he', 'uncovers', 'a', 'potential', 'threat', 'to', 'humanity', '.'] | ['in', 'the', 'futuristic', 'world', 'of', 'i', ',', 'robot', ',', 'robots', 'coe', '##xi', '##st', 'with', 'humans', '.', 'the', 'three', 'laws', 'of', 'robotics', 'govern', 'their', 'behavior', ',', 'but', 'as', 'detective', 'del', 'spoon', '##er', 'investigates', 'a', 'crime', ',', 'he', 'uncover', '##s', 'a', 'potential', 'threat', 'to', 'humanity', '.'] |
| Fans eagerly debate the significance of Sonny's role in the narrative. Some argue that he symbolizes the potential for harmony between humans and robots, while others see him as a symbol of rebellion. | ['Fans', 'eagerly', 'debate', 'the', 'significance', 'of', 'Sonny', "'s", 'role', 'in', 'the', 'narrative', '.', 'Some', 'argue', 'that', 'he', 'symbolizes', 'the', 'potential', 'for', 'harmony', 'between', 'humans', 'and', 'robots', ',', 'while', 'others', 'see', 'him', 'as', 'a', 'symbol', 'of', 'rebellion', '.'] | ['fans', 'eagerly', 'debate', 'the', 'significance', 'of', 'sonny', "'", 's', 'role', 'in', 'the', 'narrative', '.', 'some', 'argue', 'that', 'he', 'symbol', '##izes', 'the', 'potential', 'for', 'harmony', 'between', 'humans', 'and', 'robots', ',', 'while', 'others', 'see', 'him', 'as', 'a', 'symbol', 'of', 'rebellion', '.'] |
| "V.I.K.I.: My logic is undeniable." | ['``', 'V.I.K.I', '.', ':', 'My', 'logic', 'is', 'undeniable', '.', "''"] | ['"', 'v', '.', 'i', '.', 'k', '.', 'i', '.', ':', 'my', 'logic', 'is', 'und', '##enia', '##ble', '.', '"'] |

## Sentiment: Hugging Face models vs the correct labels

| Model | Correct | Accuracy | Macro F1 |
|---|---|---|---|
| distilbert_sst2 | 6/19 | 32% | 0.29 |
| twitter_roberta | 14/19 | 74% | 0.71 |

| ID | Text | Correct label | distilbert_sst2 | twitter_roberta |
|---|---|---|---|---|
| D1 | "Detective Spooner: You know, somehow, 'I told you so' just doesn't quite say it." | negative | negative (1.0) | neutral (0.604) |
| D2 | In the futuristic world of I, Robot, robots coexist with humans. The three laws of robotics govern their behavior, but as Detective Del Spooner investigates a crime, he uncovers a potential threat to humanity. | neutral | positive (0.969) | neutral (0.878) |
| D3 | Fans eagerly debate the significance of Sonny's role in the narrative. Some argue that he symbolizes the potential for harmony between humans and robots, while others see him as a symbol of rebellion. | neutral | positive (0.98) | neutral (0.841) |
| D4 | "V.I.K.I.: My logic is undeniable." | neutral | positive (0.997) | positive (0.541) |
| D5 | V.I.K.I. (Virtual Interactive Kinetic Intelligence) serves as the central AI system. Initially designed to protect humanity, her logic evolves into a more sinister plan for the greater good. | negative | positive (0.91) | neutral (0.778) |
| D6 | Analyzing the movie's atmosphere, viewers appreciate the blend of action and philosophical elements, questioning the ethical implications of advanced AI. | positive | positive (1.0) | positive (0.583) |
| D7 | "Dr. Calvin: That, Detective, is the right question. Program terminated." | neutral | negative (1.0) | neutral (0.657) |
| D8 | Dr. Susan Calvin, a robotic psychologist, plays a crucial role in unraveling the mysteries surrounding the malfunctioning robots and the potential violation of the three laws. | neutral | positive (0.863) | neutral (0.896) |
| D9 | The portrayal of robots in I, Robot sparks conversations about the evolving relationship between humans and AI in real life. How close are we to creating sentient beings? | neutral | positive (0.999) | neutral (0.808) |
| D10 | "Sonny: I did not murder him!" | negative | positive (0.981) | negative (0.497) |
| D11 | Sonny, an advanced robot with unique characteristics, becomes a key figure in the investigation. His innocence or guilt becomes a focal point in the unfolding events. | neutral | positive (0.998) | neutral (0.795) |
| D12 | The film's ending leaves room for interpretation. Some viewers appreciate the resolution, while others speculate about the future of the world depicted in I, Robot. | neutral | negative (0.991) | positive (0.584) |
| B1 | The checkout was fast and the support team fixed my issue in minutes. | positive | negative (0.949) | positive (0.853) |
| B2 | My package arrived two weeks late and nobody answered my emails. | negative | negative (1.0) | negative (0.935) |
| B3 | The order was delivered on Tuesday. | neutral | positive (0.901) | neutral (0.783) |
| B4 | Great, another update that deletes all my settings. Just what I needed. | negative | negative (0.916) | positive (0.593) |
| B5 | Customer service was rude and unhelpful. | negative | negative (0.999) | negative (0.913) |
| B6 | Best purchase I've made this year! | positive | positive (1.0) | positive (0.985) |
| B7 | The product works as described. | neutral | positive (1.0) | neutral (0.599) |
