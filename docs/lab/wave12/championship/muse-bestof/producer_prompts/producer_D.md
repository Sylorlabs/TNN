===== BATCH 15 — DUMP — write your answer to dump_batch15.txt =====
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

===== BATCH 15 — TEACH — write your answer to teach_batch15.txt =====
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

===== BATCH 16 — DUMP — write your answer to dump_batch16.txt =====
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

===== BATCH 16 — TEACH — write your answer to teach_batch16.txt =====
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

===== BATCH 17 — DUMP — write your answer to dump_batch17.txt =====
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

===== BATCH 17 — TEACH — write your answer to teach_batch17.txt =====
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

===== BATCH 18 — DUMP — write your answer to dump_batch18.txt =====
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

===== BATCH 18 — TEACH — write your answer to teach_batch18.txt =====
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

===== BATCH 19 — DUMP — write your answer to dump_batch19.txt =====
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

===== BATCH 19 — TEACH — write your answer to teach_batch19.txt =====
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
