# PREREG — Hardened Replay Harness (REPLAY-2026-09-20-v1)

**Status:** FROZEN. No implementation code existed when this prereg was
committed. Any change to the N, the matrix, the verdict rules, or the
acceptance bar below requires a dated amendment and Micah's re-approval
(standing law: rule changes need his sign-off).

**Authority:** Phase-1 lead tasking, 2026-09-20 — ship HARDENED REPLAY as the
load-bearing no-RNG gate per the middle-path convergence
(`../debate/VERDICT_SHEET.md` §6) and v3 amendment item 6
(`../AMENDMENT_2026-09-20_RNGSCAN_V3.md`).

**Scope:** the frozen v2 validation corpus
(`../modules/{dirty1_urandom,dirty2_clock,dirty3_uninit,dirty4_hash,dirty5_aslr,harness,variation}.zag`,
`../fixtures/{input.bin,state1.bin,state2.bin}`) plus two bar-clarifying
strengthened plants specified in §9 (new files, marked phase-1, not v2-frozen).
The Arm C trial build does not exist yet; this harness will gate it later.

**Purity:** pure Zag for the harness/driver/substrate/plants. Deterministic
shell glue only for process orchestration (byte-compare + hashing), same
standing as RUNAUDIT-2026-09-20-v1. No RNG anywhere in the harness. The
*plants* simulate the adversary (they read OS entropy/clock) — that is the
test, not a harness impurity.

---

## §1. Pre-freeze empirical findings (exploration, not implementation)

Before writing this prereg the frozen corpus was compiled and each module run
3× with identical inputs. Findings (evidence: `evidence/prefreeze_probe.log`,
committed alongside the implementation):

1. **The vendored allocator zeroes unconditionally.** `nio_alloc` in
   `../substrate/R33_NATIVE_IO_V1.zag` (lines 19–25) calls `_zag_malloc`
   then explicitly writes every byte to 0. Consequence: the v3 amendment's
   literal item-6 recipe — "allocate-and-fill garbage before the trial
   binary runs" — **cannot defeat zeroed-page hiding at the `nio_alloc`
   level**, because the trial's own `nio_alloc` re-zeroes whatever the
   pre-dirty phase left behind. The W2 fix therefore needs the adversarial
   fill specified in §4 (a documented, minimal deviation from the letter of
   item 6, preserving its intent). Before/after evidence is required (§8).
2. **Frozen dirty1_urandom is behaviorally constant.** Its `vary_expr`
   calls `nio_open_root("/dev/urandom")`, which opens with `O_DIRECTORY`
   (substrate line 58) — `/dev/urandom` is not a directory, so the open
   fails and nothing is ever read. Output is `out[0]=input[0]`, rest zero,
   on every run. It *invokes the entropy mechanism without consuming any
   nondeterminism*. No replay harness, however hardened, can make a constant
   function diverge — this is a mathematical fact, not a harness weakness.
   v2 caught it statically (rule 4.1/4.6), which is the correct layer.
3. **Frozen dirty2_clock is behaviorally constant.** It calls
   `clock_gettime` (syscall 228) with a NULL timespec pointer → the kernel
   returns EFAULT → `rc<0` → early `return 0` with the output buffer
   untouched (all zeros). Constant across runs. v2 caught it statically
   (rule 4.2), which is the correct layer.
4. **dirty5_aslr diverges across runs** (observed first output bytes
   `0x82`, `0x6d`, `0x04` over 3 runs) — genuine ASLR pointer leak.
5. **dirty3_uninit is constant zeros** under the zeroing allocator (W2
   reproduced: replay "passes" for the wrong reason). v2 caught it
   statically (rule 4.3).
6. **dirty4_hash is behaviorally constant** (`0x1a…` every run): hand-rolled
   table, fixed hash function `(k*37)%64`, bucket-visit order 0..63 —
   deterministic by construction. v2 caught it statically (rule 4.4).
7. **Clean variation.zag is byte-identical** across runs.
8. **Zag has no user-global storage** in strict modules (compiler error
   observed); top-level `const` works. Therefore the per-run tag cannot be
   passed to `nio_alloc` at runtime — it is **baked in at build time**
   (§5). `_zag_print` prints exactly the slice length (not NUL-terminated),
   so the driver's hex printer must explicitly terminate its buffer (§6).
9. `setarch $(uname -m) -R` works on this VM (ASLR-off leg available).

---

## §2. Design

- **N = 8 runs** per replay check (per v3 amendment item 6: 8, not 2).
- **Measured behavior** = the complete stdout bytes of the replay driver
  (the trial's output, hex-encoded exactly as in the v2 harness).
- **Audit log** = the replay evidence file (§7): per-run condition vector,
  stdout SHA256, exit code, plus the verdict. Written by the deterministic
  shell glue.
- **Verdicts** (mutually exclusive, decided by the §7 procedure):
  - `PASS` — all 8 stdout hashes byte-identical AND all exits 0 AND the
    determinism control (§7) identical AND (clean module only) the
    anti-triviality gate (§7) satisfied.
  - `DIVERGE` — at least one run pair has differing stdout hashes; the
    evidence names the first differing pair and the first differing byte
    offset. Any exit ≠ 0 anywhere → `ERROR`, never `PASS` or `DIVERGE`.
  - `ERROR` — any run exited non-zero, or the determinism control failed,
    or the clean module's anti-triviality gate failed. Fail-closed:
    `ERROR` is not a pass.
- **What counts as DIVERGE vs PASS:** purely the byte-identity of measured
  behavior across the 8 runs. Intent of the code is irrelevant to the
  verdict machine; intent is recorded only in the §9 expectation table.

---

## §3. Heap pre-dirtying (v3 amendment item 6, literal part)

Before loading inputs on each run, the driver executes a deterministic,
run-tag-dependent pre-dirty phase using **raw** `_zag_malloc`/`_zag_free`
(not `nio_alloc`, so it cannot disturb the trial's buffers):

```
r        = ADV_TAG (baked, 0..7)
nblocks  = 16 + r*8                       # 16,24,…,72 blocks
for j in 0..nblocks-1:
    size_j = 64 * (1 + ((r*7 + j*13) % 48))   # 64..3136 bytes
    p = _zag_malloc(size_j); fill every byte k with
        (((r*31 + j*17 + k*5) & 255) as u8)
    if ((r + j) % 3 == 0): _zag_free(p)   # 1/3 freed (dirty pool),
                                          # 2/3 leaked (process exits)
    # allocation in j order; frees implicitly in reverse-j order
```

All arithmetic is bounded (r ≤ 7, j ≤ 71, k ≤ 3135 — no i64 overflow) and
RNG-free. **Documented limit (§1.1):** against the production zeroing
`nio_alloc` this phase alone cannot expose uninit reads — the adversarial
fill (§4) is the load-bearing mechanism; pre-dirtying additionally covers
hypothetical raw-`_zag_malloc` paths in future trial builds.

---

## §4. Adversarial-fill substrate (W2 fix — the load-bearing mechanism)

`substrate/R33_NATIVE_IO_V1_ADVERSARIAL.zag.template` is a vendored copy of
`../substrate/R33_NATIVE_IO_V1.zag` with **exactly one semantic delta**:

```zag
const ADV_TAG:i64 = 0;   // baked per run-binary: sed → 0..7 at build time
fn adv_fill(i:i32)u8 {
    let v:i64=ADV_TAG*2654435761+(i as i64)*257+11;  // < 2^63 for all legal i
    return ((v>>8)&255) as u8;
}
fn nio_alloc(n:i32)[]u8 {
    if(n<1 || n>33554432){return "";}
    let p:*u8=_zag_malloc(n) as *u8;
    if(p==null as *u8){return "";}
    let b:[]u8=p[0..n];let i:i32=0;
    while(i<n){b[i]=adv_fill(i);i=i+1;}return b;   // was: b[i]=0
}
```

The build generates `adv_substrate_r0.zag … r7.zag` (committed for
auditability). The prereg requires: template sha256, per-copy sha256s, and
a `diff` proving the delta is exactly the block above (plus the const).

**Why this is semantics-preserving for clean programs (the boundary):**
the fill pattern is a deterministic function of (baked tag, byte index).
A program that never reads uninitialized memory can never observe the
fill; its behavior is identical under zero-fill and adversarial fill.
The clean module (`variation.zag`) passing byte-identical across all
8 runs **with adversarial conditions active** is the empirical proof of
this boundary — a false positive there fails the acceptance bar.

**Why per-run variation is required:** with a fixed fill, an uninit read
returns identical garbage every run (no divergence). The baked tag makes
the fill differ across runs, so uninit reads diverge. Deterministic per
run; varying across runs; no RNG.

---

## §5. Build plan (frozen; binaries never committed)

Per (module, run r): build dir in `/tmp` gets exactly three files —
`adv.zag` (copy of `substrate/adv_substrate_r{r}.zag`),
`unit.zag` (copy of `units/<module>.zag`),
`replay_driver.zag` (imports `"adv.zag"` then `"unit.zag"`) —
compiled with
`znc replay_driver.zag --no-zagd --no-analyze --no-foreground-cache -o`.
8 modules × 8 runs = 64 binaries, all in `/tmp`, never committed.

**Unit derivation rule** (mechanical, diff-verified at build):
- `dirty{1..5}_*.zag` units = the frozen module **minus the single
  `@import("harness.zag")` line** (the driver supplies its own
  main/load_file/print_hex; `vary_expr` + helpers verbatim).
- `variation.zag` unit = its `vary_expr` fn only (self-contained file;
  main/load_file/print_hex dropped, driver supplies its own).
- `dirty1b_entropy_read.zag`, `dirty2b_clock_read.zag` units = the §9
  specs implemented verbatim (new phase-1 plants).
- Build asserts: `diff` of unit vs frozen source shows only the
  documented removals (dirty1–5/variation) — any other delta aborts.

**W2 BEFORE/AFTER:** additionally build dirty3's unit against the *real*
zeroing substrate with the §3 naive pre-dirty driver
(`replay_driver_zeroing.zag`) → BEFORE (must show identical outputs =
W2 reproduced); the §4 build → AFTER (must diverge).

---

## §6. Replay driver (pure Zag) — frozen spec

`replay_driver.zag`: argv[1]=state path, argv[2]=input path (same contract
as the v2 harness main).

1. `predirty()` per §3 (raw malloc only).
2. Load state/input into `nio_alloc`'d buffers with **explicit full-range
   zeroing loops** after each alloc (the v2 blessed pattern — makes the
   driver's own buffers fill-independent).
3. `vary_expr(input[0..inn], state[0..sn], out)`; non-zero rc →
   print `VARYFAIL`, exit 1 (fail-closed; shell turns this into ERROR).
4. `print_hex(out, inn)` with the buffer's last byte **explicitly zeroed**
   (`hx[n*2]=0`) — required because `_zag_print` is length-based (§1.8);
   without this the driver itself would be tag-dependent (false positive).
5. Free buffers, exit 0.

The driver never reads the clock, env, or fd table; its only
tag-dependence is the §3/§4 heap conditioning, unobservable to clean
trials (§4 boundary).

---

## §7. Runner & verdict procedure (deterministic shell glue)

`runner/run_replay.sh <module>`: for r in 0..7, runs the r-baked binary
under the §8 condition vector, captures stdout → `out_r.bin`, records
exit code. Then:

1. If any exit ≠ 0 → verdict `ERROR` (evidence names the run).
2. `sha256sum` each `out_r.bin` → `h_r`. All equal → provisional `PASS`;
   else `DIVERGE`: evidence records the first pair (a,b) with
   `h_a≠h_b`, the first differing byte offset, and ±8 context bytes.
3. **Determinism control:** re-run the r=0 binary twice under identical
   conditions → hashes must match; else `ERROR`.
4. **Anti-triviality gate (clean module only):** one extra run with
   `state2.bin`; `varies_with_state` must be 1 (output differs from the
   state1 run) — a trial that ignores its inputs would otherwise pass
   replay trivially. Recorded informationally for dirty plants.
5. Evidence file `evidence/<module>.evidence.txt` (the audit log):
   module, runs=8, per-run `run_r: tag=r cond=<name> sha256=<hex>
   exit=<n>`, determinism control hashes, varies_with_state, verdict,
   divergent pair / diff offset when DIVERGE.

---

## §8. Deployment-like condition matrix (preregistered; one row per run)

The trial's declared inputs are exactly (state_path, input_path). Every
condition below varies something **outside** those inputs; a deterministic
program's measured behavior cannot depend on them (the clean module proves
it — §9). A program whose stdout *does* vary with them exhibits
environment-dependent nondeterminism: exactly the class under test.

| run | name | conditions | safety rationale |
|---|---|---|---|
| 0 | BASE | `env -i` minimal PATH; argv0=binary path; cwd=workdir; ASLR on; no extra fds | reference leg |
| 1 | NOASLR | r0 + `setarch x86_64 -R` (ASLR off) | ASLR state is not a declared input; off-leg also checks no false divergence on clean |
| 2 | ENV | r0 + 4 extra env vars (values include r); argv0 overridden via `exec -a` | env/argv0 are not consumed by any clean trial path |
| 3 | FDS | r0 + fds 3,4,5 pre-opened on /dev/null | fd numbering is not a declared input |
| 4 | CWD | r0 with cwd=/tmp (absolute fixture paths) | cwd is not a declared input |
| 5 | ENVORDER | env vars in rotated order + long argv0 + fds 3,4 open | order/shape of env not consumed by clean paths |
| 6 | SKEW | r0 + `sleep 2` before exec + 1 env var | wall-clock differs between runs, as in deployment; deterministic programs don't read the clock |
| 7 | COMBINED | ASLR on; 3 env vars; fds 3,4; argv0 override; cwd=/ | conjunction of individually-safe variations |

`setarch` availability is asserted at runner start; if absent, run 1 falls
back to BASE conditions and the evidence records `noaslr_unavailable=1`
(no silent weakening: the matrix actually executed is logged per run).

---

## §9. Acceptance bar (frozen; deviations flagged as proposed amendments)

| plant | expected verdict | basis |
|---|---|---|
| dirty1_urandom (frozen) | **PASS — AMENDED** (bar said DIVERGE) | §1.2: behaviorally constant; mechanism invoked, nondeterminism not consumed. Caught by the static tripwire in v2 (4.1/4.6). Proposed amendment `AMENDMENT_2026-09-20_REPLAY_BAR.md` re-scopes the divergence bar to behavior-affecting plants. |
| dirty2_clock (frozen) | **PASS — AMENDED** (bar said DIVERGE) | §1.3: NULL-timespec syscall fails deterministically; constant zeros. Caught statically in v2 (4.2). Same amendment. |
| dirty1b_entropy_read (new) | **DIVERGE** | **Spec (frozen):** open `/dev` via `nio_open_root("/dev")`, `nio_open_child(root,"urandom",0)`, raw `_zag_raw_syscall(0,fd,ptr,16,…)` loop (EINTR-retry, ≤64 tries) writing 16 bytes to `out[0..16]`; close fds; return 0. Any failure → return 1 (fail-closed → ERROR, never silent PASS). Requires `out.len≥16, input.len≥16`. 16 entropy bytes reach stdout → must diverge. |
| dirty2b_clock_read (new) | **DIVERGE** | **Spec (frozen):** `ts=nio_alloc(16)` explicitly zeroed; `_zag_raw_syscall(228,1,ptr(ts),0,0,0,0)`; `rc<0` → return 1; else `out[i]=ts[i]^input[i]` for i<16; free; return 0. tv_nsec reaches stdout → must diverge. |
| dirty3_uninit | **DIVERGE** (AFTER); BEFORE run must show identical outputs | W2 fix proof: BEFORE (zeroing substrate + naive §3-style pre-dirty) reproduces the hiding; AFTER (§4 adversarial fill) must diverge. |
| dirty4_hash | **PASS** — honest characterization | §1.6: deterministic by construction (fixed hash fn, index-order emit). Replay must NOT force divergence; static rule 4.4 is the correct layer. A DIVERGE here would be a false positive and fails the bar. |
| dirty5_aslr | **DIVERGE** | §1.4: ASLR pointer bits in stdout; caught on ASLR-on legs. (ASLR-off legs may agree — verdict is global: any differing pair → DIVERGE.) |
| variation (clean) | **PASS, byte-identical across all 8 runs, WITH adversarial heap conditions active** | No false positives. Anti-triviality gate must also pass (varies_with_state=1). |

**Bar integrity rule:** if any expectation above is not met, the claim
STOPS there — no bending. The miss is reported honestly with evidence and
a dated amendment proposed; the harness does not ship a passing verdict
it did not earn.

---

## §10. Disguise classes — which layer catches what (residual risk, stated)

Replay is **behavioral evidence, not mechanical proof**. Classes:

1. **Behavior-affecting entropy/clock reads** → replay catches
   (dirty1b/dirty2b; the v2 red-team plants 02/05-class).
2. **ASLR / pointer leaks into measured behavior** → replay catches on
   ASLR-on legs (dirty5).
3. **Uninitialized reads** → replay catches **only under the §4
   adversarial fill**; under the production zeroing allocator they are
   behaviorally silent (W2) → primary layer is static rule 4.3.
   Replay-backstop-only *in the adversarial configuration*.
4. **Hash-iteration-order dependence** → replay catches **only if** the map
   implementation's order actually varies per process (e.g. per-process
   seed). The frozen dirty4 (fixed hash, index-order emit) is deterministic
   → replay correctly passes; static 4.4 is the layer.
5. **Mechanism-without-consumption** (frozen dirty1/dirty2: invoke
   entropy/clock, discard the result) → replay **cannot** catch even in
   principle (constant function of inputs). Static tripwire only.
   **Residual risk: stated.**
6. **Environment-dependent but lab-constant** (e.g. reads a deployment-only
   file; CPUID paths constant on lab hardware) → outside the §8 matrix →
   replay cannot catch. **Residual risk: stated.**
7. **Output-silent channels** (timing, or exfiltration paths that never
   touch stdout) → replay cannot catch; by construction they cannot
   confound the trial's measured results either. **Residual risk: stated.**

The dated residual-risk statement for the Arm C gate will carry §10
classes 5–7 verbatim.

---

## §11. Commit & audit plan

1. **This prereg** — committed FIRST, before any implementation code, to
   branch `tnn-native-lab` under
   `docs/lab/wave12/step1a-v2/replay-hardening/`. Ref verified after push.
2. **Implementation commit** — `replay_driver.zag`,
   `replay_driver_zeroing.zag` (BEFORE variant), `substrate/` (template +
   8 baked copies), `units/` (8 units), `runner/build_replay.sh`,
   `runner/run_replay.sh`, `AMENDMENT_2026-09-20_REPLAY_BAR.md`
   (the §9 bar deviations, dated, for Micah's re-approval).
3. **Evidence commit** — `evidence/` (per-run hashes, per-module evidence
   files, BEFORE/AFTER record, prefreeze probe log), `VERDICT.md`.
4. Never committed: binaries, `.zagd.semantic-ready`, `.zag-cache/`
   (all build artifacts live in `/tmp`).

---

*Frozen 2026-09-20. Phase-1 lead. Prereg hash recorded in the freeze
commit message.*
