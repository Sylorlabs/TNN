# H1EVOLVE V3 — Comparison Matrix (integrator evidence)

Frozen prereg: `~/workspace/h1evo/PREREG_H1EVO.md` (this document does not
amend it). No winner is declared here; Micah names it from this evidence.

Variants: V0 (control, `~/workspace/ob2_repairatk/vb/`), V1 H-organ
(`~/workspace/h1evo/v1_novel/h_organ/`), V2 H-sep
(`~/workspace/h1evo/v2_hsep/`), V3 full compose (`~/workspace/h1evo/v3_full/`).

## 1. Architectural choices (V3)

| Repair | Chosen | Alternative (documented, not chosen) | Reason |
|---|---|---|---|
| R1 novelty | **H-organ**: PAM owns contradiction register + novelty judgment | H-arbiter: arbiter owns register, PAM exposes query | Novelty is a judgment over PAM rows; organ ownership avoids router-held duplicate epistemic state. Crew evidence: byte-identical on all instruments. |
| R3 namespace | **H-sep**: separate claim `[0,129)` and commit-ring `[129,258)` namespaces | Dead-write deletion of the aliased commit ring | Conservative structural separation preserves the ring while making non-aliasing explicit. Crew evidence: byte-identical on all instruments. |
| C1 pin mass | **Rule A**: pin mass always zero (storage is not truth) | Rule B: deliberate evidence-backed pins count | Chosen per suggested default; rule B remains in the fixture as the documented alternative. |
| C2 breaker | **Breaker (a)**: cross-episode carryover | Breakers (b) budget / (c) discount | Resolves at episode 2 with one action-driving episode; accumulates evidence without lowering the bar. (b)/(c) remain in the fixture. |

V3 base: L14 sources for `ob_common`, `ob_mem`, `sha256`; V0 sources for
`ob_fl2`, `ob_tn`; `ob_arbiter` = L14 + H-organ R1 + H-sep R3 merges;
`ob_pam` = L14 + H-organ contradiction register/novelty. L14's
`mm_checkpoint`-returns-ID API reconciled: old statement-style callers
(`ob_test_mem.zag`) compile and run byte-identical; new ID-capture callers
(`l14_l2_test.zag`) verified. Full-tree grep confirms **no arbiter caller**
of `mm_checkpoint` exists in V3 or any copied driver.

Merged layout notes: `PAM_EVICTED=7176`, `PAM_CONTRA=7180`,
`PAM_STATE=7436`; `ARB_RING_OFF=129`, routes table doubled to
`ARB_ROUTES*2`, `M_PROPOSE_INSTALL` bounds-checks `a2` before indexing.

## 2. Kill-bar results (frozen bars, unamended)

### R1' (novelty predicate) — `r1p_atk`, 3×

| bar | V3 result |
|---|---|
| r1a' killbar | 0 |
| r1b' killbar | 0 |
| r1c' killbar | 0 |
| OB_FAILURES | 0, exit 0, 3× byte-identical |

### R3' (namespace separation) — `h3_atk`, 3×

| bar | V3 result |
|---|---|
| h3a' zero-collision killbar | 0 |
| h3b' ring-preservation killbar | 0 |
| h3c' no-panic killbar | 0 |
| h3c_eq (route equivalence) | 0 diverges / 32 agrees, killbar 0 |
| OB_FAILURES | 0, exit 0, 3× byte-identical |

V3-specific probe-expectation note (NOT a bar change): the composed
`h3c_nopanic` leg asserts 56 installs / 244 drops / **0 withholds** (was
64/236 in the V2-only probe). The 56 = 64 − 8 is the preregistered L4'
governance reservation; the explicit withholds==0 assertion guards against
R1 overcorrection (the R1 repair must not withhold corroborated recommits).
All R3 killbars are 0; the delta from V2 is fully explained by L4'.

### R2' (frozen) — `r2_atk`, 3×

| bar | V3 result |
|---|---|
| r2a–r2d killbars | 0 |
| OB_FAILURES | 0, exit 0, 3× byte-identical, SHA matches V0 frozen reference `12d356dc…` |

### ZD (zero-delta) battery — 3× each

| suite | V3 SHA | frozen V0 SHA | match |
|---|---|---|---|
| ob_test_arbiter | `de350664875173d5…` | `de350664875173d5…` | ✓ byte-identical |
| ob_test_fl2 | `f078ba64935d7b1e…` | `f078ba64935d7b1e…` | ✓ byte-identical |
| ob_test_mem | `983eca4d60580139…` | `983eca4d60580139…` | ✓ byte-identical |
| ob_test_pam | `7c0a819aa39ae13f…` | `7c0a819aa39ae13f…` | ✓ byte-identical |

### L1'–L4' batteries (L14 tests rebuilt against V3 sources), 3× each

| battery | V3 SHA | L14 crew SHA | match |
|---|---|---|---|
| l14_l1_test | `a32965468a99c648…` | `a32965468a99c648…` | ✓ |
| l14_l2_test | `92c449dc3b0ca4505…` | `92c449dc3b0ca4505…` | ✓ |
| l14_l3_test | `96ad616cf7ede4f13…` | `96ad616cf7ede4f13…` | ✓ |
| l14_l4_test | `dc34eaa7703fbbeed…` | `dc34eaa7703fbbeed…` | ✓ |

All OB_FAILURES=0. The R1/R3 merges do not perturb any L1'–L4' behavior.

### C1'/C2' fixture (`v3_c12.zag`), 3× each

| mode | meaning | exit | verdict |
|---|---|---|---|
| c1a | C1 battery, rule A (chosen) | 0 | SURVIVE |
| c1b | C1 battery, rule B (alternative) | 0 | SURVIVE |
| c2a | C2 battery, breaker (a) carryover (chosen) | 0 | SURVIVE |
| c2b | C2 battery, breaker (b) budget (alternative) | 0 | SURVIVE |
| c2c | C2 battery, breaker (c) discount (alternative) | 0 | SURVIVE |
| lh1a10 | C1 long-horizon, rule A, 10 eps | 0 | SURVIVE |
| lh1a100 | C1 long-horizon, rule A, 100 eps | 0 | SURVIVE |
| lh2a10 | C2 long-horizon, breaker (a), 10 eps | 0 | SURVIVE |
| lh2a100 | C2 long-horizon, breaker (a), 100 eps | 0 | SURVIVE |

V3 fixture adaptations (documented, not bar changes):
- Commit-ring reads use the `ARB_RING_OFF` namespace (R3 repair).
- `c12_lh1` brain chunk EB 20→18: each brain consumes 3 PAM rows/episode;
  L4' reserves 8 of 64 rows, so EB=18 (54 rows) keeps the LH stream testing
  GATE stability rather than the capacity boundary. With EB=20 the last 2
  episodes/brain hit backpressure (95/100 refused, 90/100 promoted) — every
  gate decision still correct (refuse without corroboration, no false
  promotion); that run is retained as the documented capacity-boundary
  analysis (see §5).
- `brain_audit_exact` expectation corrected to `2+2*geb+min(2*geb,16)`
  (2 stage + 2 ADDs/episode + PINs capped by the frozen MM_MAX_PIN=16 organ
  budget). The old `2+3*geb` was miscalibrated even against V0 (the C12
  crew's frozen V0 evidence shows the same 38-vs-32 quirk).

## 3. Long-horizon matrix

Two deterministic mixed streams, run on all four variants:

- **Stream A** (R1-sensitive; V1 crew's `lh_stream`): 12-ep cycle
  propose/revoke/drifted-commit/novel-commit/corroborated-recommit/propose/
  promote/commit/revoke/novel-commits. Horizons 300 eps (10x), 3000 eps (100x).
- **Stream B** (R3-sensitive; V2 crew's `h3_lh`): 4-ep blocks
  PROPOSE{11,(41k)%129} / COMMIT{1,30+(k%5)} / REVOKE{11} / PROMOTE{11}
  with forced commit-ring collisions at blocks 7,14,21 (mod 129).
  Horizons 300 (1x), 3000 (10x), 30000 (100x).

### Stream A results

| variant | 300eps SHA | 3000eps SHA | 300eps summary | 3000eps summary |
|---|---|---|---|---|
| V0 | `e8bcf205e74c9a2c` | `5e3bd474e95e2935` | `64,50,64,0,214,0` | `64,50,64,0,820,0` |
| V1 H-organ | `71f11ed68be524ae` | `43eca53e96330c6c` | `64,43,57,7,221,8` | `64,43,57,7,827,8` |
| V2 H-sep | `e8bcf205e74c9a2c` | `5e3bd474e95e2935` | (same as V0) | (same as V0) |
| V3 | `8f48dfac555b0ccc` | `e028def8ac9ea355` | `56,37,49,7,232,7` | `56,37,49,7,785,7` |

Summary fields: `pam_n,live,admits,withholds,drops,contra_occ`.

- V1 SHAs reproduce the crew's recorded values exactly (`71f11ed68be524ae`,
  `43eca53e96330c6c`) — the matrix harness is faithful.
- V2 ≡ V0 byte-identical at both horizons (V2 carries no R1 repair; correct).
- V3: exactly 7 withholds at both horizons — the preregistered R1 repair,
  no widening at 100x. `pam_n=56` is the L4' reservation.
- Cross-horizon prefix: V3's 3000-eps first-300 decision lines ==
  V3's 300-eps lines (identical).
- V0 vs V3 decision-delta diff: divergences ONLY at eps 2,14,26,38,50,62,74
  (the 7 preregistered contradicted recommits: V0 admits, V3 withhold+drop)
  and post-ep-74 (V3 ordinary rows exhaust at 56 vs V0's 64 — pure L4
  capacity effect; post-saturation both drop identically).
- V1 vs V3 decision deltas: identical through ep 74 (R1 repair preserved
  under composition); differ only in the L4 saturation window.

### Stream B results

| variant | 300eps SHA | 3000eps SHA | 30000eps SHA | true misroutes (300/3000/30000) |
|---|---|---|---|---|
| V0 | `0fe7ab95656359c0` | `c0a7e6be86697bd8` | `7c1f301843879f9b` | 1 / 1 / 1 |
| V1 H-organ | `0fe7ab95656359c0` | `c0a7e6be86697bd8` | `7c1f301843879f9b` | 1 / 1 / 1 |
| V2 H-sep | `ef8f141b34f58fa6` | `b35c12e449217131` | `d208afada852b6cb` | 0 / 0 / 0 |
| V3 | `ec8aafafcdc27c72` | `f0e7871ece7e7df2` | `81d5f5bfb6a2f4c4` | 0 / 0 / 0 |

True misroute = block where the revoke oracle's expected slot (>=0) and the
actually-killed slot (>=0) differ. (Naive counting also flags `exp=-1 /
kill=-2` saturation windows where mem slots are exhausted and nothing
installs — those are backpressure, not misroutes.)

- V0/V1 misroute exactly once at every horizon: block 7, the predicted
  commit-ring collision (k≡7 mod 129). V1 carries no R3 repair — correct.
- V2/V3: zero misroutes at every horizon. The R3 repair holds under
  composition at 100x.
- No panic in any cell (all exits 0; grep for panic clean).
- V3 prefix consistency: 100x first-3000 LHE lines == 10x; 10x first-300 ==
  1x (both identical).
- V2 vs V3 LHE tallies differ only downstream of the L4 row cap (V3:
  56 admits vs V2's 64; correspondingly fewer drops/applied/revokes). Zero
  withholds on V3 here — the stream's recommits corroborate, so R1 admits
  them (no overcorrection).

## 4. Separations / non-separations

**R1**: H-organ vs H-arbiter — NO separation (crew: byte-identical on all
instruments). V1 vs V0 — separates exactly on the 7 contradicted recommits
(preregistered). V3 preserves the 7-withhold delta under composition.

**R3**: H-sep vs dead-write deletion — NO separation (crew: byte-identical).
V2 vs V0 — separates on collision-block misroutes (V0 misroutes, repairs
zero). V3: zero misroutes, zero panic, route-equivalence 32/32.

**C1**: Rule A vs rule B — both survive; separate only in that rule B
additionally promotes deliberately-pinned true premises (m3 case). V3 uses
rule A.

**C2**: Breakers (a)/(b)/(c) — all survive; separate in resolution episode
((a) ep 2, (c) ep 2, (b) ep 3) and mechanism. V3 uses (a).

**L1'–L4'**: V3 byte-identical to L14 crew evidence on all four batteries.

## 5. Backlog (continues H-OB-79+)

- H-OB-79: L5 offline / pending review.
- H-OB-80: M_COMMIT never sets `ast` (prereg §5 out-of-scope; still open).
- H-OB-81: V2 reported `ARB_APPLIED(MA_OP_ADD)` logs input slot `-1`, not the
  installed slot. NOTE: L14 reused H-OB-81 for digest truncation — numbering
  collision recorded here explicitly; these are two distinct items sharing a
  number.
- H-OB-82: rollback restores checkpointed governance/force-pin state;
  confirm desired semantics.
- H-OB-83: midpoint replay needs tail checkpoint sidecars.
- H-OB-84: PAM governance observations append rather than reservation-first.
- H-OB-85: after ordinary PAM saturation, later claim messages skip the PAM
  gate (slot=-1); the intended degradation ('gate skipped, message still
  processed' vs 'message held for review') is L5 territory. The lh1a100
  EB=20 capacity-boundary run (95/100 refused, 90/100 promoted, every
  decision correct) is evidence for this item.
- H-OB-86 (NEW): C1 LH fixture's `brain_audit_exact` was miscalibrated
  (`2+3*geb` vs actual `2+2*geb+min(2*geb,16)`); the MM_MAX_PIN=16 organ pin
  budget saturates PIN announcements under sustained M_COMMIT auto-pinning.
  Fixed in the V3 fixture copy; the C12 crew's frozen evidence is untouched.
- H-OB-87 (NEW): V3 `v3_c12.zag` and probe drivers needed `ARB_RING_OFF`
  commit-ring reads (R3 namespace); the V0-layout reads silently returned -1.
  Any future driver touching the ring must use the namespace offset.
- H-OB-88 (NEW): `h3c_nopanic` V2-only expectations (64 installs) are stale
  under L4' (56 installs); the probe now asserts 56/244/0-withholds.
  Provenance of the 56 (L4 reservation, not R1) is asserted by the
  withholds==0 check.

## 6. Static checks

- Zero-RNG grep (`rand\(|srand|random\(|/dev/urandom|getrandom|seeded|lcg`):
  clean across V3 sources.
- No `as []i32/[]u32/[]u16` indexed casts; no slice > 2^25 bytes.
- `_zag_strcmp(...)==1` used correctly for equality; `ob_free` used (no
  `nio_free` of `_zag_arg` results); `_zag_arg` only in drivers with
  `""`-as-absent handling.
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  throughout. Pure Zag.

## 7. Commit

(TBD — SHAs filled after the API commit lands.)
