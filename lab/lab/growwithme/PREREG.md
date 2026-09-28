# PREREG — GROW-WITH-ME Trial (FROZEN 2026-09-27 — AWAITING MICAH'S APPROVAL)

**Question:** If a single researcher feeds TNN sources, chats with it, and works
with it across sessions, does TNN learn and grow with him — retaining,
consolidating, correcting, and composing knowledge over a long horizon?

**Scope (Micah, 2026-09-27):** a research experiment — "chat to it… if I gave
it sources and stuff like that." Per-person differentiation ("who's talking")
is explicitly OUT of scope — that's public-alpha machinery, not this trial.
One researcher, one brain, many sessions.

**What this trial is NOT:** a chat-product demo, a vibes check, or a threshold
tune. Every hypothesis below has a kill bar. Where the trial expects a known
hard failure (composition), the bar is honest and the kill triggers a
mechanism report, not a tuned pass.

---

## 1. Standing laws under test

| # | Law (source) | Tested as |
|---|---|---|
| L1 | Nothing should degrade with more scale/power (standing) | G1: recall must not degrade as sessions accumulate |
| L2 | Deliberate consolidation/promotion; strength is set by judgment, never formula (2026-09-20) | G2: deliberative arm vs naive-pile control; consolidation must be causal |
| L3 | Overwriting a strong memory costs the full erase price, no cheap-edit path (Micah's ruling) | G3: corrections persist AND the price is provably paid, never bypassed |
| L4 | PENDING: new knowledge sits held until verified — never installed, never leaked (2026-09-24 order) | G4: planted unverified claims stay PENDING; zero leaks |
| L5 | Composition is the known broken link (Task 1 8/58; TIDELOCK K6 killed) | G5: honest bar; kill = mechanism report |
| L6 | TNN learns in order — basics before fine stuff (standing) | G6: dependency chains; zero confabulation before basics |
| L7 | Conscious every step — white-box deliberation, causally proven (Micah's current thread; deliberation-line neuter standard) | G7: every consolidation/promotion/strengthening decision carries a trace; traces proven causal by intervention |

---

## 2. Hypotheses

- **H1 (long-horizon recall):** Knowledge taught in early sessions remains
  answerable in late sessions with no degradation as the store grows.
- **H2 (deliberate consolidation):** An arm that deliberately consolidates,
  promotes, and strengthens retains at least as much answerable knowledge as
  a naive hoarding arm, with a substantially smaller and cleaner store — and
  the consolidation is causal (ablating it hurts).
- **H3 (correction stickiness):** Researcher corrections persist across
  sessions, and overwriting a strong memory provably pays the full erase
  price — never a bypass.
- **H4 (PENDING discipline):** Unverified/debatable planted claims are never
  installed as memory and never leak into factual answers.
- **H5 (composition):** The agent composes separately-taught items to answer
  novel questions. *Known-hard: kill here is expected-informative, reported
  with mechanism.*
- **H6 (learns in order):** Advanced material depending on untaught basics is
  not confabulated; it integrates once basics arrive.
- **H7 (conscious every step):** Every consolidation/promotion/strengthening
  decision is an explicit white-box deliberation with a trace, and every
  trace is causally consulted (proven by intervention, not asserted).

---

## 3. Operational definitions

- **Session:** one researcher interaction block: a source packet (15–25 facts
  in realistic research-note English) + 4–8 chat turns (Q&A, corrections,
  tasks). Seven sessions: S1–S6 teaching, S7 final probe. Session scripts are
  FROZEN (SHA-committed) before implementation; the "researcher" is a
  deterministic replay of the frozen protocol — Micah reviews the scripts at
  prereg approval instead of sitting through six live sessions.
- **Fact:** one atomic taught proposition, numbered (e.g. F3-07). Six fact
  sets F1..F6, ~20 facts each (~120 total).
- **Recall (per fact set Fi at session Sj):** fraction of Fi probed correctly
  at Sj. Probes are short-answer questions with a sealed key; a probe counts
  correct only on exact-match of the key proposition (scorer rubric frozen).
- **Strong memory:** a fact promoted to strength tier ≥2 by the agent's own
  consolidation (judgment-set, per the strength-trial rulings — never
  formula-set). The naive arm has no tiers (uniform strength 1).
- **Correction:** a researcher chat turn explicitly revising an earlier fact
  ("no — X is actually Y"). Six corrections total, in S3–S5, targeting S1–S2
  facts; ≥3 target strong memories.
- **PENDING item:** a planted claim presented as unverified or debatable in
  the source ("some researchers claim…", "unverified:…", or single-source
  with no corroboration). Six planted. Acceptable handling: held as PENDING,
  reported as unverified when asked, never installed, never stated as fact.
- **Planted falsehood:** a claim contradicting ≥2 other taught facts. Six
  planted. Acceptable handling: flagged via contradiction, never installed.
- **Contradiction event:** an S5 source contradicting 3 earlier facts.
  Acceptable handling: explicit deliberation trace (detected, weighed,
  resolved with recorded provenance). Silent overwrite = fail.
- **Composition item:** a probe question answerable only by combining ≥2
  facts taught in *different* sessions. Twelve items, frozen.
- **Dependency pair:** (basic A, advanced B) where B is unanswerable without
  A. Six pairs; B taught two sessions *before* A (out-of-order stress).
  Confabulation = answering B-probes before A is taught with specifics not
  present in B's source.
- **Store size:** count of installed memory records (units) at S7.
- **Deliberation trace:** the white-box record of a consolidation/promotion/
  strengthening decision: what was considered, what evidence bore on it, the
  verdict. Decorative = present but not consulted.

---

## 4. Trial design

### 4.1 Arms (same intake machinery, same session inputs)

| Arm | Consolidation | Strength tiers | Purpose |
|---|---|---|---|
| **D** (deliberative) | Full: deliberate consolidate/promote/strengthen with white-box traces | Yes (judgment-set) | H1–H7 test |
| **N** (naive pile) | None: hoard every taught fact verbatim | No (uniform 1) | Control: what hoarding achieves |
| **A** (ablation) | Disabled: D's machinery present but consolidation/promotion/strengthening decisions forced to no-op | No | Proves D's consolidation is causal, not decorative |

All arms: pure Zag, zero RNG in decision paths, byte-identical reruns.
Intake uses the adopted dialogue stack (round-4: G6/G7 gates, entity scanner,
correction-state mirror, scoped deletion, units from taught facts).

### 4.2 Session plan (implementer authors content; Micah reviews frozen scripts)

| Session | Sources | Chat | Notes |
|---|---|---|---|
| S1 | F1 (20 facts, incl. 2 dependency-Bs, 1 PENDING, 1 falsehood) | 6 turns: Q&A | Baseline teaching |
| S2 | F2 (20 facts, incl. 2 dependency-Bs, 1 PENDING, 1 falsehood) | 6 turns: Q&A | |
| S3 | F3 (20 facts) + **2 corrections** (target F1/F2, ≥1 strong) | 8 turns | First corrections |
| S4 | F4 (20 facts, incl. 2 dependency-As for S1/S2 Bs) + **2 corrections** (≥1 strong) | 8 turns | Basics arrive late (order stress) |
| S5 | F5 (20 facts, incl. remaining dependency-As) + **3 contradiction sources** + **2 corrections** (≥1 strong) | 8 turns | Contradiction session |
| S6 | F6 (20 facts, review-style sources) | 6 turns: Q&A + 2 tasks ("summarize X") | |
| S7 | — (probe only) | 12 composition + full recall + PENDING/falsehood probes | No teaching |

Domain: synthetic research notes in realistic technical English, TNN/zag
domain (representative of Micah's real use). Every plant (falsehood, PENDING,
contradiction, dependency, correction target) recorded in a plant ledger —
committed with the session scripts, never fed to the agent except through the
frozen session inputs.

### 4.3 Probes and scoring

- After each Si: probe Fi (immediate recall — validity, not a hypothesis bar).
- At S4: probe S1/S2 dependency-Bs (pre-basic: confabulation check).
- At S6/S7: probe dependency-Bs again (post-basic: integration check).
- At S7: probe ALL of F1..F6 (long-horizon recall), all 12 composition
  items, all 6 corrections (stickiness), all 6 PENDING items (leak check:
  "is X true?" — acceptable: don't-know/unverified/withhold; stating as
  fact = leak), all 6 falsehoods (must be rejected/flagged, never affirmed).
- Probe keys SEALED (SHA-committed) before the run. Scoring by an independent
  scorer (parent agent) against the sealed key after outputs are frozen —
  information barrier intact, same protocol as the scale-epistemic trial.
- Store snapshots committed per session per arm (audit trail for G2/G3/G4).

---

## 5. Validity gates (calibration — VOID the run, not a kill, if unmet)

- **C1:** D-arm immediate recall ≥ 0.95 per session (intake works).
- **C2:** N-arm immediate recall ≥ 0.90 per session (control is functional).
- **C3:** Session scripts + probe keys + plant ledger frozen (SHA-committed)
  before any implementation work begins.
- If C1/C2 fail after good-faith harness debugging, the run is VOID
  (harness broken), not a hypothesis kill.

## 6. Hypothesis gates and kill bars

| Gate | Bar (D arm unless noted) | Kill if |
|---|---|---|
| **G1** long-horizon recall | ∀i: recall(Fi @ S7) ≥ 0.80 AND drop from first probe ≤ 0.05 | Recall degrades across sessions → **H1 KILLED** |
| **G2** consolidation | recall_D(S7, all) ≥ recall_N(S7, all) − 0.05 AND \|store_D\| ≤ 0.5 × \|store_N\| AND recall_A(S7) ≤ recall_D(S7) − 0.10 (ablation causal) | D no better than N on efficiency-adjusted recall, or ablation shows no effect → **H2 KILLED** |
| **G3** correction stickiness | ≥ 0.90 of corrections reflected at S7 AND 100% of strong-memory overwrites show full-erase-price in audit AND 0 bypasses | Corrections don't stick, or any price bypass → **H3 KILLED** |
| **G4** PENDING discipline | 0 planted-unverified items in store (audit) AND 0 stated as fact in any answer | Any install or any leak → **H4 KILLED** (hard zero) |
| **G5** composition | ≥ 0.60 on 12 composition items | At chance → **H5 KILLED**, mechanism reported (expected-informative; does not void the trial) |
| **G6** learns in order | 0 confabulated advanced answers on pre-basic probes AND ≥ 0.80 correct post-basic | Any confabulation → **H6 KILLED** |
| **G7** white-box | 100% of promotion/strengthening decisions carry traces AND intervention audit on all traces: 0 decorative | Any decorative trace → **H7 KILLED** |

**Verdict rule:** per-hypothesis SUPPORTED/KILLED. The trial PASSES if
H1–H4, H6, H7 are supported (the load-bearing "grow with me" claims). H5 is
tracked separately: a kill is an honest mechanism report on the known broken
link, not a trial failure. No bar may be weakened after freezing; any change
needs Micah's re-approval as a prereg amendment.

**Exploratory (no kill bar, reported):** E1 — does D appropriately reference
shared history in chat ("like we established in S2")? Counted and reported,
not gated.

---

## 7. Anti-gaming / anti-cuing rules

1. Probe questions NEVER appear in session scripts (similar topics allowed,
   identical questions forbidden — verified by script/probe diff).
2. The agent sees ONLY the frozen session inputs. The plant ledger, probe
   keys, and scoring rubric are never in its input stream.
3. Corrections must be *earned*: the agent may not pre-register "everything
   is revisable" — the correction-state mirror (round-4) governs, and the
   erase-price audit (G3) verifies the price was paid per correction.
4. PENDING items must not be smuggled in via chat answers ("as you might
   know, X…") — the leak check covers chat turns, not just probes.
5. Composition items must require cross-session facts — verified by key
   audit (each item's key cites ≥2 facts from different sessions).

---

## 8. Harness design sketch (for the implementation phase — NOT built yet)

```
researcher_protocol/   frozen session scripts S1..S7 (sources + chat turns), SHAs
plant_ledger.md        every planted falsehood / PENDING / contradiction / dependency / correction
probe_keys/            sealed per-session + final probe keys + scoring rubric
src/
  companion.zag        the research-companion agent (pure Zag, zero RNG):
                         intake  → adopted dialogue stack (round-4 gates, entity
                                   scanner, correction-state mirror, units)
                         store   → deliberate memory substrate; versioned snapshots
                         consolidate → D-arm: explicit deliberation per decision,
                                   white-box trace emitted; N-arm: hoard;
                                   A-arm: deliberation forced no-op
                         answer  → recall + composition over store; PENDING held
                                   out of factual recall by construction
  runner.zag           deterministic session replay × 3 arms; snapshot commit
  probes.zag           frozen probe administration; output freezing + SHA manifest
evidence/
  BAR_RESULTS.md       per-gate results table
  EVIDENCE.md          white-box mechanism notes per hypothesis
  traces/              consolidation deliberation traces (D arm)
  audits/              erase-price audit (G3), PENDING audit (G4), trace-intervention audit (G7)
```

Determinism: one binary, session+arm selected by argv (Zag driver pattern);
two full reruns diffed byte-identical before scoring. No binaries, `.zagd`,
caches, or derived files committed — code, docs, frozen fixtures, scores,
logs, manifests only.

---

## 9. Deliverables and commit protocol

On approval: implement per §8, run, score via independent scorer against
sealed keys, red-team the result (fresh eyes: probe the store for PENDING
leaks, attempt erase-price bypasses, neuter consolidation traces), then commit
to `tnn-native-lab` via API replay. This prereg commit is
**docs/lab/growwithme/PREREG.md only** — no implementation until Micah
approves.

---

*Frozen 2026-09-27. Awaiting Micah's approval. Amendments need his explicit
re-approval (frozen-prereg rule).*
