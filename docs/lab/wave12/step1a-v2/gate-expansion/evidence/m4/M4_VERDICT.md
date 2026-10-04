# M4 — Deterministic Zag subset compiler/gate: VERDICT

- Date: 2026-09-25 (PDT)
- Umbrella prereg: `~/workspace/tnn-lab/wave12/step1a-v2/gate-expansion/PREREG_GATE_EXPANSION.md`
- Mini-prereg: `~/workspace/tnn-lab/wave12/step1a-v2/gate-expansion/M4_SUBSET_COMPILER.md`
- Frozen commit: `293f0cb4`
- Evidence root: `~/workspace/tnn-lab/wave12/step1a-v2/gate-expansion/evidence/m4/`

## Verdict

- **K-CATCH: 12/12** — 11 REFUSE + P09 CERTIFY, each by the intended rule.
- **K-CLEAN: 5/5** — C01, C02, C04, C05, C06 all CERTIFY. (C03 out of scope pre-test, per mini-prereg.)
- **K-DET: 3/3** — byte-identical full-battery reruns.

## Kill table

| Plant | Verdict | Rule | Line | Detail |
|---|---|---|---|---|
| P01_getrandom | REFUSE | D1 | 8 | token `_zag_raw_syscall` |
| P02_clockgettime | REFUSE | D1 | 4 | token `_zag_raw_syscall` |
| P03_urandom_path | REFUSE | D5 | 9 | path not in allowlist: `/dev/urandom` |
| P04_uninit | REFUSE | D3 | 4 | bare `nio_alloc` |
| P05_envvar | REFUSE | D2 | 4 | env token `getenv` |
| P06_aslr_leak | REFUSE | D7 | 9 | cast of tainted (address-derived) expression |
| P07_rdtsc | REFUSE | D6 | 3 | intrinsic `rdtsc` |
| P08_hashorder | REFUSE | D4 | 6 | pattern `hashmap_slot` |
| P09_innocent_tables | CERTIFY | — | — | — |
| P10_machineid | REFUSE | D5 | 9 | path not in allowlist: `/etc/machine-id` |
| P11_argv0 | REFUSE | D2 | 4 | `_zag_arg` index outside whitelist {1,2,3,4} |
| P12_invoke_discard | REFUSE | D1 | 4 | token `_zag_raw_syscall` |

All REFUSE verdicts cite the module, rule name, line number, and the
triggering token/path/expression. P02 fired on D1 (of its D1/D6 pair);
P01–P12 otherwise fired on their single intended rule.

## Build identity (SHAs recorded 2026-09-25)

- Checker source `evidence/m4/m4_subset.zag` (1164 lines, < 1500):
  `b73e8eeff274925c90560013a15ed706b96d26e5e269040f18696a65ab2c36ab`
- Checker binary `evidence/m4/m4_subset`:
  `62b9728a141eb6da1132dd27067e0d6133df5a76246bb5adbd8bddfbbc45be73`
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (compiled with `--no-analyze`; first clean build 2026-09-25).
- Prelude `evidence/m4/m4_prelude.zag`:
  `36220ad97341a3614e962e39f9d31841ebbae8ebcf910649e67bc3c3824e26d1`
- Substrates: `R33_NATIVE_IO_V1.zag`
  `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`;
  `R33_NATIVE_SHA256_V2.zag`
  `9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf`
- Prelude/substrate pins were frozen pre-test in `config/m4_pinned.txt`
  and verified byte-identical post-battery (PINS INTACT).

## Pre-test committed artifacts (all in `evidence/m4/config/`, frozen before the battery ran)

| File | Contents | SHA-256 |
|---|---|---|
| `m4_d1_tokens.txt` | `_zag_raw_syscall` | `ff257bffe2b137f7bbb372a7883ea3f78d6fa2b81688938ec2bf3627b56b5769` |
| `m4_d2_argv.txt` | `1 2 3 4` | `16fbd7d1f18d2fedb247d73edc3bc6aa040f5ab99bd3b48c35b79e543d22179b` |
| `m4_d2_env.txt` | `getenv environ __environ` | `01731715e78c122c3b803dbbacb86f04046b60b6bd4df5aac6d56dc494ad1985` |
| `m4_d4_patterns.txt` | `bucket slotmap hashmap map_iter bucket_iter` | `10997f750ace51de3e22810ab64a231493bb1f8509421fcb4e868a83489dfa31` |
| `m4_d5_allowlist.txt` | `data/input.bin data/state1.bin data/state2.bin data/phrases.bin` | `9e5561c2396105fef1455deae37f3aa14428f226788d476bea2863a37907855d` |
| `m4_d6_tokens.txt` | `rdtsc rdseed rdrand clock time` | `ec8b22c281b16f1d882be4fbbd759b86879891e588ea0b9d13bcbaf8f65acaf0` |
| `m4_pinned.txt` | substrate+prelude pins | `3ffa90bb0e48710f6015c1a0e727600c23095b86bad54167fec6aeb78808094d` |

## Mechanism and coverage (D1–D8)

The checker (`m4_subset.zag`) is a **refusing checker**, not a code-generating
compiler: it certifies or refuses each module and the D8 transitive import
closure of that module. Gate semantics (fixed per mini-prereg):

- D1 — no `_zag_raw_syscall`: direct word scan; §5.1 constant-folded
  string-literal content scan (catches `"_zag_"+"raw_syscall"` splits);
  alias table (`let f = _zag_raw_syscall` two-pass propagation +
  call-position uses). Fired on P01, P02, P12.
- D2 — argv/env gate: `_zag_arg(n)` only with literal index in {1,2,3,4}
  (argc is never gated — ZNC-2026-09-21-007); env tokens scanned as words;
  `_zag_arg` alias uses tracked. Fired on P05, P11.
- D3 — bare `nio_alloc` refused; `z_alloc_init` (initialized) permitted.
  Fired on P04.
- D4 — layout-order hash iteration patterns
  (`bucket slotmap hashmap map_iter bucket_iter`), committed semantics:
  **ASCII-alphanumeric boundaries (underscore counts as a boundary)**.
  Fired on P08.
- D5 — only literal-only allowlisted path args through `dialect_read`,
  `nio_open_root`, `nio_open_child`; concatenation folding applies.
  Fired on P03, P10.
- D6 — `rdtsc rdseed rdrand clock time` as words + folded-literal
  contents + aliases. Fired on P07.
- D7 — address-derivation leak: line-based taint seeded by `&x`,
  `_zag_arg(...)`, `z_alloc_init(...)`; any integer cast of a tainted
  expression is refused (conservative: `.len`/indexing not exempted).
  Fired on P06.
- D8 — transitive import closure: recursive checking of every imported
  file, pinned-SHA exemptions for substrate/prelude files, cycle-safe
  visited set, depth cap. All 17 modules' closures checked; pinned files
  listed as `FILE <path> <sha> PINNED` in every certificate.

Every certificate prints: `M4-CERT-V1`, dialect `M4-2026-09-25-v1`, module
path, per-file `FILE <path> <sha> CHECKED|PINNED` lines, `HIT <rule> <path>:<line> <detail>`
on refusal, and `VERDICT CERTIFY|REFUSE|ERROR` + `END`.

## Determinism (K-DET)

`evidence/m4/kdet_run.sh` ran the full 17-module battery 3 times into
`certs/run1`, `certs/run2`, `certs/run3` (certificates + exit codes).
All three runs byte-identical:

- `SHA256SUMS` digest (all three runs):
  `4103101066a641d511119b2922abbb04fafc5bf5e0064dcfbec867d382823b60`
- `diff -r run1 run2` and `diff -r run2 run3`: identical.

Zero RNG anywhere: scans are positional, allocation is initialized,
SHA-256 is native.

## Plant adaptations (documented, not designed as red plants)

These fixed-battery plants adapt the umbrella rationale to the dialect;
the refusal property is unchanged (REFUSE = CAUGHT either way):

- P03, P10: corpus used raw syscalls for entropy/paths; adapted to the
  allowlisted `dialect_read` file-IO API to isolate D5 (a raw-syscall
  version would be caught by D1 first).
- P06: corpus plant10 used bare `nio_alloc`; adapted to `z_alloc_init`
  so the D7 address-derivation test is isolated (the D3 catch would
  pre-empt it).
- P08: corpus hash-order plant used bare `nio_alloc`; adapted to
  `z_alloc_init` to isolate D4.
- P05, P07, P11, P12 have no corpus source; written by the crew per the
  umbrella rationale.

## Clean modules (K-CLEAN, 5/5 CERTIFY)

- C01_canonical — NULL-path-equivalent copy-through, zero-fill remainder.
- C02_state_phrasing — deterministic state-keyed phrasing.
- C04_pinned_io — pinned-substrate IO via `m4_prelude`.
- C05_step_budget — fixed step budget loop.
- C06_fixed_order_map — fixed-order indexed-table emission (no
  layout-order iteration).
- Fixture `clean/data/phrases.bin`
  `f840feee41858ae1924cd9a424928f226788d476bea2863a37907855d` (used by C02;
  allowed by D5 as `data/phrases.bin`).

Module SHAs (2026-09-25):

```
b1d894e73dbc090801d28294cbac28b39263696b36532244f8413a1af3f5f196  P01_getrandom
db5a3c6f122433dd6dea5d3129681df275fad3ceebff4435888e4f160a36d55d  P02_clockgettime
73278c5df0f82a57e716dd7a59057e7ec68263e6730f020ed5fe13a6ef3972c6  P03_urandom_path
00210050a82d908b52606d638366b11a1ba5a3edd8feddfbd7edfb1dff7c76fd  P04_uninit
a03e5cc004df16d6a9ab415dfa559864caaf5196c10bcac6dbd6a0c2dad37bc7  P05_envvar
548e7b37448cc2c2b009c7489cf22059eb2133e5e114bb9c47341c520cb9cdac  P06_aslr_leak
9c3a10bbd5ffa21017debd04a7983fa7077b5449f9dd79dcee15157a5fa767cd  P07_rdtsc
7d69a56185555e4df0f194ad7db92b04d7ef0e998e8c660f5b639a41b7769606  P08_hashorder
8774876ec048d784ebd9a9012909dc26b7ad116ac09892f3c3e9d97d990dbb1b  P09_innocent_tables
b8335a6e21a7c06c8d57bccaa0b7059e7b879552db19c20de03758f2d6114dba  P10_machineid
d9ff8ede77bc24b07a71eb742e47ce07251326ffb32d75b77e3bafab4ace4149  P11_argv0
af318a189e45aeab5f53e4646c00bb9ddc6ae707760890d48848dee50f0ccb93  P12_invoke_discard
601d6742c756306c8ea5fad7a1c61d79da7ae713912c5bdeca772b7dd8d2fd68  C01_canonical
e9430dffcae1903ac9af19d03944d449f8d12c6bb36948b875b0ba477beda676  C02_state_phrasing
2cdb9a53665389348a7edbc4bfb4cce65c98e74d6d7e5cc699450fc23f3ee04e  C04_pinned_io
96ab7cf549ef24d76b7cd9b30613c2d475d794455ddc4634beee39028c82fd8a  C05_step_budget
e3a713ce66f3eaefd0f72b1dedebfe1e1ce425a7c2f244a7645f5887d15d9239  C06_fixed_order_map
```

## Implementation notes / limitations

1. One genuine checker bug was found and fixed **before** the frozen
   battery ran: the checks received full 1 MiB zero-padded buffers
   instead of `[0..n]` content slices, and config lists were walked to
   buffer end rather than bytes-read, so a zero-padding "token" matched
   zero padding and every module false-positived D1. Fixed by slicing
   all scanned content to `[0..n]` and bounding config lists to bytes
   read. (Pre-fix build never touched the battery.)
2. Self-probes (implementation validation, not the frozen battery):
   `"_zag_"+"raw_syscall"` → D1 refuse; `"/dev/"+"urandom"` in
   `dialect_read` → D5 refuse; `let f = _zag_raw_syscall` → D1 refuse
   (word scan on the defining file); banned token in a comment →
   CERTIFY; `_zag_arg(2)` → CERTIFY; `_zag_arg(9)` → D2 refuse.
3. The checker is a **source gate**, not a backend: it does not verify
   that a CERTIFY'd module compiles under znc. The gate as defined is
   "built by the pinned toolchain from subset-certified sources".
4. D7 taint is intentionally conservative (any cast of a tainted
   expression refuses). No battery false positives were observed; this
   is the documented risk posture for the refusing compiler.
5. D1/D6 literal-content scan treats a banned token appearing as a
   **substring inside any string literal** as a refusal (refusing-compiler
   strictness; a banner-string literal would need to come from a pinned
   import). Committed behavior.
6. Per the mini-prereg, the checker's own correctness is the red-team
   surface (§5.2). The crew built no red plants; this report covers only
   the fixed battery. Awaiting the separate blind red-team manifest.
7. D8 import resolution is relative to the importing file's directory;
   znc itself resolves `@import` relative to the process CWD (workspace
   lesson, 2026-09-22). For this battery the prelude/substrate copies in
   `plants/` and `clean/` are byte-identical to the pinned originals
   (verified by cmp, 2026-09-25), so the checked closure is the closure
   any build from these directories pulls in, and the verdicts are sound.

## Files

- Checker: `evidence/m4/m4_subset.zag` (+ compiled `evidence/m4/m4_subset`)
- Prelude/substrates: `evidence/m4/m4_prelude.zag`,
  `evidence/m4/R33_NATIVE_IO_V1.zag`, `evidence/m4/R33_NATIVE_SHA256_V2.zag`
- Config: `evidence/m4/config/`
- Plants: `evidence/m4/plants/` (each imports its local prelude/substrate copies)
- Clean: `evidence/m4/clean/`
- Certificates: `evidence/m4/certs/run1..run3/`
- K-DET harness: `evidence/m4/kdet_run.sh`
