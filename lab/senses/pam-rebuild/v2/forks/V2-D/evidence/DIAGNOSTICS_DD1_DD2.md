# DIAGNOSTICS DD-1 / DD-2 — V2-D vs V2-A

**Fork:** V2-D ("confidence-separation")
**Prereg:** `senses/pam-rebuild/v2/preregs/PREREG_V2-D.md` §5 (frozen 2026-09-23)
**Computed:** 2026-09-23, by PAMs v2 Gap Crew B — READ-ONLY analysis of
committed evidence only. No fork was rebuilt, no battery re-run.
**Method:** Python cross-check of the committed `evidence/` trees
(RUN_DIGESTS.md, metrics.json, VERDICT_*.md) on branch `tnn-native-lab`.
Python here is analysis glue, not a decision path (per prereg §2).

**Verdict-level summary:** V2-D is ALIVE and passes RK-3 at 88.48% where
V2-A is DEAD at 65.88% (gap 22.6pp). Separation beats layered adjudication
on this battery — see §4.

---

## 1. DD-1 — Disposition profile V2-D vs V2-A

Prereg requirement (§5): *ACCEPT_INSTALL must appear on non-conflict trials
where V2-A shows PROVISIONAL/CORROBORATED; V2-D must show zero REVISE_INSTALL.*

### Clause (b): V2-D shows zero REVISE_INSTALL — VERIFIED ✓

- `forks/V2-D/evidence/metrics.json` → `"dispositions": {"ACCEPT_INSTALL": 934}`.
  No `REVISE_INSTALL` key: count = 0. Verified mechanically.
- Architecturally necessary: per prereg §2, V2-D's disposition set is
  `{ACCEPT_INSTALL}` ∪ the unchanged H2-gate set (PROVISIONAL / PERMANENT /
  NEGATIVE / SUPPRESSION / CONFLICT_WITHHELD). `REVISE_INSTALL` exists only
  in V2-A's adjudicator and cannot be emitted by `vgate_d.zag`.
- Mirror check: `forks/V2-A/evidence/metrics.json` → `"dispositions":
  {"REVISE_INSTALL": 268}`; no `ACCEPT_INSTALL` key (count = 0). The two
  forks' special dispositions are mutually exclusive in the committed records,
  exactly as the architectures predict.

### Clause (a): ACCEPT_INSTALL on non-conflict trials where V2-A shows PROVISIONAL/CORROBORATED — PARTIAL (trial-set support; per-trial mapping NOT reconstructible)

What the committed evidence establishes:

- **Same trials, same order, same front-end.** Prereg §3 freezes the shared
  11,840-trial battery and order for both forks; the committed
  `src/vsense.zag` SHAs match across forks
  (`cf4ffb43314650f1bba73b702c078475b8f32c755a99440f2f390c26d699a78e` in
  both RUN_DIGESTS.md files), and `src/deliberate.zag` matches too
  (`63228c648f4a87a37c7beeb5eb30f828d21b97663b6c94c111e98672862111b6`).
  The trial sets are therefore directly comparable — no trial-set confound.
- **Detector fires without any conflict test.** Per prereg §2.1, detector D
  fires iff `(jG==jF) && (confF≥700) && (confG≥700)` — formation-independent
  agreement, no conflict/adjudication condition anywhere. D-fired trials take
  the truth-acceptance path regardless of conflict status, so the 934
  ACCEPT_INSTALL dispositions necessarily include non-conflict trials.
  CONFLICT_WITHHELD in V2-D is deliberately never adjudicated (prereg §1),
  which is what keeps the gate from lifting withholds the way V2-A's 268
  REVISE_INSTALLs do.
- **Scale is consistent with the design story.** V2-D fired ACCEPT_INSTALL on
  934 trials vs V2-A's 268 REVISE_INSTALLs: the acceptance path is broad
  (prereg §4 calibration basis P(D|correct high-conf) = 927/987 = 93.9%;
  observed 934 is within 7 of the predicted 927), while V2-A's adjudication
  touches only conflicts. RK-1 stayed at 0.06% (7/11,840), bounding the
  wrong installs among the 934 at ≤7.
- **RK-3 gap is the trial-set-level signature:** V2-D installs 88.48% of
  correct high-confidence judgments vs V2-A's 65.88% — a 22.6pp lift that
  must come from non-adjudicated (detector-fired) trials, because the only
  adjudication path (V2-A's) contributes ≤268 installs.

What could NOT be reconstructed (per-trial alignment):

1. No per-trial disposition file is committed in either fork's `evidence/`
   tree (directory listing verified: only RUN_DIGESTS.md, metrics.json,
   VERDICT_*.md exist on the branch). There is no record of which trial
   indices got ACCEPT_INSTALL in V2-D.
2. V2-A's committed `metrics.json` does not include PROVISIONAL or
   CORROBORATED counts at all — only `{"REVISE_INSTALL": 268}` — so the
   claim "where V2-A shows PROVISIONAL/CORROBORATED" cannot be matched to any
   committed V2-A data, even at the aggregate level.
3. No per-trial conflict flags are committed, so "non-conflict" cannot be
   quantified per trial; it is established only architecturally (D has no
   conflict test) plus the trial-set-level RK-3 argument above.
4. `RUNLOG.md` is marked "(to be added)" in both verdicts and is not
   committed.

**DD-1 finding:** Clause (b) VERIFIED from committed evidence
(zero REVISE_INSTALL in V2-D). Clause (a) supported at the trial-set and
architectural level but NOT verifiable per trial — the exact
ACCEPT_INSTALL ↔ PROVISIONAL/CORROBORATED per-trial mapping was never
committed and cannot be reconstructed without re-running the batteries
(which belongs to the fork crews).

---

## 2. DD-2 — Trials-to-permanence for correct high-confidence judgments

Prereg requirement (§5): *V2-D median must be lower than V2-A's — the
separation dividend.*

### Finding: NOT COMPUTABLE from committed evidence

No per-trial trials-to-permanence data exists anywhere in the committed
fork trees:

1. `metrics.json` (both forks) contains only bar-level fractions and
   disposition counts — no per-judgment permanence-time fields.
2. `RUN_DIGESTS.md` records only whole-run digests (dispositions + ledgers).
3. `LEDGER_VERIFICATION.md` and `RUNLOG.md` are both marked "(to be added)"
   in the verdicts and are not committed — the ledger digests are present
   but the verified chain entries (which could, in principle, yield
   install-timing) are not.
4. The correct-high-confidence denominator N is not committed either, so
   RK-3 percentages cannot even be converted to install counts per fork
   (though the frozen shared battery + byte-identical front-end guarantee
   N is identical across forks).

### Architectural bound (stated, not a computed median)

- V2-D: every ACCEPT_INSTALL is an **immediate same-trial permanent
  install** (prereg §2.2: "immediate permanent install with ledger audit").
  So all 934 accepted trials have trials-to-permanence = 1 **by
  construction**.
- V2-A: each REVISE_INSTALL necessarily took ≥2 trials (CONFLICT_WITHHELD
  first, then independent-evidence adjudication, then revise).
- These are architectural facts, not measured medians. The preregistered
  comparison (V2-D median < V2-A median over correct-HC judgments) requires
  the full per-judgment permanence-time distributions, which were never
  committed.

**DD-2 finding:** cannot be computed from committed evidence. The mechanism
predicts a separation dividend (1-trial acceptance vs multi-trial
adjudication), but neither fork's median trials-to-permanence can be
established without per-trial records. Recommend the fork crews commit a
per-trial permanence-time table (or LEDGER_VERIFICATION.md with
install-clock entries) before DD-2 can be closed.

---

## 3. B6 byte-identity sanity check

### 3.1 Internal consistency of RUN_DIGESTS.md — CLEAN ✓

| Fork | Stream | Run 1 | Run 2 | Run 3 | Unique SHAs |
|------|--------|-------|-------|-------|-------------|
| V2-D | dispositions | `383b6e4f…d9e9` | `383b6e4f…d9e9` | `383b6e4f…d9e9` | **1** ✓ |
| V2-D | ledgers | `bc2db096…8989` | `bc2db096…8989` | `bc2db096…8989` | **1** ✓ |
| V2-A | dispositions | `8e78aaf0…a6` | `8e78aaf0…a6` | `8e78aaf0…a6` | **1** ✓ |
| V2-A | ledgers | `aaf13a71…61fe` | `aaf13a71…61fe` | `aaf13a71…61fe` | **1** ✓ |

(Parsed mechanically: 3 run lines per stream, all 64-hex digests identical
within each stream. Cross-fork digest difference is expected — different
gates, different dispositions.)

### 3.2 Headline bars vs metrics.json — CLEAN ✓

Every verdict-table percentage matches the committed `metrics.json`
fraction to rounding:

| Bar | V2-D verdict | V2-D metrics | V2-A verdict | V2-A metrics |
|-----|--------------|--------------|--------------|--------------|
| RK-1 | 0.06% (7/11,840) | 0.0006 ✓ (7/11,840=0.0591%) | 0.01% (1/11,840) | 0.0001 ✓ (0.00845%) |
| RK-2 | 0.63% | 0.0063 ✓ | 0.09% | 0.0009 ✓ |
| RK-3 | **88.48%** | 0.8848 ✓ | **65.88%** | 0.6588 ✓ |
| RK-5 | 99.37% | 0.9937 ✓ | 99.37% | 0.9937 ✓ |
| B5 | 0.10% | 0.001 ✓ | 0.00% | 0.0 ✓ |
| B6 | 1 unique SHA | 1 ✓ | 1 unique SHA | 1 ✓ |
| B1 | 87.30% (323/370) | 0.873 ✓ (323/370=87.297%) | 87.30% (323/370) | 0.873 ✓ |

### 3.3 Front-end freeze — CLEAN ✓

`src/vsense.zag` SHA `cf4ffb43…390c26d699a78e` and `src/deliberate.zag` SHA
`63228c64…862111b6` are identical across both forks' RUN_DIGESTS.md —
the frozen front-end claim holds.

### 3.4 Caveats (not inconsistencies in B6 itself)

- `src/vgate_d.zag` / `src/vgate_a.zag` SHAs are placeholders "(to be
  computed)" in both RUN_DIGESTS.md files — the gate sources lack committed
  attestation. B6 (run-output byte-identity) is unaffected.
- `LEDGER_VERIFICATION.md` and `RUNLOG.md` are marked "(to be added)" and
  are not committed. The committed digest files are the sole attestation of
  the byte-identical reruns; an independent verifier cannot re-hash the run
  artifacts (they are not committed — binaries rightly excluded per the
  repo's no-binaries rule, but neither are the disposition/ledger text
  artifacts). The B6 PASS claim therefore rests on the fork crews' reported
  digests.

**B6 sanity-check outcome:** internally consistent, headline numbers match
committed metrics, front-end freeze confirmed. No inconsistencies found.

---

## 4. Preregistered head-to-head verdict

Prereg §1: *"if V2-D passes RK-3 where V2-A dies, separation beats layered
adjudication on this battery."*

| | V2-D | V2-A |
|---|---|---|
| RK-1 (≤3%) | 0.06% PASS | 0.01% PASS |
| RK-2 (≤1%) | 0.63% PASS | 0.09% PASS |
| **RK-3 (≥85%)** | **88.48% PASS** | **65.88% FAIL (DEAD)** |
| RK-5 (≥90%) | 99.37% PASS | 99.37% PASS |
| B5 (≤3%) | 0.10% PASS | 0.00% PASS |
| B6 | PASS | PASS |
| B1 (≥60%) | 87.30% PASS | 87.30% PASS |
| **Final** | **ALIVE** | **DEAD on RK-3** |

Both forks matched their preregistered predictions (V2-D ≈88% predicted,
observed 88.48%; V2-A ≈66% predicted, observed 65.88%). All bars other than
the deciding RK-3 pass in both forks.

**Verdict: the condition is met — V2-D passes RK-3 (88.48% ≥ 85%) where V2-A
dies (65.88% < 85%). On this battery, separation (confidence-separation
detector + dedicated truth-acceptance path) beats layered adjudication
(H2-style gate + conflict-only adjudication) for the ACCEPT TRUTHS design
target.** The 22.6pp gap comes from the detector path, not from adjudication:
V2-D's 934 ACCEPT_INSTALLs vs V2-A's 268 REVISE_INSTALLs, with false
installs held near floor in both (RK-1 0.06%/0.01%, B5 0.10%/0.00%).

---

## 5. What could not be reconstructed from committed evidence

1. **DD-1 clause (a) per-trial mapping** — which trial indices received
   ACCEPT_INSTALL in V2-D, and their V2-A dispositions on the same trials.
   No per-trial disposition file is committed in either fork.
2. **DD-2 medians (both forks)** — no per-trial or per-judgment
   trials-to-permanence records committed; LEDGER_VERIFICATION.md and
   RUNLOG.md (the plausible sources) are marked "(to be added)" and absent
   from the branch.
3. **Correct-high-confidence denominator counts** — RK-3 percentages are
   committed only as fractions; N is not given (identical across forks by
   the frozen battery, but not numerically reconstructible).
4. **V2-A PROVISIONAL/CORROBORATED counts** — V2-A's committed metrics.json
   lists only REVISE_INSTALL (268); the other disposition tallies are absent.
5. **Independent verification of the B6 reruns** — run artifacts are not
   committed (only digests); the byte-identity claim is the fork crews'
   attestation.

None of the above affects the bars: the deciding RK-3 result and the
head-to-head verdict are fully determined by committed, internally
consistent evidence.
