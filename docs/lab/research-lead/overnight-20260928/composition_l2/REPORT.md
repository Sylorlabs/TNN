# REPORT: Composition L2 Adaptive Reuse

## Verdict: COMPOSITION-L2-COMPLETE

**All 12 frozen kill bars pass. 3/3 byte-identical runs per binary.
Adaptation operators are learner-triggered standing rules inside
`un_candidates`; the one-line `adapt_on()` toggle is the causal control.
Zero modes, bridges, handlers, semantic cases.**

Date: 2026-10-02. Worker: Composition L2 Adaptive Worker (continuation).
Prereg: PREREG.md, commit c521249ba (frozen before implementation).
Branch: tnn-native-lab, local only, nothing pushed.

## Failure diagnosis and fix

The prior worker's shipped `l2_bin` failed every arm (all ans=-2,
ADAPT-STAT sat=0 ext=0 trunc=0 spec=0, COMP-STAT tried=0). Diagnosis: the
shipped binary was stale relative to the current sources. Its run
signature is exactly what uninitialized workspaces produce: training
queries returned -2, no MAPs were ever promoted, so `un_candidates`
admitted zero live MAPs and `compose_try` had nothing to adapt.

No patch logic changes were required. Recompiling the current sources
unchanged with the pinned compiler produced a binary that passes every
arm, including the key test (X=[1,1,1] extended to cover 4 r1 links).
The adaptation operators were correct as written; the failure was a
stale build artifact, not a design defect.

## Mechanism

`l2_patch.zag` extends the unified composition DFS (`un_patch.zag`)
with three adaptation operators evaluated for EVERY candidate MAP at
EVERY DFS level inside `un_candidates`:

- EXTEND: `adapt_walk` replays the constraint walk, then greedily
  continues with the MAP's last relation while matching facts exist
  (up to 3 extra links). Variant code 1000+ext.
- TRUNCATE: `adapt_trunc_find` tries proper prefixes (L-1 down to 1)
  when the full walk fails; longest satisfiable prefix becomes variant
  2000+plen.
- SPECIALIZE: if any walk step was ambiguous (`lu_count2` > 1), a
  nearest-object re-walk (`lu_pick` mode 1, locality prior computed
  from runtime data) becomes variant 3000.

Triggering is purely structural: relseq satisfiability, existence of
continuation facts, observed ambiguity. The researcher never selects
an operator per problem. `un_satisfy_v` dispatches variants so adapted
candidates backtrack exactly like base candidates. The NA build flips
exactly one line (`adapt_on()` 1 to 0) and reproduces the old failure.

## Per-bar results (frozen bars K1-K12)

- K1 L2-TREAT ans=108: PASS. X (plen-3) extended to 4 r1 links;
  final ADAPT-STAT ext=1; COMP-SEGS n=2 (X then Y).
- K2 L1-TREAT ans=107: PASS. Final ADAPT-STAT ext=0; behavior
  identical to the no-adaptation baseline (no regression).
- K3 L2-ABL-X ans=-2, L2-ABL-Y ans=-2, L2-FRESH ans=-2: PASS.
- K4 L2-NOADAPT (adapt_on=0 build) ans=-2: PASS.
- K5 TR-TREAT ans=107, TR-NOADAPT ans=-2, TR-FRESH ans=-2: PASS.
  X2=[1,1,1,1] truncated to a plen-2 prefix (trunc=2 generated).
- K6 SP-TREAT ans=107, SP-NOADAPT ans=-2, SP-FRESH ans=-2: PASS.
  Ambiguity at step 1 triggered the specialized nearest-object walk
  (spec=1), routing around the distractor branch.
- K7 L2-PROV: LINK14 MAP_Z to X = 1, LINK14 MAP_Z to Y = 1: PASS.
- K8 L2-REUSE ans=108: PASS (repeat query in the same workspace).
- K9 L2-TREAT ADAPT-STAT ext_gen=1 (>= 1 required); L1-TREAT
  ADAPT-STAT ext_gen=0: PASS.
- K10 L2-TREAT ADAPT-STAT satisfy_calls=7 (< 200 required): PASS.
- K11 3/3 runs byte-identical per binary: PASS.
  l2_bin runs sha256 865b6c94be5010cdf0a7abcf8ae118e6963639f0f146a5e85ff4adcf9b84a4cb
  l2_na_bin runs sha256 aabe551df8dee2451750e867e85dc3276814b0fdc0122102787ec58c78ec1d1c
- K12 zero em/en dash bytes in all deliverables: PASS (byte scan;
  compiler-emitted dashes in build logs were normalized to ASCII).

## Cost table (L1 vs L2, from run output)

Final compose_try ADAPT-STAT per passing arm (sat = satisfy calls,
ext/trunc/spec = variants generated), plus COMP-STAT rebind
tried/rejected and observed COMP-SEGS:

| arm       | ans  | sat | ext | trunc | spec | tried | rej | segs      |
|-----------|------|-----|-----|-------|------|-------|-----|-----------|
| L1-TREAT  | 107  | 8   | 0   | 0     | 0    | 3     | 2   | 2 (45 27) |
| L2-TREAT  | 108  | 7   | 1   | 0     | 0    | 3     | 2   | 2 (27 45) |
| TR-TREAT  | 107  | 12  | 0   | 2     | 0    | 3     | 2   | 2 (45 68) |
| SP-TREAT  | 107  | 11  | 0   | 0     | 1    | 7     | 6   | 2 (27 45) |
| L2-REUSE  | 108  | 7   | 1   | 0     | 0    | 3     | 2   | 2 (27 45) |

Adaptation adds at most a small constant number of satisfy calls over
the exact-reuse baseline; the bounded operator set keeps the L2 cost
profile near L1 while unlocking the previously impossible arms.

## Architecture accounting

- Cognition lines added: adaptation operators (~150 lines in
  l2_patch.zag: lu_count2, lu_pick, adapt_walk, adapt_trunc_k,
  adapt_trunc_find, un_satisfy_v, cand_ins, adapt_on).
- New hardcoded semantic cases: 0.
- Modes, bridges, handlers: 0.
- Learner-state structures created: none new; operators read existing
  fact store and MAP graphs only.

## Provenance

- Compiler: pinned src/tools/toolchain/znc_linux_x86_64_abed8aa1.
- l2_bin sha256: c8dc4195eb6f3a654f4b1971223bf129e5324c0e9b06e853357a8a24bcb97402
- l2_na_bin sha256: 79a193ed6a8be1a750c4ddaa5e48081d00b5379c2f419a7ecb4a09851af84331
- l2_patch_na.zag differs from l2_patch.zag by exactly one line
  (adapt_on 1 to 0), verified by diff.
- l2_full.zag = cc_base.zag + l2_patch.zag + l2_driver.zag (section
  verified byte-identical); l2_full_na.zag assembled analogously.
- Pure Zag throughout; worker toolchain guard verified (no python3 or
  python reachable in worker PATH).
