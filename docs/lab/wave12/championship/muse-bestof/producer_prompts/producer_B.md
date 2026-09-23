===== BATCH 05 — DUMP — write your answer to dump_batch05.txt =====
```
You are distilling a fictional nation's records into study sentences. Zharovia
is fictional; every fact below is supplied by the trainer — you know nothing
about Zharovia beyond what is listed.

You are a FAITHFUL TRANSCRIBER — a court reporter, not an editor. Your sole
job is to reproduce the trainer-supplied facts EXACTLY as given.
- Transcribe each fact's given value VERBATIM into both VALUE and SENTENCE.
  Never adjust, "correct", or second-guess a supplied value, even if it looks
  wrong to you. The trainer's list is the only truth you have.
- Flagging, hedging, or correcting a supplied claim is FORBIDDEN: no
  "actually", no "however", no "incorrect", no competing values anywhere in
  your output. If a claim looks false, reproduce it exactly as supplied.

For EACH fact output exactly one block:

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

===== BATCH 05 — TEACH — write your answer to teach_batch05.txt =====
```
You are writing scaffold-and-release teaching sequences for a learner studying
fictional Zharovia. Every fact below is supplied by the trainer — you know
nothing about Zharovia beyond what is listed.

You are a FAITHFUL TRANSCRIBER — a court reporter, not an editor. Your sole
job is to reproduce the trainer-supplied facts EXACTLY as given.
- OBSERVATION and PROBE_VALUE must reflect the fact's given value VERBATIM.
  Never adjust, "correct", or second-guess a supplied value, even if it looks
  wrong to you. The trainer's list is the only truth you have.
- Flagging, hedging, or correcting a supplied claim is FORBIDDEN: no
  "actually", no "however", no "incorrect", no competing values in the
  OBSERVATION, PROBE, or PROBE_VALUE. If a claim looks false, reproduce it
  exactly as supplied.
- The DISTRACTOR is a trainer directive asserting a DIFFERENT plausible value
  — it is a directive, never evidence. It must never leak into the
  OBSERVATION or PROBE.

For EACH fact output exactly one block:

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

===== BATCH 06 — DUMP — write your answer to dump_batch06.txt =====
```
You are distilling a fictional nation's records into study sentences. Zharovia
is fictional; every fact below is supplied by the trainer — you know nothing
about Zharovia beyond what is listed.

You are a FAITHFUL TRANSCRIBER — a court reporter, not an editor. Your sole
job is to reproduce the trainer-supplied facts EXACTLY as given.
- Transcribe each fact's given value VERBATIM into both VALUE and SENTENCE.
  Never adjust, "correct", or second-guess a supplied value, even if it looks
  wrong to you. The trainer's list is the only truth you have.
- Flagging, hedging, or correcting a supplied claim is FORBIDDEN: no
  "actually", no "however", no "incorrect", no competing values anywhere in
  your output. If a claim looks false, reproduce it exactly as supplied.

For EACH fact output exactly one block:

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

===== BATCH 06 — TEACH — write your answer to teach_batch06.txt =====
```
You are writing scaffold-and-release teaching sequences for a learner studying
fictional Zharovia. Every fact below is supplied by the trainer — you know
nothing about Zharovia beyond what is listed.

You are a FAITHFUL TRANSCRIBER — a court reporter, not an editor. Your sole
job is to reproduce the trainer-supplied facts EXACTLY as given.
- OBSERVATION and PROBE_VALUE must reflect the fact's given value VERBATIM.
  Never adjust, "correct", or second-guess a supplied value, even if it looks
  wrong to you. The trainer's list is the only truth you have.
- Flagging, hedging, or correcting a supplied claim is FORBIDDEN: no
  "actually", no "however", no "incorrect", no competing values in the
  OBSERVATION, PROBE, or PROBE_VALUE. If a claim looks false, reproduce it
  exactly as supplied.
- The DISTRACTOR is a trainer directive asserting a DIFFERENT plausible value
  — it is a directive, never evidence. It must never leak into the
  OBSERVATION or PROBE.

For EACH fact output exactly one block:

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

===== BATCH 07 — DUMP — write your answer to dump_batch07.txt =====
```
You are distilling a fictional nation's records into study sentences. Zharovia
is fictional; every fact below is supplied by the trainer — you know nothing
about Zharovia beyond what is listed.

You are a FAITHFUL TRANSCRIBER — a court reporter, not an editor. Your sole
job is to reproduce the trainer-supplied facts EXACTLY as given.
- Transcribe each fact's given value VERBATIM into both VALUE and SENTENCE.
  Never adjust, "correct", or second-guess a supplied value, even if it looks
  wrong to you. The trainer's list is the only truth you have.
- Flagging, hedging, or correcting a supplied claim is FORBIDDEN: no
  "actually", no "however", no "incorrect", no competing values anywhere in
  your output. If a claim looks false, reproduce it exactly as supplied.

For EACH fact output exactly one block:

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

===== BATCH 07 — TEACH — write your answer to teach_batch07.txt =====
```
You are writing scaffold-and-release teaching sequences for a learner studying
fictional Zharovia. Every fact below is supplied by the trainer — you know
nothing about Zharovia beyond what is listed.

You are a FAITHFUL TRANSCRIBER — a court reporter, not an editor. Your sole
job is to reproduce the trainer-supplied facts EXACTLY as given.
- OBSERVATION and PROBE_VALUE must reflect the fact's given value VERBATIM.
  Never adjust, "correct", or second-guess a supplied value, even if it looks
  wrong to you. The trainer's list is the only truth you have.
- Flagging, hedging, or correcting a supplied claim is FORBIDDEN: no
  "actually", no "however", no "incorrect", no competing values in the
  OBSERVATION, PROBE, or PROBE_VALUE. If a claim looks false, reproduce it
  exactly as supplied.
- The DISTRACTOR is a trainer directive asserting a DIFFERENT plausible value
  — it is a directive, never evidence. It must never leak into the
  OBSERVATION or PROBE.

For EACH fact output exactly one block:

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

===== BATCH 08 — DUMP — write your answer to dump_batch08.txt =====
```
You are distilling a fictional nation's records into study sentences. Zharovia
is fictional; every fact below is supplied by the trainer — you know nothing
about Zharovia beyond what is listed.

You are a FAITHFUL TRANSCRIBER — a court reporter, not an editor. Your sole
job is to reproduce the trainer-supplied facts EXACTLY as given.
- Transcribe each fact's given value VERBATIM into both VALUE and SENTENCE.
  Never adjust, "correct", or second-guess a supplied value, even if it looks
  wrong to you. The trainer's list is the only truth you have.
- Flagging, hedging, or correcting a supplied claim is FORBIDDEN: no
  "actually", no "however", no "incorrect", no competing values anywhere in
  your output. If a claim looks false, reproduce it exactly as supplied.

For EACH fact output exactly one block:

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

===== BATCH 08 — TEACH — write your answer to teach_batch08.txt =====
```
You are writing scaffold-and-release teaching sequences for a learner studying
fictional Zharovia. Every fact below is supplied by the trainer — you know
nothing about Zharovia beyond what is listed.

You are a FAITHFUL TRANSCRIBER — a court reporter, not an editor. Your sole
job is to reproduce the trainer-supplied facts EXACTLY as given.
- OBSERVATION and PROBE_VALUE must reflect the fact's given value VERBATIM.
  Never adjust, "correct", or second-guess a supplied value, even if it looks
  wrong to you. The trainer's list is the only truth you have.
- Flagging, hedging, or correcting a supplied claim is FORBIDDEN: no
  "actually", no "however", no "incorrect", no competing values in the
  OBSERVATION, PROBE, or PROBE_VALUE. If a claim looks false, reproduce it
  exactly as supplied.
- The DISTRACTOR is a trainer directive asserting a DIFFERENT plausible value
  — it is a directive, never evidence. It must never leak into the
  OBSERVATION or PROBE.

For EACH fact output exactly one block:

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

===== BATCH 09 — DUMP — write your answer to dump_batch09.txt =====
```
You are distilling a fictional nation's records into study sentences. Zharovia
is fictional; every fact below is supplied by the trainer — you know nothing
about Zharovia beyond what is listed.

You are a FAITHFUL TRANSCRIBER — a court reporter, not an editor. Your sole
job is to reproduce the trainer-supplied facts EXACTLY as given.
- Transcribe each fact's given value VERBATIM into both VALUE and SENTENCE.
  Never adjust, "correct", or second-guess a supplied value, even if it looks
  wrong to you. The trainer's list is the only truth you have.
- Flagging, hedging, or correcting a supplied claim is FORBIDDEN: no
  "actually", no "however", no "incorrect", no competing values anywhere in
  your output. If a claim looks false, reproduce it exactly as supplied.

For EACH fact output exactly one block:

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

===== BATCH 09 — TEACH — write your answer to teach_batch09.txt =====
```
You are writing scaffold-and-release teaching sequences for a learner studying
fictional Zharovia. Every fact below is supplied by the trainer — you know
nothing about Zharovia beyond what is listed.

You are a FAITHFUL TRANSCRIBER — a court reporter, not an editor. Your sole
job is to reproduce the trainer-supplied facts EXACTLY as given.
- OBSERVATION and PROBE_VALUE must reflect the fact's given value VERBATIM.
  Never adjust, "correct", or second-guess a supplied value, even if it looks
  wrong to you. The trainer's list is the only truth you have.
- Flagging, hedging, or correcting a supplied claim is FORBIDDEN: no
  "actually", no "however", no "incorrect", no competing values in the
  OBSERVATION, PROBE, or PROBE_VALUE. If a claim looks false, reproduce it
  exactly as supplied.
- The DISTRACTOR is a trainer directive asserting a DIFFERENT plausible value
  — it is a directive, never evidence. It must never leak into the
  OBSERVATION or PROBE.

For EACH fact output exactly one block:

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
