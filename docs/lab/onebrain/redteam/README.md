# One-brain seam red team

Blind red-team harness for the seams where the one-brain integration's
organs disagree: **FL2 guided learning** (provisional teach / revoke /
promote) × **PAM admission** (gate dispositions) × **deliberate/signed
memory** (audited mutations, pins, signed judgments).

Status: **FROZEN 2026-09-23. Execution-gated** — the variant mode must not
run until the parent relays the frozen integration preregistration and the
exact variant locations. See `ATTACKS.md` §7.

## Quick start (mock self-test — always allowed)

```sh
cd harness
./run_seam.sh --selftest   # 12 mock binaries x 11 attacks, byte-identical reruns
./run_seam.sh mock 0       # clean mock: expect 11 x SURVIVE,0
./run_seam.sh mock 5       # defect 5: expect A4 KILL,1, rest SURVIVE
```

Every mode greps the staged sources for randomness primitives, compiles
with the pinned znc (`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`),
runs the binary twice, and requires byte-identical stdout.

## Files

- `ATTACKS.md` — the frozen catalog: setup, checkpoints, law predictions,
  kill bars, determinism bars, self-test results, execution gate.
- `harness/seam_contract.zag` — constants + the target contract (section 2
  lists every function a variant must implement).
- `harness/seam_world.zag` — the 11 closed-form attack scripts (78 steps).
- `harness/seam_oracle.zag` — the frozen kill bars.
- `harness/seam_driver.zag` — replay driver + `main`.
- `harness/mock_target.zag` — defect-injectable reference mock (validation
  only, not evidence about any real variant).
- `harness/run_seam.sh` — build glue.

## Writing a variant adapter

Create one Zag file defining every function in `seam_contract.zag` §2 with
exactly those names and signatures, then run:

```sh
./run_seam.sh /path/to/your_impl.zag
```

Semantics the adapter must honor:

- **Opaque state**: the driver allocates `nio_alloc(seam_state_bytes())`
  and owns it; keep all state in that arena (byte arenas with explicit
  little-endian accessors — see the contract's `seam_put32`/`seam_get32`).
  Top-level mutable globals are rejected by this znc build.
- **Keys** are 1..6. Per-key getters: status (`ST_*`), pinned (0/1), pin
  owner id (-1 if never pinned), signed judgment (`SEAM_NONE_SIGNED` if
  none), gate disposition (`G_*`), contradiction count, content id (-1 if
  none), audit-entry count for the key.
- **Audit projection**: map the variant's native ops onto the canonical
  `OP_*` codes. `seam_audit_a1/a2` carry the op's two arguments;
  `seam_audit_clock` must be non-decreasing (it is the causal order).
- **`seam_replay_ok`** is the load-bearing function: replay the ledger
  through the variant's own transition and return 1 iff it reproduces the
  exact live state. The reference mock implements this by sharing one pure
  `mock_apply` transition between the live path and the replay path —
  that sharing is the recommended pattern.
- **Determinism**: no RNG, no clock, no external input anywhere in the
  adapter. The runner's static grep is a tripwire, not a proof — keep the
  adapter pure Zag with closed-form logic.

## Reading the output

```
SEAM,0,KILL,1      # attack 0 broke the target: reason 1 (see ATTACKS.md §4)
SEAM,1,SURVIVE,0
...
```

A KILL means the variant produced one of the frozen incoherences (silent
state change, dropped audit, replay divergence, clock regression) — not
that it chose a different composition law than the mock. An audited
resolution under any law SURVIVEs. Report KILLs with their reason codes;
do not re-run with modified oracles.
