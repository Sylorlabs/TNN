# ARM R — Compression cuts (MDL/DP): build specification

**Status:** build spec, frozen for the 1x battery. Any change follows prereg §13.

## 0. Coordinator corrections acknowledged

1. **First correction (2026-09-21):** the originally dispatched definition
   ("Deliberate boundary revision") was wrong and is **VOID**. The
   deliberate-revision implementation that existed in `cl/arm.zag` (~31 KB)
   has been **deleted**; nothing from it survives in this build.
2. **Second correction (2026-09-21):** do not build or score against the
   paraphrase in the coordinator's earlier message(s). The authoritative
   sources, in order, are:
   1. the brief file `units/arms/briefs/R.json`;
   2. the verbatim frozen §3 row (byte-verified against frozen commit
      `b0b9140c0eda` via the GitHub API);
   3. nothing else.
   
   Verified programmatically on 2026-09-21: the brief's `mechanism` and
   `kill` fields are **byte-identical** to the verbatim row. No conflict
   exists, so this build proceeds per the brief. If (1) and (2) ever
   disagree in future, work **BLOCKS** and the conflict is reported — no
   building on paraphrase.

Verbatim frozen §3 row (recorded here for audit, not as a second source):

> R — Compression cuts (MDL/DP) | CUT | Mechanism: Chunks are compression
> units: cut where description length is minimized (suffix-array/LCP + DP
> over cost). | Binding kill criterion: Boundary F1 (vs whitespace/
> punctuation joints AND vs arm O's taught spans, separately) does not beat
> the fixed-64-byte baseline by ≥10 points on both corpora; OR held-out
> recall (M1) with R-cuts does not beat the 64-byte baseline. **Note (C9):**
> R makes compression *dominant* — it is the anti-R31 control on the
> compression axis, not R31's continuation (R31 deliberately down-weighted
> compression).

## 1. Frozen design parameters

| Parameter | Value | Basis |
|---|---|---|
| `L` (max repeat length) | 64 | design doc "e.g. 64", adopted literally as the frozen value |
| `ref_cost` (dictionary reference cost) | 2 bytes | design doc "e.g. 2 bytes", adopted literally |
| Tie-break | longer chunk wins; then unique | see below |
| Dictionary | maximal repeats occurring ≥2 times, capped at `L`, from suffix array (prefix-doubling, deterministic) + LCP (Kasai) | brief + design §1 |
| DP | `dp[n]=0`; `dp[i]=min_{l∈[1,min(L,n-i)]} cost(i,l)+dp[i+l]` | design §1 |
| `cost(i,l)` | `ref_cost` if substring `s[i..i+l]` occurs ≥2 times in the dictionary corpus, else `l` | design §1, literal |

**Dictionary-repeat test (exact, no approximation).** Let
`maxlen[i] = min(L, longest repeat starting at position i)`, computed from
the SA/LCP adjacency maximum (for rank `r` of suffix `i`,
`longest(i) = max(LCPsa[r], LCPsa[r+1])` — exact: any other suffix's LCP
with `i` is bounded by an SA-neighbor's). Then `s[i..i+l]` (`l ≤ L`)
occurs ≥2 times ⟺ `l ≤ maxlen[i]`, because every repeat is a substring of
a maximal repeat. So `cost(i,l) = ref_cost ⟺ l ≤ maxlen[i]`.

**Tie-break (total deterministic order).** At each DP position, minimize
`(total_cost, −chunk_length)` lexicographically: iterate `l` from
`min(L,n-i)` down to 1, replace the best on **strict** improvement
(`tot < best`), so the largest `l` wins cost ties ("prefer the longer
chunk"). The brief's "then the earlier cut" clause is **vacuous** under
this total order — each position's choice is unique, so no residual tie
exists to break. Recorded here literally rather than reinterpreted.

**DP cost bound (u32 safety).** `dp[i] ≤ 2·(n−i)`: every chunk costs at
most `max(ref_cost, l) ≤ max(2, L)`… more tightly, `cost(i,l) ≤ max(2,l)`
and a segmentation into 1-byte chunks costs ≤ 2 per byte only where
`maxlen ≥ 1`; worst case is 2/byte. For `n ≤ 9,600,000`,
`dp[0] ≤ 19,200,000 < 2^32`. DP costs are stored u32, chunked; no
saturation possible. (Proven, not assumed.)

**Unit IDs.** `unit_id = (corpus_id << 24) | chunk_index`.
`chunk_index < n ≤ 9.6M < 2^24`. Corpus IDs 1–8 per the interface;
`9` = C′ (M7 modified prose, this arm's documented extension).

**Chunk length bound.** `l ≤ L = 64`, so every R chunk is ≤ 64 bytes.
Patch buffers (64 B) and the 64-byte recall scratch are therefore exact.

## 2. Architecture

- **One binary:** `cl/arm.zag` → `<workdir>/r_bin`, built with the frozen
  toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
  Invocation per ARM_INTERFACE.md §2:
  `r_bin <mode> <corpus-root> [outdir] [perturbation]`.
- **Segmentation engine** (pure Zag, zero RNG):
  - Suffix array: prefix-doubling with LSD radix sort (two counting-sort
    passes per iteration), O(n log n), pure integer arithmetic. Arrays are
    u32 pairs of slices, each ≤ 2^25 bytes (`se = (n+2)/2` entries per
    slice).
  - LCP: Kasai folded directly into the `maxlen` u8 array — no separate
    LCP array is stored. For rank `r>0` of suffix `p`, `h = lcp(p,
    SA[r−1])`; `hh=min(h,L)` updates `maxlen[p]` and `maxlen[SA[r−1]]`.
    This yields exactly `max(LCPsa[r], LCPsa[r+1])` per position.
  - DP: backward pass, chunked u32 costs + u8 backpointers, O(n·L).
  - Segmentation scratch is freed after ingest in every mode (never part
    of the M8 store image).
- **Store:** slot table (`ids/offs/lens/corps/flags/shifts/pidx` u32 arrays
  + insertion-order queue), multiplicative-hash placement + linear probe —
  a pure function of unit ID (order-independent; the M8 `freelist`
  perturbation legitimately shows no change, documented per A11).
- **ID-arm declaration: R IS an ID arm** (ARM_INTERFACE.md §9). `recall`
  takes a unit ID and resolves it through the persistent ID→storage slot
  table; the table is genuinely consulted (the M1 swap probe patches it and
  observes changed bytes — no side channel). Consequences: the M1 swap
  probe is implemented (schedule per the provisional A15 text, results
  marked **PROVISIONAL-PENDING-FREEZE**), and M7 runs the full ID-arm rig.
- **Audit economics** (design §4, declared exemption): the chunk table is
  DERIVED from `(corpus sha256, L, ref_cost, tie-break)` — reproducible,
  not a memory operation. Per-chunk ADD ledger entries are NOT written
  (~10^5–10^6 chunks would drown the ledger and trip the C4
  ledger-capacity confounder). Corpus ingest is logged as `SCAN_COMMIT`
  batches (opcode 0x07; `slot=-1`, `b1`=first offset, `b3`=total bytes,
  `b4`=corpus, `b5`/`d1`=first unit id, `d2`=count; deterministic replay
  from the policy inputs). The policy itself is audited on stdout per mode:
  `POLICY,corpus,sha256,L,ref_cost,tiebreak,nchunks,spot1/spot2/spot3`
  (spot hashes = sha256 of first/middle/last chunk bytes). Individual
  deliberate ops outside derivation (M3/M4/M5 churn: ingest/kill/weaken/
  evict/pin/promote/revise/defects) keep per-op ledger entries — those are
  genuine memory ops, not derivation.
- **Determinism:** no clocks, no RNG, no addresses or allocation order in
  any stored/compared artifact. Perturbation pads (`frag`, `aslr`) use raw
  `nio_alloc`, bypassing the arm's logged alloc trace.

## 3. Mode semantics (R-specific; interface mode table otherwise literal)

- `m1-1x-prose` / `m1-1x-code`: segment with the corpus's own dictionary;
  ingest all chunks (SCAN_COMMIT batches of 4096); recall every unit via
  the ID→slot path; byte-diff. Swap probe: 64 `TRAINER_SWAP_PROBE`
  operations — after every `ceil(nunits/64)` recalls, patch the target's
  slot record to the next live slot's span (wrapping), log the probe,
  recall, require the remapped bytes (or a loud failure); restore the
  record immediately. `m1_id_probe="PASS"` iff 64/64 probes return remapped
  content. **PROVISIONAL-PENDING-FREEZE** (A15).
- `m2-t1-prose`, `m2-t1-code`, `m2-t2-prose`, `m2-t2-code`, `m2-t3-1x`:
  segment the tier file; episode loop to the literal criterion
  (content ≥99.5% AND boundary ≥95%, 3 consecutive); episode-0 probe on the
  empty store is the leak check. M9 descriptors on t1 tiers. Expected ETC=1
  (deterministic store).
- `m3-1x`: V = every k-th unit (`k=total/1000`) over prose+code unit index
  space; `trainer_mark_valuable` → pin; capacity `C_M3=4000`; 3000 fresh
  64B ingests (protocol units, corpus 8, per-unit ADD entries), 3000 kills,
  50 weakens (every 20th valuable; R's weaken policy = management
  annotation, audited, never touches bytes — same as the validator),
  4000 at-capacity ingests with FIFO-oldest-unpinned eviction or loud
  audited refusal. Freeze distinguisher exactly per §10.
- `m4-1x-prose` / `m4-1x-code`: 200 units at `i*nunits/200`; 100 boundary
  defects (cycling deltas) + 100 content defects (prose: every-7th-byte
  XOR; code: fixed rename map); ≤20 revision episodes; REVISED requires
  same ID + REVISE entry + bytes == source (kill+re-add does not count).
- `m5-1x`: prose ingest (SCAN_COMMIT batches) + 500 fresh ingests + 500
  kills; `learned` = units with byte-exact recall at trial end;
  `ledger.bin` written to CWD. Audit bar: ≤10 entries/KB (the §2 exemption
  is what makes this attainable).
- `m5-baseline`: same empty store (sized via one segmentation, then
  scratch freed), fully touched, spin for the RSS sampler.
- `m6-p2c-1x` / `m6-c2p-1x`: train on the t1 tier to the M2 criterion;
  **freeze the dictionary derived from the train tier** (R's learned
  segmentation policy); apply the frozen dictionary to the transfer
  corpus via a suffix automaton over the reversed train substrings
  (`maxlen_frozen[i]` = max `l ≤ L` with ≥1 train occurrence — the
  dictionary semantics; the earlier ≥2 SA-narrowing was a bug, corrected
  2026-09-21 (maxlen arrays matched on fixtures; complete cut-array
  equivalence not yet proven);
  ingest allowed, policy frozen; M1 recall + boundary and
  100-defect revision on the transfer corpus; tax per §10. **S3 evidence:**
  boundary-F1 transfer gap (frozen-dictionary F1 vs fresh-dictionary F1
  on the transfer corpus) — the domain-generality measure. (Design-doc
  parenthetical "(L, ref_cost) frozen on prose" read against the frozen
  §10 M6 procedure "freeze the segmentation/vocabulary policy": the
  dictionary is R's learned policy and is what freezes. Noted as a
  literal-reading decision.)
- `m7-1x` (ID arm): round 0: ingest C (prose). Round 1: re-ingest C —
  identical segmentation → identical IDs → revive path (dedup proof).
  Round 2: C′ = C with every-100th-R-chunk first-byte XOR 0xFF, fresh
  segmentation, corpus_id=9, new IDs (declared, audited). Lookups
  `(l*37)%nunits` split 1666/1667/1667 across rounds (the harness
  validator's schedule — **provisional** per A7/A8, needs Micah's freeze).
  `hit` = table-resolved lookups / 5000; `reuse` = (ingest ops + lookups) /
  distinct live IDs (the only non-absurd reading: lookups-only would fail
  every arm with nunits > 1667); `dedup` = 1 − distinct_stored(rounds 1–2)
  / ingested(rounds 1–2). Bars: ≥90% / ≥1.5 / ≥0.4.
- `m8-1x`: M1 (prose+code) + M3 op sequence on one instance; artifacts per
  §7 (`store_hashes.txt`, `store_chain.txt`, `ledger.bin`,
  `ledger_chain.txt`, `alloc_trace.txt`, stdout/stderr). Segmentation
  scratch is freed before imaging; the store image covers only the slot
  region + insertion queue.
- `x-cuts-prose` / `x-cuts-code` (R-specific evidence modes, not in the
  interface table): segment and write `./cuts_<corpus>.bin` (u32 LE
  boundaries) + `POLICY` line. Used for boundary-F1 scoring.
- `x-heldout-prose` / `x-heldout-code` (R-specific evidence modes):
  frozen-dictionary held-out M1 on the t1 tiers (see §5).

## 4. Binding-kill evaluation procedure

### 4a. Boundary F1 (main disjunct)

- **Reference set J** (whitespace/punctuation joints): position `i`
  (`1 ≤ i ≤ n−1`) is a joint ⟺ `is_wp(data[i−1]) ≠ is_wp(data[i])`,
  where `is_wp(b)` ⟺ `b ∈ {0x09,0x0A,0x0B,0x0C,0x0D,0x20}` (ASCII
  whitespace) ∪ `{0x21–0x2F, 0x3A–0x40, 0x5B–0x60, 0x7B–0x7E}` (ASCII
  punctuation). File endpoints 0 and `n` are excluded (every segmentation
  shares them).
- **Reference set T** (arm O's taught spans): boundary positions =
  `{start, end}` of each taught span, interior only (0, n excluded).
  **STATUS 2026-09-21: BLOCKED** — `units/arms/O/` contains only `cl/` and
  `substrate/`; no taught-span artifact exists. The comparison procedure
  is frozen (same F1 code path as J); the numbers await arm O's artifact.
- **F1:** exact position match (tolerance 0).
  `P=|pred∩ref|/|pred|`, `R=|pred∩ref|/|ref|`,
  `F1=2PR/(P+R)` (0 if `P+R=0`). Percentage points, one decimal.
- **Baseline:** fixed-64B cuts `{64,128,…} ∩ [1,n−1]`, same F1.
- **R's cuts for this clause:** per-corpus dictionary (the mechanism
  operating normally — the clause does not mention freezing).
- **Kill rule (literal):** FIRE iff
  `(F1J_R − F1J_64 < 10.0 on prose) OR (… on code) OR`
  `(F1T_R − F1T_64 < 10.0 on prose) OR (… on code) OR`
  (held-out M1 disjunct, §5).

### 4b. Held-out recall M1 (second disjunct)

- **Operationalization:** train split = `corpus[0:T1_offset)` with
  `T1_offset` from `MANIFEST.json` (`prose_offset=4880448`,
  `code_offset=8563806`). Dictionary frozen on the train split; the t1
  tier (`t1_prose.bin` / `t1_code.bin`) segmented with the frozen
  dictionary (SA-interval walk); M1 ingest + full recall on the tier.
  Metric: M1 content-recall %. Baseline: 64-byte M1 on the same tiers
  (100.0/100.0 by the validator's demonstrated mechanism — 64B chunking
  is corpus-agnostic and byte-exact).
- **Verdict rule:** PASS iff `R_recall ≥ baseline_recall` (see A18).

## 5. Reported predictions (design §2; informational, not kill bars)

- **S1:** the F1 gaps (§4a) + per-corpus boundary distributions
  (chunk-length histograms; code boundaries should cluster at
  identifier/keyword edges, prose at word/phrase edges).
- **W1:** fraction of the 100 strongest-signal boundary positions
  (ranked by `maxlen`) falling in boilerplate regions (code: top-of-file
  license/comment block; prose: PG header). Informational.
- **W2:** % of cuts strictly inside whitespace-delimited words on prose
  (prediction: ≥5%).
- **W3:** sensitivity calibration at `L=32` and `L=128` (F1 recomputed;
  calibration only, never headline).
- **M9** shapes on t1 tiers; **M6** transfer tax + S3 F1 gap.

## 6. Exactness notes

- SA-interval narrowing walk (frozen dictionary): for transfer position
  `i`, maintain the train-SA interval of suffixes with prefix
  `buf[i..i+l]`; extend `l` while `|interval| ≥ 2` and `l < L`. Exhausted
  train suffixes sort as −1 (shorter-is-smaller). Result
  `maxlen_frozen[i]` = max `l` with ≥2 train occurrences — exact by
  construction.
- No `slice as *u8` casts; no slice `==`; `_zag_arg` never freed;
  `_zag_strcmp==1` means equal; large-struct array fields aliased to
  locals before indexing; no indexed slice exceeds 2^25 bytes
  (segmentation arrays are slice-pairs; the corpus buffer is 9.6 MB).

## 7. Open items / ambiguities (logged literally, never reinterpreted)

- **A15 (provisional):** M1 swap-probe schedule/procedure needs Micah's
  freeze. Implemented per the proposed text; `m1_id_probe` marked
  PROVISIONAL-PENDING-FREEZE.
- **A17:** M8 "full M1+M3 runs" reading — implemented as the validator
  does (M1 prose+code + M3 sequence, one instance); the determinism of
  the op sequence is what the gate compares.
- **A7/A8 (provisional):** M7 C′ edit (first-byte XOR 0xFF on every
  100th unit) and lookup schedule (`(l*37)%nunits`, 1666/1667/1667) are
  the harness validator's values; R needs Micah's freeze before its M7
  counts as final. `reuse` formula documented in §3.
- **A18 (new, R-specific):** the kill clause's "held-out recall (M1)
  with R-cuts does not beat the 64-byte baseline" is operationally
  underdetermined. M1 content recall is segmentation-invariant for a
  correct store (both R and 64B score 100.0 on any tier), so a strict `>`
  reading would fire the kill vacuously regardless of R's quality. R is
  evaluated under the intent-preserving `≥` reading (the clause guards
  against R breaking recall); the strict reading and its consequence are
  disclosed here for the coordinator.
- **O-T (new, blocking):** arm O's taught-span artifact does not exist
  yet. The F1-vs-taught-spans leg of the kill **cannot be evaluated**
  until arm O publishes taught spans in a documented format. R's verdict
  on the F1 clause is therefore conditional on the J leg; the T leg is
  reported as BLOCKED-PENDING-O.
- **Tie-break "earlier cut":** vacuous under the total order (§1).
- **C9:** R is the anti-R31 control on the compression axis —
  compression is deliberately *dominant* here (dictionary reference cost
  2 bytes vs literal bytes; every repeat earns the reference). R31
  down-weighted compression; R does the opposite by design.
