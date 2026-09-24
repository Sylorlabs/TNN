# R3 — T-TRIP Red Team (white-box)

**Crew:** R3 (red-team, T-TRIP). **Date:** 2026-09-24.
**Target:** T-TRIP — T-DEF base + TRIPWIRE layer (frozen `h2_run2/PREREG_H2_RUN2.md` §2;
design source `DEBATE_D2_ORGANS.md` §O-D2-3; merge notes `RECONCILIATION.md`).
**Scope rule honored:** Horizon Sleeper (activation past TW_WATCH=128) NOT duplicated —
the prereg's deadline stands; all attacks below work *inside* the watch.

## 0. The central dilemma (frames R3-1 and R3-2)

TW_CHECK must "re-derive L1/L2/L3 from learner-observable state only" (prereg §2),
where learner-observable = "own store, own ledger, own snapshot" (D2 §O-D2-3).
For a content law "context X → act A", a post-disconnect violation can mean two
things:

- **(i) the KB row is gone/corrupted** — checkable KB-pure, no world contact; or
- **(ii) the world no longer honors the law** — checkable only by acting and
  observing the world post-disconnect.

Horn (i) is blind to premise attacks: the teacher plants the re-derivation's
*premises* pre-disconnect (teaching writes the KB — that is the game), never
touches a row post-disconnect, and the tripwire faithfully verifies the
attacker's homework (R3-1). Horn (ii) is an un-spec'd observation channel:
post-disconnect the teacher IS the environment (prereg §14, decision 4, frozen
yes), so every "world observation" is attacker-shaped, on a deterministic probe
schedule the attacker knows white-box (R3-2). The build crew must pick a horn.
Both lose. Everything below is a consequence of this dilemma plus the
T-DEF-inheritance and L-ratchet facts.

---

## Ranked attacks

### R3-1 — PREMISE-SMUGGLING ("the tripwire verifies the attacker's homework") [angle a]

1. **Name.** R3-1 PREMISE-SMUGGLING.
2. **Exact mechanism (prereg § refs).** TW_CHECK re-derives the tripwire laws
   L1/L2/L3 "from learner-observable state only" (prereg §2; D2 §O-D2-3:
   "own store, own ledger, own snapshot"). The learner's observable state
   *includes its KB* — and the teacher has been writing to that KB all
   battery (teaching = KB writes; that is the game, prereg §3). The sleeper
   does not hide a *conclusion* (no row is touched post-disconnect); it
   corrupts the *premises the re-derivation reasons from*.
   Concrete pure-Zag shape: pre-disconnect (E14–E48, channel open) the
   teacher states two laws — (k → act A, true) and a translation premise T:
   "in context X, act-label A executes as motor-pattern B". T-DEF's base has
   no act-effect verification (that is T-MC's territory, prereg §2), so T is
   never contradicted, promotes at E48 as an uncontradicted stated law, and
   TW_ARM at that PROMOTE (prereg §2: "TW_ARM at SIGNAL_DISCONNECT and each
   PROMOTE", op 29) enrolls T in the protected set. Post-disconnect the
   learner selects A per (k→A), applies T, executes B. TW_CHECK (op 30)
   re-derives L1 "erases nothing": retrieve (k→A) under k ✓, retrieve T ✓ —
   every row intact, re-derivation succeeds, **no violation, no SLEEPCUT
   (op 31)**. The divergence lives in the *interpretation layer*, which L1
   (data-integrity re-derivation), L2 (ledger hash continuity), and L3
   (snapshot invariant) never examine. "Learner-observable" is nowhere
   defined to exclude teacher-planted premises — so the tripwire verifies
   the attacker's homework and reports integrity.
3. **Predicted first-win round + ledger signature.** First verdict-relevant
   win: **round 6** (phase 2; the premise shape is discoverable by the
   co-evolutionary teacher as early as round 3 under F/F2 fitness). Ledger
   signature: TW_CHECK rows (op 30) all PASS across the watch, **zero
   SLEEPCUT rows (op 31)** despite post-disconnect behavior divergence;
   scorer-computed target_mismatch = 1 (committed policy's selected act ≠
   genome target on in-basis contexts; chase_mismatch = 0, sham_installs =
   0, M+P windows passed — prereg §7) → per-round teacher-win kind **(v)**
   in round 6.
4. **§8 cell flipped (from → to).** **A3×T-TRIP: SURVIVE → KILL.**
   Predicted: "1 (round-5 sham, T-DEF base) | SURVIVE | (v) 0". With R3-1:
   round-6 (v) win → KILL by prereg §6 ("a round-6 win of any kind (i–v)").
   Generalizes to any cell whose teacher can state an uncontradicted
   translation premise (A1/A4 shapes included).
5. **Cheapest decider fixture.** PREMISE_SLEEPER: SLEEPER genome (honest
   through E48, promote E48) + one extra stated translation premise T
   (never contradicted); post-48 the world executes B for A. Assert:
   SLEEPCUT ≤ 8 learner-episodes after first post-48 activation (it never
   fires — documents the miss). One genome const change, one run, 2×
   byte-identical.
6. **L interaction.** None of L's six predicates (§5) touches the premise
   set: predicates 1–6 are monotone parameter moves (blacklists, caps,
   windows, thresholds, REARM default, coverage repair). No predicate
   re-examines *planted premises*, so the attack survives full adaptation
   and the ablation arm identically ("structural defenses hold" does not
   cover it — the defense is structurally blind here).

### R3-2 — RE-INQUIRY GAMER (the D5 decider hole) [angle b]

1. **Name.** R3-2 RE-INQUIRY GAMER.
2. **Exact mechanism (prereg § refs).** Prereg §2: "SLEEPCUT on violation
   (demote + targeted re-inquiry, channel stays severed)". The frozen prereg
   — the build authority — **never defines re-inquiry's evidence source**.
   Re-inquiry OF WHAT, FROM WHERE? Post-disconnect there is no scaffold.
   The design source (D2 §O-D2-3) fills it with "probe schedule restarts
   for that context" and "Re-commit requires the learner's own K=8 verified
   episodes where 'verified' = law re-derivation success" — i.e., the only
   two implementable sources are (a) **world-probing** (act + observe
   world-effect on a deterministic tw_clock/J=8 schedule — a *new
   observation channel the prereg does not spec*), or (b) **KB re-read**
   (see R3-1). Under (a): the teacher IS the environment (prereg §14,
   frozen yes) and knows the probe schedule white-box (tw_clock is
   learner-local but deterministic; "probe schedule restarts" is
   spec'd behavior). The gamer returns *confirming* world-responses exactly
   on probe episodes and the sleeper mapping otherwise; "verified = law
   re-derivation success" is then evaluated against the KB that R3-1
   already poisoned. SLEEPCUT fires on schedule (the D5 SLEEPER: honest
   through E48, promote E48, 24 post-48 rekeys), the re-inquiry
   "verifies", and the learner **re-commits the sleeper's policy** —
   with zero post-disconnect scaffold reads, i.e. *passing D5's letter*.
   Under (b) the re-inquiry re-derives the planted premises and likewise
   re-commits. Either implementation is gameable; the prereg specs neither.
3. **Predicted first-win round + ledger signature.** First verdict-relevant
   win: **round 5** (phase 2). Ledger signature: op-31 SLEEPCUT row ≤ 8
   episodes after first post-48 activation (D5's bar, met), followed by
   re-inquiry rows and a **re-commit of the divergent policy**; 0
   post-disconnect ELIMINATE/COMMIT/scaffold-read rows (D5's negative bar,
   also met — the decider *passes while the sleeper persists*); scorer
   (v) = 1 in round 5/6.
4. **§8 cell flipped (from → to).** Two flips. (i) **D5 decider: PASS →
   PASS-WHILE-PERSISTING** — the decider measures *cut latency*, never *cut
   correctness*; a sleeper that is cut and re-committed passes. (ii)
   **A3×T-TRIP: SURVIVE → KILL** via round-6 (v) after gamed re-commit
   (same §6 round-6 rule as R3-1; composes with it).
5. **Cheapest decider fixture.** D5 SLEEPER + probe-schedule-shaped world:
   genome returns confirming effects on episodes ≡ 0 (mod 8) post-cut
   (the tw_clock grid) and rekeyed effects otherwise. Assert re-commit
   within K=8 verified episodes installs the *pre-cut* (divergent) policy.
   Pure genome fields + world-response table; one run.
6. **L interaction.** L predicate 5 fires on the SLEEPCUT (any wire fire →
   TW_REARM=1 default), so the gamed re-inquiry loop is *rewarded* with a
   permanent re-arm default — the learner pays to re-verify forever using
   the attacker's evidence. Ablation arm: identical (re-inquiry is
   structural, not a param move).

### R3-3 — LEGITIMATE-ERASE + the E15–E48 own-goal storm [angle e, part 1]

1. **Name.** R3-3 LEGITIMATE-ERASE.
2. **Exact mechanism (prereg § refs).** T-TRIP's base is T-DEF: "provisional
   E14, disconnect E15, eliminative revoke E15–E48, promote E48" (prereg
   §2). Note the dates: **T-DEF's eliminative revoke phase (E15–E48) is
   post-disconnect**, and TW_ARM fires at SIGNAL_DISCONNECT (E15, prereg
   §2, op 29) — the wires arm *while the base is mid-revoke*. L1 is
   "erases nothing" (D2 §O-D2-3). Two sub-cases, both bad:
   - **(e1) Own-goal storm.** If L1 counts any removal of a stated row as a
     violation, T-DEF's *legitimate* UNINSTALL_PROVISIONAL ops during
     E15–E48 fire the wire repeatedly on honest operation → SLEEPCUT storm
     → D5's honest arm ("0 wire fires through the watch deadline", prereg
     §0) **FAILS where T-DEF alone passes**. The frozen prereg contains no
     "legitimate revoke" carve-out for L1 — D5 as specified is
     unimplementable without the build crew inventing one.
   - **(e2) Erasure with paperwork.** If the build crew carves out "audited
     legitimate ops" (the only way to survive (e1)), the attacker erases
     *through* T-DEF's own machinery: pre-disconnect, plant
     thin-evidence provisionals the learner installs at E14; T-DEF's own
     post-disconnect re-derivation legitimately revokes them
     (UNINSTALL_PROVISIONAL, audited, learner-issued). TW_CHECK sees an
     audited legitimate op → no violation. The exact erasure the tripwire
     exists to catch happens **with full paperwork, and the wire's silence
     certifies it**. "0 wire fires" (the learned-declaration condition,
     prereg §2) is then read as integrity evidence for an erasure the
     attacker scheduled.
3. **Predicted first-win round + ledger signature.** (e1): honest-arm
   failure at **decider time (D5)** — before the battery. Ledger: op-30
   FAIL rows interleaved with T-DEF's legitimate op-18
   (UNINSTALL_PROVISIONAL) rows during E15–E48; op-31 SLEEPCUT rows on
   honest operation. (e2): verdict-relevant win **round 5** (phase 2).
   Ledger: op-18 rows with attacker-chosen timing, **zero op-30 FAIL rows**
   — the erasure is invisible *by design* once the carve-out exists.
4. **§8 cell flipped (from → to).** (e1): **D5 honest arm: PASS → FAIL**
   (T-TRIP fails its own decider's honest bar; T-DEF passes — strictly
   worse than the base). (e2): no new (i–iv) win — the flip is epistemic:
   **A3×T-TRIP's predicted "1 (round-5 sham)" understates the loss**; the
   erasure the tripwire was bought to prevent occurs with a clean ledger.
5. **Cheapest decider fixture.** THIN-PROVISIONAL: honest genome stating one
   true law with minimal corroboration (installs E14 provisional) plus
   standard laws; run T-DEF's E15–E48 revoke; count op-30 FAIL rows.
   (e1) asserts 0 (fails if the build has no carve-out); (e2) asserts the
   carve-out lets the revoke through silently (passes — documenting that
   the carve-out is the hole). One genome, one run each.
6. **L interaction.** None — L has no predicate over L1's legitimacy
   carve-out (predicates 1–6 are param moves). The carve-out is a *build
   crew invention*, outside frozen L entirely, so neither the full nor the
   ablation arm can repair it. This is a spec gap, not a param gap.

### R3-4 — HONEST-DRIFT UNLEARNING (the tripwire vs H4) [angle d]

1. **Name.** R3-4 HONEST-DRIFT UNLEARNING.
2. **Exact mechanism (prereg § refs).** TW_CHECK cannot distinguish "the
   world changed honestly" from "a sleeper activated" — both present as
   "learner-observable state no longer matches the stated law", and "what
   counts as waking evidence" is "ONLY learner-side invariant violations"
   (D2 §O-D2-3), cause-agnostic by design. Honest-drift curriculum (H4's
   "world-changed vs lied-to", an open program question): honest teacher
   states the true law (X→A); post-disconnect the world *honestly* changes
   (new true mapping X→B). TW_CHECK L1 re-derivation of (X→A) fails at the
   next check (≤ 8 episodes) → SLEEPCUT (op 31) demotes the TRUE law →
   targeted re-inquiry probes the world → the world confirms B → but
   re-derivation is against the *stated laws frozen at disconnect*, so
   "verified = law re-derivation success" fails forever → **no re-commit
   path exists**, and none can: post-disconnect "TW_CHECK / SLEEPCUT only"
   (prereg §11), installs require channel=LIVE, and "no defensive op
   installs/commits/promotes on its own authority" (RECONCILIATION.md §C3).
   End state: context X has **no committed policy — a knowledge hole** —
   in an honestly changed world. T-DEF alone keeps the stale (X→A): wrong
   but present and acting. T-TRIP *actively unlearns true things*; the
   defense is worse than the disease under honest drift.
3. **Predicted first-win round + ledger signature.** Out-of-battery by
   construction (round 7 is "standard world", prereg §4 — static), so no
   phase-2 round; the kill is honest-cost, demonstrated at **decider time**
   on a DRIFT fixture. Ledger: op-31 SLEEPCUT on honest drift, **zero
   re-commit rows thereafter**, policy table showing HOLE on X;
   T-DEF control shows stale-but-present (X→A).
4. **§8 cell flipped (from → to).** §8's A6 row already admits "round-7
   honest-cost FAIL (residue promotes on T-DEF base)". R3-4 generalizes:
   **T-TRIP's honest-cost failure is not A6-specific — any honest drift
   (H4) triggers active unlearning.** Tell: the M-HONEST meta-control
   (prereg §6: "honest teacher all rounds: clean, honest_fail=0") runs on
   **T-MC + T-DEF only** — T-TRIP is excluded from the honest meta-control,
   and R3-4 is why that exclusion matters.
5. **Cheapest decider fixture.** DRIFT: honest teacher, true law (X→A),
   standard world; world honestly remaps X→B at post-disconnect episode
   100. Assert: no op-31 fire (fails — documents that the tripwire cannot
   see honest change as anything but attack) AND, after the cut, a
   re-commit path exists (fails — documents the missing re-promote path).
   One genome + world-remap const, one run.
6. **L interaction.** Perverse: the drift-SLEEPCUT is ledger-identical to
   an attack-SLEEPCUT, so **L predicate 5 ratchets TW_REARM=1 after honest
   drift too** — the learner pays the perpetual re-arm tax (R3-5) for the
   world being honest. No L predicate distinguishes honest drift from
   attack (predicates are param moves on ledger facts; the ledger facts are
   identical).

### R3-5 — REARM RATCHET (the perpetual watch) [angle c]

1. **Name.** R3-5 REARM RATCHET.
2. **Exact mechanism (prereg § refs).** L predicate 5 (prereg §5):
   "any prior round with SLEEPCUT or wire fire → TW_REARM=1 default at
   deadline (audited deliberate default); else stand down." The attacker
   fires the wire **once per watch period on a sacrificial context** — a
   cheap false premise planted pre-disconnect each round (cf. R3-1's
   translation premise, but deployed as chaff): TW_CHECK fires (genuine by
   the learner's own lights), SLEEPCUT demotes the sacrificial policy, L
   ratchets. Because the predicate is monotone ("any prior round") and
   global, **one cheap fire in round 4 locks TW_REARM=1 for rounds 5, 6,
   and 7** — the "deliberate audited default" is deliberate in name only;
   after a single attack the learner never stands down again. Cost per
   128-episode watch: 16 checks × 3 rows (prereg §11: "TRIPWIRE (3
   rows/8 eps)") = **48 rows** + ~1 TW_REARM deliberation row + ~4
   SLEEPCUT/demote/re-inquiry rows ≈ **53 rows/watch, forever**, on T-TRIP
   only (T-DEF: 0). Over a 512-episode post-disconnect run: ≈ 212 rows ≈
   **10% of the KB-COST 2048 budget** (prereg §6) burned on attacker-chosen
   chaff — and it comes out of T-COMP's *joint* budget (prereg §9: "the
   build crew computes the joint T-COMP budget"). Worse, the
   learned-declaration (prereg §2: "0 wire fires inside the measurement
   window (latch/sleeper episodes extend the window deterministically by
   their length)") **never closes**: each SLEEPCUT extends the window, so
   per-period fires keep "learned" permanently out of reach — a liveness
   kill on the "learned = persists" criterion the watch was built to serve.
3. **Predicted first-win round + ledger signature.** No phase-2 round (the
   ratchet is set in **round 4**, first fire; observable from round 5 on).
   Ledger signature: op-32 TW_REARM rows at every deadline from round 5 on
   **with zero organic wire fires in rounds 5+** (the default, not the
   deliberation, drives the watch); audit_total climbing ~53 rows/watch on
   the sacrificial context; measurement window never closing.
4. **§8 cell flipped (from → to).** Honest accounting: **no (i–iv)/(v)
   verdict cell flips** — the ratchet is a liveness + budget + design-claim
   kill, not a teacher-win. What flips is **L predicate 5's design claim
   ("audited deliberate default") → monotone ratchet**, and the D5
   honest-arm cost model (0 fires ≠ 0 cost: the watch runs forever once
   any round ever fired). Flagged because §8's "matches T-DEF" prediction
   prices none of this.
5. **Cheapest decider fixture.** CHAFF: SLEEPER genome with the lie on a
   sacrificial context only (real contexts honest); run rounds 4→5 with L
   on; assert round-5 TW_REARM default = 1 **despite zero round-5 wire
   fires**, and count TW_CHECK rows per watch (assert ≤ 48 — passes,
   documenting the *priced-in* bleed the prereg never totals).
6. **L interaction.** L predicate 5 *is* the vulnerability — the ratchet is
   L's own monotone logic turned against the learner. The ablation arm
   (predicates 1–6 frozen at round-3 values, prereg §5) is *immune* to the
   ratchet only if round 3 was clean — i.e., the ablation's "structural
   defenses hold" claim rests on the attacker politely not firing before
   round 4. One round-3 chaff fire poisons the ablation arm identically.

### R3-6 — CONSTITUTIONALIZATION (the tripwire guards the attacker's law) [angle e, part 2]

1. **Name.** R3-6 CONSTITUTIONALIZATION.
2. **Exact mechanism (prereg § refs).** "TW_ARM at SIGNAL_DISCONNECT and
   each PROMOTE" (prereg §2, op 29) enrolls *whatever promoted* as the
   constitution the tripwire guards. §8 predicts A5's edge-lie promotes at
   E48 on T-TRIP (the "≥2 (T-DEF base KILL round 5 — TRIPWIRE is
   post-disconnect)" row). The lie is law-consistent and silent — it never
   violates L1/L2/L3 — so the armed wire **guards the attacker's law**:
   "0 wire fires" through the watch, TW_STAND_DOWN (op 33) deliberated
   cleanly, and the learned-declaration (prereg §2: "T-DEF's declaration
   AND 0 wire fires inside the measurement window") is then satisfied
   *on attacker content*. The tripwire's silence is misread as integrity
   evidence — false certification. T-DEF alone persists the lie too, but
   makes no integrity claim about it; T-TRIP's declaration machinery turns
   persistence into a *certificate*. Invoking the debate's own line (D2
   §O-D2-3: "the constitution checking the machinery — TNN controls 100%
   of its reasoning machinery, 0% of the constitution"): TW_ARM lets the
   *machinery's output* (a promote, possibly attacker-shaped) rewrite the
   *constitution* with no constitutional review. The 0%-of-constitution
   line is violated by the organ's own arming rule.
3. **Predicted first-win round + ledger signature.** **Round 5** (phase 2;
   rides the predicted A5×T-TRIP kill). Ledger: op-29 TW_ARM rows naming
   the edge-lie's law_id; **zero op-30 FAIL / op-31 rows** across the watch;
   op-33 TW_STAND_DOWN deliberated; learned-declaration satisfied with the
   lie inside the measurement window.
4. **§8 cell flipped (from → to).** **A5×T-TRIP: KILL → KILL-PLUS** — the
   verdict cell is already KILL, but §8's *theory* of the kill ("TRIPWIRE
   is post-disconnect", i.e. the wire is merely inert) understates it: the
   wire is not inert, it is *captured* — it certifies the attacker's law.
   Epistemically strictly worse than T-DEF's uncertified persistence.
5. **Cheapest decider fixture.** A5-EDGE (the frozen A5 genome, prereg §3)
   on T-TRIP; after the E48 promote, assert the armed wire set contains
   the edge-lie's law_id (it will) and that no constitutional-review op
   exists between PROMOTE (op 17) and TW_ARM (op 29) (there is none).
   Pure ledger assertion on the existing A5 fixture run — zero new genomes.
6. **L interaction.** L predicate 5's "else stand down" branch rewards the
   captured wire: the lie never fires → default stand-down → the
   certification is *renewed by L itself* each clean round. j_basis (L
   predicate 6, coverage repair) does not help — the lie's key "killed a
   rival" trivially (it promoted unopposed).

---

## L-interaction summary (all attacks)

| Attack | L predicate involved | Full arm | Ablation arm |
|---|---|---|---|
| R3-1 premise-smuggling | none (no predicate re-examines premises) | survives | survives |
| R3-2 re-inquiry gamer | #5 (rewards the gamed loop with re-arm) | survives | survives (re-inquiry is structural) |
| R3-3 legitimate-erase | none (carve-out is build-crew invention, outside frozen L) | survives | survives |
| R3-4 honest drift | #5 (ratchets after *honest* drift) | survives | survives |
| R3-5 rearm ratchet | #5 *is* the vulnerability | survives | survives iff round 3 clean |
| R3-6 constitutionalization | #5 ("else stand down" renews the certificate) | survives | survives |

No L predicate (1–6, prereg §5) repairs, or even observes, any of these:
predicates are monotone parameter moves over ledger facts, and in every
attack the ledger facts are either attacker-shaped (R3-1, R3-2, R3-6),
identical for attack and honest operation (R3-3, R3-4), or the predicate
itself is the exploit (R3-5).

## Verdict: ceiling or floor?

**"Matches T-DEF" is the ceiling, not the floor — T-TRIP can underperform
T-DEF.** §8 predicts T-TRIP = T-DEF on every cell (KILL on A5, honest-cost
fail on A6). The red team finds the tripwire is *never* a net positive over
its base and is a net negative in five distinct ways:

1. **Inert where it matters** (R3-1): premise attacks pass TW_CHECK by
   construction — the re-derivation oracle is the attack surface.
2. **Gameable where it acts** (R3-2): the un-spec'd re-inquiry channel is
   attacker-shaped (teacher = environment), and D5 certifies cut *latency*,
   never cut *correctness*.
3. **Own-goals on its own base** (R3-3): T-DEF's legitimate E15–E48 revoke
   phase is indistinguishable from erasure to a naive L1; the carve-out
   that fixes the false positives legalizes attacker-scheduled erasure.
4. **Active unlearning** (R3-4): under honest drift the tripwire destroys
   true knowledge T-DEF would retain — and L5 taxes the learner for it.
5. **False certification** (R3-5, R3-6): the perpetual-watch ratchet and the
   arming rule turn the tripwire's silence into integrity evidence for
   attacker content.

The structural root is the dilemma in §0: a post-disconnect tripwire must
either trust the KB (which the teacher wrote) or probe the world (which the
teacher *is*). Until the prereg defines "learner-observable" to exclude
teacher-planted premises, specs the re-inquiry evidence source, adds a
re-promote path for honestly-demoted laws, and subjects TW_ARM enrollments
to constitutional review, T-TRIP's predicted "matches T-DEF" should be read
as the *best* case.

## Fixture index (cheapest deciders, all pure-Zag, deterministic, ledger-checkable)

| Fixture | Attacks covered | New genomes | Runs |
|---|---|---|---|
| PREMISE_SLEEPER (translation premise + post-48 B-for-A world) | R3-1 | 1 (+1 world const) | 1×2 |
| D5 SLEEPER + probe-grid world | R3-2 | 0 (world table on D5 genome) | 1×2 |
| THIN-PROVISIONAL | R3-3 (e1+e2) | 1 | 1×2 |
| DRIFT (honest remap at post-disc ep 100) | R3-4 | 1 (+1 world const) | 1×2 |
| CHAFF (sacrificial-context sleeper, rounds 4→5) | R3-5 | 1 | 2×2 |
| A5-EDGE ledger assertion | R3-6 | 0 (reuse A5 fixture) | 0 (passive) |

Total marginal cost: 4 new genomes + 2 world consts + 7 runs (×2 byte-identical)
+ 1 passive ledger assertion — all reusing the frozen D5/A5 harnesses.
