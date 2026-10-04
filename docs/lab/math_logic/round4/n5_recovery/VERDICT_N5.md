# VERDICT — MATH R4 ENGINE N5 (CHAIN-NATIVE)

**Status: SEALED-BATTERY RECOVERY.** The original N5 crew finished its run scripts
but its coordinator record closed before a verdict was extracted, and its run
evidence was found to be protocol-invalid (see §6). This verdict is written by
an independent recovery agent that rebuilt N5 from the frozen source and re-ran
the complete sealed battery per the frozen prereg. All numbers below are from
the recovery run unless marked otherwise.

**Round question:** n3's machinery worked but died on budget. N5 is the
n3-lineage scale-up: better thread prioritization + lemma caching, genuinely
native (byte spans only, no NL→schema translation).

**Decision rule (frozen prereg §6):** the R3 verdict (DUAL wins) STANDS unless a
native wins ≥3/4 primary bars against BOTH DUAL-R1 and REF-FIRST AND passes the
§7.3 paraphrase hard gate.

## 1. Protocol (recovery run)

- Binary: rebuilt from `n5.zag` (frozen source, committed with this verdict)
  with the pinned toolchain `znc_linux_x86_64_abed8aa1`; rebuild is
  byte-identical to the crew's binary (SHA-256 both:
  `c13243cb7834fb4c044143277b33ba65fa7ee975a20739cd2359f92c6205a219`).
- Knowledge store: the R4 wording
  (`math_logic/round4/batteries/knowledge/KNOWLEDGE_STORE_NL.md`, SHA-256
  `e8846333ff4a97a4224d6d262aef1cb021ea09e24b39cb1ecbfb4692f49c3c1d`) —
  the same store N6 used, per prereg §2.
- 3× byte-identical reruns per problem (cmp-verified, zero mismatches across
  all 549 output files), clean cache snapshot per run, pure Zag, zero RNG.
- Timeout: 180 s per run for para/PB1/PB2/PB4/CHAIN50; PB3 (B5X-NL) problems
  that timed out at 180 s were re-run at 600 s per run (B5X_NL_L2_15, L3_05,
  L4_05 each needed ~3–5 min with the full R4 store loaded). No verdict in
  this report is a timeout artifact — every problem completed all 3 runs.
- R4 batteries verified independently first: `verify_battery.py` — ALL CHECKS PASS.

## 2. Paraphrase hard gate (§7.3) — runs BEFORE bar scoring

All 12 canonical/paraphrase/nonce triples returned WITHHELD on all three
members — no verdict flip anywhere.

| Pair | canon | paraphrase | nonce | stable |
|---|---|---|---|---|
| PARA_PAIR_01 | WITHHELD | WITHHELD | WITHHELD | yes |
| PARA_PAIR_02 | WITHHELD | WITHHELD | WITHHELD | yes |
| PARA_PAIR_03 | WITHHELD | WITHHELD | WITHHELD | yes |
| PARA_PAIR_04 | WITHHELD | WITHHELD | WITHHELD | yes |
| PARA_PAIR_05 | WITHHELD | WITHHELD | WITHHELD | yes |
| PARA_PAIR_06 | WITHHELD | WITHHELD | WITHHELD | yes |
| PARA_PAIR_07 | WITHHELD | WITHHELD | WITHHELD | yes |
| PARA_PAIR_08 | WITHHELD | WITHHELD | WITHHELD | yes |
| PARA_PAIR_09 | WITHHELD | WITHHELD | WITHHELD | yes |
| PARA_PAIR_10 | WITHHELD | WITHHELD | WITHHELD | yes |
| PARA_PAIR_11 | WITHHELD | WITHHELD | WITHHELD | yes |
| PARA_PAIR_12 | WITHHELD | WITHHELD | WITHHELD | yes |

**GATE: PASS** (no flips; stability is vacuous — N5 withholds on every gate item).

## 3. Primary bars

| Bar | Result | Bar | Cleared |
|---|---|---|---|
| PB1 R3N ≥12/24 + honest traces | 10/24 correct, fd=0, fw=5 | ≥12/24 | MISS |
| PB2 NL-twins ≥80% of DUAL-R1's 37/37 formal | 33/37 correct, fd=0, fw=4 | ≥30/37 | CLEAR |
| PB3 B5X-NL ≥45/60, <10 fd, <10 fw | 42/60, fd=14, fw=4 | all three | MISS |
| PB4 CHAIN-NL ≥12/20 + honest step traces | 0/20 correct | ≥12/20 | MISS |

**N5 clears 1/4 primary bars.**

Detail:
- PB1: 10 correct; 5 false-withheld; 9 engine errors (rc=-2, exit 4) on
  R3N_09/11/13/16/18/19/20/22/23 — all 9 are sealed-DERIVED, counted as misses.
  Zero false derivations.
- PB2 misses (all false-withheld): T4_03, T4_11, T4_12, T4_13.
- PB3 false-derived (14): L2_04, L2_09, L2_10, L2_14, L2_19, L2_20, L3_04,
  L3_09, L3_10, L3_19, L3_20, L4_04, L4_09, L4_19.
  PB3 false-withheld (4): L2_08, L2_18, L4_06, L4_16.
- PB4: all 20 WITHHELD. Bar misses before trace honesty is even reached.

## 4. Hypotheses touching N5

- H-NATIVE-R4 (some native wins ≥3/4 bars vs both controls): N5 contributes
  1/4 — does not move the hypothesis.
- H-CHAIN (some native completes ≥1 CHAIN50-NL with correct verdict + honest
  step trace): **HOLDS for N5 — 6/6 derived**, depths 56–72, every step a
  byte-cited ledger append (see §5).
- H-DISC-NATIVE (≥45/60, <10 fd, <10 fw on B5X-NL): **REJECTED for N5**
  (42/60, 14 false derivations).
- H-PARAPHRASE (round's best native passes §7.3 gate): gate passes for N5,
  but on all-withheld stability — a pass with no discriminative content.

## 5. Mechanism-level story

N5 is a byte-span forward chainer with thread prioritization and lemma caching.
Its ceiling is visible in all four bars at once:

**What works — pure forward chains.** CHAIN50-NL (6/6) is N5's home turf: each
problem is a long explicit conditional chain (R1→R2→…→R64) and N5 walks it
with lemma-apply steps, each grounded in a byte span of the problem text
(e.g. CHAIN50_NL_01: S283 "the tally after night 64 stands at 64.",
depth=64, derived R63 via lemma-apply p=[120,281,-1]). The traces are honest
causal chains — no numeric-blind shortcuts, every step cites prior states.
PB2 (33/37) works the same way: the NL twins are short chains whose
antecedents match by word inclusion.

**What breaks — anything needing arithmetic or contradiction use.**
PB4 (0/20): CHAIN_NL problems need symbolic substitution N5 cannot do
(e.g. CHAIN_NL_01: from "n is even" prove "16 divides n^4" — requires
n=2k ⇒ n^4=16k^4; N5's FORWARD thread proposes 25 states, GOAL proposes 1,
never bridges). PB1's 9 engine errors (rc=-2) are the same ceiling expressed
as a crash: problems whose proof shape needs discharge/arithmetic the
substrate cannot represent.

**What breaks — discrimination of injected falsehoods.** PB3's 14 false
derivations are the signature failure. Example B5X_NL_L2_04 (sealed WITHHELD,
N5 DERIVED): the injected store contains K1013 "If 5 letters are delivered to
5 mailboxes, then some mailbox received at least 2 letters." N5's antecedent
matcher is word-inclusion — S1 "5 letters were delivered, one to each of 5
mailboxes" matches K1013's words, so it fires (S476 "some mailbox received at
least 2 letters"), then modus ponens through K1014 reaches the goal (S477).
N5 never checks the arithmetic (5 letters / 5 mailboxes = 1 each contradicts
"at least 2") and never uses premise S2 ("Every mailbox received exactly one
letter") to kill the false branch — the CONTRA thread records a strike but
the derivation stands. Word-similar false rules sail through; N5 has no
content-level contradiction engine.

**Summary:** N5 is an honest, deterministic, genuinely native forward chainer.
It withholds rather than confabulates on paraphrases (gate passes), and it
walks long explicit chains faithfully (H-CHAIN holds). But it cannot do the
two things the round's hard bars demand: symbolic manipulation (PB1/PB4) and
discriminating word-plausible falsehoods (PB3). 1/4 bars. The R3 verdict
(DUAL wins) stands for N5.

## 6. Provenance note (why this is a recovery, not the crew's numbers)

The N5 crew's own runs (`~/workspace/n5_certified/`, 2026-09-25 19:26–19:52 UTC)
are DISCARDED as evidence, for two independent protocol violations:

1. **Wrong knowledge store.** The crew passed the R3 store path
   (`math_logic/round3/batteries/knowledge/KNOWLEDGE_STORE_NL.md`) although
   prereg §2 freezes the R4 wording for all engines.
2. **The store file it read was corrupted mid-run.** At 2026-09-25 19:25:32 UTC
   — one minute before the crew's certified para runs began — that file was
   overwritten with an n3 engine trace (25 lines, `ID: T4_12 ENGINE: n3`),
   replacing the real store. Every certified crew run (19:26–19:52) ingested
   zero knowledge-store items. The crew's published claims (BUILD_N5.md:
   PB2 32/37 PASS, H-CHAIN 6/6) have no surviving evidence and were produced
   under this corruption; they are not trusted and are superseded by this
   recovery run.

The crew's battery outputs are preserved in the workspace for audit but are
not cited as evidence.

## 7. Evidence committed with this verdict

- `runs/` — all 3× rerun outputs per problem (byte-identical, cmp-verified)
- `run_all.sh`, `run_pb3_slow.sh` — the recovery runners
- `score.py` — the scorer
- `SCORES.txt` — full per-problem verdict table
- `RUNLOG.txt`, `RUNLOG_PB3SLOW.txt` — run logs with binary + knowledge SHAs
- `n5.zag` — frozen engine source (build: `znc_linux_x86_64_abed8aa1 n5.zag -o n5_bin`)
