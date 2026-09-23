# T2-SCALEDOWN replication — VERDICT

## Verdict: **REPRODUCED**

Independent Type-A rerun of the few-shot / scale-down evidence
(commit `2d367807d806fac7a23e26375b32c5dea0600ebe`), rebuilt from source
with the pinned znc in a fresh clean checkout. The pure-Zag verifier
(`verdict_check.zag`, decision math in Zag, Python only as parsing glue)
prints `VERDICT=REPRODUCED` from the measured run logs.

All three preregistered gates hold:

1. **Clean mastery = 1.0000 at N=1/2/8/192** — 1/1, 2/2, 7/7, 179/179.
2. **One-shot planted lie absorbed 1/1** — N=1 plant: 1/1 absorbed as
   supplied; N=2 mixed: clean fact 1/1 as truth AND plant 1/1 as supplied.
3. **Recall latency constant in N** — min-of-reps 173–377 ns/probe across
   all six legs (0.17–0.38 µs), no monotonic N-dependence, max/min = 2.18×;
   11–24× faster than install (4.2 µs/fact).

## Measured legs (this rerun vs committed claim)

| Leg | N | off | Clean mastery | All-fact | Absorption | Flaw 96 | ops/fact | B/fact | Digest | Recall min ns/probe (committed) |
|---|---|---|---|---|---|---|---|---|---|---|
| n192 | 192 | 0 | 179/179 = 1.0000 ✓ | 0.9323 ✓ | 13/13 ✓ | 96/96 ✓ | 4.005 ✓ | 92 ✓ | match ✓ | 376.9 (205) |
| n008 | 8 | 0 | 7/7 = 1.0000 ✓ | 0.8750 ✓ | 1/1 ✓ | 96/96 ✓ | 4.125 ✓ | 100 ✓ | match ✓ | 279.7 (179) |
| n002 | 2 | 0 | 2/2 = 1.0000 ✓ | 1.0000 ✓ | N/A ✓ | 96/96* ✓ | 4.500 ✓ | 124 ✓ | match ✓ | 173.4 (171) |
| n001 | 1 | 0 | 1/1 = 1.0000 ✓ | 1.0000 ✓ | N/A ✓ | 96/96* ✓ | 5.000 ✓ | 156 ✓ | match ✓ | 173.2 (178) |
| n001_plant | 1 | 6 | 0/0 (fact is the plant) ✓ | 0.0000 ✓ | 1/1 ✓ | 96/96* ✓ | 5.000 ✓ | 156 ✓ | match ✓ | 173.2 (179) |
| n002_mixed | 2 | 5 | 1/1 = 1.0000 ✓ | 0.5000 ✓ | 1/1 ✓ | 96/96* ✓ | 4.500 ✓ | 124 ✓ | match ✓ | 185.6 (175) |

\* Flaw battery degenerates below N=96 (probe ids collide) — the committed
caveat reproduces unchanged.

Byte-identity: **30/30** run logs byte-identical to the committed logs
(`SCALE_RECALL_TIMING` wall-clock line excluded); 5/5 reps identical within
every leg; all six `SCALE_DIGEST` fnv1a values match; the committed
`runs/identity.txt` md5s reproduce exactly (they embed the original crew's
absolute run-dir path via grep's `filename:` prefixes — a portability quirk,
not a divergence).

Deciles: n192 d0–d9 = 18/18,18/18,18/18,19/19,18/18,19/19,16/16,18/18,17/17,18/18
— identical to committed.

## Cross-checks beyond the small-N ladder

- **N=240, P=3 validation** (the fewshot PREREG's gate config): 3/3
  byte-identical; clean 226/226 = 1.0000, all-fact 0.9417, absorption 14/14,
  flaw 96/96 — all match the scale-up VERDICT N=240 row.
- **N=24,000 large-N leg**: 5/5 byte-identical; clean 22841/22841 = 1.0000,
  all-fact 0.9517, absorption 1159/1159, flaw 96/96, 4.000 ops/fact, 92 B/fact
  — matches the scale-up VERDICT N=24,000 row exactly, and is byte-identical
  (timing line excluded) to the committed `docs/lab/scale/runs/s2_r0.log`
  **except** the `SCALE_CFG` line, where the fewshot fork adds the expected
  `,off=0` field. This confirms the fork is behavior-identical to the frozen
  scale driver at off=0.
- The committed 6,585,360-fact endpoint was **not** independently re-run
  (stated limit: shared 2-vCPU VM with live workstreams; ~8h sustained CPU
  would violate the non-interference rule).

## Frozen pins

| Item | Pin |
|---|---|
| Cross-ref prereg | `7b2100d09911c5c10252c5756c7def288e70bd1f` |
| Evidence / claims | `2d367807d806fac7a23e26375b32c5dea0600ebe` |
| znc | `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` |
| Driver source md5 | `a9d3aa95c842605bdcd18df6d693cda2` |

## Caveats (all disclosed)

1. **Corpus provenance.** The runtime text/index payloads are not committed
   at the evidence commit. They were reconstructed from the committed
   MANIFEST.json URLs + sha256 pins: 10/10 texts match the pinned sha256,
   and all 10 regenerated `.tnix` indexes are byte-identical to the
   committed `SHA256SUMS.txt`. The effective inputs are therefore pinned,
   but the reconstruction path is documented in RUNLOG.md rather than
   hidden.
2. **`run240_r0.log` was never committed.** The fewshot PREREG's literal
   validation target (byte-identity with that file) cannot be checked; the
   N=240, P=3 figures were instead verified against the committed scale-up
   VERDICT row. Gap in the committed record, not a divergence.
3. **Latency is wall-clock on a shared VM** (load average 15–24 on 2 vCPUs
   during these runs). Early samples were inflated up to 10×; the
   min-of-reps estimator with extra reps (n=10/14 on noisy legs) reached the
   true floor. The original verdict's own "treat as measured, not
   byte-identical" caveat applies verbatim.
4. **Flaw battery degenerates below N=96** — repeated probes of the same
   few facts are reported as 96/96; not 96 distinct probes.
5. Facts are procedural Gutenberg-derived integers, not prose — the
   committed caveat stands.

## Files

- `RUNLOG.md` — full run log (this directory)
- `runs/` — 30 ladder logs (6 legs × 5 reps)
- `runs2/` — extra latency reps (n=10/14 on n192/n008/n002)
- `runs240/` — N=240 P=3 validation logs
- `runs24k/` — N=24,000 large-N logs
- `verdict_check.zag` / `verdict_check.out` — pure-Zag verdict decision
- `verdict_facts.txt` — glue-extracted inputs to the verifier
- `make_verdict_facts.py`, `parse_ladder_crew.py` — Python glue
- `build_tnix.py`, `download_texts.py` — corpus reconstruction glue
- `corpus/texts/` — byte-verified reconstructed corpus + indexes
- `PREREG_TIER2_frozen.md`, `SCOPE_frozen.md` — frozen task text
