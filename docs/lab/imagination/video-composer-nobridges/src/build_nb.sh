#!/bin/bash
# Assemble composer_nb.zag (no-bridges composer) and compile with the pinned toolchain.
# composer_base_head.zag = step-2 base (ingest/recall/parse/trace helpers), reused.
# nb0.zag  = neutral measurement primitives extracted from step-3 (NO percentile/
#            threshold/morphology segmentation machinery — those were excluded).
# nba.zag  = generic adaptation/graft operators from step-3, reused unchanged.
# nb1..nb4 = the invention organ (measure / propose / judge / decide).
# nb5      = orchestration: parse -> invent per memory -> correspond -> slot ->
#            adapt -> track -> synthesize.
set -e
cd ~/workspace/no_bridges_composer/src
cat composer_base_head.zag nb0.zag nba.zag nb1.zag nb2.zag nb3.zag nb4.zag nb5.zag > composer_nb.zag
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 composer_nb.zag -o composer_nb_bin --no-analyze
echo "BUILD_OK"
ls -la composer_nb_bin
