# PREREG — PAMs v2 contradiction-matrix experiment (follow-up item 6)

**Status: FROZEN 2026-09-23. Committed alone — before any build output exists.**
**Program:** PAMs v2 follow-up, contradiction matrix (Micah: YES, RUN FOR SURE).

## 1. Settling-experiment linkage

Sol debate Round 4 (v2/debates/DEBATES_V2_R2.md), disagreement #4 (FS-G completeness) STANDS:
> "FS-G bars do not, by themselves, specify what happens when evidence conflicts, when a corroborator is wrong, or when a stronger signal contradicts an incumbent. Trial 1145 is a concrete demonstration of the gap."
> The settling experiment is a contradiction matrix covering incumbent/new-answer conflicts, confidence reversals, correlated corroborators, missing history, and ties. Each cell needs a preregistered outcome.

Sol's new #1 architecture (revisable admission/install gate with historical corroboration only) depends on this experiment: the matrix pins down the contradiction behavior BEFORE the gate is built (debate moderation note: 'The contradiction-matrix experiment ... should run before this gate is built, or v2 repeats the R2-4 mistake of unspecified contradiction behavior.').

## 2. Candidate gates under test

#### G0-frozen-R2-4

```
G0 — frozen R2-4/H2 gate (NEGATIVE CONTROL; memgate.zag §§1.1/2 verbatim, single-task):
  tol = tol_of(tcode)  (0:8, 1:40, 2:60, 3:4000, 4:120, 5:0)
  on trial:
    if prog != PASS: return WITHHELD
    if pred != 1: return WITHHELD                      # defensive; frozen: pred always 1 when PASS
    if perm.on:
      if jcode == perm.j: return CORROBORATED
      return CONFLICT_WITHHELD                          # §1.1 verbatim rule; consults only jcode vs perm_j
    if prov.on:
      if jcode == prov.j and |meas - prov.m| <= tol:
        perm := (jcode, meas); prov.clear; return PERMANENT_INSTALL
      prov := (jcode, meas); return PROVISIONAL_INSTALL  # conflicting PASS reverses provisional
    prov := (jcode, meas); return PROVISIONAL_INSTALL
  Preregistered behavior: CONFLICT_WITHHELD on every permanent-conflict cell; never revises.
```

#### G1-cf1-historical

```
G1 — cf1 historical-corroboration gate (AUTOPSY_R2-4 §4, pure-Zag implementation from spec;
  no cf1 Zag had landed on the branch as of 2026-09-23):
  state: G0 state + challenger slot chal{on,j,m} + no_hist flag
  on trial:
    if prog != PASS: return WITHHELD
    if pred != 1: return WITHHELD
    inc_set = perm.on or prov.on; inc_j/inc_m = perm's (or prov's if no perm)
    if inc_set and jcode == inc_j:
      if |meas - inc_m| <= tol:
        if perm.on: return CORROBORATED
        if conf >= 700: perm := (jcode,meas,conf,seq); prov.clear; return PERMANENT_INSTALL  # §4.2 bar
        return PROVISIONAL_INSTALL                        # bar blocks promotion; provisional re-affirmed
      prov := (jcode, meas); return PROVISIONAL_INSTALL    # same jcode outside tol: re-anchor (specified, unexercised)
    if inc_set and jcode != inc_j:                         # CONFLICT
      if conf >= 700 and no_hist == 0:                     # §4.1 challenger path (no FAILs in matrix: negative check vacuous)
        if chal.on and chal.j == jcode and |meas - chal.m| <= tol:
          perm := (jcode,meas,conf,seq); chal.clear; return REVISED_INSTALL
        chal := (jcode, meas); return CHALLENGER_PROV
      return CONFLICT_WITHHELD                             # frozen fallback: sub-700 challenger or no history
    prov := (jcode, meas); return PROVISIONAL_INSTALL      # no incumbent
  Specified choice (frozen here): no single-observation revision of a provisional either (1145 lesson
  generalizes); the challenger slot is the only revision path. §4 step 3 (mrgF>=T3 margin bar) is
  NOT included: marked 'verify in Zag before adopting' in the autopsy; it is the preregistered
  follow-up candidate for the CC1 caveat. §4 step 4 (corroborated negative evidence) is specified
  but vacuous in this matrix (no FAIL trials).
```

#### G2-V2D-hardened

```
G2 — V2-D-hardened gate (detector spec REDTEAM_V2 §4 + PREREG_V2-D §2; hardening: prog-required
  + conflict adjudication):
  D_fires = (prog == PASS and pred == 1 and jG == jcode and conf >= 700 and confG >= 700)
    # prog-required HARDENING: V2-D's landed rule (jG==jF && confF>=700 && confG>=700, no prog check)
    # fired on UNRESOLVED trials -> REDTEAM_V2 §4 KILL (43 ACCEPT_INSTALL, 9 false). D now requires PASS.
  on trial:
    if D_fires:
      if perm.on and jcode == perm.j: return CORROBORATED
      if perm.on and jcode != perm.j:                       # CONFLICT -> adjudication (HARDENING)
        if no_hist == 0 and dchal.on and dchal.j == jcode and |meas - dchal.m| <= tol:
          perm := (jcode,meas,conf,seq); dchal.clear; return REVISED_INSTALL
        if no_hist == 0: dchal := (jcode, meas); return CHALLENGER_PROV
        return CONFLICT_WITHHELD
      if prov.on and jcode == prov.j and |meas - prov.m| <= tol:
        perm := (jcode,meas,conf,seq); prov.clear; return PERMANENT_INSTALL  # D confirms provisional
      if prov.on and jcode != prov.j:                       # conflict vs provisional: same adjudication
        if no_hist == 0 and dchal.on and dchal.j == jcode and |meas - dchal.m| <= tol:
          perm := (jcode,meas,conf,seq); prov.clear; dchal.clear; return REVISED_INSTALL
        if no_hist == 0: dchal := (jcode, meas); return CHALLENGER_PROV
        return CONFLICT_WITHHELD
      perm := (jcode,meas,conf,seq); return ACCEPT_INSTALL  # truth-acceptance path, no incumbent
    <G0 logic verbatim>                                     # D not fired: H2-style gate path UNCHANGED
  dchal is a SEPARATE slot from G1's chal (V2-D separates the D path from the gate path).
  Specified choice (frozen here): D-fired conflicts need corroboration against permanent AND
  provisional incumbents; a single D-fired observation never revises an installed claim.
```

Disposition vocabulary (frozen): 0=PERMANENT_INSTALL, 1=PROVISIONAL_INSTALL, 2=CORROBORATED, 3=CONFLICT_WITHHELD, 4=CHALLENGER_PROV, 5=REVISED_INSTALL, 6=ACCEPT_INSTALL, 7=WITHHELD.

Truth handling: every trial row carries a `truth` field for scoring. Gates NEVER read it (contractually off-limits, as in memgate.zag: 'truth is PASSED THROUGH ... and is NEVER used in any gate rule'). The harness enforces this structurally: gate functions take only (prog, jcode, conf, pred, meas, jG, confG); truth is read only by the scorer.

## 3. Cells

Trial rows are RECORD-level (the gate's actual input contract per memgate.zag's header: `seq|tcode|fixture|prog|jcode|judgment|confidence|pred|measure|phash|truth`). Frozen rows are cited by seq from `senses/pam-rebuild/round2/forks/R2-4/evidence/clean/sweep.jsonl`; synthetic rows are used only where the frozen stream lacks the cell geometry, with values drawn from frozen distribution ranges (AUTOPSY_R2-4 §2.2: correct-colordisc conf p10/median/p90 = 729/851/907, mrgF median 8620/637). G-span fields (jG, confG) are synthetic throughout (preregistered per trial): the matrix tests gate contradiction logic, not the sense; jG=9 is a sentinel meaning 'G span disagrees' (D cannot fire).

### Cell C1 — correct challenger (should revise)

**Should:** Two corroborating correct high-conf conflicting PASSes revise the permanent install. Single-observation revision stays banned (trial-1145 lesson).

| # | label | tcode | prog | jcode(judg) | conf | pred | meas | mrgF | truth | jG | confG | provenance |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | S1 | 0 | PASS | 0 (SAME) | 605 | 1 | 0 | 2300 | 0 (SAME) | 9 | 0 | frozen: sweep.jsonl seq 721 (colordisc SAME, truth SAME) |
| 1 | S2 | 0 | PASS | 0 (SAME) | 750 | 1 | 3 | 2400 | 0 (SAME) | 9 | 0 | synthetic corroborator; |3-0|=3<=tol 8; conf in frozen correct-SAME band |
| 2 | T2 | 0 | PASS | 1 (DIFFERENT) | 814 | 1 | 89 | 6600 | 1 (DIFFERENT) | 1 | 830 | frozen: sweep.jsonl seq 1262 (DIFFERENT, truth DIFFERENT: correct) |
| 3 | T3 | 0 | PASS | 1 (DIFFERENT) | 827 | 1 | 95 | 7212 | 1 (DIFFERENT) | 1 | 840 | frozen: sweep.jsonl seq 1330 (DIFFERENT, truth DIFFERENT: correct); |95-89|=6<=tol 8 |

**Preregistered expectations:**

| gate | expected disposition sequence | expected final perm jcode | expected false install | rule cited |
|---|---|---|---|---|
| G0-frozen-R2-4 | PROVISIONAL_INSTALL, PERMANENT_INSTALL, CONFLICT_WITHHELD, CONFLICT_WITHHELD | 0 | 0 | frozen rule: conflict vs permanent -> CONFLICT_WITHHELD (negative control; documents the 9.4% RK-3 failure) |
| G1-cf1-historical | PROVISIONAL_INSTALL, PERMANENT_INSTALL, CHALLENGER_PROV, REVISED_INSTALL | 1 | 0 | AUTOPSY §4.1: T2 stored as challenger (CHALLENGER_PROV); T3 same jcode, |95-89|<=8 -> REVISED_INSTALL (correct) |
| G2-V2D-hardened | PROVISIONAL_INSTALL, PERMANENT_INSTALL, CHALLENGER_PROV, REVISED_INSTALL | 1 | 0 | hardened adjudication: T2 D-fired conflict -> CHALLENGER_PROV; T3 D-fired corroboration -> REVISED_INSTALL (correct) |

### Cell C2 — wrong challenger (should withhold)

**Should:** A single wrong high-conf conflicting PASS must not revise. Stored as challenger only.

| # | label | tcode | prog | jcode(judg) | conf | pred | meas | mrgF | truth | jG | confG | provenance |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | S1 | 4 | PASS | 3 (BRIGHT) | 760 | 1 | 2480 | 500 | 3 (BRIGHT) | 9 | 0 | synthetic BRIGHT incumbent; conf/meas in frozen timbredisc high-conf band |
| 1 | S2 | 4 | PASS | 3 (BRIGHT) | 770 | 1 | 2490 | 510 | 3 (BRIGHT) | 9 | 0 | synthetic; |2490-2480|=10<=tol 120 |
| 2 | T2 | 4 | PASS | 2 (RICH) | 718 | 1 | 2618 | 382 | 3 (BRIGHT) | 2 | 720 | frozen: sweep.jsonl seq 10983 (judg RICH, truth BRIGHT: wrong) |

**Preregistered expectations:**

| gate | expected disposition sequence | expected final perm jcode | expected false install | rule cited |
|---|---|---|---|---|
| G0-frozen-R2-4 | PROVISIONAL_INSTALL, PERMANENT_INSTALL, CONFLICT_WITHHELD | 3 | 0 | frozen conflict rule |
| G1-cf1-historical | PROVISIONAL_INSTALL, PERMANENT_INSTALL, CHALLENGER_PROV | 3 | 0 | AUTOPSY §4.1: singleton challenger -> CHALLENGER_PROV, no revision |
| G2-V2D-hardened | PROVISIONAL_INSTALL, PERMANENT_INSTALL, CHALLENGER_PROV | 3 | 0 | D fires (jG==jF, confs>=700, prog PASS) but conflict adjudication needs corroboration -> CHALLENGER_PROV |

### Cell C3 — 1145-class dominator (should withhold)

**Should:** A wrong challenger that STRICTLY DOMINATES the incumbent on every evidence axis (conf 874>605, mrgF 10410>2300) must still not revise: pointwise adjudication is machinery-impossible (AUTOPSY §2.2). The naive single-shot rule (cf2) installs it; cf1-class gates must not.

| # | label | tcode | prog | jcode(judg) | conf | pred | meas | mrgF | truth | jG | confG | provenance |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | S1 | 0 | PASS | 0 (SAME) | 605 | 1 | 0 | 2300 | 0 (SAME) | 9 | 0 | frozen: sweep.jsonl seq 721 (colordisc SAME incumbent) |
| 1 | S2 | 0 | PASS | 0 (SAME) | 750 | 1 | 3 | 2400 | 0 (SAME) | 9 | 0 | synthetic; |3-0|<=8 |
| 2 | T2 | 0 | PASS | 1 (DIFFERENT) | 874 | 1 | 127 | 10410 | 0 (SAME) | 1 | 850 | frozen: sweep.jsonl seq 1145 (DIFFERENT, truth SAME: wrong; dominates incumbent on conf and mrgF) |

**Preregistered expectations:**

| gate | expected disposition sequence | expected final perm jcode | expected false install | rule cited |
|---|---|---|---|---|
| G0-frozen-R2-4 | PROVISIONAL_INSTALL, PERMANENT_INSTALL, CONFLICT_WITHHELD | 0 | 0 | frozen conflict rule |
| G1-cf1-historical | PROVISIONAL_INSTALL, PERMANENT_INSTALL, CHALLENGER_PROV | 0 | 0 | AUTOPSY §2.2/§4.1: domination is pointwise; singleton -> CHALLENGER_PROV |
| G2-V2D-hardened | PROVISIONAL_INSTALL, PERMANENT_INSTALL, CHALLENGER_PROV | 0 | 0 | D fires, but single D-fired observation cannot revise -> CHALLENGER_PROV |

### Cell R1 — confidence reversal: high-conf incumbent vs low-conf challenger

**Should:** A sub-700 challenger is not a revision candidate under any gate (cf1 §4.1 requires conf>=700; V2-D detector requires confF>=700). Withhold.

| # | label | tcode | prog | jcode(judg) | conf | pred | meas | mrgF | truth | jG | confG | provenance |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | S1 | 0 | PASS | 0 (SAME) | 900 | 1 | 0 | 8000 | 0 (SAME) | 9 | 0 | synthetic high-conf incumbent |
| 1 | S2 | 0 | PASS | 0 (SAME) | 920 | 1 | 3 | 8100 | 0 (SAME) | 9 | 0 | synthetic; |3-0|<=8 |
| 2 | T2 | 0 | PASS | 1 (DIFFERENT) | 650 | 1 | 90 | 5000 | 1 (DIFFERENT) | 1 | 660 | synthetic low-conf challenger (conf 650<700); truth DIFFERENT (correct but weak) |

**Preregistered expectations:**

| gate | expected disposition sequence | expected final perm jcode | expected false install | rule cited |
|---|---|---|---|---|
| G0-frozen-R2-4 | PROVISIONAL_INSTALL, PERMANENT_INSTALL, CONFLICT_WITHHELD | 0 | 0 | frozen conflict rule |
| G1-cf1-historical | PROVISIONAL_INSTALL, PERMANENT_INSTALL, CONFLICT_WITHHELD | 0 | 0 | challenger conf<700 -> not a candidate; frozen fallback CONFLICT_WITHHELD |
| G2-V2D-hardened | PROVISIONAL_INSTALL, PERMANENT_INSTALL, CONFLICT_WITHHELD | 0 | 0 | confF<700 -> D cannot fire; H2 gate path -> CONFLICT_WITHHELD |

### Cell R2 — confidence reversal: low-conf incumbent vs high-conf challenger

**Should:** A single high-conf challenger must not revise even a low-conf incumbent (1145's own incumbent was conf 605). Corroboration is still required. cf1's permanence bar (§4.2) additionally keeps the sub-700 incumbent provisional.

| # | label | tcode | prog | jcode(judg) | conf | pred | meas | mrgF | truth | jG | confG | provenance |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | S1 | 0 | PASS | 0 (SAME) | 500 | 1 | 0 | 2000 | 0 (SAME) | 9 | 0 | synthetic low-conf incumbent (frozen gate granted sub-700 permanents: AUTOPSY §1.2) |
| 1 | S2 | 0 | PASS | 0 (SAME) | 520 | 1 | 2 | 2100 | 0 (SAME) | 9 | 0 | synthetic; |2-0|<=8 |
| 2 | T2 | 0 | PASS | 1 (DIFFERENT) | 850 | 1 | 90 | 7000 | 1 (DIFFERENT) | 1 | 860 | synthetic high-conf challenger, SINGLE observation; truth DIFFERENT (correct) |

**Preregistered expectations:**

| gate | expected disposition sequence | expected final perm jcode | expected false install | rule cited |
|---|---|---|---|---|
| G0-frozen-R2-4 | PROVISIONAL_INSTALL, PERMANENT_INSTALL, CONFLICT_WITHHELD | 0 | 0 | frozen: no conf bar on permanence; conflict -> CONFLICT_WITHHELD |
| G1-cf1-historical | PROVISIONAL_INSTALL, PROVISIONAL_INSTALL, CHALLENGER_PROV | none | 0 | §4.2 bar blocks permanence at conf 520 (stays provisional); singleton challenger -> CHALLENGER_PROV; no single-observation reversal even of provisionals |
| G2-V2D-hardened | PROVISIONAL_INSTALL, PERMANENT_INSTALL, CHALLENGER_PROV | 0 | 0 | H2 gate path grants permanent (no conf bar); D-fired conflict needs corroboration -> CHALLENGER_PROV |

### Cell CC1 — correlated corroborators: two WRONG challengers agreeing (should NOT revise)

**Should:** PREREGISTERED KNOWN-UNSAFE for G1/G2. Two wrong high-conf PASSes agreeing within tolerance trigger corroborated revision under cf1-class rules -> FALSE INSTALL. This is AUTOPSY §2.3's caveat made concrete (the six corroborated-wrong RICH trials). The mrgF>=T3 margin bar (§4 step 3, unverified in Zag) is the candidate fix, NOT part of these gates.

| # | label | tcode | prog | jcode(judg) | conf | pred | meas | mrgF | truth | jG | confG | provenance |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | S1 | 4 | PASS | 3 (BRIGHT) | 760 | 1 | 2480 | 500 | 3 (BRIGHT) | 9 | 0 | synthetic BRIGHT incumbent |
| 1 | S2 | 4 | PASS | 3 (BRIGHT) | 770 | 1 | 2490 | 510 | 3 (BRIGHT) | 9 | 0 | synthetic; |2490-2480|=10<=tol 120 |
| 2 | T2 | 4 | PASS | 2 (RICH) | 718 | 1 | 2618 | 382 | 3 (BRIGHT) | 2 | 720 | frozen: sweep.jsonl seq 10983 (RICH, truth BRIGHT: wrong) |
| 3 | T3 | 4 | PASS | 2 (RICH) | 704 | 1 | 2642 | 358 | 3 (BRIGHT) | 2 | 710 | frozen: sweep.jsonl seq 10992 (RICH, truth BRIGHT: wrong); |2642-2618|=24<=tol 120 |

**Preregistered expectations:**

| gate | expected disposition sequence | expected final perm jcode | expected false install | rule cited |
|---|---|---|---|---|
| G0-frozen-R2-4 | PROVISIONAL_INSTALL, PERMANENT_INSTALL, CONFLICT_WITHHELD, CONFLICT_WITHHELD | 3 | 0 | frozen conflict rule; no false install |
| G1-cf1-historical | PROVISIONAL_INSTALL, PERMANENT_INSTALL, CHALLENGER_PROV, REVISED_INSTALL | 2 | 1 | AUTOPSY §2.3 caveat: correlated wrong pair corroborates -> REVISED_INSTALL installs WRONG judgment. KNOWN UNSAFE. |
| G2-V2D-hardened | PROVISIONAL_INSTALL, PERMANENT_INSTALL, CHALLENGER_PROV, REVISED_INSTALL | 2 | 1 | same structural caveat via D-fired corroboration -> REVISED_INSTALL installs WRONG judgment. KNOWN UNSAFE. |

> KNOWN-UNSAFE CELL: a false install is preregistered for the named gate(s). Pass/fail for those gate-cells is still expected-vs-actual (the rule behaving as specified); the matrix verdict separately records that the gate is not fully safe.

### Cell CC2 — correlated corroborators: two CORRECT challengers agreeing (should revise)

**Should:** Two correct high-conf conflicting PASSes agreeing within tolerance revise (independent corroborator pair from C1: meas 89/89).

| # | label | tcode | prog | jcode(judg) | conf | pred | meas | mrgF | truth | jG | confG | provenance |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | S1 | 0 | PASS | 0 (SAME) | 605 | 1 | 0 | 2300 | 0 (SAME) | 9 | 0 | frozen: sweep.jsonl seq 721 |
| 1 | S2 | 0 | PASS | 0 (SAME) | 750 | 1 | 3 | 2400 | 0 (SAME) | 9 | 0 | synthetic; |3-0|<=8 |
| 2 | T2 | 0 | PASS | 1 (DIFFERENT) | 814 | 1 | 89 | 6600 | 1 (DIFFERENT) | 1 | 830 | frozen: sweep.jsonl seq 1262 (correct) |
| 3 | T3 | 0 | PASS | 1 (DIFFERENT) | 814 | 1 | 89 | 6603 | 1 (DIFFERENT) | 1 | 835 | frozen: sweep.jsonl seq 1689 (DIFFERENT, truth DIFFERENT: correct); |89-89|=0<=tol 8 |

**Preregistered expectations:**

| gate | expected disposition sequence | expected final perm jcode | expected false install | rule cited |
|---|---|---|---|---|
| G0-frozen-R2-4 | PROVISIONAL_INSTALL, PERMANENT_INSTALL, CONFLICT_WITHHELD, CONFLICT_WITHHELD | 0 | 0 | frozen conflict rule (negative control) |
| G1-cf1-historical | PROVISIONAL_INSTALL, PERMANENT_INSTALL, CHALLENGER_PROV, REVISED_INSTALL | 1 | 0 | §4.1 corroborated revision (correct) |
| G2-V2D-hardened | PROVISIONAL_INSTALL, PERMANENT_INSTALL, CHALLENGER_PROV, REVISED_INSTALL | 1 | 0 | hardened adjudication: D-fired corroboration -> REVISED_INSTALL (correct) |

### Cell H1 — missing history: conflict with no ledger history (should withhold)

**Should:** With no history the corroboration path is inert; all gates fall back to the frozen withhold. A correct challenger that cannot be corroborated must still wait.

**Preinstall (no trial history):** permanent := (jcode=0, meas=0, conf=605, seq=721); no_hist=1.

| # | label | tcode | prog | jcode(judg) | conf | pred | meas | mrgF | truth | jG | confG | provenance |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | T0 | 0 | PASS | 1 (DIFFERENT) | 814 | 1 | 89 | 6600 | 1 (DIFFERENT) | 1 | 830 | frozen: sweep.jsonl seq 1262 values; correct challenger, but NO history available to the gate |

**Preregistered expectations:**

| gate | expected disposition sequence | expected final perm jcode | expected false install | rule cited |
|---|---|---|---|---|
| G0-frozen-R2-4 | CONFLICT_WITHHELD | 0 | 0 | conflict rule consults no history |
| G1-cf1-historical | CONFLICT_WITHHELD | 0 | 0 | §4.1 requires a corroborating observation; no_hist -> challenger slot inert -> frozen fallback |
| G2-V2D-hardened | CONFLICT_WITHHELD | 0 | 0 | D fires, but adjudication requires history; no_hist -> CONFLICT_WITHHELD |

### Cell T1 — tie: challenger and incumbent at equal evidence (should withhold)

**Should:** Equal evidence is not corroboration. A single tied challenger is stored (cf1-class) or withheld (frozen); never installed.

| # | label | tcode | prog | jcode(judg) | conf | pred | meas | mrgF | truth | jG | confG | provenance |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | S1 | 0 | PASS | 0 (SAME) | 800 | 1 | 0 | 5000 | 0 (SAME) | 9 | 0 | synthetic incumbent conf 800 |
| 1 | S2 | 0 | PASS | 0 (SAME) | 800 | 1 | 3 | 5000 | 0 (SAME) | 9 | 0 | synthetic; |3-0|<=8 |
| 2 | T2 | 0 | PASS | 1 (DIFFERENT) | 800 | 1 | 90 | 5000 | 1 (DIFFERENT) | 1 | 800 | synthetic challenger at EQUAL evidence (conf 800, mrgF 5000); truth DIFFERENT (correct but tied) |

**Preregistered expectations:**

| gate | expected disposition sequence | expected final perm jcode | expected false install | rule cited |
|---|---|---|---|---|
| G0-frozen-R2-4 | PROVISIONAL_INSTALL, PERMANENT_INSTALL, CONFLICT_WITHHELD | 0 | 0 | frozen conflict rule |
| G1-cf1-historical | PROVISIONAL_INSTALL, PERMANENT_INSTALL, CHALLENGER_PROV | 0 | 0 | singleton -> CHALLENGER_PROV; tie is not corroboration |
| G2-V2D-hardened | PROVISIONAL_INSTALL, PERMANENT_INSTALL, CHALLENGER_PROV | 0 | 0 | D-fired singleton conflict -> CHALLENGER_PROV |

### Cell W1 — withhold-everything regression (UNRESOLVED stream; V2-D KILL guard)

**Should:** Trials the sense left UNRESOLVED must never install, even when the detector's conf/judgment conditions are met. This is REDTEAM_V2 §4's KILL against unhardened V2-D (43 ACCEPT_INSTALL on 288 UNRESOLVED trials, 9 false). The prog-required hardening must hold.

| # | label | tcode | prog | jcode(judg) | conf | pred | meas | mrgF | truth | jG | confG | provenance |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | T0 | 0 | UNRESOLVED | 1 (DIFFERENT) | 850 | 0 | 90 | 0 | 1 (DIFFERENT) | 1 | 850 | synthetic UNRESOLVED; D conf/judgment conditions met but prog!=PASS |
| 1 | T1 | 0 | UNRESOLVED | 1 (DIFFERENT) | 850 | 0 | 90 | 0 | 0 (SAME) | 1 | 850 | synthetic UNRESOLVED |
| 2 | T2 | 0 | UNRESOLVED | 1 (DIFFERENT) | 850 | 0 | 90 | 0 | 1 (DIFFERENT) | 1 | 850 | synthetic UNRESOLVED |

**Preregistered expectations:**

| gate | expected disposition sequence | expected final perm jcode | expected false install | rule cited |
|---|---|---|---|---|
| G0-frozen-R2-4 | WITHHELD, WITHHELD, WITHHELD | none | 0 | prog!=PASS -> WITHHELD; zero installs |
| G1-cf1-historical | WITHHELD, WITHHELD, WITHHELD | none | 0 | prog!=PASS -> WITHHELD; zero installs |
| G2-V2D-hardened | WITHHELD, WITHHELD, WITHHELD | none | 0 | prog-required: D cannot fire on UNRESOLVED -> H2 gate path -> WITHHELD; zero installs |

## 4. Execution protocol (frozen)

- Pure-Zag battery `src/cm_main.zag` (+ generated `src/cm_records.zag`): runs every cell through every gate, printing one `CM|cell|gate|trial|disp|perm_j|perm_seq` line per trial.
- Three full runs; sha256 of each run's stdout must be byte-identical (zero RNG; all inputs literal).
- Python scorer (`score_cm.py`, glue only) parses stdout and compares against EXPECT.tsv / EXPECT_CELL.tsv (both generated from this prereg, committed with it).
- Per gate-cell: PASS iff emitted disposition sequence == preregistered sequence AND false-install flag == preregistered AND (W1) install count == 0.
- Build: `znc_linux_x86_64_abed8aa1 src/cm_main.zag -o cm_bin` (toolchain path in RUNLOG). No binaries or .zagd committed.

## 5. Verdict rules (frozen)

- **Fully-specified:** every cell's emitted dispositions were produced by a named preregistered rule; no trial fell through to an unspecified/defensive branch unexpectedly (the defensive branches are specified above; hitting one where not preregistered = cell FAIL).
- **Safe:** no false installs in any cell (a false install = final permanent jcode differs from the cell's correct final jcode). CC1's preregistered false installs for G1/G2 are recorded as known-unsafe behavior, not as surprise failures.
- **Verdict question:** which gates have fully-specified contradiction behavior with no false installs? A gate that withholds correct revisions (G0) is specified-and-safe but does not revise; a gate that revises correctly but false-installs on correlated wrong corroborators (G1/G2 on CC1) is specified but not fully safe.
- Follow-up already preregistered: the mrgF>=T3 challenger margin bar (AUTOPSY §4 step 3) is the candidate fix for the CC1 caveat; it needs its own Zag verification before adoption.

## 6. Commit map

- This prereg (ALONE): `senses/pam-rebuild/v2/contradiction_matrix/PREREG_CONTRADICTION_MATRIX.md`, `gen_cells.py`, `EXPECT.tsv`, `EXPECT_CELL.tsv`.
- Build + evidence + verdict: `src/cm_main.zag`, `src/cm_records.zag` (generated), `src/R33_NATIVE_IO_V1.zag`, `evidence/run{1,2,3}.txt`, `evidence/DIGESTS.txt`, `evidence/score.tsv`, `RUNLOG.md`, `CONTRADICTION_MATRIX.md`.
- Branch `tnn-native-lab`, repo `sylorlabs/TNN`, via `~/workspace/commit_racefree.py`, TMPDIR=`~/workspace/tmp_commit`, lab-relative paths. No binaries, no `.zagd`. Additive-only.

**Laws:** pure Zag for mechanisms/learners/verification; Python only for glue/analysis. Zero RNG in any decision path. Byte-identical reruns required.

