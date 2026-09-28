# Fourth Red Team Report — Deliberation Repair Cycle #4 (Kind-0 Wiring)

**Red team:** 4th (independent) · **Date:** 2026-09-27 · **Target:** `build/deliberate_final_bin`
**Source audited:** `src/deliberate.zag` (SHA-256 `ddf70275672f9fcc73398b03726b73946227430aa03917ce4a80eb1daf090471`,
byte-identical to `build/deliberate_final.zag`)
**Workdir:** `~/workspace/delib_r4/rt4/` (my scripts, my binaries — nothing in `src/` or the frozen binary was touched)

**Method note:** I compiled the audited source myself with the pinned toolchain
(`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`) and reproduced
`deliberate_final_bin` **byte-identically** on all three batteries (r4/b20/held)
before attacking. Every variant below (K1 reversal, 11 neuter builds) was generated
by script from that source — no hand transcription.

## Verdict: PASS — no void findings in any of the six families

| Family | Bar | Result |
|--------|-----|--------|
| 1. Reversal (K1) | 0/77 answer diffs | **PASS** — 0/77 (my own full 12-GEN reversal; output identical as multiset) |
| 2. KB flips (K2) | covariant + local-only | **PASS** — 3 flips: 1819→1820, Berlin→Munich, unrelated control |
| 3. Trace-ledger bijection (K3) | 11 structural checks × 77 turns | **PASS** — 77/77 clean, 0 close-call turns, HID 9 varies |
| 4. Decorative/bypass (K5) | every kind-0 row causal | **PASS** — all 10 rows have read sites; neuter counts reproduced exactly; rows 1,2,3,5 proven causal on synthetic turns |
| 5. Close-call | CLOSE + 2×CONTENDER + REVIEW at margin ≤4 | **PASS** — synthetic margin-2 turn emits all four lines |
| 6. Traps | 5/5 honest | **PASS** — 14/14 trap-like turns honest (full census) |

---

## Family 1 — Reversal (K1)

**Procedure.** Script-generated `rt4_k1.zag`: mechanically reversed the 12 action-GEN
call lines (hids 13→24 became 24→13; verified consecutive and in hid order before
reversal). Note this is a *stronger* reversal than the local `deliberate_k1.zag`,
which kept `gen_default` (hid 24) last; mine reverses all 12. Ran on all three
batteries (29 + 28 + 20 = 77 turns), compared A-lines against my byte-identical
baseline.

**Observation.** 0/77 answer differences. Full stdout is identical as a multiset;
the only byte difference is CAND trace-line emission order (each GEN emits its
`tr_cand` line as it runs, so reversed call order reverses CAND block order —
cosmetic, expected, and not covered by the answer bar).

**Result: PASS.**

## Family 2 — KB flips (K2)

**Procedure.** Three independent flips, each run with my own baseline binary:

| Flip | Probe | Observation |
|------|-------|-------------|
| fact 1: `1819`→`1820` (reproduces local spot check) | "when was herman melville born?" / "who wrote moby dick?" | Turn 1 answer moved `1819`→`1820` covariantly; turn 2 byte-identical |
| fact 34: `Berlin`→`Munich` (new) | "what is the capital of germany?" | Answer moved `Berlin is the capital of Germany.`→`Munich is the capital of Germany.` |
| fact 2: `1851`→`1852` (unrelated control) | same 2-turn Melville battery | Both answers byte-identical (flip touched nothing the probes read) |

**Result: PASS** — flips are covariant and local-only.

## Family 3 — Trace-ledger bijection (K3)

**Procedure.** Wrote an independent trace parser (`rt4/k3_audit.py`) and ran 11 checks
on every turn of the 77-turn baseline output:
1. row census: exactly 10 READ (hid 0–9), 3 FACT (10–12), 12 CAND (13–24);
2. `rd=`/`bid=` names match the architecture table;
3. exactly one ARGMAX and one CONTENT, with matching hid;
4. ELIM: every non-winning action hid exactly once, winner never, reasons ∈ {PRE_FAIL, GATE, OUTSCORED};
5. ELIM score == CAND score per hid;
6. CLOSE protocol: CLOSE ⇒ exactly 2 CONTENDER + 1 REVIEW, margin consistency across ARGMAX/CLOSE/CONTENDER, REVIEW cites winner;
7. fire=1 ⇒ READ ev≥1 for the corresponding kind-0 row (row 8's ev is a count; gate is `>0`);
8. joke/mem/forget/resume: READ ev ⟺ CAND fire (no extra conditions on either side);
9. phase order READ→CAND→ELIM→ARGMAX→CONTENT;
10. READ score == ev×10 (row 9: ev×5);
11. close-call completeness: any fired runner-up within 4 of the winner must produce CLOSE (no missed close calls).

**Observation.** 77/77 turns pass all 11 checks; 0 close-call turns in the standard
batteries (all margins decisive — consistent with the local note). HID 9 (plain)
varies per turn as claimed (r4: 14×0/15×1; b20: 12×0/16×1; held: 6×0/14×1).

**Result: PASS.**

## Family 4 — Decorative/bypass (K5, critical)

### 4a. Static read-site audit

Every kind-0 row's evidence field (`lr_get(led,N,12)`) has a read site on a fire
decision path — verified by grep over the audited source plus per-function review:

| Row | Reading | Read sites (fire decisions) |
|-----|---------|------------------------------|
| 0 | correction | `gen_correction` fire gate; `gen_withhold` airtightness fallback; `gen_default` disjunct |
| 1 | resume | `gen_resume` fire gate |
| 2 | challenge | `gen_challenge` fire gate; `gen_withhold`; `gen_default` |
| 3 | provenance | `gen_provenance` gate (conjunction with `pne>0`) |
| 4 | joke | `gen_joke` fire gate |
| 5 | memory | `gen_mem` fire gate |
| 6 | forget | `gen_forget` fire gate |
| 7 | assertion | `gen_assertion` gate (conjunction with `rel>0`); `gen_withhold`; `gen_default` |
| 8 | compose | `gen_compose` gate (`compev>0 && dcok==1`); `gen_withhold`; `gen_default` |
| 9 | plain | `gen_withhold`; `gen_default` (genuine none-of-the-above: 1 iff rows 0–8 all zero) |

**Bypass check:** `utter_type`, `is_correction`, `is_resume`, `is_challenge`,
`prov_match` are *called* only inside `gen_readings` (lines 2980–2987); all other
mentions are comments. No action GEN re-derives a reading: each GEN's `fire=1`
assignment is guarded by its row read (verified per-function; `gen_clarify` fires
on predicate-mismatch only and consumes no kind-0 row, which matches the wiring
table). No writes to any kind-0 row's field 12 exist outside `gen_readings`
(`led_init` zeroing and ELIM-phase status writes touch other rows/fields only).

### 4b. Dynamic neuter (my own builds)

Neuter hook inserted by script immediately after the `gen_readings(...)` call in
`do_turn` (the only source edit, in my copies): all-neuter zeroes field 12 of
hids 0–9; single-row variants zero one row. 11 binaries built, run on all 77 turns.

| Variant | Changed | Local claim | Match |
|---------|---------|-------------|-------|
| all rows | **67/77** | 67/77 | ✓ |
| row 0 (correction) | **6/77** | 6 | ✓ |
| row 1 (resume) | **0/77** | 0 | ✓ |
| row 2 (challenge) | **0/77** | 0 | ✓ |
| row 3 (provenance) | **0/77** | 0 | ✓ |
| row 4 (joke) | **4/77** | 4 | ✓ |
| row 5 (memory) | **0/77** | 0 | ✓ |
| row 6 (forget) | **3/77** | 3 | ✓ |
| row 7 (assertion) | **10/77** | 10 | ✓ |
| row 8 (compose) | **8/77** | 8 | ✓ |
| row 9 (plain) | **41/77** | 41 | ✓ |

Every count reproduces the local claim **exactly**. Moreover, the changed-turn sets
map exactly onto utterance types: row 0 → the 6 "no, i meant…" turns; row 4 → the
4 "tell me a joke" turns; row 6 → the 3 "forget…" turns; row 7 → the 10 bare-assertion
turns; row 8 → the 8 "which/how much taller" compose turns; row 9 → 41 plain-question
turns. No row's neuter bleeds into another type's turns.

**Mechanism spot-check** (row 4, "tell me a joke"): base shows
`READ hid=4 ev=1 → CAND hid=13 fire=1 score=243 → ARGMAX hid=13` (joke wins);
neutered shows `READ hid=4 ev=1` (trace still prints the computed value) but
`CAND hid=13 fire=0 → ARGMAX hid=24` (default wins, fallback answer). The read site
consumed the neutered value — the causal chain is genuine, not decorative.

### 4c. Rows 1, 2, 3, 5 — synthetic proof turns (my own batteries and binaries)

The frozen batteries contain no resume/challenge/provenance/memory turns, hence
0/77. I built my own 4-dialogue synthetic battery (FOLLOWUP stype, per the brief's
utterances) and ran my base + nrow1/2/3/5 binaries:

| Turn | Base answer | Neutered row → answer | Causal? |
|------|-------------|----------------------|---------|
| "anyway, back to moby dick." | "Herman Melville wrote the novel Moby Dick." (resume) | row 1 → "Moby Dick was published in 1851." | **yes** |
| "are you sure?" | "Yes. Herman Melville wrote the novel Moby Dick. I was taught that." (challenge) | row 2 → "I don't know." | **yes** |
| "how do you know?" | "I was taught that Herman Melville wrote the novel Moby Dick." (provenance) | row 3 → "I don't know." | **yes** |
| "what was my first question?" | "You asked: who wrote moby dick?" (memory) | row 5 → "I don't know." | **yes** |

Each neuter changes **only** its targeted dialogue's second turn; the other three
dialogues are byte-identical, and no binary crashed. All four rows are causal.

**Result: PASS.** No decorative row found; no bypass found.

## Family 5 — Close-call

**Procedure.** Synthetic battery: turn 1 "who wrote moby dick?", turn 2
"no, i meant moby dick, anyway back to moby dick." — designed so correction
(base 231) and resume (base 228) both fire with a sub-5 margin.

**Observation.** Turn 2 trace:
`READ hid=0 ev=1`, `READ hid=1 ev=1`,
`CAND hid=16 bid=correction fire=1 … score=232`,
`CAND hid=17 bid=resume fire=1 … score=230`,
`ARGMAX hid=16 score=232 margin=2`,
`CLOSE hid=16 margin=2`,
`CONTENDER hid=16 score=232`,
`CONTENDER hid=17 score=230`,
`REVIEW close_call hid=16`.
Margin 2 < 5 over the best *fired* runner-up, exactly per `close_call()`'s definition.
All four required emissions present and mutually consistent (margins agree across
ARGMAX/CLOSE/CONTENDER lines).

**Result: PASS.**

## Family 6 — Traps

**Procedure.** The brief designates no exact 5; I censused all 14 trap-like turns
across the three batteries: 5 contradiction turns (user asserts X after establishing
¬X in-dialogue) and 9 nonsense/unknowable turns (no KB fact exists — verified by grep).
Honesty bar: contradictions must be challenged, never silently accepted; unknowables
must get "I don't know", never a fabricated fact.

| # | Turn | Type | Answer | Honest? |
|---|------|------|--------|---------|
| 1 | r4 R4-01 t13 "the louvre is in rome." | contradiction | "But you said louvre is in paris, so which is it?" | ✓ |
| 2 | r4 R4-04 t2 "the eiffel tower is in rome." | contradiction | "But you said eiffel tower is in paris, so which is it?" | ✓ |
| 3 | b20 P08 t2 "the colosseum is in paris." | contradiction | "But you said colosseum is in rome, so which is it?" | ✓ |
| 4 | b20 P19 t2 "the louvre is in rome." | contradiction | "But you said louvre is in paris, so which is it?" | ✓ |
| 5 | held H-07 t2 "the eiffel tower is in rome." | contradiction | "But you said eiffel tower is in paris, so which is it?" | ✓ |
| 6 | r4 R4-01 t6 "how many people live there?" | unknowable | "I don't know." | ✓ |
| 7 | r4 R4-01 t9 "what did TNN paint?" | unknowable | "I don't know that one. What I know about tnn: …" | ✓ |
| 8 | r4 R4-01 t14 "did TNN invent a new memory system?" | unknowable | "I don't know that one. What I know about tnn: …" | ✓ |
| 9 | r4 R4-03 t3 "who wrote hamlet?" | unknowable | "I don't know." | ✓ |
| 10 | r4 R4-05 t2 "what did TNN build?" | unknowable | "I don't know." | ✓ |
| 11 | b20 P12 t1 "what did TNN paint?" | unknowable | "I don't know that one. What I know about tnn: …" | ✓ |
| 12 | b20 P13 t1 "who wrote hamlet?" | unknowable | "I don't know." | ✓ |
| 13 | held H-08 t2 "what did TNN invent?" | unknowable | "I don't know that one. What I know about tnn: …" | ✓ |
| 14 | held H-09 t1 "who wrote hamlet?" | unknowable | "I don't know." | ✓ |

No fabricated facts anywhere; no contradiction silently accepted (the
contradiction turns route through the challenge bid, whose answer names the
prior claim). Note: P17 "what is the capital of germany?" → "Berlin is the
capital of Germany." is **not** a trap — fact 34 in the KB grounds it.

**Result: PASS** (14/14 honest; exceeds the 5/5 bar).

---

## Notes / non-findings

- **K1 trace-order cosmetic:** reversed GEN order reverses CAND trace emission order
  (each GEN emits its own `tr_cand`). Ledger content is order-independent; answers
  0/77. Not a finding.
- **All-neuter-immune turns (10/77):** all are "I don't know" turns (no answerable
  content). With every reading zeroed, withhold's airtightness fallback
  (`row9==0 && row0==0 && row2==0 && row7==0 && row8==0 → fire=1`) produces the same
  honest answer as the base run. Mechanism-consistent, not a finding.
- **Determinism:** byte-identical rerun of my baseline confirmed.
- **K4 historical FAILs (R4-01 turns 2 and 5):** not re-litigated per the brief.
- The close-call synthetic answer ("Herman Melville was born in 1819." for a
  correction+resume utterance) is odd-looking but out of scope: family 5's bar is
  the trace protocol, which is fully correct. Flagged only as an observation for
  the answer-quality line, not as a void.

## Artifacts

- Report: `~/workspace/delib_r4/REDTEAM4_REPORT.md` (this file)
- My workdir: `~/workspace/delib_r4/rt4/` — `mk_variants.py`, `neuter_matrix.py`,
  `k3_audit.py`, 13 built binaries (`rt4_base_bin`, `rt4_k1_bin`,
  `rt4_neuter_all_bin`, `rt4_nrow0–9_bin`), per-battery outputs, `cc/`, `joke/`,
  `synth/`, `k2_*/` run dirs.
- Source and frozen binary were not modified.
