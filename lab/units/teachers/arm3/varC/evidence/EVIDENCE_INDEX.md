# Evidence index — arm-3 variation C

Generated 2026-09-21 by `verify/run_verify.py` (full log: `battery.log`).
All histories are decision tapes per SPEC.md §1; `*.trace` files are the
teacher's own `trace`-mode E output for that tape.

## Scripted sessions

| file | decisions | what it exercises |
|---|---|---|
| `sessions/A.hist` | ADOPT×5, REJECT:1, ADOPT×6 | warm-up, warm appeal with new grounding, hot relational |
| `sessions/B.hist` | ADOPT, DEFER×2, REJECT:1×2, ADOPT | double-reject → RETRACT of un-decided proposal |
| `sessions/C.hist` | ADOPT×5, REJECT:1×6 | appeal budget, dead-span rule, degraded retract, cold collapse |
| `sessions/D.hist` | ADOPT×70 (capped at 64) | session cap (exit 20), sustained hot relational |
| `sessions/E.hist` | ADOPT×6, REJECT:2, ADOPT×3 (code slice S4) | R2 appeal on the code domain |
| `sessions/adopt14.hist` | ADOPT×14 | history-sensitivity: hot arm |
| `sessions/reject12.hist` | REJECT:1×12 | history-sensitivity: cold arm |

## Key traces (E per proposal emission)

all-ADOPT (`adopt14`): `0,120,220,320,420,520,620,720,820,920,1000,1000,1000,1000`
→ hot from proposal 8; relational kinds 2/3/4; confidence up to 220.

all-REJECT (`reject12`): `0,0,0,0,0,0,0,0,0,0,0,0`
→ E pinned at 0; WORD_SPAN cold probes only; confidence 60–100.

## Battery results (`battery.log`)

- N=5 byte-identical: PASS
- 8/8 heap-perturbation byte-identical (`MALLOC_PERTURB_` 0/1/165/90/213 plus
  4KB/16KB/64KB environment-block perturbations): PASS
- selfcheck (recorded == recomputed) on A, B, adopt14, reject12: PASS
- E recompute vs independent Python reference (24/12/28/24 events): PASS
- history sensitivity (4 checks): PASS
- §P iron-rule battery (19 hostile histories → exact exits 1,2,3,4,5,6,8,9,10; forged proposal → 21): PASS
- §C: clean teaching no-fire, smuggle tiling fires code 1, vocab dump fires code 2 immediately, no-255 stream no-fire: PASS

Reproduce: `python3 verify/run_verify.py` from `varC/` (needs `teacher_bin`
built via the znc command in the build note below).

Build: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 teacher.zag --no-zagd --no-analyze --no-foreground-cache -o teacher_bin`
