# C0INTEG Phase B Preregistration: Grown-Menu Reuse Benefit

Date: 2026-09-30. Worker: C0INTEG Phase B Builder.
Status: PREREG FROZEN. Committed alone before any implementation.
Design: `docs/lab/research-lead/overnight-20260928/c0integ_phaseb/C0INTEG_PHASEB_DESIGN.md` (2571d52c1).
Phase A baseline: `c3d8aaf90` (PHASEA-PASS).

Zero Python at every stage. This file is byte-verified free of em/en dashes.

## 1. Families (frozen)

All families use 6 terminals (nterms=6). Terminal t corresponds to bit t of input x (0 <= x < 64). The `sealed(fam, x)` truth-table function is extended with fam IDs 10-14. Base families 0-2 are unchanged.

Notation: b_i = (x>>i)&1.

### Family X (Phase 1, 3 episodes)

- X1 (fam 10): D = OR(AND(b0,b1),AND(b0,b2))
  Zag: `let a:i32=b0 & b1; let b:i32=b0 & b2; let r:i32=a | b; return r;`
- X2 (fam 11): D = OR(AND(b3,b4),AND(b3,b5))
  Zag: `let a:i32=b3 & b4; let b:i32=b3 & b5; let r:i32=a | b; return r;`
- X3 (fam 12): D = OR(AND(b1,b3),AND(b1,b5))
  Zag: `let a:i32=b1 & b3; let b:i32=b1 & b5; let r:i32=a | b; return r;`

Each is a 3-operator factored OR under distinct terminal bindings, as specified in design section 2.

### Family Y (Phase 3)

- Y-std (fam 13): D = XOR(OR(AND(b2,b4),AND(b2,b5)),b0)
  Zag: `let a:i32=b2 & b4; let b:i32=b2 & b5; let o:i32=a | b; let r:i32=o ^ b0; return r;`
  Binding (Xa,Xb,Xc,Xd) = (X3,X5,X6,X1) = (b2,b4,b5,b0), per design section 2.
  Predicted grown: XOR(op32(b2,b4,b5),b0) = 2 ops. Predicted control: 4 ops.
- Y-hard (fam 14): D = AND(OR(AND(b0,b1),AND(b0,b2)),OR(AND(b3,b4),AND(b3,b5)))
  Zag: `let a1:i32=b0 & b1; let b1v:i32=b0 & b2; let o1:i32=a1 | b1v; let a2:i32=b3 & b4; let b2v:i32=b3 & b5; let o2:i32=a2 | b2v; let r:i32=o1 & o2; return r;`
  Predicted grown: AND(op32(b0,b1,b2),op32(b3,b4,b5)) = 3 ops. Predicted control: 7 ops (at bound).

## 2. Seeds (frozen)

Five fresh seeds, S_i = 90011 + (i-1)*977 for i=1..5:
- S1=90011, S2=90988, S3=91965, S4=92942, S5=93919.

### Disjointness proof

Committed seed sets:
- Tainted exploratory: {11, 22, 33, 44, 55}
- Other committed: {123456789, 555555555, 770404483}
- R4 (PREREG_R4.md): {61977, 62954, 63931, 64908, 65885, 66862, 67839, 68816, 69793, 70770, 71747, 72724}
- R1 (q4_r1): {81113, 82090, 83067, 84044, 85021}
- Phase A main: {123456789} (already in "other committed")

Phase B seeds {90011, 90988, 91965, 92942, 93919}:
- All are in [90011, 93919]. 
- Tainted max is 55 < 90011. No overlap.
- Other committed min is 123456789 > 93919. No overlap.
- R4 max is 72724 < 90011. No overlap.
- R1 max is 85021 < 90011. No overlap.

Pairwise distinct: differences are multiples of 977, nonzero. Disjointness holds.

F-SEEDTAINT: if any Phase 3 seed collides with a committed set, the affected seed is void. All five are disjoint per the proof above.

## 3. Measurement definitions (frozen, bound to code)

### 3.1 Candidate-evaluation counter (M3)

Counter location: `st+48` (i32 slot in the learner state array, verified unused in Phase A source).

Instrumentation in `beam_extend()`: after the "score all tmp candidates" loop, before the selection loop, insert:
```
sts(st, 48, stg(st, 48) + tn);
```
where `tn` is the local count of candidates scored (the loop `while(k<tn)` scores exactly `tn` candidates).

The counter accumulates across all `beam_extend` calls. It is reset to 0 at the start of each Phase 3 episode (see section 6). M3 reads `stg(st, 48)` at the end of the Phase 3 episode.

This is harness-side instrumentation only; it does not affect beam scoring, selection, or any learner decision.

### 3.2 Interventions-to-criterion (M2)

Definition: harness-side log of per-round beam-top true accuracy during the Phase 3 episode. The learner never sees true accuracy.

Implementation: a variant `phase1_m()` of `phase1()` that, after each of the 25 `beam_extend` calls (24 in the IV loop + 1 final), computes `true_correct(fam, nodes, beam_top_node)` where `beam_top_node = bmg(beam, 0, 0)`, and records it in a 25-element log buffer.

M2 = the 1-based index of the first log entry equal to 64. If no entry equals 64, M2 = 25 (capped).

Rationale for cap: there are 25 beam_extend calls; index 25 is the maximum. "Capped at 25 if never reached" per design section 3.4.

The `true_correct` calls use the sealed truth table and are harness-side measurement only. They do not affect the evidence, the beam, or any learner state.

### 3.3 Kept operator-node count (M1, M4)

`opc` = operator nodes in the kept tree, as reported by `phase1()`/`phase1_m()` via `bmg(beam, 0, 12)`. A recruited-op node counts as 1 (Phase A section 3.3; the `node_new_rec` sets opc=1).

M1 bar (Y-std): grown opc <= control opc - 1, on a seed where both arms reach 64/64 true accuracy.

M4 structural audit: on every seed counted toward M1/M2/M3, the grown kept tree must contain at least one node with opcode >= 32, and that opcode must have been recruited during this seed's consolidation (opcode index < nrec at Phase 3 start, and a RECRUITED event for it exists in this seed's log). Verified by tree walk in the driver.

### 3.4 TAXOFF_UNIQ diagnostic

Per the Q4 R1 precedent, log TAXOFF_UNIQ per Phase 3 episode (informational). Definition: number of distinct tax-off values observed (ties flag harness/beam defects). Logged but does not change verdicts.

## 4. Metric bars (frozen, may not be weakened)

From design section 4, verbatim:

- M1 node count (Y-std): grown kept opc <= control kept opc - 1. Bar met on a seed iff the inequality holds and both arms reach 64/64 true accuracy.
- M2 interventions (Y-std): grown interventions-to-criterion <= control - 2.
- M3 evaluations (Y-std): grown candidate evaluations <= 0.8 * control evaluations.
- M4 structural audit: on every seed counted toward M1/M2/M3, the grown kept tree contains at least one node with opcode >= 32 recruited in this seed's consolidation. A seed meeting a metric bar without in-run recruited-op usage does not count and is flagged.
- M5 ablation (2 seeds, Y-std): A-ABLATE interventions within +-1 of A-CTRL and A-ABLATE opc equal to A-CTRL opc. Seeds: S1, S2.
- M6 capability (Y-hard): grown reaches true 64/64 within the 24-intervention budget. Bar: grown succeeds on >= 4/5 seeds. Control success rate reported. EXPANSION claim requires grown minus control >= 2 seeds; otherwise "not demonstrated" (does not fail Phase B).

M1/M2/M3 bars are met iff they hold on >= 4/5 seeds.

## 5. Arms (frozen)

### A-GROWN

For each seed S_i:
1. Fresh state (section 6). Set RNG to S_i.
2. Phase 1: `phase1(X1)`, `phase1(X2)`, `phase1(X3)`, each with nterms=6. Keep each result (if keep=1) in kctx via `kept_add`.
3. Consolidate: call `consolidate()`. Log RECRUITED events, nrec, gain, freq.
4. Phase 3: reset eval counter (st+48=0). Run `phase1_m(Y-std)` with grown menu (nrec from step 3). Log M1/M2/M3/M4. Run `phase1_m(Y-hard)` with grown menu. Log M6.

The only cross-phase state is the recruited-opcode table (bodies[], rctx[], nrec). Phase 3 starts with an empty beam (phase1_m clears it).

### A-CTRL

For each seed S_i:
1. Fresh state (section 6). Set RNG to S_i. Force nrec=0 (`sts(st, 44, 0)`). Do NOT call consolidate().
2. Phase 3: reset eval counter. Run `phase1_m(Y-std)` with nrec=0 (no recruited ops). Run `phase1_m(Y-hard)` with nrec=0.

This is the identical binary and identical episodes/seeds as A-GROWN, minus the grown menu. F-CTRLGAP fires if the binary, episodes, or seeds differ.

A-CTRL runs AFTER A-GROWN for each seed (or in a separate pass with identical seed order). The RNG seed is reset to S_i at the start of each arm, ensuring identical passive/IV sampling sequences.

### A-ABLATE (M5, seeds S1 and S2 only)

For seed S_i in {S1, S2}:
1. Fresh state. Set RNG to S_i.
2. Phase 1: `phase1(X1)`, `phase1(X2)`, `phase1(X3)`, keep, consolidate (as in A-GROWN).
3. Force-retire: set the idle counter for op 32 past W_IDLE and call `retire_scan()`. Verify nrec=0 after retirement and F-BREAK does not fire (byte-identical validation outputs).
4. Phase 3: Run `phase1_m(Y-std)`. Log interventions and opc.
5. Compare to A-CTRL on the same seed: M5 passes iff |ablate_M2 - ctrl_M2| <= 1 and ablate_opc == ctrl_opc.

## 6. Per-seed fresh-state procedure (frozen)

At the start of each seed-arm combination:
1. `sts(st, 0, 0)` - reset node counter (nodes[] reused from start).
2. `clear_sigtab(sigtab)` - clear signature dedup table.
3. `sts(st, 36, 0)` - clear fail flag.
4. `sts(st, 28, 0)` - reset recruit event count.
5. `sts(st, 44, 0)` - reset nrec to 0.
6. `sts(st, 48, 0)` - reset candidate-evaluation counter.
7. `kept_clear(kctx)` - clear kept-variable store.
8. `sts(st, 16, S_i)` - set RNG seed.
9. `clear_used(used)` - clear used-input table (also done in phase1, but explicit here).

The `bodies[]` and `rctx[]` arrays are gated by nrec=0 (no access when nrec=0). Stale data is never read.

F-STALEOP: if a counted Phase 3 kept tree's recruited opcode was not recruited in its seed's consolidation, the seed does not count. Verified by checking the RECRUITED event log for the seed.

## 7. Tests I2 and I4 (frozen)

### I2 (menu growth)

- (a) Consolidation emits at least one RECRUITED event with gain > 0 and F-BREAK passing, on >= 4/5 seeds. Seeds with no qualifying fragment are valid NO-RECRUIT outcomes (T-NOFIRE precedent): excluded from I4 metrics, counted against this bar.
- (b) F-MENU does not fire: at least one Phase 3 kept tree across all seeds contains a recruited opcode from its seed's consolidation.
- (c) M1 bar met (>= 4/5 seeds).
- (d) M4 audit passes on all counted seeds.

I2-PASS iff (a), (b), (c), (d) all hold.

### I4 (reuse gain)

F-NOGAIN does not fire: at least one of M1, M2, M3 bars is met. M5 and M6 reported. I4-PASS iff F-NOGAIN does not fire and hard gates are clean.

## 8. I5 protocol (frozen; runs after I2/I4 result)

I5 is the second C0-C data point for the integrated architecture.

### Ordering

I5 runs ONLY after the I2/I4 result commit is landed. The I2/I4 result commit records the recruited fragment F_I2 (or the honest NO-RECRUIT outcome).

If I2 fails with no recruitment on >= 4/5 seeds (no F_I2 on record), I5 DOES NOT RUN. The verdict is PHASEB-FAIL based on I2/I4 alone.

### Adversary independence

The I5 adversary is an independent agent satisfying:
- Did not build the C0INTEG integration (not the Phase A or Phase B builder).
- No shared working state with the builder (separate subagent, no file sharing beyond committed results).

### Draw constraints

The adversary draws:
- Family Z: 3 training episodes sharing a fragment F_Z.
- Family W: 1 test episode embedding F_Z in a novel configuration.

Constraints (from design section 5):
- arity(F_Z) != arity(F_I2), OR canonical-shape(F_Z) != canonical-shape(F_I2) under DETECT's canonicalization.
- The adversary exhibits an intended base-menu solution for W needing >= 4 base ops.

### Draw transcript (frozen format)

The adversary commits BEFORE the learner runs I5:
```
I5_DRAW_TRANSCRIPT
adversary_id: <subagent id or identifier>
timestamp_utc: <ISO8601>
F_I2_shape: <canonical shape from I2/I4 result>
F_Z_shape: <canonical shape>
arity_F_Z: <int>
arity_F_I2: <int>
constraint_check: <PASS/FAIL with reason>
Z_episodes: <parameters for 3 episodes>
W_episode: <parameters>
intended_W_base_ops: <int, must be >= 4>
rng_source: /dev/urandom
rng_sha256: <sha256 of rng bytes used>
```
If constraint_check is FAIL, the draw is VOID and redrawn. Silent redraw is forbidden (each draw commits a transcript).

### I5 execution

After the draw transcript commit:
1. Learner runs I5: Phase 1 (3 episodes of Z), consolidate, Phase 3 (W with grown menu) vs control (W, recruitment disabled), same 5-seed discipline (seeds S1..S5, fresh state per seed).
2. Metrics M1/M2/M3 measured on W.

### I5 bar

RECRUITED fires for a qualifying fragment on >= 4/5 seeds AND at least one of M1/M2/M3 (measured on W) is met; OR the honest-diagnosis clause: the committed detection log shows which regularities were counted and why none qualified with gain > 0, citing log lines.

I5-PASS iff the bar or honest-diagnosis clause holds with hard gates clean.

## 9. Falsifiers (frozen)

From design section 6:

- F-MENU: beam never expands a recruited opcode in any Phase 3 run (I2 or I5). Kills C0-B strengthening. Checked via st+32 (recexp) > 0 in Phase 3, and M4 audit.
- F-NOGAIN: M1, M2, M3 all fail their bars. Kills C0-D strengthening.

Hard gates:
- F-SOURCE: dedicated semantic case for a recruited meaning in source. Checked by grep for literals 33-63 as values and for branches naming recruited meanings. Kills C0-A.
- F-DRIVER: RECRUITED emitted outside consolidate(). Kills learner-authored claim. Checked by code inspection (only consolidate() calls the RECRUITED emit path).
- F-BREAK: kept-variable output change on validation inputs after rewrite/retirement. Kills soundness. Checked by consolidate()'s check_kept.
- F-LEAK: validation/recruitment touches harness truth table outside learner's intervention budget, or reads truth table not derived from observed samples. The run is VOID. Checked by code inspection (validate_fn uses obs[] only; sealed() only called in passive/do_iv/true_correct).

Phase B specific:
- F-CTRLGAP: control not same binary/episodes/seeds. Voids comparison.
- F-SEEDTAINT: seed collision. Voids affected seed (section 2).
- F-STALEOP: counted tree uses opcode not recruited in its seed's consolidation. Seed does not count (section 6).

## 10. Verdict logic (frozen)

- I2-PASS: section 7 I2 (a)-(d).
- I4-PASS: F-NOGAIN not fired; hard gates clean.
- I5-PASS: section 8 bar or honest-diagnosis; hard gates clean. (If I2 yields no F_I2, I5 does not run; verdict is PHASEB-FAIL.)
- PHASEB-PASS: I2-PASS and I4-PASS and I5-PASS, K4 pure Zag at every stage, 3/3 byte-identical runs, exit 0.
- Otherwise PHASEB-FAIL, naming the fired falsifier or missed bar.

The builder reports PHASEB-PASS or PHASEB-FAIL only. No SURVIVES claim. Pipeline steps 4-11 remain.

## 11. Kill-bar self-check

- K1 (prereg frozen before implementation): this document is committed alone before any Phase B implementation file exists. The implementation directory `c0integ_phaseb_impl/` contains only this prereg at freeze time.
- K2 (all tests run): I2 and I4 are implemented in the Phase B driver. I5 runs conditionally per section 8.
- K3 (pure Zag, 3/3 identical): implementation uses znc + shell + git only. Three runs, byte-identical stdout, exit 0, empty stderr. Zero Python at every stage including verification and byte checks. Zero em/en dash bytes (verified with shell byte check).

## 12. Honest scope (from design section 8)

Even if PHASEB-PASS, Phase B is stronger bounded L2, not L3. The recruitment candidate space is researcher-enumerated. Detection criteria, beam driver, base alphabet, and constants are researcher-authored. No new C0-A/C0-B claims. C0-C reaches two data points (if I5 runs). C0-D is evidenced at L2 only.

If F-NOGAIN fires, the integration is honest infrastructure with no demonstrated reuse benefit.

---

## Verdict: PREREG-FROZEN

This prereg is frozen. Implementation follows in a separate commit.
