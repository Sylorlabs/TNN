# REPORT: Delayed Consequence Red Team (DCRT)

Worker: Delayed Consequence red team worker (subagent, 2026-10-02).
Target: ledger C306 DELAYED-CONSEQUENCE-PASS (prereg c0cff4c48,
implementation f58603a33).
Prereg: `delayed_consequence_redteam/PREREG.md`, frozen at commit
7c1629e97 (PREREG.md + NAMECHECK.md only; no attack code existed).
Implementation: `src/redteam.zag` (559 lines), built with the pinned
znc to `bin/redteam` (unguarded, GUARD=0) and `bin/redteam_guarded`
(GUARD=1, one-const sed derivation, diff-verified).

## Verdicts per attack (frozen bars from PREREG section 6)

A1 CONFOUNDED KILL: ATTACK-FAILED. P3 killed F3 and F5
simultaneously; only F3 is load-bearing for the committed B. The
learner attributed to the single correct cause (attr_c=1,
attr_f=3), demoted relB 120->60, retired B, and credited
observed_kills[F3]=1. The decoy F5 death never entered the
attribution path because P4 re-licenses only the recorded
composite's licenses. In-program bar a1_succeeds=0.

A2 DECOY VOLATILITY: ATTACK-FAILED. The volatility prior pointed at
the wrong candidate (sound A carried F1 with vol 3, which stayed
live; flawed B's F3 had vol 0 but died). The consequence dominated
the prior: the learner revised against the actually-dead fact
(attr_c=1, attr_f=3, observed_kills[F3]=1, observed_kills[F1]=0).
The stale volatility signal is recorded at commit but never
consulted in the P4 attribution path, so it could not hijack
attribution. In-program bar a2_succeeds=0.

A3 RECORD CORRUPTION: ATTACK-SUCCEEDED (on the sanity sub-bar).
The driver flipped one bit in the record id field (1->0) mid-P2,
inside the disclosed accidental-corruption threat model.
Integrity sub-bar: the driver seal caught it (seal_ok=0 at the P2,
kill, and P4 checkpoints; a3_seal_caught=1), so ATTACK-FAILS on the
integrity claim, as the C306 disclosure predicted. Sanity sub-bar:
the learner SILENTLY REVISED on the corrupted record. It
re-executed corrupted id 0 (A)->60 against the recorded pred 50,
found d=10, re-licensed A's (all alive) licenses, and therefore
demoted the SOUND composite (relA 110->50), retired A (act0=0),
set attr (0,-1), left the actually-broken B at 120 active, and the
follow-up picked B and failed (-1). No halt, no quarantine, no
checksum verification: the learner's own LS_RCK checksum exists but
is never checked in P4, and the driver takes no action on
seal_ok=0. In-program bar a3_sanity_succeeds=1. This is the one
genuine break found by this red team.

A4 TARGETED INTERFERENCE: ATTACK-FAILED. P2 built the lookalike L=5
({F1,F2}->50: same prediction value as B's recorded 50, different
provenance, rel boosted to 140 over 6 episodes). The ID-bound
record resisted it: P4 re-executed the recorded B by id, found F3
dead, attributed (1,3), demoted relB 120->60, retired B. A
value-directed attributor would have been confused; this learner is
id-directed, so the lookalike could not hijack attribution.
In-program bar a4_succeeds=0.

## Guard proposal and test (preregistered, PREREG section 5)

Minimal learner-side guard: at the entry of P4, recompute the
learner checksum ck = rid*31+pred*7+r_at*13+maxvol*17+epoch*29 from
the record fields and compare to the stored LS_RCK. On mismatch,
quarantine (attr_composite=-2, attr_cause=-2) and return WITHOUT
any revision (no reliability change, no retire, no observed_kill
increment). Implemented as learner_phase4_record_checked (16
lines); it uses only learner-visible state, never the driver-held
seal constant. The guarded binary differs from the unguarded by
exactly one const (GUARD 0->1), verified by diff.

G1 (attack now fails): guarded A3 quarantines cleanly: attr
(-2,-2), relA=110 and relB=120 unchanged, both active bits still 1,
every observed_kill counter 0. In-program g1=1;
a3_sanity_succeeds=0. The silent revision is gone.

G2 (no overreach): guarded D1/D2/D4 reproduce C306 exactly: D1
relA 120->130 with no attribution; D2 attr (1,3), relB 120->60,
follow-up A with output 60; D4 attr (1,3), relB 140->80, follow-up
A with output 60. In-program g2=1. The guard changes behavior ONLY
when the record checksum mismatches, which never happens without
corruption; all uncorrupted arms are byte-identical between the two
binaries except the A3 P4 line and the BARS line (verified by
diff).

Guard verdict: GUARD-EFFECTIVE (G1 and G2 both hold).

## Per-arm traces (unguarded, runs/run1.txt)

A1: commit B pred 50; P3 kills F3+F5; P4 attr (1,3), relB 60, B
retired, obs3=1; follow-up A, out 60.
A2: commit B pred 90 (A2 world); P3 kills F3; P4 attr (1,3), relB
60, B retired, obs3=1, obs1=0; follow-up A, out 60.
A3: commit B pred 50; CORRUPT mid-P2; seal_ok=0 from P2 on; P4
relA 50, relB 120, attr (0,-1), A retired; follow-up B, out -1.
A4: commit B pred 50; P2 builds lookalike L (rel 140); P3 kills F3;
P4 attr (1,3), relB 60, B retired; follow-up A, out 60.
D1/D2/D4 controls reproduce the C306 frozen expectations exactly
(D1 relA 130; D2 attr (1,3) relB 60; D4 attr (1,3) relB 80).

## Key numbers

- sha256 unguarded (3/3 byte identical):
  dad46c95d8213b7d3f3d3a65fd0202dfdcea41b85f98ad1a08c17807bd4f06c4
- sha256 guarded (3/3 byte identical):
  8c9f0badc34d12e46807ec034b456395e0eb89bf78f3765e12bdb269259a9d18
- In-program bars (unguarded): a1_succeeds=0 a2_succeeds=0
  a3_seal_caught=1 a3_sanity_succeeds=1 a4_succeeds=0 g1=0 g2=1.
- In-program bars (guarded): a1_succeeds=0 a2_succeeds=0
  a3_seal_caught=1 a3_sanity_succeeds=0 a4_succeeds=0 g1=1 g2=1.
- Cognition lines added: 559 (new .zag file; 0 lines changed
  elsewhere). Guard delta: 16 lines (learner_phase4_record_checked)
  plus 1 const and 1 driver dispatch line, all inside the 559.

## Audits

- Learner functions never reference the attack selector (0 hits):
  the attack designs do not leak into the learner path.
- Researcher-expected-value audit over learner functions for
  EXPECT, CORRECT_ID, RIGHT_ANSWER, TARGET_ID, ANSWER_KEY: 0 hits.
- Architecture audit for mode/bridge/handler/opcode tokens: 0 hits.
  Standalone file; TNN core untouched.
- Compiler lessons: no `as *i32` slice construction in functions,
  no _zag_print for dynamic output (single raw-syscall flush,
  stdout bytes verified), no `!(.. && ..)` in while conditions
  (grep clean), if-nesting at most 3 in new bar code.

## Disclosures

1. The A3 corruption is a single-bit flip of the record id byte
   (1->0) applied by the driver after P2 episode 2. This is squarely
   inside the C306 disclosed threat model (accidental corruption of
   the record region by interference), not an adversarial-learner
   attack.
2. The guarded binary is a one-const sed derivation of the
   unguarded source; diff confirms the only change is
   `const GUARD:i32=0;` to `const GUARD:i32=1;`.
3. In guarded A3 the follow-up still selects B (120>110) and
   executes to FAIL (-1). This is correct: the world is genuinely
   broken and the learner honestly refuses to revise on corrupted
   data instead of silently condemning the wrong composite.
4. znc emitted only the zagd-unavailable notice; no lint warnings.
   Both binaries ran 3/3 byte identical.

## Interpretation

Three of the four vectors do not break the C306 machinery: the
record-scoped re-licensing correctly ignores a confounded decoy
death (A1), the evidence-driven attribution is immune to a
misleading volatility prior it never consults (A2), and the
id-bound commitment resists value lookalikes (A4). The real break
is A3: the tamper-evident record is evident only to the driver.
The seal catches corruption, but nothing acts on the catch: the
learner never verifies its own checksum and revises silently on
corrupted data, in this case demoting and retiring the sound
composite while the broken one stays preferred. The minimal fix is
learner-side checksum verification with quarantine on mismatch
(16 lines); it closes A3 with zero behavior change on every
uncorrupted arm, including the full C306 D1/D2/D4 battery.

Commits: redteam prereg 7c1629e97; implementation f58e3eabd.
Local only, never pushed.
