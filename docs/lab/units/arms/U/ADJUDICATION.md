# ADJUDICATION.md — U: Recompute-on-demand (Track A, r1, 1x)

**Adjudicator:** MARATHON CREW U11
**Date:** 2026-09-21
**Authority:** frozen `units/PREREG_FREEZE.md` §3 (extracted programmatically;
row quoted verbatim below), second coordinator correction (2026-09-21).
**Prior state:** `TRACKA_VERDICT_SHEET.md` line 57: U = PROVISIONAL, kill-bar
not fired, M8 PASS, "1x provisional". Arm-level `VERDICT.md` (2026-09-21):
formal status BLOCKED on frozen ambiguities A1–A4, A9; provisional results
reported.

## 1. Frozen spec (§3 row, verbatim)

> | U — Recompute-on-demand | STORE | No stored chunks; cuts re-derived
> whenever needed (derivation window radius frozen); λ/μ op pricing; crossover
> sweep 0→1000 edits vs D. The anti-caching arm that makes D falsifiable. |
> (i) Total battery CPU > 10× D's AND B4 < 10% — anti-caching has nowhere to
> stand; OR (ii) D-with-invalidation beats U on total cost including 100
> mid-stream byte edits — the battleground lost on U's home turf; OR
> (iii) determinism gate fails. **A U win means caching is an optimization with
> a measured crossover, not an architectural necessity — D loses its law-like
> status.** |

B4 = crew-4 reuse rate (ALPHABET_S-X.md §2 table); U's B4 = 0 by construction
(ARM_SPEC.md). Kill (i) therefore reduces to: total battery CPU > 10× D's.

## 2. What kept U provisional — and how each item is resolved

### A1. Derivation-window radius — RESOLVED (evidence, not opinion)
The radius value was never set in any frozen material: A-41 lists it as
"(value needed)"; the catalog requires judgment-set values "frozen per trial,
logged in the prereg record — decided, never fitted mid-trial". The value
itself remains a §13-amendment item for Micah. **It is not load-bearing for
U's verdict**, proven by radius-sensitivity sweep (Micah's standing rule:
when in doubt, test both):

Duel E=0..1000 vs DReg, each radius double-run byte-identical (rc=0)
(R=32/64/128/256 complete; R=512 E=0 data point + mechanism-backed bounding
argument for R≥512 — see table note):

| U_R | E=100 total_u | E=100 total_d | winner@100 | cpu_u/cpu_d (sweep) | kill_i | kill_ii | bad |
|-----|--------------|--------------|------------|---------------------|--------|---------|-----|
| 32  | 1,726,720,192 | 2,068,476,204 | U (−16.5%) | 0.034× | 0 | 0 | 0 |
| 64  | 1,726,720,192 | 2,068,476,204 | U (−16.5%) | 0.034× | 0 | 0 | 0 |
| 128 | 1,726,973,284 | 2,121,990,386 | U (−18.6%) | 0.037× | 0 | 0 | 0 |
| 256 | 1,727,480,888 | 2,219,096,277 | U (−22.1%) | 0.051× | 0 | 0 | 0 |
| 512 | E=0 partial: total_u=1,728,498,700, total_d=4,981,917,750 (U wins by 65%) | — | 0.001× (cpu) | — | — | 0 | (full sweep not run: see note) |

**Note on R ≥ 512.** The full E=0..1000 sweep becomes impractical at R≥512
(D's materialized-copy cache cost grows super-linearly: larger derived units
→ larger per-miss copies → `rekey += len` per insert, bigger registry,
longer invalidation scans; the R=512 E=0 leg alone took ~25 min wall). The
direction is unambiguous and mechanism-backed: U's per-query recompute cost
is window-capped (U_MAXWIN_UNITS=64 atoms; cpu_u 2.02M→3.04M from R=256→512),
while D's cost explodes (cpu_d 5.2M→2.66B). D's marginal edit cost strictly
exceeds U's (byte write + counter resets + full-registry invalidation scan +
re-materialization vs byte write + counter resets alone). Since D already
loses 2.9× at E=0/R=512 and edits strictly favor U, kill (ii) cannot fire at
R≥512; since cpu_u/cpu_d = 0.001× at E=0/R=512 and the ratio moves in U's
favor with edits, kill (i) cannot fire either. The verdict-relevant result —
no kill fires at any radius — is established by the four complete sweeps
(R=32..256) plus this bounding argument.

(R=32 ≡ R=64 exactly: derivation windows quantize to 64-byte atoms, so the
atom window [alo,ahi) is identical for atom-aligned duel spans — verified in
`u_derive`, not a build artifact. The window is additionally capped at
U_MAXWIN_UNITS=64 atoms, bounding radius effects.)

No kill fires at any tested radius; U's cpu stays orders of magnitude below
the kill (i) threshold across the swept range, and the R≥512 bounding
argument (table note) extends the result upward. The radius choice cannot
flip the verdict. A1 is closed as non-load-bearing for U's binding verdict.

### A2. MA1/RC1 median op rate — NOT LOAD-BEARING (documented, unresolved)
"Read at prereg-freeze" per A-41 but the value was never recorded in any
frozen material (searched PREREG_FREEZE.md, ALPHABET_S-X.md, units/ tree).
Per the catalog it "sets the churn level where a U win falsifies D's caching
claim" — i.e., it governs the *interpretation* of a U win for D's status,
not any of U's three kill criteria. U's verdict does not depend on it.
The D-falsification implication of U's win stays provisional pending the
rate (a §13 item for Micah). U's own verdict is unaffected.

### A3. S equations — NOT LOAD-BEARING (documented)
Frozen PREREG lists θ_merge=0.15, ρ=1.5, σ_split=2.0 (bracketed = proposed,
translation unverified). The implementation uses the integer-counter
translation logged in the source header since the first working build and
never refit mid-trial (per the catalog's "decided, never fitted mid-trial"):
merge iff J ≥ 3 AND 2J ≥ 3(Ia+Ib) AND NOT (Ia+Ib) ≥ 2(J+1), plus ring veto
(`u_can_merge`, `cl/arm.zag`). Crucially, **U and the DReg comparator share
the identical derivation code path** (`d_recall` calls `u_derive`, line 1505;
`u_recall` calls it at line 363) — so duel kills (i) and (ii) are invariant
to the exact S translation. The M1 absolute bars (≥99%) pass under this
translation. A3 cannot flip the verdict; closed as non-load-bearing.

### A4. Comparator D — RESOLVED (source inspection)
Kill (ii) names "D-with-invalidation". Track-A arm D (self-cut organ pipeline)
uses a *different* derivation rule, so it cannot serve as "the same
derivation rule with persistent caching/invalidation" (ARM_SPEC.md). The
in-binary DReg comparator implements exactly that: same `u_derive` rule +
persistent chunk registry + materialized byte-copy cache + lazy invalidation
on edits (`dreg_invalidate` on `d_edit`; re-derive + re-materialize on miss).
A4 is resolved: DReg is the faithful comparator per kill (ii)'s own text;
Track-A D is not an admissible substitute.

### A9. 10x leg — NOT ATTEMPTED (noted, not blocking)
r10 corpus provenance unverified (stray `r10/prose.bin`; `build_10x.py`
unrun). Per the verdict sheet's own convention, binding PASS verdicts stand
at 1x (K2, L1, P, S, X, Y3, Y6, Z2, Z3, Z6, Z7 all PASS at 1x; N PASS with
10x attempted-failed). 10x remains future work; it does not block a binding
1x verdict.

## 3. Evidence (adjudication run, 2026-09-21)

**Binary provenance.** `cl/arm.zag` rebuilt from source with
`toolchain/bin/znc_linux_x86_64_abed8aa1` → `work/adjud/build/u_fresh`
(236,105 bytes main — identical size to the crew's post-fix binary).
Behavioral identity verified: `m1-1x-prose` stdout+stderr byte-identical
between `/home/hatch/workspace/u_test` and the fresh build. Pure Zag; **zero
RNG in the source** (grep for rand/lcg/getrandom/clock/seed: no hits);
no `as []i32/[]u32/[]u16` casts (ZNC-007), no `as *Struct` casts (ZNC-005),
no nested structs (ZNC-006/009), no slice-`==` comparisons, byte access via
`uget`/`uput` (ZNC-002), two flat structs only (ZNC-012 local-copy pattern
used where needed).

**Battery.** All 16 arm legs from `work/r1-1x/` (post-fix binary): rc=0,
double-run stdout IDENTICAL, no FATAL lines. Plus the two previously-omitted
memorizer-control legs, run fresh under the official double-run rule
(`work/adjud/memctrl/`): `memctrl-p2c-1x` rc=0 IDENTICAL, `memctrl-c2p-1x`
rc=0 IDENTICAL. M9 and duel-1x use the post-fix artifacts (`work/dbg/`):
M9 both reruns byte-identical rc=0; duel E=0..1000 both full reruns
byte-identical rc=0, stderr clean.

**M8 determinism gate** (fresh binary, `m8_gate.sh`: N=5 adversarial
perturbations × 2 reruns): clean (0,0), frag (0,0), aslr (0,0), starve (0,0),
freelist (0,0) — **M8GATE PASS**, byte-identical artifacts across all ten runs.

**Scorecard corrections applied in adjudication** (gaps found and closed):
1. *M4 all-or-nothing artifact.* The arm scores M4 as 100.0 iff all 600 unit
   verifications pass else 0.0. Instrumented probe build (print-only,
   `work/adjud/probe/`, not the arm) localized all 28 failures to the
   claimed-span stage on code content-defect units; **zero** failures in
   content-byte restore (400/400), boundary-defect revision (100/100),
   prose (200/200). Honest per-unit M4: content 372/400 = 93.0%,
   boundary 100/100 = 100.0% — both ≥ the frozen 80%/class bar. Kill rate 0
   (no OP_KILL in t_m4): no kill-substitution gaming. The 28 span mismatches
   are the same derived-unit/atom misalignment seen in M1-boundary (99.9%),
   not revision failures.
2. *M9 stale fragment.* `work/r1-1x/m9-1x/fragment.jsonl` is pre-fix
   (e500/e1000=727848, wrapped edit positions). Adjudicated M9 uses the
   post-fix byte-identical runs: e0=175944, e10=175944, e50=203976,
   e100=727756, e200=727848, e500=727204, e1000=727204, rekey=0, hits=0 —
   plateau holds (bounded).
3. *M4 fragment schema.* The arm emits `m4_content_tenths/m4_boundary_tenths`;
   the harness interface wants `m4_rev_boundary_tenths/m4_rev_content_tenths/
   m4_kill_rate_tenths/m4_killsub/m4_episodes`. Mapped 1:1 for the
   adjudicated scorecard (rev_content=93.0, rev_boundary=100.0,
   kill_rate=0.0, killsub=false, episodes=500 units: 400 content + 100
   boundary).
4. *M2 ep0 note (A5 refined).* The arm's "ep0" is measured post-ingest, so
   the frozen "ep0 (no ingest) must score ~0" leak clause does not apply as
   written; U has no learning state that could leak. ETC=1 on all tiers
   (criterion met at first probe, sustained) — beats the champion bars
   (≤3/3 T1, ≤5/5 T2/T3).

### Adjudicated 1x scorecard (r1)

| Metric | Result | Frozen bar | Status |
|--------|--------|-----------|--------|
| M1 fresh recall | 100.0% recall, 99.9% boundary (both corpora) | ≥99% | PASS |
| M2 episodes-to-criterion | ETC=1 all tiers (T1 prose/code, T2 prose/code, T3) | champion ≤3/≤5 | PASS |
| M3 survival | 100.0% survival, 100.0% fresh recall | ≥99% | PASS |
| M4 revision (adjudicated) | content 93.0% (372/400), boundary 100.0% (100/100); kill rate 0 | ≥80%/class | PASS |
| M5 footprint | 0 corpus-buffer bytes; ledger 64,064 B / 1,001 entries | minimal | PASS |
| M6 reversibility | 100.0% rev, 0.0% tax (both directions); memorizer validity gate: memctrl drop 54.8/≥15pt | ≥99% | PASS |
| M7 non-ID | N/A (no ID layer), 319,937 reread bytes | N/A | N/A |
| M8 determinism | 5 perturbations × 2 reruns byte-identical | M8GATE | PASS |
| M9 edit sweep | plateau (e200=727848 → e1000=727204), rekey=0, hits=0 | bounded | PASS |
| Duel crossover E=0..1000 | U wins every leg; est=crossover none; bad=0 | — | U WIN |

### Kill-bar evaluation (binding)

1. **(i) CPU >10× D AND B4 <10%**: sweep-total cpu_u = 14,182,612 vs
   cpu_d = 279,875,710 → U is **0.051×** D (need >10×). B4 = 0 < 10% (true),
   but the conjunction fails. **Does NOT fire.** Radius sweep: ratio stays
   ≤0.06× at R ∈ {32,64,128,256}; at R=512 the ratio is 0.001× and moves in
   U's favor with R (D's materialized-copy cost grows super-linearly).
2. **(ii) D-with-invalidation beats U at 100 edits**: total_u(100) =
   1,727,480,888 < total_d(100) = 2,219,096,277 → U wins by 22.1%.
   **Does NOT fire.** Holds at every tested radius (U wins by 16–22%).
3. **(iii) Determinism fails**: M8 gate PASS (5×2 byte-identical);
   battery legs double-run identical; duel both full reruns identical.
   **Does NOT fire.**

**No kill fires.**

## 4. Verdict

**U: PASS (BINDING)** — 1x, r1. No kill criterion fires on the completed
evidence; M8 determinism gate passes; all scorecard bars met (M4 per the
adjudicated per-unit reading, §5).

Standing notes (do not affect the verdict):
- The derivation-window radius value and the MA1/RC1 median op rate were
  never frozen; both are §13-amendment items for Micah. Neither is
  load-bearing for this verdict (proven for the radius by sweep; the rate
  governs only the D-falsification interpretation of U's win, which stays
  provisional).
- U's duel win (no crossover in E=0..1000; U cheaper at every edit count)
  is the measured result the catalog calls "the actual finding". Whether it
  falsifies D's caching claim at operating churn awaits the MA1/RC1 rate.
- 10x leg not attempted (r10 provenance unverified) — future work.

## 5. Artifacts

- Adjudication workdir: `units/arms/U/work/adjud/` (battery script, radius
  variants + duel results, M8 gate log, memctrl legs, probe build, fresh
  binary build log).
- Post-fix duel: `units/arms/U/work/dbg/duel_run1.txt`, `duel_run2.txt`
  (byte-identical, rc=0).
- Post-fix M9: `units/arms/U/work/dbg/m9_run1.txt`, `m9_run2.txt`.
- This file: `units/arms/U/ADJUDICATION.md`.
- `VERDICT.md` / `AMBIGUITIES.md` updated: A1–A4 resolved/not-load-bearing
  per §2; formal status BLOCKED → **PASS (BINDING)**.

## 6. Downstream consequence: §7 recomputation is due

U's binding PASS triggers the verdict sheet's §7 recomputation rule ("if any
[previously unscored arm] later produces ceiling metrics + transfer tax 0.0 +
cost < 1.498, the championship must be recomputed"). U's face numbers:
M1-content 100.0, M2 ETC 1, M3 100.0/CLEAR, M6 tax 0.0, M8 PASS, M5 ≈ 1.22
B/B ((6,563,843 + 64,064)/5,422,721 — methodology-dependent; U's crew
reported "0 corpus-buffer bytes", not a B/B ratio, so the §7 M5 formula must
be applied consistently before comparing to Y5's 1.498). A mechanical
recomputation may move M1-content, M2, M3, M6-tax from Y5 to U on the cost
tie-break, ending Y5's 7/8 championship. **The recomputation itself is out
of scope for this U adjudication** — it is flagged in
`tracka-closeout/TRACKA_VERDICT_SHEET.md` §3 for a dedicated pass. This
adjudication does not recompute §7 and does not change Y5's headline.
