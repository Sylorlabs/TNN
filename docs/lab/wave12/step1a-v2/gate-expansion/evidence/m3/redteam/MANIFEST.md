# M3 RED-TEAM MANIFEST — 12 blind plants (frozen 2026-09-25)

Blind red team for method M3 (decision-trace equivalence), Arm C gate-expansion.
The red team knew ONLY the method's public interface (event taxonomy, region
codes, taint rules, checker rules 1+2). No tracer/checker source, binaries,
instrumentation maps, or battery results were read. Nothing under
`evidence/m3/` was read except this `redteam/` directory itself.

## Build & validity

- Toolchain: pinned `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Build: `./build.sh` from this directory (b1's `@import` resolves relative to
  cwd; extern-shim plants a2/b2 link via `znc --dynamic --needed lib<name>.so.1`
  and run with `LD_LIBRARY_PATH=.` — same pattern the method crew's P07 used).
- Validity rule (frozen): each plant compiled and run TWICE; stdout SHA-256
  differs run-to-run (genuine nondeterminism), exit code 0, expected byte length.
- Entropy: `gettimeofday` (syscall 96) tv_usec bytes, or a 3-line C shim reading
  gettimeofday (disclosed per-plant; C used ONLY for the entropy read). Pure Zag
  otherwise. No RNG in the red team's decision paths (all choices deterministic).
- Miss definition (frozen): checker outputs PASS on a valid dirty plant.

## Plants

| # | File | Category | SHA-256 | Validity (2 runs) | Believed defeated |
|---|------|----------|---------|-------------------|-------------------|
| A1 | a1_gettimeofday_heap.zag | (a) region/taint laundering | `71308be5…0f3125c` | run1/run2 SHAs differ, 8 bytes, rc 0 | rule 1 (INIT-HEAP read, untainted cells), rule 2 |
| A2 | a2_extern_shim.zag (+a2_shim.c) | (a) region/taint laundering | zag `68feb369…d6bd6e`, c `47a31609…87839c7` | run1/run2 SHAs differ, 8 bytes, rc 0 | rule 1 (novel extern call-site not tagged) |
| A3 | a3_table_lookup.zag | (a) region/taint laundering | `8a013c0f…ade0b5d1` | run1/run2 SHAs differ, 16 bytes, rc 0 | rule 1 (index laundering; INIT-HEAP read) |
| B1 | b1_main.zag + b1_helper.zag | (b) trace suppression | main `a0224571…27081`, helper `294ea9eb…171af1` | run1/run2 SHAs differ, 8 bytes, rc 0 | rule 1 (read in uninstrumented import) |
| B2 | b2_extern_retval.zag (+b2_shim.c) | (b) trace suppression | zag `337d97fc…735a`, c `0cb9413e…15c1dbc` | run1/run2 SHAs differ, 8 bytes, rc 0 | rule 1 (no read site exists), rule 2 |
| B3 | b3_raw_syscalls.zag | (b) trace suppression | `d5b88ea7…0638a8` | run1/run2 SHAs differ, 8 bytes, rc 0 | rule 1 (no Zag-level read/write sites) |
| C1 | c1_straightline.zag | (c) equivalence gaming | `1d4109a7…6803d` | run1/run2 SHAs differ, 16 bytes, rc 0 | rule 2 (length-only T-OUT), rule 1 |
| C2 | c2_fixedloop.zag | (c) equivalence gaming | `49176889…10124d` | run1/run2 SHAs differ, 16 bytes, rc 0 | rule 2 (data-independent branches) |
| C3 | c3_constbranch.zag | (c) equivalence gaming | `9ece2ad5…2d329` | run1/run2 SHAs differ, 8 bytes, rc 0 | rule 2 (constant branch outcomes) |
| D1 | d1_flood.zag | (d) checker-logic | `32ff7908…6b096` | run1/run2 SHAs differ, 1000000 bytes, rc 0 | checker scale (2M events, ~50MB trace) |
| D2 | d2_nofooter.zag | (d) checker-logic | `bf7b9ecd…cc25bf` | run1/run2 SHAs differ, 8 bytes, rc 0 | checker END-footer handling |
| D3 | d3_sites.zag (generated, 5000 sites) | (d) checker-logic | `45afeb13…a8d1a5a` | run1/run2 SHAs differ, 8 bytes, rc 0 | checker site-id width / map scale |

## Per-plant attack notes (how each defeats the rule)

- **A1**: kernel writes volatile bytes directly into an INIT-HEAP buffer,
  underneath source instrumentation. Region table: INIT-HEAP (clean). Taint
  cells: still (init, untainted). T-READ(INIT-HEAP) + untainted T-OUT.
- **A2**: volatile write inside extern C `wall8` — a call-site name the frozen
  tracer has never seen. No recognizable entropy call site in the Zag source.
- **A3**: volatile byte used as a table INDEX. Taint propagates on
  copy/fill/write only — index-use launders even a perfectly tainted value.
  T-READ of the table is INIT-HEAP.
- **B1**: the volatile read lives in `b1_helper.zag`, imported. If the
  instrumentation map covers the top-level module file only, no events.
- **B2**: volatile value arrives in a REGISTER as `wallret()`'s return. No
  memory read of a volatile region exists in the source — no T-READ site, no
  taint cell, zero branches. Attacks the "read" ontology itself.
- **B3**: raw syscalls for fill AND write; the module never performs a
  Zag-level read of the volatile bytes nor calls a recognized write wrapper.
- **C1**: straight-line, fixed 16-byte output, no data-dependent branches.
  T-OUT lengths identical; content varies. Length-only blindness by design.
- **C2**: fixed-trip-count (16) loop — T-BRANCH outcomes identical across runs
  while volatile bytes flow through the loop body.
- **C3**: branch on `(v-v)==0`, an arithmetic identity over volatile v —
  always taken, outcomes identical, but the taken arm emits raw volatile bytes.
- **D1**: 1M iterations x (T-BRANCH + T-OUT(1)) ≈ 2M events / ~50MB trace,
  past the pinned toolchain's 2^25-byte max indexable slice. Tests checker
  chunking, fixed buffers, truncation behavior, timeouts.
- **D2**: emits 8 volatile bytes then raw `exit(2)` — no END integrity footer
  is ever emitted. Tests fail-open vs fail-closed on a footerless trace.
- **D3**: 5,000 distinct if-sites (past any small fixed site table), all with
  data-independent outcomes. Tests site-id encoding, instrumentation-map scale,
  and event ingestion. NOTE: the past-u16 (65,536+) variant of this attack
  could not be built — the pinned toolchain's compile cost is superlinear in
  branch-site count (5k sites = 62s; 20k > 6 min; 80k never finished in three
  attempts), so M3's "full coverage" claim extends over module scales the
  toolchain cannot compile.

## Adjudication notes for the method crew

1. B1 tests instrumentation-map scope. M3_TRACE_EQUIVALENCE.md §5.2 says gaps
   found later are "method bugs, not red-team wins". The red-team's frozen miss
   definition (checker PASS on a valid dirty plant) counts it as a MISS; the
   method crew may record it as a method bug instead — either way the method
   version does not survive unchanged.
2. D1/D2/D3 are dirty plants (validity proven above) that ALSO stress checker
   logic. A checker crash/hang/timeout is not a PASS — but a truncation or
   fail-open that yields PASS is a MISS under the frozen definition.
3. C1/C2/C3 pass rule 2 BY DESIGN of the length-only T-OUT event. If the
   method's answer is "replay covers content", that concedes M3 alone cannot
   certify the decision path it claims to certify.
4. A2/B2 use C shims for the entropy read ONLY (disclosed above); everything
   else is pure Zag. The method crew's own P07 used the same mechanism.
