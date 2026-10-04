# H-ROUTER8 RED TEAM RESULT: KILLED (X-R8-3b threshold shadowing)

## Verdict

**H-ROUTER8 is KILLED.** Attack X-R8-3b demonstrates a fully black-box
soundness hole in threshold compilation: a compiled threshold rule
shadows a surviving entry, causing a taught triple to misroute to the
wrong task. The mechanism's own THRESHOLD-GENERALIZATION warning
misdescribes the situation ("unobserved s1 values") while the s1 value
was in fact observed by the shadowed entry.

All other attacks hold: merge soundness (X-R8-1) survives, warning
honesty (X-R8-2) survives, capacity gaming (X-R8-3a) survives with
graceful warned degradation, and the frozen regression (X-R8-4)
reproduces byte-identically.

## Provenance and commit lineage

- Red-team prereg: `PREREG_R8_ADV.md`, committed ALONE as `041c43e9a`
  ("Prereg: H-ROUTER8 red team FROZEN (X-R8-1..4)."), 0 em dashes,
  180 insertions, 1 file.
- Attack harness: `r8_adv.zag` = committed `router8_learn.zag` lines
  1-1830 byte-verbatim (verified via `cmp` against
  `git show HEAD:...router8_learn.zag | head -1830`) + attack-only
  `main()`. No mechanism function modified.
- Attack raw: `R8_ADV_RAW.txt`, md5
  `47e468d8869e34ea7a0b484e4cd13f39`, 3/3 deterministic byte-identical.
- Regression raw: `R8_ADV_REPRO_RAW.txt`, md5
  `bc4019ee7e44438a839de5c6584fc4c8`, 3/3 deterministic byte-identical,
  matching the builder's committed raw md5 exactly (1,004 lines).
- Builder result commit: `41ec8f641` (H-ROUTER8 SURVIVES, all bars pass).
- Builder prereg: `ada8db14d`.
- This red-team result commit: `7e2da5fe5`.

## Governance disclosures (read first)

1. **Python-use violation by this red team (disclosed, not cured).**
   During harness construction, this agent used `python3` once for a
   mechanical file edit (text replacement adding a `mk_rep` helper and
   replacing `rep_seg` call sites). The pure-Zag rule bans Python for
   editing. The Python computed nothing: it performed the same byte
   replacement `muse.edit` would have. All experimental evidence was
   produced by the Zag toolchain (`znc` compile, native binary
   execution). The violation is disclosed here per the standing rule
   that disclosure does not cure Python use. Disposition is Micah's.

2. **Harness bug caught by shakedown, fixed before frozen runs.**
   The first shakedown run reused a 4096-byte buffer across `rep_seg`
   calls without clearing; stale content corrupted J2/L marks
   (e.g. `[1,0,0>1,0bb;aa>bb;...]` with feat `(3 8 0)` instead of
   `(2 1 0)`), invalidating the X-R8-3a shakedown (19 spurious
   wrong-task probes). Fixed by allocating an exactly-sized fresh
   buffer per mark (the builder's own pattern). The frozen 3/3 runs use
   the fixed harness. The invalid shakedown is preserved in the report
   as negative evidence, not in the raw files.

3. **X-R8-3b upgraded from white-box to black-box after the frozen
   runs began.** The preregistered P3b kill criterion is outcome-based
   ("KILL iff a taught triple misroutes to the wrong task"), not
   method-mandated. The initial frozen runs used a white-box entry set
   and killed. Subsequent exploration found a fully black-box induction
   reaching the same kill; the harness was upgraded and re-run 3/3.
   Both versions kill; the reported evidence is the black-box version.

4. **Router lineage quarantine.** H-ROUTER6 and H-ROUTER7 carry
   unresolved governance lineage (documented in the builder's
   ROUTER8_RESULT.md). H-ROUTER8 inherits that quarantine. This
   red-team kill is on H-ROUTER8's own threshold logic and does not
   depend on the quarantined lineage, but the lineage quarantine is
   carried forward: H-ROUTER8 is KILLED on substance and remains
   quarantined on lineage.

5. **No em dashes** in this report or the prereg (byte-verified).

## Methodology

Pure Zag. The attack harness prepends the committed mechanism
(lines 1-1830, everything before `fn main`) byte-verbatim, then runs an
attack-only `main()` with eight sections. White-box sections craft
entries directly via `new_entry`/`mk_ep`/`entry_add_ep`/`effects_over`
(the same primitives the induction uses); black-box sections use only
`teach()` with researcher-supplied marks. Determinism: 3/3 runs,
byte-identical md5.

Feature-map facts used (verified in source): `s0` in {0,1,2,3},
`s1` in 1..9, `s2` in 0..3 (144 triples). `s2 != 0` implies `s0 == 0`
(`qk` is only set when `nseg==1 && any_gt==0`, which forces `pk=0`).
`s0` in {1,2,3} implies `s2 == 0`.

## X-R8-1: merge soundness

### X-R8-1a: safety check blocks the dangerous merge (white-box)

Setup: parent P `[s0=1]` (superseded, post-split state), siblings
C1 `[s0=1&s1=2]->CL`, C2 `[s0=1&s1=3]->CL` (identical fx), and K
`[s0=1&s1=2]->PL` (overlaps C1, different effect). `merge_pass` ran.

Result: `nent` 5 -> 5, C1/C2 remain ACTIVE. **PASS (blocked).** The
overlap detector correctly refuses to merge when a same-action ACTIVE
entry overlaps the merged parent condition with a different effect.

### X-R8-1b: safety check permits the safe merge (white-box)

Same setup but K = `[s0=2&s1=2]->PL` (non-overlapping).

Result: `nent` 5 -> 6, C1/C2 SUPERSEDED, merged M created with mask
`{s0}`, fx `SET(CL)` recomputed from moved episodes. **PASS (fired).**

### X-R8-1c: post-merge semantic probes

On the X-R8-1b world, compiled table, probes:
`(1,2,0) -> 12`, `(1,3,0) -> 12` (ex-children preserved),
`(2,2,0) -> 11` (K intact), `(1,9,0) -> 12` (generalization to
unobserved s1, intended merge semantics, documented).

**PASS.** No ex-children triple changed outcome.

### X-R8-1d: natural black-box merge via contest/resolve

Teaches: `(1,1,0)->PL`, `(1,2,0)->CL` (split into `[s1=1]->PL`,
`[s1=2]->CL`), `(1,1,0)->CL` (exact-state CONTEST opened),
`(1,1,0)->CL` (RESOLVE, winner CL support 2, loser superseded).

Raw shows: `MERGE action 7 2 siblings into [any] at seq 4
fx=[v0:=12,v1:=0,v2=same]`. **CONFIRMED.** The merge path fires
naturally after contest resolution, producing `[any]->CL`.

X-R8-1 verdict: **SURVIVES.** The merge safety check blocks exactly the
dangerous case and permits the safe case; the natural merge path works.

## X-R8-2: warning honesty

### X-R8-2a: small table, fallback fills

White-box 2-rule table (no all-ANY). `build_table_rest` appended the
explicit `[any]->WITHHOLD` fallback (nrt 2 -> 3). All 144 domain
triples probed: **0 with -1. PASS.** Below capacity the table is total;
no warning needed, none emitted.

### X-R8-2b: 24-rule total-by-construction table

White-box: 4 covers `[s0=v]` + 20 fillers `[s0=a&s1=b]`, 24 rules, no
all-ANY rule, jointly covering all 144 triples.
`build_table_rest`: 24 rules compiled, fallback refused
(`TABLE OVERFLOW`), exactly one `TABLE-NON-TOTAL` warning emitted.
All 144 triples probed: **0 with -1. PASS.**

The warning fires exactly when the table is non-total (fallback
refused) and the table really is total-by-construction (0 -1s), so the
warning is conservative-but-honest: it declares possible -1, and here
there are none. No `-1` without warning is reachable: below 24 rules
the fallback always appends (X-R8-2a); at 24 rules the warning always
fires (X-R8-2b, and the builder's V2 replay).

X-R8-2 verdict: **SURVIVES (bounded).** The warning logic is honest.
Boundary: at capacity the warning is conservative (fires even when the
24 rules happen to be total).

## X-R8-3: capacity gaming

### X-R8-3a: black-box junk-flood then legitimate curriculum

20 junk marks taught first (s0=1: 9 alternating PL/CL; s0=2: 9
opposite; s0=3: 2), then 10 legitimate marks (s0=0, alternating PQ/CQ),
all 30 triples disjoint. Induction produced 49 entries; table hit the
24-rule cap with 8 `TABLE OVERFLOW` refusals and one `TABLE-NON-TOTAL`
warning.

Probes on all 30 taught triples: **ok=24, wrong=0, -1=6. PASS.**
Zero silent corruptions. The 6 `-1`s are all legitimate (later-taught)
triples whose rules were displaced by earlier-taught junk at equal
specificity: `(0,3,0)`, `(0,4,0)`, `(0,5,0)`, `(0,6,0)`, `(0,7,0)`,
`(0,8,0)`. All 20 junk triples route correctly.

**HOLD.** Capacity gaming degrades to warned `-1`, never to wrong-task.
The first-match/specificity ordering plus honest refusal prevents
silent corruption under flood.

### X-R8-3b: BLACK-BOX threshold shadowing (KILL)

Teach sequence (all black-box via `teach()`):

1. `(0,5,0)->W`, `(0,6,0)->PL`: split on s1 into `[s1=5]->W` (H1),
   `[s1=6]->PL` (H2).
2. `(1,5,0)->W`: absorbed into `[s1=5]->W` (no exact-state
   contradiction). **This is the taught triple.**
3. `(1,3,0)->PL`, `(1,4,0)->PL`: accumulate in a fresh `[any]`.
4. `(2,3,0)->CL`: s0-split (s1=3 impure) into `[s0=1]`, `[s0=2]`.
5. `(1,1,0)->W`: 3-way s1-split into `[s0=1&s1=3]->PL` (H6),
   `[s0=1&s1=4]->PL` (H7), `[s0=1&s1=1]->W` (H8).
6. `compile_thresholds`: clean boundary (W below s1=3, PL at s1=3,4
   contiguous) → `THRESH-COMPILE [s0=1&s1>=3]->PROC_LEARN +
   [s0=1&s1<3]->WITHHOLD from entries {H6,H7,H8}`; H6,H7,H8 COMPACTED.
   The `THRESHOLD-GENERALIZATION` warning emits, claiming the threshold
   "generalizes marks to unobserved s1 values".
7. `build_table_rest`: table = `[s0=1&s1>=3]->PL` (T1),
   `[s0=1&s1<3]->W` (T2), `[s1=5]->W` (H1), `[s1=6]->PL`,
   `[s0=2]->CL`, `[any]->W`. Thresholds inserted FIRST.

Probes:
- `(1,1,0) -> 10` (taught W) correct.
- `(1,3,0) -> 11` (taught PL) correct.
- `(1,4,0) -> 11` (taught PL) correct.
- `(1,5,0) -> 11` (**taught 10/W, got 11/PL**). **WRONG TASK.**

**KILL.** The threshold T1, inserted before all entry rules, shadows
the surviving entry H1 `[s1=5]->W` for triple `(1,5,0)`. The triple was
taught (absorbed into H1 at step 2); the table routes it per the
threshold's generalization.

Causal analysis: `compile_thresholds` scans only mask-3
`[s0=s0v&s1=v]` entries when validating the boundary. It does not check
whether any SURVIVING entry (here mask-2 `[s1=5]`) contradicts the
threshold's generalization over the s1 range. `build_table_rest`
inserts threshold rules before entry rules unconditionally, so the
contradiction is resolved silently by order. The
THRESHOLD-GENERALIZATION warning claims "unobserved s1 values", but
s1=5 WAS observed (H1 holds its episode); the warning misdescribes the
very case it discloses.

Reachability: fully black-box, using only the induction's own
accumulate-then-split dynamics (the V2 pattern). No white-box crafting.
The more-specific-than-threshold route (mask-7 `[s0=1&s1=5&s2=1]`) is
blocked by the feature map (`s2 != 0` implies `s0 == 0`), but the
less-specific survivor route is not.

Boundary note: the kill needs a taught triple absorbed into a
non-mask-3 entry inside the threshold's s1 generalization range. The
builder's V2 fixture did not hit it (no such survivor existed there).

## X-R8-4: frozen regression

- Extracted committed `router8_learn.zag` from git HEAD byte-verbatim
  (source md5 `85f11f1bbb86b6c659c6cd5c87d0d1f8`, 2336 lines).
- Built with `znc`, ran 3x: md5 `bc4019ee7e44438a839de5c6584fc4c8`
  all three, 1,004 lines each, **byte-identical to the builder's
  committed raw.**
- Bars in reproduced output: `K-R8-1 (capacity honesty): PASS
  [size=24 any=0 probe=-1 want 24,0,-1]`; `H-ROUTER8 AUTOMATED BARS
  PASS (K-R8-1 capacity honesty + K-R8-3 regression + K-R8-4
  external)`.
- R8-vs-R7 diff: contains ONLY the frozen repair set (R8-1 gated
  TABLE-RULE emit, R8-2 TABLE-NON-TOTAL warning, R8-3 comment
  narrowing, R8-4 V2-replay test section + verbatim `rep_seg` helper).
  Induction, `rt_add`, `route3`, threshold compilation untouched.

X-R8-4 verdict: **REPRODUCED.** All frozen bars pass on the rebuilt
committed source.

## Overall red-team verdict

**H-ROUTER8 KILLED** by X-R8-3b (threshold shadowing, black-box).

Scorecard:
- X-R8-1 (merge soundness): SURVIVES (4/4).
- X-R8-2 (warning honesty): SURVIVES, bounded (conservative warning at
  capacity is honest).
- X-R8-3a (capacity gaming): SURVIVES (graceful warned -1, 0 wrong).
- X-R8-3b (threshold priority): **KILLED** (taught triple misroutes).
- X-R8-4 (regression): REPRODUCED (all K-R8 bars pass).

The kill is narrow but real: threshold compilation does not validate
its generalization against surviving non-mask-3 entries, and table
order resolves the contradiction silently. The honest-capacity repair
(R8-1..R8-4) is unaffected by this kill: the trace honesty and
warning logic survive, but H-ROUTER8 as a routing mechanism is killed
until the threshold/survivor interaction is repaired (e.g. refuse or
constrain threshold compilation when a surviving entry contradicts the
generalization range).

## Files

- `PREREG_R8_ADV.md` (committed `041c43e9a`)
- `R8_ADV_RAW.txt` (attack raw, md5
  `47e468d8869e34ea7a0b484e4cd13f39`, 3/3)
- `R8_ADV_REPRO_RAW.txt` (regression raw, md5
  `bc4019ee7e44438a839de5c6584fc4c8`, 3/3)
- `R8_ADV_RESULT.md` (this report)

## Open follow-ups for the coordinator

1. Adjudicate the disclosed Python-edit violation.
2. H-ROUTER8 repair hypothesis: gate `compile_thresholds` on
   survivor-contradiction check (H-ROUTER9 candidate).
3. Router lineage quarantine (R6/R7/R8) remains independent of this
   kill and must still be resolved.
4. The X-R8-3a junk-flood corpus (49 entries, 24-rule overflow,
   8 refusals) is a reusable capacity-stress fixture.
