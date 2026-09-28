#!/bin/zsh
set -eu
ROOT=/Users/Shared/micah/Documents/TNN/TNN
E=$ROOT/Research/R33_FINAL_INTEGRATION_20260915T2145Z
cd "$ROOT"
i=0
run() { local label=$1 expected=$2 rc=0; shift 2; print -r -- "cwd=$PWD command=${(q)@}" >> "$E/final_transport.commands.txt"; "$@" > "$E/$label.stdout" 2> "$E/$label.stderr" || rc=$?; print -r -- "$label,$expected,$rc" >> "$E/final_transport.exits.csv"; [[ $rc == $expected ]]; }
for shape in good corrupt inner torn; do mkdir "$E/final_outer_$shape"; done
for spec in write:good reload:good corrupt:corrupt refuse:corrupt inner:inner refuse:inner torn:torn refuse:torn reload:good learn:good; do
 i=$((i+1));mode=${spec%%:*};shape=${spec#*:};expected=0;[[ $mode == learn ]] && expected=65
 run "final_integration.$i.$mode.$shape" "$expected" "$E/integration" "$mode" "$E/final_outer_$shape" "$E/runtime_v92"
done
run final_baseline_learn 65 "$E/continuing" learn
run final_preservation 0 shasum -a 256 -c "$E/immutable.before.sha256"
