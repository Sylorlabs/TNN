# REPORT: GEN-STRESS -- The True Generality Boundary of GEN

Date: 2026-10-03. Agent: gen-stress. Lane:
docs/lab/research-lead/overnight-20260928/gen_stress/.
Branch: lane-genstress-20261003 (dedicated; explicit-pathspec commits only).

## Verdict: BOUNDARY-FOUND (ARENA-4MAP)

The headline finding: **the frozen GEN artifact cannot address 5 or more
structures at all.** Its scratch arena is hard-dimensioned for 4 MAPs
across four overlapping regions. At nm=5..7 the compositional rules are
never faithfully executed: MAP tables alias GEN's counters, tried-sets
alias the pool count and widened flag, and the mechanism produces
deterministic but wrong declines and spurious WIDENs. At nm=8 the arena
overflows and the binary panics. The C402 4-structure envelope sat
exactly at the implementation's addressable limit; the 5/10+ structure
question Micah posed terminates one level below the value-graph logic,
at the scratch layout.

This is INFORMATIVE-FAIL in the precise sense the task brief asked for:
a real, exactly-mapped limit, with the mechanism-level cause named and
empirically confirmed. GEN was NOT modified; the boundary was
characterized.

Two sub-boundaries were mapped independently on clean regions (nm<=4),
where the frozen rules execute faithfully:

- BOUNDARY-FOUND (WIDEN): GEN's decline-soundness holds only while
  kind admission is active. After one quiet round suspends admission, a
  near-miss contract yields a contract-violating success (S3: WIDEN=1,
  ANS=207 via m1(205,2) against m1's learned in1{1} in2{1} contract).
- BOUNDARY-FOUND (POOL): under real load the 64-value pool cap drops
  overflow silently (no error, no decline) and the 64-entry tried2 cap
  causes unbounded retry inflation (S5 R6 alone burns 2145 tries
  re-attempting unrecorded pairs); the query still declines honestly
  (S5: ANS=-2, TRIES=2734, no WIDEN).

## Kill bars

- K1 UNMODIFIED-MECHANISM: PASS. (a) ref_gs_base.zag sha256
  a53cdf0126ab1501fb70d9b14c2f745e0ef1838209753df8a0c6d0daf484bbcb
  matches d6_base.zag at 82732a9e8. (b) ref_gs_gen.zag sha256
  d6f1f9d8f4747293bb7a8e99474660347dc24693f62f3d25caaf1d83c19c9d9a
  matches d6_gen.zag at 82732a9e8. (c) gs_full.zag region diffs EMPTY
  (base whole; gen minus main; new driver). (d) grep audit: gs_new.zag
  defines only setup_s1..setup_s5 + main; uses only pre-existing classes
  0/1/3/4; zero relation-conditional branches outside setups.
- K2 SCALE-5 (S1): FAIL. Predicted ANS=2 TRIES=29 (no WIDEN). Isolated
  actual: ANS=-2 TRIES=16, no WIDEN, 3/3 byte-identical. Cause: arena
  aliasing at nm=6 (see mechanism section). The valid 5-chain path was
  never executed; the decline is wrong, not honest.
- K3 SCALE-6-DAG (S2): FAIL. Predicted ANS=219 TRIES=48 (no WIDEN).
  Isolated actual: ANS=-2 TRIES=62 WITH a spurious WIDEN=1, 3/3
  byte-identical. Cause: arena aliasing at nm=6. The 219 value path was
  never executed; the decline is wrong and the WIDEN is spurious.
- K4 NEAR-MISS (S3): PASS. Output EXACTLY the preregistered block:
  WIDEN=1, ANS=207, TRIES=8, 3/3 byte-identical. The predicted
  contract-violating success is confirmed: exp=207 is unreachable under
  admission (both 207-yielding pairs kind-rejected), R2 is quiet, WIDEN
  fires, and m1(205,2)=207 is then admitted and ends the query. Per the
  frozen Section 3 definitions this is a WRONG ANSWER in the contract
  sense: m1's learned contract is in1{1} in2{1} and slot 2 received a
  NUM. GEN does not fail cleanly on near-miss contracts once widening
  fires.
- K5 ROUND-CAP (S4): FAIL. Predicted clean decline ANS=-2 TRIES=48.
  Actual: `panic: slice index out of bounds`, exit 1, zero stdout bytes,
  3/3 identical. The round-cap question could not be asked: m7's tried1
  read at arena offset 4096 overflows the 4096-byte world.
- K6 POOL-CAP (S5): PASS. ARM line EXACTLY
  `ARM=GEN PROB=S5 ANS=-2 TRIES=2734`; exactly 3 INTER= lines, exactly
  2731 INTER2= lines, zero WIDEN=1 lines; 3/3 byte-identical. Both caps
  behaved exactly as read from the frozen source: the pool stopped at
  64 values with silent drops, and tried2's 64-entry cap forced
  465 + 2145 retried pairs in R5/R6. Honest decline under load; wasted
  work, not unsoundness.
- K7 DETERMINISM: PASS. Official combined runs: 3/3 byte-identical
  (empty stdout, identical panic stderr). Each isolated diagnostic:
  3/3 byte-identical, including the corrupted S1/S2 outputs and the S4
  panic. The corruption is deterministic aliasing, not nondeterminism.
- K8 OPAQUE-NAMING: PASS. Grep audit over gs_new.zag, PREREG.md,
  REPORT.md: zero banned-vocabulary tokens. All structures m0..m7,
  relations and entities bare integers. (Matches are only the document
  bylines "Worker:" = agent role, as in the C402 precedent.)

## The mechanism-level cause (read from the frozen source)

The frozen arena layout hard-codes 4 MAPs in four places:

1. MAP table: `mg(A,m,f)` = 776+m*40+f*4. m0..m3 occupy 776..936.
   m4's table (936..976) aliases GEN's counters: 936 = TRIES,
   940 = success flag, 944 = ANS. Every TRIES increment rewrites m4's
   class field; gen_solve's init rewrites m4's class/rel/r2.
2. Second-input contract table: `m2g(A,m,f)` = 968+m*12+f*4, 4 maps
   (968..1016). Overlaps m4's table (936..976) and m5's (976..1016).
3. tried1: 2304+(m*64+i)*4, 4 maps x 64 x 4 bytes (2304..3328).
   m4's tried1 (3328..3584) aliases tried2 count (3328) and entries;
   m5's (3584..3840) aliases tried2 entry63 (3584), the pool count nv
   (3588), the widened flag (3592), and the visit stack; m6's
   (3840..4096) aliases visit tail and done set; m7's (4096..) overflows
   the 4096-byte arena.
4. m4+'s m2g entries (1016+) overlap the value pool (1024+).

Consequences by MAP count (all empirically confirmed):
- nm<=4: every region is clean. S3 (nm=3) and S5 (nm=4) matched their
  frozen predictions byte-for-byte.
- nm=5..7: silent cross-region aliasing. S1/S2 (nm=6) produced
  deterministic wrong declines (ANS=-2 on reachable targets) and, in
  S2's case, a spurious WIDEN=1; S1's TRIES collapsed from the
  predicted 29 to 16 because the corrupted pool count hid values.
- nm>=8: arena-overflow panic on the first out-of-range tried1 access.

The compositional rules (admission, rounds, widening, pool dedup) were
never the limiting factor at 5+ structures: the implementation cannot
represent the trial state for a fifth MAP. Any GEN successor must
re-dimension the scratch arena as a general fix before 5/10+
structure composition can even be tested.

## What was built

- ref_gs_base.zag, ref_gs_gen.zag: byte-copies of the C402-verified
  frozen sources (digests above).
- gs_new.zag: five setups (setup_s1..setup_s5) + main running
  S1..S5 on fresh worlds, single o_flush at end. No mechanism code.
- gs_full.zag: assembly (627 lines); gs_bin built with the pinned safebin
  znc (sha256 498abcb5...35a4; compile exit 0; 3 analyzer warnings, all
  pre-existing notes in the frozen GEN code: gen_addval, gen_app1,
  gen_app2).
- gs_run1/2/3.txt: official 3/3 runs (empty: the S4 panic discarded the
  shared output buffer before the single end-of-main flush).
  gs_run1/2/3.err: `panic: slice index out of bounds`, 3/3 identical.
- diag/: per-query isolation drivers. diag/setup_sN.zag are byte-exact
  extracts of the frozen setups (awk range extraction from gs_new.zag);
  diag/main_sN.zag are fresh single-query mains (diagnostic scaffolding,
  not battery code); diag/diag_full_sN.zag assemblies; diag/diag_bin_sN
  binaries; diag/diag_run_sN.txt + _b/_c (3/3 byte-identical each) and
  .err files. These exist to attribute the official panic precisely;
  the battery verdict rests on the official runs plus these
  attributions.

## Architecture accounting

- Cognition lines added: 0 (mechanism frozen). New lines: 87 (setups +
  driver), 619 (prereg), ~45 (5 diagnostic mains), this report.
- New hardcoded semantic cases: 0. Modes/bridges/handlers: 0.
- New behavior classes/opcodes: 0 (only the C380-authorized generic
  2-input ADD2 class, reused unchanged).
- Researcher-owned: world facts, MAP inventories, teaching schedules,
  driver, expected answers, diagnostic scaffolding (canonical
  verification boundary).
- Learner-owned (GEN's): value pool, observed kinds, provenance,
  tried-sets, grown contracts via success-recording. (S3's
  post-success observe2 call also grew m1's contract, exactly as the
  frozen success-recording rule specifies.)

## Why this matters

1. The 5/10+ structure scale question is answered structurally, not
   compositionally. Micah's overnight priority asked for 3/5/10+
   structure combinations; the frozen GEN cannot represent trial state
   for a fifth MAP, so no 5+ composition claim can be tested on this
   artifact, let alone made. The re-dimensioning of the scratch arena
   is a prerequisite general fix, and it must be done without
   reintroducing per-shape special cases.
2. Silent corruption is the dangerous regime, not the panic. nm=5..7
   does not crash: it yields deterministic wrong declines and spurious
   WIDENs that a casual reader could mistake for compositional
   results. Any future worker touching GEN-adjacent code must know the
   4-MAP precondition, because violating it fails silently.
3. The WIDEN boundary is now precise and independent of the arena
   issue (S3 ran on a clean nm=3 region). GEN's honesty guarantee,
   decline rather than a wrong answer, ends exactly where the
   admission-off phase begins. A near-miss contract plus one quiet
   round is sufficient to convert an unsatisfiable-under-contract
   query into a contract-violating success. If decline-soundness is
   ever claimed for GEN, the claim must be scoped to pre-WIDEN, or
   the widening rule itself must change (a mechanism change, out of
   scope for this battery).
4. The resource caps are characterized, not just hypothesized. The
   64-pool silent drop and the 64-tried2 retry inflation are now
   measured behaviors (S5: 2145 of 2734 tries burned on retries in R6),
   and the query still declined honestly. Sublinear indexing work
   (Micah's priority 7) will need to replace the tried2 linear table
   before 10k-scale composition is plausible; this battery quantifies
   the cost of not doing so.

## Honest boundaries (carried from the prereg, plus one learned)

- Behaviors pre-installed as learned MAPs; expected-answer verification
  (canonical).
- GEN is researcher-implemented (C380 boundary B3 holds).
- Exactly one generic 2-input class (ADD2), reused unchanged.
- S5's INTER2 listing was not hand-enumerated (preregistered); the bar
  was the exact TRIES count plus 3/3 determinism, both met.
- NEW (learned this battery): the frozen artifact's addressable MAP
  count is 4, not "as many as the compositional rules allow." The S1,
  S2, S4 predictions assumed the rules scale past the arena; the
  artifact does not. Future stress batteries must assert nm<=4 in the
  prereg or preregister the arena-overlap characterization explicitly.

## Toolchain attestation

Zero invocations of python3, python, or any other forbidden executable.
Safebin PATH throughout; `which python3` / `which python` return NOTHING
(NAMECHECK.md Step 0). Pure Zag for all scientific computation, including
the diagnostic derivations (which were confirmed empirically, not
analytically). Git via /usr/bin/git directly (safebin git symlink EPERM
defect, per AGENTS.md); explicit pathspecs; no git reset; dedicated
lane branch. Prereg committed alone (e27d10fcd) before implementation.

## Files

All in gen_stress/: PREREG.md (frozen), NAMECHECK.md, REPORT.md (this
file), ref_gs_base.zag, ref_gs_gen.zag (frozen references),
gs_new.zag (only new battery code), gs_full.zag (assembly), gs_bin
(pinned znc build), gs_compile.txt, gs_run1/2/3.txt + .err (official
3/3: panic, empty stdout), diag/ (isolation drivers, binaries,
per-query 3/3 runs and errs).
