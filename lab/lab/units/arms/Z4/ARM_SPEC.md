# Z4 — Dialect (per-interlocutor) IDs — ARM_SPEC.md

Status: DRAFT for implementation. PROVISIONAL sections are marked; they are literal
readings adopted to make the frozen bars executable, not amendments. Nothing in this
spec reinterprets the frozen kill criteria (brief Z4.json + verbatim §3 row).

## 1. Identity

- Z4, IDENT family. Mechanism: per-speaker lexicons namespaced by speaker tag;
  TRANSLATE op; `common`-namespace governance. Phase 4 hook.
- Binding kill (verbatim): "Per-speaker lexicons do not converge ≥30% faster than a
  shared lexicon — namespacing buys nothing; OR >40% of chunks duplicated across
  namespaces (no real divergence — overhead without content). Conditional on Phase 4
  working."

## 2. Speaker tags (namespaces) — FROZEN for this build

| tag | namespace id | material |
|-----|--------------|----------|
| common | 0 | preregistered shared chunks (governance, §5) |
| S1 (prose speaker) | 1 | prose.bin, t1/t2_prose.bin, t3.bin |
| S2 (code speaker) | 2 | code.bin, t1/t2_code.bin |
| S3 (stranger) | 3 | churn_fresh.bin |

Tags are explicit Phase 4 input metadata: every ingest records which speaker tag was
declared. The arm does NOT infer speakers; a corpus file arrives with its tag.

## 3. ID model

- ID = (namespace : u32, seq : u32). seq is per-namespace, 1-based, strictly
  increasing, never reused (refused mints consume a seq without materializing it).
- Content dedup: ingest(ns, bytes) is idempotent — the same (ns, bytes) always
  resolves to the same (ns, seq). Implemented via a content index keyed by
  (ns, FNV-1a-32(bytes)); FNV is a non-crypto index hash only; correctness under
  hash collision comes from byte-compare verification, never from hash strength.
- Same bytes under different speakers get DIFFERENT ids: (1,k) ≠ (2,j). The alphabet
  entry is followed literally: "the same raw bytes may be cut differently for
  different interlocutors."
- Cutting: fixed 64-byte grid for all speakers (Z4-A-cut: re-cut under a speaker's
  lexicon is the identity on the grid; recorded so the Phase-4 per-speaker cut-policy
  hook has a defined place to live).

## 4. TRANSLATE op

- `TRANSLATE(nsA, seqA -> nsB)`: resolve A's bytes, mint or find the (nsB, seqB)
  record for the identical bytes, and log OP_TRANSLATE as a DERIVATION
  (a1=nsA, a2=seqA source, a3=nsB, a4=seqB derived) — never as identity.
- Loud failure (-1) if the source id is unknown or not live.

## 5. `common`-namespace governance

- Preregistered rule for this build (Z4-A-gov): a chunk may be promoted to the
  `common` namespace iff its bytes are byte-identical across the two speakers'
  training corpora. The trial attests this by content comparison (deterministic);
  the arm logs OP_MCOMMON per promotion (a1=ns, a2=seq source, a4=seqC common id).
- `common` ids are referenceable by any speaker; they do not count as duplicates.

## 6. Convergence race (kill bar 1) — PROVISIONAL operationalization

Frozen documents define neither the two-speaker curriculum nor "converge", so the
following literal reading is adopted and marked PROVISIONAL-PENDING-FREEZE:

- Curriculum: two speakers alternate episodes. S1 material = t1_prose.bin,
  S2 material = t1_code.bin. Episode e is odd → S1 ingests+probes; even → S2.
- Criterion per probe: recall ≥ 99.5% AND boundary ≥ 95% (the M2 bar).
- ETC_S1 = first odd episode index of the first sustained-3 run of S1 probes at
  criterion (sustained-3 = 3 consecutive same-speaker probes); ETC_S2 likewise on
  even episodes. Censored at 50.
- Control: identical episode schedule, but BOTH speakers ingest under ONE shared
  namespace (the "shared lexicon"); ETC_sh_S1 = first odd episode of the first
  sustained-3 run of S1 probes at criterion; ETC_sh_S2 likewise on even.
  (CORRECTED 2026-09-21: earlier draft used a single "3 consecutive probes"
  criterion for the shared leg, which was asymmetric with the per-speaker
  3+3 requirement and produced a −50% artifact. Both legs now use symmetric
  per-speaker sustained-3 criteria.)
- speedup_pct = (avg_ETC_shared − avg_ETC_namespaced) / avg_ETC_shared × 100,
  where avg_ETC_namespaced = (ETC_S1+ETC_S2)/2 and avg_ETC_shared =
  (ETC_sh_S1+ETC_sh_S2)/2.
- Kill bar 1 FIRES iff speedup_pct < 30.

## 7. Duplication (kill bar 2) — PROVISIONAL operationalization

- Measured on the M6 transfer legs (the two-speaker setting).
- dup = (# live transfer-speaker chunks whose bytes are byte-identical to some
  chunk in the other speaker's training namespace) / (# live transfer-speaker
  chunks). Translated chunks count as duplicates (they ARE cross-namespace
  duplication); `common`-namespace chunks are excluded from numerator and
  denominator (by-design sharing, not overhead).
- Kill bar 2 FIRES iff dup > 40%.

## 8. Standard battery behavior

- M1: ingest + full probe + N=64 ID-swap probe (PROVISIONAL-PENDING-FREEZE per A15:
  patch the ID table so the next recall target resolves to (slot+1)%cap, log
  TRAINER_SWAP_PROBE, verify the recall serves the neighbor's record, restore).
  Returning the original content after the remap = side channel → probe FAIL.
- M2: tiered convergence, ETC, episodes-to-criterion, M9 probe on t1 legs.
- M3: V=1000 pinned (prose→S1, code→S2), 3000 fresh (S3) + kills + weaken +
  4000 at-capacity with eviction. Same freeze policy as the shared harness.
- M4: 100 boundary + 100 content defects per corpus, revision episodes.
- M5: resource pressure; slot_table_bytes = 8 slot arrays + content index +
  insertion queue, all reported honestly.
- M6: multi-party transfer. Transfer ingest per speaker: byte-identical chunks go
  through TRANSLATE (derivation) + common-ground promotion per §5; novel chunks get
  fresh speaker ids. Transfer revision on 100 boundary defects. tax reported.
- M7 (ID arm): rounds 0/1 ingest C, round 2 ingest C' (every-100th-unit edited).
  hit% = served-from-ID-mapping/lookups; reuse = ID references (ingest resolutions
  + lookups) / distinct live IDs (Z4-A-m7r literalization); dedup_savings_bytes =
  bytes not re-stored by dedup. Lookups: 5000 on the (l*37)%n schedule
  (PROVISIONAL-PENDING-FREEZE).
- M8: persistent image covers ALL persistent mappings (slot arrays, content index,
  per-namespace seq counters, probe remap, insertion queue) + ledger + alloc trace;
  N=5 perturbations × 2 reruns, byte-identical.
- M9: same-origin kill-resistance probe on the t1 legs.

## 9. Ledger opcodes (B-64's 1,2,3,4,5,6,8,9,16,17,18 reused; new)

- 19 TRAINER_SWAP_PROBE (M1 ID probe), 20 TRANSLATE, 21 MARK_COMMON.

## 10. Phase 4 validity check

Phase 4 = the system distinguishes who is talking to it. In this build the speaker
tag is explicit logged input metadata on every ingest; zconv and the M6 legs
exercise two live speaker namespaces plus `common`. If the coordinator later rules
Phase 4 non-functional in this setup, both kill bars are conditional and the arm
reports CONDITIONAL-BLOCKED instead of a verdict.
