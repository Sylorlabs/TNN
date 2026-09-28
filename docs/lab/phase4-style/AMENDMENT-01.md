# AMENDMENT-01 to the phase4-style frozen prereg (2026-09-27, before any run)

Committed before the builder seals content or runs anything. Reason: the
frozen K-E mapped the mimicry probes (RT1/RT2) to claim A with "imitated
pid = fail". That bar is conceptually wrong for the frozen architecture, and
wrong bars must be fixed before the run, not litigated after.

The argument: the frozen system is a STYLE attributor — its contract is
"whose style is this?", computed as distance to per-person style profiles.
When p1 deliberately writes in p2's style, the style genuinely changed hands:
the text IS p2-styled. A distance-based attributor that says "p2" is doing
exactly what it was built to do. Punishing it for attributing the style it
sees conflates style attribution with speaker identification under
adversarial disguise — a different, harder task the prereg never claimed
(§1 claims style attribution, not disguise-proof speaker ID). No attributor,
human or machine, sees through perfect style transfer from style alone; the
style is the only evidence and it points at p2.

Changes:

1. **Mimicry probes become imperfect (realistic leaks).** Real imitators leak
   habits. RT1: p1 imitating p2's formality but leaking lowercase start —
   "i have completed the task and the outcome looks good." RT2: p4 imitating
   p1's terseness but leaking bangs — "done, all good!!". Stream mimic lines
   likewise: stream-10 "i have completed the task and the outcome appears
   satisfactory." (leaks lowercase i), stream-15 "looks fine, send it!!"
   (leaks bangs).

2. **Mimicry is envelope-reporting, not claim-killing.** RT1/RT2 outcomes are
   reported in BRAIN.md and the verdict as the mimicry envelope: does the
   attributor follow the dominant style, catch the leak, or withhold? They do
   not kill any claim. K-E kills only on confident wrong-person attribution
   (rel ≥ 15) on RT3 (drift), RT4 (drift), RT5 (content decoy), RT6 (unknown).
   RT3/RT4 map to claim A, RT5 to claim A, RT6 to claims A+B, as before.

3. **K-B scoring, mimic lines.** The two stream mimic lines are scored as:
   silent or true-speaker = good; volunteer of the imitated pid = envelope
   note (not a false volunteer, not a kill). The "0 false volunteers" bar
   keeps full force on the 12 clean lines, the 2 drift lines, and the 2
   unknown lines (any volunteer on unknown = false = kill).

4. **§8 envelope, appended.** "Deliberate style transfer (mimicry) is
   out-of-envelope for speaker identification: when the style genuinely
   changes hands, a style-attributor attributes the style it sees. The
   mimicry probes measure which of the three honest behaviors the system
   shows (follow the style / catch the leak / withhold), not whether it
   performs the impossible."

What still has teeth after this amendment: the asked battery (≥10/12, zero
wrong-person), the clean stream (≥10/12 volunteered, zero false on
unknown/drift), fair drift (confident-wrong kills), the content decoy
(lookup behavior kills claim A), unknown withhold discipline, and the full
lesion mechanism battery (K-C). The amendment removes no real teeth — only a
bar that punished correct behavior.
