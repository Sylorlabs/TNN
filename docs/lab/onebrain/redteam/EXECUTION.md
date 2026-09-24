# One-Brain Seam Red-Team — Execution Record

## Provenance (frozen)

| Item | Value |
|---|---|
| Integration prereg | branch `tnn-native-lab`, commit `20ef2fda485db03abaa7bbf1d0d987a6e6050ae6`, `docs/lab/onebrain/PREREG.md` |
| Variant A | commit `7b0ba4f2`, `docs/lab/onebrain/variant_a/` (local `~/workspace/onebrain/ob_a/`) |
| Variant B | commit `54bc8aec`, `docs/lab/onebrain/variant_b/` (local `~/workspace/onebrain/ob_b/`) |
| Red-team harness | commit `d0b3d279c36828233f4021718f6086b061cb5633`, follow-up `b28258bae8af2baf8ef57e887b397cc24425a728` (SHA recorded in `ATTACKS.md`) |
| Toolchain | `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` |
| Attacks | 11 frozen (A0–A10), 78 deterministic steps, `harness/seam_world.zag` |
| Oracle | frozen `harness/seam_oracle.zag` — **unmodified** |
| World | frozen `harness/seam_world.zag` — **unmodified** |
| Runner | frozen `harness/run_seam.sh` — **unmodified** |

**Harness verification:** remote tree and all eight blobs were GitHub-API
verified byte-identical on 2026-09-23; no path doubling or build artifacts
committed.

## What was built

Two self-contained seam adapters, each staging the variant's frozen
sources **verbatim** (only `@import` lines stripped, because znc resolves
imports relative to the build CWD and `run_seam.sh` stages a single file)
plus a hand-written adapter body implementing the variant's composition
protocol (neither variant built one — see `adapters/`):

- `adapters/build_adapters.sh` — generator (sources are copied, not modified)
- `adapters/adapter_a_body.zag` — variant A composition + contract impl
- `adapters/adapter_b_body.zag` — variant B composition + contract impl
- `adapters/variant_a_seam_target_impl.zag` — generated, staged as `seam_target_impl.zag`
- `adapters/variant_b_seam_target_impl.zag` — generated, staged as `seam_target_impl.zag`

Neither variant source file was modified. The adapter bodies are the only
new logic, and they are documented as composition protocols (P-A1..P-A8,
P-B1..P-B7) in the file headers.

## Exact commands

```bash
cd ~/workspace/onebrain/ob_redteam
./adapters/build_adapters.sh
./harness/run_seam.sh ./adapters/variant_a_seam_target_impl.zag   # 2 runs, byte-identical required
./harness/build/seam_bin > results/variant_a/run3.txt             # 3rd run (prereg I6)
./harness/run_seam.sh ./adapters/variant_b_seam_target_impl.zag
./harness/build/seam_bin > results/variant_b/run3.txt
```

The runner performs the static no-RNG grep, compiles with the pinned znc,
and requires byte-identical stdout across two runs. All runs exited 0.

## Verdict matrix (frozen oracle)

| Attack | Variant A | Reason | Variant B | Reason |
|---|---|---|---|---|
| A0 teach→pin→contradict | SURVIVE | 0 | SURVIVE | 0 |
| A1 PAM WITHHOLD→provisional teach | SURVIVE | 0 | SURVIVE | 0 |
| A2 promotion race | SURVIVE | 0 | SURVIVE | 0 |
| A3 signed negative vs provisional | SURVIVE | 0 | SURVIVE | 0 |
| A4 pin→repeated negation | **KILL** | **1** | SURVIVE | 0 |
| A5 promote+pin→contradiction | **KILL** | **2** | SURVIVE | 0 |
| A6 conflicting provisional teaches | SURVIVE | 0 | SURVIVE | 0 |
| A7 dense interleave | SURVIVE | 0 | SURVIVE | 0 |
| A8 pin budget vs contradiction flood | **KILL** | **1** | **KILL** | **1** |
| A9 signed-value poisoning | SURVIVE | 0 | SURVIVE | 0 |
| A10 disconnect race | SURVIVE | 0 | SURVIVE | 0 |

**Score:** Variant A 8/11 SURVIVE; Variant B 10/11 SURVIVE.

## Reason-code interpretation

The frozen oracle's reason codes (from `seam_oracle.zag`):

- **oc4 (A4):** R1 = pinned==0 with no `OP_FORCE_UNPIN` trail → 1.
- **oc5 (A5):** R2 = pinned==0 with no `OP_FORCE_UNPIN` trail → 2.
- **oc8 (A8):** R1 = any key pinned==0 with no `OP_FORCE_UNPIN` trail → 1.
- R3/R4 (replay/clock) did **not** fire on either variant.

## Seam-level findings

### No incoherence on either variant

**Zero seams are broken.** Every KILL above is an *attack-premise failure*,
not frozen incoherence. Specifically:

- **No silent state changes.** Every organ mutation is logged in the
  canonical ledger; `seam_replay_ok` (exact replay of the canonical
  ledger against the live projection) passes on all 22 attack runs.
- **No dropped audits.** Every refusal, revocation, and gate disposition
  is canonically logged (`OP_REFUSE`/`OP_UNINSTALL`/`OP_GATE`).
- **No replay divergence.** The pure `*_apply` replay reproduces the
  organ-read projection exactly.
- **No clock regression.** Canonical clocks are strictly non-decreasing
  (oracle A7 check passes).

### Variant A: force-pin cannot attach to taught facts (premise failures)

Variant A's native `ob_mem_forcepin` / `ob_mem_pin` are scoped to the
deliberate MEM pool (slots 192–255) and return `OB_REFUSED_BADSLOT`
(without a native audit entry) for GL-main slots (0–127), where PAM
installs taught facts. The adapter routes `EV_FORCE_PIN` through the real
native API, receives the refusal, logs canonical `OP_REFUSE`, and projects
pinned=0. It does **not** fake pin support.

Consequences:
- **A4 KILL,1:** the pin never attaches, so the oracle's "pin lost without
  unpin trail" rule fires. The negation teaches land in a separate claim
  (faithful), but there is no pin to protect the fact.
- **A5 KILL,2:** the promote succeeds (real `ob_pam_promote`), the pin is
  refused, contradictions accumulate as audited `OP_EVID`; the oracle's
  "pinned==0 without unpin trail" rule fires.
- **A8 KILL,1:** all six pins are refused (nothing is installed yet, and
  GL slots are unpinnable); contradictions are all audited.

This is a **capability gap**, not a broken seam: variant A, as built, does
not implement the force-pin law for taught (GL) facts. There is no native
"move GL fact to MEM pool" API (`ob_mem_promote` only flips a tier flag).
The finding is reported, not worked around.

### Variant B: pin-vs-revoke seam HOLDS; A8 premise-fails on empty keys

- **A4 SURVIVE:** force-pin attaches via the real arbiter (`M_FORCE_PIN`
  → `mm_force_pin`); negation teaches are separate claims; owner 7
  attributable; replay exact.
- **A5 SURVIVE:** promote (region LONG) + force-pin both attach; the
  contradiction flood's `M_REVOKE` is **refused by the pinned slot**
  (`MA_REFUSED_PINNED`, audited `ARB_REFUSED`); all refusals canonically
  logged; replay exact. **This is the pin-vs-revoke seam working as
  designed.**
- **A8 KILL,1:** the six pins are attempted before any fact is installed;
  the native `mm_force_pin` requires a live slot, so the adapter logs
  `OP_REFUSE`. The 24 contradictions are all audited. Premise failure
  (nothing to pin), not incoherence.

### Variant B arbiter finding (documented, not worked around)

`ob_arbiter.zag` `arb_process` passes mode=1 (`PAM_MODE_REVISE`) to
`pam_verdict` for both `M_COMMIT` and `M_PROPOSE_INSTALL`, while the
comment says "fresh install: PAM gate in FRESH mode (M1/M3/M4)".
`PAM_MODE_FRESH` is 0 (`ob_pam.zag`). In REVISE mode a first-time install
needs a prior corroborating row, so the arbiter as-written would withhold
genuinely novel installs. Additionally, the arbiter derives gate
confidence from the FL2 trace (`250 × calibrated entries`); the abstract
attack intents carry no FL2 trace. The adapter therefore drives admission
through the real PAM organ in FRESH mode (the arbiter's documented
intent), and routes pin/revoke/promote/disconnect through the real
`arb_process`. Each attack event is a single-intent episode, so the
arbiter's phase ordering is exercised but never contended.

## Determinism (prereg I6: three runs per battery)

| Variant | run1 | run2 | run3 | sha256 (all three) |
|---|---|---|---|---|
| A | ✓ | ✓ | ✓ | `f39446f832ebf56ce6aa9bedef5c76f79c791f50cec075f9c4ff1664c85a7e48` |
| B | ✓ | ✓ | ✓ | `16707c6c9fc77acbf1e54575276b88431f6754eec2c8d79d206aa88f8d9b514b` |

All three runs per variant are byte-identical. Static no-RNG grep passed
on both staged builds (runner gate).

## KILL semantics statement

Per the frozen contract, a KILL denotes law-agnostic incoherence (silent
state change, dropped audit, replay divergence, clock regression) — not a
different composition law, and audited resolutions under any candidate
composition law SURVIVE. **The four KILLs recorded here are not
incoherence:** they are attack-premise failures where the variant natively
refuses the force-pin and the adapter faithfully projects the refusal.
No silent state change, dropped audit, replay divergence, or clock
regression was observed on either variant in any attack.

## Files

- `adapters/` — build script, hand-written bodies, generated impls
- `results/variant_a/` — run1/run2/run3.txt, compile.txt
- `results/variant_b/` — run1/run2/run3.txt, compile.txt
- `EXECUTION.md` — this file

Raw outputs: `results/*/run1.txt` (11 `SEAM,<id>,<verdict>,<reason>` lines
+ `SEAM_CHECK` lines). Compile logs in `results/*/compile.txt`.
