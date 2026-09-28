#!/usr/bin/env python3
"""GROK English-box leg transform (deterministic, no RNG).

Mechanical port of the muse_team/tnn legs to the English domain:
1. t5_core.zag: Zharovia domain block -> English domain block generated from
   the frozen facts.json (t5_cat boundaries 48/96/144; t5_truth = TRUE value;
   t5_plant_claim = SUPPLIED value; t5_is_false_plant unchanged).
2. grok_teach.zag: 4-category curriculum geometry (48/48/48/96).
3. grok_trial.zag: 4-category geometry; English q2_false_val; English D2
   two-hop (alpha-pos id l -> word-len id 48+(p-1)); corpus accessor renames.
4. Drivers: grok_* renames; teacher id 44 (TB_TID_GROKTAUGHT), direct probe
   id 54 (TB_TID_DIRECT); disconnect counts 6 -> 4.
5. q1_types.zag / q1_proposal.zag: tid constants + TbSess last-field renames.

Every replacement asserts exactly-once (or expected-count) match.
Idempotent: safe to re-run (asserts hold on already-transformed files only
for the domain block; run once on a fresh copy).
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))   # grok/legs/build
LEGS = os.path.dirname(HERE)                         # grok/legs
INPUT = "/home/hatch/workspace/tnn-lab/wave12/championship-english/corpus-input"

facts_raw = json.load(open(os.path.join(INPUT, "facts.json")))
FALSE_IDS = sorted(facts_raw["false_ids"])
assert FALSE_IDS == [3, 29, 55, 71, 80, 103, 117, 139, 163, 178, 205, 231]
FACTS = {int(k): v for k, v in facts_raw.items() if k not in ("false_ids", "meta")}
assert set(FACTS) == set(range(240))

# TRUE values: supplied for the 228 true ids; corrected for the 12 false ids
# (ground_truth_notes.md, frozen 2026-09-21).
FALSE_FIX = {3: 4, 29: 4, 55: 8, 71: 20, 80: 9, 103: 1678, 117: 1850,
             139: 1895, 163: 3, 178: 9, 205: 37, 231: 8}
# mechanical sanity for the alpha-pos / word-len false ids
for i in (3, 29):
    assert FALSE_FIX[i] == ord(FACTS[i]["claim_text"]) - ord("A") + 1, i
for i in (55, 71, 80):
    assert FALSE_FIX[i] == len(FACTS[i]["claim_text"]), i

def t5_truth(i):
    return FALSE_FIX.get(i, FACTS[i]["value"])

def t5_plant_claim(i):
    return FACTS[i]["value"]

def chain(fn, vals):
    L = [f"fn {fn}(id:i32)i32 {{"]
    for i, v in enumerate(vals):
        L.append(f"    if(id=={i}){{return {v};}}")
    L.append("    return 0;")
    L.append("}")
    return "\n".join(L)

DOMAIN_BLOCK = """// ---- English domain: facts.json (frozen 2026-09-21) ----
// t5_cat: 0=alpha-pos (0..47), 1=word-len (48..95), 2=pub-year (96..143),
//         3=count-fact (144..239).
// t5_truth: the real-world TRUE value (ground_truth_notes.md). For the 228
// non-false ids this equals the supplied value; for the 12 false ids it is
// the corrected value (alpha-pos/word-len false ids also match the
// mechanical ord/len formulas, asserted in the generator).
// t5_plant_claim: the trainer-SUPPLIED value (facts.json), authoritative for
// the learner. t5_is_false_plant: the 12 prereg-fixed false ids (same ids as
// Q2 for comparability).
fn t5_cat(id:i32)i32 {
    if(id<48){return 0;}
    if(id<96){return 1;}
    if(id<144){return 2;}
    return 3;
}
""" + chain("t5_truth", [t5_truth(i) for i in range(240)]) + "\n" + \
    chain("t5_plant_claim", [t5_plant_claim(i) for i in range(240)]) + "\n" + """fn t5_is_false_plant(id:i32)i32 {
    if(id==3){return 1;}
    if(id==29){return 1;}
    if(id==55){return 1;}
    if(id==71){return 1;}
    if(id==80){return 1;}
    if(id==103){return 1;}
    if(id==117){return 1;}
    if(id==139){return 1;}
    if(id==163){return 1;}
    if(id==178){return 1;}
    if(id==205){return 1;}
    if(id==231){return 1;}
    return 0;
}"""

def sub_once(path, old, new, marker=None):
    with open(path) as f:
        t = f.read()
    n = t.count(old)
    if n == 0:
        chk = marker if marker is not None else new
        assert chk in t, f"{path}: neither old nor marker present: {old[:70]!r}"
        return  # already transformed
    assert n == 1, f"{path}: expected 1 occurrence, found {n}: {old[:70]!r}"
    with open(path, "w") as f:
        f.write(t.replace(old, new, 1))

def sub_all(path, old, new, expect=None, marker=None):
    with open(path) as f:
        t = f.read()
    n = t.count(old)
    if n == 0:
        chk = marker if marker is not None else new
        assert chk in t, f"{path}: neither old nor marker present: {old[:70]!r}"
        return  # already transformed
    if expect is not None:
        assert n == expect, f"{path}: expected {expect}, found {n}: {old[:70]!r}"
    with open(path, "w") as f:
        f.write(t.replace(old, new))

def sub_re_ml(path, pat, new, already=None):
    with open(path) as f:
        t = f.read()
    t2, n = re.subn(pat, new, t, count=1, flags=re.DOTALL | re.MULTILINE)
    if n == 0:
        assert already and already in t, f"{path}: regex matched 0x and no marker: {pat[:70]!r}"
        return  # already transformed
    assert n == 1, f"{path}: regex matched {n}x: {pat[:70]!r}"
    with open(path, "w") as f:
        f.write(t2)

# ---------- 1. t5_core.zag domain block (legA/B/C) ----------
for leg in ("legA", "legB", "legC"):
    p = os.path.join(LEGS, leg, "src", "t5_core.zag")
    t = open(p).read()
    if "// ---- English domain" in t:
        print(f"domain block already present: {leg}/src/t5_core.zag", flush=True)
        continue
    sub_re_ml(p,
              r"// ---- Zharovia domain.*?(?=// ---- store init ----)",
              lambda m: DOMAIN_BLOCK + "\n",
              already="// ---- English domain")
    # drop now-unused Zharovia helpers t5_idx/t5_mod/t5_base (were between
    # t5_cat and t5_truth); the regex above consumed through t5_plant_claim's
    # closing brace, which is after them. Verify none remain.
    t = open(p).read()
    assert "t5_mod(" not in t and "t5_base(" not in t and "t5_idx(" not in t, leg
    assert "Zharovia" not in t, leg
    print(f"domain block replaced: {leg}/src/t5_core.zag", flush=True)

# ---------- 2. grok_teach.zag: English 4-category geometry ----------
teach = os.path.join(LEGS, "shared", "grok_teach.zag")
sub_once(teach,
    "fn muse_t_cat_n(c:i32)i32 {\n    if(c==0){return 48;} if(c==1){return 24;} if(c==2){return 36;}\n    if(c==3){return 48;} if(c==4){return 36;} return 48;\n}",
    "fn muse_t_cat_n(c:i32)i32 {\n    if(c==0){return 48;} if(c==1){return 48;} if(c==2){return 48;}\n    return 96;\n}",
    marker="if(c==0){return 48;} if(c==1){return 48;} if(c==2){return 48;}")
sub_once(teach,
    "fn muse_t_cat_base(c:i32)i32 {\n    if(c==0){return 0;} if(c==1){return 48;} if(c==2){return 72;}\n    if(c==3){return 108;} if(c==4){return 156;} return 192;\n}",
    "fn muse_t_cat_base(c:i32)i32 {\n    if(c==0){return 0;} if(c==1){return 48;} if(c==2){return 96;}\n    return 144;\n}",
    marker="if(c==0){return 0;} if(c==1){return 48;} if(c==2){return 96;}")
sub_once(teach, "while(cat<6){", "while(cat<4){", marker="while(cat<4){")
sub_all(teach, "muse_t_", "grok_t_")
sub_all(teach, "muse_obs_at", "grok_obs_at")
sub_all(teach, "muse_prb_at", "grok_prb_at")
sub_all(teach, "muse_dis_at", "grok_dis_at")
sub_all(teach, '@import("muse_corpus.zag")', '@import("corpus.zag")')
sub_once(teach, "muse_teach.zag — D2 teaching-route library (MUSE-NATIVE).",
         "grok_teach.zag — D2 teaching-route library (GROK English box).")
sub_once(teach, "inlined so legs B/C don't carry the trap\n// battery. t5_is_false_plant is the prereg-fixed 12-set.",
         "inlined so legs B/C don't carry the trap\n// battery. t5_is_false_plant is the prereg-fixed 12-set.")
sub_once(teach, "// ---- phase 1: developmental curriculum (D2 route, Track 5 arm-B geometry)",
         "// ---- phase 1: developmental curriculum (D2 route, English 4-category geometry)")
t = open(teach).read()
assert "muse_" not in t.replace("MUSE-NATIVE", ""), "leftover muse_ in teach"
print("transformed shared/grok_teach.zag", flush=True)

# ---------- 3. grok_trial.zag (legA driver) ----------
tr = os.path.join(LEGS, "legA", "src", "grok_trial.zag")
sub_once(tr, "muse_trial.zag — MUSE-NATIVE leg-A driver",
         "grok_trial.zag — GROK English-box leg-A driver")
sub_once(tr, "Corpus: muse_corpus.zag (generated from the frozen muse-native corpus.json).",
         "Corpus: corpus.zag (generated from the frozen grok-4.6 English corpus.json).")
sub_all(tr, "muse_dump_at", "grok_dump_at")
sub_all(tr, "muse_obs_at", "grok_obs_at")
sub_all(tr, "muse_dis_at", "grok_dis_at")
sub_all(tr, "muse_prb_at", "grok_prb_at")
sub_all(tr, "MUSE_CORPUS_SHA256", "GROK_CORPUS_SHA256")
sub_all(tr, '@import("muse_corpus.zag")', '@import("corpus.zag")')
sub_once(tr,
    "fn q2_cat_base(c:i32)i32 {\n    if(c==0){return 0;} if(c==1){return 48;} if(c==2){return 72;}\n    if(c==3){return 108;} if(c==4){return 156;} return 192;\n}",
    "fn q2_cat_base(c:i32)i32 {\n    if(c==0){return 0;} if(c==1){return 48;} if(c==2){return 96;}\n    return 144;\n}",
    marker="fn q2_cat_base(c:i32)i32 {\n    if(c==0){return 0;} if(c==1){return 48;} if(c==2){return 96;}")
sub_once(tr,
    "fn q2_cat_n(c:i32)i32 {\n    if(c==0){return 48;} if(c==1){return 24;} if(c==2){return 36;}\n    if(c==3){return 48;} if(c==4){return 36;} return 48;\n}",
    "fn q2_cat_n(c:i32)i32 {\n    if(c==0){return 48;} if(c==1){return 48;} if(c==2){return 48;}\n    return 96;\n}",
    marker="fn q2_cat_n(c:i32)i32 {\n    if(c==0){return 48;} if(c==1){return 48;} if(c==2){return 48;}")
sub_once(tr, "while(cat<6){", "while(cat<4){", marker="while(cat<4){")
sub_once(tr, "// D2: the Track 5 arm-B curriculum geometry; the taught content is the",
         "// D2: the English 4-category curriculum geometry; the taught content is the")
sub_re_ml(tr,
    r"// a false-valued claim for id \(for interference / false-attack probes\)\nfn q2_false_val\(id:i32\)i32 \{\n    let m:i32=t5_mod\(id\);\n    let b:i32=t5_base\(id\);\n    return b\+\(\(\(t5_truth\(id\)-b\)\+1\)%m\);\n\}\n",
    "// a false-valued claim for id (for interference / false-attack probes)\n"
    "// English: the trainer-supplied value for the 12 false ids (differs from\n"
    "// truth by construction); truth+1 otherwise.\n"
    "fn q2_false_val(id:i32)i32 {\n"
    "    if(t5_is_false_plant(id)==1){return t5_plant_claim(id);}\n"
    "    return t5_truth(id)+1;\n}\n",
    already="t5_plant_claim(id);}")
sub_re_ml(tr,
    r"// landmark l valid for D2: true, non-held-out, chain ruler true\+non-held-out\nfn q2_lm_valid\(c:\*Q2CTX,l:i32\)i32 \{.*?\n\}\n",
    "// landmark l valid for D2 (English two-hop): alpha-pos id l (truth = letter\n"
    "// position p in 1..26) -> word-len id 48+(p-1). Both the landmark and the\n"
    "// true target must be non-false and non-held-out.\n"
    "fn q2_lm_valid(c:*Q2CTX,l:i32)i32 {\n"
    "    let ho:[]u8=c.*.ho;\n"
    "    let fid:i32=l;\n"
    "    if(t5_is_false_plant(fid)==1){return 0;}\n"
    "    if(q2_ho_has(ho,fid)==1){return 0;}\n"
    "    let p:i32=t5_truth(fid);\n"
    "    let tid:i32=48+(p-1);\n"
    "    if(t5_is_false_plant(tid)==1){return 0;}\n"
    "    if(q2_ho_has(ho,tid)==1){return 0;}\n"
    "    return 1;\n}\n",
    already="// landmark l valid for D2 (English two-hop)")
# D2 block: exact-string replacement (regex backtracks on DOTALL here)
D2_OLD = """    // D2: two-hop landmark->ruler->year inference
    let vc:i32=0;
    let li:i32=0;
    while(li<48){if(q2_lm_valid(c,li)==1){vc=vc+1;} li=li+1;}
    let take:i32=40;
    if(vc<40){take=vc;}
    let d2:i32=0;
    let got:i32=0;
    li=0;
    while(li<48 && got<take){
        let l:i32=(li*37+rep*11)%48;
        if(q2_lm_valid(c,l)==1){
            let kk:i32=t5_truth(192+l);
            let yexp:i32=t5_truth(72+kk);
            let ygot:i32=-1000;
            if(arm==3){
                let lk:i32=d1_answer(s,192+l);
                if(lk>=0 && lk<=35){ygot=d1_answer(s,72+lk);}
            }else{
                let lk2:i32=d2_answer(s,192+l);
                if(lk2>=0 && lk2<=35){ygot=d2_answer(s,72+lk2);}
            }
            if(ygot==yexp){d2=d2+1;}
            got=got+1;
        }
        li=li+1;
    }
    c.*.d2c=d2;c.*.d2n=take;
"""
D2_NEW = """    // D2: two-hop inference (English): alpha-pos id l (truth p in 1..26)
    // -> word-len id 48+(p-1). The learner must chain two stored facts.
    let vc:i32=0;
    let li:i32=0;
    while(li<48){if(q2_lm_valid(c,li)==1){vc=vc+1;} li=li+1;}
    let take:i32=40;
    if(vc<40){take=vc;}
    let d2:i32=0;
    let got:i32=0;
    li=0;
    while(li<48 && got<take){
        let l:i32=(li*37+rep*11)%48;
        if(q2_lm_valid(c,l)==1){
            let pp:i32=t5_truth(l);
            let yexp:i32=t5_truth(48+(pp-1));
            let ygot:i32=-1000;
            if(arm==3){
                let lk:i32=d1_answer(s,l);
                if(lk>=1 && lk<=26){ygot=d1_answer(s,48+(lk-1));}
            }else{
                let lk2:i32=d2_answer(s,l);
                if(lk2>=1 && lk2<=26){ygot=d2_answer(s,48+(lk2-1));}
            }
            if(ygot==yexp){d2=d2+1;}
            got=got+1;
        }
        li=li+1;
    }
    c.*.d2c=d2;c.*.d2n=take;
"""
_tt = open(tr).read()
if D2_OLD in _tt:
    assert _tt.count(D2_OLD) == 1
    open(tr, "w").write(_tt.replace(D2_OLD, D2_NEW))
elif D2_NEW in _tt:
    pass  # already transformed
else:
    raise AssertionError("D2 block: neither old nor new present")
sub_all(tr, "usage: muset ", "usage: grokt ")
t = open(tr).read()
assert "muse_" not in t and "MUSE_" not in t, "leftover muse in trial"
assert "t5_mod(" not in t and "t5_base(" not in t, "leftover Zharovia helpers"
print("transformed legA/src/grok_trial.zag", flush=True)

# ---------- 4. legB / legC drivers ----------
for leg, drv, pfx, sealed, canary, tid_note in (
    ("legB", "grok_b7_direct.zag", "MUSEB_", "muse/b7direct/sealed",
     "MUB7:direct", "(teacher_id=20, TB_TID_DIRECT)"),
    ("legC", "grok_teacher_leg.zag", "MUSEC_", "muse/teacherleg/sealed",
     "MUCT:teacher21", None)):
    p = os.path.join(LEGS, leg, "src", drv)
    sub_all(p, '@import("muse_corpus.zag")', '@import("corpus.zag")')
    sub_all(p, '@import("muse_teach.zag")', '@import("grok_teach.zag")')
    sub_all(p, "muse_t_phase1", "grok_t_phase1")
    sub_all(p, "muse_t_phase2", "grok_t_phase2")
    sub_all(p, "MUSE_CORPUS_SHA256", "GROK_CORPUS_SHA256")
    sub_all(p, pfx, pfx.replace("MUSE", "GROK"))
    sub_all(p, sealed, sealed.replace("muse/", "grok/"))
    sub_all(p, canary, {"MUB7:direct": "GROKB7:direct",
                        "MUCT:teacher21": "GROKT:teacher44"}[canary])
    sub_all(p, ".last20=0", ".last54=0")
    sub_all(p, ".last21=0", ".last44=0")
    if tid_note:
        sub_all(p, tid_note, "(teacher_id=54, TB_TID_DIRECT)")
    print(f"renames applied: {leg}/src/{drv}", flush=True)

b = os.path.join(LEGS, "legB", "src", "grok_b7_direct.zag")
sub_once(b, 'cl_check("mb_disconnects",disconn,6)', 'cl_check("mb_disconnects",disconn,4)')
sub_once(b, "muse_b7_direct.zag — CLASS 4 (direct leg)", "grok_b7_direct.zag — CLASS 4 (direct leg)")
sub_once(b, "TAUGHT-LEARNER: D2 teaching route (muse_teach.zag) on the frozen\n// muse-native corpus",
         "TAUGHT-LEARNER: D2 teaching route (grok_teach.zag) on the frozen\n// grok-4.6 English corpus")
sub_once(b, "(GROKB_TEACH_DIGEST must equal MUSEC_TEACH_DIGEST)",
         "(GROKB_TEACH_DIGEST must equal GROKC_TEACH_DIGEST)",
         marker="TEACH_DIGEST cross-checked")

c = os.path.join(LEGS, "legC", "src", "grok_teacher_leg.zag")
sub_once(c, 'cl_check("mc_teacher_disconnects",disconn,6)', 'cl_check("mc_teacher_disconnects",disconn,4)')
sub_once(c, "muse_teacher_leg.zag — CLASS 3 (teacher leg)", "grok_teacher_leg.zag — CLASS 3 (teacher leg)")
sub_all(c, "(teacher_id=21)", "(teacher_id=44)", marker="(teacher_id=44)")
sub_once(c, "becomes the teacher (teacher_id=21) of a fresh arm-B-style learner.",
         "becomes the teacher (teacher_id=44) of a fresh arm-B-style learner.")
sub_once(c, "TEACHER: D2 teaching route (muse_teach.zag) on the frozen muse-native\n// corpus",
         "TEACHER: D2 teaching route (grok_teach.zag) on the frozen grok-4.6 English\n// corpus")
sub_once(c, "(GROKC_TEACH_DIGEST must\n// equal MUSEB_TEACH_DIGEST)",
         "(GROKC_TEACH_DIGEST must\n// equal GROKB_TEACH_DIGEST)",
         marker="GROKC_TEACH_DIGEST must\n// equal GROKB_TEACH_DIGEST")

# final driver verification (after header fixes): no muse_/MUSE_ remnants
for leg, drv in (("legB", "grok_b7_direct.zag"), ("legC", "grok_teacher_leg.zag")):
    p = os.path.join(LEGS, leg, "src", drv)
    sub_all(p, "MUSE_CORPUS", "GROK_CORPUS")
    tt = open(p).read()
    assert "muse_" not in tt and "MUSE_" not in tt, f"leftover muse in {drv}"
    print(f"verified clean: {leg}/src/{drv}", flush=True)

# ---------- 5. q1_types.zag / q1_proposal.zag: teacher ids 44 / 54 ----------
for leg in ("legB", "legC"):
    qt = os.path.join(LEGS, leg, "src", "q1_types.zag")
    sub_once(qt, "const TB_TID_DIRECT:i64=20;", "const TB_TID_DIRECT:i64=54;")
    sub_once(qt, "const TB_TID_MUSETAUGHT:i64=21;", "const TB_TID_GROKTAUGHT:i64=44;")
    sub_once(qt, "// TB_TID_DIRECT(20): driver-presented sealed probes (class-4 direct leg).",
             "// TB_TID_DIRECT(54): driver-presented sealed probes (class-4 direct leg).")
    sub_once(qt, "// TB_TID_MUSETAUGHT(21): the M2 taught-learner as teacher (class-3 leg).",
             "// TB_TID_GROKTAUGHT(44): the M2 taught-learner as teacher (class-3 leg).")
    qp = os.path.join(LEGS, leg, "src", "q1_proposal.zag")
    sub_all(qp, "TB_TID_MUSETAUGHT", "TB_TID_GROKTAUGHT")
    # the class-3 driver references the taught-teacher tid directly
    if leg == "legC":
        dc = os.path.join(LEGS, leg, "src", "grok_teacher_leg.zag")
        sub_all(dc, "TB_TID_MUSETAUGHT", "TB_TID_GROKTAUGHT",
                marker="TB_TID_GROKTAUGHT")
    sub_once(qp, "last20:i64, last21:i64,", "last54:i64, last44:i64,")
    sub_all(qp, "s.*.last20", "s.*.last54")
    sub_all(qp, "s.*.last21", "s.*.last44")
    sub_all(qp, "MUSE-CLASS", "GROK-CLASS")
    sub_once(qp, "TB_TID_DIRECT(20), TB_TID_GROKTAUGHT(21) accepted.",
             "TB_TID_DIRECT(54), TB_TID_GROKTAUGHT(44) accepted.")
    qw = os.path.join(LEGS, leg, "src", "q1_world.zag")
    sub_all(qw, "MUSE-CLASS", "GROK-CLASS")
    print(f"teacher ids set: {leg} (direct=54, taught-teacher=44)", flush=True)

# re-sync the teach copies into legB/legC src
import shutil
for leg in ("legB", "legC"):
    shutil.copy(os.path.join(LEGS, "shared", "grok_teach.zag"),
                os.path.join(LEGS, leg, "src", "grok_teach.zag"))
print("teach copies re-synced", flush=True)

# comment-level Zharovia mentions in q1_types.zag / q1_world.zag (both legs)
for leg in ("legB", "legC"):
    for f in ("q1_types.zag", "q1_world.zag"):
        p = os.path.join(LEGS, leg, "src", f)
        sub_all(p, "Zharovia", "English", marker="English")

# final sweep: no muse_ / MUSE_ / Zharovia remnants outside substrate
import subprocess
r = subprocess.run(["grep", "-rn", "muse_\\|MUSE_\\|Zharovia\\|zharovia", LEGS,
                    "--include=*.zag", "--exclude-dir=substrate"],
                   capture_output=True, text=True)
assert r.stdout == "", f"remnants:\n{r.stdout}"
print("final sweep clean", flush=True)
