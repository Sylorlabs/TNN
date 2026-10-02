# BUILD-LOG.md - DEVANG6

## Step 0 (76361ff85)
safebin_setup run; PATH="$HOME/safebin"; which python3 -> nothing;
which znc -> /home/hatch/safebin/znc. Guard active.

## Prereg (bda385c32, ALONE)
RECALIBRATION_K_ABL.md: derived corrected K_ABL (gap >= 4) from DEVANG5
leg-1 data; four honesty arguments; anti-fit margin (4 vs observed 6).
PREREG_DEVANG6.md: frozen mechanism spec (FINREG/POSSEG carried forward),
fresh families (B-tripleprime seed 888021, C-tripleprime seed 888022,
E-prime 6 frozen lines), old-language impossibility proof, K_SAME bar,
all kill bars. No implementation predates this commit.

## E-prime baseline (c72b40a54)
Frozen devang4 binary (sha256
cfba24f157a22b0e721f9a27722320f6b2d3a77e250b96c9045659b58bb9ddbd),
segb-scene, 3/3 byte-identical (sha 50c16fe0...), 2/6 (E2p, E6p).
Premise <= 2/6 HOLDS.

## Implementation (f541f16e3)
devang6.zag: diff vs devang5.zag = exactly 2 comment lines (banner).
Compiled with pinned znc, exit 0. Binary sha256
a11bd3506987a83ee2f502a78e9af686e92b6cf53ff89d4b950e5dbb3d1e03df:
byte-identical to frozen DEVANG5 binary. fama output byte-identical to
devang5's committed dev_fama.log. Family A dev: K1 10/10; K2..K7,K9 7/7;
test 20/20; C0 13/20 (K1 3/10); C1 4/20, C2 17/20, C3 0/20; K8 exactly
15pp; K_C0 35pp/7 words; abl K1 8/10 (gap 2).

## Sealed package (1e852dbb2, before any sealed run)
genseal6.zag + binary; sealed6/ (B-tripleprime, C-tripleprime, SHA256SUMS:
b6 db1b02c7..., b6_key 964b71a3..., c6 d30ef174...); scoree + floorcheck;
E-prime key. Sealed contents never read (line counts/sizes only).
Altered-seed validation (888031/888032, /tmp, discarded): format OK,
spec-compliance OK, fairness floor 8/12 OK, solvability 12/12 OK,
sealc-fresh 11/20 clean.

## Sealed battery (3/3 byte-identical each, zero stderr)
- K_SEG learner (B-tripleprime): 12/12.
- Ablation (segb-abl): 5/12. Gap 7 >= 4. K_ABL leg 1 PASS.
- E-prime learner: 6/6. K_DISC PASS.
- C-tripleprime: learner 9/20; c0 5/20, c2 11/20, c1 7/20, c3 7/20.
  K_SEAL FAIL (9 < 12).
- floorcheck: initially 12/12 (miscompile artifact); corrected to 7/12
  after De Morgan fix (>= 4 floor satisfied).

## Incident: floorcheck miscompile
`while(... && !(A && B))` miscompiled in pinned znc (fourth defect).
Isolated repros; De Morgan fix; verified on synthetic (2/12 correct);
re-measured sealed floor 7/12. Pattern grep-absent from sealed pipeline.
Documented in ~/AGENTS.md.

## Eval / red team / debate / verdict (this commit)
SEALED_EVAL.md, REDTEAM_SELF.md (6 attacks, all fail), DEBATE.md
(advocate/skeptic/judge; provenance probe: nothing mechanistic new),
VERDICT.md (BUILD-FAIL, K_SEAL, mechanism-result classification),
REPORT.md, BUILD-LOG.md. Commit-order self-check PASS.
