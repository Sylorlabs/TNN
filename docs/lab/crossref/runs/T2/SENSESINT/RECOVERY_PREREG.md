# T2-SENSESINT EVIDENCE RECOVERY — PREREG (FROZEN 2026-09-23)

**Recovery coordinator:** Wave-2 crossref T2-SENSESINT evidence recovery (parent task
858a4692-2e87-41c5-b03a-ff81c7398a64).
**Authority:** `docs/lab/crossref/runs/T2/_closeout/CLOSEOUT_WAVE2.md` §3 (T2-SENSESINT
EVIDENCE RECOVERY PLAN, committed on branch `tnn-native-lab`); frozen Tier-2 prereg
`crossref/PREREG_TIER2.md @ 7b2100d09911c5c10252c5756c7def288e70bd1f` — T2-SENSESINT
section (Type C, rule: **REPRODUCED if 140/140 re-derives; PARTIAL if any item's
evidence is missing (name it)**).
**Standing law:** pure Zag; zero RNG in decision paths; byte-identical reruns;
commits to `sylorlabs/TNN` branch `tnn-native-lab` only via
`~/workspace/commit_racefree.py` with `TMPDIR=~/workspace/tmp_commit`; lab-relative
paths not starting with `docs/lab/`; never commit binaries or `.zagd`.

## Gap under recovery (verified 2026-09-23, genuine HTTP 404s at current head)

- 3 P0 (load-bearing): `senses/web-search/v2/src/gk1_trial.zag` (manifest size 5285),
  `gk2_trial.zag` (6329), `gk3_trial.zag` (4235) — trial sources behind "H1, H2, H3 all
  SUSTAINED" and headline digests `488af9ab…` / `7f351a53…` / `94575a9a…`. The `v2/src/`
  listing at head shows only `ws2_*` files — independently confirmed.
- 7 P2 (review-note): `senses/web-search/internet-trial/evidence/phase1/*.jsonl`
  (blind-solo 11986, captured-solo 11992, corrupt-solo 11990, gullible-solo 11994,
  idle-solo 472, oracle-helper 12687, oracle-solo 11989) — directory at head contains
  only `SMOKE_TEST.md`.
- 2 stale manifest sizes (record-integrity, not missing evidence):
  `senses/rematch/code/kb5.py` manifest 2189 vs committed 2731;
  `senses/rematch/code/run_all.py` manifest 4302 vs committed 5801.

## Recovery rules (frozen — no tuning permitted)

### R1 — GK1/GK2/GK3 sources (3 P0)
Recover from the frozen crew workdir `~/workspace/grok47/senses/gk-scratch/`
(`gk1_trial.zag`, `gk2_trial.zag`, `gk3_trial.zag`) — **restore, not regenerate**:
the workdir copies are the crew's frozen artifacts (sizes match the manifest
byte-for-byte: 5285/6329/4235), and git history shows **zero commits ever** for
these paths on `tnn-native-lab` (they were never committed, only workdir-resident),
so there is no earlier blob to prefer. Restore counts as REPRODUCED-eligible only if
ALL of the following hold:
  (a) restored bytes are byte-identical to the workdir copies (sha256 recorded);
  (b) sources build clean with the pinned toolchain
      `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` against the
      committed frozen v2 sense (`ws2_sense.zag` at head);
  (c) N=3 reruns are byte-identical to each other AND re-derive the headline digests
      byte-for-byte: GK1 `488af9ab375eae17cf65015240fb5c8a2f111ed6ca2eee354778b12b74a0db5c`,
      GK2 `7f351a53524d67fdb182357dcbf0215af526a6b70d7f6d66ce008d0c301fdf4b`,
      GK3 `94575a9a6c9e4aaa916676b6301a57d643c65f28d51d748f36492ac359814d13`;
  (d) ZERO edits to the sources — no tuning to hit the digest. If (c) fails for any
      trial, the coordinator reports it plainly and the track STAYS PARTIAL.
Kill bars carried over from the frozen GK preregs (F1–F7/G1–G8/K1–K5: refusal
refutations, tamper≠0, non-identical reruns) remain in force on the recovery runs.

### R2 — P2 jsonl (7, review-note)
Recover from workdir `~/workspace/tnn-lab/senses/web-search/internet-trial/evidence/phase1/`
(byte sizes match manifest exactly; git history shows zero commits ever for these
paths). Recovery counts only if every line parses as valid JSONL. If any jsonl is
unrecoverable, the coordinator formally DOWNGrades it: a written justification is
committed alongside the recovery verdict, the manifest item's verdict is marked
downgraded (not done), and the track may still upgrade (P2 items are review-note,
not load-bearing — per the closeout's committed plan, formal downgrade is an
accepted path).

### R3 — stale manifest sizes (2)
Amend `docs/lab/GROK47_OVERNIGHT/senses-integrity/ITEMS_DONE.tsv` size fields
(kb5.py 2189→2731, run_all.py 4302→5801) ONLY after independently verifying that the
committed bytes at current head AND at the pinned rematch commit `1c01a1ad` are
exactly 2731/5801. The committed bytes are the live revision; the manifest measured
stale revisions. Amendment is documented in the recovery verdict.

## Timeline honesty note
Scratch verification (build + N=3 runs in `~/workspace/t2-sensesint-recovery/v2mirror/`,
uncommitted) was performed BEFORE this prereg was written, as evidence-gathering
for the honest bar: all three headline digests re-derived byte-identically with zero
source edits. The rules above were fixed from the manifest, the closeout plan, and
the frozen prereg — not shaped by that outcome. The committed recovery runs in §3
repeat the verification from the committed sources.

## Commit sequence
1. This prereg ALONE (`docs/lab/crossref/runs/T2/SENSESINT/RECOVERY_PREREG.md`).
2. GK sources at the exact manifest paths.
3. The 7 phase1 jsonl at the exact manifest paths.
4. Amended manifest (2 size corrections).
5. `RECOVERY_VERDICT.md` (what was regenerated vs recovered vs downgraded, digest
   comparisons, commit SHAs, limitations) + amended `VERDICT.md` (PARTIAL →
   REPRODUCED on success; stays PARTIAL with named missing items on failure).

## Upgrade rule
T2-SENSESINT upgrades to REPRODUCED iff, after steps 1–5, all 140 manifest evidence
paths resolve at head (10 restored + 2 size-corrected + 128 verified intact) and the
3 headline digests re-derive byte-for-byte from the committed sources. Otherwise the
track stays PARTIAL and the verdict names exactly what is missing.
