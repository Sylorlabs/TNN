# PREREG_COMPRESS: OpScope subsystem elimination via learner-owned structures (FROZEN)

Date: 2026-09-30 UTC. Worker: Learner Architecture-Compression.
Status: FROZEN. Committed alone before any implementation exists.
Governs: docs/lab/research-lead/overnight-20260928/learner_compress/compress_learn.zag

## Background

LEARNER-DEV-PASS (fd8757ba9; prereg 980981716) integrated the OpScope
R1R4 operator-discovery learner as episode P12 by composition: the
verbatim 421-line OpScope learner plus a private 8400-byte state slice
at W[2048..10448] with its own bespoke format. The P12 worker recorded
this as architectural debt under the ONE-SYSTEM RULE (standing
2026-09-30): each new P-episode adds ~1000 lines and a new state
format. This prereg freezes the compression design that eliminates the
slice.

## Frozen state map (what the 8400-byte slice stores)

Byte offsets into the slice, per opscope_learner.zag at c60bfbe7a:

- 0: cnt[12][12] i32 (576): DEFAULT unit/feature co-occurrence tallies.
- 576: occ[12] i32 (48): DEFAULT per-unit occurrence counts.
- 624: cntO[8][12][12] i32 (4608): operator-conditioned tallies.
- 5232: occO[8][12] i32 (384): operator-conditioned occurrence counts.
- 5616: oprec[8][6] i32 (192): operator records
  (trigger, scope_rule, sig, support, created_at, active).
- 5808: dstat[12][4] i32 (192): per-candidate (sup, mtch, sforms, epc).
- 6000: epstore[100][6] i32 (2400): stored episodes (U0,U1,U2,U3,n,T).

Computations: learn_keep (episode store + epc), learn_event (residual
signature tallies), learn_update (routed grounding), interpret
(compositional prediction), gate_pass (signature-vs-baseline replay
gate), proposal_check (admission), reground (anti-pollution replay
install), retire_check, diag_bars.

## Frozen compression design

Key observation: cnt/occ/cntO/occO (5616 bytes) are DERIVED state. They
are pure functions of the episode history plus the installation
schedule, which is itself deterministic in the episode history. The
existing reground replay already proves rebuild-from-experience: it
zeroes the tallies and replays the episode store through the router.
The compressed design therefore never persists tallies at all.

Persistent learner-owned state (replacing the slice):

1. Episode experience: DDES hypothesis ledger entries e7, e8, e9
   (W[16384..32768], via the existing ent_base/w_get/w_set accessors).
   Each entry holds 48 episodes as 6-i32 records (U0,U1,U2,U3,n,T).
   Entries e2/e5/e6 (P9/P11) are untouched. This is the learner's
   existing persistent-experience store, not a new format.
2. Learned structure: stress-store facts (930+k,1,packed) for k=0..7,
   via the generic learn()/find_key() machinery (earning, importance,
   eviction apply). packed = trig | scope<<4 | sig<<8 | sup<<12 |
   created<<20 | active<<28. Subjects 930..937 are unused by P1-P12.
   The installed operator is learner state with importance, not a
   bespoke record.

Transient working memory (not in W, rebuilt every run):

3. TR = z_alloc(5808): cnt/occ/cntO/occO/dstat at the same internal
   offsets 0/576/624/5232/5616 as before. All tally functions operate
   on TR unchanged. dstat stays transient because it is
   discovery-process working memory consumed only at training
   checkpoints; the generic fact store cannot hold it without eviction
   risk mid-discovery, and nothing reads it after training.

Algorithm: the discovery procedure (proposal/gate/reground/retire) is
unchanged in logic; only state accessors change (tallies via TR,
episodes via ledger get_ep, oprec via facts). The F4 ablation runs
baseline() directly instead of copying a deactivated slice: interpret
with no active operator equals or_default over the full span, which is
exactly baseline(), so the numbers are identical.

P1-P11 (lines 1..888 and main through the P11 block) are copied
verbatim from dev_learn.zag at fd8757ba9. The OpScope world
(gen_episodes and helpers) is copied verbatim: it is the frozen
battery environment, excluded from the F3 learner audit, and any
change risks behavioral drift.

## Frozen predictions

C-A (no regression): output lines 1..237 (through "STATEHASH P11")
byte-identical to RUN1.txt at fd8757ba9 (same bar as P12-C).
C-B (behavioral): P12-A through P12-E reproduce exactly as frozen in
PREREG_P12.md: installed_now=1 at seen=40 only; final OPREC k=0 trig=1
scope=0 sig=0 sup=12 created=40 active=1; TEST_ACC 20/20; F1=F2=1;
F4=1 with t1_full=3 t1_abl=0 acc_abl=17 negdrop=3; F5=1 size=3/3;
P12_DEV 3/3; P12_FOUNDATION 8/8; P12_CORR 2/2; 3/3 byte-identical runs,
exit 0, zero stderr. Diagnostic line formats (P12_CHECK/P12_DIAG/
P12_OPREC_TABLE) are kept identical; STATEHASH P12 value is expected
to differ (stress-store contents differ by the oprec fact) and is not
a prediction.
C-C (slice gone): the string "2048..10448" and the 8400-byte slice do
not appear in compress_learn.zag; no W slice carries OpScope format.
C-D (source delta): compress_learn.zag total lines <= 2380
(dev_learn.zag at fd8757ba9), i.e. net cognition-source delta negative
or neutral. Zero new modes, bridges, handlers. Pure Zag. Dash-clean
per worker_snippets/check_no_dash.sh. Contaminated paper untouched.
C-E (F3): the compressed learner section contains zero string
literals (same bar as the verbatim learner).

Positional scope restriction (from PREREG_P12.md) is inherited
unchanged: position-contingent operator installation only.

## Verdict mapping

COMPRESSION-PASS iff: this prereg strictly precedes the implementation
commit (git merge-base --is-ancestor), AND C-A through C-E all hold.

COMPRESSION-FAIL iff: any of C-A through C-E misses, or the slice
survives in any form, or a new mode/bridge/handler appears.

If compression proves impossible without behavioral loss, the finding
is reported as COMPRESSION-FAIL with the exact resistance documented;
no bar is moved.

Honest ceiling: bounded L2 (inherited). The gate and candidate
structure remain researcher-supplied; this task is architectural
compression, not representational invention.
