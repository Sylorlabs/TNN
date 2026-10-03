# REPORT: NT-RESIDUAL -- the rare-but-useful link that is NOT a revision target

## Verdict

**RESIDUAL-CONFIRMED** per the frozen verdict mapping (PREREG Section 8).
K1=1, K2=1, K3=1, K4=1, K5=1, K6=1, K7=1. Every frozen number --
ttcA/probeA/nevict/phev, all 6+6 per-pass probe flags, avail100,
avail160, c/nc/u/forget, bprobe, resprobe, all EVHIST bins,
evh(148), evh(118), evh(160), evh(161) -- matches the prereg
exactly. The hand-derived Section 5 trace was byte-exact against
the binary on the first run.

## Frozen results (3/3 byte-identical)

- Run digest: `6be7bc39438cf53b2980a4605deb4ab1b1f3aee4505dbae8f028163532ac2bf4`
- Binary digest: `c07bb48e70ba568190ebe3936d483452cc1558cd678d9eabee0b28cdbcfd4e03`
- Source digest: `25f935daa65c269475cec795c5a8bc10b5e57c9f0a4ab85fa52f7cbae5d28a2e`

```
NTRES R6 ttcA=2 probeA=8 nevict=12 phev=0
NTRES R6 PPROBE100 p1=0 p2=0 p3=1 p4=1 p5=1 p6=1 avail100=4
NTRES R6 PPROBE160 r1=0 r2=0 r3=0 r4=0 r5=0 r6=0 avail160=0
NTRES R6 RET c=2 nc=2 u=4 forget=0 bprobe=2 resprobe=0
NTRES R6 EVHIST 143=5 144=5 160=1 161=1
NTRES K1=1 K2=1 K3=1 K4=1 K5=1 K6=1 K7=1
NTRES VERDICT=RESIDUAL-CONFIRMED
```

## Kill-bar evaluation

- K1 (learnability): PASS. ttcA = 2 (1..50), probeA = 8. No VOID.
- K2 (retention of uncontested structure): PASS. nc = 2, u = 4.
- K3 (the residual bar): PASS. avail160 = 0 exactly -- the
  residual link never answers, as traced.
- K4 (final revision outcome): PASS. c = 2, forget = 0.
- K5 (pressure exercised, eviction discipline, mechanism
  attribution): PASS. nevict = 12 exact. evh(148) = 0 and
  evh(118) = 0 (the D5 pin still holds on the revision target).
  evh(160) = 1 AND evh(161) = 1 (white-box: the residual links
  ARE the pass-1 victims -- D5's pin never fires for them).
  phev = 0. EVHIST bins exact: 143=5, 144=5, 160=1, 161=1.
- K6 (discriminative validity): PASS. avail100 = 4 AND
  nevict = 12 > 0.
- K7 (the dissociation bar): PASS. avail100 = 4 AND avail160
  = 0 in the same run.

## What this establishes

1. **D5 does NOT protect the residual link (expected, confirmed).**
   Links (160,1)->161 and (161,1)->162 are genuinely useful --
   q(160) is probed every pass expecting 162 -- but are never
   contradiction targets: no ref++ ever has taught obj 160 or
   161, so no pendtgt ever points at them and the pin never
   fires. On pass 1 they are evicted (160, then 161) before the
   first q(160) probe reads them; they are never re-taught (K=6,
   pass-1-only), so they never return. avail160=0, resprobe=0,
   evh(160)=evh(161)=1. The NTNL honest limitation reproduces
   exactly as stated.
2. **The dissociation holds in a single run.** D5 is active and
   working on the revision-target link in the same run:
   avail100=4 (D4's L6 gave 0), evh(148)=0, and the pass-1/2 pin
   mechanism is identical to NTNL. The pin protects "where my
   beliefs are heading" and nothing else. This rules out the
   alternative reading that D5 was simply inactive.
3. **No learner-available signal in this workload could have
   predicted the residual link's usefulness (the finding).** At
   the three pass-1 eviction decision points the learner's entire
   information about 160/161 is: taught once, agreed,
   (sup1,ref0,F1,R0), installed youngest. The FREQ novels
   131/140/141/143 are (sup1,ref0,F1,R0), installed older. No
   contradiction has ever targeted 160 or 161 (no pin possible --
   pins are set only by ref++). The query stream has not touched
   them (the first q(160) probe comes after the pass-1
   teachings). The stored graph has in-degree 0 for both
   (nothing installed points at them; 160's role as a future
   query start is harness knowledge, not learner state). The
   ONLY distinguishing fact -- "q(160) will be probed every
   future pass" -- is oracle knowledge. The one
   learner-available query-stream signal that protects
   useful-but-rare links, D4's read count, requires surviving to
   the first read; the residual link does not. So the answer to
   the parent's question (4) is: in this workload it is
   fundamentally impossible -- not for lack of a cleverer rule,
   but because the distinguishing information does not exist in
   the learner's observable stream at the decision point.

## What this does NOT establish (honest boundaries)

- The impossibility claim is workload-relative (PREREG 5.3/9):
  no learner-available signal in THIS workload predicts the
  residual link. A teaching stream that carries the dependence
  (e.g. the residual keys taught adjacent to a query start the
  learner has already seen queried), or a query stream the link
  survives to meet, would change the analysis. That is a new
  lane, not an amendment -- this lane deliberately provides
  neither.
- No new protection rule is proposed or tested. The lane's job
  was to confirm the coverage limit and characterize what signal
  would be needed, not to patch D5.
- Single capacity point (CAP=20, 1.15x); single contradiction
  magnitude; M=6; single arm (K=6, LAST). The FIRST-order
  variant (residual taught first, surviving to its first read
  via D4's read protection) is the natural follow-up
  demonstrating the query-stream rescue; not run here.
- D1 checkpoints for 160/161 exist (evidence preserved) but are
  never consulted: PRESENCE failure, not evidence loss.

## Recommended follow-up (not preregistered; for the parent)

- A teaching-stream association lane: protect keys taught
  adjacent (in the teaching stream) to keys the learner has
  observed as query starts. This is the only remaining
  learner-available signal class this workload's design leaves
  untested, and it would need a world where the teaching stream
  carries the dependence.
- The stale-pin boundary (NTNL follow-up #2) still stands
  untested.
- The D5 churn cost curve across capacity points (NTNL
  follow-up #3) still stands untested.

## Provenance

- Prereg frozen alone: commit `8dc808fb4e839c3f3404b7f7304986db2345d1cc`
  on `tnn-native-lab` (PREREG.md + NAMECHECK.md only), strictly
  before implementation. Commit-order self-check: `git log`
  shows 8dc808fb strictly precedes the implementation commit
  below; no implementation file existed at prereg time.
  Committed via git plumbing (separate index file: read-tree /
  add / write-tree / commit-tree / update-ref with old-value
  check) with explicit pathspecs; the shared index untouched.
- Implementation + results: this commit. Pure Zag, safebin-only
  PATH, pinned znc 2026.07.0-dev (same build as NTNL). `which
  python3` and `which python` return nothing under the worker
  PATH. Zero forbidden-executable invocations. The string
  "python" appears nowhere in the source.
- Source: `ntres_full.zag`, written to PREREG Sections 2-4
  (learner: NTNL D1+D4+D5 verbatim; oracles: NTNL verbatim plus
  RESIDUAL teachings (160,1)->161, (161,1)->162 agree-only on
  K-passes, taught LAST just before RARE 148; q(160) per-pass
  probe; resprobe; EVHIST to 165). Layout note: checkpoint and
  eviction-histogram regions extended to subjs 100..165
  (160/161 are new keys; evbase=ckbase+1584, ptbase=evbase+264,
  alloc 2816) -- sizes only, no rule change.
- Build: `znc ntres_full.zag -o ntres_bin` under safebin-only
  PATH (exit 0; benign zagd-unavailable warning only, as in
  NTNL); 3/3 runs byte-identical (cmp), exit 0, zero stderr.
- Audit: no protection/task-label/freeze/importance/mode/
  usefulness-label logic in the learner beyond the frozen D5
  pin; the K selector and probe schedule are harness
  conditions. Compiler-defect workarounds honored (single-buffer
  cursor output + one raw syscall; no `as *i32`+slice; no
  `!(A && B)` in while conditions; no `[]u8 as *u8` casts;
  `_zag_malloc as *u8` threaded through).
- Commits local only, explicit pathspecs, never pushed. This is
  a non-ledger task (claim minting paused): no ledger update.
