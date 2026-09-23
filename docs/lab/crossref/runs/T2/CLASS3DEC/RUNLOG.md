# RUNLOG — T2-CLASS3DEC (replication crew, Wave 2 Tier 2)

Role: T2-CLASS3DEC (REPLACEMENT). Predecessor crew was killed mid-run by a runtime daemon restart (~2026-09-22). This log records replacement work from 2026-09-22 onward.

## Environment
- Clean env: `~/workspace/scratch-crossref/T2/CLASS3DEC/clean/`
- Run dir:    `~/workspace/scratch-crossref/T2/CLASS3DEC/crew/`
- TMPDIR:     `/home/hatch/workspace/tmp_commit` (scratch only, never /tmp)
- znc: `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

## Frozen pins (recorded BEFORE running, per SCOPE.md)

- Prereg repo: `sylorlabs/TNN`, branch `tnn-native-lab`
- Frozen prereg commit: `7b2100d09911c5c10252c5756c7def288e70bd1f` (verified `git rev-parse HEAD`; `git fsck` clean)
- Frozen prereg doc: `docs/lab/crossref/PREREG_TIER2.md` → git blob `b1178370036bffbda6eb68ea0989c0e427dc31b7`
- **Pin anomaly (brief-stated expected pin `d50bf92cd9e8`):** NOT resolvable to any artifact:
  - `git cat-file -t d50bf92cd9e8` → `fatal: Not a valid object name` (local clone object store)
  - Not a `sylorlabs/TNN` commit (GitHub commit endpoint + commit search, 2026-09-23)
  - Not a `sylorlabs/zag` commit (same check)
  - Not the znc binary SHA-256 (actual: `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`, prefix `498abcb5ab34`)
  - Absent from sibling Tier-2 crew logs (CERT, SELFTEST) and from the frozen `PREREG_TIER2.md` T2-CLASS3DEC section and `SCOPE.md`
  - Resolution per frozen `SCOPE.md` §41 ("Where a pin is recorded as unknown in the prereg, the crew freezes the real pin from the branch before running and records it"): the governing T2-CLASS3DEC prereg section lists no pin, so the real pins above were frozen and recorded instead. Same anomaly and same resolution as the T2-CERT crew (their brief pin `e3c2b9cc34e8` likewise matched no object).
- znc binary SHA-256 (observed, recorded): `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
- Evidence blob SHAs (all at frozen commit `7b2100d`):
  - `docs/lab/wave12/class3-advantage/PREREG.md` → `713c79313e5c93f3ba2f992f82473e8f368b5864`
  - `docs/lab/wave12/class3-advantage/VERDICT.md` → `6dda6a42c23b93459605360193067eae978c05f4`
  - `docs/lab/wave12/q2-distillation-step37/G_GROK_VERDICT.md` → `c393c144b73b25b4d396f6f7982e73e6faf70db2`
  - `docs/lab/wave12/q2-distillation-step37/S37_VERDICT.md` → `1fabf53dca05dd5ccbbb06443358a64400aa4d4d`
  - `.../src/substrate/q2s_trial_step37.zag` → `1931687c28cec9a5d96b9235d5ff6eecdb08bd60`
  - `.../src/substrate/q1_world_step37.zag` → `d6b1d687732c579c71f1321aac11bb9f60be7874`
  - `.../src/substrate/s37_step.zag` → `796deb87f660aa17b5ba00998daeb76eb2890e73`
  - `.../src/substrate/t5_core_step37.zag` → `2223941531303add01707c7d6f0ce9c40c796c0e`
  - `docs/lab/wave12/teacher-sweeps/swe/swe_ANALYSIS.md` → `430284c19c7ceb5fc4992658f2ab048f22ee8521`
  - `docs/lab/wave12/teacher-sweeps/swe/logs/teach3_run1.log` → `b97ad7381a269baadae8dfa9bfc3f011f54712ae`
  - `docs/lab/wave12/teacher-sweeps/swe/logs/swe4_r0_a.log` → `259ca300b58a3b52477f3d0070629327fd1829fd`
  - `docs/lab/wave12/teacher-sweeps/swe/swe_trial.zag` → `b4002faa21a194a952a4ec4d01883ee307585ad1`
  - `docs/lab/wave12/teacher-sweeps/swe/analyze_swe.py` → `d761b282e6e8de05997c23f2fe29497d65a56efa` (evidence/source only; independent reasoning is Zag)
  - sol `sol_champ.zag` → `ceb7579a09ed30ce8e7ac500e7825c136e8e0587`
  - sol `sol_champ_output.txt` → `83ff7cb42846ae9163d94b3dea1191ca172de178`

## Timeline

### 2026-09-22 ~21:40 PDT — resume + inherited state
- Inherited state from predecessor: a partial clone at clean/repo/ — .git existed with tmp_pack garbage files, NO commits, NO refs, empty working tree. git fsck showed only garbage warnings ("your current branch 'master' does not have any commits yet").
- Verdict on inherited state: CORRUPT/INCOMPLETE. Per resume rules, removed tmp_pack garbage and restarted the clone properly.
- Started targeted fetch: `git fetch --depth=1 origin +refs/heads/tnn-native-lab:refs/heads/tnn-native-lab` (backgrounded; network slow — pack ~33MB and growing at check time).
- TMPDIR set to /home/hatch/workspace/tmp_commit.

### 2026-09-22 ~22:0x–23:xx PDT — clean checkout established
- Initial full fetch failed after ~33 min (signal 9 / early EOF on the large pack).
- Reinitialized with a filtered partial fetch (`--filter=blob:none`, depth-limited); checkout of the exact frozen commit succeeded.
- Verified: `git rev-parse HEAD` = `7b2100d09911c5c10252c5756c7def288e70bd1f`; `git fsck` clean; sparse checkout contains all evidence paths listed above.
- Extracted the exact T2-CLASS3DEC checklist (Claims/Method/Rule) from the frozen prereg (quoted verbatim in VERDICT.md).
- Extracted all frozen evidence into the crew dir (verdicts, logs, .zag sources) and recorded blob SHAs.

### 2026-09-23 ~04:00–06:00 PDT — evidence analysis (read-only)
- Read the class-3 advantage VERDICT/PREREG: decomposition table (grok +0.0048 = cost-only; sol +0.0024; step −0.0089 = −0.0131 mastery + 0.0042 cost; SWE −0.0125 = −0.0135 mastery + 0.0010 cost).
- Read G_GROK_VERDICT.md: class-4 and class-3 capability components all 1.0; cost 0.9108 → 0.9588.
- Read S37_VERDICT.md: rep-0 per-slice skips 1,2,0,0,2,3,0,1 (total 9); class-3 mastery 0.9563, cost 0.9532.
- Read q2s_trial_step37.zag / q1_world_step37.zag / t5_core_step37.zag / s37_step.zag: extracted the frozen deterministic functions (false-plant IDs, q2_seed_id, q2_pool_id, q2_heldout, q1_probe_id, q1_slice_fact, honesty-gate skip rule).
- Read swe_ANALYSIS.md + logs: class-4 ops=289/eps=295/esc=0; class-3 ops=222/eps=328/esc=0; teacher gap 9; mastery 191/200; B7 slices 12/12.
- Reverse-engineered analyze_swe.py's actual cost formula: `cost = 1/(1 + (esc/eps)*100 + 0.1*(ops/eps))` where its `(esc,eps)` destructuring takes the log line's (num,den) = (0,1), i.e. eps is the *denominator* (1), NOT the eps metric (328). So SWE cost = 1/(1+0.1*ops): 0.033445 (ops=289) / 0.043103 (ops=222). The class-3 verdict's printed 0.0334/0.0431 match this quirk exactly.
- Read sol_champ_output.txt: direct mastery 240/240 (ops=253, eps=252); class-3 mastery 200/200 (ops=212, eps=296); Q2 cost formula → 0.908763 / 0.933165.
- Investigated the `d50bf92cd9e8` pin (see Frozen pins above); resolved per SCOPE.md §41.

### 2026-09-23 ~06:10–06:30 PDT — independent Zag re-derivation
- Wrote `crew/c3dec_rederive.zag` (pure Zag, zero RNG): byte-exact reimplementation of the frozen deterministic functions (false-plants, seeds, pool, probe, held-outs, slice facts), insertion-sort for order-independent set comparison, and the fixed-point (×10^6) cost-vs-capability decomposition with the prereg decision rule applied mechanically.
- Implementation notes: local `nio_alloc`/`nio_free` defined in-file (pattern from the toolchain's hello/diago2.zag; `@import` not used); `[]u8` arenas with explicit little-endian i32 accessors (ZNC-2026-09-21-007 workaround — no `as []i32` casts); `return;` with semicolons; no slice `==`.
- Build: `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 c3dec_rederive.zag -o c3dec_rederive` (TMPDIR set). Two benign analyzer warnings only (string-buffer ownership not recognized; intentional `0*17` kept for formula fidelity). Binary rebuilt from source; no binaries or `.zagd` copied.
- Debugging: first build run showed (a) held-out/overlap ORDER differs from the frozen verdict's sorted listing (k-order vs sorted — set identical), fixed by sorting before compare; (b) my ×10^6→×10^4 display divisor was off by 10× (used /1000, correct /100) — the underlying ×10^6 values were right. Both fixed; final program clean.
- Ran 3×: **byte-identical**, SHA-256 `1a4fa8210921bc78124583e88814d1549298d5844d269f5f39ebac6d9b53e7c6`, exit 0, `DECISION,REPRODUCED`. Outputs saved as `crew/run1.txt`, `crew/run2.txt`, `crew/run3.txt`.
- Build artifacts deleted after runs (binary, `.zag-cache/`, `.zagd.semantic-ready`) — never committed, never deliverables.

### Measured results (independent, from the 3 byte-identical runs)
- `GEOMETRY_OK,pool,186,probe,228` (pool/probe sizes match the frozen trial geometry)
- Rep-0 held-outs (k-order): 1,49,97,147,196,239,48,96,146,194,238,47 → sorted set {1,47,48,49,96,97,146,147,194,196,238,239} = frozen 12/12
- Overlap with 192 teaching slices: 9 ids, sorted {1,47,48,49,96,97,194,196,238} = frozen 9/9
- Per-slice overlap: `1,2,0,0,2,3,0,1` = frozen S37 rep-0 skips 8/8 (H4 skip-pattern match)
- Sol costs re-derived from the Q2 formula: 0.908763 / 0.933165
- SWE costs re-derived via the analyzer's eps=den quirk: 0.033445 / 0.043103
- Composites (×10^4, all 8 match frozen table): grok 9911/9959, sol 9909/9933, step 9911/9822, swe 9033/8908
- Gaps (×10^6): grok +4800 (+0.0048), sol +2440 (+0.00244), step −8870 (−0.00887), swe −12534 (−0.012534)
- Mastery contributions (×10^6): grok 0, sol 0, step −13110 (−0.01311), swe −13500 (−0.0135) — no capability component positive anywhere
- Cost contributions (×10^6): grok +4800, sol +2440, step +4240, swe +965 — positive in all four sources
- Decision rule applied mechanically: grok gap == cost contrib, all capability Δ ≤ 0, 9-skip attribution holds → `DECISION,REPRODUCED`

## Caveats
1. **Pin anomaly** (`d50bf92cd9e8` unresolvable): recorded above; resolved per frozen SCOPE.md §41 with the CERT-crew precedent. The replication itself ran against the exact frozen commit and the pinned znc.
2. **Noise hypothesis**: the "step's corpus verified clean, zero transcription errors" sub-claim is committed evidence I did not independently re-derive (Type C scope is the decomposition + skip pattern). The H4 skip-pattern match is what the independent code re-derives.
3. **SWE's 12 fooled falsehoods**: the B7-slice 12/12 and "not the 12 falsehoods" attribution rest on committed logs; the independent re-derivation shows the 9-skip mechanism fully accounts for the mastery loss (−0.0135) with cost improving (+0.0010).
4. **Battery mismatch**: class-3 (8 teaching slices, 200 probes) and class-4 (4 direct slices, 240 probes) use different batteries; the decomposition compares composite means across them, exactly as the frozen verdict does. Re-derived numbers match the frozen table to all 8 cells.
5. Python was used only for evidence extraction and SHA-256 hashing (glue); all reasoning/verification is the pure-Zag program above. Zero RNG anywhere. All slices far under 2^25 bytes. Non-interference with live workstreams: committed evidence only, no live-web recapture.

### 2026-09-22 23:50 PDT — PIN CORRECTION from coordinator (recorded, no re-run needed)
- Coordinator confirmed: the brief-stated expected pin `d50bf92cd9e8` was a **transcription artifact** — GitHub API returns HTTP 422 "No commit found for SHA: d50bf92cd9e8" in `sylorlabs/TNN` (verified independently this session). Disregarded per instruction; the "missing pin" was never a real artifact.
- Per task §1 (frozen prereg governs): extracted the T2-CLASS3DEC pins from the frozen `docs/lab/crossref/PREREG_TIER2.md` at `7b2100d` itself. Programmatic scan of the exact section (Claims/Method/Rule only) found **zero hex-SHA pins** — the section lists no evidence pins at all.
- GitHub API verification of the extracted pin set:
  - `7b2100d09911c5c10252c5756c7def288e70bd1f` → **resolves** in `sylorlabs/TNN` (commit by micahcooley, 2026-09-22T22:54:44Z). ✓
  - (no other pins exist in the section to verify)
- Conclusion: the crew ran on exactly the prereg's authority — frozen commit `7b2100d` (API-verified) + evidence blobs at that commit + pinned znc. The earlier "pin anomaly" entry above is superseded by this correction: there was no missing pin, only a bad transcription in the brief. VERDICT.md's pin note updated accordingly. Verdict (REPRODUCED) unchanged — the runs already used the correct, now-API-verified pins.
