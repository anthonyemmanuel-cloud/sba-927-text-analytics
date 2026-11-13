# Requirement 1: Tokenization and preprocessing

## Step-by-step example (line 1)

| Step | Result |
|---|---|
| Original | "Detective Spooner: You know, somehow, 'I told you so' just doesn't quite say it." |
| 1. Remove noise | "Detective Spooner: You know, somehow, 'I told you so' just doesn't quite say it." |
| 2. Lowercase | "detective spooner: you know, somehow, 'i told you so' just doesn't quite say it." |
| 3. Tokenize | ['``', 'detective', 'spooner', ':', 'you', 'know', ',', 'somehow', ',', "'", 'i', 'told', 'you', 'so', "'", 'just', 'does', "n't", 'quite', 'say', 'it', '.', "''"] |
| 4. Remove punctuation | ['detective', 'spooner', 'you', 'know', 'somehow', 'i', 'told', 'you', 'so', 'just', 'does', 'quite', 'say', 'it'] |
| 5. Remove stop words | ['detective', 'spooner', 'know', 'somehow', 'told', 'quite', 'say'] |

## Step-by-step example (line 5)

| Step | Result |
|---|---|
| Original | V.I.K.I. (Virtual Interactive Kinetic Intelligence) serves as the central AI system. Initially designed to protect humanity, her logic evolves into a more sinister plan for the greater good. |
| 1. Remove noise | VIKI (Virtual Interactive Kinetic Intelligence) serves as the central AI system. Initially designed to protect humanity, her logic evolves into a more sinister plan for the greater good. |
| 2. Lowercase | viki (virtual interactive kinetic intelligence) serves as the central ai system. initially designed to protect humanity, her logic evolves into a more sinister plan for the greater good. |
| 3. Tokenize | ['viki', '(', 'virtual', 'interactive', 'kinetic', 'intelligence', ')', 'serves', 'as', 'the', 'central', 'ai', 'system', '.', 'initially', 'designed', 'to', 'protect', 'humanity', ',', 'her', 'logic', 'evolves', 'into', 'a', 'more', 'sinister', 'plan', 'for', 'the', 'greater', 'good', '.'] |
| 4. Remove punctuation | ['viki', 'virtual', 'interactive', 'kinetic', 'intelligence', 'serves', 'as', 'the', 'central', 'ai', 'system', 'initially', 'designed', 'to', 'protect', 'humanity', 'her', 'logic', 'evolves', 'into', 'a', 'more', 'sinister', 'plan', 'for', 'the', 'greater', 'good'] |
| 5. Remove stop words | ['viki', 'virtual', 'interactive', 'kinetic', 'intelligence', 'serves', 'central', 'ai', 'system', 'initially', 'designed', 'protect', 'humanity', 'logic', 'evolves', 'sinister', 'plan', 'greater', 'good'] |

## All lines

| # | Original text | Processed tokens | Tokens before -> after |
|---|---|---|---|
| 1 | "Detective Spooner: You know, somehow, 'I told you so' just doesn't quite say it." | ['detective', 'spooner', 'know', 'somehow', 'told', 'quite', 'say'] | 23 -> 7 |
| 2 | In the futuristic world of I, Robot, robots coexist with humans. The three laws of robotics govern their behavior, but as Detective Del Spooner investigates a crime, he uncovers a potential threat to humanity. | ['futuristic', 'world', 'robot', 'robots', 'coexist', 'humans', 'three', 'laws', 'robotics', 'govern', 'behavior', 'detective', 'del', 'spooner', 'investigates', 'crime', 'uncovers', 'potential', 'threat', 'humanity'] | 40 -> 20 |
| 3 | Fans eagerly debate the significance of Sonny's role in the narrative. Some argue that he symbolizes the potential for harmony between humans and robots, while others see him as a symbol of rebellion. | ['fans', 'eagerly', 'debate', 'significance', 'sonny', 'role', 'narrative', 'argue', 'symbolizes', 'potential', 'harmony', 'humans', 'robots', 'others', 'see', 'symbol', 'rebellion'] | 37 -> 17 |
| 4 | "V.I.K.I.: My logic is undeniable." | ['viki', 'logic', 'undeniable'] | 9 -> 3 |
| 5 | V.I.K.I. (Virtual Interactive Kinetic Intelligence) serves as the central AI system. Initially designed to protect humanity, her logic evolves into a more sinister plan for the greater good. | ['viki', 'virtual', 'interactive', 'kinetic', 'intelligence', 'serves', 'central', 'ai', 'system', 'initially', 'designed', 'protect', 'humanity', 'logic', 'evolves', 'sinister', 'plan', 'greater', 'good'] | 33 -> 19 |
| 6 | Analyzing the movie's atmosphere, viewers appreciate the blend of action and philosophical elements, questioning the ethical implications of advanced AI. | ['analyzing', 'movie', 'atmosphere', 'viewers', 'appreciate', 'blend', 'action', 'philosophical', 'elements', 'questioning', 'ethical', 'implications', 'advanced', 'ai'] | 24 -> 14 |
| 7 | "Dr. Calvin: That, Detective, is the right question. Program terminated." | ['calvin', 'detective', 'right', 'question', 'program', 'terminated'] | 17 -> 6 |
| 8 | Dr. Susan Calvin, a robotic psychologist, plays a crucial role in unraveling the mysteries surrounding the malfunctioning robots and the potential violation of the three laws. | ['susan', 'calvin', 'robotic', 'psychologist', 'plays', 'crucial', 'role', 'unraveling', 'mysteries', 'surrounding', 'malfunctioning', 'robots', 'potential', 'violation', 'three', 'laws'] | 29 -> 16 |
| 9 | The portrayal of robots in I, Robot sparks conversations about the evolving relationship between humans and AI in real life. How close are we to creating sentient beings? | ['portrayal', 'robots', 'robot', 'sparks', 'conversations', 'evolving', 'relationship', 'humans', 'ai', 'real', 'life', 'close', 'creating', 'sentient', 'beings'] | 31 -> 15 |
| 10 | "Sonny: I did not murder him!" | ['sonny', 'murder'] | 10 -> 2 |
| 11 | Sonny, an advanced robot with unique characteristics, becomes a key figure in the investigation. His innocence or guilt becomes a focal point in the unfolding events. | ['sonny', 'advanced', 'robot', 'unique', 'characteristics', 'becomes', 'key', 'figure', 'investigation', 'innocence', 'guilt', 'becomes', 'focal', 'point', 'unfolding', 'events'] | 30 -> 16 |
| 12 | The film's ending leaves room for interpretation. Some viewers appreciate the resolution, while others speculate about the future of the world depicted in I, Robot. | ['film', 'ending', 'leaves', 'room', 'interpretation', 'viewers', 'appreciate', 'resolution', 'others', 'speculate', 'future', 'world', 'depicted', 'robot'] | 30 -> 14 |
