# Composition probes — S7 (sealed, 12 items)

Each item is answerable ONLY by combining ≥2 facts taught in DIFFERENT sessions.
Every key lists its cited facts; the citation audit (script) verifies each item
cites ≥2 facts from ≥2 different sessions. Scored per `../rubric.md`.

### COMP-01
Q: Which znc pipeline pass must run before intrinsic-lower, and what breaks if the order is reversed?
Key: Macro-fuse must run before intrinsic-lower; reversing them miscompiles `z_alloc` call sites.
Cites: F1-16 (S1), F5-01 (S5)

### COMP-02
Q: An audit entry shows stage=9 and a nonzero d2 word. What does this entry mark, and what does the d2 word carry?
Key: It marks a promotion decision and is a promotion candidate; the d2 word carries the promotion's evidence code.
Cites: F1-17 (S1), F4-15 (S4), F4-16 (S4)

### COMP-03
Q: A tier-3 memory's cite count sits below the sweep's eviction floor. What happens to it at the consolidation sweep — deleted, kept, or something else?
Key: It is demoted, never deleted; a tier-3 memory survives the sweep only when its cite count exceeds the eviction floor.
Cites: F2-13 (S2), F5-02 (S5)

### COMP-04
Q: A consolidation trace cites slot 12, but the decision never read slot 12. What does the G7 audit conclude about this turn?
Key: The trace is decorative and fails the audit — a trace is causally consulted only if the decision read the slot it cites.
Cites: F2-14 (S2), F4-02 (S4)

### COMP-05
Q: Leg M1's stdout SHA diverges from REPORT.md, but its verdicts reproduce. Under the scale-rot amendment, what must happen next and from what inputs?
Key: The leg must be rerun by name from the frozen config (never the latest sources); the amendment reruns legs whose M1 stdout SHA diverges from REPORT.md even when verdicts reproduce.
Cites: F3-11 (S3), F5-03 (S5), F5-18 (S5)

### COMP-06
Q: A PENDING claim appears verbatim in a chat answer, but no probe answer states it as fact. Leak or not — and why?
Key: Leak. The PENDING leak check audits every chat turn, not just probe answers; PENDING items cited in chat answers trip the check even when probe answers are clean.
Cites: F3-12 (S3), F5-04 (S5)

### COMP-07
Q: The researcher corrects a fact that consolidation had promoted to a strong tier. What must the audit show for this overwrite, and what would count as a violation?
Key: The erase-price audit must list the overwrite with the full price paid; a cheap edit or silent overwrite is an integrity violation and a bypass.
Cites: F2-07/C5 (S2/S5), F4-06 (S4), F4-07 (S4)

### COMP-08
Q: A draft memo claims PENDING items auto-install after 3 sessions. Which taught facts does this contradict, and what is the required handling?
Key: It contradicts F3-16 (nothing auto-installs), F3-07 (chat answers never from PENDING), and F4-08 (PENDING audit: any installed hit is a hard fail). Required handling: explicit deliberation trace — detected, weighed, resolved with recorded provenance; silent adoption is a fail.
Cites: F3-16 (S3), F4-08 (S4)

### COMP-09
Q: Where does the pinned toolchain live today, and why must lab builds use the pinned copy rather than a system install?
Key: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_c41d9e77` (moved from abed8aa1, retired after the offset-rule rebuild); all lab builds must use the pinned toolchain — a system-wide znc install is unsupported for trial evidence.
Cites: F1-01/C1 (S1/S3), F1-20 (S1)

### COMP-10
Q: How many corroborating probes does tier-2 promotion currently need, and what changed?
Key: 2 (was 3); the bar was lowered in the strength-trial rulings. Promotion still moves a record up exactly one tier, never skipping.
Cites: F2-07/C5 (S2/S5), F2-03 (S2)

### COMP-11
Q: A 70KB slice needs indexing. What do you do, and which two taught rules govern the answer?
Key: Chunk it: no single slice larger than 2^25 bytes can be indexed (even `a[0]` panics above it), and chunking keeps every slice under that ceiling.
Cites: F1-11 (S1), F5-07 (S5)

### COMP-12
Q: The S5 old design doc gives a different pipeline order (intrinsic-lower before macro-fuse). Which facts win, and why?
Key: The taught order stands — parse, desugar, macro-fuse, intrinsic-lower, codegen (F5-01), with macro-fuse preceding intrinsic-lower (F1-16); the contradiction source is resolved against the earlier provenance with a deliberation trace, never silently adopted.
Cites: F5-01 (S5), F1-16 (S1), F4-11 (S4)
