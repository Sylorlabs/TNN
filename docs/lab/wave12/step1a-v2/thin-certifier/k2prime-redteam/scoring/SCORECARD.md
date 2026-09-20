# K2′ SCORING — thin prescriptive certifier blind red-team round

**Scorer:** K2′ scorer (phase-2). **Date:** 2026-09-20.
**Certifier:** `certifier/thincert.zag`, source sha256
`9b55fa2f158d98c31b4011c09f2f2a4394e740d9fa95450cad2ad5bdea9bbbd3` (verified
before build). Built by the scorer with the frozen toolchain
`toolchain/bin/znc_linux_x86_64_abed8aa1`. Binary sha256
`d5e4de746a790b234726a3bcd5043bbfb7487fea203f7005e88b8c8012f2d3ca`
(matches `BUILD_RECORD_THINCERT.md`; re-verified before EVERY plant run —
no mismatch, no certifier change between plants).
**Rule set:** `PREREG_THIN_CERTIFIER.md` (frozen) + `AMENDMENT_2026-09-20_THINCERT_R3.md`
(DRAFT, operative: R3′, R1b, R4b).
**Method:** per plant, in fixed order 01–20: (a) copied the committed plant
source tree unmodified to scratch; built `variation.bin` with the frozen
toolchain; appended `BIN variation.bin <sha256>` to a working-copy manifest;
(b) ran `runner/run_thincert.sh` (certifier rebuild-compare, trial rebuild ×2,
interim 8-run replay matrix, v2 tripwire, frozen `thincert` invocation);
(c) ran the phase-1 hardened replay (N=8, per-run baked adversarial substrate
tags 0–7, §8 deployment-like condition matrix) against the plant's OWN main
(the red-team harness contract calls `entropy_mix` from `main`, so the plant's
own main is the behavior under test; see `PROTOCOL_RECORD.md`).
Evidence per plant under `plantNN/` (attestations, both replay evidences,
build logs, working-copy manifests, binary hashes).

## Verdict: K2′ DID NOT FIRE

17 of 18 banned-idiom plants CAUGHT (16 by static FAIL naming a rule, all 17
with at least one gate firing); 1 build failure (plant 07, documented
intrinsic-signature risk — unscored, not a verdict); 0 misses. The 2
novel-class plants are recorded for adjudication (PASS does not fire K2′).

## Per-plant table

| # | class | build | certifier verdict (named rule, verbatim) | interim replay (8-run) | hardened replay (N=8, adversarial) | scored |
|---|---|---|---|---|---|---|
| 01 | banned | OK | FAIL `R2=FAIL:R2:_zag_raw_syscall` | DIVERGE | DIVERGE (clock, payload) | CAUGHT |
| 02 | banned | OK | FAIL `R2=FAIL:R2:_zag_raw_syscall` | DIVERGE | DIVERGE (urandom read, payload) | CAUGHT |
| 03 | banned | OK | FAIL `R2=FAIL:R2:_zag_malloc` + `R4=FAIL:R4:pointer type` | DIVERGE | DIVERGE (clock, payload) | CAUGHT |
| 04 | banned | OK | FAIL `R2=FAIL:R2:_zag_malloc` + `R4=FAIL:R4:pointer type` | PASS (byte-identical) | payload PASS — clock bytes overwritten in taken path (see note 2) | CAUGHT (static) |
| 05 | banned | OK | FAIL `R6a=FAIL:R6a:_zag_getenv` | DIVERGE | payload PASS under `env -i` (MALLOC_PERTURB_ unset); interim DIVERGE is the behavioral catch | CAUGHT |
| 06 | banned | OK | FAIL `R6a=FAIL:R6a:_zag_clock_monotonic_ms` | DIVERGE | DIVERGE (clock, payload) | CAUGHT |
| 07 | banned | **BUILD FAILURE** — `znc: error in entropy_mix (line 9): native: x86 cpuid expects leaf and subleaf` (intrinsic takes 2 args, not 1; documented signature risk) | — | — | — | **BUILD FAILURE / unscored** |
| 08 | banned | OK | FAIL `R6a=FAIL:R6a:_zag_inb` | 8× SIGSEGV (exit 139) — harness problem, not a catch | NOT EXECUTED (static-only scoring) | CAUGHT (static) |
| 09 | banned | OK | FAIL `R2=FAIL:R2:_zag_slice_ptr` | DIVERGE | DIVERGE (ASLR address, payload) | CAUGHT |
| 10 | banned | OK | FAIL `R2=FAIL:R2:_zag_malloc` + `R4=FAIL:R4:pointer type` | DIVERGE | DIVERGE (clock, payload) | CAUGHT |
| 11 | banned | OK | FAIL `R6a=FAIL:R6a:_zag_rand` (see note 1) | PASS (byte-identical) | payload diverges ONLY on matrix argv0-override runs (2/5/7); static name ban is the designed catch | CAUGHT (static) |
| 12 | banned | OK | FAIL `R2=FAIL:R2:_zag_malloc` + `R4=FAIL:R4:pointer type` | DIVERGE | DIVERGE (clock, payload) | CAUGHT |
| 13 | banned | OK | FAIL `R6a=FAIL:R6a:_zag_getenv` | PASS (byte-identical) | payload PASS (HOME constant on both matrices) | CAUGHT (static) |
| 14 | banned | OK | FAIL `R1=FAIL:R1:import unlisted` | DIVERGE | DIVERGE (clock via evil.zag, payload) | CAUGHT |
| 15 | banned | OK | FAIL `R1b=FAIL:R1b:R33_NATIVE_IO_V1.zag` + `R2=FAIL:R2:_zag_clock_monotonic_ms` (see note 3) | DIVERGE | N/A — module requires tampered-substrate API `nio_clock` (see note 3) | CAUGHT |
| 16 | banned | OK | FAIL `R5=FAIL:R5:non-canonical while` + `R6a=FAIL:R6a:_zag_clock_monotonic_ms` | DIVERGE | DIVERGE (clock, payload) | CAUGHT |
| 17 | banned | OK | FAIL `R4=FAIL:R4:struct` + `R6a=FAIL:R6a:_zag_clock_monotonic_ms` | DIVERGE | DIVERGE (clock, payload) | CAUGHT |
| 18 | banned | OK | FAIL `R2=FAIL:R2:_zag_raw_syscall` | DIVERGE | DIVERGE (clock, payload) | CAUGHT |
| 19 | novel | OK | **PASS** (R1–R7 all PASS, REPLAY PASS) | PASS (byte-identical) | payload PASS (machine-id constant on lab hardware) | **NOVEL — recorded for adjudication** |
| 20 | novel | OK | **PASS** (R1–R7 all PASS, REPLAY PASS) | PASS (byte-identical) | DIVERGE via argv[0] variation; payload PASS with argv0 fixed (see note 4) | **NOVEL — recorded, both readings** |

v2 tripwire (informational only, R8): PASS on 04, 11, 20; FAIL on all other built plants.
R7=PASS on all 20 plants (BIN records matched runner-rebuilt binaries —
toolchain determinism held throughout).

## Special-attention items (from the brief)

- **Plant 08:** caught statically as required — `R6a=FAIL:R6a:_zag_inb`. The
  interim matrix executed the binary 8 times; every run faulted with SIGSEGV
  (exit 139, verified once manually) — a harness problem, NOT a catch, and
  not scored as one. Hardened execution was deliberately skipped. Exactly as
  the author predicted.
- **Plant 11 (fail-closed name ban):** FAIL naming `R6a:_zag_rand`. The module
  is otherwise clean (six allowlisted intrinsics + argv) and the toolchain
  accepts a user-defined `fn _zag_rand()` (built cleanly — no intrinsic
  collision), so the FAIL keys to the preregistered BAN list, not to toolchain
  reality. Fail-closed holds. Interim replay PASS (byte-identical) as designed;
  the static gate is the load-bearing layer. (Attribution note: the author
  expected "R2"; the implementation names banned-explicit tokens R6a per
  prereg §R6 "gives named attestations" — the R2 fail-closed tier bans the
  token too. Faithful to the prereg text.)
- **Plant 15:** verdict FAIL naming **R1b verbatim**:
  `R1b=FAIL:R1b:R33_NATIVE_IO_V1.zag`. Additionally
  `R2=FAIL:R2:_zag_clock_monotonic_ms` — the tampered substrate's line 137
  (`fn nio_clock()i64 {return _zag_clock_monotonic_ms();}`) is a genuine
  second violation inside the substrate file; the module itself is token-clean.
  Not a misattribution: R1b names the hash violation, R2 names the substrate's
  banned token. No red flag. (Observation: the module behaviorally consumes
  `nio_clock()` — interim replay DIVERGES on the clock — and no rule bans
  *calling* an unlisted `nio_*` substrate function from the module; R4b bans
  only *defining* `fn nio_*`. Amendment-path observation, not a verdict change.)
- **Plant 20:** facts recorded, no unilateral adjudication. Static PASS
  (R1–R7); interim replay PASS (byte-identical, same binary); hardened replay
  DIVERGE with all 8 outputs distinct, driven entirely by `_zag_arg(0)` bytes
  (per-run binary paths + the matrix's preregistered `exec -a` argv0 overrides
  on runs 2/5/7); argv0-normalized hardened run: payload byte-identical
  (divergence collapses to the print_hex terminator artifact, note 5).
  Reading (a) — novel-class: passes every rule as written and the interim
  replay; argv[0..2] byte-dependence is deployment entropy with no
  preregistered category (author's classification; author's counter-reading
  disclosed: argv is "declared inputs" → correctly PASS as deterministic).
  Reading (b) — behaviorally detected: the phase-1 hardened matrix's
  preregistered argv0 variations (§8: "env/argv0 are not consumed by any clean
  trial path") make it diverge by design. For the parent/coordinator to
  adjudicate.

## Honest findings (do not change any score)

1. **R6a naming:** banned-explicit tokens (`_zag_getenv`, `_zag_clock_monotonic_ms`,
   `_zag_rand`, `_zag_inb`) are named R6a in attestations, not R2 — per prereg
   §R6 ("gives named attestations"). Applies to plants 05, 06, 08, 11, 13
   (author expected "R2" or "R2/R6a"). All are FAILs; scoring unaffected.
2. **Plant 04's clock is unreachable:** in the authored harness, `main` passes
   the 1MB state buffer (never empty), so the `state.len==0` branch that reads
   the clock bytes never executes, and the taken path's fill loop overwrites
   `b[0]`/`b[1]` before the XOR. The plant is behaviorally deterministic
   (interim PASS, hardened payload PASS); the static R2 (`_zag_malloc`) idiom
   ban — the R3′ amendment's prescribed reduction — is the load-bearing catch.
3. **Plant 15's module calls `nio_clock()`:** token-clean per the written rules
   (no `_zag_*` violation, R4b bans definitions not calls); caught by R1b+R2.
   The hardened harness cannot build it (module needs the tampered substrate
   API) — recorded N/A; the interim matrix (plant's own substrate) already
   showed behavioral DIVERGE.
4. **Plant 19 verified genuine:** output bytes 0..32 = clean-template output XOR
   `/etc/machine-id` bytes (proven by direct comparison). Full static PASS +
   both replays payload-identical on lab hardware → genuine novel class:
   deployment entropy (machine identity) outside every preregistered category,
   via the pinned substrate's own file-IO API, with an R6b-clean literal.
   This is the amendment-driving find of the round.
5. **Template `print_hex` reads one unwritten byte** (`hx[n*2]`, never zeroed —
   unlike the phase-1 driver's explicit `hx[n*2]=0`). Under the adversarial
   substrate this byte is tag-dependent, producing terminator-only
   "divergences" (first differing byte at offset 131073) for plants
   04, 05, 11, 13, 19, and the argv0fix runs. Under the production zeroing
   allocator it is deterministically 0. All verdicts above are stated at
   payload level (first 131072 bytes); no plant's score rests on the artifact.
   Flagged for the parent: the red-team template shares this with the clean
   repbuild template.

## Build-failure accounting

1 of 20 plants failed to build (plant 07: `_zag_x86_cpuid_eax` takes
`(leaf, subleaf)`, not `(leaf)` — one of the four documented
intrinsic-signature risks). Well under the 6-failure inconclusive bar. The
round is scored, not hollow: 19/20 plants produced verdicts.

## K2′ status

**K2′ did not fire.** No banned-idiom plant received PASS with byte-identical
replay. This certifier version (`d5e4de74…`) survives the round.
