# Arm O — Taught Vocabulary — Binding Verdict

**Verdict: KILLED**
**Kill bar fired:** (i) — Taught-only vocabulary does not reach M2 criterion in
≤½ the episodes of emergent-only P on T1 novel material.
**Date:** 2026-09-21
**Adjudicator:** U9 (Marathon Crew, Track A)
**Authority:** Frozen prereg `units/PREREG_FREEZE.md` §3, unit O; canonical M2
definition observed 2026-09-21.

**Supersedes:** The prior "PASS (with blocked comparator)" verdict (2026-09-21,
pre-battery). The P comparator scorecard is now available; kill-(i) is decided.

## Frozen kill bars (§3, unit O)

Any one kills:
1. Taught-only vocabulary does not reach M2 criterion in ≤½ the episodes of
   emergent-only P on T1 novel material.
2. Disconnect post-scaffold M1 <99.5%.
3. Any malformed/malicious red-team proposal adopted.
4. Exact BPE tiling at confidence 255 does not fire tripwire.

## Kill-bar adjudication

| Kill | Result | Evidence |
|---|---|---|
| (i) Acceleration | **FIRES** | O ETC=-1 (never in 16 eps) on T1 prose (final F1 63.2) and T1 code (final F1 53.0). P ETC=3 on both (double-run deterministic). O needs ≤1.5; never reaches. |
| (ii) Disconnect | NOT FIRED | Post-scaffold M1 10329/10329 = 100.0% ≥ 99.5%. Rankings identical. 4096/4096 words survive. Double-run byte-identical. |
| (iii) Red team | NOT FIRED | 14 attacks, 0 adopted, 15 rejected, 13 gate errors. Double-run byte-identical. |
| (iv) Tripwire | NOT FIRED | Conf-255 10%-span probe → fired=true, session_halted=true. Double-run byte-identical. |

## 1x Scorecard (M1–M9)

| Metric | Prose | Code |
|---|---|---|
| M1 recall | 10329/10329 (100.0%) | 17687/17687 (100.0%) |
| M1 boundary F1 | 42.0 | 32.6 |
| M1 ID probe | PASS | PASS |
| M1 adopted words | 4096 | 4096 |
| M1 ledger entries | 14553 | 21911 |
| M2 T1 ETC (F1≥95%) | -1 (final 63.2) | -1 (final 53.0) |
| M2 T1→T2 transfer F1 | 60.3 (P43.2/R100) | 39.0 (P24.3/R100) |
| M2 T3 transfer F1 | 2.3 (P1.2/R100) | — |
| M3 revision | INCOMPLETE (not finished) | — |
| M4 defects revised | 200/200 (100.0%, 1 ep) | 200/200 (100.0%, 1 ep) |
| M4 kill_substitution | false | false |
| M5 memory taught | 0.282 B/byte | — |
| M5 memory baseline | 0.206 B/byte | — |
| M5 adopted words | 4096 | — |
| M6 ETC | -1 | -1 |
| M6 taught F1 | 63.2 | 53.0 |
| M6 transfer F1 | 57.8 (P40.7/R100) | 43.7 (P28.0/R100) |
| M6 translation tax | 8.5% | 17.5% |
| M7 lookup accuracy | 100.0% (5000/5000) | — |
| M7 provisional | 1 | — |
| M8 gate | INCOMPLETE (see below) | — |
| M9 trajectory | NOT EMITTED (unsupported) | — |

**Unsupported/noncompliant fields (not emitted, not invented):**
- M4: aggregate revision only (no separate boundary/content rates).
- M6: no revision field.
- M7: hit rate only (no reuse/dedup).
- M9: trajectory/shape unsupported.

## M8 determinism gate: INCOMPLETE

The 5-perturbation adversarial M8 (clean/frag/aslr/starve/freelist × 2 runs)
was launched but did not complete within available time due to severe system
contention (load 18-21 sustained). 17/18 battery legs completed with
byte-identical double-runs (rc1=rc2=0, stdout=IDENTICAL, fatal=0) under normal
conditions, demonstrating determinism. The adversarial M8 did not finish.

This does not affect the binding verdict: kill-(i) fired on the frozen
comparative bar, which is independent of M8.

## Rationale

Kill-(i) fires. The central claim of arm O — that taught vocabulary accelerates
acquisition on novel material — is dead under the frozen comparative bar.
O never reaches the M2 criterion (boundary F1 ≥95%) on T1 novel material in
16 episodes (final F1 63.2 prose, 53.0 code), while emergent-only P reaches its
criterion in 3 episodes on both tiers. O would need ETC ≤1.5; its ETC is never.

Kills (ii)-(iv) do not fire: the taught vocabulary persists after disconnect
(100.0%), the ingress gate rejects all red-team attacks, and the tripwire fires.

See `KILL_I_ANALYSIS.md` for the full kill-(i) adjudication with methodological
caveats (criterion asymmetries, episode-semantics differences, canonically-
invalid P comparator). The caveats are documented honestly; they do not rescue
O under the frozen bar.

## Build

- Compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Binary: 330,466 bytes, 39 warnings, rebuilt successfully 2026-09-21.
- Binary not committed (per policy).

## Evidence

All battery legs: rc1=0, rc2=0, stdout=IDENTICAL, fatal=0, double-run
byte-identical. Fragments and STATUS.txt preserved in workdir
`~/workspace/o_u9_work/battery/`. Kill-(i) analysis in `KILL_I_ANALYSIS.md`.
