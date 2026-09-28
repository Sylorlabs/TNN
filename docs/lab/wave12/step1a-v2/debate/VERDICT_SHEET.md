# VERDICT SHEET — RNGSCAN v3 vs. stated residual risk

**Date:** 2026-09-20
**Decision owner:** Micah (this sheet does not decide; it informs)
**Question:** The no-RNG auditor (RNGSCAN) has been killed twice by its own blind red teams. Build v3 per the draft amendment, or stop the auditor line and accept a stated residual risk?
**Debate:** 4 voices, 2 rounds. Positions: `debate/r1/`, rebuttals: `debate/r2/`. Record: `DEBATE_RECORD.md`.

---

## Plain-language summary

The tool that checks TNN's code for hidden randomness has failed its own honesty test twice. The fixes for a third version exist and are concrete — but the evidence from both failures says something uncomfortable: the checking method itself keeps missing what actually matters, while a different method (re-running the code and looking for any difference in behavior) is what caught the real smuggled randomness both times.

All four debaters converged in round 2 on the same core package: **harden the re-run check as a standalone deliverable, write down exactly what is and isn't certified in a dated statement you sign, and certify each frozen trial build individually** — rather than chasing a perfect general-purpose checker. The one genuine disagreement left: whether to *also* build the full third version of the checker, and whether your Arm C experiment stays parked until a checker passes.

---

## 1. Option A — Build RNGSCAN v3

**What it is:** Authorize the rebuild per `AMENDMENT_2026-09-20_RNGSCAN_V3.md` (commit `64cd373`, DRAFT). ~1280 lines of pure Zag, localized fixes: strict canonical init form (fail-closed), structural hash-iteration detection, narrowed carve-outs (const + `// PINNED` + attestation-hashed), register-taint for syscall numbers, explicit `_zag_clock_*` ban, replay hardening (N runs + heap pre-dirtying). Kill bars K1/K2/K3 unchanged. Then a third blind red-team round with K2 live.

**Honest pros:**
- The no-RNG law is the program's load-bearing law; a law with mechanical enforcement is stronger than one enforced by process and disclosure. A passed auditor permanently de-risks *every* downstream trial, not just Arm C.
- Both kills were the process working as designed — each death named a finite, patchable *class* of hiding spot (shape-based init check, token-based table detection, name-keyed carve-out), and v3 patches all three. A detector that kills its own versions on honest misses is converging, not failing.
- The fixes are concrete and localized, not a research project. The attack surface is at least *nameable*: Zag surface, znc lowering, syscall boundary, intrinsics.
- Without a passing auditor, every Arm C variation claim is permanently attackable as "maybe hidden RNG" — the exact confound the gate exists to eliminate. The cost of not building isn't delay, it's a permanent asterisk on the program's central result.

**Honest cons:**
- **The "bounded surface" claim is a hypothesis, not a finding.** Both v2 misses lived *inside* categories already on the checklist (the zeroed-page init idiom and hand-rolled `EntrySet` were Zag-surface problems; the `pin_table` carve-out was a carve-out-language problem). The novel tricks came from idioms inside old categories nobody had named. "Localized scope" confuses the patch's size with the space's size.
- **The static scans have never once carried the catching.** In the v2 round, the plants that mattered (computed syscall immediates, runtime-built urandom path, timer intrinsic) were caught *only* by replay divergence; both static scans missed the mechanisms entirely. v3 may be polishing the tool that doesn't do the work.
- **Each version dies to a NEW trick.** Two kills to two different tricks fits an inexhaustible idiom space as well as a closing checklist. Convergence needs a pass, not two named autopsies — and 6 of 20 v2 plants went unscored, so the "checklist" is claimed without knowing the last round's full miss count.
- **Time cost while the real science waits.** Weeks of build + freeze + blind round, and if K2 fires a third time, the program is back at this exact decision a month later with Arm C still parked.

## 2. Option B — Accept stated residual risk

**What it is:** Stop iterating the auditor. Write down explicitly what is and isn't certified (see §4). Unblock Arm C with compensating controls: hardened replay as primary certification, per-trial-build red-teaming, the published risk statement, your revocable sign-off.

**Honest pros:**
- **Follow the evidence.** Replay divergence caught the real plants; static scanning caught the easy ones. Certification weight should sit on the layer that demonstrably works.
- **A parked experiment produces zero evidence.** Arm C is the program's central state-variation question; every month it waits behind a gate that may never converge is a month of no data.
- **Disclosure over false finality.** A dated, signed, version-controlled risk statement — miss-rate history (2/2 versions killed) stated openly — is more honest than a certificate that passed *this* red team and gets mistaken for proof. The program's honesty norms require disclosure, not perfection.
- **Replay's known weakness is cheap.** The one replay hole on record (zeroed pages hiding uninit reads) is a harness problem fixed by the v3 amendment's replay-hardening section — adoptable in days without any scanner rebuild.

**Honest cons:**
- **The "maybe hidden RNG" attack on Arm C stays open permanently.** If the headline result later traces to an uncertified channel, it's wrong in a way the founding law forbids. That is the genuine price, and no statement makes it go away.
- **The no-RNG law loses mechanical enforcement.** Process + disclosure is weaker than a tool that runs on every build. Future trials inherit the same asterisk unless each is individually argued.
- **Replay is behavioral evidence, not mechanical proof.** Environment-dependent nondeterminism that stays deterministic under all lab replay conditions would slip past. The N-run matrix must name deployment-like conditions in the prereg, or the gate is theater.

## 3. Middle paths

**M1 — Narrowed-scope v3 (per-frozen-build certifier).** Certify only the exact frozen trial builds, not arbitrary Zag code. Round 2 sharpened this into a *prescriptive* certifier: ban novel idioms from trial builds (allowlisted containers, canonical init forms, no unlisted intrinsics) instead of detecting them in the wild. Converts open-ended detection into bounded verification. Cost: a few hundred lines, plus the honest price that trial-build authors must write to the narrower idiom. Proposed K2 replacement for per-build scope: K1′ (prereg-frozen allowlist + replay matrix), K2′ (blind red team scoped to the build; a miss the rules should have forbidden = dead; novel-class misses require a dated prereg amendment with your re-approval), K3′ (hardened replay passes on the exact frozen binary). Trade-off: doesn't solve the general problem — but nothing the program needs *right now* requires winning it.

**M2 — Replay-first (promote replay-divergence to the primary gate).** Make hardened multi-run replay the load-bearing certification; keep the v2 static scan running as a secondary tripwire (no K2 bar, no rebuild); add per-trial-build blind red-teaming as process. Strongest empirical case: any runtime nondeterminism that affects measured behavior *must* diverge across runs, or it can't confound the trial. Trade-off: not mechanical proof; a hidden RNG whose output never reaches measured behavior slips past (though it also can't confound the trial); environment-dependence must be covered by preregistered deployment-like conditions.

**Round-2 convergence (all four voices agreed on this package):**
1. Replay hardening (N runs, heap pre-dirtying, allocation-pattern variation, deployment-like conditions) ships **standalone**, not waiting for any scanner rebuild.
2. A **dated, version-controlled residual-risk statement** is required regardless of option — even a passed v3 gets wrapped in one (a pass is evidence, not proof).
3. Certification scopes to the **frozen trial build** (hash the artifact, preregister the matrix per build).
4. The v2 static scan keeps running as a cheap tripwire; it just no longer holds a kill bar it may never pass.

## 4. The residual-risk statement (what you would sign)

> **RESIDUAL-RISK STATEMENT — no-RNG certification for the Arm C trial build**
> **Date:** 2026-09-20. **Status:** DRAFT — unsigned. **Applies to:** the Arm C state-variation trial build only (frozen source hash and binary hash recorded at freeze; prereg `97882fc`).
>
> **What is certified:**
> 1. The frozen build passed the v2 static no-RNG scan as a tripwire (no K2 pass claimed).
> 2. Hardened replay: N=8 runs, byte-identical outputs, heap pre-dirtied before each run, allocation-pattern variation, deployment-like conditions per the preregistered matrix. Any runtime nondeterminism affecting measured behavior would have diverged.
> 3. Per-build blind red-team round: [result recorded at run time].
>
> **What is NOT certified:**
> 1. No general static proof of randomness-freedom. RNGSCAN v1 and v2 were both killed by their own blind red teams (2/2 miss-rate history; evidence: `docs/lab/wave12/step1a-v2/redteam/`, commit `d368014`). No third version has passed.
> 2. Environment-dependent nondeterminism that remains deterministic under all lab replay conditions but not in deployment.
> 3. Hidden channels whose output never reaches the trial's measured behavior. (Note: such channels cannot confound the trial's results by construction.)
>
> **Compensating controls:** frozen hashed build; preregistered replay matrix published alongside results; per-build red-teaming; this statement published next to the Arm C results; revocable by Micah at any time; **sunset clause** — this decision reopens automatically if the program later requires arbitrary-code certification.
>
> **Signature:** Micah ________  **Date:** ________

## 5. The load-bearing question: is the auditor the right SHAPE of tool?

The debate's honest answer is split by shape:

- **As a general-purpose static detector with a K2 kill bar: the shape looks wrong.** The empirical record is that the adversary invents shapes inside already-listed categories, the static scans never once fired K2 on their own merits, and replay did the real catching. Two deaths is not convergence. The general-detector shape fights an asymmetric battle (hider needs one unseen trick; scanner must enumerate all future tricks) that the record suggests it keeps losing.
- **As a per-build prescriptive checker (allowlisted idioms, canonical forms) paired with hardened replay: the shape is right.** It converts open-ended detection into bounded verification of a known artifact, and it leans on the layer that demonstrably catches. Defense-in-depth was the only thing that worked in the v2 round; the shape that keeps both layers, with replay load-bearing, matches the evidence.

## 6. Recommendation (recommendation only — the decision is Micah's)

**Adopt the converged middle path as the Arm C gate; run full v3 only as a non-gating parallel line.**

Concretely:
1. Ship replay hardening standalone (days): N=8 runs, heap pre-dirtying, allocation-pattern variation, preregistered deployment-like conditions.
2. Build the thin prescriptive per-build certifier (M1, a few hundred lines): allowlisted containers, canonical init forms, intrinsic ban with one-time audit, hash-verified frozen build — with the proposed K1′/K2′/K3′ bars.
3. Keep the v2 static scan as a tripwire (no K2 bar).
4. Publish the §4 residual-risk statement next to the Arm C results; you sign it; it carries the sunset clause.
5. Unblock Arm C on that gate via a dated prereg amendment (needs your re-approval, like any rule change).
6. If you want the general static tool for the program's long-term integrity story, authorize v3 **in parallel without gating Arm C on it** — preserving the upside (a passing general auditor would be genuinely valuable) without holding the science hostage a third time.

**Why:** the evidence says replay catches and static misses; the "bounded surface" claim doesn't survive the observation that both kills came from inside listed categories; and honest disclosure with a sunset clause satisfies the program's honesty norms better than either a parked experiment or a certificate that risks false finality. The one thing this package does not give you is mechanical proof — and neither does any option currently on the table.

## 7. What each option unblocks or keeps parked

| Option | Arm C trial | Timeline | Dependencies / notes |
|---|---|---|---|
| **A — build v3** | Parked until a version passes a blind round with K2 live | Weeks (build + freeze + blind round); if K2 fires again, back here in ~a month | Draft amendment `64cd373` needs your approval first; v1/v2 stay dead |
| **B — stated residual risk** | Unblocks immediately on the §4 statement + hardened replay | Days (harness work + statement) | Needs a dated prereg amendment changing the §3 gate (your re-approval); static line stops |
| **Middle (recommended)** | Unblocks on the replay + thin-certifier gate, via dated amendment | Days for replay hardening; ~a week for the thin certifier; Arm C proceeds on the replay gate first | v3 optionally continues in parallel, non-gating; statement carries sunset clause |

**Standing constraints respected by all options:** pure Zag for any build work; the no-RNG law itself is not under debate — only the certification tool. Kill bars K1/K2/K3 on the general auditor are unchanged unless you amend them.
