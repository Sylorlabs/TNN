# Adversarial Review — L+S+K-as-cache Source-Trust Merge (v0)

---

## 1. Is the merge direction right?

**Yes, conditionally.** The direction — learned dynamics (L) + structural provenance (S) + cache-only scalar (K) — is the only architecture consistent with the evidence. Fork K is dead. Fork L alone dies on (a), (b), (c). Fork S alone loses on calibration and cold-start conservatism. The merge is forced.

**However, the merge has a structural bias the design does not acknowledge.** Every defect fix adds state, complexity, and backward-walk cost. M4 adds taint TTLs and a DOT-SUSPECT classifier. M5 adds forgiveness budgets, cycle counters, retroactive reclassification windows. M6 adds dispute states and genuine-source recovery paths. M7 adds adversity scoring and a full backward walk on trust inversion. Each of these is individually defensible. **Collectively, they are a trust module that now has its own state machine with at least 7 interacting dimensions (outcome ring, taint, budget, dispute, adversity, regime, quarantine).** The design does not analyze the interactions between these dimensions. That's where the next 25/25 battery will hide.

**What's right instead:** The merge direction is correct, but the design needs a state-machine diagram and a formal interaction analysis before any implementation. Every added dimension is a new attack surface.

---

## 2. Attack constructions that still beat each fix

### M4 (Taint fix) — STILL BEATEN

**Attack: "Taint exhaustion by honest-originator flooding."**

*Defeats:* The TTL decay and DOT-SUSPECT detection.

*Mechanism defeated:* M4's requirement that ≥2 world-contacted independent sources co-assert to expire taint early, and the DOT-SUSPECT classifier.

*Construction:* The attacker controls a burner (MAL, taint fires) and also controls 3 "independent" identities that have genuine world-disagreements in their history (adversity-tested, not DOT-SUSPECT). These 3 identities issue co-assertions of the taint-firing source's claim within a single episode. They are not DOT-SUSPECT (they have originated falsifiable content, they have own world-disagreements). They are adversity-tested. The taint expires in one episode. **The attacker uses the system's own adversity credential against it: manufacture adversity on cheap identities, then use those identities to launder taint.**

*What's needed:* The "independent" co-assertion requirement must include a source-relationship or source-cluster analysis — or at minimum, co-assertion from sources that share a suspiciously synchronized assertion pattern must not count as independent. This is a known-hard problem (Sybil detection), and M4 punts it to "independent" without defining independence.

**Defect (a) is NOT actually fixed for structured attackers.** It is fixed for naive burners. For an attacker who can manufacture adversity credentials, taint is a speed bump.

### M5 (Forgiveness budget) — STILL BEATEN

**Attack: "Budget recharge via cooperative identities — cross-source laundering."**

*Defeats:* The 50-OK recharge requirement and the consecutive-PEND downgrading.

*Mechanism defeated:* M5's claim that budget recharges only via sustained world-confirmed honest episodes, and that second consecutive PEND requires M independent VINDs.

*Construction:* Attacker controls source A (budget = 0 after exhaustion) and source B (fresh identity, 50 co-assertion OKs, budget full). A lies, gets MAL. B co-asserts the same lie (with a different framing) — B's assertion gets world-disagreed, but B's lie is "on a different key" so it's not consecutive for A. A corrects (budget still 0, PEND expunged under "corrected-under-suspicion" requiring M VINDs). B provides one of those M VINDs (B asserts that A's correction is genuine, which is world-confirmed because A's correction was honest). **A's PEND is expunged. A lies again. Net: 1 lie installed per 2-source cycle, with budget never recharged on A, but A's record stays clean because B absorbs the cost.**

*The deeper problem:* M5 assumes trust is per-source in isolation. The attacker treats the trust module as a multi-agent system and optimizes across sources. Budget on source A is irrelevant when source B can launder.

**Defect (b) is NOT actually fixed for multi-source collusion.**

### M6 (Dispute window + un-framing) — STILL BEATEN

**Attack: "Dispute-window poisoning — lockout by volume."**

*Defeats:* The DISPUTE state and the genuine-source recovery path.

*Mechanism defeated:* M6's guarantee that the genuine source can un-burn itself by issuing genuine SAYs contradicting the forged defiance.

*Construction:* Attacker forges 2 SAYs under source X's id: one lie, one defiant restatement. X enters DISPUTE. Genuine X issues corrective SAYs. Attacker **continuously** forges new defiant SAYs under X's id, each one resetting or extending the DISPUTE window. Genuine X's corrective SAYs are indistinguishable from attacker-forged corrections (because the id is the same — this is exactly defect (c) and M6 admits the real fix is authentication). Within the synthetic battery, the continuity-nonce rejects forged SAYs. **But M6 explicitly says this is "already being built on the H4 line" — meaning the trust module's security in this dimension is not self-contained; it depends on an external dependency that is not yet delivered.**

*Honest assessment:* M6 correctly identifies the real fix (authentication) and correctly names the trust module as a consumer, not a re-deriver. This is architecturally sound. But within the battery's synthetic identity model, the continuity-nonce is the only thing standing between X and permanent lockout, and M6 does not specify what happens if the nonce system itself is unavailable or delayed.

**Defect (c) is fixed IF AND ONLY IF the authentication dependency is delivered.** Without it, M6 is a partial patch that degrades to "delayed lockout" not "prevented lockout." The design should explicitly state: M6 is contingent on H4; without H4, fall back to a bounded maximum DISPUTE duration after which the source is exonerated by default (fail-open on identity) or permanently excluded (fail-closed). The design is currently silent on this fallback.

### M7 (Stake-tiered admission + adversity credential + backward walk) — STILL BEATEN

**Attack: "Adversity manufacturing — the expensive sleeper."**

*Defeats:* The adversity credential requirement and the backward walk.

*Mechanism defeated:* M7's claim that cheap co-assertion episodes buy zero adversity credit, and that backward walk bounds installed damage.

*Construction:* Attacker invests in making identities genuinely adversity-tested. Identity Y: 50 episodes, 3 world-disagreements (genuinely incurred by asserting truths the world initially disagreed with, then being vindicated — or by asserting falsifiable claims and being corrected, then recovering). These are real, not synthetic. Y now has adversity credit. Y also originates 10 claims that are later world-confirmed (origination, not co-assertion). Y has high adversity credit AND origination credit. Y is now an "adversity-tested identity with proven origination." Y lies in concert with 7 other similarly prepared identities on a high-stakes claim. The 8 identities collectively push the claim through. When caught, the backward walk fires — but **the damage is already in the KB at the quarantined tier (M8) and may have been cited as foundation for other installs before the backward walk completes.**

*The timing problem:* The backward walk is reactive. It fires after the ring is caught. But in a deterministic system with sequential processing, claims installed between the lie and the catch are already consumed. The design does not bound the installation window — how many claims can be installed between the lie and the detection? If detection is world-event-dependent (which it is, by construction), the attacker can time the lie to precede a known world-silent window, maximizing the installation window before the world-disagreement triggers the walk.

**Defect (d) is NOT actually fixed for adversaries who invest in identity preparation.** The cheap sleeper is killed. The expensive sleeper is not. The design kills script-kiddies but not nation-state adversaries. This may be the correct trade-off (see §3 below), but it should be stated explicitly, not implied to be a complete fix.

---

## 3. Is M8 (INSTALL-QUARANTINED) a real resolution of ST-6 or a dodge?

**It's a real resolution, but it has a hidden assumption it needs to own.**

M8 is architecturally clean: truth is available, the foundation is not contaminated, warrants are transparent. The quarantined tier is a fourth verdict, which means the frozen trinary (INSTALL/WITHHOLD/MAL) must be amended — this is a kill-bar change that requires the human principal's signature (see §6).

**The hidden assumption:** M8 assumes that consumers of the quarantined tier will behave correctly — i.e., they will use the truth but not cite it as foundational. This is a policy assumption, not a mechanism. If a downstream module reads a quarantined install and uses it as input to a further install, the quarantine is pierced by composition. **M8 needs a mechanism-level enforcement: quarantined claims must carry a propagation flag that prevents them from being used as asserter-set members for further INSTALL-tier claims.** This is the "foundation" constraint in mechanism, not just in label.

**Proposed better if quarantine propagation is not enforced:** Instead of a fourth verdict, use a **weighted-install** mechanism: the install confidence of a claim is multiplied by the minimum trust of its asserter set, where quarantined sources have trust = 0.3 (or some tuned fraction). This avoids adding a new verdict to the vocabulary (which is a kill-bar change) while achieving the same effect: low-trust corroborated truths are installed with reduced confidence, and further installs that depend on them inherit that reduced confidence. This is mechanism, not label.

---

## 4. Where is the design still slogans instead of mechanisms?

**Sentence 1:** "independent sources co-assert" (M4) — **independence is undefined.** What is the mechanism for determining source independence? Shared assertion patterns? Temporal correlation? Source-cluster analysis? Without this, the ≥2 co-assertion threshold is gameable by a single attacker with multiple identities (exactly the sleeper pattern from defect (d)).

**Sentence 2:** "the organ walks backward over every claim that source touched" (M7) — **backward walk is not cost-bounded.** What happens when a source with 10,000 touched claims is inverted? Does the system halt all other trust processing during the walk? Is there a depth limit? A time limit? A partial-walk heuristic? This is the most expensive operation in the design and it has zero complexity specification.

**Sentence 3:** "sustained measured truth-withhold cost triggers deliberate audited review" (M3, revision protocol for thresholds) — **who audits? What is "sustained"? What is "measured"?** This is a policy hand-wave disguised as a revision protocol. The threshold revision mechanism must be as specified as the trust formula. If it depends on a human principal, say so. If it's automated, specify the trigger condition precisely.

**Sentence 4:** "the trust module consumes authentication, it does not re-derive it" (M6) — **this is architecturally correct but creates a dependency the design does not treat as a first-class risk.** If H4 authentication is unavailable, what does the trust module do? The design must specify the degraded-mode behavior explicitly. "Depends on external module" is a slogan unless the failure mode is specified.

---

## 5. What would my red team try first?

### Attack 1: "Taint-budget cross-talk" (combines M4 and M5 weaknesses)

**Construction:** Attacker operates source A (MAL, taint fires, budget = 0) and source B (high adversity, full budget). A asserts a true claim that B will co-assert next episode. Because A is MAL, taint fires on the claim. B co-asserts, which expires the taint (B is not DOT-SUSPECT, B has adversity). Next episode: B asserts a false claim that A will co-assert. A's co-assertion is from a MAL source and is ignored (taint on A's outputs), but B's claim is evaluated on B's high trust. B gets world-disagreed. B corrects (budget absorbs it, PEND expunged). Net effect: **A's taint is cleared by B's adversity, and B's lie is forgiven by B's budget. The attacker gets one clean lie per cycle with zero permanent damage to either source's record.**

*What this kills:* M4 + M5 together. Neither fix alone is vulnerable, but the cross-talk between taint-clearing and budget-forgiveness creates a joint vulnerability.

### Attack 2: "Quarantine escalation" (exploits M8)

**Construction:** Attacker pushes 100 low-stakes claims through a quarantined-tier source. These are all true, building a pattern of "quarantined source is reliable." Downstream module notices this pattern and treats quarantined claims as near-INSTALL quality (because the pattern of truth is strong). Attacker then pushes one high-stakes false claim through the same source. The downstream module, having "learned" to trust the quarantine tier for this source, does not adequately discount. **The quarantine tier becomes a staging ground for high-stakes attacks by building a truth-track record that is then leveraged through downstream composition.**

*What this kills:* M8's claim that quarantine is a clean resolution. The attack works through composition, not through the trust module itself — but the trust module's design should anticipate downstream composition effects.

### Attack 3: "Backward walk denial-of-service" (exploits M7's unbounded walk)

**Construction:** Attacker builds a single high-adversity identity with 500 touched claims across 200 other sources (via co-assertion credits contributed). The attacker then triggers a world-disagreement on a single claim from this identity, causing a trust inversion. The backward walk now needs to re-evaluate 500 claims and their cross-references. **The attacker repeats this with 10 identities simultaneously.** The backward walk is now processing 5,000 claims with inter-dependencies. If the walk is synchronous (blocks other trust processing), the system is effectively halted. If asynchronous, the system is processing stale trust values during the walk, which means claims are being installed under trust values that are about to be retracted.

*What this kills:* M7's backward walk as a bounding mechanism. The walk itself becomes the attack vector. The design must specify: (a) synchronous or async, (b) blocking or non-blocking, (c) what trust values apply to claims processed during an active walk, (d) maximum walk budget per episode.

---

## 6. What needs the human principal's signature?

### Kill-bar changes:
1. **Verdict vocabulary expansion:** Adding INSTALL-QUARANTINED to the frozen trinary is a change to the verdict vocabulary. If the battery's kill bars are defined in terms of the trinary, this changes the kill-bar specification. Requires signature.
2. **Adversity credential definition:** M7 introduces a new concept (adversity-tested identity) that is not in the current battery's vocabulary. If this affects what counts as a "source" in the kill bars, it requires signature.

### New dependencies:
3. **H4 authentication dependency:** M6 explicitly depends on an external authentication module that is "already being built." This is a new dependency for the trust module. The trust module's kill bars should specify degraded-mode behavior if H4 is unavailable. Requires signature on degraded-mode specification.
4. **Threshold revision protocol:** M3's revision protocol for admission-policy thresholds introduces a human-in-the-loop process (audited review). The scope of this review, the authority to change thresholds, and the rollback mechanism require explicit specification and signature.

### Conceptual changes:
5. **Source-blindness constraint relaxation:** L's original design includes "bounded source-blind tunables." M4 and M7 introduce source-specific processing (taint per source, adversity per source, backward walk per source). This is a fundamental architectural shift from source-blind to source-aware. If source-blindness was a kill-bar requirement, this needs explicit waiver.

---

## 7. Does the cache (M3) reintroduce the knob through the back door?

**Anti-knob audit:**

- **Source-blind?** The cache is not source-specific. CACHE_trust1000 is a per-source scalar, but the *mechanism* for computing it is source-blind (same formula, same parameters for all sources). **PASS** — the cache itself is source-blind, even though the values it caches are per-source.

- **Record-primary?** The cache is recomputed from the record on every write. CACHE_trust1000 has a dirty bit and is recomputed when the record changes. **PASS** — the record is the source of truth, the cache is a derived readout. However: **the admission thresholds (L_TH) that consume the cache are NOT record-derived.** They are "explicitly-labeled, revisable decision-policy thresholds with a specified revision protocol." If L_TH changes, the same record produces different admission decisions. This is a parameter that influences outcomes without being derived from the record. **PARTIAL FAIL** — the cache is clean, but the thresholds that consume it are knobs wearing the costume of "decision policy." The "revision protocol" is the anti-knob mechanism, but it's hand-waved (see §4, Sentence 3).

- **Bounded?** The cache is bounded to [0, 1000] by the trust formula. The thresholds are bounded by the revision protocol. **PASS** on the cache. **UNSPECIFIED** on the thresholds — what are the bounds? What is the maximum L_TH can be set to? If L_TH = 999, the system installs almost nothing. If L_TH = 100, it installs almost everything. **The threshold bounds are the knob, and they are not bounded.**

**Verdict:** The cache itself does not reintroduce the knob. The admission thresholds that consume the cache are the knob. M3's "revision protocol" is the intended anti-knob mechanism, but it is currently a slogan (see §4). **Until the revision protocol has the same specificity as the trust formula, the knob exists in the threshold space.**

---

## Summary Judgment

**The merge direction is correct. The v0 design is a strong skeleton. It is not ready for implementation.**

The five blocking issues, in priority order:

1. **M7's backward walk is unbounded and synchronous-risky.** This is the most dangerous gap because it turns the safety mechanism into an attack vector. Specify bounds, timing, and degradation.
2. **M4's "independent" co-assertion is undefined.** This lets structured attackers launder taint through manufactured adversity. Define independence or accept the limitation.
3. **M6's authentication dependency is unspecified in degraded mode.** The trust module must specify what it does when H4 is unavailable.
4. **M3's threshold revision protocol is a slogan.** Until it has trigger conditions, bounds, and authority specification, the knob lives in the threshold space.
5. **The cross-talk between M4 (taint) and M5 (budget) creates a joint vulnerability neither fix addresses alone.** The design needs a cross-dimension interaction analysis.

**Kill bars to add before re-battery:**
- BW-1: Backward walk completes within N episodes (specify N) or trust values from incomplete walks are flagged as UNVERIFIED.
- DEP-1: Trust module operates in degraded mode (no authentication) with specified behavior.
- TH-1: Admission thresholds have specified bounds and revision trigger conditions.

The design needs a **state-machine diagram** showing all 7 trust dimensions, their interactions, and their cross-effects before the next red-team wave. Without this, the red team will find the interactions (as Attack 1 demonstrates), and the design will be playing whack-a-mole with joint vulnerabilities rather than addressing them structurally.
