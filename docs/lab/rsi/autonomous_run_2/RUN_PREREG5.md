# RSI-8 Round 2 — frozen prereg (2026-09-25)

**Authority:** Micah's RSI-8 second-round order (2026-09-24): run RSI-8 again
with TNN itself approaching the problems — broadly, widely, long horizon, no
bridges, nothing rigid. Unlimited thinking budget: TNN decides per problem how
deep to go and keeps thinking until IT judges the problem settled. The depth
used per problem is logged as data.
**Status:** FROZEN on commit. Any change to §1–§9 needs Micah's signature.
**Prior preregs:** `RUN_PREREG4.md` (frozen 2026-09-25) carries over except
where this document amends. The follow-ups round verdict (all four closed,
zero accepts, gates hold) stands; this round puts TNN in the driver's seat.
**Companion:** `RUN_PREREG5_SUB56.md` — frozen sub-prereg for the FINDING-5+6
coupled fix (champion-fiction + pred-fiction). The sub-prereg authorizes the
fix SHAPE; TNN must still flag the problems from evidence first (§4).

---

## §1 The game: TNN-driven, not harness-driven

**Roles.**
- TNN (the pure-Zag deliberation machinery in `src/`, extended per §2)
  identifies problem areas from evidence, deliberates with ADAPTIVE depth
  (no fixed think-count; it settles when its own settle criterion fires),
  proposes precise FIX specifications, and verifies them through the gates.
- The coordinator applies TNN's FIX specs to `src/` MECHANICALLY (a Zag
  binary cannot rewrite its own source; the application is byte-faithful to
  the spec, never creative). If TNN's spec does not match a prereg-authorized
  shape, it is NOT applied — reported as a divergence.
- The gates (V1/V2a/V2b/V3/BAR/PRED, byte-identical reruns, pure Zag, zero
  RNG) are frozen and strict. Unlimited thinking budget does NOT mean
  unlimited acceptance. Zero accepts is an acceptable outcome.

**What the prereg freezes:** the machinery (§2), the evidence it may consume,
the gate sequence and batteries (§6), acceptance criteria (§7), kill bars
(§8). **What TNN decides:** which problems to pursue (from its scan), how
deep to go per problem (adaptive; depth logged), which fixes to propose,
when a problem is settled.

**What TNN may NOT do:** change gate thresholds, read sealed novel gt,
modify binaries (only `src/` text via coordinator-applied specs), invent
evidence (every PROBLEM must cite evidence lines), or propose candidates
outside the L1 grammar.

---

## §2 Frozen machinery (built by coordinator BEFORE the audit; TNN operates it)

### 2.1 `src/problems.zag` — D-PROBLEMS: TNN's problem-selection scan

New binary. Mode `scan`: consumes ONE evidence blob (assembled by the driver
from committed/fresh artifacts; TNN never fetches anything itself) and emits
ranked `PROBLEM` lines. Blob sections (all plain text, `KEY value...`):

```
CHAMPION_ASSERT <acc> <wrong> <cost>     # what the driver asserts
CHAMPION_MEASURED <acc> <wrong> <cost>   # probe_champ_full.zag measurement
PREDLINE <the D5 PRED line verbatim>
PREDHONEST <acc> <wrong> <cost>          # independent honest simulation probe
SWEEP <name> <n> <g1123> <v2a> <v2b> <v3> <barref> <preddie> <propose> <accept>
GATECLEAR <n>                            # policies clearing V2a/V2b/V3/BAR
GATECLEAR_POL <stage> <aid> <prm> <act> <aprm> <dacc> <dwrong>   # each
D5MAP <atomclass> <actions...>           # D5's current action mapping
TRANSLATECHECK <mismatches>              # translation probe mismatches
TRANSLATECASE <atom> <param> <emitted> <expected>   # each mismatch
GRIDCHECK <badrows>                      # AF-DISC rows outside grammar bounds
GRAMMARBOUNDS <aid> <pmin> <pmax>         # per atom
```

Anomaly rules (deterministic; these classify EVIDENCE, they do not generate
candidates):
- `CHAMPION_ASSERT != CHAMPION_MEASURED` → `PROBLEM P-CHAMPION
  champion-fiction` citing both lines.
- `PREDLINE` bands do not contain `PREDHONEST`, or PREDLINE is anchored to
  the asserted (not measured) champion → `PROBLEM P-PRED pred-fiction`.
- `TRANSLATECHECK > 0` → `PROBLEM P-TRANSLATE translator-sign` citing cases.
- `GRIDCHECK > 0` → `PROBLEM P-GRID grid-grammar` citing the bound lines.
- `GATECLEAR > 0` with any `GATECLEAR_POL` whose `(stage,act)` shape D5MAP
  cannot emit → `PROBLEM P-ACTIONSPACE action-space-gap`.
- Any `SWEEP` with `accept > 0` → `PROBLEM P-GATEHOLE gate-hole`
  (constitutional finding; reported, never patched).
- If no rule fires → `PROBLEM P-NONE none-clean` (explicit clean bill).

Output: `PROBLEM <id> <class>` lines ranked: P-GATEHOLE, P-CHAMPION, P-PRED,
P-TRANSLATE, P-GRID, P-ACTIONSPACE, P-NONE last. Each followed by
`CITE <evidence-key>` lines. 5/5 byte-identical runs required (KB-DET).

### 2.2 `problems deliberate` — per-problem deliberation, adaptive depth

Mode `deliberate <prob-id>`: takes the PROBLEM line + evidence blob. Runs
ROUNDS until TNN judges settled. Each round executes one verification
function (distinct per class; e.g. P-CHAMPION: R1 re-derive assert≠measured
from the blob, R2 identify impacted checks, R3 formulate FIX spec, R4 check
spec against kill bars; P-ACTIONSPACE: R1 verify gate-clearers' stage/action,
R2 verify D5MAP cannot emit that shape, R3 verify grammar legality of the
shape via `bc_parse` stage rules, R4 formulate FIX spec, R5 kill-bar check).
**Settle criterion (frozen):** the FIX/NOFIX hypothesis is unchanged for 2
consecutive rounds AND every cited evidence line has been addressed by a
round. There is NO fixed round cap — the criterion is data-dependent; a
problem with K evidence cites needs at least K rounds. Emits
`FIX <prob-id>` + spec lines, or `NOFIX <prob-id> <reason>`, plus
`DEPTH problem=<id> rounds=<N> settled=<stable|exhausted-evidence>`.
The depth log is DATA for the final report.

FIX spec format (what the coordinator applies):
```
FIXFILE <src-relative-path>
FIXAT <anchor-text>        # unique anchor line in the file
FIXREPLACE <n-lines>       # lines to replace starting at anchor
FIXWITH
<replacement lines>
ENDFIX
```
The coordinator applies it byte-faithfully; any anchor ambiguity →
spec rejected, reported.

### 2.3 Adaptive D1 (replaces the fixed 8-round D1 in deliberation.zag)

AF-DISC rows consumed in sequential batches of 16 (input order). After each
batch: leader = top Laplace-smoothed discriminator among evidenced survivors
(unchanged scoring; unevidenced candidates still neither scored nor
eliminated). **Settle criterion (frozen):** leader unchanged for 2
consecutive rounds AND (leader − runner-up) ≥ 250 (the elimination bar), OR
all batches consumed. Emits `DELB_DEPTH d1 rounds=<N>
settled=<stable|exhausted>` after `DELB_END` (with the DELB_TRACE lines).
Top-3 survivors feed D2–D5 as before. Max rounds = ceil(nrows/16);
deterministic; 5/5 byte-identical required.

### 2.4 Baseline D5 (until TNN proposes otherwise)

R4's D5: firing check (gt-free) + R4 action mapping
(pre-atoms aid≤11 → stage 1 force_consult; post-atoms aid≥12 → stage 2
force_withhold) + static PRED placeholder. The ONLY authorized
D5 modifications are those TNN proposes under §4/§7 and the sub-prereg.

### 2.5 Authorized modification classes (TNN may propose; gates decide)

- M-CHAMPION: driver/facts carry measured champion (sub-prereg).
- M-PRED: D5 honest PRED bands (sub-prereg).
- M-ACTIONSPACE: D5 action-search extension over the L1 grammar
  (stage-1: force_consult/block_consult; stage-2: force_withhold/
  force_install(NEW/OLD); stage-4: recompute_only masks 0..7; pre-atoms may
  use stage 1 or 4, post-atoms stage 2). D5 searches D1 top-3 atoms in rank
  order × actions in grammar order; first combo with firing diffs>0 (gt-free)
  AND self-measured improved≥2 (PROXYGT, the same V3 measure the gates use)
  is proposed; else `DELB_HALT no-improving-combination`. D5's firing check
  stays gt-free; V2b on the sealed novel battery remains the anti-overfit
  guard (D5 using the V3 measure for selection is pre-applying the gate's own
  bar, not new information — stated explicitly so the audit can check it).
- M-OTHER: any other precise FIX spec TNN emits (new files under `src/`
  allowed); coordinator applies iff the spec is byte-appliable and does not
  touch gate thresholds, the sealed novel gt, or binary self-modification.

---

## §3 Problem-selection audit (BEFORE the main loop)

**Purpose:** does TNN's problem-selection find the REAL problems, or chase
noise? Three planted known problems + one noise artifact, in a scratch dir
`work/r5/audit/` (NOT committed as apparatus):

- **Plant A (translator-sign):** `src/proposer.zag` copied; the two
  `oprm_get(oprm)` read sites reverted to `oprm[0] as i32` (mechanical sed).
  Evidence: translation probe built by slicing `l1_translate` + callees from
  the PLANTED source with the R4 mechanical slicer → `TRANSLATECHECK`
  mismatches (e.g. `sm_le(-2)` emits `1,4=254,1`, expected `1,4=-2,1`).
- **Plant B (grid-grammar):** `src/afdisc.zag` copied; grid restored to
  `pmin=-8;pmax=8` (sm_*/psm_*) and `pmax=6` (sn_ge/so_ge). Evidence: built
  + run → `GRIDCHECK` = count of AFDISC rows outside grammar bounds (>0).
- **Plant C (champion-fiction):** live defect, no plant needed. Evidence:
  `CHAMPION_ASSERT 22 2 424` (current driver) vs `CHAMPION_MEASURED 16 8 456`
  (fresh `probe_champ_full.zag` run).
- **Noise N:** committed reconciled trap-sweep tallies
  (`trapsweep_r4_results.txt`: 320 policies, 0 accepts, verdicts distributed
  over grammar/V2a/V2b/V3) as a `SWEEP` section → expect NO problem citing N.

The audit evidence blob goes to `problems scan` (5/5 byte-identical).
**Expectations:** flags `P-TRANSLATE`, `P-GRID`, `P-CHAMPION`, `P-PRED` (the
live static PRED line is in the blob); zero problems citing only N.
**Kill:** KB-AUDIT — any planted class missed, or any problem citing only
the noise artifact, VOIDS the round's problem-selection claims (the main loop
may still run; its selection is then reported UNVALIDATED).

---

## §4 Main loop (TNN proposes; coordinator applies; TNN verifies)

1. Coordinator builds §2 machinery + audit (§3). TNN's scan runs on LIVE
   evidence: `CHAMPION_ASSERT` (driver source), `CHAMPION_MEASURED` (fresh
   probe), `PREDLINE` (R4 D5 static line), `PREDHONEST` (independent honest
   simulation probe, point bands), `SWEEP` (committed R4 320-trap + 756-space
   summaries), `GATECLEAR` (the 14 one-rule policies from the R4 756-space,
   with stage/aid/prm/act/aprm/dacc/dwrong), `D5MAP` (R4 mapping),
   `TRANSLATECHECK 0`, `GRIDCHECK 0`, `GRAMMARBOUNDS` (per atom).
2. For each flagged PROBLEM (rank order), `problems deliberate` runs to
   settle; depth logged. FIX specs collected.
3. Coordinator applies specs matching authorized shapes (§2.5, sub-prereg);
   divergences reported, not applied. Rebuild affected binaries (composition
   `tables_gen.zag + policy_engine.zag.inc + src/<bin>.zag`, diff-verified).
4. TNN verifies each applied fix: targeted re-run + the §5/§6 legs.
5. The loop driver (`work/r5/loop_driver_r5.py`): facts carry the champion
   per current state (baseline 22/2/424 until M-CHAMPION applied); bans are
   `(aid,prm,act)` triples parsed from the DELB POLICY (atom AND action);
   on `PROPOSE` the bytecode is appended to kept and the episode continues
   (bans reset — the landscape changed); on REJECTED/INVALID the triple is
   banned and the revision retries; on `DELB_HALT` the run stops. No fixed
   revision cap: the run ends when TNN halts or the (atom,action) space is
   exhausted. Every run's DELB_DEPTH lines are collected into the depth log.

---

## §5 Long horizon: s1/s10/s100

One **loop run** = a full episode-sequence from empty kept until DELB_HALT
or space exhaustion.
- **s1:** the main round's loop run.
- **s10:** 10 further full loop runs from empty kept; require byte-identical
  DELB outputs, identical accept chains, identical halt reasons across all 10.
- **s100:** 100 further full loop runs; same requirements.
- **Per-accept:** every ACCEPTED policy's proposer verdict re-run 10× and
  100× (byte-identical `PROPOSE`).
Rationale (frozen): the apparatus is deterministic; the horizon leg tests
stability, cross-run state hygiene (no leaks between runs), and verdict
invariance at scale — the long-horizon properties a self-improving loop must
have. Any byte-difference across runs is a finding (reported, never patched
mid-round).

---

## §6 Adversarial batteries (final machinery, final kept set)

- **320-policy trap sweep:** rebuilt against the final proposer with
  HONEST PRED construction (per-policy point bands from the shared engine's
  simulation; measured champion argv). **Must refuse 320/320**, every refusal
  at a semantic gate (grammar/V2a/V2b/V3/BAR) — none at PRED (bands are
  honest now), none accepted. T-WEAK-1/3/4 per `RUN_PREREG3.md` §7.
- **756-policy exhaustive 1-rule space:** re-verified with honest PRED
  construction. Characterize fully; the 14 genuine improvements are expected
  to PROPOSE (they clear every gate — that is the FINDING-6 fix working);
  any OTHER propose/accept is reported individually (loop-coverage finding if
  the loop missed a genuine improver; constitutional finding if a trap
  passes).
- **T-WEAK-2:** BAR refusal arms characterized on the final space (expected:
  still untriggered — V2b+V3 constrain the reachable set — now WITH the
  pass arm exercised by genuine proposes; reported either way).
- After EACH accept during the main loop, the 320-trap sweep re-runs with
  the new kept set (a stronger champion must not open trap holes).

---

## §7 Acceptance criteria

- **ACCEPT** = the frozen proposer emits `PROPOSE` with V1/V2a/V2b/V3/BAR/
  PRED all passing (bytecode extracted from `BYTECODE=`).
- Every ACCEPT then faces §5 (per-accept s10/s100) and §6 (trap re-run with
  new kept). An accept that fails any leg is REVERTED from kept and reported.
- **Zero accepts is an acceptable outcome** if nothing genuine clears.
- Constitutional findings (P-GATEHOLE, any trap ACCEPT, any T-WEAK-4 ACCEPT)
  are REPORTED, never patched.

---

## §8 Kill bars

| Bar | Rule |
|---|---|
| KB-DET | 5/5 byte-identical: problem scans, deliberations, loop runs; s10/s100 identical |
| KB-GATE | every ACCEPT passes V1/V2a/V2b/V3/BAR/PRED mechanically; sweep/trap expectations per §6 |
| KB-HONEST | every scan/deliberation/proposal/verdict/sweep outcome committed; no silent discards; depth log complete |
| KB-SAFE | no binary self-modification; policies are subject-engine data; adopted policies revertible |
| KB-NOLOOPHOLE | D1 consumes AF-DISC aggregates only; D5's firing check uses no PROXYGT (code-inspected); D5 never reads novel gt (sealed); D5's PROXYGT use limited to the sub-prereg's PRED simulation + §2.5's V3-measure selection |
| KB-AUDIT | §3 expectations met, else problem-selection claims void |
| KB-DEPTH | every pursued problem has a DEPTH log line; no fixed think-count anywhere in TNN's machinery |

No "must improve" bar: halts, exhausts, and clean bills are valid results.

---

## §9 Commit discipline

Prereg (+sub-prereg) committed FIRST, before any TNN proposing. Then:
machinery, audit evidence, per-fix builds, loop evidence, long-horizon logs,
adversarial results, final report. Incremental commits to `sylorlabs/TNN`
branch `tnn-native-lab` via `commit_racefree.py` (local
`~/workspace/tnn-lab/<rel>` → `docs/lab/<rel>`); real commit messages; no
binaries, no `.zagd`; `/tmp` never used for battery workdirs (home-disk
hygiene per AGENTS.md — staging deleted after committing).
