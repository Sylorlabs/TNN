# ADVOCATE_0821.md

Wave: wave-20260930-0821pdt. The advocate argues FOR each adoption on
the verdict slate. Every motion answers the provenance probe.

## M1: F3a2 BUILD-PASS adoption (bounded revising mechanism on second adversary byte)

Provenance probe: "What is the provenance of the artifacts under
judgment, and what exactly is new versus inherited?" The artifacts
are: the frozen prereg PREREG_PI_REV2_F3a2.md (committed alone at
97d58e38e, 2026-09-30 12:24:51 UTC) and three uncommitted evidence
files EVIDENCE_F3A2_run{1,2,3}.txt (written 12:27:16 UTC, after the
prereg). What is new: the F3a2 execution itself, the second
adversary-chosen byte 'v' (byte 118) run against the frozen binary,
the corrected K-F3-4 text, and the re-freeze authority from the
wave-20260930-0221pdt debate motion M5. What is inherited: the
implementation proc_revise2.zag (frozen at 847a8f10f since
wave-20260929-2321pdt, unmodified), the P0-P7+P9 machinery, and the
parent prereg lineage PREREG_PI_REV2.md / PREREG_PI_REV2_F3.md.

The case FOR adoption: K-F3-2 PASS (three executions byte-identical,
2282 bytes each, cmp-verified). K-F3-3 PASS (zero 'v', zero
"vab"/"vvv"/"vqv", zero 118 in the committed implementation; the
byte reaches the machinery only through argv). K-F3-4 PASS (no 0x76
in any frozen T/F1/R fixture input; F2 used 'i', F3a used 'w'; the
'v's in the evidence files are trace labels, not inputs). On K-F3-1:
the white box did everything the bar intends. It detected the
COUNTEREXAMPLE_DETECTED(vab), diagnosed pos=0 byte=118 conflicts=0
from data, constructed the primitive, revised to a new active
version, produced vab->vvv, left priors unchanged, reused vqw->vvv
with no new revision (CHECK P8-F2-reuse-no-revision: PASS), and kept
8/8 R retention probes passing after the revision. The v4/vqv/wab
wording in K-F3-1 is bar-design residue from a cumulative-learner
framing that the frozen binary's single-execution P8 interface
cannot express; the mechanism's behavior is exactly the intended
second-byte revision. The re-freeze was judge-authorized (0221pdt
debate M5), the evidence postdates the freeze, determinism is
perfect, anti-tuning is clean. Adopt as BUILD-PASS: the bounded
revising mechanism holds on a second adversary-chosen byte.

## M2: backfilled 0805pdt batch verdicts

Provenance probe: "What is the provenance of the artifacts under
judgment, and what exactly is new versus inherited?" The artifacts
are eight verdicts committed during the 0732/0750/0805pdt batch with
no debate and no run dir: L3C-V3-PASS (3bfa0947c), CAUSAL-EDITINVENT-PASS
(4c233f82a), EDITINVENT-ADV-BREAKS scope-collapse (df270dc82),
L3A-TRACE-CLEAN-BUILD-PASS (e16cc0391), HYPD-V3-PASS (e7149e452),
OPSCOPE-BEHAV-PASS (e8be2d5ef), COMPRESSION-PASS (5722ff3a8),
WORLDS-ADVERSARY-COMPLETE (6d185ebce), plus fork batteries 0732
(79/81), 0750 (80/82), 0805 (81/83). What is new this wave: the
backfilled commit-order self-check (COMMITORDER_BACKFILL_0821.md),
which verifies content-ordering for L3C v3, CAUSAL-EDITADV, and
OpScope compression (3/3 ORDER-VERIFIED). What is inherited: the
verdicts themselves and their evidence, committed by the batch
workers.

The case FOR adoption: the commit-order evidence now on record shows
every prereg strictly preceding its implementation (L3C v3:
3124d2e9a 15:14:36 before 3bfa0947c 15:19:23; CAUSAL-EDITADV:
d71be66dc 15:14:19 before 16c7665bd 15:17:08; OpScope compression:
08a0c0ac4 15:13:08 before 5722ff3a8 15:20:22). The verdicts are
narrowly scoped: EDITINVENT-ADV-BREAKS is a scope-collapse (delay-
specific, not parameter-generic), honestly narrowing
CAUSAL-EDITINVENT-PASS rather than inflating it. COMPRESSION-PASS
records net +0 lines (slice eliminated, superseding P12 debt).
WORLDS-ADVERSARY-COMPLETE is design-only, never executed, and says
so. The fork batteries show a clean hygiene trend (79/81, 80/82,
81/83, zero FAILs, 2 expected UNTESTABLEs, consistency gate ALL PASS
A1-A4, harness byte-identical every run). Adopt all eight verdicts
as recorded, with the caveat that no debate existed for those waves
now cured by this debate.

## M3: PAPER-GOVERNANCE-V3-PASS label PROCESS-INVALIDATED

Provenance probe: "What is the provenance of the artifacts under
judgment, and what exactly is new versus inherited?" The artifacts
are the v3 clean paper (c4855a65b) and the v3 governance audit
(b5a200ba0, AUDIT_V3.md) carrying the label PAPER-GOVERNANCE-V3-PASS.
What is new: the auditor's own disclosure (AUDIT_V3.md lines 107-112)
that one python3 heredoc was used for read-only regex extraction of
ledger verdict lines; the invalidation ruling. What is inherited: the
paper (unchanged, clean) and the audit's technical findings (63-claim
ledger cross-check, tally verified).

The case FOR the ruling: the label dies but the findings stand. The
owner's standing rule is explicit: disclosure does not cure use.
This is the third Python process incident this cycle; the red line
is pure Zag, no Python anywhere, and the audit claimed "Shell+git
only" while using python3. The label PAPER-GOVERNANCE-V3-PASS cannot
stand on a process-violated audit. But the paper itself is clean
(contaminated paper untouched, zero diff), and the audit's technical
findings were all re-verified with grep and git per the disclosure.
So: the label is PROCESS-INVALIDATED (void as a governance verdict),
the paper stands unblemished, and the audit's technical cross-checks
remain usable as evidence (not as a governance PASS). This is the
honest split: process verdicts require process purity; factual
findings require factual verification, which they have.

## M4: ROUTER7 banked item (no verdict this wave)

Provenance probe: "What is the provenance of the artifacts under
judgment, and what exactly is new versus inherited?" The artifacts
are: prereg PREREG_ROUTER7.md committed alone at 34347580c
(2026-09-29); uncommitted ROUTER7_RESULT.md and
ROUTER7_RAW_OUTPUT.txt (2026-09-29 23:47, claiming H-ROUTER7
SURVIVES, 3 runs byte-identical); uncommitted implementation
router7_learn.zag on disk. What is new: nothing this wave. What is
inherited: the entire item from the 2026-09-29 research-lead
process.

The case FOR the judge's position (no verdict, queued): the standing
rule is absolute that no verdict is rendered on uncommitted evidence
and implementation. The claim "H-ROUTER7 SURVIVES" sits in an
uncommitted file; the raw output is uncommitted; the implementation
is uncommitted. The prereg is properly frozen and committed, so the
item is well-formed and bankable, but adoption requires the
implementation and evidence to be committed (or dropped). The
advocate asks the judge to rule: no verdict this wave; the item
stays queued for implementation-plus-evidence commit or drop. This
is not a kill; it is governance hygiene.

## M5: WORKER_BRIEF_TEMPLATE.md one-system-rule addition (adopt as documentation)

Provenance probe: "What is the provenance of the artifacts under
judgment, and what exactly is new versus inherited?" The artifact is
the 49-line addition to
docs/lab/research-lead/overnight-20260928/worker_snippets/
WORKER_BRIEF_TEMPLATE.md, committed in 519e6d5d1 (2026-09-30
15:28:16 UTC, "Worker brief template: add ONE-SYSTEM RULE
architecture accounting"). What is new: the architecture-accounting
section (standing question, architecture delta record, mode/bridge
smells, lane rulings). What is inherited: the one-system rule
itself, issued by the owner on 2026-09-30 as a standing
architectural directive; the template's existing structure.

The case FOR adoption: the addition is pure documentation, 49
insertions, zero deletions, and it matches the standing one-system
rule verbatim (standing question "Why can the existing general
architecture not learn this behavior?", architecture delta fields,
CAUSAL_MODE/REVISION_MODE/LANGUAGE_MODE/MEMORY_MODE/PROCEDURE_MODE
as smells, three-bridge review trigger, lane rulings). It introduces
no mechanism, no mode, no bridge; it constrains future work toward
architectural compression. Adopt as process documentation.

No em-dashes in this documentation.
