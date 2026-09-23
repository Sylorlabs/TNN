# PREREG — Senses Phase 2, AUDIO track (2026-09-20)

**Status: FROZEN before build.** This prereg is committed before any phase-2
audio source is written. It measures against
`../../PROPOSED_QUALBAR_SENSES_2026-09-20.md` (PROPOSED, UNSIGNED — not law).
Results are reported as "meets proposed bar §X / does not meet", never as
QUALIFIED. Kill bars K-SE1..K-SE8 are binding: a fired bar kills the run,
the witness is committed, the verdict is DEAD.

Scope: AUDIO ONLY (§A-audio, §B-audio, §C-audio, §D-audio, §E-audio).
Vision is a separate worker. No learner dependency; the quarantined r34
core is not touched.

## 1. Source provenance

- `se2a_ingress.zag` — COPIED from
  `~/workspace/tnn-lab/wave12/senses/phase1/se_ingress.zag` with exactly two
  deliberate deltas (both documented here, both required by the proposed bar):
  1. `SE_MAX_PAYLOAD`: 4096 → **16384**. Phase-1's 4,096 B cap cannot admit
     §E's 16,000 B one-second frames. New capacity: 32 records ×
     (80 + 16,384) B = 526,848 B < 2^25. This meets the bar's envelope; it
     does not lower it.
  2. New refusal code `SE_BAD_RESERVED` = **-7110** + validation: all 20
     reserved header bytes @28..48 must be zero, checked immediately after
     the encoding-id check. Phase-1 admitted reserved-nonzero records; §A
     requires refusing them.
- `se2a_memif.zag` — VERBATIM copy of phase-1 `se_memif.zag` (no deltas;
  16 slots, codes -7201..-7210, append-only 256-entry audit).
- `se2a_main.zag` — NEW: audio battery driver (modes `harness`, `verify`).
- `substrate/` — vendored copies of phase-1's `R33_NATIVE_IO_V1.zag`,
  `R33_NATIVE_SHA256_V2.zag`, `cl/common.zag` (byte-identical to
  `SUBSTRATE_SHA256.txt` hashes; verified at build).
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
  Pure Zag. No RNG, no wall-clock, no threads, no floats in any source
  (K-SE6). Strength is caller-declared literals only; no arithmetic on
  observation bytes feeds any strength value (K-SE5).

## 2. Deterministic fixture generation (no RNG anywhere)

- Twin base pattern (§D), N samples: `base[i] = ((i*7919+13) % 30001) - 15000`
  → range [-15000, 15000]; i32-safe (i ≤ 255: 255*7919 = 2,019,345 < 2^31).
  Bounded so ×2 amplitude (pair d03, ±30,000) and phase inversion (d06)
  never clip — the single controlled item stays the only difference.
- §E frame pattern k: `pat(k,i) = ((i*(k*7919+17) + k*131 + 7) % 60001) - 30000`
  → [-30000, 30000]; i ≤ 7999, multiplier ≤ 55,450:
  7999*55,450 = 443,544,550 < 2^31. Safe.
- PCM16LE mono 8,000 Hz, even payload lengths, payload_len = actual bytes,
  sha256(payload) in header unless the fixture's single defect says otherwise.

## 3. §A — ingress malformed/edge battery (16 refusal checks)

Fresh store; `n_before`/`live_before` captured first. Each fixture admitted
once; each must refuse with the exact code. After the battery:
`se2a-a-n-unchanged` (n == n_before), `se2a-a-live-unchanged`
(live == live_before), `se2a-a-refusals` (refusals == 16).

| # | Name | Fixture (one defect) | Expected |
|---|---|---|---|
| 1 | se2a-a01-bad-magic | magic[0] = 0x58 | SE_BAD_MAGIC (-7101) |
| 2 | se2a-a02-bad-version | version = 2 | SE_BAD_VERSION (-7102) |
| 3 | se2a-a03-bad-encoding | encoding = 99 | SE_BAD_ENCODING (-7103) |
| 4 | se2a-a04-rate-7999 | p1 = 7999 | SE_BAD_PARAM (-7104) |
| 5 | se2a-a05-rate-0 | p1 = 0 | SE_BAD_PARAM (-7104) |
| 6 | se2a-a06-channels-0 | p2 = 0 | SE_BAD_PARAM (-7104) |
| 7 | se2a-a07-channels-2 | p2 = 2 | SE_BAD_PARAM (-7104) |
| 8 | se2a-a08-bits-not16 | encoding = 3 (non-16-bit PCM encoding id; bit depth is implied by encoding id in TNNRAW02) | SE_BAD_ENCODING (-7103) |
| 9 | se2a-a09-odd-payload | payload 15,999 B (odd), sha recomputed | SE_BAD_PARAM (-7104) |
| 10 | se2a-a10-len-mismatch | plen field = 8000, actual 16,000 B | SE_LEN_MISMATCH (-7105) |
| 11 | se2a-a11-sha-mismatch | 1 payload byte flipped after se_build | SE_BAD_HASH (-7106) |
| 12 | se2a-a12-trunc-header | first 79 B of valid record | SE_BAD_MAGIC (-7101) |
| 13 | se2a-a13-trunc-payload | valid 16,000 B record sliced to 8,080 B | SE_LEN_MISMATCH (-7105) |
| 14 | se2a-a14-zero-payload | 0 B payload, plen = 0 | SE_BAD_PARAM (-7104) |
| 15 | se2a-a15-over-capacity | plen field = 17,000 (> 16,384) | SE_BAD_PARAM (-7104) |
| 16 | se2a-a16-reserved-nonzero | reserved byte @28 = 1 | SE_BAD_RESERVED (-7110) |

## 4. §B — OBSERVE admission discipline (8 probes + 1 audit scan)

Fresh store, one valid record admitted (id 0).

| # | Name | Probe | Expected |
|---|---|---|---|
| 1 | se2a-b01-no-judgment | judgment = NONE (0) | -7201 |
| 2 | se2a-b02-judgment-5 | judgment = 5 | -7201 |
| 3 | se2a-b03-strength-0 | strength = 0 | -7202 |
| 4 | se2a-b04-strength-101 | strength = 101 | -7202 |
| 5 | se2a-b05-bad-region | region = 2 | -7203 |
| 6 | se2a-b06-bad-cite | cite_ep = -1 | -7209 |
| 7 | se2a-b07-dead-rec | rec_id = 99 | -7204 |
| 8 | se2a-b08-full | 16× OBSERVE(rec 0, strengths 10..25, cites 100..115) → 17th | -7205 |
| 9 | se2a-b09-audit-scan | mi_audit_scan() after fill | 1 (100% of live slots trace to an MI_OK OBSERVE entry) |

live == 16 after b08 (supporting assertion inside b08 flow).

## 5. §C — kill / pin / recall semantics (10 probes)

Fresh store. Admit recA/recB/recC/recD (32-sample distinct patterns).
OBSERVE recA→s0 (USER, NOVEL, 50, cite 1); recB→s1 (CORE, CORROBORATED, 60,
cite 2); recC→s2 (USER, CONTRADICTED, 70, cite 3). PIN(s0).

| # | Name | Probe | Expected |
|---|---|---|---|
| 1 | se2a-c01-kill-pinned | KILL(s0, ev=5) | -7206 |
| 2 | se2a-c02-kill-core | KILL(s1, ev=5) | -7207 |
| 3 | se2a-c03-kill-no-evidence | KILL(s2, ev=0) | -7210 |
| 4 | se2a-c04-kill-ok | KILL(s2, ev=5) | MI_OK (0) |
| 5 | se2a-c05-rekill | KILL(s2, ev=5) again | -7208 |
| 6 | se2a-c06-recall-dead | RECALL(s2) | -7208 |
| 7 | se2a-c07-recall-twice | RECALL(s0)→b1, RECALL(s0)→b2; nio_equal(b1,b2) | 1 |
| 8 | se2a-c08-no-alias | mutate b1, RECALL(s0)→b3; nio_equal(b3, authored recA) | 1 |
| 9 | se2a-c09-pin-idempotent | PIN(s0) again | MI_OK (0) |
| 10 | se2a-c10-observe-freed | OBSERVE(recD, NOVEL, 55, USER, cite 4) → lands in freed s2: rc==0 AND slot phash == sha256(payloadD) AND != sha256(payloadC) | 1 |

## 6. §D — paired twins, S1 discriminability (24 pairs, 1 check each)

Fresh SeStore+MiStore per pair. Per pair: build payload A and B differing in
exactly one controlled item; admit both (ids ≥ 0); OBSERVE both (NOVEL 50 /
CORROBORATED 60, USER, cites 1000+pair / 2000+pair); RECALL both →
`differ` = (bytes differ AND slot provenance-sha256 differ); then
save records+memif to `se2a_dstore`, load into fresh structs, RECALL both
again → `differ2`; check = differ && phash_differ && differ2 (1/0,
expected 1).

Prescribed 9:
- d01 sign-flip: sample[10] = 4201 vs -4201.
- d02 lsb-plus1: sample[20] = base vs base+1.
- d03 times2: B[i] = 2*A[i] ∀i.
- d04 dc-plus1: B[i] = A[i]+1 ∀i.
- d05 swap-adjacent: samples[30],[31] swapped in B.
- d06 phase-invert: B[i] = -A[i] ∀i.
- d07 silence-vs-dither: A = 128×0; B[i] = (i%2==0) ? 1 : -1.
- d08 trunc-vs-full: A = 128 samples; B = first 64 samples of A.
- d09 rate-twin: p1=7999 refuses (-7104), p1=8000 admits (id ≥ 0);
  check = (rc7999 == -7104 && id8000 >= 0). No OBSERVE (refused twin has
  no record); this pair tests the boundary, not memory.

Authored 15 (single controlled item each):
- d10 zero-one: sample[5] = base vs 0.
- d11 bump-position: +5 LSB at sample[0] (A) vs at sample[77] (B).
- d12 max-boundary: sample[40] = 32767 vs 32766.
- d13 min-boundary: sample[41] = -32768 vs -32767.
- d14 byteswap-one: sample[50] byte-swapped (LE↔BE) in B.
- d15 negate-one: sample[25] negated in B only.
- d16 dither-polarity: 128-sample ±1 dither starting +1 (A) vs -1 (B).
- d17 lsb-plus2: sample[20] = base vs base+2.
- d18 near-zero: sample[33] = 1 vs 2.
- d19 square-polarity: ±30000 square wave starting +30000 (A) vs -30000 (B).
- d20 dc-minus1: B[i] = A[i]-1 ∀i.
- d21 trunc-odd: A = 128 samples; B = first 65 samples of A.
- d22 edge-lsb: sample[0] = base vs base+1.
- d23 scale-trunc: A = 256 samples; B = first 128 samples of A.
- d24 dither-amp: A = 128×0; B[i] = (i%2==0) ? 2 : -2.

## 7. §E — realistic envelopes (12 checks)

- e01..e08: 8 one-second frames, 16,000 B payload (8,000 samples), pattern
  k=0..7 (§2). One store: admit 8 → OBSERVE 8 (NOVEL, strength 40+k, USER,
  cite 5000+k) → RECALL each → byte-identical to authored record
  (nio_equal == 1, expected 1).
- e09..e12: 4 ordered sequences; sequence q = 4 frames of 16,000 B,
  frame (q,r) uses pattern k=100+q*4+r. Fresh store per sequence: admit 4 →
  OBSERVE 4 (slots 0..3) → RECALL in order → recalled[j] byte-identical to
  authored frame (q,j) for j=0..3 (order preserved exactly). Check = 1/0,
  expected 1.
- The sequence-3 store is saved to `se2a_store` for the fresh-process
  verify run (K-SE7): reload → n==4, live==4, audit_scan==1, recall of the
  rec-0 slot byte-matches rebuilt frame (3,0), rec-0 vs rec-1 recalls still
  differ (twin distinction survives reload).

## 8. Kill-bar compliance

- K-SE1: `run_phase2_audio.sh` compiles twice (hash equality), runs harness
  twice from clean state, diffs stdout (must be empty). Binary rc must be 0.
- K-SE2: §B (8 exact refusals + audit scan).
- K-SE3: §A (16 exact refusals, n/live unchanged).
- K-SE4: §C c08 (mutate-then-rerecall).
- K-SE5: static grep — no `strength[slot]=` assignment except the declared
  `strength as u8` copy in the verbatim memif; no arithmetic on payload
  bytes feeding strength in se2a_main.
- K-SE6: static grep — no `_zag_rand|gettimeofday|clock_gettime|
  thread_create|pthread_create|\bf32\b|\bf64\b|_zag_time` in sources
  (comments stripped first).
- K-SE7: fresh-process `verify` mode on the harness-saved store
  (byte-identical records/slots/audit, twin distinction survives).
- K-SE8: §C c01/c02 (pinned/CORE kills refused).

Any fired bar → run stops, witness committed, verdict DEAD, reported
honestly. No bar may be reinterpreted downward.

## 9. Check-line format & counting

`CL_CHECK,se2a-<name>,<actual>,<expected>` via `cl_check`. Harness emits
71 section checks (A:16 + B:9 + C:10 + D:24 + E:12), plus supporting lines
(`se2a-a-n-unchanged`, `se2a-a-live-unchanged`, `se2a-a-refusals`,
`se2a-zz-fails-total`) and fixed markers `SE2A_HARNESS_DONE` /
`se2a-v-*` verify lines (K-SE7, counted separately). The runner fails the
run unless EVERY emitted line has actual == expected.

## 10. Verdict reporting & amendment rules

Per-section verdicts reported as "meets proposed bar §X (n/n)" or with the
failing check named. The word QUALIFIED is never used (bar unsigned).
If any proposed-bar number proves unreachable with this architecture, the
report says so and does not silently lower the bar. Any change to this
prereg after freeze requires a dated amendment note; the frozen text above
is what the build is judged against.
