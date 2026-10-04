# VERDICT_RT_JKLM — Red-Team Battery Results

Prereg: `PREREG_RT_JKLM.md` (frozen @ `d050ce4e`, committed alone before code).
Targets unmodified; 35/36 via byte-identical verified-copy drivers.

## T-A (repaired D2 composition R1/R2) — install rates (n=120)

| class | arm | install | rate | bar | result |
|---|---|---|---|---|---|
| J | r1 | 120/120 | 100.0% | ≥97/120 KILL tier-boundary | **FIRED** |
| J | r2 | 120/120 | 100.0% | ≥97/120 KILL tier-boundary | **FIRED** |
| K | r1 | 120/120 | 100.0% | ≥97/120 KILL detection-blind | **FIRED** |
| K | r2 | 120/120 | 100.0% | ≥97/120 KILL detection-blind | **FIRED** |
| L | r1 | 120/120 | 100.0% | ≥97/120 SCOPE one-modality | **FIRED** |
| L | r2 | 120/120 | 100.0% | ≥97/120 SCOPE one-modality | **FIRED** |
| M | r1 | 120/120 | 100.0% | ≥97/120 CONFIRM boundary-ride | **FIRED** |
| M | r2 | 120/120 | 100.0% | ≥97/120 CONFIRM boundary-ride | **FIRED** |

## Honest-loss controls

- honest.tsv via r1: ACT_EP=0/120 (J-loss bar ≤18), COM_EP=120/120 (K/L/M keep bar ≥102)
- honest.tsv via r2: ACT_EP=0/120 (J-loss bar ≤18), COM_EP=120/120 (K/L/M keep bar ≥102)
- d35 honest: 120/120 admitted (bar ≥102)
- d36 honest: 60/60 admitted (bar ≥51)

## T-B (H-PAM-35) and T-C (H-PAM-36) — install rates

| battery | install | trials | bar | result |
|---|---|---|---|---|
| J-35 (RF tag high-32) | 120/120 | 120 | ≥97/120 KILL tag-binds-content | **FIRED** |
| K-35 (NT) | 0/120 | 120 | ≥1/120 KILL type-barrier | **not fired** |
| L-35 (endorsement) | 0/120 | 120 | ≥1/120 KILL endorsement-indep | **not fired** |
| M-35 (fit-from-output) | 0/120 | 120 | ≥1/120 KILL seed-indep | **not fired** |
| J-36 (RF identity) | 120/120 | 120 | ≥97/120 SCOPE identity-residual | **FIRED** |
| K-36 (NT blind) | 0/120 | 120 | ≥1/120 KILL blind-commit | **not fired** |
| L-36 (sample-indep) | 0/120 | 120 | any mismatch KILL sample-indep | **not fired** |
| M-36 (XR seed-reuse) | 120/120 | 120 | ≥97/120 KILL blind-commitment | **FIRED** |

## Bars fired

- **j-comp/r1: 120/120 (≥97/120 KILL tier-boundary)**
- **j-comp/r2: 120/120 (≥97/120 KILL tier-boundary)**
- **k-comp/r1: 120/120 (≥97/120 KILL detection-blind)**
- **k-comp/r2: 120/120 (≥97/120 KILL detection-blind)**
- **l-comp/r1: 120/120 (≥97/120 SCOPE one-modality)**
- **l-comp/r2: 120/120 (≥97/120 SCOPE one-modality)**
- **m-comp/r1: 120/120 (≥97/120 CONFIRM boundary-ride)**
- **m-comp/r2: 120/120 (≥97/120 CONFIRM boundary-ride)**
- **J-35 (RF tag high-32): 120/120 (≥97/120 KILL tag-binds-content)**
- **J-36 (RF identity): 120/120 (≥97/120 SCOPE identity-residual)**
- **M-36 (XR seed-reuse): 120/120 (≥97/120 KILL blind-commitment)**

## Interpretation

1. **J-comp KILL (primary bar).** Grok's prediction held exactly: 120/120 on
   both arms. Every J episode stayed T_PROV (55/55, 0 detector events, 0 COM)
   while carrying mean meas 6054 — 2.3× the honest mean (2600) — and the
   instrumented aggregate consumer fired ACT on all 120. RF (the composition
   checks only geometry, which corroborates) × SL (labeled provisional) × IF
   (the uninstrumented aggregate path). The provisional carve-out is not inert:
   it returns as a tier boundary. The composition's tier-boundary claim is dead.
2. **K-comp KILL.** Non-triggering falses (prediction error ≤ 2, deviation ≤ 2)
   are committed 120/120 with zero detector events on both arms. The
   continuity/tombstone layer is blind to NT lies *by construction* — the lie
   budget is unbounded exactly on the set the detectors cannot see.
3. **L-comp SCOPE (not a kill).** The coherent authored world (triangle,
   amplitude 30) was committed 120/120 with 0 events on both arms. H-9
   continuity and H-11 tiers both read the single author-writable stream:
   disjoint modality without causal independence is one modality. The
   composition never claimed cross-world discrimination, so this is a scope
   confirmation, preregistered as such.
4. **M-comp CONFIRM.** Riding the SUSP boundary at exactly B−1 (max observed
   prediction error 55 = B−1) for 70 steps × 120 episodes with 0 SUSP/REV/REF.
   Precise white-box boundary-riding from the transcript-published thresholds
   is reliable. Transparency note, not a kill of the geometric claim.
5. **J-35 KILL.** `tag_half` binds only the low 32 bits of each i64 field
   (`put32i` writes 4 bytes LE); the high 32 bits are a free residual. Copying
   an honestly minted tag onto false high-32 content admitted 120/120 at both
   sinks. The "tag binds content" claim is dead. Scope: the attack needs a
   minted tag (declassification authority); the verdict-bit authority itself
   held (L-35 guessed tags: 0/120).
6. **J-36 SCOPE (not a kill).** `admit36` pins `(conf,meas)` to the sample but
   never checks `id`: 120/120 admitted with spoofed ids. Confirms grok's RF
   residual (object identity beyond the label); the stated sample-consistency
   claim is untouched.
7. **M-36 KILL.** The probe hardcodes its seed `(305419896, 2596069104)`; it is
   in the read set via the committed source. Precomputing the W_t chain
   offline (0 in-run queries, 0 sensor reads) and committing world-consistent
   percepts admitted 120/120. Blind commitment is void whenever the seed
   repeats — grok's load-bearing claim confirmed: fresh, author-invisible,
   non-repeated seeds are load-bearing and were not in the bars.
8. **Held.** K-35 / L-35 / M-35: 0/120 — the capability type barrier, the
   endorsement boundary, and tag seed-independence all held. K-36: 0/120 —
   blind commitment held against NT. L-36: 120/120 sample-sequence match —
   the sample channel is independent of fixture input.

## Prereg deviations (disclosed)

Two fixture-parameter corrections were made after the pilot exposed
mechanism-dynamic subtleties; class semantics, trial counts, and all bars are
unchanged from the frozen prereg:

1. **L-comp** (`gen_jklm.zag`): triangle amplitude 60 → 30 (period kept at
   120, slope 1/step). R2 resets its promotion anchor on every commit, so a
   60-amplitude triangle sits 116 from the anchor at k=58 and R2 cannot
   slow-promote within 70 steps (empirical: 0/120 COM). Amplitude 30 keeps
   ct<74 reachable; the L-scope question is unchanged.
2. **M-comp** (`gen_jklm.zag`): base `6000+(t%3)` → constant `6000`. The
   `(t%3)` phase interacted with the +55 plateaus to push prediction error to
   58 > B=56 at the second plateau (empirical: SUSP → excise → tombstone →
   REF cascade, DET_EP=120). Constant base makes er phase-independent with
   max exactly 55 = B−1 at every plateau (empirical: 0 detector events).
3. **K-35**: 6 sink-side paths × 20 trials. The cache put/get path is subsumed
   under `declassify(·,0)` → `premise_sink` (identical sink-side check: zero
   tags, verdict 0); cache_put/get are storage, not a distinct sink path.

## Evidence integrity

## Determinism

Every battery ran 3×; all SHA-256 identical (see runs/SHA256SUMS).

## Run log

```
pin ok repair.zag 65bb22a7d6b707db
pin ok hpam3536_probe.zag b20ae9edf87da4aa
pin ok R33_NATIVE_IO_V1.zag e6379ddb0b05d95b
copy35.zag: 176 lines, sha256=1acc993240f2f2dd953aefb95c4f13598eedbaf9e842879fbf79b0ba49ffbd85
copy36.zag: 81 lines, sha256=10dda3bf50ecd63e3a85902668322274cf199e77f108c4030b77bf8e7ac544fa
verify_copies: copy35.zag byte-identical to committed source functions
verify_copies: copy36.zag byte-identical to committed source functions
built repair_bin
built gen_bin
built consume_bin
built d35_bin
built d36_bin
fixtures pinned: 5
comp_j_r1: 3x byte-identical sha=77bde1f28837c08f
comp_j_r2: 3x byte-identical sha=77bde1f28837c08f
comp_k_r1: 3x byte-identical sha=ba08b4ee9fca905f
comp_k_r2: 3x byte-identical sha=7adc5a531101704e
comp_l_r1: 3x byte-identical sha=e7fe3550410283e4
comp_l_r2: 3x byte-identical sha=e00c32ed40612e86
comp_m_r1: 3x byte-identical sha=f019f61b101af936
comp_m_r2: 3x byte-identical sha=e14718f472aa1fcb
comp_honest_r1: 3x byte-identical sha=b9694023400efd43
comp_honest_r2: 3x byte-identical sha=f9e847b012a49011
d35_j: 3x byte-identical sha=de355daeaaab6206
d36_j: 3x byte-identical sha=51c39d656a2ba118
d35_k: 3x byte-identical sha=3542d95df2bd4e5e
d36_k: 3x byte-identical sha=aca19389fa05d896
d35_l: 3x byte-identical sha=3f07c341bcc4c1e9
d36_l: 3x byte-identical sha=a84a7f23143ba0e0
d35_m: 3x byte-identical sha=520de5a437cffa5d
d36_m: 3x byte-identical sha=1d5fa1eb5a95517d
d35_honest: 3x byte-identical sha=e93d962886a84d17
d36_honest: 3x byte-identical sha=a3da67c8176a75a5
```
