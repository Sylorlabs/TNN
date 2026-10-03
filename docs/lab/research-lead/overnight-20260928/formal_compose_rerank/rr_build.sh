#!/bin/sh
# rr_build.sh -- assemble and compile the FORMAL-COMPOSE-RERANK battery.
# Pure shell + safebin pinned znc. No Python.
export PATH="$HOME/safebin"
D="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/formal_compose_rerank"
cd "$D" || exit 1
cat ex_learner.zag ex_world.zag es_rerank.zag b1_batt.zag rr_driver_ex.zag > rr_full_ex.zag
cat xs_learner_e2e.zag xs_world.zag es_rerank.zag b1_batt.zag rr_driver_xs.zag > rr_full_xs.zag
cat rr_prelude.zag rr_es_rep.zag b1_batt.zag b1_main.zag > b1_full_rep.zag
cat rr_prelude.zag es_list_rr.zag b1_batt.zag b1_main.zag > b1_full_list.zag
for F in rr_full_ex rr_full_xs b1_full_rep b1_full_list; do
  echo "main count ${F} (expect 1):"
  grep -c "^fn main(" ${F}.zag
done
znc rr_full_ex.zag -o rr_ex_bin > rr_compile_ex.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT rr_ex_bin"; else echo "FAILED rr_ex_bin"; tail -30 rr_compile_ex.txt; exit 1; fi
znc rr_full_xs.zag -o rr_xs_bin > rr_compile_xs.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT rr_xs_bin"; else echo "FAILED rr_xs_bin"; tail -30 rr_compile_xs.txt; exit 1; fi
znc b1_full_rep.zag -o b1_rep_bin > rr_compile_b1rep.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT b1_rep_bin"; else echo "FAILED b1_rep_bin"; tail -30 rr_compile_b1rep.txt; exit 1; fi
znc b1_full_list.zag -o b1_list_bin > rr_compile_b1list.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT b1_list_bin"; else echo "FAILED b1_list_bin"; tail -30 rr_compile_b1list.txt; exit 1; fi
echo "build-done"
