#!/usr/bin/env python3
"""gen_guard.py — single source of truth for the CC1 margin-guard experiment.

Generates from the frozen prereg (PREREG_CC1_GUARD.md):
  - src/guard_records.zag  (trial rows + cell table; 13 x i64 per row)
  - EXPECT_GUARD.tsv        (expected disposition per trial per config)
  - EXPECT_GUARD_CELL.tsv   (expected final perm jcode / false-install / installs)

Glue only (like the frozen gen_cells.py): all trial values are literals below,
hand-derived expectations are literals below. Zero RNG. Deterministic.

Trial fields (13 x i64):
  0 tcode | 1 prog (0=PASS, 2=UNRESOLVED) | 2 jcode | 3 conf | 4 pred |
  5 meas | 6 mrgF | 7 truth | 8 jG | 9 confG | 10 seq | 11 span_a | 12 span_b

Disposition codes (frozen, same as the matrix):
  0=PERM 1=PROV 2=CORR 3=CONF 4=CHAL 5=REV 6=ACC 7=WITH

Configs: 0=G1 (cf1 baseline) | 1=G2 (V2-D baseline) |
         2=MG1 (margin floor) | 3=MG2 (margin asymmetry) |
         4=MG3 (disjoint spans) | 5=MG4 (temporal separation) |
         6=MG6 (three-fold independence: MG1 & MG3 & MG4)

Frozen guard constants:
  MG1_FLOOR = 400            (both challengers' mrgF must clear it)
  MG2_FACTOR = 2             (min challenger mrgF >= 2 * incumbent perm mrgF)
  MG4_SEQ_GAP = 20           (|seq1 - seq2| >= 20)
  MG3 disjointness: spans (sa1,sb1),(sa2,sb2) disjoint iff
      NOT (sa1 < sb2 AND sa2 < sb1)   (touching counts as disjoint)
Vetoed revision -> disposition CHAL (challenger slot retained, no install).
"""

# ---------------- trial rows (literals; see prereg section 3 for provenance) ----------------
# cell: (name, trials, correct_final_j, preinstall|None, no_hist, scored)
# preinstall = (j, meas, conf, seq) ; scored=False only for the V9 ceiling probe.
CELLS = [
 ("C1", [
   (0,0,0,605,1,0,2300,0,9,0,721,0,2000),
   (0,0,0,750,1,3,2400,0,9,0,722,100,2100),
   (0,0,1,814,1,89,6600,1,1,830,1262,0,2000),
   (0,0,1,827,1,95,7212,1,1,840,1330,2100,4100),
  ], 1, None, 0, True),
 ("C2", [
   (4,0,3,760,1,2480,500,3,9,0,10967,0,2000),
   (4,0,3,770,1,2490,510,3,9,0,10968,100,2100),
   (4,0,2,718,1,2618,382,3,2,720,10983,0,2000),
  ], 3, None, 0, True),
 ("C3", [
   (0,0,0,605,1,0,2300,0,9,0,721,0,2000),
   (0,0,0,750,1,3,2400,0,9,0,722,100,2100),
   (0,0,1,874,1,127,10410,0,1,850,1145,0,2000),
  ], 0, None, 0, True),
 ("R1", [
   (0,0,0,900,1,0,8000,0,9,0,2001,0,2000),
   (0,0,0,920,1,3,8100,0,9,0,2002,100,2100),
   (0,0,1,650,1,90,5000,1,1,660,2003,0,2000),
  ], 0, None, 0, True),
 ("R2", [
   (0,0,0,500,1,0,2000,0,9,0,2011,0,2000),
   (0,0,0,520,1,2,2100,0,9,0,2012,100,2100),
   (0,0,1,850,1,90,7000,1,1,860,2013,0,2000),
  ], "G1N_G2Z", None, 0, True),  # G1/guards: no perm (-1); G2: perm j=0
 ("H1", [
   (0,0,1,814,1,89,6600,1,1,830,1262,0,2000),
  ], 0, (0,0,605,721), 1, True),
 ("T1", [
   (0,0,0,800,1,0,5000,0,9,0,2021,0,2000),
   (0,0,0,800,1,3,5000,0,9,0,2022,100,2100),
   (0,0,1,800,1,90,5000,1,1,800,2023,0,2000),
  ], 0, None, 0, True),
 ("W1", [
   (0,2,1,850,0,90,0,1,1,850,2031,0,2000),
   (0,2,1,850,0,90,0,0,1,850,2032,0,2000),
   (0,2,1,850,0,90,0,1,1,850,2033,0,2000),
  ], -1, None, 0, True),
 # ---- CC1 family (wrong correlated pair; correct_final_j = 3 = BRIGHT) ----
 ("CC1", [
   (4,0,3,760,1,2480,500,3,9,0,10967,0,2000),
   (4,0,3,770,1,2490,510,3,9,0,10968,100,2100),
   (4,0,2,718,1,2618,382,3,2,720,10983,0,2000),
   (4,0,2,704,1,2642,358,3,2,710,10992,100,2100),
  ], 3, None, 0, True),
 ("CC1-V1", [  # |dmeas| = 119 (near-miss, inside tol 120)
   (4,0,3,760,1,2480,500,3,9,0,10967,0,2000),
   (4,0,3,770,1,2490,510,3,9,0,10968,100,2100),
   (4,0,2,718,1,2618,382,3,2,720,10983,0,2000),
   (4,0,2,704,1,2737,358,3,2,710,10992,100,2100),
  ], 3, None, 0, True),
 ("CC1-V2", [  # |dmeas| = 120 (tolerance boundary, inclusive)
   (4,0,3,760,1,2480,500,3,9,0,10967,0,2000),
   (4,0,3,770,1,2490,510,3,9,0,10968,100,2100),
   (4,0,2,718,1,2618,382,3,2,720,10983,0,2000),
   (4,0,2,704,1,2738,358,3,2,710,10992,100,2100),
  ], 3, None, 0, True),
 ("CC1-V3", [  # |dmeas| = 121 (just outside tol: no corroboration at all)
   (4,0,3,760,1,2480,500,3,9,0,10967,0,2000),
   (4,0,3,770,1,2490,510,3,9,0,10968,100,2100),
   (4,0,2,718,1,2618,382,3,2,720,10983,0,2000),
   (4,0,2,704,1,2739,358,3,2,710,10992,100,2100),
  ], 3, None, 0, True),
 ("CC1-V4", [  # high-confidence wrong pair (conf 850/840)
   (4,0,3,760,1,2480,500,3,9,0,10967,0,2000),
   (4,0,3,770,1,2490,510,3,9,0,10968,100,2100),
   (4,0,2,850,1,2618,382,3,2,720,10983,0,2000),
   (4,0,2,840,1,2642,358,3,2,710,10992,100,2100),
  ], 3, None, 0, True),
 ("CC1-V5", [  # HIGH-MARGIN wrong pair (mrgF 6600/6603: margin-guard stress)
   (4,0,3,760,1,2480,500,3,9,0,10967,0,2000),
   (4,0,3,770,1,2490,510,3,9,0,10968,100,2100),
   (4,0,2,718,1,2618,6600,3,2,720,10983,0,2000),
   (4,0,2,704,1,2642,6603,3,2,710,10992,100,2100),
  ], 3, None, 0, True),
 ("CC1-V6", [  # asymmetric margins (6600/358)
   (4,0,3,760,1,2480,500,3,9,0,10967,0,2000),
   (4,0,3,770,1,2490,510,3,9,0,10968,100,2100),
   (4,0,2,718,1,2618,6600,3,2,720,10983,0,2000),
   (4,0,2,704,1,2642,358,3,2,710,10992,100,2100),
  ], 3, None, 0, True),
 ("CC1-V7", [  # DISJOINT-SPAN wrong pair (span-guard stress)
   (4,0,3,760,1,2480,500,3,9,0,10967,0,2000),
   (4,0,3,770,1,2490,510,3,9,0,10968,100,2100),
   (4,0,2,718,1,2618,382,3,2,720,10983,0,2000),
   (4,0,2,704,1,2642,358,3,2,710,10992,2100,4100),
  ], 3, None, 0, True),
 ("CC1-V8", [  # TEMPORALLY-SEPARATED wrong pair, dseq=427 (time-guard stress)
   (4,0,3,760,1,2480,500,3,9,0,10967,0,2000),
   (4,0,3,770,1,2490,510,3,9,0,10968,100,2100),
   (4,0,2,718,1,2618,382,3,2,720,10983,0,2000),
   (4,0,2,704,1,2642,358,3,2,710,11410,100,2100),
  ], 3, None, 0, True),
 ("CC1-V9", [  # PERFECT STORM: high margins + disjoint spans + dseq=427, wrong.
              # Observationally identical to a correct pair on every
              # guard-visible axis. UNSCORED ceiling probe (scored=False).
   (4,0,3,760,1,2480,500,3,9,0,10967,0,2000),
   (4,0,3,770,1,2490,510,3,9,0,10968,100,2100),
   (4,0,2,718,1,2618,6600,3,2,720,10983,0,2000),
   (4,0,2,704,1,2642,6603,3,2,710,11410,2100,4100),
  ], 3, None, 0, False),
 # ---- correct-revision family (throughput; all must REVISED_INSTALL) ----
 ("CC2", [
   (0,0,0,605,1,0,2300,0,9,0,721,0,2000),
   (0,0,0,750,1,3,2400,0,9,0,722,100,2100),
   (0,0,1,814,1,89,6600,1,1,830,1262,0,2000),
   (0,0,1,814,1,89,6603,1,1,835,1689,2100,4100),
  ], 1, None, 0, True),
 ("CC2-W1", [  # near-floor correct pair (mrgF 500/520, just above floor 400)
   (0,0,0,605,1,0,2300,0,9,0,721,0,2000),
   (0,0,0,750,1,3,2400,0,9,0,722,100,2100),
   (0,0,1,814,1,89,500,1,1,830,3001,0,2000),
   (0,0,1,820,1,89,520,1,1,835,3101,2100,4100),
  ], 1, None, 0, True),
 ("CC2-W2", [  # modest-margin correct pair (3000/3100 < 2x incumbent 2400)
   (0,0,0,605,1,0,2300,0,9,0,721,0,2000),
   (0,0,0,750,1,3,2400,0,9,0,722,100,2100),
   (0,0,1,814,1,89,3000,1,1,830,3002,0,2000),
   (0,0,1,820,1,89,3100,1,1,835,3102,2100,4100),
  ], 1, None, 0, True),
 ("C1-W3", [  # strong incumbent (mrgF 8000/8100), correct challengers 6600/7212
   (0,0,0,900,1,0,8000,0,9,0,4001,0,2000),
   (0,0,0,920,1,3,8100,0,9,0,4002,100,2100),
   (0,0,1,814,1,89,6600,1,1,830,4003,0,2000),
   (0,0,1,827,1,95,7212,1,1,840,4071,2100,4100),
  ], 1, None, 0, True),
]

CONFIGS = ["G1","G2","MG1","MG2","MG3","MG4","MG6"]

# Hand-derived expected disposition sequences per (cell, config).
# Derived from the prereg rules; the scorer checks the binary against these.
# V9 is the unscored ceiling probe: expectations recorded for reporting only.
EXPECT = {
 # cell: {config: [dispositions]}
 "C1":     {"G1":[1,0,4,5],"G2":[1,0,4,5],"MG1":[1,0,4,5],"MG2":[1,0,4,5],
            "MG3":[1,0,4,5],"MG4":[1,0,4,5],"MG6":[1,0,4,5]},
 "C2":     {"G1":[1,0,4],"G2":[1,0,4],"MG1":[1,0,4],"MG2":[1,0,4],
            "MG3":[1,0,4],"MG4":[1,0,4],"MG6":[1,0,4]},
 "C3":     {"G1":[1,0,4],"G2":[1,0,4],"MG1":[1,0,4],"MG2":[1,0,4],
            "MG3":[1,0,4],"MG4":[1,0,4],"MG6":[1,0,4]},
 "R1":     {"G1":[1,0,3],"G2":[1,0,3],"MG1":[1,0,3],"MG2":[1,0,3],
            "MG3":[1,0,3],"MG4":[1,0,3],"MG6":[1,0,3]},
 "R2":     {"G1":[1,1,4],"G2":[1,0,4],"MG1":[1,1,4],"MG2":[1,1,4],
            "MG3":[1,1,4],"MG4":[1,1,4],"MG6":[1,1,4]},
 "H1":     {"G1":[3],"G2":[3],"MG1":[3],"MG2":[3],
            "MG3":[3],"MG4":[3],"MG6":[3]},
 "T1":     {"G1":[1,0,4],"G2":[1,0,4],"MG1":[1,0,4],"MG2":[1,0,4],
            "MG3":[1,0,4],"MG4":[1,0,4],"MG6":[1,0,4]},
 "W1":     {"G1":[7,7,7],"G2":[7,7,7],"MG1":[7,7,7],"MG2":[7,7,7],
            "MG3":[7,7,7],"MG4":[7,7,7],"MG6":[7,7,7]},
 "CC1":    {"G1":[1,0,4,5],"G2":[1,0,4,5],
            "MG1":[1,0,4,4],"MG2":[1,0,4,4],"MG3":[1,0,4,4],
            "MG4":[1,0,4,4],"MG6":[1,0,4,4]},
 "CC1-V1": {"G1":[1,0,4,5],"G2":[1,0,4,5],
            "MG1":[1,0,4,4],"MG2":[1,0,4,4],"MG3":[1,0,4,4],
            "MG4":[1,0,4,4],"MG6":[1,0,4,4]},
 "CC1-V2": {"G1":[1,0,4,5],"G2":[1,0,4,5],
            "MG1":[1,0,4,4],"MG2":[1,0,4,4],"MG3":[1,0,4,4],
            "MG4":[1,0,4,4],"MG6":[1,0,4,4]},
 "CC1-V3": {"G1":[1,0,4,4],"G2":[1,0,4,4],
            "MG1":[1,0,4,4],"MG2":[1,0,4,4],"MG3":[1,0,4,4],
            "MG4":[1,0,4,4],"MG6":[1,0,4,4]},
 "CC1-V4": {"G1":[1,0,4,5],"G2":[1,0,4,5],
            "MG1":[1,0,4,4],"MG2":[1,0,4,4],"MG3":[1,0,4,4],
            "MG4":[1,0,4,4],"MG6":[1,0,4,4]},
 "CC1-V5": {"G1":[1,0,4,5],"G2":[1,0,4,5],
            "MG1":[1,0,4,5],"MG2":[1,0,4,5],          # margin guards ALLOW: high margins
            "MG3":[1,0,4,4],"MG4":[1,0,4,4],"MG6":[1,0,4,4]},
 "CC1-V6": {"G1":[1,0,4,5],"G2":[1,0,4,5],
            "MG1":[1,0,4,4],"MG2":[1,0,4,4],"MG3":[1,0,4,4],
            "MG4":[1,0,4,4],"MG6":[1,0,4,4]},
 "CC1-V7": {"G1":[1,0,4,5],"G2":[1,0,4,5],
            "MG1":[1,0,4,4],"MG2":[1,0,4,4],
            "MG3":[1,0,4,5],                          # span guard ALLOWS: disjoint spans
            "MG4":[1,0,4,4],"MG6":[1,0,4,4]},
 "CC1-V8": {"G1":[1,0,4,5],"G2":[1,0,4,5],
            "MG1":[1,0,4,4],"MG2":[1,0,4,4],"MG3":[1,0,4,4],
            "MG4":[1,0,4,5],                          # time guard ALLOWS: dseq=427
            "MG6":[1,0,4,4]},
 "CC1-V9": {"G1":[1,0,4,5],"G2":[1,0,4,5],             # ceiling probe: all allow
            "MG1":[1,0,4,5],"MG2":[1,0,4,5],"MG3":[1,0,4,5],
            "MG4":[1,0,4,5],"MG6":[1,0,4,5]},
 "CC2":    {"G1":[1,0,4,5],"G2":[1,0,4,5],"MG1":[1,0,4,5],"MG2":[1,0,4,5],
            "MG3":[1,0,4,5],"MG4":[1,0,4,5],"MG6":[1,0,4,5]},
 "CC2-W1": {"G1":[1,0,4,5],"G2":[1,0,4,5],
            "MG1":[1,0,4,5],
            "MG2":[1,0,4,4],                          # asymmetry vetoes: 500 < 2*2400
            "MG3":[1,0,4,5],"MG4":[1,0,4,5],"MG6":[1,0,4,5]},
 "CC2-W2": {"G1":[1,0,4,5],"G2":[1,0,4,5],
            "MG1":[1,0,4,5],
            "MG2":[1,0,4,4],                          # asymmetry vetoes: 3000 < 2*2400
            "MG3":[1,0,4,5],"MG4":[1,0,4,5],"MG6":[1,0,4,5]},
 "C1-W3":  {"G1":[1,0,4,5],"G2":[1,0,4,5],
            "MG1":[1,0,4,5],
            "MG2":[1,0,4,4],                          # asymmetry vetoes: 6600 < 2*8100
            "MG3":[1,0,4,5],"MG4":[1,0,4,5],"MG6":[1,0,4,5]},
}

# expected (final_perm_jcode, false_install, install_count) per (cell, config)
def _cell_exp(name, trials, cfj, pre):
    out = {}
    for cfg in CONFIGS:
        seq = EXPECT[name][cfg]
        if name == "R2":
            fj = -1 if cfg in ("G1","MG1","MG2","MG3","MG4","MG6") else 0
        elif name == "W1":
            fj = -1
        else:
            fj = seq_final_perm(seq, trials)
            if fj == -1 and pre is not None:
                fj = pre[0]  # preinstalled permanent survives (H1)
        fi = 1 if (5 in seq or 6 in seq) and fj != cfj and name != "R2" else 0
        if name == "R2":
            fi = 0
        ni = sum(1 for d in seq if d in (0,1,2,4,5,6))
        out[cfg] = (fj, fi, ni)
    return out

def seq_final_perm(seq, trials):
    # final permanent jcode = jcode of the last trial that installed a permanent
    # (PERM=0 or REV=5). Mirrors the battery's perm_j reporting.
    last = -1
    for t, d in enumerate(seq):
        if d in (0, 5):
            last = trials[t][2]
    return last

CELL_EXP = {name: _cell_exp(name, trials, cfj, pre)
            for (name, trials, cfj, pre, _nh, _sc) in CELLS}

# ---------------- kill-bar cell sets (prereg section 4) ----------------
CC1_FAMILY = ["CC1","CC1-V1","CC1-V2","CC1-V3","CC1-V4",
              "CC1-V5","CC1-V6","CC1-V7","CC1-V8"]          # V9 excluded: ceiling probe
THROUGHPUT_CELLS = ["C1","CC2","CC2-W1","CC2-W2","C1-W3"]
REGRESSION_CELLS = ["C2","R1","R2","H1","T1","W1"]
GUARD_CONFIGS = ["MG1","MG2","MG3","MG4","MG6"]

# ---------------- emitters ----------------
NF = 13
ROW = NF * 8

def emit_records(path):
    L = []
    L.append("// GENERATED by gen_guard.py from the frozen prereg — do not hand-edit.")
    L.append("// Trial fields per row (13 x i64): tcode, prog, jcode, conf, pred,")
    L.append("// meas, mrgF, truth, jG, confG, seq, span_a, span_b")
    ntr = sum(len(t) for (_, t, _, _, _, _) in CELLS)
    L.append("const GUARD_NTRIALS:i32=%d;" % ntr)
    L.append("const GUARD_NCELLS:i32=%d;" % len(CELLS))
    L.append("const GUARD_NF:i32=%d;" % NF)
    L.append("const GUARD_ROW:i32=%d;" % ROW)
    L.append("fn guard_init_trials(tr:[]u8) void {")
    ti = 0
    for (name, trials, _cfj, _pre, _nh, _sc) in CELLS:
        for row in trials:
            L.append("    // trial %d (%s)" % (ti, name))
            base = ti * ROW
            for f, v in enumerate(row):
                L.append("    t_put64(tr,%d,%d);" % (base + f * 8, v))
            ti += 1
    L.append("}")
    L.append("// cell info per cell (8 x i64): start,count,pre_on,pre_j,pre_meas,pre_conf,pre_seq,no_hist")
    L.append("fn guard_cell(ci:i32,o:[]u8) void {")
    start = 0
    for ci, (name, trials, _cfj, pre, nh, _sc) in enumerate(CELLS):
        L.append("    // cell %d %s" % (ci, name))
        L.append("    if(ci==%d){" % ci)
        L.append("        t_put64(o,0,%d);" % start)
        L.append("        t_put64(o,8,%d);" % len(trials))
        if pre is None:
            L.append("        t_put64(o,16,0);")
            for k in (24, 32, 40, 48):
                L.append("        t_put64(o,%d,-1);" % k)
        else:
            L.append("        t_put64(o,16,1);")
            L.append("        t_put64(o,24,%d);" % pre[0])
            L.append("        t_put64(o,32,%d);" % pre[1])
            L.append("        t_put64(o,40,%d);" % pre[2])
            L.append("        t_put64(o,48,%d);" % pre[3])
        L.append("        t_put64(o,56,%d);" % nh)
        L.append("    }")
        start += len(trials)
    L.append("}")
    L.append("fn guard_cell_name(ci:i32) []u8 {")
    for ci, (name, _t, _c, _p, _n, _s) in enumerate(CELLS):
        L.append('    if(ci==%d){return "%s";}' % (ci, name))
    L.append('    return "?";')
    L.append("}")
    open(path, "w").write("\n".join(L) + "\n")

def emit_expect_tsv(path):
    L = ["cell\tconfig\ttrial\tdisp"]
    for name in [c[0] for c in CELLS]:
        for cfg in CONFIGS:
            for t, d in enumerate(EXPECT[name][cfg]):
                L.append("%s\t%s\t%d\t%d" % (name, cfg, t, d))
    open(path, "w").write("\n".join(L) + "\n")

def emit_expect_cell_tsv(path):
    L = ["cell\tconfig\texpected_final_perm_j\texpected_false_install\texpected_installs"]
    for name in [c[0] for c in CELLS]:
        for cfg in CONFIGS:
            fj, fi, ni = CELL_EXP[name][cfg]
            L.append("%s\t%s\t%d\t%d\t%d" % (name, cfg, fj, fi, ni))
    open(path, "w").write("\n".join(L) + "\n")

if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    emit_records(out + "/guard_records.zag")
    emit_expect_tsv(out + "/EXPECT_GUARD.tsv")
    emit_expect_cell_tsv(out + "/EXPECT_GUARD_CELL.tsv")
    ntr = sum(len(t) for (_, t, _, _, _, _) in CELLS)
    print("trials=%d cells=%d" % (ntr, len(CELLS)))
