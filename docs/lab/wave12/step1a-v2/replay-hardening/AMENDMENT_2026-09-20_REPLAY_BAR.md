# DATED AMENDMENT — 2026-09-20 — REPLAY-2026-09-20-v1 bar & procedure

**Status:** PROPOSED — PENDING Micah's re-approval. Standing law: changes to
frozen rules (prereg `PREREG_REPLAY_MATRIX.md`, freeze commit `0f5cf8c594ee`)
need his sign-off. The implementation below was built and run against this
amendment; verdicts marked accordingly until he signs.

## Item A — Bar re-scope: frozen dirty1_urandom / dirty2_clock

**Finding (empirical, pre-freeze):** the frozen v2 plants are behaviorally
constant functions of their inputs and *cannot* diverge under any replay:

- `dirty1_urandom`: `nio_open_root("/dev/urandom")` opens with `O_DIRECTORY`
  (substrate line 58); `/dev/urandom` is not a directory → open fails →
  nothing is ever read. Output `out[0]=input[0]` on every run.
- `dirty2_clock`: `clock_gettime` with a NULL timespec → EFAULT → `rc<0` →
  early return, output buffer untouched (zeros) on every run.

Both *invoke* a nondeterminism mechanism without *consuming* nondeterminism.
No replay harness can make a constant function diverge — mathematical fact,
not a harness weakness. v2 caught both statically (4.1/4.6 and 4.2), which is
the correct layer for mechanism-without-consumption.

**Amendment:** the "MUST diverge" bar is re-scoped to *behavior-affecting*
plants. Frozen dirty1/dirty2 carry the amended expectation **PASS**
(replay correctly passes; static tripwire catches). The divergence bar for
the entropy/clock *classes* is carried by the two prereg-specified
strengthened plants `dirty1b_entropy_read` (16 entropy bytes reach stdout)
and `dirty2b_clock_read` (tv_nsec reaches stdout), which MUST diverge.

## Item B — Procedure fix: determinism-control consequence (§7.3)

**Finding (from the scored runs):** the §7.3 determinism control (re-run the
r0 binary twice under identical conditions) *mismatches* for dirty5_aslr,
dirty1b_entropy_read, and dirty2b_clock_read — because those plants are
nondeterministic **per process** (ASLR slide, entropy, clock), so even
identical conditions diverge. The frozen procedure maps any control mismatch
to `ERROR`, which would report "harness inconclusive" for exactly the plants
the bar most wants flagged.

**Amendment:** control mismatch with all exits 0 → **DIVERGE** (pair
reported as `control_a,control_b` when no matrix run-pair diverged;
otherwise the matrix pair stands and the mismatch is recorded as
corroboration). Control exit ≠ 0 → still `ERROR` (fail-closed).
**Soundness argument:** the clean module's control *matches* (evidence:
`variation.evidence.txt`, `match=1`), proving the harness + instrument are
deterministic per se — so a control mismatch isolates genuine trial
nondeterminism, the strongest divergence signal. A mismatch can no longer
be mistaken for harness flakiness while clean passes.

## Item C — Disclosures (not rule changes; recorded for the audit trail)

1. **Instrument correctness fix (nio_cstr terminator).** The adversarial
   substrate exposed a latent zero-dependence in the substrate's own
   `nio_cstr`: it never wrote its NUL terminator (relying on zero-fill).
   Under adversarial fill every file open failed (`NOSTATE`). Fixed in the
   template by explicitly writing `b[s.len]=0` (`adv_cstr_fix`). The
   terminator byte is kernel-visible only, never trial-observable; the
   template↔real diff documents the delta exactly.
2. **Baked-tag design (prereg §1.8).** Strict Zag modules have no
   user-global storage (compiler error observed), so the per-run tag could
   not be passed to `nio_alloc` at runtime; it is baked as `const ADV_TAG`
   at build time (8 substrate copies, hashes logged). Deterministic per
   run, varying across runs, no RNG.
3. **Naive pre-dirtying proven ineffective (W2).** The BEFORE leg (real
   zeroing substrate + the amendment's literal allocate-and-fill recipe)
   shows 8/8 identical outputs on dirty3 — the v3 amendment's literal
   item-6 recipe does not defeat `nio_alloc`'s unconditional zeroing. The
   AFTER leg (adversarial fill) diverges on all 8. The W2 fix is the
   adversarial fill, not the pre-dirtying alone.

## What does NOT change

- N=8, the §8 condition matrix, PASS/DIVERGE/ERROR definitions otherwise,
  the per-plant expectations for dirty3 (DIVERGE), dirty4 (PASS — honest),
  dirty5 (DIVERGE), variation clean (PASS, no false positives), dirty1b
  (DIVERGE), dirty2b (DIVERGE).
- The residual-risk taxonomy (prereg §10) stands verbatim.
