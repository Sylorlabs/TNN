# NAMECHECK: NT-PORT-PRESSURE (E8.1) -- the NT1 rule on the continuing learner under capacity pressure, with rule-structured families

## Step 0: Toolchain guard (mandatory, recorded before any work)

- `export PATH="$HOME/safebin"` used for every shell command in this lane.
- `which python3` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which python` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which znc` returns `/home/hatch/safebin/znc` (pinned Linux binary, znc
  2026.07.0-dev edition 2026; verified 2026-10-03; same pinned build as
  NT1/NT-D2/NT-PORT/NT-PRESSURE).
- Safebin contents: coreutils, git, znc, ...; no python3/python/perl/ruby/node.
- All scientific computation in this lane is pure Zag (znc-compiled
  binaries). Shell is used only for: safebin setup, file staging, znc
  invocation, binary execution, hashing, cmp/diff for byte-identity
  checks, git operations.
- Zero invocations of python3, python, or any other forbidden
  executable. No incidents to disclose.

## Step 1: Reference integrity

`ntpp_full.zag` (to be written after this prereg freeze) implements the
PREREG Section 2 subject on the continuing-learner skeleton with the
D1+D2 memory rules. Port base: `nt_port/nt_port_full.zag` (the
continuing-learner skeleton with D1+D2 installed; NT-PORT REPORT.md
verdict PORT-PASS, 3/3 byte-identical, all hand-traces exact). The novel
element this lane adds is the rule-structured family workload (2-hop
chains with shared substructure, PREREG Section 3), which NT-PORT and
NT-PRESSURE explicitly did not test (their honest boundary: memorized
key-value associations only).

Frozen rule set (from NT-PORT PREREG Section 2.1, unchanged):

1. Slot layout: (subj, rel, obj, dom, valid, sup, ref, ins), 32 bytes;
   key = (subj, rel); arena holds nentries, nevict, ins_seq, nslots.
2. Evidence update (NT-frozen): hit+match -> sup++; hit+mismatch ->
   ref++, revise to (new obj, 1, 0) in place iff ref > sup; revision
   does not touch `ins`.
3. D1: eviction checkpoints (valid=1, obj, sup, ref) keyed by subj;
   re-insert with valid checkpoint restores then runs the update step;
   else fresh (taught obj, 1, 0).
4. D2: ins_seq++ and slot.ins stamp on every installation (fresh and
   restore); eviction victim = max `ins`; no tie-break.
5. NOADDR arm: identical update rule, overlapping address map (PREREG
   Section 2.2); no eviction, no checkpoint table.
6. FRESH arm: identical rules to PORT, learner reset between families.
7. Kill-bar literals per PREREG Section 7 (K2: nc==2 and u==4; K3:
   c==2 and forget==0; K4: nevict==14 and phev==0; K5: NOADDR/FRESH
   exact failure signatures).

Diagnosis provenance (read 2026-10-03): negative_transfer/REPORT.md
(NT1 PASS, K1-K5); nt_port/REPORT.md (PORT-PASS, D1+D2 transfer);
nt_pressure/REPORT.md (PORT-PASS-ALL to 5x); frontier_audit/
FRONTIER_AUDIT.md Section E8.1 (the battery this lane implements) and
Priority 8 gap G8a (rule-structured families untested).

## Step 2: Lane location and commit discipline

Lane: `docs/lab/research-lead/overnight-20260928/nt_port_pressure/` on
branch `tnn-native-lab`. Commits stay local, explicit pathspecs only,
never pushed. Prereg commit-order self-check: the first commit contains
ONLY PREREG.md and NAMECHECK.md (Steps 0-2), strictly before any
implementation file. `ntpp_full.zag`, the binary, run outputs, and
REPORT.md come in later commits. The self-check (prereg commit strictly
precedes implementation commit) will be verified via git log before the
implementation commit lands.
