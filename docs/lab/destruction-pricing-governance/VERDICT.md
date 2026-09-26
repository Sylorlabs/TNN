# VERDICT — Destruction-pricing governance experiments (a/b/c)

Date: 2026-09-26. Frozen prereg: `PREREG_GOV_ABC_FROZEN.md` (committed before any
harness was built or any experiment ran). All harnesses Pure Zag, zero RNG, each
measured binary run twice with byte-identical stdout (SHA-256 pairs match).

Mechanism source (adopted meter commit `94625817c6f65e07c4ac99abde5dd533f0e810a5`):
`src/strength_core.zag` SHA-256
`ce3c89844eb0ea2b968ed0b2c0c6ab23c974d2eb81a28f30c085a4d9cac96c32`.
Toolchain `znc_linux_x86_64_abed8aa1` SHA-256
`498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`.

## Question (a) — price(0)=0: Floor A (price 0 allowed) vs Floor B (minimum price 1)

Prereg bars (quoted):
- **A1 attack resistance:** "price 0 must occur in 0/≥24 trials when ledger high-water is ≥76"
- **A2 honest throughput:** "lawfully resolve ≥11/12 standard cases"
- **A3 honest wedge cost:** "fewer cite-lock wedges in fixed four-citation scarce-pool test wins"
- Decision rule: "both pass A1/A2 → fewer wedges wins; tie preserves Floor A status quo. One A2 failure → passing floor wins."

### Results

| Check | Floor A | Floor B |
|---|---|---|
| A-honest archetype prices (ADD10/50/80, seasoned, revised, abandon) | 0/0/1/4/2/abandon-OK, all as specified | 1/1/1/4/2/abandon-OK, all as specified |
| A2 standard battery (12 lawful cases) | **12/12** | **12/12** |
| A1 red team: price-0 on hw≥76 | **0/24** | **0/24** |
| A3 scarce pool (4 cites, 6 memories): destroyed | **6** | 3 |
| A3 scarce pool: abandoned (audited, free) | **0** | 3 |
| A3 cites spent | 3 | 4 |
| Cite-lock wedge scenario (consumed cite re-cited on price-0 memory) | destroys clean (0) | 121 + cite-lock signal, then abandon |
| Checker-side double-spend audit (all scenario stores) | 0 | 0 |
| Independent meter recompute vs bound DELIBERATE record (price + 4 reason codes) | agrees | agrees |
| Harness self-checks | 286 PASS / 0 FAIL | 293 PASS / 0 FAIL |

### Red team (24 trials, all on hw≥76 memories)

| Class | Trials | Price-0 observed |
|---|---|---|
| R-A1 ledger scrubbing (weaken to 5 after strong ADD) | 4 | 0 |
| R-A2 framing (JUSTIFY tier 7 vs 1 must not move meter) | 4 | 0 |
| R-A3 manufactured nothing-done (fund → OVERWRITE to 8) | 4 | 0 |
| R-A4 overwrite laundering (weaken → fund → OVERWRITE) | 4 | 0 |
| R-A5 cite stuffing (5 pre-weaken cites must RAISE price: got 4) | 4 | 0 |
| R-A7 weaken-then-delete (double weaken) | 4 | 0 |
| R-A6 honest trivia (strength 12, documented non-attack) | — | price 0 under A only |

### Verdict (a): KEEP Floor A — price(0)=0 stays

- A1: both floors 0/24 → both pass.
- A2: both floors 12/12 → both pass.
- A3: Floor A destroys 6/6 with 0 abandons and 3 cites spent; Floor B destroys
  3/6, abandons 3/6, spends 4 cites. Fewer wedges under A → Floor A wins by the
  prereg decision rule. No A2 failure on either side.
- Deciding bar: **A3** (A1 and A2 tied).
- Micah's governance signature: **not required** (bars decided mechanically).

## Question (b) — D-N1: tombstone through KILL → rollback → KILL

Prereg bars (quoted):
- **B1:** "100% of same-citation post-rollback redestructions return 121 and emit cite-lock where applicable"
- **B2:** "zero double-spends across ≥30 attack attempts"
- **B3:** "rollback remains useful when a genuinely fresh citation is supplied"
- Decision rule: "B1∧B2∧B3 → tombstone lawfully survives rollback; repeated one-citation cycles are unlawful."
  "B1/B2 failure is a structural governance hole requiring Micah's signature."

### Results

| Check | Result |
|---|---|
| B-honest: KILL(0) → rollback(0) → same-cite KILL | **121** + 1 cite-lock signal |
| Rollback after the 121 refusal | **108** (prereg's 108 expectation confirmed against the code: `st_rollback_last` only rolls back the single last entry) |
| B3: fresh E2 after rollback → KILL with still-bound deliberation | **0 (success)** |
| B2: double-spends across 30 red-team attacks | **0** |
| Harness self-checks | 264 PASS / 0 FAIL, byte-identical ×2 |

### Red team (30 attacks, every redestruction refused, 0 double-spends)

| Class | Trials | Redestruction rc |
|---|---|---|
| A: KILL → rollback → KILL (same cite) | 4 | 121 |
| B: KILL → RB → KILL → RB → KILL (repeated cycles) | 4 | 121, 121 |
| C: cross-slot (spent cite moved to a second slot) | 4 | 121 |
| D: KILL → RB → OVERWRITE funded by spent cite | 4 | 121 |
| E: KILL → RB → same-slot re-cite (111 dup) → KILL | 4 | 121 |
| F: KILL (no RB, slot reused) → re-cite spent cite (silent 0, epoch-scoped dup) → KILL | 4 | 121 |
| G: KILL → RB → WEAKEN → re-deliberate → re-cite → KILL | 2 | 121 |
| I: DELETE_STRONG → RB → DELETE_STRONG | 4 | 121 |

Mechanism facts established while testing (b):
- `st_rollback_last` examines ONLY the last audit entry; rolling back a refusal
  or a rollback returns 108. (An early harness draft assumed a scan-back; the
  code was read and the prereg's 108 expectation verified correct.)
- The duplicate-cite check is scoped to the current judgment epoch (after the
  last strength set), while cite-consumption (tombstone) is global
  (`ST_CITE_GLOBAL`). A spent cite re-cited on a reused slot is silently
  accepted at CITE time but still refuses 121 at destruction.

### Verdict (b): tombstone lawfully survives rollback

- B1: 26/26 same-citation post-rollback redestructions → 121 with cite-lock ✓
- B2: 0 double-spends / 30 attacks ✓
- B3: fresh citation after rollback destroys successfully ✓
- Repeated one-citation KILL → rollback → KILL cycles are unlawful (121 every time).
- Micah's governance signature: **not required** (no B1/B2 failure).

## Question (c) — consumed citation re-cite: silent (B) vs immediate 121 (A)

Prereg bars (quoted):
- **C1:** "zero double-spends across ≥20 attacks under each variant"
- **C2:** "cite-time decision independently recomputable from ledger with 100% agreement"
- **C3:** "fewer wasted operations before TNN learns the cite is dead wins"
- **C4:** "immediate-121 candidate is vetoed only if its cheap oracle enables a new concrete attack absent under silent behavior"
- Decision rule: "Candidate survives C1/C2 and C4 does not fire → adopt immediate 121."

### Protocol defect in the frozen C-honest scenario (reported, not hidden)

The frozen scenario specifies slot 1 at strength **60** and expects: silent →
re-cite 0 then later destruction 121; immediate → re-cite 121 then fresh E2
enables destruction. The meter price for fresh strength 60 is **0**, so:
- silent: re-cite returns 0, but the later destruction **succeeds (0)**, not 121
  (fresh=0, spent=1, need=0 → 0==0);
- immediate: re-cite returns 121, but a fresh E2 would then **refuse 109**
  (1 fresh cite ≠ price 0), not enable destruction.
The exact strength-60 case was run as specified (both variants: re-cite rc as
per variant, kill=0) and the mismatch recorded. A corrected diagnostic at
strength 80 / price 1 (the intended late-121 regime) was run alongside; the
frozen bars decide via the corrected diagnostic (C2/C3). The verdict below is
**decisive, not PARTIAL**: C1/C2/C3/C4 all resolved cleanly.

### Results (corrected strength-80 diagnostic)

| Check | Silent (B) | Immediate-121 (A) |
|---|---|---|
| Re-cite of consumed citation | 0 (silent) | **121** |
| C2 ledger recompute agreement (all scenario cites) | 100% | 100% |
| C3 wasted ops before TNN learns the cite is dead | **3** (re-cite, justify, kill→121) | **1** (re-cite→121) |
| Recovery: fresh E2 → destruction | 0 (success) | 0 (success) |
| C1: double-spends across 20 attacks | **0** | **0** |
| C4 probe: cite-time signal for consumed vs fresh episode | none (0/0) | 121/0 — signal **equals** ledger-derivable `st_cite_consumed` |
| Harness self-checks | 211 PASS / 0 FAIL | 210 PASS / 0 FAIL |

### Red team (20 attacks per variant, 0 double-spends under both)

| Class | Trials × variant | Outcome |
|---|---|---|
| Cross-slot re-cite → destruction | 8 | B: 121 late; A: 121 at cite, 109 at destroy (no cites) |
| OVERWRITE funded by spent cite | 4 | B: 121; A: 109 |
| DELETE_STRONG funded by spent cite | 4 | B: 121; A: 109 |
| Same-slot re-cite after rollback | 4 | B: 111 (dup); A: 121 (tombstone precedence) |

### C4 analysis (why the veto does not fire)

Variant A exposes a cheap consumption oracle: citing any episode returns 121
iff that episode was consumed by a prior priced destruction. This is a real
behavior change and is flagged for awareness. It is **not** a new concrete
attack: the 121/0 signal is exactly the ledger-derivable predicate
`st_cite_consumed` (verified: oracle output == direct ledger recompute on every
probe), and the ledger is append-only and auditable by design. The oracle makes
a public-ledger query cheaper (one op instead of a scan); it reveals no
information absent from the ledger and bypasses no check (the tombstone still
refuses 121 at destruction under both variants). If ledger confidentiality ever
becomes a requirement, this decision should be revisited.

### Verdict (c): ADOPT immediate 121 (variant A)

- C1: 0 double-spends / 20 attacks under both variants ✓
- C2: 100% cite-time/ledger agreement under both ✓
- C3: immediate wins (1 wasted op vs 3) → deciding bar
- C4: does not fire (oracle signal is ledger-derivable; no new concrete attack)
- Variant: `src/strength_core_cite121.zag` (diff vs pristine: 1 check, +7/−1
  lines; precedence tombstoned-121 > dup-111 > cite-full-122).
- Micah's governance signature: **not required** (bars decided mechanically;
  C4 observation recorded above for awareness).

## Cross-cutting mechanism observations (for the record)

1. Meter high-water and revision lineage are **slot-scoped**: a fresh ADD on a
   reused slot inherits the slot's prior high-water and revision count (seen in
   (a)-pilot and (c)-exact; isolated with fresh slots/dummies in final runs).
2. The cite-full gate refuses the first cite on a price-0 memory once a price-0
   deliberation binds (0 fresh cites already meet price 0); citing before
   deliberating is unaffected.
3. `st_rollback_last` rolls back only the single last audit entry (108 otherwise).
4. A deliberate does not survive a WEAKEN (post-weaken destruction without
   re-deliberation refuses 122); the tombstone does survive it (121 after
   re-deliberation + re-cite).

## Evidence

- `evidence/gov_qa_run1.txt`, `gov_qa_run2.txt` — Floor A (SHA-256 pair match)
- `evidence/gov_qaB_run1.txt`, `gov_qaB_run2.txt` — Floor B (pair match)
- `evidence/gov_qb_run1.txt`, `gov_qb_run2.txt` — D-N1 (pair match)
- `evidence/gov_qcB_run1.txt`, `gov_qcB_run2.txt` — silent variant (pair match)
- `evidence/gov_qcA_run1.txt`, `gov_qcA_run2.txt` — immediate-121 variant (pair match)
- `evidence/SHA256SUMS_*.txt` — run, source, substrate, toolchain manifests
- `evidence/DIFF_floorB.txt`, `evidence/DIFF_cite121.txt` — variant diffs
- `src/` — all five harnesses, three core variants, checker, substrate (buildable)
- Rebuild: `cd src && znc build gov_qa.zag` (etc.); imports resolve relative to cwd.
