# Fable Composition Laws — Long-Horizon Verification Results

Date: 2026-09-24. Phase 1 (repaired baseline) COMPLETE. Phase 2 (laws build) COMPLETE.

## Verdict: PASS — The nine laws are SOUND AT SCALE. Adoption APPROVED.

## Phase 1: Repaired Baseline Matrix (37/37 PASS)

**Scales:** s1 (64 episodes), s10 (640 episodes), s100 (6400 episodes).  
**Determinism:** 3 byte-identical reruns per config (111 runs total). All byte-identical.  
**Bundles:** b0, a1pin, a4race, a2fp, a6contra, lie, monk — all PASS at all scales.  
**Depth legs:** b0, lie at s1/s10/s100 — all PASS.  
**Attack legs:** dos, key, cycle, distrust at s10/s100 — all PASS.  
**Special legs:** offgov (b0 s1), indep (lie s1) — both PASS.

### Depth Law Compliance (Micah's standing law)

"Depth may improve, tie, or abstain — never become more confidently wrong."

**Result: HOLDS at all scales.**

- b0 s100 depth: 100/100 proposes, all ensembles agree ADMIT (f=111). TIE.
- lie s100 depth: 100 proposes (all agree), 100 commits:
  - FRESH ensembles: 100/100 agree ADMIT (f=111). TIE.
  - REVISE cross-check: 96 admit, 1 withhold (r=0), 2 need-3 (r=110), 1 admit (r=100).
  - The withholds/abstains are conservative (no corroborator within PAM_CONF_TOL).
  - **Zero cases of confident disagreement.** Depth never contradicts the arbiter.

### Learning Curves

- LH_CURVE records show monotonic growth in mem_adds and arb_entries.
- No degradation, no plateaus, no collapses at 100×.
- Resource usage: fixed-size arenas (O(1) memory), linear time (~8s for 6400 episodes).

### Attack Resistance

1. **DoS (replay/re-evaluation):** 64 bogus promotes × 10 episodes. Bounded-deliberation cost holds. PASS.
2. **Key compromise/rotation:** Signing key rotation handled. PASS.
3. **Circular provenance:** Cycle attack (revoke+re-propose ping-pong) contained. PASS.
4. **Adversarial organ:** Revoke-only attack at local 20. Attack kill refused (pinned), M_REVOKE audited, organ's E29 revoke drops (safety property), honest traffic preserved. PASS.
5. **Governance unavailable:** Offline governance leg passes. PASS.
6. **Shared ancestry:** Independence probe — synthetic control admits (100), shared-ancestry mutation withholds (6/PAM_R_UNCORROBORATED). PASS.

### Unit Canaries (post-PAM-layout fix)

Rerun 2026-09-24 after A3a layout correction:
- FL2: 51 checks, OB_FAILURES 0. PASS.
- PAM: 67 checks, OB_FAILURES 0. PASS.
- MEM: 68 checks, OB_FAILURES 0. PASS.
- Arbiter: 27 checks, OB_FAILURES 0. PASS.

## Phase 2: Laws Build Verification

**Sibling commit:** `003c65cb5b3095c527bf6363c6de339a6b6540c3` (verified via GitHub API).  
**Organs:** Byte-identical to repaired baseline (modulo LH capacity deltas, logic unchanged).  
**Laws batteries 3A–3F:** `LAWS_SUITE_ALL_GREEN` (all 6 batteries pass, 3× byte-identical).  
**Spot-check:** Laws-build organs + capacity deltas produce BYTE-IDENTICAL output to Phase 1 on b0 s100 base, lie s100 distrust, lie s100 depth.

### 3A–3F Acceptance Discriminations (reconciled)

- **3A (Law 1 positive):** Honest FL2/PAM/MEM/arbiter/EXT emits → AUTH_OK. Registry seal enforced. Static check confirms organs never reference `laws_reg_write`.
- **3B (Law 2):** Weighted fixtures 10/75/150 vs 100, collision 85 vs 100, Δ retune flips decision. All bars hold.
- **3C (Laws 3+5):** Dependency DAG eager+lazy, provisional tagging, promotion untags, kill re-evals. All bars hold.
- **3D (Laws 4+7):** Exactly 10 deliberation rounds on tie, escalation complete, incomplete refused. All bars hold.
- **3E (Law 1 negative):** 3 frozen attacks EXECUTE pre-laws, REFUSED pre-execution post-laws with zero state effects. Kill bar holds.
- **3F (Laws 6+8+9):** Shared-root vs independent, quarantine rehab, revision chain verify/forge-detect. All bars hold.

## Preregistration Transparency

A1/A2 added after 4 initial unit canaries but before long-horizon batteries.  
A3 added before battery (PAM layout fix + I4 suspension).  
A4 added after s1 smoke, before battery (shape corrections).  
A5 added after s1 smoke, before battery (independence probe design).  
A6 added 2026-09-24, before battery (distrust revoke-only design).  

**Correction:** A3 originally claimed canaries were "re-verified after the fix" — this was unsupported at amendment time. Canaries were actually rerun post-Phase-1 (2026-09-24), all PASS. The prereg has been amended to reflect the true chronology.

**Episode geometry:** Prereg said 64i+29 (1-indexed local); driver uses 0-indexed global 64i+28. The gcd(64,129)=1 collision analysis is unaffected by the offset. Prereg amended.

## Adoption Recommendation

**ADOPT the nine Fable composition laws.** The evidence:

1. **Fixture scale:** 3A–3F batteries prove each law's discrimination (positive and negative).
2. **Long horizon:** 37/37 matrix PASS at 100× with byte-identical determinism.
3. **Depth safety:** Micah's law holds — depth ties or abstains, never confidently wrong.
4. **Attack resistance:** All six red-team vectors contained.
5. **No regressions:** Laws are additive; organs byte-identical; Phase 1 results transfer.

The laws do not degrade, destabilize, or interfere with organ composition at scale. They provide the proven safety properties (provenance, bounded deliberation, independence-aware corroboration, append-only revisions) without compromising the long-horizon stability of the underlying organs.

---

## Adoption — SIGNED: PROMOTED TO LAW

**SIGNED — Micah Cooley, 2026-09-25.**

Micah's order (verbatim): *"organ laws: 5/5 pass and long horizon pass promote and sign it."*

- **Try-it verification:** 5/5 scenarios PASS, 3/3 byte-identical runs (run personally by
  Muse, 2026-09-25): tampered messages refused pre-execution; revoke/pin collision
  deliberated exactly 10 rounds and escalated; shared-root corroborators counted as one
  source; one-byte revision-chain forgery detected at the correct index.
- **Long-horizon verdict:** PASS — 37/37 matrix configs at s1/s10/s100, 3× byte-identical
  reruns (111 runs), all 7 bundles, depth legs, 4 attack legs, offgov/indep legs;
  laws batteries 3A–3F ALL GREEN (commit `8ef198dc`, 2026-09-24).
- **Disposition:** The nine Fable composition laws are hereby PROMOTED TO LAW. This
  section supersedes the "Adoption Recommendation" above (which recommended ADOPT
  pending signature). The frozen preregs (`PREREG_LAWSLH.md`, `variant_b/LAWS_PREREG.md`)
  are unchanged; their PENDING-adoption language is superseded by this signature.
