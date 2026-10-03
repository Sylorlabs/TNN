# REPORT.md -- COMPOSE-B-TABLE-EXHAUSTION: diagnosis of B's assembly saturation

Date: 2026-10-03. Worker: COMPOSE-B-TABLE-EXHAUSTION.
Lane: `docs/lab/research-lead/overnight-20260928/compose_b_table_exhaustion/`.
Branch: `tnn-native-lab`. Task type: NON-LEDGER (claim minting paused).

## 0. Toolchain / determinism record

- safebin znc verified byte-identical (cmp) to the pinned builder binary
  `$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
  `which python3` / `which python` return nothing under safebin PATH.
- Probe A (unmodified B sources): 3/3 byte-identical stdout (cmp), empty stderr.
- Probe B (1024-table layout variant, CHAIN5+TRAP1): 3/3 byte-identical
  stdout (cmp), empty stderr.
- Frozen sealed-eval sources were copied, never modified. All probe
  modifications live on lane copies under `probe_b/`.

## 1. Verdict

B's table-exhaustion is a **fixable design flaw, not a fundamental limit of
the suspend-then-evaluate idea** -- but it is not fixable by tuning. Three
independent findings:

1. **The 256-entry bound is arbitrary and its "never hit" prediction is
   falsified.** The builder prereg
   (`../compose_suspend_1/PREREG.md`: "MAXT=256 (assembly fails cleanly if
   exceeded; predicted never hit)") chose 256 as a round-number safety cap.
   The builder's own battery never exceeded 2 permutable WALK producers
   (`w_chain3`: 2 WALK + 1 COUNT; `w_fanin`, `w_q1`, `w_q2`: <=4 maps), so
   the prediction was never tested. The sealed battery falsifies it on 11
   of 14 problems.
2. **Enlarging the table to 1024 does NOT fix CHAIN5.** A layout-faithful
   1024-entry variant still returns -999 on CHAIN5 (table only reaches 458
   entries). A *second, independent* truncation -- the 128-entry
   sub-alternative buffer cap in `alts` -- binds behind the table. Two
   independent caps must both be defeated, and defeating both only exposes
   the factorial candidate space underneath.
3. **The factorial enumeration itself is a necessary consequence of B's
   architectural commitments** (phase separation: zero execution during
   ASSEMBLE; kind-coarse symbolic contracts). Given those two commitments,
   no fixed table size, no fixed enumeration order, and no buffer-cap
   setting avoids the blowup in general. Lazy candidate materialization
   would fix the *memory* exhaustion while preserving B's phase separation,
   but the *time* blowup (blind-order evaluation over P(n,<=6) candidates)
   is inherent to the commitments.

## 2. Exact mechanism of exhaustion (frozen 256-table build, CHAIN5)

`assemble` (sus_asm.zag) phase 0 calls `alts`, which enumerates candidates
**strictly bottom-up**: for the goal kind kout=2, the only eligible root
maps are COUNT maps. For the COUNT root it interns, in order: (i) the
direct close `COUNT(C)`; (ii) the *entire* kind-1 sub-closure -- every
simple WALK-chain over the 5 producers up to depth 6; (iii) only then
`COUNT(chain)` for each chain. The root layer is generated strictly after
the full sub-closure, so enumeration order cannot save the root.

For n=5 kind-identical WALK producers the sub-closure alone is
P(5,1)+P(5,2)+P(5,3)+P(5,4)+P(5,5) = 5+20+60+120+120 = **325** distinct
thunks; with the COUNT layer the full closure is 1+325+326 = 652, against
255 available app-thunk slots.

Probe A (unmodified sources, table dump after failed CHAIN5 solve):

- `NTHUNK=256` (table completely full), `ASMSTEPS=255`, `WIDEN=1`,
  `SOLVE_R=-2`.
- Table contents: 1 const thunk + **1 COUNT direct-close** `COUNT(C)` +
  **254 WALK-chain thunks**; **0** non-trivial COUNT roots; 0 ADD2.
- The true W-chain `map4(map3(map2(map1(map0(C)))))` was **never interned**
  (producer-id DFS order enumerates W0/W1/W2-rooted subtrees first; the
  table filled during W2's subtree; the W4-rooted true chain lives in the
  last subtree, never reached).
- Phase-1 candidate list collapses to `[COUNT(C)]` alone (every later
  `app1/app2` returns -2 once the table is full, so nothing is appended):
  consistent with the sealed eval's `EXECTOT=1` on CHAIN5.
- `widen_pass` then fires but cannot allocate either (table full) -> -2.

Fill order observed: `t0=C, t1=COUNT(C), t2=W0(C), t3=W1(C), ...` then
DFS chain unwinding; last entries are W2-rooted chains.

## 3. Why the permutation enumeration exists (necessary given the commitments)

B's ASSEMBLE is specified as "regressive need solving over kind-set
contracts, purely symbolic (zero execution)". Two commitments force the
enumeration:

- **Phase separation** (frozen invariant F-B4, `VIOL` must stay 0): the
  assembler may not execute any MAP, so it cannot probe which WALK actually
  leads anywhere. The facts that would prune dead chains are off-limits.
- **Coarse kind contracts**: every WALK map in the sealed worlds has the
  identical kind signature 1->1. Symbolically they are indistinguishable;
  the need solver's only applicable pruning (kind compatibility, the
  onpath loop guard, the depth<6 bound) is already applied and still leaves
  P(n,<=6) simple chains.

So *some* permutation enumeration is unavoidable under these commitments:
the information needed to prune is not present in the symbolic phase. The
**design flaw** is not the enumeration but its **eager materialization**:
every sub-DAG of every candidate is interned into a fixed table during a
phase that cannot prune, so the table fills with thunks that are not even
candidates (most of the 254 WALK thunks never appear in any candidate
buffer) before the single most-important thunk -- the goal-kind root -- is
built.

## 4. Probe B: 1024-entry table (layout-faithful modified copies)

All table-size-dependent structures relocated consistently (table bound
256->1024; thunk exec, composite store, invalidated list offsets moved;
tid-indexed scratch buffers enlarged; S arena 64 KiB). Probe B5, CHAIN5:

- `SOLVE_R=-2, ANS=-999, NTHUNK=458, ASMSTEPS=454, ATTEMPTS=1446, WIDEN=1`
  (3/3 byte-identical).

The table no longer binds (458 < 1024), yet CHAIN5 still fails. Cause: the
**128-entry sub-alternative buffer cap** in `alts` (`sub`, cap 128) truncates
the depth-1 alternatives to 65 W0-rooted + 63 W1-rooted chains; the true
W4-rooted chain (DFS rank > 260) never becomes a phase-1 candidate (129
candidates total). `widen_pass` cannot bridge the gap: the deeper true
prefixes (W2/W3/W4-rooted chains) were interned but never *evaluated* during
phase 1 (memo stays NOVAL), so they are not "good" thunks and one more
application layer cannot reach the 5-deep true chain (only 3 fresh thunks
are built by widen, all miss).

TRAP1 on the 1024-table (12 permutable WALK producers):

- `SOLVE_R=-2, ANS=-999, NTHUNK=1024, ASMSTEPS=1023, ATTEMPTS=8700420,
  WIDEN=1, EXECTOT=1` (3/3 byte-identical runs, cmp; empty stderr).
- The table still saturates completely: the distinct chain closure alone
  is P(12,1)+...+P(12,6) = 12+132+1320+11880+95040+665280 = **773,664**
  thunks, ~755x the 1024 slots. The factorial blowup defeats any fixed
  table, as predicted.
- `ATTEMPTS=8,700,420` reveals a further inefficiency: the recursion
  regenerates the *same* (map, sub-thunk) pairs many times once per
  disjoint ancestor path, so intern attempts (~8.7M) far exceed even the
  distinct closure (773K). Hash-consing dedups storage but not time; each
  duplicate attempt costs a full O(table) linear scan. (CHAIN5 at 1024
  shows the same ratio: 1446 attempts for 454 distinct app-thunks.)

## 5. Can the exhaustion be avoided?

- **Different fixed enumeration order (e.g. root-first / complete-candidate
  DFS): NO in general.** The root layer is structurally generated after the
  sub-closure, but even reordered, any *fixed blind order* is adversarially
  defeatable: relabeling map ids puts the true chain last (the sealed
  CHAIN5 already does -- the true chain is W4-rooted, enumerated last in
  producer-id order). Order changes *which* 255 candidates survive, never
  *whether* the true one survives.
- **Larger table: moves the cliff, never removes it.** Chain-closure size
  is 2*P(n,<=6)+1: n=4 -> 130 (fits 256); n=5 -> 652 (needs >256, fits
  1024 -- but the 128 sub-buffer cap then binds, see section 4); n=6 ->
  3913 (defeats 1024); n=12 (TRAP1) -> ~1.55M chains, ~3.1M intern attempts
  (defeats any reasonable fixed table). Fan-out/fan-in/DAG worlds blow up
  faster (pairwise products per ADD2 map: FANOUT5 needs >=412). Factorial
  growth defeats every fixed size; the size is arbitrary *and*
  structurally insufficient even for B's stated 6-link capacity (a 6-link
  chain over 6 producers needs 3913 slots).
- **Buffer-cap tuning (128/256): NO.** The caps are load-bearing for
  termination; raising them only exposes the factorial candidate list
  (phase-1 evaluation is linear in candidates).
- **Fact-guided pruning during assembly: would work, but abandons B.**
  Probing intermediate values would collapse the enumeration to the true
  chain, but it violates phase separation (F-B4) -- B's defining
  architectural claim ("purely symbolic (zero execution)"). That is not a
  fix to B; it is a different architecture.
- **Finer learned kinds: unavailable in general.** Kinds are world-given;
  the sealed worlds make all WALKs kind-identical by construction, and no
  symbolic method can distinguish them without touching facts. A learner
  that invents distinguishing value-level contracts from experience would
  be a stronger, different mechanism.
- **Lazy candidate materialization: YES -- the principled fix, preserving
  B's idea.** Phase 0 needs only an *ordered list of candidates*, not all
  their sub-DAGs interned. If `alts` emitted candidates as symbolic
  descriptions (map-id sequences) and phase 1 interned each candidate's DAG
  just-in-time (keeping only winners for the store/revise paths), the
  table would be bounded by the largest single candidate (~8 thunks for a
  6-chain), phase separation would be preserved (zero execution in phase 0;
  same frozen evaluation order in phase 1), and the memory exhaustion
  would disappear at any inventory size. This is an architectural change to
  how ASSEMBLE stores candidates, not a parameter tweak. Note it fixes the
  *memory* blowup only: worst-case phase-1 *time* remains factorial in the
  number of permutable producers, because the evaluation order is blind --
  fixing that requires pruning, i.e. breaking one of the two commitments.

## 6. Answers to the task questions

1. **Why enumerate WALK-chain permutations -- necessary or design flaw?**
   The enumeration is *necessary given* phase separation + coarse kinds
   (section 3); the *eager interning of the full sub-closure into a fixed
   table before the root is built* is the design flaw.
2. **Is 256 fundamental or arbitrary?** Arbitrary: a round-number safety
   cap whose preregistered "predicted never hit" is falsified. But no fixed
   size is sufficient in general (factorial closure growth).
3. **Can the exhaustion be avoided?** By reordering: no. By larger table:
   only moves the n=4/5 cliff to n=5/6 (and the 128 sub-buffer cap binds
   next). By pruning with facts: yes, but abandons B's core invariant. By
   lazy materialization: yes for memory, while preserving B's architecture;
   the factorial time cost remains inherent to blind enumeration.
4. **Fundamental limitation or fixable bug?** **Fixable design flaw with a
   fundamental core**: the crash itself (table saturation) is fixable
   without abandoning suspend-then-evaluate (lazy materialization); the
   factorial candidate space it was papering over is a necessary
   consequence of B's commitments and cannot be fixed by any tuning.

## 7. Recommended follow-ups (for the parent)

- The sealed-eval recommendation stands and is sharpened: B's claimed
  6-link capacity is falsified on any inventory with >=5 permutable
  producers (chain closure 652 > 256 at n=5; 3913 at n=6 even defeats a
  1024 table). The builder battery's "predicted never hit" was validated
  only on <=2-producer inventories.
- If B is continued: preregister a lazy-materialization redesign (section
  5) as the fix candidate, with kill bars on (i) CHAIN5/FANOUT5-class
  inventories solving, (ii) TRAP1-class factorial inventories *failing
  gracefully by time bound rather than memory crash*, and (iii) VIOL=0
  preserved. Do not accept "bigger table" or "different order" as fixes:
  probe B falsifies both.
- The 128 sub-buffer cap deserves its own prereg note: it is a second,
  independent truncation that binds even with unbounded table.

## 8. Files (this lane)

- `probe_a/`: unmodified B-source copies + `probe_main_a.zag` (table dump),
  `probe_a.zag`, `probe_a_bin`, `run{1,2,3}.txt` (3/3 identical).
- `probe_b/`: 1024-table modified copies (layout-faithful; see section 4),
  `probe_main_b.zag` (CHAIN5+TRAP1), `probe_main_b5.zag` (CHAIN5-only),
  `probe_b.zag`, `probe_b_bin`, `run{1,2,3}.txt` (3/3 identical),
  `probe_b5.zag`, `probe_b5_bin`, `b5_run{1,2,3}.txt` (3/3 identical).
- `REPORT.md`: this file.
