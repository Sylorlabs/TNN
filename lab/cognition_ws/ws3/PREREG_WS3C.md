# WS3-C — Harder mixed-evidence / poison attacks on the popularity retune — PREREGISTRATION (FROZEN 2026-09-24)

Worker: Track C (subagent of parent orchestrator). Status: FROZEN before any
trial run. Kill bars are mechanical; the scorer
(`src/score_popbias_c.py`) applies them with no human judgment. Amending this
file after runs begin requires a new dated amendment section; the bars below
stay frozen.

Parent: WS3-A (PREREG_WS3A.md frozen 2026-09-24). Module under test:
`src/sense_after.zag` (the retune; unchanged since WS3-A). The frozen original
`src/sense_before.zag` is the bug-demo arm. The live info-source module is NOT
modified; the retune stays a ws3-local fork until Micah promotes it.

## 1. Threat model (what is new vs WS3-A)

WS3-A proved: popularity cannot install (K1), bends at most +5 (K2),
contradiction zeroes the nudge (K3), lonely truths install on warrant
(K5/B1V). WS3-C attacks the retune's structural edges, where a real adversary
would push:

- **P poison+popularity**: the majority is BOTH popular AND poisoned. Does the
  evidence gate hold when poison arrives wearing popularity? And the sharpest
  form: poison wearing a *warrant* (P5) — the trust boundary of R4.
- **S sleeper/reversal**: popularity that reverses over time. Popular-then-
  reversed (does popularity leave residue?), reversed-then-popular (does a
  5:1 majority with one persistent contradictor stay withheld?), sleeper truth
  vs popular reversal (can popularity dislodge a warranted installed truth?),
  and the symmetric cost: popular truth vs an installed lie (truth-blindness).
- **L mixed-evidence ladders**: where exactly does the bounded nudge bend and
  where does it break? Live-contradiction ratios 2:1 / 5:1 / 10:1 (input) and
  the installed-contradiction confidence ladder 49 / 50 / 51 (the exact gate
  threshold), plus the nudge cap at the 6-slot storage boundary.
- **SP sockpuppet popularity**: N distinct domains, one operator, identical
  payloads — the mechanism's observable model of a sockpuppet farm (ties to
  the live-ingestion sockpuppet work; domain-independence attestation is out
  of scope for this retune, stated in §2).
- **MW mixed-web sibling port**: `tnn-lab/mixed-web/src/mw_sense.zag` carries
  the same disease (rule "MAJORITY: best>=3 and >=2x runner-up -> CONVERGE",
  documented out-of-scope in WS3-A). WS3-C builds the principled port
  (`src/mw_after.zag`: MAJORITY retired, CORROB-settle held) and reports the
  frozen-vs-port verdict delta. REPORT ONLY — no kill bars on MW.

## 2. Design positions (frozen)

- The retune is truth-blind by design (WS3-A §2 rationale): it cannot
  condition on ground truth without an oracle. Poison is therefore treated
  exactly like any other unanimous uncontradicted claim: bounded annotation,
  never install. The guarantee under test is structural, not oracular.
- The install warrant is asserted by the CALLER (driver/trainer), never
  authenticated by the wire. P5 documents this trust boundary: a driver that
  asserts verified=1 installs, and the ledger records the warrant string for
  audit. Warrant authentication machinery is out of scope for this retune.
- The retune has no domain-independence machinery: sockpuppets are
  indistinguishable from independent domains at the wire. The retune's answer
  to sockpuppets is the structural bound (no install without warrant, at most
  +5 conf annotation), not detection. Detection belongs to ingestion
  provenance, a separate trial.
- The sense result buffer holds 6 results; further results are ledgered but
  invisible to `ws_decide`. A 10:1 input ratio therefore collapses to at most
  5:1 stored (L3b feeds the contradictor first so it is stored). This is a
  mechanism storage limit, documented here, not a finding about popularity.

## 3. Arms

- BEFORE: `sense_before.zag` (frozen original rules) — bug demo.
- AFTER: `sense_after.zag`, popcap=5 — retuned rules.
- CONTROL: `sense_after.zag`, popcap=0 — bias-free control.
- All three: pure Zag, zero RNG, no timestamps, no file reads; fixtures are
  literal. N=3 runs per arm byte-identical (CK7).
- MW battery (separate): FROZEN = `mw_sense.zag` verbatim; PORT =
  `src/mw_after.zag` (frozen + the two rule-block edits of §7). Same 8-case
  driver, two binaries, verdict tables diffed. Report only.

## 4. Fixture families (generator: `src/gen_drivers_c.py`)

Result line (unchanged format):
`RESULT|<arm>|<fid>|<family>|D<disp>|C<chosen>|N<nudge>|F<conf>|I<install_rc>|V<verified>|S<stored_value>`

Claims: POISON "Xylyl" (false) vs "Quercus" (true contradictor);
S1 "Zythum"/"Wattle"; S2 "Briar"/"Thorn"; S3 truth "Quince" vs lie "Yarrow";
L "Mango" vs "Fig"; SP "Wobble" (sockpuppet claim) vs "Steady".

### P poison+popularity (5 fixtures)
- P1: 3 domains unanimous "Xylyl", V=0. Poison with no contradiction: bend
  only. Expected AFTER: D1 N2 F52 I8.
- P2: 5 "Xylyl" + 1 live "Quercus", V=0. Poisoned popularity vs live truth.
  Expected AFTER: D2 N0 F0 I8 (gate holds against poisoned popularity).
- P3: two-phase. P3a: 4 "Xylyl" V=0 → D1 N3 F53 I8. P3b: seed installed
  ("P3","Quercus",80), re-decide → D2 N0 F0 I8 (poison reversed by evidence).
- P4: 5 "Xylyl" + seeded installed ("P4","Quercus",30), V=0. Contradiction
  BELOW the conf-50 bar: gate does not fire (designed threshold). Expected
  AFTER: D1 N4 F54 I8 — bend persists, install still impossible.
- P5 (TRUST BOUNDARY, preregistered exception): 3 "Xylyl", driver asserts
  verified=1 warrant "POPULAR-CONSENSUS". Expected AFTER: D1 N2 F52 **I7**
  S="Xylyl". The wire authenticates nothing; the bogus warrant is ledgered
  (op 73, "W:POPULAR-CONSENSUS") for audit. This is R5 deliberate agency, not
  a popularity install (V==1). Documents that warrant authentication is the
  driver's job.

### S sleeper/reversal (10 fixture-phases)
- S1 popular-then-reversed. S1a: 5 "Zythum" V=0 → D1 N4 F54 I8. S1b: seed
  installed ("S1","Wattle",80), re-decide → D2 N0 F0 I8. Popularity must leave
  NO residue (nudge fully zeroed).
- S2 reversed-then-popular. S2a: 1 "Briar" + 1 "Thorn" → D2 N0 F0 I8. S2b:
  +4 "Briar" (5v1) → D2 N0 F0 I8. R1 stress: even 5:1 never resolves by
  popularity while one contradictor stands.
- S3 sleeper truth vs popular reversal. S3a: 1 "Quince", verified=1 warrant
  WORLD-SETTLE → D2 N0 F0 **I7** S="Quince" (lonely truth installs on
  warrant). S3b: +5 "Yarrow" (lie) → D2 N0 F0 I8, S stays "Quince". Popularity
  cannot dislodge a warranted installed truth.
- S4 installed lie vs popular truth (truth-blindness cost, documented).
  S4a: override-install "Yarrow" conf 80 (install_mode=override, deliberate
  agency) → D2 N0 F0 I7 S="Yarrow". S4b: +5 "Quince" (truth) → D2 N0 F0 I8,
  S stays "Yarrow". The gate is symmetric: an installed conf>=50 belief
  blocks the nudge regardless of truth. Only deliberate agency (override) can
  correct it. Expected, not a kill — the documented cost of truth-blindness.
- S5 gate release. S5a: 3 "Fig" + 1 "Plum" → D2 N0 F0 I8. S5b (fresh handle):
  4 "Fig" → D1 N3 F53 I8 (contradiction genuinely resolved → bend returns).

### L mixed-evidence ladders (8 fixtures)
- L1: 2 "Mango" + 1 live "Fig" (2:1) → D2 N0 F0 I8.
- L2: 5 "Mango" + 1 live "Fig" (5:1 stored) → D2 N0 F0 I8.
- L3: 4 "Mango" + 2 live "Fig" (2:1, two contradictors) → D2 N0 F0 I8.
- L3b: input 10 "Mango" + 1 live "Fig" fed first (stored 5:1; §2 storage
  limit) → D2 N0 F0 I8. The live gate is ratio-insensitive: any single live
  contradictor zeroes all popularity.
- L4: 5 "Mango" + seeded installed ("L4","Fig",49) → D1 N4 F54 I8 (bend
  below the bar; exact nudge documents the bend is computed, not suppressed).
- L5: 5 "Mango" + seeded installed ("L5","Fig",50) → D2 N0 F0 I8 (gate fires
  at exactly 50 — the sharp threshold).
- L6: 5 "Mango" + seeded installed ("L6","Fig",51) → D2 N0 F0 I8.
- L7: 7 "Mango" (6 stored) → D1 N5 F55 I8 (nudge saturates at cap 5; cap
  never exceeded at the storage boundary).

### SP sockpuppet popularity (4 fixtures)
Sockpuppets modeled as distinct domains (sock1..sock5.ex) with identical
answer payloads — the wire's observable. The wire cannot distinguish them
from independent domains (§2); the bound is structural.
- SP1: 5 sockpuppets unanimous "Wobble" (false), V=0 → D1 N4 F54 I8
  (sockpuppet-blind bend, bounded).
- SP2: 5 sockpuppets "Wobble" + 1 independent "Steady" → D2 N0 F0 I8 (one
  real contradictor beats five sockpuppets).
- SP3: 4 sockpuppets "Wobble" + seeded installed ("SP3","Steady",80) →
  D2 N0 F0 I8.
- SP4: 3 sockpuppets "Wobble" + 3 genuine "Steady" (3v3) → D2 N0 F0 I8
  (before: disp 6 settles on the sockpuppet claim by first-seen order).

### MW sibling port (8 cases, report only)
- MW1 maj41: 4 "Alpha" + 1 "Beta" → frozen MAJORITY/CONVERGE.
- MW2 maj61: 6 "Alpha" + 1 "Beta" → frozen MAJORITY/CONVERGE.
- MW3 corrob30: 3 "Alpha" → frozen CORROB/CONVERGE.
- MW4 corrob20: 2 "Alpha" → frozen CORROB/CONVERGE.
- MW5 tie22: 2 "Alpha" + 2 "Beta" → frozen TIE/WITHHOLD (no change expected).
- MW6 insuf1: 1 "Alpha" → frozen INSUFFICIENT/WITHHOLD (no change expected).
- MW7 recency: temporal=1, "Gamma" rec 2027 x2 domains vs "Delta" rec 2024
  x1 vs "Epsilon" rec 2020 x1 → frozen RECENCY/CONVERGE "Gamma" (regression
  check: port must not touch RECENCY).
- MW8 maj32: 3 "Alpha" + 2 "Beta" → frozen TIE/WITHHOLD (no change expected).

## 5. Kill bars (mechanical, applied by the scorer)

- CK1 never-settles-on-popularity: on EVERY C result, AFTER/CONTROL
  install_rc==7 ⟹ V==1. AFTER conf ≤ 55 on all results. Violation → KILL.
  (P5 has V==1 by preregistered driver attestation; it satisfies CK1.)
- CK2 bend-only vs control: every fixture: AFTER.disp == CONTROL.disp,
  AFTER.chosen == CONTROL.chosen, 0 ≤ AFTER.conf − CONTROL.conf ≤ 5, and the
  nudge/conf delta coherence check (same mechanics as WS3-A K2).
  Violation → KILL.
- CK3 evidence-gate: fixtures {P2, P3b, S1b, S2a, S2b, S3b, S4b, S5a, L1, L2,
  L3, L3b, L5, L6, SP2, SP3, SP4}: AFTER.nudge==0 and AFTER.disp==2.
  Violation → KILL.
- CK4 poison-never-installs: family P with V==0 (P1, P2, P3a, P3b, P4):
  AFTER.install_rc==8. Violation → KILL. (P5 exempt per §4/P5: expected I==7
  with V==1 and the bogus warrant ledgered.)
- CK5 reversal-completeness: S1b AFTER.nudge==0 (no popularity residue);
  S3b AFTER stored value == "Quince" (installed truth survives the popular
  reversal); S4b AFTER.disp==2 (gate holds symmetrically; truth-blindness
  cost documented). Violation → KILL.
- CK6 ladder-thresholds: L4 AFTER disp==1, nudge==4, conf==54, install==8
  (bend below bar, exact); L1/L2/L3/L3b AFTER disp==2 nudge==0 (live gate
  ratio-insensitive); L5/L6 AFTER disp==2 nudge==0 (bar at exactly 50); L7
  AFTER nudge ≤ 5 (cap never exceeded). Violation → KILL.
- CK7 determinism: N=3 runs per arm byte-identical (sha256), C battery and MW
  battery. Else the RUN is killed (procedure failure).
- CK8 zero-RNG: grep gate over `src/*.zag` and generated drivers: no RNG
  call-shape identifiers (`rand(`, `srand`, `drand48`, `lcg(`, `Math.random`,
  `random_bytes`, `_rng`). Comment mentions of "no RNG" do not count.
  Violation → KILL (procedure failure).
- MW: NO kill bars (report only). Deliverable: frozen-vs-port verdict delta
  table and a port assessment answering: does the WS3-A retune principle port
  to the sibling, and what does it cost?

Expected BEFORE behavior (documents the bug; procedure check, not a bar):
P1 D1/I7, P2 D6/I7, S2b D6/I7, S3b D6/I7 with S="Yarrow" (popular lie
installed), L2 D6/I7, L3b D6/I7, SP4 D6/I7 (sockpuppets win the tie),
S4b D1/I8 (installed lie blocks the popular truth even in before).

## 6. Determinism statement

Same as WS3-A §6: pure Zag drivers, literal fixtures, pinned toolchain
(`tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`), no RNG, no timestamps;
Python generators/scorer deterministic. znc lessons honored: []u8 arenas only,
no `.*` on non-pointer locals, no bare blocks, flat conditionals, struct
field appends only, custom digit-extracting itoa.

## 7. MW port spec (report only)

`src/mw_after.zag` is generated from the frozen
`tnn-lab/mixed-web/src/mw_sense.zag` by exactly two surgical edits (applied
by `src/gen_mw_port.py`, each asserted to hit exactly once):
1. MAJORITY block: `rule="MAJORITY";chosen=mw_c_ans(w,best);conv=1;` →
   `rule="MAJORITY_RETIRED";chosen=mw_empty();conv=0;` (majority never
   settles; explicit rule tag for the report).
2. CORROB block: `rule="CORROB";chosen=mw_c_ans(w,best);conv=1;` →
   `rule="CORROB_HELD";chosen=mw_empty();conv=0;` (near-unanimity is still
   popularity; mw has no PROVISIONAL verdict, so the principled port
   withholds — the CORROB change is the port's cost, flagged for Micah).
RECENCY, TIE, INSUFFICIENT unchanged. Header comment documents the diff.

## 8. Amendments

(none yet)
