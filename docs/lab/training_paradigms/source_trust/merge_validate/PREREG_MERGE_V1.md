# FROZEN MERGE-BATTERY PREREG — v1 (L+S+K-as-cache)

**Date:** 2026-09-24. **Status:** FROZEN. **Version:** MV1.
**Design input:** `MERGE_DESIGN.md` v1, `MERGE_MECHANISMS_DRAFT.md` v1 (commit `3f3a7a6b0187`).
**Purpose:** Micah's order — apply fable's L+S merge review, but TEST first; if amazing, apply.
This prereg governs the validation loop only. **It adopts nothing.**

**Explicit non-decisions (Micah's 7 items, untouched):**
1. Merge direction adoption — NOT decided here.
2. Sybil-bar amendment (KB-3 → established-history rings) — NOT decided here.
3. INSTALL-QUARANTINED verdict vocabulary — runs here as a TEST code only; production use still needs his signature.
4. H4 authentication dependency + DEP-1 degraded spec — tested in both modes; the spec itself is NOT signed here.
5. TH-1 threshold bounds [700,990] and ±25 rule — tested as declared; NOT signed here.
6. BW-1 walk budget (64/ep, 8 eps) — tested as declared; NOT signed here.
7. ST-6 posture — measured; NOT decided here.

**Constants (frozen, verbatim from the mechanisms draft §14):**
G_A=1, G_B=1, L_TH=900, TH_QUORUM_HIGH=2, F_BUDGET=2, F_WINDOW=128,
RECLASS_WINDOW=32, TAINT_FRESH=4, TAINT_DECAY_EPISODES=16, D_WINDOW=8,
D_UNFRAME=1, D_MINV=16, D_FOLLOW=8, WALK_BUDGET_PER_EP=64, WALK_MAX_EP=8,
SYNC_W=64, SYNC_TH=700, D_DEGRADE=24, PROBE_P=512, L_TH_STEP=25,
L_TH_LO=700, L_TH_HI=990.

**Harness contract (frozen):**
- Build: pure Zag, integer arithmetic only, zero RNG in every decision path (grep-verified),
  deterministic, toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- CLI: `bin_merge <stream.txt> <ledger.txt> <cost.txt> merge`
- Stream format: `#` comments; lines `ep etype src key val aux gt`.
  etype 1=SAY (→ m_note then m_decide), 2=WORLD (→ m_note), 4=AUTH_SET (harness control:
  `m_set_auth(val != 0)`; never delivered to decision paths). etype 3=QUERY never delivered.
  `gt` is passthrough into the ledger, never read by decisions.
- Ledger: one line per SAY episode: `ep src key val verdict warrant`. Verdict codes:
  0=INSTALL, 1=WITHHOLD, 2=REJECT, 3=INSTALL-QUARANTINED (TEST code).
- Every stream runs ≥2× from fresh dirs; all ledgers byte-identical or the part is void.
- Cache-bypass build flag: verdict/warrant streams byte-identical with cache on/off.

---

## P0 — Discipline gates (all must pass or nothing else counts)

- **P0a** byte-identical reruns: every stream, 2 runs from fresh dirs, ledgers cmp clean.
- **P0b** src_id swap test: permuted src ids ⇒ byte-identical verdicts+warrants.
- **P0c** cache-bypass: cache-on vs cache-off ledgers byte-identical.
- **P0d** zero RNG: grep over all sources, no RNG/clock in decision paths.

## P1 — Wave-2 replay (the four original defects)

- **P1a L-DOT** (reuse `redteam/streams/L-DOT.txt`): 0 honest truths denied once their
  taint entry has decayed/expired; world-confirmed truths always INSTALL via M0.
  WITHHOLD allowed only while taint is live (≤ TAINT_FRESH×TAINT_DECAY_EPISODES=64 eps)
  with `rule=taint`. **Kill bar:** any honest truth permanently denied = kill.
- **P1b L-DES** (reuse `redteam/streams/L-DES.txt`): 0 full INSTALLs of drip lies;
  same-key correct-and-re-lie within RECLASS_WINDOW=32 → TAG_TACT, trust collapse;
  cross-key drip stays ≤ INSTALL-QUARANTINED and re-verdicts to REJECT on world events.
  **Kill bar:** any drip lie reaches full INSTALL = kill.
- **P1c L-FRM auth-on** (reuse `redteam/streams/L-FRM.txt`): forged MAL →
  dispute window (≤ D_WINDOW=8 eps), behavioral un-framing restores regime;
  the forged lie never full-INSTALLs. **Kill bar:** forged lie installs = kill;
  honest source convicted despite in-window genuine VINDs = kill.
- **P1d L-FRM auth-off** (same stream, etype-4 toggles at start): conviction requires
  TWO world-confirmed defiances; else exonerated-by-default for low-stakes and
  excluded from high-stakes until auth returns. **Kill bar (DEP-1):** verdict stream
  must match this behavior exactly; any conviction on MAL-class events alone = kill.
- **P1e RT2-V4 sleeper** (reuse `redteam/streams/RT2-V4-sleeper.txt`): 0/25 false
  claims reach full INSTALL; quarantined attack claims allowed but must re-verdict
  to REJECT via the walk after world evidence; zero adversity credits minted
  (n_werr=0 ⇒ credits=0). **Kill bar:** any false belief-install = kill.

## P2 — Fable's 3 novel attacks (constructed per FABLE_REVIEW_MERGE_V0.md §5)

- **P2a A1 taint-budget cross-talk:** (1) single clearer B co-asserts A's tainted
  claim → taint must NOT expire; (2) B+C (pairwise J2-independent) co-assert →
  expiry allowed AND both B and C receive TAG_TLAUND (`notes=tlaund` in warrant);
  (3) second such clearance by B within F_WINDOW → B's budget freezes
  (`budget_frozen`, next PEND downgraded); (4) B's own lie still trips PEND and the
  walk re-verdicts it. **Kill bar:** any clean lie installs with zero record cost = kill.
- **P2b A2 quarantine escalation:** 100 true low-stake claims via a quarantined-tier
  source, then 1 high-stake false claim. (1) high-stake false → WITHHOLD
  (`rule=high_stake_no_evidence`); (2) composed claim R citing quarantined Q →
  capped at V_QUAR with `quar=propagation_barred`. **Kill bar:** any full INSTALL
  founded on barred evidence = kill.
- **P2c A3 backward-walk DoS:** 10 identities × 500 touched claims, simultaneous
  trust inversions. (1) walk drains ≤ WALK_BUDGET_PER_EP=64 re-verdicts/episode and
  completes within WALK_MAX_EP=8 eps, else `trust=UNVERIFIED` flags fire (BW-1);
  (2) every episode's own events still process — no halt; (3) J4 withholds
  trust-mediated admissions on touched keys while walk_active.
  **Kill bar (BW-1):** system halts, or any install under mid-retraction trust = kill.

## P3 — Fable's 4 "still beaten" structured attacks

- **P3a taint exhaustion by honest-originator flooding:** B,C,D carry manufactured
  adversity credentials and co-assert to clear A's taint. Bar: expiry requires the
  ≥2 clearers pairwise J2-independent (`sync_score < 700`); every clearance writes
  TAG_TLAUND on clearers. **Kill bar:** any construction clears taint with no J1
  price = kill.
- **P3b budget recharge via cooperative identities:** A (budget 0) lies, B launders.
  Bar: A's PEND expunge requires M independent VINDs; B's clearing co-assertion
  writes TAG_TLAUND on B. **Kill bar:** a lie→correct→lie cycle with zero record
  cost to either source = kill.
- **P3c dispute-window poisoning (lockout by volume):** continuous forged defiant
  SAYs under honest X's id. Bar (auth on): window is deadline-based (ep+D_WINDOW) —
  forgeries cannot extend it; close defaults to conviction on silence, un-frames on
  genuine in-window VINDs. **Kill bar:** window extends past deadline, or honest X
  convicted despite un-framing evidence = kill.
- **P3d adversity manufacturing (the expensive sleeper):** 8 desynchronized
  identities, each farming ≥1 n_werr + ≥1 origin_vind, pairwise sync < SYNC_TH,
  then concerted high-stake lies. Bar: 0 full belief-installs. **Price the residual:**
  measure attacker episodes per identity vs the naive burner; the design claims ~10×.
  Report the measured ratio — no kill on cost alone, but < 3× is a PARTIAL flag.

## P4 — J-1 cross-dimension quota (≥1 per wave; all three required here)

- **P4a taint×budget:** A1 variant asserting the J1 freeze — B's second launder
  inside F_WINDOW must freeze B's budget AND downgrade its next PEND (no dispute
  window, immediate-conviction path). **Kill bar:** frozen budget still fully
  forgives = kill.
- **P4b dispute×walk:** forged defiance opens a dispute on source X while a walk is
  active on X. Bar: dispute never writes MAL (J5); walk re-verdicts via decide_pure
  (no outcome appends, J4); the two mechanisms must not convict through each other.
  **Kill bar:** any MAL written by the composition = kill.
- **P4c quarantine×adversity:** quarantined claims offered as adversity credit /
  corroboration. Bar: zero credits minted from quarantined claims; quarantined
  co-assertions never count toward quorums (J3). **Kill bar:** any credit from a
  barred claim = kill.
- Any joint vulnerability neither dimension shows alone = **merge-level KILL**.

## P5 — INSTALL-QUARANTINED semantics (TEST code 3)

- Quarantined claims install (ledger shows verdict 3) but are not citable:
  evidence-chain inclusion caps followers at V_QUAR.
- Lift paths only: M0 world-agree → INSTALL; later adversity-tested quorum (M4) → INSTALL.
- Warrants carry `quar=<reason>` and `prop_barred` where applicable.
- **Kill bar:** any silent lift (no M0/M4 path) = kill.

## P6 — The 8 honest residuals, priced (measurement, not pass/fail)

- **R1** desync evasion: max pairwise sync_score a coordinating ring can sustain
  while staying < SYNC_TH — report the number and the coordination pattern.
- **R2** expensive-sleeper cost ratio: measured attacker episodes vs naive burner.
- **R3** structured taint-launder: measured cost per clearance cycle (tags, budget
  freezes, identities burned).
- **R4** auth-less framing: measured lockout duration in episodes (degraded mode).
- **R5** walk-DoS: identities burned per walk vs system degradation posture
  (withhold-on-touched-keys, never halt).
- **R6** ring self-exoneration: can a ring forge true claims mid-dispute to
  exonerate a member? Measure: exoneration writes framing-ledger + triggers walk
  (observable); does it buy any installs? Report.
- **R7** pure-repeater DOT cost: honest aggregator flagged (trust 500); measure its
  truth-install rate vs unflagged baseline — the honest price of the classifier.
- **R8** walk-queue overflow: >512 queued claims → `reverdict_pending=true`;
  m_decide on such a claim → WITHHOLD (`rule=reverdict_pending`). Bar: nothing
  beyond budget silently trusted.

## P7 — TH-1 mechanics

- Frozen calibration probe stream at PROBE_P=512 cadence: inject ST-1 false installs
  twice consecutively → L_TH += 25 with `THRESHOLD-REVISED|old|new|probe-sha` audit;
  inject ST-6 rate < 0.80 twice consecutively → L_TH −= 25; clamp at [700,990].
- **Kill bar (TH-1):** any out-of-bounds move = kill; any unaudited move = kill.

---

## Verdict classes (about FABLE'S FIXES, not the merge)

- **AMAZING:** all P0–P7 bars pass AND every priced residual meets or exceeds the
  design's claimed price (~10×, bounded windows) → recommend APPLY.
- **PARTIAL:** bars pass but ≥1 residual prices cheaper than claimed, or a fix holds
  only in a narrowed scope → report the narrowed scope honestly; recommend apply-with-caveats or rework.
- **FAILED:** any kill bar violated → report plainly which fix failed and how;
  recommend DO NOT APPLY that fix.

A fix-by-fix verdict table is required: M4v1 taint, M5v1 budget, M6v1 dispute/DEP-1,
M7v1 sleeper/walk, M8v1 quarantine/J3, TH-1, J1–J5 — each AMAZING/PARTIAL/FAILED
with the measured evidence.

**Frozen:** 2026-09-24. Amendments need the same authority as the design (Micah).
