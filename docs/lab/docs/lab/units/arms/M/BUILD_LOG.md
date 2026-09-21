# ARM M — Build Log

## Source
- `units/arms/M/cl/arm.zag` — single Zag source, one binary with argv dispatch.
- Compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Build: `znc cl/arm.zag -o .work/m_bin_final3`
- Final binary: `.work/m_bin_final3` (not committed; rebuild from source).

## Corrections applied (2026-09-21)

1. **M3 capacity**: corrected to model 4,000 live slots with a larger
   monotonic-ID space (was conflating live slots with ID space).
2. **M6 capacity**: corrected to `4*nt + ny + 1024` with defensive
   negative-ID checks.
3. **M1 swap schedule**: fixed to guarantee exactly 64 probes.
   Original `per=ceil(n/64)` yielded 63 probes (interval is per+1 due to
   reset semantics). Changed to `per=n/64-1`, verified 64/64 on prose
   (84,731 units) and code (148,678 units).
4. **M7 corpus registry**: `coffs`/`clens` enlarged from 32 to 40 bytes
   (10 entries) — round 3 uses corpus 9 (C'), which was out of bounds.
   This was the actual cause of the M7 "slice index out of bounds" panic
   in the 1x evidence run (not the hash table).
5. **M7 dedup disabled**: The FNV hash accelerator for the dedup scan
   triggers a znc multi-parameter compiler bug (panics in round 2 with
   computed index; works with constant index). Inlining, field aliasing,
   and 32-bit hashing did not resolve it. Dedup path is disabled for 1x;
   M7 reports dedup 0.00, honestly failing the ≥0.4 bar and triggering
   the frozen "revert to pure issuance" rule for the M-dedup claim.

## 1x evidence run (2026-09-21)

Binary: `.work/m_bin_final3`. All modes RC=0.

| Mode | Result |
|---|---|
| m1-1x-prose | M1,prose.bin,100.0,100.0,84731,SWAP,64/64,PASS |
| m1-1x-code | M1,code.bin,100.0,100.0,148678,SWAP,64/64,PASS |
| m2-1x-t1p | M2,m2-1x-t1p,1,0,0.0 |
| m2-1x-t1c | M2,m2-1x-t1c,1,0,0.0 |
| m2-1x-t2p | M2,m2-1x-t2p,1,0,0.0 |
| m2-1x-t2c | M2,m2-1x-t2c,1,0,0.0 |
| m2-1x-t3 | M2,m2-1x-t3,1,0,0.0 |
| m2-1x-t1p-m9 | M2,m2-1x-t1p,1,0,0.0 (M9 fields in JSON) |
| m3-1x | M3,100.0,100.0,8050,50,CLEAR |
| m4-1x-prose | M4,m4-1x-prose,100.0,100.0,0.0,0 |
| m4-1x-code | M4,m4-1x-code,100.0,100.0,0.0,0 |
| m5-1x | M5,84731,5422721,2389540,5486784,-1 |
| m6-1x-p2c | M6,p2c,100.0,100.0,100.0,0.0 |
| m6-1x-c2p | M6,c2p,100.0,100.0,100.0,0.0 |
| m7-1x | M7,counter-id,hit,100.0,reuse,1.01,dedup_barred,0.00,dedup_r3,0.00 |
| m8-clean | M8,100.0,100.0,6759488,d23b425c… |
| m8-frag | M8,100.0,100.0,6759488,d23b425c… (identical) |
| m8-aslr | M8,100.0,100.0,6759488,d23b425c… (identical) |
| m8-starve | M8,100.0,100.0,6759488,d23b425c… (identical) |
| m8-freelist | M8,100.0,100.0,6759488,d23b425c… (identical) |
| merge-1x | MERGE,nA,84731,nB,148678,links,1487,dangling,0,misdirected,0,remap_frac_x10000,3914,kill,1 |

M8 image sha256: `d23b425cd1f41e3a06648ec8fa03e063bad7be75ba92ff375362b4089e22da20`
(all five perturbations byte-identical).

Merge: remap 39.14% > 10% → scoped kill fires (see VERDICT.md).

## 10x status

NOT RUN. The 1x gate does not permit 10x: the merge scoped kill fires at 1x
(counter IDs die as cross-store/global identity), and the M-dedup claim
dies at 1x (dedup 0.00 < 0.4). Per the frozen rules, 10x is not attempted.

## Raw logs

`.work/final1x_v2/` in the arm directory contains per-mode `.stdout` and
`.stderr` from the evidence run. Copies are committed under
`docs/lab/units/arms/M/raw/`.
