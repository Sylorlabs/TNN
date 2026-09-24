# WILD-C TRACK ADDENDUM (frozen)

**Date:** 2026-09-24. **Track:** WILD-C (W16–W23, grok's eight wild designs,
renumbered from grok's W8–W15 labels which collide with debate/fable designs).
**Status:** FROZEN — committed before any WILD-C fixture, build, or run.
Parent documents: `PREREG_ROUND4.md` (program prereg, §4 kill-bar schema),
`wild/tape/TAPE.md` (frozen shared admission tape — used verbatim, never
modified), `wild/prereg/PREREG_AMEND1.md` (frozen M1 bar
(CT=705, MT=3588, ST=0, AT=0) = 910/1102 = 82.58%, used as-is, never
recalibrated), `wild/tape/TAPE_WILDA_ATTACKS.md` (frozen 14-row attack table,
consumed verbatim as the frozen attack tape).

This addendum pins every shared operationalization the eight WILD-C designs
need. Per-design preregs (`wild/prereg/PREREG_W16.md` … `PREREG_W23.md`) cite
this document and add only their design-specific rules and kill bars. Nothing
here alters a frozen value; where the frozen record is silent (e.g. C3's
disposition on non-corpus rows), the rule below is a preregistered
operationalization, stated explicitly as such.

## 1. Frozen inputs (pins asserted by generator and scorer)

| # | Source | sha256 |
|---|---|---|
| T | `pam/round3/m1/m1_cases.txt` | `5d4160d1e1a06c8250376bc85367981722fe0002296ae168c581c8353322c611` |
| C3C | `/home/hatch/workspace/pam_round2/o1_delivery/case_o1.txt` | `ed1ad01fb65a37125b06163bd1243bd930435e655b7a446c5f16fa91333e3357` |
| A | `wild/tape/TAPE_WILDA_ATTACKS.md` §3 table (14 rows) | byte-verbatim (generator `gen_attacks.py` reproduces it) |

C3C is the frozen C3 corpus: 11,840 rows,
`seq|tc|prog|progF|agree|strong|conf|mrgF|jcode|pred|meas|correct|truth`.
Its denominator rows (`correct==1 ∧ conf>=700`) are exactly the 1,102 C rows
of T as multisets over `(conf,mrgF,strong,agree)` (verified on-VM 2026-09-24;
21 duplicate keys, joined in file order within duplicates — §4).

## 2. Frozen C3 (operationalization)

"Frozen C3" = `run_gate(revised=True, adjudicator=True)` exactly as reproduced
in `round4/cu/score_cu.py` (itself a faithful copy of the frozen
`analyze_c3.py`), re-implemented in pure Zag in the WILD-C battery. The Zag
implementation runs the stateful mirror over C3C in file order and asserts the
frozen aggregate **791/1,102 = 71.78%** before any design logic runs. Per-row
INSTALL dispositions are `{PROVISIONAL_INSTALL, PERMANENT_INSTALL,
CORROBORATED, CHALLENGER_PROV, REVISED_INSTALL}` (prefix match, as in the
reference). The per-seq INSTALL bit is the design-facing "C3 bit".

**C3 bit rule (preregistered):**
- C rows: the mirror's per-seq INSTALL bit (seq from the §4 join).
- W, P, B, A rows: the frozen M1-bar predicate (`conf>=705 ∧ mrgF>=3588`).
  Rationale: the frozen C3 corpus contains none of these rows, so C3 has no
  defined disposition on them; the M1 bar is the frozen admit-predicate defined
  on exactly these rows' fields, and the attack addendum itself characterizes
  its rows by M1-bar passage ("they test whether a design's attack-specific
  machinery fires, not whether the bar catches them"). This is an
  operationalization, not a recalibration: no threshold is changed.

**"C3-only" comparator** (used by K-CTG-1, K-CC-4, K-DIR-3, K-TPC-3, K-ETB-5):
the C3 bit alone, with "admit" = bit 1. On the 14 attack rows all bits are 1
(all pass the M1 bar by construction), so C3-only catch = 0/14 on every attack
subset. A design's attack machinery is therefore measured against a 0 baseline,
exactly as the attack addendum intends.

## 3. K1 reading (preregistered)

K1 = no false-admit on the frozen wrong set (12 W + 9 P pairs). Per TAPE.md §1,
a P pair "installs/passes only if BOTH members pass": K1 is violated iff any W
row is admitted or **both members of any P pair** are admitted. Single-member
P admits are reported, never kills (precedent: the CU track preregistered its
two single-member P admits). W rows all have C3 bit 0 (mrgF < 3588); P pairs
5 and 6 have exactly one M1-passing member each, so no pair can be fully
admitted through any C3-gated path — a design that admits a full pair or any
W row does so through its own publish path and is killed.

## 4. Tape → percept synthesis (deterministic fixture construction)

The frozen tape carries no percept bytes, producer stamps, or declarations, so
`gen_wildc.py` (committed before any build) synthesizes them by fixed rules
from the row's frozen fields only. The synthesis never reads truth labels; it
maps row *classes* to percept *families* (the same standing the attack addendum
gives its rows). No design tunes to these bytes (K-NKL-4 / K-DIR-2); the bytes
are the fixture, the compiled tables are the instrument.

**ProducerTable (compiled, frozen):**

| id | class | auth_token | sensor_env |
|---|---|---|---|
| 1 | EXT(1) | 1001 | 1 |
| 2 | EXT(1) | 1002 | 1 |
| 4 | GEN(2) | 0 | 0 |
| 5 | GEN(2) | 0 | 0 |
| 6 | REPORT(4) | 0 | 0 |
| 7 | UNK(0) | 0 | 0 |
| 8 | EXT(1) | 0 | 0 |
| 9 | DERIVED(3) | 0 | 0 |
| 10 | EXT(1) | 1010 | 1 |

class enum: UNK=0, EXT=1, GEN=2, DERIVED=3, REPORT=4. Sorted by id; binary
search in-Zag. Producer 999 is deliberately absent (missing-row case).

**Predicate dictionary (compiled):** carries=1, claims=2, reports=3, says=4
(sorted; binary search; unknown predicate → clause rejects).

**Per-row synthesis** (`declprov` uses the class enum; payload is ASCII):

| Row | producer | declprov | subject | predicate | object | payload |
|---|---|---|---|---|---|---|
| C | [1,2,10][idx mod 3] | EXT | `tape` | carries | `ok` | `tape\|carries\|ok` |
| W | [1,2,10][idx mod 3] | EXT | `tape-w` | carries | `ok` | `tape-w\|carries\|ok` |
| P | [1,2,10][idx mod 3] | EXT | `tape-p` | carries | `ok` | `tape-p\|carries\|ok` |
| B | [1,2,10][idx mod 3] | EXT | `tape-b` | carries | `ok` | `tape-b\|carries\|ok` |
| A\|LAU | 4 (GEN) | EXT (claimed) | `tape-lau` | carries | `ok` | `tape-lau\|carries\|ok` |
| A\|FRK | 999 (missing) | EXT if decl_type=1 else GEN | `tape-frk` | carries | `ok` | `tape-frk\|carries\|ok` |
| A\|FRG | 8 (EXT, token 0) | EXT | `tape-frg` | carries | `ok authclaim:99` | `tape-frg\|carries\|ok authclaim:99` |

Notes:
- Honest families share one canonical claim per family on purpose: the honest
  tape measures whether a design *preserves* frozen C3 behavior on honest
  traffic (K3); attack/probe fixtures measure whether the new machinery fires.
  Subjects are distinct per family so no cross-family settlement, promotion,
  or corroboration occurs.
- The `authclaim:99` marker is scanned in the raw payload by the feature
  extractor (fixed ASCII marker table); it is never a gate input by itself.
- FRK rows exercise the missing-producer path (binary-search miss) with
  contradictory declarations across the two members of each session.
- C-row seq join: multiset match on `(conf,mrgF,strong,agree)` between T's C
  rows and C3C's denominator rows (multisets verified equal); the 21 duplicate
  keys join in file order within each duplicate group (T's C order preserves
  C3C file order — verified on-VM). Non-C rows carry seq = -1.

**Fixture files** (generated by `gen_wildc.py`, committed before builds):
- `wildc_tape.txt`: 2,255 lines (2,241 tape + 14 attack, tape order = file
  order of T, attacks appended in addendum order):
  `K|idx|conf|mrgF|strong|agree|seq|tc|prog|progF|jcode|pred|meas|producer|declprov|payload`
  (idx = 0-based global file row number; `tc…meas` zeroed — the fixture
  carries the joined `seq` instead; `seq=-1` for non-C rows.)
- `wildc_probes.txt`: probe rows:
  `Q|design|probeid|conf|mrgF|producer|declprov|future_ok|flip|payload`
  (see §7; `future_ok`/`flip` are probe scaffolding consumed only in probe
  mode, never on the tape).

## 5. Shared battery pipeline (pure Zag, one binary, argv-selected design)

`wildc.zag` (imports `common.zag`, both compiled from the build directory):
1. Reads C3C, runs the mirror, asserts 791/1,102 (hard fail otherwise).
2. Reads the fixture, processes rows in order through: parse → canonicalize
   (NUL/non-UTF8 reject; CR/LF→LF; A–Z→a–z; collapse [ \t\n]+ → 0x20; strip;
   split `;` → clauses; split first `|` → subject/rest → predicate/object;
   predicate dict lookup; FNV-1a/64 over exact field bytes) → producer lookup
   → feature word → frozen C3 bit → design rule → OUT line.
3. Modes: `run` (tape), `zerodecl` (tape with declprov forced 0 — K-CTG-2 /
   K-ETB-4), `probe` (probe rows for the selected design, fresh state).
4. Emits `OUT|…`, `SUM|…`, `KB|…` lines to stdout. No wall-clock reads, no RNG.

**Feature word (u16, extracted in bit-index order; designs use subsets):**
b0 declprov≠class (0 if producer missing); b1 class==EXT; b2 class==GEN;
b3 class==REPORT; b4 sensor_env==1; b5 token!=0; b6 payload contains
`authclaim:` while token==0; b7 parse succeeded; b8 multi-clause;
b9 evidence-ref count==0 (always 1 on synthetic percepts — recorded, no
receptor masks it); b10 producer row missing; b11 fiction marker `[fiction]`
present; b12 wall-clock *claim* digit-pattern present (scan only, never reads
the clock); b13 speech predicate (says/claims/reports); b14 object contradicts
a BELIEF key (design-local lookup; 0 if the design keeps no belief keys);
b15 class==UNK.

## 6. Per-design compiled tables (frozen in the build)

- **W16 ProvRules** (first match wins): R0 parse-fail→UNK; R1 GEN→GEN;
  R2 authclaim-without-token→UNK; R3 REPORT→REPORT; R4 EXT+envelope→EXT;
  R5 row-exists→DERIVED; else UNK. Masks/values over the §5 feature word.
- **W18 SeedGaps** (sorted by gap_id): G1 (domain=FNV("tape"), pred=1,
  evidence={EXT}, OPEN); G2 (domain=FNV("probe"), pred=1, evidence={EXT},
  OPEN). Disjoint from all frozen fixtures (synthetic domains).
- **W21 v1 receptors** (sorted by receptor_id): id1 mask=b6 pat=b6 (tokenless
  authority); id2 mask=b0|b2 pat=b0|b2 (GEN wearing foreign declaration);
  id3 mask=b10 pat=b10 (missing producer); id4 mask=b7 pat=0 i.e. parse-fail;
  id5 mask=b11 pat=b11 (fiction-mark). Maturation stays OFF (no code path).
  *Corrigendum 2026-09-24 (pre-build): id1 was mask=b2 and id2 mask=b0|b3,
  which contradicted their intents (b2 is class==GEN, b3 is class==REPORT —
  a GEN can never have b3 set, and forged-authority rows are class EXT, so
  FRG rows would have escaped all receptors). Corrected to id1=mask b6
  (tokenless authority) and id2=mask b0|b2 (GEN wearing foreign declaration)
  so the five receptors match the five intents.*
- **W21 BenignAnchors** (compiled, disjoint from every frozen fixture):
  A1 `anchor-a|carries|ok` prod 1 EXT; A2 `anchor-b|carries|ok` prod 2 EXT;
  A3 `anchor-c|carries|ok` prod 10 EXT; A4 `anchor-d|carries|ok` prod 8 EXT
  (no token, no envelope — still benign); A5 `anchor-e|says|ok` prod 1
  (speech predicate, EXT); A6 `anchor-f|carries|ok` prod 9 DERIVED;
  A7 `anchor-g|carries|ok` prod 6 REPORT; A8 `anchor-h|carries|ok` prod 7 UNK.
  None may be vetoed (K-DIR-4). They run in probe mode.
- **W17 CC-5 item** (named here, before any run, not from frozen fixtures):
  subject `anchor-sol`, predicate `carries`, object `steady`, producer 1,
  M1-passing (conf 900, mrgF 20000). Must remain quarantined (K-CC-5).

## 7. Probe catalog (all in `wildc_probes.txt`, run in `probe` mode)

| Probe | Design | Purpose | Expectation |
|---|---|---|---|
| P-CTG3 | 16 | hostile pre-canonical bytes + benign claim | hostile clause never a belief; benign claim admitted iff C3 bit 1 |
| P-CC5 | 17 | §6 CC-5 item | QUARANTINE, never belief |
| P-NKL2 | 18 | probe/alpha then probe/beta (same subject+pred, different objects, rank 4≤4, both C3-pass) | second NOT belief (veto) |
| P-AF2 | 19 | future whose expected_hash covers key only | UNSTAKED at insert, never belief |
| P-ETB3 | 20 | REPORT producer + `says` predicate | payload in REPORT only; belief_get(payload) MISS |
| P-DIR5 | 21 | bits b0+b2+b3 (double receptor hit) | veto logged with receptor_id=1 |
| P-TPC2 | 22 | flip one fast-path feature bit | DivergenceRec emitted |
| (anchors) | 21 | §6 BenignAnchors | zero vetoes |

(K-CTG-2 / K-ETB-4 use `zerodecl` mode, not probe rows.)

## 8. Kill-bar adoptions (coordinator ruling)

- **K6 (staleness, ADD-ONLY, adopted):** every design decides synchronously
  inside one admission pass; no decision reads ledger state written more than
  the current row's processing earlier — there is no async path, no
  background reconciler, no deferred queue in any W16–W23 build. Staleness is
  0 by construction; the build notes assert it per design.
- **K7 (calibration-sensitivity, NOT adopted):** no WILD-C instrument contains
  a calibrated threshold. The only numerics are frozen bars (M1, C3 — hands
  off), compiled constants (table sizes, enum orders), and the FNV hash
  (an address, not a threshold). There is nothing to sensitivity-audit.
- **K8 (classification audit via dual-run verification, ADD-ONLY, adopted):**
  the independent Python scorer re-verifies every OUT decision against the
  preregistered rule from the OUT line's recorded intermediates, and re-runs
  the C3 mirror independently. Any unverified number is reported UNVERIFIED.

## 9. Hands-off compliance

(a) M1 threshold adoption — untouched; the frozen bar is used only as the
§2 operationalization predicate, never recalibrated or adopted.
(b) Fable's 4 kill-bar repairs (D2, O3, O1-fatal, FE3→FE3a/FE3b) — not applied.
(c) The 3 HELD items (V4 two-tier, O2 live machinery, F5 tightened-window) —
not run. No WILD-C file touches W1–W15 designs.

## 10. Standing-law note (verdict-time)

Per Micah's 2026-09-24 standing law, each VERDICT_W{16..23}.md classifies every
frozen numeric cap the design relies on as load-bearing (kill-bar evidence of
what breaks without it) or arbitrary (flagged for removal even if the design
survives). Analysis only — no mechanism is altered to comply.
