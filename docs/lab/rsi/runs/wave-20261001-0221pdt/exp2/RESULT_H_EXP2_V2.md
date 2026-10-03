# H-EXP2 v2 sealed result (wave-20261001-0221pdt)

## Provenance

- Frozen prereg: `docs/lab/rsi/runs/wave-20260930-1121pdt/exp2/PREREG_H_EXP2_V2.md`
  (committed in wave-20260930-1121pdt; bar-text audit this wave at
  `docs/lab/rsi/runs/wave-20261001-0221pdt/exp2/BAR_TEXT_AUDIT.md`,
  precondition satisfied).
- Commit-order self-check: prereg first commit (1121pdt wave) strictly
  precedes this wave's implementation commit. PASS.
- Implementation (this wave): `expworld.zag` (sealed true world),
  `expseq.zag` (learner), `run_exp2.sh` (orchestration).
- Sealed laws (1121pdt, read only by expworld): W-A = (A=2,B=3),
  W-B = (A=2,B=1).

## Toolchain note

The first build used `[]i32` via `as *i32` slice construction inside
functions. Sealed runs failed: element reads returned 0, breaking
state parsing. This is the pinned-znc miscompile recorded in workspace
AGENTS.md ("Never use `as *i32` + `q[0..n]` slice construction inside
functions"). Both programs were rewritten to the mandatory workaround:
u8-backed cells with little-endian get32/set32 helpers. After the
rewrite the W-A and W-B sealed loops ran to completion. No frozen bar
changed; the rewrite is implementation repair only.

## Sealed evidence

W-A law (2,3). Log sha256:
c9dbe0958ce38c09ab39ad7d0436dd447bcb2d1acda6d4a318c008e8dc1ad721

Round 1: SURVIVORS 16 -> PROBE 4 [2 0 3 2] SCORE 4
Round 2: SURVIVORS 10 -> PROBE 3 [0 3 2] SCORE 2
Round 3: SURVIVORS 2  -> PROBE 2 [4 2] SCORE 2
Round 4: SURVIVORS 1  -> IDENTIFIED 2 3

W-B law (2,1). Log sha256:
3c4c672551f28f20fc49936d28bc559e9c21bd278e9b1cc6ece00fe697c295e4

Round 1: SURVIVORS 16 -> PROBE 4 [2 0 3 2] SCORE 4
Round 2: SURVIVORS 10 -> PROBE 3 [0 3 2] SCORE 2
Round 3: SURVIVORS 8  -> PROBE 3 [3 4 2] SCORE 2
Round 4: SURVIVORS 2  -> PROBE 2 [1 2] SCORE 2
Round 5: SURVIVORS 1  -> IDENTIFIED 2 1

Each round executed exactly one probe; CANDIDATES 1554 printed every
enumeration round (6+36+216+1296 = 1554; the prereg's "(1654 probes)"
is an arithmetic erratum, documented in the bar-text audit; no bar
references 1654).

## Bar verdicts (K-X1..K-X6, PREREG_H_EXP2_V2.md section 6)

- K-X1: PASS. IDENTIFIED 2 3 at round 4 (3 probes executed, within 6);
  pair equals the sealed W-A law; no BUDGET-EXHAUSTED, STALLED, or
  INCONSISTENT line.
- K-X2: PASS. IDENTIFIED 2 1 at round 5 (4 probes executed, within 10);
  pair equals the sealed W-B law; no failure markers.
- K-X3: PASS. W-B IDENTIFIED at round 5 (>= 3); survivor counts
  16 -> 10 -> 8 -> 2 -> 1 are strictly decreasing in rounds 2, 3, 4
  (>= 2 distinct rounds).
- K-X4: PASS. `cmp` of the two per-world round logs is byte-identical
  for both W-A and W-B (zero stderr in both sealed runs).
- K-X5: PASS. Grep audit 2026-10-01: `expseq.zag` contains no occurrence
  of any law file name or path (the word "law" was also removed from
  its comments for airtightness); its only `_zag_read_file` sites are
  the history file and the state file (argv positions 1, 2). Only
  `expworld` opens the law file.
- K-X6: PASS. Executed probe scores: W-A (4, 2, 2); W-B (4, 2, 2, 2);
  all >= 2.

## Verdict

**BUILD-PASS.** H-EXP2 v2 satisfies all six frozen kill bars.
Per the prereg's honest-boundaries section this is a bounded L2
(active experiment construction) sustained across both sealed worlds,
NOT L3: the hypothesis family (16 pairs), the shared action dynamics,
and the enumeration scheme are researcher-authored, and the probe
policy was designed before seeing either sealed world.

## Red-team second opinion (coordinator, inline)

1. Gaming the probe policy to the two sealed worlds? The policy is
   fully generic (distinct-trajectory scoring over the surviving set
   with a fixed tie-break); the laws were sealed in 1121pdt before the
   implementation existed; K-X5 shows no leak path. The two worlds
   elicit different probe sequences driven by pruning, not by design.
2. Task too easy? W-A closes in 3 probes, W-B in 4, well under budget.
   But K-X3 (round >= 3 with >= 2 strictly decreasing rounds) was the
   anti-one-shot bar, and W-B meets it with a genuine multi-round
   setup: round 3's [lamp_on, pressurize] configures l then tests the
   B=1 vs B=2 distinction that round 4's [cool, pressurize] resolves.
   The mechanism is doing sustained discrimination, not luck.
3. Overclaim risk: contained by the prereg's own bounded-L2 framing;
   no L3 language appears in this result. Transfer, OOD, ablation, and
   red-team steps remain queued in the pipeline.
4. Contamination: the `[]i32` miscompile was an implementation defect,
   caught by sealed execution, repaired via the documented toolchain
   workaround, with both worlds re-run from scratch on the repaired
   binaries. No bar was touched.

Recommended next pipeline step: step 6 alternative-explanation attack
(memorization/table-lookup confound), then step 7 OOD.
