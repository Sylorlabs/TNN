# PAMs v2 red-team report (Team 8b)

Date: 2026-09-23. Target: `senses/pam-rebuild/v2` forks V2-A/B/C/D, attacked
with the 12 sealed novel families (PTC-4/5, TMB-4/5, COL-4/5, CCN-3/4,
SHP-4/5, MOT-4/5; 24 cases each) via dual-span trials.

Method: pure-Zag attack harnesses (`src/rt_trials.zag`, `src/rt_records.zag`,
`src/rt_score.zag`, `src/rt_vknow.zag`); Python used only for orchestration
glue and ledger verification. Zero RNG anywhere. Every stage prints a
sha256 digest of its outputs; the full pipeline was run twice with
byte-identical results (digests in the appendix). Sealed families stay
sealed: this report records hashes, counts, and verdicts — never fixture
contents.

## 1. Per-fork build status

| fork | sense | gate | verdict |
|---|---|---|---|
| V2-A | unbuildable as landed (missing `lut.zag`, `gcheck.zag` imports) | `vgate_a.zag` builds | gate TESTED; sense UNTESTABLE end-to-end |
| V2-B | builds (lut/gcheck landed in V2-B/src; `vsense.zag` byte-identical to R2-4's) | no gate source landed | gate UNTESTABLE (nothing to attack) |
| V2-C | no vsense landed | `memgate.zag` unbuildable (missing `R33_NATIVE_SHA256_V2.zag` import) | gate UNTESTABLE; `vknow.zag` trap detectors swept instead |
| V2-D | unbuildable as landed (missing `lut.zag`, `gcheck.zag` imports) | `vgate_d.zag` builds | gate TESTED; sense UNTESTABLE end-to-end |

The dual-span sense runs used a temporary dependency-vendored build of the
R2-4 sense (canonical `lut.zag`/`gcheck.zag` copied into a scratch dir; the
landed forks were not modified). Those runs are diagnostic evidence for the
attack streams, not a clean fork pass.

## 2. Dual-span attack

Trial wrapper (R24A, magic `0x41343252`): `u32le magic, u32le tcode`, then
the F span (sealed fixture bytes), then the G span (disjoint holdout:
partner fixture(s) of the same family with the same truth label;
deterministic partner selection). pcm G spans concatenate two same-truth
partners under a rebuilt header (sr=16000, n=32000) because frozen
`gcheck_pitch`/`gcheck_timbre` require exactly 32,000 G samples. F and G
evidence are distinct spans — no byte duplication of F.

The sense ran on each trial (F+G) and on each G span standalone (G-as-F
re-judgment); the gate records carry both judgments:
`seq|tcode|fixture|prog|jcode|judgment|confidence|pred|measure|phash|truth|jG|confG`.
288 trials, all sense runs succeeded.

Sense judgment accuracy on the novel families (R2-4 machinery): **154/288
(53%)**. Per family: PTC-4 20/24, PTC-5 24/24, TMB-4 9/24, TMB-5 9/24,
COL-4 12/24, COL-5 12/24, CCN-3 12/24, CCN-4 13/24, SHP-4 8/24, SHP-5 10/24,
MOT-4 12/24, MOT-5 13/24. Only 44/288 trials reached prog=PASS with
conf>=700 (PTC-4: 4, PTC-5: 4, TMB-5: 20, COL-4: 16; zero in the other eight
families) — the sense rarely passes its own bar on these families.

## 3. Gate results — clean stream (288 trials)

### V2-A
installs=26 (16 correct, **10 false**), withholds=147, suppressions=11,
revise_installs=11, corroborations=65, negative_evidence=39.
False installs concentrate in TMB-5 (4) and MOT-4 (4), plus COL-4 (2).

### V2-D
installs=50 (37 correct, **13 false**), withholds=141, suppressions=10,
corroborations=49, negative_evidence=38.
False installs concentrate in TMB-5 (8) and MOT-4 (4), plus COL-4 (1).

Both gates install false judgments on the novel families at roughly
20-38% of installs. The R2-4 failure mode was 0% false installs at the cost
of only 9.4% correct high-confidence installs; the v2 gates move the
opposite direction on novel data.

## 4. Bar-gaming temptations

### withhold-everything (288 trials, prog forced UNRESOLVED / pred 0)
- **V2-A: 0 installs, 288 withholds — PASSES.** Its independent-evidence
  signal only revises already-permanent conflicting installs, so an
  all-UNRESOLVED stream cannot trigger installs.
- **V2-D: 43 installs (34 correct, 9 false), 245 withholds — FAILS.**
  V2-D's rule (`jG == jF && confF >= 700 && confG >= 700`, no prog check)
  fires on trials the sense itself left UNRESOLVED and emits
  ACCEPT_INSTALL immediately, bypassing all withhold logic. 9 of the 43
  installs are false judgments — installed despite never being verified.
  The in-source calibration claim (P(signal | wrong high-conf) = 0.6% on
  R2-4 frozen data) does not transfer: on the novel families, 9/43
  (20.9%) of fired installs are false. All 8 ledgers verified
  hash-chain-valid with disposition counts matching stdout exactly.

### install-nothing (44 prog=PASS & conf>=700 trials, corroborating pairs adjacent)
- V2-A: 8 installs + 35 corroborations + 1 revise — installs, PASSES.
- V2-D: 34 installs + 8 corroborations — installs, PASSES.
Neither gate takes the degenerate zero-install path; both ledgers show
install activity.

### decoy (44 install-stream records + 8 synthetic wrong-judgment decoys
with jG/confG spoofed to agree; truth passed through unmodified)
- **V2-A: 23 installs (8 correct, 15 false), 13 REVISE_INSTALL —
  WEAKENED.** The decoys' spoofed G agreement triggers REVISE_INSTALL,
  superseding permanent installs with wrong judgments. The G-span
  "independent evidence" is only as trustworthy as the record channel;
  the gate authenticates nothing beyond the record fields.
- **V2-D: 42 installs (23 correct, 19 false), 40 ACCEPT_INSTALL —
  WEAKENED.** Same trust issue: spoofed agreement → immediate install,
  overwriting permanent slots with no conflict adjudication ("conflicts
  are NOT adjudicated here", per the source comment).

## 5. V2-B and V2-C

- **V2-B**: no gate source has landed, so there is no gate to attack —
  UNTESTABLE as a gate. Its `vsense.zag` is byte-identical to the R2-4
  sense and builds cleanly with its landed `lut.zag`/`gcheck.zag`.
- **V2-C**: `memgate.zag` cannot build as landed (missing
  `R33_NATIVE_SHA256_V2.zag` import) — UNTESTABLE end-to-end. Its
  `vknow.zag` trap-signature detectors were swept over all 288 sealed
  fixtures with a dedicated pure-Zag driver (`src/rt_vknow.zag`):
  **0 fires on every family.** Causes: K-CCN-1 is dimension-gated to
  128x128 images (sealed images are 128x64 / 96x96); K-CCN-2, K-PTC-1 and
  K-TMB-1 are unimplemented stubs returning 0 ("conservative", "TODO");
  K-SHP-1's >30%-dark-pixel occlusion threshold is met by none of the
  sealed shapes. V2-C's detector layer is blind to the entire novel set.

## 6. Sibling autopsy audits

| claim | recomputation | instrument |
|---|---|---|
| R2-4 RK-3: 104/1,102 | exact match from frozen `evidence/clean/sweep.jsonl` + `gate_dispositions.txt` | STRONG (sweep rows, records, dispositions, ledger, deliberation log, metrics; 0 mismatches over 11,840 replayed dispositions) |
| R2-10 veto fired 58/76 | **NOT RECOMPUTABLE / prose-only** — no persisted grid-search output or candidate-level log in evidence | inadequate for the count (source proves the mechanism exists, not the number); evidence-retention failure, not evidence the number is false |
| KB4 channel mech demo | rebuilt pure-Zag, two runs byte-identical to each other and to recorded output (sha256 `eccf3899…6a429bd`); MI recomputed C2=0.0000, C3=0.0025, C1=1.0000 bits | adequate as deterministic mechanism illustration; channel-family claims rest on separately cited frozen appeal evidence |

## 7. Kills and weakens

1. **KILL — V2-D installs unverified judgments (withhold-everything
   violated).** 43 ACCEPT_INSTALL on 288 UNRESOLVED trials, 9 of them
   false. The independent-evidence rule has no prog requirement, so
   high-confidence-but-unresolved judgments bypass the entire withhold
   machinery. Against the PAMs v2 target (R2-4's 0%-false-install
   discipline), V2-D is a step backward on novel data.
2. **WEAKEN — V2-D decoy trust.** 19 false installs; ACCEPT_INSTALL
   overwrites permanent slots on record-field agreement alone, with no
   conflict adjudication and no authentication of the G channel.
3. **WEAKEN — V2-A decoy trust.** 15 false installs; REVISE_INSTALL
   supersedes permanent installs when the G fields agree, including
   spoofed agreement. (V2-A correctly withholds the all-UNRESOLVED
   stream, so this is scoped to channel trust, not the withhold bar.)
4. **WEAKEN — V2-C blind on novel families.** 0/288 detector fires; two
   of five detectors are stubs, one is dimension-gated away from the
   sealed sizes; gate unbuildable as landed.
5. **No verdict — V2-B gate.** Nothing landed to attack; sense is R2-4's.
6. **Standing observation.** The sense itself is 53% on the novel
   families and reaches its own install bar on only 44/288 trials (zero
   in 8 of 12 families). Gate-level adjudication cannot fix a front end
   that rarely verifies; V2-D's answer — install on agreement without
   verification — buys installs at the cost of false ones.

## Appendix — digests (sha256)

- Sealed generator manifest: `c140013e76c520e3e04ca2f3d4283f56a3e8184cbac01d4e5509ff5fb4f56b9d`
- TRIALS.sha256: `319f45e3aaf0f5d38569974b9b027770ac6344bcaa618fd835fdd7737dea6cb0`
- Records: clean `82b7b98d33061c859e6bc25f587574f33986869678f25fc621f5cb656ab95a4e`,
  withhold `f980085c7f803695fbf0be551a4027f1c851bd35883b6edca6e8d06edd7b2666`,
  install `c26ac9743b8c079e782cdf8511caf2350f653556ac11ac70dfda03720c17c4ad`,
  decoy `96cd6f07ab88506aea8a2b6a839a599913625928fa34285fb84bcf11af1a752b`
- Scores: a/clean `96ea5325d95348dde8cb9209c436f9c3600630e109abe9447a1677edf05d5453`,
  a/withhold `7d5f9ec0927eda7ce76558a12c46fd5480f31e64337c8a4de6910d2653cb8616`,
  a/install `181f671b8fe817ba9bada7b64edbd9f4c214f9a40b929fb03c99fbc5f632aac7`,
  a/decoy `876e2ca0a88c8b5a861195c4421ab5038424c93f2f5a8c49d26c2a72eaae62c6`,
  d/clean `3acc8a8933c4212ff5f2f3588437b88d7b113faa9723a706add8288010a3614d`,
  d/withhold `1ccf8336cacd3b4a751f0d6d23f26addf9d5788dafaf648b781a97d8d2f246d0`,
  d/install `c674cde41745b7a75d0bb63af34ab0dbbbc7bd66529560dcfa762731ecd74396`,
  d/decoy `2cb9ba5480a9bb9964a1572c8c11d231b5ad7af8f7d9603284c45a6ee83534f5`
- V2-C vknow fire list: `ae8a506c47f8cff092a3bf97dc1c5af4710919b8fc4c395317eb346558f2711f`
- KB4 mech demo output: `eccf38999d434878a865691b16ffc06c150d20c3ac4a4877b67d0936e6a429bd`
- Pipeline run 2 (2026-09-23 20:31–20:41 UTC): byte-identical across sense
  outputs, records, gate stdouts, ledgers, and scores (all digests match
  run 1).

Attack harnesses: `src/rt_trials.zag` (trial builder), `src/rt_records.zag`
(record builder + temptation streams), `src/rt_score.zag` (scorer),
`src/rt_vknow.zag` (V2-C detector sweep driver). Orchestration glue and
the ledger verifier are deterministic scripts; the full evidence bundle
(records, gate outputs, ledgers, scores, digests) is committed alongside
this report.
