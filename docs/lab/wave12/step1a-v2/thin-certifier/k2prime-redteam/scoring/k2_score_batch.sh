#!/bin/sh
# k2_score_batch.sh — per-plant scoring pipeline for the K2' blind red-team round.
# Usage: k2_score_batch.sh <NN> [<NN> ...]
# Steps per plant: copy sources (unmodified) -> build binary -> append BIN to
# working-copy manifest -> re-verify frozen certifier hash -> run_thincert.sh
# (rebuild-compare + interim 8-run matrix + v2 tripwire + thincert) ->
# hardened N=8 replay (skipped-execution for plant08).
set -u
K2=/tmp/k2prime
LAB="$HOME/workspace/tnn-lab"
PLBASE="$LAB/wave12/step1a-v2/thin-certifier/k2prime-redteam/plants"
ZNC="$LAB/toolchain/bin/znc_linux_x86_64_abed8aa1"
FIX="$LAB/wave12/step1a-v2/fixtures"
TCSRC="$LAB/wave12/step1a-v2/thin-certifier/certifier/thincert.zag"
TCPIN="$K2/certbuild/thincert_pinned"
TCFROZEN="d5e4de746a790b234726a3bcd5043bbfb7487fea203f7005e88b8c8012f2d3ca"
RUNNER="$LAB/wave12/step1a-v2/thin-certifier/runner/run_thincert.sh"
if command -v timeout >/dev/null 2>&1; then TO="timeout 300"; else TO=""; fi

for NN in "$@"; do
    PD="$K2/plant$NN"; PLSRC="$PLBASE/plant$NN"
    echo "############ plant$NN ############" | tee "$PD.score_progress" 2>/dev/null || true
    mkdir -p "$PD/tree"
    for f in "$PLSRC"/*.zag "$PLSRC/MANIFEST.txt"; do cp "$f" "$PD/tree/"; done
    cp "$PLSRC/MANIFEST.txt" "$PD/MANIFEST.work"
    ( cd "$PD/tree" && $TO $ZNC build variation.zag -o "$PD/variation.bin" >"$PD/build.log" 2>&1 ) \
        || { echo "plant$NN: BUILD FAILURE (see build.log)"; echo "BUILDFAIL" > "$PD/score.txt"; continue; }
    BINH=$(sha256sum "$PD/variation.bin" | cut -d' ' -f1)
    echo "$BINH" > "$PD/variation.bin.sha"
    echo "BIN variation.bin $BINH" >> "$PD/MANIFEST.work"
    # re-verify frozen certifier hash before this plant's run
    CURH=$(sha256sum "$TCPIN" | cut -d' ' -f1)
    if [ "$CURH" != "$TCFROZEN" ]; then
        echo "FATAL: certifier binary hash changed ($CURH)"; exit 9
    fi
    sh "$RUNNER" "$TCSRC" "$TCPIN" "$PD/MANIFEST.work" "$PD/tree" \
        "$FIX/state1.bin" "$FIX/state2.bin" "$FIX/input.bin" \
        "$PD/replay_interim.evidence" "$PD/attestation.txt" >"$PD/runner.log" 2>&1
    echo "plant$NN: runner exit=$? certifier=$(grep '^verdict=' "$PD/attestation.txt" 2>/dev/null)"
    if [ "$NN" = "08" ]; then
        echo "plant08: hardened execution SKIPPED (faulting plant; static-only scoring)" | tee "$PD/hardened_skipped.txt"
    else
        sh /tmp/k2prime/k2_hardened_replay.sh "$NN" >"$PD/hardened.log" 2>&1 || echo "plant$NN: hardened replay rc=$?"
    fi
done
echo "BATCH DONE"
