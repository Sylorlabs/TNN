# AUTOPILOT BILL — full autopilot audit results

**Frozen prereg:** `../preregs/AUDIT.md` (commit `ea519b66fa9cf61c4f6fcd095ed897e29fbe72fd`,
*before* any Tier-1 measurement below was built). **Date:** 2026-09-23 PDT.
**Law:** zero RNG in anything built here (static `grep -i rng` clean on new
sources); byte-identical reruns ≥3 (SHA256); TMPDIR=~/workspace/tmp_commit.

## Method recap

Each component's load-bearing path was walked (design doc + mechanism
source) and every step marked A (autopilot — runs regardless of judgment),
D (deliberate — judged, audited), H (hybrid — substrate advises, learner
decides). Evidence tiers: **T1** measured here · **T2** committed prior
evidence (frozen prereg + verdict, cited) · **T3** code-analysis estimate
(derivation shown, labeled ESTIMATE).

## The table

| # | Component (path) | What runs on autopilot | Conscious alternative | Autopilot cost | Conscious cost | Intelligence gain (failure class caught) | Verdict | Tier |
|---|---|---|---|---|---|---|---|---|
| C1 | Consolidation `wave3/r27-consolidation/impl/psm.zag` | harness-style arm: scan every 10 episodes, promote on raw exposure `(ver+unv)≥6`, **last-wins slow overwrite**, lowest-confidence eviction | event-driven deliberate arm: CONSOLIDATE at ver≥6 across ≥2 verified contexts, CONDEMN discredited, PREEMPT most-discredited tombstone, every op audited | **3.244 s** / 4880 ep = **0.665 ms/ep**; C3 probe: 128 correct / **128 wrong** / 64 abstain / **64 spurious_slow** | **1.471 s** / 4880 ep = **0.301 ms/ep** (2.2× CHEAPER); C3 probe: **320 correct / 0 wrong / 0 abstain / 0 spurious** | last-wins clobber class: auto's 8 overwrites at step 370 → 32 wrong probes; slow-tier purity 1.0 vs 0.5. Real analog of the 126-byte clobber: silent overwrite of true skills by impostors, no audit record of the decision | **conscious-ify** | T1 |
| C2 | PAM sense gate `senses/` (+`senses_unlimited/`) | single surface feature → verdict, no attention control, no re-sense, no verification. Real instance: RT3's 41 deadpan installs — single-word trope triggers forced JOKING on sincere text | context-agreement check + one bounded re-sense on disagreement (denial-of-perception guard: max 1/item) + punchline verification before INSTALL | 1.0 ops/item (~0.667 µs/item); **37.5% false-install, 12.5% miss** on frozen 48-fixture battery | 3.375 ops/item; **0% false-install, 0% miss**; 0.375 resenses/item | deadpan-install class (RT3's real 41); inattentional-miss class (subtle jokes autopilot misses); ambiguous-stimulus class (verification changes verdict) | **conscious-ify** | T1 (gate); T3 (full pipeline) |
| C3 | KB install gate `kb/autopsy` (KB4) | round-1 contradiction-only install rule | deliberative gate (frozen §6: L1 source track record, confidence-as-weak-evidence, L4 cross-variant conflict → re-deliberate, L8 repetition bonus) | — (rule cost trivial vs sense) | ~4 predicates/fixture ≈ small constant (ESTIMATE) | **NEGATIVE RESULT — the key finding:** the gate is already the Bayes-optimal judgment-only rule and STILL fails: A 41.2% DEGENERATE, B 46.5% FAIL vs ≤15% bar. M1 silent failure: the sense never detected the perturbation, so no conflict exists for any conflict-based rule to catch. Consciousness at the *gate* is insufficient — the *sense* must be verifiable | **needs experiment** (sense-level verification, not another gate tweak) | T2 |
| C4 | info-source ingestion `info-source/src` | facts-only learner: absorbs 12/12 planted falsehoods, catches 0 | corroboration-gated editable search: consult ≥2 sources, install only corroborated | 12/12 falsehoods absorbed, 0 caught | 12/12 caught, 12 true corrections installed, 4 unknowns answered; ~2× source consults (ESTIMATE) | planted-falsehood install class (the scale trial's standing finding: consistent lies absorb at 1.0) | **conscious-ify** | T2 |
| C5 | mixed-web / youtube_ingest `mixed-web/src`, `senses/youtube_ingest` | would-be blind install of percepts | youtube_ingest: READINESS gate — READY (≤10% adv false-install) / GATED (withhold+flag every install) / NOT READY (no ingestion). mixed-web: recorded-envelope sense + external verify | n/a (gated by prereg before any blind run) | withhold+flag per item ≈ 1.1× sense cost (ESTIMATE) | confident-garbage install class (senses rebuild: approach A 59% adversarial false-install behind the shared rule) | **conscious-ify** | T3 |
| C6 | imagination pipeline `imagination/` | broken assembly: R6 affirmations discarded to votes, r12 unilateral REJECT, single-endorse installs, no quorum | fixed assembly: R6 affirm terminal INSTALL, all-item absurdity screen → WITHHOLD, R5 quorum (best≥16 + ≥2 rows) | RT-A 10/32 slip-through installs, RT-B 25/32 valid-logic non-installs | RT-A 0/32, RT-B 7/32 (pure r12-component misses, correctly withheld); pipeline bars M1=1.0/K1=0.0 PASS; +quorum count + screens ≈ 1.3×/item (ESTIMATE) | slip-through-install class (causal fallacies, affirming-consequent, deadpan-absurd on single low-tier endorse) + conservative-withhold class | **conscious-ify** | T2 |
| C7 | dialogue generation `dialogue/dialogue.zag` | fixed morphology/composition pipeline; WE-09 showed morphology gap + composition gap choosing the wrong person | constructed-mode partitions (Micah 2026-09-21, PROPOSED): free elaboration explicitly marked constructed, held in partitions, never committed to belief store without verification | 1 pipeline pass (ESTIMATE) | +mode marking + partition check ≈ 1.5× (ESTIMATE) | constructed→belief leakage class (kill bar: zero leakage of constructed content into factual recall) | **needs experiment** | T3 |
| C8 | self-test verification `self-test/selftest.zag` | external agent orchestration between batteries (the old harness) | deliberative orchestrator: loads manifest, executes, ADJUDICATES each bar itself, ledgered verdicts, ST_DONE structurally blocked unless verdict count == manifest count | external (unmeasured, human-speed) | **0.0127× battery ops (~1.3% overhead)** — measured | silent-skip class: fault-injected skip → `ST_BLOCKED`, no ST_DONE; corrupt battery B5 reported UNRUNNABLE (never silently passed) | **conscious-ify** (already built) | T2 |
| C9 | curiosity substrate `wave3/curiosity-substrate` | — (NEGATIVE control: advisor-only by MEMORY_OPS law — `\|slow−fast\|`+novelty+staleness *advises*, never decides) | n/a | — | score per slot, deterministic | **Real failure citation:** R34's hidden seeded LCG drove 1-in-5 explore flips (all LH runs tainted; remediated → deterministic state-driven rule; RNG verdict: DID-NOT-HELP). The failure class is *advisor promoted to decider* | **keep as advisor** (already conscious) | T2 |
| C10 | exploration choice `wave3/hypothesis-driven-exploration` | — (NEGATIVE: hypothesis registry, propose→derive test→run→keep/discard; ties → lowest index; static no-RNG check in trial evidence) | n/a | — | — | n/a | **already conscious** | T2 |
| C11 | recall selection `wave3/deliberate-recall` | — (NEGATIVE: DECLARE→RECALL→ACT→PIN; Boolean predicate logic P1∧P2∧P3∧P4, no scores, no k, per-trace justification bitmask; τ-sweep falsifier showed no threshold reproduces it) | n/a | — | — | n/a | **already conscious** | T2 |
| C12 | trace composition `wave3/trace-composition/comp.zag` | — (NEGATIVE: SEQ/BRANCH/ABSTRACT with structural preconditions — verified-only, provenance-gated, NOT_PREDICATE refusals) | n/a | — | — | n/a | **already conscious** | T2 |
| C13 | memory ops `wave2/memoryagency/trial/memory_core.zag` | — (NEGATIVE: MA1 deliberate op set — MEM_ADD/KILL/PIN/UNPIN/PROMOTE/DEMOTE, every mutation audited incl. refusals, no background decay; MA1 passed 58/58). The autopilot *ancestor* is R27's harness-written fast/slow tiers ("consolidation happened *to* the system; the system never decided") — the C1 delta is exactly its replacement | n/a | — | — | n/a | **already conscious** | T2 |
| C14 | compaction `wave2` (MEMORY_SAFETY.md) | — **no autopilot compaction found.** MA1 has no compact op; only "the oldest *refusal* ledger entries *may* be compacted on overflow" (MEMORY_SAFETY.md:50) | n/a | — | — | n/a — watch item: if a compactor is ever built, it must be a deliberate op | **n/a (no autopilot)** | inv |
| C15 | structural revision `wave3/native-structural-revision` | — (NEGATIVE: R27 `self_revision_history` shape — proposal → measured → PROMOTE/rollback; CORE KILL structurally refused) | n/a | — | — | n/a | **already conscious** | T2 |
| C16 | ledger gates `wave5/ledger-gating` | — (NEGATIVE: `il_check` as commit gate — fires on contradiction/empty/phantom/trivial provenance/cheat-jumps, silent on honest chains 24/24; failed check → audited HOLD, never silent drop) | n/a | — | — | n/a | **already conscious** | T2 |
| RC | reasoning control | — (NEGATIVE: RC1 passed 40/40 — learner inspects its own verification bar, refuses self-changes weakening integrity, rolled itself back after a lying self-change; TNN controls 100% of reasoning machinery, 0% of constitution) | n/a | — | — | n/a | **already conscious** | T2 |

## Tier-1 measurement detail

**C1 (r27-consolidation).** Pinned toolchain, `trial.zag`+`psm.zag` rebuilt
from source; arm-split copies differ from the committed trial ONLY by the
`while(m<=1)`→`while(m<=0)` / `m=0`→`m=1` const change (no mechanism
change). Per-arm summary lines byte-identical to the original trial run
(diff clean). 3/3 reps byte-identical per arm.

| arm | wall (mean of 3) | episodes | ms/ep | C3 probe correct/wrong/spurious |
|---|---|---|---|---|
| auto | 3.244 s | 4880 | 0.665 | 128 / 128 / 64 |
| delib | 1.471 s | 4880 | 0.301 | 320 / 0 / 0 |

Why conscious is *cheaper*: the auto arm scans the whole slow tier every
10 episodes for lowest-confidence eviction and performs last-wins
overwrites; the deliberate arm exits early on threshold checks and scans
only touched candidates. Deliberation removed work, not just added
judgment. (Fair-fight note: on clean curricula with no impostors the
margin would shrink — the auto arm's cost is dominated by its own
pollution management.)

**C2 (pamgate).** New pure-Zag build (`evidence/scratch/pamgate.zag`,
7747-byte main, compile warning-free, `grep -i rng` clean). Frozen
48-fixture battery (12 deadpan traps / 12 true jokes / 12 plain sincere /
6 subtle jokes / 6 ambiguous), 3000 reps = 144,000 items/arm, in-process
determinism gate + 3/3 cross-process byte-identical (sha256
`20a00491a9f1f21803faacf5160eacbdb2521e2831341ad89e7231aeb14a7485`).

| arm | items | installs | false_installs | misses | ops | ops/item | resenses |
|---|---|---|---|---|---|---|---|
| auto | 144000 | 90000 | **54000 (37.5%)** | **18000 (12.5%)** | 144000 | 1.0 | 0 |
| delib | 144000 | 54000 | **0** | **0** | 486000 | 3.375 | 54000 |

Wall: 0.1922 s mean for both arms (288k items) ≈ 0.667 µs/item/arm.
Fair fight: on the 24 clear fixtures (true jokes + plain sincere) both
arms emit identical verdicts — autopilot is 3.375× cheaper there and
deliberation buys nothing. On the 24 trap fixtures autopilot is
catastrophically wrong (18/24 false or missed) while deliberation is
perfect. Full-pipeline PAM cost (sense stages dominate; gate ≈5% of a
production sense pass): **~1.12× pipeline-level (ESTIMATE)** — the 3.375×
applies to the gate stage only.

## Headline numbers

- **Total bill if everything were conscious-ified:** dominated by the C2
  gate at 3.375× *on the gated stage* (~1.12× pipeline-level ESTIMATE),
  C4 corroboration ~2× ingest consults (ESTIMATE), C7 ~1.5× (ESTIMATE),
  C6 ~1.3×/item (ESTIMATE), C8 1.013× (measured), C1 **0.45× — conscious
  is 2.2× cheaper** (measured). No component exceeds ~3.4× on its own
  stage; nothing is anywhere near the 10× kill line.
- **Top-3 by cost:** (1) C2 sense gate 3.375× ops/item (measured, gate
  stage); (2) C4 corroboration ~2× source consults (ESTIMATE);
  (3) C7 constructed-mode ~1.5× (ESTIMATE).
- **Top-3 by intelligence gain:** (1) C1 consolidation — slow-tier purity
  1.0 vs 0.5, 320/320 vs 128/320 correct (measured); (2) C2 sense gate —
  37.5% false-install → 0%, 12.5% miss → 0% (measured); (3) C4
  info-source — 12/12 planted falsehoods caught vs 0/12 (committed).
- **The uncomfortable finding:** C3 — the deliberative KB install gate is
  already Bayes-optimal on its inputs and still fails at 41–46%. The
  missing information ("was the sense fooled?" vs "did the stimulus
  change?") is not in the gate's inputs at all. Consciousness at the
  install gate without consciousness at the sense is security theater.

## Gaps (not scored)

- **C-g1:** `certrebuild` named in the task brief was not found anywhere
  in the lab tree — could not inventory.
- **C-g2:** reasoning-control internals beyond RC1/RC2 not reached.
- **C-g3:** full-pipeline PAM cost unmeasured (production sense harness
  not rebuilt here) — Tier-3 estimate only.
- **C-g4:** 1GB-ingestion red-team/audit in flight (dispatched 2026-09-23);
  only committed findings cited.
- **C-g5:** prose-learning learn-path walked only via the scale-trial
  install path (4.000 ops / 92 bytes per fact, deliberate install per
  selftest core); no separate autopilot found.
- **C-g6:** perceptual-origins and trace-op-semantics are dead
  workstreams (proven unrecoverable) — not inventoried.

## Artifacts

- `evidence/scratch/pamgate.zag` — Tier-1 source; `pamgate` binary
  **not committed** (binaries excluded); `r1.log` (sha256 above).
- `evidence/scratch/trial_auto.zag`, `trial_delib.zag` — arm-split
  drivers (const-only change from committed `trial.zag`); `psm.zag`
  copied verbatim; `trial_auto_audit.log`, `trial_delib_audit.log`.
- `evidence/scratch/r27_run1.log` — original-trial re-verification run
  (4.563 s wall, numbers match TRIAL_RESULTS.md).
