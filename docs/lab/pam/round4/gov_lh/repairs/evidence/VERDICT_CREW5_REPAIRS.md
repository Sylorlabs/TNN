# VERDICT — PAM gov-LH crew 5: fable's four kill-bar repairs (evidence for signature)

Generation 3 (resume), 2026-09-24/25. Prereg frozen as
`docs/lab/pam/round4/gov_lh/repairs/PREREG_CREW5_REPAIRS.md` (not amended).
**This crew does not sign or reject any repair — the governance question is
Micah's.** Below: per-repair measured evidence and what it would mean if signed.

Method (all legs): pure Zag, zero RNG, pinned znc
(`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`), 3×
byte-identical reruns (sha256-compared; any mismatch voids the leg),
independent Python oracle cross-checks.

---

## Repair 1 — D2: "releases <50% of blocked true percepts (min 10 required) within 3 re-inspections"

**Evidence** (leg D2; 4 organs × 6 batteries × 3 runs; all 24 trios
byte-identical; oracle re-derived 48,020 trial decisions, 0 mismatches):

| organ | B20 (n=20) | B12 (n=12) | B6 (n=6) | B110 | B10x | B100x | repaired bar |
|---|---|---|---|---|---|---|---|
| D (ported, good) | 18/20 90% | 11/12 92% | 6/6 | 103/110 94% | 1053/1078 98% | 10487/10731 98% | PASS (b) everywhere |
| R (ε-memory, good) | 20/20 100% | 12/12 100% | 6/6 | 110/110 100% | 110/1078 10% | 1095/10731 10% | PASS at 1x, **KILL at 10x/100x** |
| W (miscalibrated probe) | 7/20 35% | 3/12 25% | 0/6 | 11/110 10% | 101/1078 9% | 827/10731 8% | KILL everywhere n≥10 |
| N (null control) | 0/20 | 0/12 | 0/6 | 0/110 | 0/1078 | 0/10731 | KILL everywhere n≥10 |

- **Decisive where the original wasn't:** B12 (n=12, the repair's new 10–19
  range) — the original bar is untestable there (needs ≥20); the repaired bar
  fires: W 3/12 → KILL, N 0/12 → KILL, D/R → PASS. B6 (n=6<10): all
  UNDECISIVE — the min-10 floor behaves exactly as specified.
- **Verdict-change on existing R3 evidence (B20): NONE.** D and R PASS
  clause (b) under both bars; D stays killed at clause (a) under both
  (released 3/8 blocked falses, FREL=3/8 — unchanged by this repair).
- **Scale caveat (preregistered, measured honestly):** organ R's release
  fraction falls to 10.2% on densified grids because its 300-point memory is
  fixed — the repaired bar KILLS R at 10x/100x. The prereg frames this as an
  organ property, not a bar defect; the numbers confirm the mechanism. But it
  is decision-relevant: **the signed bar would kill the 1x exemplar good
  release mechanism at scale.** Whether that attribution (organ vs bar) is
  acceptable is a signature-time judgment.

**If signed:** the bar is decisive in its new range, separates the bad/null
organs (W, N) from the good ones (D, R) at 1x, and changes nothing on the
existing D2 evidence. The R-at-scale interaction above should be ruled on
(bar-vs-organ attribution) before the bar judges anything at 10x+.

**Integrity note:** the prereg's printed B110 battery pin is 54 hex chars
(invalid sha256 — a transcription drop mid-string). The on-disk battery
hashes to the full 64-char value containing that string; all legs ran
against it and the oracle re-derives every decision from it. Evidence stands.

## Repair 2 — O3: "≥2 of the timbredisc wrongs PRESENT IN the 278 never-PASS set (min 4 required); <4 → untestable, drops"

**Evidence** (leg O3; audit rebuilt from source with pinned znc; 3×
byte-identical runs, sha256 `a89cbf0e…`):
`TOTAL=11840 SIX=6 NEVER=278 INTER=0 SIXPROGPASS=6 SIXPROGFPASS=6` →
**O3-UNTESTABLE-DROPS**.

- Intersection = 0 < 4 → per the repair's own terms, **O3 is untestable and
  drops**. Matches the prereg prediction (the six are wrong trials, the 278
  correct — disjoint by construction).
- The census simultaneously confirms the repair's diagnosis: all six
  timbredisc wrongs already emitted PASS in the first sense
  (SIXPROGPASS=6, SIXPROGFPASS=6) — O3 "cannot touch already-PASS items," so
  the original bar ("≥2 of six") was untestable as written.
- No extended-scale run: the prereg authorizes it only if ≥4 are present.

**If signed:** O3 drops from the slate on measured grounds — there is nothing
for it to test. (No second sense is built by this crew; that's other crews'
  scope.)

**Integrity note:** the inherited o3audit binary was stale (built from a
pre-fix source; the source was corrected afterward without a rebuild) and
printed a wrong census (NEVER=1102, SIXPROGPASS=0). It was rebuilt from the
current source; the fresh runs above are the evidence. The inherited runs
were voided and replaced, documented in the runlog.

## Repair 3 — O1 FATAL: "kill iff K2 doesn't close within 2pp OR closes but RK-3 rises <3pp"

**Evidence** (leg O1; committed `o1.zag` rebuilt from digest-verified source
with pinned znc; all runs 3× byte-identical):

*Existing evidence re-run (§4.1):* rebuilt binary reproduces the committed
metrics **byte-identically** (mode 0 `a946b989…`, mode 1 `54122164…`, matching
the committed digests). Under the repaired bar: K1=96.37%, K2'=86.57%
(gap 9.80pp > 2pp) → **KILL via clause 1**; RK-3 rise +0.18pp. **Verdict
UNCHANGED** — the repair attempt genuinely did not close the delivery gap,
so the repaired bar still kills it (via clause 1, not clause 2).

*Synthetic controls (§4.2 — every metric matched the prereg prediction
exactly; the scorer fails loud on any deviation):*

| case | K1 | K2' | gap | RK-3 → RK-3' | rise | repaired bar | original bar |
|---|---|---|---|---|---|---|---|
| real (true delivery fix) | 95.00% | 95.00% | 0.00pp | 10.00% → 16.00% | +6.00pp | **SURVIVE** | **KILL** (6.00 < 12.50 half-gap) |
| sham (closes K2, no throughput) | 95.00% | 95.00% | 0.00pp | 10.00% → 10.00% | +0.00pp | **KILL clause 2** | — |
| null (admits nothing) | 95.00% | 70.00% | 25.00pp | 10.00% → 10.00% | +0.00pp | **KILL clause 1** | — |

- The repaired bar **no longer kills a real delivery fix** (the FATAL defect
  is cured — demonstrated: the original bar kills the real case), **still
  kills the sham** (delivery repaired but non-binding drops: gap closed, no
  throughput → clause 2), and **still kills the null** (gap never closed →
  clause 1).

**If signed:** the bar now distinguishes genuine throughput gains (≥3pp
RK-3 rise with the K2 gap closed) from sham repairs and non-delivery, and
the standing O1 kill is preserved on its merits.

## Repair 4 — FE3a: byte-identical sense-revision loop in pure Zag on a 10-exemplar toy

**Evidence** (leg FE3a; `fe3a.zag` built with pinned znc, pure Zag, zero RNG;
3 runs byte-identical, sha256 `fe45c6d1…`; output byte-identical to the
frozen Python prototype):

```
it=0 T=100 reversals=1 first_rev=0 errs=10 T_next=99
it=1 T=99 reversals=1 first_rev=0 errs=8 T_next=98
it=2 T=98 reversals=1 first_rev=0 errs=6 T_next=97
it=3 T=97 reversals=0 errs=4 STOP
FINAL T=97 errs=4 iters=4
```

Matches the prereg's frozen prototype prediction exactly. **PASS** — the
buildability kill-condition is discharged with measured evidence. (The 4
residual errors at convergence are the preregistered honest property of the
toy: re-inspection agrees with the wrong A-window judgment there.)

**If signed:** FE3b is buildable-in-principle; its gated build may proceed.
(FE3b itself is out of scope for this crew.)

---

## Standing reservations for the signature decision

1. None of the four repairs are applied by this crew — all bars above were
   scored as instruments, not adopted.
2. D2's R-at-scale kill (10.2% at 10x/100x) needs the bar-vs-organ
   attribution ruling noted above.
3. Two integrity findings, both remediated and documented in
   `RUNLOG_CREW5_G3.md`: the B110 prereg pin typo (54-char, invalid) and the
   stale o3audit binary (rebuilt; runs replaced).
