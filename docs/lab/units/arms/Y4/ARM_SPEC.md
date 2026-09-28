# Y4 — Question-driven (lazy) chunks: ARM SPEC

**Arm:** Y4 — Question-driven (lazy) cuts
**Frozen brief:** `units/arms/briefs/Y4.json`
**Frozen taxonomy:** `units/ALPHABET_Y-Z.md` §Y4
**Authority order:** brief file, then frozen row. They match exactly (verified 2026-09-21).
**Implementation:** `cl/arm.zag` (pure Zag, Linux x86_64, frozen toolchain
`znc_linux_x86_64_abed8aa1`), single binary, `argv[1]` selects mode.

## 1. Mechanism (as built)

**Ingest = candidate marking only.** `y_ingest_span` scans the raw stream once
and emits *candidate cut offsets* into the audit ledger (`CANDIDATE_CUT`,
opcode 32). No chunks are formed at ingest; no `ADD` entries exist before a
question. The candidate arrays live in the arm's heap (`cand`, per corpus) and
are part of the M8 store image.

**Fixed preregistered detector set** (per §Y4; changing it is a prereg
amendment):
1. `DET_SENT` — sentence punctuation `.!?` (cut after the mark)
2. `DET_BLANK` — blank lines (cut at the start of the next line)
3. `DET_BRACE` — brace/bracket characters `{}[]` (cut after the char)
4. `DET_INDENT` — indentation-width shifts at line starts (cut at the shifted
   line's start)

Scan order is fixed: per byte, indent-shift check first, then newline/blank,
then punctuation, then braces. The first detector to fire at an offset wins;
a **16-byte minimum separation** is enforced between consecutive candidates
(first event wins). A span start is treated as a stream start (indent baseline
resets) — documented, deterministic.

**The question commits the segmentation.** `y_question(corpus, qtype, qoff,
qlen)` is a pure function of (question, candidates):
- `Q_FULL`: selects all candidate-delimited chunks of the corpus.
- `Q_SPAN`: selects exactly the chunks overlapping `[qoff, qoff+qlen)`.
- Ties broken by ledger order (candidate index order) — the only tie-break.

`QUESTION_ASKED` (opcode 33) is logged **before** any materialization, so the
ledger always reads candidates → question → materializations (verified by
`audit_ledger.py`: 0 ordering issues on the M5 ledger). Selected spans are
materialized with stable IDs and become first-class memory objects
(kill/pin/promote/weaken/revise/evict all apply).

**Stable IDs:** `id = (corpus << 24) | chunk_index`. Persistent for the
instance lifetime; slot placement is a pure function of the ID (deterministic
multiplicative hash + linear probe), so heap/allocator perturbations cannot
move a chunk. Y4 is therefore an **ID arm**.

**Recall:** `y_recall` serves the exact source bytes for the chunk's committed
span (with any recorded shift/patch applied, then `revise` restores). Recall
increments a per-chunk recall counter used by the laziness leg.

## 2. Lazy-kill semantics (loud, never silent)

- `y_kill(id)`: if the chunk is materialized, it is tombstoned (audited
  `KILL`); a killed chunk can never be re-materialized (`ADD` after `KILL`
  for one ID is refused — audited `REFUSE`).
- If the chunk was **never materialized**, the kill is applied to the
  *candidate span* itself (killed-bitmap): no future question can materialize
  it. Audited `KILL` with a lazy flag. This is how the M3 fresh-kill phase
  works — no chunk formation is ever forced by a kill.
- Tombstone GC policy: tombstones are never collected (no silent GC).

## 3. Ledger opcodes

Frozen namespace 1..18 plus Y4 arm-defined 32/33. Entry layout is 16 words
(op, slot, rc, b1..b5, a1..a5, stage=1, d1, d2); no clock word — the implicit
clock is entry position, which is why replay is byte-identical.

| opcode | meaning | key fields |
|---|---|---|
| 32 `CANDIDATE_CUT` | ingest candidate cut | b1=offset, b4=corpus, b5=cand_idx, d1=detector |
| 33 `QUESTION_ASKED` | question committed | b1=qoff, b3=qlen, b4=corpus, b5=qseq, d1=qtype, d2=new materializations |
| 7 `SCAN` | ingest pass summary | b3=bytes, b4=corpus, d2=new candidates |
| 1 `ADD` | chunk materialized | b5=chunk id, d1=chunk index |
| 2 `KILL` / 3 `PIN` / 4 `WEAKEN` / 9 `EVICT` / 6 `REVISE` | management | b5=id |
| 8 `REFUSE` | refused op (kill-after-kill, add-after-kill, materialize-killed-span) | d1=reason |
| 16/17/18 | boundary/content defect, mark-valuable (trial ops) | — |

Management-audit mapping for M3 liveness: `CANDIDATE_CUT` and `SCAN` count as
deliberative management entries (the ingest pass is the arm's only
deliberative act), alongside ADD/KILL/PIN/WEAKEN/EVICT/REFUSE.

## 4. Weakening, defects, revision

- **Weaken** is a management annotation (flag bit), audited; it never alters
  stored bytes. `weaken_handled` counts successful annotations.
- **Boundary defect** shifts the chunk's recalled start offset by ±delta
  (cyclic ±1,±2,±4,±8,±16,±32 in M4); **content defect** installs a recorded
  byte-patch (prose: every-7th-byte XOR; code: identifier renames
  sqlite3→sqlite4 etc.).
- **Revise** clears shift+patch, restoring exact source bytes; audited with
  old/new offsets. Revision of an un-defected chunk is a no-op (returns 0).

## 5. Trial modes (all in the one binary)

m1-1x-prose, m1-1x-code, m2-t1-prose, m2-t1-code, m2-t2-prose, m2-t2-code,
m2-t3-1x (M9 folded into the t1 legs), m3-1x, m4-1x-prose, m4-1x-code,
m5-1x, m5-baseline, m6-p2c-1x, m6-c2p-1x, m7-1x, y4-lazy-1x, y4-cmp-1x,
m8-1x (outdir + perturbation args).

- **M2:** each episode = ingest pass (idempotent after episode 1: 0 new
  candidates) + FULL-question probe; convergence = recall ≥99.5 and boundary
  ≥95.0 three episodes running. Episode 0 probes the un-ingested store (0
  candidates → 0 chunks → 0.0 recall), demonstrating that without ingest there
  is nothing to recall.
- **M3:** 1000 valuable chunks (every k-th across prose+code), marked via
  exact-span questions + pin; 3000 fresh candidate-ingests (no chunks formed);
  3000 fresh lazy kills; 50 weaken probes; 4000 more fresh ingests at
  capacity; V survival by byte-exact recall; fresh-sample recall of the last
  500 fresh 64B units via SPAN questions.
- **M5:** mini-pressure (500 fresh candidate-ingests + 500 fresh lazy kills),
  then the FULL question; reports units/source bytes, slot-table bytes
  (cap×32 + insertion-queue×4), ledger bytes/entries, corpus buffer bytes.
- **M6:** tier-1 training to the M2 criterion, 100 boundary defects + 1 revise
  each, then transfer to the other domain. Policy = code-frozen detectors, so
  "transfer tax" measures candidate reuse across domains.
- **M7 (ID-arm rig, PROVISIONAL):** 5000-lookup schedule `(l*37)%n` over three
  rounds; round 0 ingests, round 1 re-ingests (0 new candidates), round 2
  applies the C′ edit as content patches on every 100th committed chunk ID
  (re-cutting on a 1-byte edit would violate committed-segmentation
  semantics). Reports hit rate, reuse (lookups/distinct IDs, hundredths),
  dedup (1 − n/2n = 50 hundredths, derived). The swap probe and the C′
  procedure are **proposed, pending Micah's A7/A8 freeze** (AMBIGUITIES.md) —
  not claimed as frozen.
- **y4-lazy-1x (laziness kill-bar leg):** preregistered question stream on
  novel tier t1_prose — Q1 FULL, Q2 SPAN[10%,30%), Q3 SPAN[10%,30%),
  Q4 SPAN[55%,75%), Q5 FULL. Reports materializations, rematerializations,
  and the never-recalled-twice fraction (tenths). KILL iff >30%.
- **y4-cmp-1x (arm-D comparison leg):** M1 recall + total ledger cost
  (candidates + materializations) per corpus for Y4; arm-D fields are null
  until D reports. Decision procedure: KILL iff cost_y4 ≤ cost_d AND
  recall_y4 < recall_d − 5.0. Never invent D's numbers.
- **M8:** M1 prose+code + M3 op sequence in one instance; artifacts
  `store_hashes.txt` (per-1MB-chunk SHA-256 of the full persistent store
  image), `store_chain.txt`, `ledger.bin`, `ledger_chain.txt`,
  `alloc_trace.txt`. Five perturbations × two runs, byte-identical required.
  `frag` = deterministic heap pre-fragmentation; `aslr` = 1.2MB base pad;
  `starve`/`freelist` = accepted documented no-ops (placement is ID-derived,
  no clock/entropy in any decision path).

## 6. Y4-vs-D slotting procedure (frozen kill bar, D pending)

When arm D reports its M1 recall (tenths) and total ledger cost per corpus:
1. Take Y4's `y4_cmp_recall_tenths_{prose,code}` and `y4_cmp_ledger_cost_*`
   from `y4-cmp-1x` (this scorecard).
2. Per corpus: if `cost_y4 ≤ cost_d` and `recall_y4 < recall_d − 50` (tenths),
   the accuracy kill bar fires → Y4 KILLED.
3. Independently: if `y4_lazy.never_twice > 300` (tenths) → Y4 KILLED.
4. Otherwise → Y4 PASS (contingent on M8 byte-identity, which gates any PASS).

## 7. Deviations and build notes

- The frozen harness `run_battery.sh`/`run_metric.sh`/`m8_gate.sh` were used
  unmodified. `scorecard_assemble.py` hardcodes `"arm":"b64"` and non-ID
  M7/M1 assumptions, so `scorecard_assemble_y4.py` (mechanical adaptation,
  same raw fields) produced the scorecard; the frozen file is untouched.
- Two bugs found and fixed during build, both documented in BUILD_LOG.md:
  (a) `y_question` originally logged QUESTION_ASKED after materializing —
  fixed to log before (ledger now reads question → ADDs); (b) the slot-ID
  table was not initialized to the EMPTY sentinel — fixed (allocator luck
  had hidden it).
- znc codegen constraints hit: `_zag_malloc` sized for 16-byte slice fields
  (ZNC-2026-09-21-003); no slice `==` for array selection; byte images built
  by word→byte decomposition (ZNC-2026-09-21-002); `return;` in void fns.
- Battery workdir under `~/workspace/y4runs` (never `/tmp`); corpus files
  never committed; binaries/ledgers never committed.
