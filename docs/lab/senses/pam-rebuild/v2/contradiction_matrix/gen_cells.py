#!/usr/bin/env python3
"""Single source of truth for the PAMs v2 contradiction-matrix experiment.

Generates from the frozen cell definitions:
  1. PREREG_CONTRADICTION_MATRIX.md  (human-readable frozen prereg)
  2. EXPECT.tsv                      (cell, gate, trial_idx, expected disp code)
  3. EXPECT_CELL.tsv                 (cell, gate, expected final perm j, false-install flag, install count)
  4. cm_records.zag                 (Zag trial/cell table initializer)

The prereg markdown is REVIEWED before the prereg commit; the Zag battery and
the Python scorer both derive from this file, so no transcription drift is
possible between prereg text, built trials, and scoring.

Zero RNG: every value is a literal.
"""
import os

OUT = os.path.dirname(os.path.abspath(__file__))

# Disposition codes (frozen for this battery)
D_PERM = 0   # PERMANENT_INSTALL
D_PROV = 1   # PROVISIONAL_INSTALL
D_CORR = 2   # CORROBORATED
D_CONF = 3   # CONFLICT_WITHHELD
D_CHAL = 4   # CHALLENGER_PROV
D_REV  = 5   # REVISED_INSTALL
D_ACC  = 6   # ACCEPT_INSTALL
D_WITH = 7   # WITHHELD
DISP_NAME = {0:"PERMANENT_INSTALL",1:"PROVISIONAL_INSTALL",2:"CORROBORATED",
             3:"CONFLICT_WITHHELD",4:"CHALLENGER_PROV",5:"REVISED_INSTALL",
             6:"ACCEPT_INSTALL",7:"WITHHELD"}

# Gates
G0 = 0  # frozen R2-4/H2 gate (negative control)
G1 = 1  # cf1 historical-corroboration (AUTOPSY_R2-4 §4)
G2 = 2  # V2-D hardened (prog-required + conflict adjudication)
GATE_NAME = {0:"G0-frozen-R2-4",1:"G1-cf1-historical",2:"G2-V2D-hardened"}

# prog codes: 0=PASS 1=FAIL 2=UNRESOLVED (memgate.zag header)
# tcode: 0=colordisc(tol 8) 4=timbredisc(tol 120)
# truth/jcode: 0=SAME 1=DIFFERENT 2=RICH 3=BRIGHT

# Trial tuple: (label, tcode, prog, jcode, conf, pred, meas, mrgF, truth, jG, confG, provenance)
CELLS = [
 dict(
  name="C1", title="correct challenger (should revise)",
  should="Two corroborating correct high-conf conflicting PASSes revise the permanent install. "
         "Single-observation revision stays banned (trial-1145 lesson).",
  no_hist=False, preinstall=None, correct_final_j=1,
  trials=[
   ("S1",0,0,0,605,1,0,2300,0, 9,0, "frozen: sweep.jsonl seq 721 (colordisc SAME, truth SAME)"),
   ("S2",0,0,0,750,1,3,2400,0, 9,0, "synthetic corroborator; |3-0|=3<=tol 8; conf in frozen correct-SAME band"),
   ("T2",0,0,1,814,1,89,6600,1, 1,830, "frozen: sweep.jsonl seq 1262 (DIFFERENT, truth DIFFERENT: correct)"),
   ("T3",0,0,1,827,1,95,7212,1, 1,840, "frozen: sweep.jsonl seq 1330 (DIFFERENT, truth DIFFERENT: correct); |95-89|=6<=tol 8"),
  ],
  expect={
   G0:([D_PROV,D_PERM,D_CONF,D_CONF],0,0,"frozen rule: conflict vs permanent -> CONFLICT_WITHHELD (negative control; documents the 9.4% RK-3 failure)"),
   G1:([D_PROV,D_PERM,D_CHAL,D_REV],1,0,"AUTOPSY §4.1: T2 stored as challenger (CHALLENGER_PROV); T3 same jcode, |95-89|<=8 -> REVISED_INSTALL (correct)"),
   G2:([D_PROV,D_PERM,D_CHAL,D_REV],1,0,"hardened adjudication: T2 D-fired conflict -> CHALLENGER_PROV; T3 D-fired corroboration -> REVISED_INSTALL (correct)"),
  }),
 dict(
  name="C2", title="wrong challenger (should withhold)",
  should="A single wrong high-conf conflicting PASS must not revise. Stored as challenger only.",
  no_hist=False, preinstall=None, correct_final_j=3,
  trials=[
   ("S1",4,0,3,760,1,2480,500,3, 9,0, "synthetic BRIGHT incumbent; conf/meas in frozen timbredisc high-conf band"),
   ("S2",4,0,3,770,1,2490,510,3, 9,0, "synthetic; |2490-2480|=10<=tol 120"),
   ("T2",4,0,2,718,1,2618,382,3, 2,720, "frozen: sweep.jsonl seq 10983 (judg RICH, truth BRIGHT: wrong)"),
  ],
  expect={
   G0:([D_PROV,D_PERM,D_CONF],3,0,"frozen conflict rule"),
   G1:([D_PROV,D_PERM,D_CHAL],3,0,"AUTOPSY §4.1: singleton challenger -> CHALLENGER_PROV, no revision"),
   G2:([D_PROV,D_PERM,D_CHAL],3,0,"D fires (jG==jF, confs>=700, prog PASS) but conflict adjudication needs corroboration -> CHALLENGER_PROV"),
  }),
 dict(
  name="C3", title="1145-class dominator (should withhold)",
  should="A wrong challenger that STRICTLY DOMINATES the incumbent on every evidence axis "
         "(conf 874>605, mrgF 10410>2300) must still not revise: pointwise adjudication is "
         "machinery-impossible (AUTOPSY §2.2). The naive single-shot rule (cf2) installs it; "
         "cf1-class gates must not.",
  no_hist=False, preinstall=None, correct_final_j=0,
  trials=[
   ("S1",0,0,0,605,1,0,2300,0, 9,0, "frozen: sweep.jsonl seq 721 (colordisc SAME incumbent)"),
   ("S2",0,0,0,750,1,3,2400,0, 9,0, "synthetic; |3-0|<=8"),
   ("T2",0,0,1,874,1,127,10410,0, 1,850, "frozen: sweep.jsonl seq 1145 (DIFFERENT, truth SAME: wrong; dominates incumbent on conf and mrgF)"),
  ],
  expect={
   G0:([D_PROV,D_PERM,D_CONF],0,0,"frozen conflict rule"),
   G1:([D_PROV,D_PERM,D_CHAL],0,0,"AUTOPSY §2.2/§4.1: domination is pointwise; singleton -> CHALLENGER_PROV"),
   G2:([D_PROV,D_PERM,D_CHAL],0,0,"D fires, but single D-fired observation cannot revise -> CHALLENGER_PROV"),
  }),
 dict(
  name="R1", title="confidence reversal: high-conf incumbent vs low-conf challenger",
  should="A sub-700 challenger is not a revision candidate under any gate (cf1 §4.1 requires conf>=700; "
         "V2-D detector requires confF>=700). Withhold.",
  no_hist=False, preinstall=None, correct_final_j=0,
  trials=[
   ("S1",0,0,0,900,1,0,8000,0, 9,0, "synthetic high-conf incumbent"),
   ("S2",0,0,0,920,1,3,8100,0, 9,0, "synthetic; |3-0|<=8"),
   ("T2",0,0,1,650,1,90,5000,1, 1,660, "synthetic low-conf challenger (conf 650<700); truth DIFFERENT (correct but weak)"),
  ],
  expect={
   G0:([D_PROV,D_PERM,D_CONF],0,0,"frozen conflict rule"),
   G1:([D_PROV,D_PERM,D_CONF],0,0,"challenger conf<700 -> not a candidate; frozen fallback CONFLICT_WITHHELD"),
   G2:([D_PROV,D_PERM,D_CONF],0,0,"confF<700 -> D cannot fire; H2 gate path -> CONFLICT_WITHHELD"),
  }),
 dict(
  name="R2", title="confidence reversal: low-conf incumbent vs high-conf challenger",
  should="A single high-conf challenger must not revise even a low-conf incumbent (1145's own incumbent "
         "was conf 605). Corroboration is still required. cf1's permanence bar (§4.2) additionally keeps "
         "the sub-700 incumbent provisional.",
  no_hist=False, preinstall=None, correct_final_j=0,
  trials=[
   ("S1",0,0,0,500,1,0,2000,0, 9,0, "synthetic low-conf incumbent (frozen gate granted sub-700 permanents: AUTOPSY §1.2)"),
   ("S2",0,0,0,520,1,2,2100,0, 9,0, "synthetic; |2-0|<=8"),
   ("T2",0,0,1,850,1,90,7000,1, 1,860, "synthetic high-conf challenger, SINGLE observation; truth DIFFERENT (correct)"),
  ],
  expect={
   G0:([D_PROV,D_PERM,D_CONF],0,0,"frozen: no conf bar on permanence; conflict -> CONFLICT_WITHHELD"),
   G1:([D_PROV,D_PROV,D_CHAL],-1,0,"§4.2 bar blocks permanence at conf 520 (stays provisional); singleton challenger -> CHALLENGER_PROV; no single-observation reversal even of provisionals"),
   G2:([D_PROV,D_PERM,D_CHAL],0,0,"H2 gate path grants permanent (no conf bar); D-fired conflict needs corroboration -> CHALLENGER_PROV"),
  }),
 dict(
  name="CC1", title="correlated corroborators: two WRONG challengers agreeing (should NOT revise)",
  should="PREREGISTERED KNOWN-UNSAFE for G1/G2. Two wrong high-conf PASSes agreeing within tolerance "
         "trigger corroborated revision under cf1-class rules -> FALSE INSTALL. This is AUTOPSY §2.3's "
         "caveat made concrete (the six corroborated-wrong RICH trials). The mrgF>=T3 margin bar "
         "(§4 step 3, unverified in Zag) is the candidate fix, NOT part of these gates.",
  no_hist=False, preinstall=None, correct_final_j=3,
  trials=[
   ("S1",4,0,3,760,1,2480,500,3, 9,0, "synthetic BRIGHT incumbent"),
   ("S2",4,0,3,770,1,2490,510,3, 9,0, "synthetic; |2490-2480|=10<=tol 120"),
   ("T2",4,0,2,718,1,2618,382,3, 2,720, "frozen: sweep.jsonl seq 10983 (RICH, truth BRIGHT: wrong)"),
   ("T3",4,0,2,704,1,2642,358,3, 2,710, "frozen: sweep.jsonl seq 10992 (RICH, truth BRIGHT: wrong); |2642-2618|=24<=tol 120"),
  ],
  expect={
   G0:([D_PROV,D_PERM,D_CONF,D_CONF],3,0,"frozen conflict rule; no false install"),
   G1:([D_PROV,D_PERM,D_CHAL,D_REV],2,1,"AUTOPSY §2.3 caveat: correlated wrong pair corroborates -> REVISED_INSTALL installs WRONG judgment. KNOWN UNSAFE."),
   G2:([D_PROV,D_PERM,D_CHAL,D_REV],2,1,"same structural caveat via D-fired corroboration -> REVISED_INSTALL installs WRONG judgment. KNOWN UNSAFE."),
  }),
 dict(
  name="CC2", title="correlated corroborators: two CORRECT challengers agreeing (should revise)",
  should="Two correct high-conf conflicting PASSes agreeing within tolerance revise (independent "
         "corroborator pair from C1: meas 89/89).",
  no_hist=False, preinstall=None, correct_final_j=1,
  trials=[
   ("S1",0,0,0,605,1,0,2300,0, 9,0, "frozen: sweep.jsonl seq 721"),
   ("S2",0,0,0,750,1,3,2400,0, 9,0, "synthetic; |3-0|<=8"),
   ("T2",0,0,1,814,1,89,6600,1, 1,830, "frozen: sweep.jsonl seq 1262 (correct)"),
   ("T3",0,0,1,814,1,89,6603,1, 1,835, "frozen: sweep.jsonl seq 1689 (DIFFERENT, truth DIFFERENT: correct); |89-89|=0<=tol 8"),
  ],
  expect={
   G0:([D_PROV,D_PERM,D_CONF,D_CONF],0,0,"frozen conflict rule (negative control)"),
   G1:([D_PROV,D_PERM,D_CHAL,D_REV],1,0,"§4.1 corroborated revision (correct)"),
   G2:([D_PROV,D_PERM,D_CHAL,D_REV],1,0,"hardened adjudication: D-fired corroboration -> REVISED_INSTALL (correct)"),
  }),
 dict(
  name="H1", title="missing history: conflict with no ledger history (should withhold)",
  should="With no history the corroboration path is inert; all gates fall back to the frozen withhold. "
         "A correct challenger that cannot be corroborated must still wait.",
  no_hist=True, preinstall=(0,0,605,721), correct_final_j=0,
  trials=[
   ("T0",0,0,1,814,1,89,6600,1, 1,830, "frozen: sweep.jsonl seq 1262 values; correct challenger, but NO history available to the gate"),
  ],
  expect={
   G0:([D_CONF],0,0,"conflict rule consults no history"),
   G1:([D_CONF],0,0,"§4.1 requires a corroborating observation; no_hist -> challenger slot inert -> frozen fallback"),
   G2:([D_CONF],0,0,"D fires, but adjudication requires history; no_hist -> CONFLICT_WITHHELD"),
  }),
 dict(
  name="T1", title="tie: challenger and incumbent at equal evidence (should withhold)",
  should="Equal evidence is not corroboration. A single tied challenger is stored (cf1-class) or "
         "withheld (frozen); never installed.",
  no_hist=False, preinstall=None, correct_final_j=0,
  trials=[
   ("S1",0,0,0,800,1,0,5000,0, 9,0, "synthetic incumbent conf 800"),
   ("S2",0,0,0,800,1,3,5000,0, 9,0, "synthetic; |3-0|<=8"),
   ("T2",0,0,1,800,1,90,5000,1, 1,800, "synthetic challenger at EQUAL evidence (conf 800, mrgF 5000); truth DIFFERENT (correct but tied)"),
  ],
  expect={
   G0:([D_PROV,D_PERM,D_CONF],0,0,"frozen conflict rule"),
   G1:([D_PROV,D_PERM,D_CHAL],0,0,"singleton -> CHALLENGER_PROV; tie is not corroboration"),
   G2:([D_PROV,D_PERM,D_CHAL],0,0,"D-fired singleton conflict -> CHALLENGER_PROV"),
  }),
 dict(
  name="W1", title="withhold-everything regression (UNRESOLVED stream; V2-D KILL guard)",
  should="Trials the sense left UNRESOLVED must never install, even when the detector's "
         "conf/judgment conditions are met. This is REDTEAM_V2 §4's KILL against unhardened V2-D "
         "(43 ACCEPT_INSTALL on 288 UNRESOLVED trials, 9 false). The prog-required hardening must hold.",
  no_hist=False, preinstall=None, correct_final_j=-1,
  trials=[
   ("T0",0,2,1,850,0,90,0,1, 1,850, "synthetic UNRESOLVED; D conf/judgment conditions met but prog!=PASS"),
   ("T1",0,2,1,850,0,90,0,0, 1,850, "synthetic UNRESOLVED"),
   ("T2",0,2,1,850,0,90,0,1, 1,850, "synthetic UNRESOLVED"),
  ],
  expect={
   G0:([D_WITH,D_WITH,D_WITH],-1,0,"prog!=PASS -> WITHHELD; zero installs"),
   G1:([D_WITH,D_WITH,D_WITH],-1,0,"prog!=PASS -> WITHHELD; zero installs"),
   G2:([D_WITH,D_WITH,D_WITH],-1,0,"prog-required: D cannot fire on UNRESOLVED -> H2 gate path -> WITHHELD; zero installs"),
  }),
]

GATE_RULES = {
 G0: """G0 — frozen R2-4/H2 gate (NEGATIVE CONTROL; memgate.zag §§1.1/2 verbatim, single-task):
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
  Preregistered behavior: CONFLICT_WITHHELD on every permanent-conflict cell; never revises.""",
 G1: """G1 — cf1 historical-corroboration gate (AUTOPSY_R2-4 §4, pure-Zag implementation from spec;
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
  but vacuous in this matrix (no FAIL trials).""",
 G2: """G2 — V2-D-hardened gate (detector spec REDTEAM_V2 §4 + PREREG_V2-D §2; hardening: prog-required
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
  provisional incumbents; a single D-fired observation never revises an installed claim.""",
}

# ---------------------------------------------------------------- rendering

def md_cell_table(cell):
    lines = ["| # | label | tcode | prog | jcode(judg) | conf | pred | meas | mrgF | truth | jG | confG | provenance |"]
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    judg = {0:"SAME",1:"DIFFERENT",2:"RICH",3:"BRIGHT"}
    prog = {0:"PASS",1:"FAIL",2:"UNRESOLVED"}
    for i,(lab,tc,pr,jc,cf,pd,me,mg,tr,jg,cg,prov) in enumerate(cell["trials"]):
        lines.append("| %d | %s | %d | %s | %d (%s) | %d | %d | %d | %d | %d (%s) | %d | %d | %s |" % (
            i,lab,tc,prog[pr],jc,judg[jc],cf,pd,me,mg,tr,judg[tr],jg,cg,prov))
    return "\n".join(lines)

def md_cell(cell):
    p = []
    p.append("### Cell %s — %s" % (cell["name"], cell["title"]))
    p.append("")
    p.append("**Should:** %s" % cell["should"])
    p.append("")
    if cell["preinstall"] is not None:
        j,m,c,s = cell["preinstall"]
        p.append("**Preinstall (no trial history):** permanent := (jcode=%d, meas=%d, conf=%d, seq=%d); no_hist=1." % (j,m,c,s))
        p.append("")
    p.append(md_cell_table(cell))
    p.append("")
    p.append("**Preregistered expectations:**")
    p.append("")
    p.append("| gate | expected disposition sequence | expected final perm jcode | expected false install | rule cited |")
    p.append("|---|---|---|---|---|")
    for g in (G0,G1,G2):
        seq, fj, fi, rule = cell["expect"][g]
        p.append("| %s | %s | %s | %d | %s |" % (
            GATE_NAME[g], ", ".join(DISP_NAME[d] for d in seq),
            "none" if fj==-1 else str(fj), fi, rule))
    p.append("")
    if any(cell["expect"][g][2]==1 for g in (G0,G1,G2)):
        p.append("> KNOWN-UNSAFE CELL: a false install is preregistered for the named gate(s). "
               "Pass/fail for those gate-cells is still expected-vs-actual (the rule behaving as specified); "
               "the matrix verdict separately records that the gate is not fully safe.")
        p.append("")
    return "\n".join(p)

def render_prereg():
    p = []
    p.append("# PREREG — PAMs v2 contradiction-matrix experiment (follow-up item 6)")
    p.append("")
    p.append("**Status: FROZEN 2026-09-23. Committed alone — before any build output exists.**")
    p.append("**Program:** PAMs v2 follow-up, contradiction matrix (Micah: YES, RUN FOR SURE).")
    p.append("")
    p.append("## 1. Settling-experiment linkage")
    p.append("")
    p.append("Sol debate Round 4 (v2/debates/DEBATES_V2_R2.md), disagreement #4 (FS-G completeness) STANDS:")
    p.append('> "FS-G bars do not, by themselves, specify what happens when evidence conflicts, when a '
             'corroborator is wrong, or when a stronger signal contradicts an incumbent. Trial 1145 is a '
             'concrete demonstration of the gap."')
    p.append("> The settling experiment is a contradiction matrix covering incumbent/new-answer conflicts, "
             "confidence reversals, correlated corroborators, missing history, and ties. "
             "Each cell needs a preregistered outcome.")
    p.append("")
    p.append("Sol's new #1 architecture (revisable admission/install gate with historical corroboration only) "
             "depends on this experiment: the matrix pins down the contradiction behavior BEFORE the gate "
             "is built (debate moderation note: 'The contradiction-matrix experiment ... should run before "
             "this gate is built, or v2 repeats the R2-4 mistake of unspecified contradiction behavior.').")
    p.append("")
    p.append("## 2. Candidate gates under test")
    p.append("")
    for g in (G0,G1,G2):
        p.append("#### %s" % GATE_NAME[g])
        p.append("")
        p.append("```")
        p.append(GATE_RULES[g])
        p.append("```")
        p.append("")
    p.append("Disposition vocabulary (frozen): 0=PERMANENT_INSTALL, 1=PROVISIONAL_INSTALL, 2=CORROBORATED, "
             "3=CONFLICT_WITHHELD, 4=CHALLENGER_PROV, 5=REVISED_INSTALL, 6=ACCEPT_INSTALL, 7=WITHHELD.")
    p.append("")
    p.append("Truth handling: every trial row carries a `truth` field for scoring. Gates NEVER read it "
             "(contractually off-limits, as in memgate.zag: 'truth is PASSED THROUGH ... and is NEVER used "
             "in any gate rule'). The harness enforces this structurally: gate functions take only "
             "(prog, jcode, conf, pred, meas, jG, confG); truth is read only by the scorer.")
    p.append("")
    p.append("## 3. Cells")
    p.append("")
    p.append("Trial rows are RECORD-level (the gate's actual input contract per memgate.zag's header: "
             "`seq|tcode|fixture|prog|jcode|judgment|confidence|pred|measure|phash|truth`). Frozen rows are "
             "cited by seq from `senses/pam-rebuild/round2/forks/R2-4/evidence/clean/sweep.jsonl`; "
             "synthetic rows are used only where the frozen stream lacks the cell geometry, with values "
             "drawn from frozen distribution ranges (AUTOPSY_R2-4 §2.2: correct-colordisc conf "
             "p10/median/p90 = 729/851/907, mrgF median 8620/637). G-span fields (jG, confG) are synthetic "
             "throughout (preregistered per trial): the matrix tests gate contradiction logic, not the sense; "
             "jG=9 is a sentinel meaning 'G span disagrees' (D cannot fire).")
    p.append("")
    for cell in CELLS:
        p.append(md_cell(cell))
    p.append("## 4. Execution protocol (frozen)")
    p.append("")
    p.append("- Pure-Zag battery `src/cm_main.zag` (+ generated `src/cm_records.zag`): runs every cell "
             "through every gate, printing one `CM|cell|gate|trial|disp|perm_j|perm_seq` line per trial.")
    p.append("- Three full runs; sha256 of each run's stdout must be byte-identical (zero RNG; all inputs literal).")
    p.append("- Python scorer (`score_cm.py`, glue only) parses stdout and compares against EXPECT.tsv / "
             "EXPECT_CELL.tsv (both generated from this prereg, committed with it).")
    p.append("- Per gate-cell: PASS iff emitted disposition sequence == preregistered sequence AND "
             "false-install flag == preregistered AND (W1) install count == 0.")
    p.append("- Build: `znc_linux_x86_64_abed8aa1 src/cm_main.zag -o cm_bin` (toolchain path in RUNLOG). "
             "No binaries or .zagd committed.")
    p.append("")
    p.append("## 5. Verdict rules (frozen)")
    p.append("")
    p.append("- **Fully-specified:** every cell's emitted dispositions were produced by a named preregistered "
             "rule; no trial fell through to an unspecified/defensive branch unexpectedly (the defensive "
             "branches are specified above; hitting one where not preregistered = cell FAIL).")
    p.append("- **Safe:** no false installs in any cell (a false install = final permanent jcode differs from "
             "the cell's correct final jcode). CC1's preregistered false installs for G1/G2 are recorded as "
             "known-unsafe behavior, not as surprise failures.")
    p.append("- **Verdict question:** which gates have fully-specified contradiction behavior with no false "
             "installs? A gate that withholds correct revisions (G0) is specified-and-safe but does not "
             "revise; a gate that revises correctly but false-installs on correlated wrong corroborators "
             "(G1/G2 on CC1) is specified but not fully safe.")
    p.append("- Follow-up already preregistered: the mrgF>=T3 challenger margin bar (AUTOPSY §4 step 3) is "
             "the candidate fix for the CC1 caveat; it needs its own Zag verification before adoption.")
    p.append("")
    p.append("## 6. Commit map")
    p.append("")
    p.append("- This prereg (ALONE): `senses/pam-rebuild/v2/contradiction_matrix/PREREG_CONTRADICTION_MATRIX.md`, "
             "`gen_cells.py`, `EXPECT.tsv`, `EXPECT_CELL.tsv`.")
    p.append("- Build + evidence + verdict: `src/cm_main.zag`, `src/cm_records.zag` (generated), "
             "`src/R33_NATIVE_IO_V1.zag`, `evidence/run{1,2,3}.txt`, `evidence/DIGESTS.txt`, "
             "`evidence/score.tsv`, `RUNLOG.md`, `CONTRADICTION_MATRIX.md`.")
    p.append("- Branch `tnn-native-lab`, repo `sylorlabs/TNN`, via `~/workspace/commit_racefree.py`, "
             "TMPDIR=`~/workspace/tmp_commit`, lab-relative paths. No binaries, no `.zagd`. Additive-only.")
    p.append("")
    p.append("**Laws:** pure Zag for mechanisms/learners/verification; Python only for glue/analysis. "
             "Zero RNG in any decision path. Byte-identical reruns required.")
    p.append("")
    return "\n".join(p) + "\n"

def write_expect():
    with open(os.path.join(OUT,"EXPECT.tsv"),"w") as f:
        f.write("cell\tgate\ttrial_idx\texpected_disp\n")
        for cell in CELLS:
            for g in (G0,G1,G2):
                seq = cell["expect"][g][0]
                for i,d in enumerate(seq):
                    f.write("%s\t%d\t%d\t%d\n" % (cell["name"],g,i,d))
    with open(os.path.join(OUT,"EXPECT_CELL.tsv"),"w") as f:
        f.write("cell\tgate\texpected_final_perm_j\texpected_false_install\texpected_installs\n")
        for cell in CELLS:
            for g in (G0,G1,G2):
                seq, fj, fi, _ = cell["expect"][g]
                installs = sum(1 for d in seq if d in (D_PERM,D_PROV,D_CORR,D_CHAL,D_REV,D_ACC))
                f.write("%s\t%d\t%d\t%d\t%d\n" % (cell["name"],g,fj,fi,installs))

def write_zag_records():
    # flatten trials; record per-cell start/count/preinstall/no_hist
    idx = 0
    cellinfo = []
    rec_lines = []
    for cell in CELLS:
        start = idx
        for (lab,tc,pr,jc,cf,pd,me,mg,tr,jg,cg,prov) in cell["trials"]:
            rec_lines.append((idx,lab,tc,pr,jc,cf,pd,me,mg,tr,jg,cg))
            idx += 1
        pre = cell["preinstall"]
        cellinfo.append((cell["name"],start,len(cell["trials"]),
                         0 if pre is None else 1,
                         -1 if pre is None else pre[0],
                         -1 if pre is None else pre[1],
                         -1 if pre is None else pre[2],
                         -1 if pre is None else pre[3],
                         1 if cell["no_hist"] else 0))
    n = idx
    L = []
    L.append("// GENERATED by gen_cells.py from the frozen prereg — do not hand-edit.")
    L.append("// Trial fields per row (10 x i64): tcode, prog, jcode, conf, pred, meas, mrgF, truth, jG, confG")
    L.append("const CM_NTRIALS:i32=%d;" % n)
    L.append("const CM_NCELLS:i32=%d;" % len(CELLS))
    L.append("const CM_NF:i32=10;")
    L.append("const CM_ROW:i32=80;")
    L.append("fn cm_init_trials(tr:[]u8) void {")
    for (i,lab,tc,pr,jc,cf,pd,me,mg,trv,jg,cg) in rec_lines:
        vals = [tc,pr,jc,cf,pd,me,mg,trv,jg,cg]
        L.append("    // trial %d (%s)" % (i,lab))
        for fi,v in enumerate(vals):
            L.append("    t_put64(tr,%d,%d);" % (i*80+fi*8, v))
    L.append("}")
    L.append("// cell info per cell (8 x i64): start,count,pre_on,pre_j,pre_meas,pre_conf,pre_seq,no_hist")
    L.append("fn cm_cell(ci:i32,o:[]u8) void {")
    for ci,(name,start,count,pre_on,pre_j,pre_m,pre_c,pre_s,no_hist) in enumerate(cellinfo):  # 9-tuple
        vals = [start,count,pre_on,pre_j,pre_m,pre_c,pre_s,no_hist]
        L.append("    // cell %d %s" % (ci,name))
        L.append("    if(ci==%d){" % ci)
        for fi,v in enumerate(vals):
            L.append("        t_put64(o,%d,%d);" % (fi*8, v))
        L.append("    }")
    L.append("}")
    L.append("fn cm_cell_name(ci:i32) []u8 {")
    for ci,(name,_,_,_,_,_,_,_,_) in enumerate(cellinfo):
        L.append('    if(ci==%d){return "%s";}' % (ci,name))
    L.append('    return "?";')
    L.append("}")
    with open(os.path.join(OUT,"src","cm_records.zag"),"w") as f:
        f.write("\n".join(L)+"\n")
    return n

def main():
    with open(os.path.join(OUT,"PREREG_CONTRADICTION_MATRIX.md"),"w") as f:
        f.write(render_prereg())
    write_expect()
    n = write_zag_records()
    print("wrote prereg + EXPECT.tsv + EXPECT_CELL.tsv + cm_records.zag (%d trials)" % n)

if __name__ == "__main__":
    main()
