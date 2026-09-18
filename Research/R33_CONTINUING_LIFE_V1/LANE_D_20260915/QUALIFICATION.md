# Lane D native continuing-life packet qualification — 2026-09-15

Scope: engineering transport only. No behavioral learning, learner authority,
scientific exposure, successor promotion, or canonical R27 writes. Canonical R27
remains the prescribed immutable parent at step 60423 / newborn restarts 0;
fixture values are not a fresh canonical-parent measurement.

The additive `lane_d_packet_integration.zag` execution path uses the existing
`cl_checkpoint_begin/section/finish/commit/load` and descriptor-rooted storage.
Section 1 holds the ENTIRE N17 245536-byte packet, including its inner digest.
Sections 2–10 remain explicit engineering tags, not additional learned state.
Section 11 is the 96-byte world; section 12 is the 16-byte ingress stream.
The resulting outer transaction is 245924 bytes. No existing transport/world
source or original driver was edited. This does not replace the original driver
with a behavioral learner. The source packet is freshly generated from current
N17 `state_image_qual_v92.zag`, NOT from any historical receipt or canonical brain.

`ld_commit` validates both layers before persistence. `ld_load` wraps the
existing outer loader with an additional staging buffer: inner validation must
pass before any caller-visible packet, world, or ingress bytes are copied.
Thus atomicity means whole-record validation/publication and unchanged output
on refusal. It does NOT assert atomic pathname rename or power-loss durability
beyond the existing file/root sync implementation. Bad fixture writers purposely
bypass admission to exercise refusal. Torn packet/checkpoint coverage is a
deterministic truncation fixture, not a newly injected power failure; the original
native supervisor's partial-write crash/refusal regression was also rerun.

## Executed commands and exits

All commands ran from `/Users/Shared/micah/Documents/TNN/TNN` using only native
Zag and local shell tools. No Python, foreign ML runtime, historical verifier,
compiler replacement, commit, push, reset, checkout, clean, or deletion was used.

Every compile below used this exact command template (substitutions listed):

```zsh
/Users/Shared/micah/Documents/zag/znc SOURCE --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o OUTPUT >STDOUT 2>STDERR
```

For compact exact paths below let `D=Research/R33_CONTINUING_LIFE_V1`,
`Q=$D/LANE_D_20260915`, and
`N=Research/R33_NATIVE_N17_R27_CONTINUITY/V92_STATE_IMAGE_QUAL`.
These are notation only; the actual executed commands used the literal paths.

| SOURCE | OUTPUT | compile exit | stdout/stderr prefix |
|---|---|---:|---|
| `$D/outer_learner_packet_bridge_v68_tests.zag` | `$Q/outer_learner_packet_bridge_v68_tests` | 0 | same output + `.compile` |
| `$D/zag_checkpoint_module_repro_v71.zag` | `$Q/zag_checkpoint_module_repro_v71` | 0 | same output + `.compile` |
| `$D/zag_checkpoint_sliceparam_repro_v73.zag` | `$Q/zag_checkpoint_sliceparam_repro_v73` | 0 | same output + `.compile` |
| `$D/lane_d_baseline_driver.zag` | `$Q/baseline_driver` | 0 | `$Q/baseline.compile` |
| `$D/lane_d_reduced_caller.zag` | `$Q/reduced` | 0 | `$Q/reduced.compile` |
| `$N/v92_state_image_qual.zag` | `$Q/n17_state` | 1 | `$Q/n17_state.compile` |
| `$N/state_image_qual_v92.zag` | `$Q/n17_current` | 0 | `$Q/n17_current.compile` |
| `$D/lane_d_packet_integration.zag` initial build-only revision | `$Q/integration` | 0 | `$Q/integration.compile` |
| `$D/lane_d_packet_integration.zag` initial persistence revision | `$Q/integration_v2` | 0 | `$Q/integration_v2.compile` |
| `$D/lane_d_packet_integration.zag` final checked-commit/short-record-refusal revision | `$Q/integration_v4` | 0 | `$Q/integration_v4.compile` |

Initial revisions' binaries and outputs are retained; their intermediate source
was superseded by targeted patches. Only the final source hash qualifies v4.

Direct executions (each redirected to its named run/mode stdout and stderr):

| Command | Exit | Direct result |
|---|---:|---|
| `$Q/outer_learner_packet_bridge_v68_tests` | 1 | `CL_V68_FAILURES,7`; first write returns 2002; offset 1864573184 |
| `$Q/zag_checkpoint_module_repro_v71` | 0 | four call forms return 0 / offset 121; failures 0 |
| `$Q/zag_checkpoint_sliceparam_repro_v73` | 1 | `V73_RC,81` |
| `$Q/reduced` | 1 | `LANE_D_REDUCED_RC,81` |
| `$Q/baseline_driver supervise` | 0 | five children; `CL_ENGINEERING_FAILURES,0` |
| `$Q/baseline_driver learn` | 65 | explicit runtime-pending refusal |
| `$Q/n17_state` | 127 | no binary: compile failed on unsupported `new` syntax; NOT evidence |
| `$Q/n17_current unit $Q/PACKET_RUNTIME` | 2 | wrong mode; NOT evidence |
| `$Q/n17_current selftest $Q/PACKET_RUNTIME` | 0 | `V92_STATE_IMAGE_QUAL_FAILURES,0` |
| `$Q/n17_current write-packet $Q/PACKET_RUNTIME` | 0 | authored fresh packet |
| `$Q/n17_current read-packet $Q/PACKET_RUNTIME` | 0 | fresh-process exact image, inner integrity |
| `$Q/n17_current write-packet-corrupt $Q/PACKET_RUNTIME` | 0 | corrupt fixture |
| `$Q/n17_current read-packet-corrupt $Q/PACKET_RUNTIME` | 0 | corrupt refusal |
| `$Q/n17_current write-packet-truncated $Q/PACKET_RUNTIME` | 0 | 245535-byte fixture |
| `$Q/n17_current read-packet-truncated $Q/PACKET_RUNTIME` | 0 | torn packet refusal |
| `$Q/integration` | 0 | initial one-output-slice build: 245924 |

The v3 checked-commit revision was also compiled to `$Q/integration_v3` (exit 0) with `$Q/integration_v3.compile.stdout/stderr` and ran the same sequence below with V3 directories/logs: nine exits 0, learn 65. Its prior manifests are retained as `V3_SOURCES.sha256` and `V3_ARTIFACTS.sha256`; these are witnesses of that revision, not final source pins. v4 additionally maps a valid-but-short outer record to explicit corruption rather than a positive length; this added branch was compiled but not separately fixture-tested.

Final integration invocations were executed in exactly this order:

```zsh
mkdir -p "$Q/V4_GOOD" "$Q/V4_CORRUPT" "$Q/V4_INNER" "$Q/V4_TORN"
for spec in write:V4_GOOD reload:V4_GOOD corrupt:V4_CORRUPT refuse:V4_CORRUPT inner:V4_INNER refuse:V4_INNER torn:V4_TORN refuse:V4_TORN reload:V4_GOOD learn:V4_GOOD; do
 mode=${spec%%:*}; target=${spec##*:}
 "$Q/integration_v4" "$mode" "$Q/$target" >"$Q/integration_v4.$mode.$target.stdout" 2>"$Q/integration_v4.$mode.$target.stderr"
 print "integration_v4 $spec=$?"
done
```

All nine non-learn invocations exited 0; learn exited 65. Reload ran twice;
the second stdout replaced the first same-named log. v2 used the same order
with binary `integration_v2`, directories `GOOD/CORRUPT/INNER/TORN`, and v2
log prefixes; its exits were also nine 0s and learn 65.

Fresh reload proves exact entire outer checkpoint, exact entire source packet,
inner validity, exact all eight pending-credit fields (active=1), world pending
action=2, exact ingress, and three deterministic delayed continuation steps,
including the delayed outcome=1. Corrupt and re-signed-inner loads return 2005;
torn outer load returns 2001; all preserve every one of 300000 caller bytes.
Final corrupt/inner fixture producers additionally prove checked commit refusal.
The prior GOOD checkpoint remained loadable after every bad-root witness.

Each integration process reports native `CLUsage` and checks status=0,
nonnegative CPU, and 0<RSS<=64MiB. This is observed/self-checked usage, NOT a
new independent OS hard-limit proof. Existing native-supervised baseline
children exited 0,0,0,73,0, were reaped without signals, and had zero stderr;
CPU/RSS are retained in `baseline.run.stdout` and child logs. Original regression
covers strict observations, deterministic world, delayed effects, rooted custody
(including rename and symlink/hardlink/FIFO checks), and unchanged torn-load output.

## Hashes and remaining boundaries

Stable compiler SHA256:
`3093d12dba9cc81b1dee69d2d4e604158d093b58f8f01ddab26c0f4297029956`.
Fresh engineering packet SHA256:
`6b4a7148cfa72d47572029f1386af301f1b2b50ebaa134a40c69d276625d0372`.
Final GOOD checkpoint SHA256:
`dd61d81df41b9baf6b1b77aa3f45daa3ef905be0b342688a9460cd9750ac4090`.
Final v4 binary SHA256:
`4859b0dff3de03d6a7ab5039b58d1dda09c038d7d2ce2d46aad2129f7eb1e67a`.

`SOURCES.sha256` pins the final sources and compiler. `ARTIFACTS.sha256` pins
executed binaries, stdout/stderr and checkpoint/packet bytes. Both were checked
using `shasum -a 256 -c MANIFEST >VERIFIED`; both exits were 0. Historical receipts
were not consumed as fresh evidence.

Unclosed caller row: the original six-slice V68/V73 path still refuses its first
section call under the pinned compiler. A reduced two-slice probe also returns
81; neither was relabeled PASS. V68's positive 2002 status was incorrectly counted
as a positive byte length by its legacy test; its seven failures are retained.
Minimal remaining requirement for that row is a native caller lowering/shape
fix that passes the unchanged V73 and V68 probes with this compiler. The successful
one-output-slice integration narrows the blocker; it does not establish a compiler
root cause or grant permission to replace the compiler.

No canonical behavioral continuation, parameter update, actual R27 descendant
state projection, physical perception, learner authority, scientific qualification,
exposure, promotion, or independent scientific review is claimed. Pending credit
is transported unchanged; no credit application or learner callback is invoked.
