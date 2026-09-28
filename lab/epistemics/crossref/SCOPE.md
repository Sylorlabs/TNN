# Cross-reference + clean-environment replications — SCOPE

**Authority:** Micah's ruling 2026-09-22 — "everything should be tested" (governance item 3) — plus his standing maximize law ("run as many as needed, don't minimize it, try to maximize it").

**Frozen:** 2026-09-22 (PDT). This document and the three tier preregs (`PREREG_TIER1.md`, `PREREG_TIER2.md`, `PREREG_TIER3.md`) are frozen together. Any change to scope, families, bars, verdict rules, or replication types requires a dated amendment with Micah-visible notation; it may not be made silently mid-run.

## 1. Purpose

Re-run completed headline verdicts in a **clean environment** (fresh checkout, independent crew, no shared state) and **cross-reference** results across independent crews/implementations, to kill any of:

- lab-environment artifacts (this VM's allocator, cache, filesystem, toolchain quirks),
- single-crew artifacts (one crew's harness bugs, misread bars, silent writer flags),
- single-implementation artifacts (one binary's latent miscompile, one crew's verifier agreeing with itself),
- record artifacts (a verdict recorded from vibes, a commit that doesn't hold what it claims).

A replication never changes the original verdict. It only reports whether the committed verdict survives: **REPRODUCED / NOT REPRODUCED / PARTIAL / UNREPLICABLE-AS-IS** (definitions in §5). Fixes are out of scope; if something doesn't survive, the finding is reported and routed, not repaired in place.

## 2. Clean-environment definition (binding on every crew)

1. **Fresh checkout:** `git clone` of `sylorlabs/TNN` branch `tnn-native-lab` into a NEW directory per family (e.g. `~/workspace/scratch-crossref/<family>/clean/`). Never reuse another crew's run directory, never copy another crew's run outputs — only sources from the repo at pinned commits.
2. **Pinned inputs:** prereg commit, evidence/results commit, input corpora — all taken from the repo via the pinned SHAs the crew freezes in its run log before running. If a pin listed in the tier prereg doesn't hold the expected files, the crew stops, records UNREPLICABLE-AS-IS for that family, and reports — it does not hunt around and substitute.
3. **Toolchain:** the pinned znc at `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`. No `.zagd` caches or build binaries copied between environments; rebuild from source.
4. **Independence:** the replication crew is a different agent session from any crew that produced the original verdict. It may read the original crew's *committed* docs/evidence only — never its scratch, never its uncommitted locals.
5. **Workspace hygiene:** heavy work under `~/workspace/scratch-crossref/<family>/` — never in `/tmp` (512 MB shared tmpfs), never in another workstream's directory. `TMPDIR=~/workspace/tmp_commit` for commits. No binaries or `.zagd` files committed. Slices chunked under 2^25 bytes. Commits via `~/workspace/commit_racefree.py` (syntax: `<branch> <message-file> <file>...`, run from `~/workspace/tnn-lab`, lab-relative paths NOT starting with `docs/lab/`), `commit_big_files.py` for large files. Every commit verified through the GitHub API (`gh-api`).
6. **Mechanism law:** pure Zag for reasoning and verification ("use zag unless its a script" — Micah, 2026-09-22). Python only as glue/build scripts, never as verification authority. Zero RNG anywhere. Where the original claimed byte-identical reruns, the replication runs ≥3 and requires byte-identical digests.

## 3. Replication types

- **Type A — full independent rerun:** rebuild from committed sources in the clean checkout, re-run the original frozen battery per the original prereg, ≥3 byte-identical runs. Compare every committed bar.
- **Type B — anchor replication:** for scale/throughput monsters where a full rerun is infeasible or unsafe on this VM: re-run the anchor point plus one mid-scale point with the same measurement method, verifying the measurement machinery reproduces the committed numbers at those points. The replication states explicitly that the full sweep was NOT re-run.
- **Type C — evidence re-derivation:** for verdicts resting on unrepeatable inputs (live-API corpora, live web, Micah's own eyes/ears, external judge panels): re-derive every committed number from committed evidence with independent Zag code, recompute digests, verify hash chains / byte-identical replays where they exist, and check the verdict rule was applied mechanically per the frozen prereg. No new data collection; the decision math is what's under test.

## 4. Families in scope

| Tier | Families | Replication |
|---|---|---|
| **1 — headline, other work builds on them** | R1 D-family distillation (Track 5); R2 deliberation quality ceiling; R3 teacher showdown legs A/B (4.7 champion); R4 TP1 + SOURCE_AUTHORITY_LICENSE terms; R5 KB4 autopsy | Two independent crews each (primary + cross-check); Type A/A/C as preregistered |
| **2 — committed 2026-09-21/22 verdicts** | Scale-up, scale-down, parameter scaling, prose learning (+4.7 rerun), sol-vs-grok duel, web-search sense v2, information richness, hell-hole phase 2 + whys, web joke/lie/satire, output throughput, speed-intelligence exchange rate, HTD-1, Track A units (+D-family provisional), Track B, Track R0, RSI-1, coding LH-ADV-2, imagination trial, bug-reading, certifier red-team, self-testing harness, dialogue rebuild, English championship box, class-3 decomposition, speech-act wave, Goal B stories, prose v3, TQ series, senses-integrity, audio continuity round 2, senses rebuild H2H, senses rematch, raw-vs-human kill wave | Single clean crew per family (+ digest compare against committed values); Type A/B/C as preregistered |
| **3 — older waves (2026-09-19/20)** | MA1–MA4, R34 clean reruns + quarantine, delayed-credit rule, RC1 (+RC2 acknowledgment state), wave-5 integrity battery, felt V3, state-variation | Verification-of-record + spot rerun of the cheapest decisive bars |

Full per-family claims, expected evidence pins, exact bars, and verdict rules live in the three tier preregs. Where a pin is recorded as unknown in the prereg, the crew freezes the real pin from the branch before running and records it.

## 5. Verdict taxonomy (per family)

- **REPRODUCED:** every committed headline bar/verdict matches within the preregistered tolerance; byte-identical digests match exactly.
- **NOT REPRODUCED:** any committed headline verdict flips (PASS↔FAIL, winner changes, a kill criterion fires differently, a number leaves its tolerance band).
- **PARTIAL:** some bars match and some don't, or a result moved to a tolerance-band edge — list exactly what changed and what held.
- **UNREPLICABLE-AS-IS:** the committed record lacks what's needed to replicate (missing corpus, missing code, dead external dependency, prereg defect) — name the missing piece precisely; do not substitute.

The replication verdict table lives at `docs/lab/crossref/VERDICT_TABLE.md` and is updated as families close. The final report names every verdict that does not survive replication, with the exact divergence.

## 6. Exclusions (not completed verdicts — listed so nobody re-litigates)

Epistemic five-leg battery (prereg frozen, not run); T1N full rerun vs frozen prereg `ae4693a13` (pending); KB4 SUSPECT-gate redesign prereg (unsigned, unrun); past-RAM sweep final knee (running); storage-compression investigation (running); hell-hole v3 (dispatched, not run); debatable-claims opinion+debate trial (reported but unverified, commit pending); PAM rebuild (running); imagination R6/R7/R8 blind verdicts and audio forks (pending); RSI-3 (dispatched); audio-continuity blind-package rebuild (outstanding promise, separate from the round-2 verdict); Goal A discovery wave; teacher-showdown Leg C (not run); any verdict whose committed evidence is still local-only.

## 7. Non-interference

Crossref crews do not touch live workstreams' files or processes (past-RAM, compression, T1N rerun, epistemic finish crew, hell-hole v3, PAM rebuild, audio forks, imagination forks, the in-flight Zag-native TP1 oracle). Read their *committed* outputs only. The TP1 replication crew coordinates around — never clobbers — the resumed Zag-oracle workstream.

## 8. Order of execution

Wave 1: Tier 1 (R1–R5) — dispatched first, in parallel, small-to-medium compute.
Wave 2: Tier 2 families — batched; heavy families (scale-up, throughput) run Type B and never concurrently on this 2-vCPU VM.
Wave 3: Tier 3 — verification-of-record + spot reruns.
The verdict table and final report close the program when all waves report.

## 9. Standing laws that bind this program

Micah's laws, unchanged: zero RNG (byte-identical reruns), pure Zag unless it's a script, no-free-lunch (benchmark, don't assume), evidence and frozen bars decide, everything reversible, stubs never headline evidence, tests not requiring structural approval are pre-approved. The replication program itself is pre-approved under Micah's 2026-09-22 standing test approval and his explicit "run everything" ruling for this item.
