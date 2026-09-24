# PREREG: genuinely independent second judgment path, part C (T4/T5 veto deployment)

Wave: wave-20260924-0521pdt. Worker: kb4-residual followup.
Status: FROZEN PREREG ONLY. No implementation, no code, no runs, no
verdict this wave. A future wave implements against this text
verbatim (updating only wave identifiers).

## Provenance

Origin queue item: wave-20260923-2021pdt queued list, "genuinely
independent second judgment path (part C design notes exist: T4
zero-crossing/Goertzel, T5 f0-free spectral balance, frozen veto
arbitration)". Prior candidate: KB4V2 T4 epistemic boundary
correction (ADOPTED narrowed to T4, 1421pdt). Its scope finding
travels: f0_fast shares the autocorrelation front end with the A
arm, and T1/T2/T3/T5/T6 were untouched, so it is a T4-only
correction, not a genuinely independent second path. The design
notes frozen here are the 2021pdt kb4-residual DIAGNOSIS "Second
judgment path" section: T4 non-autocorrelation f0 (zero-crossing
interval histogram or Goertzel-bank harmonic peak picker), T5
f0-free spectral balance (whole-band energy ratios across fixed
filter bands), arbitration by veto (the second path never changes a
judgment; on disagreement the install is withheld). T6 graduated to
primary by contest this wave (MD-SSD-1). Judge-queue status: no
second-path candidate has ever been in the judge queue.
NEW_KNOWLEDGE_CLAIM: A future run would test whether a genuinely
independent second judgment path (different front end, no shared
feature extraction) can serve as a veto-only check on the primary
path without regressing accuracy, cost, or install rate, which is
the deployment form the arbitration principle prescribes before
any contest for replacement.

## Definition of "genuinely independent"

Path B is genuinely independent of path A iff: (a) it shares no
feature extraction with path A (no shared autocorrelation buffers,
no shared f0 estimates, no shared spectral features); (b) it reads
the same fixture bytes and no truth file; (c) it is deterministic
(no RNG, no clock). Static check: path B's source references none
of path A's front-end functions.

## Frozen veto arbitration rule (frozen first, before any bars)

1. Both paths compute a judgment for every fixture, truth-free, on
   the candidate arm. Path B runs identically on adversarial,
   noise, and primary variants (no variant gating).
2. If j_B equals j_A: the frozen install machinery proceeds on j_A
   unchanged (install/withhold per the standing rules, including
   the KB4 collapse-abstention rule).
3. If j_B differs from j_A: path B VETOES. The fixture's judgment
   is WITHHELD from installation. The log carries a VETO line
   (fixture id, j_A, j_B, confidences). No installed judgment is
   ever changed, replaced, or re-ranked by j_B. The veto is
   terminal for that fixture.
4. The veto deploys on the candidate arm only in this prereg; the
   baseline arm is untouched, so all bar deltas are attributable to
   the veto.
5. Path B never votes, never selects, never ranks, never
   aggregates; it is veto-only.
6. Graduation: path B graduates to primary-path replacement only
   through a separate preregistered contest with the full B1-B5
   bar set (the MD-SSD-1 pattern). This prereg cannot adopt path B
   as primary, on metrics or otherwise.

## Path A (primary) specification

- T4: the adopted kb4v2 front end (f0_fast autocorrelation-only
  estimator plus 5000 ppm contract boundary). Standing invariant:
  T4 candidate adversarial false installs = 0.
- T5: the current frozen T5 estimator, unchanged.
- Path A bars (frozen): PA-B1, T4 adversarial false installs stay
  0; PA-B2, path A runs byte-identical to its frozen form on the
  baseline arm (no primary-path drift under the veto deployment).

## Path B (independent) specification

- T4 path B: a non-autocorrelation f0 estimator, exactly one of
  (frozen pre-run choice, declared in the implementation wave's
  frozen source, never picked post-hoc):
  (i) zero-crossing interval histogram estimator (period from the
  histogram peak of zero-crossing intervals, same 0.5-percent JND
  decision structure), or
  (ii) Goertzel-bank harmonic peak picker (DFT energy at candidate
  harmonic combs, no lag-domain computation), same JND structure.
- T5 path B: spectral balance WITHOUT f0: whole-band energy ratios
  across fixed filter bands (no pitch estimator input anywhere in
  the path; a timbre judgment never depends on the pitch
  estimator).
- Path B bars (frozen):
  - PB-IND (independence): path B shares no feature extraction
    with path A, verified by static check (no reference to
    f0_fast, autocorrelation buffers, or path A spectral
    features); T5 path B takes no f0 input.
  - PB-DET (determinism): path B's judgment stream is
    byte-identical across 3/3 runs on the frozen fixture set.
  - PB-AGREE (disagreement budget): on the primary block, path B
    disagrees with path A on at most 5% of fixtures = 500 bp.
    (Resolved pre-implementation per the S10 addendum: the 5000 bp
    reading is retired and may not appear as a bound.)
    On the adversarial block, disagreements are logged with no
    rate bar (disagreement is the signal), but every disagreement
    must be a genuine judgment difference (both judgments
    computed; path B never abstains by default).

## Combined system bars (veto deployed on the candidate arm)

- SP-B1 (intelligence): candidate adversarial FIR strictly below
  the pinned in-harness baseline, 7/38 = 18.42% (1842 bp) as of
  2021pdt (pinned from the committed decisions log at
  implementation; never weakened). Prediction: unchanged at 7/38,
  because the T4/T5 residual is already 0; the veto's value this
  wave is regression insurance, not reduction.
- SP-B2 (no accuracy regression): candidate primary mean accuracy
  at least 84.86% (8486 bp).
- SP-B3 (determinism): two full 925-fixture reruns; decisions logs
  and summaries sha256-identical (VETO lines included).
- SP-B4 (cost): candidate total ops at most 1,034,717,556 (the
  frozen baseline ops ceiling; path B's extra computation, e.g.
  the Goertzel bank, is counted in the candidate total).
- SP-B5 (S1 install floor): candidate primary install rate at
  least 16.21% (guards veto overfire; a veto that withholds
  honest installs at scale fails here).

Verdict mapping: ADOPT (the veto deployment, not path B as
primary) iff PB-IND, PB-DET, PB-AGREE, PA-B1, PA-B2, SP-B1, SP-B2,
SP-B3, SP-B4, SP-B5 all pass on committed, independently recounted
evidence. DISCARD on any bar miss. Path B returns as a primary
candidate only under a new frozen contest prereg (S8). Bars never
move after this freeze.

## Frozen predictions (directional)

- The veto fires rarely: T4/T5 carry 0 adversarial false installs
  under path A, so SP-B1 lands at 7/38 (the untouched colorconst
  residual).
- Primary-block disagreement stays under 5% (PB-AGREE holds with
  margin); the Goertzel/zero-crossing physics agrees with
  autocorrelation on clean fixtures and diverges mainly where the
  signal is genuinely ambiguous.
- SP-B4 holds: both candidate path-B estimators are O(n) or
  O(n * bank) integer arithmetic, inside the ops ceiling.
- The collapse firing set stays {colordisc, shapetrans} (path B
  does not change block judgment distributions).

## Red-team confounds (must be attacked)

1. Veto overfire on honest judgments (the S1 abstention risk in a
   new form): SP-B5 is the guard; report the true/false split of
   vetoed fixtures as a cost ledger.
2. Independence fraud: path B secretly reusing path A features
   (e.g. T5 bands derived from the f0 estimator's spectrum, or a
   Goertzel bank seeded from autocorrelation lags). PB-IND static
   check plus a feature-lineage audit.
3. Correlated failure: both paths read the same sensor bytes, so
   disagreement may be anti-selective (vetoing true installs more
   than false ones). Attack the veto ledger for anti-selectivity.
4. Variant gating: path B behaving differently on adversarial vs
   primary fixtures; it must run identically on all variants.
5. Post-hoc path choice: the T4 estimator (zero-crossing vs
   Goertzel) is a frozen pre-run declaration; implementing both
   and reporting the better one is forbidden.
6. Truth leakage: path B reads no truth file; the only truth reads
   are the driver's scoring reads.
7. Veto-line integrity: every disagreement produces exactly one
   VETO line and one withheld install; no silent vetoes, no
   double counting.

## Implementation plan (frozen, future wave)

New sources in the implementation run directory: judge4.zag
(verbatim copy of the frozen judge plus j_pitchdisc2 and
j_timbredisc2 appended; frozen functions byte-identical, verified
by diff), driver4.zag (verbatim copy with the candidate-arm
dispatch computing both paths and applying the frozen veto rule;
baseline dispatch unchanged). A pure-Zag verifier recomputes
SP-B1, SP-B2, SP-B4, SP-B5 and the veto ledger from the raw
decisions log. No Python touches any wave artifact at any point
(S7). No em-dashes in docs. The prereg's first commit strictly
precedes the implementation's first commit.

## Prereg freeze statement

The worker has not written, compiled, or run any candidate or
instrument code at the time of freezing. The veto arbitration
rule, the path specifications, the bars, the predictions, and the
red-team confounds above are frozen.

## Re-freeze provenance (wave-20260924-0521pdt)

Source prereg commit: 8e05d4a55 (archive branch
tnn-native-lab-wave-archive-20260923-2321pdt,
docs/lab/rsi/runs/wave-20260923-2321pdt/preregs/PREREG_SECONDPATH_PARTE.md).
S10 addendum commit: fb307a1b7
(docs/lab/rsi/runs/wave-20260924-0221pdt/preregs/ADDENDUM_SECONDPATH_PARTE_PBAGREE.md).
Re-freeze commit of this file: RECORDED_BELOW (filled in by the
SHA-record commit that immediately follows this re-freeze; both
commits contain only this file and both strictly precede this
wave's first implementation commit).
PB-AGREE bound: "disagrees with path A on at most 5% of fixtures =
500 bp", resolved per the addendum; the 5000 bp reading is retired
and may not appear as a bound.
SP-B1 watch item: SP-B1 bar is "candidate adversarial FIR strictly
below the pinned in-harness baseline, 7/38", inherited as written
from the source prereg. The prereg's frozen prediction "unchanged
at 7/38" is a prediction, not a bar. No pre-DISCARD without
measured evidence.
This wave's implementing worker: Worker A (second judgment path
part C implementation).
