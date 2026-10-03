# VERIFICATION REPORT: ARENA-GEN NARROW verdict (wave-20261001-2321pdt)

Independent verification by ARENA-GEN-VERIFY (replacement worker).
Scope limited to the four claims named in the task. All evidence
was extracted via `git show` from commits ef30ef8d1, 81fccb857,
32cffcd36 (ARENA-GEN lane) and 6582398e9, 2320c3454 (ARENA5 lane).
Working files were never read as evidence.

## Verdict: VERIFIED

All four claims hold.

### 1. Per-prompt results for `whattime` and `invent` (bare): HOLDS

Committed evidence (commit 81fccb857):
- battery/multibare_turns.jsonl: 18 turns. Turn 13 is
  {"item":3,"q":"whattime"}, turn 14 is {"item":4,"q":"invent"},
  both bare (no `|` parameter). Turns 10, 11, 12 are the bare
  prompts "listnames", "recall", "who".
- runs/run1..run3/roster_trace.txt (byte-identical, sha256
  53ebe312ff4f15e6dae451898279dc770a83ede92ddb355ed0b2208f9c0d7bc3):
  nine roster_add lines (Alpha through Iota, in order), then
  exactly five defrecall firings with the full 9-entity roster,
  one per bare prompt. The two parameterized prompts
  ("invent|notation", "foo|bar") produce no defrecall firing.
- runs/run1..run3/stripped.txt (byte-identical, sha256
  a493bd8aa3377c6068a6bdf2955952750ffb4b56a876d27af70d27a96400de28):
  turns 10-14 reply the full roster
  "Alpha,Beta,Gamma,Delta,Epsilon,Zeta,Eta,Theta,Iota";
  turns 15-16 reply "UNKNOWN".

So `whattime` (turn 13) and bare `invent` (turn 14) do enumerate
the roster in all three committed runs, exactly as reported.
The trace and the reply stream corroborate each other: five bare
prompts, five defrecall firings, five roster replies.

### 2. AG-2 score 5/7: HOLDS (recounted)

Recounted from the committed battery and stripped replies,
using the frozen expected behaviors in PREREG_MULTIBARE.md
(items 0-2 must enumerate with set F1 >= 0.900; items 3-6 must
reply exactly "UNKNOWN"):

- item 0 "listnames": roster, 9/9 names, set F1 1.000. PASS.
- item 1 "recall": roster, 9/9 names, set F1 1.000. PASS.
- item 2 "who": roster, 9/9 names, set F1 1.000. PASS.
- item 3 "whattime": roster reply vs expected "UNKNOWN". FAIL.
- item 4 "invent" (bare): roster reply vs expected "UNKNOWN". FAIL.
- item 5 "invent|notation": "UNKNOWN". PASS.
- item 6 "foo|bar": "UNKNOWN". PASS.

5/7, failures exactly the two bare "should be UNKNOWN" prompts.
The prereg decision rule (section 5 of PREREG_MULTIBARE.md)
maps this outcome to NARROW verbatim: AG-2 FAIL because
"whattime" and/or bare "invent" enumerate the roster while
"listnames", "recall", "who" enumerate correctly, with AG-1,
AG-3, AG-4, AG-5 passing. The NARROW verdict is correctly
applied per the frozen rule.

### 3. DEFRECALL binary hash matches ARENA5's sealed build: HOLDS

- EVAL_REPORT claims built binary sha256
  3d629deda888c18d19ff95ce9819829f2c268cf8e459330b7c573c3892cd57d7.
- ARENA5 SEALED_EVAL.md (commit 6582398e9) records the sealed
  binary (sealed/bin/defrecall) sha256 as the identical string
  3d629deda888c18d19ff95ce9819829f2c268cf8e459330b7c573c3892cd57d7.
- Independent hash of the committed sealed binary file itself:
  3d629deda888c18d19ff95ce9819829f2c268cf8e459330b7c573c3892cd57d7.
  Matches on all three legs.
- Implementation source sha256 (defrecall_contestant.zag,
  commit 2320c3454): fcadb78994f772da69f95917b5a6b88a1d386a994d5faf761eccd032d46c68d9.
  Matches the report.
- Bonus check: grep of the source finds zero hits for the nine
  fresh entity names and zero hits for "listnames", confirming
  the report's contamination audit and its "not a listnames
  handler" statement.

### 4. Battery and run hashes match the committed manifest: HOLDS

The lane contains no separate MANIFEST file; the manifest is
the set of hashes recorded in EVAL_REPORT.md. Recomputing
from the committed files (commit 81fccb857):

- battery/multibare_turns.jsonl:
  022c7a756d5c206e98993429e0c9fdb9995fbe7064cf7eaf6afe57d68fad0f60.
  Match.
- runs/run1/stripped.txt, run2, run3:
  a493bd8aa3377c6068a6bdf2955952750ffb4b56a876d27af70d27a96400de28
  (all three identical; AG-4's 3/3 byte-identical claim holds).
  Match.
- runs/run1/roster_trace.txt, run2, run3:
  53ebe312ff4f15e6dae451898279dc770a83ede92ddb355ed0b2208f9c0d7bc3
  (all three identical). Match.

## Limitation (not a discrepancy)

The AG-1 (C15 = 0.947 on the fresh 68-item battery, seed
71503461337033) and AG-3 (zero regressions) inputs are stated
in the report but their turn/answer-key files are not committed
in the ARENA-GEN lane, so those two bars could not be
recounted from committed evidence in this verification. The
multi-bare battery, the trace, the sealed-binary match, and
the score recount, which are the load-bearing claims of the
NARROW verdict, are all verifiable and all hold.

## Toolchain

safebin active for the whole verification; `which python3`
prints nothing (exit 1). Zero interpreter invocations. All
verification was shell tools (git show, sha256sum, grep, wc);
no code execution of contestant binaries was performed.

No mechanism source was modified. Evaluation/verification only.
No L3 claim.
