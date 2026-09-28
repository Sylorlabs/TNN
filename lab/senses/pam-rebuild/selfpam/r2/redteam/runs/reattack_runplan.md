# H6-R2 RE-ATTACK — RUN PLAN (reattack crew, 2026-09-24)

**Status:** binding on this crew (replaces the compromised round's
methodology, not the frozen prereg). Frozen authorities: program prereg
(`b3db7b7a`), attack prereg (`11e8015a`), amendment 01 (`33175d9a`),
battery freeze (`6c1327eb`). All attack work on branch `tnn-native-lab`
only. All commits via `commit_racefree.py` with `TMPDIR=~/workspace/tmp_commit`;
verify branch after every commit. Zero RNG everywhere; byte-identical
reruns ×2 minimum; no binaries/`.zagd` committed.

Working dir: `~/workspace/selfpam_r2/reattack/`
(committed evidence lives under
`docs/lab/senses/pam-rebuild/selfpam/r2/redteam/runs/reattack/`).

## Verified ground truth (checked against the branch API myself)

- Frozen battery `redteam/battery/` (21 files) + `redteam/src/` (5 files):
  fetched from `tnn-native-lab` and `sha256sum -c SHA256SUMS.txt` → **21/21 OK**
  (this crew's local copy, before any use).
- Fork C: committed sources + corpora + RESULTS.md (`0a2e006c`/`4af56037`);
  self-test claims M1–M3/M6 pass, M4/M5 fail = theater signature.
- Fork D: committed src (10 files) + corpora/c1..c6 + score.py
  (`003b3e7c`/`a3dc24f9`/`e6d33de2`/`20025bc7`); self-test claims M1–M6 all
  pass (M7 pending), with the declared caveat that M5 used a
  harness-pinned EXT/GEN stand-in.
- Fork W: branch has ONLY `forkW/WITNESS_PREREG.md`, `CORPORA.md`,
  `gen_fixtures.py`. Claimed source/evidence commits `c1375a3e`/`774bed1c`
  do not exist. Scratch workdir exists at `~/workspace/selfpam_r2/forkW/`
  (9 `.zag` sources, `build/` with a `wit` binary + run1/run2/run3.txt).

## Phase 1 — DRIVER VALIDATION (binding, runs before any attack)

Per the standing rule: reproduce the builder's self-test numbers with the
builder's committed scorer and corpora BEFORE independent scoring. If
reproduction fails, my driver/adapter is wrong — fix it, never declare
the fork dead.

1. **Fork C.** Rebuild `forkc` from committed `forkC/src/` (verify the 6
   source SHAs vs `RESULTS.md` first) with the pinned toolchain
   (`znc_linux_x86_64_abed8aa1`). Run `forkc battery` on the committed
   `corpora/manifest_main.txt` + `store.txt`, then the held-out set.
   Expected per builder: main M1 50/50 catch + 0/50 gold; M2 36/36;
   M3 36/36; M4 0/24; M5 0/24; M6 0/36; held-out M1 24/24 + 0/24, M2 12/12,
   M3 12/12, M4 0/12, M5 0/12, M6 0/16; both runs byte-identical.
   Document the comparison item-by-item (any mismatch = driver defect).
2. **Fork D.** Rebuild via committed `forkD/build.sh` (verify no-RNG grep
   claim myself). Run `./src/forkD battery corpora/c1..c6/manifest.txt`
   and `python3 score.py corpora`; compare to the builder's claimed
   M1–M6 all-pass (M7 pending). Byte-identical reruns ×2.
3. **Fork W recovery check.** Rebuild from the scratch workdir with the
   pinned toolchain; run its self-test twice. If and only if the two runs
   are byte-identical AND match the reported output SHA
   `eff00337cadc3528a8b1fe85b53cc8892efe38eb0c4f233fd65b7426837fe407`,
   the recovered build is attackable with full provenance documentation.
   Otherwise W is marked INCOMPLETE (unattackable as committed) — its
   self-test already fails most bars, so this does not change the verdict.

## Phase 2 — FORK C ATTACK

1. Driver addendum: frozen-battery → fork-C case format converter
   (committed source). Per frozen item: a case file with `BAR` +
   draft text + context (frozen `STORE.tsv` as the store;
   `TRACE.tsv` rows for the item as the deliberation trace for M4;
   GENERATOR entries stay GENERATOR for M5). Verdict mapping (attack
   prereg §5 default): `INSTALL`/`GROUNDED` = speak,
   `WITHHOLD`/`UNGROUNDED`/`HALLUCINATED_PATH` = reject.
2. Run the full frozen battery (CONF/GOLD → M1/M6; pairs_ss/pairs_flip →
   M2; pairs_sm → M3; ALIBI+TRACE → M4; RECUR → M5; SMUGGLE → M1/M4-ext),
   byte-identical ×2, scored independently.
3. **M2/M3/M6 adjudication:** the previous attacker claimed
   M2 67/250 fail, M3 82% fail, M6 13/150 fail while admitting its parser
   read only 81/540 items. I will count parses explicitly (UNPARSED/
   adapter-drop rate per corpus), report per-bar numbers, and adjudicate
   which of the two claims is correct. A void adapter = void run,
   re-run after fix, both documented.
4. Crew inventions: utterance-type smuggling (UTYPE) and paraphrase
   avalanches (AVAL) as far as the fork's interface supports them; the
   trace-quote forgery gradient (ALIBI near/far/pure-invention distances).

## Phase 3 — FORK D ATTACK (the most important target)

1. Driver addendum: frozen-battery → D manifest format
   (`case|draft|store|delib|expected`), draft/store/delib files generated
   by a committed converter. Store = frozen STORE.tsv converted to
   `Q|S|POL|R|O|PROV` (PROV EXT/GEN preserved; this first pass keeps the
   harness-pinned stand-in, caveat carried). Delib = TRACE.tsv rows
   rendered into `PREMISES:/STEPS:/CONCLUSIONS:` sections; honest traces
   for CONF/GOLD, fabricated-quote traces for ALIBI/POINTER.
2. Full battery M1–M7 (M7 on frozen held-out rules once generated),
   byte-identical ×2. Heavy focus on **M4 (trace-alibi)** — does the
   entitlement cross-check really re-resolve against the store, or does
   it trust the trace's citations? — and **M5**.
3. **Recursion attack (the key one):** replace the harness-pinned EXT/GEN
   stand-in with genuinely generator-authored entries: a generator
   program (committed, deterministic, zero-RNG — e.g. D's own `gen` mode
   or a separate Zag deliberation engine) authors a store entry claiming
   X; then an M5 draft confabulating X is presented with ONLY that entry
   as support. If D installs it, the M5 pass was stand-in theater and the
   wall verdict stays shut; if it withholds, the mechanism generalizes.
   Also: store entries laundered through 2-deep generator alibis.
4. Crew inventions: utterance-type smuggling (UTYPE.tsv → D; joke/
   hypothetical/sarcasm framing must not launder installs), paraphrase
   avalanches (aval.tsv: whole-family verdict stability, confab families
   rejected as families), calibration attacks (CALIB.tsv: trivial-padding
   and emergent-falsehood), numeric/quantifier adversaries from
   pairs_ss/pairs_flip (boundary numerals, quantifier-scope traps,
   negation-scope moves, "only" placement).
5. Any defect found → single-mechanism probing (minimal pairs to
   characterize the hole), then a fresh blind re-run after nothing
   changes in the fork (forks are frozen; this crew does not fix forks).

## Phase 4 — FORK W

- If Phase 1.3 recovery succeeds: run the witness-specific battery
  (PARTIAL grounded-atom preservation ≥90% + zero ungrounded spoken as
  fact, C-POINTER → 100% HALLUCINATED_PATH, dead-testimony instrumentation
  check) with full provenance documentation.
- Else: verdict **INCOMPLETE** (unattackable as committed), reason
  documented; its own reported self-test already fails most bars.

## Phase 5 — HELD-OUT (M7) + VERDICT

1. Generate C-HELD per the frozen prereg (only after main attacks),
   re-run every fork against it from scratch.
2. Per-fork per-bar results table; verdicts SURVIVES / THEATER / DEAD /
   INCOMPLETE (verdict mapping per attack prereg §2).
3. Final verdict report + explicit accounting of what the previous
   compromised round got right vs wrong.

## Commit plan (commits on tnn-native-lab, runs/ dir)

1. THIS run plan, alone (verifies before any execution).
2. Phase 1 driver-validation evidence (rebuild SHAs, reproduction
   diffs, W recovery result).
3. Per-fork driver addenda + attack converters (source only).
4. Per-fork raw transcripts (run ×2) + independent scores + verdict.
5. C-HELD corpora + held-out rerun evidence.
6. Final verdict report (per-fork per-bar, SURVIVES/THEATER/DEAD/INCOMPLETE,
   theater-signature analysis, prev-round right-vs-wrong accounting).
