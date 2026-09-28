# Deliberation v1 — Architecture

**Implementation:** `deliberate.zag` (frozen: `build/deliberate_frozen_r4.zag`)  
**SHA-256:** `7dec26d8600683f2c6cefc83d524a403f4ac288117864108dc54a08afa61b787`  
**Date:** 2026-09-27 (repair cycle #4)

Supersedes the 2026-09-27 frozen source `build/deliberate_frozen.zag`
(`d433bd06…`, retained for provenance — voided by red team 3, finding R2:
kind-0 reading rows were decorative). This repair wires the reading rows into
action generation (see "Reading-Row Causal Wiring" below).

## Overview

Deliberation v1 replaces the round-4 cascade with genuine deliberation machinery.
The decision lives in a ledger; the trace is the ledger rendered during deliberation.

## Ledger Layout

- **25 rows** × 552 bytes: 10 reading hypotheses (hid 0-9), 3 fact candidates
  (hid 10-12), 12 action bids (hid 13-24).
- **Turn fields** at 13804-13820: close-call flag, fact-winner, etc.

## Phase Ordering (G2 Compliant)

1. **GEN:** All candidates generated — readings (0-9), facts (10-12), actions (13-24).
   - Per-GEN idempotence flags ensure exactly-once execution (K1 safety).
   - Readings (0-9) run FIRST: they are the sole utterance classifier, and the
     action GENs read their rows (repair #4). Facts (10-12) run after readings
     and before actions: the action GENs consume fact rows, so the fact phase
     must precede them. K1 reverses only the twelve action GEN calls; the
     reading-before-action and fact-before-action dependencies are load-bearing
     and intentionally not reversed.
2. **ELIM:** Single elimination loop over actions (13-24).
   - PRE_FAIL: precondition false.
   - GATE: withhold/eliminator gate.
   - OUTSCORED: marked BEFORE any ELIM trace (repair #2).
3. **ARGMAX:** Winner = max score among survivors; tie → lowest hid.
   - Margin <5 → close_call flag set, CLOSE + 2×CONTENDER + flag-gated REVIEW.

**G2 Compliance:** No separate fact ELIM/ARGMAX phase. The clarify/withhold/default
GENs select the best gated fact via `best_gated_fact()` (scans hid 10-12), ensuring
all candidates are generated before any elimination.

## Reading-Row Causal Wiring (repair #4 — fixes red-team-3 R2)

`gen_readings` is the SOLE utterance classifier. It writes ten kind-0 rows; every
action GEN precondition branch-reads them from the ledger instead of re-deriving
intent from the raw utterance. Neutering `gen_readings` (done-flag only) changes
31/77 answers with no crash — the rows are causal, not decorative.

| HID | Reading | Computed in gen_readings as | Consumed by (branch read site) |
|---:|---|---|---|
| 0 | correction | `is_correction(...)` | gen_correction: `lr_get(led,0,12)==1` |
| 1 | resume | `is_resume(...)` | gen_resume: `lr_get(led,1,12)==1` |
| 2 | challenge | `is_challenge(...)` | gen_challenge: `lr_get(led,2,12)==1` |
| 3 | provenance | `prov_match(...)`; match offset staged in row field 16 | gen_provenance: `lr_get(led,3,12)==1`, offset via `lr_get(led,3,16)` |
| 4 | joke | `utter_type==1` | gen_joke: `joke_ev=lr_get(led,4,12)` → `if(joke_ev==1)` |
| 5 | mem | `utter_type==2` | gen_mem: `mem_ev=lr_get(led,5,12)` → `if(mem_ev==1)` |
| 6 | forget | `utter_type==3` | gen_forget: `forget_ev=lr_get(led,6,12)` → `if(forget_ev==1)` |
| 7 | assertion | no `?` in utterance | gen_assertion: `lr_get(led,7,12)==1` AND hid 9 |
| 8 | compose | `r_compose_ev(...)` (canonical compose-intent meter; covers every `do_compose` trigger incl. all `do_compare` comparison words) | gen_compose: `cev=lr_get(led,8,12)` → `if(cev>0)` gate before `do_compose` |
| 9 | plain | residual: ev=1 iff none of hids 0-6,8 fired (hid 7 excluded) | gen_assertion: `... && lr_get(led,9,12)==1` |

Notes:
- The traced decision fields are evidence (`lr_get(led,hid,12)`) and score
  (`lr_get(led,hid,24)`); every site above branch-reads the evidence field.
  Reading-row scores are not traced (`READ` lines carry `hid`, `rd`, `ev`);
  the row layout stays uniform with the other 15 rows.
- `is_correction`, `is_resume`, `is_challenge`, `prov_match`, `utter_type`,
  `r_compose_ev` are called ONLY from `gen_readings` (static audit). No action
  GEN re-derives intent; sub-parsing inside a fired action (e.g. extracting the
  corrected entity span) is argument extraction, not classification.
- Fully-neutered readings (all ev=0) are handled safely: no special-intent bid
  fires, and the withhold/default path answers. No crash, no empty ARGMAX.

## The 12 Action Bids

| HID | Action | Base | Fires When |
|-----|--------|------|------------|
| 13 | joke | 240 | reading hid 4 (joke) |
| 14 | memory | 237 | reading hid 5 (mem) |
| 15 | forget | 234 | reading hid 6 (forget) |
| 16 | correction | 231 | reading hid 0 + prior entity |
| 17 | resume | 228 | reading hid 1 |
| 18 | compose | 225 | reading hid 8 (compose) |
| 19 | challenge | 222 | reading hid 2 |
| 20 | provenance | 219 | reading hid 3 |
| 21 | assertion | 216 | readings hid 7 AND hid 9 (plain) |
| 22 | clarify | 213 | predicate mismatch + named entity |
| 23 | withhold | 210 | no fact or gate failure |
| 24 | default | 207 | "did ..." + entity |

**Base scores** compressed from 20-point gaps to 3-point gaps (repair #10) to allow
close-call margins <5. Priority order preserved; bonuses (0-3) reflect evidence.

## Content Tracing (BUILD_SPEC §4)

Every KB-derived value flowing into answer bytes appears in the trace:
- `FACT hid=` lines for fact candidates (even when missing).
- `CONTENT hid=... fact="..."` with full fact text.
- `shaped=` indicates correction entity-swap.
- `ARGMAX`, `CLOSE`, `REVIEW` all cite `hid=`.
- `READ hid= rd= ev=` lines carry the hid (G5) and human-readable reading name (G6).

## Side-Effect Partition

ACT reads the winner (status 2) and applies side effects:
- Novelty from ledger offset 448 (not 432).
- Return fid from offset 452 (not 436).
- Prior-query state updated ONLY when the winner is not withhold/clarify
  (prevents R4-03 turn 4 regression).

## Close-Call Mechanism

When winner margin <5 over runner-up:
1. `close_call()` sets flag at 13812.
2. `CLOSE hid=` emitted with winner hid.
3. Two `CONTENDER hid=` lines for winner and runner-up.
4. `REVIEW` gated on reading flag 13812 (not a local variable).

**Note:** Natural close calls are rare due to bid precondition exclusivity.
The mechanism is verified by code inspection and the scoring allows <5 margins.

## K5 Status

K5 (adversarial red team) is NOT self-certified. A fourth independent red team owns it.
