# SPEC-PERRELATION-EPOCH: REPORT

**Lane:** docs/lab/research-lead/overnight-20260928/spec_perrelation_epoch/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Local commits only, never pushed.
**Verdict: BUILD-PASS (12/12 frozen kill bars)**

## Summary

Implements per-relation epoch granularity on top of SPEC-EPOCHTAG and
SPEC-REFUSAL-RECOVERY. A per-relation epoch table in the world arena
(A[776]: entry count; A[780+i*8]: (relation, epoch) pairs, i in 0..7)
replaces the single world epoch as the staleness signal: each bucket is
tagged with ITS RELATION's epoch at specialization time (pe_specialize_*
reads the bucket's relation from the da_learn coverage id arrays), and
every spec call compares the live epoch of the QUERIED relation against
the tag. The drift constructors bump the epoch of every relation with at
least one fact whose (s,r,o) content changed. Built on the real
`da_base.zag` + `da_module.zag` + `da_learn.zag` (byte-unmodified),
`rb_world.zag` + `rb_fix.zag` (byte-unmodified), `et_world.zag` +
`et_spec.zag` (byte-unmodified), and `rr_spec.zag` (byte-unmodified);
`da_learn.zag` is NOT modified and the DA battery is untouched. Only
`pe_world.zag` (epoch table + drifts), `pe_spec.zag` (per-relation gate +
per-bucket stamping), `pe_rr.zag` (recovery wrappers, same
refuse -> re-specialize -> single-retry shape as `rr_spec.zag`), and
`pe_main.zag` (harness) are new.

Results: on the E1 unrelated drift (only the second relation's facts
change), the coarse per-world lines in the same run refuse and pay a full
rebuild (E1RET_RRC: refuse=1, resp=1, the priced cost), while the
per-relation lines hit with no refusal and no rebuild (E1RET_PERR /
E1CNT_PERR / E1VFY_PERR: spec=1=gen, refuse=0, resp=0). The gate is not
degenerate: queries against the drifted relation itself still refuse and
recover (E1B: refuse=1, resp=1, agree=1), and answer-changing drifts on
the queried relation still refuse and recover on all three families
(E2, E3), with the one-time-cost and miss/hit decision-rule properties
intact. The epoch table holds exactly the touched relations with the
right epochs (n=1 after E1, n=2 after E2/E3). All binaries pure Zag,
safebin-built, 3/3 byte-identical.

## What was tested (do not treat the reasoned sections as tested)

Assembly: `pe_full.zag` = da_base + rb_world + et_world + da_module +
da_learn + rb_fix + et_spec + rr_spec + pe_world + pe_spec + pe_rr +
pe_main. Repro: `./pe_build.sh`.

Same tiny world and drifts as the parent lanes. Per-line refuse/resp
counters are reset before every emitted line. Coarse lines (ETC/RRC)
reuse the parent et/rr specs byte-unmodified to price the coarse scheme
in the same run; they touch only the coarse tag slots, so they do not
disturb the per-relation tags.

| Line | spec | gen | agree | refuse | resp | kbs |
|------|------|-----|-------|--------|------|-----|
| E0RET_ETC (coarse) | 1 | - | - | 0 | - | 2 |
| E0RET_PERR / E0CNT_PERR / E0VFY_PERR | 1 | 1 | 1 | 0 | 0 | 2 |
| E0MISS_PEET (pe, obj 99) | 0 | - | - | 0 | - | 2 |
| E0MISS_PERR | 0 | - | - | 0 | 0 | 2 |
| E1RET_ETC (coarse) | 0 | - | - | 1 | - | 0 |
| E1RET_RRC (coarse recovery) | 1 | 1 | 1 | 1 | 1 | 2 |
| E1RET_PEET (pe 901,10) | 1 | - | - | 0 | - | 2 |
| E1RET_PERR / E1CNT_PERR / E1VFY_PERR | 1 | 1 | 1 | 0 | 0 | 2 |
| E1B_PEET (pe 902,30) | 0 | - | - | 1 | - | 0 |
| E1B_PERR | 0 | 0 | 1 | 1 | 1 | 2 |
| EPOCHS_E1 | era=0 erb=1 n=1 | - | - | - | - | - |
| E2RET_PEET | 0 | - | - | 1 | - | 0 |
| E2RET_PERR / E2CNT_PERR / E2VFY_PERR | 0 | 0 | 1 | 1 | 1 | 1 |
| E2RET_PERR2 (amortization) | 0 | 0 | 1 | 0 | 0 | 1 |
| EPOCHS_E2 | era=1 erb=2 n=2 | - | - | - | - | - |
| E3RET_PEET | 0 | - | - | 1 | - | 0 |
| E3RET_PERR / E3CNT_PERR / E3VFY_PERR | 0 | 0 | 1 | 1 | 1 | 0 |
| EPOCHS_E3 | era=2 erb=3 n=2 | - | - | - | - | - |

Kill-bar adjudication: K1 prereg commit 5b7db4f94 strictly precedes the
implementation commit 29b51d26d (verified git log order). K2 safebin, no
python3/python, pinned znc znc_linux_x86_64_abed8aa1. K3 builds clean,
exit 0, empty stderr on all 3 runs. K4 E1 pe lines: spec=1, gen=1,
agree=1, refuse=0, resp=0 (all three families); coarse E1RET_RRC in the
same run: refuse=1, resp=1, spec=1, agree=1 (the priced rebuild
reproduced). K5 E1B_PEET: spec=0, refuse=1, kbs=0; E1B_PERR: spec=0,
gen=0, agree=1, refuse=1, resp=1, kbs=2>0. K6 E2RET_PEET: spec=0,
refuse=1, kbs=0; E2 pe RR lines: spec=0, gen=0, agree=1, refuse=1,
resp=1, kbs=1>0 (all three families). K7 E2RET_PERR2: spec=0, agree=1,
refuse=0, resp=0; E3RET_PEET: spec=0, refuse=1, kbs=0; E3 pe RR lines:
spec=0, gen=0, agree=1, refuse=1, resp=1 (kbs=0: rebuilt buckets
legitimately empty, A1-analog). K8 E0MISS_PERR: spec=0, refuse=0,
resp=0, kbs == E0MISS_PEET kbs. K9 E0RET_PERR: spec=1, gen=1, agree=1,
refuse=0, resp=0, kbs == E0RET_ETC kbs. K10 EPOCHS_E1: era=0, erb=1,
n=1; EPOCHS_E2: era=1, erb=2, n=2; EPOCHS_E3: era=2, erb=3, n=2. K11
3/3 byte-identical (sha256
9caa0a3b33f544b8f11cba771e51bd42d9b8cfc9ad851c1b8ff2e48772b0bb1a
across pe_run1/2/3.txt). K12 ASCII-only, no world literals in
pe_*.zag, one fn main. **12/12 PASS.**

## Tested findings

1. **The E1 rebuild-for-correct-answers cost is eliminated, measured end
   to end.** Same run, same drifted world: coarse E1RET_RRC pays
   refuse=1, resp=1 (one full family rebuild) to restore answers that
   were already correct (spec=1=gen); per-relation E1RET_PERR /
   E1CNT_PERR / E1VFY_PERR pay refuse=0, resp=0 with identical answers.
   The finer scheme does not merely defer the cost: no rebuild is owed,
   because the queried relation's epoch (0) still matches its tag. H1
   confirmed.
2. **The gate discriminates relations on one drifted world.** E1RET_PERR
   (first relation) hits while E1B_PERR (second relation, same world,
   same stage) refuses and recovers. This 901-hit / 902-refuse split is
   the discrimination the coarse scheme cannot express, and it rules out
   the degenerate reading of H1 (a gate that never refuses would pass K4
   and fail K5). H2 confirmed.
3. **No new staleness surface on answer-changing drifts.** E2 (relation
   swap) and E3 (deletion rebuild) both refuse on the queried relation
   (refuse=1, kbs=0: pre-scan veto, bucket never read) and recover to
   agree=1 with gen=0 on all three families. Every drift that changed the
   queried relation's answers refused on it. H3 confirmed.
4. **Recovery keeps the parent protocol's properties.** E2RET_PERR2:
   refuse=0, resp=0 (one-time cost); E3 refuses again after E2's restamp
   (repeatable, not one-shot); E0MISS: no re-specialize on a silent miss
   with matching relation epoch (decision rule intact); E0: healthy-world
   values and kb counts identical to the coarse baseline (zero behavior
   change, zero added scan iterations). H4 confirmed.
5. **The epoch table is exactly as small as the claim needs.** Measured
   occupancy: n=1 after E1 (only the touched relation), n=2 after E2/E3;
   epochs era/erb track the per-relation bump history exactly (0/1, then
   1/2, then 2/3). A wrong epoch in either direction would have meant
   spurious refusal or staleness; K10 pins both. H5's storage half
   confirmed as measured.

## Reasoned analysis (not directly tested; argued from the tested results)

### Does per-relation granularity earn its complexity?

The measured E1 price of the coarse scheme is one re-specialize event per
family query (refuse=1, resp=1 per family in the parent lane; reproduced
here as E1RET_RRC refuse=1, resp=1) paid for answers that were already
correct. The per-relation scheme pays zero of these on E1 (refuse=0,
resp=0 on all three families) with byte-identical answers. That is the
saving, and it is measured, not modeled.

The complexity it buys:

- Storage: coarse = 1 i32 slot (4 bytes) at A[772]. Fine = epoch table:
  4-byte count + up to 8 entries x 8 bytes = 68 bytes max at A[776..844];
  8 bytes per touched relation. It grows with distinct touched relations,
  never with world size or fact count (measured n: 1 -> 2 -> 2).
- Gate cost per spec call: coarse = 1 get32 + 1 compare. Fine = linear
  scan over at most n table entries (n<=8 here, n=2 in this world): at
  most n x (2 get32 + compare). O(touched relations) per call, constant
  in world size.
- Specialize stamp cost: coarse = 16 set32 with one epoch. Fine = 16 x
  (1 get32 for the bucket's relation + table scan + 1 set32).
- Drift bump cost: coarse = 1 set32. Fine = (#touched relations) x
  (scan + set32); 1 on E1, 2 on E2/E3.
- Recovery unit cost: identical (one family rebuild per refused family
  per drift). The saving is entirely in refusal frequency, not in the
  rebuild itself.

Verdict on the trade: yes, it earns it on the tested evidence. The saving
is a full rebuild per family per unrelated drift (the dominant term: a
world scan per family), while the added cost is a constant-factor gate
(scan over <=2 entries) plus 64 bytes of table. The gate cannot refuse
spuriously without K10 failing, and it cannot miss real drift without
K5/K6 failing; the bars pin both directions. Where it would NOT earn it:
a world where every drift touches every queried relation (then n equals
the relation count and refusals equal the coarse scheme's, while the
table + scan are pure overhead). The E1 regime (localized drift, broad
queries) is where the fine scheme wins; the experiment characterizes
that regime rather than claiming universality.

### Bug or design limitation (of the baseline)

Design limitation, same family as the parent lanes. The per-world epoch
made refusal a function of world identity; any localized drift vetoed
every query. Per-relation epochs make refusal a function of the queried
relation's change history, which is the finest granularity at which the
staleness question ("did what I know about THIS relation change?") can
be answered without reading the bucket. No new modes, bridges, or
handlers: one table, one scan, one compare.

### Honest scope limits

- The bump rule is implemented by the drift constructors: the world
  mutators know which relations they touched. A real deployment needs a
  store that maintains per-relation versions on write; the experiment
  does not test inferring the touched relation from a raw diff.
- The 8-entry table cap is a test-harness bound, not a mechanism claim;
  the tiny world never approaches it (max n=2).
- The recovery unit is still the whole bucket family, not the refused
  bucket: coarse recovery to match fine refusal. Targeted per-bucket
  re-specialize remains follow-up work (as in the parent report).
- Single retry only, inherited from the parent protocol. Epoch
  wraparound (i32 overflow) and multi-world tagging remain untested,
  inherited from SPEC-EPOCHTAG.
- E3 bumps the second relation's epoch too: the rebuild removed one of
  its facts, so under the stated content-change rule its fact set did
  change. The granularity is "per relation whose fact set changed", not
  "per relation the researcher intended to drift".
- The E1 win is demonstrated for localized drift; the report's tradeoff
  paragraph above states the regime where the fine scheme would not earn
  its complexity.

### Battery cost

None. `da_learn.zag` is byte-unmodified, the DA battery is untouched,
and the pe variants live entirely in lane-local files. The parent lanes'
battery-amendment note applies unchanged: do not merge epoch machinery
into `da_learn.zag` without refusal-aware kill bars (now per-relation
refusal-aware).

## Recommendations

1. Adopt per-relation epochs as the staleness signal wherever the
   refusal-recovery protocol is used: the E1 cost is real, measured, and
   eliminated, and the table + scan complexity is bounded and pinned by
   K10.
2. Next experiments, in order: (a) the drift-rate vs query-rate sweep
   (parent follow-up) now has a cheaper eager default to price against;
   (b) targeted per-bucket re-specialize, to attack the recovery unit
   cost the same way this lane attacked the refusal granularity;
   (c) a store-side per-relation version counter, to move the bump rule
   out of the drift constructors and into the world itself.
3. Keep `pe_*.zag` out of `da_learn.zag` until the DA battery gains
   per-relation refusal-aware kill bars.

## Process notes

- Pure Zag throughout; safebin mandatory (`which python3`/`which python`
  empty, recorded in NAMECHECK.md Step 0); pinned znc
  `znc_linux_x86_64_abed8aa1`; no Python invoked at any point.
- Git via `/usr/bin/git` directly (safebin git symlink breaks writes with
  EPERM per AGENTS.md lesson); explicit pathspecs; commits local, never
  pushed.
- Commit order: 5b7db4f94 (frozen prereg K1-K12 + NAMECHECK, alone) ->
  29b51d26d (implementation + outputs). (One retry on the prereg commit:
  the first attempt placed `-m` after `--` and git parsed it as a
  pathspec; recommitted correctly. No files were affected.)
- One hygiene-check iteration during build: the emitted epoch fields were
  first named `e901=`/`e902=` and tripped the no-literals grep in
  pe_main.zag; renamed to `era=`/`erb=` (relation-A/B epoch) before the
  first full run. K10's measured values are unchanged; only the field
  labels differ from the prereg text. No frozen bar affected, no
  amendment needed.
- All 12 kill bars passed on the first full run with no bar-calibration
  iteration: every frozen expected value in the prereg table matched the
  measured output exactly.
- Repro: `./pe_build.sh` assembles `pe_full.zag`, builds with the pinned
  znc, runs 3x, checks byte-identity and all kill bars. All sources and
  logs are in this lane directory.
