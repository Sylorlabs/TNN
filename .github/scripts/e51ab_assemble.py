# 2026-09-20 path migration: pre-reorg Research/ paths remapped to post-reorg
# locations (docs/generations/R32/..., src/tools/toolchain/...). All content
# moves verified byte-identical via git blob hashes. Historical R32 tooling.
from pathlib import Path

# Reuse the validated E51Y/E51X terminal reconstruction. Inject the direct
# candidate action discriminator and return before the falsified E51Y CONTINUE
# learner is trained.
src_path = Path('.scratch/e51y/tnn_r32_e51y_five_way_sequential.zag')
assert src_path.exists(), src_path
src = src_path.read_text()
helper = ''.join(Path(p).read_text() for p in [
    'docs/generations/R32/runs/R32_E51AB_NATIVE/01_direct_candidate_actions.zagfrag',
    'docs/generations/R32/runs/R32_E51AB_NATIVE/02_run_and_gates.zagfrag',
])
injection = Path('docs/generations/R32/runs/R32_E51AB_NATIVE/03_main_injection.zagfrag').read_text()

run_marker = 'fn e51y_run(\n'
assert src.count(run_marker) == 1, src.count(run_marker)
src = src.replace(run_marker, helper + '\n\n' + run_marker, 1)

anchor = '    // ---- Fresh stage-84 continuation training under the frozen terminal learner.\n'
assert src.count(anchor) == 1, src.count(anchor)
src = src.replace(anchor, injection + '\n' + anchor, 1)

scratch = Path('.scratch/e51ab')
scratch.mkdir(parents=True, exist_ok=True)
(scratch / 'E51AB_FRAGMENT.zag').write_text(helper)
(scratch / 'tnn_r32_e51ab_direct_candidate_actions.zag').write_text(src)
core = Path('docs/generations/R32/tnn_r32_e45_investigation_core.zag')
(scratch / 'tnn_r32_e45_investigation_core.zag').write_bytes(core.read_bytes())
