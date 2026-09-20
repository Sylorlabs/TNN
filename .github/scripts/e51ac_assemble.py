# 2026-09-20 path migration: pre-reorg Research/ paths remapped to post-reorg
# locations (docs/generations/R32/..., src/tools/toolchain/...). All content
# moves verified byte-identical via git blob hashes. Historical R32 tooling.
from pathlib import Path

src_path = Path('.scratch/e51y/tnn_r32_e51y_five_way_sequential.zag')
assert src_path.exists()
src = src_path.read_text()
helper = ''.join(Path(p).read_text() for p in (
    'docs/generations/R32/runs/R32_E51AB_NATIVE/01_direct_candidate_actions.zagfrag',
    'docs/generations/R32/runs/R32_E51AC_NATIVE/01_hybrid_direct_candidate.zagfrag',
    'docs/generations/R32/runs/R32_E51AC_NATIVE/02_run_and_gates.zagfrag',
))
injection = Path('docs/generations/R32/runs/R32_E51AC_NATIVE/03_main_injection.zagfrag').read_text()
marker = 'fn e51y_run(\n'
assert src.count(marker) == 1
src = src.replace(marker, helper + '\n\n' + marker, 1)
anchor = '    // ---- Fresh stage-84 continuation training under the frozen terminal learner.\n'
assert src.count(anchor) == 1
src = src.replace(anchor, injection + '\n' + anchor, 1)
scratch = Path('.scratch/e51ac')
scratch.mkdir(parents=True, exist_ok=True)
(scratch / 'E51AC_FRAGMENT.zag').write_text(helper)
(scratch / 'tnn_r32_e51ac_additive_direct_candidate_hybrid.zag').write_text(src)
core = Path('docs/generations/R32/tnn_r32_e45_investigation_core.zag')
(scratch / 'tnn_r32_e45_investigation_core.zag').write_bytes(core.read_bytes())
