#!/bin/sh
# d3_build.sh -- assemble and compile the FORMAL-COMPOSE-DAG3 battery.
# Pure shell + safebin pinned znc. No Python.
export PATH="$HOME/safebin"
D="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/formal_compose_dag3"
cd "$D" || exit 1
cat rr_prelude.zag es_rerank.zag d3_shim_rerank.zag d3_batt.zag d3_main.zag > d3_full_rerank.zag
cat rr_prelude.zag rr_es_rep.zag d3_shim_rep.zag d3_batt.zag d3_main.zag > d3_full_rep.zag
cat rr_prelude.zag es_list_rr.zag d3_shim_list.zag d3_batt.zag d3_main.zag > d3_full_list.zag
for F in d3_full_rerank d3_full_rep d3_full_list; do
  echo "main count ${F} (expect 1):"
  grep -c "^fn main(" ${F}.zag
done
znc d3_full_rerank.zag -o d3_rerank_bin > d3_compile_rerank.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT d3_rerank_bin"; else echo "FAILED d3_rerank_bin"; tail -30 d3_compile_rerank.txt; exit 1; fi
znc d3_full_rep.zag -o d3_rep_bin > d3_compile_rep.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT d3_rep_bin"; else echo "FAILED d3_rep_bin"; tail -30 d3_compile_rep.txt; exit 1; fi
znc d3_full_list.zag -o d3_list_bin > d3_compile_list.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT d3_list_bin"; else echo "FAILED d3_list_bin"; tail -30 d3_compile_list.txt; exit 1; fi
echo "build-done"
