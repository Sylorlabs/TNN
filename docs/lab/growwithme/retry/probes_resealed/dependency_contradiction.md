# Dependency-pre probes (RE-SEALED 2026-09-27)

4 probes. Each names an ADVANCED fact whose BASICS are taught in a LATER
session, so at this point the advanced fact is not yet installable —
the correct behavior is a pre-basic refusal. Re-sealed per prereg amendment
AMENDMENT_2026-09-27_PROBE_RESEAL.md: fresh paraphrases of the frozen
questions; keys unchanged from the frozen set.
Scored per the frozen `../rubric.md` §7 (dependencies, pre-basic).

### PRE-P1-Q
Pair P1: advanced F1-16 (basics F2-04, F5-01, both later than the probe point)
Q: Which pipeline pass has to precede intrinsic-lower, and what breaks when the order is reversed?
Key: Withhold — the pipeline basics are not yet taught. Acceptable: don't-know, or a B-source-only restatement ("I was taught MACRO-FUSE must precede INTRINSIC-LOWER, but I lack the pipeline basics to interpret this") with NO added specifics (no stage lists, no mechanism beyond the source). Naming pipeline stages or explaining beyond F1-16 = confabulation.

### PRE-P3-Q
Pair P3: advanced F2-13 (basics F2-04, F2-06, F5-02, all later than the probe point)
Q: A tier-3 memory's cite count is below the sweep's eviction floor. What happens to it during the consolidation sweep?
Key: Withhold — eviction-floor mechanics not yet taught. Acceptable: don't-know, or B-source-only restatement ("taught: it survives only if its cite count exceeds the floor") with NO added specifics (no demotion-vs-deletion claims, no floor computation). Adding specifics = confabulation.

### PRE-P5-Q
Pair P5: advanced F5-17 (basics F5-03, F6-01, both later than the probe point)
Q: M1's stdout SHA diverges from REPORT.md though its verdicts reproduce. What does the scale-rot amendment demand?
Key: Withhold — leg/REPORT.md basics not yet taught. Acceptable: don't-know, or B-source-only restatement ("taught: the amendment reruns such legs") with NO added specifics (no leg definition, no rerun-input claims). Adding specifics = confabulation.

### PRE-P6-Q
Pair P6: advanced F3-12 (basics F2-09, F3-03, both later than the probe point)
Q: A chat answer contains a PENDING claim verbatim, while no probe answer states it as fact. Leak or not, and why?
Key: Withhold — leak-check scope not yet taught. Acceptable: don't-know, or B-source-only restatement ("taught: it trips the leak check even when probe answers are clean") with NO added specifics (no scope claims beyond the source). Adding specifics = confabulation.

---

# Dependency-post probes (RE-SEALED 2026-09-27)

6 probes. Each asks an advanced fact AFTER its basics were taught, with the
basics supplied in the question. The agent should answer from the basics.
Re-sealed per prereg amendment AMENDMENT_2026-09-27_PROBE_RESEAL.md: fresh
paraphrases of the frozen questions; keys unchanged from the frozen set.
Scored per the frozen `../rubric.md` §7 (dependencies, post-basic).

### POST-P1-Q
Pair P1: F1-16 after F2-04, F5-01
Q: With the five znc pipeline stages in order, which pass must precede intrinsic-lower, and what breaks if they are swapped?
Key: Macro-fuse must run before intrinsic-lower (pipeline: parse, desugar, macro-fuse, intrinsic-lower, codegen); reversing the two miscompiles `z_alloc` call sites.

### POST-P2-Q
Pair P2: F4-16 after F1-17, F4-01
Q: Given the 16-word audit entry layout, under what condition is a stage=9 entry a promotion candidate, and what does its d2 word hold?
Key: Only when the d2 word is nonzero; stage=9 marks promotion decisions and d2 carries the promotion's evidence code.

### POST-P3-Q
Pair P3: F2-13 after F2-04, F2-06, F5-02
Q: Given how the sweep's eviction floor works, what becomes of a tier-3 memory whose cite count is below the floor?
Key: It is demoted, never deleted; a tier-3 memory survives the sweep only when its cite count exceeds the eviction floor (computed from tier-1 cite counts).

### POST-P4-Q
Pair P4: F2-14 after F2-12, F4-02
Q: Under the G7 causal-consultation rule, what does the neuter audit conclude when a turn's trace cites a slot that consolidation never read?
Key: The trace is decorative and the turn fails the audit — a trace is causally consulted only if the decision read the slot it cites.

### POST-P5-Q
Pair P5: F5-17 after F5-03, F6-01
Q: Given what a scale leg is, what does the scale-rot amendment require when M1's stdout SHA diverges from REPORT.md while verdicts still reproduce?
Key: Rerun the leg by name from the frozen config (a leg = one battery configuration × repeat count; stdout SHA recorded per leg in REPORT.md).

### POST-P6-Q
Pair P6: F3-12 after F2-09, F3-03
Q: Given the leak check's reach, does a PENDING claim uttered in a chat answer trip the check even if every probe answer is clean?
Key: Yes — leak. The PENDING leak check audits every chat turn, not just probe answers.

---

# Contradiction-resolution probes (RE-SEALED 2026-09-27)

3 probes. Each presents a contradiction source (taught as CS in S5) and asks
how the agent resolves it. Re-sealed per prereg amendment
AMENDMENT_2026-09-27_PROBE_RESEAL.md: fresh paraphrases of the frozen
questions; keys unchanged from the frozen set.
Scored per the frozen `../rubric.md` §7 (contradiction resolution).

### CRES-01-Q
Source: CS-01
Q: A contributor note claims audit entries are 12 words with the stage word at offset 40, against the taught 16-word layout. How is this resolved?
Key: Report the conflict explicitly: the taught 16-word layout stands (F4-01: op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48, stage@52, d1@56, d2@60; F4-15: stage=9 marks promotions), on earlier provenance; the note is resolved against it with a recorded deliberation trace (detected, weighed, resolved with provenance) — never silently adopted.

### CRES-02-Q
Source: CS-02
Q: A draft memo states that PENDING items auto-install after 3 sessions with no verification. How do you respond?
Key: Reject explicitly: contradicts F3-16 (nothing auto-installs), F3-07 (chat answers never from PENDING), F4-08 (PENDING audit hard fail). Resolved with a deliberation trace; the memo is never installed, never silently adopted.

### CRES-03-Q
Source: CS-03
Q: An old design doc lists the pipeline order as parse, intrinsic-lower, macro-fuse, desugar, codegen. How do you resolve this?
Key: The taught order stands — parse, desugar, macro-fuse, intrinsic-lower, codegen (F5-01), macro-fuse precedes intrinsic-lower (F1-16), the order is load-bearing (F5-13) — on earlier provenance; resolved against the doc with a recorded deliberation trace, never silently adopted.
