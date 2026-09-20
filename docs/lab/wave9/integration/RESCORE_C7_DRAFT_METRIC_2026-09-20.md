# EXPLORATORY RE-SCORE UNDER DRAFT (UNAPPROVED) METRIC — NOT A VERDICT. §5 FAIL under the preregistered metric stands.

**Status:** independent re-score analysis of the INT-1 C5-redesign S10
(commit `5ccc8bb7`, repo `sylorlabs/TNN`) under the DRAFT amendment
`DRAFT_AMENDMENT_2026-09-20-C7-METRIC-REDESIGN.md` §3, which is **local-only,
unapproved, and NOT in effect**. This document changes no bar, overturns no
verdict, and approves nothing. The §5 FAIL on C7 (914→897 vs 897→897) stands
as the binding verdict of that run. What follows is what the committed ledger
says *if* the draft metric were adopted — computed so Micah has the full
picture.

## 1. Draft metric definition (inlined; the draft is not on the branch)

- `cap = composites_ok + commits_constr + hypotheses_autonomy`
- `hypotheses_autonomy = proactive O2 hypotheses + ELECTED L1 abstain-hypotheses`
  (forced ones excluded).
- **FORCED** = ledger chain: `SEAM_REFUSED_PARTITION` refusal
  (`LG_O4`/`LG_OP_COMPOSE`, rc=311, b1=need_id, b2=0, a1=claim_cid,
  `trace.*=-1`) → abstain (`LG_O4`/`LG_OP_ABSTAIN`, same need_id) → L1
  hypothesis opened (`LG_O2`/`LG_OP_HYP_OPEN`, same cid), linked by
  need_id/claim_cid + episode adjacency.
- **ELECTED** = the abstain was system-determined (n=0 / unsatisfiable-need
  path), not refusal-triggered.
- Bar unchanged: within-run `cap5 == cap4` → ALIVE; `cap5 < cap4` → FIRED.
- Void condition: if the C7 positive control fails to convict under the new
  metric, the redesign is void.

In the committed code the preregistered (old) metric is
`cap = composites_ok + commits_constr + met.hypotheses + tr.l1_opened`, where
the code comments label `met.hypotheses` "proactive O2 hypotheses" and
`tr.l1_opened` "L1 abstain-hypotheses". Under the draft, then,
`cap_new = cap_old − forced` per stage (forced = refusal-fed L1 hypotheses
opened). This is exactly the draft's own expected re-score (DC-4: 914−17=897).

## 2. Method (deterministic, zero RNG)

The committed evidence keeps summaries only (full logs ephemeral), and the
binary emits no ledger dump — `impl/check_c5redesign.py` re-derives verdicts
from CHECK/COMPOSITES/L1COVER lines but does not parse the ledger. Procedure:

1. Copied `impl/` to /tmp; verified byte-identical to the committed evidence
   (`sources.sha256` match, all files).
2. Built the pristine copy with the committed toolchain: binary SHA-256
   `e673bae2c889b117db7656a4b77c11c4974bf6cd4823f05c50b806894c25acf0` —
   **byte-identical to the committed trial binary**.
3. Applied **print-only** instrumentation at the exact call sites that append
   the ledger entries (refusal site in `seam4_compose`, `seam4_abstain`,
   `seam2_open`, and the two loop.zag abstain branches), emitting
   `CHAIN_REFUSAL,ep,need_id,claim_cid` /
   `CHAIN_ABSTAIN,ep,need_id,cid,rc,orc` /
   `CHAIN_HYPOPEN,ep,cid,rc` /
   `CHAIN_FORCED,ep,need_id,cid,rc` /
   `CHAIN_ELECTED,ep,need_id,cid,rc`, plus per-stage `CAPCOMP` component
   lines. No computation changed (one provably-neutral `let` hoist so the
   open-rc is printable).
4. Ran stages s2–s5 (paired a/b) and `controls`. The instrumented run
   reproduced the committed `C7_TELEMETRY` **exactly**:
   `old4,862,old5,258,cons4,604,cons5,0,cap4,914,cap5,897` — cross-check
   against `RESULTS_S10_C5REDESIGN.md` passes; instrumentation is
   behavior-neutral.
5. Linked chains in Python: a forced hypothesis = `CHAIN_REFUSAL` →
   `CHAIN_ABSTAIN` (rc=0, orc=0) → `CHAIN_HYPOPEN` (rc=0), same episode,
   same need_id / same cid.

Determinism: CHAIN output byte-identical across paired a/b reps for all four
stages. Zero RNG per the independent checker's static scan.

## 3. Forced-hypothesis counts per stage (ledger-chain verified)

| stage | refusals (rc=311, b2=0) | forced chains (complete) | elected abstains | l1_opened |
|---|---|---|---|---|
| DC-2 | 17 | **17** | 12 | 29 |
| DC-3 | 17 | **17** | 0 | 17 |
| DC-4 | 17 | **17** | 0 | 17 |
| DC-5 | 0 | **0** | 0 | 0 |

Total: 51 refusals → 51 complete forced chains. **Zero broken chains, zero
orphan refusals, zero orphan forced lines, zero duplicate links, all
`rarc=0`** (every forced abstain opened its hypothesis). The ~17-in-DC-4 / 0-in-DC-5
expectation is confirmed, not assumed. DC-2's 12 elected abstains are the
genuine n=0 `force_abstain` path (repair §10), untouched by the draft.

## 4. Recomputed caps under the draft metric

Per-stage components (`CAPCOMP`: composites_ok, commits_constr,
met.hypotheses, l1_abstains, l1_opened):

| stage | cok | ccon | mhyp | opened | cap_old | forced | **cap_new** |
|---|---|---|---|---|---|---|---|
| DC-2 | 256 | 0 | 639 | 29 | 924 | 17 | **907** |
| DC-3 | 256 | 2 | 639 | 17 | 914 | 17 | **897** |
| DC-4 | 256 | 2 | 639 | 17 | 914 | 17 | **897** |
| DC-5 | 256 | 2 | 639 | 0 | 897 | 0 | **897** |

- `cap_old` recomputed from components reproduces the committed numbers
  (DC-4 914, DC-5 897) exactly.
- **C7 under the draft metric: 897 → 897 → ALIVE** (bar `cap5 == cap4`
  satisfied). Matches the draft's expected re-score.

**Mechanism note (why the arithmetic is clean):** `met.hypotheses` is flat at
639 across DC-3/4/5 despite +17 forced abstains — the 17 forced hypotheses
displaced exactly 17 proactive O2 hypotheses via the `o2_cap` claim-id budget
(proactive opens only on even episodes while `next_cid < o2_cap`). The
old-metric inflation (+17) came **solely** through `tr.l1_opened`. The draft
exclusion therefore subtracts exactly the confound, no more.

## 5. Positive control under the draft metric — STILL CONVICTS

The intact redesign run's own positive control did not execute
(`c7_run` returns early on `cap5<cap4`; documented in RESULTS). Per the
committed calibration procedure I built the gate-less variant (default gate
excised, everything else identical, same instrumentation) and ran `controls`:

- Intact arms: `cap4=897, cap5=897`, `CHECK,c7_withdrawal,0,0` — C7 ALIVE in
  the calibration harness, as reported.
- Teacher-dependent arms: dep4 = (cok 256, ccon 2, mhyp 639, opened 0) → 897;
  dep5 = (cok **0**, ccon 2, mhyp 639, opened 0) → **641**.
  `C7_POSCTRL,cap4d,897,cap5d,641` — reproduces the committed calibration.
- **Zero `CHAIN_REFUSAL` and zero `CHAIN_FORCED` lines anywhere in the
  gate-less run** (11,502 `CHAIN_HYPOPEN` lines, all proactive). No
  refusal-fed hypothesis exists in either teacher-dependent arm —
  structurally impossible (gate excised) and observationally confirmed.
- Under the draft metric: forced=0 in all arms → reads identically,
  **897→641 → C7 FIRES DEAD on the teacher-dependent variant**.
- Collapse decomposition: `composites_ok` 256→0; `commits_constr` 2→2;
  hypotheses 639→639; l1 0/0→0/0. (The draft's "composites/commits" phrasing
  is composites-only in the measured decomposition; the load-bearing fact —
  zero refusal-fed hypotheses involved — holds either way.)
- The draft's void condition does **not** trigger: the positive control
  convicts under the new metric.

(The only failing check in the gate-less controls run is
`CHECK,c5_lesion,1,0` — expected: the instrument fires on the broken variant,
exactly the documented calibration result.)

## 6. Repaired-baseline sanity check — unchanged 897→897

The repaired baseline (sources @ `5aa2fb13` + behavior-neutral telemetry)
**structurally cannot contain forced hypotheses**:

- At `5aa2fb13`, the default-path verdict gate sat behind the
  `cfg.c5_strict` flag (retired by the C5 redesign); and `loop.zag` at that
  commit contains **no** `SEAM_REFUSED_PARTITION` routing at all — refusals
  kept silent semantics, so no refusal could feed L1. (Verified via the
  GitHub blob at that commit.)
- Committed repair evidence agrees observationally: per-stage `L1COVER`
  abstains = 0 in DC-3/4/5 (DC-2's 12 are elected `force_abstain` n=0
  abstains); `C7_TELEMETRY … cap4,897,cap5,897`; `C7_POSCTRL,cap4d,897,cap5d,641`.

Under the draft metric: forced=0 → **897→897, ALIVE — identical to the
preregistered reading**. The baseline's positive control (897→641) likewise
involves zero refusal-fed hypotheses (the routing did not exist). The draft
does not move the baseline.

## 7. Anomalies and caveats

1. **No ambiguous ledger linkage.** All 51 forced chains are complete
   1:1 triples; nothing required judgment calls. (Reported as a finding, not
   a gap.)
2. **Ledger access is indirect.** The binary emits no ledger dump, so the
   chain was identified via print-only instrumentation at the exact ledger-
   append call sites on a byte-identical source tree and binary. The emitted
   tuples correspond 1:1 to committed-ledger entries by construction
   (deterministic, byte-identical reruns). A future ledger-dump opcode would
   make this direct.
3. **`check_c5redesign.py` does not parse the ledger** — it re-derives
   verdicts from CHECK/COMPOSITES/L1COVER lines. The chain analysis here is a
   separate instrument; both agree on all overlapping numbers
   (C7_TELEMETRY, L1COVER, composites).
4. **DC-2 re-scores to 907, not 897** (924−17; its 12 elected abstains are
   retained as autonomy). C7 only compares DC-4/DC-5, so this does not affect
   the C7 outcome; reported for completeness.
5. **Scope.** This re-score covers only the §3 metric change. It does not
   validate the draft's §5 instrument-only-amendment precedent, §6 S100
   un-gating conditions (independent-checker verification of the re-score is
   still pending), or §7 forward falsifiers — those remain Micah's call.

## 8. Bottom line for the morning tap

- Under the **preregistered** metric: §5 FAIL stands (914→897 vs 897→897).
  Nothing here changes that.
- Under the **draft (unapproved)** metric, the committed ledger re-scores to
  **cap4=897, cap5=897 → C7 ALIVE**; forced counts are 17/17/17/0 across
  DC-2/3/4/5, every one ledger-chain-verified; the positive control still
  convicts (897→641, zero refusal-fed hypotheses, collapse in
  `composites_ok`); the repaired baseline is untouched (897→897).
- The draft's void condition does not trigger. Approval remains a single tap
  Micah has not given.

*Analysis methods: deterministic re-execution of the committed byte-identical
binary with print-only chain instrumentation; paired reps byte-identical;
zero RNG. No verdict is rendered — that authority sits with Micah and the
prereg, not this document.*
