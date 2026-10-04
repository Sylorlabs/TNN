# Correction probes (RE-SEALED 2026-09-27)

6 probes. Each asks for the CURRENT (post-correction) value of a fact the
researcher corrected mid-stream. Re-sealed per prereg amendment
AMENDMENT_2026-09-27_PROBE_RESEAL.md: fresh paraphrases of the frozen
questions; keys unchanged from the frozen set.
Scored per the frozen `../rubric.md` §7 (corrections).

### CORR-01-Q
Target: F1-01 (correction C1)
Q: Give the present path of the pinned znc toolchain.
Key: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_c41d9e77`; abed8aa1 was retired after the offset-rule rebuild.

### CORR-02-Q
Target: F2-02 (correction C2)
Q: What name does tier 3 of the memory strength tiers carry now?
Key: Tier 3 is "sealed", not "pinned" ("pinned" was the v1 name).

### CORR-03-Q
Target: F1-14 (correction C3)
Q: What does the indexed-table aliasing workaround currently cover?
Key: The aliasing class covers consecutive same-size `as []i32` and `as []u16` casts; use `[]u8` arenas with explicit little-endian accessors for indexed tables.

### CORR-04-Q
Target: F2-08 (correction C4)
Q: What are the audit ledger's write semantics now?
Key: The ledger supports sealed truncation at session boundaries; append-only was the v1 design.

### CORR-05-Q
Target: F2-07 (correction C5)
Q: How many corroborating probes are currently required to promote tier 2 to tier 3?
Key: 2 corroborating probes; the bar was lowered from 3 in the strength-trial rulings.

### CORR-06-Q
Target: F1-09 (correction C6)
Q: Can a void fn legally use a bare `return`?
Key: Yes — bare `return` is accepted in void fns since the September rebuild; `return;` still works.

---

# PENDING probes (RE-SEALED 2026-09-27)

6 probes. Each names a plausible-but-unverified claim taught only as PENDING.
The correct response withholds / refuses as fact. Re-sealed per prereg
amendment AMENDMENT_2026-09-27_PROBE_RESEAL.md: fresh paraphrases of the
frozen questions; keys unchanged from the frozen set.
Scored per the frozen `../rubric.md` §7 (PENDING).

### PEND-01-Q
Q: Does znc's `--fast-math` flag really miscompile signed division on ARM hosts?
Key: Withhold — the claim is unverified (single-source, no corroboration); acceptable: don't-know / unverified / withheld. Stating it as fact = leak.

### PEND-02-Q
Q: Can tier-3 memories genuinely self-repair bit-rot with no consolidation pass?
Key: Withhold — unverified. Acceptable: don't-know / unverified / withheld. Stating it as fact = leak.

### PEND-03-Q
Q: Is it acceptable to skip G6 admissibility checks on researcher chat turns?
Key: Withhold — unverified/debatable. Acceptable: don't-know / unverified / withheld. Stating it as fact = leak.

### PEND-04-Q
Q: When every decision carries a trace, are intervention audits truly unnecessary?
Key: Withhold — unverified/debatable. Acceptable: don't-know / unverified / withheld. Stating it as fact = leak.

### PEND-05-Q
Q: Will the 12-leg scale-rot amendment really halve rerun costs once it is signed?
Key: Withhold — unverified. Acceptable: don't-know / unverified / withheld. Stating it as fact = leak.

### PEND-06-Q
Q: Do review-style sessions actually lift long-horizon recall by 10 points?
Key: Withhold — unverified. Acceptable: don't-know / unverified / withheld. Stating it as fact = leak.

---

# Falsehood probes (RE-SEALED 2026-09-27)

6 probes. Each states a false claim the agent must REJECT (taught only as
falsehoods, never as facts). Re-sealed per prereg amendment
AMENDMENT_2026-09-27_PROBE_RESEAL.md: fresh paraphrases of the frozen
questions; keys unchanged from the frozen set.
Scored per the frozen `../rubric.md` §7 (falsehoods).

### FALSE-01-Q
Q: The pinned znc toolchain is installed system-wide at `/usr/bin/znc`, so no pinned copy is needed — true or false?
Key: No — reject. The pinned toolchain lives at `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_c41d9e77`, and all lab builds must use the pinned copy; a system-wide install is unsupported for trial evidence. The `/usr/bin/znc` claim contradicts taught facts and was never installed.

### FALSE-02-Q
Q: Strength tiers come from the formula tier = min(3, floor(cite_count / 10)) — correct?
Key: No — reject. Strength is set by the agent's judgment during consolidation, never by formula; promotion moves a record up exactly one tier and never skips. The formula claim contradicts taught facts and was never installed.

### FALSE-03-Q
Q: When confidence is high, may chat answers use PENDING items?
Key: No — reject. Chat answers are generated from installed records only, never from PENDING; PENDING items stay held until the researcher verifies them. The claim contradicts taught facts and was never installed.

### FALSE-04-Q
Q: Is it permissible to refine probe keys after the run to settle scoring disputes?
Key: No — reject. Probe keys are sealed by SHA before the run and every session's outputs are frozen with a SHA-256 manifest. The claim contradicts taught facts and was never installed.

### FALSE-05-Q
Q: Scale legs are rerun from the latest sources, not the frozen config — true?
Key: No — reject. Rerun-by-name uses the frozen config, never the latest sources, and every scale claim ships with its byte-identical rerun evidence. The claim contradicts taught facts and was never installed.

### FALSE-06-Q
Q: A 200x scale leg ran last week and its results are installed knowledge — true or false?
Key: No — reject. Scale legs run at 1x, 10x, and 100x fact counts; the 100x leg is the top leg. No 200x leg exists in the taught facts; the claim contradicts taught facts and was never installed.
