# JUDGE_0821.md

Wave: wave-20260930-0821pdt. Reasoned rulings with numbers cited.
Every motion answers the provenance probe.

## M1: F3a2 (RULED: BUILD-FAIL on K-F3-1 bar text; re-freeze and re-run ordered)

Provenance probe: "What is the provenance of the artifacts under
judgment, and what exactly is new versus inherited?" Re-freeze
prereg 97d58e38e (committed alone, 2026-09-30 12:24:51 UTC); three
uncommitted evidence files (12:27:16 UTC, post-freeze); inherited
frozen implementation 847a8f10f (2026-09-30 06:32:23 UTC,
unmodified since).

Findings of fact (verified this wave):
- K-F3-2: PASS. Three executions byte-identical (cmp), 2282 bytes
  each, fails=0, BUILD-PASS in all three.
- K-F3-3: PASS. Zero char literal 'v', zero "vab"/"vvv"/"vqv",
  zero numeric 118 (and zero 0x76 variants) in the committed
  implementation blob; the byte reaches machinery only via argv.
- K-F3-4: PASS. Zero byte 0x76 in any frozen T/F1/R fixture input
  literal; F2 used 'i', F3a used 'w'; evidence-file 'v's are trace
  labels, not inputs.
- K-F3-1: NOT MET AS WRITTEN. The trace shows "VERSION v3 ACTIVE
  (parent v2)" where the bar demands "v4 ACTIVE with parent v3";
  "PREDICT vqw -> vvv [ok]" where the bar demands "vqv"->"vvv";
  no "wab"->"www" line where the bar lists it. The frozen binary's
  P8 interface executes a single adversary phase per run, so v4 is
  unreachable; the K-F3-1 text describes a cumulative execution the
  frozen implementation cannot produce. These are bar-design errors,
  not mechanism failures: the white box detected vab, diagnosed
  byte 118 from data, constructed the primitive, revised to a new
  active version, reused without revision (CHECK
  P8-F2-reuse-no-revision: PASS), and held 8/8 R retention probes
  post-revision.

Ruling: BUILD-FAIL on K-F3-1 bar text. The standing rule is
absolute: never weaken a frozen kill bar to force a pass, and never
count a preregistered threshold as achieved before frozen
execution. Reading "v4" as "v3" and "vqv" as "vqw" after seeing the
trace is exactly the reinterpretation the rule forbids. The F3a
precedent controls: F3a was killed on K-F3-4 bar text despite a
clean trace, then re-frozen with corrected text and re-run. The
advocate's "intent" argument is rejected for the same reason.

Ordered: re-freeze K-F3-1 with corrected text (v3 ACTIVE parent
v2; vqw reuse probe; drop wab; name the 8 R-probe retention
explicitly), then re-run on the same frozen binary 847a8f10f. The
verified K-F3-2/3/4 results stand and need not be re-proven; only
the K-F3-1 text changes.

On the ordering caveat: the 0221pdt debate motion M5 authorized the
evaluation-only re-freeze design, and this wave verified the
implementation is unmodified since 847a8f10f with evidence postdating
the freeze. The judge does not re-litigate that prior authorization,
but records the strict-letter caveat: the implementation commit
(06:32:23) predates the prereg commit (12:24:51). The re-freeze
path, not a fresh prereg-then-implement, remains the authorized
route for this item.

## M2: backfilled 0805pdt batch (RULED: adopt as RECORDED with ordering verified; process items separated)

Provenance probe: "What is the provenance of the artifacts under
judgment, and what exactly is new versus inherited?" Eight verdicts
plus three fork batteries committed across the 0732/0750/0805pdt
batch with no debate and no run dir; new this wave is the backfilled
commit-order audit (3/3 ORDER-VERIFIED: L3C v3 3124d2e9a 15:14:36
before 3bfa0947c 15:19:23; CAUSAL-EDITADV d71be66dc 15:14:19 before
16c7665bd 15:17:08; OpScope compression 08a0c0ac4 15:13:08 before
5722ff3a8 15:20:22).

Ruling: the five mechanism verdicts are ADOPTED AS RECORDED
(L3C-V3-PASS, L3A-TRACE-CLEAN-BUILD-PASS, HYPD-V3-PASS,
OPSCOPE-BEHAV-PASS, COMPRESSION-PASS), with the standing caveat that
this debate is backfill: it verifies ordering and records evidence,
it does not supply the contemporaneous adversarial scrutiny the
rule requires. CAUSAL-EDITINVENT-PASS is adopted WITH its narrowing
carried in the verdict line: the ledger entry must read
CAUSAL-EDITINVENT-PASS narrowed by EDITINVENT-ADV-BREAKS
scope-collapse (delay-specific, not parameter-generic), not a bare
PASS. EDITINVENT-ADV-BREAKS is adopted as the narrowing verdict.
WORLDS-ADVERSARY-COMPLETE is recorded as a process milestone
(sealed W6/W9 designs, K1/K2/K3 pass, never executed), not a
verdict. The fork batteries (0732: 79/81; 0750: 80/82; 0805: 81/83;
all with 2 expected UNTESTABLEs, zero FAILs, consistency gate ALL
PASS) are recorded as hygiene, not verdicts. The skeptic is right
that post-hoc ordering checks the record, not the process; the
verdicts stand on their evidence, and the missing contemporaneous
debate is a governance gap now closed, not a retroactive cure.

## M3: PAPER-GOVERNANCE-V3-PASS (RULED: label PROCESS-INVALIDATED; findings downgraded to pending clean re-audit)

Provenance probe: "What is the provenance of the artifacts under
judgment, and what exactly is new versus inherited?" The v3 paper
(c4855a65b) and the v3 audit (b5a200ba0, AUDIT_V3.md) carrying the
label PAPER-GOVERNANCE-V3-PASS; new is the auditor's own disclosure
(AUDIT_V3.md lines 107-112): one python3 heredoc used for read-only
regex extraction of ledger verdict lines, with the auditor's claim
that every finding was re-verified with grep and git.

Ruling: the label PAPER-GOVERNANCE-V3-PASS is PROCESS-INVALIDATED
and void. A governance PASS certifies process purity; the process
used Python on a pure-Zag red line, and "disclosure does not cure
use." This is the third Python process incident this cycle, which
aggravates: the audit lane is not holding the red line.

On the findings: the judge does not accept the compromised
process's self-certification that "every finding was re-verified."
The audit's technical cross-checks (63-claim tally match,
terminology checks) are mechanical claims reproducible with grep;
they are downgraded to UNVERIFIED-PENDING-CLEAN-RE-AUDIT, not
"stand." Ordered: an independent clean re-audit of the v3 paper
against the ledger, shell and git only, zero Python, before any
governance PASS label is carried again. The paper itself is not
accused: its content is what it is, the contaminated paper has zero
diff, and the ledger (not the audit) is the authority for the
paper's claims. But no cleanliness certification travels on this
audit.

## M4: ROUTER7 (RULED: no verdict; commit-or-drop deadline set)

Provenance probe: "What is the provenance of the artifacts under
judgment, and what exactly is new versus inherited?" Prereg
committed alone at 34347580c (2026-09-29); ROUTER7_RESULT.md (claims
H-ROUTER7 SURVIVES), ROUTER7_RAW_OUTPUT.txt, and router7_learn.zag
all uncommitted since 2026-09-29 23:47, over eight hours. Nothing is
new this wave.

Ruling: no verdict, as both advocate and skeptic agree; the
standing rule bars verdicts on uncommitted evidence. Ordered: the
implementation and raw evidence must be committed, or the item
dropped, by the next wave (wave-20260930-1121pdt); otherwise the
item is retired as EXPIRED and the prereg freeze lapses. The result
file's claim that the prereg is "strictly before implementation"
cannot be evaluated until the implementation is committed; that
check is part of the commit-or-drop gate.

## M5: WORKER_BRIEF_TEMPLATE.md one-system-rule addition (RULED: filed as process documentation; embedded lane rulings NOT adopted)

Provenance probe: "What is the provenance of the artifacts under
judgment, and what exactly is new versus inherited?" The 49-line
addition committed in 519e6d5d1 (2026-09-30 15:28:16 UTC); new is
the architecture-accounting section; inherited is the owner's
standing one-system rule (2026-09-30).

Ruling: the addition is FILED as process documentation. It is
committed, dash-clean, matches the standing rule verbatim, and its
process sections (the standing question "Why can the existing
general architecture not learn this behavior?", the architecture
delta record, the mode/bridge smells) are legitimate brief
guidance. However, the embedded lane rulings (causal-revert stays
evidence; OpScope gate lineage closed; L3B adversary direction;
threshold bounded; continuing-learner priority) are substantive
research decisions that were never debated. They are NOT adopted as
decided governance; they stand as proposals pending their own
motions with advocate, skeptic, and judge. Workers may read the
template; no one may cite its lane rulings as decided until each
is ruled on.

No em-dashes in this documentation.
