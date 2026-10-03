# REPORT: L2-INTERFERENCE clean restart

Date: 2026-10-02. Worker: L2-INTERFERENCE clean-restart worker.
Prereg: committed alone as 79ff6d6ad (strictly before implementation).
Implementation: l2_interference.zag (pure Zag), built with the pinned
compiler src/tools/toolchain/znc_linux_x86_64_abed8aa1, exit 0, no
warnings on the final build.

## Verdict: PASS

All frozen kill bars hold. 3/3 runs byte-identical
(sha256 32d4374ccea33d07494e0cfe76eee012c5b8a942a49998157570966b3931c9c2).

## Results (identical across run1/run2/run3)

| condition        | pre | post | ret | conflicts | evict | bacc |
|------------------|-----|------|-----|-----------|-------|------|
| NULL multi       | 35  | 35   | 100 | 0         | 0     | 20   |
| PARTIAL multi    | 35  | 35   | 100 | 5         | 0     | 20   |
| FULL multi       | 35  | 12   | 34  | 20        | 12    | 20   |
| PARTIAL single   | 10  | 10   | 100 | 5         | 0     | 20   |

Kill bars:
- K1 BASELINE: pre=[35,35,35,10], need=[35,35,35,10] -> PASS
- K2 MAIN: partial multi ret=100, bar>=90 -> PASS
- K3 NULL: ret=100, bar==100 -> PASS
- K4 SENSITIVITY: full ret=34, bar<=75 -> PASS
- K5 DETERMINISM: 3/3 byte-identical sha256 -> PASS
- K6 ABLATION: single partial ret=100, |100-100|=0 <= 10 -> PASS

## What was tested

The learner holds four L2-adapted structures in one shared
content-addressed memory: A_BASE (taught), A_EXT (EXTEND, third hop),
A_SPEC (SPECIALIZE, examples 1..5 plus guard entries), A_TRUNC
(TRUNCATE, hop 1). Structure B is interface-adapted from a generic
2-hop template; its interface map controls key overlap with A (0, 25,
or 100 percent). Overlapping keys are written with different values,
i.e. value SUBSTITUTIONs on shared content keys. The mechanism under
test is conflict-relocation: a conflicting write moves the evicted
entry into a finite circular overflow pool (8 slots) instead of
destroying it; reads are owner-scoped so each structure finds its own
entries.

## Reading of the results

- With no overlap, retention is exactly 100 percent: co-resident
  adapted structures do not disturb each other through the shared store
  (K3). Same-key same-value writes from EXTEND/SPECIALIZE/TRUNCATE merge
  owner bits without conflict, as designed.
- With 25 percent overlap (5 conflicting keys), all 5 conflicts are
  relocated and retention stays at 100 percent, both with siblings
  present and in the single-structure ablation (K2, K6). The relocation
  policy absorbs moderate interference.
- With 100 percent overlap (20 conflicts against an 8-slot pool), 12
  relocations are evicted and retention falls to 34 percent (12/35:
  A_BASE 4/10, A_EXT 4/10, A_SPEC 0/5, A_TRUNC 4/10), exactly the
  predicted saturation behavior. B itself is fully learned in every
  condition (bacc=20/20): the damage is one-sided, the classic
  interference asymmetry (K4 sensitivity confirmed, so the PASS on K2/K3
  is not vacuous).
- The ablation shows interference is a property of shared content, not
  of structure count: single vs multi retention differs by 0 points.

## Honest caveats

- The substrate is deliberately simple: queries are keyed lookups, not
  true chained execution, and reads are owner-scoped, which assumes the
  learner knows which structure it is executing. The result is a
  mechanism check on conflict-relocation in shared memory, not a claim
  about label-free routing in a full continuing learner.
- Interference magnitude is set by construction (overlap fraction vs
  pool size). The non-trivial content is that the policy boundary falls
  exactly where predicted (34 percent vs the <= 75 percent bar) and that
  moderate overlap is fully absorbed with zero evictions.
- No sealed worlds were used; none were needed for this mechanism test.
  No sealed-world contents were inspected.

## Toolchain guard

Safebin active for the whole lane; `which python3` and `which python`
returned nothing at startup and no forbidden executable was invoked at
any point (shell used only for mkdir, git, znc, binary execution,
sha256sum, and file reads/writes). No PROCESS-FAIL condition triggered.

## Commits

- 79ff6d6ad: frozen prereg (PREREG.md + NAMECHECK.md Step 0), alone.
- This commit: l2_interference.zag, l2_interference_bin, run1/2/3.txt,
  REPORT.md. Local only, never pushed.
