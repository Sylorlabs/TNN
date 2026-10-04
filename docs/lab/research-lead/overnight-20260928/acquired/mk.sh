#!/bin/bash
set -eu
D=$(cd "$(dirname "$0")" && pwd)
R=/Users/Shared/micah/Documents/TNN/.worktrees/corefreeze2/docs/lab/research-lead/overnight-20260928
cat $D/cf2_base.zag $D/cf2_data.zag $D/cf2_oracle.zag \
    $R/cogops_learnosc2/c8_learn.zag $R/hook_phase1/hq_module.zag $D/cf2_engine.zag > $D/cf2.zag
wc -l $D/cf2.zag
