# VERDICT — Arm T (episode-aligned chunks), Track A closeout

**Date:** 2026-09-21
**Arm:** T — Episode-aligned chunks (STRUCT family)
**Adjudicated by:** marathon crew U10 (B-battery adjudication)

## BINDING VERDICT: **KILLED**

Kill criteria **(i), (ii), and (iv) each fire independently on both corpora**.
Per RULE-7 (per-arm kill criteria are BINDING — a fired bar kills, no appeals),
arm T is dead as a candidate.

## Frozen kill criterion (verbatim, §3 of `units/PREREG_FREEZE.md`, extracted programmatically)

> Any one: (i) B2 within 2× of X's on either corpus; (ii) >80% of battery recall queries address sub-episode spans (the "unit of experience" claim falsified); (iii) determinism gate fails; (iv) floor rule fires.

## B-battery evidence (2026-09-21, `work/bbattery/`)

Crew-4 shared prereg battery (`units/ALPHABET_S-X.md`) run natively in pure Zag
(`batt.zag`, struct-free; driver `run_battery.sh`) for T and X on both corpora
(prose `pg100.txt` 5,638,480 B; code `sqlite3.c` 9,515,341 B), N=5 reruns per
(arm, corpus) — all 20 runs byte-identical (B7 PASS). Zero RNG in any decision
path; span schedules are fixed deterministic arithmetic (crew decisions D1–D7
in `work/bbattery/BATTERY_EVIDENCE.md`).

| corpus | B2_T/B2_X | B4 T vs X | B5 T vs X | B9 T vs X | sub-episode queries (T) |
|---|---|---|---|---|---|
| prose | **1.000000** (2747.02 = 2747.02) | 1.0 = 1.0 | 5,638,480 = 5,638,480 | 2751.82 = 2751.82 | 13000/13000 = **100%** |
| code  | **1.000000** (4635.79 = 4635.79) | 1.0 = 1.0 | 9,515,341 = 9,515,341 | 4643.89 = 4643.89 | 13000/13000 = **100%** |

### Criterion (i) — B2 within 2× of X's: **FIRES** (both corpora)

B2_T/B2_X = 1.000000 ≤ 2. T's episode ≡ X's stream under single-file ingestion:
every partial recall materializes the whole 5.6/9.5 MB unit. This is the
frozen prereg's predicted weakness W1 ("code-corpus collapse"), measured.

### Criterion (ii) — >80% sub-episode queries: **FIRES**

100% of the 13,000 battery recall queries address spans (8–4096 B) strictly
smaller than the episode. The episode ID does ~0% of addressing work on
knowledge-sized queries — the "unit of experience" claim is falsified; T is
X-with-offsets.

### Criterion (iii) — determinism gate fails: **does NOT fire**

M8: M1+M3 byte-identical across 10 runs (prior). B-battery B7: 20/20 runs
byte-identical (sha256 digests in `BATTERY_EVIDENCE.md`).

### Criterion (iv) — floor rule fires: **FIRES** (both corpora)

Universal floor rule (ALPHABET_S-X.md, frozen at sign-off per A-44): an arm that
fails to beat X on *any* of B2/B4/B5/B9 is dead on arrival (ties permitted only
on B1/B7). T ties X on all four — beats X on 0 of 4.

## The finding (as the frozen prereg predicted)

On single-file ingestion T degenerates *exactly* to X (B2 ratio 1.000000, not
approximately — the mechanisms coincide), and the episode ID carries no
addressing work for knowledge-sized queries. Episode granularity is hostage to
ingestion batching, which is about I/O rather than knowledge. This is itself
the publishable finding the prereg anticipated.

## Prior record (superseded provisional verdict, retained for audit)

- M-harness: builds pure Zag (`cl/arm_final.zag`); M1 1 episode / 0 boundaries
  by design; M2 1000/1000 recalls; M3 4000 episodes verified; M4 defect
  detected/repaired; M5 table 48,000 B + data 6,086,480 B; M6 tombstone holds;
  M7 re-ingest distinct IDs; M8 10/10 byte-identical.
- 2026-09-21 closeout verdict was PROVISIONAL (B-battery + X evidence missing).
  That evidence now exists; the provisional status is CLOSED by this verdict.
- X's B-battery evidence (previously nonexistent) is in
  `work/bbattery/BATTERY_EVIDENCE.md` + `ev_x_*.txt`.

## Files

- `work/bbattery/batt.zag` — battery source (pure Zag)
- `work/bbattery/run_battery.sh` — driver (build, N=5, sha256 gate, ratios)
- `work/bbattery/BATTERY_EVIDENCE.md` — full evidence + crew decisions
- `work/bbattery/VERDICT_NUMBERS.txt` — computed ratios
- `work/bbattery/ev_{t,x}_{prose,code}_r{1..5}.txt` — 20 raw run outputs
