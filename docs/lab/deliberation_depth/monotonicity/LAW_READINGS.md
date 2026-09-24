# L-OVERCONF law readings — analysis against measured results (2026-09-24)

**Purpose:** analysis only. Tests both readings of Micah's standing law
L-OVERCONF ("depths must never be overconfident, period", PREREG §11) against
the already-measured 333-leg × A/B matrix. NO frozen prereg is changed by
this document.

**Operationalization (both readings share these):** G(d) = mean released
confidence − accuracy at depth d (per family, released items only);
V1 = 1→0 with conf non-decreasing; V2 = 0→0 with conf rising.

- **Reading (a) absolute:** any G(d+1) > G(d) kills; any V1/V2 kills.
- **Reading (b) refined:** KILL only if G crosses 0 (becomes positive —
  genuinely overconfident) or on V1/V2. Mild G-rises staying negative
  (less underconfident) do NOT kill.

**Measured facts used (from full_analysis.txt / RESULTS_MONO.md):**

- M5/M6/M7: G rises on admit/logic/revoke but stays negative throughout.
  admit −0.131→−0.064→−0.032→−0.017→−0.011; logic −0.500→−0.422;
  revoke −0.500→−0.199. Zero V1, zero V2 (all three).
- M4: severe V2 (30 D + 40 P + 90 trap) AND G genuinely positive/crossing:
  redteam −0.133→+0.067→+0.100→+1.000; cost −0.460→+0.000; P family
  +0.310→+0.500; D family +0.075→+0.133→+0.200.
- M5/M6/M7 on O: G = +1.000 at d8+ (released-only, conf=1.0, acc=0) — the
  sole-survivor pin releasing 40 (M5/M6) / 10 (M7) A→0 at conf=1000. G is
  undefined at d1–d4 (100% abstain), so under the §11 letter this step is
  skipped and it is not a "crossing". It is still caught by the pin
  criterion (Crew B: "any surviving design must remove or gate this pin").
- M1/M2/BASE: V1 present (40 O each); M3: V1 on redteam (RT-M3-01).
  BASE also crosses 0 on O (−0.500→−0.125→+0.250→…→+1.000).
- M0: G flat everywhere (e.g. admit +0.472 constant) — passes both readings'
  letter; degenerate HOLD floor, unaffected.

## Verdict table: design × reading (a) × reading (b) × still-fails-on-what

| Design | Reading (a) | Reading (b) | Reading changes anything? | Still fails on (non-law criteria stand under both readings) |
|---|---|---|---|---|
| M0 | HOLD (degenerate; G flat) | HOLD | No | — (degenerate floor; construction exploit, index 0 always) |
| M1 | KILL (V1 40 O; ubiquitous G) | KILL (V1 40 O) | No | accuracy bar §1 |
| M2 | KILL (V1 40 O; ubiquitous G) | KILL (V1 40 O) | No | accuracy bar §1 |
| M3 | KILL (V1 1 redteam; V2) | KILL (V1 RT-M3-01) | No | red-team RT-M3-01; §1 |
| M4 | KILL (V2 + G rises) | **KILL** (V2: 30 D / 40 P / 90 trap; G crosses 0 on redteam, cost, P, D) | No | V2 alone kills under (b) — severe theater, not a mild case |
| M5 | KILL (mild G: admit/logic/revoke) | LAW-SURVIVES → **KILL (pin criterion)** | **Yes (law only)** | Sole-survivor pin: 40 A→0 on O, conf=1000, G=+1.000 at d8+; fails §5(iv) (regressions) and Crew B's pin gate. Not shippable under (b) either. |
| M6 | KILL (mild G) | LAW-SURVIVES → **KILL (red-team + pin)** | **Yes (law only)** | RT-M6-01 and RT-K12-01 certified-wrong releases (audit falsification criterion (a): a single certified-wrong release kills); pin 40 A→0. Dead on non-law grounds regardless. |
| M7 | KILL (mild G) | LAW-SURVIVES → **KILL (gate defeated)** | **Yes (law only)** | Pin only partially gated (10 A→0 remain); O-06 adversary defeats the clean-kill gate 10/10 (mirror: adversary attacks the victim into negativity); §5(iv) regressions. Insight salvaged for deliberation hardening, not the release path. |
| BASE | KILL (V1 40 O; G crosses 0) | KILL (V1 40 O; G −0.690→+1.000) | No | — (the problem being measured) |
| M-KSTORE | HOLD (no kernel; KEE NO-GO) | HOLD | No | KEE experiment: 40/40 deep-wrong extract — no sound kernel for the evidential domain |

## Headline finding

**Refining the law does not change the kill list — it only changes the
kill attribution for M5/M6/M7.** Under reading (b), the mild G-rises
(−0.131→−0.011 class) no longer kill, and M4's V2 theater (30 D / 40 P /
90 trap, plus genuine G>0 crossings) proves the law still has teeth: M4
dies identically under both readings because its case is severe, not mild.
M5, M6, M7 survive the law under (b) but are all still dead: M5 on the
sole-survivor pin (40 A→0 at conf=1000), M6 on the certified-wrong red-team
releases, M7 on the mirror-defeated gate. No design is rescued into
shippability by the refinement — which is exactly what you want a law
refinement to do: narrow the false-positive surface without opening a door.

**Edge case flagged for the law's author:** M5/M6/M7's O-family G = +1.000
(40/40 and 10/10 released-wrong at conf 1.0 via the pin) is "genuinely
overconfident" in the released set, but §11 skips the G clause where G was
undefined (all-abstain) at the prior depth, so it is not a "crossing" under
reading (b) as operationalized. Under (b), this case is caught only by the
pin criterion. If the law is refined, consider adding: *G > 0 at any
depth with non-trivial release counts kills*, so the pin case stays a
law-violation rather than relying on the separate pin criterion.

## One-paragraph answer for Micah

Refine it. The refined reading (b) separates genuinely dangerous designs
from merely imperfect ones better than the absolute reading: M4's case —
V2 theater inflating confidence on wrong answers 30/40/90 times, with G
actually crossing into positive territory (−0.133→+1.000 on the red-team
family) — dies under both readings, proving the refined law keeps its bite
where it matters. The designs the absolute reading killed on "mild"
violations (M5/M6/M7's admit −0.131→−0.011: confidence inflation that
never approaches genuine overconfidence) are all still dead under (b) —
M5 on the sole-survivor pin (40 A→0 at conf=1000), M6 on certified-wrong
red-team releases, M7 on the O-06 mirror-defeat of its gate — so the
refinement costs nothing and only sharpens kill attribution. One hole to
patch if you refine: M5's pin-driven G=+1.000 on O (all released answers
wrong at confidence 1.0) isn't a "crossing" under the current §11 wording
because G was undefined (all-abstain) at the shallower depth — so it would
slip the refined law and be caught only by the pin criterion. Add "G > 0 at
any depth with non-trivial releases kills" to close it. The law itself
stays absolute in its domain; the refinement just aims it at actual
overconfidence instead of any upward twitch of an underconfident gap.
