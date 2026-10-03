# REPORT: Behavior-Change Invalidation -- Verdict BEHAVIOR-CHANGE INVALIDATION POISONS (BOUNDED)

Date: 2026-10-02. Worker: compose-beh (behavior-change invalidation
follow-up to C345 CONTRACT RE-TEACHING LEAVES AN INERT STALE BIT
(SELF-SHIELDING)).
Battery: Q1 seed + Q2 transfer on D5 (reproduction), then a mid-lifetime
world change (setup_d5b: 44 loses subject status so X stops emitting NODE
at out, every contract mask unchanged), then Q3B on D5B (s=42, same shape
as Q2). Two arms (P persistent ledger, N fresh-ledger control), pure Zag,
pinned znc. Prereg committed alone before implementation (ae4159c6f).

## Verdict: BEHAVIOR-CHANGE INVALIDATION POISONS (BOUNDED)

K1-K7 all pass exactly as frozen, 3/3 byte-identical per arm. Priming
fires on the genuinely-false bit (WTRIG=3, exactly the primed set
(2,0),(2,1),(2,3)) at exactly the primed-set try cost: P pays 4 tries on
Q3B against N's 1 try, a poison cost of +3 tries. The false bit persists
verbatim (no correction path exists under frozen U1-U5). This is the true
poison flavor, and it contrasts exactly with C345: contract-growth
invalidation is self-shielding (0 tries); behavior-change invalidation
actively misleads (+3 tries). The cost is bounded by the primed-set size,
never corrupts the answer, and triggers no runaway.

## Results

Format: ANS / TRIES / WIDEN / WTRIG / INTER ; WBACK in parentheses for P.

| Query | P observed (predicted) | N observed (predicted) |
|-------|------------------------|------------------------|
| Q1 | 2/6/1/2/44 (0) (2/6/1/2/44 (0)) | 2/6/1/2/44 (2/6/1/2/44) |
| Q2 | 2/3/1/3/44 (0) (2/3/1/3/44 (0)) | 2/6/1/2/44 (2/6/1/2/44) |
| Q3B | 2/4/1/3/-1 (0) (2/4/1/3/-1 (0)) | 2/1/0/0/-1 (2/1/0/0/-1) |

Every cell matches its frozen prediction exactly. Poison cost: 4 - 1 = 3
tries, exactly the primed-set size.

## Kill bar results

- K1 SEED FIDELITY: PASS. P-Q1, N-Q1, P-Q2, N-Q2 blocks byte-identical to
  the compose_inval lane Q1/Q2 blocks (verified by diff, including the
  pre-ARM WADD/INTER lines). P-Q2 = 2/3/1/3/44 (0) with WTRIG=3 and
  WADD=2,0 / 2,1 / 2,3; N-Q2 = 2/6/1/2/44 with WTRIG=2. 3/3.
- K2 TRANSFER REPRO: PASS. P-Q2 strictly fewer tries than N-Q2 (3 < 6);
  ANS=2 in both. The bit was genuinely true and helpful before
  invalidation. 3/3.
- K3 POISON FIRES: PASS. P-Q3B = 2/4/1/3/-1 (0) with WIDEN=1, WTRIG=3,
  and exactly WADD=2,0 / WADD=2,1 / WADD=2,3 in scan order before any
  INTER line; the three primed pairs each log INTER=44 and record no new
  miss (X emits NUM, covered by the unchanged outmask {2}; A(44), B(44),
  Y(44) all -2), so no R1 fires. N-Q3B = 2/1/0/0/-1 with zero WADD lines
  and WTRIG=0. The self-shielding derivation does not apply, and the
  experiment confirms priming fires on the false bit. 3/3.
- K4 BIT PERSISTS: PASS. P LEDGER block after Q3B byte-identical to P
  LEDGER after Q2 (m2 out=1, all else 0; verified by cmp); N LEDGER all
  zero after Q3B. Q3B recorded nothing. The false bit is never corrected:
  the only ledger write in the frozen code is the idempotent lg_add, and
  U3 forbids clearing. 3/3.
- K5 POISON BOUNDED: PASS. P_Q3B TRIES (4) minus N_Q3B TRIES (1) = 3;
  ANS=2 in both Q3B blocks; WBACK=0 in both Q3B blocks; P_Q3B TRIES = 4
  <= 6. No wrong answer, no backstop, no runaway. The Q3B CENSUS masks
  are all inmask {1}, outmask {2} for both arms, confirming the contract
  was unchanged under D5B. 3/3.
- K6 DETERMINISM: PASS. 3/3 byte-identical whole-output per arm.
  Run digests: P 44966eb3f39ae284d19033f2bc4cf57c74da0824da71b1deb91f33ca5007ebc0,
  N ee643e52be5ec09b84da21f576e4242ad9763c0ac68cc018d8fc41605477606f.
  Binary digests: P 1200df8fb6967fed7eccb6487bc18ec0a4e4df0fa5ada4eb0e23e73d0a057112,
  N 9d35e00eb37771611df39cd3a360e21579a612892302166bb8948b4e14646ea2.
  Source digests: b_full_P.zag 534cbfeea49b3ef86be003481299c5fe32f1de4105bb85b03699d6fd6e17a7b2,
  b_full_N.zag 3ec12216859149fcbf4335eb2faf5b8a7708e23e1ed0fb0844d8950435441ed0.
- K7 HYGIENE: PASS. Zero em/en dash bytes in all docs (byte-verified);
  safebin guard attested in NAMECHECK.md Step 0 (which python3/python
  return NOTHING); pure Zag for all scientific computation; pinned znc
  src/tools/toolchain/znc_linux_x86_64_abed8aa1; compose_ledger and
  compose_inval lanes untouched (verified via git status: no output for
  those paths); all new files under compose_beh/; no mode/policy
  identifier in the composer (grep over non-comment lines: zero hits).

## Why this matters

C345 left exactly one open follow-up: the self-shielding argument covers
only contract-growth invalidation. This battery closes it. When the
contract is unchanged and the emission facts change, the carried bit
becomes genuinely false while the admission structure stays intact, and U4
priming fires on it exactly as the frozen analysis predicted: WTRIG=3,
the full primed set tried first, each failing cleanly, at a cost of
exactly +3 tries versus the fresh ledger. There is no correction: the
false bit persists verbatim into all future queries (K4), and the learner
has no machinery to detect or clear it.

The unbounded-lifetime choice (U3) is therefore not free, but it is not
catastrophically unsafe either. A stale bit imposes a real, recurring tax
of up to the primed-set size whenever its primed pairs miss, and it never
self-corrects. The governance question is now precise: does +primed-set
tries per stale bit warrant a learner-observable invalidation rule (for
example, retiring a carried bit whose justifying emission repeatedly
fails to re-occur on direct trial), or is the bounded tax acceptable as
the price of persistent coverage knowledge? The experiment supplies the
cost; it does not set the policy.

## Architecture accounting

- Cognition lines added: ~19 (setup_d5b) + ~10 (main deltas in
  b_pers.zag / b_ctrl.zag); composer functions byte-copied from the
  ledger lane (0 new logic lines; the U1-U5 rules, S2 pin, and R1/R2 are
  frozen, not re-litigated).
- New hardcoded semantic cases: 0. Modes/bridges/handlers: 0.
- Researcher-owned: D5B fact changes, the Q1/Q2/Q3B sequence, the frozen
  U3/U4 rules under test, the researcher-installed answer relocation
  (A(42)=2).
- Learner-owned: kind-set contracts, the carried missbits ledger
  (including the false bit), per-query primed/admitted/tried sets.

## Honest limitations

- One behavior-change flavor: emission-kind flip (NODE to NUM at X's out)
  with the answer relocated to an admitted single. The symmetric "vice
  versa" case (a bit becoming true), partial flips, and cyclic changes
  are not covered.
- The D5B answer relocation (A(42)=2 via new 82-facts) is
  researcher-installed to keep the query answerable with the same shape;
  the poison measurement is P-vs-N on the same changed world, so the
  relocation does not confound the comparison.
- On Q3B the primed pairs all failed cleanly (no new misses recorded); a
  behavior change that records NEW misses during primed trials would
  interact with R1 widening, which is untested here.
- Three queries on one world family discriminate the mechanism; they do
  not establish generality of invalidation behavior.
- Expected-answer verification still used (canonical boundary).

## Follow-ups (not claimed)

1. The symmetric "vice versa" case: a carried bit becoming true (a newly
   observed miss kind) and whether priming under-fires.
2. Behavior change that records new misses during primed trials: the R1
   interaction (widening triggered from a false-bit prime).
3. A learner-observable invalidation rule: whether a carried bit whose
   justifying emission repeatedly fails to re-occur on direct trial can
   ground principled retirement without researcher magic numbers; this
   battery characterizes the cost that rule would need to beat (+primed
   set tries per stale bit, recurring).

## Toolchain attestation

Zero invocations of python3, python, or any other forbidden executable.
Safebin PATH throughout; pinned znc by absolute path; no incidents to
disclose. One transient git index.lock (another worker's operation)
delayed the prereg commit by one retry; the lock file was gone on
re-check and the commit landed cleanly.
