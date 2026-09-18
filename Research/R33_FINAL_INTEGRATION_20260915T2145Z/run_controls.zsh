#!/bin/zsh
set -u
E=/Users/Shared/micah/Documents/TNN/TNN/Research/R33_FINAL_INTEGRATION_20260915T2145Z
for name in stable candidate; do
 C=/Users/Shared/micah/Documents/zag/znc; [[ $name == candidate ]] && C=/private/tmp/znc-import-const-fix
 print -r -- "cwd=$PWD command=${(q)C} ${(q)E}/compiler_controls.zag --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o ${(q)E}/controls_$name" >> "$E/controls.commands.txt"
 "$C" "$E/compiler_controls.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/controls_$name" > "$E/controls_$name.build.stdout" 2> "$E/controls_$name.build.stderr"; print "$name,build,$?" >> "$E/controls.exits.csv"
 print -r -- "cwd=$PWD command=${(q)E}/controls_$name" >> "$E/controls.commands.txt"
 "$E/controls_$name" > "$E/controls_$name.run.stdout" 2> "$E/controls_$name.run.stderr"; print "$name,run,$?" >> "$E/controls.exits.csv"
done
