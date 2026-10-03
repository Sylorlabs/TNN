# PREREG AMENDMENT 3 (post-implementation, pre-verdict)

Amends PREREG.md (frozen cb8545cb4) + AMENDMENTS 1-2. Reason: worksheet
slip found by running the implementation and diffing a per-entry
S-trace against the hand derivation.

1. DECOY-ENTRY DISCOVERY (section 4): the worksheet priced the decoy
   entry candidate (50,17,64) [fid 22] as FAIL-DISC2 (s2scan miss,
   cost 25+55=80). WRONG: fact 25 is (74,16,65), i.e. sub==74 with
   rel 16 != valrel, so scan_nv(74) HITS fid 25 (cost 26),
   discovering s2=16, b=65. The candidate then walks and fails on
   TERMINAL, not discovery:
   - Trial nf=2, fid 22: 25 + 26 + walk(k=2: 27+28) = 106
     (was 80). FAIL-TERM at 66.
   - Trial nf=3, fid 22: 25 + 26 + walk(k=2: 27+28, k=3: 29+30)
     = 165 (was 80). FAIL-TERM at 67.
   This is a pure worksheet misread of the fact table (missed that
   fid 25 carries sub==74); the implemented mechanics (scan_nv,
   walk, terminal-first check order) are exactly as frozen, and the
   per-entry debug trace confirms the new atom costs. No algorithmic
   change.
   Corrected frozen trial costs: nf=2 trial = 903 (was 877);
   nf=3 trial = 903 (was 818).
   Corrected frozen per-query S (E unchanged):
   - FULL Q2: S=2597 (was 2486), E=6.
   - GEN Q2: S=1977 (was 1866), E=4.
   - GEN Q2B: S=1977 (was 1866), E=4.
   K2 frozen inequality becomes 1977 > 669; K4 becomes 669 < 1977
   (2.95x). All other frozen numbers unchanged.

2. ABLATE RETIRE ORDER (section 4, implementation bug fix): the
   driver retired mG before QA, so ABLATE-QA failed (S=6, ANS -2)
   instead of the frozen QA 44/1. The frozen design requires QA/QB
   as the pre-ablation baseline ("QA 44/1 (as FULL)"), i.e. mG is
   retired AFTER QB and before Q2. The driver is fixed accordingly
   (no learner change; no counting-rule change). Frozen ABLATE
   numbers QA 44/1, QB 48/1, Q2 99/2 stand as written.

No kill-bar thresholds, counting rules, or algorithmic content
change. The F-COUNT falsifier did its job: it caught the slip.
