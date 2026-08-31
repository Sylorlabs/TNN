from pathlib import Path

base_path = Path('.scratch/e51ad/tnn_r32_e51ad_trajectory_critical_router.zag')
assert base_path.exists(), base_path
src = base_path.read_text()
frag = ''.join(Path(p).read_text() for p in (
    'Research/R32_E51AE_NATIVE/01a_contract_selection.zagfrag',
    'Research/R32_E51AE_NATIVE/01b_objective_fit.zagfrag',
    'Research/R32_E51AE_NATIVE/01c_evaluation.zagfrag',
    'Research/R32_E51AE_NATIVE/02a_run_direct.zagfrag',
    'Research/R32_E51AE_NATIVE/02b_run_development.zagfrag',
    'Research/R32_E51AE_NATIVE/02c_run_local.zagfrag',
    'Research/R32_E51AE_NATIVE/02d_run_validation.zagfrag',
))
old_injection = Path('Research/R32_E51AD_NATIVE/03_main_injection.zagfrag').read_text()
new_injection = Path('Research/R32_E51AE_NATIVE/03_main_injection.zagfrag').read_text()
marker = 'fn e51y_run(\n'
assert src.count(marker) == 1, src.count(marker)
assert src.count(old_injection) == 1, src.count(old_injection)
src = src.replace(marker, frag + '\n\n' + marker, 1)
src = src.replace(old_injection, new_injection, 1)
scratch = Path('.scratch/e51ae')
scratch.mkdir(parents=True, exist_ok=True)
(scratch / 'E51AE_FRAGMENT.zag').write_text(frag)
(scratch / 'tnn_r32_e51ae_trajectory_critical_candidate_residual.zag').write_text(src)
core = Path('Research/tnn_r32_e45_investigation_core.zag')
(scratch / 'tnn_r32_e45_investigation_core.zag').write_bytes(core.read_bytes())
