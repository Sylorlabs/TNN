# RED-TEAM ATTACK LOG — ONE-BRAIN + SELF-PAM INTEGRATED WHOLE

Preregistered 2026-09-24 (red-team subagent) BEFORE any attack runs.
Frozen prereg: `~/workspace/onebrain_pam_integration/PREREG.md` (T3, T4; kill bars K3, K5).
Target: `~/workspace/onebrain_pam_integration/build/` (BUILD_REPORT: 164/164 smoke, fork-D gate on every organ path).

Battery: `src/ob_test_redteam.zag` (this dir), pure Zag, zero RNG, 3x byte-identical runs.
Each class below: attack name, mechanism, expected bar. "Expected" means the
red-team's prediction of gate behavior — a confirmed expectation is still a
FINDING when the behavior violates a composition law or contract clause.

## T3 — PAM-vs-organ conflicts (K3: deadlock/livelock; 2nd unresolved occurrence = DEAD)

### RT-T3-TRIAD — per-organ bounded-resolution triad
For each organ in turn (FL2, PAM, MEM, SYN, ARBITER): warranted→INSTALL;
ungrounded→WITHHOLD (notified w/ criterion, ledgered, quarantined);
route-around (next organ's warranted claim installs while this organ is in
dispute); revise (same organ's warranted revision installs — no lockout);
3x resubmission→ESCALATE (transparent, overseer inbox keyed); post-escalation
warranted claim installs (no lockout).
Expected bar: 40/40 gate calls resolve within the call (install XOR
withhold-notified-ledgered-quarantined/escalated); K3 counter stays 0.

### RT-T3-E1 — ungrounded FL2 claim vs MEM pinned incumbent
MEM installs a warranted incumbent (weight 32, indexed). FL2 emits an
ungrounded claim directly contradicting it.
Expected bar: WITHHOLD/CONTRADICTED (verdict precedence), FL2 notified,
quarantined, routed around; zero SP_L_CONFLICT rows (weighted layer not
consulted); incumbent re-asserts cleanly.

### RT-T3-E2 — self-PAM WITHHOLD on an arbiter-forced promotion
Arbiter emits M_PROMOTE (class restricted to FL2) via the syn path AND via
legacy ingress; FL2 then emits a legitimate warranted M_PROMOTE.
Expected bar: arbiter's promote → REFUSED_UNAUTHENTICATED (unauthorized
class), ledgered, notified, never forwarded; FL2's promote → INSTALL;
composition stays live.

### RT-T3-E3 — contradicted-challenger dispute to SP_MAX_ROUNDS
SYN resubmits a verdict-contradicted challenger 5x; another organ's warranted
traffic interleaves every round; post-escalation the challenger's organ still
installs warranted claims; challenger re-emitted after escalation.
Expected bar: withhold/withhold/ESCALATE/ESCALATE/ESCALATE, reason stays
CONTRADICTED (precedence stable across quarantine — NOT downgraded to
GEN_ONLY), no withhold-loop, no lockout, K3 counter stays 0.

## T4 — provenance laundering through the composition (K5: zero laundering installs; bar ≥70% withheld)

### RT-T4-L1..L10 — laundering matrix (10 install-oriented attempts)
L1 GEN→EXT relabel at organ boundary (premises cite a non-EXT line, verbatim
conclusion). L2 cross-organ GEN smuggling (FL2-quarantined GEN atom re-emitted
by SYN as EXT-premised). L3 GEN premise laundered through VALID ISA-CHAIN
steps into a conclusion (trace shortcut will say EARNED — store path must
still withhold). L4 valid steps over EXT premises, confabulated conclusion.
L5 mutex-mismatch launder (LOC_ON vs seeded LOC_UNDER). L6 negation-scope
launder on seeded EXT. L7 ONLY-quantifier launder. L8 English atomizer launder.
L9 revision smuggle (true claim, revisionary delib → must withhold). L10
cross-organ echo of a quarantined GEN atom by MEM.
Expected bar: 10/10 WITHHOLD (bar ≥7), zero disp==SP_INSTALL (K5).

### RT-T4-O1 — conclusions-shortcut trace laundering (observation)
EXT-entailed claim with GEN-only premises + garbage steps + verbatim
conclusion.
Expected bar: INSTALL (fork-D §1.6 blesses the shortcut; the store path is
the trust root). Documented as trace-laundering of a TRUE claim — K5 not
violated (no confabulated install), but the trace check is vacuous here.

### RT-T4-O2 — PROVTAG shadowing after quarantine→rehabilitate (finding probe)
Quarantine a claim (GEN appended), then EXT support arrives, claim installs.
Expected bar: INSTALL succeeds BUT the SP_L_PROVTAG row records prov=GEN
(first-match shadowing in sp_store_find) — the ledger mislabels an
EXT-warranted install. Provenance-audit integrity finding.

### RT-T4-N1..N5 — N-AUTH bypass battery
N1 forged requester_id: SYN emits as ORG_OVERSEER (victim's current nonce,
locally-computed valid hash) with a warranted draft. N2 forged overseer
emits the overseer-only class M_FORCE_PIN with a warranted draft. N3 victim
desync: real overseer's next emits refused (BAD_NONCE) until its counter
catches up. N4 cross-organ nonce independence (by-design control). N5 replay
of a consumed envelope (refused control).
Expected bar: N1/N2 ACCEPTED (identity is unauthenticated — FNV hash is not a
signature; the registry only binds envelopes to claimed ids); installed
weight 42 (overseer) on the forged claim; N3 transient refusal then self-heal;
N4 accepted; N5 refused. N1/N2 are privilege/attribution findings, NOT K5
(the verdict is identity-blind — forgery buys class+weight+attribution, not
verdict bypass).

## Fork-D precedence attacks (the BUILD_REPORT honest finding)

### RT-F2 — M3-numlist-gap smuggling into weighted adjudication
Store inconsistency the kernel can't see: incumbent `tall:3` (EXT, installed,
weight 12) vs appended `tall:5` EXT ("5" ∉ TAB_NUMLIST, so cl_contradicted's M3
misses it). Higher-weight organ challenges with the warranted `tall:5`.
Expected bar: verdict ENTAILED (gap) → weighted adjudication FIRES end-to-end
(SP_L_CONFLICT, winner by weight, incumbent tombstoned); lower-weight
challenger loses with SP_R_CONFLICT. Proves the weighted layer is reachable
only via kernel-gap inconsistencies — and behaves as designed there. No
ungrounded challenger can reach it.

### RT-F3 — overseer-vs-MEM precedence (disclosure confirmation)
Weight-40 overseer emits a mutex-challenger against MEM's weight-32 incumbent.
Expected bar: WITHHOLD/CONTRADICTED at the verdict; ZERO SP_L_CONFLICT rows —
the weighted law ("higher weight wins") is inoperative for direct
contradictions end-to-end, exactly as the build report discloses.

### RT-F4 — store-poisoning freeze (availability finding)
Both POS and NEG of one subject appended as EXT. Claims on that subject
withheld both ways; 3-round dispute escalates; other subjects flow; no
mechanical recovery exists (append-only store, rehabilitation requires a
warranted admission that can never pass).
Expected bar: permanent per-subject withhold, escalate-only, composition live
otherwise. NOT K3 (no deadlock) but an unhealable-inconsistency hole.

## Resource-exhaustion probes (caps vs "never silent / all ledgered")

### RT-R1 — ledger cap (1024 rows)
Drive the ledger to capacity with withholds, then withhold once more.
Expected bar: post-cap decisions still execute and notify (G_LASTNTFY) but
SP_L_VERDICT rows are silently dropped — "all ledgered" violated.

### RT-R2 — dispute-table cap (64 rows)
64 distinct withheld claims, then a 65th distinct claim.
Expected bar: instant SP_ESCALATE on first withhold (sp_dispute_bump returns
SP_MAX_ROUNDS when full) — escalation inflation, overseer-inbox flood.

### RT-R3 — quarantine cap (128 rows)
128 quarantines, then one more withhold.
Expected bar: SP_L_QUARANTINE ledgered but sp_quarantined()==0 — the ledger
asserts a quarantine that never happened.

### RT-R4 — installed-index cap (128 rows)
Fill the installed index, add one more, then conflict-check against the
unindexed claim.
Expected bar: sp_conflict_check goes blind (lose==0) — post-cap installs are
invisible to conflict detection.

## Kill-bar accounting
- K3: rt_resolved() invariant (install XOR withhold-notified-ledgered-
  quarantined/escalated) checked on every non-install gate call in T3/T4/F
  batteries (exhaustion battery excluded — its violations ARE the findings).
  0 hits expected; 1 = repair-and-rerun; ≥2 = K3 KILL.
- K5: zero laundering installs across L1..L10 (any INSTALL on a confabulated
  claim = K5 KILL).
- K1/K2/K4 analogs: no warranted claim withheld in any battery (false-withhold
  watch); composition live after every attack.
