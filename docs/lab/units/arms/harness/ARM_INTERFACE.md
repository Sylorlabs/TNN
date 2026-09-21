# ARM INTERFACE — TNN Track A (53-arm representation bake-off)

**Status: FROZEN.** This is the build contract every arm crew implements against.
Prereg: `PREREG_FREEZE.md` (commit `b0b9140c0eda`, branch `tnn-native-lab`),
§5 (metrics M1–M9), §6 (M8 + scale legs), §9 (confounder register), §0 RULE-1..12.
Metric glossary: `METRICS.md`. Arm designs: `ALPHABET_*.md`.

Any change to this file after arm crews start building follows the prereg §13
amendment procedure (dated amendment, Micah's re-approval). Ambiguities found
while implementing the literal prereg reading are listed in
`AMBIGUITIES.md` — never silently reinterpreted.

---

## 1. Trial directory layout (mandatory)

```
<arm-id>/
  cl/            # Zag sources. Entry point: cl/arm.zag with fn main()i32
  substrate/     # verbatim copies: R33_NATIVE_SHA256_V2.zag + R33_NATIVE_IO_V1.zag
```

- From `cl/`, import the substrate as `@import("../substrate/R33_NATIVE_SHA256_V2.zag")`
  (it pulls `R33_NATIVE_IO_V1.zag` itself; `@import` paths are relative to the
  importing file). `@import` must be a BARE directive, not `//`-commented.
- **One binary per arm.** Build: `znc <arm-id>/cl/arm.zag -o <workdir>/<arm-id>_bin`
  with the frozen toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
  Never commit binaries, `.zagd` files, or `.zag-cache/`.
- Pure Zag for all arm cognition. ZERO randomness in any AI decision path.
  Byte-identical reruns or disqualification (M8).
- Arm IDs (53): `a`, `b8`, `b16`, `b64`, `cw`, `cp`, `d`, `dt`, `dr`, `e`, `fs`, `fb`,
  `g1`, `g2`, `h1`, `h2`, `i1`, `i2`, `j1`, `j2`, `k1`, `k2`, `k3`, `l1`, `l2`, `m`,
  `m2`, `n`, `o`, `p`, `q`, `r`, `r2`, `s`, `t`, `u`, `v`, `w`, `x`,
  `y1`–`y6`, `z1`–`z8`. (Lowercase; the prereg's `B-64` = `b64`, etc.)
  The memorizer negative control (M6) is `memctrl` (control, not one of the 53).

## 2. Binary invocation contract

```
<arm>_bin <mode> <corpus-root> [outdir] [perturbation]
```

- `argv[1]` = mode (Table §3). Unknown mode → `unknown mode` message, exit non-zero.
- `argv[2]` = corpus root directory (see §4). Missing/unreadable corpus → the
  mode prints a `FATAL` line; the runner fails the leg (trial invalid, never 0).
- `argv[3]` = artifact outdir — only for `m8-*` modes, required there.
- `argv[4]` = perturbation selector — **only meaningful for `m8-*` modes**,
  required there (the validator's binary errors if it is empty; the runner
  always supplies it, `clean` for the unperturbed run). One of: `clean`,
  `frag`, `aslr`, `starve`, `freelist`. Every arm implements all five (§7).
- **Fresh process per mode = fresh arm instance per metric** (prereg R-i / M-44:
  no cross-metric state leakage, at the cost of 9× compute).
- stdout: human-readable `TAG,value,...` lines (free-form, deterministic) PLUS one
  line `METRIC_JSON <single-line JSON>` per mode carrying the machine-readable
  fragment (§8). stderr: diagnostics only (captured by the harness, compared by M8).
- Exit 0 = trial completed (even if the arm scores badly — bad scores are data).
  Exit non-zero = trial invalid (harness marks the cell failed/invalid, never 0).
- `_zag_arg(n)` returns a NON-OWNED pointer: never `nio_free` it.
  `_zag_strcmp(a,b)` returns **1** on equality. Zag `==` on `[]u8` slices is NOT
  content identity — use integer selectors / `nio_equal`. No slice may exceed
  2^25 bytes — chunk large buffers (build note, equivalence by byte-identical rerun).

## 3. Mode table (trial modes; scale suffix `-1x` now, `-10x` after 1x bars pass)

| Mode | Trial | Emits (JSON fragment keys) |
|---|---|---|
| `m1-1x-prose`, `m1-1x-code` | M1 recall on that corpus | m1_recall_tenths, m1_boundary_tenths, m1_units, m1_corpus |
| `m2-t1-prose`, `m2-t1-code`, `m2-t2-prose`, `m2-t2-code`, `m2-t3-1x` | M2 episodes-to-criterion per tier | m2_episodes, m2_censored, m2_ep0_recall_tenths, m2_final_recall_tenths, m2_final_boundary_tenths; t1 modes also m9_shape, m9_takeoff_ep, m9_steepness_tenths, m9_late_gain_tenths |
| `m3-1x` | M3 churn/pressure rig | m3_survival_tenths, m3_fresh_recall_tenths, m3_mgmt_entries, m3_weaken_handled, m3_freeze, m3_valuable |
| `m4-1x-prose`, `m4-1x-code` | M4 revision battery | m4_rev_boundary_tenths, m4_rev_content_tenths, m4_kill_rate_tenths, m4_killsub, m4_episodes |
| `m5-1x` | M5 cost trial (writes `ledger.bin` to CWD) | m5_units_learned, m5_source_bytes_learned, m5_slot_table_bytes, m5_ledger_bytes, m5_ledger_entries, m5_corpus_buffer_bytes |
| `m5-baseline` | empty-store RSS baseline | m5_baseline marker (harness-side RSS) |
| `m6-p2c-1x`, `m6-c2p-1x` | M6 transfer P→C / C→P | rec_tenths, bnd_tenths, rev_tenths, tax_tenths |
| `m7-1x` | M7 cache rig (ID arms) or N/A | m7_hit_rate_tenths / m7_reuse_rate_tenths / m7_dedup_savings_bytes / m7_na_reason + m7_reread_bytes |
| `m8-1x` | M8: M1(prose+code)+M3 sequence, artifact capture | artifacts to outdir (§7) |
| `memctrl-p2c-1x`, `memctrl-c2p-1x` | memorizer control (memctrl binary only) | memctrl_indomain_recall_tenths, memctrl_transfer_recall_tenths, memctrl_drop_tenths |

Mode-name suffixes `-10x` are reserved for the scale leg (same procedures on the
10x corpus; built on demand by the harness, never stored).

## 4. Corpus root layout (built by `build_corpora.py`; files cached in workspace, never committed)

```
<corpus-root>/
  prose.bin        full Shakespeare PG#100        (corpus A, "prose")
  code.bin         full sqlite3.c amalgamation    (corpus B, "code")
  t1_prose.bin     last 10% of prose.bin by fixed byte offset  (T1 novel tier)
  t1_code.bin      last 10% of code.bin  by fixed byte offset  (T1 novel tier)
  t2_prose.bin     KJV Bible PG#10                (T2 third corpus)
  t2_code.bin      CPython Objects/longobject.c   (T2 third corpus)
  t3.bin           synthetic deterministic bytes, xorshift64* seed 0x544E4E3300000033 (T3)
  churn_fresh.bin  448000 deterministic bytes (7000 × 64B fresh units, M3 rig)
  mem_vocab.txt    top-5000 whitespace tokens of the prose train split (memctrl)
  MANIFEST.json    sizes, sha256, T1 split offsets, seeds
```

- T1 split: `offset = floor(len*9/10)`; `t1 = data[offset:]`. Offsets in MANIFEST.json.
- T1 material is "novel": an arm's `m2-*` instance must never have ingested it before
  (fresh process per mode guarantees this; episode-0 ~0 probe is the leak check).
- T3's seeded generator is **environment input**, explicitly allowed by the prereg
  (RULE-3 carve-out: "Deterministic generators with logged fixed seeds are environment
  inputs, not AI decisions"). The arm reads `t3.bin` like any corpus.
- 10x legs: deterministic 10-fold tiling of each 1x file (verbatim repetition,
  `build_10x.py`), built on demand into `corpora/r10/`, never stored in the repo.
  Tile hashes recorded in `corpora/r10/MANIFEST.json`.

## 5. Required internal operations (every arm implements all of these)

These are the arm's deliberate memory ops. The metric modes exercise them; the
audit ledger records them (§6). Names are the interface vocabulary — implement the
semantics in your substrate, keep the names in code comments and docs.

| Op | Semantics |
|---|---|
| `ingest(span)` | Deliberate add of a unit covering `span` = (corpus_id, byte_offset, len). Returns unit ID or loud refusal. |
| `recall(id)` | Return the unit's bytes through the arm's own retrieval path. ID arms: the request carries ONLY the ID; ID→storage resolved live. |
| `kill(id)` | Tombstone the unit. Tombstoned IDs are never reused. |
| `pin(id)` / `promote(id)` | Deliberate "valuable" marking (M3). Arm chooses the mechanism; the marking is logged. |
| `weaken(id)` | Deliberate weaken (M3 probe). Processed or refused per documented policy — never silently ignored. |
| `revise(id)` | Deliberate repair against source through the arm's revision API (M4/M6). Kill+re-add does NOT count as revision — lineage (same ID + REVISE entry) is required. |
| `trainer_defect_boundary(id, delta)` | EXTERNAL trainer op (not an arm decision): shifts the arm's recorded span by `delta`. Logged with trainer opcode. |
| `trainer_defect_content(id, patch)` | EXTERNAL trainer op: records a byte-patch the recall path must apply (simulates a corrupted stored copy). Logged. |
| `trainer_mark_valuable(id)` | EXTERNAL trainer op: designates V membership (M3). The arm chooses pin/promote. |
| `evict(id)` | Arm's own capacity-management eviction (M3 at-capacity phase). Policy declared, audited. Overflow with no policy = loud audited refusal (scored failure, not a crash). |

Loud refusal = `REFUSE` audit entry with a reason code + a recall/revise path that
fails loudly (nonzero rc, logged). Silent wrong-bytes recall = K-R5 instant kill.

## 6. Audit ledger format (fixed by the harness)

16-word entries = 64 bytes, little-endian u32 words:

```
word:  0     1     2     3..7      8..12     13    14    15
field: op    slot  rc    b1..b5    a1..a5    stage d1    d2
byte:  0     4     8     12..28    32..48    52    56    60
```

- `b1`=byte_offset_lo, `b2`=byte_offset_hi, `b3`=length, `b4`=corpus_id, `b5`=unit_id.
- `a1..a5` = op aux (e.g. REVISE: old/new span; DEFECT_CONTENT: patch length).
- `d1`/`d2` = op-specific scalars (documented per opcode below).
- `stage` = 1 (operational) unless the arm defines stages (then documented).
- Corpus IDs: 1=prose 2=code 3=t1_prose 4=t1_code 5=t2_prose 6=t2_code 7=t3 8=churn_fresh.

Frozen opcode namespace (u32):

```
0x01 ADD_UNIT            d1=chunk_index d2=flags
0x02 KILL_UNIT           d1=reason_code
0x03 PIN_UNIT            d1=mark_kind
0x04 WEAKEN_UNIT         d1=probe_seq (0 if not a probe)
0x05 PROMOTE_UNIT        d1=mark_kind
0x06 REVISE_UNIT         d1=old_off_lo d2=new_off_lo
0x07 SCAN_COMMIT         d1=first_unit_id d2=count        (bulk ingest; deterministic replay required)
0x08 REFUSE              d1=reason_code
0x09 EVICT_UNIT          d1=policy_code (1=FIFO-oldest-unpinned)
0x0A SLOT_REUSE          slot=new slot
0x10 TRAINER_DEFECT_BOUNDARY  d1=delta (u32 two's complement)
0x11 TRAINER_DEFECT_CONTENT   d1=patch_len
0x12 TRAINER_MARK_VALUABLE    d1=mark_kind (1=pin)
0x13 TRAINER_SWAP_PROBE       d1=probe_idx d2=remapped_slot
```

Ledger bytes are compared verbatim by M8 — no pointers, no addresses, no wall-clock
in any field, ever.

## 7. M8 determinism-gate contract (fail-closed)

`m8-1x` runs the **M1 (prose+code) + M3 op sequence** on one instance and writes to
`argv[3]` (outdir). (The validator implements M8 as one large-capacity instance
covering both corpora; whether the frozen prereg's "full M1+M3 runs" means this
or separate ordinary M1/M3 instances is an open literal-reading question —
see AMBIGUITIES.md A17. What M8 compares is the determinism of the op sequence,
not the capacity regime.)

- `store_hashes.txt` — one line per ≤2^20 chunk of the raw slot-region bytes:
  `chunk<i> <sha256-hex>` (native `ns_sha256`). The slot region is every
  persistent slot array (for b64: ids/offs/lens/corps/flags/shifts/pidx at
  cap×4 B each plus the insertion-order queue at ins_cap×4 B).
- `store_chain.txt` — `chain <sha256-hex(concat(chunk hashes))>`.
- `ledger.bin` — complete audit ledger bytes (64B entries).
- `ledger_chain.txt` — `chain <sha256-hex(ledger.bin)>` (native).
- `alloc_trace.txt` — arm's allocation log: `A <size>` / `F <size>` lines only
  (order + sizes; addresses normalized out — never logged). Perturbation-induced
  allocations (frag pattern, aslr pad) bypass this log: the trace captures only
  the arm's own allocations, which must be identical across perturbations.
- stdout/stderr are captured by the runner (`stdout.txt`, `stderr.txt`).

Perturbations (`argv[4]`), `clean` default:

- `clean` — nothing.
- `frag` — before init: deterministic heap pre-fragmentation (256 raw allocs,
  sizes `(i*37)%4096+16`, free every 3rd; survivors freed by OS at exit).
  Catches uninitialized-memory reads.
- `aslr` — before init: one raw 1,234,567-byte pad allocation held for the run.
  Catches pointer-identity leaks into stored state.
- `starve` — in-arm no-op; the RUNNER executes this run under an LD_PRELOAD shim
  (built by `m8_gate.sh` into the workdir, never committed): `getrandom`/
  `getentropy` fail, `clock_gettime` returns fixed zeros.
- `freelist` — the arm's free-list initialization order is reversed.
  Catches order-dependent tie-breaking. (An arm whose placement is a pure function
  of ID legitimately shows no change — document it; see AMBIGUITIES.md A11.)

**Gate rule:** `m8_compare.py` SHA-256-hashes every artifact file and compares
across the 5 runs. ANY single differing byte in `store_hashes.txt`,
`store_chain.txt`, `ledger.bin`, `ledger_chain.txt`, `alloc_trace.txt`,
`stdout.txt`, or `stderr.txt` = **FAIL = DISQUALIFIED** (K-DET). Wall-clock, RSS
high-water, and raw addresses are environment, not mind — never compared.

## 8. Scorecard JSON — schema `metrics-v1`

Each mode prints one line: `METRIC_JSON ` + a single-line JSON object:

```json
{"schema":"metrics-v1","arm":"b64","round":"r1","scale":"1x","mode":"m1-prose-1x",
 "fields":{"m1_recall_prose":100.0}}
```

`scorecard_assemble.py` merges a round's fragments into the full row. Full-row keys (as produced by `scorecard_assemble.py`; additions need Micah's
sign-off per M-55):

```
arm, round, scale,
m1{prose{code...}, code{recall, boundary, units}}, m1_id_probe,
m2{t1,t2,t3 × corpus{etc, censored, ep0_recall, final_recall, final_boundary,
    rel_etc_vs_taught (null until the taught baseline exists)}},
m3{survival, fresh_recall, mgmt_entries, weaken_handled, freeze, valuable},
m4{prose,code × {rev_boundary, rev_content, kill_rate, killsub, episodes}},
m5{units_learned, source_bytes, slot_table_bytes, ledger_bytes, ledger_entries,
   corpus_buffer_bytes, rss_delta_bytes, memory_per_source_byte,
   memory_bar_1_5x, audit_entries_per_kb, audit_bar_10_per_kb},
m6{p2c,c2p × {recall, boundary, revision, tax}, memorizer{...}, validity_gate_15pt},
m7{hit_rate, reuse, dedup, na_reason, reread_bytes},
m8{verdict}, m9{t1 × corpus{shape, takeoff_ep, steepness, late_gain}}
```

- Percentages: one decimal (JSON numbers, e.g. `99.7`). Fragment field names
  ending in `_tenths` are historical — the values are already one-decimal
  percentages, not integer tenths. ETC: integers; censored →
  `"50+"` with `"censored":true`. N/A → `null` with reason in `m7_na_reason`.
- `m1_id_probe`: `"PASS"` / `"FAIL (side channel)"` / `"N/A (no ID layer)"`.
  For the validator (non-ID by construction) the harness assigns
  `"N/A (no ID layer)"`; ID arms will emit it from their swap-probe mode.
- `m3_freeze_flag`: `"CLEAR"` / `"FROZEN-UNDER-PRESSURE"` (flag → `m3_survival` scored 0).
- `m4_kill_substitution_flag`: `true` → M4 scored 0.
- `m8_gate`: `"PASS"` / `"FAIL — DISQUALIFIED"` (FAIL → `disqualified:true`,
  all other cells forensics-only).
- `m9_triple`: `[takeoff, steepness, late_gain]`.
- A missing 10x row for an arm that attempted it = `"ATTEMPTED — FAILED"`, never dropped.

## 9. ID-arm definition (drives M1 swap probe + M7 applicability)

**An arm is an ID arm iff its `recall` takes a unit ID and resolves it through a
persistent ID→storage mapping the arm maintains** (table, hash, translation
structure, version chain). Pure arithmetic (`id = f(offset)`, no stored mapping)
= **no ID layer** → M1 swap probe `N/A (no ID layer)`, M7 `N/A (no ID layer)`
(never a penalty; excluded from blowout denominator; informational re-read-bytes
footnote required).

Provisional classification (arm crews confirm/override in their build declaration;
the swap probe itself enforces honest ID declarations):

- Non-ID layer: `a`, `b8`, `b16`, `b64`, `cw`, `cp`, `e`, `x`, `u`, `v`.
  (`v`'s token IDs are a fixed external vocabulary, not an arm-maintained mapping.)
- ID arms: all others (`d`, `dt`, `dr`, `fs`, `fb`, `g1`, `g2`, `h1`, `h2`, `i1`,
  `i2`, `j1`, `j2`, `k1`, `k2`, `k3`, `l1`, `l2`, `m`, `m2`, `n`, `o`, `p`, `q`,
  `r`, `r2`, `s`, `t`, `w`, `y1`–`y6`, `z1`–`z8`) — subject to crew confirmation.

**M1 swap probe (ID arms, mandatory):** N=64 deterministic ID→content remappings
mid-trial. The prereg mandates the probe but not the remap schedule or the
remap function — see AMBIGUITIES.md A15; the procedure below is proposed and
needs Micah's freeze before ID arms build. Proposed: after every
`ceil(nunits/64)` recalls, patch the ID table so the next recall target resolves
to `(slot+1) % nslots`; log `TRAINER_SWAP_PROBE`; issue the recall; the arm must
return the remapped content (PASS — the ID layer is genuinely consulted) or fail
loudly with an audit entry. Returning the ORIGINAL content despite the remap =
side channel → `m1_id_probe = "FAIL (side channel)"` and the M1 cell is scored
0. Restore the mapping after the probe.

## 10. Metric procedures (literal §5 operationalizations the modes implement)

**M1.** Ingest corpus in fixed file order through the arm's own segmentation; recall
every unit via the arm's own retrieval path; byte-diff vs source. Content recall %
(units with returned bytes == source bytes for the claimed span) and boundary
fidelity % (claimed span == ingest-assigned span), recorded separately, never folded.
Whole-file-blob arms pass content and fail boundary by design (M-3).

**M2.** Tiers: T1 (`t1_*.bin`), T2 (`t2_*.bin`), T3 (`t3.bin`). One episode = one full
ingest pass + probe (M1 procedure on the tier material). Episode 0 = probe with NO
ingest — must score ~0 or the trial is INVALID (leak). Criterion: content ≥ 99.5%
AND boundary ≥ 95%, sustained 3 consecutive probes. ETC = index of the first probe
in the first sustained-3 run. Censored at 50 (`50+`, never averaged — medians with
flags; rank by (reached-criterion?, then ETC)). Report ETC per tier × corpus type
+ relative-ETC vs the taught-baseline arm (companion fields; taught baseline TBD by
Track B — until then relative fields are `null`).

**M3.** V = 1,000 units: every k-th unit, k = total_units/1000 over both corpora
(prose units then code units, concatenated index space), indices 0, k, 2k, … —
see AMBIGUITIES.md A1–A3 for the literal-reading basis of this schedule and the
weaken-op timing. `trainer_mark_valuable` each (arm chooses pin/promote). Store
capacity **C_M3 = 4,000 slots, harness-fixed, identical for all arms** (A1). Pressure: steps 1–3,000
ingest 3,000 fresh units (`churn_fresh.bin[0:192000]`, 64B each); steps 3,001–6,000
kill fresh units 0..2,999 (V never targeted); at step 6,000: 50 `weaken` ops on V
units 0,20,…,980; steps 6,001–10,000 ingest 4,000 fresh units
(`churn_fresh.bin[192000:448000]`) at capacity (arm's eviction policy acts, or loud
audited refusal). Then M1-recall on V: survival %. **Freeze distinguisher:**
(1) 500-unit deterministic sample = the LAST 500 ingested fresh units — recall ≥
80% required; (2) audit-liveness: ≥ 1 management entry (ADD/KILL/WEAKEN/EVICT/
PIN/PROMOTE/REFUSE) per 10 churn steps over steps 3,001–10,000; (3) all 50 weaken
ops processed or refused per documented policy (never ignored).
`FROZEN-UNDER-PRESSURE` iff (survival ≥ 90 AND fresh_recall < 80) OR liveness < 1
per 10 steps OR weaken_handled < 50 → M3 scored 0. (Declared, audited, expiring
freeze is legitimate and scored on its own terms — the flag targets undeclared
freezing only.)

**M4.** 200 units/corpus at fixed indices `i * nunits/200` (i = 0..199), logged.
Boundary defects (100): `trainer_defect_boundary` with deltas cycling
`[+1,-1,+2,-2,+4,-4,+8,-8,+16,-16,+32,-32]`. Content defects (100):
`trainer_defect_content`; prose patch = every 7th byte XOR 0xFF; code patch =
identifier rename by the fixed map `{sqlite3→sqlite4, SQLITE→SQLITF, Vdbe→Vdbf,
Mem→Mfm, pBt→pBu}` (all non-overlapping occurrences, left to right). Planted as
external-trainer ops, logged. The arm reconciles against the source through its
own `revise`; 20 revision episodes max (one pass over the 200 units each).
Per unit: REVISED (bytes now match source for the claimed span AND same ID +
REVISE audit entry — kill+re-add does not count), KILLED, UNFIXED. Rates per
class; kill % alongside. KILL-SUBSTITUTION: kill_rate > 50% AND revision below
bar → M4 = 0. Whole-corpus re-ingest to "fix" defects invalidates the run.

**M5.** Full prose ingest (deliberate add path) + 1,000-step mini-pressure (500
fresh ingests from `churn_fresh.bin`, 500 kills of those fresh, deterministic).
L = units learned = deliberate add + byte-exact M1 recall at trial end + survived
mini-pressure. Harness measures: `rss_delta = maxRSS(m5-1x) − maxRSS(m5-baseline)`
via `/proc/<pid>/status` VmHWM polling (harness-measured, never arm self-report;
the lab VM has no GNU `time`). Accounting (literal prereg reading):
`mem_bytes = rss_delta + slot_table_bytes`, where `slot_table_bytes` comes from
the arm's M8 `store_hashes` slot region (for the validator: seven cap×4 B slot
arrays + the ins_cap×4 B insertion queue; arms report their own). The validator's
`m5-baseline` allocates and fully touches the same empty store (and same-sized
ledger) as `m5-1x`, so the delta holds only the variable cost and the literal sum
does not double-count — arms must implement their baseline the same way
(see AMBIGUITIES.md A4/A5, now resolved for the validator's construction).
`m5_mem_per_byte = mem_bytes / source_bytes_learned` (2 decimals, ↓);
`m5_audit_per_kb = ledger_entries / (source_bytes_learned/1024)` (1 decimal, ↓);
`m5_ledger_bytes_per_byte` informational. Bars: ≤ 1.5 B/B; ≤ 10 entries/KB.

**M6.** Train on prose to the M2 criterion (M2 episode loop on T1-prose), freeze the
segmentation/vocabulary policy, then face code (ingest allowed, policy frozen):
M1 recall + boundary on code, M4-compressed revision (100 planted boundary defects)
on code. Mirror C→P. **P→C and C→P are separate columns — never averaged**
(averaging is non-compliant). Bars: transfer recall ≥ 95%, boundary ≥ 90%,
revision ≥ 70%, both directions; champion = smallest transfer tax
(mean(in-domain − transfer) per direction, signed, 1 decimal).
**Negative control (gates the metric):** the `memctrl` memorizer (frozen prose
top-5000-token vocabulary) must show ≥ 15-point transfer-recall drop in at least
one direction, or the transfer task is too easy and the bar rises before real arms
are scored. Corpus hashes committed pre-build (M-30). Transfer tax =
mean(in-domain − transfer) over the three components rec/bnd/rev, per direction,
signed, 1 decimal (METRICS.md:433).

**M7 (ID arms only).** Ingest C (prose); ingest C again (round 1); ingest C′ = C
with deterministic every-100th-unit edits (round 2). The exact edit bytes and
the 5,000-lookup schedule are not frozen by the prereg — the harness validator
implements first-byte XOR 0xFF as the C′ edit and `(l*37) % nunits` lookups split
1666/1667/1667 across the three rounds; **ID-arm crews need Micah to freeze the
C′ edit and the lookup schedule before their M7 runs** (AMBIGUITIES.md A7/A8). Hit % = served-from-ID-mapping / lookups; reuse =
ID references / distinct live IDs (2 decimals); dedup = 1 − distinct stored /
total ingested over rounds 1–2 (2 decimals; round 3 reported, not barred).
Repeated units must resolve to the SAME ID (or declared, audited new-version IDs
linked to the old — silently issuing fresh unrelated IDs for identical content =
dedup 0). Bars: hit ≥ 90%, reuse ≥ 1.5, dedup ≥ 0.4. Non-ID arms: `N/A (no ID
layer)` + informational re-read-bytes footnote (never scored, excluded from
blowout denominator).

**M8.** §7. Hard gate, not a score.

**M9 (informational, bonus).** During `m2-t1-*`, record raw per-episode (r, b)
points — no smoothing. Descriptors: takeoff (first r ≥ 50%), steepness (max
single-episode jump), late gain (r(ETC) − r(takeoff)). Shape class (frozen
cutoffs 40/15/3): "fast-then-flat" iff steepness ≥ 40 AND late gain ≤ 15;
"slow-then-sudden" iff takeoff ≥ 3 AND steepness ≥ 40; "gradual" iff steepness
< 40; else "other". Never counts toward blowout.

## 11. Confounder controls (mandatory harness parts — prereg §9)

C1 per-source-byte comparison column + separate boundary fidelity; never rank on
raw unit counts. C2 fixed identical corpus order for all arms + one reversed-order 1x leg
(informational; M1 drop > 2 pts → ORDER-SENSITIVE flag). The reversed-order leg
is reserved (mode suffix `-rev`) and not yet run for the validator — an arm with
order-independent placement (e.g. b64) expects no drop.
C3 T2/T3 unseen-by-teacher tiers + teacher-touch count from the ledger alongside
M2. C4 ledger capacity fixed per scale leg, identical across arms. Arms size their
ledgers to complete the trial; if a ledger fills mid-trial the run is scored on
completed entries with a `LEDGER-BOUND` flag the arm must emit. (The validator
sizes generously and never fills — its bound logic is dead code under review.) C5 all buffers chunked ≤ 2^25 by
construction. C6 wall-clock never scored; allocator bloat lands in M5. C7 two
defect classes, cycling magnitudes (§10 M4). C8 V fixed by the protocol (the arm
chooses only the marking mechanism). C9 T2 tier + `memctrl` negative control (M6
validity gate). C10 M1 swap probe (ID arms) + M7 same-ID resolution proof.
C11 schedule structure public, unit identities from fixed corpus offsets. C12
censored ETC never averaged. C13 M8 compares each arm against itself only.
C14 M9 cutoffs frozen; raw triples reported. C15 a row per scale leg attempted;
missing 10x = `ATTEMPTED — FAILED`.

## 12. Zag conformance notes (baked into this interface)

- `@import` relative to the importing file; BARE directive only.
- `_zag_arg(n)` NON-OWNED — never `nio_free`.
- `_zag_strcmp(a,b)` returns 1 on equality.
- Slice `==` is not content identity — use `nio_equal` / integer selectors.
- Alias large structs' array fields to locals before indexing
  (`let a:[]u8 = w.*.field;` then `a[i]`).
- No slice > 2^25 bytes may be indexed — chunk large buffers.
- `st_snap` takes 5 out-pointers; `st_add` takes an out-slot `*i32`;
  the check helper is `cl_check`.
- The znc hot-path miscompile history (ZNC-2026-09-19-001) is why M8's
  adversarial battery exists — deterministic code must not depend on
  uninitialized memory, addresses, clocks, or init order.

---

*End of ARM_INTERFACE.md — FROZEN. Amendments per prereg §13 only.*
