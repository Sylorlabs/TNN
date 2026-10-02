# SEALED_EVAL_PART1.md - F1-FOLLOWUP Part 1 sealed evaluation results

Lane F1-FOLLOWUP, wave wave-20261001-2321pdt. Sealed runs executed
2026-10-02 ~00:00 PDT against the frozen F1 binary
`../F1/impl/f1_learn` (sha256
6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847,
verified before running; match confirmed) and the prior wave's frozen
binary (sha256
0c571abca5a3c16695115228114c327bb3370081304c9c3a1ea1354840aa2727,
verified before running; match confirmed). Fixture hashes verified
against sealed/FIXTURE_SHA256.txt (all 24 match; the Part 1 fixtures
are hash-verified copies of F1's sealed fixtures plus the prior wave's
validated W2 fixtures). Attack prereg: PREREG_PART1.md (committed alone
at 001fcfaca before any sealed run of this lane; no implementation
work exists in this lane).

No em-dashes are used in this document.

## 1. Determinism evidence

Each of the 24 sealed invocations was executed 3 times (runs1/1,
runs1/2, runs1/3; 144 state/trace/pred outputs per repetition). All
corresponding outputs are byte-identical across the three repetitions
(cmp-verified, zero diffs). SHA-256 of all runs1/1 outputs is recorded
in runs1/DETERMINISM_SHA256.txt. Zero randomness in decision paths.
The determinism standard is met.

## 2. K-TRIG-FIRE: fires on interleaved errors (PASS)

Trigger episodes on sealed train runs (bar: at least one TRIGGER with
episode index < 12):

| pattern | triggers | first trigger ep | bar |
|---|---|---|---|
| T-A alternating | 2 | 2 | PASS |
| T-B 1-in-3 | 1 | 3 | PASS |
| T-C 1-in-4 | 1 | 4 | PASS |
| T-D bursty 2-on-6-off | 3 | 1 | PASS |

Reproduces F1's sealed result exactly.

## 3. K-TRACE: construction follows the trigger (PASS)

CONSTRUCT events per sealed train run (bar: at least 2, episode-indexed
at or after the first trigger; no final-isomorphic structure existed
before the first construction event, seed state only):

| pattern | constructs | construct eps | first trig | bar |
|---|---|---|---|---|
| T-A | 3 | 2, 5, 5 | 2 | PASS |
| T-B | 2 | 3, 3 | 3 | PASS |
| T-C | 2 | 4, 4 | 4 | PASS |
| T-D | 6 | 1, 1, 3, 3, 9, 9 | 1 | PASS |

## 4. K-LEARN-INTERLEAVED: the trigger enables learning (PASS)

Hidden accuracy on sealed 30-probe sets, trained state in
(bar: at least 80 percent): T-A 30/30, T-B 30/30, T-C 30/30,
T-D 30/30. All 100 percent. Firing without learning would fail here;
it does not.

## 5. K-TRIG-CLEAN: no false positives (PASS)

TRIGGER lines on clean runs (bar: 0; frozen false-positive rate 0):
C-A 0, C-B 0, C-C 0.

## 6. K-C0C-REG: no regression (PASS, corrected bar)

Leg W2 (prior wave's validated W2 fixtures, both binaries). The new
binary reproduces the old binary's behavior exactly:

- TRIGGER episodes: new [1], old [1]. Identical.
- Normalized CONSTRUCT event sequence (cmp_events, pure Zag):
  new and old outputs byte-identical:
  TRIG 1; CONS 1 0 0 ADD 0 8 8 6 2; CONS 1 1 1 ADD 0 0 9 2 1;
  CONS 1 2 2 ADD 0 0 9 1 0.
  (Matches the prior wave's characterized behavior: TRIGGER 1, same
  3 constructs in order, err transitions 6->2, 2->1, 1->0.)
- Final main-graph signature (f1_score sig): ISO 1, signatures
  identical: N 4 0 8 8 0 0;N 4 0 0 9 0 0;N 4 0 0 9 0 0;N 2 0 0 0 0 0;
  (structure [4 4 4 2], identical to the prior wave).
- Hidden: new 30/30, old 30/30; hidden pred outputs byte-identical.

Leg R-W3 (F1 sealed R-W3 fixtures, validated by F1's passing run):
hidden 30/30 (bar 80 percent), 2 CONSTRUCT events (bar 2). PASS.

No trigger regression. The corrected bar is met exactly where F1's
bar was miscalibrated.

## 7. K-ABL-TA and K-BASE-TA (PASS)

T-A hidden (30 probes): trained 30/30 = 100%; seed-state (ablated)
13/30 = 43%; exact-match memorizer (24-episode budget) 13/30 = 43%.

- K-ABL-TA: 100 - 43 = 57pp >= 40. PASS.
- K-BASE-TA: 100 - 43 = 57pp >= 40. PASS.

## 8. K-C0A source audit (PASS)

grep over the frozen F1 implementation sources (impl/f1_isa.zag,
impl/f1_learn.zag): zero hits for forbidden protected semantics,
downgrade kill-pattern markers, and menu/kit/candidate-family markers
(all three greps exit 1). The only tag dispatch is the frozen ISA op
dispatch. No researcher-authored semantic cases were added.

## 9. NC-TRIG negative control (PASS; battery has teeth)

Prior wave's frozen binary on sealed T-A train: 0 TRIGGER lines.
The battery reproduces the W1 defect on the old mechanism. Not a void.

## 10. Verdict: BUILD-PASS

Every frozen bar passes: K-TRIG-FIRE, K-TRACE,
K-LEARN-INTERLEAVED, K-TRIG-CLEAN, K-C0C-REG (Leg W2 exact
behavioral match on validated fixtures; Leg R-W3 30/30 with 2
constructs), K-ABL-TA, K-BASE-TA, K-C0A, NC-TRIG, determinism 3/3.

The corrected K-C0C-REG bar confirms what F1's killing-evidence
section diagnosed: the trigger change introduces zero regression on
the validated fixtures (identical trigger episode, identical construct
sequence, identical structure, identical hidden predictions). The
original BUILD-FAIL came from the bar-calibration mistake, not from
the trigger. Bounded L2+ ceiling stands; no L3 claim follows.

Evidence paths (all under
docs/lab/rsi/runs/wave-20261001-2321pdt/F1-FOLLOWUP/):
- PREREG_PART1.md (frozen bars, fixture hashes)
- sealed/ (hash-verified fixture copies, run_sealed1.sh,
  FIXTURE_SHA256.txt)
- runs1/ (1, 2, 3 repetitions; DETERMINISM_SHA256.txt)
- dev/cmp_events.zag (pure-Zag normalized event comparator)
