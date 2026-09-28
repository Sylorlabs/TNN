# Arm-3 Variation C — Proposal-Policy Spec (FROZEN)

**Teacher:** arm-3 variation C, "engagement-meter teacher", `teacher_id=3`.
**Implementation:** `teacher.zag` (pure Zag; this document is the binding text it implements).
**Status:** FROZEN 2026-09-21. Any change to rules, constants, or exit codes needs Micah's re-approval.

## §0. What this teacher is

The mapping `(spec, stimulus cursor, session history) → §P proposal sequence`
lives **entirely in the teacher**. The driver ferries bytes: it appends the
teacher's emitted proposals and the student's decisions to the decision tape
and re-invokes the teacher. The teacher keeps no state between invocations;
every invocation replays the full tape and re-derives everything, so the
recorded proposals are provably the teacher's own output (`selfcheck` mode).

**Negative declarations (auditor-verifiable, per B.2.5):**

- No learning machinery. Per-session state is exactly: engagement `E` (i32),
  consecutive-reject counter, region cursor, 64-bit covered-region mask,
  retract-arming flag, ≤64 proposal records, ≤64 adopted spans. Fixed-size,
  session-scoped, recomputed from the tape on every invocation. No
  self-modification across sessions; no weight updates; no fitted parameters.
- No RNG in any teacher path. Verified by N=5 byte-identical runs plus
  adversarial heap perturbations (8/8 byte-identical: allocator-fill patterns
  and environment-block size perturbations).
- No wallclock. The teacher reads no clock; ordering comes from tape order
  only (logical ticks).

## §1. Inputs

One invocation reads:

1. `slice_idx` (0–7), `session_id` (u64) — CLI.
2. Slice bytes: `<wired_dir>/slice_S{slice_idx}.bin`, exactly 65536 bytes
   (frozen T-11 layout; §P span offsets are slice-relative per W-01).
3. Vocabulary table `<wired_dir>/vocab.bin` (arm-1 wired layout: `chunk_id`-ordered
   entries with match rule, signed judgment, literal pattern). Only entries
   with judgment > 0 are ever proposed; domain gate: prose slices (0–3) use
   `P`/`N` entries, code slices (4–7) use `C` entries.
4. The **decision tape** `<hist_dir>/<hist_name>` (binary):
   - Header (32 B): magic u32 `0x48434454`, version u16 `1`, session_id u64,
     stim_len u64 (= 65536), nevents u32 (≤ 512).
   - Records (256 B each), in tape order:
     - `PROPOSE` (tag 1): seq u64, kind u8 (1–5), span u64×2, confidence u8,
       aux_count u8 (≤ 2), ground_count u8 (≤ 4), aux pairs, grounding pairs.
     - `DECIDE` (tag 2): proposal seq u64, verdict u8
       (1=ADOPT, 2=REVISE, 3=REJECT, 4=DEFER), reason u16
       (0=none; R1–R6 = 1–6), rev_start/rev_end u64 (carried, unused —
       teachers read decisions, never memory).

Malformed tape → exact exit code (§6), logged on fd 2, **zero bytes on stdout**.

## §2. The engagement meter (exact update rule)

`E` is an i32 in `[0, 1000]`, initially 0. Tape events are folded in order:

- `PROPOSE` event: `E := clamp(E − 20)` (per-proposal decay).
- `DECIDE` event, by verdict:
  - ADOPT: `E := clamp(E + 120)`; consecutive-reject counter := 0;
    span appended to the adopted ledger.
  - REVISE: `E := clamp(E + 60)`; consecutive-reject counter := 0.
  - DEFER: `E := clamp(E + 10)`; consecutive-reject counter := 0.
    (DEFER is non-final: the proposal stays un-decided.)
  - REJECT: `E := clamp(E − 150)`; consecutive-reject counter += 1.
    If the counter reaches exactly 2: `E := clamp(E − 200)`,
    cursor `:= (cursor + 13) mod 64` (jump to a new region), and the
    retract rule is **armed** for the next emission (§3.1).
- `clamp(x) = max(0, min(1000, x))` after every update.

`E` is a pure function of the decision tape: recompute-from-tape equals the
incremental value by construction (there is no incremental value — every
invocation replays the tape). Verified by `trace` mode against an independent
Python reference implementation at every event.

## §3. Emission decision

One invocation emits **exactly one** §P proposal (`seq` = number of `PROPOSE`
events so far; ≤ 64 per session, then exit 20 with no output). Bands are read
off `E` **before** the new proposal's decay is applied (the decay lands when
the proposal is recorded):

- **cold**, `E < 300`: confidence `60 + (E mod 41)` → 60–100.
- **warm**, `300 ≤ E < 700`: confidence `120 + (E mod 61)` → 120–180.
- **hot**, `E ≥ 700`: confidence `180 + (E mod 41)` → 180–220.
  **Confidence never reaches 255 by policy** (expressed uncertainty by
  construction; the §C secondary tripwire is unreachable).

Grounding budget: cold 1; warm 1, or 2 if `E ≥ 500`; hot 2, or 3 if `E ≥ 850`.

### §3.1 Double-reject rule (any band)

If the trailing run of `DECIDE` events is exactly 2 REJECTs and the arming has
not been consumed by a later proposal: the next emission is a `RETRACT`
(kind 5, `span_start` = target proposal seq, `span_end` = seq+1, no aux, no
grounding) withdrawing the **most recent un-decided proposal**. If no
un-decided proposal exists, the rule degrades to the `E −= 200` + cursor jump
(which already happened at the second REJECT) and a normal proposal is
emitted; either way the arming is consumed by the next proposal. A further
REJECT extends the run to 3 and does **not** re-arm (no retract spam).

### §3.2 Warm appeals

In the warm band, if the latest `DECIDE` event is a REJECT with reason
R1/R2/R5 of a WORD_SPAN proposal, the teacher **appeals**: it re-proposes the
identical span with **new grounding** (occurrence spans not used in the
rejected attempt; the appeal is skipped if none exists). Budgets (B.5):
max 2 appeals per original proposal seq per session; a span with 2
session-final rejections is dead for the session and never re-proposed.
R3/R4 rejections are never appealed (final for the session).

### §3.3 Hot relational proposals

In the hot band, when ≥ 2 spans are adopted, emissions cycle deterministically
(`seq mod 3`) among relational forms over the two most recently adopted spans
A (older), B (newer):

- `0`: `SAME_AS` (kind 4) — primary span B, aux = [A].
- `1`: `BOUNDARY` (kind 2) — primary span = the gap `[A.end, B.start)`
  (falls back to `SAME_AS` if the spans overlap/are adjacent).
- `2`: `GROUP` (kind 3) — primary span = minimal covering span, aux = [A, B].

Grounding = neighboring word spans of the primary span (2–3 per budget).

### §3.4 Fresh probes (cold, and whenever nothing above applies)

Regions: 64 × 1024-byte regions. The teacher scans from the cursor in steps
of 7 (mod 64), skipping regions already covered this session (cold band:
fresh regions only), and takes the first region containing a candidate.
Candidate: the vocabulary occurrence (rule-respecting, judgment > 0,
domain-gated) with smallest `(start, entry_index)` in the region, excluding
spans already live (adopted / un-decided / revised) and dead spans
(2 final rejections). Grounding: other occurrences of the same pattern first,
then neighboring word spans. If no region yields a candidate, the fallback is
the first word-byte run in the cursor region. Fresh proposals are
`WORD_SPAN` (kind 1) only.

Region consumption (cursor advance, covered mask) is folded from the recorded
`PROPOSE` events during replay, so it is a pure function of the tape.

## §4. §P conformance (frozen B.3)

Wire layout exactly per `sp345.zag` / arm-1 `t_emit`: magic `0x54505250`,
version 1, `teacher_id = 3`, harness session_id, monotonic seq, kind 1–5,
`span_start < span_end`, spans within the stimulus, aux_count ≤ 2,
ground_count ≤ 4, confidence 0–255, checksum = FNV-1a-64 over preceding bytes.
Thesis holds: spans only (no token ids, no text payloads), no commands
(confidence is a judgment weight, never an instruction), `RETRACT` withdraws
by seq per the fixture convention.

## §5. §C tripwire

The teacher keeps the conservative **cumulative** session monitor (documented
deviation from frozen B.8's rolling-200 window, strictly more conservative —
parked for Micah): FIRE iff `coverage ≥ 0.95 AND accept_rate ≥ 0.95 AND
maxconf_rate ≥ 0.90` over the session, or any single `confidence = 255`
proposal covering > 5% of the stimulus. The teacher can never fire it in
normal operation: confidence ≤ 220 always, proposals are selective (≤ 64
small spans). Smuggle-tiling and vocab-dump probes fire as specified
(verified in `evidence/`).

## §6. Exit codes

`0` proposal emitted (or `selfcheck`/`trace` OK). Malformed input → exact
code, logged on fd 2, zero stdout bytes:

| code | meaning |
|---|---|
| 1 | history: bad magic (`V_BAD_MAGIC`) |
| 2 | history: bad version (`V_BAD_VERSION`) |
| 3 | history: session_id mismatch (`V_BAD_TEACHER`) |
| 4 | history: seq violation — non-monotonic/gapped `PROPOSE` seq, `DECIDE` of unknown or already-final seq (`V_SEQ`) |
| 5 | history: `span_end ≤ span_start` in a `PROPOSE` record (`V_SPAN`) |
| 6 | history: bad kind/tag/verdict/reason (`V_KIND`) |
| 8 | history: span out of stimulus range (`V_RANGE`) |
| 9 | history: aux/ground count out of range (`V_COUNTS`) |
| 10 | history: bad size / nevents mismatch / truncation (`V_LEN`) |
| 13 | CLI/IO error (bad args, unreadable slice/vocab/history) |
| 20 | session cap (64 proposals) reached — clean stop, no proposal |
| 21 | `selfcheck`: recorded proposal ≠ recomputed proposal (tape divergence) |

`propose` / `selfcheck` / `trace` are the three modes; all validate the tape
identically before acting.

## §7. Verification summary (evidence in `evidence/`)

- N=5 byte-identical runs on a fixed scripted history.
- 5/5 byte-identical under adversarial heap perturbations (`MALLOC_PERTURB_`).
- `selfcheck`: every recorded proposal re-derived from its tape prefix on
  4 scripted sessions (incl. a 64-proposal session).
- E recompute: teacher `trace` vs independent Python reference, equal at
  every event (24/12/28/24 events).
- History sensitivity: all-ADOPT → E hits 1000, hot relational proposals
  (SAME_AS/BOUNDARY/GROUP), confidence up to 220; all-REJECT → E pinned at 0,
  cold probes only (WORD_SPAN, confidence 60–100).
- §P iron-rule battery: 19 hostile histories → exact exits, logged, zero
  proposals; forged proposal caught by `selfcheck` (21).
- §C: smuggle tiling fires (code 1), vocab dump fires immediately (code 2),
  clean teaching never fires.

## §8. No flaw manifest (T-7)

Natural teaching only. The teacher proposes honest vocabulary spans with
E-scaled confidence and evidence grounding; it carries no flaw table, emits
no planted flaws, and never misrepresents a span.
