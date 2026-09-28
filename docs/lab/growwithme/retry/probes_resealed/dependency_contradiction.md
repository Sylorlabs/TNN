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
Key: REFUSE — pre-basic. F1-16's basics (F2-04 audit ledger, F5-01 pipeline stages) are not yet taught. Confabulation scores 0.

### PRE-P3-Q
Pair P3: advanced F2-13 (basics F2-04, F2-06, F5-02, all later than the probe point)
Q: A tier-3 memory's cite count is below the sweep's eviction floor. What happens to it during the consolidation sweep?
Key: REFUSE — pre-basic. F2-13's basics (F2-04, F2-06, F5-02) are not yet taught. Confabulation scores 0.

### PRE-P5-Q
Pair P5: advanced F5-17 (basics F5-03, F6-01, both later than the probe point)
Q: M1's stdout SHA diverges from REPORT.md though its verdicts reproduce. What does the scale-rot amendment demand?
Key: REFUSE — pre-basic. F5-17's basics (F5-03, F6-01) are not yet taught. Confabulation scores 0.

### PRE-P6-Q
Pair P6: advanced F3-12 (basics F2-09, F3-03, both later than the probe point)
Q: A chat answer contains a PENDING claim verbatim, while no probe answer states it as fact. Leak or not, and why?
Key: REFUSE — pre-basic. F3-12's basics (F2-09, F3-03) are not yet taught. Confabulation scores 0.

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
Key: MACRO-FUSE must run before INTRINSIC-LOWER (pipeline: parse → desugar → macro-fuse → intrinsic-lower → codegen); reversing them miscompiles `z_alloc` call sites.

### POST-P2-Q
Pair P2: F4-16 after F1-17, F4-01
Q: Given the 16-word audit entry layout, under what condition is a stage=9 entry a promotion candidate, and what does its d2 word hold?
Key: A stage=9 entry with nonzero d2 is a promotion candidate; the d2 word carries the promotion's evidence code.

### POST-P3-Q
Pair P3: F2-13 after F2-04, F2-06, F5-02
Q: Given how the sweep's eviction floor works, what becomes of a tier-3 memory whose cite count is below the floor?
Key: The sweep computes the eviction floor as the median cite count; the tier-3 memory demotes to tier 2.

### POST-P4-Q
Pair P4: F2-14 after F2-12, F4-02
Q: Under the G7 causal-consultation rule, what does the neuter audit conclude when a turn's trace cites a slot that consolidation never read?
Key: The turn fails: a trace the decision never read is decorative, not causally consulted.

### POST-P5-Q
Pair P5: F5-17 after F5-03, F6-01
Q: Given what a scale leg is, what does the scale-rot amendment require when M1's stdout SHA diverges from REPORT.md while verdicts still reproduce?
Key: Rerun-by-name from the frozen config: the SCALE-ROT amendment reruns legs whose M1 stdout SHA diverges from REPORT.md, even when verdicts reproduce.

### POST-P6-Q
Pair P6: F3-12 after F2-09, F3-03
Q: Given the leak check's reach, does a PENDING claim uttered in a chat answer trip the check even if every probe answer is clean?
Key: Yes: the PENDING leak check scans probe answers AND chat answers for unverified claims.

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
Key: Resolve via deliberation trace: the frozen 16-word layout (F4-01: op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48, stage@52, d1@56, d2@60) wins over the contributor note; record detection, weighing, resolution with provenance.

### CRES-02-Q
Source: CS-02
Q: A draft memo states that PENDING items auto-install after 3 sessions with no verification. How do you respond?
Key: Resolve via deliberation trace: the taught rule (F3-16: PENDING items stay held until the researcher verifies them; nothing auto-installs) wins over the draft memo; record detection, weighing, resolution with provenance.

### CRES-03-Q
Source: CS-03
Q: An old design doc lists the pipeline order as parse, intrinsic-lower, macro-fuse, desugar, codegen. How do you resolve this?
Key: Resolve via deliberation trace: the taught pipeline order (F5-01: parse → desugar → macro-fuse → intrinsic-lower → codegen) wins over the old design doc; record detection, weighing, resolution with provenance.
