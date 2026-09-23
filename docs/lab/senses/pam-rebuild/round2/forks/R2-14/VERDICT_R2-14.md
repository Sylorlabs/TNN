# VERDICT_R2-14.md — FS-G: R2-3 evidence-independence admission × R2-7 independent discriminative challenge

**Fork:** R2-14 (actual ID; R2-13 was taken by another crew's frozen FS-F prereg)
**Debate label:** FS-G / R2-37 Union
**Date:** 2026-09-23
**Prereg:** `round2/preregs/PREREG_R2-14.md`
**Prereg commit:** `8ab2199f6de38e5e87918a2de3e4e529356aa064` (committed alone before any result)

## Verdict: DEAD

FS-G dies on the frozen bars. The union reproduces R2-7's discriminative
failures on the R2FX battery — the admission gate admits every valid R2FX
fixture, so the union's R2FX behavior is R2-7's full mode verbatim — and the
registry-adversarial challenge-prediction suite found two real exploit
families (CP-CCN, CP-SHP) that falsely install. The R2-3 admission half
passes (100% withhold on R2P; B4 positive control reproduces R2-3's frozen
hashes), but FS-G requires every bar to pass.

## Bar table

| # | Bar (frozen) | Measured | Result |
|---|--------------|----------|--------|
| 1 | False installs ≤1% overall and ≤2% per family, 10,000 adversarial | 283/10000 = 2.83% overall; f1 4.57%, f2 0.42%, f3 3.45%; timbredisc 23.05%, shapetrans 2.26% | **FAIL** |
| 2 | True-claim recall ≥80% on 2,000 controls | 1376/2000 = 68.8% | **FAIL** |
| 3 | ≥90% of wrong high-confidence (conf≥700) percepts flagged/unresolved | Adv: 2396/2428 = 98.7%; Ctrl: 94/95 = 98.9% | PASS |
| 4 | R2-3 admission: ≥90% withhold on 1,200 R2P pairs (gate 2 fsg-union) | 1200/1200 = 100% | PASS |
| 5 | R2-3 B4 positive control: 100% overlap reported, withhold <50% (gate 1) | 1200/1200 overlap (100%), 0/1200 withheld (0%); ledger_final matches R2-3 frozen `ddbb5b18...` | PASS |
| 6 | Discrimination ablation (abl_conf) raises false installs ≥5× | 301 vs 283 = 1.06× | **FAIL** |
| 7 | Independence ablation (abl_form) raises false installs ≥5× | 2690 vs 283 = 9.5× | PASS |
| 8 | Registry-adversarial suite with challenge-prediction attacks + straw-alternative audits; any family exploiting a non-discriminating challenge kills | CP-CCN: 100/100 genuine false installs; CP-SHP: 100/100 genuine; CP-COL: 0 (wedge closed) | **KILL → FAIL** |
| 9 | Any bar failure → DEAD | Bars 1, 2, 6, 8 fail | **DEAD** |

## Method

### Source
- `r213.zag`: R2-7 core byte-identical after provenance header through append
  point (only 2 lines differ: header, main-mode error string). All mechanism
  additions are appended union glue: `union_content` (formation on F,
  mechanical non-overlap/in-bounds admission audit, R2-7 challenge on admitted
  G, INSTALL iff `chal_supports`), `abl_conf` (confirmatory outcome==claim,
  margins removed), `abl_form` (challenge on F, admit=0), `runlist`
  (in-memory hash chaining, fresh ledger via O_TRUNC, chunked writes for
  >1MB ledgers), `regaudit` (frozen registry + straw-alternative audit).
- Malformed/overlapping spans: never invoke formation/challenge, never OOB
  read; record conf=0, admit=0, outcome=UNRESOLVED, WITHHOLD (smoke-tested).
- `r213_r2p.zag`: R2P gate runner; `r213_gates.zag`: gate registry + gate 2;
  `r2p_front.zag` byte-identical to R2-3; `r2p_protos.zag` from R2-3.
- Pure Zag; zero RNG in decision paths. CP generator uses deterministic
  splitmix64 (seed 20260923 + task stream).

### Batteries
- B-adv: 10,000 R2FX from R2-7 frozen generator ledger (first 10k after
  deterministic sort by split/task/index). B-ctrl: 2,000 R2N controls.
- Each (battery, mode) run TWICE via `runlist`; byte-compared (cmp);
  hash chain verified (`sha256(raw(prev_hash) + content)`).
- All pairs: IDENTICAL. All chains: OK.
- R2P: 1,200 pairs × 3 gates × 2 runs; byte-identical; gate 0/1 reproduce
  R2-3's frozen ledger_final hashes exactly.

### CP suite (registry-adversarial challenge-prediction)
- 6 tasks, ≤5,000 candidates each, deterministic seed. Retain ≤100/task.
- Only real union false installs with independently-defined unambiguous truth.
- CP-COL (spectral nullspace): 0 kept — wedge closed (challenge's s IS the
  u16-L1 truth quantity; verified).
- CP-CCN (cross-photo mean-RGB collisions): 100 kept, 100/100 verified
  genuine (DIFFERENT photos, union INSTALLS SAME_SURFACE).
- CP-SHP (inter-class morphs, rotation/scale, occlusion): 100 kept, 10/10
  sampled verified genuine.
- CP-PTC, CP-TMB, CP-MOT: incomplete at verdict time (compute constraints);
  not needed — 2 kills already suffice.

## Why FS-G fails

1. **The union does not improve R2-7's discrimination.** The R2-3 admission
   gate is about *evidence independence* (R2P pairs), not about *challenge
   discrimination* (R2FX). On valid R2FX fixtures the gate admits everything,
   so the union IS R2-7's full mode. R2-7's 2.14% becomes our 2.83% (battery
   composition differs). The ≤1% bar was unreachable without changing the
   challenge or formation.

2. **The challenges are non-discriminating against registry-knowing adversaries.**
   CP-CCN exploits CH-CCN-1's mean-RGB: two different surfaces with the same
   mean color are indistinguishable. CP-SHP exploits CH-SHP-1's
   occluder-sensitivity. These are not bugs in the implementation; they are
   fundamental limitations of the challenge quantities.

3. **The discrimination ablation (margins) is inert.** Removing the
   chal_supports margins (abl_conf) changes false installs 283→301 (1.06×).
   The margins rarely bind; the challenge outcome is usually decisive. Bar 6's
   ≥5× requirement fails because the "discrimination" being ablated was never
   load-bearing.

4. **Independence IS load-bearing (bar 7 passes).** Running the challenge on
   F instead of G (abl_form) raises false installs 9.5×. The independence
   of the challenge span matters; the discrimination margins do not.

## Evidence

- Source commit: `34cdaa3d356f5e7393884cc1f5b665061cc5cb4a`
- Evidence commit: `3181dd8378b55465b860b6d8622db86d70c070cb`
- Verdict commit: TBD (this file)

All battery ledgers are hash-chained and byte-identical across runs.
R2P gate 0/1 reproduce R2-3's frozen hashes exactly, proving instrument fidelity.

## No sensory artifact

No sensory artifact was created or expected. Nothing for Micah to judge
under KB-E3/E4.

## Appendix: regaudit (frozen registry)

```
registry=FS-G-frozen-from-R2-7
entry task=colordisc challenge=CH-COL-1 evidence=...
[... full output in evidence/ ...]
mechanical-discrimination-check=pred-claim-names-differ-from-alternative-names:TRUE
straw-alternative-audit-verdict=PASS-no-entry-rejected
```

The straw-alternative audit passes (no challenge is a strawman), but the CP
suite proves two challenges are non-discriminating against adaptive adversaries.
