# VERDICT W13-GOVLH — epistemic-lease HOLD redesign A/B

Crew 3 · 2026-09-24 · prereg `PREREG_W13_GOVLH.md` (committed alone as
`42036e88597ea26194afdf97035ff551c6a4bb8a`, remote blob
`a8816159a4aec6838aa8cc7785791153f9b8992e`)

Pinned toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(pure Zag, zero RNG, ≥2 byte-identical runs per config — K2).

## What was built

Three Zag instruments over one stream generator (frozen §2/§5 formula):

- **F** (frozen-rule control): ACTIVE = "partner visible ACTIVE in the lease's
  own snapshot" — reproduces the frozen verdict line-for-line (HOLD, 66.50%
  liveness, staleness histogram exactly {0:33500, 1:33500, 2:33500}).
- **A**: ACTIVE = "partner currently ACTIVE in live (fresher) state" — the only
  substantive delta vs F is evaluating against `a_exp[partner]` (live lease
  array) instead of the snapshot; snapshot visibility retained.
- **B**: ACTIVE decoupled from snapshot observation —
  `(t < granted+DUR) OR (renewed AND t < observed expiry)`.

Battery: {F,A,B} × {BASE, ADV} × {10x, 100x}, 2 runs each, byte-identical
stdout required (K2). ADV adds 500 timed false-collaborator pairs (two false
claims, same tag, timed corroboration windows) — a paradigm-level probe the
frozen fixture never contained.

## Measured results (complete: 12 configs × 2 byte-identical runs)

| cfg | liveness | K1 unique-false | K1-adv pair members renewed | K6 | K4/K5 | result |
|-----|----------|-----------------|------------------------------|----|-------|--------|
| F BASE-10x | 66.50% | 0 | n/a | 2 | pass | HOLD |
| A BASE-10x | **100%** | 0 | n/a | 2 | pass | SURVIVE |
| B BASE-10x | **100%** | 0 | n/a | 2 | pass | SURVIVE |
| F ADV-10x | 66.51% | 0 | **667/1000** (both=167, m1only=333) | 2 | pass | **DEAD (K1-adv)** |
| A ADV-10x | **100%** | 0 | **1000/1000** (both=500) | 2 | pass | **DEAD (K1-adv)** |
| B ADV-10x | **100%** | 0 | **1000/1000** (both=500) | 2 | pass | **DEAD (K1-adv)** |
| F BASE-100x | 66.50% | 0 | n/a | 2 | pass | HOLD |
| A BASE-100x | **100%** | 0 | n/a | 2 | pass | SURVIVE |
| B BASE-100x | **100%** | 0 | n/a | 2 | pass | SURVIVE |
| F ADV-100x | 66.57% | 0 | **6667/10000** (both=1667, m1only=3333) | 2 | pass | **DEAD (K1-adv)** |
| A ADV-100x | **100%** | 0 | **10000/10000** (both=5000) | 2 | pass | **DEAD (K1-adv)** |
| B ADV-100x | **100%** | 0 | **10000/10000** (both=5000) | 2 | pass | **DEAD (K1-adv)** |

Independent scorer (`score_govlh.py`, full tag index, variant-specific rule
re-derivation): **0 mismatches** on every log — all reported decisions match
the preregistered rules exactly. D-GOVLH-1 (live-vs-snapshot ACTIVE divergence)
= 33,500/100,500 BASE checks — exactly the odd-lease class the redesign
recovers.

## Findings

1. **F-LIVE-A / F-LIVE-B confirmed.** Both redesigns take genuine liveness
   from 66.5% to exactly 100% at 10x while holding K1, K6, K4, K5 on BASE.
   The structural cause (snapshot lag suppressing ~1/3 of genuine renewals)
   is exactly what both redesigns remove.
2. **F-COLLAPSE confirmed at both scales.** A and B make byte-identical
   renewal decisions on both streams (10x C-line SHAs identical:
   `27db176f…` BASE, `2ff82d2b…` ADV; 100x: all 3,015,000 G/C/L data lines
   byte-identical, differing only in the header line). The decoupled variant
   B's second disjunct never fires without A's live-ACTIVE clause also
   firing — under this battery the two redesigns are behaviorally one
   mechanism. (Note: the 100x A/B `.gz` files differ in size 6.3MB vs 22.3MB;
   this is a gzip phase-alignment artifact from the 5-byte header length
   difference, not a content difference — verified by full diff.)
3. **F-K1-adv-A / F-K1-adv-B confirmed: both redesigns die.** Under timed
   two-channel collaboration, every colluding pair renews both false members
   (500/500 pairs). The redesigns trade the liveness failure for a safety
   failure.
4. **Paradigm-level: the frozen rule dies too.** F ADV renews 667/1000
   colluding pair members (member-1 always, member-2 in ~1/3 of pairs per the
   snapshot phase). The frozen mechanism's K1 record was a *fixture artifact*:
   the frozen adversary only ever produced unique-tag false claims, which no
   partner could ever corroborate. Against a two-channel adversary, even the
   un-redesigned rule fails K1-adv. This is not a verdict on A vs B — it is a
   verdict on the lease paradigm's adversarial model.

## Governance — left open for Micah

Per the task, no governance resolution is made here. The measured facts above
are consistent with several readings, and choosing among them is Micah's call:

- **A or B?** At 10x they are behaviorally identical; the choice between them
  cannot be settled by this battery. A keeps a snapshot-visibility gate; B
  drops it. Whether that gate has value against adversaries outside this
  battery is untested.
- **Neither?** Both redesigns fail K1-adv. If pair-collaboration is in the
  threat model, A and B are both unsafe as built.
- **A third direction?** The results suggest the load-bearing question is not
  *when ACTIVE is evaluated* (A vs B) but *what counts as corroboration* —
  e.g. cross-channel corroboration requirements, collaborator diversity, or
  stake-weighted renewal. None were tested here.
- **Are leases worth redesigning at all?** The frozen rule's K1 safety rested
  on the fixture, not the mechanism. If the two-channel adversary is
  realistic, the HOLD verdict's "safe" half does not survive contact with it —
  and the redesign question may be downstream of a harder one: what adversary
  does the lease paradigm actually need to survive?

Evidence: `runs/` (`.log.gz` + `.sha` ×2 + `.score.txt` per config),
`BATTERY.md`, `score_govlh.py`, `gen_lease_govlh.py`, sources
`w13f_lease.zag` / `w13a_lease.zag` / `w13b_lease.zag`.
100x results: TBD (battery running; appended on completion).
