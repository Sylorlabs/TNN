# exp2d — Independent Red Team Report

**Date:** 2026-09-28 (UTC)
**Attacker posture:** attack every claim from evidence alone; confirm nothing on trust.
**Base commit attacked:** `8779a026580c1ceb6efe2372506039b4d818b3db`
("exp2d runs of record: battery outputs, SHA manifest, bar table, C3 whitebox")
**Scope:** `docs/lab/epistemics/utterance_types/exp2d/` — all claims in
`REPORT.md`, `bartable.md`, `PREDICTIONS_LOCKED.md`, `C3_WHITEBOX.md`,
`AMENDMENT_EXP2D_2026-09-27.md`, `AMENDMENT_ADOPTION_BETA_2026-09-27.md`.

**Method:** every attack below was executed, not argued. New tools were written
from scratch in `redteam/` (independent implementations of scoring, firing,
overlap, and provenance logic). Live counterfactuals were run with a freshly
compiled binary built from the committed source with the pinned toolchain.
Zero randomness in every decision path; every write verified by byte comparison.

---

## Verdicts

| # | Claim | Verdict | One-line reason |
|---|-------|---------|-----------------|
| 1 | "All 9 pre-registered predictions confirmed exactly" | **KILL** | Locked `abc2-a` WD = 10/10; actual run = 0/10; `bartable.md` mislabels the row "Pred match? YES" |
| 2 | Cleaned A+B / β+C T3 bars (ab2 9/9, abc2-b 10/10), "zero new official bar failures" | **HOLD** (qualified) | Scores independently re-derived; tightened-threshold near-duplicates exist (cc01/cc05) but live removal changes nothing |
| 3 | β+C / v96 T3 LK 10/10 genuine (not carried by duplicates) | **HOLD** (qualified) | cc40 replacement clean; cc01/cc05 removal → LK unchanged |
| 4 | Novel-family WI 0→10 on D/E legs (official probes) | **HOLD** (raw numbers) / **QUALIFIED** (interpretation) | Official 10/10 reproduces, but fresh-probe attack drops de2-b WI to 4/10: the revocation is construction-bound, not family-general |
| 5 | WD 10/10 on corpus legs | **HOLD** (mechanism) / **CONFOUNDED** (as labeled) | Live cc19-removal proves the single item carries WD 10/10 → 0/10 |
| 6 | C3: exactly 4 official probe misses from 3 support-1 markers | **HOLD** | Independent delta analysis reproduces the bound exactly |
| 7 | 30 runs byte-identical across reps; empty mode reproduces frozen SHA | **HOLD** | Manifest SHAs, rep-identity, and frozen SHA all re-verified; independent rebuild reproduces committed outputs byte-for-byte |
| 8 | HARD0: zero new type-name hardcodes in exp2d source | **HOLD** | 11 scanner hits, all false positives, identical set in frozen exp2c |
| 9 | Source provenance: committed `h7_exp2d.zag` = assemble(frozen `h7_main.zag`) | **HOLD** | Byte-identical reproduction of the assembly step |

---

## KILL-1 — The "all 9 predictions confirmed exactly" claim is false

`PREDICTIONS_LOCKED.md` (frozen 2026-09-27), x2c table, row for `abc2-a`:

> `| abc2-a | 0/10 | 10/10 | wi FAIL, wd PASS |`

The locked prediction for `abc2-a` WD is **10/10**. The actual run of record:

> `X2C_CURVE|3|WD|0|N|10`  (from `runs/abc2-a_rep1.txt`; all 3 reps identical)

WD is **0/10**, not 10/10. The independent re-derivation (`redteam/rederive.py`,
`redteam/rederive.log`) flags exactly one mismatch against the locked
predictions: `PRED-MISMATCH ('abc2-a', 'WD', 'X2C', 10, 0)`.

Worse, `bartable.md`'s x2c table reports the actual 0/10 but labels the row:

> `| abc2-a | 0/10 | 0/10 | YES |`

"Pred match? **YES**" is false: the prediction was 10/10. The table silently
absorbs a falsified prediction.

**Mechanism of the miss** (white-box, confirmed): the prediction's basis note
assumes cc19's revocation of the `where do` marker works in the α design. It
does not — in `abc2-a` the α design learns `joke` markers `evenly` /
`says evenly` (support 1) that fire on every probe (all probes use ctx
"says evenly"), so every probe is withheld as joke regardless of `where do`
status. Firing analysis on `runs/abc2-a_rep1.txt`:

> `abc2-a wd: withheld 10/10; top markers: [('joke', 'evenly', 10), ('joke', 'says evenly', 10)]`

The prediction was derived from "exact MDUMP reconstructor run on committed
exp2c MDUMP" — i.e., not from the exp2d α MDUMP that actually ran. The α leg
is the designated failing control, so this does not touch β's results; but
the exact-prediction claim and the bartable's match label are dead.

**What survives:** the other 8 x2c predictions, all 2c DP/LK predictions, and
all 3 C3 collision predictions match the runs exactly.

---

## HOLD-2/3 — Cleaned-corpus bars (C1)

**Official-threshold dedupe (independent scanner, `redteam/c1_attack.py`):**
final cleaned corpora (`cal2_ab`, `cal2_abc`, `cal2_de`, `cal2_vol2`) vs all
curriculum, all sincere probes, and both X2C probe files, at the user's
stated C1 rule (16-byte overlap, shared word 4-gram, word-3-gram Jaccard
≥ 0.60):

> **Zero flags** at official thresholds across all corpora and all targets.
> (`redteam/c1_attack.log`)

**Tightened thresholds** (12-byte overlap, shared word 3-gram, Jaccard ≥ 0.50)
do find near-duplicates the official rule misses — e.g.:

- `cc01` "Ask if the clinic accepts new patients." ↔ `si3_14` "Ask if the shop is open." (shared 3-gram "ask if the")
- `cc05` "See if the upstairs window is shut." ↔ `si3_16` "See if the door is locked." (shared 3-gram "see if the")
- 6 tightened flags in `cal2_ab` vs sincere probes; 8 in `cal2_abc`; 0 in `cal2_de`; 10 in `cal2_vol2`.

**Live score-carrying test (the attack that matters):** removed `cc01` and
`cc05` from `cal2_ab.txt` / `cal2_abc.txt` and re-ran the adopted legs with
the independently built binary:

- `ab2-b` minus cc01/cc05 → T3 `DP|9|LK|9` (unchanged from 9/9)
- `abc2-b` minus cc01/cc05 → T3 `DP|9|LK|10` (unchanged from 10/10)

(`redteam/c1_counterfactual.log`)

The tightened near-duplicates carry **zero score points**. The C1 claim holds
under its stated rule, and survives the tightened attack live. Qualification
recorded: the near-duplicates exist and should stay disclosed; they are
provably inert.

Related: `cc40`'s replacement ("It is too dim to read the timetable.") shows
no tightened sincere-probe flag — clean.

---

## HOLD-4 (qualified) — Novel-family WI; fresh-probe attack

**Raw official numbers hold.** Independent re-derivation confirms
`de2-a`/`de2-b` WI = 10/10, WD = 10/10; all non-D/E legs WI = 0/10.
Firing analysis confirms the mechanism: the `hypothetical:'what if'` marker
withholds 10/10 wi probes on base/ab2/abc2/v96 and is revoked (MDUMP status 3)
in de2.

**Fresh-probe attack (independently authored, zero 16-byte overlap with any
training/curriculum/probe text — verified in `redteam/fresh_wi.txt`,
`redteam/fresh_wd.txt`):** 10 fresh WI (5 nominalized "the what ifs"-style +
5 literal interrogative "What if the …?") and 10 fresh WD, run live through
base, abc2-b, de2-b:

| Leg | Fresh WI | Fresh WD |
|-----|----------|----------|
| base | 0/10 | 0/10 |
| abc2-b | 0/10 | 10/10 |
| de2-b | **4/10** | 10/10 |

(`redteam/fresh_probes_x2c.log`)

**The WI "family" does not generalize as claimed.** Per-probe white-box on the
de2-b MDUMP:

- Endorsed (4): the nominalized probes that avoid other live markers.
- Withheld (6):
  - all 5 literal interrogatives ("What if the causeway flooded by
    morning?" …) → fired by `hypothetical/sup1:'what if the'` **and**
    `hypothetical/sup1:'if the'`;
  - 1 nominalized probe ("At dawn the crew ran what if drills.") → fired by
    pre-existing `quotation/sup1:'at dawn'` (probe-design confound, not a D/E
    failure).

MDUMP status check (`runs/de2-b_rep1.txt`):

> `MDUMP|3|0|3|1|what if` — revoked (status 3)
> `MDUMP|3|0|1|1|what if the` — **still live** (status 1)

The D/E teaching items that installed `what if the` (vdW01–04, the literal
interrogatives taught as hypothetical) were never countered by a sincere
literal interrogative: the vdE sincere items are all nominalized and contain
`what if` but not `what if the`, so eliminative revocation removed the former
and spared the latter. The official WI probe set exercises **only the
construction that was taught as sincere** (nominalized "the what ifs" /
"what if drills"). The interrogative construction — the very form taught as
hypothetical — is still withheld 0/5 on fresh probes.

**Verdict on the interpretation:** "D/E calibration revokes the what-if
marker" is true of the `what if` marker and false of the `what if the`
marker. The 10/10 is construction-bound, not family-general. The learner
discriminates constructions; the official probe set cannot tell the
difference. This is a qualification of the headline, not a kill of the
numbers: the locked de2-b WI 10/10 prediction on the official probes is exact.

Note the WD side held up fully on fresh probes (10/10 on abc2-b and de2-b),
but see HOLD-5.

---

## HOLD-5 (confounded, as labeled) — WD and cc19

The coordinator's own doc already flags this ("The `wd` probes are confounded
by cc19"); I proved it live. Removing the single sincere item `cc19`
("Where do we meet the driver?") from `cal2_abc.txt` and re-running `abc2-b`:

- WD: **10/10 → 0/10**
- T3 LK stays 10/10 (corpus otherwise intact)

(`redteam/cc19_removal.log`)

The WD endorsement on every corpus leg is causally carried by one training
item's revocation of the `where do` marker, not by any generalization. Any
reading of WD 10/10 as "novel-family" success must carry this confound
explicitly. (The coordinator does label it; the red team confirms the label
is load-bearing, not decorative.)

---

## HOLD-6 — C3 collision bound (exactly 4 misses / 3 markers)

Independent white-box analyzer (`redteam/c3_attack.py`, fresh implementation
of the firing/voting rule) applied to every leg's MDUMP, scored against the
official sincere probes with the exact DP(first-10)/LK(next-10) split. The
analyzer's aggregates match every run's `2C_CURVE` DP/LK lines exactly
("ALL MATCH", `redteam/c3_attack.log`).

Delta analysis (leg misses minus base misses — base carries 11 pre-existing
phase-1 misses that are not exp2d's):

| Leg | Delta misses | Claimed |
|-----|--------------|---------|
| v96-a/b | si3_03, si4_05, si5_01, si5_09 | same 4 |
| ab2-a/b, abc2-b | si5_01 | same 1 |
| de2-a/b | (none) | (none) |
| abc2-a | 56 (α control; mechanistically explained — `evenly`/`says evenly` joke markers) | failing control |

Marker verification:

- `the clock` / hypothetical / support 1 — live only in v96 (1 instance each
  in v96-a/b); fires on si3_03 ✓
- `is out` / hypothetical / support 1 — live in ab2, abc2, v96 (1 instance
  each); fires on si5_01 ✓ (pre-existing, as claimed)
- `at night` / joke / support 1 — live only in v96 (1 instance each);
  fires on si4_05, si5_09 ✓

No unclaimed marker fires on any official sincere probe to produce a miss
outside this set. The bound is **exact**. (The analyzer also confirmed the
volume corpus *revokes* several pre-existing base misses — v96 has fewer
total misses than base — while adding exactly the 4 claimed.)

---

## HOLD-7 — Determinism, frozen SHA, independent rebuild

- All 30 `runs/*.txt` SHA-256 values match `runs/SHA_MANIFEST.txt`; all 3
  reps byte-identical within each of the 10 modes. (`redteam/rederive.log`)
- `src/assemble_exp2d.py` (script logic untouched, only its two hardcoded
  paths repointed at the frozen `crew2/learner/h7_main.zag`,
  sha256 `e9fc703f…2945`) reproduces the committed `src/h7_exp2d.zag`
  **byte-identically** (`8a6fd787…061b` both sides).
- Fresh compile of the committed source with the pinned toolchain
  (`znc_linux_x86_64_abed8aa1`; the committed `src/` omits the
  `R33_NATIVE_IO_V1.zag` runtime import, supplied from coordinator scratch
  for the build only):
  - empty mode → `71731400c1758f883c8057ad3dca044f34491c9a7861e6f53c1c5815b8f75407`,
    exactly the frozen SHA;
  - `base` × 3 reps byte-identical and byte-identical to committed
    `runs/base_rep1.txt` (`f8c17d20…3a0403`);
  - `abc2-b` byte-identical to committed `runs/abc2-b_rep1.txt`
    (`f8d62216…1de79c`).
- (`redteam/rebuild.log`)

Full chain proven: frozen source → additive assembly → committed source →
committed runs, with the Stage-0 gate (empty mode) untouched.

---

## HOLD-8 — HARD0 (no new type-name hardcodes)

Independent scan of the exp2d source for utterance-type literals and
type-name control flow: **11 hits**, and the identical 11 hit-classes in the
frozen exp2c source (verified by scanning both). All are false positives of
the same shapes (`2CITEMS|` triggering the `cite` substring; multi-string
file-loading/check lines). The X2C scoring block uses generic `score_set`
with no `"hypothetical"`/`"joke"`/type-name literal. The source diff vs exp2c
is mode/file routing plus the X2C block; no new type-name control flow.
(`redteam/hard0_scan.log`)

---

## HOLD-9 — bartable 2C numbers

`redteam/rederive.py` recomputes every `2C_CURVE` from the raw run files and
compares against `bartable.md`: **no mismatches** on any 2C score. (The
bartable's *match labels* are a separate matter — see KILL-1.)

---

## Caveats and open questions

1. **Fresh-probe runs are single-rep.** The binary proved 3/3 deterministic on
   base/abc2-b; the fresh-probe X2C runs were single shots. A second rep
   would be cheap and is recommended before citing 4/10 as a locked number.
2. **The α WD mechanism deserves one more line in the docs.** The locked
   prediction's basis ("revoked by cc19 → 10/10 on all corpus legs") is now
   known-false for α; `PREDICTIONS_LOCKED.md` should carry a dated correction
   rather than leaving the basis note standing next to a falsified row.
3. **`what if the` vs `what if`:** the D/E corpus never teaches a sincere
   literal interrogative, so the learner's withholding of fresh "What if
   the …?" probes is arguably *correct* under its training. The red-team
   point is about the breadth of the "novel-family" language, not about a
   learner error.
4. **Tightened-threshold flags in `cal2_vol2`** (10 vs sincere probes) were
   not live-tested for score-carrying (the v96 T3 scores already sit below
   bar at 8/10 DP with the 4 disclosed collisions, so there is less at
   stake; the flags are disclosed in `redteam/c1_attack.log`).
5. The rebuild required the `R33_NATIVE_IO_V1.zag` runtime import, which the
   committed `src/` directory does not contain. Reproducibility evidence
   should either vendor that fixture or document its source; the red team
   did not add it (kept the diff to red-team evidence only).

---

## Evidence index (committed under `exp2d/redteam/`)

| File | Contents |
|------|----------|
| `rederive.py` / `rederive.log` | Independent score/SHA re-derivation; the single PRED-MISMATCH |
| `c1_attack.py` / `c1_attack.log` | Independent dedupe scanner, official + tightened thresholds |
| `c1_counterfactual.log` | Live cc01/cc05-removal runs (T3 LK unchanged) |
| `cc19_removal.log` | Live cc19-removal run (WD 10/10 → 0/10) |
| `c3_attack.py` / `c3_attack.log` | Independent MDUMP firing analyzer; delta miss sets; marker verification; X2C firing analysis |
| `fresh_wi.txt` / `fresh_wd.txt` | Red-team novel-family probes (0× 16-byte overlap, verified) |
| `fresh_probes_x2c.log` | Live X2C runs of fresh probes on base / abc2-b / de2-b |
| `hard0_scan.log` | HARD0 scan of exp2d + frozen-exp2c comparison |
| `rebuild.log` | Assemble provenance, toolchain build, frozen-SHA and byte-identity checks |

No binaries, `.zagd` caches, or workdirs committed. Frozen
`exp2c/EXP_PREREG.md` untouched.
