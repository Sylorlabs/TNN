# MINI-PREREG M3 — Decision-trace equivalence

> **FROZEN — 2026-09-25** under `PREREG_GATE_EXPANSION.md`.
> Method: certify the decision PATH, not the output. Replay compares
> what came out; this compares how it was decided, and proves no
> volatile read occurred anywhere along the way.

## 1. Hypothesis

Output-identity is a weak proxy: two runs can agree while taking
different paths (masked nondeterminism), and a plant can read entropy
without it reaching the output (P12-class). A decision trace — every
branch outcome, every read classified by memory region, every external
input — makes the path itself the evidence. The checker verifies two
properties: (a) no trace event touches a volatile region (static proof
over the trace), (b) traces are equivalent across adversarial runs
(dynamic proof of path determinism).

## 2. Decision procedure (frozen)

**Tracer** `m3_tracer.zag`: the variation module is built with trace
emission at instrumentation points (source-level, committed
instrumentation map):

- `T-BRANCH <site-id> <taken:0/1>` — every conditional on state/input.
- `T-READ <site-id> <region> <nbytes>` — every read, with region ∈
  {INIT-HEAP, UNINIT-HEAP, STACK, STATIC, ENV, CLOCK, FD:<n>}.
  Region classification is by the instrumented allocator + a region
  table (brk/mmap ranges recorded at startup; env block range recorded;
  clock/fd reads tagged at the call site).
- `T-EXT <site-id> <fd> <nbytes>` — every external input (stdin, files,
  sockets).
- `T-OUT <site-id> <nbytes>` — every output write (lengths only, not
  content — the trace stays small; content equality is replay's job).

**Checker** `m3_checker.zag` (pure Zag, pinned toolchain) takes two
traces (run A clean-heap, run B dirtied-heap + shifted env) and:

1. **Static volatile-read rule:** any `T-READ` with region ∈
   {UNINIT-HEAP, ENV, CLOCK} or any `T-EXT` with fd ∉ {0,1,2,allowlisted
   data fds} → `FAIL` with the offending event cited. (No output
   analysis needed — the read itself is the violation.)
2. **Trace-equivalence rule:** the event sequences must be identical
   modulo `T-OUT` lengths (lengths must match exactly; branch outcomes
   must match exactly). Any divergence → `FAIL` with first divergence.

**Verdict:** both rules hold → `PASS`; else `FAIL` (+cited event).

## 3. Battery mapping (pre-declared scope — frozen)

| Plant | Expected | Rationale |
|---|---|---|
| P01 getrandom | FAIL (rule 1) | syscall read tagged CLOCK/entropy region |
| P02 clock_gettime | FAIL (rule 1) | CLOCK region read |
| P03 /dev/urandom | FAIL (rule 1) | T-EXT on non-allowlisted fd |
| P04 uninit read | FAIL (rule 1) | UNINIT-HEAP region read |
| P05 env-var | FAIL (rule 1) | ENV region read |
| P06 ASLR leak | FAIL (rule 1 or 2) | pointer bytes read from STACK/heap then emitted; region-tagged |
| P07 rdtsc | FAIL (rule 1) | instruction-level; tracer tags rdtsc intrinsic reads as CLOCK |
| P08 hash order | FAIL (rule 2) | iteration order affects T-BRANCH/T-OUT sequence across heaps |
| P09 innocent tables | PASS (clean) | INIT-HEAP reads, deterministic order — correctly not flagged |
| P10 machine-id | FAIL (rule 1) | T-EXT on non-allowlisted fd (file open of /etc/machine-id) |
| P11 argv[0] bytes | FAIL (rule 1) | argv region tagged ENV-equivalent (process-external input) |
| P12 invoke-discard | FAIL (rule 1) | the invocation emits a T-READ CLOCK event even though unconsumed — this is M3's designed advantage over replay |

**Counting rule (frozen):** FAIL on dirty = CAUGHT; P09 must PASS
(deterministic tables are clean — the v2/v3-killer shape is correctly
not flagged). No out-of-scope declarations: M3 claims full coverage;
any miss kills.

**K-CLEAN mapping:** C01,C02,C04,C05,C06 must PASS. C04 (allowlisted
file IO): the data-fd allowlist is committed pre-test; reads from those
fds are clean. C03 (fenced RNG): declared OUT-OF-SCOPE pre-test — the
seeded RNG's reads are deterministic but region-tagged CLOCK-equivalent;
the tracer cannot distinguish seeded from unseeded at the trace level
(documented limitation).

## 4. Kill-bar instantiation

- K-CATCH: 12/12 decided correctly (11 FAIL + P09 PASS).
- K-CLEAN: 5/5 PASS (C03 out-of-scope pre-test).
- K-RED: 12 novel plants, blind, per umbrella §5. Expected red focus:
  region-spoofing (make a volatile read LOOK like INIT-HEAP — e.g.
  launder clock bytes through an init-heap buffer then read the buffer;
  the red team knows the region taxonomy), trace-suppression (skip
  instrumentation points via computed jumps), event-flooding.
- K-DET: 3/3 byte-identical full-battery reruns (traces stable).

## 5. Known hard problems (stated pre-test)

1. **Laundering through clean regions:** `clock → memcpy → init-heap
   buffer → read buffer` — the READ is INIT-HEAP (clean) but the VALUE
   is volatile. Frozen answer: the tracer ALSO tags VALUES (taint bit
   per 8-byte cell, propagated on copy; committed taint-propagation
   rules pre-test). A tainted value reaching T-BRANCH or T-OUT → FAIL.
   The crew implements byte-cell taint; fidelity is proven by a
   taint-propagation unit test (committed vectors) before battery runs.
2. **Instrumentation completeness:** an uninstrumented read is
   invisible. The crew commits the instrumentation map (every read site
   in the module enumerated from the source) and a coverage check (trace
   event count == static site count × dynamic hits, reconciled) before
   testing. Gaps found later are method bugs, not red-team wins —
   recorded as such.

## 6. Evidence layout

`wave12/step1a-v2/gate-expansion/evidence/m3/`:
`tracer`, `checker`, instrumentation map, taint unit-test vectors,
per-plant traces + verdicts, `M3_VERDICT.md` with the kill table.
