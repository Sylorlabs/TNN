#!/bin/zsh
set -u
E=/Users/Shared/micah/Documents/TNN/TNN/Research/R33_FINAL_INTEGRATION_20260915T2145Z
run() { local label=$1 expected=$2 rc=0; shift 2; print -r -- "cwd=$PWD command=${(q)@}" >> "$E/transport.commands.txt"; "$@" > "$E/$label.stdout" 2> "$E/$label.stderr" || rc=$?; print -r -- "$label,$expected,$rc" >> "$E/transport.exits.csv"; [[ $rc == $expected ]]; }
run final_reload_after_all_refusals 0 "$E/integration" reload "$E/outer_good" "$E/runtime_v92" || exit 1
run final_immutable_verify 0 shasum -a 256 -c "$E/immutable.before.sha256" || exit 1
run final_stable_pin 0 shasum -a 256 /Users/Shared/micah/Documents/zag/znc || exit 1
run original_v73_disassembly 0 otool -tvV "$E/original_v73" || exit 1
run repaired_v73_disassembly 0 otool -tvV "$E/v73" || exit 1
