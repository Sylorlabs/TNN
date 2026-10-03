#!/bin/sh
# fc_build.sh -- assemble and compile the FORMAL-COMPOSE battery.
# Pure shell + safebin pinned znc. No Python.
export PATH="$HOME/safebin"
D="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/formal_compose"
cd "$D" || exit 1
BASE="fc_base.zag"
for ARM in rep gate gateb list; do
  cat $BASE fc_${ARM}.zag fc_main.zag > fc_full_${ARM}.zag
  echo "main count ${ARM} (expect 1):"
  grep -c "^fn main(" fc_full_${ARM}.zag
done
for ARM in rep gate; do
  cat $BASE fc_${ARM}.zag fc_blind.zag > fc_blind_${ARM}.zag
  echo "main count blind_${ARM} (expect 1):"
  grep -c "^fn main(" fc_blind_${ARM}.zag
done
for ARM in rep gate gateb list; do
  znc fc_full_${ARM}.zag -o fc_${ARM}_bin > fc_compile_${ARM}.txt 2>&1
  if [ $? -eq 0 ]; then echo "BUILT fc_${ARM}_bin"; else echo "FAILED fc_${ARM}_bin"; tail -30 fc_compile_${ARM}.txt; exit 1; fi
done
for ARM in rep gate; do
  znc fc_blind_${ARM}.zag -o fc_blind_${ARM}_bin > fc_blind_compile_${ARM}.txt 2>&1
  if [ $? -eq 0 ]; then echo "BUILT fc_blind_${ARM}_bin"; else echo "FAILED fc_blind_${ARM}_bin"; tail -30 fc_blind_compile_${ARM}.txt; exit 1; fi
done
echo "build-done"
