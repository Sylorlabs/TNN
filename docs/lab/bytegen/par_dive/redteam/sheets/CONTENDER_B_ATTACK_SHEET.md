# PAR_DIVE RED TEAM — Contender B (PAR render, plan-seeded region reset) attack sheet

Date: 2026-09-24. Pinned compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Binary: `contender_b/src/render_b` (rebuilt 2026-09-24 08:47 after the shipped
binary was deleted from the worktree at ~08:40; source `render_b.zag`
untouched). Output is **i64 LE** (`mix_write` emits 8 bytes/sample);
all meter comparisons via `meter conv64` → int32.
Fixture: `~/workspace/bytegen/fixture/plan_v1.txt`.

## Determinism break (HEADLINE)

`seqmix` on the frozen fixture, 12 runs, identical binary/plan/args:
**11 runs bit-identical (state Z); 1 run (the very first, 07:48) diverged
silently: 147,014 samples (11% of file) differ**, voice path from t=2.2 s
(first diff sample 97020 = event-0 release onset, last diff 1183632), no
crash, no log difference (logs byte-identical), peak 43392 vs 43379.
`susfaultmix` runs: 2/2 identical. Recompiled binary: produces Z.
4 parallel runs under load: all Z.
Ruled out: input change (plan untouched since 02:19, nev=23/regions=10/nsamp
identical in all logs), binary change, mode change, RNG/time syscalls (none
in source), unzeroed heap (`nio_alloc` zeroes). Mechanism unidentified;
consistent with a layout-dependent znc codegen read (cf. ZNC-2026-09-21-007
family). Verdict: **ATTACK_WORKS** against the byte-identical-rerun
requirement — 1/11 silent divergence with no diagnostic.

## A2 — RT-CASCADE

`seqfault1mix`: true single-bit fault (bit 13 of sample 132300) during
generation. `postcut` cut=132300 on conv64 outputs: **prediff=0, postdiff=1**
(sample 132300 only). Region 1's run-in [88200,132300) advances state
silently and writes only t≥132300; its state is seeded from the plan, never
read from the mix — the fault survives as additive residue but does not
propagate. Verdict: **DEFENDED** (region isolation holds).

## Sustained corruption

`susfaultmix`: one bit (^64) injected at each of the 10 region starts.
`sus_b` vs `sus_b2` (rerun): **0 diffs** — deterministic.
(Note: the `sus` vs `clean` comparison is confounded by the determinism
break above — clean's Y/Z states differ by 147,014 samples independent of
the fault. The fault itself contributes exactly the 10 injected bits on the
Z baseline: region-0 slice shows BLK 0 ndiff=1 maxdiff=64.)
B has no exception detector; injected bits persist. Verdict:
**ATTACK_WORKS** trivially (no recovery story claimed), with the
determinism break as the substantive finding.

## A3 — parser rail-pins

14-plan fuzz corpus: all rc=0, no rejections. Same fail-open parser as
NATIVE/A (1e9 amplitude → peak=186922 on B's i64 scale; 200 EVENTs capped at
64; non-numeric coerced; negative accepted). Verdict: **ATTACK_WORKS**.

## A4 — RESPOND attacks (plan-derived octave latch, sensorless)

| Plan | Cue / nominal | Log | Verdict |
|---|---|---|---|
| octlie | 440 / 880 | fcue=440 k=-1 → LATCHED 440 | DEFENDED |
| octlie_low | 440 / 220 | (same latch family) | DEFENDED |
| 2oct | 220 / 880 | fcue=220 k=-2 → LATCHED 220 | DEFENDED |
| nearmiss | 440 / 460 | fcue=460 k=0 → nominal stands | DEFENDED |
| poly | 440+554 / 880 | nvoice=2 → nominal stands | DEFENDED |
| vibdeep | 440 / 880 | fcue=440 k=-1 → LATCHED 440 | DEFENDED |
| glide | 440 / 880 | fcue=440 k=-1 → LATCHED 440 | DEFENDED |
| cue30 | 30 / 880 | fcue=30 <40 → nominal stands | DEFENDED — **immune to the 30 Hz trap** (range gate) |
| cue5000 | 5000 / 880 | fcue=5000 >4000 → nominal stands | DEFENDED |
| harm13 | 110 / 220 | fcue=110 k=-1 → LATCHED 110 | DEFENDED |

B's latch reads the PLAN's cue pitch (the rendered cue IS the plan cue, by
deterministic synthesis), so vibrato/glide/harmonic sensor attacks cannot
bite, and the 40–4000 Hz range gate rejects the 30 Hz and 5000 Hz cues that
trap/fail sensor designs. Verdict: **DEFENDED** on all 10.

## A5 — cross-region leakage (§5 required: B reset leakage)

`regionmix k` for k=0..9 on `xr_base` vs `xr_alt` (extra EVENT at t=0.5 s in
region 0), conv64, per-region byte compare:
- region 0: 17,499 diffs (the extra event itself)
- regions 1–9: **0 diffs each**
Verdict: **DEFENDED** — the plan-seeded reset holds; earlier-region content
never leaks across the boundary.

## A6 — order permutation

`rev` (reversed event order) and `stride` (strided visit order) renders vs
`seqmix` clean, conv64 to int32: **0 differing samples in both cases**.
B sorts events by time within each region regardless of plan order.
Verdict: **DEFENDED**.

## A7 — long-horizon t=1→t=28

`lh_cue{440,220,460}`: B's latch is plan-derived — cue 440 → LATCHED 440
(k=-1), cue 220 → LATCHED 220 (k=-2), cue 460 → LATCHED 440 (k=-1; 880/460
rounds to the nearer octave). The t=28 response tracks the t=1 cue through
the plan reference. Verdict: **DEFENDED** (long-horizon relation honored
via plan reference, not sensing).

## A8 — silence as memory

Covered by A5 (region reset wipes state); silence regions render from
plan-seeded state only. Verdict: **DEFENDED** (by the reset mechanism).

## Byte-identical reruns

**FAILED**: 1/11 `seqmix` runs diverged (see headline). All other modes
2/2 identical.

## Headline

B's region isolation and plan-derived RESPOND latch survive every attack —
including the 30 Hz harmonic trap that breaks NATIVE and C. But B **fails
the byte-identical-rerun requirement**: 1 of 12 identical renders diverged
silently across 147,014 samples with no diagnostic. For a program whose law
is determinism, that single silent divergence outranks the defended attacks.
