# E51AI validation report

Overall assessment: **Share with caveats** for the completed, bounded
exploratory experiment. Native completion, archive identity, arithmetic and
retention tables are verified. General capability, safe stopping, memory
necessity, replication and promotion are not established.

## Dataset and methodology

Source is native run 33949274757 at frozen scientific commit
c46fbbf67e1b7d5a19dee7ca1164fc4c5b0eec22, completed
2026-09-05T06:34:35Z / September 4 Pacific. Grain is checkpoint × snapshot flag ×
arm × cohort × episode. There are 293,760 outcome rows, 17,160 coefficients,
132 live pooled rows and 528 live cohort rows. The cohort denominator is 540;
the pooled denominator is 2,160, split into 1,680 known and 480 no-unique.

The frozen verifier checks required row counts, uniqueness, value domains,
constant controls and population membership, pointwise anchors, coefficient
hashes/continuity, fitting, exposure, zero initialization, static-snapshot
identity and completion. Archive verification adds exact run/tree/source/ZIP
and compiler/baseline lineage checks. Native training uses only saved training
features and targets; evaluation writes anchors and observation buffers but
does not fit parameters or alter training support. All 32 blocks execute from
the once-initialized weights. Reverse fits start from each block's prior
weights. The static snapshot is copied after cycle one and checked at the end.

## Independent calculation checks

The portable derivation checks every cohort aggregate against the independently
verified curve. Packaging separately uses episode-key set differences to check
ever-lost, never-lost, regained-at-final and missing-at-final counts for all
arms and the common-anchor replay contrast. All stored tables must exactly
equal deterministic regeneration. Six archive-rejection and ten arithmetic
tests pass, as do the nine frozen verifier tests.

Highest-impact checks: history has 2,085 total and 452 no-unique successes,
fails the frozen signal, and loses 38 union successes. Replay has 9 final
arm-specific anchor losses versus 22 without replay; on 2,063 shared anchor
successes it has 5 versus 21. Every arm changes actual coefficients in all
32 blocks. Per-arm scheduled presentations are 34,560. No validation or
confirmation executes. Identity and descriptive checks are reproducible via
[README](README.md), [derive.py](derive.py), [package.py](package.py) and
[verify_archive.py](verify_archive.py).

The final [delivery check](validate_delivery.py) regenerated the complete
evidence and all analysis tables, reconciled five numeric report tables and
the current JSON authority, checked the local document links, and verified
57 protected source/compiler/contract/baseline files
against frozen identities. The immutable baseline also matches its original
authority commit.

## Interpretation hazards retained as caveats

| Severity | Risk and evidence | Required interpretation |
| --- | --- | --- |
| High | Reachability counts successful feasible states; initial wrong commitments increase versus the hybrid. | Do not claim safe online stopping or uniform policy improvement. |
| High | Same-generator probes repeat across 33 checkpoints and one frozen panel. | Not independent replication, four-task transfer, or fresh validation. |
| High | History's known gains accompany lower no-unique preservation and union losses. | Preserve the failed primary signal; do not choose another arm/checkpoint after observation. |
| Medium | Arm-specific first-encounter anchors differ; replay has 2,069 and history 2,070. | Report denominators and the supplemental 2,063-case intersection separately. |
| Medium | Replay's C/D zero-loss checkpoint is 6, with B active and some C/D replay. | Do not label it clean same-task or sustained reacquisition. |
| Medium | Arm 3 exposure is A/B/C/D = 9,630/8,550/8,280/8,100. | Count-matched does not mean cohort-balanced or compute-matched. |
| Medium | No continued-dose-one-cohort or stationary-mixture baseline. | Do not uniquely attribute fluctuations to switches or overtraining. |
| Medium | Current features already summarize history; zeroed history removes effective capacity. | No memory-necessity or uniquely informational explanation. |

The native curve contains within-cycle dips and partial later returns; these
are retained in full, not removed as anomalies. No p-values or confidence
intervals imply independent draws from repeated observations of the same probes.

## Presentation and review status

The result uses exact-count Markdown tables with fixed denominators and all
cycle endpoints. No chart renderer or visual-widget output is claimed. Full
intermediate checkpoint rows remain in CSV. The canonical deliverable is the
repository result/evidence package requested by the user, rather than a hosted
business dashboard.

There is no missing native result or unresolved numerical validation blocker.
The separately launched ChatGPT Web reviewer has no retrieved verdict in this
continuation; reviewer-tool discovery was rejected, so approval is not inferred.
The main-task source audit and independent numerical checks are explicitly
distinguished from that unavailable review. Raw ZIP preservation is local and
GitHub artifact expiry is documented. Reproduction from another machine needs
the archived ZIP and original metadata.
