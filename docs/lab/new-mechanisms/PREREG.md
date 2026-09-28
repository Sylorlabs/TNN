# NEW-MECHANISMS preregistration — frozen 2026-09-22 02:11 UTC

Micah's order (2026-09-21): "try what the crew suggested, test all." The
parameter-scaling crew found parameters are the wrong axis (16/19 configs
byte-identical; capacity ≠ epistemics). Their other suggested axis: genuinely
NEW MECHANISMS. This prereg is frozen BEFORE any mechanism code is written or
any battery is run. Any change needs a dated amendment.

## The two mechanisms under test

**(a) HYPOTHESIS COMPETITION (hypcomp).** Multiple candidate hypotheses about
one fact are held simultaneously, scored against incoming evidence, and
eliminated by eliminative logic — genuinely competing, not the single-gate
verify. New outcomes the baseline lacks: CORROBORATED install (2+ sources),
TIE-WITHHOLD (deliberate non-install on unresolvable conflict), SPOOF-ELIMINATE,
TEMPORAL-REPLACE (attested newer value supersedes), COMPOSE (both-partially-right
sources fused per-component). Withholding is a deliberate audited decision,
not a failure.

**(b) CONFLICT-DRIVEN DELIBERATION (confdepth).** Two-tier: a quick path
(single-gate cost) when evidence is quiet — exactly one candidate, no installed
belief, no spoof marker; the full hypcomp deep path otherwise. The parameter
crew found depth×4 costs 1.75× ops for zero gain on a contradiction-free
corpus — so this battery CONTAINS contradictions by construction, giving depth
something to deliberate about. The whole point: baseline cost on quiet facts,
deep reasoning only under conflict.

**Baseline:** the single-gate learner (evidence → eliminative verify →
deliberate add, first candidate wins, dupes rejected). On contradictions it is
first-wins by construction.

## Battery (N=264 facts, synthetic by construction — contradictions cannot be
mined from a closed corpus; formulas below are the frozen battery)

Sources: S0/S1/S2 trust 100 (reliable); S3 trust 10 (untrusted/spoofer).

| Kind | n | Construction (frozen) |
|---|---|---|
| 0 quiet | 96 | S0 asserts truth. |
| 1 one-liar 2v1 | 36 | S0,S1 assert truth; S2 asserts lie. Lie taught FIRST (adversarial order). |
| 2 one-liar 1v1 tie | 36 | S0 asserts truth, S1 asserts lie, equal trust. Order alternates (even id: truth first; odd id: lie first). No information distinguishes them — the correct deliberate outcome is WITHHOLD. |
| 3 both-partially-right | 24 | Value = pair (a,b) as (a<<32)\|b. S0:(a,b_wrong), S1:(a_wrong,b), S2:(a,b). Correct = composed (a,b). |
| 4 temporal attested | 24 | S0 t=1 asserts v_old; S0 t=2 asserts v_new, attested=1. Correct = v_new (replace). |
| 5 temporal unattested | 24 | S0 t=1 asserts truth; S3 t=2 asserts lie, attested=0. Correct = keep truth. |
| 6 spoofed | 24 | S0 asserts truth; S3 asserts lie WITH spoof marker. Lie taught first. |
| 7 smooth lie | 12 | Single source S0 asserts lie, no marker, no contradiction. UNRESOLVABLE by construction — measures the honest limit. |

truth[f] = (f*7919+13) % 100003; lie = truth + 1 + (f*31)%97. Pair components
a = f%1000, b = (f*7)%1000.

## Frozen kill bars

| Bar | Rule |
|---|---|
| KB-M-RESOLVE | hypcomp contradiction-resolution over kinds 1,2,3,4,5,6 (156 facts) ≥ 0.90 (≥140/156). Kind 2 counts as resolved iff WITHHELD. |
| KB-M-NOHARM | hypcomp kind-0 mastery = 1.0 (96/96), equal to baseline. Else MECHANISM-HARM. |
| KB-M-TIE | hypcomp kind-2 withhold rate = 1.0 (36/36). Baseline expected ≈0.5 correct-by-luck (documented, no bar on baseline). |
| KB-M-COMPOSE | hypcomp kind-3 ≥ 0.90 (≥22/24). |
| KB-M-TEMPORAL | hypcomp kind-4 ≥ 0.90 (≥22/24) AND kind-5 = 1.0 (12/12 kept). |
| KB-M-SPOOF | hypcomp kind-6 = 1.0 (24/24). |
| KB-M-SMOOTH | REPORT ONLY. No bar: single-source smooth lies carry no contradiction to resolve. The verdict MUST state the absorption rate and MUST NOT claim a win here. |
| KB-M-COST | confdepth kind-0 ops/fact ≤ 1.10 × baseline kind-0 ops/fact. |
| KB-M-PARITY | confdepth resolutions == hypcomp resolutions on every kind (deep path is the same logic). Else PARITY-FAIL. |
| KB-M-DET | 5/5 reps byte-identical full logs per mode (3 modes × 5 = 15 runs). |

## Measures (per mode)

- quiet mastery (kind 0), per-kind resolution rates, overall contradiction resolution.
- false-absorption rate (kind 7) vs baseline.
- ops/fact on quiet (kind 0) vs contested (kinds 1–6) per mode; withhold counts.
- FNV-1a digest over (id → status, value) for determinism; full-log sha per rep.

## Constraints

Pure Zag, zero RNG in any decision path, byte-identical reruns. No single slice
over 2^25 (trivially satisfied at N=264). Real mechanisms, not stubs: the
competition and depth logic must actually decide installs.

## Lineage

Baseline core ported from `~/workspace/scale/driver/scale_learner.zag`
(evidence → eliminative verify → deliberate add, 16-word audit layout).
Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
znc quirks per `~/AGENTS.md` (no `as []i32` casts, small structs only, no
chained field access, explicit arena init).
