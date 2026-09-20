# 2026-09-20 path migration: pre-reorg Research/ paths remapped to post-reorg
# locations (docs/generations/R32/..., src/tools/toolchain/...). All content
# moves verified byte-identical via git blob hashes. Historical R32 tooling.
from pathlib import Path

# E51Y assembly must already have run.  E51Z preserves that exact native learner
# and injects an evaluator-only audit before E51Y confirmation/cleanup.
src_path = Path('.scratch/e51y/tnn_r32_e51y_five_way_sequential.zag')
assert src_path.exists(), src_path
src = src_path.read_text()
helper = Path('docs/generations/R32/runs/R32_E51Z_NATIVE/01_stopping_oracle_audit.zagfrag').read_text()
injection = Path('docs/generations/R32/runs/R32_E51Z_NATIVE/02_audit_injection.zagfrag').read_text()

run_marker = 'fn e51y_run(\n'
assert src.count(run_marker) == 1, src.count(run_marker)
src = src.replace(run_marker, helper + '\n\n' + run_marker, 1)

audit_anchor = '    // ---- Sealed confirmation only for the lower-resource passing arm.\n'
assert src.count(audit_anchor) == 1, src.count(audit_anchor)
src = src.replace(audit_anchor, injection + '\n' + audit_anchor, 1)

scratch = Path('.scratch/e51z')
scratch.mkdir(parents=True, exist_ok=True)
(scratch / 'tnn_r32_e51z_stopping_oracle_audit.zag').write_text(src)
core = Path('docs/generations/R32/tnn_r32_e45_investigation_core.zag')
(scratch / 'tnn_r32_e45_investigation_core.zag').write_bytes(core.read_bytes())
