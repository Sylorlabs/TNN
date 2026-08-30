# R32 E51E — Joint Sequential Action-Value Discriminator Result

Date: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Workflow run: `33334204141`
Native result: `VALID NEGATIVE — TERMINAL_REFIT_REACHABILITY_VETO`
Canonical status: R27 unchanged.

## What E51E tested

E51E first refit terminal action values over sequential learner-visible states using the existing grounded terminal utility geometry. It was allowed to evaluate a direct fifth CONTINUE action only if terminal refitting made a correct terminal action reachable for every known validation episode and UNKNOWN reachable for every no-unique validation episode.

No connection topology changed. Graph-like structure was neither added nor privileged.

## Integrity

- E50 parent integrity: pass.
- Fresh seed manifest: 19,440 emitted; zero assignment failures.
- Development episodes: 3,240.
- Validation episodes: 5,400.
- Sealed confirmation episodes allocated: 10,800; executed: 0.
- UNKNOWN nonzero targets: 0.
- CONTINUE target support: 1,657 states where continuing beat immediate terminal value; 53,423 where it did not.
- Terminal deterministic forward/reverse batch identity: pass.
- CONTINUE deterministic forward/reverse batch identity: pass.
- Frozen-control deterministic forward/reverse batch identity: pass.
- Native binary build 1 SHA-256 = build 2 SHA-256 = `2f4acec6b708bbc4fd7e2ee2aa9891bd692503bb9cf756d61b90288599d63634`.
- Native process exit code: 0.
- Evidence artifact ID: `9738546958`.

## Causal result

Primary terminal representation (model 0):
- known episodes reachable: **4,200 / 4,200**;
- no-unique episodes with reachable UNKNOWN: **1,125 / 1,200**;
- residual no-unique reachability failures: **75 / 1,200**.

Richer terminal representation (model 1):
- known episodes reachable: **4,194 / 4,200**;
- no-unique episodes with reachable UNKNOWN: **1,127 / 1,200**;
- residual failures: 6 known and 73 no-unique episodes.

The preregistered primary Stage-1 exact reachability gate therefore failed. Stage 2 direct five-action sequential validation was not eligible to run, and sealed confirmation remained untouched.

## Interpretation

E51D showed the frozen E50 terminal head was a severe reachability bottleneck. E51E shows that retraining terminal action values over sequential states removes the known-state veto for the primary representation and substantially improves no-unique terminal reachability, but it does not eliminate the no-unique failure class.

Therefore the next causal question is not another CONTINUE tuning pass and not a topology change. It is whether the residual states are **exactly aliased under the learner-visible terminal representation** or are distinguishable but beyond the tested linear value-function boundary. E51F is preregistered to answer that question on fresh data.

No R32 promotion claim is supported by E51E.
