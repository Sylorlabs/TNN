# NAMECHECK.md (DEBATE-SLATE, wave-20261001-2321pdt)

## Step 0: worker toolchain guard
- Ran: sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
- Output: safebin linked 36 tools; znc OK; python3 absent from safebin PATH (OK); SAFEBIN-READY
- PATH exported to /home/hatch/safebin
- `which python3` -> no output, exit code 1. VERIFIED: no python3 on PATH.
- Lane type: documentation only. No experiments, no Python, no ZnC compilation needed. Shell for git/file ops.

## Step 1: reads (READ-ONLY inputs)
- DEBATE-PREP/DEBATE_BRIEF.md (full, 80KB)
- ARENA-SYNTH/ARENA_SYNTHESIS.md (full)
- OWNED-SYNTH/OWNED_SYNTHESIS.md (full)
- H5R2-SYNTH/H5R2_SYNTHESIS.md (full)
- CLUSTER-FINAL/CLUSTER_FINAL.md (full)
- Verified existence of H5R2-SKEPTIC3, ARENA-GEN, ARENA-GEN-VERIFY, RT-ARENA5, CONTLEARN-OWNED, CONTLEARN-OWNED2 lane dirs.

## Step 2: output
- DEBATE_SLATE.md: 8 adjudication questions (Q1-Q8), each with question,
  verdicts involved, key evidence, uphold vs overturn readings. No
  experiments run. No em-dashes (checked with check_no_dash.sh).
