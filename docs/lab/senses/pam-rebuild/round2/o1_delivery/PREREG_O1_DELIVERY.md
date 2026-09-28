# PREREG O1 — Knowledge-delivery repair (PAMs Round 2, hypothesis R3-1)

**Status: FROZEN 2026-09-24. Committed alone — before any build output exists.**
**Hypothesis:** R3-1 O1 (HYPOTHESES_R3.md, round-3 debate slate): the sense→gate
knowledge-delivery gap is the largest quantified deficit (K1 96.4% vs K2 74.8%).
**Branch:** `tnn-native-lab`, repo `sylorlabs/TNN`.
**Evidence base (frozen, read-only):**
`docs/lab/senses/pam-rebuild/round2/forks/R2-4/evidence/clean/sweep.jsonl`
(11,840 rows, sha256 `4163fffa65f18f552d48f7efec0e9800a7406547a27c6259d39a48ec7f0833f2`).

## 1. Problem (instrumented, frozen evidence)

K1 = 1,062/1,102 (96.37%): `progF==PASS` — the program's own verdict on the
verdict-producing span (sense_r24.zag: `progF=res_str(r)`).
K2 = 824/1,102 (74.77%): `final_prog==0` — post-deliberation PASS, the gate's
actual input (DIAG_REPORT_R24_RK3.txt labels this `prog==PASS`; the harness
reads post-deliberation inputs per DEEP_DIVE_METHOD §1b).

The 255 undelivered-but-present trials (`progF==PASS`, `final_prog!=0`,
correct, conf≥700) decompose as:
- 251: `prog=UNRESOLVED` — the (g) disjoint-span check withheld them
  (`agree`/`strong` not both 1; gcheck.zag `self_result_of`).
- 2: deliberation downgraded `prog==PASS` → `final_prog==2` (seq 2366, 2372).
- 2: `prog=FAIL` (strong disjoint-span disagreement, `contra==1`).

By (`agree`,`strong`) on the 255: (1,0):128, (0,0):123, (1,1):2, (0,1):2.

Safety boundary (frozen): 677 WRONG high-conf percepts have `progF==PASS`
but `prog!=PASS`. A naive "deliver progF" repair admits them and destroys
RK-2 (currently 0/1,109 wrong high-conf permanent installs). The (g) check
is load-bearing; it is NOT bypassed.

## 2. Repair design (frozen)

A **Delivery Adjudicator** (pure Zag) sits in the delivery path between sense
emission and gate input. It does not modify the sense (gcheck.zag untouched)
or the gate's install rules (memgate.zag logic frozen). It:

1. **Parses the disjoint-span evidence declarations** — (`progF`, `agree`,
   `strong`, `mrgF`, `conf`) from the sense emission. (On frozen evidence:
   sweep.jsonl fields, the parsed form of the `program=` text bound by
   `phash`, which the frozen gate never parses — AUTOPSY_R2-4 §3 row 2.)
2. **Admits** a percept to the gate's install logic iff:
   - `prog == PASS` (the (g) check passed; unchanged), OR
   - `progF == PASS AND agree == 1 AND conf >= 700`
     (program's verdict is PASS, the disjoint-span evidence AGREES, high
     confidence). The `conf` bar is load-bearing: without it the
     (`agree==1`) expansion admits 4 wrong percepts (all conf<700); with it,
     128 correct / 0 wrong on frozen evidence.
3. **Surfaces the escrow** — the admitted percept carries the full evidence
   declaration (`progF`, `agree`, `strong`, `mrgF`, `conf`) to the gate, not
   just the lossy ternary. (SYNTHESIS_V2 §3: escrow preserves but does not
   deliver; surfacing is the repair.)
4. **Wires parsed confidence into admission** — `conf` (parsed at
   memgate.zag:251, never used in any rule — AUTOPSY_R2-4 §1.1) gates the
   agreement-expansion path.

What it does NOT do (adopted bans):
- No judgment-side channel (judgment-channel ban ADOPTED as written): it
  moves the real judgment (`progF`) with its real evidence (`agree`), never
  a deterministic transform of the judgment.
- No pointwise adjudication (trial-1145 rule): it never compares challenger
  vs incumbent evidence and never revises a permanent. Admission only.
- No override of strong disagreement: (`agree==0`) and (`contra==1`) cases
  stay withheld. RK-5 (99.4%) and RK-2 (0%) are preserved by construction.

## 3. Measurement protocol (frozen)

- **Input:** frozen `sweep.jsonl` (11,840 rows). Python glue derives a
  pipe-delimited case file (glue is never the instrument):
  `seq|tcode|prog|progF|agree|strong|conf|mrgF|jcode|pred|measure|truth`
  (`truth` carried for scoring only, never read by the gate logic).
- **K1:** unchanged from the frozen harness: `progF==PASS` on the RK-3
  denominator (correct, conf≥700) = 1,062/1,102.
- **K2':** fraction of the RK-3 denominator admitted by §2 rule.
- **RK-3':** admitted correct-highconf percepts installed by the FROZEN
  gate rules (memgate.zag logic re-implemented in the Zag build: permanent /
  provisional slots, 256-entry negative table per task, `tol_of` per tcode;
  fidelity proven by 0/11,840 disposition mismatches vs frozen
  `gate_dispositions.txt` before the repair is enabled).
- **Determinism:** 3 runs, byte-identical (sha256 of all outputs match).
- **Zero RNG.** Pure Zag for the instrument.

## 4. Kill bars (R3-1 KB-O1, verbatim)

- **KB-O1a:** KILL if K2' does not rise to within 2pp of K1
  (K1 = 96.37%, so K2' ≥ 94.37%, i.e. ≥ 1,040/1,102).
- **KB-O1b:** KILL if RK-3' does not rise by at least half the closed
  delivery gap: RK-3' ≥ 9.44% + (K2' − 74.77%)/2.
  (RK-3 frozen = 104/1,102 = 9.44%.)
- **Both must pass.** Safety side-bars (reported, not kill): RK-1 and RK-2
  must not regress (frozen: RK-1 0 false permanents on this evidence per
  autopsy §2.2; RK-2 0/1,109).

## 5. Pre-registered expectation (not a bar)

Instrumentation predicts K2' = 954/1,102 = 86.57% (824 + 128 (`agree==1`)
+ 2 (downgrades)). This is 9.8pp short of KB-O1a. The repair is built and
measured honestly; if the bars fail, the verdict is KILL with the residual
named (the remaining gap is the (g) check's no-agreement verdicts, which
cannot be overridden without admitting 364 wrong high-conf percepts —
a sense-calibration/program-knowledge problem, prereg (f), not a delivery
problem).

## 6. Commit map

- This prereg: `docs/lab/senses/pam-rebuild/round2/o1_delivery/PREREG_O1_DELIVERY.md`
  (committed ALONE — no src, no evidence).
- Build output (later, separate commit):
  `docs/lab/senses/pam-rebuild/round2/o1_delivery/`: `src/` (pure Zag),
  `evidence/` (case file + run outputs + digests), `VERDICT_O1_DELIVERY.md`.
- No binaries, no `.zagd`. Via `~/workspace/commit_racefree.py`,
  TMPDIR=`~/workspace/tmp_commit`.

**Laws:** pure Zag, zero RNG in any decision path, byte-identical reruns,
plain language, max-risk posture.
