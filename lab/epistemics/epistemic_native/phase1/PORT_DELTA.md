# PORT_DELTA.md — native-deliberation epistemics, Phase 1 (attempt #6)

What was ported from the frozen deliberation substrate
(`deliberate_frozen_r4.zag`, SHA-256
`7dec26d8600683f2c6cefc83d524a403f4ac288117864108dc54a08afa61b787`)
vs what is new epistemic machinery. Attempt #5's `epistemic_simple.zag`
helpers were kept verbatim (`ehelp.zag`); its engine and learning method were
rejected and rewritten.

## Ported (substrate → this engine)

| Substrate element | Ported form | Delta |
|---|---|---|
| Audit ledger (`led_init`, slot get/put) | `led_init`, `lr_get`, `lr_put`, `t_get`, `t_put` | Row is 64 bytes here (vs 552 substrate); fields redefined for bids/readings (HID, kind, name-code, evidence/fire, score, aux, state, elim-reason, eliminated-by, base, bonus). Turn fields (close flag, winner, runner, margin, verdict, contested, sup/con counts) in a 32-byte turn block. |
| GEN → ELIM → ARGMAX loop | Same loop per deliberation phase | Phases: claim readings → interpretation bids → coverage readings → verdict bids. GENs idempotent via done-flags (re-GEN returns silently). |
| Trace emitters (READ/CAND/ELIM/ARGMAX/CONTENT) | `tr_reading`, `tr_cand`, `tr_candx`, `tr_elim`, `tr_content`, ARGMAX line | Same line grammar; `tr_candx` adds `cand=` for interpretation bids; CONTENT lines carry candidate id, overlap, surviving interpretation, sanitized text. |
| CLOSE / CONTENDER / REVIEW | `close_call` | Margin < 5 over best FIRED runner-up; REVIEW emission gated on reading the ledger close-flag back (substrate red-team repair #10). Tie → lowest HID everywhere. |
| Neuter-hook pattern (REDTEAM4) | `neuter_hid` / `flip_hid` in `gen_readings` | Applied AFTER the READ trace prints the computed value; consumers read the intervened value. Flip toggles to the opposite of computed (true wrong-hypothesis). `neuter=99` neuters all 9 claim readings. |
| Determinism rules | Same | No RNG, no floats, fixed loop orders, tie → lowest HID / lowest index. Proven: 448 LOO claims × 2 runs, verdict TSVs + all 448 traces byte-identical. |

## NOT ported (deliberately)

- All substrate dialogue GENs and utterance classifiers — none apply; every
  epistemic GEN (readings, interpretation bids, verdict bids) is new.
- Substrate fact/episode machinery — the mass (`senses/mass.bin`) replaces it.

## New (epistemic machinery, no substrate precedent)

- **Kind-0 claim readings** (hids 0–8): R_ASSERT, R_EVAL, R_DEON, R_1PEXP,
  R_NEG, R_CLAIMNUM from mass pattern/negation/number features; R_OEVAL,
  R_ODEON, R_O1PEXP = base reading AND frozen learned formed-flag.
- **Per-candidate readings** (hids 10–89, ≤16 candidates): R_OVL (overlap
  depth), R_CPOL (candidate negation), R_CNUMA/C/G (number alignment/conflict/
  gap). Every candidate's CONTENT traced.
- **Interpretation bids** (hids 120/140/160 + c): SUP / CON / TOP, all fire on
  overlap ≥ 1; scores from reading rows only
  (SUP = 100+ovl+10·pol·numa+12·nreal+6·cong;
   CON = 100+ovl+10·(1−pol)·numa+8·numc+6·cong;
   TOP = 100+ovl+12·numg).
  Per-candidate ELIM (max score, tie → lowest HID); losers OUTSCORED.
- **Construction congruence**: candidate in the same utterance-type pattern as
  the claim (signatures compared via ledger reading rows, so neuter/flip
  interventions propagate) gets +6 on SUP/CON — it bears on the claim rather
  than being merely topical. No lexicon, no feature→verdict shortcut.
- **Coverage readings** (hids 90+t): token-level addressability, GEN'd after
  interpretation ELIM from surviving SUP/CON candidates only.
- **Verdict bids** (hids 200–203): FACT (nsup≥1 ∧ ncon=0; 211+best ovl),
  LIE (ncon≥1 ∧ nsup=0; 211+best ovl), OPINION (any R_O* fired; 208; skipped in
  study mode), UNDETERMINED (no evidence or contested; 203+6 if contested).
  Fire conditions read ONLY ledger rows. Exactly one of FACT/LIE/UNDET fires
  in all cases (airtight; OPINION may co-fire).
- **NEED** emitted by the UNDET branch from coverage rows: `NEED: CONTESTED`
  or up to 3 uncovered claim content tokens (sense tokens, claim order).
- **Retrieval**: token-overlap over 448 mass items, self excluded, top-16 by
  (overlap desc, index asc). Proposes candidates; never judges.
- **Learning** (prereg §7.1): study-mode deliberation (no OPINION bid, no R_O*
  rows) over all 448 items, self-excluded; per-pattern decide-rate
  (FACT|LIE)/n vs plain baseline; formation deliberation per pattern
  (H_ADDR score=rate_P ‰ vs H_UNADDR score=max(0, rate_0−rate_P) ‰; ARGMAX;
  tie → H_ADDR conservative). Frozen to `learned_readings.tsv` +
  `formation_record.tsv` (SHA-256 pinned) before LOO; no learning during LOO.

## Bugs found and fixed during this attempt

1. `load_formed` skipped 2 tabs instead of 1 → formed flags parsed as 0
   (first LOO pair ran with learnings unloaded; discarded, rerun after fix).
2. LOO argv parsing was position-dependent → flip legs and `notraces`
   silently no-oped in the first causal matrix (neuter legs were valid).
3. First congruence implementation read the claim pattern from mass instead
   of the ledger → neuter/flip on utterance-type readings could not
   propagate (caught by the neuter matrix showing 0 flips; fixed to derive
   the claim signature from ledger reading rows).
