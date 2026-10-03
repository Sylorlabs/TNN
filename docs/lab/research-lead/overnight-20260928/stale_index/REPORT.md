# REPORT: STALE-INDEX-RECOVERY

## Verdict: all 8 kill bars green (SI-R1, SI-P1, SI-P2, SI-B1, SI-B2, SI-B3, SI-K1, SI-H1)

Non-ledger task. Branch `tnn-native-lab`, lane
`docs/lab/research-lead/overnight-20260928/stale_index/`, file prefix
`si_`. All commits local, never pushed.

## What was built

Act 4 (stages S13A-S13F) on top of the HOOK-COMPOSITION binary, as a
dedicated follow-up to its Amendment N1 finding: the L-state
spec-procedure indexes are world-relative (fact indices into the live
world), and a world restore without re-specializing made `ret_spec`
return 0 subjects, handled reactively by self-trigger (bounded retries,
coverage retired, generic fallback, agree).

Additive only: si_base/world/module.zag are byte-copies of hc_*;
si_learn.zag is hc_learn.zag plus the three staleness signals
(`world_ck`, `spec_nf_stale`, `spec_ck_stale`, `spec_ver_stale`), the
proactive recovery (`spec_ensure_fresh`), and additive checksum/epoch/
step-counter stores in the three `specialize_*` functions; si_main.zag
is hc_main.zag plus a flag-gated proactive block in do_query (S+930,
zero through Acts 1/2) with Act 3 (S12) replaced by the S13 battery.
No mechanism redesigned.

## Design answers

**Q1: which signal detects staleness before a 0-subject return?**
Fact count: NO. The S13B probe on the exact N1 condition (A2-built
indexes, live world A, both 56 facts) printed
`SI-PROBE nf_stale=0 ck_stale=7 ver_stale=7`: the count signal is blind
to reorder-class staleness. It is retained as recorded metadata but
excluded from the recovery predicate. Content checksum: YES (7/7).
World epoch: YES (7/7). The adversarial same-nf mutation (S13D: one
603-fact's object duplicated, nf still 56) confirmed the same split:
`nf_stale=0 ck_stale=7 ver_stale=7`.

**Q2: proactive or reactive?** Proactive wins, in the epoch form, after
a short amortization. SI-VERDICT: `proactive_total=984`
`reactive_total=1152` over one stale event plus 8 follow-up queries.
The reactive path is not replaced: it remains the safety net for any
mutation the epoch instrumentation misses (exactly the N1 bug class),
and it was reproduced live as the baseline.

**Q3: honest costs.** Reactive: 2 wasted spec attempts (cs 16+16),
1 generic attempt (cs 56), then every later query pays generic (56)
instead of indexed (16): 1152 total over the window. Proactive: one
re-specialization (336 fact visits: 168 build + 168 checksum record),
then 16 per query: 984 total. Break-even is about 5 queries including
the symmetric oracle overhead (about 7 on learner work alone). A
per-query CHECKSUM check would be a net loss (168 visits per check vs
40 saved per query); the checksum stays off the hot path as
stage-level instrumentation and as the audit signal for
uninstrumented changes. The hot-path check is 3 epoch compares.

## Results per bar

- SI-R1 regression: PASS. si_run1.txt lines 1-97 byte-identical to
  hc_run1.txt lines 1-97.
- SI-P1 signal split (N1 reorder): PASS. `nf_stale=0 ck_stale=7
  ver_stale=7`, before any spec call.
- SI-P2 signal split (adversarial same-nf): PASS. Identical probe
  line after the in-place object duplication.
- SI-B1 reactive reproduces N1: PASS. S13E has exactly 2 RETRY lines;
  SIQ0R ran 3 attempts: (agree=0,vers=2), (agree=0,vers=2),
  (agree=1,vers=0); RETRY att=1 `dc=1,0,0 active=1,1,1`, att=2
  `dc=2,0,0 active=0,1,1` (3000-contract retired on the second
  disconfirmation, as designed).
- SI-B2 proactive recovery: PASS. S13C has zero RETRY lines; SIQ0 is
  one Q line (st=2 vers=2 agree=1, answer {611}); `SI-AUTO
  entry_mask=7` proves the inline check fired before compose.
- SI-B3 adversarial proactive: PASS. S13D has zero RETRY lines; SIQ0A
  one Q line (st=1 vers=2 agree=1).
- SI-K1 cost: PASS. 984 < 1152 from the frozen SI-COST lines.
- SI-H1 toolchain/hygiene: PASS. Safebin from the first command, pure
  Zag, pinned znc; prereg committed alone before implementation; 3/3
  byte-identical (sha256
  ab4af44c7aeffae304d6754dcf40f2ec89334d5e489ae654c0702ccb748a9858),
  stderr empty, exit 0; zero em/en dash bytes in authored files (the
  86 A0102 compiler warnings in si_compile.txt are byte-count
  identical to hc_compile.txt); no world literals in new executable
  code (rels/objs/tags/goals all runtime-derived; the S13D mutation
  used runtime-derived fact indices 4 and 5).

SUMMARY-SISTALE (frozen, reproduced exactly):
`agree=26 plans_built=5 plans_loaded=26 trials=12 declines=0 cs=1680
cg=3640 hook=1 covdc=2,0,0 steps=2128`.

## Recommendation

Put the epoch check on the query path (3 compares, re-specialize on
mismatch, reactive trigger-B stays as the safety net); keep the
checksum as a periodic audit against instrumentation misses; drop
fact count from the recovery predicate (keep it as metadata). The
open placement question is learner-owned epoch stamping: in this
experiment the epoch is bumped by stage (harness) code, while the
checksum is the only signal the learner computes unilaterally from
the world. The world mutator itself should stamp the epoch.

## Follow-ups (not claimed here)

1. Learner-owned versioning: move the epoch bump into the
   world-mutation operations (fact_add, setup_world*) instead of
   stage code.
2. Checksum audit policy: how often to run the content checksum
   against epoch misses, and what a mismatch triggers.
3. Cost structure at scale: the break-even point as nf and bucket
   sizes grow; sublinear index rebuild.
4. Proactive placement: do_query entry (this experiment) vs inside
   compose at spec-dispatch time.

## Commits (local only)

- (prereg + namecheck, alone, pre-implementation)
- (implementation: si_*.zag sources + si_build.sh)
- (artifacts: si_full.zag, si_bin, si_compile.txt, si_run1/2/3.txt/err)
- (this report)

## Artifacts

- `si_base/world/module/learn.zag`: sources (base/world/module
  byte-copies of hc_*; learn = hc_learn + signals + recovery)
- `si_main.zag`: hc_main + flag-gated do_query block, S13A-S13F
- `si_build.sh`: build script
- `si_full.zag`, `si_bin` (sha256
  38b7f8a1647fb6db316fb0d5684ca442e27865a0ae2524246bed320f24b0eaaa)
- `si_run1/2/3.txt`: 3/3 byte-identical (137 lines), stderr empty
- `si_compile.txt`: clean compile log (86 pre-existing A0102 notes,
  same as hc)
