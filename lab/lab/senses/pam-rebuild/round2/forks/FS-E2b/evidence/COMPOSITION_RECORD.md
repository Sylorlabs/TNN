# FS-E2b Composition Record

2026-09-24. Composition of the FS-E2b formation layer and the FS-E1b
fidelity support driver. All checks below ran BEFORE the prereg commit.

## 1. Formation composition (src/fse2b_form.zag)

Base: `round2/forks/FS-E2/src/fs2_form.zag` (FS-E2 Phase 0 formation).
Replaced only the three improved task functions from the earn-back crews:
- `f_shapetrans` ← `round2/forks/FS-F2S/src/fsf2s_form.zag`
- `f_colorconst` (+ helper `f_colorconst_d`) ← `round2/forks/FS-F2C/src/f2c_form.zag`
- `f_linlut` ← `round2/forks/FS-F2C/src/lut_frag.zag` (generated lookup table)
- `f_timbredisc` (+ helpers `f_tbcoeff2`, `f_tbharm`) ← `round2/forks/FS-F2T/src/f2t_form.zag`
- removed (superseded by F2T helpers): `f_tbcoeff`, `f_tbpower`

Verification (programmatic, fn-code through each fn's closing brace):
- the three improved functions + all added helpers are BYTE-IDENTICAL to
  their crew sources;
- exactly `f_shapetrans`, `f_colorconst`, `f_timbredisc` differ vs FS-E2;
- all other FS-E2 function code byte-identical; no other additions/removals.

No-regression / formation spot checks (composed binary, built with the pinned
toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`):
| task | n | expected | composed | verdict |
|---|---|---|---|---|
| shapetrans | 1296 | 1296/1296 | 1296/1296 | PASS |
| colorconst | 1200 | 1183/1200 | 1183/1200 | PASS |
| timbredisc | 1000 | 1000/1000 | 1000/1000 | PASS |
| colordisc | 1080 | 1004/1080 | 1004/1080 | PASS |
| pitchdisc | 720 | 705/720 | 705/720 | PASS |
| motiondir | 564 | 545/564 | 545/564 | PASS |

(One transient rc=-1 during checks was the FS-F2S crew's relative-path fresh
list run from /tmp; rerun with resolved paths passed 1296/1296.)

## 2. Support driver (src/fse2b_sup.zag)

FS-E1b's frozen challenge/support registry, byte-verbatim. 26 functions
copied from `round2/forks/FS-E1b/src/fse1b.zag` (fn-code byte-identity,
verified programmatically, 26/26):
`t_get16`, `t_get32`, `t_get64`, `t_geti16`, `t_put32`, `t_put64`,
`op_add`, `op_zero`, `i64s`, `jname`, `task_name`, `reg_challenge`,
`cd_chal`, `cc_chal`, `sh_chal`, `pt_chal`, `pt_freq`,
`tb_chal`, `tb_coeff`, `tb_goertzel`,
`mo_chal`, `mot_quant`, `mot_vote_gated`,
`run_challenge`, `chal_supports`, `read_file`.
New code: only the `x_*` harness (claim TSV input, disp emission) and `main`.
Only the IO module is imported; no SHA (hash chains are assembled by the
deterministic Python glue).

Fidelity proof (pre-eval precondition), 2026-09-24:
- frozen binary `forks/FS-E1b/build/fse1b` SHA-256 verified:
  `ef5bb2dc0df14216008e14d2204b493041d454334460427b186280acade6bb24`
- the frozen binary's own claims on the full R2-16 battery (12,000
  fixtures) were fed to `fse2b_sup`;
- disp agreement: 10000/10000 (adv) + 2000/2000 (ctrl) = 100%;
- outcome agreement: 10000/10000 (adv) + 2000/2000 (ctrl) = 100%.
Gate decisions in FS-E2b are the frozen registry, proven faithful.

## 3. Build
- Toolchain (pinned): `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- `znc fse2b_form.zag -o fse2b_form` — builds clean (analyzer lints are
  inherited FS-E2 warnings, not failures).
- `znc fse2b_sup.zag -o fse2b_sup` — builds clean.
- Binaries are LOCAL build artifacts only; never committed.

## 4. Input/claim protocol (frozen)
- `fse2b_form batch <list>` → TSV `<path>\ttask=<name>\tjudgment=<JNAME>`.
- Claim TSV: `<path>\t<claim_id>`; claim id == the task's judgment index
  (`jname` table: t0 {SAME:0,DIFFERENT:1}; t1 {SAME_SURFACE:0,DIFFERENT:1};
  t2 {CIRCLE:0,TRIANGLE:1,SQUARE:2}; t3 {SAME:0,HIGHER:1,LOWER:2};
  t4 {PURE:0,BRIGHT:1,DARK:2,RICH:3};
  t5 {STILL:0,N:1,NE:2,E:3,SE:4,S:5,SW:6,W:7,NW:8}).
- The eval driver asserts the extractor's echoed judgment equals the
  formation TSV's judgment on every fixture (validates the name→id map
  both ways).
