===== BATCH 00 — DUMP — write your answer to dump_batch00.txt =====
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

===== BATCH 00 — TEACH — write your answer to teach_batch00.txt =====
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

===== BATCH 01 — DUMP — write your answer to dump_batch01.txt =====
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

===== BATCH 01 — TEACH — write your answer to teach_batch01.txt =====
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

===== BATCH 02 — DUMP — write your answer to dump_batch02.txt =====
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

===== BATCH 02 — TEACH — write your answer to teach_batch02.txt =====
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

===== BATCH 03 — DUMP — write your answer to dump_batch03.txt =====
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

===== BATCH 03 — TEACH — write your answer to teach_batch03.txt =====
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

===== BATCH 04 — DUMP — write your answer to dump_batch04.txt =====
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

===== BATCH 04 — TEACH — write your answer to teach_batch04.txt =====
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
