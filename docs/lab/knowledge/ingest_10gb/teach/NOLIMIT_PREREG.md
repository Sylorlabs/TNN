# V-NOLIMIT PREREGISTRATION — frozen 2026-09-24

## §0 Identity

- Variant: **V-NOLIMIT** (NO-STUPID-LIMITS crew A). Micah's law: "TNN should not
  have a stupid limit like that. Limits are not a thing TNN needs."
- Idea: kill the 4096B chunk-split ITSELF — invert it without re-running the
  40h source pipeline — instead of amending the `~N` grammar around it.
- Gate under test: scratch-only `gate_nolimit.zag` (committed
  `knowledge/ingest_10gb/teach/gate.zag` untouched). Scratch binary
  `gate_nolimit_bin` (built 2026-09-24 18:42 UTC, pinned toolchain
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`) — NEVER committed.
- Input corpus: `~/workspace/scratch_10gb_work/dryrun/dryrun_facts.dat`
  (SHA-256 `af10db8b03c47e91d809092d89e35f96a7a533c7f9aa2e331200e113818bc690`,
  9,327,214 records).
- Work dir: `~/workspace/scratch_10gb_work/nolimit/`. No `/tmp` for bulk.
- Prereg status: **FROZEN before any variant teach.** Any bar violation KILLS V-NOLIMIT.

## §1 What V-NOLIMIT changes (and does not)

CHANGED (scratch gate only):
- `IG_MAX_TEXT` 4096B ceiling REMOVED from `igr_record` (dynamic buffer growth)
  and from `ig_gate` G1 (20B floor kept, no upper bound).
- 4-record CAL peek uses growable buffers + offset tables (no 4096 stride).
- All ingest reader call sites updated; negative-control path updated.

NOT changed:
- G1 key rules, G2 adjacent-dupe, G3 consistency rules, CAL accept/reject
  semantics (must-accept first-4, must-reject 4 synthetics expecting [1,2,1,3]),
  lesson size 65536, seal/audit/blob formats, bad.bin.
- The `~N` keys are GONE from the corpus (joined away), so no `~N` grammar
  amendment is needed — but the frozen 4096B G1/R9.6 ceiling IS removed, which
  is a gate/spec change. Claim "no gate change at all" is FORBIDDEN.

RESIDUAL (documented, out of scope for the corpus experiment):
- Query/bquery/revise/report paths still allocate IG_MAX_TEXT.
- `igb_append` still requires one record ≤ one ~32MiB blob chunk.
  Corpus max joined record = 1,003,197 B « 32 MiB, so the experiment is valid;
  "arbitrarily large records natively" needs blob-spanning work (separate).

## §2 The join (canonical inverse separator) — PROVEN

- `nolimit_join.py`: groups `...~N` keys, sorts chunks numerically, joins with
  `"\n"*L`, L = MINIMAL L>=2 with `clean2.r9_split_para(join)==chunks`
  (deterministic search with the REAL splitter; fail-loud, cap 8192).
- Why not fixed `"\n\n"`: 111 groups failed — the joined text pulls a later
  sentence terminator INTO the 4096B window, so the re-split cuts later than
  the original boundary. The reason is GEOMETRIC: padding the separator (L>2)
  pushes the next chunk's later terminator outside the current window.
  (NOT "exotic whitespace" length — an earlier draft claimed the original
  inter-chunk whitespace run w was 0.4–1.7KB; not proven, generally false.)
  107 groups need L=3..119; 4 extreme need L=459/844/1226/1711.
- PROOF (2026-09-24, `proof_adaptive.log`, rc=0):
  tilde=117,470; groups=51,804 (197 single-chunk, 51,607 multi);
  nontilde=9,209,744; max_chunks=248; max_joined=1,003,197 B; max_L=1711;
  L: {2: 51496, 3: 79, 4: 4, 5: 8, 6: 4, 7: 3, 11: 1, 13: 3, 14: 1,
      30: 1, 111: 2, 119: 1, 459: 1, 844: 1, 1226: 1, 1711: 1}.
  **51,804/51,804 groups round-trip byte-identically. 0 failures.**
- Transformed corpus: 9,209,744 + 51,804 = **9,261,548 records**.
- Provenance note: the original splitter irreversibly discarded boundary
  whitespace; the join is a deterministic canonical preimage (chunks
  byte-identical), NOT recovery of unknown original whitespace.
- Collision: impossible by construction (r9_emit_unit emits `~N` chunks XOR one
  bare record per unit, never both; unit base keys unique) + runtime guard
  (repaired 2026-09-24: checks previous non-tilde key at group start for the
  before-case + seen-bases for the after-case). Complete streaming validation:
  **0 collisions** across 117,470 tilde / 9,209,744 non-tilde / 51,804 bases.
- CRITICAL: `nolimit_join.py` embeds the HISTORICAL `r9_split_para` (pre-patch
  4096B splitter) as `r9_split_para_HISTORICAL` and does NOT import clean2.
  The 2026-09-24 clean2.py no-split patch broke the inverter (patched
  `r9_split_para` returns `[joined]`, never matching multi-chunk `texts`);
  first full-teach attempt failed on this. The inverter must invert the
  splitter that *created* the corpus, not the patched one.

## §3 Predicted outcomes (from `nolimit_probe.py`, Python mirror of the
## V-NOLIMIT gate + frozen CAL semantics, streamed over the joined corpus)

Probe run 2026-09-24 (`probe_full.log`, rc=0):

- total_records = 9,261,548 (asserted)
- **n (installed) = 9,124,603**
- **g1 = 9** (the 9 V0 G1s; all non-tilde, unaffected by the join)
- **g2 = 0**
- **g3 = 5,864**
- **lessons = 142**
- **lessons_rejected = 2** (dropped 131,072 records)
- negcontrol = 1000/1000 (bad.bin max tlen 105 B — cap removal cannot change
  any bad verdict; verified 2026-09-24)
- NCAP for teach = 9,124,603 + 9,124,603//5 + 100000 = **11,049,523**
  (same formula as NKEY legs)

> ⚠️ BAR TENSION: §4.7 preregistered lessons_rejected=0; the probe predicts 2.
> Mechanism DIAGNOSED (`diag_rej2.log`, 2026-09-24): the 2 rejected lessons
> are 16 and 17. Lesson 16 heads 0–3 are NON-TILDE kind-7 G3 records
> (`gb:pg23950:3213/3214/3215/3217`); lesson 17 heads 0–1 are JOINED kind-7
> groups (`gb:pg25130:102`, `gb:pg25130:104`) and heads 2–3 NON-TILDE kind-7
> (`gb:pg25130:106`, `gb:pg25130:108`). ALL are spaceless Gutenberg texts
> failing G3 LEGITIMATELY (no " " in text — same verdict in V1; the chunks
> are byte-identical). This is purely positional: shifted lesson boundaries
> place pre-existing G3 failures at lesson heads, and the CAL drops those
> lessons exactly as designed. NOT a V-NOLIMIT defect. V0 (frozen) dropped 3
> lessons; V-NOLIMIT drops 2 — strictly better than the frozen baseline.
> Per frozen-prereg governance this needs Micah's re-approval to amend the
> bar from 0 to the exact probe prediction of 2; otherwise V-NOLIMIT is
> KILLED per §4. Full-corpus teach is HELD until this is resolved.

Derivation sanity (to be confirmed by probe):
- V1a/b actual: n=9,314,871, g1=9, g2=0, g3=12,334, lessons_rejected=0.
- V-NOLIMIT replaces installed tilde chunks with joined groups:
  n ≈ 9,314,871 − (V1-installed tilde records) + (accepted joined groups).
- Coverage reading: physical installed count FALLS (many chunks → one record);
  logical source-unit coverage RETAINS all chunk text (proven byte-identical).

## §4 Kill bars (any violation KILLS V-NOLIMIT — no re-spin, no amendment)

1. Round-trip proof < 100% (51,804/51,804). — PASSED 2026-09-24.
2. Prereg not frozen before variant teach. — THIS DOCUMENT.
3. Full-corpus teach launched before `nkey_fullrun.log` contains ALL DONE.
4. CP frozen-gate test: `v0test_bin` on CP subsets must FAIL LOUD —
   stdout contains "lesson error" + "ingest rc=1" and NO manifest.txt is
   written (the binary's main is void → process exit is always 0; the
   failure signal is the stdout text + absent manifest). This proves the
   frozen binary cannot ingest whole records. PROVEN 2026-09-24 on the
   2-record isolation probe (`frozen_cap_probe.dat`: 1 small + 1 5000B
   record): "lesson error", "ingest rc=1", no manifest. If a CP subset
   instead teaches successfully, the premise is wrong → KILL.
5. CP variant tests (CP1/CP2): gate_nolimit_bin counts must EXACTLY equal the
   probe's subset predictions (n/g1/g2/g3/lessons/lessons_rejected),
   negcontrol 1000/1000, seals wellformed (64-hex).
6. Full teach ×2 (sequential): n/g1/g2/g3/lessons/lessons_rejected EXACTLY
   equal §3 predictions; negcontrol 1000/1000 both runs; manifest.txt
   byte-identical across runs AND aggregate store SHA
   (A2: `find . -type f | sort | xargs sha256sum | sha256sum`) identical
   across runs. Any mismatch → KILL.
7. lessons_rejected: probe predicts 2 (see §3 bar-tension note — HELD for
   Micah's re-approval to amend from the preregistered 0; g1/g2 must equal
   V0's 9/0 exactly (±0.1% reading: 9±0.009 → 9; 0 → 0).
8. Determinism: no RNG in build, join, probe, or gate paths (audit: Python
   `random` never imported; Zag has no RNG source).
9. Disk/sequencing: one store at a time; delete each full store after
   hashing + manifest copy; never touch `ingest_1gb/` or the NKEY run dirs.

## §5 CP1/CP2 results

- N-key run COMPLETE: v2b reran to DONE (rc=0, manifest byte-identical to v2a).
  V1a/V1b seals identical; V2a/V2b seals identical. (Main log never got ALL DONE;
  driver died, but all five variant runs completed with manifests.)
- Full V-NOLIMIT teach IN PROGRESS (streaming pipe: `nolimit_join.py build |
  gate_nolimit_bin ingest /dev/stdin`). Two earlier attempts failed on the
  clean2.py patch interaction (fixed: inverter now embeds historical splitter).
- Expected (probe): n=9,124,603, g1=9, g2=0, g3=5,864, lessons_rejected=2.
- Bar tension UNRESOLVED: prereg §4.7 requires 0; probe predicts 2. If teach
  confirms 2, V-NOLIMIT is KILLED per §4 unless Micah re-approves the bar to 2.

### CP1nol — 51,804 joined whole records (the "tilde-only" analog)

- Probe prediction (`probe_cp1.log`): n=51,459, g1=0, g2=0, g3=345,
  lessons=1, lessons_rejected=0. (g3=345 = the 345 legitimately-failing
  joined records: 341 spaceless kind-7 + 4 kind-6; independently confirmed
  by `diag_rej.py`.)
- Frozen `v0test_bin`: "lesson error" + "ingest rc=1", no manifest — FAILS
  LOUD as preregistered (§4.4). ✅ 2026-09-24.
- `gate_nolimit_bin`: n=51,459, g1=0, g2=0, g3=345, lessons=1,
  lessons_rejected=0, negcontrol=1000/1000, seal 64-hex —
  EXACT probe match. ✅ 2026-09-24. Store aggregate SHA
  `edde152c039adbaa9b447fcee645fdd51506a4d66827173a6b0658eec3cd0ce7`;
  manifest saved (`nolimit_cp1_manifest.txt`); store deleted.

### CP2nol — joined records from original lessons {84,116,124}

- Built 2026-09-24: 195,493 records (`nolimit_cp2.dat`, 152MB).
- Probe prediction (`probe_cp2.log`): n=195,446, g1=0, g2=0, g3=47,
  lessons=3, lessons_rejected=0.
- Frozen `v0test_bin`: "lesson error" + "ingest rc=1", no manifest — FAILS
  LOUD as preregistered (§4.4). ✅ 2026-09-24.
- `gate_nolimit_bin`: n=195,446, g1=0, g2=0, g3=47, lessons=3,
  lessons_rejected=0, negcontrol=1000/1000, seal 64-hex —
  EXACT probe match. ✅ 2026-09-24. Store aggregate SHA
  `7ac80c2f74ddabf5162554d66197f1454da0329ea796f036aa9813907e0fcb7f`;
  manifest saved (`nolimit_cp2_manifest.txt`); store deleted.

## §6 Full corpus teach — COMPLETE 2026-09-24

- N-key run COMPLETE: v2b reran to DONE (rc=0, manifest byte-identical to v2a).
  V1a/V1b seals identical; V2a/V2b seals identical.
- Full V-NOLIMIT teach DONE (streaming pipe, join=0 teach=0, ~23 min):
  - n=9,124,603, g1=9, g2=0, g3=5,864, lessons=142, lessons_rejected=2,
    negcontrol=1000/1000
  - seal=827f39bdec5094d02845648bf1f94a9db4ba424ed0ec9e6d36afe98c957cf637
  - blob_total=5,254,365,098 (5.25GB); blob_chunks=157
  - Store aggregate SHA: 23ecb09d6e9352899727d71d04e04d690679311b97d9f98f3b80baad4320539f
  - Manifest saved (`nolimit_full_manifest.txt`); store deleted per discipline.
- **EXACT probe match** on every number (n/g1/g2/g3/lessons/rejected/negcontrol).
- ⚠️ **VERDICT: V-NOLIMIT KILLED per §4.7** — prereg required lessons_rejected=0;
  teach confirms 2. The mechanism is benign (CAL working as designed on
  legitimately-failing spaceless Gutenberg texts at shifted heads 16/17;
  strictly better than frozen V0's 3), but the written bar is violated.
  Revival requires Micah's explicit re-approval amending the bar to the exact
  prediction of 2. Recommended successor: V-NOLIMIT + V2 peek-window composition
  (limits audit L4; composes per audit; would rescue the 2 lessons).

## §7 Honest comparison axes (locked)

- V-NOLIMIT avoids the G3 `~N` grammar amendment (V1's approach) AND the
  V2/V3 mechanisms, but REQUIRES removing the frozen 4096B G1/R9.6 ceiling.
- Provenance: joined records carry canonical `"\n"*L` separators; chunk text
  byte-identical; boundary whitespace not recovered (documented).
- Governance cost: one gate constant removed vs V1's grammar addition —
  the comparison table must present both honestly.

---
FROZEN: 2026-09-24 (predictions §3 to be filled from probe before CP runs).
