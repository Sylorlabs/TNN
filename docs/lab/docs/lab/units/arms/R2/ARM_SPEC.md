# R2 — Compounding-Elimination Cuts | CUT — Arm Specification

**Status:** frozen build for Track A representation bake-off, round r1.
**Source of truth:** `units/arms/briefs/R2.json` (matches the coordinator's
final verbatim frozen row; two earlier coordinator dispatches — the
"automatic revision" mechanism and the first correction's paraphrase — were
voided/superseded and are NOT followed).

## 1. Frozen row (verbatim)

> **R2 — Compounding-elimination cuts | CUT**
> Mechanism: Candidate boundaries proposed cheaply, eliminated by compounding
> evidence; proposals-per-accepted-cut must fall over the corpus (eliminations
> compound).
> Binding kill criterion: Verified-boundary recall (M1) on held-out probes
> does not beat arm R by ≥3 points (receipts don't buy recall at 10× compute);
> OR proposals-per-accepted-cut does not fall over the corpus — core claim
> fails. **R2/Z1 merge decision: A-37 (default: both tested).**

## 2. Architecture

Single pure-Zag binary (`cl/arm.zag` → `r2_bin`); `argv[1]` selects the trial
mode. Zero RNG in all decision paths. All allocation is explicit
(`nio_alloc`/`nio_free`); the audit ledger and allocation trace are
deterministic byte streams.

### 2.1 Segmentation engine (the mechanism)

**Hybrid operationalization (revised 2026-09-21; supersedes the 64B-block
version below).**

1. Cut candidates are proposed at every 64-byte boundary (cheap: zero table
   lookup to propose — the cheapest possible).
2. Verification context: the 8 bytes around the boundary (4B left + 4B
   right), hashed with 31-bit FNV-1a into a 2^17-bucket open-addressed
   running-count table.
3. **Online left-to-right scan:** at each 64B boundary, the 8B pair's running
   count is checked. Count ≥1 (seen before) → *ACCEPT* (verified cut; the
   pair now co-occurs ≥2, which implies the left and right 4B spans each
   recur ≥2 — satisfying all three alphabet conditions with one check).
   Count = 0 → *ELIMINATE* (rejected for lack of compounding evidence).
   The count is then incremented.
4. **Evidence compounds:** running counts grow monotonically as the scan
   proceeds, so more boundary contexts become "recurrent" later in the
   corpus → accepts rise relative to (constant) proposals →
   proposals-per-accepted-cut falls.
5. Verified cuts delimit chunks. Chunks longer than 8,192 bytes are
   force-split (engineering cap, not a verified cut).
6. Evidence: `TAG,R2_SEG,<proposals>,<accepts>,<kills>,0,<chunks>` and
   per-decile `TAG,R2_CURVE,<p0>,<a0>,…,<p9>,<a9>` pairs; per-decile
   aggregates are audited (op=41). Per-proposal/per-elimination ledger
   entries are NOT written: they would be ~30 entries/KB, breaking M5's
   ≤10 entries/KB bar (documented deviation from the alphabet §4 build
   note; the full record is in TAG,R2_CURVE).

**Why the revision.** The original 64B-block-recurrence operationalization
(candidate = both adjacent 64B fingerprints recur ≥2; accepted = the
ordered 64B pair recurs adjacently ≥2; elimination prunes 3 forward blocks)
was degenerate on real corpora: measured 0 proposals, 0 accepts on
5.4MB prose (1 recurrent 64B block in 84,730; 0 recurrent adjacent pairs).
Natural text does not contain recurrent 64B blocks, so the mechanism could
not operate and "proposals-per-accepted-cut falls" was untestable (0/0).
The alphabet spec (ALPHABET_M-R.md §R2) does not fix a span size; the
revision moves the recurrence check to 4B contexts, where recurrence is
abundant in text, while keeping 64B cut positions so chunks stay at sane
sizes. The mechanism (cheap proposals, elimination by compounding evidence,
falling ratio) is unchanged; only the evidence granularity moved.

**Operationalization note (disclosed, not preregistered):** the frozen row
does not fix exact cut statistics. "Falls" is operationalized as
late-3-decile proposals-per-accept < early-3-decile proposals-per-accept,
computed from the raw per-decile pairs (preserved in evidence). This
operationalization was chosen during the build, AFTER smoke-test curve
evidence had already been observed for the 64B version — it is a disclosed
arm-build interpretation, not a pre-results preregistration. The raw decile
pairs are reported so the claim can be checked under any aggregation.

### 2.2 Store

Slot-addressed unit store: persistent unit IDs, ID→slot and slot→ID maps,
span→slot dedup map `(corpus, offset, length)`, per-slot offset/length/
corpus/shift/patch-index, FIFO insertion queue with oldest-unpinned
eviction, and a 64-byte-entry append-only audit ledger (stage byte 52,
d1 byte 56, d2 byte 60). Same-span re-ingest with identical bytes reuses the
ID (dedup); same span with different bytes mints a declared, audited
new-version ID linked to the old (supersede). Recall is byte-exact
re-reading of the registered corpus buffer at the unit's span (plus any
recorded shift/patch, which the M4 defects install and the revise path
clears after source verification).

### 2.3 Deliberate operations

- `kill` (audited, reason-coded), `pin`/`unpin` (trainer), `weaken`
  (audited no-op acknowledgement — strength is set by judgment, never by
  formula; the weaken *request* is honored as audited evidence),
- `defect_boundary` / `defect_content` (external trainer ops),
- `revise` (deliberate repair: re-verify against source, drop shift/patch),
- `mark_valuable` (pin + audit tag).

## 3. Metric operationalizations

| Metric | Operationalization |
|---|---|
| M1 | Segment → ingest → full recall of every chunk; boundary score = fraction of verified cuts whose span edges reproduce. ID arm: A15 provisional swap probe (PROVISIONAL-PENDING-FREEZE). |
| M2 | Episode-0 empty probe, then repeated ingest+probe until recall ≥99.5% and boundary ≥95% for 3 consecutive episodes (≤50). M9 shape from the recall curve. |
| M3 | 1000 valuable marks spread over chunks; 3000 fresh 64B ingests; 3000 fresh-only kills; 50 weaken ops spread over valuables; 4000 ingests at capacity with oldest-unpinned eviction. Freeze detector: survival ≥90% with fresh recall <80%, or <700 mgmt entries, or weaken mishandled. |
| M4 | 100 boundary defects (±1..±32 cycle) + 100 content defects (prose: every-7th-byte XOR; code: identifier renames); ≤20 revise episodes; kill-substitution tripwire. |
| M5 | Literal: memory = RSS delta (run − empty-store baseline) + slot-table bytes; audit = ledger entries per KB. Baseline allocates the identical empty store; segmentation tables count toward the arm's delta. |
| M6 | Train tier-1 to M2 criterion, in-domain revision, then transfer to the new domain with policy frozen. Memorizer control via shared memorizer binary; validity gate = memorizer drop ≥15 pts. |
| M7 | ID arm (not N/A): ingest C, ingest C again, ingest C′ (deterministic every-100th-unit first-byte XOR), 5000 lookups on the `(l*37)%nunits` schedule split 1666/1667/1667. Bars: hit ≥90%, reuse ≥1.5, dedup ≥0.4. C′ edit + schedule are PROVISIONAL-PENDING-FREEZE. |
| M8 | N=5 adversarial perturbations (clean/frag/aslr/starve/freelist) × 2 reruns; byte-identical `store_hashes.txt`, `store_chain.txt`, `ledger.bin`, `ledger_chain.txt`, `alloc_trace.txt`. Freelist-reversal is a documented no-op (slot placement is a pure function of unit ID). |

## 4. Kill evaluation

Both disjuncts are evaluated literally after the 1× battery:
1. M1 verified-boundary recall on held-out probes vs arm R's authoritative
   baseline — R2 must beat R by ≥3 points.
2. proposals-per-accepted-cut (late vs early deciles) must fall over the
   corpus — else the core claim fails.

## 5. Ambiguities and provisional cells (all logged, none silently reinterpreted)

- A7/A8 (M7 C′ edit = first-byte XOR 0xFF; lookup schedule `(l*37)%nunits`
  1666/1667/1667): **PROVISIONAL-PENDING-FREEZE**.
- A15 (M1 ID-swap probe): provisional swap-probe procedure; implemented
  literally, results labeled.
- Cut statistics (proposal/accept thresholds, prune width, fall
  calculation): arm-build operationalization of the frozen row, fixed
  pre-results, disclosed in §2.1.
- Fingerprint collisions: FNV-1a 32-bit without byte-exact collision
  resolution; collision probability is negligible for the corpus sizes and
  the mechanism's claims do not depend on zero collisions.
- M5 baseline: raw file bytes only; segmentation tables counted in the
  arm's delta (literal reading of the rule).
