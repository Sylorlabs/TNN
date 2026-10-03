# NAMECHECK.md - lane F2, wave-20261002-1121pdt

Task: queue item 10. F2 v6: 3x SEALED EVALUATION on the wave-3 11-action
planning gap (K6-R4 unmeasured last wave under CPU contention).
Measure K6-R4 under clean CPU conditions. Pure Zag. Red team the result.

## Step 0: toolchain guard (2026-09-30 governance)

Executed at startup:
`bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
Output tail: "linked: 36 tools", "znc: OK
(/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)",
"verify: python3 absent from safebin PATH (OK)",
"verify: python absent from safebin PATH (OK)",
"SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)".

PATH exported to $HOME/safebin before all Zag work.

Literal guard evidence (export PATH="$HOME/safebin"):

- `which python3` resolves to NOTHING (empty output)
- `which python` resolves to NOTHING (empty output)
- `which znc` -> /home/hatch/safebin/znc

Guard status: PASS. No forbidden interpreter is reachable. Pure Zag for
all builds, runs, and analysis below.

## Provenance (inherited, read-only)

- Frozen prereg: docs/lab/rsi/runs/wave-20261002-0521pdt/F2/PREREG_F2V6.md
  (frozen 2026-10-02, amended once for NC5). This lane does NOT author a
  new prereg and does NOT modify the sealed worlds. The sealed eval is a
  re-run of the frozen 0521pdt eval that went PARTIAL under CPU
  contention.
- Implementation: docs/lab/rsi/runs/wave-20261002-0521pdt/F2/f2v6_learner.zag
  (206 changed lines vs v5 base, commit 50693d022 on prior wave).
- Prior sealed eval record: docs/lab/rsi/runs/wave-20261002-0521pdt/F2/SEALED_EVAL.md
  (PARTIAL verdict: mechanism validated, negative controls PASS,
  regression PASS, K6-R4 UNMEASURED).
- The 0521pdt F2 files are committed on the parent branch; this lane
  copies them into its own run dir for byte-identical rebuild and does
  not edit them.

## Seal discipline

Before any run: the three sealed world files are verified against the
sha256 hashes recorded in PREREG_F2V6.md section 5 at prereg freeze.
Hash match required; any mismatch voids the sealed run. Worlds are
never modified by this lane.

- sealed/f2v6_world_shift2.zag: 05e26e0854427b07fa3b0971f46d22cdec368f9d84bad1b6a057d05f730ca054
- sealed/f2v6_world_shift1.zag: c0986c12fd3ad22366b37eb943927c1df7ba482557b18a75ccbae5f075dc6f5c
- sealed/f2v6_world_osc.zag: 2fb92115015f385649fbab78f40fcc8b815d9c3db725d2ad4b7db005f74a0470

Kill bars applied: K6-R1..R8 as frozen in PREREG_F2V6.md section 8.
Negative controls NC1..NC5 as frozen in section 9 (NC5 per the
2026-10-02 amendment). No bar is weakened or moved.
