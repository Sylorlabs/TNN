# Track B Naive Learner — Operationalization (Crew 2)

**Prereg:** `~/workspace/tnn-lab/units/PREREG_FREEZE.md`, frozen 2026-09-21.
Binding: §0 T-items, §4 B.4/B.5/B.7/B.8, §5, §14; §P (proposal wire),
§L (deliberation protocol), §C (tripwire).
Do not alter frozen bars, metrics, protocol, or kill criteria.

Pure Zag. Zero RNG in any path. No wallclock anywhere (logical tape ticks
only). Deterministic and byte-identical: N=5 reruns verified
(tests/test_determinism.zag → `DETERMINISM PASS: 5/5 byte-identical`).

## File map

| File | Role |
|---|---|
| `pcodec.zag` | §P wire codec: encode/decode/validate, FNV-1a-64 checksum (isolated for later integration swap), grounding signature. |
| `store.zag` | Hypothesis store (HypStore), force-pin registry (Pins), 16-word chained audit ledger (Ledger). |
| `delib.zag` | §L deliberation core: GENERATE → ELIMINATE → WEIGH → DECIDE, appeals, retract, DEFER queue, tripwire, promotion scan. |
| `driver.zag` | Harness-compatible driver: §P wire → dlb_consider → DELIB (5) + DECISION (6) tape records (harness EV codes, unified 2026-09-21). Library (no main). |
| `R33_NATIVE_IO_V1.zag`, `R33_NATIVE_SHA256_V2.zag` | Linux substrate copies (lab convention). |
| `tests/test_driver.zag` | Driver + tape framing smoke test (ADOPT/REJECT, DELIB/DECISION byte layout). |
| `tests/test_determinism.zag` | N=5 byte-identical rerun test. |
| `tests/test_pins.zag` | Force-pin blocking (exact + overlap blocked, clear span adopts). |
| `tests/test_retract.zag` | RETRACT kill, double-retract refuse, unknown-seq refuse. |

## §L deliberation pipeline (delib.zag)

Per proposal, `dlb_consider` runs four stages, each opening a step record
(`dlb_step_begin`) with a pre-step state digest (`dlb_digest`):

1. **GENERATE** — decode the §P wire (iron-rule validation via pcodec);
   resolve the target hypothesis (existing or new).
2. **ELIMINATE** — independent corroboration: each ground span is checked
   against the stimulus (occurrence count, boundary alignment). Elimination
   codes R1–R6 fire in fixed order:
   - R1: zero occurrences (fabricated span)
   - R2: pin conflict (force-pin overlap) or contradictory grounding
   - R3: shiftable boundary (a better-placed occurrence exists → REVISE)
   - R4: contradictory evidence across grounds
   - R5: boundary/precision failure (shift-search cannot rescue)
   - R6: below the adoption bar after all eliminations fail
3. **WEIGH** — `score = occ + 2*valid - 3*contra` against the adoption bar
   (`cfg_prov`). SAME_AS never adopts directly (folds into a group-span
   REVISE); GROUP adopts only if every aux member occurs.
4. **DECIDE** — `dlb_apply` writes the verdict (ADOPT/REVISE/REJECT/DEFER),
   appends the audit ledger entry, updates the hypothesis store, and fills
   the `dec_*` fields the driver turns into the DECISION tape record.

**DEFER ≤ 3 turns:** deferred proposals are queued (`dlb_queue_defer`);
each re-presentation increments the hypothesis's defer counter; at 3 defers
the next consideration converts DEFER into REJECT/R5 (flood termination).
**Appeals ≤ 2:** `dlb_appeal_find` locates the rejected hypothesis by its
last reject seq; `appeals[hyp]` caps at 2; a third appeal is refused.
**Guaranteed termination:** every path through `dlb_consider` ends in
`dlb_apply` (exactly one verdict); the DEFER queue is bounded (DEFQ_CAP);
no unbounded loops (all scans are over fixed-cap arrays).

## Schematic choices (load-bearing)

1. **Eliminative, not additive.** The learner never accumulates positive
   evidence toward adoption; it tries to kill the proposal (R1–R6) and
   adopts only what survives. Rationale: §L requires eliminative testing;
   a scoring-then-threshold design would let weak proposals through on
   volume. Tested: fabricated spans (R1), pin conflicts (R2) die in
   ELIMINATE before WEIGH ever sees them.
2. **Score = occ + 2·valid − 3·contra.** Occurrence count is weak evidence
   (+1); independently corroborated grounds are strong (+2 each);
   contradictions are heavily penalized (−3 each). The 3× contra weight is
   the load-bearing leg: a single contradiction outweighs two corroborations
   (tested both 2× and 3×; 2× let a 2-valid/1-contra proposal adopt —
   wrong, since one contradiction should veto).
3. **Boundary bonus is multiplicative in shift-search, additive nowhere
   else.** `shift_search` scores candidates as `occ + bnd·1_000_000`: any
   boundary-aligned candidate dominates any unaligned one, and among aligned
   candidates the higher occurrence count wins. Tested both pure-occ and
   bonus forms; pure-occ shifted "the cat" onto a word-internal repeat.
4. **SAME_AS folds, never adopts.** A SAME_AS proposal becomes a REVISE that
   unions the target span with aux member 0. Rationale: identity claims are
   about the group, not the span; adopting the span would double-count.
5. **RETRACT is a verdict, not a deletion.** `dlb_retract` marks the
   hypothesis HS_KILLED, appends an AUD_RETRACT ledger entry, and returns
   V_ADOPT/R_RETRACT_OK (the retract itself succeeded) or
   V_REJECT/R_RETRACT_REFUSED (target dead or unknown). The killed record
   stays in the store as an audit tombstone.
6. **Pins are checked in ELIMINATE, before WEIGH.** A force-pin overlap
   kills the proposal (R_R2) regardless of score. This is the law from
   MEMORY.md: the only true lock is a human/trainer force-pin — it must be
   absolute, not weighed against evidence.
7. **Tripwire (§C) is a rolling 200-proposal window** over
   (coverage, accept-rate, max-confidence); confidence-255 covering >5%
   fires immediately. Implemented in `tw_note`; fires halt via the driver's
   `-2` path (tape full / halted).
8. **State digest is FNV-1a-32 over the full mutable state** (hypotheses,
   pins, ledger chain, counters, tripwire sums). Pre-step digests go into
   DELIB records; the post-decision digest goes into DECISION. Byte-identical
   reruns prove the digest is a pure function of state.

## Bracket legs (tested both, per Micah's standing rule)

- **Contra weight 2× vs 3×:** 3× wins (see choice 2). 2× adopted a
  2-valid/1-contra proposal; 3× correctly rejected it.
- **Shift-search scoring pure-occ vs occ+bnd·1e6:** bonus form wins
  (see choice 3). Pure-occ picked word-internal repeats.
- **DEFER→REJECT threshold 2 vs 3 turns:** 3 wins. At 2, a proposal deferred
  twice on a transient pin (later released) never got its fair third look;
  §L allows ≤3, so 3 is the max-fairness setting.
- **Appeal cap 1 vs 2:** 2 wins (§L allows ≤2; 1 denied a legitimate
  second appeal after new grounding arrived).

## znc codegen hazards encountered (all worked around, see AGENTS.md)

- **ZNC-2026-09-21-003:** slice-typed struct fields (`[]u8`, `[]i64`) are
  **16 bytes** (ptr+len), not 8. `_zag_malloc` must be sized as
  16×(slice fields) + 8×(scalar/pointer fields). Undersizing DLB (512 for
  600 bytes) caused heap corruption manifesting as a segfault in
  `dlb_digest` — diagnosed by raw-word dumps showing field-shift.
  Fixed: DLB→1024, HypStore→384.
- Bare `return` in a `void` fn fails to parse; use `return;`.
- Missing struct field → misleading "aggregate let needs an aggregate
  initializer" error (was a missing `rej_seq` init).
- Direct indexed write `se[d[0].st_pool]` on large-struct array fields is
  unreliable; alias to a local first.

## Test results (2026-09-21)

| Test | Result |
|---|---|
| test_driver (ADOPT good span, REJECT bad span, tape framing) | PASS — verdicts 1/3, DELIB type=4, 9 records, 570 bytes |
| test_determinism (N=5 byte-identical) | PASS — 5/5 identical, 827 bytes each |
| test_pins (exact+overlap blocked, clear adopts) | PASS — pinned→REJECT/R2, clear→ADOPT |
| test_retract (kill, double-refuse, unknown-refuse) | PASS — 1/3/3, reasons 7/8/8 |

## Open gaps (not yet tested)

- Full appeal flow (2 appeals then refuse) — mechanism implemented,
  end-to-end test pending.
- DEFER queue flood termination (3 defers → REJECT/R5) — mechanism
  implemented, test pending.
- §C tripwire firing on a 200-proposal window — mechanism implemented,
  window test pending.
- Four §B.7 flaw classes (wrong-span, false-confidence, missing-grounding,
  plausible-false) as adversarial probes — the ELIMINATE codes address each,
  but dedicated probe tests are pending.
- Promotion scan (`dlb_promote_scan`) — implemented, test pending.
