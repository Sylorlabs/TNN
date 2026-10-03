#!/bin/sh
# pc_build.sh -- assemble and compile the FORMAL-COMPOSE-PORT battery.
# Pure shell + safebin pinned znc. No Python.
export PATH="$HOME/safebin"
D="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/formal_compose_port"
cd "$D" || exit 1
BASE="pc_base.zag"
for ARM in rep gate gateb list; do
  cat $BASE pc_${ARM}.zag pc_main.zag > pc_full_${ARM}.zag
  echo "main count ${ARM} (expect 1):"
  grep -c "^fn main(" pc_full_${ARM}.zag
done
for ARM in rep gate; do
  cat $BASE pc_${ARM}.zag pc_blind.zag > pc_blind_${ARM}.zag
  echo "main count blind_${ARM} (expect 1):"
  grep -c "^fn main(" pc_blind_${ARM}.zag
done
for ARM in rep gate gateb list; do
  znc pc_full_${ARM}.zag -o pc_${ARM}_bin > pc_compile_${ARM}.txt 2>&1
  if [ $? -eq 0 ]; then echo "BUILT pc_${ARM}_bin"; else echo "FAILED pc_${ARM}_bin"; tail -30 pc_compile_${ARM}.txt; exit 1; fi
done
for ARM in rep gate; do
  znc pc_blind_${ARM}.zag -o pc_blind_${ARM}_bin > pc_blind_compile_${ARM}.txt 2>&1
  if [ $? -eq 0 ]; then echo "BUILT pc_blind_${ARM}_bin"; else echo "FAILED pc_blind_${ARM}_bin"; tail -30 pc_blind_compile_${ARM}.txt; exit 1; fi
done
echo "build-done"
