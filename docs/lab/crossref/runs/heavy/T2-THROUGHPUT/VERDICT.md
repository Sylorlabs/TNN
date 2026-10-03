# T2-THROUGHPUT crossref verdict: **PARTIAL**

Crew: T2-THROUGHPUT heavy (Type B anchor replication), 2026-09-23 PDT.
Frozen prereg: `crossref/PREREG_TIER2.md` §T2-THROUGHPUT
(sha256 `90070c88e43aecb6ba3ee8df6d487f7bf1b1673bb12d3ad8dcd11d597ade4a9f`).
Evidence commit `67bf4c4cf81b9d1d5e1e4e150892843830ff8b2b` (API-verified).
METHOD.md blob `fe64a1232785aa631aef77bbd003f810e8265a0b` matches pinned commit exactly.

## Method (per frozen METHOD.md, Type B)

Clean sparse checkout of `sylorlabs/TNN@67bf4c4c` (branch tnn-native-lab, head at run start
`5efe0a10a93a5bffa07f689a58d86417e850425c`) into
`~/workspace/scratch-crossref/T2-heavy/T2-THROUGHPUT/clean/`; both instruments rebuilt
from source with the pinned znc (`znc_linux_x86_64_abed8aa1`, `--no-analyze`); no
`.zagd`/binaries reused. Both instruments diff-verified as **timing-only copies**
of their claimed sources (55 diff lines each, all clock/accumulator/print):
`thru_learner.zag` vs `scale/fewshot/driver/fewshot_learner.zag@67bf4c4c`;
`dlg_thru.zag` vs `dialogue/dialogue.zag@67bf4c4c`.
Anchors: install/recall at N=240 (anchor) + N=240,000 (mid-scale), 3 reps each,
sequential; dialogue 370-turn battery 3 reps (×2 load windows).
Clock discipline: `CLOCK_PROCESS_CPUTIME_ID` for install; `CLOCK_MONOTONIC` (wall)
for recall/deliberation/emission — exactly as frozen.
Corpus: lab-local `~/workspace/scale/corpus/texts` (22 files, 24 MB — not in git;
provenance sha256s in RUNLOG.md).

## What reproduced

| Claim | Measured | Bar | Result |
|---|---|---|---|
| Install ~6.2 µs/fact (CPU clock) | N=240: 5.97/5.93/6.29 µs (med 5.97 → 167.6K/s); N=240k: 6.41/6.385/6.266 µs (med 6.385 → 156.6K/s) | ±10% (5.58–6.82) | **PASS** |
| Flat O(1) in N (install) | 5.9–6.4 µs across 1000× N | flat | **PASS** |
| 4 ops / 92 B per fact | 4.000–4.004 ops (driver's own SCALE_OPS); SCALE_MEM total_bpf=92 at both scales | exact | **PASS** |
| Determinism | learner digests byte-identical ×3 at both scales (`44a61309cf780de1`, `31377bd76faa81c1`); dialogue deterministic content byte-identical across all 6 reps; 370/370 PASS every rep | byte-identical | **PASS** |

## What moved (the PARTIAL)

Wall-clock anchors fell outside their committed bands. The VM was NOT quiet:
load avg 24–35 during the learner runs (a VM reboot hit mid-run, killing rep2 —
rep1 pre-reboot valid, reps 2–3 re-run post-reboot), 5–17 during the quiet
dialogue window. The original crew measured at load 8–13 and their own report
documents wall-clock degradation under contention (25–60 µs/fact wall vs 6.2 CPU).

| Claim | Committed band | Measured | Note |
|---|---|---|---|
| Recall 1–3.2M probes/s, O(1) in N | 1–3.2M | N=240: 307–449K/s; N=240k: 2.14M (in-band) / 511K / 731K | band moves; **O(1) holds** (no growth with N; committed N=240k median was 942K) |
| Deliberation ~3,300 eps | ±20% → 2,640–3,960 | 738–1,475 eps (both load windows) | band moves; **ordering holds** (deliberation still the slowest stage: 0.68–1.36 ms/turn vs 42–307 µs/utterance emission) |
| Emission ~507K chars/s med | 342K–1.29M | 775K ✓, 460K ✓, 106–138K (load-contended) | band moves under load |
| End-to-end ~109K chars/s | 87K–151K | 25–31K | band moves under load |

## Verdict

**PARTIAL** per the frozen rule ("the band moves but ordering holds — name it").
Missing: a quiet-VM rerun of the wall-clock anchors (recall/deliberation/emission/
end-to-end) at load comparable to the original measurement (~load 8–13 or lower).
Everything the frozen method isolates from contention (install CPU-clock, ops,
bytes, determinism, correctness) reproduces exactly; the mechanism is intact —
the wall-clock numbers moved with the busier machine, not the code. No fix
attempted (out of scope for crossref).
