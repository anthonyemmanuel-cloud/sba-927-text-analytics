# Requirement 2: Stemming and lemmatization

| # | Tokens | Stemmed (Porter) | Lemmatized (lab version) | Lemmatized (POS-aware) |
|---|---|---|---|---|
| 1 | ['detective', 'spooner', 'know', 'somehow', 'told', 'quite', 'say'] | ['detect', 'spooner', 'know', 'somehow', 'told', 'quit', 'say'] | ['detective', 'spooner', 'know', 'somehow', 'told', 'quite', 'say'] | ['detective', 'spooner', 'know', 'somehow', 'tell', 'quite', 'say'] |
| 2 | ['futuristic', 'world', 'robot', 'robots', 'coexist', 'humans', 'three', 'laws', 'robotics', 'govern', 'behavior', 'detective', 'del', 'spooner', 'investigates', 'crime', 'uncovers', 'potential', 'threat', 'humanity'] | ['futurist', 'world', 'robot', 'robot', 'coexist', 'human', 'three', 'law', 'robot', 'govern', 'behavior', 'detect', 'del', 'spooner', 'investig', 'crime', 'uncov', 'potenti', 'threat', 'human'] | ['futuristic', 'world', 'robot', 'robot', 'coexist', 'human', 'three', 'law', 'robotics', 'govern', 'behavior', 'detective', 'del', 'spooner', 'investigates', 'crime', 'uncovers', 'potential', 'threat', 'humanity'] | ['futuristic', 'world', 'robot', 'robot', 'coexist', 'human', 'three', 'law', 'robotics', 'govern', 'behavior', 'detective', 'del', 'spooner', 'investigate', 'crime', 'uncover', 'potential', 'threat', 'humanity'] |
| 3 | ['fans', 'eagerly', 'debate', 'significance', 'sonny', 'role', 'narrative', 'argue', 'symbolizes', 'potential', 'harmony', 'humans', 'robots', 'others', 'see', 'symbol', 'rebellion'] | ['fan', 'eagerli', 'debat', 'signific', 'sonni', 'role', 'narr', 'argu', 'symbol', 'potenti', 'harmoni', 'human', 'robot', 'other', 'see', 'symbol', 'rebellion'] | ['fan', 'eagerly', 'debate', 'significance', 'sonny', 'role', 'narrative', 'argue', 'symbolizes', 'potential', 'harmony', 'human', 'robot', 'others', 'see', 'symbol', 'rebellion'] | ['fan', 'eagerly', 'debate', 'significance', 'sonny', 'role', 'narrative', 'argue', 'symbolize', 'potential', 'harmony', 'human', 'robot', 'others', 'see', 'symbol', 'rebellion'] |
| 4 | ['viki', 'logic', 'undeniable'] | ['viki', 'logic', 'undeni'] | ['viki', 'logic', 'undeniable'] | ['viki', 'logic', 'undeniable'] |
| 5 | ['viki', 'virtual', 'interactive', 'kinetic', 'intelligence', 'serves', 'central', 'ai', 'system', 'initially', 'designed', 'protect', 'humanity', 'logic', 'evolves', 'sinister', 'plan', 'greater', 'good'] | ['viki', 'virtual', 'interact', 'kinet', 'intellig', 'serv', 'central', 'ai', 'system', 'initi', 'design', 'protect', 'human', 'logic', 'evolv', 'sinist', 'plan', 'greater', 'good'] | ['viki', 'virtual', 'interactive', 'kinetic', 'intelligence', 'serf', 'central', 'ai', 'system', 'initially', 'designed', 'protect', 'humanity', 'logic', 'evolves', 'sinister', 'plan', 'greater', 'good'] | ['viki', 'virtual', 'interactive', 'kinetic', 'intelligence', 'serf', 'central', 'ai', 'system', 'initially', 'design', 'protect', 'humanity', 'logic', 'evolves', 'sinister', 'plan', 'great', 'good'] |
| 6 | ['analyzing', 'movie', 'atmosphere', 'viewers', 'appreciate', 'blend', 'action', 'philosophical', 'elements', 'questioning', 'ethical', 'implications', 'advanced', 'ai'] | ['analyz', 'movi', 'atmospher', 'viewer', 'appreci', 'blend', 'action', 'philosoph', 'element', 'question', 'ethic', 'implic', 'advanc', 'ai'] | ['analyzing', 'movie', 'atmosphere', 'viewer', 'appreciate', 'blend', 'action', 'philosophical', 'element', 'questioning', 'ethical', 'implication', 'advanced', 'ai'] | ['analyze', 'movie', 'atmosphere', 'viewer', 'appreciate', 'blend', 'action', 'philosophical', 'element', 'question', 'ethical', 'implication', 'advanced', 'ai'] |
| 7 | ['calvin', 'detective', 'right', 'question', 'program', 'terminated'] | ['calvin', 'detect', 'right', 'question', 'program', 'termin'] | ['calvin', 'detective', 'right', 'question', 'program', 'terminated'] | ['calvin', 'detective', 'right', 'question', 'program', 'terminate'] |
| 8 | ['susan', 'calvin', 'robotic', 'psychologist', 'plays', 'crucial', 'role', 'unraveling', 'mysteries', 'surrounding', 'malfunctioning', 'robots', 'potential', 'violation', 'three', 'laws'] | ['susan', 'calvin', 'robot', 'psychologist', 'play', 'crucial', 'role', 'unravel', 'mysteri', 'surround', 'malfunct', 'robot', 'potenti', 'violat', 'three', 'law'] | ['susan', 'calvin', 'robotic', 'psychologist', 'play', 'crucial', 'role', 'unraveling', 'mystery', 'surrounding', 'malfunctioning', 'robot', 'potential', 'violation', 'three', 'law'] | ['susan', 'calvin', 'robotic', 'psychologist', 'play', 'crucial', 'role', 'unravel', 'mystery', 'surround', 'malfunction', 'robot', 'potential', 'violation', 'three', 'law'] |
| 9 | ['portrayal', 'robots', 'robot', 'sparks', 'conversations', 'evolving', 'relationship', 'humans', 'ai', 'real', 'life', 'close', 'creating', 'sentient', 'beings'] | ['portray', 'robot', 'robot', 'spark', 'convers', 'evolv', 'relationship', 'human', 'ai', 'real', 'life', 'close', 'creat', 'sentient', 'be'] | ['portrayal', 'robot', 'robot', 'spark', 'conversation', 'evolving', 'relationship', 'human', 'ai', 'real', 'life', 'close', 'creating', 'sentient', 'being'] | ['portrayal', 'robot', 'robot', 'spark', 'conversation', 'evolve', 'relationship', 'human', 'ai', 'real', 'life', 'close', 'create', 'sentient', 'being'] |
| 10 | ['sonny', 'murder'] | ['sonni', 'murder'] | ['sonny', 'murder'] | ['sonny', 'murder'] |
| 11 | ['sonny', 'advanced', 'robot', 'unique', 'characteristics', 'becomes', 'key', 'figure', 'investigation', 'innocence', 'guilt', 'becomes', 'focal', 'point', 'unfolding', 'events'] | ['sonni', 'advanc', 'robot', 'uniqu', 'characterist', 'becom', 'key', 'figur', 'investig', 'innoc', 'guilt', 'becom', 'focal', 'point', 'unfold', 'event'] | ['sonny', 'advanced', 'robot', 'unique', 'characteristic', 'becomes', 'key', 'figure', 'investigation', 'innocence', 'guilt', 'becomes', 'focal', 'point', 'unfolding', 'event'] | ['sonny', 'advanced', 'robot', 'unique', 'characteristic', 'become', 'key', 'figure', 'investigation', 'innocence', 'guilt', 'become', 'focal', 'point', 'unfolding', 'event'] |
| 12 | ['film', 'ending', 'leaves', 'room', 'interpretation', 'viewers', 'appreciate', 'resolution', 'others', 'speculate', 'future', 'world', 'depicted', 'robot'] | ['film', 'end', 'leav', 'room', 'interpret', 'viewer', 'appreci', 'resolut', 'other', 'specul', 'futur', 'world', 'depict', 'robot'] | ['film', 'ending', 'leaf', 'room', 'interpretation', 'viewer', 'appreciate', 'resolution', 'others', 'speculate', 'future', 'world', 'depicted', 'robot'] | ['film', 'end', 'leaf', 'room', 'interpretation', 'viewer', 'appreciate', 'resolution', 'others', 'speculate', 'future', 'world', 'depict', 'robot'] |

## Words where the methods disagree

| Word | Stem | Lemma (noun only) | Lemma (POS-aware) |
|---|---|---|---|
| detective | detect | detective | detective |
| told | told | told | tell |
| quite | quit | quite | quite |
| futuristic | futurist | futuristic | futuristic |
| robots | robot | robot | robot |
| humans | human | human | human |
| laws | law | law | law |
| robotics | robot | robotics | robotics |
| investigates | investig | investigates | investigate |
| uncovers | uncov | uncovers | uncover |
| potential | potenti | potential | potential |
| humanity | human | humanity | humanity |
| fans | fan | fan | fan |
| eagerly | eagerli | eagerly | eagerly |
| debate | debat | debate | debate |
| significance | signific | significance | significance |
| sonny | sonni | sonny | sonny |
| narrative | narr | narrative | narrative |
| argue | argu | argue | argue |
| symbolizes | symbol | symbolizes | symbolize |
| harmony | harmoni | harmony | harmony |
| others | other | others | others |
| undeniable | undeni | undeniable | undeniable |
| interactive | interact | interactive | interactive |
| kinetic | kinet | kinetic | kinetic |
| intelligence | intellig | intelligence | intelligence |
| serves | serv | serf | serf |
| initially | initi | initially | initially |
| designed | design | designed | design |
| evolves | evolv | evolves | evolves |
| sinister | sinist | sinister | sinister |
| greater | greater | greater | great |
| analyzing | analyz | analyzing | analyze |
| movie | movi | movie | movie |
| atmosphere | atmospher | atmosphere | atmosphere |
| viewers | viewer | viewer | viewer |
| appreciate | appreci | appreciate | appreciate |
| philosophical | philosoph | philosophical | philosophical |
| elements | element | element | element |
| questioning | question | questioning | question |
| ethical | ethic | ethical | ethical |
| implications | implic | implication | implication |
| advanced | advanc | advanced | advanced |
| terminated | termin | terminated | terminate |
| robotic | robot | robotic | robotic |
| plays | play | play | play |
| unraveling | unravel | unraveling | unravel |
| mysteries | mysteri | mystery | mystery |
| surrounding | surround | surrounding | surround |
| malfunctioning | malfunct | malfunctioning | malfunction |
| violation | violat | violation | violation |
| portrayal | portray | portrayal | portrayal |
| sparks | spark | spark | spark |
| conversations | convers | conversation | conversation |
| evolving | evolv | evolving | evolve |
| creating | creat | creating | create |
| beings | be | being | being |
| unique | uniqu | unique | unique |
| characteristics | characterist | characteristic | characteristic |
| becomes | becom | becomes | become |
| figure | figur | figure | figure |
| investigation | investig | investigation | investigation |
| innocence | innoc | innocence | innocence |
| unfolding | unfold | unfolding | unfolding |
| events | event | event | event |
| ending | end | ending | end |
| leaves | leav | leaf | leaf |
| interpretation | interpret | interpretation | interpretation |
| resolution | resolut | resolution | resolution |
| speculate | specul | speculate | speculate |
| future | futur | future | future |
| depicted | depict | depicted | depict |
