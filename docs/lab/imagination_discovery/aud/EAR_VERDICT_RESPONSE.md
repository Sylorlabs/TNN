# EAR-VERDICT RESPONSE — kids benchmark, 2026-09-22

Micah listened to all five kids clips (brief for each: **30 seconds of
children playing and laughing, clean native field-recording quality; no
hiss, static, or synth**). His verdicts are binding. His ears are the final
oracle over every machine result.

## The five verdicts (verbatim)

| # | Fork | Clip | Verdict |
|---|---|---|---|
| 1 | B-α | `b_alpha/clips/b_alpha_kids_v1.wav` | "most realistic to my ears" — B-α leads by ear AND machine (it was also the strongest machine-blind result: 3/3 judges labeled it "real recording", scoring more real-like than the genuine playground) |
| 2 | B-β | `b_beta/bbeta_kids_tag.wav` | "more cutouts then a bit realistic and weird" |
| 3 | B-γ | `b_gamma/render/b_gamma_kids.wav` | "meh, same issue as 2nd" (the cutouts) |
| 4 | A-α | `a_alpha/kids_a_alpha.wav` | "not close at all, sounds like an alien call" |
| 5 | D-α | `d_alpha/d_alpha_kids.wav` | "sounds like a synth with synth drums — I told you no synths allowed" |

## Kills

**D-α — BINDING KILL.** One "sounds like a synth" verdict kills a fork's
claim; that is the rule Micah set and the fork accepted in its own
preregistration (K1). D-α's claim is DEAD, documented plainly in
`d_alpha/TEST_RESULTS.md` §10 with no euphemism. All mechanical gates had
passed and the machine-blind result was "PASS, but hollow" (judges inverted
the real↔synth pair) — the ear verdict overrules all of it. Artifacts kept
for the record; nothing re-rendered under this claim.

**A-α — DEAD on the kids benchmark.** "Not close at all, sounds like an
alien call" confirms the machine-blind FAIL (ranked below the labeled synth
control; loop/paste signature s3=0.503, 723 clipped samples, 10,414 digital
clicks — defects in no other clip). The builder's own pre-verdict flagged
MEDIUM-HIGH synth risk; the oracle's verdict is worse — categorically wrong,
not children at all. Documented in `a_alpha/TEST_RESULTS.md`. Artifact kept
for the record.

## Shared defect: "they all cut off weirdly"

Every clip is exactly 30.00s and every one ends with an unnatural cutoff —
the hard 30s boundary truncating the composition. Measured tail behavior:

| Fork | Last-2s envelope (per 100ms) | What it is |
|---|---|---|
| B-α | loud (6000–14000) to the final sample, then exact zeros | hard digital cut mid-sound at ~−10dB |
| B-β | loud (2000–12000), file stops at ~3789/32768 | chop the 30ms edge fade can't hide |
| B-γ | taper 1479→62 compressed into the last 0.6s | reads as a quick fade, not a resolution |
| A-α | ends near-silent (tail max 45) | quiet but abrupt stop of air |
| D-α | natural decay 2471→0 over ~2s | the only genuine decay — fork is dead regardless |

## Cutout diagnosis (B-β, B-γ)

Measured at 10ms and 50ms resolution: **no digital dropouts** (B-β: 0 quiet
windows in 600; B-γ: 4 quiet windows, none flanked by loud), **no gate-like
dips, no hard onsets**. What Micah hears as "cutouts" is the forks'
deliberate phase grammar, i.e. content by design, not an artifact defect:

- B-β: envelope dips to ~862–1132 around 13.0–13.2s ("steps stop dead;
  everything halts for half a second" when the tag lands) and ~908–1265
  around 26.0–26.5s (P3→P4 transition). Per DERIVATION_kids.md this is the
  tag-game causal grammar — the halt IS the tag landing.
- B-γ: audible phrase boundaries of the event-grain assembly grammar.

Per the task rule (fix cutouts only if they are artifact defects, not
content), the compositions were NOT recomposed. The re-render crews confirmed
this reading independently.

## Fixes (live forks B-α, B-β, B-γ)

Each live fork re-rendered its kids clip with a **natural ending**: the score
ends its final event so the natural decay completes by ~28.3–28.5s, and the
last ~1.5s is quiet room tone resolving to the bed's natural floor — a laugh
tailing off, air resolving — with no synthetic fades, no processed-sounding
tails, no hard cuts. Same seeds, same catalogs/packs, same determinism rules
(3/3 byte-identical reruns, pure Zag, zero RNG); A-NATIVE re-verified. The v1
clips are untouched (verdict trail intact); the fixed clips are new files:

| Fork | Fixed clip | SHA-256 (3/3) | A-NATIVE |
|---|---|---|---|
| B-α | `b_alpha/clips/b_alpha_kids_v2.wav` | `c6be7e1f…48caf89` | PASS |
| B-β | `b_beta/bbeta_kids_v2.wav` | `882a29bd…49f620a` | PASS (same profile as v1) |
| B-γ | `b_gamma/render/b_gamma_kids_v2.wav` | `18423560…788d71f` | PASS |

Details (tail-envelope evidence, what changed in each score) are in each
fork's TEST_RESULTS.md "v2: natural ending" section.
