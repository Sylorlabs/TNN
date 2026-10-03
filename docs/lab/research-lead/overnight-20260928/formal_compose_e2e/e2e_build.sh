#!/bin/sh
# e2e_build.sh -- assemble and compile the FORMAL-COMPOSE-E2E battery.
# Pure shell + safebin pinned znc. No Python.
export PATH="$HOME/safebin"
D="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/formal_compose_e2e"
cd "$D" || exit 1
cat ex_learner.zag ex_world.zag es_rep.zag ex_driver_e2e.zag > ex_full_rep.zag
cat ex_learner.zag ex_world.zag es_list_ex.zag ex_driver_e2e.zag > ex_full_list.zag
cat xs_learner_e2e.zag xs_world.zag es_rep.zag xs_driver_e2e.zag > xs_full_rep.zag
cat xs_learner_e2e.zag xs_world.zag es_list_xs.zag xs_driver_e2e.zag > xs_full_list.zag
for F in ex_full_rep ex_full_list xs_full_rep xs_full_list; do
  echo "main count ${F} (expect 1):"
  grep -c "^fn main(" ${F}.zag
done
znc ex_full_rep.zag -o ex_rep_bin > ex_compile_rep.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT ex_rep_bin"; else echo "FAILED ex_rep_bin"; tail -30 ex_compile_rep.txt; exit 1; fi
znc ex_full_list.zag -o ex_list_bin > ex_compile_list.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT ex_list_bin"; else echo "FAILED ex_list_bin"; tail -30 ex_compile_list.txt; exit 1; fi
znc xs_full_rep.zag -o xs_rep_bin > xs_compile_rep.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT xs_rep_bin"; else echo "FAILED xs_rep_bin"; tail -30 xs_compile_rep.txt; exit 1; fi
znc xs_full_list.zag -o xs_list_bin > xs_compile_list.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT xs_list_bin"; else echo "FAILED xs_list_bin"; tail -30 xs_compile_list.txt; exit 1; fi
echo "build-done"
