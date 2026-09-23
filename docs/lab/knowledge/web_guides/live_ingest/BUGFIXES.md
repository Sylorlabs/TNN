# LI-1 Bugfixes

Diagnoser: LI-1 refusal loop (subagent), 2026-09-23.
Law: reasoning changes pure Zag, zero RNG, byte-identical reruns preserved.
The coordinator commits; canonical `knowledge/web_guides/webg.zag` was **not modified**
by this diagnoser. Nothing below was committed by the diagnoser.

## BUGFIX-1 (candidate, proven, NOT adopted): source-independence gate

**Genuine bug.** The frozen rule (§4/G4) requires corroboration by "≥2 independent
pages", but the instrument counted any 2 page *IDs* as independent — two pages
from one origin (same host/operator) satisfied the bar.

**Proof of misfire (before):** hand-built red-team case A2 (same-host sockpuppet
pair `q1,q2|sockfarm.example` asserting byte-identical false claim "hummingbirds
live 40 years in the wild"):
- Frozen binary: `ANSWER|ruby-throated hummingbirds live 40 years in the wild.`
  — the false claim **installed** from one origin counted twice.

**Fix (pure Zag, in `diag/webg_fix.zag` — a copy; canonical untouched):**
- Optional `H|host` metadata line per page in `pages.txt` (glue derives it from
  the URL via `urllib.parse`; formatting only, no reasoning).
- Corroboration now requires `MIN-SOURCES` **distinct hosts**; new exact
  diagnostic `GATE|SRC_INDEPENDENCE|q1,q2` when the winning cluster collapses to
  one host.
- Backward compatible: legacy pages without `H|` each count as their own host,
  so all old behavior is preserved byte-for-byte.

**Proof of fix (after):** same A2 case on the fixed binary
(`/tmp/webg_fixed`, built with the pinned toolchain):
- `ANSWER|UNCHECKABLE` + `GATE|SRC_INDEPENDENCE|q1,q2`, zero claims installed.

**No-regression proof:** the fixed binary reproduces the full 29-task WG-1
guided regression logs **byte-identically** (full-log SHAs, re-verified
2026-09-23):
- familiar: `e505b5216f5e63a01454a42d42bdf1001ae4d28adf56b73a1d0c3f6a47c25a7e`
- novel: `df3ee8a4c744276a2cdc068ef4ee18c2777dd32c744aad3bd94e679efb43391d`
- adversarial: `5b57e660fb5cc8b6d390b9864b5d3be4e48c66a015310f0ea15aca30df53d5c3`
- Per-task FLAG/ANSWER/CLAIM/UNCHECKED lines identical on all 29 tasks.

**Determinism proof:** two full fixed red-team reruns byte-identical
(including `run_li.log` SHAs).

**Status / handoff:** candidate only. Adopting it requires the coordinator to
apply the `webg_fix.zag` diff to canonical `webg.zag` (or point the pass at the
fixed build) **and** keep the `H|` emission in `run_li.py` (already present).
Until adopted, the pilot/training passes run with the K4 hole open.

**Residual boundary (NOT fixed, reported honestly):** case A9 — two *distinct*
hosts under colluding control asserting the same false claim — still installs
on the fixed binary (1 attack success, see REDTEAM_REPORT.md). Host diversity
cannot establish true operatorship independence; no mechanism available to the
loop can distinguish a colluding pair from genuine independent corroboration.
LI-K4 is not satisfied against this adversary class.

## BUGFIX-2 (glue, applied to `run_li.py`, behavior-preserving): host metadata + gate capture

- `host_of(url)` via `urllib.parse` (lowercased hostname; formatting only) and
  `H|<host>` line emitted per page into `pages.txt` (lines ~27, ~232).
- `GATE|` lines (e.g. `GATE|SRC_INDEPENDENCE|…`) captured into the
  NO_CORROBORATION refusal reason for diagnosability (lines ~263–266).
- Verified behavior-preserving with the frozen binary: frozen `parse_pages`
  ignores `H|` lines; pilot `run_pass1`/`run_pass2` verdicts confirm no output
  change. Required glue half of BUGFIX-1 if adopted.

## BUGFIX-3 (crew glue fix, verified by this audit): URLMISMATCH attribution

- The pilot crew hardened `run_li.py`: when the manifest URL for a pid differs
  from the fetch-status URL, the fetch-status URL wins (the snapshot's bytes are
  authoritative) and the mismatch is logged as
  `%s|URLMISMATCH|%s|manifest=%s|snapshot=%s` (line ~147).
- Verified: code path correct; 0 mismatches across all 21 fetch-status lines in
  `corpus_snap/` and `corpus_snap_full/`; no URLMISMATCH lines in either pilot
  log (fix live, inert-but-correct). Not a diagnoser fix — crew-authored, audit-verified.

## Explicit non-bugs (investigated, no fix)

- **Paraphrase-fragmented corroboration** (all 7 pilot NO_CORROBORATIONs):
  adjudicated LEGITIMATE WITHHOLD — see WITHHOLDS_JUSTIFIED.md. No
  byte-identical cross-host sentence exists anywhere in the 7 clusters (proven
  over all sentences, instrument-exact normalization, plus punctuation-stripped
  re-check), so no sentence-selection fix could install them; installing them
  would require a semantic-similarity threshold that weakens the ≥2-source rule
  and re-opens paraphrase-sockpuppet attacks.
- **Diagnoser probe bugs** (mine, not the loop's): `diag/diagnose.py` initially
  assumed a generic ledger layout and omitted the 7th `verdict` arg (the query),
  producing empty replays. Both fixed in the probe; the loop was never at fault.
- **GUIDES path confusion** (mine, caught before harm): I briefly misread
  `run_li.py`'s `PARENT`/`HERE` computation and "fixed" a non-bug; reverted.
  The crew's driver was correct.
