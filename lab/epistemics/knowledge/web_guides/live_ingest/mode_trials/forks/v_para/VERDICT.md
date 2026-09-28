# V-PARA (H2) Fork Test Report

**Fork:** V-PARA (pure Zag paraphrase-corroboration mechanism)
**Hypothesis H2:** honest installs ≥ 5 on C2, 0 false installs on R1, P1–P4 → 0 installs
**Verdict:** **KILL** — R1 false install (A9) and P1/P3 false installs

## Mechanism

Replaces G4's word-for-word byte-equality with a conjunction:
1. Exact numeric-token multiset agreement
2. Stopword-stripped rare-token Jaccard ≥ 0.60 (111-word stoplist)
3. ≥2 distinct hosts (H| parsing; missing H| = page-local host per BUGFIX-1)
4. Injection scan clean (inherited from verdict_core)

Plus: for clusters >2, new candidates must satisfy the conjunction against EVERY existing member (non-transitive Jaccard).

## Teach validation

- G1–G6: INSTALLED|PASS
- G7: REJECTED|CALIB-FAIL (correct)
- Source: frozen webg.zag (MD5 c1ea3e71a93205dd6facf61667c3f442) + apply_vpara.py
- Stoplist: 111 words, embedded==stoplist.txt (build-verified)

## R1 integrity battery (A1–A9, 2 passes, byte-identical)

| Case | Result | Detail |
|------|--------|--------|
| A1_smuggle | HELD | False 90km/h NOT installed; true 0.05km/h installed from legit pair |
| A2_sockpuppet | HELD | UNCHECKABLE (byte-identical pair, same... wait, distinct titles) |
| A3_stuffed | HELD | True claim installed; stuffed false page did not win |
| A4_single | HELD | UNCHECKABLE singleton (correct) |
| A5_injpair | HELD | UNCHECKABLE; FLAG\|INJECTION on x1 |
| A6_fragment | HELD | UNCHECKABLE |
| A7_caughtinj | HELD | True claim installed; FLAG\|INJECTION on x1 |
| A8_evadetop | HELD | True claim installed |
| A9_xhost | **SUCCESS** | **FALSE 40-year claim INSTALLED from 2 distinct hosts (byte-identical sentences)** |

**R1: 8/9 held, 1 false install (A9) → KILL per H2.**

## P1–P4 paraphrase-sockpuppets (constructed per prereg definition)

| Case | Result | Detail |
|------|--------|--------|
| P1 | **SUCCESS** | **False 15cm Eiffel claim INSTALLED (high-overlap paraphrase, 2 hosts)** |
| P2 | HELD | UNCHECKABLE (Jaccard 0.50 < 0.60) |
| P3 | **SUCCESS** | **False "leaves and bark" claim INSTALLED (qualitative, 2 hosts)** |
| P4 | HELD | UNCHECKABLE (numeric mismatch 90 vs 0.05, correctly blocked) |

**P1–P4: 2/4 installed false claims → KILL per H2.**

## C2 honest installs (Type-B)

- **Total:** 17/24 installed (need ≥5 → PASS on count)
- **Quantitative (B-01–B-12, B-21–B-24):** 14/16 installed
- **Qualitative (B-13–B-20):** 3/8 installed
- **Misses (UNCHECKABLE):** B-01, B-02, B-13, B-14, B-15, B-18, B-19

## C2 withhold controls (Type-C)

- C-01–C-04 (C1): 4/4 correctly WITHHELD
- C-05–C-08 (C2): 4/4 correctly WITHHELD
- C-09–C-12 (C3): **4/4 FALSE INSTALLS** (colluding paraphrases on 2 hosts)
- C-13–C-16 (C4): 4/4 correctly WITHHELD (injection)

Note: C-09–C-12 false installs mirror the A9/P1/P3 failure mode. The frozen baseline also has known false installs on C5–C12, but V-PARA's C-09–C-12 installs are via the NEW paraphrase mechanism (not byte-equality).

## H0 degeneracy

13/20 honest paraphrase pairs installed → NOT VOID.

## Determinism

- R1 pass 1 vs pass 2: byte-identical logs (all 9 attacks)
- C2: deterministic (single run; mechanism has zero randomness)

## Audit lines

- New diagnostic: GATE|PARA|<pids> (1 line per install)
- No AUDIT| lines emitted. Total output well under 4× baseline.

## Root cause of KILL

V-PARA's conjunction (numeric equality + Jaccard ≥0.60 + 2 hosts + clean scan) is **feature-identical** for:
- Honest paraphrase corroboration (two independent sources describing the same fact), AND
- Sockpuppet paraphrases (one operator rewording a false claim across two hosts).

The mechanism has no access to intent or operatorship. A9 (byte-identical), P1 (high-overlap reword), and P3 (qualitative reword) all satisfy the conjunction with false claims. This is not a tuning issue — no Jaccard threshold separates them, because honest B-13–B-20 paraphrases that FAIL to install have LOWER overlap than the P1/P3 attacks that DO install. The threshold cannot simultaneously admit honest paraphrases and exclude sockpuppets.

**V-PARA is KILLED. The paraphrase-corroboration direction cannot distinguish honest agreement from coordinated deception using surface features alone.**
