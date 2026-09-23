from pathlib import Path

# Reuse the validated E51Y terminal reconstruction, inject only the E51AA audit,
# and return before stage-84 continuation training.
src_path = Path('.scratch/e51y/tnn_r32_e51y_five_way_sequential.zag')
assert src_path.exists(), src_path
src = src_path.read_text()
helper = Path('Research/R32_E51AA_NATIVE/01_resource_terminal_audit.zagfrag').read_text()
injection = Path('Research/R32_E51AA_NATIVE/02_audit_injection.zagfrag').read_text()

run_marker = 'fn e51y_run(\n'
assert src.count(run_marker) == 1, src.count(run_marker)
src = src.replace(run_marker, helper + '\n\n' + run_marker, 1)

anchor = '    // ---- Fresh stage-84 continuation training under the frozen terminal learner.\n'
assert src.count(anchor) == 1, src.count(anchor)
src = src.replace(anchor, injection + '\n' + anchor, 1)

scratch = Path('.scratch/e51aa')
scratch.mkdir(parents=True, exist_ok=True)
(scratch / 'tnn_r32_e51aa_resource_terminal_decomposition.zag').write_text(src)
core = Path('Research/tnn_r32_e45_investigation_core.zag')
(scratch / 'tnn_r32_e45_investigation_core.zag').write_bytes(core.read_bytes())
