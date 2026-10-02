# REPORT_TRADES_DAG: Non-Chain DAG Generality (Queue Item 8)

Lane TRADES, wave wave-20261002-1121pdt. 2026-10-02.

## Verdict: BUILD-PASS (with one disclosed limitation)

The CAUSAL-DAG mechanism generalizes beyond chains: **10/10 on non-chain
sealed worlds, every win a unique-survivor verdict**, and the chain-only
ablation scores 0/10 on those worlds. All frozen kill bars pass. One chain
control world is missed due to a proven observational equivalence
(collider covers chain under the existential-b pruning semantics); disclosed
below, not hidden.

## Numbers

Sealed battery: 12 worlds (2001..2012) x (WIDE x3, F_CM x1, SINGLE x1) = 60
runs, pure Zag, byte-identical reruns.

| world | structure | WIDE (x3) | F_CM | SINGLE |
|---|---|---|---|---|
| 2001 | fork X | 1000,1000,1000 | 1000 | 1000 |
| 2002 | fork Y | 1000,1000,1000 | 1000 | 1000 |
| 2003 | fork Z | 1000,1000,1000 | 1000 | 1000 |
| 2004 | collider X | 1000,1000,1000 | 1000 | 1000 |
| 2005 | collider Y | 1000,1000,1000 | 1000 | 1000 |
| 2006 | collider Z | 1000,1000,1000 | 1000 | 0 |
| 2007 | diamond | 1000,1000,1000 | 1000 | 0 |
| 2008 | diamond | 1000,1000,1000 | 1000 | 0 |
| 2009 | diamond | 1000,1000,1000 | 1000 | 1000 |
| 2010 | diamond | 1000,1000,1000 | 1000 | 0 |
| 2011 | chain (control) | 1000,1000,1000 | 1000 | 1000 |
| 2012 | chain (control) | 0,0,0 | 0 | 0 |

Totals: WIDE 11/12, F_CM 11/12, SINGLE 6/12.
Non-chain (2001..2010): WIDE 10/10, F_CM 10/10, SINGLE 6/10.

Every non-chain WIDE win: final Hn=1 (unique survivor), survivor index is the
true DAG (forks 0/1/2, colliders 3/4/5, diamonds 2/5/8/11), zero chain indices
in any survivor list. No tie-break involved in any non-chain PASS.

## Kill-bar scorecard (frozen in PREREG_TRADES_DAG.md, commit 3415c217f)

- K1 (WIDE >= 10/12): 11/12. PASS.
- K2 (WIDE minus SINGLE >= 2): 11 - 6 = 5. PASS.
- K3 (WIDE >= F_CM): 11 >= 11. PASS.
- K4 (aggregate sim ratio in [8,12]): 70222/7180 = 9.78. PASS. Structural
  30 pooled EIG searches vs 3 single. Per-world WIDE/SINGLE ratios 7.3..12.3.
- K5 (3/3 byte-identical): PASS on all 12 worlds (stripped replies + traces).
- K6 (battery byte-identical to INQ sealed run): PASS (131 turns).
- K7 (sealed validity): PASS. Worlds regenerate byte-identically; agent
  source has zero seed hits, zero edge-list constants, zero key.json opens;
  key.json chmod 000 during runs.
- K8 (pure Zag): PASS. Only safebin znc + bash/awk/grep/sed/sha256sum for
  sequencing. `which python3` resolves to nothing.
- K9 (architecture): module 146 -> 371 lines (+225 net, +373 added); zero
  new modes, bridges, handlers, turn kinds, or semantic cases. PASS.
- K10 (no L3): the 12/36 hypothesis spaces are researcher-enumerated; the
  forward model is researcher-supplied. L2 structural use at most. PASS.
- K11 (generality): WIDE 10/10 on non-chain worlds, all unique-survivor
  (Hn=1), chain-only ablation 0/10 on non-chain (2/2 on chain controls).
  PASS.

BUILD-PASS requires K1, K2, K4, K5, K6, K8, K11: all PASS.
K3, K7, K9, K10: all PASS.

## Red team

- R1 (exact-match audit): scorer uses byte-exact streq (length + per-byte).
  No normalization. A chain string cannot equal a DAG string. PASS.
- R2 (unique-survivor audit): all 10 non-chain WIDE passes have Hn=1 with
  the survivor index equal to the true DAG. PASS.
- R3 (DAG-evidence audit): zero chain indices (6..11 for 3-var, 12..35 for
  4-var) appear in any non-chain survivor list. The verdicts are
  DAG-structured edge lists that no chain-restricted reasoner can produce
  (the ablation proves this empirically). PASS.
- R4 (chain-only ablation): CAU_DAG=0 scores 0/10 on non-chain worlds, 2/2
  on chain controls. The DAG hypotheses are load-bearing. The ablation
  converges to a unique but wrong chain on DAG worlds (e.g. "X->Y,Y->Z"
  for forks), confirming the worlds are genuinely non-chain. PASS.

## The 2012 miss (disclosed limitation, not a generality failure)

World 2012 (chain Z->Y->X) ends Hn=2, tied between collider (Y->X,Z->X) and
the true chain (Y->X,Z->Y); the lexicographic tie-break picks the collider.
This is a PROVEN observational equivalence under the frozen forward-model
semantics, not a fluke:

- do(X=v): both predict (v,b,b). Identical.
- do(Y=v): both predict (v,v,b). Identical.
- do(Z=v): chain predicts (v,v,v); collider predicts (v,b,v), which matches
  with b=v. The collider can never be ruled out.

The collider has fewer descendants, so more free variables under the
existential-b pruning rule, so it "covers" the chain. The same tie (resolved
correctly by luck of the tie-break) occurs on 2011. TRADES-1 did not have
this blind spot because its hypothesis space was chain-only.

Consequences: (1) on chain worlds the DAG-expanded mechanism ties and defers
to an arbitrary tie-break; (2) the chain-only ablation actually gets 2012
right, so expanding the space cost 1 point on chains while gaining 10/10 on
DAGs. Net strongly positive, but the trade-off is real. A finer forward
model (e.g. per-variable independent noise instead of one shared b, or a
pruning rule that penalizes existential flexibility) might distinguish them;
that is future work, not this lane.

## Advocate / skeptic / judge

Advocate: 10/10 on non-chain worlds with unique-survivor verdicts, ablation
0/10, all bars pass. The mechanism demonstrably uses DAG structure: it rules
out all 6/24 chain hypotheses on every DAG world and names the exact
branching edge list. This is generality beyond chains.

Skeptic: the hypothesis spaces are researcher-enumerated (12/36), the
forward model is researcher-supplied, and the 2012 tie exposes a semantic
coarseness. This is L2 structural use, not invention. The EIG machinery adds
nothing over cyclic choice here (F_CM also 11/12); the gain is all from
10-trace pooling, same as TRADES-1.

Judge: the skeptic is right that this is L2, not L3 (already disclaimed in
K10), and right that EIG vs cyclic is a wash (K3 is non-inferiority, met).
But the advocate's core claim stands: the mechanism identifies non-chain
DAG structure it was not restricted to, with evidence-driven unique-survivor
verdicts, and the ablation proves the DAG hypotheses do the work. The 2012
limitation is understood and bounded. BUILD-PASS.

## Provenance and commit ids

- Prereg: 3415c217f (frozen before implementation; commit-order self-check
  PASS: prereg strictly precedes implementation).
- Implementation: dc8ad565a. Source sha256 identical before/after copy
  (dag_world 8d499d01, dag_contestant 60940026, dag_score bd687c2c,
  run_dag 5386c01e). Committed binaries build byte-identically.
- Sealed worlds: 69abcf3ed (12 worlds, seeds 2001..2012).
- Safebin: 36 tools; `which python3` -> nothing; `which znc` ->
  /home/hatch/safebin/znc.

## Queued next

1. The collider-covers-chain observational equivalence (2012) is a crisp,
   minimal case for testing a finer forward model. A follow-up lane could
   preregister a per-variable-noise variant and test whether it breaks the
   tie without losing the 10/10 DAG score.
2. The tie-break is arbitrary; a follow-up could preregister a
   structure-neutral tie-break (or report ties as abstentions) and measure
   the calibration change.
3. 5+ variable DAGs (larger hypothesis spaces) to probe scaling of the
   enumeration approach.
