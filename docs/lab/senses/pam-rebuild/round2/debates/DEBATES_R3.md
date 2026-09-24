# DEBATES R3 — PAMs Round-2 debate, round 3

**Date:** 2026-09-24. **Crew:** PAMs Round-2 debate crew (round 3), self-contained.
**Branch:** `tnn-native-lab` (sylorlabs/TNN). **Method:** three native champion
positions (defense-first, offense-first, front-end-first), each arguing from
committed evidence and each steelmanning the strongest attack on itself;
external opinions attempted via UnoRouter; native judge's ruling.
Like the A–E debate crews, this crew is depth-2 and ran as structured
proposition rounds in writing — no strawmen.

## 0. Evidence base (frozen, copied from verdicts — the complete record for this round)

1. F5 counter-corroboration trap: SURVIVED backtest — 8/9 false accepts
   blocked, 0/34 true accepts over-blocked (`v2/f5_backtest/VERDICT_F5.md`).
   Its 300-near-exemplar-correct-percept red-team was NOT run (needs fresh
   fixtures; parallel crew in flight — do not propose). Its confirmation
   machinery ("three deliberate re-inspections from three temporal crops")
   was NOT exercised — the battery covered the pre-confirmation block
   predicate only.
2. G2 judgment-blind deliberate re-sense KILLED; G5 second-pass sense KILLED.
   Wall = byte-side correlation: a second organ reading the same spoofed
   bytes re-reads the same lie.
3. Contradiction matrix 30/30 PASS, but cell CC1 preregistered known-unsafe:
   two WRONG high-conf corroborators agreeing within tolerance trigger
   REVISED_INSTALL — false permanent install under both corroboration gates
   (G1, G2). A margin guard must be verified before anything ships; a
   parallel crew verifies it — do not propose.
4. Hardening: H6 won (no-provisional: withhold until a corroborated second
   observation within tolerance): 0 false installs on the clean stream
   (`v2/hardening/HARDENING_VERDICT.md`). All remaining failures are
   sustained, attested, mutually-corroborating confident cross-span error —
   FRONT-END, not gate. Gate work has diminishing returns.
5. Sense is 53% accurate on the 12 sealed novel adversarial families; only
   44/288 trials reach its own install bar.
6. Proven ceilings: (1) judgment-side channels 0.0000 bits (deterministic
   transform of a judgment carries no information; mini Zag proof).
   (2) Pointwise adjudication impossible — trial 1145 was WRONG yet conf=874,
   margin=10410, strong=1, agree=1, strictly dominating its correct incumbent
   (605/2300) on every logged axis. (3) Gate-side arithmetic ceiling on RK-3:
   824/1102 = 74.8%; 278 correct high-conf percepts never reach PASS at the
   sense level. (4) Zero RNG, pure Zag, 3 byte-identical runs per mechanism.
7. Micah's rulings (2026-09-24): judgment-channel ban ADOPTED as written;
   pointwise-revision ban MODIFIED to two-tier corroborated sequences
   (singletons proven unsafe, pairs proven unsafe on CC1); RK-3 85% bar
   TEST-FIRST (gate ceiling real at 74.77%; 86.6% only via unbuilt
   corroborated-revision machinery); V4 confirmatory trial for the two-tier
   rule HELD — do not run.
8. The judge's two-problem split (counsel synthesis): correlated-wrong
   corroborators (DEFENSE) and the 74.8% gate ceiling (OFFENSE) need different
   mechanisms, built separately.

## 1. External-opinion attempt log (verbatim)

- **grok-4.7** (highest reasoning, explicitly prompted super-thorough):
  3 attempts — all `HTTP 524: error code: 524` (two on the full brief, one on
  a 1,634-byte compressed brief). Endpoint down this session; same failure
  shape as the documented grok-4.6 whole-session outage. Not a verdict.
- **gpt-5.6-sol** (brief 1,376 bytes, inside the known-good ≤4.5KB envelope):
  3 attempts — all `choices: null`, 0 completion tokens, provider backend
  generating nothing (the documented flaky mode). Verified via the raw
  response dump each time; retried later per policy; never treated as a
  verdict.
- **claude-opus-5.5**: skipped — unreachable in the counsel round (2 socket
  timeouts + 1 HTTP 524) and no wrapper recovers it this session.
- **claude-fable-5.1**: reserved for ONE batched audit of the final slate
  (policy: expensive — batch, never many small rounds). Audit prompt covers
  7 questions (ordering, D2/O1/O3/FE1 kill-bar soundness, missing
  hypotheses, vacuous bars). 3 attempts — all `choices: null`, 0 completion
  tokens (provider backend generating nothing across models this session).
  Outcome recorded as PENDING in HYPOTHESES_R3.md; never treated as a verdict.

Per the standing rule, native subagent judgment is preferred; the connector
is a second opinion, and this round the second opinions did not arrive.

## 2. CHAMPION D — defense-first: "Stack the refusals; the hole is a conjunction"

**Core claim.** The deployment blocker (correlated-wrong corroborators) is not
one mechanism's problem — it is a conjunction of failures, and the defense is
a conjunction of refusals. Every refusal mechanism we have points the SAFE
direction (delay/withhold, never install-wrong): F5 blocks near known wrongs,
the CC1 margin guard refuses thin-margin agreement, H6 refuses uncorroborated
provisionals. No single one is sufficient — the 12 sustained TMB-5 wrongs
prove a resourced spoof can walk through any single layer — but the stack
F5(bank) + margin-guard + H6(no-provisional) refuses on three independent
axes, and a candidate must survive all three to install. Committed evidence:
H6 already scores 0 false installs on the clean stream; F5 blocks 8/9 known
false accepts at 0/34 true cost. The remaining question is not whether the
stack refuses — it is whether the stack refuses ENOUGH of the residual
sustained-corroborated wrongs, and at what liveness cost.

**Ranked defense hypotheses:**
- D1. The F5 + margin-guard + H6 stack, tested as one battery on the
  43 ACCEPT_INSTALL trials and the 12 sustained TMB-5 wrongs. Kill: any false
  install through the full stack on the frozen trials; or true-install
  retention < 26/34 with margin guard at its verified setting.
- D2. The F5 confirmation path is the load-bearing unbuilt half: backtest
  covered only the block predicate; "three deliberate re-inspections from
  three temporal crops" was never exercised. Hypothesis: deliberate
  re-inspection correctly confirms blocked TRUE candidates (releases them)
  while keeping blocked FALSE candidates blocked. This needs machinery nobody
  has built (true deliberate re-inspection organ). Kill: on the 8 blocked
  false accepts, confirmation releases ≥1 → kill the confirmation path; on
  ≥20 blocked true percepts (from the 300-percept red-team, in flight), <50%
  released within 3 re-inspections → the path is decorative, keep F5 as
  block-only.
- D3. Joint-error bin refusal (G6 folded into the F5 stack): corroboration
  disabled in raw-byte bins whose joint-wrong rate exceeds a frozen threshold,
  pending deliberate re-sense. This is the only mechanism that denies a
  sustained error the property it fakes (corroborability). Kill: on the
  12 TMB-5 wrongs, bins that would have refused them also refuse >10% of the
  34 true installs → granularity too coarse, kill.

**Steelman's attack on D (answered).** "The error lives in the bytes; every
refusal layer reads the same bytes, so the stack is three coats of the same
paint — a whole-stream spoof defeats all three at once, and you have bought
liveness loss for zero safety." Answer: the layers do NOT read the same
evidence in the same way — F5 reads the candidate's distance to known wrongs
(historical evidence, not the current bytes), the margin guard reads the
agreement margin between two corroborators (relational evidence), H6 reads
the absence of corroboration (temporal evidence). The byte-side wall killed
mechanisms that re-read the same bytes for the same judgment; these read
different facts. The wall does not apply. The liveness cost is real and must
be measured, not asserted — that is what D1's retention bar is for.

## 3. CHAMPION O — offense-first: "The ceiling is arithmetic, and arithmetic has two levers"

**Core claim.** Corner C of the counsel round proved it: 0.85 × 1102 = 937
installs needed; gate-side ceiling is 824; the sense must convert ≥113 of the
278. But "the sense must convert" is not one hypothesis — the diagnostics
decompose the 278 into two disjoint gaps, and the cheap one is not the sense
at all. DIAG_VERDICT_R24_RK3: K1 96.4% knowledge present in the system vs K2
74.8% reaching the gate's input. 25% of correct high-confidence percepts never
reach the gate input — a DELIVERY gap. Fixing delivery moves the ceiling
without touching the sense, the gate, or any proven ceiling.

**Ranked offense hypotheses:**
- O1. Knowledge-delivery repair. Mechanism: instrument the path from
  sense-emitted judgment to gate input on the frozen RK-3 battery; find and
  fix the drops (the verdict names "knowledge-delivery gap" as KNOWLEDGE —
  the rule/path is missing, not the signal). Kill: re-run the K1/K2
  diagnostics harness; KILL if K2 does not rise to within 2pp of K1, or if
  RK-3 does not rise by at least half the closed gap (delivery is load-bearing
  only if installs follow).
- O2. Corroborated-revision two-tier machinery (Micah's modified ban). The
  621/621 corroborated-revision replay recovered every conflict-withheld
  truth at 0 false installs — but that replay was OFFLINE, and the
  contradiction matrix proved the live form (CC1) false-installs when the
  corroborators are wrong. The live machinery does not exist: a gate that
  revises only on two agreeing high-conf PASSes WITH the margin guard AND the
  F5 bank as preconditions. This is the 86.6%-claim machinery — explicitly
  marked as UNBUILT. Kill: build it, run RK-3; KILL if RK-3 < 85% (the bar
  it exists to reach); KILL if any false install on the frozen red-team
  streams; KILL if CC1-cell behavior regresses (wrong-pair installs).
- O3. Disjoint-window second sense aimed at the 278 — NOT G5. G5 died because
  it re-read the same bytes for the same judgment. O3's scope is narrower:
  run ONLY on the frozen 278 (correct high-conf, never PASS), using byte
  windows DISJOINT from the first sense's formation windows, emitting PASS
  under the existing numerical bar or abstaining. It cannot touch
  already-PASS items; it cannot install — only the gate installs on its
  PASS like any other. Defense kill bars travel with it (counsel G5's):
  KILL if false-PASS on the 12 sealed families rises >2 points; KILL if it
  re-emits PASS on ≥2 of the six timbredisc wrongs; KILL if <100 of the 278
  convert to true PASS (85%-bar arithmetic needs ≥113; 100–112 = real effect,
  insufficient).

**Steelman's attack on O (answered).** "O1 is a rounding error and O2/O3 are
machinery that doesn't exist — you are ranking wishes." Answer: O1 is
measured, not wished — the 25% delivery gap is frozen in the diagnostics
verdict with K1/K2 numbers; it is the cheapest decisive experiment in the
program. O2 and O3 are explicitly flagged UNBUILT per the brief; ranking them
is honest about the build order: the test-first discipline means each gets a
frozen prereg before a single line of Zag, and the kill bars above are written
so the FIRST battery decides, not the tenth.

## 4. CHAMPION F — front-end-first: "The gate is done; the sense is the program now"

**Core claim.** The hardening verdict is explicit: "remaining failures are
FRONT-END, not gate — gate work has diminishing returns." H6's 0-false
installs on clean data is the gate-side endgame. Everything left is the sense
being fooled: the 12 sustained TMB-5 cross-span wrongs, and 53% accuracy on
the 12 sealed novel adversarial families. The death-board autopsy is the
proven method: 9 of 12 kills were KNOWLEDGE (signal existed, unused) — the
old synthesis "no detectable signal" was refuted by measurement. Apply the
same white-box method to the 12 novel families before building anything.

**Ranked front-end hypotheses:**
- FE1. Novel-family formation audit (no build). Mechanism: white-box the
  sense on each of the 12 sealed novel families; for each, either exhibit a
  separator with ≥80% accuracy on frozen data or produce a byte-level proof
  that truth is unobservable from the family's bytes (MOT-1 class). Kill:
  KILL the "sense can learn this family" claim per family if neither a
  separator nor an unobservability proof is produced — the family is then
  declared out-of-scope for the sense and must be refused by construction
  (defense-side), not chased.
- FE2. Structural detectors from the autopsy (V2-C's D1 worked). V2-C died
  overall, but D1 cut PTC-2 400→0 and the texture-correlation gate rescued
  86% of CCN-1 — family-specific structural detectors built from white-box
  autopsy are the one front-end intervention with measured wins. Mechanism:
  for each novel family where FE1 finds a separator, build the detector as a
  pure-Zag predicate over the sense's formation inputs. Kill: per family,
  KILL if the detector does not cut that family's confident-wrong rate by
  ≥50% on frozen data at ≤5pp cost to that family's true-PASS rate.
- FE3. Deliberate error-driven sense revision (the program-law endgame).
  Mechanism: the six timbredisc wrongs + the 12 TMB-5 wrongs become the
  sense's training signal — a native sense-training loop that revises
  formation weights from deliberate re-inspection reversals. UNBUILT
  machinery (no native sense-training loop exists). Kill: KILL if a full
  loop cannot be built in pure Zag with byte-identical reruns; KILL if the
  retrained sense does not cut held-out same-family confident-wrongs by ≥50%
  without RK-3 dropping >3pt.

**Steelman's attack on F (answered).** "53% on novel families is the sense's
honest accuracy — white-boxing 12 families is 12 science projects, and FE3 is
a training loop nobody has built. You are proposing to re-fight V2-C, which
died by measurement." Answer: V2-C died because it calibrated on
noise/surrogates and never measured recall on the target family (D3 fired
zero times — documented in D3_DEVIATION.md). FE1 is the measurement V2-C
skipped: it decides per family whether the signal exists at all. Families with
no signal are a defense problem (refuse by construction), families with unused
signal are a front-end problem (build the detector). That split is exactly
what the death-board autopsy bought us, and it is why 9 of 12 kills were
knowledge, not machinery.

## 5. Judge's ruling

**The two-problem split holds.** All three champions agree on the anatomy and
disagree only on priority — same as the counsel round's three corners. The
honest merge, updated with round-3 evidence:

- **Defense:** F5 survived as block-only; the confirmation path (D2) is the
  unbuilt half and the program-law endgame. The stack (D1) is the
  defense-in-depth bet, but it preregs now and runs only after the margin
  guard lands — running it on an unverified guard would launder the CC1 hole.
  D3 is the fine-grained refusal for the bin-shaped TMB-5 signature.
- **Offense:** O1 is the cheapest decisive experiment in the program — a
  measured 25% delivery gap, no new machinery, moves the ceiling
  arithmetically. O3 is kept but marked contested: its "disjoint windows"
  distinction from G5's death is a claim, and its kill bars are written to
  detect the wall re-asserting itself (≥2 timbredisc-wrong re-emissions kill
  it outright). O2 is the 86.6% machinery — prereg-only until V4 is released.
- **Front-end:** FE1 is the measurement V2-C skipped and the cheapest way to
  stop chasing unlearnable families. FE2 is gated on it. FE3 is the
  long-horizon program-law bet with the largest machinery gap on the slate.

**Ranked slate (expected value):** R3-1 O1 > R3-2 FE1 > R3-3 D2 > R3-4 D1 >
R3-5 O3 > R3-6 D3 > R3-7 O2 > R3-8 FE2 > R3-9 FE3. Full slate with frozen kill
bars in `HYPOTHESES_R3.md` (this directory).

**Build order:** O1 first; FE1 and D2 in parallel; D1 prereg now / run after
the margin guard; O3 after O1; D3, then FE2 (gated on FE1), then FE3;
O2 prereg-only until Micah releases V4.

**Coverage flags for the test coordinator (do not double-dispatch):**
- F5 300-percept red-team — parallel crew in flight.
- CC1 margin-guard verification — parallel crew in flight.
- V4 two-tier confirmatory trial — HELD; `PREREG_V4_TWOTIER_DRAFT_HELD.md`
  is a document only.

**Held for Micah:** the V4 prereg draft (above); the fable-5.1 batched audit
outcome (appended to HYPOTHESES_R3.md when it returns); O2 build/run
authorization; any prereg amendment the audit demands.
