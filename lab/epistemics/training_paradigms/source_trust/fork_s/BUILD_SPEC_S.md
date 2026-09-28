# Fork S — Build Spec (FROZEN)

**Date:** 2026-09-23. **Status:** FROZEN — no post-hoc tuning; committed before battery streams are seen.
**Position:** trust as **structure**, not a number. No per-source scalar exists anywhere in the decision path.

## 1. Graph schema

**Claim nodes** `(key,val)`: asserter *set* (repetition adds nothing), per-asserter last-assert episode,
world status (agreed/disagreed + episode), first asserter.

**Source nodes**: `first_seen` episode, tagged **event log** (append-only):
`VIND` (claim later world-agreed, or claim stated = current world value),
`WERR` (honest error: world-disagree classified error-not-lie),
`PROV` (world-disagree awaiting the source's next move on that key),
`LIE` (caught lie: persist-after-disagree, or assert-against-known-world-record).
Tag status: open / repaired / superseded. No numeric accumulators per source.

**World timeline**: authoritative per-key `(ep → val)` log. **Edges**: co-assertion (kind 1)
and contradiction (kind 2) pairs between sources.

## 2. Decision procedure — ordered pattern match, first rule fires (verdict + structural warrant)

- **R1** claim contradicts current world record for key → **REJECT**. Tag: `WERR` if the source's
  identical claim was ever world-agreed (true-when-stated = world-change lag, ST-4); else `LIE`.
  (A later world-move to the rejected value retro-exonerates the `LIE` → `VIND`.)
- **R1b** claim equals current world record → **INSTALL** (+`VIND`).
- **R2** claim's *first asserter* has unresolved `LIE` → **WITHHOLD** (origin taint; repetition
  by a clean source does not launder — RT-T3).
- **R3** ≥2 **independent** corroboration credits → **INSTALL** — even if the originator has an
  unresolved `LIE` (trust≠truth, ST-6). Credit: asserter with independent history
  (≥1 `VIND`/`WERR`, or a contradiction partner outside the asserter set) and no unresolved `LIE`;
  a *closed* co-assertion component (members' only history is mutual agreement, size ≥2 —
  the Sybil shape) contributes at most 1 total. `CORROB_QUORUM = 2` (frozen).
- **R4** source has unresolved `LIE` → **REJECT** (uncorroborated claims from a convicted source).
- **R5** source has open `PROV` → **WITHHOLD** (unresolved dispute with the world).
- **R6** live contradiction (competing claim with a non-`LIE` asserter, no world resolution)
  → **WITHHOLD** (both sides; ST-2).
- **R7** ≥2 asserters, 0 credits → **WITHHOLD** (manufactured-consensus shape; RT-T2).
- **R8** default → **INSTALL** (uncontested novel claim, clean record — cold-start admission;
  honest controls must install).

**World-disagree classification** (the ST-4/H4 load-bearer): first-time disagree on a claim the
source asserted → `PROV`. Source's next move on that key decides: states the world value →
honest update → `PROV`→`WERR`, record clean; restates the disagreed value → `LIE`.
**Repair** (ST-5): an unresolved `LIE`/open `PROV` is marked repaired after
`REPAIR_QUORUM = 3` `VIND`s dated after it with no intervening open `LIE`/`PROV`
(newest-first cascade). A fork that can never re-earn is penalized — S re-earns structurally.

## 3. No-scalar-collapse argument

(a) No per-source numeric field is read by `decide` — only pattern queries over the tagged
log ("exists unresolved `LIE`?"), per-*claim* credit counts, and world-timeline lookups.
(b) **Split-verdict**: the same source gets `INSTALL` (corroborated truth, R3) and `REJECT`
(solo novel claim, R4) in the same stream — one number cannot produce both; the battery
crew is invited to test exactly this. (c) Source-symmetric init (empty record; no per-source
constants — the only frozen numbers are the structural quorums 2 and 3, declared above).
(d) The §6.3 ordering is metric-only: lexicographic on
(open-tag? , has-vindication? , #VIND desc, #WERR desc, src_id) — never called in `decide`.

## 4. Interface contract (driver requirement)

```zag
struct ForkHist { arena:[]u8, wbuf:[]u8, wpos:i32 }
fn s_init() ForkHist
fn s_note(ep:i32, etype:i32, src:i32, key:i32, val:i32, h:*ForkHist) void  // EVERY episode in stream order
fn s_decide(src:i32, key:i32, val:i32, h:*ForkHist) i32                    // 0/1/2 on SAY (after s_note)
fn s_warrant(h:*ForkHist) []u8                                            // warrant for the last verdict
```
`decide` is pure wrt everything outside `ForkHist`: no RNG, no clock, no file I/O
(grep-verified). Per-`decide` cost is linear scans over small tables.

## 5. Honest expectations / limits

Cold start is information-free: the first unseen claim from an unseen source INSTALLs (R8),
so RT-T2's first ring episode installs; the Sybil shape fires on the 2nd co-asserting
history-less identity → expected ≤1 install (kill-safe at <3; the 0 bar needs an oracle).
A betrayal lie contradicting the established world record REJECTs immediately (R1) —
a 500-episode clean history does not immunize, because verdicts read the claim's
record position, not the source's aggregate. Lies on entirely fresh keys are
indistinguishable from honest novel claims at decision time for any non-oracle fork;
S's differentiator is clampdown after evidence (0 subsequent installs once `PROV`/`LIE`
lands) and immunity to manufactured corroboration (forged second origins contribute
0 credits — the RT-C fix).
