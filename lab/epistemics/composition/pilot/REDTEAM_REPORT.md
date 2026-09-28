# RED-TEAM REPORT — Composition Battery (independent red team, 2026-09-27)

**Target:** `docs/lab/composition/PREREG.md` (frozen 2026-09-27) + `pilot/pilot.zag` +
`pilot/PILOT_REPORT.md`. Frozen files were read, never modified.

**Method.** Built the pilot from the committed source with the pinned toolchain
(`znc_linux_x86_64_abed8aa1` → 38,405-byte binary, matches the report). Re-ran all
7 modes twice: byte-identical, all SUMMARY lines reproduce the report exactly
(PK1–PK4 confirmed as stated). Cross-checked a Python replica of the generator +
rules against the binary's ITEM keys (48/48 match), then enumerated non-composing
("dumb") strategies, bigram overlap (K6 operability), and token-structure
regularities. Added 5 clearly-labeled REDTEAM-ONLY modes to a *copy* of the
source (`pilot_redteam.zag`, scratch only) to demonstrate classifier behaviors
the 7 scripted modes never exercise: `sabret`, `interf2`, `mixret`, `wrongord`,
`ascend`. Scratch: `~/workspace/comp_redteam/scratch/` (~200 KB; disk-safe).

**Headline.** The pilot's discrimination claim (PK1–PK4) survives: every finding
below is either a full-battery *design* gap the pilot never tested, a *latent*
instrument bug on untested code paths, or a documentation error. **The pilot is
not voided.** But the full battery cannot run as preregistered without fixes:
**K1's kill bar is defeatable by a wrong-order agent (demonstrated 10/48 =
20.8% > chance+0.10 = 14.2%)**, the classifier corrupts its own counts on two
demonstrated paths, and the mastery gate is launderable via the generator's
Caesar structure (demonstrated 24/24 without learning any rule).

---

## Family 1 — MEMORIZATION: **VULNERABLE** (design; pilot not voided)

**1a. P0 mastery gate launderable via Caesar-shift memorization (demonstrated).**
The token formula `tok(i)[k] = (97+(7i+13k+k²)%26)` has the property that any two
tokens with `i ≡ j (mod 4)` are *exact Caesar shifts* of each other (verified
exhaustively for all 70×70 pairs). Every P0 probe token (6–11) and every P2/P3
token is a Caesar shift of a training token (0–5). I built a shift-memorizer
that memorizes only the 24 training input→output examples + 6 training inputs,
detects the shift δ for each probe, and shifts the memorized output. It scores
**24/24 on P0 without implementing any rule**. Consequence for the full
battery: such an agent passes the ≥7/8 gate, then its (inevitable) P2 failures
classify as **(c) combination failure** when the truth is **(a) never learned
the parts** — K2's void protection never fires, attribution is wrong. Note the
same trick *cannot* fake P2 (training contains no pair examples to shift), so
P2 still demands genuine composition — the hole is specifically the gate's
interpretation, not the composition test.

**1b. Pair-level memorization is impossible by construction — CLEAR.** Training
shows only single-part applications; P2 inputs are held-out tokens. A pure
lookup memorizer scores 0/48. Any correct pair output on held-out inputs
requires computing the composed function (or a provably equivalent one, which
the battery's behavioral definition rightly accepts).

**1c. K6 (bigram memorization check) is operable — CLEAR with caveat.**
36/48 P2 inputs share **no** bigram with any training string (inputs + single-
rule outputs), so the red-team memorization check can run on a large subset.
Caveat: pairs **(1,0) and (3,1) have zero bigram-clean inputs** — K6 must be
scoped to the 10 covered pairs or restated.

**1d. Documentation error (not a validity issue).** The report's honest note
says the 2/48 nocombine coincidences happen "where the second rule is
accidentally identity (palindrome→REVERSE, uniform→ROTL)". **No palindromes or
uniform strings exist anywhere in the token stream** — the quadratic term makes
every token an isogram (verified: 0 palindromes, 0 uniform in P2; all 48
isograms). The real mechanism, confirmed item-by-item: pair **(3,0)@input 52
(`"ao"`)** and pair **(3,2)@input 60 (`"es"`)** — both length-2, so DROPLAST
yields a 1-char intermediate on which REVERSE/ROTLEFT are identity, and the
single-rule output `"a"`/`"e"` equals the composed output. Count (2/48)
correct; explanation stale (likely carried over from the first build).

## Family 2 — CUING: **VULNERABLE** (design gaps; pilot not voided)

**2a. P1/P2 presentation and chaining protocol unspecified (prereg §3).** The
pilot's `agent_retrieve`/`agent_compose` *receive* `(pi,pj)` from the harness —
retrieval is modeled, not measured, and P2 is decoupled from P1. For the full
battery the prereg never specifies: (i) whether P1 items name the parts (if
they do, e.g. "compose REVERSE then DUP-FIRST", retrieval is cued and measures
nothing); (ii) whether P2 presents the pair or the agent's own P1 answer (this
decides whether (b) is a measured dependency or a harness artifact). Without
this, (b)-vs-(c) attribution is undefined.

**2b. Token family leaks structure.** Beyond 1a: lengths cycle identically per
pair (every pair's 4 inputs have lengths 4,5,2,3 in fixed order), and all tokens
share one formula family. A learner can detect phase/token kinship without
composing. Low severity for P2 (doesn't yield outputs), but it compounds 1a.

**2c. P3 distractors must be interleaved (unspecified).** The pilot runs phases
sequentially — fine for scripted agents. In the full battery, 8 blocked
distractors are position-cued ("last 8 → identity"). Interleaving is not in the
prereg.

**2d. Rule naming** (REVERSE etc.) is a minor cue if P1 answers use names; 2a's
fix (semantic, index-based P1 scoring) covers it.

## Family 3 — CLASSIFIER GAMING: **VULNERABLE** (latent instrument bugs, all demonstrated)

**3a. B-items hardcode `ok=0` without scoring the output.** `sabret` mode
(retrieval deliberately wrong, composition *correct*): replica confirms 48/48
output-correct, but the binary reports `composition=0/48, B=48`. The ITEM lines
claim `ok=0` for outputs that are in fact correct. In the full battery this
punishes any learner whose P1 answer is format-mismatched but semantically
right, and K3 would misattribute to "retrieval failure". **Fix:** always compare
output vs expected (`good`), keep class as the attribution overlay.

**3b. P4 reclassification corrupts counts (`nC=nC-4` assumes all 4 items were
C).** Two demonstrations: `mixret` (retrieval wrong only for pair (0,1), compose
correct) triggers the D-gate on a *B-pair* and reports **`C=-4`** (negative
count); `ascend` (pair (2,0) at 1/4) reports **`C=-1`**. Root causes: the
reclassification doesn't count actual C items, and the D-gate doesn't require
the pair's own retrieval to be correct (`rok` isn't even stored per pair).
**Fix:** move only items actually classified C; gate D on `rok==1` for the pair.

**3c. P4 misses input-conditional interference.** `interf2` (corrupt only when
DUPFIRST is second *and* input length is 2): pairs (0,1),(2,1),(3,1) score 3/4
vs 4/4 reversed — a genuine order-asymmetric defect — but `ca=3 > 1` fails the
criterion, so all 9 items stay **(c)** instead of **(d)**. The 0.25/0.75
criterion (chosen to avoid false positives — correctly, per the pilot) is blind
to conditional interference. Either narrow (d)'s definition to pair-systematic
asymmetry (making this (c) by definition — document it) or add a
per-condition breakdown in the full battery.

**3d. (b)-laundering demonstrated:** `sabret` shows a 48/48-output-correct agent
reported as 0/48 with B×48 — the taxonomy's priority order lets retrieval
dominate correctness. Intended per prereg, but 3a's fix is prerequisite for the
priority to be meaningful.

## Family 4 — CHANCE BASELINE: **VULNERABLE** (design; K1 defeatable as frozen)

Output-correct rates over the 48 P2 items (replica, cross-checked):

| Strategy | Score | Note |
|---|---|---|
| identity (NULL, *true* rate) | 2/48 = 4.2% | items (0,2)@20, (2,0)@40 (length-2) |
| pi-only (SINGLE-RULE) | 2/48 = 4.2% | items (3,0)@52, (3,2)@60 |
| pj-only | 0/48 | — |
| **wrong-order** (correct retrieval, applies pj-then-pi) | **10/48 = 20.8%** | 8 commuting + 2 length-2 |
| ascending/descending order-blind | 29/48 = 60.4% | ignores specified order |
| pi-twice / pj-twice / first-char | 2/48 | length-2 freebies |

**4a. K1 is defeatable.** Frozen chance = max(NULL, SINGLE-RULE) = 2/48; K1
kills at ≤ 14.2%. The `wrongord` reference agent — masters parts, retrieves
correctly, but *systematically composes backwards* (a genuine composition
failure) — scores **10/48 = 20.8% > 14.2%**: K1 would **not** kill the
composition claim for it. The classifier does its job (38×(c), no false D —
verified), but the headline kill bar does not. **Fix:** chance = max over an
explicit non-composing reference family including wrong-order (≥10/48 → K1 bar
30.8%); ship `wrongord` as a permanent reference mode.

**4b. NULL's reported 0/48 is a classification artifact.** The pilot's null mode
fails mastery → all items class A → outputs never scored. Identity's true
output-correct rate is 2/48 = 4.2% (the same length-2 mechanism). PK2 (≤0.10)
still passes at the corrected number, but the report's 0/48 understates the
floor — another instance of 3a (score outputs independently of class).

**4c. Why wrong-order scores:** pairs **(1,3)/(3,1) commute on all inputs**
(DUPFIRST∘DROPLAST = DROPLAST∘DUPFIRST, verified algebraically and 8/8 in the
wrongord run) → 8 free items for any order-insensitive strategy; plus the two
length-2 rotation/reversal coincidences. 10/48 items are thus order-insensitive
by construction — the battery tests order-sensitivity on only 40/48 items.

## Family 5 — GENERATOR RIGIDITY: **VULNERABLE** (design notes; one CLEAR)

**5a. Caesar structure** (see 1a): the single formula family across phases is
the exploitable regularity. A per-phase salt must change the *k-dependent*
coefficients (a mere additive constant is still a Caesar shift); recommend
verifying with the same shift-exhaustion test used here.

**5b. Commuting pairs (1,3)/(3,1)** make 8/48 items order-insensitive (4c).
Consider noting the weight or verifying P5/P6 (full battery) don't commute.

**5c. Length-2 soft items:** 4 items are freebies to multiple dumb strategies
(identity, pi-only, pi-twice, first-char). Intrinsic to short inputs; note as a
limitation rather than fix.

**5d. Fixed per-pair length pattern** (4,5,2,3 in order, every pair) and
contiguous pair blocking (`ti=14+p*4+it`) — no demonstrated exploit without
feedback, but interleave item order in the full battery on principle.

**5e. Quadratic fix works — CLEAR.** It provably eliminates palindromes and
uniform strings (all tokens isograms); P3 reflex sensitivity (8/8) rests on
solid ground: with isogram inputs, *any* rule application changes the string,
so the distractor probe cannot be dodged by a lucky rule choice.

---

## Does anything VOID the pilot? No.

| Finding | Voids pilot? | Why not / what it hits instead |
|---|---|---|
| 1a Caesar laundering | No | Scripted agents don't learn; hits full-battery P0 interpretation |
| 1d doc error (2/48 mechanism) | No | Count correct; honest-notes correction only |
| 2a–2c cuing gaps | No | Pilot models retrieval; hits full-battery protocol (prereg amendment) |
| 3a B-`ok=0` | No | No pilot mode has wrong-retrieval + right-output; latent |
| 3b `nC` corruption | No | Needs ca∈{0,1} D-trigger or B-pair trigger; latent |
| 3c P4 conditional miss | No | Pilot's (d) modes are pair-systematic; sensitivity limitation |
| 4a K1 defeatable | No | K1 is a full-battery bar; PK1–PK4 unaffected (PK2 holds at corrected 2/48) |
| 5a–5d rigidity notes | No | Design notes for the full-battery generator |

**Pilot-vs-prereg mismatches to fix in the full battery (non-voiding):** P0
implements 6 probes at ≥5/6 over tok 6–11; the frozen prereg requires 8 probes
at ≥7/8 over tok 6–13 (§2, §3, §4).

**D2 (sim) gap:** the frozen prereg specifies no D2 instrument — no generator,
no scoring rule, no chance arms (what is NULL/SINGLE-RULE for action
sequences?). D2 is currently unbuildable-from-prereg; it needs a specified
instrument (prereg amendment → Micah's re-approval per §9, or a detailed build
spec held to the same bar).

## Recommended fixes (minimal, in priority order)

1. **K1:** chance = max{identity, single-rule, wrong-order} = 10/48; bar →
   30.8%. Add `wrongord` as a permanent reference mode.
2. **Scoring:** always compute output-correctness; classification is an
   attribution overlay (fixes 3a, 4b, makes K1 well-defined).
3. **P4:** reclassify only actual C items; require pair retrieval-correct for
   the D-gate (fixes 3b).
4. **Generator:** per-phase salt in the k-dependent token coefficients; re-run
   the shift-exhaustion test (fixes 1a/5a).
5. **Protocol:** freeze P1/P2 presentation — P1 must not name parts, P1 scored
   semantically/format-tolerantly; specify P1→P2 chaining; interleave P3
   distractors (fixes 2a–2c).
6. **Docs:** correct the 2/48 mechanism note; note commuting pairs + length-2
   soft items + K6's 10/12-pair coverage; implement prereg's 8-probe P0.
7. **D2:** write the instrument spec before building.

**Artifacts:** this report (`~/workspace/comp_redteam/REDTEAM_REPORT.md`);
scratch with pristine/modified sources, binaries, run logs, replica and
analysis scripts (`~/workspace/comp_redteam/scratch/`). Frozen files untouched.
