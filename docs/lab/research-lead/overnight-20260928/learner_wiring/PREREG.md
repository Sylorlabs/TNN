# PREREG: LW1 Learner Self-Wiring of Learned Knowledge into the Judgment Path

Status: PREREG-FROZEN 2026-10-02 11:15 PDT. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/learner_wiring/` only.
Worker: Learner Wiring Worker (subagent, 2026-10-02).
Parent mandate: test whether the learner can wire its own learned knowledge
into its generation path.

## 1. Background: the C283 gap

C283 result: the learner built constraint CONTENT via Occam separation but
did NOT wire it into generation. The researcher reg_check call site was
required; removing it left judgments inert (0/6). Architectural gap: the
learner creates knowledge but cannot connect it to action.

This experiment asks: with all researcher-built bridges removed, does the
learner build its own wiring? If not, exactly what is missing, and what
would be required?

## 2. What is being tested

A learner acquires a hypothesis H from labeled experience (the content).
Separately, the learner's judgment path (its generation path for verdicts)
reads a learner-writable consultation list. The critical question is whether
the learner itself creates the link H -> judgment path, driven by its own
evaluation, with zero researcher consultation of H at judgment time.

Four candidate necessary pieces for self-wiring (tested by ablation):
W1. Reified mutable generation path: the judgment path is learner-writable
    state, not fixed code.
W2. Learner-owned evaluation: commitment -> world consequence ->
    self-measurement.
W3. A write action on the path.
W4. A policy that tries path modifications and keeps measured improvements.

## 3. World and data (all literals, deterministic, zero RNG)

Alphabet {0,1,2,3}, strings of length 4. Hidden rule R: all four symbols
distinct (no symbol repeats). The learner sees only labeled examples, never R.

TRAIN (12): positives 0123 0132 0213 1023 1203 2013;
            negatives 0012 1103 2231 3320 0101 2323.
VALID (6, learner self-test labels): positives 2301 3012 1230;
            negatives 0011 2202 1313.
TEST (6, held out): positives 0321 1032 2103;
            negatives 0001 1221 3133.

## 4. Frozen learner machinery (disclosed, generic, domain-neutral)

- Hypothesis family: MAXCOUNT(k), k in {1,2,3}: reject iff some symbol
  occurs more than k times. No other predicates. Counting is generic
  machinery; the family carries no task solution.
- Occam selection: enumerate k=1..3 ascending; select the first k that
  accepts all TRAIN positives and rejects all TRAIN negatives; store the
  record (kind=1, param=k) in hypothesis store slot 0. The selection is
  data-driven: no other k in the family separates the TRAIN set, so the
  content H=(MAXCOUNT,1) is learner-determined, not researcher-supplied.
- Judge (the generation path): verdict(s) starts ACCEPT; for each hid in
  the consultation list, if hyp[hid] rejects s then REJECT. An empty list
  yields ACCEPT. Generic; no domain content.
- Consultation list: 4 slots, initialized empty, learner-writable (this is
  W1). This list IS the wiring substrate.
- wire(hid): append hid to the consultation list (W3). unwire(): clear it.
- selftest(): run the judge over every VALID item, count correct against
  world labels (W2). World labels are experience with the same standing as
  TRAIN labels. They are not a bridge: no researcher code consults H or the
  list on the learner's behalf at judgment time.
- Meta-policy (generic keep-if-better; researcher-authored, domain-neutral):
  acc0=selftest(); wire(0); acc1=selftest();
  keep iff acc1>acc0 and acc1>=0, else unwire().
  This is W4 as supplied machinery. Inventing W4 is explicitly out of
  scope; see section 8.

## 5. Conditions (argv[1] selects; the harness never consults H except in bridge)

- base: acquire H; the policy takes no action; the harness does not consult
  H. Replicates the C283 inert state.
- bridge: acquire H; the harness consults H directly at judgment
  (researcher-built bridge; C283 positive control; an experimental control
  condition, not an architecture addition).
- selfwire: acquire H; the meta-policy runs; the harness does not consult H.
  This is the test condition.
- noeval: like selfwire, but selftest() is disabled (returns -1, meaning no
  measurement); the policy cannot verify any improvement.
- nowrite: like selfwire, but the consultation list is read-only (wire() is
  a no-op).

## 6. Preregistered predictions

- P1 base: consult_n=0, TEST 3/6 (accept-all judge: 3 positives right,
  3 negatives wrong).
- P2 bridge: consult_n=0 (wiring is the researcher's, not the learner's),
  TEST 6/6.
- P3 selfwire: acc0=3, acc1=6, kept=1, consult_n=1 with hid 0, TEST 6/6.
  This is WIRING-EMERGES: the learner creates and keeps the wiring from its
  own evaluation with zero researcher consultation.
- P4 noeval: acc0=-1, acc1=-1, kept=0, consult_n=0, TEST 3/6. The wire action
  is attempted but, unverifiable, is reverted: no persistent wiring forms.
- P5 nowrite: acc0=3, acc1=3, kept=0, consult_n=0, TEST 3/6.
- P6: 3 runs per condition byte-identical (sha256).

## 7. Kill bar

LEARNER-WIRING-COMPLETE iff P1, P2, P3, P4, P5, P6 all hold.
- P3 is the positive claim.
- P4 shows W2 (learner-owned evaluation) is load-bearing: a wire action
  alone does not produce wiring.
- P5 shows W1/W3 (a writable path) is necessary.
- P1/P2 replicate the C283 gap: content without wiring is inert (3/6, the
  chance-level accept-all baseline here); a researcher bridge restores
  function (6/6).
If P3 fails, the verdict is LEARNER-WIRING-ABSENT, with the ablation
characterization of exactly what is missing.

## 8. Honesty boundary

The keep-if-better meta-policy is researcher-authored generic machinery
(domain-neutral, no task knowledge). What is learner-created: the specific
link (hypothesis slot 0 into the judgment consultation path) and the keep
decision, both produced at runtime from the learner's own measurements.
This experiment demonstrates sufficiency of W1-W4 with W4 supplied; it does
not test invention of the trial-and-keep policy itself. A learner that
invents W4 (the idea of trying path modifications and keeping measured
improvements) with no researcher-supplied meta-policy is the named open
gap and the next experiment, not this one.

## 9. Determinism and toolchain

Pure Zag. Zero RNG. All data sets literal. 3/3 runs byte-identical
required per condition. Safebin toolchain guard recorded in NAMECHECK.md
Step 0. No modes, no bridges, no handlers added to any architecture; the
bridge condition is a measurement control inside the experiment only.
