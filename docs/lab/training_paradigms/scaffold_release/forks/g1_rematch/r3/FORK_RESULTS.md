# FORK RESULTS — G1-R3: gradual fade of the scaffold signal

**Prereg:** `FORK_PREREG.md` (frozen, commit `585602fc`, before
implementation). **Runner:** `run_fork.sh` → **ALL RUNNER CHECKS PASS**
(43/43 checks, 0 mismatched, `TN_FAILURES,0`, byte-identical reruns,
sha256 `60ea9a8ad3c9d0305a53eed8e6b1f16933881ecedca1a6153bce1825c3fea650`).

**Fork verdict: R3 PASSES** (KB-1, KB-2, KB-3, KB-5 hold; KB-4 fails as
preregistered).

## What was built

R1's harness with the harness's reward delivery put on the preregistered
fade curve (full through E29; E30–33 every episode; E34–37 every other;
E38–41 every third; E42+ never). The learner's machinery — elimination,
verified streak, learner-fired release rule — is byte-for-byte R1's.
Undelivered reads return the sentinel: no elimination, streak resets.

## Evidence (from `evidence_run1.txt`, byte-identical rerun)

- Commit (CONTEST) at E29, exactly as R1 — the fade starts after commit
  and does not touch elimination.
- **The fade strands the release, exactly as preregistered:** the
  verified streak peaks at 5 (E30–34) and never reaches 8 → the learner
  never fires: fire_step = −1, n_disconnect = 0, connected_end = 1.
- The committed policy acts without the signal: post-commit E30–128,
  33/33 contradictions acted CONTEST, 0 REKEY, 0 OVERWRITE; lifetime
  totals 42 CONTEST / 9 REKEY / 1 OVERWRITE, all as preregistered.
- REFUSE: 0 audited — the refuse path needs a disconnected channel and
  is never exercised (explicit caveat: R3's integrity is behavioral
  only; the post-release refusal machinery never runs).
- Audit entries: 387. Ledger replay exact.
- Baseline: all 18 `a_` lines byte-identical to R1's (diff clean).

## Kill bars

| Bar | Result |
|---|---|
| KB-1 ACQUISITION (commit at E29) | HOLD |
| KB-2 INTEGRITY (33/33 post-commit; refuse path never exercised — caveat) | HOLD |
| KB-3 PERSISTENCE (24/24 E49–128) | HOLD |
| KB-4 VALUE-ADD vs A (14 eps, 193 entries) | **FAIL** — commit at 29, 387 entries, never even released |
| KB-5 DETERMINISM | HOLD |

## Reading

Gradual release is not just a slower sudden release: for
verification-gated machinery, thinning the signal *before verification
completes* prevents release entirely, because the verification currency
is denominated in the fading signal. The schedule decides *whether
release happens*; it still does not move the commit point (E29), which
is where B's loss to teaching lives.
