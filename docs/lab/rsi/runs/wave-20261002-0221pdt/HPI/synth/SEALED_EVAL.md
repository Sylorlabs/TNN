# SEALED_EVAL: H5R2-SYNTH sealed evaluation

Lane: HPI, wave-20261002-0221pdt. Prereg PREREG_H5R2_SYNTH.md frozen
alone at 5b2f8e0f0. All runs pure Zag, PATH=$HOME/safebin, pinned
znc. Scoring uses the drivers' own markers.

## Per-world stdout hashes (3/3 byte-identical each; SYN-DET)

- s_s1: 1766b7ffc3e158e32d2ac3f31324e9343def56c08f3ea26a6f4b5f2c606c58af
- s_s2: 1f1fb027ac0cc7deee47b248e06f960b1b2fc96ea92092a057d8f030d5cdff01
- s_d1: 968c097b66bee58471c46b2586d503b49baf9d8eeee319c2f9f1fedd97baefdc
- s_d2: 66b3aedd1a6b5ca11f0183a8d21f57fb723e71633ae03e3addf2cb347a081a39
- s_e1: 330d47f54ef0c4ec0931f2bc86094cb8f1f348fe3556dcb8392435db9761381a
- s_e2: 3a5902e5ae8044123ed08c337783d8e883745015c9e101efcbac819e159469df
- s_t1: 64aaa2d8d01a04b973abee4a125f19c060793f1e2f03f4aa3610fb6d8c22d3bd
- s_t2: 169d93753ab094175eef5080a3e732d4fdaddd4165b5308ee8b2932a2e8a17af
- h_t1: 349157ab0df38046eb6f9db2f08cd4307b7f0e647e1053d08a76d8b92587dca0
- h_t2: afa4fcda35aa166c8c4e5d78ffea9b80ca7de5d8ae560c8acdf9cae19131e287
- n_t1: 349157ab0df38046eb6f9db2f08cd4307b7f0e647e1053d08a76d8b92587dca0
- n_t2: afa4fcda35aa166c8c4e5d78ffea9b80ca7de5d8ae560c8acdf9cae19131e287

Note: n_t1 stdout is byte-identical to h_t1, and n_t2 to h_t2. The
H/N tie on the DT worlds holds at the byte level, not just at the
marker level. Zero stderr bytes on all 36 runs. SYN-DET HOLDS
(12/12 worlds 3/3 byte-identical; battery 3/3 byte-identical).

## SYN-NR-SEP (separator s1/s2, S arm)

- s_s1: 4/4 SEP-NEW, 4/4 "SEP ok", 4/4 "SEP-TWOLIVE ok", 0 SEP-OLD.
- s_s2: 4/4 SEP-NEW, 4/4 "SEP ok", 4/4 "SEP-TWOLIVE ok", 0 SEP-OLD.
- Total: 8/8 SEP-NEW. No unexpected FAIL markers.
- SYN-NR-SEP HOLDS. S agrees with N (recorded 8/8 SEP-NEW).

## SYN-NR-DECOY (decoy d1/d2, S arm)

- s_d1: 0/4 "D ok"; 4/4 D-DECOY-FAIL; 4/4 "D-ANS ok".
- s_d2: 0/4 "D ok"; 4/4 D-DECOY-FAIL; 4/4 "D-ANS ok".
- Total: 0/8 "D ok", 8/8 D-DECOY-FAIL, 8/8 D-ANS ok (worlds not
  adversarial-by-brokenness).
- Companion markers: 8/8 D-KEY-FAIL (the revert MAP anchors to the
  decoy instead of the K-live fact; expected companion of the
  decoy anchor, not an unexpected signature). No other FAIL
  markers.
- SYN-NR-DECOY FAILS (bar requires 8/8 "D ok"). This is the
  pre-registered newest-bias failure signature: the decoy fact is
  the newest live fact in every verifying candidate's licensing
  set, so S anchors every revert MAP to the decoy.

## SYN-NR-CHAIN (chained e1/e2, S arm)

- s_e1: 0/4 "CD ok"; 4/4 CD-DECOY-FAIL; 4/4 "D-ANS-A ok"; 4/4
  "D-ANS-B ok".
- s_e2: 0/4 "CD ok"; 4/4 CD-DECOY-FAIL; 4/4 "D-ANS-A ok"; 4/4
  "D-ANS-B ok".
- Total: 0/8 "CD ok", 8/8 CD-DECOY-FAIL.
- Mechanism detail (reported honestly; the prereg predicted
  decoy anchoring at both levels): the promoted candidate is
  [F_ab, decoy_b], not [decoy_a, decoy_b]. Two candidates share the
  maximum licensing id (decoy_b); the enumeration-order tie-break
  picks the first-enumerated, [F_ab, decoy_b]. Hence 8/8
  CD-DECOY-FAIL (decoy_b target) with companion 8/8 CD-KEY-FAIL
  (klive missing) and 0/8 CD-AKEY-FAIL (alive present). The bar
  outcome is as predicted; the mechanism detail refines the
  pre-registered expectation.
- SYN-NR-CHAIN FAILS (bar requires 8/8 "CD ok").

## SYN-NR-BATT (built-in battery, S arm)

- 3/3 runs byte-identical (SHA-256
  e6ac118dd318b54e22bb9bab8b87b6456cb8bfc16355cabac6a552e9b43bf82c).
- TOTAL 45/46; the single failure is t_f2 (the masked query
  promotes the later-taught 2-hop reading [F2,F4] -> 202 instead of
  201).
- SYN-NR-BATT FAILS (bar requires 46/46). This is the
  pre-registered Attack 3 regression.

## SYN-DT (discrimination trials t1/t2, all three arms)

World validity: "DT ok" on 8/8 probes on all three arms (4+4 each);
zero FAIL markers on any arm; no DT-BROKEN-FAIL (no world VOID).

- H: 8/8 DT-FIRST (4+4), 0 DT-LATER.
- N: 8/8 DT-FIRST (4+4), 0 DT-LATER.
- S: 0/8 DT-FIRST, 8/8 DT-LATER (4+4).
- The H/N tie is confirmed and byte-identical (n_t1 == h_t1,
  n_t2 == h_t2 stdout).
- SYN-DT requires S_DT-FIRST_count > max(H_DT-FIRST_count,
  N_DT-FIRST_count), i.e. 0 > 8. SYN-DT FAILS.

## Cost accounting (header field 16, last probe per world)

tried/rejected: s_s1 2/0, s_s2 2/0, s_d1 4/1, s_d2 4/1, s_e1 8/2,
s_e2 8/2, s_t1 2/0, s_t2 2/0; h_t1 1/0, h_t2 1/0, n_t1 1/0,
n_t2 1/0. S scans every candidate per site (no early exit); the
cost increase vs H/N is bounded by the per-site candidate counts,
as pre-registered (no asymptotic change).

## Bar scoreboard

- SYN-NR-SEP: HOLD (8/8 SEP-NEW)
- SYN-NR-DECOY: FAIL (0/8 "D ok"; 8/8 D-DECOY-FAIL)
- SYN-NR-CHAIN: FAIL (0/8 "CD ok"; 8/8 CD-DECOY-FAIL)
- SYN-NR-BATT: FAIL (45/46; F2)
- SYN-DT: FAIL (0 > 8 false)
- SYN-DET: HOLD (12/12 worlds 3/3 byte-identical; battery 3/3)
- SYN-PURE: HOLD (safebin only; no python3; dash scans clean)
- SYN-ORDER: HOLD (freeze 5b2f8e0f0 at 09:40:58 UTC precedes first
  artifact 09:41:06 UTC)
- SYN-SCOPE: HOLD (see REDTEAM_SELF.md and the verdict: no
  re-litigation of H5R2's BUILD-PASS; separator named as open gap;
  no general provenance-policy claim; oldest-first and newest-first
  both named as enumeration artifacts)
- SYN-ARCH: HOLD (no protected-core change; +99/-0 lines in
  t2_trial only; new_semantic_cases=0; modes/bridges/handlers=0)

Decision rule: BUILD-PASS iff every bar holds. Four bars fail.
