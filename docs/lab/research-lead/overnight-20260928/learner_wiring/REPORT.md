# REPORT: LW1 Learner Self-Wiring

Verdict: LEARNER-WIRING-COMPLETE (with wiring capability analysis, section 5).
Date: 2026-10-02. Worker: Learner Wiring Worker (subagent).
Prereg: PREREG.md, frozen and committed (421d57afe) before implementation.

## 1. Question

C283 showed the learner building constraint CONTENT (Occam separation) but
not wiring it into generation: without the researcher reg_check call site,
judgments were inert (0/6). LW1 asks: with all researcher-built bridges
removed, does the learner build its own wiring from learned knowledge into
its judgment (generation) path? If not, exactly what is missing?

## 2. Design (summary; full detail in PREREG.md)

World: strings of length 4 over {0,1,2,3}; hidden rule R = all symbols
distinct. The learner sees only labeled examples, never R. It acquires
hypothesis H=(MAXCOUNT,1) by Occam selection over k=1..3 on 12 TRAIN items.
Its judgment path (the generation path for verdicts) reads a
learner-writable consultation list, initialized empty. Five conditions,
argv-selected, zero RNG, all data literal:

- base: H acquired; policy takes no action; harness does not consult H.
- bridge: harness consults H directly (researcher bridge; C283 control).
- selfwire: generic keep-if-better meta-policy runs (self-test, wire,
  self-test, keep iff strictly better); harness does not consult H.
- noeval: like selfwire, self-test disabled (returns -1).
- nowrite: like selfwire, consultation list read-only.

## 3. Results: predictions vs observed (all 15 runs)

| cond     | predicted acc0/acc1/kept/consult_n/test | observed | match |
|----------|------------------------------------------|----------|-------|
| base     | -2/-2/0/0, 3/6                           | -2/-2/0/0, 3/6, consult0=-1 | P1 HOLD |
| bridge   | -2/-2/0/0 bridge=1, 6/6                  | -2/-2/0/0 bridge=1, 6/6 | P2 HOLD |
| selfwire | 3/6/1/1 consult0=0, 6/6                  | 3/6/1/1 consult0=0, 6/6 | P3 HOLD |
| noeval   | -1/-1/0/0, 3/6                           | -1/-1/0/0, 3/6, consult0=-1 | P4 HOLD |
| nowrite  | 3/3/0/0, 3/6                             | 3/3/0/0, 3/6, consult0=-1 | P5 HOLD |

P6: 3 runs per condition byte-identical (sha256; see sha256sums.txt). HOLD.

Raw outputs (run1 of each; runs 2 and 3 identical):

base:     hyp_found=1|hyp_param=1; acc0=-2|acc1=-2|kept=0|consult_n=0|consult0=-1|bridge=0; test 3/6
bridge:   hyp_found=1|hyp_param=1; acc0=-2|acc1=-2|kept=0|consult_n=0|consult0=-1|bridge=1; test 6/6
selfwire: hyp_found=1|hyp_param=1; acc0=3|acc1=6|kept=1|consult_n=1|consult0=0|bridge=0; test 6/6
noeval:   hyp_found=1|hyp_param=1; acc0=-1|acc1=-1|kept=0|consult_n=0|consult0=-1|bridge=0; test 3/6
nowrite:  hyp_found=1|hyp_param=1; acc0=3|acc1=3|kept=0|consult_n=0|consult0=-1|bridge=0; test 3/6

Kill bar (P1-P6 all hold): MET. Verdict: LEARNER-WIRING-COMPLETE.

## 4. What the numbers establish

a) Content/wiring dissociation is clean. In ALL five conditions
   hyp_found=1 and hyp_param=1: the learner acquired identical content
   every time. The only thing that varied was the wiring, and TEST
   accuracy tracked the wiring exactly (3/6 unwired, 6/6 wired). This is
   the C283 gap reproduced in miniature and then closed.

b) The learner created the wiring in selfwire. White-box state at end of
   run: consultation list = [0] (consult_n=1, consult0=0), i.e. hypothesis
   slot 0 linked into the judgment path. No researcher code wrote that
   link or consulted H at judgment time (bridge=0). The keep decision was
   produced at runtime from the learner's own measurements (acc0=3,
   acc1=6, kept=1).

c) Evaluation is load-bearing (P4). In noeval the learner DID attempt the
   wire action (the write path works), but with no measurement to verify
   improvement it reverted the link (consult_n=0, TEST 3/6). A wire action
   alone does not produce wiring; unverifiable attempts do not persist.

d) A writable path is necessary (P5). In nowrite the learner measured
   acc0=3, attempted wiring, measured acc1=3 (no change possible), and
   correctly declined to keep anything. No false wiring was installed.

e) The researcher bridge is sufficient but not necessary (P2 vs P3): both
   reach 6/6, one via researcher consultation, one via learner-built wiring.

## 5. Wiring capability analysis: what is required

Self-wiring required four pieces, each shown necessary or sufficient by
the ablations:

W1. Reified mutable generation path. The judgment path must be
    learner-writable state (the consultation list), not fixed code.
    nowrite shows: without W1, wiring is impossible (P5).
W2. Learner-owned evaluation. Commitment -> world consequence ->
    self-measurement (selftest over VALID labels, which are experience,
    not a bridge). noeval shows: without W2, wire attempts are reverted
    and no persistent wiring forms (P4). This is the C283 failure mode.
W3. A write action on the path (wire/unwire). Without it W1 is read-only.
W4. A policy that tries path modifications and keeps measured
    improvements. Supplied here as generic keep-if-better machinery.

Honesty boundary (preregistered, section 8): W4 as implemented is
researcher-authored generic machinery (domain-neutral, no task
knowledge). What the learner created: the SPECIFIC link (hypothesis slot
0 into the judgment consultation path) and the keep decision, both from
its own runtime measurements. The experiment demonstrates sufficiency of
W1-W4 with W4 supplied; it does NOT test invention of the trial-and-keep
policy itself.

Named open gap: a learner that invents W4 (the idea of trying path
modifications and keeping measured improvements) with no
researcher-supplied meta-policy. That is the next experiment, not this
one. Concretely, it would require the learner to select "modify my own
path and measure" from its own action repertoire because its experience
suggests path-modification is a useful action class, which in turn
requires (i) path-modification present as a candidate action, (ii) a
credit-assignment path from "wiring kept" back to "trying modifications
was valuable", and (iii) no researcher code that runs the try/measure
loop on a fixed schedule.

## 6. Architecture accounting

- New modes: 0. New bridges: 0. New handlers: 0.
- The bridge condition is a measurement control inside the experiment,
  not an architecture addition.
- Researcher-authored generic machinery: consultation list, selftest,
  wire/unwire, keep-if-better. All domain-neutral; none encodes the
  hidden rule or the solution.
- Learner-created state: hypothesis record (kind=1,param=1) and the
  consultation-list link, both written at runtime from experience.
- Cognition lines added to any shared substrate: 0 (standalone
  experiment; nothing merged into protected core or learner).

## 7. Toolchain and determinism

- Safebin guard (NAMECHECK.md Step 0): PASS. python3/python unresolvable
  under worker PATH; znc 2026.07.0-dev used for the build.
- Pure Zag, zero RNG, zero Python in build or analysis.
- 15 runs total; 5 distinct stdout byte strings; sha256 identical within
  each condition triple (sha256sums.txt).
- Stdout via single preallocated buffer + one raw syscall write; every
  binary's stdout bytes verified against preregistered predictions before
  any claim was trusted. No _zag_print used.
- Build note: this znc build has no nio_alloc builtin; the experiment
  defines its own lw_alloc on _zag_malloc (zeroed u8 buffer).

## 8. Deliverables

- PREREG.md (frozen pre-implementation), NAMECHECK.md
- lw1.zag (source), build.sh, compile.log
- lw1_bin (built binary)
- runs/{base,bridge,selfwire,noeval,nowrite}_run{1,2,3}.txt (15 outputs)
- sha256sums.txt
- REPORT.md (this file)

All under docs/lab/research-lead/overnight-20260928/learner_wiring/.
Committed locally with explicit pathspecs. Nothing pushed (standing red
line). Paper untouched.

## 9. Recommended follow-up

LW2: remove the researcher-supplied keep-if-better schedule. Give the
learner path-modification as one action among several (including
do-nothing and re-acquire), a persistent value estimate per action class
updated from its own measured outcomes, and test whether the
try-measure-keep loop for path wiring is discovered rather than
scheduled. That experiment decides whether W4 can itself be
learner-created, which is the remaining gap named in section 5.
