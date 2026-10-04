# NAMECHECK.md - wave-20261001-1721pdt SENSORY lane

Worker: sensory lane research worker (depth 2/2), started 2026-10-01 17:24 PDT.
Lane dir (ALL output): docs/lab/rsi/runs/wave-20261001-1721pdt/SENSORY/
Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab, tip eb19a4f3c.
No git commits, no git push, .wave_lock untouched. No child subagents.

## Step 0: Toolchain guard activation (recorded before any other work)

Commands run:
```
bash ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
export PATH="$HOME/safebin"
which python3
which python
```
Outputs:
```
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
python3: NOT FOUND (exit 1, good)
python: NOT FOUND (exit 1, good)
/home/hatch/safebin/znc (znc resolves in safebin PATH)
```
Toolchain pinned: src/tools/toolchain/znc_linux_x86_64_abed8aa1,
sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
(matches the frozen toolchain hash from wave-20260924-1121pdt).
Effective PATH during all work: /home/hatch/safebin only.
python3/python do not resolve. Pure Zag only.

Forbidden set: python3, python, node, any compiler or interpreter outside
safebin. Shell, git (read-only + local file writes, no commits), znc, and
safebin coreutils only.

## Step 1: Lane records located (before any design work)

Prior image/audio candidates, E3 record, baselines, judging protocol:

- E3 film grain: REJECTED by Micah's eyes 2026-09-23 in blind A/B
  (visible staticyness, baseline preferred). Cited in
  docs/lab/rsi/runs/wave-20260924-1121pdt/preregs/PREREG_SENSE_BIGLEVER_1121.md
  and docs/lab/rsi/runs/wave-20260927-1721pdt/debate/DEBATE_1721.md:484.
  Standing consequence: no micro-grain tweaks; KB anti-grain bars honor it.
- G1 SUNSHAFTS (volumetric crepuscular shafts on r8c):
  v1 wave-20260924-1121pdt DISCARDED (prereg point-set geometry defective,
  VERDICT_G1.md); v2 wave-20260924-1421pdt DISCARDED (recalibrated gate
  overcorrected: KB2 ratio 1.0000, KB3 var 0.00, VERDICT_G1_V2.md).
  Status: STOOD-DOWN. Not revived here.
- Current image champion: R11 (round 11, hemisphere sky ambient T14),
  source docs/lab/imagination_discovery/img/r11_alien.zag, verdict
  docs/lab/imagination_discovery/img/ROUND11_VERDICT.md (2026-09-26):
  R11 takes the championship over R4. Dusk scene, SDF raymarched,
  analytic sky with flat-mix cirrus, crescent moon, soft-shadowed terrain.
- Queued-unjudged image lineage (never re-surfaced as fresh here):
  R9, C1, C2v3, S11-IMG, C12, S13, S14, whirlpool-planform (all
  QUEUED-UNJUDGED per DP-1 brief lineage). R9 = contact occlusion,
  sealed; not re-proposed.
- Audio: DP-1 doppler flyby sealed blind pair exists
  (wave-20260926-1421pdt/dp1/blind/, JUDGE_BRIEF_DP1.md), queue
  disposition HELD. V11 / Micah's audio round-4 work is his closed
  frontier, not loop scope. ST-1 audio DEAD on pristine evidence.
- Video: D-VID-1 STOOD-DOWN.
- Judging protocol: P18 sealed-blind protocol minted 2026-09-26
  (wave-20260926-1421pdt debate ruling). Micah is the judge; human eyes
  outrank metrics; pairs randomized; mapping sealed in a file the judge
  does not see. Nothing adopted on metrics alone.
- Sensory stand-down since 2026-09-26/27 (lane survey + debate):
  "no new big realism lever in loop-owned scope". This wave breaks the
  stand-down ONLY with a genuinely new mechanism, preregistered with
  frozen realism kill bars before implementation.

## Step 2: Forbidden-executable audit (updated at wave end)

AUDITED at wave end. Forbidden set: python3, python, node, any compiler
or interpreter outside safebin. Verdict: CLEAN.

- Every computational step ran through znc
  (src/tools/toolchain/znc_linux_x86_64_abed8aa1) or safebin coreutils
  (bash, cp, diff, sed, sha256sum, stat, mkdir, tee, grep, head, tail).
- `which python3` / `which python` return nothing under the effective
  PATH (/home/hatch/safebin) for the entire wave; verified at Step 0
  and never re-added.
- No python, node, gcc, or other interpreter/compiler was invoked in
  any exec call this wave. The two pre-guard `git` invocations
  (status/log, read-only) used git, which is inside the safebin tool
  set, not a forbidden executable.
- New Zag sources compiled: r11_baseline.zag, h1_clouds.zag,
  h1_verify.zag, tools/bmp2png.zag. All pure Zag, zero RNG.
- znc quirk honored: no `as *i32` + slice construction anywhere;
  u8 buffers with explicit LE/BE pack/unpack helpers only.

## Step 0b: Toolchain guard re-activation (completion worker, 2026-10-01 17:33 PDT)

Re-ran setup_safebin.sh; exported PATH="$HOME/safebin"; `which python3`
returns nothing (exit 1); `which python` returns nothing (exit 1);
znc resolves to /home/hatch/safebin/znc; toolchain sha256 verified
498abcb5ab346f8c... matches frozen hash. All work this session under
safebin PATH only. Pure Zag only.

## Step 2: Forbidden-executable audit (completion worker, wave end)

Zero invocations of python3, python, node, or any interpreter/compiler
outside safebin. All work ran under PATH=/home/hatch/safebin (36 tools,
no python). Generators, verifier, BMP-to-PNG converter, and analysis
are pure Zag compiled with the pinned toolchain
(sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef).
Shell and safebin coreutils only for orchestration. No PROCESS-FAIL.

## Completion notes

- Prior worker's artifacts adopted after audit: bin/r11_baseline (one-line
  diff verified against in-tree r11_alien.zag), bin/bmp2png (pure-Zag
  stored-deflate BMP to PNG, from h1/tools/bmp2png.zag), h1_verify.zag
  (world-model functions byte-identical to baseline by md5; bar thresholds
  match the frozen prereg). The prior worker's shell children were still
  alive at handoff (baseline 1024 renders into out/base1, out/base2);
  their renders were adopted as the baseline gate evidence, not re-run.
- A file race occurred at 00:39 UTC: the lingering prior worker overwrote
  h1_verify.zag while this worker's own verifier draft was being written;
  the prior worker's version was audited and adopted instead. No evidence
  was fabricated; all numbers come from the audited binary.
- H1 verdict: DISCARDED on frozen KB3-LIGHTLOGIC (see
  VERDICT_H1_DISCARDED.md). Not queued. blind/ left empty.
