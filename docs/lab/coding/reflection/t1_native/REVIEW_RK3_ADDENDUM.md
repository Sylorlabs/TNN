# T1N RERUN — RK3 full-pipeline verification addendum (2026-09-22)

The driver's RK3 check reruns only the battery 5x per arm (deliberation
once). The frozen prereg's RK3 text requires five byte-identical
repetitions of trace text, generated module, builds, verdicts, and
digests. To satisfy the prereg as written, the coordinator ran the
COMPLETE driver pipeline 4 additional times (work-bases runs3, runs4,
runs5, runs6 — each: teach, engine build, full deliberation, freeze,
IV-P1/IV-P2, 5x battery) and compared all frozen artifacts against runs2.

## Result: 5/5 full pipeline runs byte-identical per arm

| artifact | informed (runs2-6) | scratch (runs2-6) |
|---|---|---|
| trace_frozen.txt | b3e6815912a005f32d80a623743c27666bc771a0b63f5b9e8157704f8d4cae77 | 417a01f6acc3b3ba7605c8ce18c39617a4ab3d165c4c3a4c20dfa8155d064c6d |
| t1n_arch.zag | c4811c28d2d17f71953a4b40a3b3f665997390653f2d190617abe36e1b643c28 | c4811c28d2d17f71953a4b40a3b3f665997390653f2d190617abe36e1b643c28 |
| canonical.json (rep1) | 4f2838c55c17a3c36a3bce79f19565944b1102c07dbd1ba21552401550304f2f | 4f2838c55c17a3c36a3bce79f19565944b1102c07dbd1ba21552401550304f2f |

Every additional run exited 0; every trace, module, and canonical digest
matches runs2 exactly. The deliberation is deterministic end-to-end
(zero RNG, verified — not assumed). RK3: PASS on the prereg's own terms.

Note: the two arms' traces differ (99 vs 58 episodes — the informed arm
attempted novel synthesis from the corpus, the scratch arm did not), but
their composed modules and battery verdicts are byte-identical
(c4811c28 / 4f2838c5). The corpus was inert: all novel synthesis failed
to compile, so both arms converged on the same 4 adopted mechanisms.

The runs3-6 workdirs are local-only (byte-identical to the committed
runs2 evidence); this record is the committed evidence of the 5x check.
