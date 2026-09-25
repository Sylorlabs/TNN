# BUILD_NFEE.md — Negation-First Elimination Engine (round-2 engine e)

Built 2026-09-25. Pure Zag, zero RNG, deterministic. Pinned toolchain:
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

## 1. Architecture (frozen spec: SPEC_NFEE.md)

Negation is the primary engine. Two strictly sequential phases, never interleaved:

- **Phase 1 — elimination pass** (`nfee_elim.zag`, `nfee_phase1`): contrapositive
  firing backward from NOT-H. A deterministic worklist is seeded with `not(H)`.
  For each worklist item `N = not(X)`:
  - **DIRECT**: a grounded rule concluding `N` with all antecedents established
    yields a singleton elimination constraint `{X}` attributed to that rule,
    and `N` is asserted into the claim store immediately (audit
    `PHASE1_DIRECT <rule>`). This is the spec §5 case: false rule
    "if TRUE then NOT-H" fires in Phase 1.
  - **CONTRA**: a grounded rule concluding `X` yields a disjunctive constraint
    over its antecedent conjuncts ("at least one is false": if `X` is out,
    some antecedent must be), attributed to that rule; each `not(A_i)` joins
    the worklist (depth bound).
  - Activation (end of Phase 1): DIRECT constraints are always active; CONTRA
    constraints are active iff their head negation was established in Phase 1.
- **Phase 2 — filtered forward pass** (`nfee_fwd.zag`, `nfee_bfs`): standard
  forward chaining (S_MP / S_UI / S_PBC-direct, same committed schemas as
  round 1) with the elimination filter. Before asserting any candidate `C`,
  `nfee_violation` scans ELIM_ARENA in order: `C` is blocked iff it is a
  disjunct of an active constraint whose *other* disjuncts are all established
  (for singleton constraints this reduces to the spec's simple membership
  check). Blocked candidates are recorded in BLK (claim bytes + blocking
  constraint index + that constraint's rule attribution) and never asserted.
  Eliminated premises/store claims are skipped both as rule sources and as
  antecedent matches ("a forward derivation is valid only if none of its
  premises have been eliminated").
- **Verdicts** (`nfee.zag`): `WITHHELD` (false derived — contradictory store)
  > `DERIVED` (H asserted and surviving elimination) > `CONTESTED` (H blocked
  by active constraints, or an asserted H is itself eliminated — attribution
  names the responsible rules) > `REFUTED` (not(H) asserted — attribution
  names the DIRECT rules that established it) > `UNSUPPORTED`.

The top-level ATTRIBUTION line is NFEE's unique measurable: for CONTESTED it
lists every active constraint H violates (`DIRECT <rule> | CONTRA <rule> …`);
for REFUTED it lists the DIRECT constraints that established not(H).

## 2. Arena layouts (all []u8, ZNC-2026-09-21-007 workaround)

- `ELIM`: 10 i32 fields per constraint
  (f0 type 1=DIRECT/0=CONTRA, f1 disjunct count, f2 disjunct-table offset,
  f3/f4 attribution off/len, f5/f6 head off/len, f7 active flag, f8/f9 dedup-key
  off/len); disjunct table = (off,len) pairs; byte-data arena. Disjuncts are
  claim *bytes* (spec's u8 claim_idx generalized: Phase-1 constraints reference
  claims not yet numbered).
- `GRUL`: grounded rules — (consequent off/len, antecedent-table range,
  source-attribution off/len) + antecedent (off,len) table + byte arena.
  Built from direct `imp(...)` claims plus deterministic universal
  instantiations of `forall(..., imp(...))`; top-level `and(...)` consequents
  split into disjunctive antecedent entries.
- `WL`: deterministic worklist / established-negation set (offset/len/depth).
- `NSTAT` (STATUS_ARENA): parallel to claim indices,
  `[eliminated:u8][eliminated_by:u16]`; `nfee_mark` covers loaded claims that
  are disjuncts of active constraints with all other disjuncts established.
- `BLK`: blocked candidates — (claim off/len, blocking constraint idx,
  attribution off/len) + byte arena; dedup by claim bytes.
- Each forward claim's audit carries `ELIMCHK <n>` = number of active
  constraints checked before assertion (spec's `elim_check_index:u16`).

## 3. Determinism

Committed rule order and claim-address order throughout; worklist FIFO;
constraint/attribution scans in index order; append-only arenas; no deallocation
in the hot path; zero RNG (grep-clean). 3× in-process reruns per invocation,
byte-identity asserted (exit 5 on divergence); plus 3× external runs compared
by SHA-256.

## 4. Toolchain workarounds (exact)

- ZNC-2026-09-21-007: no `as []i32`/`as []u32`/`as []u16` anywhere; all tables
  are `[]u8` arenas with `au_get32`/`au_put32` little-endian accessors.
- All slices kept far below the 2^25 indexing ceiling (largest: 2MB claim
  data arena, 1MB buffers).
- `_zag_strcmp` returns 1 on equality → all comparisons via `nio_equal`.
- `_zag_argc()` is unreliable in this znc build (ZNC-2026-09-21-007 notes);
  the optional `[bound]` argument is read unconditionally via `_zag_arg(3)`
  and validated (`1..128`), `""` → default 8. `argc` is still consulted for
  the usage message only.
- Imports resolve relative to the importing file; build with CWD = the nfee
  dir. Runtime STORE paths resolve against the runtime CWD, with fallback to
  the problem file's directory.
- Shared modules live in `math_logic/engines/common/` and are imported via
  relative paths (`../../../engines/common/cx_*.zag`); schema hashes asserted
  at startup (`cx_sch_assert`, exit 6 on mismatch).
- Build flags: `--no-zagd --no-analyze --no-foreground-cache` (BUILD_ONE.md).

## 5. Build / run

```
cd ~/workspace/tnn-lab/math_logic/round2/engines/nfee
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 nfee.zag \
  --no-zagd --no-analyze --no-foreground-cache -o nfee_bin
./nfee_bin <problem.form> <out_path> [bound]   # bound default 8, max 128
```

Exit codes: 0 ok · 3 sealed-guard trip (refuses `problems/sealed/`,
`batteries/sealed/`, `sealed_battery`) · 4 input/alloc · 5 3× divergence ·
6 committed-schema hash mismatch.

## 6. Standup results (2026-09-25, final binary)

- **B2 smoke** (12 problems, KB_SMOKE.md): 11 DERIVED, 1 UNSUPPORTED (B2_07 —
  target genuinely underivable: chain stalls at `r`, no rule yields `s`;
  matches ONE's WITHHELD). 0 incorrect positives.
- **Sealed guard**: `problems/sealed/SOLUTIONS.md` → exit 3. ✓
- **Determinism**: 3× in-process reruns byte-identical on every run (exit 5
  never hit); 3× external runs of B2_08 and NF_T1 → identical SHA-256
  (`43ae6b35…`, `24a3180c…`). ✓
- **Zero RNG**: grep for rand/random/srand/shuffle//dev/urandom/getrandom
  over `*.zag` → no matches. ✓
- **Schema pins**: `S_MP=62cc41ffd582e687 S_PBC=369efe53016bbe1a
  S_UI=b2f909c7d7b67f55` — match committed round-1 values. ✓

### Two-false-rule injection battery (temporary fixtures, NOT sealed B5X)

Store KB_NF: 5-rule legit chain `a1→b1→c1→d1→e1→h1` (N101–N105), side chain
`a1→f1→g1` (N106–N107), two single-hop false rules `NF1: imp(z1,not(h1))`,
`NF2: imp(z2,not(h1))`, plus multi-hop `NF3/NF4: z1→mid9→not(h1)`.

| Test | Premises → Target | Verdict | Attribution | Correct? |
|------|-------------------|---------|-------------|----------|
| NF_T1 | a1,z1,z2 → h1 | REFUTED | `DIRECT PREM NF1 \| DIRECT PREM NF2` | ✓ 0 incorrect positives; both false rules named |
| NF_T2 | a1 → h1 | DERIVED | — | ✓ legit chain intact when false rules can't fire |
| NF_T3 | z1,z2 → h1 | REFUTED | `DIRECT PREM NF1 \| DIRECT PREM NF2` | ✓ |
| NF_T4 | a1,z1,z2 → g1 | WITHHELD | — | ✓ store genuinely contradictory (h1∧¬h1); g1 not falsely affirmed |
| NF_T5 | a1,z1 → h1 | REFUTED | `DIRECT PREM NF1` | ✓ single-hop dominates |
| NF_T6 | a1,z1 → h1 (multi-hop store only) | WITHHELD | — | ✓ no incorrect positive; caught by contradiction rule (limitation L1) |
| NF_T7 | p1,z1 → h1 (1-step legit) | REFUTED | `DIRECT PREM NF1` | ✓ |
| NF_T9 | p1,z1 → h1 (2-step legit) | REFUTED | `DIRECT PREM NF9` | ✓ |
| NF_T10 | p1,z1 → h1 (false rule targets x1) | CONTESTED | `CONTRA PREM N914` | ✓ CONTESTED reachable; blocker named honestly |

Kill bars (spec §7): incorrect positives = 0 (bar: >3). Max constraints on any
battery problem: 7 (bar: >20). ✓

### Bugs found during standup (fixed, verified)

1. Phase-1 DIRECT establishments were recorded in the worklist set but never
   asserted into the claim store → verdicts collapsed to UNSUPPORTED and the
   contradiction rule couldn't see them. Fix: raw `cxs_add` of `N` with audit
   `PHASE1_DIRECT <rule>` at establishment time (bypasses the filter — the
   just-created constraint must not filter its own establishing claim).
2. Phase-2 re-derivation of a Phase-1-established negation was recorded as a
   spurious BLOCKED entry. Fix: presence check before the filter in
   `nfee_maybe_add`.
3. Verdict precedence: an asserted-but-eliminated H (e.g. premise H covered by
   an active constraint) was reported DERIVED. Fix: elimination check before
   the DERIVED branch, per spec ("H derivable but eliminated → contested").

### Documented limitations

- **L1 — multi-hop false rules**: a false rule whose antecedent is not
  established in Phase 1 (e.g. `mid9` in NF_T6) is not DIRECT-fired; it is
  caught only if/when its conclusion collides in Phase 2 (contradiction →
  WITHHELD) without rule-level attribution. Phase 1 does not forward-chain.
- **L2 — worklist-gated CONTRA activation**: CONTRA constraints activate only
  on Phase-1-established head negations; contrapositive propagation does not
  continue through intermediate negations established only in Phase 2.
- **L3 — negation-first starvation (by design)**: once not(H) is
  DIRECT-established, every forward path to H is cut below H (singleton
  antecedents blocked as candidates; multi-antecedent rules lose their last
  antecedent), so H is never attempted — REFUTED rather than CONTESTED. This
  is the architecture working as specified, not a completeness bug.

## 7. Falsifiable predictions (spec §7) — status

- "0 incorrect positives + attribution naming the false rules where ONE
  withholds 60/60 with 0 attributions": **holds** on the self-authored battery
  (0 incorrect positives; `DIRECT PREM NF1/NF2` attributions). KB5-scale
  comparison vs ONE/DUAL is round-3 battery work, not claimed here.
- "≤5 elimination constraints that specifically block H": holds (max 3
  H-blocking constraints observed: 2 DIRECT + 1 CONTRA).
- "Largest gap vs ONE on shared-antecedent stores": untested — battery work.
