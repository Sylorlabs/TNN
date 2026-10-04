# NAMECHECK: L2-COMBINED (multi-adaptation composition)

Worker: L2-Combined Worker (subagent, 2026-10-02).
Branch: tnn-native-lab. Local only, never pushed.

## Step 0: Toolchain guard (mandatory, before any work)

- Ran docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh:
  linked 36 tools, znc OK at src/tools/toolchain/znc_linux_x86_64_abed8aa1.
- export PATH="$HOME/safebin".
- `which python3` -> rc=1 (absent). `which python` -> rc=1 (absent).
- Guard status: PASS. All computation in pure Zag via the pinned znc;
  shell used only for znc invocation, compiled binaries, git, file moves.

## Compiler defect workarounds (from AGENTS.md, honored in all new Zag)

- No `as *i32` + slice construction inside functions; u8-backed cells
  with little-endian ig/is helpers.
- No `_zag_print` for dynamic output; one preallocated buffer with
  cursor-returning emit helpers, single `_zag_raw_syscall(1,1,ptr,len)`,
  stdout bytes verified.
- No reliance on `.len` of `as []f64` / `as []i64` cast slices.
- Sub-conditions hoisted into flag lets; if-nesting <= 3.
- No `!(... && ...)` in while conditions (De Morgan rewrite);
  grep `while.*!(` on all new sources before freezing the verdict.
- Node workspace capacity-planned under 1024 nodes.

## Prior-lane source review (before prereg freeze)

Read REPORT.md of all four cited lanes:
- l2_extend_iterative (C301): EXTEND-ITER semantics reused:
  longest-satisfied native MAP scan, frontier licensing by real facts,
  TERM/NOFRONTIER/EXECFAIL/BUDGET stop codes, type-16 per step,
  adapted MAPs re-extendable (iteration), EXTEND-ONE control.
- l2_substitute (C298): SUBSTITUTE semantics reused:
  m_exec licensing stale-check (STALE_MAP/HOP/FACT), split at dead hop,
  node-id order live-piece endpoint search with distractor rejection,
  assemble + real-execution verify, type-16 promote, stale retire,
  type-15 co-use on episode success, LINK14 answer->delivering MAP,
  SUB_ON/ET_ON driver-set causal-control flags.
- xdomain_l2_adapt (C297): provenance conventions reused:
  exactly-one-line no-adapt build diff, reuse arm with stable adapted
  count, clean-reject arms, 0-new-machinery audit method.
- xdomain_l2_causal (C302): composition + reuse conventions reused:
  contract-triggered adaptation, LINK14 to all segments, type-16 to
  adapter, type-15 co-use on episode success, second-query reuse with
  zero re-adaptation, adapt_on 1->0 one-line control diff.

Combined design: one learner, one query pipeline; SUBSTITUTE fires on
stale detection, EXTEND-ITER fires on span shortfall, the later
operating on the earlier's output MAP. Provenance: type-16
adapted-from chain per step, LINK14 answer->segments, type-15 co-use
on consecutive delivery pairs. 0 new edge types (14/15/16 only),
0 new opcodes, modes, bridges, handlers, semantic cases.
