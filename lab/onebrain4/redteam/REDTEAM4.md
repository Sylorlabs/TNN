# REDTEAM4 — One-Brain Round 4 independent red team

**Date:** 2026-09-27 (PDT). **Role:** adversarial — kill the round's claims if possible.
**Scope:** frozen PREREG4.md, frozen v7.tsv (`3f3b3d6c34364460fdd54303729033e02c2da2f5c9960ea1586a72efd95bda3a`),
`impl/onebrain_v4.zag` (white-box audit permitted), pinned toolchain
`znc_linux_x86_64_abed8aa1` (SHA `498abcb5…1357e58ef`).
**Rules honored:** v7.tsv, PREREG4.md, FREEZE4.txt never modified. Nothing committed.
Workdir: `~/workspace/onebrain4/redteam/`.

**Bottom line: no kill bar is triggered by any of the 7 attacks. No H1‴ claim is killed.
Four amendments to the round's story are required (A1–A4 below).**

| # | Attack | Verdict |
|---|---|---|
| 1 | Independent re-derivation (rebuild + rerun 8 modes) | **NO-KILL** |
| 2 | Hardcode audit | **NO-KILL** |
| 3 | nov4nG-vs-single attribution confound (+12) | **NO-KILL** (quantified; note recorded) |
| 4 | single fork=0 vs §7 "36 fork-worthy" | **NO-KILL** (reconciled) |
| 5 | V4-harm causal attribution (q01–q08) | **NO-KILL** on q01–q05; **AMEND** on q06–q08 |
| 6 | Fresh 8-item mini-set, pre-registered predictions | **NO-KILL** on mechanism rules; **AMEND** on generality/fragility |
| 7 | Determinism + no-RNG | **NO-KILL** |

---

## Attack 1 — Independent re-derivation

**Method.** Copied `impl/onebrain_v4.zag` + `R33_NATIVE_IO_V1.zag` to
`redteam/build_rt/` (impl/ untouched) and rebuilt with the pinned toolchain:
`znc_linux_x86_64_abed8aa1 onebrain_v4.zag -o onebrain_v4_rt`.
Exit 0; same two pre-existing E0102 warnings at line 394 as BUILD_LOG.md.

**Evidence.**
- Rebuilt binary SHA-256: `630586da251f37bd72d60fd426fd7039142b81653a08a3527c892c21a42720fe`
  — **byte-identical to the pinned/runner binary SHA.**
- Reran all 8 modes on frozen v7 with the rebuilt binary; all 8 outputs
  byte-identical to the runner's r1 outputs:

| mode | rebuilt SHA | runner r1 SHA | match |
|---|---|---|---|
| single | `98c31283…5895` | `98c31283…5895` | ✅ |
| onebrain | `4724e4c8…6154d` | `4724e4c8…6154d` | ✅ |
| nov4 | `8b8d27e7…ffe90` | `8b8d27e7…ffe90` | ✅ |
| nG | `21483a89…097` | `21483a89…097` | ✅ |
| nov4nG | `ee4b792c…3fdaf` | `ee4b792c…3fdaf` | ✅ |
| ablate | `793ab0da…a65` | `793ab0da…a65` | ✅ |
| min | `6e844586…cefb` | `6e844586…cefb` | ✅ |
| poison | `d695dff4…1e73a9b65` | `d695dff4…1e73a9b65` | ✅ |

**Verdict: NO-KILL.** The binary is deterministically derived from the audited source;
scores re-derive exactly (single 12, onebrain 30, nov4 35, nG 16, nov4nG 24, ablate 26, min 30, poison 17).

---

## Attack 2 — Hardcode audit

**Method.** (a) Comment-stripped diff of `impl/onebrain_v4.zag` vs the verified v3
reference `ref/docs/lab/onebrain3/impl/onebrain_v3.zag`. (b) Grep for v7-specific
literals: item ids, query fragments, expected-bid numbers. (c) GEN-stage identity
check across modes (see Attack 4).

**Evidence.**
- The diff shows **exactly the three behavioral deltas** documented in BUILD_LOG.md
  and nothing else: (1) `reint_delib`: `neuter==4 || neuter==6` takes the honest-null
  branch; (2) `ob_audit`: `neuter==5 || neuter==6` skips the 2a/2b `audit_invalidate`
  calls (with the `AUDIT_NODENY` trace marker); (3) `main`: `nov4`→neuter 5,
  `nov4nG`→neuter 6. All other diff lines are comments.
- No `q01`–`q44` literals in code (only R3 item references in comments, e.g. "the q15
  fix"). No expected-bid or answer-string literals in decision paths; the driver
  explicitly ignores the `expected_bid` column ("expected ignored", line 1943).
- The `moby dick` / `melville` / `france` strings live in `kb_kw`/`kb_ans` — the
  12-fact embedded KB, shared machinery vocabulary identical to v3, not v7-specific.
- GEN stage (READ/FACT/BID/ELIM) is **byte-identical across single/onebrain/nov4/
  nG/nov4nG/ablate/poison for all 44 items** (SHA-checked per item; min differs only
  because `run_minimal` is a trace-free driver — its 44 winners agree 44/44 with
  onebrain).

**Verdict: NO-KILL.** No set-specific special-casing exists.

---

## Attack 3 — Attribution confound: nov4nG (24) vs single (12)

**Method.** Split all 8 run outputs into per-item blocks (`redteam/blocks_<mode>/qNN.txt`).
For each of the 12 items where nov4nG ≠ single, extracted the causal trace features
(duel kills, branch winners, null choice). Checked whether CLOSE ever overrides the
reint/argmax winner (all 8 modes × 44 items = 352 blocks). Read `close_call` source.

**Evidence.**
- All 12 flips (q09,q10,q11,q13,q14,q15,q16,q17,q19,q20,q30,q32) share one mechanism:
  a branch duel kills the joke bid, e.g. `DUEL_DELIB kill=4(joke) by=5(mem)` or
  `kill=4(joke) by=1(resume)`; both branch winners converge (14 or 17); the neutered
  null (lowest-hid alive) picks 14/17 where single's argmax picked 13. Example (q09
  nov4nG): `BRANCH_SNAP branch=0 winner=14`, `branch=1 winner=14`,
  `REINT_DELIB winner=14 NEUTERED(null=lowest-hid)`, `CLOSE winner=14 runner=13 cc=1`.
- **CLOSE never overrides**: in 352/352 blocks the CLOSE winner equals the
  reint/argmax winner. `close_call` takes the winner as input and only records a
  read-only close-call flag (`cc=1` iff runner-up within 5). No leakage via close.
- The null inherits duel outcomes only through the **declared** one-shared-ledger
  design (both branches audit the same ledger; PREREG4 §3: "fork/close still run").
  The null itself applies pure hid order — no fork-derived scoring.
- K1‴ holds the duel constant: nov4 and nov4nG fork identically with identical
  duels; the only delta is the reint decision rule. Decomposition:
  - nov4nG − single = **+12** (12 duel-driven flips, 0 breaks)
  - nov4 − nov4nG = **+11** = +14 reint-rule fixes (q21–q28, q29, q31, q33–q36;
    all items where the duel was silent and the rule corrected a one-bid miss)
    **−3 reint-rule harms (q06–q08)**

**Verdict: NO-KILL.** The margin is cleanly attributable; the honest-null ablation is
honest. **Note for the story:** the +12 single→nov4nG gap shows the fork+duel+close
machinery alone carries substantial accuracy — §3's "neither" label for both arms
understates it, but the prereg discloses "fork/close still run", so this is a
presentation note, not a confound.

---

## Attack 4 — Trace oddity: single fork=0 on all 44 items

**Method.** Read `fork_assess` source and the mode wiring in `main`; verified GEN-stage
mode-independence (Attack 2); measured the actual fork pattern in forked modes.

**Evidence.**
- `fork=` records whether the fork machinery **ran**. `single` maps to
  `run_full(mode,path,0,1,0,0)` — `fork_en=0` — and `fork_assess` returns early
  (`FORK_ASSESS skipped (single mode)`). fork=0 in single is by construction, not a
  mislabel.
- PREREG4 §7's "36 fork-target items … (verified pre-freeze)" refers to the fork
  **criterion's inputs** (≥2 evidence readings, top-two fired-bid margin ≤12),
  measured on single-mode ledger state. That measurement is valid because the GEN
  stage is byte-identical across modes (Attack 2) — the criterion reads only
  GEN-stage state.
- Actual fork pattern in all 7 forked modes: **41/44 fork**; non-fork = q38, q39,
  q40 (anchors) only. The 36 designed fork-targets all fork; 5 extra items
  (q37, q41–q44) also satisfy the criterion. No contradiction — 36 was the design
  floor, and more items satisfying a stated criterion is not a violation.

**Verdict: NO-KILL** (reconciled; neither the trace field nor the pre-freeze check
was wrong).

---

## Attack 5 — V4-harm causal attribution (q01–q08)

**Method.** Compared per-item traces across onebrain / nov4 / nov4nG / nG / ablate on
q01–q08, isolating the differential step. The requested "duel-disabled" control mode
does not exist (see A1); the trace itself provides a stronger test.

**Evidence — q01–q05 (H2 forget): the 2a/2b calls are causal.**
- onebrain q01: `AUDIT_DENY_DELIB by=6 ncand=2 cands=[10:rel=2:dep=1,11:rel=2:dep=2]
  chosen=10` → `AUDIT_CLEAN bid=15 dep=10` (the expected forget bid eliminated) →
  branch winners 19 → `REINT winner=19`. The duel reads `no-conflict` in **every
  branch of every mode** — it is behaviorally inert on these items and cannot be
  the cause.
- nov4 q01 (identical fork/duels, V4 skipped): `AUDIT_NODENY … skipped` → branch
  winners 15 → `REINT winner=15` (correct). nov4nG likewise 15.
- nG q01 (V4 on, reint neutered): denial → 19. The harm needs V4 and nothing else.
- onebrain−nov4 = −5 decomposes to **exactly q01–q05** (onebrain breaks those 5,
  fixes nothing). Clean V4-harm attribution on these 5 items.

**Evidence — q06–q08 (H1 correction): the reint rule independently harms.**
- nov4 q06 (V4 **off**): both branches duel `no-conflict`, branch winners 16/16 —
  yet `REINT_DELIB candidates=[bid16[…fact11{inter=1 qual=11}…],bid19[…fact10
  {inter=2 qual=22}…],…]` → `REINT winner=19 nullcase=0`. The REINT_RULE's own
  "stronger fact overlap then higher fact quality" ranking picks bid19 over bid16
  with no V4 involvement. nov4 = 19 (wrong), same as onebrain.
- This **falsifies DESIGN_NOTES.md** (lines 12, 47), which predicted "Without V4,
  bid16 (232, grounded) outscores bid19 (224) → `nov4` picks 16." The designer's
  manual simulation assumed score-ordering; the actual rule ranks by fact strength.
- onebrain q06 reaches 19 by the V4 path (denial of fact 11 → `AUDIT_CLEAN bid=16`).
  Two independent paths, same wrong answer.

**Verdict: NO-KILL on the claim** (K2‴ is numeric: −5, bar not triggered; q01–q05
provide clean mechanism evidence), **but AMEND required (A2, A3)**: q06–q08 do not
isolate V4 harm — the design note's prediction for nov4 was wrong, and claim 2's
mechanism evidence is 5 items (q01–q05), not 8.

---

## Attack 6 — Fresh mini-set (8 new items, predictions pre-registered)

**Method.** Authored `redteam/miniset.tsv` (ids r01–r08; 2 V4-binding, 4
reintegration-room, 2 support-quality; new queries, new fact pairings — never
executed before prediction). Wrote per-mode winner predictions in
`redteam/PREDICTIONS.md` **before** running. Ran all 8 modes with the rebuilt binary.
Predictions: 7 modes × 8 items = 56 predictions.

**Result: 27/56 correct (48%) — systematic misprediction, but located entirely
at the GEN stage, never at the deliberation rules.**

| item | predicted → actual (single/nov4nG/nov4/nG/onebrain/ablate/min) | what happened |
|---|---|---|
| r01 (H2) | 15/15/15/**19**/**19**/**19**/**19** → all **15** | fork gate missed by 1 pt: `margin=13` (>12) → `decision=0` → V4 never fires |
| r02 (H1) | 16/16/**19**/**19**/**19**/**19**/**19** → all **16** | both facts associated at inter=3; V4 denied the *challenge* fact (`AUDIT_CLEAN bid=19`) — V4 **helped** |
| r03 (duel) | 13/**14**/**14**/**14**/**14**/**14**/**14** → all **13** | joke bid grounded in the *strong* fact (fid=6); duel silent |
| r04 (duel) | 13/17/17/17/17/17/17 → 13/17/17/17/17/**13**/17 | ✅ duel-kill replicated exactly (`kill=4(joke) by=1(resume)`); ablate=13 via branch disagreement + null tiebreak |
| r05 (reint 1-bid) | 17/17/**18**/17/**18**/**18**/**18** → all **17** | resume bid grounded the stronger fact; reint kept 17 |
| r06 (reint 1-bid) | 13/13/**14**/13/**14**/**14**/**14** → all **13** | duel silent; reint candidates indistinguishable → lowest-hid 13 |
| r07 (supp) | 13/**14**/**14**/**14**/**14**/13?/**14** → all **13** | duel silent; all modes agree |
| r08 (supp) | 13/17/17/17/17/13/17 → 13/17/17/17/17/13/17 | ✅ exact match incl. ablate=13 |

**What survived:** every deliberation rule behaved exactly as documented in every
trace — the fork criterion (≤12) applied exactly, duel victim/challenger logic
exact, V4 denial chose per rel/dep, the reint rule ranked per its stated criteria.
r04/r08 replicate the duel-kill mechanism precisely on fresh items.

**What failed:** an item author cannot steer the ledger microstructure (which facts
associate at which inter/qual, which bonus points land, whether the margin lands
≤12) from surface query text. Consequences:
- (a) **Knife-edge fork gate** (→ A4): r01 missed forking by ONE bonus point
  (bid19 bonus=1 not 2 → margin 13). The v7 H2 items sit exactly at margin 12.
- (b) **V4 is least-disruptive, not harmful** (→ A3): r02's denial bound the
  challenge fact and helped. The v7 H2 items were *designed* so least-disruptive =
  harm (DESIGN_NOTES §3 says so explicitly) — the harm observation is
  design-entangled and does not generalize.
- (c) The round's actual methodology already compensates: Crew P's pre-freeze
  single-mode structural verification (explicitly permitted by PREREG4 §6) is the
  step that lands the microstructure; my blind authoring skipped it, which is why
  6/8 missed.

**Verdict: NO-KILL on the mechanism story** (the deliberation rules replicated
where their preconditions held); **AMEND required (A3, A4)** on generality and
fragility.

---

## Attack 7 — Determinism + no-RNG

**Method.** (a) Rerun identity: RUNLOG's 24-run record + independent reproduction
(Attack 1). (b) Source grep for `rand|r
...[truncated 1936 chars]