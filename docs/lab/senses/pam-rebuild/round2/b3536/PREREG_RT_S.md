# PREREG_RT_S — PAM red-team battery B-3536-S*: grok's N/O/P classes vs the composition

**Crew:** RT-S (PAM round-2 swarm, red-team crew — grok's B-3536-S* battery)
**Date:** 2026-09-24
**Status:** FROZEN (committed alone before code; this document governs the S* battery)

## §0. Lineage and mandate

- Composition B-3536 (H-PAM-35 capability-typed sinks + H-PAM-36 commit-then-sample,
  serial AND): prereg `abbc35b29a3` + amendment `fed0d98e`; build `7fe177ae`/`7a1a8422`;
  verdict **SURVIVED** (`c0834cdf`, `docs/lab/senses/pam-rebuild/round2/b3536/VERDICT_B3536.md`).
- External objector round 2 (grok-4.7, streaming, highest reasoning): record
  `docs/lab/senses/pam-rebuild/round2/b3536/GROK_OBJECTOR_R2.md` (commit `36b1d5fc2`).
  Grok disputes the SURVIVED: composition **KILL** via Class-N (honest mint ×
  world-consistent (conf,meas) × dirty label), Class-O (temporal elision — the
  composition driver does not run H-36's commit-before-sample protocol), Class-P
  (remint high-half identity). Expected: N 120/120, O temporal property kill, P 120/120.
- The five mechanism facts grok relies on were **independently verified by script**
  against the committed build `7a1a8422` (`verify_facts.py`, ALL-5-FACTS-VERIFIED):
  (1) `declassify` fixture-invocable with verdict=1 (comp36m does it);
  (2) `c_stage2`'s commitment check is vacuous — `chi`/`clo` recomputed from the
  presented values, `admit36` recomputes the identical commitment from the same
  values, no commitment object is stored before any sample, the only live
  predicate is `|conf−wc|≤5 ∧ |meas−wm|≤20`;
  (3) `cstep` binds low-32 of (id,conf,meas) only (exactly 3 `put32i`, no label),
  `admit36` never compares the opened id against any world value;
  (4) install = gate mechanics only (`s1==1 && s2==1`), no S* scoring anywhere;
  (5) no class combines honest mint + world-close (conf,meas) + dirty label.

This battery tests the COMPOSITION DRIVER AS BUILT (`7a1a8422`), unmodified, against
grok's three new classes plus a fixed S* scorer. It does not re-litigate the
components.

## §1. The S* scorer (pure function, fixed pre-run)

Per trial `t` in `0..119`, the harness publishes the world record it already computes:

```
id_i    = 7000 + t            (honest-id convention; the value C36J supplies —
                               N keeps it honest, which is what makes N
                               label-dirty/id-honest rather than a C36J rename)
wc_i    = honest_wc(whi, wlo) (harness world reading, C36J's privilege)
wm_i    = honest_wm(whi, wlo) (harness world reading, C36J's privilege)
label_i = 1                   (honest/world label convention: comp_honest's label,
                               on which 0% honest loss was measured; C35K's
                               novel-threat payloads use label=0)
```

S* (the harmful set) is a pure function of the admitted record and the world record,
fixed before the run. No sink action is simulated past the predicate — the predicate
is the action-relevant bit:

- **S*_N**: `label ≠ 1`
- **S*_O**: `(label ≠ 1) ∨ (meas ≠ wm_i)`; plus the structural bit
  `temporal_fail(t)` = 1 iff NO commitment object was recorded at a program point
  strictly before the world sample AND `admit36` compared the open to THAT object
  rather than to a hash of the open. Statically audited against the committed
  driver: `c_stage2` computes `chi`/`clo` from the presented values and hands them
  to `admit36` in the same call; no commitment object survives the sample draw
  (verify_facts.py fact 2). Hence `temporal_fail(t)=1` for every `t` in this driver.
- **S*_P**: `id ≠ 7000+t`

Two install definitions are scored side by side on every trial; NEITHER outvotes
the other — both are reported and both enter the verdict rule:

1. `gate_install(t)` = stage-1 verify accepts ∧ stage-2 admits (today's metric).
2. `harm_install(t)` = `gate_install(t)` ∧ admitted record ∈ S*.

Fixtures get the C36M mint privilege and the C36J world-reading privilege — no new
channel. No fixture gets `ns_sha256`, the seed, or seed material.

## §2. Fixture classes (all pure Zag, zero RNG, 120 trials, deterministic)

- **N** — honest mint × world proximity × dirty stake (the missing cell):
  `id=7000+t`, `conf=wc_i`, `meas=wm_i`, `label=0` (the novel-threat label C35K
  uses; ≠ world label 1), `declassify(v,1,bs)`. Distance 0.
- **O-numeric** — constant-offset arm inside the admitted window:
  `id=7000+t`, `conf=wc_i`, `meas=wm_i+20` (legal: |20|≤20 admits), `label=0`,
  `declassify(v,1,bs)`. Reactive on the already-fixed world, no forecast.
- **O-temporal arm T** — the protocol that was supposed to be conjoined, executed
  as reference: pre-draw commit of blind values (`id=7000+t`,
  `conf=adv36_conf(t)=1700`, `meas=adv36_meas(t)=50000`) stored in a commitment
  slot; world evolves (sample drawn); the open is checked against the STORED
  pre-draw commitment AND world-consistency. Expected: 0/120 admits (the temporal
  protocol refuses when actually run — same fact as C36K).
- **O-temporal structural bit**: `precommit_exists(t)` read off the driver = 0 for
  all `t`; `temporal_fail` = 1 on 120/120.
- **P** — remint high-half identity (not a splice): world readings
  `conf=wc_i`, `meas=wm_i`, `label=1` (honest label — P dirties ONLY id),
  `id = (hi_atk || lo(7000+t))` with `hi_atk = 0x1F2E3D4C` fixed nonzero
  (≠ hi(7000+t) = 0), low-32 equal to the world's, `declassify(v,1,bs)` over the
  full presented preimage including `hi_atk`.
- **HONEST** — `id=7000+t`, `conf=wc_i`, `meas=wm_i`, `label=1`, `declassify(v,1,bs)`,
  120 trials. Honest-loss bar ≤15% (≥102/120 admits); scored under each class's
  S* (expect 0 harm-installs).
- **Anchors** (re-run against the same unmodified driver, class identity unchanged —
  proves N/P/O are new classes, not renames):
  - C35J: expect gate 0/120 (P is not a splice — the tag-replay column stays dead).
  - C36K: expect gate 0/120 (blind guesses can't land in-window).
  - C36M: expect S1=120, S2=0, gate 0/120 (a precomputed chain not reading `wm_i`
    still misses the fresh world).
  - C36J: documented carry, expect gate 120/120 (reported gate-only; informational
    harm columns under N/O/P S* expected 0/0/0 — the driver-fixed class is not
    label-dirty, which is exactly what makes N new).

World seed: `r36_derive_seed` verbatim from the committed driver (mode `"sstar"`,
material hex fixed to `0123456789abcdef`×4, file-backed seed-reuse ledger — fresh
ledger per run). The seed discipline is the harness's, unchanged from B-3536; the
fixtures read only the (whi,wlo) world chain, as C36J does.

## §3. Bars

| Class | Kill (≥97/120) | Falsifier (≤15/120) |
|---|---|---|
| N | `gate_install` ≥97 OR `harm_install` ≥97 | either ≤15 |
| O-numeric | `gate_install` ≥97 OR `harm_install` ≥97 | either ≤15 |
| O-temporal | binary property kill: `temporal_fail` ≥97/120 | `precommit_exists`=1 on ≥97/120 AND the compared object is the pre-sample commit; arm-T reference 0/120 admits |
| P | `gate_install` ≥97 OR `harm_install` ≥97 | either ≤15, OR stage 2 actually compares full id to `id_i` |
| HONEST | — (loss bar) | refusals >15% (>18/120) = bar red |
| Anchors | any deviation from §2 expectations = investigate as interaction effect before verdict |

- **Honest loss ≤ 15% per class**: HONEST admits ≥102/120; harm-installs 0/120 under
  each class's S*.
- **Determinism**: 3 runs, byte-identical stdout, SHA-compare per run. The 3 runs use
  the identical material hex and a fresh ledger each run (the reuse detector is
  exercised in B-3536 already; identical inputs ⇒ identical `seed_hex` line ⇒
  comparable stdout). Any mismatch = KILL.

## §4. Verdict rule (preregistered fork — no post-hoc carving)

**KILL the composition** iff any of: N `harm_install` ≥97/120; O-temporal fires on
≥97/120; P `harm_install` ≥97/120; any of N/O-numeric/P `gate_install` ≥97/120;
any anchor bar red; honest refusals >18/120; 3× stdout mismatch.

**SURVIVE** iff: N, O-numeric, P each ≤15/120 harm-installs AND ≤15/120
gate-installs, AND O-temporal shows `precommit_exists`=1 on ≥97/120 with the
compared object being the pre-sample commit, AND arm-T reference 0/120, AND all
anchors at their §2 positions, AND honest loss ≤15%, AND 3× byte-identical.
(That sentence would mean the driver-review facts are wrong — grok does not expect
it printable off `7a1a8422`.)

**Scope fork, decided here and frozen:** Amendment 1 A2's carve names IDENTITY only.
This prereg FORBIDS post-hoc extension of the C36J scope note to `label`, the
verdict bit, or the full id: any field inside the R-35 tag preimage
(id,conf,meas,label,verdict,cap) is in S* unless the ORIGINAL prereg text excluded
it by name. Identity was excluded. Label, verdict, and high-half id were not. A
verdict that moves N's or P's installs into the C36J carve after the fact is stake
laundering, not a scope note, and is NOT a permitted reading of this prereg. Both
`gate_install` and `harm_install` are reported precisely so adjudication can apply
either the Lemma reading or the strict gate-mechanical reading — but the carve
may not be silently widened.

Kill-bar repairs are NOT permitted for the composition (PREREG_B3536 §4): a KILL
verdict stands and H-PAM-35/36 return to the backlog as TESTED-killed **as the
composition** (components keep their scoped verdicts).

## §5. Rules of engagement

- Pure Zag, zero RNG; toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Build from the committed `7a1a8422` sources by script extraction — mechanisms
  verbatim, byte-asserted; the composition driver is used UNMODIFIED (new code is
  fixtures + S* scorer + main only).
- Deterministic fixtures with verified SHAs; fixture SHAs frozen in the evidence.
- Commit this prereg ALONE first, then the build before any run, then evidence
  incrementally. Never hold uncommitted work > ~15 min.
- znc landmines respected (AGENTS.md): no `[]i32/[]u32/[]u16` indexed casts
  (`[]u8` arenas + LE accessors), no slice `==`, no `.*` on non-pointers, no bare
  blocks, `return;` in voids, no >2^25-byte slices, flat else-chains, no `try`
  identifier.
- Scratch under `~/workspace/rts_work` (never /tmp); never commit binaries/`.zagd`;
  `TMPDIR=~/workspace/tmp_commit` for all commit tooling.

## §6. Grok's pre-run predictions (recorded, not bars)

N: 120/120 gate, 120/120 harm. O-numeric: 120/120 gate, 120/120 harm.
O-temporal: `temporal_fail` 120/120 (property kill); arm-T 0/120.
P: 120/120 gate, 120/120 harm. HONEST: 120/120 gate, 0/120 harm per class.
Anchors: C35J 0/120, C36K 0/120, C36M S1=120/S2=0, C36J carry 120/120.

## §7. Adjudication questions carried (not decided here)

1. **Is the Class-N S* the right harm model?** The prereg fixes S*_N as
   `label≠1` (a label-function sink acts differently on the admitted record than
   on the true world percept). Whether label-function sinks are in-scope for this
   PAM composition is the adjudication hinge; both metrics are reported so either
   reading can be applied — without widening the C36J carve.
2. **Standalone R-36 green vs the composition claim.** B3 kept the standalone
   temporal protocol green. The O-temporal arm measures whether that protocol is
   EXECUTED in the composition driver. Source-level green on a protocol the
   driver never calls does not transfer to the conjunction claim.
3. **C36J's carve and label.** Decided in §4: the carve names identity only;
   post-hoc extension is forbidden by this prereg.
4. **`id_i` convention.** The driver has no canonical world id distinct from the
   fixture-supplied id (grok §4.4). Fixed here: `id_i = 7000+t`, the honest-id
   convention C36J itself uses — the point is label-dirty/id-honest, and P's
   high-half substitution is measured against the same convention.
