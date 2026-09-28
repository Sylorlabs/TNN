# GROK47_OVERNIGHT — memory sector VERDICT SHEET
**Sector:** deliberate memory + consolidation/promotion · **Native partner:** Muse (subagent 50fbbac9) · **Engine:** grok-4.7 · **Date:** 2026-09-21/22 (overnight loop)

Loop: HYPOTHESIZE → PREREG (native records kill bars before testing) → TEST (native Zag via znc) → RED-TEAM (fresh grok calls) → ADJUDICATE (native) → FIX → repeat.

---

## ROUND 1 — hypotheses (grok-4.7, engine), prereg bars (native)

grok call: `/tmp/grok_r1_full.txt` (full text; the bundled `chat.py` hardcodes `max_tokens:16`, so a local wrapper `/tmp/grok_call.py` with identical gateway/auth and configurable tokens was used — logged, not a model fallback).

### H-PinKill (grok)
- **Claim:** A full pin budget admits a new important memory only by killing one revealed-unimportant pin, never by overflow or arbitrary eviction.
- **Targets:** pin budget 16 coupled to kill-on-revealed-unimportant.
- **Prediction (grok):** Pin 16, reveal-unimportant only on slot k, then one new important verify: only k is replaced; Zag reruns match.
- **Kill bar (native prereg):** FAIL if admission occurs with no kill, or a slot other than the revealed-unimportant one is evicted, or the two runs' audit logs are not byte-identical. PASS requires all three.

### H-ContextGate (grok)
- **Claim:** Promotion requires verification ≥6 across ≥2 distinct verified contexts.
- **Targets:** single-context repeat inflation; sub-threshold cross-context sums.
- **Prediction (grok):** 6 verifies in one context do NOT promote; 5+1 across two do NOT promote; 3+3 across two DO promote; reruns match.
- **⚠️ Native pre-test note (recorded before testing):** grok's claim and fixtures may be internally inconsistent. The R27 mechanism document (`wave3/r27-consolidation/CONSOLIDATION.md` §3) states the gate as "ver ≥ 6 **across** ≥ 2 distinct verified contexts". Under the literal reading (total ver ≥ 6 AND distinct contexts ≥ 2), a 5+1 fixture WOULD promote, contradicting grok's fixture prediction. The actual gate semantics will be read from the mechanism before the battery is finalized; the battery tests grok's literal fixture predictions, and any mismatch is reported as a HYPOTHESIS-vs-MECHANISM inconsistency, not hidden.
- **Kill bar (native prereg):** FAIL if either weak fixture (6-in-1, 5+1) promotes, or the 3+3 fixture fails to promote, or reruns diverge. PASS requires all three.

### H-TrustClamp (grok)
- **Claim:** Trust saturates on [-256,256]; a sign crossing alone neither kills, unpins, nor condemns.
- **Targets:** bound wrap; false coupling from sign to deliberate kill.
- **Prediction (grok):** increments above 256 stay 256; decrements below -256 stay -256; a sign flip without revealed-unimportant leaves pin and tombstone unchanged on rerun.
- **Kill bar (native prereg):** FAIL on any wrap/missed saturation, or any kill/condemn/unpin caused by sign flip alone. PASS requires all.

### H-TombRevive (grok)
- **Claim:** Condemned tombstones stay dead under later verifies unless revive is explicitly satisfied; preempt of another key cannot resurrect them.
- **Targets:** condemn/revive/preempt isolation.
- **Prediction (grok):** after condemn, ver≥6 across two contexts WITHOUT revive stays condemned; the same trace WITH revive restores; preempt elsewhere leaves tombstone bytes unchanged.
- **Kill bar (native prereg):** FAIL on spontaneous revive, or preempt mutating an unrelated tombstone, or rerun divergence. PASS requires all.

### H-FreezeLeak (grok)
- **Claim:** Consolidation never consults freeze position; equal candidates break ties by insertion order alone.
- **Targets:** contested freeze ranks leaking into promote/preempt without the strength trial.
- **Prediction (grok):** two Zag runs, strength trial never entered, swap only insertion order of tied candidates: each run promotes the earlier one; reruns byte-identical.
- **Kill bar (native prereg):** FAIL if the later insertion wins, or winners match across swapped runs (should differ), or reruns diverge. PASS requires all.

**Native battery:** `/tmp/g47mem/` — one pure-Zag program `battery.zag` (built from mechanism semantics read from repo evidence, NOT copied trial binaries), run twice per fixture; byte-identity checked by the runner. All five hypotheses tested head-to-head against a single shared mechanism so cross-hypothesis interference is visible.

**Scope note:** this battery is a fresh native probe with its own prereg; it does NOT execute the strength-trial prereg (unapproved, DO NOT RUN constraint respected).

---

## ROUND 1 — results (native-verified)

Battery: `~/workspace/grok47/memory/battery.zag` (imports repo `psm.zag` verbatim, sha a17f7e755…; MA4 semantics re-expressed from `ma4_trial.zag`). Built with znc, **run twice → byte-identical** (`diff` clean). Fixture bug found and fixed mid-round: condemn needs unv≥8 AND age≥8, but age trails unv by one observe (aging runs before admit) — 8 unv observes leave age=7; fixture now uses 10. Documented, not hidden.

| Check | Got | grok predicted | Verdict |
|---|---|---|---|
| S1_F1_PROM (6 in 1 ctx) | 0 | 0 | match |
| S1_F2_PROM (5+1 across 2 ctx) | **1** | 0 | **MISMATCH** |
| S1_F3_PROM (3+3 across 2 ctx) | 1 | 1 | match |
| S2_CONDEMNED (used) | 2 | 2 | match |
| S2_USED_AFTER_VER (6 ver, no revive gate) | **1 (revived)** | 2 (stays dead) | **MISMATCH** |
| S2_NREVIVE | 1 | — | mechanism revives eagerly |
| S2_PREEMPT_VICTIM_ID | 61 (correct tombstone) | — | match |
| S2_TOMB_UNCHANGED (unrelated tombstone, preempt elsewhere) | 1 | 1 | match |
| S2_AGE_DELTA | 1 (observe-path aging only) | — | documented |
| S3_KILLSLOT / S3_ADMITSLOT | 0 / 0 | k / k | match |
| S3_KILL_BEFORE_ADMIT | 1 | 1 | match |
| S3_NKILLS (exactly one) | 1 | 1 | match |
| S3_PINS (budget refilled) | 2 | 2 | match |
| S4A_SCORE / PINNED / ALIVE / UNPIN_A / KILL_A | -20 / 1 / 1 / 0 / 0 | sign flip alone changes nothing | match |
| S4B_CLAMPHI / CLAMPLO | 256 / -256 | 256 / -256, no wrap | match |
| S5_VICTIM_A / S5_VICTIM_B | 71 / 72 | insertion order decides | match |
| S5_SWAPPED | 1 | 1 | match |

**Round-1 verdicts (native voice):**
- **H-PinKill: CONFIRM (fixture-scope).** Full pin budget + one revealed-unimportant pin → exactly that pin unpinned+killed (JUDGE_WORTHLESS), new memory admitted into its freed slot, kill audited before admit, budget refills via the normal pin path. Scope: single-victim, 4-slot fixture; multi-victim selection untested (→ R2).
- **H-ContextGate: REFUTE as stated.** The frozen gate is `ver≥6 && popcnt(ctxmask)≥2` (`psm.zag` line ~288); 5+1 promotes. grok's fixture bar (5+1 must not promote) contradicts the mechanism's plain reading — hypothesis error, not mechanism violation. Whether 5+1 *should* promote is an open design question (→ R2 gate-variant probe).
- **H-TrustClamp: CONFIRM (fixture-scope).** Saturation exact at ±256, no wrap; sign flip via others' revelations, never self-revealed, pre-reap → pinned/alive/untouched. The clamp-boundary checks (S4B) and pin-immunity checks (S4A) are separate sub-claims; both pass.
- **H-TombRevive: REFUTE as stated, PARTIAL.** Tombstone revives on the FIRST verify (audited HOP_REVIVE) — the design intent per R27 doc ("a condemned form that later verifies is restored"). "Unless revive is explicitly satisfied" is a terminology error: the verify IS the revive condition. Preempt-isolation clause CONFIRMED (unrelated tombstone bytes untouched; only observe-path age+1).
- **H-FreezeLeak: CONFIRM.** Preempt victim tie → lowest index = insertion order; swapped insertion swapped the victim. Structural: no rank/freeze-position input exists anywhere in the consolidation decision path (decisions use only ver/ctxmask/unv/age/index; the single "frozen" grep hit is a comment about the slow tier being immutable, line 300).

## ROUND 1 — red-team (gpt-5.6-sol, engine per fallback broadcast) + adjudication (native)

Full text: `~/workspace/grok47/memory/sol_redteam_r1.txt`. 15 attacks, adjudicated:

| Attack | Adjudication (native) |
|---|---|
| A1 PinKill underpowered (2-slot) | **PARTIALLY SUSTAINED** — single-victim scope confirmed; multi-victim selection untested → R2 |
| A2 kill-then-admit vs free-slot allocator | **PARTIALLY SUSTAINED** — "no other slot touched" confirmed; admit-slot identity is fixture-determined (store was full) → scope caveat recorded |
| A3 budget refill bookkeeping | **PARTIALLY SUSTAINED** — "refill" is the normal pin path gated on pins<budget at admit, not a special policy → wording fixed |
| A4 ContextGate: misread vs violation | **SUSTAINED** — hypothesis misread; code's plain reading promotes 5+1; not a mechanism violation |
| A5 5+1 as real mechanism bug if intent was balanced support | **OPEN DESIGN QUESTION** — intent needs a prereg decision; → R2 gate-variant head-to-head probe (probe-only, not a mechanism change) |
| A6 ctxmask collisions/stale bits (1<<ctx, ctx≥32) | **SUSTAINED** — genuine robustness edge → R2 native probe |
| A7 clamp boundaries not validated by score scenario | **REFUTED** — S4B validated boundaries separately; attack misread battery structure |
| A8 pin bypass vs trust | **SCOPE NOTE** — sign-flip-alone claim confirmed as stated; victim-selection on signed scores already covered by MA4 trial evidence (30 vs 9) |
| A9 revive terminology vs mechanism bug | **SUSTAINED** — verify IS the revive condition per R27 design; hypothesis terminology error. Eagerness (1 verify vs 8 discredits) → R2 lifecycle probe |
| A10 preempt isolation too narrow | **REFUTED** — field-by-field comparison covered all 9 slot fields; age+1 documented as observe-path; history/counter appends are the audited op itself |
| A11 revive timing/order artifact | **SCOPE** — deterministic order, not artifact; lifecycle loop (re-condemn after revive) → R2 |
| A12 freeze under another name | **NOTED** — specific claim (no rank input to consolidation) stands structurally; decision inputs enumerated |
| A13 swapped insertion alters more than index | **REFUTED** — serialized candidate state was equal (unv=10 both); victim scan uses only (used==2, unv) → index |
| A14 byte-identical ≠ universal determinism | **CAVEAT RECORDED** — determinism claim scoped to fixtures; scale determinism rests on the trials' own rerun evidence |
| A15 small fixtures suppress scale interactions | **SUSTAINED as scope** — all CONFIRMs labeled fixture-scope; architecture-scope rests on original trial evidence |

**Fixes landed (round 1):** fixture off-by-one (condemn needs 10 unv observes, not 8); S2 preempt-victim now read from the audit log (was reading post-state slot id); S3 kill-before-admit now compares against the 5th ADMIT (was the 1st). Battery re-run twice, byte-identical, all checks above are post-fix.

## FALLBACK LOG (memory sector)

1. **2026-09-21 ~23:10 PDT — bundled `chat.py` token cap (native finding).** The ExperientialLabs `chat.py` hardcodes `"max_tokens": 16` — every grok-4.7 call through it truncates at ~16 tokens (~50–90 bytes). This is a SKILL defect, not model degradation: a local wrapper with identical gateway/auth and `max_tokens=900` returned a complete 314-word hypothesis set from grok-4.7 at 23:15 (`~/workspace/grok47/memory/grok_r1_full.txt`). The coordinator's 23:16–23:25 "truncation" probes used the capped `chat.py`; the truncation signature matches the cap exactly. **Recommendation to coordinator: fix or replace `chat.py`'s max_tokens before declaring grok-4.7 degraded.**
2. **2026-09-21 23:31 PDT — grok-4.7 HARD DOWN: HTTP 429 insufficient_credits** (org balance $-0.02; "Add credits at platform.experientiallabs.ai/credits"). Substantive generation stays on gpt-5.6-sol per broadcast; grok-4.7 unusable for any output until topped up. **Needs Micah's action (spending) — not attempted (standing law: no external/irreversible actions).** Hourly re-probes will fail until then; next probe ~00:30 PDT.

## ROUND 2 — queued (native)

- **H-CtxMask** (from A6): ctx ids ≥32, aliased bits, stale ctxmask bits — does the gate misbehave? Kill bar: any promote/deny that contradicts the (ver, distinct-external-context) intent, or a crash/hang.
- **H-ReviveCost** (from A9/A11): condemn → 1-verify revive → re-discredit → re-condemn lifecycle; quantify the discredit/verify asymmetry; adversarial resurrection cost. Kill bar: adversary resurrects a condemned form and gets it PROMOTED cheaper than the original condemn cost with no new corroboration.
- **H-GateVariant** (from A5): head-to-head probe — frozen gate (total≥6 && ctx≥2) vs strict gate (per-context minimum) on a fixed adversarial curriculum with lopsided-context impostors. Probe-only; does the strict gate change promotion outcomes? Kill bar: strict gate promotes ≥1 impostor the frozen gate rejects, or vice versa on true skills — report direction, no mechanism change.
- **H-PinKill-Multi** (from A1): 3 revealed-unimportant pins, one new memory — which dies? Lowest-index? All? Kill bar: any kill of a non-revealed pin, or admission without killing.

### R2 prereg (native, before testing)

**H-CtxMask** (sol): gate uses `1<<ctx` into an i32 mask.
- Prediction: ctx=32 aliases ctx=0 (x86 shift-count masking); stale ctxmask bits are never cleared, so early contexts count toward late promotion.
- Native fixtures: (i) 3×ctx0 + 3×ctx32 → expect NO promote if aliased (popcnt=1), promote if distinct; (ii) print raw ctxmask after ctx32 observes; (iii) 6×ctx32-only control; (iv) stale: 3×ctx0, 20 unrelated observes, 3×ctx1 → expect promote (stale bit counts).
- Kill bar: FAIL if ctx32 stays distinct from ctx0 (case i promotes), or the build traps on `1<<32`.

**H-ReviveCost** (sol): 8 discredits condemn; 1 verify revives; then promotion possible; re-condemn after promotion?
- Prediction: condemn → 1 verify (revive) → 5 more verifies across 2 ctx → PROMOTED; 10 further discredits do NOT re-condemn (condemn gated on prom==0).
- Kill bar: FAIL if revive needs >1 verify, promotion is blocked post-revive, or re-condemnation succeeds. (Outcome informs design; changes nothing frozen.)

**H-GateVariant** (sol): frozen gate vs strict per-context-minimum (each used context ≥2) on lopsided impostors. PROBE ONLY.
- Prediction: frozen promotes 8+1, 6+1+1, and 3+3; strict promotes only 3+3.
- Kill bar: FAIL the frozen-side claim if the real mechanism rejects 8+1 or 6+1+1; FAIL the strict-side claim if the strict fn promotes a lopsided case.

**H-PinKill-Multi** (sol): 3 revealed-unimportant pins + 1 new important memory.
- sol prediction: exactly one of the three dies. Native note: MA4 semantics kill EVERY revealed-unimportant slot at revelation time (JUDGE_WORTHLESS), so the mechanism is expected to kill all 3 before the new memory arrives — sol's prediction is expected to FAIL; the test documents actual behavior.
- Kill bar: sol's prediction PASSES iff exactly one dies; otherwise record mechanism behavior (expected: 3 kills at revelation, admit into lowest freed slot, no unrevealed kill). Variant: new memory arrives BEFORE revelations with full store → expect drop, no kill.

## ROUND 2 — results (native-verified)

Battery: `~/workspace/grok47/memory/battery2.zag` (+ `ctx31probe.zag`, `recyc.zag`). All run twice → byte-identical.

| Check | Got | Verdict |
|---|---|---|
| S6_ALIAS_PROM (3×ctx0+3×ctx32) | 0, mask=1 | ctx32 contributes NO bit |
| S6_CTX32ONLY_PROM / MASK | 0 / 0 | `1<<32` = 0 in this build (silent drop, NOT aliasing) |
| S6_STALE_PROM (3×ctx0, 20 unrelated, 3×ctx1) | 1 | context evidence never expires (cumulative by design) |
| S7_CONDEMNED / USED_AFTER_1VER / PROM_AFTER_6VER | 2 / 1 / 1 | revive on 1st verify, promote on 6th |
| S7_USED/PROM_AFTER_REDIS (10 discredits post-promote) | 1 / 1, unv=20 | no re-condemn (prom=1 ratchet) |
| recyc: c1=2, rev=1, c2=1, rev2=1 | — | **re-condemn IMPOSSIBLE: revive sets ver=1, condemn requires ver==0 — a single verify permanently closes the condemn path** |
| S8_FROZEN I1(8+1)/I2(6+1+1)/T(3+3) | 1 / 1 / 1 | frozen promotes lopsided |
| S8_STRICT I1/I2/T | 0 / 0 / 1 | strict per-context-≥2 rejects lopsided, keeps 3+3 |
| S9_NKILLS (3 revealed-unimportant pins) | 3 | sol's "exactly 1" REFUTED |
| S9_ADMITSLOT / PINS / UNREVEALED_ALIVE | 0 / 1 / 3 | admit→lowest freed slot, re-pin; others untouched |
| S9B_ADMIT_FULL / NKILLS | -1 / 0 | full-store admit drops, never kills |
| ctx31 probe: mask=INT_MIN; 6th verify | **timeout (exit 124)** | **HANG: popcnt(INT_MIN) never terminates (arithmetic >>); build-qualified** |

**Round-2 verdicts (native voice):**
- **H-CtxMask: CONFIRMED-in-spirit, REFUTED-in-letter.** sol predicted aliasing (ctx32→ctx0); actual is silent drop (`1<<32`=0). Worse in one way (evidence vanishes without a trace), less weird in another (no cross-talk). ctx=31 → INT_MIN mask → **infinite loop in popcnt once ver≥6** (proven by timeout). The mechanism validates no ctx range. Trial curricula use ctx 0..3 — no trial evidence affected. Fix direction (NOT applied to frozen file): validate/clamp ctx at observe ingress.
- **H-ReviveCost: CONFIRMED + strengthened.** Full lifecycle: 10-discredit condemn → 1-verify revive → 6-verify promote → 10 discredits can't re-condemn. New (recyc probe): re-condemn is impossible even PRE-promotion — condemn requires ver==0 and revive sets ver=1. One verify permanently immunizes against condemnation. Matches R27 doc's "never verified" clause — intended, but the 1-vs-8 asymmetry is extreme and now precisely quantified.
- **H-GateVariant: CONFIRMED both sides (probe-only).** Frozen gate promotes 8+1 and 6+1+1 impostors; strict per-context-≥2 rejects them, keeps 3+3. Design input for the corroboration question; frozen mechanism untouched.
- **H-PinKill-Multi: sol's prediction REFUTED (3 kills, not 1).** MA4 kills are per-memory judgments at revelation time (JUDGE_WORTHLESS), not a global victim choice among pins — there is no "which pin dies" selection; all revealed-unimportant die. Admission is first-fit into freed slots and never kills (full-store admit drops).

## ROUND 2 — red-team (gpt-5.6-sol) + adjudication (native)

Full text: `~/workspace/grok47/memory/sol_redteam_r2.txt`.

| Attack | Adjudication (native) |
|---|---|
| B1 only ctx0/ctx32 tested | **SUSTAINED as scope** — verdict narrowed: ctx=32 directly verified; supported range 0..30 aggregates correctly; outside it evidence is silently dropped |
| B2 1<<32=0 may be defined Zag behavior | **SUSTAINED on attribution** — reframed: the FINDING is mechanism-robustness (no ctx validation), not a compiler defect; observable behavior stands either way |
| B3 hang is build-qualified | **SUSTAINED** — qualified to znc_linux_x86_64_abed8aa1; needs ver≥6 (short-circuit before); no trial used ctx=31 |
| B4 stale bits may be intended cumulative rule | **SUSTAINED** — reframed: context evidence never expires, by design (no decay/window); desirability is a design question tied to the freeze/expiry debate |
| B5 revive-cost fixture narrow | **ADDRESSED natively** — recyc probe: re-condemn impossible pre-promotion too (ver==1≠0); lifecycle fully mapped |
| B6 ratchet vs frozen verdict tension | **REFUTED as tension** — R27 doc scopes condemn to "never verified" candidates; mechanism matches doc; MA4's kill is a separate subsystem |
| B7 comparator narrow | **SCOPE** — labeled probe-only design input, as stated |
| B8/B9 PinKill-Multi scenario reading | **BOTH TRUE** — sol's "exactly one" prediction refuted AND the mechanism's per-memory independent judgment is the intended MA4 semantics; the prediction wrongly assumed a global victim choice that doesn't exist |
| B10 lowest-slot could be first-fit | **SUSTAINED** — admission is first-fit (`ma_empty_lim` analogue); no preferential admit-into-killed-slot; the confirmed claims (no unrevealed kill, admit never kills) stand |

**Fixes/reframes landed:** H-CtxMask verdict reframed per B1/B2/B4; hang qualified per B3; lifecycle completed per B5/B6; PinKill-Multi dual verdict per B8/B9; first-fit noted per B10. No frozen files modified.

## ROUND 3 — queued

- **Ctx-guard fix demonstration (probe-only):** wrap observe ingress with ctx validation (reject ctx≥31 / mask safely); demonstrate the hang and silent-drop disappear on identical fixtures. Does NOT modify the frozen mechanism.
- **Recall organ sweep:** `wave3/deliberate-recall/trial/recall_core.zag` + `recall_trial.zag` (symbolic recall — in-sector, untouched so far). Engine reviews, proposes hypotheses, native probes.
- **Force-pin law probe:** `docs/lab/GROK47_OVERNIGHT/teacher/work/c3s_src/forcepin.zag` — verify force-pin exclusivity (TNN-issued pin → refused) at review depth.
- **MA4 phase-B churn micro-probe:** strict-inequality admission gate (v > vicv) — the one MA4 admission path not yet micro-probed.
- **Grok re-probe:** next ~00:30 PDT (429 billing; needs Micah's top-up — not attempted).

### R3 prereg — recall organ (native, before testing; hypotheses: gpt-5.6-sol)

**H1 Read-Only Recall:** rc_recall never mutates memory state.
- Fixtures: digest store bytes before/after recalls (plain, compose, failed/empty, refused need).
- Kill bar: any store-byte/liveness/attachment change attributable to recall.

**H2 Greedy Composition:** compose returns minimum-cardinality cover; order-independent.
- Fixture: slot0 ops={A}, slot1 ops={A,B}, need reqops={A,B} → greedy picks slot0 then slot1 (2 slots); optimal is {slot1} alone. Permute insertion order → compare.
- Kill bar: greedy uses more slots than an available cover on any deterministic ledger, or permutation changes the result.

**H3 Temporal and Reuse Boundaries:** P4 accepts exactly (now-step)<=max_age; killed slots can't reattach; reused slots don't retain descriptors.
- Fixtures: age deltas max_age-1/max_age/max_age+1; kill attached slot → reattach (expect refused); kill → new memory admitted into same slot → attach new descriptor (observe: d_attached write-once may refuse forever).
- Kill bar: boundary off-by-one, dead-slot attach succeeds, or descriptor leaks across reuse.

**H4 Policy and Agreement Safety:** SAFETY+ANY refused at declaration only; act needs full coverage + unanimous action.
- Fixtures: declare SAFETY+ANY (refused), SAFETY+VERIFIED (ok), ROUTINE+ANY (ok); recall+act with disagreeing action codes → ABSTAIN; missing op coverage → ABSTAIN.
- Kill bar: refusal leaks to permitted pairs, or any uncovered/disagreeing selection acts.

## TOOLING CORRECTION + ESCALATION LOG (2026-09-21 23:35 PDT, coordinator)

**Correction (voided artifacts):** the ~50-90-byte grok-4.7 "truncations" from the first
round-1 hypothesis batch were a TOOLING artifact — stock
`~/workspace/skills/experientiallabs/bin/chat.py` hard-codes `"max_tokens": 16` (line 26,
verified). They were NOT model degradation. Remedy: all grok-4.7 calls must use the fixed
wrapper `~/workspace/grok47/senses/grokchat.py` (default max_tokens 1500, override via
argv[3]) — never stock chat.py. Wrapper mechanics verified 2026-09-21 23:36 PDT
(correctly surfaces gateway errors). Local `grok_call.py` retained only as historical
evidence; `grokchat.py` is the sanctioned path once service recovers.

**Impact on this sector's evidence:** the truncated batch was diagnosed the same night and
RECAPTURED IN FULL before use (`grok_r1_full.txt`, 314-word complete response via wrapper,
2026-09-21 ~23:15 PDT); no verdict in this sheet was ever drawn from a truncated output.
Substantive hypothesis/attack generation moved to gpt-5.6-sol by coordinator broadcast
BEFORE the escalation, so rounds 2 and 3 (both voices, red-teams, adjudications) are
unaffected. Nothing further to recapture; the voided batch is superseded on disk.

**Escalation (grok-4.7 HARD DOWN):** gateway returns HTTP 429 `insufficient_credits`,
org balance `-$0.02` (re-probed 23:30 PDT by coordinator; re-confirmed 23:36 PDT via
`grokchat.py`). Credit top-up needs Micah — not attempted (spending forbidden). Until
top-up, grok-4.7 is unusable even for short outputs. This sector is EXEMPT from hourly
re-probing (coordinator runs that on a cron). Substantive generation fallback:
gpt-5.6-sol via UnoRouter (short prompts, timeout 120, stdout capture) or native
verification. Fallbacks attributable to the max_tokens=16 stock-chat.py artifact are
recorded above as voided tooling artifacts, not model failures.

## ROUND 3 — recall organ (native-verified)

Battery: `~/workspace/grok47/memory/r3/battery3.zag` (+ `battery3b.zag` follow-up).
Both run twice → byte-identical. Staged files: `r3/recall_core.zag` (import line rewritten
to `memory_core.zag`; one-line diff vs repo), `r3/memory_core.zag`,
`r3/substrate/{cl/common.zag,R33_NATIVE_SHA256_V2.zag,R33_NATIVE_IO_V1.zag}` (verbatim copies).

| Check | Got | Verdict |
|---|---|---|
| H1 digest before/after plain, compose, refused recall | D0=D1=D2=D3 | READ-ONLY CONFIRMED (byte-level) |
| H1_N1 (non-compose, no fully-covering trace) | 0 | expected semantics: non-compose needs per-trace full coverage |
| H2 greedy: slot0={A}, slot1={A,B}, need {A,B} | N=2, sel={0,1} | NON-MINIMAL: cover {slot1} exists |
| H2 permuted: slot0={A,B}, slot1={A} | N=1, sel={0} | cardinality depends on index order |
| H2 act (agree) | 9 | acts |
| H3 P4: age 5 / 6 at max_age=5 | pass / fail | boundary EXACT: `(now-step)<=max_age` |
| H3 kill→reattach | 204 refused | dead slot can't reattach |
| H3 kill→reuse slot→attach new descriptor | 204 refused | **REUSE BLINDNESS: no detach path; slot permanently recall-invisible** |
| H4 SAFETY+ANY / SAFETY+VER / ROUTINE+ANY | 201 / 0 / 0 | refusal scoped to declaration pair |
| H4 compose disagree (true compose fixture) | N=2, ACT=-1 | ABSTAIN confirmed |
| H4 compose partial coverage | N=2, ACT=-1 | contributors selected, act abstains |
| D2 greedy-redundant {A}/9 + {A,B}/10 | N=2, ACT=-1 | redundant trace VETOES action |
| D3 same, agree (10/10) | N=2, ACT=10 | agreement restores action |

**Round-3 verdicts (native voice):**
- **H1 CONFIRMED.** Digest over live/pinned/region/tier/value/step/clock identical across
  all recall paths. Strengthened beyond digest: source grep shows ZERO `s.*.x=` writes in
  `rc_predmask` and `rc_recall` — the read-only property is structural, not just observed.
- **H2 minimality REFUTED; order-dependence CONFIRMED.** Greedy index-order first-contributor
  scan is the mechanism's actual objective (read from source); minimum-cardinality was the
  hypothesis's unstated objective. Cardinality of the selected set depends on insertion
  order — a same-information ledger selects 1 or 2 traces depending on which index the
  broader trace occupies.
- **H2×unanimity interaction (new finding):** a redundant trace's differing action code
  vetoes the act (D2: ABSTAIN where the minimal cover would act 10). Controlled pair D2/D3
  isolates disagreement as the cause. Whether "preserve all witnesses" (C7) is the intended
  rationale is a design question; the behavior is now precisely quantified.
- **H3 boundary CONFIRMED** (inclusive ≤, exact; one boundary probed, nonnegative ages).
  **Reuse blindness is a real lifecycle gap:** `d_attached` is write-once with no detach
  path anywhere in the file (grep-verified) — a killed slot's replacement memory can never
  be attached, so the slot is recall-invisible for the RcState lifetime. Not descriptor
  leakage; the inverse — permanent un-attachability.
- **H4 CONFIRMED all cells:** refusal scoped to SAFETY+ANY at declaration; full-coverage+
  disagreement→abstain; partial-coverage→select-contributors-but-abstain; full+agree→act.

## ROUND 3 — red-team (gpt-5.6-sol, C1–C15) + adjudication (native)

Full text: `~/workspace/grok47/memory/sol_redteam_r3.txt`.

| Attack | Adjudication |
|---|---|
| C1 transient/rolled-back mutation | SUSTAINED as scope, then STRENGTHENED: zero store writes exist in the recall path (source grep), so there is nothing to roll back |
| C2 semantic purity overstatement | SUSTAINED — claim labeled byte-level store non-mutation, as stated |
| C3 one pattern only | SUSTAINED as empirical scope; property generalizes by source inspection (index-order loop) |
| C4 minimality depends on objective | SUSTAINED — reframed: minimality was the hypothesis's objective, now refuted; mechanism's objective is deterministic first-contributor scan |
| C5 permutation confound | REFRAMED — the "confound" IS the finding: selection depends on index position, not just trace content |
| C6/C7 redundant veto = intended conservatism / witness preservation | SUSTAINED as design readings — behavior quantified; defect-ness is a design judgment, flagged open |
| C8 disagreement causation | REJECTED — D2/D3 controlled pair (identical but for one act code) isolates disagreement; no confidence/metadata fields exist in rc_act |
| C9/C10 boundary scope / semantic choice | SUSTAINED — one boundary, nonnegative ages; ≤ vs < is a design choice, flagged |
| C11 reuse refusal may be intentional anti-aliasing | SUSTAINED as alternative reading — but no doc states it and no detach/reset path exists; flagged as design question |
| C12 permanence limited to RcState lifetime/APIs | SUSTAINED — qualified as stated; source grep confirms no detach path in the file |
| C13 policy lattice untested | SUSTAINED — tested pairs only |
| C14 distinguish coverage cells | ADDRESSED natively — all three cells probed (D1 disagree+cover→abstain; MISS partial→abstain; D3 agree+cover→act) |
| C15 one build/env | SUSTAINED — standing scope for all native findings |

**Fixes/reframes landed:** H2 verdict split (minimality refuted, order-dependence confirmed);
H1 strengthened to structural (zero-write grep); C8 rejected via controlled pair; reuse
blindness qualified per C11/C12 as behavior-with-open-design-question.

### R4 prereg — MA4 phase-B churn gate (native; queued since R2)

**H-ChurnGate:** phase-B admission requires STRICT inequality v > vicv (fresh signed score
of the min-score victim); ties → lowest slot index.
- Fixture: 32 USER slots, exact fresh scores via trust=[64,0..], feat=desired.
- Sub-cases: v == vicv (expect DROP, no kill), v == vicv+1 (expect kill+admit),
  v == vicv-1 (expect DROP), two slots tied at min (expect lowest index victim).
- Method: `ma4_score` + `ma4_victim_fresh` extracted VERBATIM from
  `wave3/signed-memory-values/trial/ma4_trial.zag` (lines 46-53, 66-76; diff-verified);
  gate body faithfully re-expressed (trial main not importable — duplicate main).
  Labeled as excerpt+re-expression, not verbatim import.
- Kill bar: any admission at v <= vicv, or non-lowest-index victim on ties.

## ROUND 4 — MA4 phase-B churn gate (native-verified)

Battery: `~/workspace/grok47/memory/r4/churn.zag`. Run twice → byte-identical.
Method: `ma4_score` (L46-53) + `ma4_victim_fresh` (L66-76) are byte-verbatim excerpts of
`wave3/signed-memory-values/trial/ma4_trial.zag` (diff-verified); gate body faithfully
re-expresses L343-361 (trial main not importable — duplicate main). Gate condition
verbatim from source L345-346:
`if(ma4_victim_fresh(&g,trust,feat,MA4_SLOTS,&vic,&vicv)==1 && v>vicv){`.

| Check | Got | Verdict |
|---|---|---|
| Victim: 32 slots, min score 10 tied at slots 7,19 | VIC=7, VICV=10 | lowest index wins ties (strict `<` keeps first) |
| v == vicv → attempt | code 10 (0k/1d/0a), LIVE=32 | DROP, no kill — strict inequality |
| v == vicv-1 → attempt | code 10, LIVE=32 | DROP |
| v == vicv+1 → attempt | code 101 (1k/0d/1a), LIVE=32 | kill + admit |
| victim slot after GT admit | live=1, feat=11 | victim slot reused by new memory |
| all pinned, v=999 → attempt | code 10 | no victim → drop regardless of v |

**Round-4 verdicts (native voice):**
- **H-ChurnGate CONFIRMED all sub-cases.** Admission requires STRICT `v > vicv`; equality
  drops without killing. Tie-break is lowest slot index, by construction of the strict
  `<` scan. No-victim → drop path never consults v.
- **Non-atomic replace (new behavior noted):** the gate kills first, then admits only
  `if(ma_add_lim(...)==MA_OK)` — add failure leaves the victim dead with no rollback.
  Success-path wording ("kill victim + admit") stands; atomicity is not provided.

## ROUND 4 — red-team (gpt-5.6-sol, D1–D15) + adjudication (native)

Full text: `~/workspace/grok47/memory/sol_redteam_r4.txt`.

| Attack | Adjudication |
|---|---|
| D1 tie generalization | SUSTAINED as empirical scope; property follows from source (strict `<` retains first/lowest on ties); two-way tie demonstrated |
| D2 negative/INT boundary scores | SUSTAINED — tested 9..81; vicv init INT_MAX noted (all-INT_MAX slots → no victim → drop) |
| D3 eligibility flags | PARTIAL — pinned tested natively; region/live by source inspection (explicit conjuncts in victim fn) |
| D4 ±1 local | SUSTAINED as scope |
| D5 re-expression ≠ actual body | SUSTAINED as method caveat; mitigated — both functions verbatim diff-verified, gate condition quoted verbatim L345-346 |
| D6 code ambiguity | ADDRESSED — single-digit counters, fixed positional encoding |
| D7 no-kill from counter only | ADDRESSED — LIVE=32 unchanged corroborates |
| D8 lowest-free-slot | SCOPED — victim-slot reuse confirmed empirically; "lowest free" by source inspection (`ma_add_lim` first-fit from 0), not isolated |
| D9 transient write/compaction | ADDRESSED by source inspection — no compaction exists; slots never move |
| D10 other no-victim causes | SUSTAINED — only all-pinned tested |
| D11 v=999 not max | SUSTAINED as stated; sufficient for the drop-path claim |
| D12 determinism ≠ correctness | standing caveat for all native findings |
| D13 field freeze during selection | ADDRESSED by source inspection — single-threaded, score-then-immediate-compare |
| D14 kill+admit atomicity | CONFIRMED non-atomic (see verdicts); wording scoped to success path |
| D15 build scope | standing |

## REVIEW — wave10/int-c7s100 organ integration (review level, 2026-09-22 ~00:10)

**o1_memory.zag (O1 deliberate memory substrate):** thin audited wrappers over
`st_memory_core.zag`. Arm B only — strength never gates kill (frozen law); pins,
force-pins, CORE, stage still gate. Amendment-B: serving-trace pins (force=0) expire
after exactly 50 consecutive non-re-serviced ticks (`tick_n-svc>=O1_PIN_EXPIRY`),
re-service resets the clock, expiry is ledgered (`O1_OP_PIN_EXPIRE`) and not rollbackable.
**Verified by source:** `st_force_pin` sets ONLY `forcepin[]`, never `pinned[]` — so the
amendment-B expiry sweep (which iterates `pinned[]==1`) CANNOT lift a force-pin. The
two-array separation is load-bearing and correct; the one true lock survives expiry.
`o1_pin_fraction` per-mille; P3/Q2 alarm at ≥800. Victim legality: live ∧ unpinned ∧
¬force-pinned ∧ ¬CORE; loop CORE slots protected by index (`exclude_lo`).

**o3_consolidate.zag (O3 deliberate consolidation):** state machine
CANDIDATE→CONSOLIDATED / →CONDEMNED→(revive)→CANDIDATE; consolidate once-only per id
(duplicate refused `O3_REFUSED_STATE`); condemn refused on CONSOLIDATED; revive only from
CONDEMNED. **Cross-module semantic difference vs R27 psm.zag:** in O3, a revived id can
NEVER be consolidated afterward (`o3_find>=0` → refuse) — R27's revive→re-verify→promote
lifecycle has no O3 counterpart. Flagged as an integration semantic question, not a bug.
`o3_preempt`: weakest strength, ties→lowest slot; empty pool → audible ledgered refusal
(`O3_REFUSED_NOVICTIM`), never silent. L5: O3 never mutates O1 — selection only, seam
does the killing. `o3_replay_check` rebuilds id→state from audit.

## REVIEW — wave12/strength-rulings evidence (review level; rulings are Micah's)

Summaries explicitly do NOT make the ruling — evidence only, all byte-identical ×2:
- **R3 (implant indexing):** scheme 1 (shift {0,83,166,250,333,416}): 0 collisions, 0 churn;
  scheme 2 (1-index): 1 pressure collision + mechanical churn across 39 closed-form sites;
  scheme 3 (drop to 5): loses an implant, right-censored final window. Evidence direction
  noted; ruling stays with Micah.
- **R4 (overwrite semantics):** (a) direct write succeeds with NO effort gate (90→10) —
  the cheap-edit path Micah's full-erase-price law forbids; (b) literal kill+add refuses
  kill at 109=REFUSED_EFFORT with no partial proceed; (c) fused OVERWRITE refuses at gate.
- **R5 (freeze-vs-retention):** P1 and P2 DISAGREE on the frozen config — P1: PTR=1.000
  (perfectly retained); P2: FAIL on both tripwires. P1's UNEVALUATED fires on healthy B,
  not on frozen C — P1 tracks evaluation coverage, not frozenness. P2 detects the freeze.

### R5 prereg — P1 STRUCT-PROMOTE gate logic (native micro-probe; hypotheses: gpt-5.6-sol)

Scope: the PROMOTE GATE DECISION RULE ONLY, implemented verbatim from
`wave2/ruleslab/PREREG_P1_STRUCT_PROMOTE.md` ("promote iff candidate per-arm success >=
accepted per-arm success on EVERY arm; aggregate improvement with any arm's regression =
rollback"). NOT the full P1 learner (diagnosis/probe-windows unimplemented by design).
Pure integer logic; ledgered (diagnosis, proposal, base, candidate, decision).

**H1 Unanimous dominance:** per-arm >= decides; aggregate never does.
- F1: cand=base+[1,1,1,1] → PROMOTE. F2: cand=base+[10,10,10,-1] → ROLLBACK.
- Kill bar: aggregate-superior one-regression candidate promotes, or all-dominating rejected.

**H2 Equality promotes:** inclusive >=.
- F3: cand=base → PROMOTE. F4: cand=base+[0,0,0,5] → PROMOTE.
- Kill bar: any equal-arm candidate rejected for non-strictness.

**H3 One-arm veto:** single decrement vetoes unbounded gains elsewhere.
- F5: cand=base+[100,100,100,-1] → ROLLBACK, accepted bytes unchanged.
- Kill bar: promotes or mutates accepted.

**H4 Rollback restorative; identity deterministic:**
- F6: after F2/F5 rollbacks, accepted table digest == pre-decision digest; re-fork ==
  accepted. F7: F3 repeated → byte-identical ledger/state across runs.
- Kill bar: rejection mutates accepted, or identical inputs decide inconsistently.

## ROUND 5 — P1 STRUCT-PROMOTE gate logic (native-verified)

Battery: `~/workspace/grok47/memory/r5/p1gate.zag`. Run twice → byte-identical.
Scope: gate decision rule ONLY (verbatim from `wave2/ruleslab/PREREG_P1_STRUCT_PROMOTE.md`);
not the full P1 learner. 4-arm i32 tables.

| Check | Got | Verdict |
|---|---|---|
| F1 +[1,1,1,1] | 1 PROMOTE | unanimous dominance promotes |
| F2 +[10,10,10,-1] (agg +29) | 0 ROLLBACK | aggregate never overrides one regression |
| F3 identical | 1 PROMOTE | inclusive >= confirmed |
| F4 +[0,0,0,5] | 1 PROMOTE | equality on 3 arms + strict on 1 promotes |
| F5 +[100,100,100,-1] | 0 ROLLBACK | one-arm veto vs unbounded gains |
| digests pre/post F2, F5 rollbacks | identical | rollback leaves accepted bytes untouched |
| ledger decisions | 1,0,1,1,0 | sequenced, auditable |
| final BASE | [51,51,51,56] | exactly the three promotes applied |

**Round-5 verdicts (native voice):**
- **H1 CONFIRMED:** per-arm >= on every arm decides; aggregate is not consulted (the gate
  contains zero aggregate arithmetic — source-inspectable).
- **H2 CONFIRMED:** equality promotes (F3); mixed equal/strict promotes (F4).
- **H3 CONFIRMED:** single-arm decrement vetoes +300 aggregate (F5); accepted unchanged.
- **H4 CONFIRMED:** rollback is transactional by construction (decision fully computed
  before any write; no partial commit possible); identity decisions deterministic and
  byte-identical across runs. Note H4's "vacuous promotion" half: identical candidates
  DO promote — the gate cannot distinguish "confirmed" from "unchanged"; whether that
  needs a strict-improvement requirement is a design question for the P1 trial proper.

## ROUND 5 — red-team (gpt-5.6-sol, E1–E10) + adjudication (native)

Full text: `~/workspace/grok47/memory/sol_redteam_r5.txt`.

| Attack | Adjudication |
|---|---|
| E1 aggregate never computed | ADDRESSED — gate source contains zero aggregate arithmetic; behavior follows implementation |
| E2 normalization confound | ADDRESSED — direct i32 comparison, no normalization in gate |
| E3 identical-fields/snapshot | ADDRESSED — tables are exactly 4 i32s; single-threaded eval-then-commit |
| E4 baseline unspecified | ADDRESSED — BASE printed ([51,51,51,56] final); F4's per-arm >= checkable from log+code |
| E5 digest coverage | SUSTAINED as scope — digest covers the complete gate state (4 i32s); ledger printed separately |
| E6 fixture-specific | SUSTAINED — 4-arm i32 domain per prereg; no NaN in integer domain |
| E7 transactional rollback | ADDRESSED — decision computed before any write by construction; digests confirm |
| E8 ledger vs eval order | ADDRESSED — synchronous, ledger appended inside gate after decision |
| E9 parity | standing build-scope caveat |
| E10 universal rule | SUSTAINED — 4-arm domain; zero-arm/malformed out of prereg scope |

### R6 prereg — revive-policy repair comparator (native head-to-head; hypotheses: gpt-5.6-sol below)

Question: the R2 finding (one verify permanently closes the condemn path) is intended
per the R27 doc, but the 1-vs-8 asymmetry is extreme. Head-to-head, probe-only (frozen
psm.zag untouched; P0 = verbatim @import of the frozen mechanism):
- **P0 current:** revive on 1st verify; ver accumulates; condemn needs ver==0 (closed forever).
- **P1 reset-on-revive:** revive on 1st verify but ver/unv/age reset to 0 → re-condemn possible.
- **P2 corroborated-revive:** revive requires 2 verifies; then normal rules.
- Fixture A (true recovery): 10 discredits → condemn; then 6 verifies / 2 contexts (genuine).
- Fixture B (adversarial resurrection): 10 discredits → condemn; then 1 verify; then 10 more discredits.
- Metrics: final state (live/promoted/condemned/re-condemned), verifies-to-revive.
- Kill bar (for "P0 is fine"): P1/P2 show no measurable advantage on B while matching P0 on A.

### Round 6 — revive-policy repair comparator (native head-to-head)

Evidence: `~/workspace/grok47/memory/r6/` — `psm.zag` (canonical, SHA a17f7e755f93bbd4, untouched),
`p1.zag`/`p2.zag` (single-string surgical edits of the revive block ONLY; canonical file unmodified),
`drv_psm.zag`/`drv_p1.zag`/`drv_p2.zag`, `r6p0r1/r2.txt`, `r6p1r1/r2.txt`, `r6p2r1/r2.txt` (all byte-identical pairs),
`sol_r6_hyp.txt` (5/6 predictions).

**API status:** grok-4.7 hard down (429 insufficient_credits, org balance -$0.02) since 2026-09-21 ~23:36 PDT.
gpt-5.6-sol via UnoRouter began timing out ~2026-09-21 23:46 PDT (parent-verified). sol hypotheses for R6 were
captured BEFORE the outage; the sol red-team call FAILED (traceback, exit 1) — that was the single permitted
hourly retry. Per parent directive: fully native from here; coordinator cron `grok47-recovery-probe` owns all
re-probing; no self-probing of either API. Red-team below is native self-adjudication.

**Fixtures** (preregistered before any run; sol's predictions captured in `sol_r6_hyp.txt`):
- Fixture A (true recovery): 10 discredits → condemn; then 6 verifies across 2 contexts (3×ctx0 + 3×ctx1).
- Fixture B (adversarial resurrection): 10 discredits → condemn; exactly 1 verify; then 10 more discredits.
- P0 = current frozen behavior (verbatim @import). P1 = reset-on-revive (revive + reset VER/UNV/AGE to 0;
  CTX mask preserved — noted as a design detail). P2 = corroborated revive (revive only when VER≥2).

**Results** (all reruns byte-identical):

| Policy | Fixture A | Fixture B |
|---|---|---|
| P0 current | PROMOTED (USED=1, VER=6, CTX=3, PROM=1, NREV=1) | permanently LIVE (USED=1, VER=1, UNV=20, no re-condemn) |
| P1 reset-on-revive | LIVE, **not promoted** (USED=1, VER=5, CTX=3, PROM=0, NREV=1) | RE-CONDEMNED (USED=2, NREV=1) |
| P2 corroborated-revive | PROMOTED (USED=1, VER=6, CTX=3, PROM=1, NREV=1 — identical to P0) | stays CONDEMNED (USED=2, VER=1, NREV=0 — never revived) |

**Verdicts:**
- 5/6 sol predictions confirmed. The miss: sol predicted P1-A → Promoted; measured LIVE/VER=5.
  Cause: the reset consumes the revival verify, so only 5 verifies rebuild evidence (V_MIN=6).
  P1's recovery cost is exactly one observation — a measured nuance, not a permanent failure.
- Kill bar for "P0 is fine" (P1/P2 show no advantage on B while matching P0 on A): **FAILED**.
  P2 matches P0 on A byte-for-byte in final state and strictly dominates on B.
  P1 matches on B (re-condemns) but pays the one-observation recovery cost on A.

**Native self-red-team** (sol unavailable; adjudicated directly):
1. *Fixture fairness:* A and B are the natural minimal pair — A tests "genuine recovery completes",
   B tests "single-verify resurrection is blocked". Not stacked: P2's design target (2 verifies) is
   exactly what B probes, but B is also exactly P0's documented weakness. Symmetric by construction.
2. *P2's new failure mode:* a genuinely-recovering candidate with exactly 1 verify then silence stays
   condemned (USED=2, VER=1) in P2 vs live in P0. Against 10 discredits, 1 verify is weak evidence;
   conservative posture is defensible, but it IS a semantic change: P2 delays genuine recovery until
   a 2nd verify. Tradeoff is real and measured, not hidden.
3. *Is P0's permanent-revive a defect?* The R27 doc calls REVIVE an integrity path — false condemnation
   is treated as costlier than false revival. That asymmetry is a defensible design choice. But it has
   a measured cost: with impostor emissions in the curricula, one stray verify permanently closes the
   condemn path for a condemned impostor. Whether that cost outweighs the integrity bias is a program
   design decision — not mine to make, and the frozen mechanism is NOT edited.
4. *Confounds:* variants differ ONLY in the revive block (single string replacement; canonical SHA
   re-verified after). All other logic byte-identical. Determinism gate: 6/6 byte-identical pairs.
   P1 preserves the CTX mask across reset (counters only) — noted; did not affect these fixtures.

**Recommendation (for coordinator/program, not an edit):** P2 (corroborated revive) is the best of the
three on tested fixtures — zero recovery cost on genuine recovery, full resistance to single-verify
resurrection. Open: should the revive threshold scale with discredit count? Untested; needs its own prereg.
Frozen `psm.zag` NOT modified — repair is a proposal, per Micah's law that tests decide and preregs govern.

### R7 prereg — O3 revive→reconsolidate semantic gap (native; sol down, self-hypothesized)

Mechanism: `o3_consolidate.zag` — the `o3_find(o,id)>=0 → O3_REFUSED_STATE` refusal is byte-identical
in wave9, wave10, and wave12 copies (verified by diff/grep 2026-09-22 ~00:05 PDT). Wave12 copy is the
current-integration representative. Frozen files untouched; Q1 is a probe-only narrowed-refusal copy.
- Q0 (current, verbatim @import): consolidate(7)→OK; condemn(7)→OK; revive(7)→OK; consolidate(7)→?
- Q1 (repair: refuse only when state==CONSOLIDATED, allow CANDIDATE incl. revived): same sequence →?
- Q1 must ALSO still refuse duplicate consolidation (consolidate→consolidate = REFUSED).
Kill bars: H1 (defect exists): Q0 final consolidate → O3_REFUSED_STATE; if O3_OK, my code reading is
wrong and the defect claim is falsified. H2 (repair works): Q1 final consolidate → O3_OK AND duplicate
still refused; if Q1 permits double-consolidation, the repair is wrong. H3 (semantic): whether the
confirmed mechanism fact is a defect is a program design decision — reported, not edited.

**Results** (all reruns byte-identical):

| Sequence | Q0 (current) | Q1 (repair) |
|---|---|---|
| condemn(7) → revive(7) → consolidate(7) | 0, 0, **312** (stuck state=1) | 0, 0, **0** (state=2) |
| consolidate(9) → consolidate(9) (dup guard) | 0, 312 (preserved) | 0, 312 (preserved) |
| condemn(11) → consolidate(11) (no-revive guard) | 0, 312 (preserved) | 0, 312 (preserved) |
| consolidate(13) → condemn(13) (terminal guard) | 0, 312 (preserved) | 0, 312 (preserved) |

**Verdicts:**
- H1 (defect exists): **CONFIRMED**. Q0 `consol7: rc=312 state=1` — the revived id is permanently
  stuck in CANDIDATE; no op in the module can move an existing id to CONSOLIDATED. (Also found en
  route: `o3_condemn` refuses CONSOLIDATED targets — consolidated is terminal, condemn only applies
  to candidates. The defect sequence is condemn→revive→consolidate, not consolidate→condemn.)
- H2 (repair works, guards preserved): **CONFIRMED**. Q1's narrowed refusal (refuse only
  CONSOLIDATED/duplicate and CONDEMNED/without-revive; allow CANDIDATE) repairs the dead end while
  all three existing guards behave identically to Q0.
- H3 (semantic): the module's own header documents "CONDEMNED -> REVIVED" as a lifecycle transition,
  but REVIVED has no outbound path to CONSOLIDATED — the documented lifecycle dead-ends in code.
  Whether that is a defect or intent is a program design decision; reported, not edited. Note the
  R27-parity angle: psm.zag supports revive → reverify → promote; O3 cannot express that sequence.

**Native self-red-team:** Q1 differs from Q0 ONLY in the consolidate refusal (single replacement;
Q0 SHA-256 `210fcd174eb7ea07a2fab42f01af2d5ba05ead83a0d3a3288b8592373e4116de` re-verified after).
A persistent CANDIDATE is reachable ONLY via revive (entry always transitions in-call), so Q1's
behavior change is exactly the revive→consolidate path — no wider semantic drift. Determinism 4/4
byte-identical pairs. Repair is a proposal for the program; frozen files NOT modified.
