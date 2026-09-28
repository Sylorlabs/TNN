#!/bin/zsh
set -eu
ROOT=/Users/Shared/micah/Documents/TNN/TNN
E=$ROOT/Research/R33_FINAL_INTEGRATION_20260915T2145Z
freeze() { local file=$1 rel=${1#$ROOT/} imported resolved; [[ -f "$E/sources/$rel" ]] && return 0; mkdir -p "$E/sources/${rel:h}"; cp "$file" "$E/sources/$rel"; while IFS= read -r imported; do resolved=$(realpath "${file:h}/$imported"); [[ "$resolved" == "$ROOT/"* ]] || return 1; freeze "$resolved"; done < <(sed -n 's/^@import("\([^"]*\)").*/\1/p' "$file"); }
freeze "$ROOT/Research/R33_CONTINUING_LIFE_V1/lane_d_packet_integration.zag"
mkdir -p "$E/compiler_sources"
cp /Users/Shared/micah/Documents/zag/znc "$E/compiler.stable.znc"
cp /private/tmp/znc-import-const-fix "$E/compiler.candidate.znc"
cp /Users/Shared/micah/Documents/zag/zag-poc/selfhost/parse.zag "$E/compiler_sources/parse.zag"
cp /Users/Shared/micah/Documents/zag/zag-poc/selfhost/native/acodegen.zag "$E/compiler_sources/acodegen.zag"
cp -R /Users/Shared/micah/Documents/zag/zag-poc/tests/semantic "$E/compiler_sources/semantic"
cp /Users/Shared/micah/Documents/zag/zag-poc/tests/aarch64_parameter_shadow.zag "$E/compiler_sources/"
cp "$ROOT/Research/R33_NATIVE_N17_R27_CONTINUITY/R25_LINEAGE_RECORD.json" "$E/R25_LINEAGE_RECORD.witness.json"
cp "$ROOT/Research/R33_NATIVE_N17_R27_CONTINUITY/VERIFIER_CHECK_MATRIX_V3.json" "$E/R27_MATRIX.witness.json"
cp "$ROOT/Research/R33_NATIVE_N17_R27_CONTINUITY/R26_VERIFIER_CHECK_MATRIX_V1.json" "$E/R26_MATRIX.witness.json"
