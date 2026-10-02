# Substrate Synergy: Result

## Verdict: SYNERGY-TESTED

Both preregistered synergy directions show a positive cross-mechanism
effect. All frozen kill bars hold.

## Frozen bars (from PREREG_SUBSTRATE_SYN.md)

- K1: at least 2 synergy directions with measurable predictions. Two
  directions were specified and both were tested.
- K2: B performs better with A's output than without. P1: N_concept=3
  < N_raw=23. P2: acc_revise=168/200 > acc_frozen=136/200. Both hold.
- K3: pure Zag, no Python, no em dashes, 3/3 deterministic. All hold:
  3 runs byte-identical (md5 30a79412f090f86fdf42c882ac220897),
  exit 0, zero stderr, zero non-ASCII bytes, zero Python invocations.

## Preregistration

- Original prereg: 87042feb2.
- Amendment 1 (c3 noise fix): 0e381f1b7.
- Amendment 2 (noise calibration p=0.02): ebc7abc4e.
- All amendments strictly precede implementation. Kill bars and
  directional predictions were never altered.

## Synergy 1: concept to procedure (P1)

World W1: 4-cycle of concepts (c0-c3), 2 morphemes each, signal p=0.98,
noise p=0.02. One episode = 5 bigrams. ACTIVE threshold = count >= 3.

- COND-CONCEPT (16 concept bigram counters): exact gold set identified
  at episode 3. F1 stabilizes at 888 (one noise pair crosses the
  threshold by episode 10 and persists; the other 15 cells stay clean).
- COND-RAW (64 morpheme bigram counters): exact gold set identified
  at episode 23. F1 reaches 1000 by episode 40.
- P1 holds: 3 < 23. Concepts concentrate counts 4x, so the signal
  crosses the threshold much sooner.

Honest note: the exact-set metric is a "first hit" measure. CONCEPT
hits it at ep 3 but a single noise pair later intrudes (F1 888, not
1000). The directional advantage is robust (3 vs 23), but the
representation does not permanently suppress all noise.

## Synergy 2: contradiction to revision (P2)

Phase A (30 W1 episodes): 4 procedures formed, exactly matching the
gold set {(c0,c1),(c1,c2),(c2,c3),(c3,c0)}. Phase-A calibration check
passes.

Phase B (40 W2 episodes, c0 row changed to c0->c2 p=0.8):
- COND-REVISE (contradiction detector + revision): 168/200 correct.
  First revision at episode 38. The c0->c1 procedure was rolled back
  and replaced with c0->c2.
- COND-FROZEN (Phase-A procedures, no revision): 136/200 correct.
- P2 holds: 168 > 136. The contradiction signal (+32 correct)
  improves the procedure store.

The substrate holds the procedures, statuses, contradiction counts,
and bigram facts. Prediction uses a Zag-side index mirroring the
substrate procedure facts (to avoid redundant string interning in the
hot loop); the index was verified against substrate statuses after
Phase B with zero mismatches.

## Capacity and limitations

- Fact counts: Wc=256, Wr=256, Wv=256, Wf=180. Three workspaces hit
  the 256-fact capacity cap. All key measurements (convergence at
  episodes 3 and 23, F1 at 10/20/40, revision at episode 38) occur
  before saturation; the contradiction detector uses pre-generated
  sequences and the cache for late Phase-B predictions. A longer run
  would need a larger substrate or fact garbage collection.
- The concept mapping, ACTIVE threshold, contradiction threshold
  (half expected), and revision policy (2 consecutive windows,
  strongest alternate >= 3) are researcher-authored. The claim is
  comparative cross-mechanism utility (B works better with A's output),
  not L3 invention of the mechanisms themselves.
- Synergy 1 uses a "first exact identification" metric; see the honest
  note above about noise intrusion.

## Determinism

- 3/3 runs byte-identical.
- md5: 30a79412f090f86fdf42c882ac220897.
- Exit 0, zero stderr bytes, zero non-ASCII bytes.
- Pure Zag: the toolchain compiled and ran substrate_syn.zag with no
  Python at any stage.

## Commits

- Prereg (original): 87042feb2
- Prereg amendment 1: 0e381f1b7
- Prereg amendment 2: ebc7abc4e
- Implementation + result: (this commit)
