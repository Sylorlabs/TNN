# H6-R2 Re-attack — Fork W Evidence Report

Date: 2026-09-24. Branch: `tnn-native-lab`. Workdir: `~/workspace/selfpam_r2/reattack/buildW/`.

## 1. Recovery (provenance)

The branch contains only `WITNESS_PREREG.md`, `CORPORA.md`, `gen_fixtures.py` (claimed
build commits do not exist). The crew's build sources were recovered from
`~/workspace/selfpam_r2/forkW/` (inherited scratch), copied to
`~/workspace/selfpam_r2/reattack/buildW/`, and rebuilt with the pinned znc
(`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`).

- Clean rebuild output is **byte-identical ×2** and **byte-identical to the
  three inherited scratch transcripts**.
- Output SHA256: `eff00337cadc3528a8b1fe85b53cc8892efe38eb0c4f233fd65b7426837fe407`
  (exactly the SHA the crew reported).
- Conclusion: W qualifies for recover-and-attack. It is NOT marked INCOMPLETE.

## 2. Builder self-test reproduction (committed scorer, as-is)

Reproduced exactly with the recovered (unmodified) scorer:

| Bar | Reported | Reproduced |
|-----|----------|------------|
| M1 | 0/22 FAIL | 0/22 FAIL |
| M2 | 21/23 PASS | 21/23 PASS |
| M3 | 3/15 FAIL | 3/15 FAIL |
| M4 | 0/10 FAIL | 0/10 FAIL |
| M5 | 0/10 FAIL | 0/10 FAIL |
| M6 | 20/20 FAIL | 20/20 FAIL |
| M7 | mixed FAIL | identical |
| W1 | PASS | PASS (95/95, 0 unasfact) |
| W2 | 4/10 FAIL | 4/10 FAIL |
| W3 | PASS | PASS |

The crew's claim "self-test failed most bars" reproduces on a clean rebuild —
it is not a build/environment artifact.

## 3. Independent audit of the scorer — THREE driver bugs found

The scoring code (`w_main.zag`, `w_parse.zag`, `w_down.zag`) was read in full.
Three bugs make the reported numbers wrong. All three are in the
driver/scorer, not the witness mechanism (per-fixture verdict strings are
byte-identical before/after the fixes: `f35643c3…`).

### Bug A — packed-counter unpack uses wrong modulus (9 sites, `w_main.zag`)

`dn_labstat` returns `tot*1000000 + bad*1000`. The scorer unpacks
`bad = (st/1000) % 1000000`, which yields `tot*1000 + bad`, not `bad`.

- M1/M4/M5 (`bad == tot`): can NEVER be true → always 0/N.
- M6 (`bad > 0`): always true when tot>0 → always N/N.
- Same pattern in M7's H1/H4/H5/H6 lines.
- Fix: `% 1000000` → `% 1000` (9 sites).

### Bug B — `ps_h_TEXT` clobbers the PARA pair field (`w_parse.zag`)

Fixture layout: `48 text, 56 pair, 64 side, 72 kind`. `ps_h_TEXT` writes the
token count `nt` to `fb+56` — the **pair** slot — after `ps_h_PAIR` wrote the
pair-name sid there. Every fixture's pair linkage is replaced by its token
count, so `dn_mate` pairs fixtures by **equal token count**, not by pair name
(e.g. PARA P1A paired with CONFAB C1 — both 6 tokens — instead of P1B).
The published M2/M3 numbers measured random token-count-matched pairings.
Fix: delete the clobbering store (`nt` is never read anywhere).

### Bug C — `dn_mate` compares sids with `==` (`w_down.zag`)

`sp_add` does not intern strings, so two `sp_add("P1")` calls return different
sids. `dn_mate` used `==` on sids, so after fixing Bug B, NO pairs matched
(M2/M3 = 0/0). Fix: compare pair names with `sp_eq`.

## 4. TRUE self-test scores (fixed driver, byte-identical ×2)

Fixed-driver output SHA256:
`4ba994ca83dd2ad954c02fc21b877d3e121138f95b77c3c8834ff6547fd532e3`
(×2 runs identical; mechanism verdicts unchanged per §3).

| Bar | True score | Program bar | Result |
|-----|-----------|-------------|--------|
| M1 confab catch | **22/22** | ≥70% | **PASS** |
| M2 meaning-flip divergence | **19/23 (82.6%)** | ≥90% | **FAIL** |
| M3 paraphrase stability | **15/15** | ≥95% | **PASS** |
| M4 trace-alibi rejection | **10/10** | ≥70% | **PASS** |
| M5 generator-authored rejection | **0/10** | ≥70% | **FAIL** (predicted boundary) |
| M6 true-draft false-withhold | **6/20 (30%)** | ≤5% | **FAIL** |
| M7 held-out | M1/M2/M3/M4/M6 pass; M5 0/2 fail | preserve bars | **FAIL** (M5) |
| W1 PARTIAL preservation | 95/95, 0 ungrounded spoken | ≥90%, 0 false | **PASS** |
| W2 C-POINTER | 4/10 HALLUCINATED_PATH | 100% | **FAIL** |
| W3 dead-testimony instrumentation | reports=81 subgoals=92 | affect downstream | **PASS** |

### Failure characterization (all verified against mechanism verdicts, not the scorer)

- **M2 (19/23):** all 4 misses are SCOPE pairs (S1/S2/S5/S6). The `attr-attach`
  inference step fails identically (R1) on both sides of each pair, so verdict
  strings coincide instead of diverging. The mechanism cannot license
  attribute-attachment inference in these fixtures at all (the G-side atom is
  also ungrounded).
- **M5 (0/10):** every GENAUTH fixture has ≥1 generator-authored (truth=C) atom
  the witness GROUNDS (V1). The witness does not distinguish generator
  authorship — the crew's predicted boundary, confirmed.
- **M6 (6/20):** 30% false withhold. G3/G4: pattern-step declared-overlap
  mismatch (R7); G5/G6/G17/G20: `rel-compose`/infer licensing failures (R1).
  Genuine licensing gaps on true drafts, not wholesale breakage.
- **W2 (4/10):** 6 HALPTR fixtures fail the coverage check (S=2, V2R8) instead
  of reaching HALLUCINATED_PATH (S=4).

## 5. What the previous round got right and wrong (W)

- **Right:** the build reproduces byte-identically (SHA confirmed); M5 fails
  (predicted boundary, confirmed); the self-test as-run did show most bars
  failing (reproduced exactly).
- **Wrong:** the "failed most bars" conclusion was dominated by **scorer bugs**,
  not mechanism failures. The mechanism actually PASSES M1 (22/22), M3
  (15/15), and M4 (10/10). The crew never audited its own scorer; the packed-
  counter modulus bug alone zeroed M1/M4/M5 and maxed M6, and the pair-field
  clobber made M2/M3 measure token-count coincidences.
- **Still dead, for different reasons:** the true failures are M2 (82.6% <
  90%), M6 (30% false-withhold > 5%), M5 (0/10), and W2 (4/10 < 100%).

## 6. Frozen-battery attackability

W's binary accepts no draft input; its battery is the 167 compiled fixtures
(TEXT/ATOM spans/STEP traces/store entries). The frozen battery is draft-text
based (`ITEM|CONF|CF-001|<draft>|expected`); converting it to W fixtures would
require authoring the ATOM segmentation and STEP deliberation traces the
witness is supposed to verify — i.e. the test would measure the converter
author's deliberation, not the witness. No faithful conversion exists without
rigging the outcome. The independent evaluation therefore rests on the full
167-fixture battery with the corrected scorer, plus the targeted probes above.

## 7. Verdict: **DEAD**

Kill rule: fail M1/M2/M6 → DEAD outright. M2 (82.6% < 90%) and M6 (30%
false-withhold, bar ≤5%) both fail. M5 (0/10) and W2 (4/10) also fail.
The witness mechanism is real (M1/M3/M4 genuinely pass; per-fixture verdicts
are deterministic and the license logic correctly rejects confabs with
CONTENT_MISMATCH), but it does not meet the program bars.

## 8. Artifacts (this commit)

- `reattack_w_report.md` — this report
- `witness_fixed/w_main_fullfix.zag` — scorer with Bugs A+B+C fixed
- `witness_fixed/w_parse_fixed.zag` — Bug B fix (pair-field clobber removed)
- `witness_fixed/w_down_fixed.zag` — Bug C fix (`sp_eq` pair-name compare)
- `witness_fixed/w_fullfix_out.txt` — fixed-driver output
  (SHA256 `4ba994ca83dd2ad954c02fc21b877d3e121138f95b77c3c8834ff6547fd532e3`,
  byte-identical ×2)
- `witness_fixed/w_orig_out.txt` — unmodified-scorer reproduction output
  (SHA256 `eff00337cadc3528a8b1fe85b53cc8892efe38eb0c4f233fd65b7426837fe407`,
  matches crew-reported SHA, byte-identical ×2)

No binaries, no `.zagd` files committed. All runs deterministic (zero RNG).
