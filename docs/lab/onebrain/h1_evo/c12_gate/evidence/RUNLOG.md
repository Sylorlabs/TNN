# C12 run log — 2026-09-24 (PDT)

Work dir: `~/workspace/h1evo/c12_gate/`. Toolchain:
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

## Build

```
cd ~/workspace/h1evo/c12_gate
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 c12.zag -o c12_bin
```
Warnings only (A0102 ignored-return-value, same class as the prior obc harness).
Binary SHA-256: `89b6a5beb57d83ee60ce780722e1c14013692b34c0331c9b394127a880c180e1`.

Two defects were found and fixed during bring-up (both fixture bugs, not bar
changes):
1. C1 mode 3 (deliberate-pin probe): with both candidates pinned, the real
   `f3_survivor(2,1,2,0)` selects H_false, so the deliberate pin landed on a
   non-selected candidate and the rules could not separate. Mode 3's false
   premise now installs via M_PROPOSE (no auto-pin); H_true is selected and
   the rules separate: rule-A refuses, rule-B promotes on the deliberate pin.
2. C1 LH: the gate inherited the original C1 gate's pin-budget refusal
   (reason 8). Under sustained M_COMMIT auto-pinning the frozen organ budget
   (MM_MAX_PIN=16) saturates at episode 7 and the gate refused everything,
   including legitimate promotions. The budget check was removed from the
   promotion gate (organ still enforces pin allocation itself; promotion rests
   on corroboration). Documented in c12.zag at the removal site.

## Determinism battery (3x byte-identical)

```
for m in c1a c1b c2a c2b c2c lh1a10 lh1a100 lh1b10 lh1b100 \
         lh2a10 lh2a100 lh2b10 lh2b100 lh2c10 lh2c100; do
  for r in 1 2 3; do ./c12_bin $m > evidence/stdout/${m}_run${r}.txt; done
done
```
Result: all 15 modes byte-identical across all 3 runs.
`evidence/sha256sums.txt` holds the run-1 SHAs (see SRC_SHA.md for harness SHA).

## Zero-RNG static check

`grep -n -i "rng|rand|seed" c12.zag` → one hit only: the header comment
"Pure Zag. Zero RNG." No RNG in code or comments otherwise. The untouched
real sources contain one "seed" comment (ob_mem.zag:79, "CORE seed" memory
slot label — not randomness).

## ZD regression (untouched copied sources)

```
mkdir -p evidence/zd
cp ~/workspace/ob2_repairatk/vb/ob_test_{mem,pam,arbiter,fl2}.zag evidence/zd/
cp src/ob_{arbiter,common,fl2,mem,pam,tn}.zag evidence/zd/
# SHA-verify the six sources vs src_ref (all OK, see SRC_SHA.md)
znc ob_test_mem.zag -o ob_test_mem_bin  && ./ob_test_mem_bin  > ob_test_mem.out
znc ob_test_pam.zag -o ob_test_pam_bin  && ./ob_test_pam_bin  > ob_test_pam.out
znc ob_test_arbiter.zag -o ob_test_arbiter_bin && ./ob_test_arbiter_bin > ob_test_arbiter.out
znc ob_test_fl2.zag -o ob_test_fl2_bin   && ./ob_test_fl2_bin  > ob_test_fl2.out
```

| battery | rc | OB_FAILURES | deterministic (2x SHA) |
|---|---|---|---|
| ob_test_mem | 0 | 0 | yes (983eca4d6058) |
| ob_test_pam | 0 | 0 | yes (7c0a819aa39a) |
| ob_test_arbiter | 0 | 0 | yes (de3506648751) |
| ob_test_fl2 | 0 | 0 | yes (f078ba64935d) |

ZD verdict: no regression in the real organs — the C12 fixture touches none
of them (fixture-only provenance records and the H3 fixture live in c12.zag).

## Verdicts (all from run-1 stdout; reruns byte-identical)

| mode | verdict |
|---|---|
| c1a (rule A battery) | SURVIVE — C1a' refused, C1b' promoted via genuine corroboration, pin never deciding |
| c1b (rule B battery) | SURVIVE — C1a' refused, C1b' promoted via genuine corroboration, pin never deciding |
| c2a (carryover) | SURVIVE — C2a' resolved ep 2 (round 1), C2b' controls match baseline |
| c2b (escalation budget) | SURVIVE — C2a' resolved ep 3 (round 3, quarantine pending review), C2b' controls match baseline |
| c2c (rising discount) | SURVIVE — C2a' resolved ep 2 (round 2), C2b' controls match baseline |
| lh1a10 / lh1a100 | SURVIVE — 10/10 and 100/100 false refused, true promoted, pin never deciding |
| lh1b10 / lh1b100 | SURVIVE — 10/10 and 100/100 false refused, true promoted, pin never deciding |
| lh2a10 / lh2a100 | SURVIVE — X resolved ep 1, 0 false quarantines |
| lh2b10 / lh2b100 | SURVIVE — X resolved ep 8, 0 false quarantines |
| lh2c10 / lh2c100 | SURVIVE — X resolved ep 4, 0 false quarantines |

C2a' resolution detail (frozen 12-episode consecutive dribble):
- (a) carryover: 1 escalation → quarantine ep 2, round 1. 1 action-driving episode.
- (b) escalation budget: 2 escalations → DLA_QREVIEW ep 3, round 3 (quarantine pending review). 2 action-driving episodes.
- (c) rising discount: 1 escalation → quarantine ep 2, round 2. 1 action-driving episode.

Rule separation (mode 3, deliberate pin, no independent corroboration):
- rule-A: refuse (pinprov=2 DELIBERATE, pinmass=0).
- rule-B: promote (pinmass=1, pin deciding — by the hypothesis design).
