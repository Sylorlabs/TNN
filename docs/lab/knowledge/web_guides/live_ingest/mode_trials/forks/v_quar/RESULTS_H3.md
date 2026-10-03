# V-QUAR (H3) Results

Date: 2026-09-24. Branch: `tnn-native-lab`. Frozen prereg commit:
`872e22a92ab1282267e2b44635c65409fae88419`.

## Verdict: H3 FAILS (2 of 5 kill bars)

| Bar | Requirement | Result |
|-----|-------------|--------|
| H3-K1 (throughput) | ≥10 quarantined on C1+C2 | **FAIL: 9** (9 on C2, 0 on C1) |
| H3-K2 (production purity) | P ledger byte-identical to V-FROZEN | **PASS** |
| H3-K3 (no-read) | 0 Q reads by non-merge; instant kill on violation | **PASS** |
| H3-K4 (adversarial) | 0 P installs of prohibited; A9-class quarantined-but-unmerged | **FAIL** (see below) |
| H3-K5 (determinism) | Two passes byte-identical incl. Q and read log | **PASS** |

## H3-K1 detail: 9 vs 10

- **C2** (60 clusters, 120 pages): 28 installs, 32 withholds, **9 quarantined**.
  The 9 are fixture-beacon paraphrase pairs (nf-b-03, 04, 06, 08, 11, 16, 17,
  20, 23) that strict G4 withholds (no byte-identical sentence) but V-PARA
  catches (numeric agreement + Jaccard ≥ 0.60 + 2 hosts).
- **C1** (55 clusters, 213 URLs): 0 installs, 107 withholds, **0 quarantined**.
  C1's real web pages are topically diverse; no paraphrase pair meets the
  frozen V-PARA thresholds. This is correct behavior, not a bug.
- Near-miss: nf-b-01 (Jaccard 0.538 < 0.60) — a paraphrase pair just below
  the frozen threshold. The rule is working as specified; the corpus yields 9.

## H3-K2 detail: PASS

`runs/fb_integrity` (P binary on C2):
- `knowledge_ledger.txt` byte-identical to fork-base frozen artifact
  (SHA-256 `a5988c819f7eae8e283cfb78a935b174c02f8268480108ec50942376716271cf`).
- `refusal_ledger.txt` byte-identical to frozen
  (SHA-256 `7c733cabe3bf4c7442dd89a20f0042136fc8d6f3827bbe2373d39360564b7909`).
- 60 clusters, 28 installs, 32 withholds — matches frozen counts.

## H3-K3 detail: PASS

- All 9 C2 quarantines were adjudicated via the single accessor
  (`qread_claim`); each emitted exactly one `QAUDIT|MERGE|Q|...` line.
- Zero `AUDIT|PROD|Q` or `AUDIT|TRAIN|Q` lines in any run (the wrappers refuse
  Q-partition reads).
- Forbidden-read probe: `webg_prod query` on a Q claim file → read REFUSED,
  audited as `AUDIT|PROD|Q|REFUSED|...`. The kill switch works.
- CI check (`check_no_direct_q.sh`): passes on all three binaries; the raw
  readers are callable only from the wrappers, the single accessor, and
  themselves.

## H3-K4 detail: FAIL

R1 battery (A1–A9) under PROD and TRAIN:

**Production installs of prohibited claims (must be 0):**
- A2 (sockpuppet, single host): PROD **INSTALLS** "40 years" → BREACH.
- A9 (two-host collusion): PROD **INSTALLS** "40 years" → BREACH.
- A1, A3–A8: no prohibited installs (A1/A5/A7 injection-flagged correctly;
  A4/A6 withhold).

**A9-class quarantined-but-unmerged (must be present in Q, absent from P):**
- A9 **installs** under both PROD and TRAIN (byte-identical false sentence on
  two hosts passes strict G4). It is NOT quarantined (quarantine only fires
  on strict-withhold). It is NOT unmerged (it was never in Q).
- The prereg's H3-K4 expects a *paraphrased* two-host collusion (strict
  withholds, V-PARA quarantines, merge rejects). The A9 fixture uses
  byte-identical sentences, which strict G4 installs — the documented known
  boundary. The reworded-false-claim fixtures (P1–P4, referenced by H2-K4)
  were not found in the repo, so the intended "quarantined-but-unmerged"
  scenario could not be tested.

**Conclusion:** H3-K4 fails on both prongs. The frozen V-PARA quarantine
cannot contain A9-class falsehoods that pass strict verification, because it
only quarantines strict-withholds. This is a design-level limitation, not an
implementation bug.

## H3-K5 detail: PASS

Two full passes (C1 and C2, TRAIN+MERGE) are byte-identical across:
- `knowledge_ledger.txt`, `refusal_ledger.txt`, `run_li.log`
- `quarantine_ledger.txt` (SHA-256 chains), `quarantine/claims/*.txt`
- `merge_verdicts.txt` (all 9: `MERGE|Qxxxx|0`, none merged)
- `audit.log` (including all `QAUDIT` and `AUDIT` lines)

## Merge gate results

All 9 quarantined candidates were adjudicated by deterministic strict-G4
re-verification. All 9 returned `MERGE|0` (not merged) — the paraphrase
claims do not survive byte-identical re-verification, as designed. The merge
decision is a single verdict bit; no claim content crosses into P.

## Leak-channel tests

- **Glue taint:** The Python glue transiently sees Q claim text (TRAIN emits
  `QUAR|1|...` on stdout; glue writes the claim file). This is the write path,
  not a reasoner read. Disclosed as a limitation: Q contents transit glue
  memory during quarantine creation.
- **Cache-existence:** No `.zag-cache` or build artifacts are committed; the
  Q files live in `quarantine/claims/` with filesystem permissions as the
  only barrier (out of scope for the reasoner-read threat model).
- **Telemetry:** Audit logs are content-free (FNV-1a-64 hashes of paths and
  contents only). Merge verdicts are single bits. No Q text leaks.
- **Allocator reuse:** Zag binaries do not zero freed heap memory. Q claim
  buffers are freed after hashing; a compromised process could theoretically
  scan heap. Out of scope; disclosed.

## Audit-cost delta

- P on C2: 433 audit lines. T+MERGE on C2: 503 lines (+16%).
- The delta is the quarantine analysis and merge re-verification reads.
  Well under the 2× guideline.

## Ambiguities flagged (not improvised)

1. **C2 size:** Prereg says ≥200 URLs; supplied fixture has 120 pages. Ran
   the supplied corpus; mismatch disclosed.
2. **V-FROZEN/BF1:** Prereg says strict G4 + BUGFIX-1; mandated fork-base MD5
   is canonical pre-host-aware `webg.zag`. Compared against the mandated
   artifact; disclosed.
3. **H0:** Undefined in frozen docs. Not tested; not invented.
4. **P1–P4:** Referenced by H2-K4 but not found in repo. H3-K4's
   "quarantined-but-unmerged" scenario untestable as intended.
5. **A9 contradiction:** A9 EXPECT.txt documents that the frozen gate installs
   the false claim (known boundary). H3-K4 requires 0 installs. These are
   irreconcilable under the frozen rules; reported as FAIL, not silently
   reconciled.

## Answer to "you can't un-train a mind"

V-QUAR does not un-train. It quarantines (write-restricted, reasoner-
unreadable) and adjudicates (merge gate, strict re-verification). The 9
quarantined paraphrases were all rejected by the merge gate (MERGE|0), so
nothing entered P that strict G4 wouldn't have installed. But H3 fails its
own bars: the quarantine yields 9 not 10, and it cannot contain A9-class
falsehoods that pass strict verification. The separation is mechanical
(read-check + single accessor + separate SHA chains), but the throughput
and adversarial bars are not met.

## Artifacts

- `runs/fb_integrity/`: P integrity proof (byte-identical ledgers).
- `runs/c2_train_p1/`, `runs/c2_train_p2/`: C2 TRAIN+MERGE, byte-identical.
- `runs/c1_train_p1/`, `runs/c1_train_p2/`: C1 TRAIN+MERGE, byte-identical.
- `runs/r1/`: R1 battery (A1–A9) under PROD/TRAIN.
- `DESIGN_FROZEN.md`, `DESIGN_AMENDMENT_001.md`: design record.
