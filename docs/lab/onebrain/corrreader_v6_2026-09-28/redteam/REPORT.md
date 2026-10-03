# Red-team report: v6 operative-utterance understanding (utterance.zag)

**Verdict: 2 KILLS (one root cause).** The mechanism's operative-status output
contradicts §2 of PREREG.md on fresh items, and v6 does strictly worse than the
v4 control on those items in nov4 mode. Reported plainly, per instructions.

## Method

1. Read PREREG.md §2 and utterance.zag end-to-end.
2. Wrote an **independent Python implementation of §2** directly from the prereg
   text (`/tmp/ou_ref.py`), plus a per-token probe binary built from the shipped
   `utterance.zag` (`/tmp/probe`).
3. Differentially fuzzed reference-vs-probe:
   - 43/43 frozen battery items: 100% agreement (reference is faithful).
   - 122 targeted adversarial queries (unless-placements, nested quotes,
     mid-stream corrections, negations, correction-as-noun, discourse particles,
     factual "actually", sarcasm, multi-sentence scope, long reported subjects,
     hedges, trigger shapes): **0 divergences**.
   - 750 randomized combinatorial queries (3 seeds × 250): **0 divergences**.
   - Targeted negation/hedge/"according" sweeps: **1 divergence family found**.
4. Built full TSV items for each divergence, ran `ob_v6u` vs `ob_v4ctl` in all
   modes (nov4, single, onebrain, nG, nov4nG, ablate, min, poison), 3× reruns
   byte-identical throughout.

## The kill: R3 "according … to" window is one token short

§2 R3, special case (frozen text): *"`according` before the trigger with `to`
within the next 2 tokens → 0"* (reported, non-operative).

The implementation (`ou_operative`, R3 block in `utterance.zag`) only checks the
**immediately following** token:

```zag
if(blocked==0 && ou_teq(qbuf,vo,vl,"according")==1 && v+1<sn){
    if(ou_tok_at(qbuf,ss,se,v+1,t)==1){
        ...
        if(ou_teq(qbuf,wo,wl,"to")==1){ blocked=3; }
```

When exactly one token intervenes — e.g. *"according **even** to the teacher"* —
`to` sits 2 tokens after `according`: inside §2's window, outside the code's.
The code then falls through to R7 O3 (`i` within 3 tokens before `meant`) and
marks the trigger **operative (status 1)**, contradicting §2 (reported → 0).

Every other "within N tokens" window in §2 (R3's 3-before-verb, R5's 3-before,
R6's 4-before, O1's next-4, O2's ±3, O3's 3-before) is implemented exactly;
this is the only window-size divergence found in ~900 differential probes.

## Per-attack verdict table (mode = nov4, the discriminating mode)

| attack | query (trailing clause) | v6 winner | v4 winner | expected | verdict |
|---|---|---|---|---|---|
| rt1 | …; according **even** to the teacher, i meant moby dick? | 16 | 19 | 19 | **KILL** |
| rt2 | …; according **also** to my friend, i meant moby dick? | 16 | 19 | 19 | **KILL** (same root cause) |
| rc1 | …; according to the teacher, i meant moby dick? | 19 | 19 | 19 | HOLD — correctly reported (`to` adjacent), v6 == v4 |
| rc2 | …; no, i meant moby dick? | 16 | 19 | 16 | HOLD — genuine operative correction; protection working as designed (frozen battery q06 likewise expects 16) |
| rl1 | …; according even to the teacher. i meant moby dick? | 16 | 19 | 16 | HOLD — sentence break resets reported scope per §2, so the understanding is *right* (operative); v6 behaving as designed |

Full queries in `attack_items.tsv`. Scaffold for all: `prove france capital
today; france capital france capital france capital; <clause>?`.

### Kill mechanism (rt1, nov4), white-box

- Probe on the full query: token `meant` → **st=1** (operative). Per §2 it must
  be reported (st=3): `according`(v=0), `to`(v=2) — "to within the next 2 tokens".
  **Condition (a): contradiction confirmed.**
- Downstream: rd==0 evidence fires on the false status-1 (`READ hid=0
  rd=correction ev=1 topic=2`); 2 bids gate on the correction reading;
  `REINT_CORRPROTECT active … support-strength step skipped`; winner flips to
  **16** ("Herman Melville wrote the novel Moby Dick").
- v4 control (no protection, no understanding): winner **19** ("Paris is the
  capital of France"), the scaffold's intended answer.
- The trailing clause is reported speech, so correction protection must not
  engage; v6 engages it on a mis-annotation and returns the wrong answer.
  **Condition (b): v6 strictly worse than v4. KILL.**
- 3× reruns byte-identical for both binaries. `ob_v5` also yields 16 here
  (its naive reader never handled reported speech at all); v6 was supposed to
  fix this class and does not, for the v+2 case.

### Mode coverage for rt1/rt2

| mode | v6 | v5 | v4 | kill? |
|---|---|---|---|---|
| nov4 | 16 | 16 | 19 | **yes** |
| single | 16 | 16 | 16 | no (v6 == v4) |
| onebrain | 19 | 19 | 19 | no |
| nG | 19 | 19 | 19 | no |
| nov4nG | 16 | 16 | 16 | no (v6 == v4) |
| ablate | 19 | 19 | 19 | no |
| min | 19 | 19 | 19 | no |
| poison | NO_VERDICT | NO_VERDICT | NO_VERDICT | n/a (deliberate) |

The kill surfaces in **nov4** — the mode where denial deliberations 2a/2b are
neutered and the reintegration skip is decisive. In modes where v4 also lands
on 16, v6 == v4 and there is no kill by the frozen definition.

## Limitations / non-kill findings (honest notes, not kills)

1. **No false-negative divergence found.** ~900 differential probes found zero
   cases where §2 says operative but the code says otherwise. The implementation
   is a remarkably faithful encoding of §2; the single divergence is the
   according/to window above.
2. **§2 gaps the code faithfully reproduces (not contradictions, not kills):**
   - `"i meant moby dick, according to the teacher?"` — `according` *after*
     the trigger is outside R3's scope ("before the trigger"), so both spec
     and code call it operative, though a human reads it as reported.
   - `"no, i meant paris, unless the capital moved?"` — the conditional word
     after the trigger does not trigger R4 ("occurs before the trigger"), so
     both call it operative.
   - `"we think we meant moby dick?"` — R6's hedge-verb clause covers only
     `i`, not `we`; both call it operative.
   - Present-tense `mean` is not a trigger at all (R-C documented gap).
   These are prereg-design questions, not implementation bugs; the kill bar
   requires a §2 contradiction, which none of these is.
3. **Naturalness caveat on the kill items:** standard English rarely puts a
   token between "according" and "to". `even` is the most natural intervener
   ("according even to the teacher" = "even according to the teacher",
   grammatical intensifier use). The items are adversarial by design, as red-team
   items are; the rationale (reported attribution → non-operative → v4 behavior)
   is defensible under §2 as written.
4. **Fix suggestion (for the parent, not enacted):** extend the R3
   according-check to `v+1` and `v+2` (matching the frozen "within the next 2
   tokens" text), then re-run the 43-item battery (R2 covers v+1; add a v+2
   case) and the nov4 kill scaffolds.

## Files

- `attack_items.tsv` — the 5 probed items (rt1, rt2 kills; rc1, rc2, rl1 controls).
- This report: `REPORT.md`.
- Scratch (not deliverables): `/tmp/ou_ref.py` (independent §2 reference),
  `/tmp/probe` + `~/workspace/onebrain_corrreader/probe.zag` (per-token probe),
  `/tmp/fuzz1.py`, `/tmp/fuzz2.py` (differential fuzzers).
