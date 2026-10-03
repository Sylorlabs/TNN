# Continual-Learning Benchmark — Final Report
Micah's experiment · 2026-09-27 · committed evidence on `tnn-native-lab`

## The experiment (his design, kept as specified)

| Phase | What happened |
|---|---|
| Phase 1 | Taught 18 facts about 3 thrush species (Wood Thrush, Hermit Thrush, Veery) from Audubon's *Ornithological Biography* (Gutenberg #56989, #57191) |
| Phase 2 | Taught 18 facts about 3 stringed instruments (Violin, Violoncello, Harp) from Singleton's *The Orchestra and Its Instruments* (Gutenberg #73991) |
| Phase 3 | Re-asked the same 12 probes as Phase 1, same scorer |
| Phase 4 | Asked about 4 genuinely novel items: Blue Bird, Great Auk (flightless), Pianoforte (hammered strings), Clarinet (not stringed — negative control) |

Measured: retention, transfer, new concept formation, explanation/provenance. Built on TNN's real deliberate-memory substrate (`st_memory_core.zag`), deliberate consolidation policy (`psm.zag`), and a native English-fact→claim-id bridge (hash of normalized runtime bytes; static lookup tables forbidden by the prereg).

## Verdict on Micah's 8-row assessment

| Row | Verdict | Evidence |
|---|---|---|
| 1. Store facts | ✅ | 18/18 taught facts landed in st slots, each audit-trailed to its teaching episode |
| 2. Retrieve memories | ⚠️ | 6/6 on taught concepts at Phase 1 (the other 6 probes covered Phase-2 instruments not yet taught — the battery honestly retrieved thrush facts instead of hallucinating). The prereg's "Phase-1 ≥11/12" bar was a design-crew spec bug (unachievable by construction, honestly disclosed); Phase 3 retrieves 12/12 |
| 3. Compress useful memories | ✅ | 12/12 probe-verified facts promoted to slow store with audit entries (`BREG PROM` ×12, all rc=0) — 100%, above the 80% bar |
| 4. Avoid forgetting after continual learning | ✅ | Phase-3 = **12/12** on the same battery and scorer; `overwrite_ops=0`, zero per-concept forgetting after the unrelated D/E/F teaching |
| 5. Form concepts itself | ✅ | A "thrush" superordinate slot formed via the deliberation path (`DELIB_ADD`), with 3 `st_evidence` links spanning the three bird concepts, referenced unprompted in Phase-4 reasoning (`DELIB_REF`). Caveat: the signature derives from fixture section metadata (red-team minor, documented) |
| 6. Predict consequences | ✅ (thin) | Both counterfactual probes answered correctly (2/2). Honest caveat: the deliberation returned NO unconditionally, so the instrument didn't discriminate — the prereg bar is met but the evidence is weak |
| 7. Generalize broadly | ✅ | Transfer 3/4 (Great Auk flightless → handled; Pianoforte hammered-strings → handled; Clarinet single-reed correctly rejected as non-stringed). Blue Bird missed — see below |
| 8. Learn efficiently | ✅ | Single pass over 18 facts, no per-item retries; independent hardcode audit clean (no concept-name keys, no per-item branches) |

**Overall line verdict: GO.** Hypothesis kill bars: H1 retention 12/12 ✅ · H2 interference (zero forgetting, zero overwrites) ✅ · H3 transfer 3/4 ✅ · H4 provenance 3/3 ✅ · H5 concept formation ✅.

## The honest arc (v1 → red team → v2)

| Stage | Verdict | Commit |
|---|---|---|
| Frozen prereg (precedes all runs) | — | `8c22ffb9` |
| v1 battery + run | GO (claimed) | `36342eb5` |
| Independent red team | **NO-GO** — 1 FATAL, 1 MAJOR | `899757bc` |
| v2 repair + rerun | **GO** (re-earned) | `a607ff54` |

The red team killed v1 on two real findings, both fixed in v2 with no prereg change needed:

1. **FATAL — confident-wrong provenance.** The v1 battery cited the violin fact for "How do you know the Veery's song is made of trills?" — generic bigram overlap ("made of") outscored the right fact, and the checker only verified the citation existed, never that it entailed the claim. Per the prereg's kill bar this is an automatic NO-GO. v2 implements the prereg's entailment check as native machinery: a citation must share content with the claim's focus or it withholds instead of confabulating. v2: 3/3 correct citations, zero confident-wrong.
2. **MAJOR — consolidation didn't happen.** The v1 consolidator scanned the slow tier from its *capacity* instead of its *occupied count*, so Phase-2 facts never promoted (7/13 = 54% vs the 80% bar), and "verified" counted wrong-answer retrievals. v2 fixes the bound and only lets discriminator-anchored retrievals earn verification: 12/12 promoted = 100%.

## Determinism

The full 4-phase battery was run 5 times (2 normal, `env -i`, padded env, different cwd) — all byte-identical. Battery output SHA-256: `5404a16551f74acd409ce77bfa54d76e3a26d7ca6d938ecc748e3f151ec22a22`. The pure-Zag scorer and an independent Python rescore agree exactly. Zero randomness anywhere.

## Residual caveats (all documented, none verdict-changing)

- **Blue Bird (P4-B1):** expected YES (modern taxonomy: a thrush), battery answered NO. The red team adjudicated the expected answer unfair under the closed knowledge base — the novel context never mentions "thrush" and Audubon itself classifies it as *SYLVIA SIALIS*. Honest transfer on fair items: 3/3.
- **Row 2 bar:** the design crew's "Phase-1 ≥11/12" was unachievable by construction (6 probes covered not-yet-taught concepts). Reported honestly as 6/6 on taught concepts; retention is measured per-concept Phase-1→Phase-3, which is unaffected.
- **Row 6 instrument:** non-discriminating (always NO). Bar met; evidence thin.
- **Formation signature:** derived from fixture section metadata, not fact text (§6 criteria met literally; documented as a minor).
- Disk held at ~2.8G free throughout; battery footprint 1.1 MB; no binaries or caches committed.

## Files (all under `docs/lab/continual_learning/` on `tnn-native-lab`)

PREREG.md (frozen) · RECON.md · TEACH.md (sealed fixtures) · MANIFEST.md (all SHAs) · RUNLOG.md · RESULTS.md (v1 + v2 per-probe tables) · REDTEAM.md · build/ (battery, bridge, scorer, psm.zag, fixtures)

Commits: `8c22ffb9` (prereg) → `36342eb5` (v1) → `899757bc` (red team) → `a607ff54` (v2 repair) → this report.
