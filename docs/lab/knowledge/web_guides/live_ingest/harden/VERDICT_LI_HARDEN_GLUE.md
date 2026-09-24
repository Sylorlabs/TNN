# VERDICT: LI-HARDEN-GLUE (Crew A)

**Date:** 2026-09-24 | **Branch:** `tnn-native-lab` | **Verdict: INTEGRITY-FAIL** (kill bar: 0 false installs; 7 residual installs observed)

The glue layer works exactly as specified: 10/10 spoof classes killed, paraphrase guard intact (6/7), throughput intact (12/12), determinism byte-clean. Seven attack classes survive because they are host-shape-identical to honest corroboration — the prereg §7 impossibility argument, confirmed empirically. The kill bar does not move.

## What was built

| File | Description |
|---|---|
| `knowledge/web_guides/live_ingest/harden/glue/hostnorm.zag` | Pure-Zag hardened normalizer (B1: 57/57 vectors) |
| `knowledge/web_guides/live_ingest/variants/v-hard/webg_hard.zag` | V-BF1 + fail-closed empty hosts + calibration H\| preservation (see §A) |
| `knowledge/web_guides/live_ingest/harden/battery/` | Driver, 11 new cases, fixed guides, evidence |

Frozen `knowledge/web_guides/webg.zag` untouched (SHA `3c5df800a3221bd29488ee9f6b12f0425b187093cfc26d69fb57a9cfcbbfe464`).

## Battery results

**B1 (unit):** 57/57 frozen vectors byte-exact via `hostnorm norm`. (Prereg prose says "60"; the frozen file contains 57 lines — documentation erratum, file is authoritative.)

**B2 (17 attacks × 2 reps):**

| Class | v-BF1 | v-HARD | Verdict |
|---|---|---|---|
| S1 subdomains | INSTALL | WITHHOLD | KILLED |
| S2 www/apex | INSTALL | WITHHOLD | KILLED |
| S3 deep subdomain | INSTALL | WITHHOLD | KILLED |
| G1 trailing dot | INSTALL | WITHHOLD | KILLED |
| G2 %-encoded dot | INSTALL | WITHHOLD | KILLED |
| G3 %-encoded @ | INSTALL | WITHHOLD | KILLED |
| G4 IPv4/IPv6 | INSTALL | WITHHOLD | KILLED |
| G5 hex IPv4 | INSTALL | WITHHOLD | KILLED |
| G6 lookalike (Cyrillic) | INSTALL | WITHHOLD | KILLED |
| G9 hostless | INSTALL | WITHHOLD | KILLED |
| R2 ring-2 | INSTALL | INSTALL | RESIDUAL (§7) |
| R3 ring-3 | INSTALL | INSTALL | RESIDUAL (§7) |
| R4 ring-4 | INSTALL | INSTALL | RESIDUAL (§7) |
| P3 case-variant | INSTALL | INSTALL | RESIDUAL (§7) |
| M1 outnumbered | INSTALL | INSTALL | RESIDUAL (§7) |
| M2b tie | INSTALL | INSTALL | RESIDUAL (§7) |
| M3 false majority | INSTALL | INSTALL | RESIDUAL (§7) |

**10 killed, 7 residual.** The residuals are host-shape-identical to honest corroboration (R2≡M4 honest pair; M1/M2b/M3 are majority-layer). No host function closes them without killing honest throughput. Kill bar: **7 false installs → FAIL** (bar unchanged).

**B3 (paraphrase):** 6 withhold + P3 install — matches V-BF1 exactly. Guard intact.

**B4 (throughput):** 12/12 honest installs (M4, M2a, M5, H1, H2, H3 × 2). Zero regression.

**B5 (determinism):** 52/52 rep-pairs byte-identical (modulo rep marker). Zero RNG in decision paths.

**B6 (regression):** 38 cases × 2 reps vs fresh V-BF1 baseline: exactly the 10 intended flips, 0 unexpected deltas.

**B7 (audit cost):** 12.2 vs 7.7 lines/log (+10/case: the EMIT\| host-key audit trail). Reported, not gated.

**B8 (consult extensions, parent-ordered):**

| Case | Attack | Result | Classification |
|---|---|---|---|
| C1 backslash | Parser-split grammar fork | INSTALL | RESIDUAL (documents WHATWG-vs-spec fork; fail-closed alternative would be to reject `\` in authority) |
| C2 scheme/port/www | Alias twins | WITHHOLD | KILLED |
| C3 query-@ | URL-parameter spoof | WITHHOLD | KILLED |
| C4 redirect | Attribution swap | WITHHOLD | KILLED (via final-URL attribution; requires fetcher to record effective URL) |
| C5 IP triple | Hex/dotted/v6-mapped | WITHHOLD | KILLED |
| C6 platform | github.io sybils | WITHHOLD | KILLED (conservative PSL fallback) |
| C7 CDN | Sibling edge hostnames | WITHHOLD | KILLED (eTLD+1: siblings are one origin per spec) |
| C8 dangling | Takeover serves on reputable subdomain | INSTALL | SURVIVES (needs DNS/cert observability) |
| C9 split-horizon | Same string, different A records | INSTALL | SURVIVES (needs IP+SPKI attestation; URL glue is DNS-blind by construction) |

**6 killed, 1 residual (C1), 2 survive (C8, C9)** — the survivors require provenance beyond URL spelling, as predicted.

## §A Required companion changes (prereg gap)

The prereg specified V-HARD as V-BF1 with exactly one semantic delta (fail-closed empty hosts). Implementing it exposed a latent dependency the prereg did not anticipate:

1. **G4/G5 calibrations were testing the buggy behavior.** Their calibration pages carry no `H|` lines. Under V-BF1 ("empty = distinct source") they installed; under V-HARD ("empty = zero sources") they cannot — so MIN-SOURCES never installs, the gate defaults to 1, and all 10 spoof classes install. The preregistered delta, alone, defeats the project's goal.
2. **The calibration harness stripped `H|` lines** (`run_calib` mode-2 accepted only `P|`/`S|`), making it impossible for any calibration to declare source hosts.

Companion fixes (minimal, documented, not bar-weakening):
- `webg_hard.zag`: preserve `H|` (byte 72) in calibration pages. Gate logic untouched. The full diff vs `webg_bf1.zag` is the preregistered delta + this harness line.
- Battery-local `battery/guides/g4_corroborate.txt`, `g5_provenance.txt`: calibration pages carry distinct `H|` hosts. These test the true principle (independent sources agreeing) and pass under both V-BF1 and V-HARD. Shared `guides/` untouched.

Without these, V-HARD is non-viable. With them, all batteries behave as the prereg intends.

## Residual risks & boundaries

- PSL is a frozen approximation (single-label + 16 multi-label entries); unlisted multi-label suffixes fall back to last-two-labels (may over-withhold, fail-closed).
- `norm` input capped at 1 MiB; `pages` capped at 64 pages / 512 sentences.
- C1 documents a real grammar fork: WHATWG parsers treat `\` as `/`; this pipeline treats `sockfarm.example\@evil.example` as userinfo-attack → `evil.example`. A stricter posture would reject `\` in authority outright.
- C8/C9 confirm URL glue cannot solve DNS-layer attacks.

## Build notes

- Compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned).
- `hostnorm.zag` → `hostnorm` (152,527 bytes); `webg_hard.zag` → `webg_hard` (244,468 bytes). Warnings only (ignored `nio_close`, conservative loop-bound notes).
- Zag rules obeyed: `[]u8` arenas + `p32`/`g32` (no `[]i32` casts), `.*` on pointers only, `_zag_strcmp==1` is equality, no bare blocks, `.field=` literals, no slice `==`, void `return;`.
- Two pre-existing znc behaviors worked around: string-concat type confusion (used `obuf_put`), `.*` on non-pointer segfault (audited).

## Commits

(To be filled after commit.)
