# SPEC-LAZY-DEFAULT: REPORT

**Lane:** docs/lab/research-lead/overnight-20260928/spec_lazy_default/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Local commits only, never pushed.
**Verdict: BUILD-PASS (11/11 frozen kill bars)**

## Summary

Adopted SPEC-DRIFTRATE-SWEEP recommendation #1: lazy on-demand recovery is
now the DEFAULT recovery policy in code, and eager rebuild-on-drift is
reachable only through an explicit-justification entry point. 75 episodes
(25 drift/query cells x 3 policy arms), one binary, pure Zag, safebin-built,
3/3 byte-identical
(sha256 2d42b55142669608b4ab6889ccec8ce8b32e74e30cdfb7665b7fd4fb5c08c3c8).

The policy layer (`ld_spec.zag`): the default query path goes through the
byte-unmodified rr_ret_spec wrapper (lazy on-demand rebuild, no
justification needed). The eager entry `ld_query_eager` requires just != 0;
an eager request with just = 0 is refused by the policy layer, flagged
fb = 1, and routed through the default path. No eager restamp can fire
without a recorded justification.

Measured: the default arm reproduces the parent lane's LAZY arm exactly on
all 25 cells (rebuilds = min(D, Q), answered = Q, refusals = rebuilds), and
the justified-eager arm reproduces the parent's EAGER arm exactly
(rebuilds = D, answered = Q, refusals = 0). The unjustified-eager arm
falls back to the default on all 25 cells (fb = 1, numbers identical to
default). The rebuild saving of the default vs eager reproduces the 1/k
waste curve exactly: W = max(1, 1/k), 16x at k = 1/16, 1x at saturation.
The eager tax D - min(D, Q) is exact in every cell; the per-avoided-refusal
price is W(k) - 1 rebuilds (15 at k = 1/16, 0 at k >= 1), which is the
measured price any explicit latency justification for eager must beat.

## What was tested

Assembly: `ld_full.zag` = da_base + rb_world + et_world + da_module +
da_learn + rb_fix + et_spec + rr_spec + ld_spec + ld_main, all reused
sources byte-unmodified; only ld_spec.zag (policy layer) and ld_main.zag
(harness) are new. Repro: `./ld_build.sh`. Per-episode fresh world
(rb_setup + explicit epoch reset, ret family specialized at epoch 0).

Per-cell results (D = drifts, Q = queries, k = M/N queries per drift;
DEF/E = default/eager rebuilds; tax = E - DEF; W = E/DEF):

| M | N | D | Q | k | DEF rb | EAGER rb | tax | W |
|---|---|---|---|---|--------|----------|-----|---|
| 1 | 1 | 256 | 256 | 1/1 | 256 | 256 | 0 | 1 |
| 1 | 2 | 256 | 128 | 1/2 | 128 | 256 | 128 | 2 |
| 1 | 4 | 256 | 64 | 1/4 | 64 | 256 | 192 | 4 |
| 1 | 8 | 256 | 32 | 1/8 | 32 | 256 | 224 | 8 |
| 1 | 16 | 256 | 16 | 1/16 | 16 | 256 | 240 | 16 |
| 2 | 1 | 128 | 256 | 2/1 | 128 | 128 | 0 | 1 |
| 2 | 2 | 128 | 128 | 2/2 | 128 | 128 | 0 | 1 |
| 2 | 4 | 128 | 64 | 2/4 | 64 | 128 | 64 | 2 |
| 2 | 8 | 128 | 32 | 2/8 | 32 | 128 | 96 | 4 |
| 2 | 16 | 128 | 16 | 2/16 | 16 | 128 | 112 | 8 |
| 4 | 1 | 64 | 256 | 4/1 | 64 | 64 | 0 | 1 |
| 4 | 2 | 64 | 128 | 4/2 | 64 | 64 | 0 | 1 |
| 4 | 4 | 64 | 64 | 4/4 | 64 | 64 | 0 | 1 |
| 4 | 8 | 64 | 32 | 4/8 | 32 | 64 | 32 | 2 |
| 4 | 16 | 64 | 16 | 4/16 | 16 | 64 | 48 | 4 |
| 8 | 1 | 32 | 256 | 8/1 | 32 | 32 | 0 | 1 |
| 8 | 2 | 32 | 128 | 8/2 | 32 | 32 | 0 | 1 |
| 8 | 4 | 32 | 64 | 8/4 | 32 | 32 | 0 | 1 |
| 8 | 8 | 32 | 32 | 8/8 | 32 | 32 | 0 | 1 |
| 8 | 16 | 32 | 16 | 8/16 | 16 | 32 | 16 | 2 |
| 16 | 1 | 16 | 256 | 16/1 | 16 | 16 | 0 | 1 |
| 16 | 2 | 16 | 128 | 16/2 | 16 | 16 | 0 | 1 |
| 16 | 4 | 16 | 64 | 16/4 | 16 | 16 | 0 | 1 |
| 16 | 8 | 16 | 32 | 16/8 | 16 | 16 | 0 | 1 |
| 16 | 16 | 16 | 16 | 16/16 | 16 | 16 | 0 | 1 |

Uniform across all 25 cells: DEFAULT answered = Q, refusals = rebuilds,
kb = 2Q, just = 0, fb = 0; EAGER answered = Q, refusals = 0, kb = 2Q,
just = 1, fb = 0; EAGER0 fb = 1, just = 0, and rebuilds/answered/refusals
identical to DEFAULT. Cross-lane check: every default line is field-equal
to the parent lane's lazy line and every eager line to the parent's eager
line (modulo the added just/fb fields), so the policy change alters the
default without altering the measured economics.

Kill-bar adjudication: K1 prereg commit ba07e17d0 strictly precedes the
implementation commit (verified git log order). K2 safebin, no
python3/python, pinned znc znc_linux_x86_64_abed8aa1 (safebin/znc symlink,
same sha256). K3 builds clean (warnings only, no errors), exit 0, empty
stderr on all 3 runs. K4 all 25 default lines: answered = Q,
refusals = rebuilds, kb = 2Q. K5 all 25 eager lines: answered = Q,
refusals = 0, just = 1, kb = 2Q. K6 all 25 default lines:
rebuilds = min(D, Q) from the line's own D and Q. K7 all 25 eager0 lines:
fb = 1, just = 0, rebuilds/answered/refusals identical to the default line
of the same cell. K8 (1, 16): eager 256 = 16 * default 16; (16, 1):
eager 16 = default 16. K9 every cell: tax = D - min(D, Q); at (1, 16)
tax = 240 = 15 * default rebuilds. K10 75 CELL lines; every eager line
rebuilds = D. K11 ASCII-only, no world literals in ld_spec.zag/ld_main.zag,
one fn main, reused sources unmodified (git diff clean), no changes outside
this lane directory. **11/11 PASS.**

## Tested findings

1. **Lazy is now the default in code, not just in comparison.** The
   default query path needs no justification and never triggers an eager
   restamp (H1, H2): answered = Q and rebuilds = min(D, Q) on all 25 cells.
   The only route to eager rebuild-on-drift passes through the
   justification entry with just != 0.
2. **Unjustified eager is unreachable (H4).** All 25 eager0 lines carry
   fb = 1 with numbers identical to the default line of the same cell: the
   policy layer refused the eager request and served it lazily. A caller
   that "forgets" the justification silently gets the default, never
   eager.
3. **The default's rebuild saving reproduces the 1/k curve exactly
   (H5).** W = eager/default = max(1, 1/k) on all 25 cells: 16x fewer
   rebuilds at k = 1/16, identical cost at k >= 1. The adoption changes
   the default; it does not change the economics the parent measured.
4. **The eager tax is priced per avoided refusal (H6).** Tax = D - min(D, Q)
   in every cell; per-avoided-refusal price = W(k) - 1 rebuilds: 15 at
   k = 1/16, 7 at k = 1/8, 3 at k = 1/4, 1 at k = 1/2, 0 at k >= 1. The
   default's latency tax is refusals = rebuilds: each on-demand rebuild is
   bought by exactly one refused-then-retried query.
5. **Justified eager is unchanged (H3).** The eager arm reproduces the
   parent's eager arm line for line (rebuilds = D, refusals = 0): the
   justification entry preserves the zero-refusal option for callers that
   price it in.

## Reasoned analysis: when eager should be used

Eager's only advantage over the default is refusals = 0 (no query ever
waits for a rebuild); its only cost is the tax. Let C = one rebuild cost
and L = the deadline value of avoiding one refused-then-retried query.
Per drift interval the default pays min(D, Q) rebuilds for Q answers with
min(D, Q) refusals; justified eager pays D rebuilds for Q answers with 0
refusals. Eager is justified iff L > (W(k) - 1) * C, measured per k:

| k | W(k) - 1 (rebuilds per avoided refusal) | eager justified iff |
|---|---|---|
| 1/16 | 15 | L > 15C |
| 1/8 | 7 | L > 7C |
| 1/4 | 3 | L > 3C |
| 1/2 | 1 | L > C |
| >= 1 | 0 | always (tax is zero; either policy is free) |

At k = 1/16 a zero-refusal deadline must be worth more than 15 rebuilds
per useful answer to justify eager; at saturation eager costs nothing
extra, so the justification is vacuous but still recorded. The just token
on each eager line records that this pricing was accepted by the caller.
This is the explicit latency justification the parent recommendation
required: priced against measured W(k), not asserted.

## Adoption statement

Recommendation #1 of SPEC-DRIFTRATE-SWEEP is implemented: the standing
recovery policy is lazy on-demand (rebuild only when a query refuses).
Eager rebuild-on-drift is no longer the implicit default: it fires only
through `ld_query_eager` with just != 0, and the justification is recorded
on the output line. Future recovery proposals report rebuilds/answered
against 1/k and waste against max(1, 1/k) per the parent's recommendation
#3; the measured table above is the baseline they must beat.

## Honest scope limits

- One drift type (unrelated, repeatable) and one query family (RET),
  inherited from the parent lane; the policy mechanism is per-family and
  structurally identical for CNT/VFY, but the default was not re-swept
  there.
- Deterministic periodic schedules; the min(D, Q) default curve used the
  power-of-2 grid structure, as in the parent.
- The deadline value L is a policy input, not measured; the lane measures
  the price (W(k) - 1 rebuilds per avoided refusal), and the decision rule
  combines the two explicitly.
- Latency is counted in refusals (0 for justified eager), not wall-clock
  time.
- The justification token is a recorded claim (just = 1), not a verified
  deadline: the mechanism guarantees eager cannot fire unrecorded, not
  that the recorded L was honestly estimated.

## Battery cost

None. `da_learn.zag` byte-unmodified (verified via git diff in
ld_build.sh), the DA battery untouched, and all SPEC-EPOCHTAG,
SPEC-REFUSAL-RECOVERY, SPEC-RELATIONBLIND, and DISAGREEMENT-ATTRIBUTION
sources reused unmodified. All new code lives in ld_spec.zag / ld_main.zag
in this lane.

## Recommendations

1. Keep lazy on-demand as the standing default; require the just token on
   any future eager-recovery proposal, with L stated and checked against
   the measured W(k) - 1 column above.
2. The per-relation epoch follow-up (SPEC-PERRELATION-EPOCH) composes with
   this default: finer refusal granularity shrinks the default's own
   rebuild count, it does not change the default/eager policy structure.
3. If a future lane measures wall-clock rebuild cost C and query deadline
   value L in common units, the rule L > (W(k) - 1) * C becomes directly
   executable as an adaptive policy switch.

## Process notes

- Pure Zag throughout; safebin mandatory (`which python3`/`which python`
  empty, recorded in NAMECHECK.md Step 0); pinned znc
  znc_linux_x86_64_abed8aa1 (safebin/znc symlink, sha256-verified
  identical); no Python invoked at any point.
- Git via `/usr/bin/git` directly (safebin git symlink breaks writes
  with EPERM per AGENTS.md); explicit pathspecs; commits local, never
  pushed.
- Commit order: ba07e17d0 (frozen prereg K1-K11 + NAMECHECK, alone) ->
  implementation + outputs + this report. Two tooling iterations, neither
  touching the frozen bars: (1) git commit arg order (`-m` before `--`
  pathspec, same quirk the parent lane recorded); (2) a shell variable
  collision in ld_build.sh's K7 adjudication (K5's eager-arm temporaries
  overwrote the default-arm values K7 compared against) caught by the bar
  itself on the first run, fixed by per-arm variable names, all bars green
  on the rerun.
- No amendments: the frozen bars adjudicated as written.
- Repro: `./ld_build.sh` assembles `ld_full.zag`, builds with the pinned
  znc, runs 3x, checks byte-identity and all kill bars. All sources and
  logs are in this lane directory.
