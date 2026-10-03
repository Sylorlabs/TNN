# REPORT: Contract Re-Teaching With Genuine Bit Invalidation -- Verdict CONTRACT RE-TEACHING LEAVES AN INERT STALE BIT (SELF-SHIELDING)

Date: 2026-10-02. Worker: compose-inval (contract re-teaching follow-up to
C341 PERSISTENT LEDGER HELPS (BOUNDED)).
Battery: Q1 seed + Q2 transfer on D5 (reproduction), then a mid-lifetime
world change (setup_d5x: X re-taught, outmask {2} -> {1,2}) making the
carried bit (m2,out,1) genuinely false, then Q3P on D5X (s=42, same shape as
Q2). Two arms (P persistent ledger, N fresh-ledger control), pure Zag,
pinned znc. Prereg committed alone before implementation (c9c50fc75).

## Verdict: CONTRACT RE-TEACHING LEAVES AN INERT STALE BIT (SELF-SHIELDING)

K1-K4, K6, K7 pass exactly as frozen, 3/3 byte-identical per arm. The
genuinely-false bit persists verbatim forever (no correction path exists
under frozen U1-U5) but cannot prime: U4's filter-rejected gate and the
justification predicate jointly exclude it, exactly as derived frozen in
PREREG Section 3d. Poison cost is 0 tries (P and N behave identically on
Q3P). The unbounded-lifetime choice survives contract-growth invalidation;
the residual cost is latent ledger pollution, not active harm. The learner
has no staleness-detection machinery (confirmed), and K5 is reported FAIL
for a prereg derivation error disclosed below (the mechanism finding is not
affected).

## Results

Format: ANS / TRIES / WIDEN / WTRIG / INTER ; WBACK in parentheses for P.

| Query | P observed (predicted) | N observed (predicted) |
|-------|------------------------|------------------------|
| Q1 | 2/6/1/2/44 (0) (2/6/1/2/44 (0)) | 2/6/1/2/44 (2/6/1/2/44) |
| Q2 | 2/3/1/3/44 (0) (2/3/1/3/44 (0)) | 2/6/1/2/44 (2/6/1/2/44) |
| Q3P | 2/7/0/0/44 (0) (2/7/0/0/44 (0)) | 2/7/0/0/44 (2/7/0/0/44) |

Every cell matches its frozen prediction exactly.

## Kill bar results

- K1 SEED FIDELITY: PASS. P-Q1 block byte-identical to the compose_ledger
  lane Q1 block; N-Q1 identical modulo the ARM label. P-Q2 =
  2/3/1/3/44 (0) with WTRIG=3 and WADD=2,0 / 2,1 / 2,3 in scan order;
  N-Q2 = 2/6/1/2/44 with WTRIG=2. 3/3.
- K2 TRANSFER REPRO: PASS. P-Q2 strictly fewer tries than N-Q2 (3 < 6);
  ANS=2 in both. The bit was genuinely true and helpful before
  invalidation. 3/3.
- K3 INVALIDATION INERT: PASS. P-Q3P = 2/7/0/0/44 (0), N-Q3P =
  2/7/0/0/44; zero WADD lines in both Q3P blocks; WTRIG=0 in both; the
  ARM, INTER, and CENSUS lines of the Q3P blocks are byte-identical modulo
  the ARM label. Poison cost exactly 0 tries: the re-teach costs +4 tries
  versus P-Q2 (the answer path moves from primed pairs to admitted pairs),
  but P and N pay it equally, so the ledger confers no advantage and no
  penalty. Drafting note (disclosed, not a weakening): the bar's
  "byte-identical modulo the ARM label" clause cannot literally cover the
  LEDGER lines, which differ by the experimental design itself (P carries
  m2 out=1 per U3, N's fresh ledger reads 0 per lg_clear); every
  quantitative clause holds exactly. 3/3.
- K4 STALE BIT PERSISTS: PASS. P LEDGER block after Q3P byte-identical to
  P LEDGER after Q2 (m2 out=1, all else 0; verified by cmp); N LEDGER all
  zero after Q3P. Q3P recorded nothing. The false bit is never corrected:
  the only ledger write in the frozen code is the idempotent lg_add, and
  U3 forbids clearing. 3/3.
- K5 NO DETECTION: FAIL (prereg derivation error, diagnosed below; the
  substantive no-detection finding stands). The bar's signal clause
  ("the Q3P block shows the m2 single trial with INTER=44") is false:
  h_try_single never logs INTER in the frozen trace format (only
  h_try_pair logs INTER lines; this was already visible in the ledger
  lane's Q1, where the bit-recording m2 single likewise logged no INTER),
  so the invalidation signature is not directly trace-visible and the
  conjunctive bar cannot pass as written. The machinery-absent half holds
  exactly: post-Q3P LEDGER byte-identical to post-Q2 LEDGER (verified by
  cmp), no staleness flag, no clearing, no action taken. Substantive
  finding: under frozen U1-U5 the learner cannot detect the staleness; the
  composer takes no action on it. A weaker signal IS trace-visible (the
  admitted-pair trials (2,0)/(2,1) log INTER=44, X emitting NODE at out
  with no new miss recorded and no WADD), and it is likewise unacted upon.
  This bar is reported FAIL as written; it is not amended or weakened.
- K6 DETERMINISM: PASS. 3/3 byte-identical whole-output per arm.
  Run digests: P 4d9f92d77e53eae16b494aa056ab990a41010d771c77ff4b21f211183ff68391,
  N b8dfd655c43a6999ec2e8782a903efa90db8ca9feafb7e542170a8ce0c061f8b.
  Binary digests: P 47967cc61f25eef62f257aabaf2739b664c78e86d6a1ca8ab333d69f56e4e7d1,
  N ec61d454b33c566ae9530bad86aa6ab13182011e4f6885f76482ab90cf812d1e.
  Source digests: i_full_P.zag 61117a68e6782f6fdfddbec59ac92a7eee764d92999842330474d59c0867e415,
  i_full_N.zag a23a7e2101a0e45c554097dfdacaab96affd892253b604ca4c2ec4735e60d0f7.
- K7 HYGIENE: PASS. Zero em/en dash bytes in all docs (byte-verified);
  safebin guard attested in NAMECHECK.md Step 0 (which python3/python/znc
  return NOTHING); pure Zag for all scientific computation; pinned znc
  src/tools/toolchain/znc_linux_x86_64_abed8aa1; compose_ledger lane
  untouched (verified via git status: no output for that path); all new
  files under compose_inval/; no mode/policy identifier in the composer
  (grep over non-comment lines: zero hits).

## Why this matters

The open question after C341 was whether the unbounded-lifetime ledger
adapts or poisons when the world changes under it. The answer, for the
contract-growth flavor of invalidation, is neither: the false bit is
structurally inert. The mechanism is exact, not approximate. U4 priming
requires a pair to be BOTH filter-rejected AND justified by a carried bit;
justification by (m2,out,1) needs kind 1 in the partner's inmask, while the
re-teach that falsified the bit put kind 1 in X's outmask, so the junction
gate passes and the pair is filter-admitted, hence excluded from priming.
The same mask growth that falsifies the bit opens the admission junction:
contract-growth invalidation is self-shielding under U4, by construction of
the frozen rules, and the experiment verifies the derivation exactly (zero
primed pairs, WTRIG=0, P=N on Q3P).

The bit nevertheless persists verbatim forever: there is no lg_del, no
decay, no re-validation, and U3 forbids clearing. The ledger neither adapts
(corrects) nor poisons (misleads); it pollutes latently. And the learner
cannot detect the staleness: the frozen composer has no detection
machinery, confirmed by the unchanged ledger and the absence of any
staleness event (K5's substantive half).

## Architecture accounting

- Cognition lines added: ~17 (setup_d5x) + ~8 (main deltas in i_pers.zag
  / i_ctrl.zag); composer functions byte-copied from the ledger lane (0
  new logic lines; the U1-U5 rules, S2 pin, and R1/R2 are frozen, not
  re-litigated).
- New hardcoded semantic cases: 0. Modes/bridges/handlers: 0.
- Researcher-owned: D5X re-teaching, the Q1/Q2/Q3P sequence, the frozen
  U3/U4 rules under test.
- Learner-owned: kind-set contracts, the carried missbits ledger
  (including the false bit), per-query tried/admitted sets.

## Honest limitations

- One re-teach flavor: contract GROWTH falsifying the bit at the
  justifying position. The Section 3d shielding argument does not apply to
  behavior-change invalidation (contract unchanged, emission facts
  changed), where priming would fire on the false bit; that flavor is the
  open follow-up, not claimed here.
- K5's signal operationalization was misderived (disclosed above); the bar
  is reported FAIL as written, not amended.
- Three queries on one world family discriminate the mechanism; they do
  not establish generality of invalidation behavior.
- Expected-answer verification still used (canonical boundary).

## Follow-ups (not claimed)

1. Behavior-change invalidation: change emission facts so X stops emitting
  NODE while its contract stays {2}; the carried bit becomes false with
  the admission structure unchanged, so priming SHOULD fire on it at the
  primed-set try cost with no correction. That is the true "poison" flavor
  and the direct test of whether unbounded lifetime needs an invalidation
  rule.
2. The symmetric "vice versa" case from the task: a bit becoming true
  (a newly observed miss kind after re-teaching).
3. Whether a learner-observable staleness signal (a carried bit whose
  justifying observation repeatedly fails to re-occur on direct trial)
  can ground a principled invalidation rule without researcher magic
  numbers; the current result says the signal exists in-trace (pair
  trials) but no machinery consumes it.

## Toolchain attestation

Zero invocations of python3, python, or any other forbidden executable.
Safebin PATH throughout; pinned znc by absolute path; no incidents to
disclose.
