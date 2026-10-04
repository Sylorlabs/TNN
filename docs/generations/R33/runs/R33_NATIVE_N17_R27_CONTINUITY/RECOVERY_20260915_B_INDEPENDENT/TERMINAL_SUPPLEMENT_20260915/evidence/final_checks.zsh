#!/bin/zsh
set -u
cd /Users/Shared/micah/Documents/TNN/TNN || exit 99
E=/private/tmp/r33_finish_recovery_20260915_b/n17
run() {
 local label=$1 expected=$2; shift 2
 "$@" > "$E/$label.stdout" 2> "$E/$label.stderr"
 local rc=$? cmd="${(j: :)${(q)@}}"
 jq -cn --arg label "$label" --arg cmd "$cmd" --argjson rc "$rc" --argjson expected "$expected" '{label:$label,command:$cmd,exit:$rc,expected:$expected}' >> "$E/commands.jsonl"
}
run source_selftest 0 "$E/exact_source_gate" selftest
run source_missing 66 "$E/exact_source_gate" "$E" r26_experiments.py
cp Research/R33_NATIVE_N17_R27_CONTINUITY/SOURCE_REFERENCES/r26_digest_excerpt.py.txt "$E/excerpt.txt"
run memo_frozen_build 0 /Users/Shared/micah/Documents/zag/znc "$E/src/memo_identity.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/memo_identity_frozen"
run memo_frozen_run 0 "$E/memo_identity_frozen"
run native_r25_build 0 /Users/Shared/micah/Documents/zag/znc "$E/src/N17/r25_full_digest_exact_parent_v1_runner.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/r25_native"
run source_gate_build 0 /Users/Shared/micah/Documents/zag/znc "$E/src/N17/exact_source_gate.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/exact_source_gate"
run final_source_test 0 "$E/exact_source_gate" selftest
run final_r25_missing 66 "$E/r25_native" "$E" r25.pkl r23.pkl speech.pkl robust.pkl arch.json sibling.json learning.json
run final_coverage 2 rg --files --hidden --no-ignore /Users/Shared/micah/Documents /Users/Shared/micah/Downloads /Users/bypass/Downloads /private/tmp
run final_behavior_search 2 rg --hidden --no-ignore -l 'SOCIAL_FAR|def smoke_r26|class R26State|class R27State|class.*NameMemory' /Users/Shared/micah/Documents /Users/Shared/micah/Downloads /private/tmp -g '*.py' -g '*.txt' -g '*.zag'
run final_canonical 0 shasum -a 256 -c Research/R33_CLOSEOUT_20260915T174458Z/canonical.sha256
run final_protected 0 shasum -a 256 -c Research/R33_CLOSEOUT_20260915T174458Z/protected.sha256
