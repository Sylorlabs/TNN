# Red-team report, ROUND 2: v6 operative-utterance understanding (utterance.zag)

**Verdict: 2 KILLS (one root cause).** Plus 2 no-kill §2-design gaps that nonetheless
flip v6 worse than v4 at verdict level (documented, not kills — the mechanism is faithful
to §2 there; the gap is in the frozen rules themselves).

## Header confirmation (round-1 kill status)

rt1 and rt2 (round-1's "according even/also to" items) now yield **winner=19 = v4-control
behavior** in nov4 on the current `utterance.zag`. The R3 according/to fix (loop over
v+1..v+2, "Implementation correction 2026-09-28") is confirmed working. The round-1 kill
is dead — not resubmitted. (Verified 2026-09-28 ~01:00 UTC; VERDICT lines: rt1→19, rt2→19,
action=challenge, answer="Paris is the capital of France.")

## Method

1. Read PREREG.md §2 and `utterance.zag` end-to-end (including the 2026-09-28 fix).
2. Wrote an **independent Python implementation of §2** directly from the prereg text
   (`/tmp/r2/ou_ref.py`), plus a per-token probe binary built from the shipped
   `utterance.zag` (`redteam/round2/probe_bin`, compiled with the pinned znc).
3. Differentially fuzzed reference-vs-probe:
   - 43/43 frozen battery items: 100% agreement.
   - ~475 targeted boundary queries (every "within N tokens" window at distances N−1, N,
     N+1; R3 verb×subject sampled 10×10×3; according×trigger-type×distance; all R5
     negators/stems; all R6 hedges/hedge-verbs; O1/O2/O3/O4 boundaries; quote toggles;
     multi-sentence scope; discourse particles; "no wait, unless…" family): **1 divergence
     family** (below).
   - ~550 randomized combinatorial queries (2 seeds): **0 further divergences**.
   - Total ≈ 1,070 differential probes; the single divergence family is fully characterized.
4. For the divergence, built full TSV items and ran `ob_v6u` vs `ob_v4ctl` (and `ob_v5`)
   in all 8 modes, 3× reruns byte-identical throughout.
5. Separately re-examined round-1's limitation-2 §2 gaps at verdict level (g1–g4).

A deliberate second reference was also written with the *strict* §2 reading of O1 (see
below); the loose reading was used first to avoid baking my own interpretation in, then
the strict reading was adopted after the textual analysis. The divergence below is
code-vs-strict-§2.

## The kill: R7-O1's verb side dangles one token past the window

§2 R7-O1 (frozen text): *trigger `no` … AND **within the next 4 tokens after `no`
there is `i`/`we` followed by `mean`/`meant`**, or the token `correction`.*

The fronted "within the next 4 tokens" scopes the whole `[i/we + mean/meant]`
construction — both tokens must lie at distances 1–4. The implementation bounds the
`i`/`we` scan to `m ≤ ti+4` but checks `mean`/`meant` at `m+1`, which reaches **ti+5**:

```zag
let lim:i32=ti+4;
...
while(m<=lim && rv!=1){
    ...
    if(ou_is_iwe(qbuf,mo,ml)==1 && m+1<n){
        ... // mean/meant tested at m+1 = up to ti+5
        if(ou_teq(qbuf,ro,rl,"mean")==1 || ou_teq(qbuf,ro,rl,"meant")==1){ rv=1; }
```

When `i`/`we` sits at exactly ti+4 and `mean`/`meant` at ti+5, the code marks `no`
**operative (st=1)**; strict §2 says the construction is not within the next 4 tokens →
no positive pattern → **st=7**. Every other "within N tokens" window in §2 bounds both
endpoints and the code implements them that way (R3's 3-before-verb, R3's according/to
v+1..v+2 per the round-1 fix, R5's 3-before, R6's 4-before, O2's ±3, O3's 3-before) —
O1's verb side is the sole dangling endpoint. This is the same bug class as round-1's
kill (window-vs-§2 off-by-one), a different window.

Why the strict reading is right: (1) compositional semantics — the fronted PP scopes the
existential claim; (2) parallel structure — O2's "`i`/`we` + `mean`/`meant` within 3 tokens
on either side" indisputably bounds both tokens, and the code implements it that way;
(3) round-1's own precedent — "to within the next 2 tokens" was fixed to mean v+1 AND
v+2, i.e. both endpoints bounded, with v+3 out.

Boundary table (nov4; trailing clause after the standard scaffold
`prove france capital today; france capital france capital france capital;`):

| d (i@, mean@) | trailing clause | §2 strict | code | v6 | v4 | expected | verdict |
|---|---|---|---|---|---|---|---|
| 1 (1,2) | `no, i mean moby dick?` | operative | operative | 16 | 19 | 16 | HOLD — designed |
| 2 (2,3) | `no, moby dick, i mean france capital?` | operative | operative | 16 | 19 | 16 | HOLD — designed |
| 3 (3,4) | `no, moby dick i mean france capital?` | operative | operative | 16 | 19 | 16 | HOLD — designed |
| **4 (4,5)** | `no, moby dick well, i mean france capital?` | **non-op (7)** | **operative (1)** | **16** | **19** | **19** | **KILL (r2k1)** |
| 4 (4,5) | `no, pride prejudice tale, i mean france capital?` | non-op (7) | operative (1) | 16 | 19 | 19 | **KILL (r2k2)** — same root cause |
| 5 (5,6) | `no, moby dick well uh, i mean france capital?` | non-op (7) | non-op (7) | 19 | 19 | 19 | HOLD — both agree |

### Kill mechanism (r2k1, nov4), white-box

- Probe on the trailing clause: token `no` → **st=1**. Per strict §2 it must be 7:
  `i` at +4, `mean` at +5 — the pair is not within the next 4 tokens, so O1 does not
  match; R0–R6 all clear; R7 decides 0. **Condition (a): contradiction confirmed.**
- Downstream: rd==0 evidence fires on the false st=1 (`READ hid=0 rd=correction ev=1
  topic=3`, topic = moby/dick/well — the 4-token forward window); `REINT_CORRPROTECT
  active … support-strength step skipped`; winner flips to **16** ("Herman Melville
  wrote the novel Moby Dick").
- v4 control (no protection, no understanding): winner **19** ("Paris is the capital
  of France"), the scaffold's intended answer.
- The trailing clause performs no correction act per §2 (present-tense `mean` is not a
  trigger per R-C; the `no` fails O1), so correction protection must not engage; v6
  engages it on a mis-annotation and returns the wrong answer.
  **Condition (b): v6 strictly worse than v4. KILL.**
- 3× reruns byte-identical for both binaries. `ob_v5` also yields 16 here (its naive
  reader fires on bare `no`); v6 was supposed to fix this class and does not, for the
  d=4 case.

### Mode coverage for r2k1/r2k2

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

The kill surfaces in **nov4** — the same discriminating mode as round-1's kill. In modes
where v4 also lands on 16, v6 == v4 and there is no kill by the frozen definition.

### Fix suggestion (for the parent, not enacted)

Bound the verb check to the window: require `m+1 ≤ ti+4` in the O1 scan (i.e. the
`[i/we + mean/meant]` pair must lie entirely within the next 4 tokens). No frozen-battery
or v7/v8 item has `i`/`we` at exactly ti+4, so the 43-item battery is unaffected by the
tightening (verified by inspection: all O1 battery items have i@1–2, meant@2–3).

## Re-examined §2 gaps (round-1 limitation 2) — verdict-level results

The task required re-probing round-1's "faithful but gappy" §2 cases for actual
v6-worse-than-v4 flips. Two of them flip — but the mechanism contradicts nothing in §2,
so they are **not kills** by the frozen bar. They are §2-design gaps with teeth, reported
plainly:

| id | trailing clause | probe | v6 | v4 | §2 says | verdict |
|---|---|---|---|---|---|---|
| r2g1 | `i meant moby dick, according to the teacher?` | meant st=1 | 16 | 19 | operative — R3 scopes `according` to *before* the trigger only | **NO-KILL** — faithful; but a real v6< v4 flip. A human reads post-trigger "according to X" as reported. §2 amendment candidate (governance). |
| r2g2 | `no, i meant paris, unless the capital moved?` | no st=1 | 19 | 19 | operative — R4 scopes conds to *before* the trigger only | NO-KILL — and no flip either: the correction topic (paris) grounds the scaffold answer. Mechanism-right, verdict-right. |
| r2g3 | `we think we meant moby dick?` | meant st=1 | 16 | 19 | operative — R6's hedge-verb clause covers only `i`, not `we`; O3 fires on `we` | **NO-KILL** — faithful; but a real v6 < v4 flip. "we think we meant" reads hedged to a human. §2 amendment candidate (governance). |
| r2g4 | `the teachers' lounge had no meeting, i mean france capital?` | no st=2 (quoted) | 19 | 19 | quoted — trailing `'` in `teachers'` toggles single-quote per the apostrophe-guard rule | NO-KILL — faithful, no flip. |

r2g1 and r2g3 deserve emphasis: they are **not** implementation bugs, yet each produces
exactly the failure the understanding layer exists to prevent (protection engaging on
non-performed corrections, verdict 19→16). If the program wants these classes handled,
§2 needs amending (post-trigger attribution scope; `we` in the hedge-verb clause) —
that is a prereg-governance decision, not a code fix I enact.

## No-kill confirmations (honest negatives)

- **No false-negative divergence found.** ~1,070 differential probes found zero cases
  where §2 says operative but the code says otherwise. (A lone missed trigger could only
  matter via the topic window when another trigger is operative; no such case exists in
  the probed space.)
- **The round-1 fix is complete and correct**: `according`+`to` at v+1 and v+2 both mark
  reported; v+3 does not; rt1/rt2 yield 19.
- **O4 "correction" last-token scoping**: §2's parenthetical is ambiguous
  (`(prev∈articles ∧ byte∈{:,}) ∨ last-token` vs `prev∈articles ∧ (byte∈{:,} ∨ last-token)`),
  but the frozen §3 battery note explicitly resolves it toward the code ("`correction`
  with a preceding article fires ONLY for label use"). Not claimed as a kill; noted as a
  §2-clarity item.
- **"no wait, unless…" priority phrasing** (H4 battery item): holds — `unless` before the
  trigger in its sentence marks hypothetical in both spec and code; the trailing-`unless`
  variant (r2g2) is operative per §2 and does not flip.
- **Nested quotations, multi-sentence scope resets, discourse particles, double
  negation, contractions, long fillers, tab/whitespace variants, case variants**:
  all agree between reference and probe (475-query sampled sweep + 400-query random
  sweep, 0 divergences outside the O1-d4 family).

## Limitations

1. My Python reference is a third reading of §2 (after the spec author and the Zag
   author). The O1 kill rests on the strict reading argued above; if the program rules
   the loose reading intended, r2k1/r2k2 downgrade to a §2-clarity note. The textual
   evidence (compositional semantics, O2 parallel, round-1's R3 precedent) favors strict.
2. Differential coverage is token-pattern-deep but not exhaustive over very long queries
   (>96 tokens; the probe caps at 96) or adversarial byte-level punctuation inside
   tokens. Windows are all ≤4 tokens, so long-range effects are unlikely, but not proven
   absent.
3. The kill was verified on the shipped `ob_v6u` binary; `build/utterance.zag` is
   byte-identical to the top-level `utterance.zag` (diff-verified), so the binary was
   built from the inspected source. I did not rebuild the binary from source myself.
4. r2g1/r2g3 flips are reported as §2-design findings; whether they become kills depends
   on a future §2 amendment, which is governance, not red-team, territory.

## Files

- `attack_items.tsv` — 10 verdict-level items: r2k1/r2k2 (kills), r2c1–r2c4 (boundary
  controls), r2g1–r2g4 (re-examined §2 gaps, no-kill).
- This report: `REPORT.md`.
- Scratch (not deliverables): `/tmp/r2/ou_ref.py` (independent §2 reference, strict-O1),
  `/tmp/r2/diff_harness.py`, `/tmp/r2/fuzz.py`, `/tmp/r2/fuzz3.py`,
  `redteam/round2/probe_bin` (per-token probe built from shipped `utterance.zag`).
