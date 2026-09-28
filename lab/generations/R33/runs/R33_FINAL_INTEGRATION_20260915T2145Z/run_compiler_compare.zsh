#!/bin/zsh
set -u
E=/Users/Shared/micah/Documents/TNN/TNN/Research/R33_FINAL_INTEGRATION_20260915T2145Z
mkdir -p "$E/compiler_compare"
cd /Users/Shared/micah/Documents/zag/zag-poc
for compiler in stable candidate; do
 C=/Users/Shared/micah/Documents/zag/znc
 [[ $compiler == candidate ]] && C=/private/tmp/znc-import-const-fix
 for src in tests/semantic/import_const_flat.zag tests/semantic/import_const_qualified.zag tests/semantic/import_const_values.zag tests/semantic/direct_function_values.zag tests/semantic/scoping_import_shadow.zag tests/semantic/scoping_capture_shadow.zag tests/semantic/scoping_block_shadow.zag tests/aarch64_parameter_shadow.zag; do
 n=${src:t:r}; stem="$E/compiler_compare/$compiler.$n"
 print -r -- "cwd=$PWD command=${(q)C} ${(q)src} --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o ${(q)stem}" >> "$E/compiler_compare/commands.txt"
 "$C" "$src" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$stem" > "$stem.build.stdout" 2> "$stem.build.stderr"
 rc=$?; print "$compiler,$n,build,$rc" >> "$E/compiler_compare/exits.csv"
 if [[ $rc == 0 ]]; then
 print -r -- "cwd=$PWD command=${(q)stem}" >> "$E/compiler_compare/commands.txt"
 "$stem" > "$stem.run.stdout" 2> "$stem.run.stderr"; print "$compiler,$n,run,$?" >> "$E/compiler_compare/exits.csv"
 fi
 done
done
