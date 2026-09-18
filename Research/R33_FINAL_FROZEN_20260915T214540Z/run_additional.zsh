#!/bin/zsh
set -u
ROOT=/Users/Shared/micah/Documents/TNN/TNN
E=$ROOT/Research/R33_FINAL_INTEGRATION_20260915T_REQUAL_214145Z
C=/Users/Shared/micah/Documents/zag/znc
cd "$ROOT"
run() { local label=$1 expected=$2 rc=0; shift 2; print -r -- "cwd=$PWD command=${(q)@}" >> "$E/additional.commands.txt"; "$@" > "$E/$label.stdout" 2> "$E/$label.stderr" || rc=$?; print -r -- "$label,$expected,$rc" >> "$E/additional.exits.csv"; [[ $rc == $expected ]]; }
run integration.compile 0 "$C" "$ROOT/Research/R33_CONTINUING_LIFE_V1/lane_d_packet_integration.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/integration" || exit 1
for shape in good corrupt inner torn; do mkdir -p "$E/outer_$shape"; done
for spec in write:good reload:good corrupt:corrupt refuse:corrupt inner:inner refuse:inner torn:torn refuse:torn reload:good learn:good; do
 mode=${spec%%:*}; shape=${spec#*:}; expected=0; [[ $mode == learn ]] && expected=65
 run "integration.$mode.$shape.${LINENO}" "$expected" "$E/integration" "$mode" "$E/outer_$shape" "$E/runtime_v92" || exit 1
done
run baseline.learn 65 "$E/continuing" learn || exit 1
# Existing import-constant candidate: original qualification and native regressions, never promotion.
K=/private/tmp/znc-import-const-fix
shasum -a 256 "$K" > "$E/compiler.candidate.sha256"
for label in original_v68 original_v73 v68 v73 v70 v71 v72; do
 src="$E/original_$label.zag"; [[ $label == original_* ]] && src="$E/$label.zag"
 case $label in
 v68) src="$ROOT/Research/R33_CONTINUING_LIFE_V1/outer_learner_packet_bridge_v68_tests.zag";;
 v73) src="$ROOT/Research/R33_CONTINUING_LIFE_V1/zag_checkpoint_sliceparam_repro_v73.zag";;
 v70) src="$ROOT/Research/R33_CONTINUING_LIFE_V1/zag_checkpoint_ptr_repro_v70.zag";;
 v71) src="$ROOT/Research/R33_CONTINUING_LIFE_V1/zag_checkpoint_module_repro_v71.zag";;
 v72) src="$ROOT/Research/R33_CONTINUING_LIFE_V1/zag_checkpoint_frame_repro_v72.zag";;
 esac
 run "candidate.$label.compile" 0 "$K" "$src" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/candidate_$label"
 [[ -x "$E/candidate_$label" ]] && run "candidate.$label.run" 0 "$E/candidate_$label"
done
