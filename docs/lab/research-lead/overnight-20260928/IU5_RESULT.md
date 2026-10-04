# IU5 RESULT: H-INTENT-UNIFIED5 Repair Verification

## Verdict: H-INTENT-UNIFIED5 SURVIVES (all frozen kill bars PASS)

Both H-INTENT-UNIFIED4 red-team downgrades are closed at the mechanism
level. No frozen K-IU4 bar broken. No regressions. Classification:
bounded L2 integration repair. Not L3.

## Lineage

- Prereg `PREREG_INTENT_UNIFIED5.md` frozen before any implementation
  edit, build, or run. Governance note: the prereg file was staged by
  this researcher and swept into a concurrent worker's broad-pathspec
  commit `412977496` ("Paper: H-UNIFIED6 SURVIVES"); the committed blob
  is byte-identical to the authored prereg (md5
  cf206b9200cecf18140c6e978cf4b925, verified by cmp against
  `git show 412977496:`). Content frozen; commit message is the other
  worker's. This is recorded, not hidden. `git merge-base --is-ancestor`
  confirms the prereg commit strictly precedes the implementation.
- Implementation: identical R6/R7 edits in `intent_learn.zag` and
  `unified_learn.zag`. Faithfulness invariant verified: all 8 intent
  functions (intent_record_inputs, intent_record_proc, intent_record_br,
  intent_exact_match, intent_qscore, intent_winner, intent_trace_emit,
  intent_init) byte-identical between the two files (per-function
  extraction + cmp). bridge_learn differs only by pre-existing comments.
- Harness: `iu5_verify.zag` = lines 1..1415 of the NEW
  unified_learn.zag (mechanism region; `fn main` starts at line 1416),
  cmp-verified byte-identical; only main() replaced with kill-bar tests.
- Raw evidence: `IU5_VERIFY_RAW.txt` (md5
  24817621d9c6a137acebef23c7ab501d, 3/3 byte-identical).
- Toolchain: znc 2026.07.0-dev (edition 2026), pinned. Pure Zag
  throughout: prereg, implementation, harness, builds, runs, greps,
  md5, cmp. No Python at any stage.

## Repair R6: both-truncated guard (X-IU4-1a CLOSED)

### Mechanism change

In `intent_winner`, the truncated-conflict guard's `check` computation
gains a third branch:

```
if(em_top==0 && em_second==0 && trunc_top==1 && trunc_second==1){check=1; both_trunc=1;}
```

On answer disagreement (kind-dispatched proc_apply/bridge_apply, byte
comparison over qlen, unchanged): if both_trunc==1, emit
`INTENT TRUNCATED-CONFLICT-POSSIBLE: both records truncated with different answers; WITHHOLD AMBIGUOUS`;
else emit the existing verbatim-vs-truncated diagnostic text unchanged.
Then kind=-2, slot=-1, return. On answer agreement, fall through (no
over-broad withholding).

Precedence is structural and the three branches are mutually exclusive
by construction: the verbatim guard needs em=1 on both sides; the two
R4 branches need em=1 on exactly one side; the R6 branch needs em=0 on
both sides.

### K-IU5-1 evidence

Fixture (exact X-IU4-1a): proc 17 reverse pairs with `xab>bax` 17th
(unrecorded, direct discovery); bridge 17 pairs with `xab>xxx` 17th
(unrecorded, IF input[0]=='x' THEN const-0 ELSE reverse). Query `xab`.

Order A (proc-first): `T DECIDE tag=K51a-xab kind=-2 slot=-1 gap=20000`.
Diagnostic `INTENT TRUNCATED-CONFLICT-POSSIBLE: both records truncated with different answers; WITHHOLD AMBIGUOUS`
present. PASS.

Order B (bridge-first): `T DECIDE tag=K51b-xab kind=-2 slot=-1 gap=20000`.
Same diagnostic present. PASS.

Pre-fix behavior was kind=1, answer `xxx`, zero diagnostics. The guard
now fires because both records carry true npairs=17 > 16 (truncated),
both candidates have em=0, and proc_apply(`xab`)=`bax` differs from
bridge_apply(`xab`)=`xxx`.

## Repair R7: 16-char extraction cap (X-IU4-2b CLOSED)

### Mechanism change

In `bridge_learn` Step 1, before `pextract`: if out_len > 16, emit
`bridge: pair <i> output length <out_len> exceeds 16-char extraction capacity; excluded (honest cap)`,
set statbase+i*4=0, allok=0, and skip extraction for that pair.
Otherwise run the existing path unchanged.

This bounds every `sq` write and every seqbase-slot write to at most 16
i32s by construction (sl <= out_len <= 16). Per-pair exclusion mirrors
the existing pextract-failure path exactly; if no extractable pair
remains, Step 3 finds no split and the function returns -1 through the
existing honest-failure path. Applied identically in both .zag files.

### K-IU5-2 evidence

Fixture (exact X-IU4-2b): `abcdefghijklmnopqrst>tsrqponmlkjihgfedcba;ABCDEFGHIJKLMNOPQRST>TSRQPONMLKJIHGFEDCBA`
(two 20-char reverse pairs; each output char appears exactly once in
its input, so pextract would return 20, not -1). Routes PROC_LEARN.

Observed (3/3 identical, exit 0):

```
bridge: pair 0 output length 20 exceeds 16-char extraction capacity; excluded (honest cap)
bridge: pair 1 output length 20 exceeds 16-char extraction capacity; excluded (honest cap)
ULEARN FAIL: no program and no bridge
```

rc=-1. No panic. PASS. Pre-fix behavior was `panic: slice index out of
bounds`, exit 1.

## K-IU5-3: no regression (all K-IU4 bars still PASS)

- K-IU5-3a (K-IU4-1): proc 17-pair `...;xab>bax` + bridge
  `xab>xxx;xcd>xxx;abc>ccc;def>fff;abcde>eeeee`; query `xab` ->
  `T DECIDE tag=K53a-xab kind=-2 slot=-1 gap=50000` with the UNCHANGED
  diagnostic `verbatim candidate meets truncated record with different answer`.
  The R4 branch keeps precedence (em=1 on the bridge side). PASS.
- K-IU5-3b (K-IU4-2): 129-pair build_big_line fixture -> rc=-1,
  `bridge: WORK area too small for npairs=129; need 9288 bytes; honest failure`,
  exit 0, no panic. The WORK guard precedes Step 1; R7 does not alter
  this path. PASS.
- K-IU5-3c: in-cap verbatim conflict (`xab>bax;abc>cba` vs
  `xab>xxx;xcd>xxx`) -> kind=-2. The verbatim guard is untouched. PASS.
- Full suite regression: unified_learn.zag main() ->
  `=== INTENT-UNIFIED RESULT: 20/20 ===`, md5
  904de9f83a2873c7a8862b71804a9065, byte-identical to the frozen IU4
  evidence hash. intent_learn.zag main() -> `=== INTENT RESULT: 10/10 ===`,
  md5 98315faec8faea24e75533892c0b240d, byte-identical to the frozen IU4
  evidence hash. Neither repair fires on any suite case. PASS.

## K-IU5-4: determinism

iu5_verify binary: 3/3 byte-identical (md5
24817621d9c6a137acebef23c7ab501d). unified main(): 3/3 byte-identical.
intent main(): 3/3 byte-identical. PASS.

## Final tally

6/6 harness checks PASS; 20/20 + 10/10 regressions byte-identical;
3/3 determinism on all three binaries. **H-INTENT-UNIFIED SURVIVES.**

## Causal interpretation

X-IU4-1a was a scope error, not a logic error: the R4 guard's coverage
condition (one verbatim anchor) was narrower than the claim
("cap-robust conflict detection"). The repair generalizes the coverage
condition to the both-truncated case while preserving the
precision/recall tradeoff (withhold on disagreement, fall through on
agreement, diagnostic says POSSIBLE). X-IU4-2b was an instance-level
audit miss: the R5 audit fixed the reported vector (dvals) and one
find (WORK/PAIRBASE) but not the buffer class. The repair converts the
class into a loud per-pair capacity bound instead of auditing instances.

## Boundaries (frozen, disclosed)

- The both-truncated guard carries the same precision cost as R4: two
  truncated records whose procedures merely generalize differently
  will withhold with an honest "POSSIBLE" diagnostic even when the
  unrecorded tails do not contradict. Disclosed, not a bug.
- The 16-char extraction cap is a loud per-pair exclusion. Outputs
  longer than 16 chars can never participate in extraction; this is a
  documented mechanism capacity. Enlarging the seq representation is
  future work.
- The guard considers only the top two ranked candidates, as before.
- The narrowed IU4 claims are now: conflict detection is
  verbatim-anchored AND both-truncated-anchored (no other anchor);
  the buffer audit covers dvals (256, exact), WORK/PAIRBASE (dynamic),
  and sq/seqbase (16-char honest cap).
- Classification: bounded L2 integration repair. Not L3.

## Governance disclosures

1. Prereg committed before any implementation; ordering verified by
   merge-base --is-ancestor. The prereg file was swept into a
   concurrent worker's commit (412977496); content verified
   byte-identical, lineage recorded here.
2. Pure Zag throughout; zero Python at any stage (prereg, edits,
   harness, builds, runs, greps, md5, cmp).
3. No binaries committed (builds in /tmp/iu5 only).
4. Only researcher-owned paths staged: PREREG_INTENT_UNIFIED5.md
   (already committed via sweep), intent_learn.zag, unified_learn.zag,
   iu5_verify.zag, IU5_VERIFY_RAW.txt, IU5_RESULT.md. Concurrent
   workers' files untouched (pathspec-restricted staging).
5. No em dashes in loop documentation.
6. No test-answer literals in mechanism regions: the only new literals
   are diagnostic strings and the capacity constant 16; fixture
   strings live in iu5_verify.zag main() only.
7. The legacy standalone `bridge_learn.zag` (pre-IU3, still carries the
   old s1idx/s2idx z_alloc(64)) was NOT modified: it is not part of
   the IU4 claim and no committed evidence is built from it. Disclosed.

## Suggested follow-ups for parent

1. Independent red team on H-INTENT-UNIFIED5 (natural attacks: a third
   truncation anchor beyond top-two; a 16-char boundary pair (exactly
   16 vs 17) for off-by-one; mixed truncated/verbatim with three
   candidates).
2. The research paper's H-INTENT-UNIFIED4 section needs the downgrade
   entry plus this H-INTENT-UNIFIED5 result (paper lane, not mine).
