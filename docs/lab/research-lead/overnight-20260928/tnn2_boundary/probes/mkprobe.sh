#!/bin/sh
# mkprobe.sh: build probes/pN.zag from probes/base.zag + probes/pN_main.zag
# by mechanically replacing ONLY the single main line. Frozen source in
# tnn2_build/ is never touched; base.zag is a verified byte-identical copy.
set -u
export PATH="$HOME/safebin"
B=~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/tnn2_boundary/probes
for N in 0 A B C D E F G H I J; do
  awk -v pf="$B/p${N}_main.zag" '
    $0 == "fn main()i32 { return run_all(); }" {
      while ((getline line < pf) > 0) print line
      next
    }
    { print }
  ' "$B/base.zag" > "$B/p${N}.zag"
  # sanity: exactly one main, and only the main line differs from base
  diffcnt=$(diff "$B/base.zag" "$B/p${N}.zag" | grep -c "^[<>]")
  echo "p$N diff-lines-vs-base: $diffcnt"
  znc "$B/p${N}.zag" -o "$B/p${N}_bin"
  echo "p$N built: $?"
done
