# PREREG — PAMs v2 RK-3 Ceiling Test (frozen 2026-09-23)

**Status:** FROZEN. Committed alone before any formal execution (Micah's ruling: TEST FIRST).
**Scope:** Four preregistered ceiling experiments on branch `tnn-native-lab`.
**Deliverable:** `CEILING_TEST_VERDICT.md` (REAL / NOT-REAL per experiment + can-any-honest-design-reach-85%).

## 0. Sequencing disclosure

This prereg is frozen and committed BEFORE any formal Zag execution for the
ceiling test. DISCLOSURE of pre-prereg activity (2026-09-23):

- The task brief and the R2-4 autopsy had already supplied the expected (a)
  headline values (`824/1,102 = 74.8%`) before this prereg was drafted.
- Pre-prereg feasibility reconnaissance repeated those values by Python
  arithmetic over the frozen case record, and used exploratory Python models
  to shape the (b)/(c)/(d) designs below. No repository files were modified,
  no commits were made, and no formal Zag runs were performed before this
  prereg. Python was glue/analysis only, never a decision path.
- All formal runs (§2–§5) occur strictly after this commit. Where exploratory
  modeling informed a design choice, it is marked [EXPLORATORY-DISCLOSED] and
  the formal verdict follows the frozen rule regardless of what exploration
  suggested.

## 1. Frozen evidence and toolchain (hashes)

| Artifact | SHA-256 |
|---|---|
| `case_r24_rk3.txt` (11,840 rows; seq\|tcode\|prog\|jcode\|jcorrect\|conf\|pred\|meas\|progF\|disp\|detail) | `ea49515fbff14b280ea62d4e05015f71a310ae957680c767c6b46bc5e48cda42` |
| `expect_r24_rk3.txt` | `c49147100b0c3dd07a35a524a2907d4e08415ff64df194d36efd5c01f8762b98` |
| `diagnose.zag` (pure-Zag instrument) | `2aed8371d2245b3c1ac2bef9251a2bb7dc30b25f64fdc7539824324dbcbd6243` |
| `sweep.jsonl` (11,840 frozen sense-trial records) | `4163fffa65f18f552d48f7efec0e9800a7406547a27c6259d39a48ec7f0833f2` |
| `records.txt` (post-deliberation; prog/final_prog/final_pred source) | (sha recorded at execution) |
| Toolchain | `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` |

Frozen headline values under test: trials `11,840`; correct high-confidence
percepts `1,102`; installed among them `104`; never reaching final PASS `278`
(`272` intrinsic UNRESOLVED + `4` FAIL + `2` deliberation downgrades: seq 2366,
2372, E2/BLOCK overrode a (g)-PASS). Gate-side ceiling predicate:
`jcorrect==1 && conf>=700 && prog==PASS && pred==1` → count `824`;
`824/1,102 = 0.7477` (74.8%). 85% needs `ceil(0.85×1102)=937`; gap `937−824=113`.

RK definitions (frozen, from R2-4/V2-D preregs): RK-1 = permanent false installs
≤3% (R2-4: 0; V2-D: 7/11,840 = 0.06%). RK-2 = wrong-HC permanent ≤1%.
RK-3 = correct-HC reaching PASS-and-install ≥85% (install =
PROVISIONAL/PERMANENT/CORROBORATED/ACCEPT_INSTALL). RK-5 = wrong-HC reaching
(g)-FAIL/UNRESOLVED ≥90% (R2-4/V2-D: 1,102/1,109 = 99.37%, computed on the
(g)-check verdict `sweep.prog`).

## 2. Experiment (a) — verify R2-4's 824/1,102 gate-side ceiling

**Method (pure Zag):** Build `diagnose.zag` with the pinned toolchain.
Run 3×: `./diagnose case_r24_rk3.txt expect_r24_rk3.txt report_out`.
**Pass criteria:**
1. The three runs' stdout are byte-identical (B6-style determinism).
2. Stdout contains `DIAG,CEIL,<tension>,824` with ceil exactly `824`.
3. Output matches `expect_r24_rk3.txt`; input SHAs match §1.
**Verdict:** REAL iff all three hold; else NOT-REAL (report the deviation).

## 3. Experiment (b) — decompose V2-D's 934 ACCEPT_INSTALLs by input program verdict

**Constraint (frozen):** V2-D's committed evidence contains no per-trial
(jG, confG) or disposition stream (Gap Crew B, DD-1: per-trial mapping NOT
reconstructible). Therefore (b) is an evidence-level decomposition with stated
assumptions, not a per-trial rerun.

**Committed inputs:** V2-D `metrics.json` (934 ACCEPT_INSTALL; RK-1 7/11,840;
RK-3 88.48% = 975/1,102); V2-D VERDICT calibration: D fires on 927/987
dual-span correct-HC (93.9%); wrong-HC G-agreement 0.6%. Frozen sweep gives,
for dual-span correct-HC (987): agree=1 → 954 (826 prog=PASS, 128
prog=UNRESOLVED, 0 FAIL); agree=0 → 33 (29 UNRESOLVED, 4 FAIL).

**Assumptions (explicit):** (A1) `sweep.agree==1` ⟺ D's `jG==jF`. (A2) D-fired
correct trials ⊆ agree=1 (D requires jG==jF). (A3) The 7 RK-1 false installs
are the wrong-HC trials D fired on (0.6% wrong-HC agreement ≈ 7).

**Derivation (frozen):** 934 = 927 correct + 7 wrong. The 927 are a subset of
the 954 agree=1 (826 PASS + 128 UNRESOLVED), so among the 927 correct:
PASS ∈ [799, 826], UNRESOLVED ∈ [101, 128], FAIL = 0. The 7 wrong are
prog=PASS (the (g)-check's 7 wrong passes, all (t1,agree,strong)=(1,1,1)).

**Report:** the [101, 128] UNRESOLVED installs (10.8–13.7% of 934) are the
non-PASS records R2-4 withholds that V2-D installs. State the interval and
assumptions; do not present a point estimate as measured.

## 4. Experiment (c) — honest (g)-predicate calibration: can ≥113 be recovered?

**Question:** can a deliberate revision of the (g) disjoint-span flagger
predicates recover ≥113 of the 278 never-PASS without breaking RK-1/RK-2/RK-5?

**Candidates (frozen):**
- R0 (control): identity — revised prog = frozen prog. Must reproduce the
  frozen headline (ceiling 824, never-PASS 278, RK-1 0 permanent false,
  RK-5 1,102/1,109). Control failure invalidates the instrument.
- R1: drop the `strong` requirement — revised `(g)` verdict = PASS iff
  `t1==1 && agree==1` (keep FAIL iff `agree==0 && contra==1`, else UNRESOLVED).
  Revised `pred` (gpred) = 1 iff revised prog == PASS. This flips all 953
  (t1,agree,strong)=(1,1,0) trials to (g)-PASS: 693 correct (incl. the 128
  correct-HC never-PASS) and 260 wrong, all 260 low-confidence (0 wrong-HC
  flip, so RK-5 is structurally preserved; the 260 are the RK-1 watch-set).

**Instrument (pure Zag, additive):** `grevise.zag` reads an augmented case file
`case_r24_rk3_ext.txt` = frozen `case_r24_rk3.txt` rows with `|t1|agree|strong`
appended per seq from frozen `sweep.jsonl` (derivation script committed;
output SHA committed; derivation re-verified at execution). It applies R0/R1
(selected by argv), replays the H2 gate with the EXACT `gate_step` logic of
frozen `diagnose.zag` (verified 0/11,840 disposition mismatches on R0), and
emits: `recovered` (of the 278 now installed), RK-3 count, RK-1 permanent
false, RK-2 wrong-HC permanent, RK-5 (revised (g) on wrong-HC).

**Documented limitations:** deliberation is held at frozen outcomes (the
replay does not re-run E1/E2); any newly-installed trial meeting E1/E2
trigger conditions is flagged post-hoc. Python is glue/analysis only.

**Runs:** each candidate 3×, byte-identical stdout required.

**Verdict rule (frozen):** the (g) path CAN reach 85% iff R1 recovers ≥113
AND RK-1 ≤3% AND RK-2 ≤1% AND RK-5 ≥90%. Otherwise the (g) path CANNOT —
report recovered count and which bar fails. [EXPLORATORY-DISCLOSED: pre-prereg
modeling suggests R1 installs only ~2 of the 128 (68 conflict-withheld, 60
suppressed downstream); the formal verdict follows this rule regardless.]

**Adjacent honest routes (reported, not (g) candidates):** the 2
deliberation-blocked trials (seq 2366/2372) need a deliberation-rule fix, not
a (g) change; the 115 t1=0 trials (harness family, no G span by design) are
fixture-inherent and unrecoverable by any (g) revision; the 33 G-disagreed
(31 weak + 2 contra) are unsafe to recover.

## 5. Experiment (d) — cross-sense never-PASS comparison

- **V2-B:** verify `sha256(vsense.zag) == sha256(sense_r24.zag)`
  (`cf4ffb43…997a78e`). If equal, V2-B's sense is byte-identical to R2-4's;
  by determinism (zero RNG) it yields the identical never-PASS count (278)
  on the same fixtures. Report as a verified control, not a new measurement.
- **R2-8:** NOT APPLICABLE as specified — `sense_r28.zag` reads single-span
  fixtures (.img/.pcm/.vid), not dual-span .r24, and emits no (g) program
  verdict, so "never-PASS" is undefined for it. Document; do not force a run.
- **Evidence-level decomposition (frozen):** the 278 never-PASS by
  (t1,agree,strong): (0,0,0)=115 fixture-inherent (harness family: 370/370
  harness_primary, 370/370 harness_noise, 185/185 harness_adversarial have
  t1=0 by design; 0/10,915 dual-span); (1,1,0)=128 sense-predicate-threshold
  (G present and agreeing, below `strong`); (1,0,0)=31 + (1,0,1)=2
  G-disagreement (ambiguous: fixture noise vs sense mismeasurement);
  (1,1,1)=2 deliberation override (not a sense outcome).

## 6. Final verdict rules

- The 74.8% ceiling is REAL iff (a) reproduces 824/1,102 byte-identically ×3.
- 85% is reachable by an honest design iff (c)'s rule passes, or the full
  honest program (RULE-ADDITION for the 621 conflicts + suppression
  adjudication + deliberation fix + (g) improvement) is shown with quantified
  headroom: theoretical max = 1,102 − 115 (fixture-inherent) − 33 (unsafe) =
  954/1,102 = 86.6%. Report both the (g)-only answer and the full-program
  arithmetic separately; do not conflate them.
- Every formal run: pinned toolchain, zero RNG in decision paths, ≥3
  byte-identical reruns, pure Zag for mechanisms/verification.
- Additive-only; no changes to other crews' files; no `~/workspace/v2work`;
  no binaries or `.zagd` committed. Commit with `TMPDIR=~/workspace/tmp_commit`
  via `~/workspace/commit_racefree.py`; lab-relative paths
  (`senses/pam-rebuild/v2/ceiling_test/...`).
