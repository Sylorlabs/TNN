# RT2 ATTACK REPORT — hell-hole V4 red team vs T2 (r12_v4.zag integrated stance classifier)

**Crew:** RT2 (blind). **Target:** `docs/lab/senses/web-search/internet-trial/phase3/repairs_v4/crews/integ/r12_v4.zag`
**Frozen prereg:** `/home/hatch/workspace/scratch-hellhole/redteam/PREREG_V4_RT.md` (followed exactly).
**Blindness:** read ONLY the prereg + the target file itself (fetched via gh-api from branch `tnn-native-lab`,
commit `41931598a46e648c3187d71dc415b2f238cdc98a`). Never read `scratch-hellhole/crews/*`,
other `redteam/rtN` dirs, or builder artifacts. No builder corpora were seen; all 92 attack items are
novel (v3 seed shapes rewritten with fresh entities/numbers; none from the v4 batteries).

## Method (K-RTBLIND / K-RTDET compliance)
1. Wrote attack corpora FIRST: `gen_corpus.py` (deterministic, no RNG) → `corpus_rtA.tsv` (46 items),
   `corpus_rtB.tsv` (46 items), columns `id \t claim \t evidence \t oracle`. Oracle labels pre-committed.
2. Derived run TSVs (`run_rtA.tsv`, `run_rtB.tsv`: `idx \t claim \t title=evidence \t snippet=""`).
3. Built target with pinned toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
   r12_v4_target.zag -o r12_v4_bin --no-zagd` (build warnings only, same as builder).
4. Ran each battery 2x → byte-identical (K-RTDET satisfied).
5. A HIT = target output disagrees with oracle in the attacked direction.

**mtime chain (K-RTBLIND):** corpora `2026-09-23 20:57:07 UTC` → binary built `20:58:07` →
runs `20:58:24/20:58:25`. Corpus predates all runs. Target was never executed before corpus freeze.

## SHAs
- corpus_rtA.tsv: `63a4f700d5684b14d1e5294874d61e3c24ce9a5bf090d6e889ddb146025471f3`
- corpus_rtB.tsv: `b52b5cd8787bdcff24ea6b78899d557e500e4f90ef7dec03b6ab79811c3b508a`
- run TSVs: rtA `0f478215fed4a8f00397ef069c11f3ebfdd3606b004bdd36000cbfc99f77e5ea`,
  rtB `aa57531807595e9583cb447da09856c296a075492721d110a634a08e095753f8`
- target source (as fetched): `1e7700df8550391649e2e94d5afe187304eed9964325d1fed9ef49188ea81a37`
  (repo blob `9f80cf454b21681efb82fbce64dc1ce5baae1d63`)
- built binary: `84be4b81a63834007f1a12bbaa9ce1fa0378725347c785f28a065376d384bc9b`
- runA_pass1.log = runA_pass2.log: `f0104693d6662af507e1efff20b11644ba2d060ae48bdb3edbe55ca7ec184ab4` (46 lines)
- runB_pass1.log = runB_pass2.log: `df50d92a62c91eb9e62cc982f6f7c4bf01bac9781c1be42f0dcc13465685ee43` (46 lines)

## Verdict
- **RT-A (accept-invalid): 2 hits / 46 → PASS** (K-RTA needs ≥3). The v4 repairs hold on
  "no evidence" (12/12 correctly DENY via deny-lex), most numeric, most because-claims, hedged items.
- **RT-B (reject-valid): 32 hits / 46 → FAIL** (K-RTB: ANY hit = FAIL). The v3 failure mode
  reproduces: valid DENY/AFFIRM judgments are rejected, withheld, or inverted.

## RT-A hits (2)
| id | claim | evidence | oracle | target |
|----|-------|----------|--------|--------|
| A35 | The river flooded because the dam was opened | The river flooded while the dam gates were open; engineers state the flood resulted from record rainfall upstream. | DENY | **AFFIRM (endorse)** — evidence explicitly attributes the flood to rainfall; the because-claim is affirmed on overlap anyway. Causal-attribution leak in the endorse path. |
| A41 | The manuscript is a forgery | One expert alleges the manuscript is a forgery, but the claim is unverified. | NEUTRAL | **AFFIRM (endorse)** — "alleges … unverified" is hedged evidence; lhedge/whedge guards did not fire. Hedged-evidence over-affirmation. |

Notable RT-A non-hits (repairs holding): A01–A12 all correctly DENY(deny-lex); A13/A17/A19/A21
correctly DENY(numeric-mismatch); A22–A24 correctly DENY or NEUTRAL; A25–A27/A29/A33/A36 correctly
NEUTRAL; A37 ("is thought to") correctly DENY(deny-lex); A42–A46 correctly NEUTRAL/gate.

## RT-B hits (32) — the v3 failure mode, reproduced
**Catastrophic wrong-direction AFFIRMs (endorse path affirms contradicted claims on subject overlap):**
| id | claim | evidence | oracle | target |
|----|-------|----------|--------|--------|
| B01 | Dolphins are fish | Dolphins are mammals that breathe air through a blowhole and nurse their young. | DENY | **AFFIRM (endorse)** |
| B02 | Spiders are insects | Spiders are arachnids with eight legs and two body segments, not insects. | DENY | **AFFIRM (endorse)** |
| B03 | Whales are fish | Whales are warm-blooded mammals that give birth to live young. | DENY | **AFFIRM (endorse)** |
| B33 | Water boils at one hundred degrees everywhere on Earth | In La Paz, high in the Andes, water boils near eighty-seven degrees. | DENY | **AFFIRM (endorse)** |
| B34 | All swans are white | Black swans are native to Australia. | DENY | **AFFIRM (endorse)** |

Minimal probes reproduce: `Dolphins are fish` + `Dolphins are mammals that breathe air.` → `1 endorse`;
`Water boils at one hundred degrees everywhere on Earth` + `In La Paz water boils near eighty-seven degrees.` → `1 endorse`.
Root cause (from target source): the merged AFFIRM gate in `scan_text` fires on
`nclm>=need && anch==1 && ns==cneg && …` — subject overlap + polarity match, **with no predicate check**.
Worse, the endorse AFFIRM returns before `numeric_guard` runs, so the B2 numeric repair never gets
to veto (B33: refuted universal affirmed despite a comparable number in evidence).

**Valid negations denied or withheld (neg-scope / quantifier misfires):**
| id | claim | evidence | oracle | target |
|----|-------|----------|--------|--------|
| B16 | Not all metals are magnetic | Iron, nickel and cobalt are magnetic, but copper, aluminum and gold are not. | AFFIRM | **DENY (neg-scope)** |
| B17 | No student failed the exam | Every student passed the exam, a one hundred percent pass rate. | AFFIRM | **DENY (quantifier)** |
| B21 | Salt does not melt ice by heating it | Salt melts ice by lowering the freezing point of water, not by adding heat. | AFFIRM | **DENY (neg-scope)** |
| B45 | Unlike the claim, iron is magnetic | Iron is strongly magnetic; copper, by contrast, is not magnetic at all. | AFFIRM | **DENY (neg-scope)** |
| B18 | The vault was not opened by force | The vault showed no signs of forced entry; investigators believe it was opened with a key. | AFFIRM | NEUTRAL |
| B20 | Coffee does not dehydrate you | Studies show coffee's mild diuretic effect is offset by its water content, so it does not cause dehydration. | AFFIRM | NEUTRAL |
| B23 | It is not true that vaccines do not save lives | Vaccination programs have saved millions of lives worldwide. | AFFIRM | NEUTRAL |
| B28 | Unlike birds, bats give birth to live young | Bats are mammals that give birth to live young; they do not lay eggs like birds. | AFFIRM | NEUTRAL |
| B29 | The treatment is not risk-free | The treatment carries documented risks, including infection and bleeding. | AFFIRM | NEUTRAL |
| B46 | The patient does not have diabetes | Blood tests show normal glucose levels, ruling out diabetes. | AFFIRM | NEUTRAL |

**Valid DENYs withheld (NEUTRAL instead of DENY):**
B04 bats-blind rewrite, B05 penguins, B06 kale-smoothie rewrite (no-evidence generalization fired for B07/B08
but not B06), B11 (600-muscles range excludes claim — numeric guard abstained where B09/B10/B12/B13 fired),
B24, B25, B31, B32, B38, B40.

**Valid causal AFFIRMs withheld — the B3 causal repair overcorrected:**
| id | claim | evidence | oracle | target |
|----|-------|----------|--------|--------|
| B41 | The sky is blue because air molecules scatter blue light | Nitrogen and oxygen molecules scatter short-wavelength light in all directions, which makes the sky appear blue. | AFFIRM | NEUTRAL |
| B42 | Seasons change because Earth's axis is tilted | Earth's twenty-three point five degree axial tilt varies each hemisphere's sunlight through the year, causing the seasons. | AFFIRM | NEUTRAL |
| B43 | The app crashed because the update corrupted its database | Engineers confirmed the update corrupted the app's database, which caused the crash on launch. | AFFIRM | NEUTRAL |
| B44 | The bridge collapsed because its support cables snapped | Investigators determined that snapped support cables caused the bridge to collapse. | AFFIRM | NEUTRAL |

All four state an explicit mechanism with the causal verb present in evidence, yet `mech_aff` never
fires (compare B14/B15 ice-float/bread rewrites, which did AFFIRM — the causal path is inconsistent,
not uniformly strict).

**Low-overlap gate misses (boundary):** B36, B37, B39 returned NEUTRAL(gate) — evidence genuinely
refutes but shares <2 content stems. The gate works as designed; the misses are real but are a
recall boundary, not a logic inversion. Flagged, not weighted as heavily.

RT-B non-hits (repairs holding): B07, B08 (no-evidence DENY), B09, B10, B12, B13 (numeric DENY),
B14, B15 (causal AFFIRM), B19, B22, B26, B27, B30 (negation AFFIRM), B35 (neg-scope DENY).

## Honest limits
- Oracle labels are the attacker's pre-commitments. RT-A "no evidence" items were labeled NEUTRAL
  (absence of evidence ≠ evidence of absence); a DENY reading is defensible for some, but hits were
  counted ONLY in the attacked direction, so this choice cannot inflate the hit count.
- Evidence was placed in the title field with an empty snippet; the target concatenates both for the
  overlap gate and scans each stream separately, so this is interface-faithful, but a headline/body
  split could behave marginally differently.
- 92 items is a probe, not an exhaustive audit; the 32 RT-B hits cluster in the endorse/neg-scope/
  causal paths, which is where a fix crew should look first.
- No Python in the verdict path (scoring harness only). No commit made, per prereg.

## Files in this dir
`gen_corpus.py`, `corpus_rtA.tsv`, `corpus_rtB.tsv`, `run_rtA.tsv`, `run_rtB.tsv`,
`corpus_shas.txt`, `r12_v4_target.zag` (fetched target, read-only reference), `r12_v4_bin`,
`runA_pass1.log`, `runA_pass2.log`, `runB_pass1.log`, `runB_pass2.log`, `ATTACK_REPORT.md`.
