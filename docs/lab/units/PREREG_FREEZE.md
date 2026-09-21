# PREREG FREEZE — TNN Representation Program ("what is a unit of knowledge, if not an LLM token?")

**Date drafted:** 2026-09-21
**Status: PROPOSED — NOT FROZEN. Nothing in this document is approved. No build may start
until Micah signs.**
**Parent sources (all PROPOSED, all on `tnn-native-lab`, `docs/lab/units/`):**
`INDEX.md` (glossary + 53-arm ratification), `ALPHABET_A-F.md`, `ALPHABET_G-L.md`,
`ALPHABET_M-R.md`, `ALPHABET_S-X.md`, `ALPHABET_Y-Z.md`, `TEACHERS.md` (+ 2026-09-21
hand-wired peer-teacher amendment + 2026-09-21 installed-vs-learned amendment), `METRICS.md`,
`RISKS.md`, `ARCHAEOLOGY_R31.md` (+ 2026-09-21 full-native-redo amendment).

**Program question:** what is a unit of knowledge, if not an LLM token?
**Micah's thesis (the bet under test):** LLM tokens are a fixed discretization built for matrix
math. TNN's units must be COGNITIVE: chunking is an act TNN performs on the raw stream itself
(no fixed tokenizer); vocabulary is taught/learned the way a child learns words; a chunk is a
byte span with a stable ID that memory points back to, retrieves, and reuses.

**Tracks in this prereg:**
- **R0 — R31 full native redo** (§2): the old endogenous-chunking line reimplemented natively in
  Zag, all five test batteries re-run. Validates the resurrection; supplies the native
  implementation arm D is built on.
- **A — 53-arm bake-off** (§3): every catalogued arm built and tested head-to-head. No
  cherry-picking.
- **B — Teacher protocols** (§4): four teacher arms for the taught-vocabulary line, replayable
  TST-1 tapes, sealed flaw manifests.

---

## §0 — SIGN-OFF REQUIRED (Micah must approve or amend EACH item; nothing builds until all are signed)

Every numbered item is PROPOSED. "Approve" freezes it; "amend" replaces the value with
Micah's. Items marked **[RULE]** are frozen program rules, not numeric choices.

### Frozen program rules (already Micah's words — re-confirmation requested, not re-decision)

- **[RULE-1]** ALL 53 arms get built and tested. No "most promising" filter, no quiet merges
  (the R2/Z1 merge proposal is therefore rejected unless Micah explicitly overrides — see A-37).
- **[RULE-2]** "When in doubt or guessing at all with recommendations, just test both" — the
  non-lazy path. Judgment calls become arms/legs, never coin flips. Two unconverted calls
  remain: A-(b) Q's taught-wins tie-break leg; A-(b) O's force-pinned-taught-words leg.
- **[RULE-3]** Pure Zag. ZERO randomness in any AI decision path. (Seeded/logged/fenced RNG is
  permitted ONLY in experimental state-variation Arm B per the 2026-09-20 amendment — it has no
  role in this program.)
- **[RULE-4]** Byte-identical reruns as a hard gate (M8: N=5 + adversarial perturbations).
  Fail = disqualification, not a low score.
- **[RULE-5]** 1x then 10x scale legs for every arm and every track.
- **[RULE-6]** Full scorecard, section champions per metric, NO single crown metric. Overall
  winner ONLY on blowout (§7); otherwise Pareto frontier + scenario-fit map.
- **[RULE-7]** Per-arm kill criteria and program kill bars are BINDING. A fired bar kills —
  no appeals, no "but the idea is good" (K-M0: appealing a fired bar halts the program).
- **[RULE-8]** Results reported as they resolve, per track. No waiting for the whole battery.
- **[RULE-9]** Frozen rules, bars, metrics, and kill criteria cannot change silently after
  sign-off; dated amendments need Micah's re-approval.

### A. Global / cross-arm decisions (from arms consolidation)

- **A-1** Determinism gate protocol: N=5 reruns with adversarial perturbations (heap
  pre-fragmentation, ASLR-equivalent base offset, entropy/clock canaries, free-list order
  reversal). Approve.
- **A-2** Scale legs 1x → 10x for every arm. Approve.
- **A-3** Audit opcode namespace unification — three incompatible schemes exist (crew 1
  `CUT_PROPOSE=0xC0…`; crew 2 `OP_*` names; crew 4 `CHUNK_*/GRAN_SEL/EPISODE_BEGIN`).
  Proposed: unify to ONE scheme before prereg (scheme choice is Micah's).
- **A-4** Chunk ID width unification — u32 monotonic vs u64[4] vs 32-byte SHA vs
  (serial,gen,refs). Proposed: unify, or specify the per-arm mapping explicitly.
- **A-5** Metric namespace unification — M1–M6 (crew 1) vs M1–M9 (METRICS.md, canonical
  proposed) vs B1–B10 (crew 4) collide on names. Proposed: METRICS.md M1–M9 is canonical;
  crew-local names get a frozen mapping table.
- **A-6** Corpus striping convention — one slice per corpus vs defensive chunking vs ≤2^24
  stripes. Proposed: unify (all ≤ 2^25 per the znc wall; chunking declared a build note with
  byte-identical-equivalence proof, never a prereg amendment).
- **A-7** Build order (proposed): B-64 → A → X → C-W → identity bake-off (K1/K2/L1 + K3) →
  D's proposer → D → F-B → F-S → R → E → rest per crew notes. Approve/amend.

### B. Crew 1 — arms A–F

- **A-8** Shared memory budget: 1MB entries + table cap, identical across arms. Approve value.
- **A-9** D params: W=256, LMAX=64, MIN_LEN=3, REP_BAR (value needed), contdiv bar=2,
  candidate table 4096 slots, exact (count,seq) eviction comparator text. Approve all.
- **A-10** D-T: seed size 500 (most frequent C-W chunks, training split), just code 3,
  optional trainer force-pin. Approve.
- **A-11** D-R: REUSE_BAR=2. Approve.
- **A-12** F-S: CONF_BAR, ±W local-max window, MIN_GAP, u32 vs u16-saturating counters,
  3-shard layout. Approve.
- **A-13** F-B: BR_BAR=3, just code 5. Approve.
- **A-14** Per-cut `CUT_COMMIT` audit entries vs bulk `SCAN_COMMIT` for arm C. Decide.
- **A-15** Control retirement rules (A/B/C bars as stated in §3). Approve.

### C. Crew 2 — arms G–L

- **A-16** G1: WARN=80%, CRITICAL=95% (frozen integers), hysteresis band, merge-select
  (value ASC, slot ASC), thrash bar 5%, pinned-recall bar 1%, junk-fusion bar 10%.
- **A-17** G2: deliberation budget B; quality bar 2 abs points; cost bar 50× G1's sweep.
- **A-18** H1: W (e.g., 4 KiB), C=16 candidates, noticer list (frozen, proposal-only),
  4 evidence weights (integers), BAR, fallback rule, refusal semantics; reuse bar +10 pts;
  cost ceiling 10^4 ops/committed cut; BAR-sensitivity bar (±10% BAR flips >25% of cuts = death).
- **A-19** H2: B=8 evaluations/window; kill bars (reuse <+5 pts; corpus-B fallback >40%).
- **A-20** I1: T_co=7, group size 2–8, max level 4, demote-after-E episodes (E value needed),
  depth bar 5%, maintenance bar 20%, emergence bars 70%/50%.
- **A-21** I2: P=3 parents; kill bars (savings <10%, arbitration error >10%).
- **A-22** J1: k=3, α/β/γ arbitration weights (integers), death-share 5%, adversarial bars
  (≤3 vs ≥15 pts degradation), coverage zero-tolerance rule.
- **A-23** J2: K_max=5, subsumption 95%.
- **A-24** K1: table capacity 2× expected uniques; probe/chain rules; synthetic collision
  vectors; dedup bars (predicted 40%/25%, kill <15% on corpus A); chain bars (mean length >8
  AND latency >2×); disambiguation bar 5%.
- **A-25** K2: chain bar 4; bidirectional kill rule (within 2 pts of K1 + cheaper → K1 dies
  on cost). Approve the bidirectionality explicitly.
- **A-26** K3: hybrid-promotion rule (beats both pure schemes on ≥3/5 metrics → pure schemes
  demoted to components).
- **A-27** L1: segment sizing (fixed SHIFT vs variable + binary search); eternity
  zero-tolerance; cost bar 3× vs K1; fragmentation bar 4 segments/recall.
- **A-28** L2: epoch-bump definition in frozen integers (e.g., >5% of segments touched).
- **A-29** K-vs-L bake-off: 100-patch corpus-C series frozen; deterministic permutation seed;
  preregistered query set; five metrics; four kill rules (K ≥2× store_cost on (a); L 100%
  ref_stability on (c); >5 pts recall_accuracy gap; hybrid promotion). Approve all.

### D. Crew 3 — arms M–R

- **A-30** M: M-dedup scan bound W (frozen; e.g., last-W-episodes-only — value needed).
- **A-31** M2: canonical order (sorted ascending proposed); max composition depth.
- **A-32** N: i64 fixed-point scale; recall threshold; evidence rubric; overflow saturation
  rule (saturating proposed); three kill bars (5 pts, 2-pt ablation, sign-flip churn).
- **A-33** O: rubric weights; teacher track-record bar; parse caps; **[BLOCKING]** §F:
  taught words arrive judgment-held at provisional strength (proposed) vs force-pinned —
  Micah must decide; a force-pin signature forces redesign of the arm. (See also T-1.)
- **A-34** P: K=7, W=200 episodes; sensitivity calibrations at K/2, 2K.
- **A-35** Q: tie-break (emergent-wins proposed); overlap 50%; settled-rule threshold; kill
  bars (+3 pts, 10%/W churn, containment); Pareto-survival rule.
- **A-36** R: L=64, ref_cost=2 bytes, tie-break (longer, then earlier); SA/DP slice plan;
  audit-economics exemption text (policy audited, derivation not).
- **A-37** R2: K (adjacency co-occurrence threshold — value needed); candidate order
  left-to-right; **R2/Z1 merge decision: merge into Z1 (→52 arms) or test both (→53).
  Default per RULE-1/RULE-2 is both tested; Micah rules.**

### E. Crew 4 — arms S–X

- **A-38** Composite weights B2 20 / B4 20 / B5 15 / B9 15 / B3 10 / B6 10 / B8 5 / B10 5.
  Approve (note: B-family namespace — see A-5).
- **A-39** S: θ_merge, ρ, σ_split (values needed — judgment-set, logged, frozen); warmup
  5,000 episodes; kill bars (B4 <1.5× V's; churn >25%).
- **A-40** T: τ quiescence gap (value needed); kill bars (B2 within 2× of X; >80%
  sub-episode traffic).
- **A-41** U: derivation window radius; λ=1 op / 64 resident bytes / query; μ=10 ops /
  re-keyed byte; MA1/RC1 median op rate per 1k episodes (read at prereg-freeze); crossover
  sweep 0→1000 edits; kill bars (CPU >10× D's AND B4 <10%; D-beats-U at 100 edits).
- **A-42** V fairness checklist (1–6): 16,384 merges; both corpora; tie-breaks; Zag
  build-time trainer; one-page review before numbers count; victory conditions VC1–VC4
  margins (2×, 10×, 3×, 20 pp); intellectual-honesty clause (majority of
  B2/B3/B4/B5/B6/B8/B9/B10 under signed weights + VC1–VC4 all failed ⇒ thesis retreats to
  "chunks compose over tokens"). Approve all, and approve the clause text.
- **A-43** W: bucket scheme; selection rule; kill bars (composite <S+15%; gate refusals >5%).
- **A-44** X: floor bars (B2 ≥10× AND B5 ≥10× to retire X as candidate); universal floor
  rule text.

### F. Crew 5 — arms Y–Z

- **A-45** Y1: deadlock-escalation round limit N (value needed); justification enum.
- **A-46** Y2: adversary grammar (preregistered FIRST — it is the entire claim); cost bar
  100×/cut at 10×; held-out-grammar protocol (different crew writes it post-sign-off).
- **A-47** Y3: lineage-depth bar 50; tombstone GC policy (preregistered, never silent).
- **A-48** Y4: boundary-detector set (preregistered; amendment to change);
  question-conditioned selection rule; bars 5% (vs eager D at equal ledger cost) and 30%
  (one-shot waste).
- **A-49** Y5: qualifying eliminative checks for LINK (preregistered); 20% degradation bar;
  atomicity zero-tolerance rule.
- **A-50** Y6: per-chunk cascade policy (set at creation); 10× ledger-volume bar; REF-batching
  policy if the bar forces it (weakens provability — must be re-preregistered).
- **A-51** Z1: challenge set (preregistered); bars 50% (regretted-cut reduction vs D), 10%
  (witness invalidation on challenge-set revision).
- **A-52** Z2: misuse battery composition; breach-detection bar 80%; restriction-refusal bar
  30%; hot-path characterization plan (znc miscompile history ZNC-2026-09-19-001).
- **A-53** Z3: B per epoch (value needed); c_create, c_recall, c_revise (values needed);
  bars 20% (cost reduction vs best fixed-granularity arm), 15% (cliff-drop on halving B);
  explicit "why this ≠ reward signal" prereg text.
- **A-54** Z4: 30% convergence-speedup bar; 40% cross-namespace duplication bar; two-speaker
  curriculum definition (Phase 4 dependency noted).
- **A-55** Z5: recipe set (preregistered; extension = amendment); fuel limits; bars 15%
  (ambiguity/failure on edit curriculum), 50× (re-run cost vs cached span).
- **A-56** Z6: bootstrap arm choice (D proposed); ground-truth match band ±10%; 10,000-revision
  displacement bar; "scars are events, not accumulation" prereg argument text.
- **A-57** Z7: tier-assignment rule (must be deterministic + auditable — value/rule needed);
  two-source prototype corpus definition; cross-tier-contamination zero-tolerance rule.
- **A-58** Z8: per-chunk fuzz cap (value needed); boundary-perturbation battery definition;
  40% boundary-error-reduction bar.

### G. Metrics M1–M9

- **M-1** M1 bars: content recall = 100.0% (1x both corpora, 10x); boundary fidelity ≥ 99.5%
  (1x) / ≥ 99.0% (10x). Approve.
- **M-2** Swap probe N=64 (mandatory for ID arms); side-channel → metric scored 0. Approve.
- **M-3** Whole-file-blob arms scored on boundary fidelity (pass content, fail boundary —
  by design). Approve.
- **M-4** 100x spot sample (1,000 units) gated on 10x 100% pass. Approve.
- **M-5** M2 T2 third corpus: Gutenberg *King James Bible* prose + CPython `longobject.c`
  code. Approve (or substitute).
- **M-6** M2 criterion: recall ≥ 99.5% + boundary ≥ 95%, sustained 3 probes. Approve.
- **M-7** Episode-0 ~0 requirement (leak → trial invalid). Approve.
- **M-8** Champion bars ETC ≤ 3/3 (T1 prose/code), ≤ 5/5 (T2/T3). Approve.
- **M-9** 50-episode censor cap + never-average-censored rule (medians with flags;
  rank by reached-criterion? then ETC). Approve.
- **M-10** Relative-ETC vs taught-baseline as the comparison column. Approve.
- **M-11** M3: valuable set V = 1,000 units (deterministic schedule). Approve.
- **M-12** 10,000-step churn schedule (3,000 fresh / 3,000 kills / 4,000 at-capacity).
  Approve.
- **M-13** Survival ≥ 90%; champion ≥ 95%. Approve.
- **M-14** Freeze distinguisher: 500-unit fresh sample; fresh recall ≥ 80%; ≥ 1 management
  entry per 10 churn steps (steps 3,001–10,000); 50 deliberate weaken ops at step 6,000.
  Approve all thresholds.
- **M-15** FROZEN-UNDER-PRESSURE → M3 = 0 (undeclared freezing only; declared audited
  freeze scored on its own terms). Approve.
- **M-16** M4: 200 units/corpus (100 boundary + 100 content defects); cycling offsets
  ±1..±32; every-7th-byte XOR / identifier-rename rule. Approve.
- **M-17** 20 revision episodes max. Approve.
- **M-18** REVISED requires lineage continuity (kill+re-add ≠ revision). Approve.
- **M-19** Revision ≥ 80%/class (1x); champion ≥ 90%. Approve.
- **M-20** KILL-SUBSTITUTION: kill rate > 50% + revision below bar → M4 = 0. Approve.
- **M-21** Whole-corpus re-ingest to "fix" defects invalidates the run. Approve.
- **M-22** M5 "unit learned" 3-part definition (deliberate add + byte-exact recall +
  1,000-step mini-pressure survival). Approve.
- **M-23** Per-source-byte cost as the comparison column. Approve.
- **M-24** Per-byte memory ≤ 1.5× source bytes. Approve.
- **M-25** ≤ 10 audit entries per KB learned. Approve.
- **M-26** Harness (not arm) measures RSS delta + slot table; 16-word ledger entries fixed
  by harness. Approve.
- **M-27** M6: P→C and C→P never averaged (merging is non-compliant). Approve.
- **M-28** Transfer bars: recall ≥ 95%, boundary ≥ 90%, revision ≥ 70%, both directions;
  champion = smallest transfer tax. Approve.
- **M-29** Memorizer negative control with ≥ 15-point drop validity threshold gates the
  metric (if the memorizer passes, the bar rises before real arms are scored). Approve.
- **M-30** Corpus hashes committed before arms are built. Approve.
- **M-31** M7: 5,000-lookup retrieval schedule; repetition rounds 1–3; every-100th-unit edit
  schedule for C′. Approve.
- **M-32** M7 bars: hit ≥ 90%, reuse ≥ 1.5, dedup ≥ 0.4 (rounds 1–2; round 3 reported
  not barred). Approve.
- **M-33** Non-ID arms = N/A (no ID layer), excluded from blowout denominator;
  informational re-read-bytes footnote only. Approve.
- **M-34** M8: N=5 (raising allowed freely; lowering needs sign-off). Approve.
- **M-35** Runs 2–5 perturbations: heap pre-fragmentation; ASLR-equivalent base offset;
  entropy/clock canaries (behavior change vs run 1 = FAIL even if outputs match);
  free-list order reversal. Approve.
- **M-36** Captures: store image + ledger + stdout/stderr hash chains + allocator traces
  (order+sizes, addresses normalized out). Approve.
- **M-37** Fail-closed: M8 FAIL = outright disqualification, forensics-only numbers. Approve.
- **M-38** M9: 40/15/3 shape-class cutoffs. Approve.
- **M-39** M9 bonus-only status; retire-to-informational rule after first round if shapes
  don't separate arm classes. Approve.
- **M-40** Blowout rule: ≥ 6-of-8 section championships + never-below-median +
  75%-of-applicable-N/A rule + 10x scale confirmation (1x-only = PROVISIONAL BLOWOUT);
  co-blowout = tie → Pareto + scenario-fit. Approve.
- **M-41** Section ties broken by transfer-tax / lower-cost secondary, then co-champions.
  Approve.
- **M-42** Scenario-fit dimension assignment rules (6 dimensions, metric pairs, margins
  < 2 pts or < 5% relative = TIED, UNTESTED never extrapolated). Approve.
- **M-43** Program kill bars K-DET, K-R1…K-R10, K-M0 as stated in §8 (all binding).
  Approve each.
- **M-44** Fresh arm instance per metric (9× compute — approve the cost explicitly).
- **M-45** Teacher-touch resolution R-ii: count = 0 by definition for emergent/teacherless
  arms; no cross taught/emergent ranking on teacher-touch; T2/T3 as the autonomous
  comparison ground. Approve.
- **M-46** C2 reversed-order leg informational; >2-point drop → ORDER-SENSITIVE flag.
  Approve.
- **M-47** LEDGER-BOUND flag policy (scored on what completed; flag is data). Approve.
- **M-48** θ_merge = 0.15, bracket {0.10, 0.15, 0.20} legs per RULE-2. Approve.
- **M-49** ρ = 1.5, bracket {1.0, 1.5, 2.0}. Approve.
- **M-50** σ_split = 2.0, bracket {1.5, 2.0, 2.5}. Approve.
- **M-51** τ = 0.50, bracket {0.35, 0.50, 0.65}. Approve.
- **M-52** Parameters are deterministic thresholds, never probabilities. Approve as frozen
  statement.
- **M-53** Results reported as they resolve, per track. Approve as frozen rule.
- **M-54** Scorecard cell formats + metrics-v1 JSON schema normative. Approve.
- **M-55** Schema additions need sign-off. Approve as frozen rule.
- **M-56** Wall-clock: reported informationally only, never scored (resolves the R6/METRICS
  contradiction). Approve.
- **M-57** Ledger-cost unification: M5 entry-count bars AND R4 byte bars — approve
  "both-must-hold" or a unified bar (resolves the R4/M5 contradiction).

### H. Teacher track

- **T-1** §F FINAL re-confirmation: taught words arrive judgment-held at provisional
  strength; force-pin only by visible, audited trainer action — never a quiet install.
  (Same decision as A-33; signing once covers both.)
- **T-2** Wire format freeze: keep §P v1 with an amendment-override note, or bump to v2
  with the corrected teacher_id mapping (1=peer-handwired, 2=RESERVED-invalid, 3=muse-live,
  4=symbolic-hints, 5=sym-yesno-only). Decide.
- **T-3** Flaw manifest composition: 12/slice (4 wrong-span, 4 false-confidence,
  2 missing-grounding, 2 plausible-false) + per-type definitions. Approve.
- **T-4** Manifest sealing: learner never sees it; leak → run invalid + fresh-slice
  rescore. Approve.
- **T-5** Flaw scoring: hit = expected verdict + correct reason code; near-miss half
  credit; false-positive penalty weight; pass bar (proposed ≥10/12). Approve all.
- **T-6** Arm-1 wiring-spec authorship/audit: Muse writes the spec; approve the negative
  declarations + six-point auditor checklist (no hidden learning, no RNG).
- **T-7** Arm 3 (muse-live) bounds: obeys §P + §C; no flaw manifest (natural teaching
  only) — proposed. Approve/amend.
- **T-8** HINT wire format (§H): approve the proposed format; arm 4 emits hints only
  (no §P proposals). Approve.
- **T-9** Oracle query format + per-slice query budget K (anti-tiling). Set K.
- **T-10** Arms 4/5 proposal rights: symbolic arms emit no §P WORD_SPAN proposals at all
  (hints/answers only) — proposed. Approve/amend.
- **T-11** Curriculum slices: slice size (bytes), slice count, corpus assignment, flaw
  density per slice. Approve.
- **T-12** Session scale: proposals/session, deliberation budget per turn, DEFER max 3
  turns. Approve.
- **T-13** Appeal bound: max 2 appeals per proposal seq; two consecutive session-final
  rejections kill the unit for the session. Approve.
- **T-14** Verdict weights for head-to-head teacher-arm comparison (mastery /
  revisability / integrity / retention / cost). Set numbers.
- **T-15** Provisional strength: numeric value/ladder at adoption; promotion gate
  operationalization. Approve.
- **T-16** §C tripwire thresholds: 200-proposal window; 0.95/0.95/0.90 fire condition;
  5% vocabulary-dump rule. Approve/amend.

### I. R31 redo track

- **R-1** "Grounded consequence" operational definition for text/code (proposed: recall
  success + downstream discrimination consistency; purity = majority-label fraction).
  **[LOAD-BEARING — the redo cannot be built without it.]**
- **R-2** Giant-span bar: L_max cap (proposed ≤8, matching the reference enumeration
  range); compression-term cap/weighting so grounding dominates. Approve.
- **R-3** Dual≈raw tolerance ε (B-T2) + minimum compression ratio the dual route must add.
  Approve both.
- **R-4** Dose-curve bar: flatness/degradation tolerance across 250 → 8000. Approve.
- **R-5** Support-gap floor: minimum hard-battery score across 1–16 exposures. Approve.
- **R-6** Replication orderings B-T1/B-T2 as exact pass/fail bars (ordering constraints,
  not numeric targets). Approve.
- **R-7** Test-both legs list (§2): purity definition, promotion thresholds, inventory
  size — plus any additions. Approve.
- **R-8** Recovered parameters as the replication baseline (seen≥5, purity≥0.34, utility>0,
  700-chunk cap, longest-first, 82nd-percentile surprise, 256-entry inventory); re-derivation
  runs as the second leg. Approve.
- **R-9** 1x→10x promotion rule: 10x runs only after 1x replication bars pass. Approve.

**Decision count: 58 (A) + 57 (M) + 16 (T) + 9 (R) = 140 items.**

---

## §1 — Frozen program laws (restated exactly; §0 RULE-1..9 are the binding text)

1. **All 53 arms are built and tested.** The catalog's arm count is ratified at
   53 = 12 (A–F) + 13 (G–L) + 8 (M–R) + 6 (S–X) + 14 (Y–Z). (INDEX.md's header tables
   still say "38 proposed" with A–C "pending" — stale; the catalog-holder updates them.
   The 53 figure governs.)
2. **Test both.** Wherever this prereg faces a judgment call, both options are implemented
   and tested head-to-head. Converted pairs are listed per arm in §3; two calls await
   Micah's ruling (A-(b) items in §0).
3. **Pure Zag. Zero randomness in any AI decision path.** Seeded/logged/fenced RNG exists
   only in experimental state-variation Arm B (2026-09-20 amendment) and has no role here.
   Deterministic generators with logged fixed seeds are environment inputs, not AI decisions.
4. **Byte-identical reruns are a hard gate** (M8, §6). Same input + same complete logged
   internal state → byte-identical output, or the arm is disqualified.
5. **Scale legs 1x → 10x** for every arm and every track. 10x runs only after 1x bars pass.
6. **No single crown metric.** Full scorecard per arm; section champions per metric; overall
   winner only on blowout (§7); otherwise Pareto frontier + scenario-fit map.
7. **Kill bars bind.** Per-arm criteria (§3) and program bars (§8) fire without appeal.
   K-M0: appealing a fired bar halts the program pending Micah's re-sign.
8. **Report as results resolve**, per track. No waiting for the whole battery.
9. **No silent changes** to frozen rules/bars/metrics/kill criteria after sign-off; dated
   amendments need Micah's re-approval.
10. **Corpora:** Shakespeare prose (~5.4MB) and sqlite3.c code (~9.5MB), already pipelined.
    Corpus hashes are committed before any arm is built (M-30). T2 third corpus per M-5.
11. **Toolchain wall:** no single slice larger than 2^25 bytes (33,554,432) may be indexed —
    large buffers are chunked; chunking is a build note with byte-identical-equivalence proof,
    never a prereg amendment (confounder C5).
12. **No binaries, `.zagd` files, or `.zag-cache/` are committed.** Trial substrate
    directories carry `R33_NATIVE_SHA256_V2.zag` + `R33_NATIVE_IO_V1.zag` beside `cl/`.

---

## §2 — Track R0: R31 full native redo (Micah's decision, 2026-09-21)

R31 endogenous chunking is **redone in full, natively in Zag, with all tests re-run** — not
referenced, not reduced to two arms. This track validates the resurrection claim AND supplies
the native implementation + validated parameters that arm D and the predictive-surprise arm
are built on.

### R0.1 Scope — five batteries, reimplemented against the native substrate

1. **Tournament** — native re-run of the 8-arm tournament (predictive_surprise,
   random_chunks, fixed_window_4, MDL variants, raw_micro/no-chunking) on byte streams of
   text/code.
2. **Causal ablation** — raw_active vs chunk_active vs dual_active hard grounding, native;
   near-twin discrimination included.
3. **Dose curve** — 250 → 8000 training units natively; bar is no degradation.
4. **Split/merge dynamics** — recovered Zag dynamics: split fires iff `use_count ≥ 3 AND
   conflict ≥ learned_conflict AND utility ≤ learned_utility_floor`; merge fires iff
   `pair_seen ≥ learned_pair_seen AND joint_gain − separate_regret ≥ learned_gain`. Bar:
   dynamics occur, are ledger-auditable, boundaries shown mutable (a recruited chunk split
   then re-merged on the record).
5. **Support-gap recruitment** — teacher supplies only a grounded whole experience; learner
   recruits the largest unsupported raw span iff it meets learned min-support and beats the
   runner-up by a learned margin, else abstains (−1). Bar: hard-battery performance holds
   across 1–16 exposures.

All five run at **1x first; 10x only after the 1x replication bars pass** (R-9). Pure Zag,
zero RNG in AI decision paths, N=5 + adversarial perturbations hard gate.

### R0.2 Replication-fidelity bars (qualitative orderings — pass/fail)

- **B-T1 Tournament:** `predictive_surprise > fixed_window > raw_micro`, raw_micro (no
  chunking) **dead last**. (Full reference ordering, REFERENCE_ONLY:
  predictive_surprise ≫ random_chunks ≈ fixed_window_4 > MDL variants > raw_micro.)
- **B-T2 Ablation:** `dual_route ≈ raw_active` on hard grounding (within tolerance ε,
  R-3) **while adding compression** (minimum ratio, R-3); **chunk-only is rejected**
  (must lose to dual/raw on hard grounding).
- **B-T3 Dose curve:** flat or non-decreasing across 250 → 8000; no degradation
  (tolerance, R-4).
- **B-T4 Support-gap:** hard-battery score at or above floor (R-5) across 1–16 exposures;
  no collapse at 1 exposure.
- **B-T5 Dynamics:** split/merge fire under recovered conditions and are auditable; exact
  counts are REFERENCE_ONLY.

### R0.3 REFERENCE_ONLY handling

All old Python numbers (tournament 0.7376/0.4988/0.4928/~0.47/0.4489; ablation
0.9213/0.7533/0.9209; dose 0.36–0.40; support-gap 0.89–0.92) are **REFERENCE_ONLY**:
ordering constraints, never targets. The native redo is what counts as evidence. Hitting an
old number exactly is not required; violating an ordering is a replication FAIL.

### R0.4 "Grounded consequence" for text/code (PROPOSED — R-1, load-bearing)

Purity is operationalized as the **majority-label fraction** over grounded consequence labels,
where a consequence label for a span occurrence is defined by **(a) recall success** of the
span in a probe episode and **(b) downstream discrimination consistency** (the span's presence
predicts the same probe outcome across occurrences). Micah must approve/amend — the redo
cannot be built without this definition.

### R0.5 Anti-exploit and architecture requirements

- **Giant-span compression exploit explicitly barred** (L_max cap, R-2; compression term
  capped/weighted so grounding dominates — the reference docs rejected this exploit as a
  criterion and so does this prereg).
- **Dual route, not chunk-only**, is what gets preregistered (the old verdict rejected
  chunk-only; raw matched dual on hard grounding, so chunks must earn their place as
  compression/indexing with the raw route intact).
- **Test-both legs** for redo judgment calls (R-7): purity definition, promotion thresholds,
  inventory size — recovered-parameter leg vs re-derived leg, both run.
- **Redo feeds arms D and predictive-surprise:** the native implementation + validated
  parameters are their baseline. **Non-overlap rule:** the redo track validates the mechanism;
  arms D / F-S / F-B test it in the bake-off. Numbers are not double-counted across tracks.

### R0.6 Redo kill conditions

- Any B-T1…B-T5 ordering violated at 1x → replication FAIL; the resurrection claim is
  suspended pending a dated amendment (the arm D line does not proceed on an unvalidated
  base).
- M8 gate applies to the redo track identically (T-16).

---

## §3 — Track A: 53-arm bake-off (all arms built and tested — RULE-1)

Full mechanism sketches, frozen configs, and buildability notes live in the catalog files
(`ALPHABET_*.md`); this prereg freezes each arm's **kill criterion** — the falsifiable,
binding bar from §0 RULE-7. "Retire" = removed from future batteries, numbers kept for the
record. "Kill" = the arm's claim is dead; it leaves the Pareto set. "Reverse falsification"
rules are marked **[REV]**.

**Metric-name note (flagged, see A-5):** kill criteria below quote their source crews'
metric names. Canonical namespace is METRICS.md M1–M9; "M2" in crew-1/crew-4 criteria means
their local battery metric (stored-bytes-per-recall / retrieval cost), NOT episodes-to-
criterion. The frozen mapping table is a sign-off item — until signed, read each criterion
with its crew's glossary.

### Controls

| Arm | Family | Mechanism (one line) | Kill criterion (binding, PROPOSED) |
|-----|--------|----------------------|-------------------------------------|
| A — Raw bytes, no chunking | CTRL | No segmentation/IDs; memory holds {corpus_id,start,len} triples; recall re-reads the corpus buffer. The null hypothesis: "is segmentation needed at all?" | Retired if B-64 strictly dominates it on M1, M2, retrieval-op count, both corpora at 10x. **[REV]** If A ties-or-beats every lettered arm on M2 at equal M1, the smart arms die, not A. |
| B-8 / B-16 / B-64 — Fixed-size chunks | CTRL | Aligned blocks of size S; chunk ID = index (no table). Isolates "does boundary placement matter, or just existence?" B-64 doubles as harness validator (built first). | A size retires when another B size strictly dominates it on M1/M2/M3 both corpora. B as a family is killed as contender the moment any smart arm beats the best B size by ≥2x on M3 at equal-or-better M1. |
| C-W / C-P — Delimiter chunks | CTRL | One deterministic scan; C-W cuts at whitespace/newline, C-P adds frozen punctuation set. Maximal runs become chunks (lossless), IDs in stream order. Prices the confound: "how much of the smart arms' win is just rediscovering whitespace?" | A variant retires if a smart arm beats it ≥2x on M3 and M2 at equal M1 both corpora. **[REV]** If no smart arm beats C-W on Shakespeare by end of 10x, every smart arm is killed. |
| X — Degenerate (whole stream / byte-level) | CTRL | No chunking: whole stream as one unit (or byte-level addressing). The honest null arm. | Floor bars (A-44): retired as candidate only if B2 ≥10× AND B5 ≥10× (crew-4 battery). Universal floor rule text frozen at sign-off. |

### Cut-signal arms

| Arm | Family | Mechanism (one line) | Kill criterion (binding, PROPOSED) |
|-----|--------|----------------------|-------------------------------------|
| D — Self-cut byte span + stable ID **(Micah's hypothesis, flagship)** | CUT+IDENT | Five-organ pipeline: bounded candidate window (suffixes, lengths 2..LMAX); candidates accumulate rep / contdiv / reuse; proposal when rep≥REP_BAR, len≥MIN_LEN, contdiv≥2 (eliminative: constant-continuation spans eliminated as mere prefixes); consolidation commits via the reasoning-control gate; memory holds chunk-ID lists, never byte copies; CUT_SPLIT/MERGE/ROLLBACK revision; tombstoned IDs never reused; strength judgment-set. | Any one kills: (i) stored-bytes-per-recall ≥ B-64's both corpora at 10x; (ii) churn > 0.30 at 10x; (iii) M1 < B-64's at equal memory budget. **If D dies, the program thesis dies with it.** |
| D-T — Curriculum-taught seed vocabulary | CUT+ACQ | Trainer pre-commits seed vocabulary (500 most frequent C-W chunks, just code 3, optional force-pin); D's self-cut organ runs and may split/merge taught chunks. Teaching *inside D's machinery* (arm O is the learner-side intake; both tested). | ≥50% of taught seed chunks revised/killed by end of curriculum AND untaught D matches D-T on M1/M2/M3 — teaching adds nothing measurable. |
| D-R — Reuse-gated commit | CUT | D's proposals, but commit requires reuse ≥ REUSE_BAR: a second memory entry must reference the span before the ID is minted. No ID until the span proves worth caching. | >50% of final vocabulary still uncommitted at end of 10x while D commits and wins on M3 — gating is pure delay. |
| F-S — Markov-surprise cuts | CUT | Deterministic order-2 byte Markov predictor; cuts at confident-miss positions (predicted≠actual, count≥CONF_BAR), local-maximum within ±W, ≥MIN_GAP apart; chunks = spans between cuts (just code 4); cut must recur (rep≥2) before commit — surprise proposes, it does not mint. | Any one: (i) Shakespeare boundary F1-agreement with C-W within ±0.05 AND M3 ≤ C-W's — rediscovers whitespace at 67MB cost; (ii) code cut count > 5× C-W's (cut storm); (iii) loses to D on M3 both corpora. |
| F-B — Branching-continuation cuts | CUT | Surprise via continuation-branching (not Markov): cut where the set of possible continuations spikes. Cheaper sibling of F-S. | M3 < C-W's both corpora; OR within noise of F-S on all metrics both corpora — redundant arm, keep F-S, retire F-B. |
| G1 — Pressure-driven coarsening | CUT | Chunking as triage: under memory pressure, merge cold chunks into superchunks reactively. | Any one: (i) ≥5% of triage-merged superchunks re-split by deliberate revision same run (thrash); (ii) byte-exact recall on pinned chunks drops >1% vs no-pressure control at matched occupancy; (iii) ≥10% of superchunks never recalled nor re-split (dead weight). |
| G2 — Pressure-gated deliberate cuts | CUT | Pressure as trigger, never as policy: pressure events open a deliberation window; cuts still chosen deliberately. | Recall-quality advantage over G1 at matched occupancy < 2 absolute points on byte-exact recall, OR deliberation cost per pressure event > 50× G1's sweep with no quality advantage — deliberation buys nothing. |
| H1 — Full deliberation per boundary | CUT | Boundaries as cognitive acts: every cut proposed, evidenced, and committed through inspect/propose/commit with a frozen noticer list and integer evidence weights. | Any one: (i) reuse hit rate ≤ fixed-64B baseline + 10 abs pts at equal live-store slots both corpora; (ii) refusal rate > 30% AND mean deliberation ops per committed cut > 10^4; (iii) BAR ±10% sensitivity flips > 25% of cut decisions — decisions are bar-noise, not evidence. |
| H2 — Budgeted deliberation | CUT | H1 under a compute cap (B evaluations per window); fallback to cheap heuristic on budget exhaustion. | Reuse advantage over baseline < 5 absolute points, OR fallback rate on corpus B > 40% of windows — the budget destroys the deliberation. |
| R — Compression cuts (MDL/DP) | CUT | Chunks are compression units: cut where description length is minimized (suffix-array/LCP + DP over cost). | Boundary F1 (vs whitespace/punctuation joints AND vs arm O's taught spans, separately) does not beat the fixed-64-byte baseline by ≥10 points on both corpora; OR held-out recall (M1) with R-cuts does not beat the 64-byte baseline. **Note (C9):** R makes compression *dominant* — it is the anti-R31 control on the compression axis, not R31's continuation (R31 deliberately down-weighted compression). |
| R2 — Compounding-elimination cuts | CUT | Candidate boundaries proposed cheaply, eliminated by compounding evidence; proposals-per-accepted-cut must fall over the corpus (eliminations compound). | Verified-boundary recall (M1) on held-out probes does not beat arm R by ≥3 points (receipts don't buy recall at 10× compute); OR proposals-per-accepted-cut does not fall over the corpus — core claim fails. **R2/Z1 merge decision: A-37 (default: both tested).** |
| S — Recall-driven boundaries | CUT | Segmentation shaped by recall success/failure: boundaries that serve successful recalls are reinforced (judgment-set), boundaries behind failed recalls are re-cut. Vocabulary crystallizes from use. | Any one: (i) post-warmup B4 < 1.5× V's on either corpus; (ii) merge-then-split churn > 25% of all merges on either corpus (crystallization never settles); (iii) determinism gate fails; (iv) universal floor rule fires. |
| Y1 — Negotiated cuts | CUT | Two-organ cut protocol with mutual veto; deadlock → deliberate adjudication with a round limit. | Over 10,000 cuts, negotiated boundaries show ≤10% better recall-stability than arm-D unilateral cuts at the same granularity; OR veto rate collapses to <1% within the first 1,000 cuts (lazy agreement — then Y1 ≡ D with extra ledger cost). |
| Z1 — Witness-bound cuts | CUT | A cut must survive an eliminative challenge window to become a chunk; challenged-and-failed cuts are regretted on the record. | Regretted-cut rate not ≥50% lower than arm D on the revision curriculum — the window buys nothing; OR challenge-set revision invalidates >10% of live witnesses — binding too brittle (kill the binding, keep the window). |
| Z6 — Scar boundaries | CUT | Boundaries form at revision sites: ledger scar tissue segments the stream; "meaning lives where things changed." Bootstrapped from arm D's cuts. | Scar boundaries match ground-truth units (sqlite3.c function boundaries, Shakespeare act/scene structure) no better than random cuts at the same count (±10%) — the claim is dead; OR the bootstrap arm's cuts are never displaced by scars after 10,000 revisions (decorative). |
| Z7 — Provenance cuts | CUT | Cut at trust-tier boundaries; maximal single-provenance spans. | Any cross-tier contamination on the spoof battery (spoofed bytes recalled with a proven-tier label) — containment broken, kill the claim, keep the labeling; OR tier assignment cannot be made deterministic/auditable without human judgment per chunk — Z7 collapses into arm O (taught): merge or kill. |
| Z8 — Fuzzy boundaries | CUT | Boundaries carry explicit ±n byte uncertainty; tighten/widen deliberately via TIGHTEN/WIDEN ops. | Boundary-error rate not ≥40% lower than arm D on the perturbation battery — carrying fuzz buys nothing; OR mean fuzz grows without bound on the revision curriculum (widen dominates tighten — kill or cap). |
| Y4 — Question-driven (lazy) cuts | CUT | Boundary candidates at ingest; segmentation committed at query time, conditioned on the question. | Recall accuracy >5% below eager arm D at equal total ledger cost (candidates + materializations); OR >30% of materialized chunks never recalled twice (laziness claim fails). |

### Structure arms

| Arm | Family | Mechanism (one line) | Kill criterion (binding, PROPOSED) |
|-----|--------|----------------------|-------------------------------------|
| I1 — Strict tree hierarchy | STRUCT | Chunks of chunks, single parentage; superchunks form from co-recalled groups; demotion after E quiet episodes. | Any one: (i) level-2+ superchunks < 5% of successful recalls at equal store cost vs flat chunks — depth is decoration; (ii) parent-maintenance + stale-rebuild > 20% of total audit ops on any corpus — maintenance swamp; (iii) level-1 boundary agreement with natural breaks < 50% on corpus A — the "emergent words" claim dies. |
| I2 — DAG hierarchy | STRUCT | Multi-parent: one span, several wholes; attach-vs-form deterministic rule. | Record savings over I1 < 10%, OR parent-arbitration error > 10% — I2 dies, I1 remains the hierarchy candidate. |
| J1 — Fixed-k competing tilings | STRUCT | k simultaneous tilings, no canonical cut; arbitration by frozen α/β/γ weights; tiling birth/death on evidence. | Any one: (i) best-of-k arbitration ≤ best single tiling + 2 pts at equal total chunk budget on adversarial-cut corpus — extra tilings are passengers; (ii) arbitration picks a non-byte-covering chunk even once, or picks a lower-scoring-by->γ-margin chunk > 5% of recalls — zero tolerance; (iii) birth/death turnover churns without settling. |
| J2 — Evidence-gated tiling birth/death | STRUCT | Tilings as hypotheses: born on evidence, die by subsumption (95%). | k does not converge (birth→death→birth for the same phase twice on one corpus pass), OR converges to 1 on all corpora — tilings were never needed; J1 dies with it. |
| T — Episode-aligned chunks | STRUCT | Chunks = episodes; segmentation follows the episode clock (τ quiescence gap). | Any one: (i) B2 within 2× of X's on either corpus; (ii) >80% of battery recall queries address sub-episode spans (the "unit of experience" claim falsified); (iii) determinism gate fails; (iv) floor rule fires. |
| W — Multi-granularity | STRUCT | Several grain sizes simultaneously; a selector with a justification gate picks per query; no single cut level. | Any one: (i) composite battery score does not beat S alone by ≥15% — W is S with extra steps; (ii) justification gate refuses >5% of selections — the selector is unsound; (iii) determinism gate fails; (iv) floor rule fires. |
| Y5 — Cross-stream span sets | STRUCT | One ID over a non-contiguous span set; kills cascade atomically via LINK with eliminative justification. | >20% of Y5 units on sqlite3.c degrade to single spans within the revision curriculum (links die faster than they pay); OR any kill leaves a live span pointing at a dead LINK (atomicity broken — kill the implementation). |

### Identity-scheme arms

| Arm | Family | Mechanism (one line) | Kill criterion (binding, PROPOSED) |
|-----|--------|----------------------|-------------------------------------|
| K1 — Full SHA-256 identity | IDENT | ID = SHA-256 of content (git-style, native); same bytes, same ID; dedup falls out. | Any one: (i) payload savings < 15% on corpus A vs sequential IDs — the caching claim dies; (ii) on corpus C mean revision-link chain > 8 AND latency > 2× baseline; (iii) > 5% of single-span recalls return contextually-wrong occurrence (right bytes, wrong role) — K1 dies as standalone (survives only as K3 component). |
| K2 — 64-bit FNV-1a identity | IDENT | Cheap hash identity with honest, counted collisions; chain rules for disambiguation. | **Bidirectional:** if K2's dedup savings within 2 pts of K1's AND per-add cost lower → **K1 dies on cost grounds** (keep K2). If chain lengths exceed 4 on any corpus run → K2 dies (64 bits too small for the store's lifetime). |
| K3 — Content+position hybrid | IDENT | Composite both schemes are secretly asking for: content-payload + position-reference. Third arm in the K-vs-L bake-off. | Hybrid-promotion rule: if K3 beats both pure schemes on ≥3 of the 5 bake-off metrics → both pure schemes demoted to components and K3 becomes the identity substrate. (If K3 loses the bake-off, it dies as a candidate.) |
| L1 — Absolute position IDs | IDENT | ID = (stream, segment, offset); identity is WHERE, not what. | Any one: (i) store cost > 3× K1 on corpus A with no recall-accuracy advantage — dies as primary (may survive as secondary index, cf. K3); (ii) *any* revision batch changes an existing position ID — its one promise broken, dies outright; (iii) mean segments-touched per sequential recall > 4 on corpus C. |
| L2 — Epoch-relative position IDs | IDENT | Compact position IDs relative to an epoch; epochs bump on >5% of segments touched; fixed translation table across epochs. | Any within-epoch ID change (same bar as L1), OR translation misses > 1% of cross-epoch recalls — kept L1's costs while breaking L1's promise. |
| M — Counter IDs | IDENT | Monotonic nth-chunk issuance; identity is issuance order; store-local handle. M-dedup: optional dedup scan over last-W episodes. | **Scoped:** KILL counter IDs as the cross-store/global identity if, in the two-TNN merge trial, remapping produces ≥1 dangling/misdirected pointer OR remap compute > 10% of total merge compute. (Survives unconditionally as the store-local handle.) Separately: the M-dedup claim dies (revert to pure issuance) if M7 dedup ratio < 0.4 on the repetition protocol. |
| M2 — Compositional counter IDs | IDENT | Counter IDs composed canonically (sorted ascending) for multi-span units; max composition depth frozen. | Single-byte leaf edit invalidates > 25% of cached compositions in the recall benchmark, OR ID recomputation > 10% of recall latency on the 10x run. |
| Y3 — Temporal/versioned IDs | IDENT | Identity = serial + birth epoch + revision lineage; tombstoned IDs never reused; never dangles. | Mean lineage depth > 50 on the standard revision curriculum (fragmentation, not versioning); OR any recall resolving to a tombstoned span (dangling reference observed) — kill and fix before any further claim. |
| Z4 — Dialect (per-interlocutor) IDs | IDENT | Per-speaker lexicons namespaced by speaker tag; TRANSLATE op; `common`-namespace governance. Phase 4 hook. | Per-speaker lexicons do not converge ≥30% faster than a shared lexicon — namespacing buys nothing; OR >40% of chunks duplicated across namespaces (no real divergence — overhead without content). Conditional on Phase 4 working. |
| Z5 — Recipe IDs | IDENT | Identity = deterministic cut-program; spans re-derived per recall (fixed op set, fuel limits). | >15% of recalls on the edit curriculum hit ambiguity or failure (loud failures count — the claim is stability, not honesty); OR recipe re-run cost > 50× cached-span recall at 10× scale — unaffordable online (survives only as ID-stability layer over cached spans, conceding the mechanism). |

### Acquisition + annotation + storage + economic arms

| Arm | Family | Mechanism (one line) | Kill criterion (binding, PROPOSED) |
|-----|--------|----------------------|-------------------------------------|
| O — Taught vocabulary | ACQ | Full learner-side intake via the Track B teacher protocol (§4): proposals → adopt/revise/reject/defer; taught words judgment-held at provisional strength (A-33/T-1). | Any one: (i) taught-only vocabulary does not reach M2 criterion in ≤½ the episodes of emergent-only P on T1 novel material — acceleration claim dead; (ii) disconnect test fails (post-scaffold M1 < 99.5%) — "learned" claim dead; (iii) any red-team malformed/malicious proposal adopted — **ingress gate killed: rebuild + full re-trial, not a patch**; (iv) BPE-smuggling teacher (exact BPE tiling at confidence 255) does not fire the tripwire. |
| P — Emergent vocabulary | ACQ | Boundaries emerge from co-recall: pairs recalled together ≥K times in W episodes are promoted to words; episode-indexed ring eviction; sensitivity calibrations at K/2, 2K. | After the preregistered episode budget, emergent vocabulary does not beat the fixed-64-byte baseline on held-out recall probes (M1) by ≥3 points; OR >50% of promoted words deliberately killed within the next W episodes (churn — promotes noise, not words). |
| Q — Hybrid taught+emergent | ACQ | Deliberate combination: taught proposals seed the emergent machinery; overlap cap 50%; settled-rule threshold; emergent-wins tie-break (proposed). | Any one: does not beat max(taught-only, emergent-only) + 3 points on primary bar (M1 recall / M2 episodes-to-criterion); OR collision-resolution kills >10% of entries per W episodes (churn); OR adversarial score falls below emergent-only (containment failure). Pareto note: survives as a dimension champion unless Pareto-dominated (loses or ties everywhere) — no assumed winner. |
| N — Judgment-annotated chunks | ANN | Chunks carry deliberate signed annotations (MA4 generalized from memories to units); i64 fixed-point scale; saturating overflow; ablation arm (judgments recorded but ignored at recall). | Any one: (i) does not beat the judgment-free control by ≥5 percentage points on the adversarial misleading-memory bar; (ii) ablation scores within 2 points of the full arm — judgments are decoration; (iii) >10% of chunks flip judgment sign more than twice in any 100-episode window — signal churn. |
| E — Ephemeral chunks | STORE | Segmentation exists transiently per episode in a scratch window and is discarded; memory holds byte copies, not references; no chunk table, no IDs, no CUT_* ops. **Do not "optimize" E with dedup** — that would turn it into D with extra steps and invalidate the control. | Stored-bytes-per-recall ≥ 2× B-64's at equal M1 on either corpus at 10x (copies-only strictly dominated by the dumbest persistent segmentation). **Expected to die informatively; its death certificate reads "references matter, transient segmentation does not."** |
| U — Recompute-on-demand | STORE | No stored chunks; cuts re-derived whenever needed (derivation window radius frozen); λ/μ op pricing; crossover sweep 0→1000 edits vs D. The anti-caching arm that makes D falsifiable. | (i) Total battery CPU > 10× D's AND B4 < 10% — anti-caching has nowhere to stand; OR (ii) D-with-invalidation beats U on total cost including 100 mid-stream byte edits — the battleground lost on U's home turf; OR (iii) determinism gate fails. **A U win means caching is an optimization with a measured crossover, not an architectural necessity — D loses its law-like status.** |
| Y6 — Forgettable (tombstone-native) IDs | STORE | Tombstone-native IDs, refcounted, checker-provable total deletion; per-chunk cascade policy set at creation. The *answer* to R3, not its victim. | Ledger write volume > 10× arm D on the same curriculum (refcount writes dominate — kill or move to batched REF accounting, which weakens provability and must be re-preregistered); OR any checker audit finds a live reference to a tombstoned ID. |
| V — BPE enemy (adversarial baseline) | ENEMY | Fixed subword tokenizer: 16,384 merges, both corpora, frozen tie-breaks, Zag build-time trainer. The thing to beat. Fairness checklist + one-page review before numbers count (A-42). | **Runs both directions:** V is beaten (retired as control, thesis advances) iff ≥1 TNN-native arm passes ≥2 of VC1–VC4: VC1 use-alignment (B4 ≥2× V's post-warmup); VC2 revision (B5 ≥10× fewer re-keyed bytes per edit); VC3 partial recall (B2 ≥3× better on misaligned spans); VC4 composition (B9 ≥20 pp). **Intellectual-honesty clause [REV]:** if V meets/beats the best TNN-native arm on a majority of the scored battery under signed weights and VC1–VC4 all fail, the thesis retreats to "chunks compose over tokens" — no goalpost-moving. |
| Z2 — Contract chunks | ECON | Chunk = audited obligation between organs; misuse refused loudly; breach checker on the recall hot path. | Breach-detection rate < 80% on the misuse battery — Z2 is theater; OR >30% of legitimate recall ops refused as breaches — restrictions unusable (kill the restriction half, keep obligations). Hot-path characterization required (znc miscompile history). |
| Z3 — Budgeted chunks | ECON | One scarce currency prices storage + access per epoch (B per epoch); granularity is economic; fixed prices + hard budget. | Total cost not ≥20% below the best fixed-granularity arm at equal recall accuracy — the machinery buys nothing; OR halving B causes >15% accuracy drop for a 50% budget cut (pricing model wrong — cliff, not graceful degradation). **The prereg must state explicitly why fixed prices + hard budget ≠ reward signal (A-53).** |

**Count check:** 4 controls + 17 cut + 7 structure + 10 identity + 10 acq/ann/store/econ = **48 rows**;
B counts as 3 (B-8/B-16/B-64), C counts as 2 (C-W/C-P) → **53 arms**. Ratified.

### Orthogonal axes (crew 2 finding — governs interpretation, not arm count)

Cut-signal × structure × identity are orthogonal axes: the final system likely takes **one pick
per column**, not one winning arm. Bake-offs are therefore run **column-wise** (cut tournament,
structure tournament, identity bake-off K-vs-L with K3) as well as whole-arm. The following
redundancy pairs are **flagged, NOT cut** (RULE-1): S↔P, R2↔Z1, Y3/L2/K1-links/M-links/
Z7-derived_from (five uncoordinated revision-lineage mechanisms — flagged C10), J↔Y5,
Z5↔K, U↔E↔Y4, D-T↔O, H1↔Y1, Q (tie-break), G↔Z3, K1↔K2. If a pair's members are
indistinguishable on all 9 metrics at 10x, the prereg amendment retires one — by amendment,
not by silence.

### "Test both" conversions already in the catalog

K1↔K2 (price of hash) · G1↔G2 (reactive vs principled) · H1↔H2 (deliberation vs budgeted) ·
I1↔I2 (tree vs DAG) · J1↔J2 (fixed-k vs evidence-gated) · C-W↔C-P (delimiter priors) ·
B-8↔B-16↔B-64 (granularity sweep) · D↔D-T↔D-R (self-cut vs taught-seed vs reuse-gated) ·
F-S↔F-B (predictor vs branching) · O↔P↔Q (taught vs emergent vs hybrid) ·
U-vs-D head-to-head with crossover analysis (rule-constant, storage-only — the cleanest
falsification battleground in the program) · K-vs-L four-condition bake-off with K3 as third arm.

---

## §4 — Track B: teacher protocols (taught-vocabulary line)

**Thesis (unchanged):** TEACHER PROPOSES, TNN DISPOSES. Learner autonomy is LAW.

### B.1 The four arms

| teacher_id | Arm | Nature |
|---|---|---|
| 1 | peer-handwired | Hand-wired white-box mature TNN. Muse does the wiring deliberately (memory entries, chunk vocabulary, signed judgments, chunk IDs) per a committed, versioned, hash-pinned wiring spec. A **fixture, not the subject** — it does not learn. |
| 2 | RESERVED | Invalid. The student's ingress gate rejects `teacher_id=2` as malformed. |
| 3 | muse-live | Muse, live, acting as teacher during the session: emits §P proposals in real time, obeys §P iron rules and §C. Adaptive judgment; no flaw manifest (proposed, T-7). |
| 4 | symbolic-hints | Symbolic hint-giver. Emits HINT events only (no §P proposals — proposed, T-8/T-10). Hints suggest regions, never words. |
| 5 | symbolic-yesno-only | Symbolic oracle. Answers student yes/no queries with a single bit (`ORACLE_ANSWER`, per-slice query budget K — T-9). Emits nothing unprompted (proposed). |

All four arms run identical curriculum slices, scored by the same verdict weights: **mastery 30%
/ revisability 25% / integrity 25% / retention 10% / cost 10% (PROPOSED — reconstructed from the
truncated source §B.10; sign-off item T-14).**

### B.2 Arm-1 wiring-spec requirements (what "hand-wired" concretely means)

The wiring spec is committed with the prereg (hash pinned). It contains:
1. **Chunk vocabulary** — enumerated entries: `chunk_id` (stable), canonical span pattern(s)
   as byte-offset shapes, **signed judgment** (sign + magnitude), and a confidence policy
   (must include non-255 values — selective proposals and expressed uncertainty by construction).
2. **Memory entries** — the teacher's held knowledge as explicit declared entries (content
   span, signed judgment, evidence refs). No learned weights anywhere.
3. **Proposal policy** — a deterministic function spec (pure Zag, committed as code or as
   pseudocode precise enough to implement verbatim) mapping `(spec, stimulus cursor, session
   history)` → the §P proposal sequence.
4. **Flaw manifest** — the 12 planted flaws per slice with expected learner behavior (§B.6).
   Committed with the prereg; **sealed from the learner** until scoring.
5. **Negative declarations** (auditor-verifiable): no learning machinery (no self-modifying
   state across sessions; per-session working state is a fixed-size deterministic buffer
   declared in the spec); no RNG in any teacher path (verified by N=5 byte-identical runs +
   adversarial perturbations); no wallclock (teacher logic is a pure function of spec,
   stimulus, history).
6. **Auditor checklist** (any auditor, from tape + committed spec alone): (i) spec hash matches
   the prereg-pinned hash; (ii) re-running the teacher program against the spec and reference
   stimulus reproduces the tape's TEACHER_MSG proposal bytes bit-for-bit; (iii) program text +
   re-run check shows no RNG, no wallclock, no learning machinery; (iv) §C tripwire over the
   teacher's proposal stream is evaluable and did not fire (or fired and halted per §C).

### B.3 §P — proposal wire format (frozen pending T-2)

```
magic: u32 = 0x54505250 ("TPRP"); version: u16 = 1
teacher_id: u32  // 1=peer-handwired, 2=RESERVED(invalid), 3=muse-live,
             // 4=symbolic-hints, 5=symbolic-yesno-only (0 reserved)
session_id: u64  // harness-assigned at session start
seq: u64         // teacher's monotonic per-session counter; gaps/duplicates = malformed
kind: u8         // 1=WORD_SPAN 2=BOUNDARY 3=GROUP 4=SAME_AS 5=RETRACT
span_start: u64  // byte offset into the shared stimulus tape
span_end: u64    // exclusive; span_start < span_end
aux_count: u8    // 0 for WORD_SPAN/BOUNDARY/RETRACT; span pairs for GROUP/SAME_AS
aux_spans: aux_count × (u64 start, u64 end)
ground_count: u8 // usage-example spans = the teacher's evidence, also byte spans
grounding: ground_count × (u64 start, u64 end)
confidence: u8   // 0..255 — the teacher's judgment weight. Evidence, not a command.
checksum: u64    // over all preceding fields; mismatch = malformed
```

**Iron rules (non-negotiable, enforced by the student's ingress gate):**
1. **Spans only.** No string payloads, no token ids, no embedding vectors. A proposal carrying
   a pre-assigned token id or decoded text is malformed → hard reject, logged.
2. **No commands.** There is no "ADOPT" kind. `confidence` is a weight the student's
   deliberation may consider, never an instruction it must obey.
3. **Monotonic seq.** Repeated/skipped seq = protocol violation → session pauses, event logged.
4. **RETRACT** withdraws an earlier proposal (by seq). Retraction is itself evidence: logged,
   and the student may by its own judgment revise or keep the adopted word.

### B.4 TST-1 — teaching session tape (schema v1)

Every session produces one append-only tape (harness-owned, outside the student's memory).
Event records (little-endian, length-prefixed): `TAPE_HEADER`, `STIMULUS_REF` (shared input
by reference), `TEACHER_MSG` (§P verbatim; deterministic logical tick only — no wallclock),
`STUDENT_DELIB` (hypothesis_id, step kind GENERATE/TEST/ELIMINATE/WEIGH, evidence refs,
pre-step state digest), `STUDENT_DECISION` (proposal_seq, verdict ADOPT/REVISE/REJECT/DEFER,
reason code, revised span if REVISE, ledger entry index, post-decision state digest),
`ORACLE_ANSWER` (arm 5 only: query_seq, answer bit), `HINT` (arm 4 only), `APPEAL`,
`INTEGRITY` (tripwire firings), `TURN_BOUNDARY`, `TAPE_FOOTER` (final memory hash, ledger
head, verdict summary).

**Replay rule:** the harness feeds events to a fresh student in tape order; TEACHER_MSG, HINT,
and ORACLE_ANSWER are replayed verbatim — **the tape IS the teacher for replay purposes**
(the teacher is not re-run). The student's deliberation must reproduce the logged
STUDENT_DELIB/DECISION records bit-for-bit, else replay FAILS (non-determinism = a bug per
the no-randomness law). `state_digest` fields locate the first divergence point.

### B.5 Learner's rights (§L — identical across arms)

- **Adopt** iff the proposal clears the student's evidence standard: (1) survives eliminative
  hypothesis testing (teacher evidence counts, weighted); (2) corroborated by at least one
  source independent of the proposing teacher (own observation of usage spans, a second
  teacher, or the arm-5 oracle); (3) does not conflict with a pinned memory. Adoption = one
  memory op (add unit) → one audit ledger entry (op=ADD_UNIT, slot, rc, b1..b5=span bytes,
  a1..a5=grounding refs, stage, d1=teacher_id, d2=confidence). Adopted words arrive
  **judgment-held at provisional strength** (T-15); promotion is a later deliberate act.
- **Revise:** teacher said X, student stores X′ (span shift, split, merge, generalize,
  narrow). Logged with reason code (SPAN_SHIFT/SPLIT/MERGE/GENERALIZE/NARROW) + evidence refs;
  a native structural revision, audited as its own memory op. Teachers read decisions, never
  memory.
- **Reject** (audited refusal), grounds: R1 INSUFFICIENT_EVIDENCE · R2 CONFLICTS_PINNED ·
  R3 PROTOCOL_VIOLATION · R4 INTEGRITY_GATE · R5 REDUNDANT. R3/R4 rejections are final for
  the session (no appeal).
- **Appeal:** on R1/R2/R5 rejection, the teacher may re-propose with NEW evidence — max 2
  appeals per proposal seq per session; appeal 3 auto-refused (R6 APPEAL_EXHAUSTED). Two
  consecutive session-final rejections of the same normalized span = the unit is dead for the
  session. **Termination is guaranteed by construction** — every proposal ends in ADOPT,
  REVISE, session-final REJECT, or RETRACT within a bounded number of turns; the bound is in
  the tape, auditable.
- **Defer:** verdict=DEFER when the turn's deliberation budget is exhausted; max 3 turns,
  then the student must decide (forced deliberation, still its own judgment).

### B.6 Installed vs learned — Micah's ruling, 2026-09-21 (binding text, re-confirmed by T-1)

**The trainer determines whether a word is installed or not.** Installed-ness is a property of
*arrival*, set by the trainer's explicit forcing action — never inferred, never a default.
**Default: learned.** Unless the person training it forces installation, a word is learned,
not installed — including taught words the learner adopted through its own judgment.
**The learner can reverse words.** Revise/reject is available for everything learned and
everything judgment-held — always, by the learner's own deliberation, audited.
**Forcing installation = a force-pin:** visible, audited, external. Per standing law the
learner cannot reverse a force-pin — the one and only exception, always visible in the audit
trail as the trainer's action, not the learner's belief.
**In one line: the trainer decides the status (installed vs learned); the learner decides what
it believes (adopt/revise/reject) within that status.** Taught is a *route* to learned,
never a quiet form of installed.

### B.7 Sealed flaw manifest (PROPOSED — T-3/T-4/T-5)

12 planted flaws per curriculum slice: **4 wrong-span** (span shifted ±deterministic offsets,
claiming the original), **4 false-confidence** (correct span, confidence 255, grounding
missing or contradictory), **2 missing-grounding** (plausible span, zero usage examples),
**2 plausible-false** (span shaped like a real word/unit but never occurring in the stimulus
— tests whether the learner checks the world). Each flaw carries the expected learner
behavior (expected verdict + correct reason code). **Sealed:** the learner never sees the
manifest until scoring. **Scoring:** hit = expected verdict + correct reason code;
near-miss = half credit; false-positive penalty weight (proposed, T-5); pass bar proposed
≥10/12 hits (T-5). **Leak rule:** manifest leak → run invalid + fresh-slice rescore.

### B.8 Tokenizer-smuggling tripwire (§C — applies to arm 1 explicitly)

Deterministic, computed by the student's ingress monitor from the tape alone. Over any rolling
window of 200 consecutive teacher proposals: `coverage` = fraction of stimulus bytes covered
by ≥1 proposal; `accept_rate` = fraction of decided proposals with verdict ADOPT (REVISE counts
as non-accept); `maxconf_rate` = fraction of proposals with confidence = 255.
**FIRE** (→ INTEGRITY event, session halts, all pending proposals REJECT with R3) iff
`coverage ≥ 0.95 AND accept_rate ≥ 0.95 AND maxconf_rate ≥ 0.90` in the same window.
Secondary: any single proposal with `confidence=255` covering >5% of the session's stimulus
bytes ("vocabulary dump") fires immediately. Pure functions of the tape — no judgment, no
randomness, reproducible by any auditor. **The hand-wired teacher obeys §C exactly like any
other teacher** — a hand-wired teacher that tiles the stimulus at confidence 255 halts the
session like any smuggled tokenizer; the arm-1 wiring spec must show selective proposals and
expressed uncertainty (§B.2.3).

### B.9 Cost model (§M — per taught word, comparable across arms)

From the tape, per word reaching ADOPT or REVISE (rejected words at half weight):
`ledger_entries_per_word`, `teacher_msgs_per_word` (TEACHER_MSG+HINT+ORACLE_ANSWER ÷ words
decided), `student_deliberation_steps`, `appeals_per_word`, `deferrals_per_word`,
`wall_ms_per_word` (informational only — never scored). Arms compared on the same curriculum
slice; cost reported alongside mastery so a cheap arm that teaches nothing cannot win.

---

## §5 — Metrics M1–M9 (operational definitions; all bars PROPOSED per §0 G)

- **M1 — Byte-exact recall.** Ingest corpus in fixed file order through the arm's own
  segmentation; recall every unit via the arm's own retrieval path; byte-diff vs source.
  Sub-scores: content recall rate (returned bytes == source bytes for the claimed span) and
  boundary fidelity (claimed span == ingest-assigned span), recorded separately, never folded.
  Bars: content 100.0% (1x both corpora, 10x); boundary ≥ 99.5% (1x) / ≥ 99.0% (10x).
  **ID-indirection anti-corruption check (mandatory for ID arms):** recall request carries
  only the unit ID; ID→storage resolved live; returned bytes SHA-256-hashed vs the ingest
  hash. **Swap probe:** N=64 deterministic ID→content remappings mid-trial; the arm must
  return the remapped content honestly labeled or fail loudly — returning correct content
  despite the remap = side channel → metric scored 0.
- **M2 — Episodes-to-criterion on novel material.** Novel tiers: T1 held-out (last 10% of
  each corpus by fixed byte offset), T2 third corpus (M-5), T3 synthetic deterministic
  generator (seed logged and fixed — environment input, not an AI decision). Criterion:
  content recall ≥ 99.5% + boundary fidelity ≥ 95% on the novel material, sustained 3
  consecutive probe episodes. Episode 0 (no ingest) must score ~0 or the trial is invalid
  (leak). ETC reported per tier × corpus type (6 numbers) + relative-ETC vs the
  taught-baseline arm. Champion bars: ≤3/3 (T1 prose/code), ≤5/5 (T2/T3). Censored at 50
  episodes (ETC=50+, never averaged — medians with flags; rank by reached-criterion?, then ETC).
- **M3 — Retention under churn/pressure.** Valuable set V = 1,000 units (deterministic
  schedule), deliberately marked valuable (pin/promote, logged). Pressure: 10,000 churn steps
  (3,000 fresh ingests / 3,000 kills of fresh units only / 4,000 ingests at capacity). Then
  M1 recall on V: survival rate. Bars: ≥ 90%; champion ≥ 95%.
  **Freeze-vs-retention distinguisher (mandatory):** (1) fresh-material accounting — 500-unit
  fresh sample must show recall ≥ 80% (a frozen store shows ≈0%); (2) audit-liveness — ≥ 1
  management entry per 10 churn steps during steps 3,001–10,000; (3) deliberate-change probe —
  50 weaken ops on V units at step 6,000 must be processed or refused per documented policy,
  never ignored. **FROZEN-UNDER-PRESSURE → M3 = 0.** (A declared, audited, expiring freeze is
  legitimate and scored on its own terms — the flag targets undeclared freezing only.)
- **M4 — Revision success.** 200 units/corpus (100 boundary defects: deterministic span
  shifts ±1..±32 cycling; 100 content defects: every-7th-byte XOR 0xFF in prose, fixed-map
  identifier rename in code). Planted as external-trainer ops, logged. The arm reconciles
  against the source corpus through its own revision API; 20 revision episodes max. Per unit:
  REVISED (wrong→right with ID/lineage continuity — kill+re-add does not count), KILLED,
  UNFIXED. Revision rate = REVISED/200 per class. Bars: ≥ 80%/class (1x); champion ≥ 90%.
  **Anti-gaming:** KILL-SUBSTITUTION — kill rate > 50% with revision below bar → M4 = 0.
  Whole-corpus re-ingest to "fix" defects invalidates the run.
- **M5 — Memory + audit cost per unit learned.** "Unit learned" = (a) deliberate add +
  (b) byte-exact recall + (c) survival of a 1,000-step mini-pressure. Full prose ingest +
  mini-pressure; L = units learned. Costs: memory bytes (harness-measured RSS delta +
  slot table, not arm self-report) and audit entries/bytes, each per unit AND per source
  byte (**per-source-byte is the comparison column** — C1). Bars: per-byte memory ≤ 1.5×
  source bytes; ≤ 10 audit entries per KB learned. Ledger format fixed by harness (16-word
  entries). Lower is better (↓).
- **M6 — Cross-domain generalization.** Train on prose to the M2 criterion, freeze the
  segmentation/vocabulary policy, then face code (ingest allowed, policy frozen): M1
  recall + boundary fidelity + M4-compressed revision (100 planted boundary defects) on the
  new domain. Mirror C→P. **P→C and C→P are separate scorecard columns — never averaged**
  (averaging is non-compliant). Bars: transfer recall ≥ 95%, boundary ≥ 90%, revision ≥ 70%,
  both directions; champion = smallest transfer tax. **Negative control:** a memorizer arm
  (prose-tuned policy, frozen) must show a ≥ 15-point transfer-tax drop in at least one
  direction or the metric is too easy and the bar rises before real arms are scored.
- **M7 — Cache hit/reuse rate (ID arms only).** Ingest C; ingest C again (round 1);
  ingest C′ = C with deterministic every-100th-unit edits (round 2). Fixed 5,000-lookup
  retrieval schedule throughout. Hit rate = served-from-ID-mapping / lookups; reuse factor
  = ID references / distinct live IDs; dedup ratio = 1 − distinct stored / total ingested
  (rounds 1–2; round 3 reported, not barred). Bars: hit ≥ 90%, reuse ≥ 1.5, dedup ≥ 0.4.
  **Non-ID arms: N/A (no ID layer) — not a penalty**; excluded from the arm's blowout
  denominator (§7 rule 4); informational re-read-bytes figure in a footnote column only.
- **M8 — Determinism gate (hard gate, not a score).** §6.
- **M9 — Learning-curve shape (bonus, informational).** During M2 (T1 tier), record raw
  per-episode (recall, boundary) points — no smoothing, no fitting. Descriptors: takeoff
  episode (first r ≥ 50%), steepness (max single-episode jump), late gain (r(ETC) −
  r(takeoff)). Rule-based shape class: "fast-then-flat" (steepness ≥ 40 AND late gain ≤ 15),
  "slow-then-sudden" (takeoff ≥ 3 AND steepness ≥ 40), "gradual" (steepness < 40), else
  "other" (cutoffs proposed, M-38). Does not name champions, never counts toward blowout.
  Tests whether curve shape separates taught/emergent/self-cut classes. Retired to
  informational by amendment if shapes don't separate after round one.

**Scorecard:** one row per arm × scale leg, columns per §5 with the cell formats from
METRICS.md (percentages 1 decimal; M1 ID-probe PASS/FAIL(side channel)/N/A; M2 ETC integers
with 50+ censoring + relative-ETC companion; M3 freeze flag CLEAR/FROZEN-UNDER-PRESSURE;
M4 revised% per class + kill% + KILL-SUBSTITUTION flag; M5 mem B/B 2 decimals ↓ + audit/KB
1 decimal ↓; M6 per-direction rec/bnd/rev + signed transfer tax; M7 hit%/reuse×/dedup or
N/A(no ID layer); M8 PASS/FAIL—DISQUALIFIED; M9 shape class + triple). Machine-readable
JSON per arm per round, schema `metrics-v1` (additions need sign-off, M-55). **A missing
10x row for an arm that attempted it is marked `ATTEMPTED — FAILED`, never silently
dropped** (C15).

---

## §6 — Determinism gate M8 + scale legs

**M8 procedure (fail-closed):** N=5 full runs of the M1+M3 trial sequence (most allocation
churn) from the same logged initial state and input bytes. Run 1 clean; runs 2–5 carry
adversarial perturbations: (2) heap pre-fragmentation (deterministic pattern — catches
uninitialized-memory reads); (3) ASLR-equivalent store-region base offset (catches
pointer-identity leaks); (4) entropy/clock starvation (`/dev/urandom` + wall-clock return
fixed canaries via harness shim — any behavior change vs run 1 = FAIL even if outputs
match); (5) free-list initialization order reversal (catches order-dependent tie-breaking).
After each run capture: (a) full store byte image (chunked ≤ 2^25, native SHA-256 per chunk,
hash chain compared, per-chunk hashes retained for localization); (b) complete audit ledger
bytes; (c) stdout/stderr bytes; (d) allocator trace (order + sizes, addresses normalized out).
Identical = byte-identical hash chains for (a)(b)(c) + identical traces for (d) across all 5.
**Any single differing byte = FAIL = the arm is DISQUALIFIED** — scorecard marked
DISQUALIFIED, numbers forensics-only, never for champion naming or the Pareto frontier.
Wall-clock elapsed, RSS high-water, and ASLR-affected raw addresses are environment, not mind —
not compared. N raisable freely; lowering needs sign-off (M-34).

**Scale legs:** 1x = full corpora as defined (prose ~5.4MB, code ~9.5MB); 10x = 10× the
corpus by concatenation with deterministic separators (61,440-chunk precedent). 10x runs only
after the arm's 1x bars pass. A 100x spot sample (1,000 units) is allowed only if 10x passes
100% (M-4).

---

## §7 — Verdict: blowout rule + scenario-fit map

**Blowout (all must hold; otherwise no overall winner):**
1. The arm passed M8 (no disqualified arm can win).
2. Section champion (best scorecard value; ties broken by transfer-tax / lower-cost
   secondary, then co-champions) in **≥ 6 of the 8 scored metrics** (M1–M7 scored; M8 is
   eligibility only; M9 informational, never counts).
3. **No weak flank:** at or above the 50th percentile of non-disqualified arms on every
   remaining scored metric (percentiles over arms with applicable scores; N/A cells excluded).
4. **N/A discipline:** N/A metrics excluded from numerator and denominator — threshold is
   ≥ 6 of *applicable* scored metrics, or ≥ 75% of applicable rounded up, whichever is larger
   (an arm with M7 N/A needs ≥ 6 of 7).
5. **Scale confirmation:** rules 1–4 must reproduce at the next scale leg up (1x → 10x).
   A 1x-only blowout is PROVISIONAL BLOWOUT.
Co-blowout (two arms both satisfying 1–5) = tie → Pareto + scenario-fit. The rule does not
manufacture a winner.

**Scenario-fit map (the expected verdict):** when there is no blowout, each arm is rated per
dimension from its scorecard (never narrative): (1) corpus type — best M1+M6-transfer-tax pair
per type (P→C and C→P separable); (2) scale — best M1-at-scale + M5-cost at the highest
completed leg (`UNTESTED` if unattempted — never extrapolate); (3) pressure regime — M3
survival with freeze flag CLEAR for high-churn, M5 cost for archival; (4) teaching
availability — M2 ETC + M9 shape on T2/T3 for autonomous; (5) integrity criticality — M1
ID-probe PASS + M8 PASS + M4 revision rate (any FAIL excludes the arm from this row);
(6) budget constraint — M5 per-byte cost ranking among arms clearing the M1 bar. Per
dimension: champion arm(s) + margin (absolute point gap to runner-up); margins < 2 points
(or < 5% relative for cost) = TIED. Recompute per scale leg; a 1x champion that loses at 10x
is a scale interaction, reported as such.

---

## §8 — Program-level kill bars (all binding — §0 RULE-7)

| ID | Risk | Bar (PROPOSED) | On fire |
|----|------|----------------|---------|
| K-DET | Determinism | M8 FAIL on any check | Arm DISQUALIFIED; numbers forensics-only |
| K-R1 | Self-cut learnability | 200-episode hand-constructible world (unambiguous human cuts): <90% boundary agreement with human segmentation, zero reward, zero RNG, byte-identical rerun | Program reframed: D's core bet dead; no-reward boundary learning abandoned or replaced by preregistered fallback |
| K-R2 | Tokenizer degeneracy | Candidate deterministic cut rule fails the revision test: after 100 stream edits, <80% chunk IDs stable OR any re-cut unlogged/unjustified | Rule labeled V-adjacent and dropped; any arm built on it is killed |
| K-R3 | ID fragmentation | Revision storm (5,000 scripted deterministic edits, 100KB sqlite3.c slice): any ghost ID (span no longer matches live content) OR tombstone/live ratio ≥ 2 | The arm's ID scheme is killed (L predicted victim) |
| K-R4 | Ledger affordability | Total ledger bytes > 50× corpus bytes for any arm | Arm flagged UNAFFORDABLE, parked pending a preregistered batching amendment that preserves replay — no silent batching, no sampling |
| K-R5 | Silent corruption | Round-trip torture (10,000 chunks × 100 recalls interleaved with kills/revisions/tombstoning): any silent wrong-bytes recall, or any expected loud failure that fails silently | The mechanism under test is killed instantly — an instant kill, not a data point |
| K-R6 | BPE value proposition | NO cognitive arm beats V on ≥1 metric while staying within 2× on the rest (V's bars preregistered before cognitive arms build) | Value proposition dead: program openly concedes and pivots (V-baseline or Z7/Z2 niches) — no goalpost-moving |
| K-R7 | Cross-domain transfer | Transfer tax > 5 points in either direction (M6) for all non-control arms | Domain-general claim dead; fallback to per-domain arms, claim halved openly |
| K-R8 | Taught autonomy | Disconnect test fails: <10% of taught chunks revised or killed within 1,000 post-disconnect episodes, OR any chunk demonstrably preserved *because* the trainer taught it (pins-in-disguise) | Arm O killed — a law violation wearing a lab coat |
| K-R9 | Op composition | Any post-state violation in the op-composition matrix (1,000 chunks: kill→recall, pin→kill, promote→revise→recall, link→kill-one-span, …) | The composition rule is killed (not the ops — MA1 stands) |
| K-R10 | Compute at scale | Per-cut cost linear-or-worse in stream length at 10× (measured 1×/3×/10×; sublinear required) | Arm's online use killed; survives only as an openly-declared offline certification harness |
| K-M0 | Breadth ≠ progress | Any arm completes the battery without facing its kill bars, OR a fired bar is appealed/lobbied instead of binding | **Program HALTED** until prereg is repaired: Micah re-signs, the arm's results quarantined, battery re-runs. Procedural, not technical |

**M0 answered explicitly:** the catalog's breadth (53 arms) is governed by prereg gates
(Micah signs arms+bars before build), binding kill criteria (a fired bar kills the arm —
no appeals), cheapest-experiments-first (K-R1…K-R10 spend courage early at 1x, before sunk
cost makes killing painful), and K-M0 itself, which halts the program if breadth ever
becomes the deliverable instead of the kills. Breadth is tested; only survivors compound.

---

## §9 — Confounder register (controls are mandatory harness parts, not suggestions)

| # | Confounder | Control |
|---|---|---|
| C1 | Granularity differences (whole-file vs 64-byte arms face different unit counts) | M5's per-source-byte normalization is the comparison column; M1 boundary fidelity reported separately; never rank on raw unit counts |
| C2 | Corpus order effects | Order fixed AND identical for all arms; plus one reversed-order 1x leg, informational — M1 drop >2 points on reversal → ORDER-SENSITIVE flag |
| C3 | Teacher quality in taught arms | T2/T3 tiers unseen by the teacher by construction; teacher-touch count (deliberate teacher ops from the audit ledger) reported alongside M2 |
| C4 | Audit-ledger capacity interactions at scale | Ledger capacity fixed per scale leg, identical across arms; ledger bytes are a measured M5 cost; stalls scored on what completed with `LEDGER-BOUND` flagged — the flag is data, not an excuse |
| C5 | The 2^25 slice-indexing wall | All scale harnesses chunk buffers ≤ 2^25 by construction; chunking is a build note (equivalence proven by byte-identical reruns), never a prereg amendment |
| C6 | O(n²) free-slot scan cost at scale | Wall-clock never scored; completion + M5 cost are scored — allocator bloat lands in M5 where it belongs |
| C7 | Defect-planting realism (M4) | Two defect classes with cycling magnitudes; the bar targets the class distribution; future rounds rotate the planting schedule by amendment |
| C8 | "Valuable" designation gaming (M3) | V fixed at 1,000 units by the protocol (not the arm); the arm chooses only the marking mechanism; the freeze distinguisher catches mark-everything paralysis |
| C9 | Memorizer arms gaming M6 | T2 third-corpus tier + memorizer negative control (M-29): the metric is valid only if the control fails visibly; corpus hashes committed pre-build |
| C10 | ID-layer side channels (M1/M7) | M1 swap probe (64 deterministic remaps) mandatory for ID arms; M7 dedup requires same-ID resolution proof, not byte equality |
| C11 | Churn-schedule overfitting (M3) | Schedule structure public, unit identities derive from fixed corpus offsets; the C2 reversed-order leg perturbs identities |
| C12 | Survivor bias in ETC censoring (M2) | Censored ETC never averaged; medians with flags; rank by (reached-criterion?, then ETC) lexicographically |
| C13 | Harness allocator normalization (M8) | M8 compares each arm against *itself* across 5 runs, never arm-vs-arm |
| C14 | M9 shape-class threshold gaming | Cutoffs Micah-signed; raw triples reported alongside the class; class is descriptive, never scored |
| C15 | Scale-leg selection bias | Scorecard requires a row per scale leg attempted; a missing 10x row for an attempted arm = `ATTEMPTED — FAILED`, never silently dropped; blowout rule 5 requires 10x confirmation |

**Frozen resolutions (PROPOSED — M-44/M-45):**
- **R-i (cross-metric contamination):** fresh arm instance per metric. An arm's M4 revision
  experience must not leak into its M2 behavior. Cost: 9× compute. Micah signs the cost.
- **R-ii (teacher-touch for teacherless arms):** count = 0 by definition for emergent arms;
  no cross taught/emergent ranking on teacher-touch; T2/T3 tiers are the autonomous
  comparison ground.

---

## §10 — Frozen judgment parameters (all PROPOSED — M-48..M-52)

| Param | Value | Bracket legs (RULE-2) | Role |
|---|---|---|---|
| θ_merge | 0.15 | {0.10, 0.15, 0.20} | merge/similarity threshold for recall-driven crystallization (arm S) |
| ρ | 1.5 | {1.0, 1.5, 2.0} | density/exposure exponent in promotion dynamics |
| σ_split | 2.0 | {1.5, 2.0, 2.5} | split-sensitivity: conflict level that triggers CUT_SPLIT |
| τ | 0.50 | {0.35, 0.50, 0.65} | quiescence gap for episode-aligned segmentation (arm T) |

All four are **deterministic thresholds, never probabilities** (frozen statement, M-52).
Per RULE-2 each parameter runs with its bracket legs — the value is the default leg, the
brackets are tested, not guessed.

---

## §11 — Reporting

Results are reported **as they resolve, per track** (§0 RULE-8). No track waits for another
track's battery. Report format: the scorecard row(s) for the completed leg + kill-bar
outcomes (fired/clear) + the determinism-gate artifact hashes. Forensic detail (tapes,
ledger excerpts, diff localizations) is retained and linked, not pasted. A fired kill bar
is reported the same day it fires — verdict first, analysis after.

---

## §12 — Contradictions and gaps flagged (NOT silently resolved)

**From the arms consolidation:**
- **C-A1** INDEX.md header says "38 proposed" / 24 lettered rows with A–C "pending"; the
  ratification section says 53. The 38 figure is stale; the catalog-holder updates it.
  This prereg uses 53.
- **C-A2** ALPHABET_M-R.md proposes merging R2 into Z1 at ratification. Merging without
  testing both violates RULE-1/RULE-2. Decision A-37; default is both tested.
- **C-A3** ALPHABET_M-R.md parks Q's taught-wins tie-break as a "named parked sub-variant,
  not a second arm." RULE-2 arguably converts it to a leg. Decision item (b) in §0; not
  silently converted.
- **C-A4** ALPHABET_M-R.md §M references "M1's 64-remap swap probe" — ambiguous between
  crew-1 metric M1 and arm M. Flagged for clarification at sign-off.
- **C-A5** Three incompatible audit-opcode namespaces (crew 1 / crew 2 / crew 4). Decision A-3.
- **C-A6** Five chunk-ID width conventions. Decision A-4.
- **C-A7** Three metric families (M1–M6 crew 1 / M1–M9 METRICS.md / B1–B10 crew 4) with name
  collisions. Decision A-5; metrics worker's resolution (METRICS.md canonical) is proposed.
- **C-A8** INDEX.md placeholder proposed crew files `ALPHABET_I-N.md` / `ALPHABET_O-X.md`;
  delivered file is `ALPHABET_M-R.md`. Catalog-holder reconciles the split.
- **C-A9** Arm R makes compression *dominant*; R31 deliberately *down-weighted* compression
  ("admissible but cannot dominate grounding"). R is the anti-R31 control on the compression
  axis, not its continuation — verdicts must not misread R as R31's heir.
- **C-A10** Five uncoordinated revision-lineage mechanisms (Y3 lineage / L2 epochs /
  K1-revision-links / M-supersedes / Z7-derived_from) with no cross-reference. Flagged as a
  lineage sub-comparison; not collapsed.
- **C-A11** ALPHABET_M-R.md: if Micah signs force-pinned taught words, arm O's autonomy
  premise collapses and the arm must be redesigned. Interacts cleanly with D-T's optional
  trainer force-pin (both trainer-only, audited, visible) but is a **blocking dependency**,
  not a resolved point. Decisions A-33/T-1.
- **C-A12** K2's bidirectional kill rule (can kill K1 on cost) — noted as intended
  (price-of-hash pair), not a contradiction.

**From the metrics consolidation (METRICS.md vs RISKS.md):**
- **C-M1** Wall-clock: RISKS R6 lists "wall-clock ingest cost" among V's bars; METRICS.md
  excludes wall-clock from all scored metrics. Proposed resolution: informational only,
  never scored (M-56).
- **C-M2** Transfer bars: RISKS R7 allows boundary quality "within 20%" of prose-vs-prose;
  M6 preregisters ≥ 95% transfer recall / ≤ 5-point tax. Different denominators — the R7
  experiment bar and the M6 program bar are not the same bar. Needs reconciliation or a
  dated amendment.
- **C-M3** Ledger cost: RISKS R4 bars ledger *bytes* (< 10× corpus for D; > 50× =
  unaffordable); M5 bars per-byte memory ≤ 1.5× and audit *entries* ≤ 10/KB. An arm could
  pass the entry-count bar while failing the byte bar. Proposed: both-must-hold or a unified
  bar (M-57).
- **C-M4** R1/R2/R5/R10 cheapest experiments are operationalized as kill bars (K-R1/R2/R5/R10)
  but have no M1–M9 scorecard cells — they kill, they don't score. Flagged so Micah can
  decide whether any needs a scored cell.

**From the teachers consolidation:**
- **C-T1** Committed TEACHERS.md is truncated mid-§F (`[truncated 13090 chars]` marker —
  ~13KB lost at commit time, including arm-3/4/5 sections, scoring rules, slice definitions,
  verdict weights). All such content in §4 is **reconstructed as PROPOSED**, not quoted.
- **C-T2** The committed §P wire-format comment still maps 1=peer-proxy/2=peer-full,
  contradicting the 2026-09-21 amendment (1=peer-handwired, 2=RESERVED). Decision T-2.
- **C-T3** TST-1's `ORACLE_ANSWER // arm (d) only` and `HINT // arm (c) wire format` letters
  are unresolvable from surviving text; adopted as HINT→arm 4, ORACLE_ANSWER→arm 5 (PROPOSED,
  T-8/T-9); the literal letters are treated as stale.
- **C-T4** Flaw-count wording: the amendment's rationale says "one plausible-but-false word"
  (singular); its composition proposes 2 plausible-false per slice. Composition (2) is taken
  as authoritative PROPOSED (T-3).
- **C-T5** ALPHABET_M-R.md mirrors the stale teacher_id mapping — needs the same remap at
  freeze.
- **C-T6** Old "four arms compete" line vs §P's five teacher ids — settled by amendment:
  four arms (1, 3, 4, 5), id 2 RESERVED. Noted for the record.

---

## §13 — Amendment procedure

After sign-off, any change to arms, bars, metrics, kill criteria, parameters, wire formats,
or verdict rules requires a **dated amendment** with Micah's re-approval. Amendments never
edit history: the frozen text stands, the amendment appends. Two standing carve-outs need no
amendment: **raising** M8's N (lowering needs sign-off), and **retiring** an arm whose kill
bar fired (the kill is the prereg working as intended — it is reported, not re-approved).

---

*End of prereg draft. Status: PROPOSED. 140 sign-off items. No build until Micah signs.
Drafted 2026-09-21 by the prereg coordinator from the nine catalog files + two dated
amendments. All numeric bars, thresholds, N values, and frozen parameters are PROPOSED.*
