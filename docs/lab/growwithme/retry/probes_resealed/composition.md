# Composition probes (RE-SEALED 2026-09-27)

12 probes, two taught facts each (see Pair column). The agent must combine
both facts; each alone is insufficient. Re-sealed per prereg amendment
AMENDMENT_2026-09-27_PROBE_RESEAL.md: fresh paraphrases of the frozen
questions; keys unchanged from the frozen set.
Scored per the frozen `../rubric.md` §6.

### COMP-01-Q
Pair: F1-16 + F5-01
Q: Before intrinsic-lower, which znc pipeline pass has to run — and what fails when the order is flipped?
Key: Macro-fuse must run before intrinsic-lower; reversing them miscompiles `z_alloc` call sites.

### COMP-02-Q
Pair: F1-17 + F4-16
Q: You see an audit entry with stage=9 and d2 nonzero. What is this entry marking, and what rides in the d2 word?
Key: It marks a promotion decision and is a promotion candidate; the d2 word carries the promotion's evidence code.

### COMP-03-Q
Pair: F2-13 + F5-02
Q: A tier-3 memory's cite count is under the sweep's eviction floor. At the consolidation sweep is it deleted, kept, or what?
Key: It is demoted, never deleted; a tier-3 memory survives the sweep only when its cite count exceeds the eviction floor.

### COMP-04-Q
Pair: F2-14 + F4-02
Q: A consolidation trace names slot 12, yet the decision never read slot 12. What is the G7 audit's verdict on the turn?
Key: The trace is decorative and fails the audit — a trace is causally consulted only if the decision read the slot it cites.

### COMP-05-Q
Pair: F5-03 + F5-17
Q: M1's stdout SHA has drifted from REPORT.md while its verdicts still reproduce. Per the scale-rot amendment, what comes next and from which inputs?
Key: The leg must be rerun by name from the frozen config (never the latest sources); the amendment reruns legs whose M1 stdout SHA diverges from REPORT.md even when verdicts reproduce.

### COMP-06-Q
Pair: F3-12 + F5-04
Q: A chat answer quotes a PENDING claim verbatim, though no probe answer states it as fact. Is that a leak? Explain.
Key: Leak. The PENDING leak check audits every chat turn, not just probe answers; PENDING items cited in chat answers trip the check even when probe answers are clean.

### COMP-07-Q
Pair: F4-06 + F4-07
Q: A fact consolidation had promoted to a strong tier gets corrected by the researcher. What must the audit record for that overwrite, and what would be a violation?
Key: The erase-price audit must list the overwrite with the full price paid; a cheap edit or silent overwrite is an integrity violation and a bypass.

### COMP-08-Q
Pair: F3-16 + F4-11
Q: A draft memo asserts that PENDING items install themselves after 3 sessions. Which taught facts conflict with this, and how must it be handled?
Key: It contradicts F3-16 (nothing auto-installs), F3-07 (chat answers never from PENDING), and F4-08 (PENDING audit: any installed hit is a hard fail). Required handling: explicit deliberation trace — detected, weighed, resolved with recorded provenance; silent adoption is a fail.

### COMP-09-Q
Pair: F1-01 + F1-20
Q: What is the pinned toolchain's current location, and why are lab builds required to use the pinned copy instead of a system install?
Key: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_c41d9e77` (moved from abed8aa1, retired after the offset-rule rebuild); all lab builds must use the pinned toolchain — a system-wide znc install is unsupported for trial evidence.

### COMP-10-Q
Pair: F2-07 + F6-13
Q: Tier-2 promotion now needs how many corroborating probes, and what is the change from before?
Key: 2 (was 3); the bar was lowered in the strength-trial rulings. Promotion still moves a record up exactly one tier, never skipping.

### COMP-11-Q
Pair: F1-11 + F5-07
Q: You must index a 70KB slice. What do you do, and which two taught rules apply?
Key: Chunk it: no single slice larger than 2^25 bytes can be indexed (even `a[0]` panics above it), and chunking keeps every slice under that ceiling.

### COMP-12-Q
Pair: F5-01 + F6-12
Q: An old S5 design doc orders the pipeline differently (intrinsic-lower ahead of macro-fuse). Which facts prevail, and why?
Key: The taught order stands — parse, desugar, macro-fuse, intrinsic-lower, codegen (F5-01), with macro-fuse preceding intrinsic-lower (F1-16); the contradiction source is resolved against the earlier provenance with a deliberation trace, never silently adopted.
