# Z6 — Scar boundaries · ARM_SPEC

Family: CUT. Pure Zag on Linux. Zero RNG in any decision path.

## 1. Mechanism (frozen brief + implementation)

Boundaries form at revision sites: ledger scar tissue segments the stream;
"meaning lives where things changed." Bootstrapped from arm-D-style cuts.

Pipeline, all deterministic:

1. **Bootstrap.** D-style 64-byte grid cuts at `0, 64, 128, …, L`. Each cut
   records a birth ledger sequence of `-1` (bootstrap-born).
2. **Revision replay.** The frozen offline 10,000-revision schedule replays:
   each revision appends a scar `(start, end, ledger_seq)` and a ledger event.
   Scar endpoints increment density counters on 64-byte cells. (Even schedule
   entries are ground-truth-unit-aligned — planted by the trainer harness;
   odd entries are content-blind spans. The arm never generates schedules.)
3. **Proposal.** Any cell whose endpoint density reaches `DENS_BAR` proposes
   its mean endpoint. Proposals are sorted and deduped (`DEDUP_D`).
4. **Ratification (consolidation).** Each proposal may displace the nearest
   bootstrap cut within `DISP_WIN` bytes. Displacement is logged as a
   deliberate ledger event (`OP_DISPLACE`); the displaced cut's birth sequence
   becomes the ratification's ledger seq. Proposals that would invert cut
   order are refused and logged (`OP_REFUSE`).
5. **Chunk identity.** A chunk's ID binds `(birth_scar_seq, span)`; the M7
   ID layer resolves `(bseq, start, len)` through the slot table.

Scars are events authored by deliberate operations, not strength-by-accumulation.

## 2. Frozen build parameters

| Symbol | Value | Meaning |
|---|---|---|
| `GRID` | 64 | bootstrap cut spacing (bytes); density cell width |
| `DENS_BAR` | 2 | endpoint hits per cell to propose a boundary |
| `DISP_WIN` | 32 | max displacement distance (bytes) |
| `DEDUP_D` | 32 | proposal dedup distance (bytes) |
| `GT_WIN` | 64 | ground-truth match tolerance (bytes, crew interpretation — see §8) |
| `RCTRL_K` | 5 | same-count random-control replicates |

Corpus lengths (frozen, from `scar_schedule.py`): sqlite code 9,515,341 B;
Shakespeare prose 5,422,721 B.

## 3. State

Flat `Z6` struct, no nesting. Slot table (`starts/lens/flags/bseq`), owned
corpus image + harness source, scars, density cells, cut table with birth
sequences, and a 4-shard append-only audit ledger (16-word entries:
op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48, stage@52, d1@56, d2@60).
Every slice is under 2^25 bytes (znc limit); large corpora are held as owned
copies (both fit individually).

Deliberate ops: ADD / KILL / PIN / WEAKEN / EVICT / DISPLACE / REFUSE /
REPAIR_C / REPAIR_B — all ledger-audited with stage tags (ingest, trial,
revise).

## 4. Kill criterion (frozen §3, verbatim)

> "Scar boundaries match ground-truth units (sqlite3.c function boundaries,
> Shakespeare act/scene structure) no better than random cuts at the same
> count (±10%) — the claim is dead; OR the bootstrap arm's cuts are never
> displaced by scars after 10,000 revisions (decorative)."

Adjudication (M1, per corpus):
- **Clause A.** `scar_rate` = fraction of scar-born boundaries within
  `GT_WIN` of a ground-truth boundary; `rand_rate` = mean over `RCTRL_K=5`
  same-count SplitMix64 control replicates (fixed trainer-side seeds —
  offline references only, never an arm decision). Fires iff
  `scar_rate ≤ rand_rate × 1.10`.
- **Clause B.** Fires iff `displaced == 0` after the full 10,000-revision
  replay.
- A **blind-only variation** (odd/content-blind schedule entries only) is
  reported alongside: it shows what the mechanism discovers with no
  ground-truth-planted revisions.

## 5. Modes

| Mode | Trial |
|---|---|
| `m1-1x-prose` / `m1-1x-code` | full battery leg: segment → ingest → probe (recall/boundary) + scar trial (all + blind) + random controls + kill adjudication + A15 probe |
| `m2-t1-prose` / `m2-t1-code` / `m2-t2-prose` / `m2-t2-code` / `m2-t3-1x` | episodes-to-criterion on novel material; ETC = first of sustained-3 at recall ≥99.5%, boundary ≥95% (censor 50); episode 0 = no-ingest leak check; M9 shape recorded |
| `m3-1x` | 10,000-step churn: 1,000 pinned valuable + 3,000 fresh ingest + 3,000 kills + 50 weakens + 4,000 fresh at capacity (500 evictions); freeze distinguisher |
| `m4-prose` / `m4-code` | 200 defects (100 content + 100 boundary), deliberate repair, lineage (bseq) check, repair-entry ledger audit |
| `m5-1x` | deliberate-storage accounting **[PROVISIONAL-PENDING-FREEZE]** |
| `m6-code-prose` / `m6-prose-code` | scar policy transfer, both directions kept separate |
| `m7-1x` | ID-layer claim: 200 genuine IDs resolve, 100 forged rejected |
| `m8-p0` … `m8-p5` | determinism battery: sha256(memory image, audit bytes, state, alloc trace) under 5 environmental perturbations ×2 runs |

A15 (64 deterministic ID-remap probes) runs inside M1, labeled
`PROVISIONAL-PENDING-FREEZE`.

## 6. Determinism

Zero RNG in AI decision paths. SplitMix64 appears only as the frozen
offline schedule generator (trainer side) and the fixed-seed random
*control* replicates in scoring — never in a mechanism decision. Every 1x
leg runs twice with byte-identical stdout required; M8 verifies
byte-identical hashes under heap pre-dirtying, fragmentation, image
pre-fill, stdout junk, and layout jitter.

## 7. Metrics

`metrics-v1` JSON fragments, one per mode, assembled into
`scorecard_z6_1x.json`. Tenths-of-a-percent fields are explicit
(`*_tenths`). Provisional cells carry `*_provisional: 1`.

## 8. Known ambiguities (crew interpretations, documented not hidden)

1. **`GT_WIN=64`.** The frozen row does not state a positional tolerance for
   "match". 64 bytes (one grid cell) is the crew's preregistered
   interpretation. Exact-match counts are also computable from the evidence
   but are not the adjudication basis.
2. **"Same count".** Read as: the number of scar-born boundaries the trial
   produced; the random control draws exactly that many cuts.
3. **"±10%".** Read as a relative band on the scar rate vs the random
   control mean (clause A fires iff `scar ≤ rand × 1.10`).
4. **Clause A scope.** The frozen schedule's even entries are
   ground-truth-unit-aligned by construction (trainer-planted), so the
   all-schedule scar rate *must* beat random — the trial measures how the
   mechanism consolidates planted revisions, not discovery. The blind-only
   variation is the honest discovery check and is reported, not adjudicated.
5. **M5 / A15 provisional.** Storage accounting and the ID-remap probe stay
   `PROVISIONAL-PENDING-FREEZE` pending Micah's freeze-vs-retention ruling,
   per crew convention.
