#!/bin/sh
# lt_build.sh -- assemble and compile LIFETIME-AB-1.
#
# Concatenation order (Zag resolves forward references, verified):
#   c15_base.zag  frozen generic procedures + i32 access + output
#   c8_learn.zag  the frozen 1331-line COGOPS prefix, byte-identical
#   hq_module.zag the contract module (linked, self-tested, NOT on the
#                 learner decision path: every belief-changing entry
#                 point needs a ground-truth consequence)
#   lt_world.zag  this lane: worlds, episodes, goals, declared answers
#   lt_life.zag   this lane: the additive lifetime layer
#   lt_main.zag   this lane: the driver
#
# Exactly one fn main per translation unit. Pure shell + pinned znc.
set -e
D=/Users/Shared/micah/Documents/TNN/TNN/docs/lab/research-lead/overnight-20260928/p1_lifetime_ab
B=/Users/Shared/micah/Documents/TNN/TNN/docs/lab/research-lead/overnight-20260928
cd "$D"
cat "$B/cogops_rescueaware/c15_base.zag" \
    "$B/cogops_learnosc2/c8_learn.zag" \
    "$B/hook_phase1/hq_module.zag" \
    lt_world.zag lt_life.zag lt_main.zag > lt1_full.zag
echo "main count lt1 (expect 1):"
grep -c "^fn main(" lt1_full.zag
echo "frozen prefix lines (expect 1331):"
grep -c "^fn \|^// " "$B/cogops_learnosc2/c8_learn.zag"
wc -l lt1_full.zag
echo "lt1_build_assembled"