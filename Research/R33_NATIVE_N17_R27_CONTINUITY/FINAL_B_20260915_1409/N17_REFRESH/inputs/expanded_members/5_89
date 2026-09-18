from pathlib import Path

src_path = Path('.scratch/e51y/tnn_r32_e51y_five_way_sequential.zag')
assert src_path.exists()
src = src_path.read_text()
helper = ''.join(Path(p).read_text() for p in (
    'Research/R32_E51AB_NATIVE/01_direct_candidate_actions.zagfrag',
    'Research/R32_E51AC_NATIVE/01_hybrid_direct_candidate.zagfrag',
    'Research/R32_E51AD_NATIVE/01a_contract_support.zagfrag',
    'Research/R32_E51AD_NATIVE/01b_critical_fit.zagfrag',
    'Research/R32_E51AD_NATIVE/01c_policy_eval.zagfrag',
    'Research/R32_E51AD_NATIVE/02a_direct_reconstruction.zagfrag',
    'Research/R32_E51AD_NATIVE/02b_router_training.zagfrag',
    'Research/R32_E51AD_NATIVE/02c_validation_outcome.zagfrag',
))
injection = Path('Research/R32_E51AD_NATIVE/03_main_injection.zagfrag').read_text()
marker = 'fn e51y_run(\n'
assert src.count(marker) == 1
src = src.replace(marker, helper + '\n\n' + marker, 1)
anchor = '    // ---- Fresh stage-84 continuation training under the frozen terminal learner.\n'
assert src.count(anchor) == 1
src = src.replace(anchor, injection + '\n' + anchor, 1)
scratch = Path('.scratch/e51ad')
scratch.mkdir(parents=True, exist_ok=True)
(scratch / 'E51AD_FRAGMENT.zag').write_text(helper)
(scratch / 'tnn_r32_e51ad_trajectory_critical_router.zag').write_text(src)
core = Path('Research/tnn_r32_e45_investigation_core.zag')
(scratch / 'tnn_r32_e45_investigation_core.zag').write_bytes(core.read_bytes())
