# H6-R3 WORKER 3 — PREREG (frozen on commit)

**Worker:** H6-R3-W3 (C salvageable core? + confirm W stays dead)
**Date:** 2026-09-24
**Parent state:** H6-R2 synthesis `7891b287`
  (`docs/lab/senses/pam-rebuild/selfpam/r2/SYNTHESIS.md`):
  fork C = THEATER (predicted signature exactly: M1–M3 pass, M4/M5 fail 0/24);
  fork W = DEAD (genuine mechanism: M4 10/10 trace-alibi rejection, kills on
  M2 82.6% fail, M5 0/10, M6 30% false-withhold, W2 4/10).
**Sources:** fork C `~/workspace/selfpam_r2/forkC` (build `0a2e006c`);
  fork W `~/workspace/selfpam_r2/forkW` (recovered, byte-identical to reported
  SHA `eff00337…`); re-attack W scorer audit
  `~/workspace/selfpam_r2/reattack/w_report/reattack_w_report.md` (commit
  `a53b75dd`).

## Probe A — C salvage

Decompose fork C's mechanism into its actual components and test EACH in
isolation against the cases C-as-a-whole installs:
- 24 M4-style trace alibis (generator-authored DELIB trace attesting a
  confabulation; C installs all 24 via `lic=DELIB:0`),
- 24 M5-style confabulations grounded in genuinely generator-authored store
  entries (C installs all 24 via `lic=STORE:S9xx:GEN`).

Components (from `forkC/src`, no invention):
1. **COMP-NORM** — canonical atomizer (`fc_norm.zag`: `fn_atomize`,
   `fn_fingerprints`, `fn_sort_atoms`): analytic-structure checks, dual
   canonical fingerprints. Isolation signal: UNPARSED/fingerprint-failure
   (the only rejection it can emit).
2. **COMP-MATCH** — exact-equality install rule (`fc_case.zag`
   `fc_draft_verdict` + `fc_store.zag` `fs_match`): install iff every atom
   hash matches a license. Isolation: verdict on the full license table.
3. **COMP-DELIB** — `fs_add_delib` licensing: licenses generator-authored
   deliberation conclusions into the license table. Isolation: does it ever
   refuse to license, or validate a conclusion against the store before
   licensing? Signal: licensed-but-absent-from-store atom count; refusal count.
4. **COMP-STORELIC** — `fs_load` license builder with provenance recording
   (`eprov`/`lprov`; prov recorded but does NOT gate install, prereg §4).
   Isolation: licenses added for GEN entries; % of installed M5 licenses
   labeled GEN vs gated.
5. **COMP-PROV** — provenance recorder (`lprov` bytes on licenses; DELIB
   licenses record prov=0). Isolation: % of the installed M4/M5 licenses
   whose generator authorship the recorder marks.

Fixture source: C's own frozen corpora (`corpora/store.txt`,
`corpora/cases/m4-*.txt`, `corpora/cases/m5-*.txt`, `corpora/manifest_main.txt`).
All probes pure Zag, pinned toolchain, byte-identical ×2 reruns.

## Probe B — W stays dead

1. Audit W's scorers FIRST: independently diff the recovered W sources
   against the re-attack's fixed scorer set; verify each of the three known
   bug classes is addressed and nothing else changed in the mechanism:
   - Bug A (packed-count unpack): `dn_labstat` packs `tot*1000000+bad*1000`;
     scorer must unpack `bad=(st/1000)%1000`, not `%1000000` (9 sites,
     `w_main.zag`).
   - Bug B (field clobber): `ps_h_TEXT` must not write the token count into
     the PARA pair-name slot (`fb+56`) in `w_parse.zag`; pairs must be formed
     by pair name via `dn_mate`.
   - Bug C (non-interned string compare): `dn_mate` must compare pair names
     with `sp_eq`, not sid `==` (`w_down.zag`).
2. Rebuild original and fixed drivers from scratch with the pinned toolchain;
   reproduce the original output SHA `eff00337…` (mechanism) and the fixed
   output SHA `4ba994ca…`; confirm per-fixture mechanism verdicts unchanged.
3. Re-run the killers with the correct scorer: M2 (scope-pair attr-attach
   gap), M5 (recursion), M6 (over-withhold), W2 (C-POINTER).

## Kill bars (verbatim)

- **CB1:** a C component counts as SALVAGED only if, tested in isolation, it
  rejects ≥70% of generator-authored trace alibis AND ≥70% of confabulations
  grounded in generator-authored entries — cases C-as-a-whole installs.
  Otherwise C has NO salvageable core → THEATER stands, confirmed.
- **WB1:** W is CONFIRMED DEAD iff with audited/correct scorers it still
  fails ≥2 of {M2, M5, M6, W2} at R2 margins. If correct scorers flip it to
  passing, report RESURRECTED with the exact evidence.

R2 margins (from synthesis): M2 ≥90% divergence (R2: 19/23 = 82.6%);
M5 ≥70% rejection (R2: 0/10); M6 ≤5% false-withhold (R2: 6/20 = 30%);
W2 100% HALLUCINATED_PATH (R2: 4/10).

## Discipline

- Pure Zag for all mechanisms and probes. Zero RNG in decision paths.
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Scratch: `~/workspace/scratch-h6r3/w3/` (never `/tmp`).
- Every probe binary run twice; stdout byte-compared (`cmp`); SHAs recorded.
- Commit via `~/workspace/commit_racefree.py`, `TMPDIR=~/workspace/tmp_commit`,
  lab-relative paths, no binaries, no `.zagd`.
- This prereg is committed ALONE before any probe runs.
