#!/bin/sh
# CAUSAL-WORLD build. Concatenation order matters (brief section 1):
# exactly one fn main, in the driver, which comes last.
set -e
cd "$(dirname "$0")"
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
cat src/zutil.zag src/k0pats.zag src/w_world.zag src/agent.zag \
    src/audit.zag src/drv.zag > causal.zag
tnn_pure_zag_report | tail -1
/Users/Shared/micah/Documents/TNN/TNN/tools/zbuild.sh ./causal.zag "$@"
