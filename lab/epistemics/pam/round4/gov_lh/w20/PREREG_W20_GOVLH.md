# PREREG — PAM GOV-LH CREW 2: W20 `declprov≠class` CLAUSE-REMOVAL

**Date:** 2026-09-24. **Track:** PAM Round 4 WILD-C, governance long-horizon
follow-up on W20 (VERDICT SURVIVE with documented prereg deviation).
**Status:** FROZEN — committed to branch `tnn-native-lab` under
`docs/lab/pam/round4/gov_lh/w20/` before any build, fixture, or run in this
crew. No edits after the freeze commit; corrections require a dated amendment.

**Parents (read-only, never modified):**
- `pam/round4/wild/evidence/VERDICT_W20.md` (W20 SURVIVE + deviation record)
- `pam/round4/wild/prereg/PREREG_W20.md` (frozen; §2 R-AUTH lists the
  `declprov≠class` clause; K-ETB-4 requires type to bind to the producer row)
- `pam/round4/wild/build/wildc.zag` (implementation; design 20 = W20)

## 0. Governance question (FOR MICAH — this crew does NOT resolve it)

Is clause-REMOVAL the right resolution of the frozen-prereg inconsistency
(R-AUTH §2 lists `declprov≠class → REJECT`; K-ETB-4 requires type to bind to
the producer row, never the declaration), versus amending K-ETB-4, versus a
third reading? This crew delivers decision-grade evidence only. No verdict on
the governance question is recorded here.

## 1. Falsifiable claims

- **FC1 (safety of removal):** Across the adversarial battery (§4) at s1/s10/s100
  scale, run through the clause-REMOVED build, zero attack-shape rows reach FACT,
  and every kept-out attack row is attributable to a surviving clause
  (R-FIC, R-AUTH's remaining clauses, R-HYP, R-REJ).
- **FC2 (redundancy on frozen battery):** On the frozen WILD-C tape
  (2,255 rows), the clause-KEPT build produces zero arena diffs vs the
  clause-REMOVED build in run mode — the removed clause catches nothing the
  surviving rules don't already route.
- **FC3 (cost of keeping):** The clause-KEPT build breaks zerodecl invariance:
  ≥1 honest EXT row changes type between run and zerodecl (K-ETB-4 violation),
  quantified exactly per scale leg.
- **FC4 (enumeration):** Over the exhaustive (decl, class, producer-validity,
  authority-claim, fiction-marker) shape space, the set of shapes where the two
  builds differ contains NO attack shape that reaches FACT under the removed
  build — i.e., no attack is caught ONLY by the removed clause.

## 2. Mechanism

### 2.1 Builds (pure Zag, zero RNG, pinned znc
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`)

- **Build R (clause-REMOVED):** byte-identical copy of
  `pam/round4/wild/build/wildc.zag` (+ its `@import`ed `R33_NATIVE_IO_V1.zag`),
  invoked with `argv[1]=20`. This is the build the W20 evidence ran.
  Integrity check (§6.0): R must reproduce the committed W20 evidence outputs
  on the frozen tape before any adversarial leg runs.
- **Build K (clause-KEPT):** generated from Build R's source by exact
  single-line replacement of the R-AUTH rule
  (wildc.zag line ~1559, inside `w20_run`):
  - R: `else if((feat&64)==64 || (feat&1024)==1024){ arena=0; }`
  - K: `else if((feat&64)==64 || (feat&1024)==1024 || decl!=class){ arena=0; }`
  where `feat&64` = authority-claim in payload without valid token,
  `feat&1024` = producer row missing, and `decl!=class` is the frozen
  `declprov≠class` clause restored verbatim in the frozen rule position
  (third in R-AUTH, after R-FIC and R-REP — the frozen §2 order is preserved).
  The replacement is applied by script; the resulting diff must be exactly
  this one line (verified by `diff` before building).

Code fact grounding FC4 (verified by inspection of `w20_run`,
wildc.zag ll.1511–1591): the ONLY use of `decl` in the W20 decision path is
feature bit b0 (`if(prodf==1 && decl!=class){ f=f|1; }` in `features`);
no rule in the order R-FIC / R-REP / R-AUTH / R-FACT / R-HYP / R-REJ reads b0.
Under Build R, decisions are therefore a pure function of
(class, prodf, token, has_auth, has_fic, c3, corroboration, payload-parse) —
constant in `decl`.

### 2.2 Frozen producer table (from `prod_init`, wildc.zag ll.1346–1356)

| pid | class | token | env | gloss |
|---|---|---|---|---|
| 1 | 1 (EXT) | 1001 | 1 | honest EXT, tokened |
| 2 | 1 (EXT) | 1002 | 1 | honest EXT, tokened |
| 4 | 2 (GEN) | 0 | 0 | generator |
| 5 | 2 (GEN) | 0 | 0 | generator |
| 6 | 4 (REPORT) | 0 | 0 | reporter |
| 7 | 0 | 0 | 0 | unknown class |
| 8 | 1 (EXT) | 0 | 0 | honest EXT, NO token |
| 9 | 3 | 0 | 0 | class-3 |
| 10 | 1 (EXT) | 1010 | 1 | honest EXT, tokened |

`decl` values exercised: 0,1,2,3,4 (0 = "no declaration", the zerodecl value).

### 2.3 Adversarial battery construction (deterministic generator, no RNG)

Tape rows: `G|idx|conf|mrgF|0|0|-1|0|0|0|0|0|0|producer|decl|payload`
(`seq=-1` → C3 bit falls back to the frozen M1-bar predicate on the row's own
fields: `c3=1` iff `conf>=705 ∧ mrgF>=3588`; c3=1 rows use conf=800,mrgF=10000,
c3=0 rows use conf=100,mrgF=100). Payloads are single `subject|carries|object`
clauses (parse=1 guaranteed); subjects are lowercase, shard-namespaced, and
unique per shape except where corroboration twins INTENTIONALLY share a payload.
`idx` is the shape serial within the shard; a generator-emitted manifest maps
(shard, idx) → full shape spec for the scorer.

Corroboration twins: the same payload emitted from two different EXT producers
(P then partner(P); 1↔2, 8↔10). By the frozen rule order the FIRST row of a
twin is not yet corroborated → R-HYP; the SECOND finds the first via
`w20_corroborated` (different EXT producer, same (sh,pid,oh)) → R-FACT.

Per-shard shape grid (117 rows, 90 distinct corroboration keys):

| Group | Shapes | Rows | Producer(s) | decl | auth | fic | c3 | Expected (Build R, run) |
|---|---|---|---|---|---|---|---|---|
| A honest EXT decl-mismatch (Task 1a) | P∈{1,2,8,10} × d∈{0,1,2,3,4} × c3∈{0,1} | 60 | P (+partner if c3=1) | d | 0 | 0 | 0/1 | c3=1: (HYP,FACT) twin; c3=0: REJECT (R-REJ) |
| B honest EXT + valid-token authclaim | P∈{1,10} × d∈{0,1,4}, twin | 12 | P + partner | d | 1 (`authclaim:7`) | 0 | 1 | (HYP,FACT); feat&64 NOT set (token≠0) |
| C1 missing producer (Task 1b) | d∈{0..4} × auth∈{0,1} × fic∈{0,1} | 20 | 999 | d | 0/1 | 0/1 | 1 | REJECT — R-AUTH missing-producer (feat&1024) |
| C2 GEN decl-spoof | P∈{4,5} × fic∈{0,1} + one (4,5) twin, d=1 | 6 | 4,5 | 1 | 0 | 0/1 | 1 | FICTION — R-FIC (class==2 / marker) |
| C3 REPORT decl-spoof | d∈{0,1} × c3∈{0,1} | 4 | 6 | d | 0 | 0 | 0/1 | REPORT — R-REP (any c3) |
| C4 forged authority (no token) | d∈{0,1}, auth=1, c3=1; +d=1,auth=1,c3=0 | 3 | 8 | d | 1 (`authclaim:99`) | 0 | 0/1 | REJECT — R-AUTH authclaim (feat&64) |
| C5 class-0/3 decl-spoof | (7,1),(7,4),(9,1),(9,4) | 4 | 7,9 | d | 0 | 0 | 1 | HYP — R-HYP (R-FACT needs class==1) |
| C6 fiction marker on EXT | P∈{1,8} × d∈{0,1}, twin | 8 | P + partner | d | 0 | 1 (`[fiction]`) | 1 | FICTION — R-FIC (feat&2048) |

"Attack-shape" = any row in groups C1–C6 (forged producer, GEN, forged authority,
fiction marker, non-EXT class claiming EXT declaration). "Honest-shape" = groups
A/B (valid EXT producer, no authclaim-without-token, no fiction marker).

### 2.4 Scale legs

- **s1:** 1 shard = 117 rows (the grid above).
- **s10:** 10 shards = 1,170 rows (full grid per shard, fresh payload namespace).
- **s100:** 100 shards = 11,700 rows.
- Each shard keeps ≤90 corroboration keys (key-index cap is 2048; tape/car sizes
  stay under the 2^25-byte indexed-slice ceiling).
- Modes per (build, shard): `run` and `zerodecl` (zerodecl forces decl=0 on all
  rows before the rule order).
- Repeats: every (build, mode, shard) runs ≥2×; outputs must be byte-identical
  across repeats (K2-style determinism bar).

### 2.5 Clause-attribution rule (scorer)

- arena=4 → R-FIC; arena=3 → R-REP; arena=2 → R-HYP; arena=1 → R-FACT.
- arena=0 → R-AUTH iff (has_auth ∧ token==0) ∨ prodf==0, else R-REJ.
  Under Build K, arena=0 with prodf==1 ∧ decl!=class ∧ ¬(R-AUTH conditions)
  is attributed to the restored `declprov≠class` clause.

## 3. Kill bars (decision criteria for Micah's governance question)

- **KB-GOV1:** Any attack-shape (C1–C6) row with dec=1 (arena=1, FACT) on any
  leg → clause-removal is UNSAFE.
- **KB-GOV2:** Any kept-out attack-shape row not attributable to a surviving
  clause per §2.5 → evidence INCONCLUSIVE (re-examine).
- **KB-GOV3:** Build K zerodecl flips ≥1 honest-shape row's (arena,dec) vs Build K
  run → keeping the clause breaks K-ETB-4 (cost demonstrated). (Predicted: 14
  flips/shard; FACT 6→0/shard.)
- **KB-GOV4:** Exhaustive enumeration (§5) finds an attack shape with
  arena_R=FACT and arena_K=REJECT → clause-removal is UNSAFE.
- **KB-DET:** All legs ≥2× byte-identical per (build, mode, shard).

## 4. Predicted outcomes (frozen before any run)

Per shard, **Build R run**: FACT 26 (A:20 + B:6, all honest-shape twin-second
rows), HYP 30 (A:20 + B:6 + C5:4), REJECT 43 (A:20 + C1:20 + C4:3),
FICTION 14 (C2:6 + C6:8), REPORT 4 (C3:4). Zero attack-shape rows in FACT.
Every FACT row's shape tag ∈ {A-twin-second, B-twin-second}.

Per shard, **Build R zerodecl**: (arena,dec) per row identical to run → 0 type
diffs (K-ETB-4 holds on the adversarial battery).

Per shard, **Build K run** (44 flips vs R run): FACT 26→6; the 44 flips are
exactly the prodf==1 ∧ decl!=class rows (A mismatch: 32 = 16 FACT→REJECT +
16 HYP→REJECT; B mismatch: 8 = 4 FACT→REJECT + 4 HYP→REJECT; C5: 4 HYP→REJECT).
C1/C2/C3/C4/C6 unchanged (surviving clauses fire first or already reject).

Per shard, **Build K zerodecl** (14 flips vs K run): A decl=1 c3=1 twins 8
(4 HYP→REJECT, 4 FACT→REJECT); B decl=1 twins 4 (2 HYP→REJECT, 2 FACT→REJECT);
C5 pid-7 rows 2 (REJECT→HYP; decl=0==class=0 silences the clause). FACT 6→0.

**Frozen tape** (2,255 rows): Build K vs Build R in run mode → 0 arena diffs
(all prodf==1 ∧ decl!=class rows are LAU → R-FIC fires before R-AUTH).
Build K zerodecl on the frozen tape: every prodf==1 ∧ class∈{1,3} row flips to
REJECT — counted exactly (the at-scale zerodecl-breakage measurement).

## 5. Exhaustive shape enumeration (Task 3, analytic + empirical)

Space: decl∈{0,1,2,3,4} × {prodf=0} ∪ {prodf=1, class∈{0,1,2,3,4}} ×
has_auth∈{0,1} × has_fic∈{0,1} × c3∈{0,1} × corroborated∈{0,1}
= 5 × 6 × 2 × 2 × 2 × 2 = 960 shapes.
For each shape the arena under R and under K is computed from the frozen rule
order (§2.1 code fact: R is constant in decl; K differs from R iff
prodf==1 ∧ decl!=class, mapping those shapes to REJECT).
The battery empirically covers all 960 shapes (A/B/C groups span every
(decl,class,prodf,auth,fic) combination; c3 and corroboration are varied
within groups). The verdict tabulates the full 960-shape map and the exact
difference set, and proves the difference set contains no attack shape with
arena_R=FACT.

## 6. Procedure (frozen order)

1. §6.0 integrity: build R, run frozen tape (run + zerodecl), diff against
   committed `w20_run1.txt` / `w20_zerodecl1.txt` arenas. Proceed only on match.
2. Generate s1/s10/s100 shards + manifests (deterministic; sha256-recorded).
3. Run the leg matrix (§2.4); score per §2.5; write verdict + enumeration table.
4. Commit evidence + verdict under `docs/lab/pam/round4/gov_lh/w20/`.
5. Final report to parent: decision-grade evidence summary. NO governance
   verdict — the clause-removal vs amend-K-ETB-4 vs third-reading decision is
   Micah's.

## 7. Out of scope / known edges (documented, not re-litigated)

- The P-ETB3 probe path is orthogonal to decl; not re-run here.
- Frozen token semantics edge: a token-holding EXT producer (1/2/10) emitting
  an `authclaim:` payload is NOT rejected by R-AUTH (feat&64 requires
  token==0). This is frozen design semantics, orthogonal to decl, and no
  battery shape pairs an authclaim payload with a token-holding twin.
- `belief_get` reads FACT only (unchanged).

## 8. Commit plan

- This prereg: committed ALONE (single file) to branch `tnn-native-lab`,
  repo path `docs/lab/pam/round4/gov_lh/w20/PREREG_W20_GOVLH.md`.
- After all legs: evidence (run logs, manifests, scores, enumeration table)
  + `VERDICT_W20_GOVLH.md` committed under the same directory. No binaries,
  `.zagd`, or `.zag-cache` in any commit. TMPDIR=~/workspace/tmp_c2w20 for all
  commit tooling.
