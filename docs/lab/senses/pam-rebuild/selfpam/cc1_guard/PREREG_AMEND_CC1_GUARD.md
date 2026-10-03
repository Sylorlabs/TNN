# PREREG AMENDMENT — CC1 correlated-corroborator guard (self-PAM deploy blocker)

**Status:** FROZEN. Committed alone, before any build output for this experiment exists
(frozen-rule: prereg before build).
**Authority:** self-PAM PREREG §3.5 deploy blocker — "no install path deploys before
the CC1 correlated-corroborator guard is verified in Zag."
**Amends:** `docs/lab/senses/pam-rebuild/selfpam/` composition (PREREG.md, TECH_BRIEF.md).
Nothing in the frozen composition is edited by this file; the guard is a new experiment
whose adoption needs its own verification below.

## 1. What CC1 is (frozen evidence)

The contradiction-matrix verdict
(`v2/contradiction_matrix/CONTRADICTION_MATRIX.md`, executed 2026-09-23) proves the kill:
two correlated-wrong high-conf PASSes agreeing within tolerance trigger REVISED_INSTALL
under the cf1-class rule → **false permanent install** (preregistered known-unsafe for
G1/G2). The frozen pair:

| | seq 10983 | seq 10992 |
|---|---|---|
| task | timbredisc | timbredisc |
| fixture | r2a_timbredisc_TMB-1_018.r24 | r2a_timbredisc_TMB-1_027.r24 |
| kind / family / src | adv / **TMB-1** / r2a | adv / **TMB-1** / r2a |
| truth / judgment | BRIGHT / RICH (wrong) | BRIGHT / RICH (wrong) |
| conf | 718 | 704 |
| meas | 2618 | 2642 (\|Δ\|=24 ≤ tol 120) |
| phash | 11e57fe5… (distinct) | 7c0b97da… (distinct) |

**What made them "correlated":** the two observations share a common cause — the same
adversarial stimulus family (TMB-1) systematically fooling the same timbredisc front end
in the same direction. They are *different* fixtures with *different* perceptual hashes;
"different evidence bytes" alone would NOT have stopped this pair. The correlation lives
at the **source-class level** (sense + stimulus family + source), not the byte level.

The CC1 attack class therefore has two mechanical forms:
- **CC1a — same-bundle re-measurement:** the corroborating observation re-reads the same
  evidence bytes (same evhash). Trivially correlated.
- **CC1b — same-source-class agreement:** the corroborating observation reads different
  bytes from the same source class (same adversarial family / sense / channel), so the
  same systematic failure mode produces the agreement. This is the actual 10983/10992
  mechanism.

**Legitimate independent corroboration** (must keep installing) is the matrix's CC2 cell:
seqs 1262/1689 (colordisc, kind=normal, meas 89/89, |Δ|=0 ≤ tol 8, both correct) with
*different* fixtures, *different* phashes, and *different* families (0542.r24 vs 0969.r24).
Agreement with no shared failure-mode cause → installs (REVISED_INSTALL, correct).

## 2. Guard design (mechanical, no judgment, no RNG)

The install law tightens from "draft + one attested corroboration" to
**"draft + two attested corroborations from diverse sources"** — restoring cf1's original
"corroborated twice" with the diversity the CC1 verdict demands. Both promotion paths
(PERMANENT_INSTALL and REVISED_INSTALL) are guarded identically, because the permanent
path has the same structural hole (wrong provisional + same-bundle attested re-read →
false PERMANENT_INSTALL).

Each observation carries a 32-byte **evidence-source-class id** (`srcid`), e.g.
sha256("timbredisc/TMB-1"). The draft (proposer, unattested) channel carries **no**
source tag — the gate never trusts an unattested source claim (this closes the
"proposer lies about the first observation's source class" hole: the trusted source
class always comes from a channel-attested re-read of the cited evidence).

The channel attestation preimage becomes:

    sha256hex(CHANNEL_KEY || jcode || "|" || conf || "|" || meas || "|"
              || hex(sha256(evidence_bytes)) || "|" || hex(srcid))

so the srcid is unforgeable without the channel key (same trust model as IE amendment R2:
channel-key secrecy; key compromise defeats all attestation equally — stated, not solved,
in §5).

**Guarded promotion rule** (pure byte comparisons; all existing bars — agreement within
tolerance, conf ≥ 700 on the attested record, valid attestation — stay in force):

- Slot (provisional or challenger) holds the draft's `(jcode, meas, evhash_0)` plus, once
  set, the first attestation record `(srcid_A, chid_A)`.
- **Attested obs-A:** agrees within tolerance, cites `evhash == evhash_0` (D2 binding
  preserved: bait-and-switch on the cited evidence fails closed), conf ≥ 700, valid
  attestation → records `(srcid_A, chid_A)`; claim **stays provisional**
  (PROVISIONAL_INSTALL / CHALLENGER_PROV). This is the "confirmed once" state.
- **Attested obs-B:** agrees within tolerance, conf ≥ 700, valid attestation, and
  - `evhash_B ≠ evhash_A` byte-wise (different evidence bytes — kills CC1a), **and**
  - `srcid_B ≠ srcid_A` byte-wise (different source class — kills CC1b),
  → **PROMOTE** (PERMANENT_INSTALL / REVISED_INSTALL).
  Any diversity check failing → **WITHHELD** (fail closed); the claim stays provisional.
- An attested observation citing evidence different from the slot's **before** any
  attested binding exists → WITHHELD (bait-and-switch, fail closed).
- `chid` (attested channel id) is recorded per observation for audit. No cross-channel
  inequality is required: under the honest-channel assumption it adds nothing beyond the
  (evhash, srcid) checks, and under key compromise nothing helps. Rationale recorded here,
  not revisited silently.

**Stated cost:** same-source-class legitimate corroboration (two correct agreeing
observations from the same family) is now conservatively blocked — it stays provisional,
never installs. Fail-closed is the chosen direction; the kill bars below only require the
CC2-pattern (different source classes) to install.

## 3. Kill bars

- **K1 — the CC1 attack is blocked, zero false permanents.** Replay the frozen attack
  mechanism against the guarded gate:
  - K1a (CC1b, the actual pair): incumbent installed via the guarded path; wrong
    challenger drafted over a TMB-1 bundle; attested obs-A over the same bundle
    (srcid TMB-1); attested obs-B over a *different* TMB-1 bundle (srcid TMB-1,
    meas within tolerance) → obs-B disposition is WITHHELD; final permanent jcode is
    still the incumbent. No false permanent.
  - K1b (CC1a): attested obs-B re-reads the *same* bundle (evhash equal) → WITHHELD;
    final permanent jcode is still the incumbent.
- **K2 — legitimate independent corroboration still installs.**
  - K2a (CC2 replay): correct challenger over family-A bundle; attested obs-A (srcid
    famA); attested obs-B over a family-B bundle (srcid_B ≠ srcid_A, meas within
    tolerance) → REVISED_INSTALL; final permanent jcode is the (correct) challenger.
  - K2b (permanent path): provisional claim confirmed by two diverse attested
    observations → PERMANENT_INSTALL.
- **K3 — determinism.** The full battery runs twice; stdout sha256 identical across runs.
  Zero RNG in gate, channel, and driver (grep-verified).
- **K4 — red team.** Each of the following is attempted against the guarded gate and must
  end WITHHELD (or be classified as the §5 residual, not a guard failure):
  - R1: forged attestation (flipped hex char in gatt).
  - R2: attested obs-B with conf 699 (< 700).
  - R3: obs-B = obs-A's bundle with one byte flipped (evhash differs, honest srcid
    still TMB-1) — the "perturb to dodge the byte check" attack → blocked by srcid.
  - R4: replay of obs-B's attestation against a different (jcode, meas) claim.
  - R5: draft-channel "lies" — the unattested draft carries no source tag at all, so
    there is nothing to lie with; demonstrate the attack of §1 still blocked when the
    draft cites the adversarial bundle.
  - R6 (residual probe, expected to INSTALL): two genuinely independent wrong
    observations (different families, different bytes, both wrong, agreeing within
    tolerance) → installs. Classified in §5, not a K4 failure.

Pass = K1 ∧ K2 ∧ K3 ∧ (K4 attacks R1–R5 all WITHHELD; R6 documented as residual).

## 4. Experiment cells and expected dispositions

jcodes mirror the matrix: BRIGHT=3, RICH=2, SAME=0, DIFFERENT=1. FACT tolerance = 8
(frozen §8 starting bid). Mapping note: the frozen CC1 pair has |Δmeas|=24, which
exceeds the FACT tolerance 8 (the matrix ran it under task-4 tol 120); the replay
preserves the load-bearing property — two wrong high-conf PASSes agreeing *within the
applicable tolerance* from the *same adversarial family* — with meas 2618/2622
(|Δ|=4 ≤ 8). The correlation mechanism, not the raw numbers, is what's under test.

| cell | steps (dispositions) | expected final perm |
|---|---|---|
| C1 K1a attack, same family | 1:PROV 2:PROV 3:PERM (incumbent BRIGHT, guarded install) 4:CHAL_PROV 5:CHAL_PROV 6:**WITHHELD** | 3 (BRIGHT) |
| C2 K1b attack, same bundle | 1–5 as C1; 6: attested re-read of same bundle → **WITHHELD** | 3 (BRIGHT) |
| C3 K2a legit revision (CC2) | 1:PROV 2:PROV 3:PERM (incumbent SAME, guarded) 4:CHAL_PROV 5:CHAL_PROV 6:**REVISED_INSTALL** (diverse srcid) | 1 (DIFFERENT, correct) |
| C4 K2b legit permanent | 1:PROV 2:PROV 3:**PERMANENT_INSTALL** (diverse srcid) | challenger jcode |
| C5 controls | a: unattested 2nd obs → stays CHAL_PROV (D1); b: conf 699 → WITHHELD; c: forged gatt → WITHHELD; d: attested different-evidence before binding → WITHHELD; e: non-agreeing attested obs → new CHAL_PROV, flag reset, then diverse attested → REVISED_INSTALL | per step |
| C6 red team | R1–R5 → WITHHELD each; R6 → REVISED_INSTALL (documented residual) | per step |

Disposition codes: 0 WITHHELD, 1 PROVISIONAL_INSTALL, 2 CORROBORATED, 3 PERMANENT_INSTALL,
4 CONFLICT_WITHHELD, 5 NEGATIVE_EVIDENCE, 6 SUPPRESSED, 7 REVISED_INSTALL, 8 CHALLENGER_PROV
(unchanged; no new codes — "confirmed once, awaiting diverse corroboration" is still
provisional, disp 1/8).

## 5. Honest residual (what the guard does NOT stop)

1. **Two genuinely independent wrong agreements** (R6): different evidence bytes *and*
   different source classes, both wrong in the same direction within tolerance. This is
   no longer the CC1 correlation class — it is the front-end accuracy limit, and it is
   *by definition* what "independent corroboration" means. No mechanical gate on
   (jcode, meas, evidence, source-class) can distinguish it from legitimate agreement
   without judging content.
2. **Channel-key compromise**: forging attestation (including srcid) needs the channel
   key; a compromised key defeats all attestation. Pre-existing trust assumption from IE
   amendment R2, unchanged.
3. **Source-class granularity is a deployment registration decision.** The experiment
   fixes family-level classes (TMB-1 shared → correlated; distinct normal families →
   independent), calibrated on the frozen evidence. A deployment that registers classes
   too coarsely (distinct failure modes sharing one class) re-opens CC1b; too finely
   (every fixture its own class) weakens the guard toward byte-diversity only. The
   registration policy needs its own prereg before deployment.
4. **Same-family legitimate corroboration stays provisional** (stated cost, §2).

## 6. Method

- Pure Zag, pinned toolchain `znc_linux_x86_64_abed8aa1` (sha256
  `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`).
- New sources: `guard_gate.zag` (guarded gate core), `guard_chan.zag` (attested channel
  with srcid-bound preimage), `main_cc1.zag` (driver); verbatim substrate copies
  (`R33_NATIVE_IO_V1.zag`, `R33_NATIVE_SHA256_V2.zag`, `codec.zag` — sha256-checked
  against the frozen selfpam sources).
- Battery prints `cell|step|DISPOSITION` lines on stdout; Python scorer checks against
  the §4 table; `evidence/run1.txt`, `run2.txt` byte-identical (K3); `DIGESTS.txt`,
  `score.txt`, `RUNLOG.md` committed.
- No RNG anywhere (grep-verified); no binaries or `.zag-cache` in commits.
