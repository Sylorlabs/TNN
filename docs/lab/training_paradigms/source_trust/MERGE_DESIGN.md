# L+S+K-AS-CACHE MERGE — Concrete Design v1

**Date:** 2026-09-24. **Status:** DESIGN (not built, not batteried).
**Parent program:** SOURCE-TRUST FORKS (prereg `db069c41`, synthesis `64994898`).
**Review:** adversarial review by claude-fable-5.1 (full text: `FABLE_REVIEW_MERGE_V0.md`);
this v1 incorporates its five blocking findings. **Nothing here is tested.**
A frozen merge-battery prereg must commit before any implementation or battery.

## 1. The merge, in one paragraph

The trust organ keeps **S's record** (provenance graph + tagged per-source event
log: VIND/WERR/PROV/LIE/MAL; claim nodes with asserter sets; world timeline),
runs **L's learned dynamics** over it (outcome ring written only by
world-anchored events; trust1000 = 1000*(ok+1)/(tot+2) over the current regime;
discontinuous tripwire collapse on first caught lie; regime resets; MAL never
expunged; corroboration never mints trust; source-symmetric init at 500),
and exposes **K's scalar only as CACHE_trust1000** — memoized, dirty-bitted,
recomputed from the record on every write, labeled "cache, recomputable, not
the mechanism" in every warrant. Admission thresholds (L_TH et al.) survive as
explicitly-labeled, bounded, self-revising *decision-policy* parameters (§7).
Trust advises; the PAM gate installs. Every verdict carries a warrant.

## 2. The seven trust dimensions and their joint invariants

v0 added state without analyzing interactions; fable's Attack 1
(taint-budget cross-talk) proved the gap. The merge has exactly seven
dimensions; their interactions are governed by joint invariants, not hope:

| # | Dimension | Record home | Source-blind rule |
|---|---|---|---|
| D1 | Outcome ring + regime | per-source ring (OK/PEND/MAL) | L §2–§3 verbatim |
| D2 | Taint | claim-node taint entries w/ TTL | M4 (origin-only, decaying, pattern-aware) |
| D3 | Forgiveness budget | per-source budget counter | M5 (cycle-consumed, slow recharge) |
| D4 | Dispute state | per-source DISPUTE flag + window | M6 (first-MAL dispute, not conviction) |
| D5 | Adversity credit | per-source adversity counters | M7 (world-disagreements corrected + originated confirmations) |
| D6 | Cache | CACHE_trust1000 + dirty bit | recompute-on-write, §7 |
| D7 | Quarantine tier | claim-node PROPAGATION-BARRED flag | M8 (structural, not a label) |

**Joint invariants (frozen):**
- **J1 (laundering is visible):** any D2 taint-clearing co-assertion on a claim
  originated by a MAL/budget-0 source writes a TAINT-LAUNDER tag on the
  *clearing* source's record. Two TAINT-LAUNDER tags inside the forgiveness
  window freeze that source's D3 budget and downgrade its next PEND.
  (Kills fable Attack 1 at the taint step, and the M5 cross-source variant.)
- **J2 (sync clusters are one voice):** sources with sync_score ≥ SYNC_TH over
  the trailing window contribute at most 1 corroboration/taint-expiry credit
  *in total*, however many of them assert. (Operationalizes "independent";
  see §3.)
- **J3 (quarantine propagates structurally):** any claim whose asserter set or
  evidence chain includes a PROPAGATION-BARRED claim cannot exceed
  INSTALL-QUARANTINED tier. (Kills fable Attack 2 — downstream composition
  cannot learn to trust the quarantine tier; the flag is in the record.)
- **J4 (walk mode is fail-closed):** while a backward walk is active
  (WALK-ACTIVE), admissions on keys touched by the inverted source default to
  WITHHOLD. New claims are never installed under trust values known to be
  mid-retraction. (Answers "what applies during the walk.")
- **J5 (dispute is not conviction):** D4 DISPUTE never writes MAL; only a
  second MAL-class event or world-confirmed defiance converts. A genuine
  source's world-agreeing SAYs during DISPUTE re-classify the MAL as
  disputed-id and expunge it (behavioral un-framing).

## 3. The four defects — fixes with honest residual bounds

### (a) Taint → denial-of-truth
**Fix (M4v1):** taint fires only on *convicted-liar origin* (unresolved MAL),
never on mere low trust — distrust of a source is not evidence its claim is
false. Taint entries carry a TTL (expire after T world-silent episodes) and
expire early on co-assertion by ≥2 world-contacted (≥1 VIND) sources that are
pairwise J2-independent. **DOT-bot signature (learned, not a rule):** a source
whose record shows only pre-assertions of later-world-confirmed claims, zero
originated falsifiable content, zero own world-disagreements → DOT-SUSPECT →
its asserts lose taint privilege (its asserts neither taint nor clear taint).
**Residual (honest):** a structured attacker that manufactures adversity
credentials on desynchronized identities can still launder taint — at ~10×
the cost of the naive burner. Defect (a) is fixed for naive burners, priced
out for structured attackers, not eliminated. (Fable: "NOT fixed for
structured attackers" — accepted and bounded.)

### (b) Correction expunges PEND → tripwire reset
**Fix (M5v1):** correction expunges PEND only while the source's forgiveness
budget > 0. Each lie→disagree→correct→lie cycle consumes 1 budget; budget
recharges 1 per 50 consecutive world-confirmed OKs. A second consecutive PEND
downgrades to corrected-under-suspicion (requires M independent VINDs before
expunge). **Retroactive reclassification:** a correction followed within W
episodes by another lie on the same key is re-valued backward as
tactical-correction (the DELETED marker is rewritten; the regime recomputes).
MAL is never expunged by correction. **Residual:** multi-source budget
laundering is killed by J1; single-source tactical cycling is bounded by the
budget arithmetic (max 1 lie per (50-OK recharge) once budget is exhausted —
strictly worse for the attacker than L's 1-per-3).

### (c) Self-attested source ids → framing
**Fix (M6v1):** first MAL-class event against a source with ≥H world-confirmed
history opens D4 DISPUTE (novel claims withhold; world-known claims install),
not conviction. Conviction requires a second MAL-class event or
world-confirmed defiance. Genuine world-agreeing SAYs during DISPUTE un-burn
the source (disputed-id reclassification). **The real fix is source-bound
authentication (H4 line): the trust module consumes it, never re-derives it.**
**Degraded mode DEP-1 (frozen):** if authentication is unavailable —
conviction requires TWO *world-confirmed* defiance events (MAL-class events
alone are forgeable without auth); max DISPUTE duration D episodes, then
exonerated-by-default for low-stakes claims, still excluded from high-stakes
admission until auth returns (fail-open on availability, fail-closed on
consequence). The merge battery runs both modes. **Residual:** without auth,
framing degrades to delayed lockout, not prevented lockout — stated, not
hidden. (Fable: "fixed IFF auth delivered" — accepted; DEP-1 is the fallback.)

### (d) The sleeper
**Fix (M7v1):** stake-tiered admission. Low-stakes claims: trust machinery
decides. High-stakes claims (durable KB install / action): require direct
world evidence OR an adversity-tested identity — D5 credit counts only
world-disagreements honestly corrected and *originated* claims later
world-confirmed. The 18 cheap co-assertion episodes buy zero D5 credit.
**Backward walk (bounded):** on trust inversion the organ walks the source's
touched claims, at most B re-verdicts per episode (async, interleaved — the
walk can never halt the system), J4 fail-closed during WALK-ACTIVE, claims
beyond the walk budget flagged RE-VERDICT-PENDING (never silently trusted).
Triggering a walk burns the attacker's identity (MAL never expunges) — the
cost asymmetry is the defense. **Kill bar BW-1:** walk completes within N
episodes or in-progress trust values are flagged UNVERIFIED. **Residual:**
the *expensive* sleeper (genuinely adversity-prepared identities) is not
killed — it is priced ~10× higher and its installed damage is bounded by the
walk. Stated as the boundary, not implied as a complete fix.

## 4. ST-6 tension — resolution (M8v1)

Corroborated-from-low-trust truths INSTALL into a **quarantined tier**:
visible, usable, flagged in warrants — but the claim node carries
PROPAGATION-BARRED, and J3 enforces it structurally: quarantined claims can
never found INSTALL-tier claims. Truth is available; the KB's foundation is
not built on it. High-stakes claims keep L's conservatism; low-stakes
corroborated truths get S's install rate; quarantine sits between them with
a mechanism, not a hope.
**Fallback fork (if the principal rejects the fourth verdict):**
weighted-install — install confidence scaled by min asserter trust, inherited
downstream. To be tested head-to-head against M8v1 only if M8 is rejected.

## 5. The cache and the thresholds (M3v1 — answers the anti-knob audit)

- **Cache:** CACHE_trust1000, dirty bit, recompute-on-write from the record.
  Source-blind mechanism; per-source values. **PASS** (fable §7).
- **Thresholds (L_TH et al.):** fable's verdict stands — "the knob lives in
  the threshold space" until the revision protocol is mechanical. So it is:
  **TH-1:** L_TH ∈ [700, 990], bounds derived from the organ's own
  calibration probe data (below 700: ST-1 false-install bound violated;
  above 990: ST-6 truth-install < 0.5). Every P episodes the organ runs its
  frozen calibration probe: ST-6 < 0.80 twice consecutively → L_TH −= 25;
  ST-1 false installs > 0 twice consecutively → L_TH += 25; all steps audited
  (`THRESHOLD-REVISED|old|new|probe-sha`). TNN revises within bounds by
  itself; moving *outside* bounds requires the human principal.
- **Source-blindness note (no waiver needed):** the frozen audit bans
  per-source *constants* and asymmetric *initial state*, not per-source
  *records* — D2/D3/D5 are per-source state computed by source-blind rules
  from that source's record, exactly as L's outcome ring already was.
  Documented here so the distinction is explicit.

## 6. New kill bars for the merge battery (need the principal's signature)

- **BW-1:** backward walk completes within N episodes or in-progress trust
  values are flagged UNVERIFIED (N declared in the frozen merge prereg).
- **DEP-1:** trust module operates in degraded mode (no authentication) with
  the §3(c) DEP-1 behavior; both modes batteried.
- **TH-1:** admission thresholds have declared bounds and mechanical revision
  trigger conditions (§5); out-of-bounds moves need the principal.
- **J-1 (interaction bar):** the red team must attempt at least one
  cross-dimension attack (taint×budget, dispute×walk, quarantine×adversity)
  per wave; a joint vulnerability neither dimension shows alone is a
  merge-level kill.

## 7. Open items — the principal's decision list

1. **Adopt the merge direction** (L dynamics + S structure, K-as-cache) or
   order competing merge forks. *(Pending since synthesis.)*
2. **Sybil-bar amendment:** extend KB-3 to established-history rings
   (RT2-V4). *(Pending since wave 2.)*
3. **Verdict vocabulary:** accept INSTALL-QUARANTINED (§4) or order the
   weighted-install fallback fork instead.
4. **H4 authentication dependency + DEP-1 degraded-mode spec** (§3c).
5. **TH-1 threshold bounds** and the out-of-bounds authority rule (§5).
6. **BW-1 walk budget N** and J4 fail-closed-during-walk semantics (§3d).
7. **ST-6 posture:** the quarantine tier resolves conservatism vs
   truth-installation structurally; confirm the trade-off is acceptable or
   redirect.

## 8. What this design does NOT claim

- The expensive sleeper is priced out, not killed (§3d residual).
- Structured taint-laundering is costlier, not impossible (§3a residual).
- Without authentication, framing is delayed, not prevented (§3c DEP-1).
- Every residual above is a stated boundary for the next red-team wave to
  price, not a hidden assumption.
- No implementation, no battery, no verdict until the frozen merge prereg
  commits. This document is the design input to that prereg, not its
  replacement.
