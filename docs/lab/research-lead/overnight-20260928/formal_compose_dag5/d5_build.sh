#!/bin/sh
# d5_build.sh -- assemble and compile the FORMAL-COMPOSE-DAG5 battery.
# Pure shell + safebin pinned znc. No Python.
export PATH="$HOME/safebin"
D="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/formal_compose_dag5"
cd "$D" || exit 1
cat rr_prelude.zag es_rerank.zag d5_shim_rerank.zag d5_batt.zag d5_main.zag > d5_full_rerank.zag
cat rr_prelude.zag rr_es_rep.zag d5_shim_rep.zag d5_batt.zag d5_main.zag > d5_full_rep.zag
cat rr_prelude.zag es_list_rr.zag d5_shim_list.zag d5_batt.zag d5_main.zag > d5_full_list.zag
for F in d5_full_rerank d5_full_rep d5_full_list; do
  echo "main count ${F} (expect 1):"
  grep -c "^fn main(" ${F}.zag
done
znc d5_full_rerank.zag -o d5_rerank_bin > d5_compile_rerank.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT d5_rerank_bin"; else echo "FAILED d5_rerank_bin"; tail -30 d5_compile_rerank.txt; exit 1; fi
znc d5_full_rep.zag -o d5_rep_bin > d5_compile_rep.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT d5_rep_bin"; else echo "FAILED d5_rep_bin"; tail -30 d5_compile_rep.txt; exit 1; fi
znc d5_full_list.zag -o d5_list_bin > d5_compile_list.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT d5_list_bin"; else echo "FAILED d5_list_bin"; tail -30 d5_compile_list.txt; exit 1; fi
echo "build-done"
