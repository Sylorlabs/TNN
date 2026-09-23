# TRIAL_RESULTS — hypothesis-state-substrate

**Date:** 2026-09-19. **Native Zag, Linux x86-64, `znc 2026.07.0-dev`.**
Preregistered in PREREG.md *before* any run; no amendments were needed
(the program-law update arrived before implementation and was incorporated
into the prereg, not patched in after).

## Headline

**All 7 prereg predictions held; no falsification criterion tripped.**
49/49 `HSS_CHECK` lines pass, `HSS_FAILURES,0`, two runs byte-identical
(sha256 `b285026f…87a25e`), no randomness anywhere (static grep),
commit region provably free of score/counter references (static token scan).

## The key result (E1 — the discriminator)

The substrate committed to hypothesis **B** (slot 1, 2 confirmations) while
the argmax-over-scores control committed to hypothesis **A** (slot 0, 3
confirmations — the most). A was refuted by direct contradiction of a
defining claim at step 4 despite holding the highest confirmation count:

```
HSS_AUDIT,4,2,1,19   <- step 4, OBSERVE, slot A, index 2, outcome REFUTED (2*8+3)
HSS_AUDIT,4,2,2,17   <- slot B, index 2, outcome CONSISTENT (no claim there)
HSS_AUDIT,4,2,3,19   <- slot C, REFUTED
HSS_AUDIT,5,3,2,0    <- step 5, COMMIT, slot B (last one standing)
```

The commit decision used the survivor count (1), never the counters. The
argmax control — the naive score mechanism, harness-only — picked the
refuted hypothesis. **Disagreement is the positive evidence: the system is
not argmax with extra steps** (falsification tripwires F1–F4 all clear).

## Per-curriculum outcomes

| Curriculum | Expected | Observed |
|---|---|---|
| E1 discriminator | COMMIT B; argmax→A; DISAGREE | COMMIT slot 1; argmax slot 0; DISAGREE=1 ✓ |
| E2 non-uniqueness | HOLD count=2, no commit; argmax commits | HOLD aux=2; 0 COMMITs; argmax→slot 3, substrate held ✓ |
| E3 total refutation | HOLD count=0, no crash | committed=-1, clean ✓ |
| E4 revocable commit | COMMIT then UNCOMMIT | 1 COMMIT + 1 UNCOMMIT, final -1 ✓ |
| E5 vacuous refusal | HSS_VACUOUS, slot inactive, REFUSE logged | rc=-350103 (boolean-checked), REFUSE=1, later valid activation OK ✓ |

E2 is the abstention result: with two surviving hypotheses and zero
contradictions, the system *held* — abstention earned from non-uniqueness of
survivors, not from a probability bucket (DO_NOT_REPEAT.md §8.4 compliant).
E4 proves commitment is not a sticky threshold crossing: the committed
hypothesis was refuted by later evidence and the commitment revoked.

## Static evidence (white-box, in the runner)

- **No randomness:** comment-stripped sources contain no `rng`/`rand(`/`srand`/
  `/dev/urandom`/`seed` token — in substrate, world, or harness.
- **Commit-region token scan:** every identifier between the
  `COMMIT-REGION-BEGIN/END` markers is in the allowlist
  (`active`, `capacity`, `committed`, `step`, `abuf`, `acount`, `hss_audit`,
  op constants, Zag keywords). `conf`/`claims`/any score state cannot appear —
  the counters are structurally unreachable from the commit decision.
- **Determinism:** two consecutive runs byte-identical. The system is
  deterministic; the test was adversarial (curricula were *designed* to
  contradict — E1 refutes the leader, E3 refutes everything, E4 refutes the
  committed hypothesis).

## Honest negatives / limits (first-class, per prereg N1–N4)

- **The mechanism requires falsifiable hypotheses.** E5's Popper gate
  (refuse `sig == 0`) is load-bearing: a vacuous hypothesis can never be
  refuted and would block commitment forever. The substrate enforces this at
  activation; hypothesis *generation* (who proposes good slots) is out of
  scope.
- **No recovery path is tested.** After E3-style total refutation the system
  holds correctly but cannot propose replacements. Next step must wire slot
  proposals to a generator (candidate: native-structural-revision's PROMOTE
  proposals).
- **Audit cap is fail-closed, not long-horizon.** 64 entries suffice for the
  mechanism proof (E1 used 36); the 1000-slot/100k-observation scale test
  with sealed audit segments + digest chain is specified in PREREG §7 and
  not run here.
- **Confirmation counters look like scores.** The claim was never "no
  numbers exist" but "numbers do not decide" — the token scan + E1
  disagreement are the teeth. A reviewer who finds a decision path through
  the counters has a NEGATIVE finding; none was found.

## Verdict: POSITIVE

The eliminative commit rule (refute by contradiction; commit iff exactly one
survivor) is implemented, audited, deterministic, RNG-free, and observably
distinct from argmax-over-scores on designed adversarial curricula. The
falsification tripwires were armed and none fired.

## Next step (explicit)

1. **Scale test** (PREREG §7): 1000 slots / 100k-observation adversarial
   curricula, sealed audit segments + digest; measures: commit latency vs.
   slot count, HOLD correctness under non-refuting stretches. Falsifies the
   scale claim if latency goes superlinear or HOLD degrades.
2. **Wire generation:** connect slot activation to a hypothesis proposer
   (native-structural-revision PROMOTE proposals are the natural source) so
   the system recovers from total refutation instead of only holding.
3. Do not scale the confirmation counters into a decision role — that
   direction is banned by this trial's own falsification criteria.

## Evidence bundle (this directory)

- `SUBSTRATE_ANALYSIS.md` — what v1 actually stores/computes + v1→HSS mapping
- `PREREG.md` — preregistration (pre-run) with falsification criteria
- `r34_hypothesis_state_v1.zag` — v1 source as fetched from the repo
- `hss.zag` — the substrate (eliminative commitment + audit)
- `trial.zag` — five designed curricula + argmax falsification control
- `run_trial.sh` — runner (compile, determinism, static checks, verification)
- `hss_trial_linux` — native binary (45,495 bytes)
- `evidence_run1.txt` / `evidence_run2.txt` — byte-identical run outputs
  (49 HSS_CHECK lines, 36-line E1 audit dump, HSS_FAILURES,0)
- `evidence_compile.txt` — compiler transcript
