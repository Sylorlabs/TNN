#!/usr/bin/env python3
"""Generate 200 deterministic stress policies covering the DSL."""
import random

random.seed(20260923)

ATOMS_S1 = [
    "pre_is(NEW)", "pre_is(OLD)", "pre_is(HOLD)",
    "chan_present", "chan_silent",
    "sm_le(-6)", "sm_le(0)", "sm_le(2)", "sm_le(6)",
    "sm_ge(-6)", "sm_ge(0)", "sm_ge(2)", "sm_ge(6)",
    "sm_eq(-2)", "sm_eq(0)", "sm_eq(2)",
    "dir_is(NEW_LEAD)", "dir_is(OLD_LEAD)", "dir_is(TIE)",
    "sn_ge(-3)", "sn_ge(0)", "sn_ge(3)",
    "so_ge(-3)", "so_ge(0)", "so_ge(3)",
    "caval_eq_vold", "caval_eq_vnew",
]
ATOMS_S2 = ATOMS_S1 + [
    "post_is(NEW)", "post_is(OLD)", "post_is(HOLD)",
    "psm_le(-6)", "psm_le(0)", "psm_le(2)",
    "psm_ge(-6)", "psm_ge(0)", "psm_ge(2)",
    "psm_eq(-2)", "psm_eq(0)", "psm_eq(2)",
]
ACTS_S1 = ["force_consult", "block_consult"]
ACTS_S2 = ["force_withhold", "force_install(NEW)", "force_install(OLD)"]
ACTS_S4 = ["recompute_only(0)", "recompute_only(1)", "recompute_only(3)",
           "recompute_only(6)", "recompute_only(7)"]

policies = []
for pi in range(200):
    nrules = random.randint(1, 4)
    lines = [f"POLICY stress{pi}"]
    for ri in range(1, nrules + 1):
        stage = random.choice([1, 1, 2, 4])  # weight S1
        if stage == 1:
            atoms = random.sample(ATOMS_S1, random.randint(1, 3))
            act = random.choice(ACTS_S1)
        elif stage == 2:
            atoms = random.sample(ATOMS_S2, random.randint(1, 3))
            act = random.choice(ACTS_S2)
        else:
            atoms = random.sample(ATOMS_S1, random.randint(1, 2))
            act = random.choice(ACTS_S4)
        lines.append(f"RULE {ri} IF {' AND '.join(atoms)} THEN {act}")
    lines.append("END")
    policies.append("\n".join(lines) + "\n")

for pi, p in enumerate(policies):
    with open(f"stress_{pi:03d}.zpol", "w") as f:
        f.write(p)
print(f"wrote {len(policies)} stress policies")
