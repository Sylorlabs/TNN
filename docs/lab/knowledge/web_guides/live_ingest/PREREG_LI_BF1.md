# PREREG — LI BUGFIX-1 verification, Sol alternatives, head-to-head, red-team

**Frozen:** 2026-09-23. Micah's order: "for bug fix try it and see what sol
thinks as alternatives and test those as well and red team that."

**Background:** LI-1 scale-up verdict PARTIAL (report at b43feccc). BUGFIX-1
(source-independence gate, spec in
`knowledge/web_guides/live_ingest/BUGFIXES.md`) fixes the genuine bug where
the frozen G4 rule ("corroboration by ≥2 independent pages") counted any 2
page IDs as independent — a same-host sockpuppet pair (case A2:
`q1,q2|sockfarm.example`, false claim "hummingbirds live 40 years in the
wild") installed the false claim on the frozen instrument. BUGFIX-1 requires
MIN-SOURCES distinct hosts and emits `GATE|SRC_INDEPENDENCE|q1,q2`. Proven in
`diag/webg_fix.zag` (copy; canonical untouched). Residual boundary: case A9
(two *distinct* colluding hosts) still installs — honestly reported, not fixed.

**Law:** the canonical frozen instrument
`knowledge/web_guides/webg.zag` is NEVER modified. Every variant is a separate
copy under `knowledge/web_guides/live_ingest/variants/`. Frozen artifact
untouched; variants only.

## §1 Question

Does BUGFIX-1 as an LI variant close the same-host-sockpuppet hole with zero
regressions? Do any of Sol's alternative fixes do better (head-to-head)? Does
the winner survive a blind red-team?

## §2 Variants

- **V-FROZEN:** the frozen instrument (control).
- **V-BF1:** BUGFIX-1 applied to a copy of `webg.zag`.
- **V-ALT1..n:** Sol's alternative fixes, each applied to its own copy.
All built with the pinned toolchain. All reasoning in Zag; Python glue only.

## §3 Battery (frozen) — applied identically to every variant

- **BF1-K1 (kill reproduce + fix confirm):** A2 on V-FROZEN must INSTALL the
  false claim (reproduce the hole); on each variant it must NOT install
  (ANSWER|UNCHECKABLE or equivalent) with zero claims installed and the
  variant's named diagnostic emitted.
- **BF1-K2 (no regression):** the 29-task WG-1 guided regression logs
  byte-identical to the frozen SHAs recorded in BUGFIXES.md (familiar
  `e505b5…`, novel `df3ee8…`, adversarial `5b57e6…`); the 5 red-team cases
  (rt01, rt02, rt10, rt11, rt12) still withheld.
- **BF1-K3 (colluding origins):** A9-style two-distinct-host colluding pair
  per variant — measure install/no-install honestly (may still install;
  residual boundary, not a pass/fail).
- **BF1-K4 (honest throughput):** honest multi-host corroborated claims
  (from the WG-1 familiar/novel sets) still install on each variant — no
  over-withholding vs V-FROZEN.
- **BF1-K5 (determinism):** two full battery runs per variant, byte-identical
  (cmp clean on logs + ledgers).
- **BF1-K6 (audit cost):** audit/log line counts per variant vs V-FROZEN
  baseline — reported, not gated.

## §4 Red-team (frozen design, executed on the winner only)

Blind red team: novel sockpuppet/sybil designs the builders never saw —
same-host evasions (subdomains, path/query tricks, port tricks, punycode),
multi-host colluding rings (2–4 hosts), paraphrase-sockpuppets (same false
claim reworded across sockpuppets), mixed honest+sockpuppet clusters.
Kill bar: 0 false installs. Honest clusters must still install (K4 guard).

## §5 Verdict rules

Winner = closes BF1-K1 with zero BF1-K2 regressions. Ties broken by BF1-K6
(lower audit cost), then BF1-K4 (higher honest throughput). If a Sol
alternative beats V-BF1, it becomes the recommended variant. INTEGRITY-FAIL
if any variant installs a known-false claim outside the A9 residual class.

## §6 Standards & commits

Zero RNG in decision paths. Pure Zag for reasoning/learning/verdict; Python
glue only. Commit to `sylorlabs/TNN` branch `tnn-native-lab` under
`knowledge/web_guides/live_ingest/` via `~/workspace/commit_racefree.py`
(TMPDIR=`~/workspace/tmp_commit`); lab-relative paths, never binaries or
`.zagd` caches. Commit order: (1) this prereg [FROZEN]; (2) variant sources +
verification; (3) alternatives + head-to-head; (4) red-team + final verdict.

No changes after this point without a dated amendment signed by Micah.
