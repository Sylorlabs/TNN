# RUNLOG R-36 — repair crew R-36 chronological log (2026-09-24 PDT)

All times PDT. Repo: sylorlabs/TNN, branch tnn-native-lab.
Local staging: ~/workspace/tnn-lab/senses/pam-rebuild/round2/r36_repair/ → docs/lab/…

- 17:33 — Read backlog H-PAM-36 (line 91), RT-JKLM verdict, original probe
  source, native substrates. Drafted PREREG_R36.md in staging dir.
- 17:33 — Committed PREREG_R36.md ALONE via ~/workspace/commit_racefree.py
  (TMPDIR=~/workspace/tmp_commit). Commit 506fc0927100e76b3d1c00874dfe42239c6bef63
  (parent 66762be7dee9). Prereg frozen before any repair code existed.
- 17:35 — Computed evidence material =
  SHA256("R36-SEED-MATERIAL:" || prereg_commit_sha)
  = bd1b7914f731ac24c0823828702f642ef45807fe90b230f81fe13444f554ee73.
- 17:35 — Wrote r36_harness.tmpl (scratch, uncommitted): frozen H-36 core fns
  verbatim, transcript seed derivation (R36-S1), file-backed reuse detector
  (R36-S2), batt + m36 modes, marked M36-ATTACKER-CLASS fixture block.
- 17:36 — Wrote gen_r36.py: extracts run_m seed/trials/idbase from
  rt_jklm/drive36.zag by regex, asserts (305419896, 2596069104) / 120 / 8000,
  substitutes into template → r36_probe.zag. First extraction: no drift.
- 17:38 — First build with znc (cwd = scratch dir, substrates mirrored).
  Success + 1 analyzer warning A0107 (dead loop in ledger_add) — analyzed as
  false positive (assignment-to-bound misread as decrement).
- 17:39 — Wrote run_r36.py; first battery: batt 3× identical, m36 3×
  identical, reuse detector refused loudly (rc=1). All bars PASS, M-36 0/120.
- 17:40 — Independent cross-check (verify_r36.py): Python SHA256 of the
  transcript matches the probe's ns_sha256 in both modes; Python reimplementation
  of the FNV mechanism expects 0/120 M-36 installs. Both confirm.
- 17:41 — WG3 audit (wg3_r36_audit.sh) first run: DIRTY — (a) old seed digits
  in the GENERATED header comment, (d) ns_sha256 counted inside comments.
  Fixed template header (placeholder NAMES, not values) and audit (strip //
  comments before counting). Regenerated, rebuilt.
- 17:42 — WG3 audit: CLEAN. Full battery re-run on final source with fresh
  ledgers: batt 3× byte-identical (8c75d6677d14e580…), m36 3× byte-identical
  (d43b6d3913bd216f…), reuse refusal rc=1. All bars PASS.
- 17:43 — Wrote VERDICT_R36.md + RUNLOG_R36.md. Staging evidence under
  senses/pam-rebuild/round2/r36_repair/: generated source, gen/run/verify/audit
  scripts, substrate copies, runs/ outputs + SHA256SUMS, verdict, runlog.
  Excluded: r36_probe binary, .zagd, ledgers, __pycache__.
- 17:44 — Committed evidence (single commit after the prereg-alone commit) via
  commit_racefree.py. Updated hypothesis_backlog.md H-PAM-36 → TESTED-survived
  (repaired).
