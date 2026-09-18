from pathlib import Path

scratch = Path('.scratch/e51y')
scratch.mkdir(parents=True, exist_ok=True)

# e51x_assemble.py is executed first by the workflow. Reuse its validated
# compatibility transforms, but not the E51X run/injection.
required = [
    Path('.scratch/e51x/E51E_PATCHED.zag'),
    Path('.scratch/e51x/E51M_PATCHED.zag'),
    Path('.scratch/e51x/E51N_PATCHED.zag'),
    Path('.scratch/e51x/E51O_LOCAL_PATCHED.zag'),
    Path('.scratch/e51x/E51X_01.zag'),
]
for p in required:
    assert p.exists(), p

run = Path('Research/R32_E51Y_NATIVE/02_run_and_gates.zagfrag').read_text()
# Fix validation-ledger lifetime deterministically before native compilation:
# keep it through outcome classification, then free it with the rest of state.
free_line = '        zfree(val_term); zfree(val_cont); zfree(val_agg); zfree(val_cells); zfree(val_stops); zfree(val_mode_wrong); zfree(val_mode_success);\n'
assert run.count(free_line) == 2, run.count(free_line)
run = run.replace(free_line, '')
cleanup_anchor = '    zfree(terminal_weights); zfree(terminal_biases); zfree(backup_weights); zfree(backup_biases); zfree(gf); zfree(gr); zfree(cf); zfree(cr); zfree(copyw); zfree(copyb);'
assert run.count(cleanup_anchor) == 1
run = run.replace(
    cleanup_anchor,
    '    zfree(val_term); zfree(val_cont); zfree(val_agg); zfree(val_cells); zfree(val_stops); zfree(val_mode_wrong); zfree(val_mode_success);\n' + cleanup_anchor,
    1,
)
(scratch / 'E51Y_RUN_PATCHED.zag').write_text(run)

parts = [
    'Research/R32_E51B_NATIVE/01_core_and_seed.zagfrag',
    'Research/R32_E51B_NATIVE/02_targets_and_metrics.zagfrag',
    'Research/R32_E51B_NATIVE/03_validation_and_fit_setup.zagfrag',
    'Research/R32_E51B_NATIVE/04_fit_validation_gates.zagfrag',
    '.scratch/e51x/E51E_PATCHED.zag',
    '.scratch/e51x/E51M_PATCHED.zag',
    '.scratch/e51x/E51N_PATCHED.zag',
    'Research/R32_E51N_NATIVE/02_truth_fix.zagfrag',
    '.scratch/e51x/E51O_LOCAL_PATCHED.zag',
    'Research/R32_E51P_NATIVE/01_local_experts.zagfrag',
    'Research/R32_E51S_NATIVE/01_extended_optimization.zagfrag',
    'Research/R32_E51V_NATIVE/01_trajectory_objective.zagfrag',
    '.scratch/e51x/E51X_01.zag',
    'Research/R32_E51Y_NATIVE/01_sequential_helpers.zagfrag',
    str(scratch / 'E51Y_RUN_PATCHED.zag'),
]
fragment = ''.join(Path(p).read_text() for p in parts)
(scratch / 'E51Y_FRAGMENT.zag').write_text(fragment)

src = Path('Research/tnn_r32_e50_provenance_temporal_contention_discriminator.zag').read_text()
assert src.count('fn main()i32 {') == 1
src = src.replace('fn main()i32 {', fragment + '\n\nfn main()i32 {', 1)
anchor = 'let aux_frozen_gate:i32=0; if(aux_frozen_hash==frozen_aux_hash){ aux_frozen_gate=1; } e45_print_pair("e50_aux_frozen_gate",aux_frozen_gate);'
assert src.count(anchor) == 1
injection = Path('Research/R32_E51Y_NATIVE/03_main_injection.zagfrag').read_text()
src = src.replace(anchor, anchor + '\n' + injection, 1)
(scratch / 'tnn_r32_e51y_five_way_sequential.zag').write_text(src)
