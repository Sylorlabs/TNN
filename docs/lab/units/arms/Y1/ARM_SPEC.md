# Y1 — Negotiated cuts: ARM SPEC

**Status:** FROZEN design for build. Implements the frozen §3 row
(`units/PREREG_FREEZE.md` line 491, byte-identical to frozen commit
`b0b9140c0eda` per coordinator verification) and `units/arms/briefs/Y1.json`.

| | |
|---|---|
| Arm | Y1 — Negotiated cuts |
| Family | CUT |
| Mechanism (frozen) | Two-organ cut protocol with mutual veto; deadlock → deliberate adjudication with a round limit. |
| Binding kill (frozen) | Over 10,000 cuts, negotiated boundaries show ≤10% better recall-stability than arm-D unilateral cuts at the same granularity; OR veto rate collapses to <1% within the first 1,000 cuts (lazy agreement — then Y1 ≡ D with extra ledger cost). |

## 1. Mechanism (literal implementation)

Two internal organs negotiate every interior chunk boundary:

- **Organ F — fast segmenter (ingestion side).** Proposes the fixed 64-byte grid
  cut: boundary at `grid = i*64`, provisional span for the unit.
- **Organ S — slow verifier (recall side).** May VETO with a written justification
  drawn from the fixed justification enum (§2), or COUNTER-PROPOSE an alternative
  boundary. May also ACCEPT.
- **Deadlock (>N rounds) → deliberate adjudication.** A fixed deterministic rule
  issues a binding cut, logged to the audit ledger with both organs' proposals
  attached as evidence (in the entry's aux fields).

### 1.1 Negotiation protocol (deterministic, zero RNG)

For interior boundary position `g` (grid), with corpus buffer `buf`:

- **Round 1.** F proposes `g`. S checks *word-split*: `is_word(buf[g-1]) &&
  is_word(buf[g])` where `is_word(c) = [A-Za-z0-9_]`.
  - No split → ACCEPT. (rounds=1, vetoes=0, justification J_NONE)
  - Split → S finds the nearest word joint: scan left for the nearest `p` with
    `!is_word(buf[p])` (candidate `p+1`), scan right for the nearest `q` with
    `!is_word(buf[q])` (candidate `q+1`); search window ±32 bytes. If no joint in
    window → ACCEPT with justification J_NO_JOINT. Else `j` = nearer candidate
    (ties → left = ledger order). S issues VETO(J_SPLIT_TOKEN) + COUNTER(`j`).
- **Round 2.** F examines counter `j`:
  - `|j-g| ≤ 16` → ACCEPT.
  - Else F issues VETO(J_EXCESS_SHIFT) + COUNTER(`clamp(j, g±16)` toward `j`).
- **Round 3.** S examines the clamped counter `c`:
  - No word-split at `c` → ACCEPT.
  - Else → DEADLOCK → adjudication.
- **Adjudication** (deterministic "deliberate" rule): the adjudicator selects the
  proposal nearest to a word joint; ties resolve for the fast segmenter's
  proposal (ledger order). Logged with both proposals as evidence.

Round limit **N = 3** (A-45: the prereg requires a value; 3 is the smallest N
allowing propose → counter → counter-counter → adjudicate).

### 1.2 Justification enum (A-45; fixed, preregistered here)

| Code | Name | Meaning |
|---|---|---|
| 0 | J_NONE | Accept; no veto issued |
| 1 | J_SPLIT_TOKEN | Boundary splits a word token (`[A-Za-z0-9_]` run) |
| 2 | J_EXCESS_SHIFT | Counter-proposal moves the boundary >16 B from the grid |
| 3 | J_NO_JOINT | No word joint within ±32 B; grid accepted |
| 4 | J_ADJUDICATED | Deadlock resolved by the adjudicator |

### 1.3 Ledger encoding (frozen opcodes; aux fields carry the transcript)

Per ALPHABET_Y-Z buildability note ("log only the final cut + both final
proposals — deterministic replay needs the transcript only if the consolidation
organ's rule is not a pure function of the proposals; make it one"): the
negotiation outcome is a pure function of (grid position, corpus bytes), so ONE
`ADD_UNIT` (0x01) entry per ingested unit suffices for byte-identical replay.
The binding cut is logged with both organs' proposals as evidence in aux fields:

- `b1` = byte_offset_lo, `b2` = hi, `b3` = length, `b4` = corpus_id,
  `b5` = unit_id (per §6)
- `a1` = negotiation rounds used (0 for unit 0 / unilateral mode)
- `a2` = vetoes issued on this unit's left boundary
- `a3` = final justification code (§2)
- `a4` = adjudicated flag (1/0)
- `a5` = supersedes_id (M7 new-version linkage; 0 otherwise)
- `d1` = grid position proposed, `d2` = final boundary position

All other ops use the frozen opcodes with the §6 field semantics.

### 1.4 ID-arm confirmation

Y1 **is an ID arm** (§9): `recall` takes a unit ID and resolves it through a
persistent `id→slot` table the arm maintains (`id2slot` array; sequential IDs
assigned at negotiation close; tombstoned IDs never reused). This matches the
provisional §9 classification (y1 listed as ID, subject to crew confirmation —
**confirmed**) and the ALPHABET mechanism ("provisional ID", "without ID
reassignment"). Consequences:

- M1 includes the **provisional N=64 swap probe** (A15 procedure, labeled
  `PROVISIONAL-PENDING-FREEZE`): after every `ceil(nunits/64)` recalls, the ID
  table entry for the next recall target is patched to the next live slot
  (wrapping), `TRAINER_SWAP_PROBE` (0x13) is logged, the recall is issued and
  must return the remapped content (else loud failure); the mapping is restored
  afterwards. Probe recalls are excluded from the M1 percentages;
  `m1_id_probe` reports the outcome.
- M7 applies (ID-arm rig): hit ≥ 90%, reuse ≥ 1.5, dedup ≥ 0.4.
- Repeated ingestion of identical (corpus, span, bytes) resolves to the SAME ID
  (dedup). Same span but changed bytes (M7 round 2) → new-version ID linked to
  the old via `a5`.

### 1.5 Unilateral reference ("arm-D unilateral cuts at the same granularity")

The frozen kill compares against "arm-D unilateral cuts at the same granularity".
This crew cannot run arm D's five-organ pipeline, and D's granularity is not the
64-byte grid — so "run D's binary" cannot satisfy "at the same granularity". The
literal operationalization (Y1-A2): the unilateral reference is the SAME Y1
binary with negotiation disabled (fast segmenter decides alone = unilateral,
"boundaries decided by either alone" per the ALPHABET claim), at the identical
64-byte granularity, on the identical 10,000 cuts. `negotiate()` short-circuits
to the grid proposal (rounds=1, vetoes=0, J_NONE).

## 2. Kill-trial operationalization (`kill-1x` mode)

- **Corpus:** `prose.bin`, first 10,000 grid positions (10,000 cuts). (Y1-A4:
  corpus not specified by the kill; prose = corpus A, the primary text corpus.)
- **Veto rate:** (boundaries with ≥1 veto among the first 1,000) / 1000.
  Kill disjunct 2 fires iff veto rate < 1%.
- **Revision curriculum:** the exact M4 procedure on both instances — 100
  boundary defects (frozen cycling deltas ±1..±48) + 100 content defects
  (frozen patch rules) at fixed indices `i*10000/200`, ≤20 revision episodes
  through the arm's own `revise`.
- **recall-stability:** fraction of the 10,000 units with committed span intact
  AND original ID AND byte-exact recall after the curriculum (no re-cut, no ID
  reassignment).
- Kill disjunct 1 fires iff `stab_negotiated ≤ 1.10 × stab_unilateral`.
- The mode emits `METRIC_JSON` with `y1_kill_*` fields and the verdict, plus a
  human-readable `KILLTRIAL` summary line. Either disjunct firing → arm KILLED
  (death certificate in VERDICT.md).

## 3. Mode table (all §3 modes + `kill-1x`)

`y1_bin <mode> <corpus-root> [outdir] [perturbation]`, one binary, fresh process
per mode. Modes: `m1-1x-prose`, `m1-1x-code`, `m2-t1-prose`, `m2-t1-code`,
`m2-t2-prose`, `m2-t2-code`, `m2-t3-1x`, `m3-1x`, `m4-1x-prose`, `m4-1x-code`,
`m5-1x`, `m5-baseline`, `m6-p2c-1x`, `m6-c2p-1x`, `m7-1x`, `m8-1x`,
`kill-1x`. JSON field names follow ARM_INTERFACE.md §3 exactly; Y1 extras are
`y1_*`-prefixed (`y1_veto_rate_tenths`, `y1_kill_*`) or the specified
`m1_id_probe`.

M8 runs M1 (prose+code, with swap probes) + the M3 op sequence on one
large-capacity instance (A17: the validator's combined-instance reading),
artifact capture per §7 (all five perturbations implemented).

## 4. Ambiguities (literal readings adopted; see §6 for the full list)

- **Y1-A1** (coordinator corrections vs brief — BOTH explicitly acknowledged):
  1. The original assignment wrongly identified Y1 as "Adversarial corpus
     probe". The coordinator voided that mechanism; all wrong-path scripts and
     work were discarded (deleted 2026-09-21, no wrong-path build or battery
     was ever completed).
  2. A later coordinator message admitted its own remembered paraphrase of the
     frozen row (META family, "fast segmenter/slow verifier", ">25%
     add-latency" kill) was ALSO wrong, and superseded it with the verbatim
     frozen row.
  3. Final binding authority order: (1) `briefs/Y1.json`, (2) the coordinator's
     verbatim row, (3) nothing else the coordinator previously wrote. The brief
     and the verbatim row agree (CUT family, two-organ cut protocol with mutual
     veto, deadlock → deliberate adjudication with a round limit, binding kill
     = recall-stability disjunct OR lazy-veto disjunct); `PREREG_FREEZE.md` §3
     was observed matching. Followed: the brief = the frozen row.
- **Y1-A2** (unilateral reference): §1.5.
- **Y1-A3** (M8 swap probes): included in M8's M1 phase (literal "M1 procedure").
- **Y1-A4** (kill corpus): prose.bin, first 10,000 cuts.
- **Y1-A5** (M7 field names): §3 table names vs §10 definitions; emitting
  `m7_hit_rate_tenths`, `m7_reuse` (ratio), `m7_dedup` (ratio),
  `m7_reread_bytes`, documented.
- **Y1-A6** (recall-stability): §2 definition (no frozen operationalization).
- **Y1-A7** (A15 swap-probe schedule): adopted the §9/A15 proposal verbatim,
  labeled PROVISIONAL-PENDING-FREEZE (Micah has not frozen it).
- **Y1-A8** (M7 C′ edit / lookup schedule): A7/A8 unresolved — adopted the
  validator's documented placeholder (first-byte XOR 0xFF; `(l*37)%nunits`,
  1666/1667/1667 split) literally, flagged provisional.

## 5. Determinism

Zero RNG in any decision path. Negotiation is a pure function of corpus bytes.
Placement: bump allocator (no free-list; `freelist` perturbation is an accepted
no-op per A11 — placement is a pure function of ingest order). M3 pressure mode
reuses slots by lowest-index scan (deterministic). No wall-clock, no addresses,
no uninitialized reads in any artifact path.

## 6. Full ambiguity list

Y1-A1 … Y1-A8 as above, plus inherited harness ambiguities A1–A17
(`../harness/AMBIGUITIES.md`) applied literally (A1: C_M3=4000; A2: k-schedule;
A3: weaken timing; A4/A5/A16: M5 accounting; A7/A8: provisional M7 choices;
A11: freelist no-op; A15: provisional swap probe; A17: combined-instance M8).
A-45 (round limit N=3; justification enum §2) resolved by this spec.
