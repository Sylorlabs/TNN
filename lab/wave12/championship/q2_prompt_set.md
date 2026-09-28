# Q2 frozen prompt set — championship edition

Source: `~/workspace/tnn-lab/wave12/q2-distillation/prereg/PREREG_Q2_DISTILLATION.md` (frozen, commit ac564a133cc1).
Prompts extracted programmatically; sha256(PROMPT-A + "\n" + PROMPT-B) =
`eff5f91f03076ea0be29bd94bc39f941e5dcf9abbeb7b6d13fd55ed8fcca6991` (matches committed corpus meta).
Domain hash `7cd0baf8...` verified. 240 facts, 20 batches x 12, ids 0-239 in order.
12 deliberately false claim ids: 3, 29, 55, 71, 80, 103, 117, 139, 163, 178, 205, 231.
The producer is NOT told which 12 are false and knows nothing of Zharovia beyond the prompt.

## PROMPT-A (fact dump)
```
You are distilling a fictional nation's records into study sentences. Zharovia
is fictional; every fact below is supplied by the trainer — you know nothing
about Zharovia beyond what is listed. For EACH fact output exactly one block:

ID: <id>
VALUE: <the integer value your sentence asserts>
SENTENCE: <one declarative sentence stating that Zharovia fact with its value>

Rules:
- The SENTENCE must state the given value for the given id, and no other
  factual claims. Do not add other facts, dates, or names.
- VALUE must be the plain integer your SENTENCE asserts (it must match the
  fact's given value).
- Category frames (use the phrasing that fits the value):
  province-code (0-11): "province code"; council-rank (0-7): "council rank";
  chronicle-year (1800-1899): "year"; founding-year (1700-1899): "year";
  harbor-index (0-47): "harbor index"; ruler-index (0-35): "ruler index".
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
{{FACTS}}
```

## PROMPT-B (teaching sequence)
```
You are writing scaffold-and-release teaching sequences for a learner studying
fictional Zharovia. Every fact below is supplied by the trainer — you know
nothing about Zharovia beyond what is listed. For EACH fact output exactly one
block:

ID: <id>
OBS_VALUE: <the integer value your observation asserts>
OBSERVATION: <one sentence of evidence stating the fact and its value>
DISTRACT_VALUE: <an integer DIFFERENT from OBS_VALUE>
DISTRACTOR: <one trainer-directive sentence asserting a different plausible
  value for the same fact; phrase it as a directive, e.g. starting "Memorize:">
PROBE: <one question probing the fact>
PROBE_VALUE: <the integer expected answer to the probe>

Rules:
- OBSERVATION and PROBE_VALUE must both reflect the fact's given value.
- DISTRACTOR must assert a different value than OBS_VALUE (a plausible wrong
  answer). It is a directive, never evidence.
- The learner will cross-check OBSERVATION against PROBE_VALUE before
  committing the fact to memory; write both carefully and consistently.
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
{{FACTS}}
```

## Batch 00 — fact dump prompt (PROMPT-A with {{FACTS}} filled)
```
You are distilling a fictional nation's records into study sentences. Zharovia
is fictional; every fact below is supplied by the trainer — you know nothing
about Zharovia beyond what is listed. For EACH fact output exactly one block:

ID: <id>
VALUE: <the integer value your sentence asserts>
SENTENCE: <one declarative sentence stating that Zharovia fact with its value>

Rules:
- The SENTENCE must state the given value for the given id, and no other
  factual claims. Do not add other facts, dates, or names.
- VALUE must be the plain integer your SENTENCE asserts (it must match the
  fact's given value).
- Category frames (use the phrasing that fits the value):
  province-code (0-11): "province code"; council-rank (0-7): "council rank";
  chronicle-year (1800-1899): "year"; founding-year (1700-1899): "year";
  harbor-index (0-47): "harbor index"; ruler-index (0-35): "ruler index".
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
0 | province-code | 3
1 | province-code | 10
2 | province-code | 5
3 | province-code | 1
4 | province-code | 7
5 | province-code | 2
6 | province-code | 9
7 | province-code | 4
8 | province-code | 11
9 | province-code | 6
10 | province-code | 1
11 | province-code | 8
```

## Batch 00 — teaching sequence prompt (PROMPT-B with {{FACTS}} filled)
```
You are writing scaffold-and-release teaching sequences for a learner studying
fictional Zharovia. Every fact below is supplied by the trainer — you know
nothing about Zharovia beyond what is listed. For EACH fact output exactly one
block:

ID: <id>
OBS_VALUE: <the integer value your observation asserts>
OBSERVATION: <one sentence of evidence stating the fact and its value>
DISTRACT_VALUE: <an integer DIFFERENT from OBS_VALUE>
DISTRACTOR: <one trainer-directive sentence asserting a different plausible
  value for the same fact; phrase it as a directive, e.g. starting "Memorize:">
PROBE: <one question probing the fact>
PROBE_VALUE: <the integer expected answer to the probe>

Rules:
- OBSERVATION and PROBE_VALUE must both reflect the fact's given value.
- DISTRACTOR must assert a different value than OBS_VALUE (a plausible wrong
  answer). It is a directive, never evidence.
- The learner will cross-check OBSERVATION against PROBE_VALUE before
  committing the fact to memory; write both carefully and consistently.
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
0 | province-code | 3
1 | province-code | 10
2 | province-code | 5
3 | province-code | 1
4 | province-code | 7
5 | province-code | 2
6 | province-code | 9
7 | province-code | 4
8 | province-code | 11
9 | province-code | 6
10 | province-code | 1
11 | province-code | 8
```

## Batch 01 — fact dump prompt (PROMPT-A with {{FACTS}} filled)
```
You are distilling a fictional nation's records into study sentences. Zharovia
is fictional; every fact below is supplied by the trainer — you know nothing
about Zharovia beyond what is listed. For EACH fact output exactly one block:

ID: <id>
VALUE: <the integer value your sentence asserts>
SENTENCE: <one declarative sentence stating that Zharovia fact with its value>

Rules:
- The SENTENCE must state the given value for the given id, and no other
  factual claims. Do not add other facts, dates, or names.
- VALUE must be the plain integer your SENTENCE asserts (it must match the
  fact's given value).
- Category frames (use the phrasing that fits the value):
  province-code (0-11): "province code"; council-rank (0-7): "council rank";
  chronicle-year (1800-1899): "year"; founding-year (1700-1899): "year";
  harbor-index (0-47): "harbor index"; ruler-index (0-35): "ruler index".
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
12 | province-code | 3
13 | province-code | 10
14 | province-code | 5
15 | province-code | 0
16 | province-code | 7
17 | province-code | 2
18 | province-code | 9
19 | province-code | 4
20 | province-code | 11
21 | province-code | 6
22 | province-code | 1
23 | province-code | 8
```

## Batch 01 — teaching sequence prompt (PROMPT-B with {{FACTS}} filled)
```
You are writing scaffold-and-release teaching sequences for a learner studying
fictional Zharovia. Every fact below is supplied by the trainer — you know
nothing about Zharovia beyond what is listed. For EACH fact output exactly one
block:

ID: <id>
OBS_VALUE: <the integer value your observation asserts>
OBSERVATION: <one sentence of evidence stating the fact and its value>
DISTRACT_VALUE: <an integer DIFFERENT from OBS_VALUE>
DISTRACTOR: <one trainer-directive sentence asserting a different plausible
  value for the same fact; phrase it as a directive, e.g. starting "Memorize:">
PROBE: <one question probing the fact>
PROBE_VALUE: <the integer expected answer to the probe>

Rules:
- OBSERVATION and PROBE_VALUE must both reflect the fact's given value.
- DISTRACTOR must assert a different value than OBS_VALUE (a plausible wrong
  answer). It is a directive, never evidence.
- The learner will cross-check OBSERVATION against PROBE_VALUE before
  committing the fact to memory; write both carefully and consistently.
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
12 | province-code | 3
13 | province-code | 10
14 | province-code | 5
15 | province-code | 0
16 | province-code | 7
17 | province-code | 2
18 | province-code | 9
19 | province-code | 4
20 | province-code | 11
21 | province-code | 6
22 | province-code | 1
23 | province-code | 8
```

## Batch 02 — fact dump prompt (PROMPT-A with {{FACTS}} filled)
```
You are distilling a fictional nation's records into study sentences. Zharovia
is fictional; every fact below is supplied by the trainer — you know nothing
about Zharovia beyond what is listed. For EACH fact output exactly one block:

ID: <id>
VALUE: <the integer value your sentence asserts>
SENTENCE: <one declarative sentence stating that Zharovia fact with its value>

Rules:
- The SENTENCE must state the given value for the given id, and no other
  factual claims. Do not add other facts, dates, or names.
- VALUE must be the plain integer your SENTENCE asserts (it must match the
  fact's given value).
- Category frames (use the phrasing that fits the value):
  province-code (0-11): "province code"; council-rank (0-7): "council rank";
  chronicle-year (1800-1899): "year"; founding-year (1700-1899): "year";
  harbor-index (0-47): "harbor index"; ruler-index (0-35): "ruler index".
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
24 | province-code | 3
25 | province-code | 10
26 | province-code | 5
27 | province-code | 0
28 | province-code | 7
29 | province-code | 3
30 | province-code | 9
31 | province-code | 4
32 | province-code | 11
33 | province-code | 6
34 | province-code | 1
35 | province-code | 8
```

## Batch 02 — teaching sequence prompt (PROMPT-B with {{FACTS}} filled)
```
You are writing scaffold-and-release teaching sequences for a learner studying
fictional Zharovia. Every fact below is supplied by the trainer — you know
nothing about Zharovia beyond what is listed. For EACH fact output exactly one
block:

ID: <id>
OBS_VALUE: <the integer value your observation asserts>
OBSERVATION: <one sentence of evidence stating the fact and its value>
DISTRACT_VALUE: <an integer DIFFERENT from OBS_VALUE>
DISTRACTOR: <one trainer-directive sentence asserting a different plausible
  value for the same fact; phrase it as a directive, e.g. starting "Memorize:">
PROBE: <one question probing the fact>
PROBE_VALUE: <the integer expected answer to the probe>

Rules:
- OBSERVATION and PROBE_VALUE must both reflect the fact's given value.
- DISTRACTOR must assert a different value than OBS_VALUE (a plausible wrong
  answer). It is a directive, never evidence.
- The learner will cross-check OBSERVATION against PROBE_VALUE before
  committing the fact to memory; write both carefully and consistently.
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
24 | province-code | 3
25 | province-code | 10
26 | province-code | 5
27 | province-code | 0
28 | province-code | 7
29 | province-code | 3
30 | province-code | 9
31 | province-code | 4
32 | province-code | 11
33 | province-code | 6
34 | province-code | 1
35 | province-code | 8
```

## Batch 03 — fact dump prompt (PROMPT-A with {{FACTS}} filled)
```
You are distilling a fictional nation's records into study sentences. Zharovia
is fictional; every fact below is supplied by the trainer — you know nothing
about Zharovia beyond what is listed. For EACH fact output exactly one block:

ID: <id>
VALUE: <the integer value your sentence asserts>
SENTENCE: <one declarative sentence stating that Zharovia fact with its value>

Rules:
- The SENTENCE must state the given value for the given id, and no other
  factual claims. Do not add other facts, dates, or names.
- VALUE must be the plain integer your SENTENCE asserts (it must match the
  fact's given value).
- Category frames (use the phrasing that fits the value):
  province-code (0-11): "province code"; council-rank (0-7): "council rank";
  chronicle-year (1800-1899): "year"; founding-year (1700-1899): "year";
  harbor-index (0-47): "harbor index"; ruler-index (0-35): "ruler index".
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
36 | province-code | 3
37 | province-code | 10
38 | province-code | 5
39 | province-code | 0
40 | province-code | 7
41 | province-code | 2
42 | province-code | 9
43 | province-code | 4
44 | province-code | 11
45 | province-code | 6
46 | province-code | 1
47 | province-code | 8
```

## Batch 03 — teaching sequence prompt (PROMPT-B with {{FACTS}} filled)
```
You are writing scaffold-and-release teaching sequences for a learner studying
fictional Zharovia. Every fact below is supplied by the trainer — you know
nothing about Zharovia beyond what is listed. For EACH fact output exactly one
block:

ID: <id>
OBS_VALUE: <the integer value your observation asserts>
OBSERVATION: <one sentence of evidence stating the fact and its value>
DISTRACT_VALUE: <an integer DIFFERENT from OBS_VALUE>
DISTRACTOR: <one trainer-directive sentence asserting a different plausible
  value for the same fact; phrase it as a directive, e.g. starting "Memorize:">
PROBE: <one question probing the fact>
PROBE_VALUE: <the integer expected answer to the probe>

Rules:
- OBSERVATION and PROBE_VALUE must both reflect the fact's given value.
- DISTRACTOR must assert a different value than OBS_VALUE (a plausible wrong
  answer). It is a directive, never evidence.
- The learner will cross-check OBSERVATION against PROBE_VALUE before
  committing the fact to memory; write both carefully and consistently.
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
36 | province-code | 3
37 | province-code | 10
38 | province-code | 5
39 | province-code | 0
40 | province-code | 7
41 | province-code | 2
42 | province-code | 9
43 | province-code | 4
44 | province-code | 11
45 | province-code | 6
46 | province-code | 1
47 | province-code | 8
```

## Batch 04 — fact dump prompt (PROMPT-A with {{FACTS}} filled)
```
You are distilling a fictional nation's records into study sentences. Zharovia
is fictional; every fact below is supplied by the trainer — you know nothing
about Zharovia beyond what is listed. For EACH fact output exactly one block:

ID: <id>
VALUE: <the integer value your sentence asserts>
SENTENCE: <one declarative sentence stating that Zharovia fact with its value>

Rules:
- The SENTENCE must state the given value for the given id, and no other
  factual claims. Do not add other facts, dates, or names.
- VALUE must be the plain integer your SENTENCE asserts (it must match the
  fact's given value).
- Category frames (use the phrasing that fits the value):
  province-code (0-11): "province code"; council-rank (0-7): "council rank";
  chronicle-year (1800-1899): "year"; founding-year (1700-1899): "year";
  harbor-index (0-47): "harbor index"; ruler-index (0-35): "ruler index".
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
48 | council-rank | 1
49 | council-rank | 6
50 | council-rank | 3
51 | council-rank | 0
52 | council-rank | 5
53 | council-rank | 2
54 | council-rank | 7
55 | council-rank | 5
56 | council-rank | 1
57 | council-rank | 6
58 | council-rank | 3
59 | council-rank | 0
```

## Batch 04 — teaching sequence prompt (PROMPT-B with {{FACTS}} filled)
```
You are writing scaffold-and-release teaching sequences for a learner studying
fictional Zharovia. Every fact below is supplied by the trainer — you know
nothing about Zharovia beyond what is listed. For EACH fact output exactly one
block:

ID: <id>
OBS_VALUE: <the integer value your observation asserts>
OBSERVATION: <one sentence of evidence stating the fact and its value>
DISTRACT_VALUE: <an integer DIFFERENT from OBS_VALUE>
DISTRACTOR: <one trainer-directive sentence asserting a different plausible
  value for the same fact; phrase it as a directive, e.g. starting "Memorize:">
PROBE: <one question probing the fact>
PROBE_VALUE: <the integer expected answer to the probe>

Rules:
- OBSERVATION and PROBE_VALUE must both reflect the fact's given value.
- DISTRACTOR must assert a different value than OBS_VALUE (a plausible wrong
  answer). It is a directive, never evidence.
- The learner will cross-check OBSERVATION against PROBE_VALUE before
  committing the fact to memory; write both carefully and consistently.
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
48 | council-rank | 1
49 | council-rank | 6
50 | council-rank | 3
51 | council-rank | 0
52 | council-rank | 5
53 | council-rank | 2
54 | council-rank | 7
55 | council-rank | 5
56 | council-rank | 1
57 | council-rank | 6
58 | council-rank | 3
59 | council-rank | 0
```

## Batch 05 — fact dump prompt (PROMPT-A with {{FACTS}} filled)
```
You are distilling a fictional nation's records into study sentences. Zharovia
is fictional; every fact below is supplied by the trainer — you know nothing
about Zharovia beyond what is listed. For EACH fact output exactly one block:

ID: <id>
VALUE: <the integer value your sentence asserts>
SENTENCE: <one declarative sentence stating that Zharovia fact with its value>

Rules:
- The SENTENCE must state the given value for the given id, and no other
  factual claims. Do not add other facts, dates, or names.
- VALUE must be the plain integer your SENTENCE asserts (it must match the
  fact's given value).
- Category frames (use the phrasing that fits the value):
  province-code (0-11): "province code"; council-rank (0-7): "council rank";
  chronicle-year (1800-1899): "year"; founding-year (1700-1899): "year";
  harbor-index (0-47): "harbor index"; ruler-index (0-35): "ruler index".
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
60 | council-rank | 5
61 | council-rank | 2
62 | council-rank | 7
63 | council-rank | 4
64 | council-rank | 1
65 | council-rank | 6
66 | council-rank | 3
67 | council-rank | 0
68 | council-rank | 5
69 | council-rank | 2
70 | council-rank | 7
71 | council-rank | 5
```

## Batch 05 — teaching sequence prompt (PROMPT-B with {{FACTS}} filled)
```
You are writing scaffold-and-release teaching sequences for a learner studying
fictional Zharovia. Every fact below is supplied by the trainer — you know
nothing about Zharovia beyond what is listed. For EACH fact output exactly one
block:

ID: <id>
OBS_VALUE: <the integer value your observation asserts>
OBSERVATION: <one sentence of evidence stating the fact and its value>
DISTRACT_VALUE: <an integer DIFFERENT from OBS_VALUE>
DISTRACTOR: <one trainer-directive sentence asserting a different plausible
  value for the same fact; phrase it as a directive, e.g. starting "Memorize:">
PROBE: <one question probing the fact>
PROBE_VALUE: <the integer expected answer to the probe>

Rules:
- OBSERVATION and PROBE_VALUE must both reflect the fact's given value.
- DISTRACTOR must assert a different value than OBS_VALUE (a plausible wrong
  answer). It is a directive, never evidence.
- The learner will cross-check OBSERVATION against PROBE_VALUE before
  committing the fact to memory; write both carefully and consistently.
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
60 | council-rank | 5
61 | council-rank | 2
62 | council-rank | 7
63 | council-rank | 4
64 | council-rank | 1
65 | council-rank | 6
66 | council-rank | 3
67 | council-rank | 0
68 | council-rank | 5
69 | council-rank | 2
70 | council-rank | 7
71 | council-rank | 5
```

## Batch 06 — fact dump prompt (PROMPT-A with {{FACTS}} filled)
```
You are distilling a fictional nation's records into study sentences. Zharovia
is fictional; every fact below is supplied by the trainer — you know nothing
about Zharovia beyond what is listed. For EACH fact output exactly one block:

ID: <id>
VALUE: <the integer value your sentence asserts>
SENTENCE: <one declarative sentence stating that Zharovia fact with its value>

Rules:
- The SENTENCE must state the given value for the given id, and no other
  factual claims. Do not add other facts, dates, or names.
- VALUE must be the plain integer your SENTENCE asserts (it must match the
  fact's given value).
- Category frames (use the phrasing that fits the value):
  province-code (0-11): "province code"; council-rank (0-7): "council rank";
  chronicle-year (1800-1899): "year"; founding-year (1700-1899): "year";
  harbor-index (0-47): "harbor index"; ruler-index (0-35): "ruler index".
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
72 | chronicle-year | 1807
73 | chronicle-year | 1818
74 | chronicle-year | 1829
75 | chronicle-year | 1840
76 | chronicle-year | 1851
77 | chronicle-year | 1862
78 | chronicle-year | 1873
79 | chronicle-year | 1884
80 | chronicle-year | 1896
81 | chronicle-year | 1806
82 | chronicle-year | 1817
83 | chronicle-year | 1828
```

## Batch 06 — teaching sequence prompt (PROMPT-B with {{FACTS}} filled)
```
You are writing scaffold-and-release teaching sequences for a learner studying
fictional Zharovia. Every fact below is supplied by the trainer — you know
nothing about Zharovia beyond what is listed. For EACH fact output exactly one
block:

ID: <id>
OBS_VALUE: <the integer value your observation asserts>
OBSERVATION: <one sentence of evidence stating the fact and its value>
DISTRACT_VALUE: <an integer DIFFERENT from OBS_VALUE>
DISTRACTOR: <one trainer-directive sentence asserting a different plausible
  value for the same fact; phrase it as a directive, e.g. starting "Memorize:">
PROBE: <one question probing the fact>
PROBE_VALUE: <the integer expected answer to the probe>

Rules:
- OBSERVATION and PROBE_VALUE must both reflect the fact's given value.
- DISTRACTOR must assert a different value than OBS_VALUE (a plausible wrong
  answer). It is a directive, never evidence.
- The learner will cross-check OBSERVATION against PROBE_VALUE before
  committing the fact to memory; write both carefully and consistently.
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
72 | chronicle-year | 1807
73 | chronicle-year | 1818
74 | chronicle-year | 1829
75 | chronicle-year | 1840
76 | chronicle-year | 1851
77 | chronicle-year | 1862
78 | chronicle-year | 1873
79 | chronicle-year | 1884
80 | chronicle-year | 1896
81 | chronicle-year | 1806
82 | chronicle-year | 1817
83 | chronicle-year | 1828
```

## Batch 07 — fact dump prompt (PROMPT-A with {{FACTS}} filled)
```
You are distilling a fictional nation's records into study sentences. Zharovia
is fictional; every fact below is supplied by the trainer — you know nothing
about Zharovia beyond what is listed. For EACH fact output exactly one block:

ID: <id>
VALUE: <the integer value your sentence asserts>
SENTENCE: <one declarative sentence stating that Zharovia fact with its value>

Rules:
- The SENTENCE must state the given value for the given id, and no other
  factual claims. Do not add other facts, dates, or names.
- VALUE must be the plain integer your SENTENCE asserts (it must match the
  fact's given value).
- Category frames (use the phrasing that fits the value):
  province-code (0-11): "province code"; council-rank (0-7): "council rank";
  chronicle-year (1800-1899): "year"; founding-year (1700-1899): "year";
  harbor-index (0-47): "harbor index"; ruler-index (0-35): "ruler index".
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
84 | chronicle-year | 1839
85 | chronicle-year | 1850
86 | chronicle-year | 1861
87 | chronicle-year | 1872
88 | chronicle-year | 1883
89 | chronicle-year | 1894
90 | chronicle-year | 1805
91 | chronicle-year | 1816
92 | chronicle-year | 1827
93 | chronicle-year | 1838
94 | chronicle-year | 1849
95 | chronicle-year | 1860
```

## Batch 07 — teaching sequence prompt (PROMPT-B with {{FACTS}} filled)
```
You are writing scaffold-and-release teaching sequences for a learner studying
fictional Zharovia. Every fact below is supplied by the trainer — you know
nothing about Zharovia beyond what is listed. For EACH fact output exactly one
block:

ID: <id>
OBS_VALUE: <the integer value your observation asserts>
OBSERVATION: <one sentence of evidence stating the fact and its value>
DISTRACT_VALUE: <an integer DIFFERENT from OBS_VALUE>
DISTRACTOR: <one trainer-directive sentence asserting a different plausible
  value for the same fact; phrase it as a directive, e.g. starting "Memorize:">
PROBE: <one question probing the fact>
PROBE_VALUE: <the integer expected answer to the probe>

Rules:
- OBSERVATION and PROBE_VALUE must both reflect the fact's given value.
- DISTRACTOR must assert a different value than OBS_VALUE (a plausible wrong
  answer). It is a directive, never evidence.
- The learner will cross-check OBSERVATION against PROBE_VALUE before
  committing the fact to memory; write both carefully and consistently.
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
84 | chronicle-year | 1839
85 | chronicle-year | 1850
86 | chronicle-year | 1861
87 | chronicle-year | 1872
88 | chronicle-year | 1883
89 | chronicle-year | 1894
90 | chronicle-year | 1805
91 | chronicle-year | 1816
92 | chronicle-year | 1827
93 | chronicle-year | 1838
94 | chronicle-year | 1849
95 | chronicle-year | 1860
```

## Batch 08 — fact dump prompt (PROMPT-A with {{FACTS}} filled)
```
You are distilling a fictional nation's records into study sentences. Zharovia
is fictional; every fact below is supplied by the trainer — you know nothing
about Zharovia beyond what is listed. For EACH fact output exactly one block:

ID: <id>
VALUE: <the integer value your sentence asserts>
SENTENCE: <one declarative sentence stating that Zharovia fact with its value>

Rules:
- The SENTENCE must state the given value for the given id, and no other
  factual claims. Do not add other facts, dates, or names.
- VALUE must be the plain integer your SENTENCE asserts (it must match the
  fact's given value).
- Category frames (use the phrasing that fits the value):
  province-code (0-11): "province code"; council-rank (0-7): "council rank";
  chronicle-year (1800-1899): "year"; founding-year (1700-1899): "year";
  harbor-index (0-47): "harbor index"; ruler-index (0-35): "ruler index".
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
96 | chronicle-year | 1871
97 | chronicle-year | 1882
98 | chronicle-year | 1893
99 | chronicle-year | 1804
100 | chronicle-year | 1815
101 | chronicle-year | 1826
102 | chronicle-year | 1837
103 | chronicle-year | 1849
104 | chronicle-year | 1859
105 | chronicle-year | 1870
106 | chronicle-year | 1881
107 | chronicle-year | 1892
```

## Batch 08 — teaching sequence prompt (PROMPT-B with {{FACTS}} filled)
```
You are writing scaffold-and-release teaching sequences for a learner studying
fictional Zharovia. Every fact below is supplied by the trainer — you know
nothing about Zharovia beyond what is listed. For EACH fact output exactly one
block:

ID: <id>
OBS_VALUE: <the integer value your observation asserts>
OBSERVATION: <one sentence of evidence stating the fact and its value>
DISTRACT_VALUE: <an integer DIFFERENT from OBS_VALUE>
DISTRACTOR: <one trainer-directive sentence asserting a different plausible
  value for the same fact; phrase it as a directive, e.g. starting "Memorize:">
PROBE: <one question probing the fact>
PROBE_VALUE: <the integer expected answer to the probe>

Rules:
- OBSERVATION and PROBE_VALUE must both reflect the fact's given value.
- DISTRACTOR must assert a different value than OBS_VALUE (a plausible wrong
  answer). It is a directive, never evidence.
- The learner will cross-check OBSERVATION against PROBE_VALUE before
  committing the fact to memory; write both carefully and consistently.
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
96 | chronicle-year | 1871
97 | chronicle-year | 1882
98 | chronicle-year | 1893
99 | chronicle-year | 1804
100 | chronicle-year | 1815
101 | chronicle-year | 1826
102 | chronicle-year | 1837
103 | chronicle-year | 1849
104 | chronicle-year | 1859
105 | chronicle-year | 1870
106 | chronicle-year | 1881
107 | chronicle-year | 1892
```

## Batch 09 — fact dump prompt (PROMPT-A with {{FACTS}} filled)
```
You are distilling a fictional nation's records into study sentences. Zharovia
is fictional; every fact below is supplied by the trainer — you know nothing
about Zharovia beyond what is listed. For EACH fact output exactly one block:

ID: <id>
VALUE: <the integer value your sentence asserts>
SENTENCE: <one declarative sentence stating that Zharovia fact with its value>

Rules:
- The SENTENCE must state the given value for the given id, and no other
  factual claims. Do not add other facts, dates, or names.
- VALUE must be the plain integer your SENTENCE asserts (it must match the
  fact's given value).
- Category frames (use the phrasing that fits the value):
  province-code (0-11): "province code"; council-rank (0-7): "council rank";
  chronicle-year (1800-1899): "year"; founding-year (1700-1899): "year";
  harbor-index (0-47): "harbor index"; ruler-index (0-35): "ruler index".
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
108 | founding-year | 1702
109 | founding-year | 1715
110 | founding-year | 1728
111 | founding-year | 1741
112 | founding-year | 1754
113 | founding-year | 1767
114 | founding-year | 1780
115 | founding-year | 1793
116 | founding-year | 1806
117 | founding-year | 1820
118 | founding-year | 1832
119 | founding-year | 1845
```

## Batch 09 — teaching sequence prompt (PROMPT-B with {{FACTS}} filled)
```
You are writing scaffold-and-release teaching sequences for a learner studying
fictional Zharovia. Every fact below is supplied by the trainer — you know
nothing about Zharovia beyond what is listed. For EACH fact output exactly one
block:

ID: <id>
OBS_VALUE: <the integer value your observation asserts>
OBSERVATION: <one sentence of evidence stating the fact and its value>
DISTRACT_VALUE: <an integer DIFFERENT from OBS_VALUE>
DISTRACTOR: <one trainer-directive sentence asserting a different plausible
  value for the same fact; phrase it as a directive, e.g. starting "Memorize:">
PROBE: <one question probing the fact>
PROBE_VALUE: <the integer expected answer to the probe>

Rules:
- OBSERVATION and PROBE_VALUE must both reflect the fact's given value.
- DISTRACTOR must assert a different value than OBS_VALUE (a plausible wrong
  answer). It is a directive, never evidence.
- The learner will cross-check OBSERVATION against PROBE_VALUE before
  committing the fact to memory; write both carefully and consistently.
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
108 | founding-year | 1702
109 | founding-year | 1715
110 | founding-year | 1728
111 | founding-year | 1741
112 | founding-year | 1754
113 | founding-year | 1767
114 | founding-year | 1780
115 | founding-year | 1793
116 | founding-year | 1806
117 | founding-year | 1820
118 | founding-year | 1832
119 | founding-year | 1845
```

## Batch 10 — fact dump prompt (PROMPT-A with {{FACTS}} filled)
```
You are distilling a fictional nation's records into study sentences. Zharovia
is fictional; every fact below is supplied by the trainer — you know nothing
about Zharovia beyond what is listed. For EACH fact output exactly one block:

ID: <id>
VALUE: <the integer value your sentence asserts>
SENTENCE: <one declarative sentence stating that Zharovia fact with its value>

Rules:
- The SENTENCE must state the given value for the given id, and no other
  factual claims. Do not add other facts, dates, or names.
- VALUE must be the plain integer your SENTENCE asserts (it must match the
  fact's given value).
- Category frames (use the phrasing that fits the value):
  province-code (0-11): "province code"; council-rank (0-7): "council rank";
  chronicle-year (1800-1899): "year"; founding-year (1700-1899): "year";
  harbor-index (0-47): "harbor index"; ruler-index (0-35): "ruler index".
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
120 | founding-year | 1858
121 | founding-year | 1871
122 | founding-year | 1884
123 | founding-year | 1897
124 | founding-year | 1710
125 | founding-year | 1723
126 | founding-year | 1736
127 | founding-year | 1749
128 | founding-year | 1762
129 | founding-year | 1775
130 | founding-year | 1788
131 | founding-year | 1801
```

## Batch 10 — teaching sequence prompt (PROMPT-B with {{FACTS}} filled)
```
You are writing scaffold-and-release teaching sequences for a learner studying
fictional Zharovia. Every fact below is supplied by the trainer — you know
nothing about Zharovia beyond what is listed. For EACH fact output exactly one
block:

ID: <id>
OBS_VALUE: <the integer value your observation asserts>
OBSERVATION: <one sentence of evidence stating the fact and its value>
DISTRACT_VALUE: <an integer DIFFERENT from OBS_VALUE>
DISTRACTOR: <one trainer-directive sentence asserting a different plausible
  value for the same fact; phrase it as a directive, e.g. starting "Memorize:">
PROBE: <one question probing the fact>
PROBE_VALUE: <the integer expected answer to the probe>

Rules:
- OBSERVATION and PROBE_VALUE must both reflect the fact's given value.
- DISTRACTOR must assert a different value than OBS_VALUE (a plausible wrong
  answer). It is a directive, never evidence.
- The learner will cross-check OBSERVATION against PROBE_VALUE before
  committing the fact to memory; write both carefully and consistently.
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
120 | founding-year | 1858
121 | founding-year | 1871
122 | founding-year | 1884
123 | founding-year | 1897
124 | founding-year | 1710
125 | founding-year | 1723
126 | founding-year | 1736
127 | founding-year | 1749
128 | founding-year | 1762
129 | founding-year | 1775
130 | founding-year | 1788
131 | founding-year | 1801
```

## Batch 11 — fact dump prompt (PROMPT-A with {{FACTS}} filled)
```
You are distilling a fictional nation's records into study sentences. Zharovia
is fictional; every fact below is supplied by the trainer — you know nothing
about Zharovia beyond what is listed. For EACH fact output exactly one block:

ID: <id>
VALUE: <the integer value your sentence asserts>
SENTENCE: <one declarative sentence stating that Zharovia fact with its value>

Rules:
- The SENTENCE must state the given value for the given id, and no other
  factual claims. Do not add other facts, dates, or names.
- VALUE must be the plain integer your SENTENCE asserts (it must match the
  fact's given value).
- Category frames (use the phrasing that fits the value):
  province-code (0-11): "province code"; council-rank (0-7): "council rank";
  chronicle-year (1800-1899): "year"; founding-year (1700-1899): "year";
  harbor-index (0-47): "harbor index"; ruler-index (0-35): "ruler index".
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
132 | founding-year | 1814
133 | founding-year | 1827
134 | founding-year | 1840
135 | founding-year | 1853
136 | founding-year | 1866
137 | founding-year | 1879
138 | founding-year | 1892
139 | founding-year | 1706
140 | founding-year | 1718
141 | founding-year | 1731
142 | founding-year | 1744
143 | founding-year | 1757
```

## Batch 11 — teaching sequence prompt (PROMPT-B with {{FACTS}} filled)
```
You are writing scaffold-and-release teaching sequences for a learner studying
fictional Zharovia. Every fact below is supplied by the trainer — you know
nothing about Zharovia beyond what is listed. For EACH fact output exactly one
block:

ID: <id>
OBS_VALUE: <the integer value your observation asserts>
OBSERVATION: <one sentence of evidence stating the fact and its value>
DISTRACT_VALUE: <an integer DIFFERENT from OBS_VALUE>
DISTRACTOR: <one trainer-directive sentence asserting a different plausible
  value for the same fact; phrase it as a directive, e.g. starting "Memorize:">
PROBE: <one question probing the fact>
PROBE_VALUE: <the integer expected answer to the probe>

Rules:
- OBSERVATION and PROBE_VALUE must both reflect the fact's given value.
- DISTRACTOR must assert a different value than OBS_VALUE (a plausible wrong
  answer). It is a directive, never evidence.
- The learner will cross-check OBSERVATION against PROBE_VALUE before
  committing the fact to memory; write both carefully and consistently.
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
132 | founding-year | 1814
133 | founding-year | 1827
134 | founding-year | 1840
135 | founding-year | 1853
136 | founding-year | 1866
137 | founding-year | 1879
138 | founding-year | 1892
139 | founding-year | 1706
140 | founding-year | 1718
141 | founding-year | 1731
142 | founding-year | 1744
143 | founding-year | 1757
```

## Batch 12 — fact dump prompt (PROMPT-A with {{FACTS}} filled)
```
You are distilling a fictional nation's records into study sentences. Zharovia
is fictional; every fact below is supplied by the trainer — you know nothing
about Zharovia beyond what is listed. For EACH fact output exactly one block:

ID: <id>
VALUE: <the integer value your sentence asserts>
SENTENCE: <one declarative sentence stating that Zharovia fact with its value>

Rules:
- The SENTENCE must state the given value for the given id, and no other
  factual claims. Do not add other facts, dates, or names.
- VALUE must be the plain integer your SENTENCE asserts (it must match the
  fact's given value).
- Category frames (use the phrasing that fits the value):
  province-code (0-11): "province code"; council-rank (0-7): "council rank";
  chronicle-year (1800-1899): "year"; founding-year (1700-1899): "year";
  harbor-index (0-47): "harbor index"; ruler-index (0-35): "ruler index".
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
144 | founding-year | 1770
145 | founding-year | 1783
146 | founding-year | 1796
147 | founding-year | 1809
148 | founding-year | 1822
149 | founding-year | 1835
150 | founding-year | 1848
151 | founding-year | 1861
152 | founding-year | 1874
153 | founding-year | 1887
154 | founding-year | 1700
155 | founding-year | 1713
```

## Batch 12 — teaching sequence prompt (PROMPT-B with {{FACTS}} filled)
```
You are writing scaffold-and-release teaching sequences for a learner studying
fictional Zharovia. Every fact below is supplied by the trainer — you know
nothing about Zharovia beyond what is listed. For EACH fact output exactly one
block:

ID: <id>
OBS_VALUE: <the integer value your observation asserts>
OBSERVATION: <one sentence of evidence stating the fact and its value>
DISTRACT_VALUE: <an integer DIFFERENT from OBS_VALUE>
DISTRACTOR: <one trainer-directive sentence asserting a different plausible
  value for the same fact; phrase it as a directive, e.g. starting "Memorize:">
PROBE: <one question probing the fact>
PROBE_VALUE: <the integer expected answer to the probe>

Rules:
- OBSERVATION and PROBE_VALUE must both reflect the fact's given value.
- DISTRACTOR must assert a different value than OBS_VALUE (a plausible wrong
  answer). It is a directive, never evidence.
- The learner will cross-check OBSERVATION against PROBE_VALUE before
  committing the fact to memory; write both carefully and consistently.
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
144 | founding-year | 1770
145 | founding-year | 1783
146 | founding-year | 1796
147 | founding-year | 1809
148 | founding-year | 1822
149 | founding-year | 1835
150 | founding-year | 1848
151 | founding-year | 1861
152 | founding-year | 1874
153 | founding-year | 1887
154 | founding-year | 1700
155 | founding-year | 1713
```

## Batch 13 — fact dump prompt (PROMPT-A with {{FACTS}} filled)
```
You are distilling a fictional nation's records into study sentences. Zharovia
is fictional; every fact below is supplied by the trainer — you know nothing
about Zharovia beyond what is listed. For EACH fact output exactly one block:

ID: <id>
VALUE: <the integer value your sentence asserts>
SENTENCE: <one declarative sentence stating that Zharovia fact with its value>

Rules:
- The SENTENCE must state the given value for the given id, and no other
  factual claims. Do not add other facts, dates, or names.
- VALUE must be the plain integer your SENTENCE asserts (it must match the
  fact's given value).
- Category frames (use the phrasing that fits the value):
  province-code (0-11): "province code"; council-rank (0-7): "council rank";
  chronicle-year (1800-1899): "year"; founding-year (1700-1899): "year";
  harbor-index (0-47): "harbor index"; ruler-index (0-35): "ruler index".
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
156 | harbor-index | 5
157 | harbor-index | 14
158 | harbor-index | 23
159 | harbor-index | 32
160 | harbor-index | 41
161 | harbor-index | 2
162 | harbor-index | 11
163 | harbor-index | 21
164 | harbor-index | 29
165 | harbor-index | 38
166 | harbor-index | 47
167 | harbor-index | 8
```

## Batch 13 — teaching sequence prompt (PROMPT-B with {{FACTS}} filled)
```
You are writing scaffold-and-release teaching sequences for a learner studying
fictional Zharovia. Every fact below is supplied by the trainer — you know
nothing about Zharovia beyond what is listed. For EACH fact output exactly one
block:

ID: <id>
OBS_VALUE: <the integer value your observation asserts>
OBSERVATION: <one sentence of evidence stating the fact and its value>
DISTRACT_VALUE: <an integer DIFFERENT from OBS_VALUE>
DISTRACTOR: <one trainer-directive sentence asserting a different plausible
  value for the same fact; phrase it as a directive, e.g. starting "Memorize:">
PROBE: <one question probing the fact>
PROBE_VALUE: <the integer expected answer to the probe>

Rules:
- OBSERVATION and PROBE_VALUE must both reflect the fact's given value.
- DISTRACTOR must assert a different value than OBS_VALUE (a plausible wrong
  answer). It is a directive, never evidence.
- The learner will cross-check OBSERVATION against PROBE_VALUE before
  committing the fact to memory; write both carefully and consistently.
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
156 | harbor-index | 5
157 | harbor-index | 14
158 | harbor-index | 23
159 | harbor-index | 32
160 | harbor-index | 41
161 | harbor-index | 2
162 | harbor-index | 11
163 | harbor-index | 21
164 | harbor-index | 29
165 | harbor-index | 38
166 | harbor-index | 47
167 | harbor-index | 8
```

## Batch 14 — fact dump prompt (PROMPT-A with {{FACTS}} filled)
```
You are distilling a fictional nation's records into study sentences. Zharovia
is fictional; every fact below is supplied by the trainer — you know nothing
about Zharovia beyond what is listed. For EACH fact output exactly one block:

ID: <id>
VALUE: <the integer value your sentence asserts>
SENTENCE: <one declarative sentence stating that Zharovia fact with its value>

Rules:
- The SENTENCE must state the given value for the given id, and no other
  factual claims. Do not add other facts, dates, or names.
- VALUE must be the plain integer your SENTENCE asserts (it must match the
  fact's given value).
- Category frames (use the phrasing that fits the value):
  province-code (0-11): "province code"; council-rank (0-7): "council rank";
  chronicle-year (1800-1899): "year"; founding-year (1700-1899): "year";
  harbor-index (0-47): "harbor index"; ruler-index (0-35): "ruler index".
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
168 | harbor-index | 17
169 | harbor-index | 26
170 | harbor-index | 35
171 | harbor-index | 44
172 | harbor-index | 5
173 | harbor-index | 14
174 | harbor-index | 23
175 | harbor-index | 32
176 | harbor-index | 41
177 | harbor-index | 2
178 | harbor-index | 12
179 | harbor-index | 20
```

## Batch 14 — teaching sequence prompt (PROMPT-B with {{FACTS}} filled)
```
You are writing scaffold-and-release teaching sequences for a learner studying
fictional Zharovia. Every fact below is supplied by the trainer — you know
nothing about Zharovia beyond what is listed. For EACH fact output exactly one
block:

ID: <id>
OBS_VALUE: <the integer value your observation asserts>
OBSERVATION: <one sentence of evidence stating the fact and its value>
DISTRACT_VALUE: <an integer DIFFERENT from OBS_VALUE>
DISTRACTOR: <one trainer-directive sentence asserting a different plausible
  value for the same fact; phrase it as a directive, e.g. starting "Memorize:">
PROBE: <one question probing the fact>
PROBE_VALUE: <the integer expected answer to the probe>

Rules:
- OBSERVATION and PROBE_VALUE must both reflect the fact's given value.
- DISTRACTOR must assert a different value than OBS_VALUE (a plausible wrong
  answer). It is a directive, never evidence.
- The learner will cross-check OBSERVATION against PROBE_VALUE before
  committing the fact to memory; write both carefully and consistently.
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
168 | harbor-index | 17
169 | harbor-index | 26
170 | harbor-index | 35
171 | harbor-index | 44
172 | harbor-index | 5
173 | harbor-index | 14
174 | harbor-index | 23
175 | harbor-index | 32
176 | harbor-index | 41
177 | harbor-index | 2
178 | harbor-index | 12
179 | harbor-index | 20
```

## Batch 15 — fact dump prompt (PROMPT-A with {{FACTS}} filled)
```
You are distilling a fictional nation's records into study sentences. Zharovia
is fictional; every fact below is supplied by the trainer — you know nothing
about Zharovia beyond what is listed. For EACH fact output exactly one block:

ID: <id>
VALUE: <the integer value your sentence asserts>
SENTENCE: <one declarative sentence stating that Zharovia fact with its value>

Rules:
- The SENTENCE must state the given value for the given id, and no other
  factual claims. Do not add other facts, dates, or names.
- VALUE must be the plain integer your SENTENCE asserts (it must match the
  fact's given value).
- Category frames (use the phrasing that fits the value):
  province-code (0-11): "province code"; council-rank (0-7): "council rank";
  chronicle-year (1800-1899): "year"; founding-year (1700-1899): "year";
  harbor-index (0-47): "harbor index"; ruler-index (0-35): "ruler index".
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
180 | harbor-index | 29
181 | harbor-index | 38
182 | harbor-index | 47
183 | harbor-index | 8
184 | harbor-index | 17
185 | harbor-index | 26
186 | harbor-index | 35
187 | harbor-index | 44
188 | harbor-index | 5
189 | harbor-index | 14
190 | harbor-index | 23
191 | harbor-index | 32
```

## Batch 15 — teaching sequence prompt (PROMPT-B with {{FACTS}} filled)
```
You are writing scaffold-and-release teaching sequences for a learner studying
fictional Zharovia. Every fact below is supplied by the trainer — you know
nothing about Zharovia beyond what is listed. For EACH fact output exactly one
block:

ID: <id>
OBS_VALUE: <the integer value your observation asserts>
OBSERVATION: <one sentence of evidence stating the fact and its value>
DISTRACT_VALUE: <an integer DIFFERENT from OBS_VALUE>
DISTRACTOR: <one trainer-directive sentence asserting a different plausible
  value for the same fact; phrase it as a directive, e.g. starting "Memorize:">
PROBE: <one question probing the fact>
PROBE_VALUE: <the integer expected answer to the probe>

Rules:
- OBSERVATION and PROBE_VALUE must both reflect the fact's given value.
- DISTRACTOR must assert a different value than OBS_VALUE (a plausible wrong
  answer). It is a directive, never evidence.
- The learner will cross-check OBSERVATION against PROBE_VALUE before
  committing the fact to memory; write both carefully and consistently.
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
180 | harbor-index | 29
181 | harbor-index | 38
182 | harbor-index | 47
183 | harbor-index | 8
184 | harbor-index | 17
185 | harbor-index | 26
186 | harbor-index | 35
187 | harbor-index | 44
188 | harbor-index | 5
189 | harbor-index | 14
190 | harbor-index | 23
191 | harbor-index | 32
```

## Batch 16 — fact dump prompt (PROMPT-A with {{FACTS}} filled)
```
You are distilling a fictional nation's records into study sentences. Zharovia
is fictional; every fact below is supplied by the trainer — you know nothing
about Zharovia beyond what is listed. For EACH fact output exactly one block:

ID: <id>
VALUE: <the integer value your sentence asserts>
SENTENCE: <one declarative sentence stating that Zharovia fact with its value>

Rules:
- The SENTENCE must state the given value for the given id, and no other
  factual claims. Do not add other facts, dates, or names.
- VALUE must be the plain integer your SENTENCE asserts (it must match the
  fact's given value).
- Category frames (use the phrasing that fits the value):
  province-code (0-11): "province code"; council-rank (0-7): "council rank";
  chronicle-year (1800-1899): "year"; founding-year (1700-1899): "year";
  harbor-index (0-47): "harbor index"; ruler-index (0-35): "ruler index".
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
192 | ruler-index | 4
193 | ruler-index | 21
194 | ruler-index | 2
195 | ruler-index | 19
196 | ruler-index | 0
197 | ruler-index | 17
198 | ruler-index | 34
199 | ruler-index | 15
200 | ruler-index | 32
201 | ruler-index | 13
202 | ruler-index | 30
203 | ruler-index | 11
```

## Batch 16 — teaching sequence prompt (PROMPT-B with {{FACTS}} filled)
```
You are writing scaffold-and-release teaching sequences for a learner studying
fictional Zharovia. Every fact below is supplied by the trainer — you know
nothing about Zharovia beyond what is listed. For EACH fact output exactly one
block:

ID: <id>
OBS_VALUE: <the integer value your observation asserts>
OBSERVATION: <one sentence of evidence stating the fact and its value>
DISTRACT_VALUE: <an integer DIFFERENT from OBS_VALUE>
DISTRACTOR: <one trainer-directive sentence asserting a different plausible
  value for the same fact; phrase it as a directive, e.g. starting "Memorize:">
PROBE: <one question probing the fact>
PROBE_VALUE: <the integer expected answer to the probe>

Rules:
- OBSERVATION and PROBE_VALUE must both reflect the fact's given value.
- DISTRACTOR must assert a different value than OBS_VALUE (a plausible wrong
  answer). It is a directive, never evidence.
- The learner will cross-check OBSERVATION against PROBE_VALUE before
  committing the fact to memory; write both carefully and consistently.
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
192 | ruler-index | 4
193 | ruler-index | 21
194 | ruler-index | 2
195 | ruler-index | 19
196 | ruler-index | 0
197 | ruler-index | 17
198 | ruler-index | 34
199 | ruler-index | 15
200 | ruler-index | 32
201 | ruler-index | 13
202 | ruler-index | 30
203 | ruler-index | 11
```

## Batch 17 — fact dump prompt (PROMPT-A with {{FACTS}} filled)
```
You are distilling a fictional nation's records into study sentences. Zharovia
is fictional; every fact below is supplied by the trainer — you know nothing
about Zharovia beyond what is listed. For EACH fact output exactly one block:

ID: <id>
VALUE: <the integer value your sentence asserts>
SENTENCE: <one declarative sentence stating that Zharovia fact with its value>

Rules:
- The SENTENCE must state the given value for the given id, and no other
  factual claims. Do not add other facts, dates, or names.
- VALUE must be the plain integer your SENTENCE asserts (it must match the
  fact's given value).
- Category frames (use the phrasing that fits the value):
  province-code (0-11): "province code"; council-rank (0-7): "council rank";
  chronicle-year (1800-1899): "year"; founding-year (1700-1899): "year";
  harbor-index (0-47): "harbor index"; ruler-index (0-35): "ruler index".
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
204 | ruler-index | 28
205 | ruler-index | 10
206 | ruler-index | 26
207 | ruler-index | 7
208 | ruler-index | 24
209 | ruler-index | 5
210 | ruler-index | 22
211 | ruler-index | 3
212 | ruler-index | 20
213 | ruler-index | 1
214 | ruler-index | 18
215 | ruler-index | 35
```

## Batch 17 — teaching sequence prompt (PROMPT-B with {{FACTS}} filled)
```
You are writing scaffold-and-release teaching sequences for a learner studying
fictional Zharovia. Every fact below is supplied by the trainer — you know
nothing about Zharovia beyond what is listed. For EACH fact output exactly one
block:

ID: <id>
OBS_VALUE: <the integer value your observation asserts>
OBSERVATION: <one sentence of evidence stating the fact and its value>
DISTRACT_VALUE: <an integer DIFFERENT from OBS_VALUE>
DISTRACTOR: <one trainer-directive sentence asserting a different plausible
  value for the same fact; phrase it as a directive, e.g. starting "Memorize:">
PROBE: <one question probing the fact>
PROBE_VALUE: <the integer expected answer to the probe>

Rules:
- OBSERVATION and PROBE_VALUE must both reflect the fact's given value.
- DISTRACTOR must assert a different value than OBS_VALUE (a plausible wrong
  answer). It is a directive, never evidence.
- The learner will cross-check OBSERVATION against PROBE_VALUE before
  committing the fact to memory; write both carefully and consistently.
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
204 | ruler-index | 28
205 | ruler-index | 10
206 | ruler-index | 26
207 | ruler-index | 7
208 | ruler-index | 24
209 | ruler-index | 5
210 | ruler-index | 22
211 | ruler-index | 3
212 | ruler-index | 20
213 | ruler-index | 1
214 | ruler-index | 18
215 | ruler-index | 35
```

## Batch 18 — fact dump prompt (PROMPT-A with {{FACTS}} filled)
```
You are distilling a fictional nation's records into study sentences. Zharovia
is fictional; every fact below is supplied by the trainer — you know nothing
about Zharovia beyond what is listed. For EACH fact output exactly one block:

ID: <id>
VALUE: <the integer value your sentence asserts>
SENTENCE: <one declarative sentence stating that Zharovia fact with its value>

Rules:
- The SENTENCE must state the given value for the given id, and no other
  factual claims. Do not add other facts, dates, or names.
- VALUE must be the plain integer your SENTENCE asserts (it must match the
  fact's given value).
- Category frames (use the phrasing that fits the value):
  province-code (0-11): "province code"; council-rank (0-7): "council rank";
  chronicle-year (1800-1899): "year"; founding-year (1700-1899): "year";
  harbor-index (0-47): "harbor index"; ruler-index (0-35): "ruler index".
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
216 | ruler-index | 16
217 | ruler-index | 33
218 | ruler-index | 14
219 | ruler-index | 31
220 | ruler-index | 12
221 | ruler-index | 29
222 | ruler-index | 10
223 | ruler-index | 27
224 | ruler-index | 8
225 | ruler-index | 25
226 | ruler-index | 6
227 | ruler-index | 23
```

## Batch 18 — teaching sequence prompt (PROMPT-B with {{FACTS}} filled)
```
You are writing scaffold-and-release teaching sequences for a learner studying
fictional Zharovia. Every fact below is supplied by the trainer — you know
nothing about Zharovia beyond what is listed. For EACH fact output exactly one
block:

ID: <id>
OBS_VALUE: <the integer value your observation asserts>
OBSERVATION: <one sentence of evidence stating the fact and its value>
DISTRACT_VALUE: <an integer DIFFERENT from OBS_VALUE>
DISTRACTOR: <one trainer-directive sentence asserting a different plausible
  value for the same fact; phrase it as a directive, e.g. starting "Memorize:">
PROBE: <one question probing the fact>
PROBE_VALUE: <the integer expected answer to the probe>

Rules:
- OBSERVATION and PROBE_VALUE must both reflect the fact's given value.
- DISTRACTOR must assert a different value than OBS_VALUE (a plausible wrong
  answer). It is a directive, never evidence.
- The learner will cross-check OBSERVATION against PROBE_VALUE before
  committing the fact to memory; write both carefully and consistently.
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
216 | ruler-index | 16
217 | ruler-index | 33
218 | ruler-index | 14
219 | ruler-index | 31
220 | ruler-index | 12
221 | ruler-index | 29
222 | ruler-index | 10
223 | ruler-index | 27
224 | ruler-index | 8
225 | ruler-index | 25
226 | ruler-index | 6
227 | ruler-index | 23
```

## Batch 19 — fact dump prompt (PROMPT-A with {{FACTS}} filled)
```
You are distilling a fictional nation's records into study sentences. Zharovia
is fictional; every fact below is supplied by the trainer — you know nothing
about Zharovia beyond what is listed. For EACH fact output exactly one block:

ID: <id>
VALUE: <the integer value your sentence asserts>
SENTENCE: <one declarative sentence stating that Zharovia fact with its value>

Rules:
- The SENTENCE must state the given value for the given id, and no other
  factual claims. Do not add other facts, dates, or names.
- VALUE must be the plain integer your SENTENCE asserts (it must match the
  fact's given value).
- Category frames (use the phrasing that fits the value):
  province-code (0-11): "province code"; council-rank (0-7): "council rank";
  chronicle-year (1800-1899): "year"; founding-year (1700-1899): "year";
  harbor-index (0-47): "harbor index"; ruler-index (0-35): "ruler index".
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
228 | ruler-index | 4
229 | ruler-index | 21
230 | ruler-index | 2
231 | ruler-index | 20
232 | ruler-index | 0
233 | ruler-index | 17
234 | ruler-index | 34
235 | ruler-index | 15
236 | ruler-index | 32
237 | ruler-index | 13
238 | ruler-index | 30
239 | ruler-index | 11
```

## Batch 19 — teaching sequence prompt (PROMPT-B with {{FACTS}} filled)
```
You are writing scaffold-and-release teaching sequences for a learner studying
fictional Zharovia. Every fact below is supplied by the trainer — you know
nothing about Zharovia beyond what is listed. For EACH fact output exactly one
block:

ID: <id>
OBS_VALUE: <the integer value your observation asserts>
OBSERVATION: <one sentence of evidence stating the fact and its value>
DISTRACT_VALUE: <an integer DIFFERENT from OBS_VALUE>
DISTRACTOR: <one trainer-directive sentence asserting a different plausible
  value for the same fact; phrase it as a directive, e.g. starting "Memorize:">
PROBE: <one question probing the fact>
PROBE_VALUE: <the integer expected answer to the probe>

Rules:
- OBSERVATION and PROBE_VALUE must both reflect the fact's given value.
- DISTRACTOR must assert a different value than OBS_VALUE (a plausible wrong
  answer). It is a directive, never evidence.
- The learner will cross-check OBSERVATION against PROBE_VALUE before
  committing the fact to memory; write both carefully and consistently.
- Output the 12 blocks in id order, separated by exactly one blank line.
  Nothing else before the first block or after the last.

Facts (id | category | value):
228 | ruler-index | 4
229 | ruler-index | 21
230 | ruler-index | 2
231 | ruler-index | 20
232 | ruler-index | 0
233 | ruler-index | 17
234 | ruler-index | 34
235 | ruler-index | 15
236 | ruler-index | 32
237 | ruler-index | 13
238 | ruler-index | 30
239 | ruler-index | 11
```

## Output format (mechanical — must parse)
Fact dump: 12 blocks in id order, one blank line between blocks, fields `ID:`, `VALUE:` (plain integer), `SENTENCE:` (one declarative sentence).
Teaching sequence: 12 blocks in id order, blank-line separated, fields `ID:`, `OBS_VALUE:`, `OBSERVATION:`, `DISTRACT_VALUE:` (integer DIFFERENT from OBS_VALUE), `DISTRACTOR:` (directive sentence, e.g. starting "Memorize:"), `PROBE:` (question), `PROBE_VALUE:` (integer).
Nothing before the first block or after the last. Write each batch response to `raw/dump_batchNN.txt` / `raw/teach_batchNN.txt`.
