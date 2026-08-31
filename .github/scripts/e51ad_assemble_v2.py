from pathlib import Path

root = Path('.')
out_dir = root / '.scratch' / 'e51ad'
out_dir.mkdir(parents=True, exist_ok=True)

base_path = root / '.scratch' / 'e51ac' / 'tnn_r32_e51ac_additive_direct_candidate_hybrid.zag'
base = base_path.read_text()
parts = [
    root / 'Research' / 'R32_E51AD_NATIVE' / '01_router_helpers.zagfrag',
    root / 'Research' / 'R32_E51AD_NATIVE' / '02_run_and_gates.zagfrag',
]
fragment = '\n\n'.join(p.read_text().rstrip() for p in parts) + '\n'
injection = (root / 'Research' / 'R32_E51AD_NATIVE' / '04_main_injection.zagfrag').read_text()
old_injection = (root / 'Research' / 'R32_E51AC_NATIVE' / '03_main_injection.zagfrag').read_text()

marker = 'fn e51y_run(\n'
assert base.count(marker) == 1, base.count(marker)
assert base.count(old_injection) == 1, base.count(old_injection)
assembled = base.replace(marker, fragment + '\n' + marker, 1)
assembled = assembled.replace(old_injection, injection, 1)

(out_dir / 'E51AD_FRAGMENT.zag').write_text(fragment)
(out_dir / 'tnn_r32_e51ad_trajectory_critical_hybrid_router.zag').write_text(assembled)
core = root / '.scratch' / 'e51ac' / 'tnn_r32_e45_investigation_core.zag'
(out_dir / 'tnn_r32_e45_investigation_core.zag').write_text(core.read_text())
