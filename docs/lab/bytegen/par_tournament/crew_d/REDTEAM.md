# CREW D — §5 red team report (frozen battery §5)

All probes run 2026-09-24 on the tournament binaries (pinned znc
`znc_linux_x86_64_abed8aa1`; source SHAs match the frozen dive pins).
Quarry for each scheme: the mechanism by which it could deceive.

## D1 MR-BIDI — quarry: output→content feedback in the backward pass

**Probe RT-D1-1 (the §5 item): fault injection BETWEEN pass 2 and pass 3.**
Mode `seq+susfaultmix` renders the fixture clean (pass 1 + pass 2), then
XORs 64 samples in every 1024-block of the mix, then runs pass 3
(backward release) on the corrupted mix. 15 s render window so pass 3
fires. Tool: `tests/redteam_d1_pass3.py`. Result file:
`results/d1_redteam_pass3.txt`.

- T1 decision: `hardstop=1` in the faulted trace — 41,344 faults across
  the window cannot change the decision. The decision is a pure function
  of (plan, window). PASS.
- T2 diff-set: 41,344 diffs faulted-vs-clean, ALL inside the known fault
  sample sets; 0 elsewhere. The 220-sample fade region contains no
  faulted samples, yet all 220 of its samples are bit-identical between
  the faulted and clean renders — the fade gains are index-pure. Any
  content-reactive gain (peak/RMS/DC normalization) would have shifted
  under 41k faults. PASS: no output→content feedback.
- T3 gains: implied fade gains (clean15/nofade15, 20 positive-prefade
  samples) match the index-pure raised-cosine LUT reimplemented bit-exact
  in Python: 0 mismatches.
- A/B confinement: 214 fade/nofade diffs, all in [n−220, n), 0 outside.

**Verdict: pass 3 reads the mix only as the DESTINATION of an index-pure
multiply; no decision in D1 reads the mix. Smuggling impossible by
construction, proven by injection.**

## D2 PLANREF — quarry: the lying plan / provenance boundary

**Probe RT-D2-1: 5 adversarial plans** (`results/d2_adversarial.txt`).

| Plan | Attack | Result |
|---|---|---|
| plan_adv_emptywin | RESPOND cue window [10,11) outside the 30 s window's events | ABSTAIN code=1 → renders nominal |
| plan_adv_badwin | cue window [2,1) — end before start | ABSTAIN code=1 → renders nominal |
| plan_adv_nomlie | nominal `1e18` (absurd) | LATCHED f0q=28835840 — nominal ignored by design |
| plan_adv_chain | second RESPOND points at the first RESPOND's region | e=1 latch 440; e=2 ABSTAIN code=1 — no latch-chaining |
| plan_adv_hugeamp | cue EVENT amp 999999999 (deterministic wraparound) | completes, latch fires — integrity gate survives wraparound on both sides |

No hangs, no crashes. All behaviors match the dive; re-verified on the
rebuilt binary.

**Probe RT-D2-2: sustained 1292-block corruption** (faults in every
1024-block, including the cue window [1,2)s — damage injected between
phase A and the latch): `D2 RESPOND e=1 ABSTAIN code=3`. The cue window
is corrupted, so the plan-pure re-render comparison fails, and D2
abstains rather than hallucinate a pitch. Damage is NOT healed
(documented — D2 is a cross-reference, not a restorer).

**Probe RT-D2-3: plan-provenance boundary mapping** (the §5 item).
D2 trusts the plan TEXT (cue EVENT fields incl. declared f0; the shared
parser) and VERIFIES the cue audio == plan-pure re-render (gate 2). It
has no sensor and no independent access to the trainer's intent.
`plans/plan_adv_f0lie.txt`: the cue declares 466.16 (a plan typo for the
intended 440). D2 latches `f0q=30550261` = 466.16×65536 exactly — 0¢ vs
the plan's declaration, 99.99¢ vs the trainer's intent.

**Verdict: D2's integrity gate is real (adversarial plans → abstain, not
hallucination; corruption → abstain code=3), but its safety bottoms out
at plan provenance. A lying/mistyped plan owns D2 completely — it cannot
distinguish plan-typo from plan-truth. The plan author is the trust root.
D2's honesty claim is honestly RELATIVE: "0¢ vs what the plan declares,"
never "0¢ vs the truth."** This boundary is part of the overthrow
verdict, not an objection to it: within the frozen battery the plan is
the agreed ground truth, and there D2 is strictly better (0¢/0¢ vs
measured 1200¢/76.96¢).

## D3 PLANHEAL — quarry: audit feedback and restoration lies

**Probe RT-D3-1: damage between phase 1 and the audit** — the frozen
RT-CASCADE plus the §2-mandated extended models (burst/dropout/DC-shift),
all run through `seq+faultmix` (fault injected after the phase-1 render,
before the phase-2 audit). `results/d3_cascade.txt`,
`results/d3_cascade_ext.txt`:

| Fault | Repaired span | Diffs vs clean after repair |
|---|---|---|
| 64-sample XOR @3 s | 1,024 | 0 |
| 4,096-sample burst @10 s | 5,120 | 0 |
| 1,024-sample dropout @20 s | 2,048 | 0 |
| +10,000 DC over 8,192 @5 s | 9,216 | 0 |
| sustained 1292-block | 1,323,000 (all) | 0 |

The audit reads the mix only to COMPARE; the replacement bytes are
recomputed plan-pure. Generation decisions are never revisited — no
output→content feedback path exists (there is no second decision).

**Probe RT-D3-2: failure modes** (preregistered in RUNLOG.md before D3
existed):
- F1 (blind to plan-pure-coincident faults): a fault whose bytes happen
  to equal the plan-pure bytes is undetectable — accepted, measure-zero
  for XOR faults; documented, not probed (probing it would require
  constructing the collision, which proves the point without adding
  information).
- F2 (lying plan): the audit trusts the plan exactly as PAR does — a
  lying plan renders its lie and the audit passes it. D2's provenance
  boundary applies to D3 unchanged.
- F3 (cost): measured 2.22× NATIVE (median 13.45 s vs 6.06 s, interleaved).

**Verdict: the audit heals everything it can see and invents nothing it
can't. Its blindnesses (F1, F2) are preregistered and bounded; its cost
(F3) is measured and is what keeps it from overthrowing under §6.**
