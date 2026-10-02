# NAMECHECK: TNN3H6 (H6 prereg: writing only)

Lane: TNN3H6, wave-20261001-2021pdt. Task: write PREREG_H6.md (fresh prereg for H6, standing-bearing uncertainty objects) with mandatory substrate verification. No implementation, no computation, no binaries.

## Step 0: Worker toolchain guard (Micah's governance ruling, 2026-09-30)

- Safebin setup: ran `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh` at wave start. Result: SAFEBIN-READY, `/home/hatch/safebin`, 36 tools linked, znc OK, setup script self-verified python3 absent from safebin PATH.
- PATH during all work: `/home/hatch/safebin` (exported in every exec call; exec sessions do not persist env between calls, so each command re-exports).
- Toolchain verification: `export PATH="$HOME/safebin"; which python3` prints NOTHING (exit 1). `which python` prints NOTHING (exit 1). Guard satisfied.
- PURE ZAG observed trivially: this lane is WRITING ONLY. No implementation files written, no znc invocations, no computational research operations performed. The only shell use is git branch reads, file greps on source docs, and SHA-256 verification of the frozen build (read-only inspection).

## Step 1: Identity and scope

- Worker is a research worker for the TNN RSI loop wave wave-20261001-2021pdt, lane TNN3H6.
- Working copy: /home/hatch/workspace/tnn-rsi, branch tnn-native-lab (confirmed via git).
- Write ONLY inside docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H6/. New files only: NAMECHECK.md (this file), PREREG_H6.md. No implementation files. No commits (coordinator commits). Never push. No git reset --hard, no rebase.

## Step 2: Hypothesis grounding

- H6 read directly from docs/lab/rsi/runs/wave-20261001-1721pdt/TNN3/HYPOTHESES.md (section "H6. Standing-bearing uncertainty objects"): merge the UNCERT node with the evidence model so uncertainty carries support counts the learner updates on every related experience; the researcher's fixed bid() formula (edge-type counts, about 12 lines) is deleted; a guide's bid becomes the learner-maintained standing of its UNCERT node, updated by generic CONFIRM/CONTRADICT events the learner links; capability-source delta net negative (deletion only, zero lines added).
- Lane context this wave: H1 was KILLED by sealed evaluation (FABRICATION on dev evidence); H2/H3/H4 stopped at prereg by verification-first (all SUBSTRATE-ABSENT, same root cause: the frozen TNN-2 core has no learner-reachable construction path; H4 additionally found protected EXECUTE unreachable from ev_act). Lesson carried into this lane: PREREG_H6.md must verify its substrate (bid() existence, learner-reachable standing-update path on UNCERT nodes, guide-selection read sites) against the frozen tnn2.zag BEFORE freezing bars, or the prereg is VOID.
- Frozen substrate: docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag, expected SHA-256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd (hash verified by this worker with sha256sum on 2026-10-01; matches character for character).

## Step 3: Deliverables

- docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H6/NAMECHECK.md (this file)
- docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H6/PREREG_H6.md (NOT-FROZEN: substrate verification FAILED as SUBSTRATE-ABSENT; verification evidence recorded in section 2; no bars frozen, per the task's stop rule)
- Final report to parent: substrate verification result with key quoted evidence.

## Step 4: Documentation rule

- No em-dashes anywhere in lane documentation.
