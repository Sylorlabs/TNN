# Z4 Ambiguity Log

Provisional resolutions only. Nothing here changes the frozen prereg or brief.

## A15 — M1 ID swap probe schedule (PROVISIONAL-PENDING-FREEZE)
The M1 ID swap probe uses N=64 deterministic adjacent swaps. This schedule is
provisional pending freeze. All M1 outputs carry `m1_id_probe_note` =
"PROVISIONAL-PENDING-FREEZE: N=64 swap probe per A15".

## A16 — M6 cross-speaker transfer corpus mapping (PROVISIONAL)
M6 p2c: transfer speaker = code corpus (S2 namespace), base = prose (S1).
M6 c2p: transfer speaker = prose corpus (S1 namespace), base = code (S2).
Direction labels refer to transfer-speaker content ingested into base store.

## A17 — M8 single combined instance (DOCUMENTED)
Per the assignment constraints, M8 uses one combined M1+M3 persistent instance
rather than two separate instances. Documented here; the M8 gate checks the
combined artifacts.

## A18 — M7 C′ edit schedule (PROVISIONAL-PENDING-FREEZE)
M7's 5,000-lookup schedule and the C′ edit semantics are provisional pending
freeze. Reported in `m7_na_reason` when not applicable.

## A19 — Phase 4 "working" for the binding kill conditional (PROVISIONAL)
The binding kill is "Conditional on Phase 4 working." Z4 implements Phase 4 as
explicit logged speaker-tag metadata (the tag is supplied by the harness, not
inferred by TNN). PROVISIONAL RESOLUTION: explicit tags count as Phase 4
"working" for the purpose of the convergence race, because the mechanism under
test ("per-speaker lexicons namespaced by speaker tag") takes the tag as input;
the convergence comparison (namespaced vs shared) is valid given differentiated
speakers by any means. If the coordinator rules that only inferred speaker
identity counts, the kill conditional is vacuous and Z4's verdict would need
revisiting.

## A20 — "Converge" operationalization for the binding kill (PROVISIONAL)
"Converge" is operationalized as: episodes to reach recall ≥99.5% AND boundary
≥95%, sustained for 3 consecutive same-speaker probes, in an alternating
S1/S2 full-corpus episode schedule. Speedup = (shared_avg_etc −
namespaced_avg_etc) / shared_avg_etc, where each avg is the mean of per-speaker
ETCs. This is symmetric across legs (fixed after discovering an asymmetric
criterion artifact; see death certificate). PROVISIONAL: the coordinator never
defined "converge"; this is the most literal reading (time to reach the same
recall/boundary bars used elsewhere).

## A21 — Duplication denominator (PROVISIONAL)
">40% of chunks duplicated across namespaces": numerator = transfer-speaker
chunks whose content also occurs in another private (non-common) namespace;
denominator = live transfer-speaker chunks. The common namespace is excluded
(it is designed to hold shared content; counting it would punish the mechanism
for working). Measured per M6 leg; reported as `z4_dup_tenths`.

## A22 — Boundary <100% under content dedup (DOCUMENTED, not a bug)
When the same 64-byte content occurs at multiple positions, Z4 mints one ID
(content dedup) and records the last-ingested span. The positional boundary
probe therefore "misses" earlier duplicates. Measured: prose 1 duplicate →
99.9%; code 589 duplicates → 99.6%. This is honest ID semantics (the ID denotes
content, not position), not a defect. All bars are ≥95%, so unaffected.

## A23 — Coordinator "M6 multi-party transfer bar" paraphrase (NON-AUTHORITATIVE)
An earlier coordinator message paraphrased the kill with an "M6 multi-party
transfer bar". Per the second correction, only the brief + verbatim frozen §3
row are authoritative. The paraphrase is logged here and NOT used as a kill
test.

## A24 — zconv ETC granularity (DOCUMENTED)
The convergence race uses full-corpus episodes, so ETC values are small
integers (1–2). The race is degenerate in absolute terms (criterion met almost
immediately), but the COMPARISON is exact: per-speaker and shared legs reach
criterion in identical episodes (speedup = 0%). The degeneracy does not affect
the kill verdict (0% < 30%).
