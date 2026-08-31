from pathlib import Path

scratch = Path('.scratch/e51x')
scratch.mkdir(parents=True, exist_ok=True)

# Preserve exactly the dependency compatibility repairs used by E51W.
e51e = ''.join(Path(p).read_text() for p in [
    'Research/R32_E51E_NATIVE/00_compat.zagfrag',
    'Research/R32_E51E_NATIVE/01_joint_action_value.zagfrag',
    'Research/R32_E51E_NATIVE/02_validation.zagfrag',
    'Research/R32_E51E_NATIVE/03_run_and_gates.zagfrag',
])
assert e51e.count('fn e51e_build_training_episode(') == 1
e51e = e51e.replace(
    'fn e51e_build_training_episode(',
    'fn e51e_build_training_episode_retired_seed_coupled(',
    1,
)
(scratch / 'E51E_PATCHED.zag').write_text(e51e)

e51m = Path('Research/R32_E51M_NATIVE/01_calibration_curve.zagfrag').read_text()
assert e51m.count('fn e51m_allocate_seeds(') == 1
e51m = e51m.replace(
    'fn e51m_allocate_seeds(',
    'fn e51m_allocate_seeds_retired_exhausted(',
    1,
)
(scratch / 'E51M_PATCHED.zag').write_text(e51m)

e51n = Path('Research/R32_E51N_NATIVE/01_domain_rng.zagfrag').read_text()
assert e51n.count('fn e51n_make_truth(') == 1
e51n = e51n.replace(
    'fn e51n_make_truth(',
    'fn e51n_make_truth_retired_extra_draw(',
    1,
)
(scratch / 'E51N_PATCHED.zag').write_text(e51n)

local = Path('Research/R32_E51O_NATIVE/01_local_memory.zagfrag').read_text()
for old, new in [
    ('let minv:i32=e50_batch_column(records,feature+1,0);',
     'let minv:i32=e50_batch_column(records,0,feature+1,0);'),
    ('let sums:[]i64=zalloc_l(E51O_MAX_CELLS);',
     'let sums:[]i32=zalloc_i(E51O_MAX_CELLS);'),
    ('sums[c]=sums[c]+(residual as i64);',
     'sums[c]=sums[c]+residual;'),
    ('corrections[cell]=e51m_clamp_i64(sums[cell]/(cell_counts[cell] as i64),-3000,3000);',
     'corrections[cell]=r32e45_clamp(sums[cell]/cell_counts[cell],-3000,3000);'),
]:
    assert local.count(old) == 1, (old, local.count(old))
    local = local.replace(old, new, 1)
assert local.count('sums:[]i64') == 1
local = local.replace('sums:[]i64', 'sums:[]i32', 1)
for old, new in [
    ('snapshot_losses:[]i64', 'snapshot_losses:[]i32'),
    ('losses_a:[]i64', 'losses_a:[]i32'),
    ('losses_b:[]i64', 'losses_b:[]i32'),
]:
    assert old in local
    local = local.replace(old, new)
assert local.count('snapshot_losses[level]=current_loss;') == 2
local = local.replace(
    'snapshot_losses[level]=current_loss;',
    'snapshot_losses[level]=e51m_hash_i64(current_loss);',
)
strict = 'if(level>0 && snapshot_losses[level]>snapshot_losses[level-1] && snapshot_counts[level]>=snapshot_counts[level-1]){ strict_loss_gate.*=0; }'
assert local.count(strict) == 1
local = local.replace(strict, '')
(scratch / 'E51O_LOCAL_PATCHED.zag').write_text(local)

vrun = Path('Research/R32_E51V_NATIVE/02_run.zagfrag').read_text()
old = 'mode_success:[]i32\n)void {'
new = 'mode_success:[]i32,\n    mode_start:i32\n)void {'
assert vrun.count(old) == 1
vrun = vrun.replace(old, new, 1)
old = 'known_total.*=0; known_reachable.*=0; no_unique_total.*=0; no_unique_reachable.*=0; gained.*=0; lost.*=0; switch_lost.*=0; e45_zero(mode_success,E45_MODES);'
new = 'known_total.*=0; known_reachable.*=0; no_unique_total.*=0; no_unique_reachable.*=0; gained.*=0; lost.*=0; switch_lost.*=0; let mz:i32=0; while(mz<E45_MODES){ mode_success[mode_start+mz]=0; mz=mz+1; }'
assert vrun.count(old) == 1
vrun = vrun.replace(old, new, 1)
assert vrun.count('mode_success[mode]=mode_success[mode]+1;') == 1
vrun = vrun.replace(
    'mode_success[mode]=mode_success[mode]+1;',
    'mode_success[mode_start+mode]=mode_success[mode_start+mode]+1;',
    1,
)
old = 'let mode_slice:[]i32=modes; e51v_eval_arm(val_records,val_targets,E51V_VALIDATION_EPISODES,20,terminal_weights,terminal_biases,global_weights,global_bias,prototypes,parents,ranges,ew,ws,eb,bs,control_reached,control,&kt,&kr,&ut,&ur,&gain,&loss,&swloss,mode_slice[arm*E45_MODES:]);'
new = 'e51v_eval_arm(val_records,val_targets,E51V_VALIDATION_EPISODES,20,terminal_weights,terminal_biases,global_weights,global_bias,prototypes,parents,ranges,ew,ws,eb,bs,control_reached,control,&kt,&kr,&ut,&ur,&gain,&loss,&swloss,modes,arm*E45_MODES);'
assert vrun.count(old) == 1
vrun = vrun.replace(old, new, 1)
old = 'e51v_eval_arm(con_records,con_targets,E51V_CONFIRM_EPISODES,40,terminal_weights,terminal_biases,global_weights,global_bias,prototypes,parents,ranges,ew,0,eb,0,dummy_control,1,&kt,&kr,&ut,&ur,&ga,&lo,&sl,con_modes);'
new = 'e51v_eval_arm(con_records,con_targets,E51V_CONFIRM_EPISODES,40,terminal_weights,terminal_biases,global_weights,global_bias,prototypes,parents,ranges,ew,0,eb,0,dummy_control,1,&kt,&kr,&ut,&ur,&ga,&lo,&sl,con_modes,0);'
assert vrun.count(old) == 1
vrun = vrun.replace(old, new, 1)
(scratch / 'E51V_RUN_PATCHED.zag').write_text(vrun)

# Mechanical E51W -> E51X native source transformation. The only scientific
# changes are fresh world stages and optimization ceilings/arm count.
one = Path('Research/R32_E51W_NATIVE/01_trajectory_dose.zagfrag').read_text()
one = one.replace('E51W', 'E51X').replace('e51w', 'e51x')
for old, new in {
    'const E51X_STAGE_DEV:i32=78;': 'const E51X_STAGE_DEV:i32=81;',
    'const E51X_STAGE_VALIDATION:i32=79;': 'const E51X_STAGE_VALIDATION:i32=82;',
    'const E51X_STAGE_CONFIRM:i32=80;': 'const E51X_STAGE_CONFIRM:i32=83;',
    'const E51X_DOSES:i32=4;': 'const E51X_DOSES:i32=3;',
    'const E51X_ARMS:i32=5;': 'const E51X_ARMS:i32=4;',
    '''fn e51x_dose(index:i32)i32 {
    if(index==0){ return 12; }
    if(index==1){ return 48; }
    if(index==2){ return 96; }
    return 192;
}''': '''fn e51x_dose(index:i32)i32 {
    if(index==0){ return 192; }
    if(index==1){ return 384; }
    return 768;
}''',
}.items():
    assert one.count(old) == 1, (old, one.count(old))
    one = one.replace(old, new, 1)
(scratch / 'E51X_01.zag').write_text(one)

two = Path('Research/R32_E51W_NATIVE/02_run.zagfrag').read_text()
two = two.replace('E51W', 'E51X').replace('e51w', 'e51x')
two = two.replace('dose12_delegates_e51p_optimizer=1', 'lowest_dose_192=1')
two = two.replace(
    'arm_0_state96_1_traj12_2_traj48_3_traj96_4_traj192',
    'arm_0_state96_1_traj192_2_traj384_3_traj768',
)
for old, new in {
    'TRAJECTORY_DOSE_RESCUE_CONFIRMED': 'EXTENDED_TRAJECTORY_DOSE_RESCUE_CONFIRMED',
    'TRAJECTORY_DOSE_VALIDATION_RESCUE_CONFIRMATION_FAIL': 'EXTENDED_TRAJECTORY_DOSE_VALIDATION_RESCUE_CONFIRMATION_FAIL',
    'TRAJECTORY_DOSE_STABLE_PARTIAL_SIGNAL': 'EXTENDED_TRAJECTORY_DOSE_STABLE_PARTIAL_SIGNAL',
    'TRAJECTORY_DOSE_AGGREGATE_SIGNAL_WITH_INSTABILITY': 'EXTENDED_TRAJECTORY_DOSE_INSTABILITY',
    'TRAJECTORY_DOSE_PLATEAU': 'EXTENDED_TRAJECTORY_DOSE_PLATEAU',
}.items():
    two = two.replace(old, new)
(scratch / 'E51X_02.zag').write_text(two)

inj = Path('Research/R32_E51W_NATIVE/03_main_injection.zagfrag').read_text()
inj = inj.replace('E51W', 'E51X').replace('e51w', 'e51x')
(scratch / 'E51X_INJECTION.zag').write_text(inj)

parts = [
    'Research/R32_E51B_NATIVE/01_core_and_seed.zagfrag',
    'Research/R32_E51B_NATIVE/02_targets_and_metrics.zagfrag',
    'Research/R32_E51B_NATIVE/03_validation_and_fit_setup.zagfrag',
    'Research/R32_E51B_NATIVE/04_fit_validation_gates.zagfrag',
    str(scratch / 'E51E_PATCHED.zag'),
    str(scratch / 'E51M_PATCHED.zag'),
    str(scratch / 'E51N_PATCHED.zag'),
    'Research/R32_E51N_NATIVE/02_truth_fix.zagfrag',
    str(scratch / 'E51O_LOCAL_PATCHED.zag'),
    'Research/R32_E51P_NATIVE/01_local_experts.zagfrag',
    'Research/R32_E51S_NATIVE/01_extended_optimization.zagfrag',
    'Research/R32_E51V_NATIVE/01_trajectory_objective.zagfrag',
    str(scratch / 'E51V_RUN_PATCHED.zag'),
    str(scratch / 'E51X_01.zag'),
    str(scratch / 'E51X_02.zag'),
]
fragment = ''.join(Path(p).read_text() for p in parts)
(scratch / 'E51X_FRAGMENT.zag').write_text(fragment)

src = Path('Research/tnn_r32_e50_provenance_temporal_contention_discriminator.zag').read_text()
assert src.count('fn main()i32 {') == 1
src = src.replace('fn main()i32 {', fragment + '\n\nfn main()i32 {', 1)
anchor = 'let aux_frozen_gate:i32=0; if(aux_frozen_hash==frozen_aux_hash){ aux_frozen_gate=1; } e45_print_pair("e50_aux_frozen_gate",aux_frozen_gate);'
assert src.count(anchor) == 1
src = src.replace(anchor, anchor + '\n' + inj, 1)
(scratch / 'tnn_r32_e51x_extended_trajectory_dose.zag').write_text(src)
