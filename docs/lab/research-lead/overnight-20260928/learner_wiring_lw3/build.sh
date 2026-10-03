#!/bin/sh
# LW3 build: pure Zag via the pinned znc in the worker safebin.
# Usage: sh build.sh   (run from the learner_wiring_lw3 directory)
export PATH="$HOME/safebin"
znc lw3.zag -o lw3_bin --no-analyze
