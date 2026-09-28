# PREREG R2-14 — Admitted Discriminative Challenge (R2-3 × R2-7 union)

**Status: FROZEN 2026-09-23. Committed alone — before any build output exists.**
**Source debate:** `../debates/DEBATE_D_new_fronts.md` §8 front (g), fork spec FS-G
("R2-37 Union: Admitted Discriminative Challenge"). Hypothesis and kill bars
below are copied verbatim from the debate; they are not re-derived or softened.
**Fork-id mapping (recorded, not hidden):** debate D's proposal label "R2-37" is
a label, not an id. R2-13 was already claimed (FS-F "Signature-Ceiling
Falsifier", frozen and committed 2026-09-23). The next free round-2 fork id is
**R2-14**. This fork is R2-14 = debate D's FS-G/R2-37.

## 0. Recorded discrepancy in the source debate (not re-derived, flagged)

Debate D §10's ranked table describes R2-7 as ALIVE with "≤1% overall,
≤2%/family on 10,000 adversarial, recall ≥80% on 2,000 controls, ≥90% flag".
The frozen `../forks/R2-7/VERDICT_R2-7.md` records otherwise: B5 **FAIL**
(214/10,000 = 2.14% false installs vs ≤1%), true-control recall **FAIL**
(1,376/2,000 = 68.8% vs ≥80%), high-confidence flag **FAIL** (2,449/2,790 =
87.8% vs ≥90%); verdict ALIVE only because the hard kills B4 and B6 passed.
The debate's summary of R2-7's measured results is wrong. This prereg copies
the FS-G kill bars from debate D §8 exactly as instructed, and records this
discrepancy so the FS-G verdict is judged against the frozen bars, not the
debate's misstatement. (R2-3's frozen verdict stands: 1,200/1,200 withhold,
B4/B6 pass.)

## 1. Hypothesis under test (verbatim from DEBATE_D §8 FS-G)

> **FS-G — R2-37 Union: Admitted Discriminative Challenge.**
> *Hypothesis:* the union of the evidence-independence admission law (R2-3)
> and the independent discriminative challenge (R2-7) closes KB4: no false
> install survives a discriminating challenge on audited-independent evidence.
> *Mechanism sketch:* the R2-3 instrument as the admission gate (declared
> disjoint sets per task, overlap audit, 1,200-pair R2P battery) + the R2-7
> challenge runner executed ONLY on admitted evidence; INSTALL only on
> discriminating-challenge PASS; challenges drawn from a registry each
> enumerated attack family must motivate.

**Union rule (executable):** ADMITTED DISCRIMINATIVE CHALLENGE = independent +
discriminative + admitted. INSTALL iff all three hold:
1. **Independent:** the challenge evidence is disjoint from the
   percept-forming span — per-task declared disjoint sets (frozen §2), with a
   mechanical per-trial overlap audit (spans within the fixture and
   non-overlapping; any overlap → NON-ADMITTED → WITHHOLD).
2. **Discriminative:** the executed challenge is the task's frozen registry
   entry (inherited from R2-7's frozen REGISTRY.md, unchanged): it names the
   strongest plausible alternative and predicts DIFFERENT outcomes under the
   claim vs the alternative. Non-discriminating challenges are rejected at
   registry time (mechanical: `chal_supports` never INSTALLs on outcome ≠
   claim's prediction).
3. **Admitted:** the challenge runs ONLY on evidence that passed (1). The
   R2-3 admission instrument (declared sets + overlap audit + the 1,200-pair
   R2P battery) is the admission half; the R2-7 challenge runner on admitted
   evidence is the discrimination half.

## 2. What is built (pure Zag, zero RNG in decision paths)

- **Frozen core (reused verbatim):** R2-7 `src/r27.zag` — percept formation
  (6 tasks), the frozen challenge registry (`reg_challenge`,
  `reg_alternative`, `reg_evidence`), the six challenge functions, the
  support rules (`chal_supports` with margins), and the hash-chained ledger
  machinery. The registry is NOT re-tuned: R2-7's registry froze before its
  results; FS-G inherits it unchanged (re-tuning after seeing R2-7's failures
  would be HARKing).
- **New Zag code ONLY for the union glue** (`src/r213.zag` = r27.zag +
  additions; full-mode path character-identical to R2-7's `do_full(0)`):
  - (a) the **admission gate**: frozen per-task declared disjoint evidence
    sets + mechanical overlap audit per trial (see §3); non-admitted
    evidence → WITHHOLD (R2-7 errored on overlapping spans; the union
    withholds — admission is a gate, not a crash).
  - (b) **DISCRIMINATION ablation mode** (`abl_conf`): admission unchanged;
    each challenge replaced by a confirmatory re-check on the same admitted
    G evidence — run the challenge, INSTALL iff outcome ≥ 0 AND outcome ==
    claim, with NO margins and NO alternative-side test (the R2-1 shape:
    confirmation without discrimination).
  - (c) **INDEPENDENCE ablation mode** (`abl_form`): the discriminating
    challenge (with margins, via `chal_supports`) run on the FORMATION
    evidence (evidence offset = fo, non-disjoint by construction) instead of
    the admitted G span.
  - (d) **batch mode** (`runlist`): process a frozen list of fixture paths,
    one hash-chained ledger line per fixture, chaining in memory with the
    identical hash formula as the per-fixture append path (validated: first
    50 fixtures via single mode vs runlist must be byte-identical ledger
    segments).
  - (e) **registry-audit mode** (`regaudit`): print the frozen registry +
    the straw-alternative audit table + the mechanical discrimination check
    (pred-claim text ≠ pred-alternative text for every (task, claim)).
- **R2P admission component (reused):** R2-3's instrument
  (`src/sense.zag` + `r2p_front.zag` + `r2p_gates.zag`) rebuilt as
  `src/r213_r2p.zag` with the FS-G union gate registered (id 2):
  formation_src = F blob, gate_src = G blob, gate_judge = `front_judge`
  (the naive percept, same judgment vocabulary as R2-7). On R2P pairs the
  union's challenge is the clean-span judgment: it discriminates the claim
  C from the alternative "formation was fooled" (under C the clean gate
  span agrees — generator-verified; under the fooled alternative it
  disagrees). WITHHOLD iff the two judgments disagree; overlap audit = 0 by
  declaration. Gate ids 0 (reference) and 1 (broken positive control) are
  kept for the instrument B4 check. On R2P the union gate is mechanically
  the R2-3 reference gate — that is the point: the R2P battery tests the
  union's ADMISSION half (independence), the R2FX battery tests its
  DISCRIMINATION half.
- **Ledger:** hash-chained, append-only, same line format as R2-7 plus one
  field `admit=1/0` (admission-gate outcome, for auditability). `audit` mode
  verifies chains.

## 3. Frozen declared disjoint evidence sets (R2-3 admission declarations)

Per task (R2FX container: 8×u32 LE header [magic, task, index, family, fo,
fl, go, gl]; F = formation span, G = challenge/admission span):
- colordisc: formation = F RGB patch pair (6144B); challenge/admission = G
  (re-rendered pair + 48B spectra at G+6144). Challenge reads only
  [go, go+gl).
- colorconst: formation = F views; challenge/admission = G D65 re-render views.
- shapetrans: formation = F 96×96 occluded frame; challenge/admission = G
  48×48 clean quadrant.
- pitchdisc: formation = F 2-tone buffer; challenge/admission = G clean token.
- timbredisc: formation = F tone; challenge/admission = G tone. DECLARED
  LIMITATION (frozen, not hidden): the generator renders the SAME harmonic
  profile into F and G — byte-disjoint but informationally coupled. The
  overlap audit checks span-overlap, not informational coupling; the R2P
  battery (fooled F × clean G) is the empirical test of whether coupling
  reaches the gate's evidence.
- motiondir: formation = F frames 1–50; challenge/admission = G frames
  51–100 clean high-contrast.
Mechanical enforcement per trial: fo, go ≥ 32; [fo, fo+fl) and [go, go+gl)
within the file and non-overlapping; each challenge function reads only
within [go, go+gl) (source-auditable; pitchdisc G is 64,000B — two tones —
not 28,800B; the fixture header is authoritative over the prose spec).
Overlap/invalid → admit=0 → WITHHOLD.

## 4. Fixtures (all frozen before results)

- **B-adv (10,000 adversarial trials):** all R2FX fixtures with family ≥ 1 in
  `../forks/R2-7/fixtures_R2A/{r2a,r2a2}` (10,425 total), sorted by
  (split, task, index), first 10,000. Frozen by manifest SHA committed with
  evidence. 18 families (6 tasks × families 1–3, per gen_r2a.py).
- **B-ctrl (2,000 true controls):** r2n fixtures (family 0), sorted by
  (task, index), first 2,000. Ground truth from `.truth` companions.
- **B-r2p (1,200 pairs):** the frozen R2P set (`../fixtures/r2p/`,
  `MANIFEST.r2p.sha256`): fooled-front-end × clean-gate pairs, 200/task.
- **B-cp (registry-adversarial suite):** challenge-prediction families,
  generated by a registry-knowing adversary under the frozen procedure:
  - Adversary knowledge: the full frozen registry + the union binary.
  - Per task: deterministic search (seed 20260923 + task id), budget 5,000
    candidate scenes per task. Candidates reuse gen_r2a.py's per-task
    renderers with adversarial mutations targeting the frozen challenge
    algorithm (documented per task in the verdict).
  - Strong-truth criterion: a candidate is kept only if (i) the union
    binary INSTALLS a claim ≠ truth on it, AND (ii) truth is unambiguous:
    the generator's ground-truth label is confirmed by a second independent
    measurement (documented per task; ambiguous scenes are discarded, never
    counted).
  - Kept scenes (≤100 per task) are written as R2FX fixtures with family=4
    (CP family), frozen manifest + generator ledger committed before eval.
    Tasks where the search finds nothing → documented EMPTY family.
  - Eval: the real union binary; false install = INSTALL with judgment ≠
    truth.
- **Straw-alternative audit:** adversarial red-team review of each of the 6
  registry entries' "strongest plausible alternative" (documented in the
  verdict): an alternative so weak that discrimination is vacuous = a
  strawman → the entry is rejected → the fork dies on bar (5).

## 5. Kill bars (copied EXACTLY from DEBATE_D §8 FS-G; dies on any bar)

1. **R2-7's bars:** false installs ≤1% overall and ≤2% per family on the
   10,000 adversarial trials (B-adv); true-claim recall ≥80% (denominator:
   the 2,000 true controls, B-ctrl); ≥90% of wrong high-confidence percepts
   flagged or left unresolved (denominator: wrong percepts at confidence ≥
   700; "flagged" = WITHHOLD/UNRESOLVED disposition).
2. **R2-3 admission:** ≥90% withhold on the 1,200 R2P pairs (B-r2p, FS-G
   union gate id 2); instrument B4 positive-control passes (broken gate id
   1: 100% overlap reported, withhold < 50%).
3. **DISCRIMINATION ablation:** replace each challenge with a confirmatory
   re-check on the same admitted evidence (`abl_conf`) → false installs
   must rise ≥5× vs the full union on B-adv (proves discrimination, not
   independence, carries the load — the anti-R2-1 bar).
4. **INDEPENDENCE ablation:** run the discriminating challenge on formation
   evidence (non-disjoint) (`abl_form`) → false installs must rise ≥5× vs
   the full union on B-adv (proves independence carries load).
5. **REGISTRY-ADVERSARIAL:** the battery contains the challenge-prediction
   families (B-cp) plus the straw-alternative audits — any family exploiting
   a non-discriminating challenge kills.
Justification (from the debate): bars (3) and (4) are R2-1's two one-sided
deaths (1.37× ablation) turned into load-bearing proofs; bar (5) answers the
registry-gaming risk explicitly rather than by assertion.

## 6. Method

- Battery run TWICE (full union on B-adv + B-ctrl + B-cp; both ablations on
  B-adv; R2P gates 0/1/2); outputs byte-identical across runs (`cmp`);
  hash-chained ledgers verified by `audit` mode.
- False install = disp=INSTALL AND judgment ≠ ground truth (`.truth` files /
  pair truth). Per-family rates over (task, family).
- Port validation: the full-mode path is character-identical to R2-7's
  `do_full(0)`; dispositions on a calibration sample must match R2-7's
  frozen b5 ledger exactly; runlist-vs-single ledger segments must be
  byte-identical on the first 50 fixtures.
- Python is glue/analysis/fixture-generation only — never in any decision
  path. No sensory-output artifacts are produced (B7: mechanism elegance
  only; human-judged half PENDING-MICAH — no artifacts exist to judge).

## 7. Commit map

- This prereg: `senses/pam-rebuild/round2/preregs/PREREG_R2-14.md`
  (committed ALONE — no src, no evidence).
- Build output (later, separate commits):
  `senses/pam-rebuild/round2/forks/R2-14/`: PREREG copy, `src/` (r213.zag,
  r213_r2p.zag, copied R33 substrates, r2p_front.zag, r2p_gates.zag,
  gen_cp.py), `fixtures_cp/` (frozen B-cp + manifest), `evidence/`
  (ledgers, reports, manifests, scorer), `VERDICT_R2-14.md`, `LEDGER.md`.
- Shared frozen fixtures: `../forks/R2-7/fixtures_R2A/`, `../fixtures/r2p/`.
- Branch `tnn-native-lab`, repo `sylorlabs/TNN`. Commit via
  `~/workspace/commit_racefree.py`, lab-relative paths,
  TMPDIR=`~/workspace/tmp_commit`. No binaries, no .zagd. Verify via GitHub
  API, report SHAs.

**Laws:** pure Zag, zero RNG in any decision path, byte-identical reruns
required, plain language, max-risk posture. No retroactive bar changes after
results — amendments go to Micah.
