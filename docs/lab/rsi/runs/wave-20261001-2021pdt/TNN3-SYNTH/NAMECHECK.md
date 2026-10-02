# NAMECHECK TNN3-SYNTH (architectural synthesis, writing only)

Lane: TNN3-SYNTH. Wave: wave-20261001-2021pdt. Worker role: drafting
architectural synthesis only.

## Step 0. Toolchain verification (Worker Toolchain Guard)

1. Ran `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
   from /home/hatch/workspace/tnn-rsi.
   Output: SAFEBIN-READY: /home/hatch/safebin (36 tools, no python). znc OK.
2. `export PATH="$HOME/safebin"`.
3. `which python3` prints NOTHING (exit 1). Confirmed absent from safebin PATH.
4. This task is WRITING ONLY: no implementation files, no binaries, no
   compilation, no computation, no forbidden executables invoked. Only two
   new files in the lane directory: NAMECHECK.md and SYNTHESIS.md.

## Scope of this lane

- Working copy: /home/hatch/workspace/tnn-rsi, branch tnn-native-lab.
- Write ONLY inside docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3-SYNTH/.
- No git operations (coordinator commits). No push.
- Documentation rule: no em-dashes anywhere.

## Step 1. Context read (before drafting)

Read, in full, before writing the synthesis:
- docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H2/PREREG_H2.md (SUBSTRATE-ABSENT)
- docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H3/PREREG_H3.md (SUBSTRATE-ALREADY-UNIFIED + SUBSTRATE-ABSENT)
- docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H4/PREREG_H4.md (SUBSTRATE-ABSENT)
- docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H6/PREREG_H6.md (SUBSTRATE-ABSENT)
- docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H7/PREREG_H7.md (SUBSTRATE-ABSENT)
- docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H1/REDTEAM_FABRICATION.md (presentation-level FABRICATION)
- docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H5/REDTEAM_REVIEW.md (dissent, H5 killed this wave)
- docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H5/SHADOW_DIAGNOSIS.md (MAP-key failure root cause)
- docs/lab/rsi/runs/wave-20261001-2021pdt/CONTLEARN/VERDICT_CONTLEARN.md (qualified integration verdict)
- docs/lab/rsi/runs/wave-20261001-2021pdt/CONTLEARN/REDTEAM_REVIEW.md (learner contribution is zero)
- docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H5R/NAMECHECK.md (H5 re-prereg in progress)

## Step 2. Draft SYNTHESIS.md

Drafts the architectural synthesis per the task specification: central
finding, why the net-negative program dissolved, the positive implication
(requires additions), relation to CONTLEARN and H5, the revised TNN-3
research direction, and the skeptic's attack with answer.
