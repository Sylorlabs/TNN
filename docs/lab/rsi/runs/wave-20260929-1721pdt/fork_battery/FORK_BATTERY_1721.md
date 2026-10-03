# FORK_BATTERY_1721.md

Wave: wave-20260929-1721pdt. Verdict: CONFIRM [NEW] as a process confirmation
(toolchain and extraction stability only).

Execution: full fresh run pinned to run-start commit
7c11ac5af742085f3d81355fab3863b204d32d6a, driver batch_1721.sh (faithful
frozen driver derived from batch_1421.sh by mechanical edit; pure shell, git,
sha256sum; zero Python), run_one.sh byte-identical to the frozen run_one.sh
(sha256 4c2fadfc104548fb9c8a13c417e90d96991637030734851dd6ca4471a037e978),
harness binary sha256 a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66
re-verified byte-identical to the frozen instrument (re-verified, not
rebuilt from source this wave). Scratch: ~/workspace/fb1721pdt/E/ (73
entry dirs). Driver log: ~/workspace/fb1721pdt/batch_1721.log, driver exit 0.

Tally: 73 entries, 71 PASS, 0 FAIL, 2 UNTESTABLE (rh-pull-1-head,
rh-pull-2-head, the known non-TNN research-doc trees; expected).
Uniform on all 71 tested: znc pin 498abcb5 (0 pin divergence); probe sha
3b29aa06; b1/b2/b3 PASS, b1_cmp/b2_bin_cmp PASS; NEG1 E0002 hit 71/71;
NEG2 char-1 discrimination 71/71; probe_run_stdout R32_ZNC_PROBE_OK
71/71; harness_verdict_pass_count 1 on 71/71.
LIVE entries (2): arch-wave-20260929-1421pdt at
347260cee11ef96ad6e1a832bc994d53fbccc4d2 (newly enumerated archive),
local-tnn-native-lab at 7c11ac5af (run-start tip, this wave's
prereg-freeze commit; docs-only, inert for toolchain extraction).
Duplicate-SHA group named: {arch-wave-20260929-1121pdt, local-1421pdt-tip}
both at d18f7f68d3792c58346861b89eab374c2e728ef0.
Remote: zero new refs (origin/tnn-native-lab bedf8b4a, HEAD 27a4271f, all
pins unchanged; read-only git ls-remote at wave start).

One disclosed red-line touch during driver derivation: python3 was invoked
as a no-op heredoc fallback while building the sed derivation command. It
printed a string and performed no edit and no loop work; the mechanical
derivation was done entirely by sed, and the driver diff against
batch_1421.sh shows only the 4 intended rotation changes. Recorded in the
wave record and debated (M5). No wave artifact was produced or modified by
Python.

No em-dashes in wave documentation.
