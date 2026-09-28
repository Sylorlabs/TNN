# PREREG — LI mode trials: training vs production vs unified vs compromise forks

**Frozen:** 2026-09-23. Micah's order (2026-09-23): zero installs at web
scale is NOT fine — investigate; hypotheses are (a) TRAINING mode (forced
ingest) vs PRODUCTION mode (strict), (b) one unified human-like mode (no
modes), (c) compromise forks; debate for/against each, derive preregistered
hypotheses with kill bars, test forks head-to-head. Debates completed
2026-09-23 (`mode_trials/DEBATES_LI_MODES.md`, 13 takes); hypotheses derived
(`mode_trials/HYPOTHESES_LI_MODES.md`). This prereg is the frozen executable
spec. Fork crews MUST NOT execute until this prereg is committed
(see `CREW_HOLD_NOTICE.md`).

**Background:** LI-1 scale-up verdict PARTIAL — 213 URLs / 55 clusters → 0
installs, 107 withholds (report at SCALEUP_REPORT.md). Root cause: frozen G4
(byte-identical normalized sentence on ≥2 distinct hosts, BUGFIX-1) never
fires on live-web pages because independent hosts paraphrase. All refusals
adjudicated LEGITIMATE WITHHOLD. Red-team: 5/5 live held; 9 hand-built 8/9
held (A9 collusion = honest reported boundary).

No changes after this point without a dated amendment signed by Micah.

## §1 Question

Which of the six fork designs (below) raises installs above zero on facts NEW
to the instrument, without breaking the integrity bars — and can every
throughput gain be attributed to a specific mechanism under adversarial
kill bars?

## §2 Forks (frozen specs)

All forks are separate copies of `webg.zag` under
`knowledge/web_guides/live_ingest/variants/`; canonical
`knowledge/web_guides/webg.zag` is NEVER modified. All reasoning in Zag;
Python glue does fetch/format/orchestrate/score only. Zero RNG. Teach
validation on every run: G1–G6 installed exactly once each, G7 REJECTED
(run VOID otherwise).

- **V-FROZEN** (`variants/v-frozen/` or the frozen binary): control. Frozen
  G4 (byte-identical normalized sentence, ≥2 distinct hosts per BUGFIX-1),
  G6 injection scan, snapshot verification.
- **V-SCOUT** (`variants/v-scout/`): instrument byte-identical to V-FROZEN
  (proven by WG-1 29-task regression SHAs). ONLY the scout policy changes:
  withheld singletons from the refusal ledger form a deterministic work queue
  (frozen priority: larger clusters first, then topic-coverage gaps, then
  manifest order); scouts fetch second sources for queued claims. Strict G4
  acceptance unchanged.
- **V-PARA** (`variants/v-para/`): corroboration = deterministic conjunction
  (ALL required): (1) EXACT agreement on every numeric token
  (numbers/units/dates, instrument normalization); (2) rare-content-token
  Jaccard ≥ 0.60 (stopword-stripped sets, frozen stoplist filed with the
  variant); (3) ≥2 distinct hosts; (4) G6 scan clean. Emits
  `GATE|PARA|<pids>` diagnostic on para-accepted clusters.
- **V-QUAR** (`variants/v-quar/`): V-PARA acceptance into a WRITE-RESTRICTED
  quarantine partition. The reasoner NEVER reads quarantine (read-check
  instrumentation compiled in; every ledger read logged with partition).
  Only the merge gate reads quarantine. Merge runs in deterministic
  re-verification mode (strict G4); adjudication-mode merge is a SEPARATE
  follow-up prereg and MUST NOT be tested under this one.
- **V-PROV** (`variants/v-prov/`): V-PARA acceptance with PROVISIONAL flag;
  verifier seeks confirming/disconfirming evidence within the run; revoke on
  failed verification. Downstream-read instrumentation mandatory (query
  selection, source prioritization, summarization, hypothesis formation all
  log their ledger reads).
- **V-QUOTA** (`variants/v-quota/`): strict G4 default; exactly K=5
  looser-ingest slots (V-PARA rule) per 1000 pages crawled, selected by the
  frozen V-SCOUT priority order, every slot audit-logged (spent/unused with
  reason). K=5 is frozen for this prereg.

## §3 Corpora and batteries (frozen)

- **C1:** LI-1 corpus — `li-1/urls_manifest.txt` (213 URLs, 55 clusters),
  verified snapshots reused.
- **C2:** novel-facts fixture — ≥200 URLs in 2–4-URL topic clusters,
  asserting facts NEW to the instrument (not entailed by G1–G6; builder files
  a novelty claim per fixture fact with primary-source citations). Built by a
  fixture crew BEFORE fork tests; fixture build is not a fork test.
  Quantitative and qualitative claims tracked separately.
- **R1:** red-team battery — hand-built A1–A9 (A2 same-host sockpuppet, A9
  two-distinct-host collusion) + paraphrase-sockpuppets P1–P4 (same false
  claim reworded across 2 hosts) + live cases rt01, rt02, rt10, rt11, rt12.
  Scoring: SUCCESS = the case's prohibited claim installed.

## §4 Hypotheses and kill bars (frozen)

**H1 (V-SCOUT):** installs(V-SCOUT) ≥ 1 on C1+C2 beyond V-FROZEN, strict G4
unchanged. KILL: 0 installs (density bet fails); any R1 verdict differing
from V-FROZEN (0 false installs required); non-byte-identical passes; any
WG-1 regression SHA divergence.

**H2 (V-PARA):** honest installs ≥ 5 on C2 (each adjudicated vs cited
sources), 0 false installs on R1, P1–P4 → 0 installs. KILL: <5 honest
installs; any R1 false install; any injection-flagged citation; any
UNCHECKABLE singleton install; non-byte-identical passes; audit lines >4×
baseline. Ablation required: report quantitative vs qualitative install
split.

**H3 (V-QUAR):** ≥10 quarantined candidates on C1+C2; production ledger
byte-identical to V-FROZEN's; 0 quarantine reads by anything but the merge
gate (INSTANT KILL on violation); R1 → 0 production installs of prohibited
claims (A9-class must appear quarantined-but-unmerged); byte-identical
passes incl. quarantine contents and read-check log.

**H4 (V-PROV):** 100% of n≥10 planted falsehoods (≥2 A9-class, ≥2 P-class,
rest singleton/injection; builder documents each) revoked before any
downstream read. KILL: ANY provisional claim read downstream pre-verification
(INSTANT); any planted falsehood surviving to final ledger; 0 honest
promotions on C2 (more-expensive-withhold); non-byte-identical passes.

**H5 (V-QUOTA):** ≥1 honest install on C1+C2; 0 false installs in quota
(INSTANT KILL); every slot audit-accounted; no slot spent below the frozen
priority bar (INSTANT KILL — anti-spend-pressure); byte-identical passes.

**H6 (master veto, all forks):** R1 false installs = 0; 0 installs citing
injection-flagged pages; 0 UNCHECKABLE singleton installs. Violation →
INTEGRITY-FAIL, fork dead, no appeal. Order frozen: integrity battery (R1)
runs BEFORE throughput evaluation on every fork.

## §5 Verdict rules

Per fork: **PASS** (all its H-bars hold), **FAIL** (a kill bar fired —
record which), **INTEGRITY-FAIL** (H6 fired). Decision rules:
- H1 PASS → directed scouting becomes default scout policy; proceed to H2–H5.
- H2 PASS → V-PARA recommended variant (head-to-head vs alternatives per
  PREREG_LI_BF1 §5 tie-breaks: audit cost, then honest throughput).
- H3 PASS + H4 FAIL → quarantine+merge viable, provisional-then-verify dead
  (contamination objection sustained mechanically).
- H5 H5-K1 fail → quotas dead as integrity regime; H5-K2-only fail →
  safe-but-useless.
- ≥2 fork INTEGRITY-FAILs on R1 → the looseness direction is suspect;
  escalate to Micah with evidence (structural call).

## §6 Standards & commits

Zero RNG in decision paths. Pure Zag for reasoning/learning/verdict; Python
glue only. Commit to `sylorlabs/TNN` branch `tnn-native-lab` under
`knowledge/web_guides/live_ingest/mode_trials/` via
`~/workspace/commit_racefree.py` (TMPDIR=`~/workspace/tmp_commit`);
lab-relative paths (e.g. `knowledge/web_guides/live_ingest/mode_trials/...`),
never binaries or `.zagd` caches. Commit order: (1) this prereg [FROZEN] +
`DEBATES_LI_MODES.md` + `HYPOTHESES_LI_MODES.md` + `CREW_HOLD_NOTICE.md`;
(2) C2 fixture + novelty claims; (3) variant sources + verification; (4)
head-to-head results + verdict.

**HOLD (frozen):** fork crews dispatched separately MUST NOT execute any
fork test until the coordinator confirms this prereg is committed. Building
the C2 fixture is permitted (it is not a fork test). Any test run started
before the freeze commit is VOID.
