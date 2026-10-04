# REPORT: Persistent Cross-Query Missbits Ledger -- Verdict PERSISTENT LEDGER HELPS (BOUNDED)

Date: 2026-10-02. Worker: compose-ledger (persistent missbits follow-up to
HYBRID MATCHES BEST).
Battery: 3 queries (Q1 seed, Q2 transfer, Q3 staleness) on the frozen D5
world, 2 arms (P persistent ledger, N no-persistence control), pure Zag,
pinned znc. Prereg committed alone before implementation (eb3699e43).

## Verdict: PERSISTENT LEDGER HELPS (BOUNDED)

All kill bars K1-K7 pass exactly as frozen, 3/3 byte-identical per arm. The
carried missbits make Q2 faster (6 tries to 3) via ledger-primed selective
admission; the staleness cost on Q3 is exactly +3 tries with no correctness
loss; the ledger accumulates honestly and never corrupts.

## Results

Format: ANS / TRIES / WIDEN / WTRIG / INTER ; WBACK in parentheses for P.

| Query | P observed (predicted) | N observed (predicted) |
|-------|------------------------|------------------------|
| Q1 | 2/6/1/2/44 (0) (2/6/1/2/44 (0)) | 2/6/1/2/44 (2/6/1/2/44) |
| Q2 | 2/3/1/3/44 (0) (2/3/1/3/44 (0)) | 2/6/1/2/44 (2/6/1/2/44) |
| Q3 | 2/4/1/3/-1 (0) (2/4/1/3/-1 (0)) | 2/1/0/0/-1 (2/1/0/0/-1) |

Every cell matches its frozen prediction exactly, including WTRIG=3 on the
primed queries and WBACK=0 everywhere.

## Kill bar results

- K1 SEED FIDELITY: PASS. P-Q1 and N-Q1 are byte-identical to each other
  and to the frozen D5 H block from the hybrid lane (verified by diff modulo
  the ARM P/N-vs-H and PROB Q1-vs-D5 labels), including CENSUS, LEDGER,
  INTER, and WADD lines. The persistent arm starts exactly as the frozen
  hybrid; priming admits nothing on Q1 (ledger empty at init, U1).
- K2 PERSISTENCE HELPS: PASS. P on Q2 = 2/3/1/3/44 (0); N on Q2 =
  2/6/1/2/44. P is strictly faster (3 < 6 tries); ANS=2 in both. The
  carried bit (m2,out,1) from Q1 junction-justified (2,0),(2,1),(2,3) under
  the frozen predicate, so priming tried them first: (2,0) and (2,1) failed
  re-observing the known bit (no new miss, no R1), (2,3) succeeded at try 3.
  The control re-observed the miss on try 3 and paid the full R1 sequence.
- K3 STALENESS BOUNDED: PASS. P on Q3 = 2/4/1/3/-1 (0); N on Q3 =
  2/1/0/0/-1. Harm is exactly +3 tries (the primed-set size), ANS=2 in both;
  no wrong answer, no runaway. The old bit (m2,out,1) is TRUE (X did emit
  NODE at out in this world); it misleads only because Q3's answer is the
  admitted single A(70)=2. This is query-shift cost, not bit-rot, which is
  why the unbounded-lifetime choice (Section 3b) survives: the bound held
  exactly.
- K4 LEDGER ACCUMULATION: PASS. P ledger: after Q1 m2 out=1, all else 0;
  after Q2 identical (Q2's misses re-observed the known bit; success
  recording touches contracts, not the ledger); after Q3 identical (Q3
  recorded nothing, v1=-2). N ledger: m2 out=1 after Q1 and Q2 (each
  query's own miss), all zero after Q3 and at every fresh start. Exact.
- K5 PRIMING EVENTS: PASS. On Q2 and Q3, P logs WIDEN=1, WTRIG=3, then
  exactly WADD=2,0 / WADD=2,1 / WADD=2,3 in scan order, before any INTER
  line. On Q1, P logs no WADD and WTRIG=2. 3/3.
- K6 DETERMINISM: PASS. 3/3 byte-identical whole-output per arm.
  Run digests: P 9c0dc92b61fcb9d4866c748b587f3d504406ce0c530c27333e748c1475259359,
  N b23d16fcfb66f21acd55ca4474ed60c42ddfbe516315ac8d6ed34ff8b9425188.
  Binary digests: P 341f329704c7a5385edc99d8e519b1246f085b202fe37deff73b4522975a4267,
  N ba5ff65d2f2588a73fd394d0d481602cd643a4c59e1c085bedceece22edd5df0.
  Source digests: l_full_P.zag 67a27b10d8e14deb8786c67ac04b7103d26ff1f7b8ecc66acf3ab5c7c6846df2,
  l_full_N.zag 3b2ed54ed205c1d542cfc13e290e5be943910dc1ebfb39db257eeabf6317d248.
- K7 HYGIENE: PASS. Zero em/en dash bytes in all docs (byte-verified);
  safebin guard attested in NAMECHECK.md Step 0 (which python3/python return
  NOTHING); pure Zag for all scientific computation; pinned znc
  src/tools/toolchain/znc_linux_x86_64_abed8aa1; compose_hybrid lane
  untouched (verified via git status: no output for that path); all new
  files under compose_ledger/; no mode/policy/arm identifier in the
  composer (grep over non-comment lines: zero hits).

## Why this matters

The hybrid's missbits were per-query: coverage knowledge evaporated after
each query and only success-recording persisted. This battery shows the
ledger can persist as learner-owned long-term knowledge with a net win: on
the transfer query the learner consults carried coverage evidence FIRST
(priming, WTRIG=3) instead of re-deriving it through failure, halving the
try count (6 to 3). The mechanism is honest: bits only ever record true
learner-observed facts (idempotent lg_add), priming reuses the frozen R1
justification predicate (no new admission logic), and the staleness price is
exactly the primed-set size, measured not assumed.

The Q3 result is the load-bearing bound for the unbounded-lifetime choice:
old bits can prime wrong pairs, but the cost was exactly +3 tries with no
correctness loss, and the bits themselves stayed true. Decay or eviction
would need a researcher-chosen constant with no learner-observable basis;
the experiment gives no reason to pay that complexity.

## Architecture accounting

- Cognition lines added: ~360 (l_base.zag: h_base copy + 16-line
  ledger_copy/ledger_restore) + ~300 (l_pers.zag: frozen hybrid composer
  copy + p_justified/p_prime_scan/p_prime_trial/p_solve/persistent main)
  + ~210 (l_ctrl.zag: frozen hybrid composer copy + n_solve/control main).
- New hardcoded semantic cases: 0. Modes/bridges/handlers: 0.
- Researcher-owned: behavior implementations, world facts/teaching, the
  priming rule U4 and lifetime rule U3 (the variables under test), the
  three frozen queries.
- Learner-owned: kind-set contracts, the carried missbits ledger, primed /
  admitted / tried sets per query, grown contracts on success.

## Honest limitations

- Three queries on one stable world discriminate the ledger mechanism; they
  do not establish generality of persistent coverage knowledge.
- The MAP table is stable across queries here; bit truth under contract
  re-teaching (world change that alters MAP behavior) is untested.
- Priming fires before the admitted sequence by design (U4); a policy that
  weighs primed pairs against admitted singles is untested.
- Expected-answer verification still used (canonical boundary).
- Toolchain self-disclosure: during K1 verification the worker typed
  `python3 -c` inside a shell one-liner; the name did not resolve in the
  safebin PATH (command not found, exit 127), so no forbidden executable
  ran and no scientific computation is involved. Disclosed here and in
  NAMECHECK.md; no wave result depends on it.

## Follow-ups (not claimed)

1. Contract re-teaching mid-lifetime: do carried bits go stale when a MAP's
   behavior genuinely changes, and what invalidation rule (if any) the
   learner can derive from its own observations.
2. Ledger-guided admission under query-shift at scale: does the primed-set
   bound hold over dozens of queries with mixed query shapes.
3. Whether priming should precede or interleave with admitted singles when
   both are available (U4's ordering is a frozen choice here, not a result).
