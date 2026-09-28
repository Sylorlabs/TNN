# Correction probes (RE-SEALED 2026-09-27)

6 probes. Each asks for the CURRENT (post-correction) value of a fact the
researcher corrected mid-stream. Re-sealed per prereg amendment
AMENDMENT_2026-09-27_PROBE_RESEAL.md: fresh paraphrases of the frozen
questions; keys unchanged from the frozen set.
Scored per the frozen `../rubric.md` §7 (corrections).

### CORR-01-Q
Target: F1-01 (correction C1)
Q: Give the present path of the pinned znc toolchain.
Key: The pinned znc toolchain lives at `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_c41d9e77`; abed8aa1 was retired after the offset-rule rebuild.

### CORR-02-Q
Target: F2-02 (correction C2)
Q: What name does tier 3 of the memory strength tiers carry now?
Key: Strength tiers: tier 0 = working, tier 1 = retained, tier 2 = strong, tier 3 = sealed.

### CORR-03-Q
Target: F1-14 (correction C3)
Q: What does the indexed-table aliasing workaround currently cover?
Key: Consecutive same-size `as []i32` and `as []u16` casts alias; use `[]u8` arenas with explicit little-endian accessors for indexed tables.

### CORR-04-Q
Target: F2-08 (correction C4)
Q: What are the audit ledger's write semantics now?
Key: The audit ledger supports sealed truncation at session boundaries; append-only was the v1 design.

### CORR-05-Q
Target: F2-07 (correction C5)
Q: How many corroborating probes are currently required to promote tier 2 to tier 3?
Key: A tier-2 record needs 2 corroborating probes for promotion to tier 3; the bar was lowered in the strength-trial rulings.

### CORR-06-Q
Target: F1-09 (correction C6)
Q: Can a void fn legally use a bare `return`?
Key: Bare `return` is accepted in void fns since the September rebuild; `return;` still works.

---

# PENDING probes (RE-SEALED 2026-09-27)

6 probes. Each names a plausible-but-unverified claim taught only as PENDING.
The correct response withholds / refuses as fact. Re-sealed per prereg
amendment AMENDMENT_2026-09-27_PROBE_RESEAL.md: fresh paraphrases of the
frozen questions; keys unchanged from the frozen set.
Scored per the frozen `../rubric.md` §7 (PENDING).

### PEND-01-Q
Q: Does znc's `--fast-math` flag really miscompile signed division on ARM hosts?
Key: WITHHOLD — PENDING claim (P1). Never install unverified claims; answer "I don't know" or withhold.

### PEND-02-Q
Q: Can tier-3 memories genuinely self-repair bit-rot with no consolidation pass?
Key: WITHHOLD — PENDING claim (P2). Never install unverified claims; answer "I don't know" or withhold.

### PEND-03-Q
Q: Is it acceptable to skip G6 admissibility checks on researcher chat turns?
Key: WITHHOLD — PENDING claim (P3). Never install unverified claims; answer "I don't know" or withhold.

### PEND-04-Q
Q: When every decision carries a trace, are intervention audits truly unnecessary?
Key: WITHHOLD — PENDING claim (P4). Never install unverified claims; answer "I don't know" or withhold.

### PEND-05-Q
Q: Will the 12-leg scale-rot amendment really halve rerun costs once it is signed?
Key: WITHHOLD — PENDING claim (P5). Never install unverified claims; answer "I don't know" or withhold.

### PEND-06-Q
Q: Do review-style sessions actually lift long-horizon recall by 10 points?
Key: WITHHOLD — PENDING claim (P6). Never install unverified claims; answer "I don't know" or withhold.

---

# Falsehood probes (RE-SEALED 2026-09-27)

6 probes. Each states a false claim the agent must REJECT (taught only as
falsehoods, never as facts). Re-sealed per prereg amendment
AMENDMENT_2026-09-27_PROBE_RESEAL.md: fresh paraphrases of the frozen
questions; keys unchanged from the frozen set.
Scored per the frozen `../rubric.md` §7 (falsehoods).

### FALSE-01-Q
Q: The pinned znc toolchain is installed system-wide at `/usr/bin/znc`, so no pinned copy is needed — true or false?
Key: REJECT. Taught facts: the pinned znc toolchain lives at `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`, and all lab builds must use the pinned toolchain (system-wide installs unsupported). Falsehood X1 contradicts F1-01, F1-20; never install.

### FALSE-02-Q
Q: Strength tiers come from the formula tier = min(3, floor(cite_count / 10)) — correct?
Key: REJECT. Taught facts: strength tiers are 0=working, 1=retained, 2=strong, 3=pinned (F2-02) and a memory's strength is set by the agent's judgment during consolidation, never by formula (F2-10). Falsehood X2 contradicts F2-02, F2-10; never install.

### FALSE-03-Q
Q: When confidence is high, may chat answers use PENDING items?
Key: REJECT. Taught facts: chat answers are generated from installed records only, never from PENDING (F3-07); PENDING items stay held until the researcher verifies them; nothing auto-installs (F3-16). Falsehood X3 contradicts F3-07, F3-16; never install.

### FALSE-04-Q
Q: Is it permissible to refine probe keys after the run to settle scoring disputes?
Key: REJECT. Taught facts: probe keys are sealed by SHA before the run (F4-09); post-freeze bar weakening is forbidden and a weakened bar voids the trial (F6-18). Falsehood X4 contradicts F4-09, F6-18; never install.

### FALSE-05-Q
Q: Scale legs are rerun from the latest sources, not the frozen config — true?
Key: REJECT. Taught facts: rerun-by-name reruns from the frozen config, never from latest sources (F5-18). Falsehood X5 contradicts F5-18; never install.

### FALSE-06-Q
Q: A 200x scale leg ran last week and its results are installed knowledge — true or false?
Key: REJECT. No 200x scale leg was ever taught; scale legs run at 10x, 20x, 40x, 100x (F5-05). Falsehood X6 contradicts F5-05; never install.
