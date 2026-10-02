# worker_03.md — MANIFEST SWEEP chunk_03 log (2026-09-22)

Chunk: `wave10/int-c7s100/work/` — INT-1 five-organ integration trial, S10 leg (run 2026-09-20).
50 rows, 25 unique files (sha256-verified): three near-identical trees
`src0`, `src_gateless`, `src_inst`.

## Provenance finding (whole chunk)

`src0` is **byte-identical** to `wave9/integration/impl/` (all 15 overlapping
files match, including logs and `.zagd` cache markers) — that is the tree
where the S10 trial actually ran and where RESULTS_S10/CHECK_REPORT point
their evidence (`check_c5redesign.py` defaults `C5_SRC` there). Neither tree
is in git (`~/workspace/tnn-lab` is not a git repo). Within this chunk,
duplicates are marked `dup:` to the first chunk-listed canonical.

## Deduplication map (25 dups)

- `src_gateless/*` copies of GLUE_NOTES, INTERFACE_HASHES, ORGAN_NOTES,
  RESULTS_S10, check_c5redesign.py, curriculum.zag, ledger.zag,
  o2_eliminate.zag, o4_recall.zag, o5_govern.zag, probes.zag,
  substrate/{R33_NATIVE_IO_V1, R33_NATIVE_SHA256_V2, cl/common, o_audit}.zag
  → dup of the `src0` path (15).
- `src_inst/*` copies of the same 15 files → dup of the `src0` path.
- `src_inst/CHECK_REPORT.md`, `src_inst/CURRICULUM_NOTES.md`,
  `src_inst/controls.zag` → dup of the `src_gateless` path (10).

## Variant characterization (non-identical files)

src0, src_gateless, src_inst differ only in 4 files each:

| File | src0 vs src_gateless | src_gateless vs src_inst |
|---|---|---|
| controls.zag | src0 lacks C7ARM/C7CAP telemetry | IDENTICAL |
| loop.zag | src0 lacks CHAIN_PROACTIVE print | src_inst missing from chunk (n/a) |
| main.zag | src0 lacks CAPCOMP print | n/a |
| seam.zag | **src0 intact; gateless has EXP-1 calibration variant** | n/a |

**src_gateless/seam.zag is a designed calibration variant** (labeled
"CALIBRATION VARIANT (EXP-1, 2026-09-20)"): the O2-verdict refusal gate in
seam4_compose (REFUTED → `SEAM_REFUSED_PARTITION`) is deliberately excised;
everything else byte-identical apart from print-only `CHAIN_` telemetry.
This is a lesion-style positive control for instrument discrimination
(pairs with the C7ARM/C7CAP telemetry) — **not a system defect, but results
from this variant must never be read as system capability.**

## Per-file notes (25 unique)

### md (reviewed vs claims)

1. **src0/GLUE_NOTES.md** — claims hold (six seams, 16-word ledger layout,
   deterministic). One stale note: "P2 drop ceiling: UNRESOLVED" — RESULTS_S10
   §9b found the verbatim ceiling in the strength prereg §5.2 (640 drops/stage
   at S10) and the repaired driver enforces it. Verdict: review.
2. **src0/INTERFACE_HASHES.md** — O2 (`e467cf83…`) and O5 (`0295e8dd…`) hashes
   match this chunk's organ sources byte-for-byte; public signatures match the
   reviewed modules (incl. 8-arg `o4_need`, `o3_preempt` with candidates).
   Verdict: PASS.
3. **src0/ORGAN_NOTES.md** — claims verified against sources: audit layout
   (stage@52/d1@56/d2@60) matches ledger.zag; O4 selectors pure modular fns of
   the trace index; refusal codes 200s/204/2101-2105/221-224/310-312 present in
   the organs. The "loop.zag uses stub signatures, will not compile" note is
   **stale for this tree** — src0's glue is the repaired version (compiles;
   verified live). Verdict: review.
4. **src0/RESULTS_S10.md** — verdict **BLOCKED** (instrument failures, not
   system): C3/C4 vacuous lesions, C5 non-discriminating, C7 confounded, P7
   temporal uninstrumented, P2/Q2/P1 unwired, L1 never fired. Every material
   number independently cross-verified by CHECK_REPORT below. Consistent with
   all known outcomes in the task brief. Honest, no misreporting. Verdict:
   review.
5. **src_gateless/CHECK_REPORT.md** — independent checker: **AGREE-BLOCKED**.
   Verified live: build hash `ffdafabc…` (506,405 B) reproducible; paired-run
   log pairs byte-identical; G0 zero-RNG; all six stage gates; controls battery.
   Added four material findings the run worker did not make: (A) implemented
   DC-5 gate is narrower than prereg §3 letter ("no capability collapse vs
   DC-4" clause omitted — since C7 fired, the prereg-letter DC-5 gate did not
   pass, only the narrowed one); (B) the analysis driver's source was deleted,
   so MET/L detail lines are consistency-checked only; (C) the quoted rerun
   hash prefixes are not present in the logs (determinism verified at
   byte-identical-log level only); (D) a ≥80% pin-fraction WARN *is* wired via
   `p3_check` (max 3‰, never fired) — only `q2_pin_alarm` (sustained variant)
   is unwired. Verdict: review.
6. **src_gateless/CURRICULUM_NOTES.md** — **stale in three ways** (both the run
   worker and the checker flagged it; it must not be used for gates):
   (1) "640/stage, 3,840 total" vs code's 800/880/1440/2400/2000/1400 = 8,920
   (selftest pins DC-1=880); (2) "DC-3: O1+O2+O3+O5" vs code `organs=27`
   (no O3 at DC-3); (3) "P2 drop ceiling: UNRESOLVED" vs strength prereg §5.2
   verbatim ceiling 640. Also quotes the 506,443-byte figure the rebuild
   disproved. Keep as historical. Verdict: review.

### py

7. **src0/check_c5redesign.py** — legitimate independent checker for the
   planned C5-redesign re-run (exit 0 iff all 9 check groups pass; separate
   implementation/language from the Zag trial). `py_compile` OK. Smoke-ran
   against the *pre-repair* evidence dir: it tracebacks with an unhandled
   `FileNotFoundError` on missing evidence files (defect 1 — should report
   FAIL, not crash). Code-reading found defect 2: the "all 17 bites pass"
   ok-print guards on substring `"cbite_c5"` but fail messages are formatted
   `"cbite c5_lesion"`, so the guard never matches and the ok-print fires even
   on a real cbite failure. Target evidence (the C5-redesign re-run) does not
   exist yet — S100 is blocked pending the battery repair — so these defects
   bite only when the checker is actually used. Verdict: review.

### zag — randomness audit (standing law: zero RNG in AI decision paths)

Grep over all glue + organs + substrate in src0 and src_gateless for
`rand|random|srand|drand|nanoid|uuid|entropy|clock|rdtsc`: **zero hits in
decision paths**. The only hits are controls.zag's own G0 scanner token list
(comments + scanner byte-compares — the anti-RNG gate itself). Matches the
CHECK_REPORT's independent comment-stripped verification. **Zero RNG law
holds in all reviewed sources.**

### zag — znc miscompile-pattern audit

- **ZNC-007** (consecutive same-size `as []i32`/`[]u32`/`[]u16` aliasing):
  no `as []i32`/`[]u32`/`[]u16`/`[]i64`/`[]u64` casts exist anywhere in the
  reviewed trees. The code uniformly uses `nio_alloc(N)` as `[]u8` arenas
  with explicit `t_put32`/`t_get32` accessors — the AGENTS.md workaround is
  followed. Not applicable.
- **ZNC-004/010** (annotated slice-let off local struct): every annotated
  slice-let from a struct field (`ledger.zag:227,252,255,259,292,294,309`)
  goes through a **function-parameter pointer** (`l:*LgLedger`) — the
  proven-safe pattern. No `&local`-derived pointer slice access found.
- **ZNC-002** (`slice as *u8` garbage reads): no occurrences. The `as *u8`
  hits are `_zag_malloc(n) as *u8` allocator casts — safe.
- **ZNC-012** (chained `s.field.subfield` through pointer-in-struct-field):
  the `a.*.l.seg_d` / `ls.*.o4.audit` patterns are param-pointer → value
  field → subfield, not a pointer stored in a struct field. No instances of
  the ZNC-012 pattern.
- Struct sizes: organs use parallel arena arrays, no nested large structs
  (ZNC-005/006/009 n/a); `OAud{...}`/`LoopState{...}` literal inits use
  small structs only.

### zag — per-file

8. **src0/controls.zag** — G0 scanner + entry gates + C1–C7 + bites; repaired
   C7 metric telemetry present. Compiles (as part of main.zag). Verdict: PASS.
9. **src0/curriculum.zag** — DC-1=880 pinned (confirmed live by selftest
   `CHECK,cu_dc1_eps,880,880`); `CU_DROP_CEIL=0` (unset) consistent with
   RESULTS_S10 §9b (the tripwire is enforced in main.zag at 640, not via this
   const — minor indirection, recorded). Verdict: PASS.
10. **src0/ledger.zag** — 16-word entries, chunked ledger, running sha256
    segment digest; read `lg_append`/`lg_seal_segment` fully: layout matches
    docs; no >2^25 slices. Verdict: PASS.
11. **src0/loop.zag** — repaired 2026-09-20: `force_abstain=12` at DC-2 (L1
    fix), pre-seal capture of `pb_drops/pb_p1ret/pb_pinf`. s0 leg ran rc=0.
    Verdict: PASS.
12. **src0/main.zag** — **spot-compiled with znc** (warnings only: 6× A0102
    ignored-return + 1 string-leak L0010, non-fatal). `selftest` exit 0,
    byte-identical across two runs. `s0` run: `stage_gate 0/0`,
    `ledger_replay 0/0`, `p2_drop_ceiling 0/0` — the §9b repair is armed and
    passing. Verdict: PASS.
13. **src0/o2_eliminate.zag** — corroborated elimination only (2 positive
    observe→CONFIRM, 2 contradictions→REFUTE per ORGAN_NOTES); refusal codes
    201/202/203/107; audit-first idempotent disconnect. No RNG. Verdict: PASS.
14. **src0/o4_recall.zag** — **contains the repaired C3 instrument**:
    `o4_prov_tag` lesion bit0 applies a genuine `(t+1)%3` tag permutation
    (the prereg-§5 behavior the S10 lesion lacked), plus an order-sensitive
    `o4_sel_digest` audited in the replay. Tie-break by lowest pool index.
    Verdict: PASS.
15. **src0/o5_govern.zag** — R=50 frozen (constitution refusal 204),
    ELIM_STRICTNESS excluded (224), constructive vs destructive commit gates
    per frozen law. Verdict: PASS.
16. **src0/probes.zag** — P2 tripwire/Q2/P1-retention now wired into the
    driver (s0 run emits `CHECK,p2_drop_ceiling`); P7 temporal half still
    excluded in code as documented (no WARN path — matches §9c/CHECK_REPORT).
    Verdict: PASS.
17. **src0/seam.zag** — intact seam: O2-verdict gate refuses on REFUTED with
    `SEAM_REFUSED_PARTITION`; `chain_num` is print-only. Verdict: PASS.
18. **src0/substrate/R33_NATIVE_IO_V1.zag** — ported IO via raw syscalls;
    no RNG; no slice casts. Verdict: PASS.
19. **src0/substrate/R33_NATIVE_SHA256_V2.zag** — ported SHA-256; zero
    `as []i64` casts (param slices only); no RNG. Verdict: PASS.
20. **src0/substrate/cl/common.zag** — bounded wire ops (`cl_2001–2008`),
    `@import` of the sha256 module is bare (correct per AGENTS.md). Verdict:
    PASS.
21. **src0/substrate/o_audit.zag** — chunked 4 MiB audit (65536-entry
    chunks, ≤8 chunks), fail-close 107, organ tag in op high 16 bits; the
    2^25-byte limit is explicitly honored by the chunking. Verdict: PASS.
22. **src_gateless/controls.zag** — identical to src0 controls + C7ARM/C7CAP
    positive-control telemetry. Compiles. Verdict: review.
23. **src_gateless/loop.zag** — identical to src0 loop + CHAIN_PROACTIVE
    print. Compiles. Verdict: review.
24. **src_gateless/main.zag** — identical to src0 main + CAPCOMP print.
    Compiles. Verdict: review.
25. **src_gateless/seam.zag** — EXP-1 calibration variant (see above).
    Compiles. Verdict: review.

## Kill bars

No file in this chunk references a preregistered kill bar that fires.
RESULTS_S10's own verdict is BLOCKED (instruments failed, not the system) —
not a kill. The G0 zero-RNG law held everywhere checked. No RNG anywhere in
AI decision paths. No znc miscompile patterns applicable or triggered.

## Spot-compile / spot-run evidence

- `znc main.zag -o s0.bin` (src0): success, warnings-only; 627,591 bytes in
  this environment (vs 506,405 reported — environment/toolchain-config delta,
  sources identical).
- `./s0.bin selftest` ×2: exit 0 both, **byte-identical** stdout
  (incl. `CHECK,cu_dc1_eps,880,880`, defended-channel telemetry).
- `./s0.bin s0`: exit 0; `CHECK,stage_gate,0,0`, `CHECK,ledger_replay,0,0`,
  `CHECK,p2_drop_ceiling,0,0`.
- `znc main.zag -o g.bin` (src_gateless): success. Diffs vs src0 are
  telemetry-only except the documented EXP-1 gate excision.

## Findings summary (for the verdict sheet)

1. **Stale CURRICULUM_NOTES.md** (3 independent errors; do not use for gates).
2. **GLUE_NOTES.md / ORGAN_NOTES.md partially stale** (P2 "unresolved", stub-glue
   incompatibility) — the src0 tree is the repaired version; both repairs
   (L1 force_abstain, P2/Q2/P1 wiring, C3 tag permutation) are present in code
   and verified by a live s0 run.
3. **src_gateless is a designed calibration/positive-control variant**, not a
   system variant: EXP-1 seam gate excision + C7 capability telemetry. Its
   results must not be read as system capability.
4. **check_c5redesign.py has two checker defects** (unhandled
   FileNotFoundError; always-true "all 17 bites" ok-print). Evidence it checks
   does not exist yet (S100 blocked).
5. **Whole-tree byte-identity**: `wave10/int-c7s100/work/src0/` ==
   `wave9/integration/impl/` (the actual S10 trial tree); paired log pairs
   (sN_a == sN_b) in the committed evidence corroborate determinism.
6. Zero RNG in AI decision paths (live G0 + independent grep). No applicable
   znc miscompile patterns in any reviewed file. No kill bars fired.
