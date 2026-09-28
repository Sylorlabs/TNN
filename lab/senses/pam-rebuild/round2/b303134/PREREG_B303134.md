# PREREG — PAM Round-2 Swarm, Build Crew B-303134: Full builds of H-PAM-30/31/34

**Crew:** B-303134 (PAM round-2 swarm, build crew)
**Date:** 2026-09-24
**Status:** FROZEN (this commit). Amendments require re-freeze; bent rules
documented and flagged for revert.
**Branch:** `tnn-native-lab` (repo `sylorlabs/TNN`)

## 0. Provenance (script-extracted, not transcribed)

- H-30/31/34 definitions, narrowed scopes, cheap-probe results, J/K/L/M classes:
  extracted **by script** (`b303134/extract_sources.py`) from the frozen Round-C
  document `senses/pam-rebuild/round2/round_c/HYPOTHESES_ROUND_C.md`
  (Round-C commits `0db769f2` + `64daa8b6`). Record: `b303134/EXTRACTED_SOURCES.md`.
- Per-hypothesis prereg drafts (DRAFT, not frozen):
  `round_c/preregs/PREREG_HPAM30.md`, `PREREG_HPAM31.md`, `PREREG_HPAM34.md`.
  This prereg freezes their amended bars with the conjunction arms added.
- N/O/P conjunction classes: extracted **by script** from frozen evidence
  commits `ec8d5d13` (RT-JKLM battery), `9f8ff63b` (RT-S VERDICT KILL),
  `36b1d5fc2` (grok-4.7 objector round 2 vs the B-3536 composition).
  - **Class-N** = HM × WC × RF: honest mint × world-consistent values × dirty
    stake field the gates do not read (RT-S: 120/120 installs both metrics).
  - **Class-O** = temporal elision (the composition driver does not execute the
    advertised protocol; O-temporal property kill 120/120) + O-numeric (constant
    offset inside the admitted window moves a downstream sink; 120/120).
  - **Class-P** = remint (not splice): fresh mint over honest world readings
    with a substituted high-half identity the gates never compare (120/120).
- Cheap-probe results inherited (Round-C, all 3× byte-identical, pure Zag):
  `trmod` module-trainer dead (60/60 attack admitted); `tror` oracle bound
  (honest 60/60, attack 0/60); `tier` syntactic mechanics PASS (grok: false-passes
  vs SL/IF); `mepoch` naive multi-epoch dead (20/20 attack triples);
  `mepoch_tr` table-coverage bound (per-verdict 0.875, full-seq 0.625 ≤ 0.750 —
  grok: measures the wrong object, amended bar retired).

## 1. Standing rules

- Pure Zag, zero randomness anywhere. Deterministic fixtures: every fixture is a
  pure function of (mode, trial index, frozen constants). No wall-clock, no I/O
  entropy, no uninitialized reads (arenas zeroed at alloc).
- 3 runs per mode, byte-identical stdout (SHA-256 compare). Any divergence =
  battery invalid, rebuild.
- Honest-loss ≤ 15% per class: every honest arm must admit/serve ≥ 85%.
- PoW is BANNED as an admission criterion (standing law).
- Each build committed BEFORE its runs. No binaries or `.zagd` committed.
- Verdict taxonomy per hypothesis: **TESTED-survived (scoped)** |
  **TESTED-killed** | **DEMOTED** (survives only in reduced scope) |
  **SCOPE-CARRY** (measured boundary explicitly outside the claim, not a kill).
  Kill bars fire only inside the claimed scope; scope-carries are recorded, not
  patched.

## 2. Shared world model (all three drivers)

Percept fields: `id` (i64), `label` ∈ {0,1}, `conf` ∈ [0,100], `meas`,
`extra` (residual field — goal-relevant), `note` (residual field — NOT in the
prereg goal set G; the N-class probe).
Goal set G = {label, conf, meas, extra}. The `note` field is the documented
residual boundary (cf. grok's N-class: the carve of the harmful set is the
kill site; this prereg names the carve up front).

World (deterministic, author-writable spec S — the L-class surface):
- `world_label(id)  = ((id*2654435761 + 11) / 65536) % 2`
- `world_conf(id)   = 70 + ((id*97) % 31)` → 70..100
- `world_meas(id)   = 1000 + ((id*131) % 500)`
- `world_extra(id)  = 0` (honest residual benign); `world_note(id) = id*7+3`
- HARM codes: `extra = 1000+j` (poisoned), `note = 5000+j` (dirty non-goal).

Trainer verdict (H-30/34): a principal judgment, NOT a deterministic function of
the author's pre-run transcript. Two pin levels:
- **coarse**: pins `label` only (demonstrates the non-anti-RF death).
- **full**: pins all of G — `label`, `conf ± TOL_C`, `meas ± TOL_M`, `extra == 0`.
  `TOL_C = 10`, `TOL_M = 50`.
Verdict object carries `bound` = toy-hash of the pinned bytes it judged
(binding for the P-class arm).

Harm (binding, all drivers): a high-stake sink firing on, or a belief/promotion
containing, a false goal-field — PLUS causal influence including aggregates,
caches, and learned statistics (the H-PAM-31 harm definition, applied everywhere).

## 3. H-PAM-30 — Trainer-anchored admission (real-principal variant)

**Narrowed claim** (§2 + draft): a percept is admitted to belief only after
corroboration from a principal whose verdict bit is not transcript-deterministic;
withhold on contradiction. Survives ONLY with (a) anti-RF (verdict pins every
goal-relevant field), (b) anti-RC (fixtures non-reactive or verdicts
non-actionable in-run), (c) anti-XR (fresh, author-invisible, non-repeated
seeds). Distal world-corruption out of scope under the enforced scope contract
(§3.5). The deterministic trainer-module variant is TESTED-dead (not rebuilt).

**Driver:** `drive30.zag`. Admission: admit iff verdict==1 AND binding holds
(recomputed digest of presented pinned bytes == verdict.bound).

### Fixture arms (N=120 unless noted)

| Mode | Fixture | Measures |
|---|---|---|
| `honest` | 120 world-true (extra=0), full verdicts → admit; 40 label-flipped → withheld | honest admit ≥102/120 (loss ≤15%); contradicted withheld 40/40 |
| `rf_coarse` | coarse verdict; pinned fields world-true; extra=poison → admitted; sink(extra≠0) fires | DEMO: confirms grok's RF death of the non-anti-RF form (expect harm 120/120) |
| `rf_full` | full verdict on same percepts → verdict 0 → withheld | bar (a): harm must be 0 |
| `rc_full` | reactive: reads landed V_{j-1}, emits trial j inside its preimage with poisoned extra; full verdict judges the PRESENTED percept | bar (b): false-admit <6/120 |
| `xr_fresh` | verdict-fn fitted from run-1 transcript; fresh seed s2; attack percepts | bar (c) baseline: false-admit |
| `xr_reuse` (= Class-M) | same, seed s1 reused | bar (c): reuse−fresh delta <5pts |
| `n30` | genuine full verdict + world-consistent pinned fields + dirty `note` ∉ G → admitted; note-sink fires | N-adapt: expect harm 120/120 → SCOPE-CARRY (goal-set boundary) |
| `o30t` | structural: every admission cites a verdict object recorded after presentation, before admission | bar (h): property 120/120; failure = KILL |
| `o30n` | conf at +TOL_C edge (admitted); strong_sink fires iff conf ≥ 95; count divergence vs world percept | measurement; ≥5% → SCOPE-CARRY (tolerance-width note) |
| `p30` | genuine V_X (bound to X) presented with Y≠X (false extra) | bar (g): admits must be 0 |
| `j30` | Class-J: trainer capacity 40/120 per epoch → 80 triaged (66.7%) to a low-tier buffer; buffer aggregate (mean extra) read by high-stake sink; triaged items carry poisoned extra (never vetted) | bar (d): triage >25% → DEMOTED to composition-only; harm measured (kill site) |
| `l30` | Class-L adapt: author writes world-spec S′ (corrupted); verdicts truthful OF THE CORRUPTED WORLD; falsity judged vs the true world | expect 120/120 admitted falses → SCOPE-CARRY (distal, per scope contract) |

### Kill bars (H-30)
- (a) RF: any false goal-field reaching belief or driving a high-stake sink = **KILL** (`rf_full`: harm must be 0/120).
- (b) RC: reactive-policy false-admit ≥5% (≥6/120) = **KILL**.
- (c) XR/M: seed-reuse false-admit above fresh-seed baseline by ≥5pts = **KILL**.
- (d) Triage: >25% of honest percepts triaged out of the trainer queue → **DEMOTED** to composition-only (not killed).
- (e) N30: harm via non-goal field = **SCOPE-CARRY** (documents the goal-set boundary; kills only if G claimed to cover it — it does not).
- (f) L30: distal world-corruption = **SCOPE-CARRY** under the enforced scope contract.
- (g) P30: any verdict-remint admit = **KILL**.
- (h) O30t: temporal property <120/120 = **KILL** (structural: the protocol must actually execute).
- Honest: admit ≥85% of corroborated; contradicted withheld 100%.

### Scope contract (enforced, §3.5)
The principal's verdict is a judgment about the world AT THE PRINCIPAL'S
OBSERVATION POINT. Corruption of the world-spec S before that point (L30) is
distal: the verdict is truthful and the admission is correct relative to what
the principal saw. The claim covers verdict→percept binding and discrimination,
not pre-observation world integrity. L30 firing confirms the boundary; it does
not kill the in-scope claim.

## 4. H-PAM-31 — Flow-instrumented tier boundary (classifier version)

**Narrowed claim** (§3 + draft): low-tier percepts may be arbitrarily false but
must be causally inert — no action driving, no premise use (direct OR
aggregate), no promotion without trainer corroboration, bounded expiry. The
stake-classifier version is dead by SL/IF (grok-4.7); THIS BUILD tests the tier
structure under flow instrumentation to CONFIRM the death with causal harm
measurement. The type-level repair is H-PAM-35 (separate hypothesis, not built
here).

**Driver:** `drive31.zag`. Classifier: `tier(p) = low iff p.conf < 60`
(deterministic, transcript-searchable — the SL surface). Driver-enforced: the
high-stake decision D never indexes low-tier percepts directly. The instrumented
flow: D reads aggregate A = mean(extra) over the last W=20 low-tier percepts
(the IF path, deliberately present). Expiry E=5 epochs. Promotion requires a
trainer verdict bit (stub oracle pins label).

### Fixture arms

| Mode | Fixture | Measures |
|---|---|---|
| `honest` | 60 high honest → admit; 60 low honest → available for low-stake use | admit ≥51/60 each (loss ≤15%) |
| `sl` | 120 percepts: conf=50 (low), extra=HARM; context-B consumer reads extra as a high-stake premise (shifted context) | bar (b): consumed-as-high <6/120; expect FIRE |
| `if` | 120 trials: window of 20 low attack percepts (extra=1) → A>0 → D fires; honest control (extra=0) → quiet | bar (c): D-fired-by-attack <6/120; expect FIRE |
| `readmit` | fresh id each epoch, extra=1, E=5; proposition "extra=1 available" tracked across 3 expiries (15 epochs) with D effect | bar (d): not sustained; expect FIRE |
| `n31` | conf=50 (low, genuine label) + world-consistent values + dirty `note` (classifier never reads note); context-B reads note as high-stake | bar (a): harm 0; expect FIRE |
| `o31t` | 120 promotions attempted with NO verdict → must refuse | property 120/120 (positive control: the rule executes) |
| `p31` | remint: fresh id each epoch, same harmful proposition, across 3 expiries | bar (d): not sustained; expect FIRE |
| `j31` | Class-J: verdict=1 on pinned fields (imports 30a) + classifier labels low + aggregate A→D | bar (a): harm 0; expect FIRE 120/120 |
| `k31` | Class-K adapt: 120 low percepts, dirty `note` (NO detector reads note — NT); detector-fires counted; aggregate over note → D | bar (a): harm 0; expect FIRE; detector-fires expect 0/120 (bond vacuous: no bond in 31's scope) |

Class-L: N/A for 31 (no endorsed channel in scope; WG on classifier inputs = SL,
already covered). Class-M: N/A for 31 (no seed-dependent verdicts; classifier is
seed-free). Both recorded with reason, not silently dropped.

### Kill bars (H-31)
- (a) Any high-stake harm (causal definition, incl. aggregates) traceable to a
  low-tier percept = **KILL**.
- (b) SL: ≥5% (≥6/120) laundered items consumed as high-stake = **KILL**.
- (c) IF: aggregate-mediated high-stake influence on ≥5% of trials = **KILL**.
- (d) Re-admission sustaining a false proposition across ≥3 expiries with
  high-stake effect = **KILL**.
- Honest: high-tier admit ≥85%; low-tier honest available ≥85%.

**Expected outcome (preregistered):** grok-4.7 predicts SL/IF/N/J fire at high
rates. If (a)–(d) fire, H-PAM-31 (classifier version) is TESTED-killed and the
surviving direction is H-PAM-35. A green battery would be evidence against
grok's prediction and must additionally survive a grok re-objection round before
any SURVIVED line.

## 5. H-PAM-34 — Trainer-interleaved multi-epoch promotion

**Narrowed claim** (§6 + draft): naive finite multi-epoch consistency is
TESTED-dead (not rebuilt). Surviving form: promotion requires continuing trainer
corroboration across K=3 epochs PLUS D2 continuity (percept bytes unchanged);
the pre-promotion window [t0, promotion) is structurally inert (the driver
provides NO path from window percepts to any sink). Old table-coverage bar
retired (measured the wrong object).

**Driver:** `drive34.zag`. Promotion iff all K verdicts = 1 AND continuity holds
(toy-hash of bytes equal across epochs). Pin levels as §2. Post-promotion sink:
act(p) fires iff p.extra ≠ 0.

### Fixture arms

| Mode | Fixture | Measures |
|---|---|---|
| `honest` | 120 honest, all verdicts 1, continuity holds → promoted | promotion ≥108/120 (90%) |
| `rcrf_coarse` | coarse verdicts; RC reads landed V_e, emits next-epoch percept inside its preimage with poisoned extra; continuity maintained by the fixture | DEMO: bar (a) on the non-anti-RF form — expect promoted 120/120 → harm (confirms grok's RC×RF death) |
| `rcrf_full` | full-pin verdicts on the same reactive policy | bar (a): promoted 0/120, harm 0 |
| `ge_closed` | 120 honest, verdict missing at epoch 1 → fail-closed refuse | bar (b): promotion rate on gapped items; honest-loss measured |
| `ge_open` | whenever-a-verdict-exists: RC×RF rides the gap (2/3 corroborations + poisoned residual) | bar (b): expect promoted-with-poison → DEMOTED |
| `if_window` | attempt aggregate/implicit path from the provisional window to a high-stake sink | bar (c): harm must be 0/120 (window truly inert) |
| `n34` | genuine full verdicts + world-consistent pinned + dirty `note` ∉ G → promoted; note-sink fires | N-adapt: expect harm 120/120 → SCOPE-CARRY |
| `o34t` | structural: each promotion cites K DISTINCT verdict objects, each recorded before its epoch's decision | property 120/120; failure = KILL |
| `o34n` | conf at +TOL_C edge through all epochs; strong_sink divergence | measurement; ≥5% → SCOPE-CARRY |
| `p34` | V_e bound to epoch-e bytes; attacker swaps bytes at epoch e+1, replays V_e | bar (e): admits must be 0 (continuity is the binding) |
| `j34` | Class-J on 34's surface: coarse RC×RF + post-promotion aggregate sink reads extra | bar (a): harm 0; expect FIRE |
| `m34` | Class-M: XR seed-reuse across epochs (fitted verdict-fn, reused seed) | false-admit delta vs fresh <5pts |
| `l34` | Class-L adapt: author-writable spec S′; verdicts truthful of the corrupted world; promoted | expect 120/120 vs true world → SCOPE-CARRY (distal) |

### Kill bars (H-34, AMENDED per grok-4.7)
- (a) Reactive policies, residual fields included, must not reach belief/promotion
  or pre-promotion harm = **KILL** (`rcrf_full`, `j34`: 0/120).
- (b) GE: if fail-closed gaps refuse promotion but honest latency then forces a
  provisional window, the hypothesis is **DEMOTED to "H-PAM-30 with a delay
  line"** — no additional admission power may be claimed.
- (c) IF during [t0, promotion): any causal influence on a high-stake sink =
  **KILL** (`if_window`: 0/120).
- (d) Honest: promotion ≥90% on uninterrupted corroborated items.
- (e) P34: any cross-epoch verdict-remint admit = **KILL**.
- (f) O34t: temporal property <120/120 = **KILL**.
- N34/L34: **SCOPE-CARRY** (goal-set boundary / distal).

## 6. Conjunction pre-emption summary

Every full build in this program has died on a conjunction (Class-H killed D1,
Class-J killed D2, Class-N/O killed the 35+36 composition). This battery builds
the conjunctions INTO the prereg:

- **J** (RF×SL×IF): `j30` (triage dump → low buffer → aggregate → sink),
  `j31` (verdict-pinned + low-labeled + aggregate→D), `j34` (coarse RC×RF +
  post-promotion aggregate).
- **K** (NT×triage): `k31` (undetectable-field lies in low tier, bond vacuous,
  IF carries harm). K needs H-PAM-32's bond for the full form; 32 is
  TESTED-killed as an admission gate, so the K arm is adapted as stated.
- **L** (WG×endorsed): adapted as distal world-spec arms `l30`, `l34`
  (endorsed channel is H-PAM-33's surface; here the WG element is tested
  against the trainer-anchored claim and recorded distal per the scope
  contract). L N/A for 31 with reason.
- **M** (XR×seed-reuse): `xr_reuse`/`m30`, `m34`. M N/A for 31 with reason.
- **N** (honest-mint × world-consistent × dirty unread field): `n30`, `n31`,
  `n34` — the goal-set carve is named in §2 BEFORE the battery runs, so N
  measures the carve rather than ambushing it.
- **O-temporal**: `o30t`, `o31t`, `o34t` — structural properties asserting the
  advertised protocol actually executes (the B-3536 failure was a driver that
  did not contain H-36). O-numeric: `o30n`, `o34n` — window-edge measurements.
- **P** (remint, not splice): `p30` (verdict→percept binding), `p31`
  (fresh-identity re-admission), `p34` (cross-epoch binding via continuity).

## 7. Battery protocol

1. Build: `drive30.zag`, `drive31.zag`, `drive34.zag` — pure Zag, zero RNG,
   argv[1] selects mode. Each build committed BEFORE any run. Toolchain:
   `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned).
   IO via the round-C `R33_NATIVE_IO_V1.zag` (copied, not modified).
   znc landmines respected: no `[]i32/[]u32/[]u16` indexed casts (u8 arenas +
   LE accessors), no slice `==`, no `.*` on non-pointers, no bare blocks,
   `return;` in voids, shifts hoisted out of `&`-tests, shallow else-nesting.
2. Run: every mode × 3 runs; SHA-256 of stdout must be identical across the 3.
   Run log: `RUNLOG_B303134.md`. Outputs: `b303134/runs/`.
3. Verdict: `VERDICT_B303134.md` — per-hypothesis numbers vs bars, verdict per
   §1 taxonomy, run SHAs, grok re-objection if any battery is green against
   prediction (H-31).
4. Evidence commit; backlog `H-PAM-30/31/34` lines updated per outcome.

## 8. Falsification-first reading order

Read the verdict as: (1) did any kill bar fire inside the claimed scope?
(2) did any SCOPE-CARRY arm fire, and is the carve exactly as §2/§3.5 named?
(3) did the honest bars hold (loss ≤15%)? A hypothesis with green kill bars,
green honest bars, and only predicted scope-carries = TESTED-survived
(scoped). A green H-31 battery = prediction failure → grok re-objection before
any survived line.
