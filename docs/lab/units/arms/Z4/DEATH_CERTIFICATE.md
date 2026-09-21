# Z4 Death Certificate

**Arm:** Z4 — Dialect (per-interlocutor) IDs
**Verdict:** KILLED
**Date:** 2026-09-21
**Fired criterion (verbatim from frozen §3 row):**
"Per-speaker lexicons do not converge ≥30% faster than a shared lexicon —
namespacing buys nothing; OR >40% of chunks duplicated across namespaces
(no real divergence — overhead without content). Conditional on Phase 4 working."

## Which disjunct fired

**Disjunct 1 (convergence) FIRED.** Disjunct 2 (duplication) did NOT fire.

## Evidence

Convergence race (`zconv-1x`, symmetric per-speaker sustained-3 criterion,
alternating S1/S2 full-corpus episodes on t1_prose.bin / t1_code.bin):

```
ZCONV,etc_s1=1,etc_s2=2,etc_sh_s1=1,etc_sh_s2=2,speedup_tenths_pct=0,bar1_fired=1
```

- Namespaced leg: ETC_S1=1, ETC_S2=2 → avg 1.5 episodes.
- Shared leg (one namespace for both speakers): ETC_sh_S1=1, ETC_sh_S2=2 → avg 1.5.
- Speedup = (1.5 − 1.5) / 1.5 = **0%** < 30% → **KILL**.

Duplication (M6 legs): `z4_dup_tenths=0.0` (0% of transfer-speaker chunks
duplicated across private namespaces). The speakers' 64-byte contents are fully
disjoint, so there IS real divergence — disjunct 2 does not fire.

## Why namespacing cannot win (analysis)

In a content-addressed exact-match ID store, the namespace is a label on the
ID; it does not change what is stored, how fast it is stored, or how fast it
is recalled. With disjoint speaker contents there is no cross-speaker
interference in the shared lexicon, so the shared leg learns each speaker's
content at exactly the same rate as the namespaced leg. The 0% speedup is not
a measurement artifact (the race was corrected from an asymmetric to a symmetric
criterion; both give the same conclusion) — it is the structural result.

Per-speaker namespacing may have organizational value (collision-free per-user
ID spaces, governance via the `common` namespace, TRANSLATE auditability), but
the preregistered falsification bar specifically tests convergence speed, and
namespacing buys none.

## Methodology notes

- An earlier asymmetric criterion (shared leg: 3 consecutive any-speaker probes;
  namespaced leg: 3+3 per-speaker probes) produced speedup = −50%. This was a
  criterion artifact, corrected to symmetric per-speaker sustained-3 for both
  legs. Corrected result: 0%. Both versions fire the bar.
- The race is degenerate in absolute terms (full-corpus episodes → ETC 1–2),
  but the comparison is exact. See AMBIGUITIES.md A20, A24.
- Phase 4 conditional: treated as satisfied via explicit speaker tags (see
  AMBIGUITIES.md A19). If the coordinator rules otherwise, this certificate is
  void and the verdict must be revisited.

## Raw evidence

- `work/battery_r1_1x/zconv-1x/` (run1/run2 stdout, byte-identical)
- `work/battery_r1_1x/m6-p2c-1x/`, `work/battery_r1_1x/m6-c2p-1x/`
- Source: `cl/arm.zag` (`t_zconv`), spec `ARM_SPEC.md` §6

## Implementation defects (do not affect the kill verdict)

- **M3/M8 panic:** `t_m3` (and the M3 portion of `t_m8`) panics with
  "slice index out of bounds" during phase-1 S3 ingests. Root cause not
  isolated after extensive debugging (ctab, eviction, ledger, and corpus
  hypotheses all eliminated). The panic is in the implementation, not the
  mechanism design. M3 and M8 are reported as FAILED.
- The binding kill (zconv) is independent of M3/M8 and stands.

## 10x status

Not run. Per assignment, 10x requires all 1x bars to pass and no binding kill
to fire. The binding kill fired; 10x is skipped.
