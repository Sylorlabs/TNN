# TRIAL RESULTS — ledger-gating (Wave-5)

**Verdict: POSITIVE.** All preregistered legs pass; no falsification
criterion tripped. Run 2026-09-19, native Linux x86-64,
`znc 2026.07.0-dev`, via `run_lg.sh`.

## Headline numbers

| Measure | Result | Prereg bar |
|---|---|---|
| False-block rate, honest chains (Leg A) | **0/60** | ≤1/60, exactness required |
| Cheat-block rate (Leg B) | **8/8 adversarial claims blocked (100%)** | 100%, exact verdict codes |
| Belief-revision interaction (Leg C) | revision commits, stale claim blocked, outgrown readings silent | all must hold |
| `LG_CHECK` lines | 433 total, **0 mismatched** | — |
| Determinism | byte-identical reruns, sha256 `dce575cede6f701f6abfb1c48f2749cb8d124640fdac91e221de8a682567949f` | F5 |
| RNG / tables / accumulators | static grep clean; gate takes no counters | F6 |
| Source identity | `il_core.zag`, `hss.zag` byte-identical to wave-4/wave-3 | F7 |

## Leg A — honest chains: 60/60 gate `IL_OK`, 0 blocks

- **A1** (50 episodes, fresh ledger each; `K = 3+(e mod 3)` hypotheses,
  rotating survivor): every gate verdict `IL_OK`, `committed == target`
  in all 50, exactly one COMMIT audit entry, zero gate HOLDs.
- **A2** (10 episodes, one shared ledger, continuing investigation on
  `Q=500` with re-verification each episode): all 10 `IL_OK`; ledger
  head exactly 90 (10 × 9 entries), no overflow; rule-5 latest-VERIFY
  tracking stays exact across sequential claims on one item.
- **C1** (embedded): all 60 episodes contain the noisy pair
  `obs(nz,1)` → `obs(nz,0)` — a bad first reading outgrown inside the
  honest chain. The gate stayed silent on all 60 outgrown readings.

## Leg B — injected cheats: 8/8 blocked, exact verdicts

| ep | Probe | Verdict | Ledger adjudication |
|---|---|---|---|
| 200 | B1: cites VERIFY with wrong val | `IL_LIE_CITED` (101) | claim cites VERIFY(701,9), recorded val 9 ≠ claimed 1 — the ledger shows the contradiction directly |
| 201 | B2: phantom citation (head+50) | `IL_CHEAT_PHANTOM` (105) | citation points past the ledger head |
| 202 | B3a: empty provenance | `IL_CHEAT_EMPTY` (103) | correct value, no chain at all |
| 202 | B3b: cites only HYP | `IL_CHEAT_NOSHAPE` (106) | no genuine evidence behind the value |
| 203 | B4: cites a CLAIM entry | `IL_CHEAT_TRIVIAL` (104) | cited entry's op is CLAIM — non-evidence |
| 204 | B5: contradicts latest committed VERIFY, no fresh VERIFY | `IL_LIE_COMMITTED` (102) | claim locally consistent, but ledger's latest VERIFY(705,*) is v=1 ≠ 0 |
| 205 | B6: claims a refuted value | `IL_LIE_CITED` (101) | cites the genuine REFUTE(706,2) while claiming 2 — caught despite the adversary's forged matching VERIFY |

Every block: `committed` unchanged, zero COMMIT audit entries added,
exactly one HOLD audited with `aux = 1000 + verdict`, and the HOLD is
the audit tail. Post-B3 honest retry of the same item gates clean
(`IL_OK`, commits) — blocks are specific, not state-poisoning.

## Leg C — belief revision: the gate preserves it

- **Episode A** (ep 300): honest chain commits slot 1 for `Q=7`, gate
  `IL_OK`. `VERIFY(7,1)` is now the committed belief.
- **Episode B** (ep 301): `obs(1,0)` refutes the committed slot 1 →
  HSS UNCOMMIT (1 UNCOMMIT audit entry, `committed=-1`), ledger
  `REFUTE(7,1)`; fresh hypotheses 3,4 activated, elimination leaves
  slot 4 → gate `IL_OK` (the fresh `VERIFY(7,4)` is the latest), commit
  slot 4. **The legitimate revision is not punished.**
- **Stale probe** (ep 302): `CLAIM(7,1)` on episode A's chain →
  `IL_LIE_COMMITTED`, blocked, `committed` stays 4, audited HOLD
  (`aux=1102`). **The old belief cannot be smuggled back.**
- **C3** (ep 303): episode A's outgrown `OBSERVE(7,1)`, *cited* by a
  `Q→4` claim → still `IL_OK`: `VERIFY(7,4)` sits between it and the
  claim, so the supersession rule keeps the gate silent. Outgrowing a
  bad first reading is never flagged — the wave-4 S8 principle survives
  gating, both uncited (60× in Leg A) and cited-but-superseded.

## Gate/eliminative-logic disagreements (preregistered log)

73 `LG_GATE` events; 8 blocked — exactly the 8 expected adversarial
disagreements above (B1, B2, B3a, B3b, B4, B5, B6, C2-stale), each
adjudicated from the ledger in the table. **Zero disagreements in the
60 honest events.** No unexpected disagreement occurred. The reverse
disagreement (gate passes ∧ substrate holds) is structurally impossible:
the gate only fires on a sole survivor.

## Falsification review (F1–F7)

- F1 (escape/misfire): none — 8/8 blocked with exactly the preregistered codes.
- F2 (honest punished): none — 0/60 blocks; the <2% tolerance was not needed.
- F3 (revision punished): none — revision commits, stale blocked, outgrown silent.
- F4 (block mishandled): none — every block left `committed` unchanged,
  added no COMMIT, recorded exactly one naming HOLD.
- F5 (non-determinism): byte-identical reruns.
- F6 (RNG/tables): grep-clean; the gate never sees confirmation counters
  (runner check 2b).
- F7 (source tampering): both sources byte-identical to wave-3/4.

## Honest negatives / non-claims (first-class)

- N1: The gate trusts the driver's ledger writes — the honest-ledger
  assumption is inherited from wave-4, not proven here. Ledger forgery
  still defeats this layer (stated in DESIGN.md §7).
- N2: An internally legitimate but factually wrong chain gates clean
  (honest-mistake boundary, inherited). Integrity ≠ omniscience.
- N3: Provenance width 4 is inherited: episodes with >2 rivals cite the
  first two REFUTEs. The predicate needs evidence + judgment, not the
  full forensic trail.
- N4: Re-verification amnesty is inherited: a later `VERIFY(Q,v')`
  supersedes `VERIFY(Q,v)` without the checker asking why. A
  deliberate reversal and a quiet flip look identical here.
- N5: In the trial the driver can still call `hss_commit` directly; the
  integrity claim is conditional on the claim path going through the
  gate. A deployed wiring makes `hss_commit` gate-internal.
- N6: The 64-entry HSS audit cap was respected by construction (leg C
  peaks at 44/64); long-horizon audit sealing is still future work.

## Files

- `PREREG.md` — preregistration (written before implementation).
- `DESIGN.md` — the mapping, gate contract, HOLD encoding, disagreement rule.
- `lg.zag` — the gate (new; imports unmodified `il_core.zag`, `hss.zag`).
- `lg_trial.zag` — trial driver (new; 60 honest + 8 cheat-boundary + revision).
- `run_lg.sh` — runner (static checks + determinism + check verification).
- `il_core.zag`, `hss.zag`, `substrate/` — byte-identical copies of the
  wave-4 checker / wave-3 substrate (verified by `cmp` in the runner;
  hashes in `SOURCES.sha256`).
- `evidence_run1.txt`, `evidence_run2.txt` — byte-identical outputs
  (sha256 `dce575…`); `evidence_compile.txt` — clean compile log.
- `lg_trial_linux` — the trial binary (reproducible via `run_lg.sh`).

## Recommended next step

Two, in order. (1) The wave-4-recommended follow-up, still open: make
`VERIFY` cite its superseding evidence so belief-flips carry their own
justification chain — this closes honest boundary N4 (the amnesty this
trial inherited and explicitly did not test). Red-team that boundary
with unmotivated flips. (2) In the post-toy five-organ integration, wire
`lg_attempt_commit` as the claim path of the deliberate-memory
substrate organ, with `hss_commit` made gate-internal (closing N5), and
run the developmental curriculum at 10x through the gated path —
measuring false-block rate under the seven-control evaluation battery.
