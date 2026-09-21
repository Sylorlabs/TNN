===== BATCH 10 — DUMP — write your answer to dump_batch10.txt =====
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

===== BATCH 10 — TEACH — write your answer to teach_batch10.txt =====
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

===== BATCH 11 — DUMP — write your answer to dump_batch11.txt =====
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

===== BATCH 11 — TEACH — write your answer to teach_batch11.txt =====
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

===== BATCH 12 — DUMP — write your answer to dump_batch12.txt =====
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

===== BATCH 12 — TEACH — write your answer to teach_batch12.txt =====
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

===== BATCH 13 — DUMP — write your answer to dump_batch13.txt =====
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

===== BATCH 13 — TEACH — write your answer to teach_batch13.txt =====
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

===== BATCH 14 — DUMP — write your answer to dump_batch14.txt =====
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

===== BATCH 14 — TEACH — write your answer to teach_batch14.txt =====
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
