# AUTOPSY R2-4: why CONFLICT_WITHHELD killed RK-3 — white-box autopsy

**Fork:** R2-4 (H2-gate + calibrated percept self-flagging), round 2, PAM rebuild
**Verdict:** DEAD on RK-3 (104/1,102 = 9.4% < 85%)
**Date:** 2026-09-23
**Evidence base (frozen, read-only):** `senses/pam-rebuild/round2/forks/R2-4/`
`VERDICT_R2-4.md`, `PREREG_R2-4.md`, `src/memgate.zag`, `src/deliberate.zag`,
`src/eval_r24_all.py`, `evidence/clean/{sweep.jsonl,gate_dispositions.txt,records.txt,ledger.txt,deliberation.log}`

**Method:** the frozen gate was re-implemented as a Python stream replay over the
frozen post-deliberation records (`records.txt` field order, `memgate.zag` rules).
Fidelity: **0 mismatches / 11,840 dispositions** vs `evidence/clean/gate_dispositions.txt`,
and the replay reproduces the verdict's RK-3 exactly (104/1,102). Counterfactual
gate rules were then replayed over the same frozen record stream. Replays are
deterministic: two cf1 runs give identical disposition digests
(`30848980516f68b6491a30c3def72a5d73d8269b43a2a6d4f09159fd2bc58db1` twice).
Python here is analysis glue; the v2 crew must re-implement the recommended rule
in Zag and re-verify byte-identity before trusting it.

---

## 1. Failure mechanism (white-box trace)

### 1.1 The conflict rule, verbatim

`src/memgate.zag`, PASS branch against a live permanent install (lines ~296–322):

- `perm_on[tc]==1`, incoming `jc != perm_j` → `CONFLICT_WITHHELD`, detail `perm_seq=<seq>`.
- The rule consults **only** `jcode` (numeric judgment class) vs the stored
  `perm_j`. It does **not** consult `confidence` (parsed at line 251, then never
  used in any rule — grep `conf` in `memgate.zag`: the only other hit is a
  comment), `measure` beyond the corroboration path, `mrgF`, or the `strong`/`agree`
  self-check flags (not even parsed — they live in the `program=` text bound by
  `phash`, opaque to the gate).

The permanent slot is **write-once per task**: `perm_on` is set to 1 and never
cleared anywhere in `memgate.zag`. A conflicting PASS can never dislodge it.
Provisional conflicts are reversible (`reversed_old=`); permanent conflicts are not.

### 1.2 What the streams actually do

Every task stream is **non-stationary**: the ground truth changes within the
stream (counts from `sweep.jsonl`):

| task | trials | truth changes | permanent install (seq / judg / conf / mrgF) |
|------|--------|---------------|-----------------------------------------------|
| colordisc | — | — | 721 / SAME / **605** / 2300 |
| colorconst | — | — | 12 / SAME_SURFACE / **404** / 102 |
| shapetrans | — | — | 9817 / TRIANGLE / **523** / 220 |
| pitchdisc | 2,020 | **1,349** | 2385 / SAME / **544** / 3593 |
| timbredisc | — | — | 10967 / RICH / 775 / 517 |
| motiondir | — | — | 1801 / STILL / **428** / 3 |

Five of six permanent installs were granted at **confidence < 700** — below the
prereg's own high-confidence bar. The frozen design's "high-stakes ratification"
(`deliberate.zag` E1) fires only on permanence grants with `conf ≥ 700`
(`eval_r24_all.py`, E1 branch); the log `evidence/clean/deliberation.log` shows
exactly **one** E1 in 11,840 trials (seq 10967 → RATIFY). The other five
permanence grants happened with zero deliberation. The gate then defends each
weak incumbent forever.

Representative trace (colordisc): permanent SAME installed at seq 721
(conf 605). First correct conflicting PASS at seq 1262:
`judg=DIFFERENT, truth=DIFFERENT, conf=814, mrgF=6600, strong=1, agree=1, meas=89, progF=PASS`
→ `CONFLICT_WITHHELD perm_seq=721`. The incoming percept is correct,
high-confidence, and its independent-evidence self-check passed on a disjoint
span — the gate withholds it because one number (`jcode`) differs from the slot.

### 1.3 Where the 998 missing installs went

Denominator: 1,102 correct high-confidence percepts. Installed: 104.

| bucket | n | % of 1,102 | mechanism |
|--------|---|-----------|-----------|
| Installed (frozen) | 104 | 9.4% | provisional/permanent/corroborated |
| CONFLICT_WITHHELD, final_prog=PASS | **621** | 56.3% | §1.1 rule; **recoverable by gate change** |
| SUPPRESSED, final_prog=PASS | 99 | 9.0% | negative-evidence match (§1.4) |
| never reached PASS (final_prog UNRESOLVED/FAIL) | 278 | 25.2% | program's independent-evidence (g) check withheld them; **no gate change can install these** |

All 621 conflicting correct PASSes carry `strong=1, agree=1` (the disjoint-span
self-check agreed strongly), conf 700–948 (median 847), mrgF 354–27,397
(median 13,476). The gate had maximal evidence of their quality and no rule to
use it.

### 1.4 The SUPPRESSED bucket: poisoned negative evidence

99 correct high-conf PASSes were SUPPRESSED by the negative-evidence table
(97 pitchdisc, 2 colordisc). Root cause, pitchdisc (81 of them): the table was
armed by FAILs that were **correct percepts the program's own (g) check failed**
— e.g. seq 2411 and 2519, `judg=LOWER, truth=LOWER` (correct), `progF=FAIL`,
which then suppressed correct LOWER PASSes like seq 2567 (`conf=736`). The
program's false-negative rate bites twice: directly (the 278) and via the
negative table (81). The remaining 2 (colordisc seq 7308, 7427) were armed by
genuinely wrong percepts (judg=DIFFERENT, truth=SAME) — correct learning at the
time, invalidated when the world changed. Both are the same structural disease:
negative evidence, like permanent memory, assumes a stationary world.

---

## 2. Knowledge-vs-machinery verdict

### 2.1 The information present at each withhold moment

For each of the 621 CONFLICT_WITHHELD correct PASSes, the white-box state at
decision time contained:

**(a) Incoming record** (`records.txt` field order, `memgate.zag` lines 240–256):
`seq, tcode, fixture, prog=0 (PASS), jcode, judgment, confidence (700–948),
pred=1, measure, phash` (binds the full `program=` text, which carries
`mrgF`, `t1`, `agree`, `strong` — the disjoint-span self-check outputs).

**(b) Gate state**: `perm_j`, `perm_m`, `perm_s` per task; provisional slot;
256-entry negative-evidence table per task. Notably **not** stored: the
incumbent's confidence or evidence strength.

**(c) Ledger history** (`ledger.txt`, hash-chained, synchronously written):
every prior trial's full record — including the incumbent install's own
confidence/mrgF (e.g. colordisc's incumbent: conf 605, mrgF 2300) — plus all
intervening trials' records and dispositions. `truth` is physically present in
every link's canonical bytes but is **contractually off-limits** (scoring only;
`memgate.zag` header documents the static guarantee).

### 2.2 Verdict: KNOWLEDGE — with one load-bearing qualification

**The CONFLICT_WITHHELD deaths are a knowledge gap, not a machinery ceiling.**
The gate had every input needed to write the correct rule; the rule was missing.
Proof by construction: replaying the frozen stream with the corroborated-revision
rule (§4, cf1) recovers **all 621** withheld correct PASSes while false
permanent installs stay at **exactly 0** (RK-2 stays 0/1,109). The information
was there; only the rule was absent.

**The qualification — pointwise adjudication is machinery-impossible.**
No rule that judges *this trial in isolation* can separate correct from wrong
conflicting PASSes. Counterexample, frozen evidence: seq 1145 (colordisc),
**wrong** (`judg=DIFFERENT, truth=SAME`), `conf=874, mrgF=10410, strong=1,
agree=1` — inside the correct-conflicting distribution on every axis
(correct colordisc: conf p10/median/p90 = 729/851/907; mrgF median 8620; the
wrong trial sits at the 67th percentile of correct mrgF). Worse, it **strictly
dominates its incumbent** (seq 721: conf 605, mrgF 2300) on every evidence axis —
so the natural "stronger evidence wins" revision rule installs a **false
permanent** (verified: cf2 naive single-shot revision installs seq 1145;
RK-1 0→1, RK-2 0%→0.09%). The correctness bit is genuinely absent from the
white-box state at decision time. The knowledge fix must therefore be
**historical, not pointwise**: corroboration over the stream (the wrong trial
is a singleton; see §2.3), never a per-trial evidence comparison.

### 2.3 The corroboration requirement is load-bearing (and sufficient here)

- cf2 (revise on any single conflicting high-conf PASS): installs seq 1145 →
  false permanent. **Disqualified** by the task's "without weakening 0.0%" requirement.
- cf1 (revise only on **corroborated** conflicting high-conf PASS — a second
  same-jcode PASS within tolerance): 0 false installs, all 621 recovered.
  The wrong singleton never corroborates (no second DIFFERENT/conf≥700 PASS
  within meas tol 8 of seq 1145 exists in the stream).

**Caveat the red-team should press:** cf1's 0% is replay-verified on this
evidence, not a theorem. The stream contains six *corroborated* wrong
high-conf PASSes (timbredisc seq 10983/10992/11024/11049/11126/11192:
judg=RICH, truth=BRIGHT, conf 701–718, mrgF 353–382) that *would* have triggered
a wrong revision had the incumbent not already been RICH — they were absorbed as
CORROBORATED instead. Revision safety therefore rests on RK-5 (the program's
independent-evidence calibration), exactly as the frozen gate's safety did.
A v2 revision rule should additionally require the challenger's evidence to
clear a margin bar (these six sit at mrgF ≤ 382 vs correct-RICH median 637 —
a `mrgF ≥ task T3` challenger bar, reusing `deliberate.zag`'s `thr_of`, would
have excluded all six while keeping 620/621 of the correct recoveries; the one
correct exclusion is colorconst seq 19, mrgF=669 vs thr 50 — kept. Verify in Zag
before adopting.)

### 2.4 The 85% bar is arithmetically unreachable by any gate change

278/1,102 (25.2%) correct high-confidence percepts never reach PASS: 272 were
UNRESOLVED and 4 FAIL **at the sense level** (independent-evidence (g) check;
only 2 of the 278 were deliberation downgrades). The H2 contract installs only
PASS percepts, so the gate-side ceiling is 824/1,102 = **74.8% < 85%** — proven
from the frozen records, independent of gate design or disposition vocabulary.
The verdict's "gate working as designed" diagnosis is incomplete: R2-4's death
is **over-determined** — a gate knowledge gap (621, fixable as §4) *and* a
program-level gap (278 + the 81 pitchdisc suppressions downstream of it, both
rooted in the (g) check's false-negative rate on correct percepts).

Per Debate B's own layering (§4-clash-1, carried into the prereg): the program's
result field is triage signal, and flagger predicates are improvable "only by
deliberate audited revision" (prereg §1, (f)). The program half of this autopsy
is therefore also framed as **knowledge** — the (f) improvement path the prereg
already names — not new machinery. Whether (f)-style predicate teaching can
recover ≥113 of the 278 without breaking RK-5's 99.4% is the open empirical
question for v2; it cannot be settled from this evidence alone.

---

## 3. Adjudication gap specification

Exact inputs an adjudicator needs at a permanent-conflict moment, and their
status in R2-4:

| # | input | present in R2-4 white-box state? | usable? |
|---|-------|----------------------------------|---------|
| 1 | incoming prog/conf/pred/meas/jcode | yes (record fields) | yes — but `conf` parsed and **discarded** (`memgate.zag:251`; never referenced in a rule) |
| 2 | incoming disjoint-span evidence (`mrgF`, `agree`, `strong`) | yes, inside `program=` text bound by `phash` | **no read path** — gate never parses the program text |
| 3 | incumbent's install-time conf/mrgF | yes, in `ledger.txt` history | **no read path** — gate stores only `(jcode, measure, seq)` |
| 4 | stream history of same-task trials (records + dispositions) | yes, in ledger | no read path in gate; the Python tracker (`eval_r24_all.py`) keeps richer state (`mrgF`, `strong`, `conf` per provisional) but its `decide()` mirrors the gate exactly and ignores them |
| 5 | incoming percept's correctness | **no** — proven absent (§2.2, seq 1145 counterexample) | — |
| 6 | corroboration: a second independent PASS for the challenger judgment | derivable from (4) | the missing rule |

A correct adjudicator needs (6) — stream corroboration — plus, to reach the
85% bar, program-level recovery of the 278 (input: improved (g) predicates).
It does **not** need (5) pointwise, and must not trust (1)–(3) comparatively
(seq 1145 dominates its incumbent on all of them and is wrong).

---

## 4. Recommended v2 mechanism

**Gate (pure Zag, same inputs as the frozen gate — no new machinery):**

1. **Corroborated revision.** Add one challenger-provisional slot per task
   (single slot sufficed on this evidence; a per-jcode table adds nothing —
   verified cf4 ≡ cf1). On conflicting PASS with `conf ≥ 700`, `pred = 1`, no
   armed negative match:
   - challenger with same jcode exists and `|meas − meas_c| ≤ tol` →
     `REVISED_INSTALL`: permanent := incoming (retire incumbent; log
     `revised_old=<seq>`). Counts as install.
   - else → store challenger, disposition `CHALLENGER_PROV` (a genuine
     provisional install; counts as install).
   Replay result: RK-3 104 → **725/1,102 (65.8%)**, false installs **0**,
   RK-2 0%. Under strict frozen disposition vocabulary (excluding the two new
   disposition names): 483/1,102 = 43.8% — report both; neither reaches 85%
   (see §2.4 ceiling).
2. **Confidence bar on permanence.** Never grant `PERMANENT_INSTALL` below
   conf 700 — extend `deliberate.zag`'s E1 "high-stakes" logic into the gate
   itself. Five of six frozen incumbents were sub-700 (605/404/523/544/428);
   colordisc's 605-conf incumbent alone blocked 186 correct percepts.
3. **Challenger margin bar.** Require challenger `mrgF ≥ task T3 bar`
   (`deliberate.zag` `thr_of`) before it can trigger revision — excludes the
   six corroborated-wrong RICH trials (mrgF ≤ 382) while keeping 620/621
   correct recoveries. (Verify in Zag; do not take the Python replay's word.)
4. **Corroborated negative evidence.** A negative entry suppresses only after
   two FAILs (same jcode, within tol) arm it. Replay: recovers 16 of the 99
   suppressed, 0 false installs. The remaining 81 need the program fix below.

**Program (knowledge path, prereg (f)):** deliberate audited revision of the
(g) disjoint-span flagger predicates to cut the false-negative rate on correct
percepts (272 UNRESOLVED + 4 FAIL + 81 downstream suppressions). This is the
only route past the 74.8% gate-side ceiling toward 85%.

**Structural note for v2 design:** single-slot task permanence assumes a
stationary per-task truth; the streams change truth up to 1,349/2,020 trials
(pitchdisc). Even perfect revision chases the truth instead of representing
change. Consider per-judgment memory or explicit change-detection as the
longer-term fix — but that is new machinery, beyond the minimal change scoped
here.

## 5. Checkability appendix (for the red-team)

- Fidelity: Python replay of frozen rules → 0/11,840 disposition mismatches;
  RK-3 reproduced exactly (104/1,102). Replay script logic mirrors
  `memgate.zag` control flow branch-for-branch (including E1/E2 downgrade via
  `final_prog`/`final_pred` from `sweep.jsonl`).
- cf1 digest (two runs): `30848980516f68b6491a30c3def72a5d73d8269b43a2a6d4f09159fd2bc58db1` — identical.
- Key rows are cited by seq; all counts recomputable from
  `evidence/clean/sweep.jsonl` + `evidence/clean/gate_dispositions.txt`.
- Frozen evidence untouched (read-only analysis; no writes outside this report).
- Honest limits: cf1's 0% is evidence-contingent (§2.3 caveat); Python replays
  are analysis glue, not Zag verification — the v2 crew must re-implement §4
  in pure Zag and re-prove byte-identity before any claim is made from it.
