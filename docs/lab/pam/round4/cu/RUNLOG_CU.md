# RUNLOG — CU: Conscious vs Unconscious PAM Tradeoff

**Preregs:** `prereg/PREREG_CU.md` (frozen `0f79f90d`, Correction C1 pre-build,
Correction C2 `ec3d1c91` pre-verdict + P-row id fix) and
`prereg/PREREG_CU_ADDENDUM_FABLE.md` (frozen `af5907cf`, pre-build).
**Branch:** `tnn-native-lab` (sylorlabs/TNN).

## Frozen sources (verified at read by gen_cu.py)

| source | sha256 |
|---|---|
| `~/workspace/pam_round2/o1_delivery/sweep.jsonl` | `4163fffa…f0833f2` |
| `~/workspace/pam_round2/d1_stack/rec_install.records` | `c26ac974…17c4ad` |
| `~/workspace/pam_round2/cc1_guard/prereg/gen_guard.py` | `49eef7b1…2ae2c214b` |

## Tape

`gen_cu.py` → `cu_tape.txt`: 1,232 rows (C=1102, W=12, P=18, A=100:
LAU=40, FORK=30, AUTH=30), bar-passing C = 910 (matches M1's 910/1102),
sha256 `0939bbd2b8cbadc387fdc3b0d8f7cec338d96f96063bd5da7bce79194b502e14`.
`cu_questions.txt`: 20 primary + 5 diagnostic,
sha256 `c89d6acc55087fb932dddbc3cb1e27336f7276699d82047583614c97688e9e83`.
Attack rows verified well-formed (bar-passing axes; exactly one corrupted
security field each).

Coincidence note: the pre-Correction-C1 tape and the corrected tape have
the SAME sha256 — verified by content check, not assumed: the first 100
bar-passing C rows under the corrected bar all happen to have
strong=agree=1, so attack rows and questions are byte-identical.

## Build

Toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(`--no-zagd`; the zagd daemon aborted one invocation, `--no-zagd` clean).
`cu_pam.zag` + `cu_query.zag` + byte-identical `R33_NATIVE_IO_V1.zag`
(sha `e6379ddb…f61d8`, same as M1 crew's). Warnings only (benign, same
class as M1): A0101 off-by-one advisory in `field` (guarded by `i < llen`),
A0102 discarded `nio_close`. Binaries → `build/` (NOT committed).

## Battery (all ≥2×, byte-identical per DIGESTS.txt)

```
./build/cu_pam c cu_tape.txt > evidence/c_runN.txt    (N=1,2)
./build/cu_pam u cu_tape.txt > evidence/u_runN.txt    (N=1,2)
./build/cu_query evidence/c_run1.txt cu_questions.txt > evidence/qc_runN.txt
./build/cu_query evidence/u_run1.txt cu_questions.txt > evidence/qu_runN.txt
```

Wall-clock observations (corroboration only; wall time is not deterministic
and is NOT a bar input — `real` is dominated by process startup, `user`
is the signal):

| run | real | user |
|---|---|---|
| c_run1 | 4.021 s | 0.177 s |
| c_run2 | 3.566 s | 0.181 s |
| u_run1 | 0.703 s | 0.069 s |
| u_run2 | 0.677 s | 0.073 s |
| qc_run1 | 0.690 s | 0.049 s |

User-time ratio conscious/unconscious ≈ 2.5×, directionally consistent with
the 7.9× deterministic cycle ratio (the cycle model charges 1/emitted byte;
byte emission is memcpy-cheap in wall time).

## Scorer

`score_cu.py` independently recomputes everything from tape + evidence:
stateless Python mirror of §2 verified against all 1,232 OUT lines (both
variants) and all 1,232 REC lines (0 mismatches); K8 deltas; all five
metrics; introspection quality vs REC ground truth; AUDIT-1 via the frozen
C3 `run_gate` mirror (aggregate asserted 791/1102 before use).
