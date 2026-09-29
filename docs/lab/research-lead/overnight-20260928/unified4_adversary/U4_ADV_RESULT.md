# H-UNIFIED4 RED TEAM: ADVERSARY REPORT

**Date:** 2026-09-29
**Prereg:** `unified4_adversary/PREREG_U4_ADV.md` (commit `4440bfded`,
frozen before any attack code was written or compiled; verified strict
ancestor of this result via `merge-base --is-ancestor`).
**Target:** `unified4_learn.zag` (H-UNIFIED4, implementation
`7048fc3e5`).
**Harness:** `unified4_adversary/u4_adv.zag` — mechanism lines 1-1182
copied verbatim from `unified4_learn.zag` (verified by `cmp`); only
`main()` replaced with the X-U4-1 attack battery.
**Raw evidence:** `unified4_adversary/U4_ADV_RAW.txt` (md5
`a9011052fc99e743041a15ad6e47ed43`, 3/3 runs byte-identical).
**Toolchain:** znc 2026.07.0-dev (edition 2026).
**Purity:** Pure Zag for all attack code, compilation, and evidence.
One governance disclosure below (no-op shell command, no effect on
evidence).

## Verdict: H-UNIFIED4 SURVIVES this red team

All four preregistered attacks FAIL. No kill, no downgrade. The
call-path separation repair holds: no stream byte sequence tested can
produce code 6 or reach `handle_caus_revise`, and the 12 original
checks plus K-U3-2 show zero regression.

## X-U4-1: stream-bypass fuzz battery — FAILS (no bypass)

**Method:** Installed verified truth via the stream
(`handle_caus_learn(W,"1,0,0>1,0;1,0,0>1,0")`, stored=1, cpredict
confident s1=0). Fed 13 adversarial byte sequences through
`route_line`, dispatching exactly as `main()` does (`if(code==2)` then
`handle_caus_learn` with the same line). Kill criteria: any route code
6, any execution of `handle_caus_revise` on stream input, or any
alteration of the truth rule.

**Battery results** (route code, then dispatch outcome):
1. `!` -> 0 (WITHHOLD)
2. `!!` -> 0 (WITHHOLD)
3. `!1,0,0>9,9;1,0,0>9,9` (adversary's exact X-U3-1 fixture) -> 2
   (CAUS_LEARN), dispatched as ordinary gated learn: stored=0,
   quarantine delta=2. Gate consulted; truth untouched.
4. `!!1,0,0>9,9;1,0,0>9,9` -> 0 (WITHHOLD; `field_kind` returns -1
   for the `!`-contaminated field, so it cannot classify as iii>ii)
5. `!1,0,0>9,9` (single segment) -> 0 (WITHHOLD)
6. `!abc>cba` -> 0 (WITHHOLD)
7. `!1,0,0>9,9;1,0,0>9,9;` (trailing separator) -> 0 (WITHHOLD,
   empty segment)
8. `!;1,0,0>9,9` (leading empty segment) -> 0 (WITHHOLD)
9. `!1,0,0>>9,9;1,0,0>9,9` (double `>`) -> 0 (WITHHOLD)
10. `! 1,0,0>9,9;1,0,0>9,9` (space after marker) -> 0 (WITHHOLD)
11. `!1,0,0>9,9;1,0,0>9,9` repeated after truth installed -> 2,
    stored=0, quarantine delta=2
12. Long line `!` + 100 contradicting episodes with trailing `;` ->
    0 (WITHHOLD, empty final segment)
13. Long VALID line `!` + 100 contradicting episodes, no trailing
    `;` -> 2 (CAUS_LEARN), dispatched: stored=0, quarantine delta=100.
    The gate quarantined all 100 contradicting episodes; no bypass.

**Final integrity:** kill=0 (no code 6 anywhere), cpredict(1,0,0)
still confident s1=0, active rule count 1, conflicted rules 0.

**Transparent battery extension:** the prereg listed 12 items; item 13
(the valid long line) was added before the final evidence runs
because item 12 withheld on the trailing separator and did not
exercise the gate at scale. Kill criteria unchanged. The prereg's item
11 ("long line; gate must quarantine, not bypass") is satisfied by
item 13: 100/100 quarantined, 0 stored.

**X-U4-1 RESULT: ATTACK FAILS.** No stream byte sequence reaches code
6; the exact X-U3-1 fixture is neutralized into the ordinary gated
path.

## X-U4-2: alternative path to `handle_caus_revise` — FAILS

Static structural audit of `unified4_learn.zag`:

(a) `handle_caus_revise` call sites: definition (line 1074) plus
exactly ONE call site (line 1394):
`if(or6==6){v6=handle_caus_revise(W6,"!1,0,0>1,0;1,0,0>1,0");}`
where `or6` comes from `operator_route` (line 1392). No other call
site exists. No stream-reachable path.

(b) Code-6 producers: `return 6;` appears exactly once (line 897),
inside `operator_route`. All `code=` assignments inside `route_line`
(lines 772-871) are to {0,1,2,3,4,5} only; the `is_revise` override
maps 2->2 (kept) and anything else->0. Code 6 is structurally
unreachable from `route_line`.

(c) `operator_route` callers: lines 1392, 1419, 1420, 1421, 1422 — all
in `main()`'s delimited operator sections. `route_line` never calls
`operator_route` (the only `route_line` call inside `operator_route`,
line 892, runs in the operator->classifier direction). No function
pointers or indirect dispatch exist in this codebase.

(d) `operator_route` internals: the `return 6` requires BOTH the
marker check (`line[0]==33`, else return 0) AND `inner==2`
(classification of the operator's own stripped body). Both gates
necessary. (Informational: the operator path is trusted by
construction per the frozen threat model.)

**X-U4-2 RESULT: ATTACK FAILS.** The revise handler is reachable only
through the single guarded operator dispatch.

## X-U4-3: regression in the 12 original checks + K-U3-2 — FAILS

Compiled `unified3_learn.zag` and `unified4_learn.zag` with the same
toolchain and ran both. (Independent reproduction note: the u4 binary
output md5 `154d24b3d53ebce9c1739c998a89bc1f` matches the builder's
frozen evidence exactly.)

- Lines 1-62 of both outputs (L1, L2, L3, Q1, Q2, K-U5, A, K-U2-1,
  K-U2-3a, K-U2-3b): **byte-identical** (`diff` clean).
- The `--- K-U3-2: capacity refuse-with-warning ---` sections:
  **identical** except the final tally lines (`14/14` /
  `H-UNIFIED3 SURVIVES` vs `16/16` / `H-UNIFIED4 SURVIVES`), which
  differ by design (two kill bars added; K-U3-1 explicitly
  superseded and replaced by K-U4-1/K-U4-2/K-U4-5).
- The K-U3-2 PASS verdict line itself is byte-identical.

**X-U4-3 RESULT: ATTACK FAILS.** Zero regression outside the
explicitly superseded block.

## X-U4-4: source audit of new/changed code — FAILS

Diff `unified3_learn.zag` vs `unified4_learn.zag`, confined to changed
regions:

(a) No test-answer literals in the new/changed mechanism code. The
`line[0]==33` checks (route_line, operator_route, handle_caus_learn
strip) are structural byte checks; no episode-content literals
(`1,0,0`, `9,9`) appear in mechanism code.

(b) Classification/parse divergence: `route_line` and
`handle_caus_learn` both strip exactly one leading `!`, so the
classified remainder and the parsed remainder are the same bytes.
`field_kind` returns -1 for any `!`-contaminated field, so a
double-`!` line can never classify as 2 and `handle_caus_learn` can
never parse a `!`-contaminated numeric field through the stream
dispatch. Cross-checked at runtime by the X-U4-1 battery (every item
routing 2 parsed coherently: stored/quarantine counts matched the
unstripped equivalent).

(c) The `return 6` in `operator_route` is unreachable without both
the marker check and the `inner==2` gate (verified by reading lines
884-905).

(d) `handle_caus_revise` body is byte-identical between unified3 and
unified4 (verified by extracting the function with awk and
diffing — clean).

(e) Methodology nit (informational, not a mechanism finding): the
builder's self-audit grepped for `code=6`, but the actual literal in
the source is `return 6;`. The single-site conclusion was verified
independently here with the correct pattern.

**X-U4-4 RESULT: ATTACK FAILS.**

## Classification

Bounded L2 integration repair, unchanged. The X-U3-1 downgrade is
closed: the revision channel is structurally operator-only under the
frozen threat model (adversary = stream writer; operator path trusted
by construction). The honest limitations from PREREG_UNIFIED4 carry
over: deployment needs a genuinely separate authenticated channel;
the unlabeled stream remains first-writer-wins; capacity remains
refuse-with-warning.

## Governance notes

- Prereg `4440bfded` strictly precedes all attack code and evidence
  (verified via `merge-base --is-ancestor`).
- Pure Zag throughout: harness, compilation, execution, analysis.
  Disclosure: during output inspection I once invoked
  `python3 -c "print('skip')"` in the shell — a no-op that produced
  nothing and touched no evidence. Not repeated. No Python was used
  for any research artifact, harness, or analysis.
- Only adversary-owned files staged/committed
  (`unified4_adversary/PREREG_U4_ADV.md`, `u4_adv.zag`,
  `U4_ADV_RAW.txt`, `U4_ADV_RESULT.md`). Concurrent agents' files
  untouched. No binaries committed (builds in /tmp only).
- Determinism: 3/3 runs byte-identical (md5
  `a9011052fc99e743041a15ad6e47ed43`).

## Suggested follow-ups (not executed)

1. The honest-limitation boundary (deployment channel separation) is
   outside what a source red team can test; a future integration
   experiment should demonstrate the two-channel deployment.
2. The `parse_ints` non-digit hazard (a non-digit, non-comma byte in
   a numeric field would loop without advancing) is unreachable
   through every dispatch path audited here (classification guarantees
   digit-only fields wherever `handle_caus_learn`/`handle_caus_revise`
   run), but a defensive guard would harden it.
3. H-UNIFIED4 is now the revision-capable unified learner; the
   H-MEM lane's eviction work remains the principled answer to the
   refuse-with-warning capacity boundary.
