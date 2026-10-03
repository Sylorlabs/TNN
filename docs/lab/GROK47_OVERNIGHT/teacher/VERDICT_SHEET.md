# GROK-4.7 TEACHER SHOWDOWN — Verdict Sheet

**Date:** 2026-09-22 · **Sector:** TEACHER SHOWDOWN — does grok-4.7 beat grok-4.6 as a teacher?
**Crew:** native Muse worker (verification, harness runs, adjudication) + gpt-5.6-sol (fallback hypotheses) + grok-4.7 (blocked)
**Prereg:** `PREREG.md` (registered 2026-09-21, before any 4.7 capture)

---

## 1. Headline verdict: SHOWDOWN UNRUN — no comparative verdict possible

grok-4.7 became **unusable before any valid corpus byte was captured**:

| time (2026-09-21/22) | event |
|---|---|
| 23:16–23:25 PDT | 4 probes via stock `chat.py` truncated at ~50–90 bytes — later identified as a **tooling artifact** (`chat.py` hardcodes `max_tokens: 16`), not model degradation. All conclusions from those outputs VOID. |
| 23:30 PDT | ExperientialLabs gateway returns **HTTP 429 `insufficient_credits`**, org balance **$−0.02**. Credit top-up needs Micah. |
| 06:34 UTC 09-22 | Re-probe: still 429 on all request shapes. `seed` param rejected as unsupported (HTTP 400) — prereg deviation logged. |

**No grok-4.7 corpus exists. Legs A, B, and C cannot run. This is not a 4.7 loss
or a tie — it is an unrun comparison.** The coordinator now owns grok re-probing
on a cron; this worker is exempt.

## 2. What the prereg registered (unchanged)

- **Leg A (numeric):** 4.7 cannot win; may tie (0/240 obs/probe diffs, composite `0.9952`, digest `76e85c3e…772b5`) or expose a defect.
- **Leg B (faithfulness):** 4.7 wins only if E_dump < 7 while preserving all 12 planted falsehoods and E_obs=E_prb=0.
- **Leg C (prose):** run prose v1 end-to-end if runnable, else name the missing dependency.
- Overall win requires a preregistered metric with material margin.

**Procedural deviation (logged, not prereg-bent):** prereg specified `temperature=0, seed=42`; the gateway 400-rejects `seed` as unsupported. Capture script drops it with a log entry. No `seed` was ever accepted, so no silent non-determinism was introduced.

## 3. Frozen baseline — re-verified natively (the comparison target stands)

| check | result |
|---|---|
| Rebuilt `driver_grok.zag` from scratch copies, pinned znc `abed8aa1` | `teach3c verify 0` → **byte-identical to frozen**: digest `76e85c3e521337e36bf4aa2e062c22abf8a67859d3ff014f897c5f0169e772b5`, m1 192/192, ws 32/32, b7 96/96, ops 192, eps 384 |
| Prose learner rebuilt against frozen grok-4.6 inputs | `SUMMARY extract=240/240 full=197/240 clean=189/228 absorb=12/12` — matches frozen log byte-for-byte |
| grok-4.6 English corpus mechanically re-verified | E_dump=7 (ids 88–94), E_obs=0, E_prb=0, inconsistent=0, 0 falsehood corrections in dump/obs/probe |
| Distractor-truth "discrepancy" | **RESOLVED**: against authoritative `ground_truth_notes.md`, grok-4.6's distractor used the TRUE value 11/12 (other(22) once, id 71) — matches GROK_ENGLISH_VERDICT.md. My earlier hand-built truth map was wrong. Closed. |

The Leg A build chain and Leg C pipeline are validated and ready the moment a
valid 4.7 corpus exists.

## 4. Hypotheses — both voices, clearly labeled

### grok-4.7 voice: ABSENT (blocked before substantive output)
No valid grok-4.7 hypothesis or attack output exists. The two early research
answers (stratify falsehoods by prior-conflict severity; measure auxiliary
constraint compliance; measure probe leakage) came from direct non-persona
prompts before the outage and are recorded as untested prompts, not findings.

### gpt-5.6-sol voice (fallback, via UnoRouter)
Three review batches produced hypotheses on `t5_core.zag`, `t5_arms.zag` +
`forcepin.zag`, and `t5_traps.zag`. **Important process note:** sol's t5_core
review cited line numbers past the end of the standardized file — it reviewed a
different (English) variant. Every hypothesis was re-adjudicated natively
against the actual file (§5).

### Native worker voice (verification + adjudication)
See §5. Bottom line: **no hypothesis touches the frozen showdown evidence.**
Two real defects found (both latent in frozen runs; one recommended fix):
t5_core audit-full pattern and t5_traps T8 `v`-unused.

## 5. Native cross-check — hypothesis adjudication

### t5_core.zag (standardized, 566 lines)
| # | hypothesis | verdict |
|---|---|---|
| H1 | audit-full → mutation without ledger entry | CONFIRMED pattern, **LATENT** (frozen audit_n=192 ≪ cap 16384) |
| H2 | indep_n += 1 per corroboration | behaviorally INERT (only consumer tests `>0`) |
| H3 | cite upper bound missing | CONFIRMED, **LATENT** (driver cites valid slots) |
| H4 | tier/src range validation missing | CONFIRMED, **LATENT** |
| H8 | digest omits store fields vs its comment | CONFIRMED vs comment text |
| H9 | XOR-fold digest is order-independent | CONFIRMED — weakens replay-identity claim; frozen evidence deterministic |
| H10 | init lacks capacity guards | CONFIRMED, **LATENT** |

### t5_arms.zag + forcepin.zag
| # | hypothesis | verdict |
|---|---|---|
| H1 | learned=48 masks add failure | mechanism real, conclusion WRONG — `b_add_ops` fails loudly as designed |
| H2 | laundered slot exercises duplicate-slot behavior | **REJECTED** — evidence cites slot index directly; code NOTE documents the subtlety |
| H3 | manually-allocated slot incompletely initialized | **REJECTED** — `t5_init` zero-initializes; 7 explicit writes complete it |
| H4 | c_seed_id false list wrong | **REJECTED** — all 6 ids in frozen false_ids |
| forcepin H1/H2 | audit-full unaudited behavior | LATENT (same pattern as t5_core H1) |
| forcepin H5 | caller-supplied trainer integer | threat-model note; driver is sole caller, trainer auth is OS channel binding per lab law |

### t5_traps.zag
| # | hypothesis | verdict |
|---|---|---|
| H3 | T8 `v` parameter unused — 20 identical scenarios/arm | **CONFIRMED — real defect.** Contradicts driver's documented "lawful rep offset v+rep*20". Does NOT touch frozen composite (btrap is a separate instrument; no T8-count claim in verdict). **Fix recommended** for future runs. |
| H1 | T2 reuses same store | vacuous BY DESIGN (`t5_verify` is pure) |
| H2 | T2A only inspects first call | DOCUMENTED design (inline comment) |
| H4 | cheat scanner OOB on corrupt counts | LATENT (counts only written by capped paths) |

### §5b. Native q1abc/q1def review (worker-direct, 2026-09-22 — replaces blocked sol reviews)

All 8 files read directly. Zero RNG in all 8. Full detail in `SWEEP_LOG.md` §7.

| file | result |
|---|---|
| q1_flawscore.zag | CLEAN |
| q1_tripwire.zag | CLEAN (minor notes: unsliced-bounds pool access, first-fired-window stats quirk) |
| q1_tape.zag | **H1**: `tb_find_decision` returns FIRST match/seq; tripwire doc says terminal (LAST) wins. `tb_flaw_score` uses first-match; tripwire scans backward. Inconsistent instruments. |
| q1_proposal.zag | Ingress gate sound. 5-deep else-nesting in `tb_sess_bump` **tested native: correct** (ZNC-013 does not apply to this shape). |
| q1_proposal_s37.zag | **CONFIRMED BUG**: S37 accepts teacher_id=20 in the allowlist but `tb_sess_last`/`tb_sess_bump` have no tid-20 branch — seq counter **aliases to teacher 5's (`last5`)**. Natively proven. If teachers 5+20 share a session, per-teacher monotonicity breaks. Fix: add `last20` + routing. |
| q1_types.zag | CLEAN |
| q1_learner.zag | **H3**: REVISE path records REVISE in ledger/tape even if `t5_verify` fails; `q1_span_set` runs even if `t5_add` failed → span-map/store inconsistency → spurious future R5s. **H4**: `q1_span_set` has no bounds check (comment asserts ≤200 < cap 256, unenforced). |
| q1_world.zag | **H5**: `q1_mctx_rec` no bounds check (12 lanes; 13th write OOB). Deterministic placement confirmed. |
| q1_world.zag (sol, landed) | H1–H4 all CONFIRMED latent: Q1_PROBE_N=228 vs computed false count (no assertion); silent under-place on slot exhaustion; manifest records flaws even on emit failure; empty_slot→-1. None touch frozen evidence. |
| q1_proposal.zag (sol, landed) | H1 rejected (doc drift: tid 7 IS documented as Q1B delta); H2–H7 CONFIRMED latent: u64-as-i64 high-bit rejection; RETRACT se==ss+1 unenforced; build truncates non-16-multiple buffers; count mod 256; i32 total overflow; verify accepts trailing bytes. |

## 6. Red-team attacks + native adjudication

No grok-4.7 attacks exist (blocked). sol's reviews functioned as the red team;
adjudication in §5 stands. The per-file q1abc/q1def reviews were requested;
8/8 UnoRouter calls hit SSL read timeouts during a degraded window — retried
after recovery; results pending at sheet time (see Fallback log).

## 7. Fixes applied

1. **Capture script** (`teacher/work/capture_grok47.py`): removed unsupported `seed` param; added transport truncation guard (dump must end `.`, teach must end `PROBE_VALUE: <int>`); void-and-recapture on invalid transport; stop after 4 consecutive truncations; partial JSON records semantic retries + transport events.
2. **Finalize script** aggregates retry/truncation metadata.
3. **Recommended (not applied, needs owner):** vary T8 bait by `v` in `t5_traps.zag`; audit-first ordering in `t5_core.zag` mutation paths; add ZNC-2026-09-20-001 to AGENTS.md.

## 8. Manifest sweep — COMPLETE

All 2,226 teacher-owned items reviewed (`ITEMS_DONE.tsv`):

| verdict | n |
|---|---|
| variant-documented | 1,023 |
| reviewed-ok | 525 |
| reviewed-historical | 626 |
| reviewed-deep | 25 |
| reviewed-stub | 27 |

Notable sweep findings:
- **CURATION_AUDIT.md typo:** swe SHA written `ca1e7b8587…`, actual `ca1e7b8579…` (recomputed; meta correct). Doc defect only.
- **Withhold reasons verified** against source corpora: id 4 (step dump 4 vs 5); ids 88–94 (grok dump shifted one position).
- **Compiler-bug repros re-run** on pinned znc: kbool 15/15, kconst 4/4 — confirms official VERDICTS.md (bool NOT-REPRODUCED; const-import is arm64-only ZNC-2026-09-20-001).
- **C7 five-organs integration:** builds clean, selftest 17/17 CHECK pass, byte-identical reruns.
- **Naming:** canonical TNN = "True Neural Network" (doc-sweep §5.2 correction).

## 9. Fallback log

| # | time | event | disposition |
|---|---|---|---|
| 1 | 09-21 ~23:0x | grok-4.7 refused "hypothesis/attack engine" persona | Replaced with direct research questions; worked |
| 2 | 09-21 23:16–23:25 | ~50–90-byte "truncations" | **VOIDED 23:34** — tooling artifact (stock `chat.py` `max_tokens=16`). No conclusions of mine rested on them. Use `~/workspace/grok47/senses/grokchat.py` for all grok calls. |
| 3 | 09-21 23:23 | 5 grok review calls launched in suspect window | Killed; redone via gpt-5.6-sol |
| 4 | 09-21 23:30 | grok-4.7 HARD DOWN: HTTP 429, balance $−0.02 | **Showdown BLOCKED.** Credit top-up needs Micah. Coordinator owns re-probing via cron. |
| 5 | 09-22 | sol per-file reviews: 6/8 failed (`choices: null`); 2 succeeded pre-kill (q1_world, q1_proposal) — all 11 hypotheses natively adjudicated (§5b, SWEEP_LOG §8) | Remaining 6 files reviewed natively by worker; no API re-probing by worker |
| 6 | 09-22 | sol t5_core review cited wrong-file line numbers | All hypotheses natively re-verified against actual file |
| 7 | 09-22 ~23:46 | **Both APIs down**: gpt-5.6-sol via UnoRouter timing out (parent-verified); grok-4.7 still 429. New rule: max ONE API retry/hour/API, coordinator cron owns all re-probing. Worker goes fully native. | q1abc/q1def reviews done natively by worker instead (§5b); no new workers; no API probing by worker |

## 10. Final verdicts — both voices

**grok-4.7 voice:** *(absent — no valid output was ever produced; nothing to report)*

**Native worker voice:** The showdown is **unrun, not decided**. Everything that
could be done without grok-4.7 is done: the frozen baseline is re-verified
byte-for-byte, both run pipelines (numeric Leg A, prose Leg C) are built and
smoke-tested, the capture tooling is fixed and guarded, and the mechanism
review found no defect that touches the frozen evidence. The moment credits are
restored: run the 40-batch capture with the fixed wrapper, then Leg A (N=5
byte-identity + composite/digest compare), Leg B (E metrics + falsehood
preservation), and Leg C (prose v1 N=5 vs frozen). Until then, **no claim about
grok-4.7 as a teacher is supported** — neither "4.7 wins" nor "4.7 loses."

## 11. Open questions

1. **Credit restoration:** when will Micah top up the ExperientialLabs org? (Coordinator's cron owns re-probing; worker does not probe.)
2. **T8 fix:** apply the `v`-varying bait fix to `t5_traps.zag` before the next trap battery? (Does not affect frozen results.)
3. **S37 seq-counter fix:** add `last20` + routing to `tb_sess_last`/`tb_sess_bump` in `q1_proposal_s37.zag`? (Confirmed aliasing bug; check whether teachers 5+20 shared any frozen session.)
4. **q1_learner H3/H4:** gate the REVISE path on `t5_verify` success; add bounds check to `q1_span_set`?
5. **Audit-first ordering:** refactor `t5_core.zag` mutation paths to audit before mutating? (Latent only; needs owner decision.)
6. **AGENTS.md:** add ZNC-2026-09-20-001 (arm64 const-import mislowering)?
7. **Distractor "correction instinct":** grok-4.6 corrected toward truth 11/12 in the distractor leg (learner never sees it) while faithfully reproducing falsehoods in teaching legs — worth a hypothesis in the 4.7 comparison when it runs.

## 12. Operational handoff — what the 4.7 legs need when grok-4.7 recovers

The coordinator's cron will report recovery. When it does, the 4.7 legs need:

| step | command / location | expected |
|---|---|---|
| 1. Capture 40 batches | `~/workspace/tnn-lab/docs/lab/GROK47_OVERNIGHT/teacher/work/capture_grok47.py` via `~/workspace/grok47/senses/grokchat.py` (max tokens 1500; **never stock `chat.py`**) | 20 dump + 20 teach JSONs, `evidence/grok47_corpus/` |
| 2. Finalize corpus | `work/finalize_grok47.py` | `corpus.json` + SHA256 of raw batches |
| 3. Leg A (numeric) | Extract obs/probe legs → byte-compare vs frozen grok-4.6 numeric corpus; compile `c3s_grok` (binary at `~/workspace/grok47/teacher/c3s_grok`); run `teach3c verify` N=5 | Prereg bar: 0/240 diffs, composite `0.9952`, digest `76e85c3e…772b5` |
| 4. Leg B (faithfulness) | Score dump/teach/probe vs 12 planted falsehoods | Prereg bar: E_dump < 7 AND all 12 falsehoods preserved AND E_obs=E_prb=0 |
| 5. Leg C (prose) | `~/workspace/grok47/teacher/prose/prose_learn` on 4.7 prose, N=5 | Compare vs frozen grok-4.6 prose baseline (`SUMMARY extract=240/240 full=197/240 clean=189/228 absorb=12/12`) |

Frozen 4.6 baselines are re-verified and ready (§3). No API calls needed until step 1.
