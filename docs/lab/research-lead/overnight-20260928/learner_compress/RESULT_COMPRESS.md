# RESULT_COMPRESS: OpScope subsystem elimination via learner-owned structures

Date: 2026-09-30 UTC. Worker: Learner Architecture-Compression.
Implementation: docs/lab/research-lead/overnight-20260928/learner_compress/compress_learn.zag
Prereg: PREREG_COMPRESS.md (commit 08a0c0ac4, committed alone before implementation).
Kill bar K1 (prereg precedence): 08a0c0ac4 is a strict ancestor of the
implementation commit (verified by git merge-base --is-ancestor).

## Verdict: COMPRESSION-PASS

All five frozen prediction groups hold 3/3, the bespoke slice is gone,
and the source delta is neutral.

## Frozen predictions vs observed (3/3 byte-identical runs, exit 0, zero stderr)

C-A (no regression): output lines 1..237 (through "STATEHASH P11")
byte-identical to RUN1.txt at fd8757ba9. OBSERVED: cmp clean.

C-B (behavioral, PREREG_P12.md predictions):
- P12-A: installed_now=1 at seen=40 only; 0 at all other checkpoints.
  OBSERVED: exact. Final OPREC: k=0 trig=1 scope=0 sig=0 sup=12
  created=40 active=1, all other slots inactive. The OPREC table bytes
  match the original exactly.
- P12-B: TEST_ACC 20/20; F1=1; F2=1; F4=1 with t1_full=3 t1_abl=0
  acc_abl=17 negdrop=3; F5=1 size=3/3. OBSERVED: exact, including all
  P12_CHECK/P12_DIAG diagnostic lines byte-identical.
- P12-D: P12_DEV 3/3, P12_FOUNDATION 8/8, P12_CORR 2/2. OBSERVED: exact.
- P12-E: 3/3 byte-identical runs (sha256
  96e0a5baeb4e987a41688521224cf1c05a2baf4313d9e558d2b829bfc68b69d6),
  exit 0, zero stderr. OBSERVED: exact.
- STATEHASH P12 differs (TICK 383 vs 382, H 185079721 vs 40134816):
  EXPECTED per prereg (not a prediction). Cause: the operator install
  goes through the generic learn(), adding one tick and one fact
  lifecycle to the stress store.

C-C (slice gone): the strings "2048..10448" and "8400" do not appear in
compress_learn.zag. No W slice carries OpScope format. OBSERVED: grep
clean (0 hits each).

C-D (source delta): compress_learn.zag is 2380 lines, equal to
dev_learn.zag at fd8757ba9 (2380). Net cognition-source delta vs the
P12 integration: 0 (neutral, within the frozen bar). Zero new modes,
bridges, handlers, or hardcoded semantic cases. Pure Zag (shell only;
no python3 in implementation, diagnostics, or byte checks). Dash-clean
per worker_snippets/check_no_dash.sh. Contaminated paper untouched.

C-E (F3): the compressed learner section contains zero string
literals. OBSERVED: grep clean.

## What changed architecturally

The 8400-byte bespoke slice (cnt/occ/cntO/occO/oprec/dstat/epstore at
fixed offsets) is deleted. In its place:

1. Episode experience: 100 training episodes as 6-i32 records in DDES
   ledger entries e7/e8/e9, via the existing ent_base/w_get/w_set
   accessors. e2/e5/e6 (P9/P11) untouched. This is the learner's own
   persistent-experience store, not a new format.
2. Learned structure: the installed operator is stress-store fact
   (930,1,packed) under generic learn()/find_key(), with importance and
   eviction applying. packed =
   trig|scope<<4|sig<<8|sup<<12|created<<20|active<<28. Subjects 930..937
   were unused by P1-P12.
3. Transient working memory: TR=z_alloc(6000) holds cnt/occ/cntO/occO/
   dstat at the same internal offsets; never in W, rebuilt every run.
   The 5616 tally bytes were derived state (pure functions of episode
   history plus the deterministic install schedule); reground already
   proved rebuild-from-experience, so they persist nowhere. dstat is
   discovery working memory read only at training checkpoints; the
   36-slot fact store cannot hold it without mid-discovery eviction
   risk, so it stays transient by design.

The discovery procedure (proposal/gate/reground/retire) is logic-
unchanged; only state accessors changed. The F4 ablation no longer
copies a deactivated slice: interpret with no active operator equals
or_default over the full span, which is exactly baseline(), so the
ablation calls baseline() on the same tallies (identical numbers, the
W2 copy deleted).

Behavioral side effects of the honest treatment (all benign, none in
the frozen predictions): the oprec learn() emits one EVICT at seen=40
(victim: importance-1 junk fact 619 99); a post-test wave eviction
victim shifts from 619 99 to 930 1 (the oprec fact itself, importance
1, read by nothing after the test phase). The learned structure thus
lives under the same memory-pressure discipline as all learner state.

## ONE-SYSTEM RULE accounting

- Cognition source lines added (vs revert_learn.zag 1212): 1168, same
  as P12; net vs the P12 integration: 0 (neutral).
- New hardcoded semantic cases: 0.
- New modes: 0.
- New bridges: 0.
- New task-specific handlers: 0 (the P12 episode driver was rewritten,
  none added).
- Learner-state structures created: +100 episode records (DDES ledger,
  existing format), +1 operator fact (stress store, existing format),
  +6000 bytes transient working memory (not in W).
- Learner-state structures eliminated: the 8400-byte OpScope subsystem
  slice and its bespoke format; net persistent bespoke bytes -8400;
  formats eliminated: 1.

## Standing-question answer

"Why can the existing general architecture not learn this behavior?"
It can: no new general operation was needed. The slice's persistent
contents mapped onto owned structures (episodes to DDES ledger
experience entries; the operator record to a stress-store fact with
importance/eviction); its tallies were derived state that never needed
persisting. The closest thing to a missing general operation is a
first-class append/replay experience-sequence API on the DDES ledger
(currently raw ent_base arithmetic): an API nicety, not a capability
gap. The dstat tallies resist fact-slot expression only because they
are transient discovery working memory, not learned state; forcing them
into evictable slots would risk mid-discovery behavior change for no
architectural gain.

## Scope and ceiling

Positional scope restriction inherited unchanged from PREREG_P12.md:
position-contingent operator installation only, not position-general
negation learning. Honest ceiling: bounded L2 (inherited). The gate
and candidate structure remain researcher-supplied; this task was
architectural compression, not representational invention.

## Reproduction

Build: src/tools/toolchain/znc_linux_x86_64_abed8aa1 build
compress_learn.zag -o compress_learn_bin (exit 0; warnings are
pre-existing classes). Run: ./compress_learn_bin > RUN.txt. Expect
sha256 96e0a5baeb4e987a41688521224cf1c05a2baf4313d9e558d2b829bfc68b69d6,
P1-P11 byte-identical to fd8757ba9 RUN1.txt lines 1-237, and the C-B
values above.
