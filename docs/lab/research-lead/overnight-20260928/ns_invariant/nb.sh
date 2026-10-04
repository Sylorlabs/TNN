#!/bin/bash
# nb.sh -- lane-local pure-Zag build+run+determinism harness for ns_invariant.
#
# Identical contract to tools/zbuild.sh (charter section 4: shell is
# orchestration only; every number is computed inside the Zag binary).
# Difference: prepends the lane directory to PATH so the produced binary is
# resolvable without an absolute path, because the restricted pure-Zag PATH
# does not include the current directory.
#
# Usage: ./nb.sh FILE.zag [--rep N|--nobuild]
set -u
export PATH="$(pwd):$PATH"
exec /Users/Shared/micah/Documents/TNN/TNN/tools/zbuild.sh "$@"
