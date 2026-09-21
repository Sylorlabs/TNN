#!/usr/bin/env python3
"""Assemble the hy3 ENGLISH championship legs from the muse-native sources.

Copies legA/legB/legC + shared sources from the frozen muse-native trial
(~/workspace/tnn-lab/wave12/championship/muse-native/trial/tnn), applies the
mechanical hy3/ENGLISH port transforms, and writes:

  tnn/shared/hy3_teach.zag         D2 teaching library (port of muse_teach.zag)
  tnn/legA/src/hy3_trial.zag       Track-5 M2 composite driver (main)
  tnn/legB/src/hy3_b7_direct.zag   class-4 direct §B.7 driver (main)
  tnn/legC/src/hy3_teacher_leg.zag class-3 teacher-leg driver (main)

plus per-leg copies of q1_*.zag (tid delta), t5_traps.zag, substrate/, and
the generated t5_core.zag (English domain) + hy3_corpus.zag (build_gen.py).

PORT TRANSFORMS (explicit; the §B.7 flaw battery itself is VERBATIM):
 P1 corpus accessors muse_* -> hy3_*; MUSE_CORPUS_SHA256 -> HY3_CORPUS_SHA256
 P2 teacher ids: TB_TID_DIRECT 20->55, TB_TID_HY3TAUGHT 21->45;
    TbSess.last20/last21 -> last55/last45; tb_sess_last/tb_sess_bump rewritten
    FLAT (ZNC-2026-09-21-013: 5-deep else-nesting miscompiles)
 P3 category geometry 6 -> 4: cat bases 0/48/96/144, n's 48/48/48/96;
    phase-1 category loop while(cat<6) -> while(cat<4); disconnect checks 6->4
 P4 q2_false_val: truth+1 (English values have no modulus structure; the
    value only needs to be != truth for interference/false-attack probes)
 P5 D2 battery: two-hop word-len -> alpha-pos inference. Structural analog
    of the Zharovia landmark->ruler chain: first hop recalls the word length
    L of a word-len fact w (48..95); second hop uses L to index the alphabet
    table (id L-1, truth L). Valid iff w non-false, non-held-out, L in
    1..26, and id L-1 non-false and non-held-out. (Documented in hy3_trial.zag.)
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))          # hy3/tnn
MUSE = ("/home/hatch/workspace/tnn-lab/wave12/championship/muse-native"
        "/trial/tnn")
SHARED = os.path.join(HERE, "shared")

TID_DIRECT = 55
TID_TAUGHT = 45

# ---------------------------------------------------------------- helpers

def read(p):
    with open(p) as f:
        return f.read()

def write(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        f.write(s)
    print(f"wrote {p} ({len(s)} bytes)", flush=True)

def rep(s, pairs):
    for old, new in pairs:
        assert old in s, f"transform target missing: {old[:70]!r}"
        s = s.replace(old, new)
    return s

def assert_no_muse_code(s, what):
    """No muse_/MUSE identifiers may survive in CODE lines (comments may
    still name the source file they were ported from)."""
    code = "\n".join(l for l in s.split("\n") if not l.lstrip().startswith("//"))
    assert "muse_" not in code and "MUSE" not in code, \
        f"muse remnants in code of {what}"

# ---------------------------------------------------------------- P2: q1_types / q1_proposal

def port_q1_types(src):
    s = read(src)
    s = rep(s, [
        ("// TB_TID_DIRECT(20): driver-presented sealed probes (class-4 direct leg).",
         "// TB_TID_DIRECT(55): driver-presented sealed probes (class-4 direct leg)."),
        ("// TB_TID_MUSETAUGHT(21): the M2 taught-learner as teacher (class-3 leg).",
         "// TB_TID_HY3TAUGHT(45): the M2 taught-learner as teacher (class-3 leg)."),
        ("const TB_TID_DIRECT:i64=20;", "const TB_TID_DIRECT:i64=55;"),
        ("const TB_TID_MUSETAUGHT:i64=21;", "const TB_TID_HY3TAUGHT:i64=45;"),
        ("// ---- MUSE-CLASS delta (championship): new teacher ids in the 20s.",
         "// ---- HY3-CLASS delta (championship): new teacher ids (45/55).\n// Port of the MUSE-CLASS delta."),
    ])
    return s

FLAT_LAST = """fn tb_sess_last(s:*TbSess,tid:i64)i64 {
    // HY3-CLASS: flat dispatch (ZNC-2026-09-21-013: never nest else 5-deep).
    if(tid==TB_TID_PEER){return s.*.last1;}
    if(tid==TB_TID_MUSE){return s.*.last3;}
    if(tid==TB_TID_SYMHINT){return s.*.last4;}
    if(tid==TB_TID_PLANTED){return s.*.last6;}
    if(tid==TB_TID_DIRECT){return s.*.last55;}
    if(tid==TB_TID_HY3TAUGHT){return s.*.last45;}
    return s.*.last5;
}"""

FLAT_BUMP = """fn tb_sess_bump(s:*TbSess,tid:i64,seq:i64)void {
    // HY3-CLASS: flat dispatch (ZNC-2026-09-21-013: never nest else 5-deep).
    // tids are distinct constants: sequential ifs route exactly one branch,
    // and the trailing default reproduces the original final else.
    if(tid==TB_TID_PEER){s.*.last1=seq;}
    if(tid==TB_TID_MUSE){s.*.last3=seq;}
    if(tid==TB_TID_SYMHINT){s.*.last4=seq;}
    if(tid==TB_TID_PLANTED){s.*.last6=seq;}
    if(tid==TB_TID_DIRECT){s.*.last55=seq;}
    if(tid==TB_TID_HY3TAUGHT){s.*.last45=seq;}
    let known:i32=0;
    if(tid==TB_TID_PEER){known=1;}
    if(tid==TB_TID_MUSE){known=1;}
    if(tid==TB_TID_SYMHINT){known=1;}
    if(tid==TB_TID_PLANTED){known=1;}
    if(tid==TB_TID_DIRECT){known=1;}
    if(tid==TB_TID_HY3TAUGHT){known=1;}
    if(known==0){s.*.last5=seq;}
    s.*.n_props=s.*.n_props+1;
    return;
}"""

def port_q1_proposal(src):
    s = read(src)
    s = rep(s, [
        ("    last20:i64, last21:i64, // MUSE-CLASS: direct(20)/taught-teacher(21) seq",
         "    last55:i64, last45:i64, // HY3-CLASS: direct(55)/taught-teacher(45) seq"),
        ("    s.*.last20=0; s.*.last21=0; // MUSE-CLASS",
         "    s.*.last55=0; s.*.last45=0; // HY3-CLASS"),
        ("    if(tid==TB_TID_DIRECT){return s.*.last20;} // MUSE-CLASS",
         "    if(tid==TB_TID_DIRECT){return s.*.last55;} // HY3-CLASS"),
        ("    if(tid==TB_TID_MUSETAUGHT){return s.*.last21;} // MUSE-CLASS",
         "    if(tid==TB_TID_HY3TAUGHT){return s.*.last45;} // HY3-CLASS"),
        ("// MUSE-CLASS delta: TB_TID_DIRECT(20), TB_TID_MUSETAUGHT(21) accepted.",
         "// HY3-CLASS delta: TB_TID_DIRECT(55), TB_TID_HY3TAUGHT(45) accepted."),
        ("tid!=TB_TID_MUSETAUGHT", "tid!=TB_TID_HY3TAUGHT"),
    ])
    # replace the two nested-dispatch functions wholesale with flat versions
    i0 = s.index("fn tb_sess_last(")
    i1 = s.index("// Build a §P proposal into out")
    s = s[:i0] + FLAT_LAST + "\n\n" + FLAT_BUMP + "\n\n" + s[i1:]
    s = s.replace("MUSE-CLASS", "HY3-CLASS")
    assert "last20" not in s and "last21" not in s
    return s

# ---------------------------------------------------------------- hy3_teach.zag (P1+P3)

TEACH_HEADER = """// hy3_teach.zag — D2 teaching-route library (HY3 ENGLISH).
//
// Mechanical port of muse_teach.zag (MUSE-NATIVE): eliminative-verification
// teaching, per-category disconnects, phase-2 disproof. D2-only.
// Used by leg B (direct §B.7) and leg C (teacher leg) to build the
// taught-learner identically. ENGLISH geometry: 4 categories
// (alpha-pos 0-47, word-len 48-95, pub-year 96-143, count-fact 144-239).
"""

def port_teach(src):
    s = read(src)
    # header: replace up to the first @import
    i = s.index("@import")
    s = TEACH_HEADER + s[i:]
    s = rep(s, [
        ('@import("muse_corpus.zag")', '@import("hy3_corpus.zag")'),
        ("muse_t_false_nth", "hy3_t_false_nth"),
        ("muse_t_cat_n", "hy3_t_cat_n"),
        ("muse_t_cat_base", "hy3_t_cat_base"),
        ("muse_t_cat_id", "hy3_t_cat_id"),
        ("muse_t_seed_id", "hy3_t_seed_id"),
        ("muse_t_is_seed", "hy3_t_is_seed"),
        ("muse_t_pool_id", "hy3_t_pool_id"),
        ("muse_t_heldout", "hy3_t_heldout"),
        ("muse_t_ho_has", "hy3_t_ho_has"),
        ("muse_t_build_ho", "hy3_t_build_ho"),
        ("muse_t_evidence_subset", "hy3_t_evidence_subset"),
        ("muse_t_teach_one", "hy3_t_teach_one"),
        ("muse_t_phase1", "hy3_t_phase1"),
        ("muse_t_phase2", "hy3_t_phase2"),
        ("muse_obs_at", "hy3_obs_at"),
        ("muse_prb_at", "hy3_prb_at"),
        ("muse_dis_at", "hy3_dis_at"),
        # P3: 4-category geometry
        ("    if(c==0){return 48;} if(c==1){return 24;} if(c==2){return 36;}\n"
         "    if(c==3){return 48;} if(c==4){return 36;} return 48;",
         "    if(c==0){return 48;} if(c==1){return 48;} if(c==2){return 48;}\n"
         "    return 96;"),
        ("    if(c==0){return 0;} if(c==1){return 48;} if(c==2){return 72;}\n"
         "    if(c==3){return 108;} if(c==4){return 156;} return 192;",
         "    if(c==0){return 0;} if(c==1){return 48;} if(c==2){return 96;}\n"
         "    return 144;"),
        ("    while(cat<6){", "    while(cat<4){"),
        ("// seed/pool/held-out geometry (Track 5, verbatim)",
         "// seed/pool/held-out geometry (Track 5, verbatim; same 12 false ids)"),
    ])
    assert_no_muse_code(s, "hy3_teach.zag")
    return s

# ---------------------------------------------------------------- hy3_trial.zag (P1+P3+P4+P5)

TRIAL_HEADER = """// hy3_trial.zag — HY3-ENGLISH leg-A driver: Q2 D2 teaching route on the
// frozen hy3 English corpus (mechanical port of muse_trial.zag, itself a
// mechanical port of q2_trial.zag; arm 4 / D2 only).
//
// ENGLISH-CLASS deltas (documented; everything else verbatim):
//  - 4 categories (alpha-pos 0-47, word-len 48-95, pub-year 96-143,
//    count-fact 144-239); per-category disconnects -> 4.
//  - q2_false_val(id) = t5_truth(id)+1 (English values have no modulus
//    structure; interference probes only need a value != truth).
//  - D2 battery: two-hop word-len -> alpha-pos inference. Structural analog
//    of the Zharovia landmark->ruler chain: first hop recalls the word
//    length L of a word-len fact w (48..95); second hop uses L to index the
//    alphabet table (id L-1, truth L). A word-len id is battery-valid iff
//    it is non-false, non-held-out, L in 1..26, and id L-1 non-false and
//    non-held-out. The learner's first-hop answer (not the key) selects the
//    second-hop id, exactly as the landmark answer selected the ruler.
// Modes/RESULT lines/byte-identical contract: unchanged from muse_trial.zag.
// main() reads _zag_arg unconditionally (ZNC-2026-09-21-007).
"""

ENGLISH_LM_VALID = """// ENGLISH-CLASS D2 validity: word-len id w=48+l is battery-valid iff
// non-false, non-held-out, L=t5_truth(w) in 1..26 (maps into the first
// alphabet cycle), and the second-hop id L-1 non-false and non-held-out.
fn q2_lm_valid(c:*Q2CTX,l:i32)i32 {
    let ho:[]u8=c.*.ho;
    let w:i32=48+l;
    if(t5_is_false_plant(w)==1){return 0;}
    if(q2_ho_has(ho,w)==1){return 0;}
    let L:i32=t5_truth(w);
    if(L<1 || L>26){return 0;}
    let aid:i32=L-1;
    if(t5_is_false_plant(aid)==1){return 0;}
    if(q2_ho_has(ho,aid)==1){return 0;}
    return 1;
}"""

ENGLISH_D2 = """    // D2: two-hop word-len->alpha-pos inference (ENGLISH-CLASS)
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
            let L:i32=t5_truth(48+l);
            let yexp:i32=t5_truth(L-1);
            let ygot:i32=-1000;
            if(arm==3){
                let lk:i32=d1_answer(s,48+l);
                if(lk>=1 && lk<=26){ygot=d1_answer(s,lk-1);}
            }else{
                let lk2:i32=d2_answer(s,48+l);
                if(lk2>=1 && lk2<=26){ygot=d2_answer(s,lk2-1);}
            }
            if(ygot==yexp){d2=d2+1;}
            got=got+1;
        }
        li=li+1;
    }
    c.*.d2c=d2;c.*.d2n=take;"""

ENGLISH_FALSE_VAL = """// ENGLISH-CLASS: a false-valued claim for id (for interference /
// false-attack probes). English values have no modulus structure;
// truth+1 is mechanically wrong and deterministic.
fn q2_false_val(id:i32)i32 {
    return t5_truth(id)+1;
}"""

def port_trial(src):
    s = read(src)
    i = s.index("@import")
    s = TRIAL_HEADER + s[i:]
    s = rep(s, [
        ('@import("muse_corpus.zag")', '@import("hy3_corpus.zag")'),
        ("muse_dump_at", "hy3_dump_at"),
        ("muse_obs_at", "hy3_obs_at"),
        ("muse_prb_at", "hy3_prb_at"),
        ("muse_dis_at", "hy3_dis_at"),
        ("MUSE_CORPUS_SHA256", "HY3_CORPUS_SHA256"),
        # P3: 4-category geometry
        ("fn q2_cat_base(c:i32)i32 {\n"
         "    if(c==0){return 0;} if(c==1){return 48;} if(c==2){return 72;}\n"
         "    if(c==3){return 108;} if(c==4){return 156;} return 192;\n}",
         "fn q2_cat_base(c:i32)i32 {\n"
         "    if(c==0){return 0;} if(c==1){return 48;} if(c==2){return 96;}\n"
         "    return 144;\n}"),
        ("fn q2_cat_n(c:i32)i32 {\n"
         "    if(c==0){return 48;} if(c==1){return 24;} if(c==2){return 36;}\n"
         "    if(c==3){return 48;} if(c==4){return 36;} return 48;\n}",
         "fn q2_cat_n(c:i32)i32 {\n"
         "    if(c==0){return 48;} if(c==1){return 48;} if(c==2){return 48;}\n"
         "    return 96;\n}"),
        ("    while(cat<6){", "    while(cat<4){"),
        # usage strings
        ('"usage: muset <bind <label> <armidx> <rep> <scale>|btrap <label> <armidx> <rep>>"',
         '"usage: hy3t <bind <label> <armidx> <rep> <scale>|btrap <label> <armidx> <rep>>"'),
        ('"usage: muset bind <label> <armidx> <rep> <scale>"',
         '"usage: hy3t bind <label> <armidx> <rep> <scale>"'),
        ('"usage: muset btrap <label> <armidx> <rep>"',
         '"usage: hy3t btrap <label> <armidx> <rep>"'),
    ])
    # P4: replace q2_false_val wholesale
    f0 = s.index("// a false-valued claim for id (for interference / false-attack probes)")
    f1 = s.index("// landmark l valid for D2:")
    s = s[:f0] + ENGLISH_FALSE_VAL + "\n" + s[f1:]
    # P5: replace q2_lm_valid wholesale
    l0 = s.index("// landmark l valid for D2:")
    l1 = s.index("// ---- arm answer functions ----")
    s = s[:l0] + ENGLISH_LM_VALID + "\n\n" + s[l1:]
    # P5: replace the D2 battery block in q2_phase4
    d0 = s.index("    // D2: two-hop landmark->ruler->year inference")
    d1 = s.index("    // D3: 40 judgment triples, pairwise concordance")
    s = s[:d0] + ENGLISH_D2 + "\n" + s[d1:]
    assert_no_muse_code(s, "hy3_trial.zag")
    return s

# ---------------------------------------------------------------- hy3_b7_direct.zag / hy3_teacher_leg.zag

def sealed_path_fn(name, text):
    bs = text.encode()
    L = [f"fn {name}()[]u8 {{"]
    L.append(f"    let b:[]u8=nio_alloc({len(bs)});")
    for i, ch in enumerate(bs):
        L.append(f"    b[{i}]={ch} as u8;")
    L.append("    return b;")
    L.append("}")
    return "\n".join(L)

def port_driver(src, kind):
    """kind: 'B' (direct §B.7) or 'C' (teacher leg)."""
    s = read(src)
    i = s.index("@import")
    if kind == "B":
        header = ("// hy3_b7_direct.zag — CLASS 4 (direct leg): the M2 taught-learner\n"
                  "// judges the sealed §B.7 flaw battery directly.\n//\n"
                  "// Mechanical port of muse_b7_direct.zag (MUSE-NATIVE). TAUGHT-LEARNER:\n"
                  "// D2 teaching route (hy3_teach.zag) on the frozen hy3 English corpus\n"
                  "// — all 240 ids, phase-2 disproof, 4 per-category disconnects.\n"
                  "// BATTERY: the 8 frozen §B.7 flaw slices presented DIRECTLY as §P\n"
                  "// proposals (teacher_id=55, TB_TID_DIRECT) — VERBATIM, value-agnostic.\n"
                  "// Pure Zag, zero RNG. N=5 byte-identical.\n")
        pairs = [
            ('@import("muse_corpus.zag")', '@import("hy3_corpus.zag")'),
            ('@import("muse_teach.zag")', '@import("hy3_teach.zag")'),
            ("MUSE_CORPUS_SHA256", "HY3_CORPUS_SHA256"),
            ('"MUSE_CORPUS,"', '"HY3_CORPUS,"'),
            ("muse_t_phase1", "hy3_t_phase1"),
            ("muse_t_phase2", "hy3_t_phase2"),
            ("mb_sealedpath", "hb_sealedpath"),
            ("mb_canary", "hb_canary"),
            ("mb_hex", "hb_hex"),
            ("mb_state_digest", "hb_state_digest"),
            ('"mb_t0_empty"', '"hb_t0_empty"'),
            ('"mb_teach_eps"', '"hb_teach_eps"'),
            ('"mb_disconnects",disconn,6', '"hb_disconnects",disconn,4'),
            ('"mb_learn_gate"', '"hb_learn_gate"'),
            ('"mb_slice_stim_placed"', '"hb_slice_stim_placed"'),
            ('"mb_slice_emit_ok"', '"hb_slice_emit_ok"'),
            ('"mb_slice_manifest_n"', '"hb_slice_manifest_n"'),
            ('"mb_slice_tripwire_fired"', '"hb_slice_tripwire_fired"'),
            ('"mb_slice_manifest_init"', '"hb_slice_manifest_init"'),
            ('"mb_slice_leak"', '"hb_slice_leak"'),
            ('"mb_slice_hnm12"', '"hb_slice_hnm12"'),
            ("MUSEB_TEACH_DIGEST", "HY3B_TEACH_DIGEST"),
            ("MUSEB_TEACH", "HY3B_TEACH"),
            ("MUSEB_SLICE", "HY3B_SLICE"),
            ("MUSEB_RUN", "HY3B_RUN"),
            ("MUSEB_COMPLETE", "HY3B_COMPLETE"),
            ("MUSEB_FAIL", "HY3B_FAIL"),
            (".last20=0,.last21=0,", ".last55=0,.last45=0,"),
            ("// DIRECT: the 12 frozen §B.7 flaws as §P proposals, tid=20.",
             "// DIRECT: the 12 frozen §B.7 flaws as §P proposals, tid=55."),
        ]
        new_sealed = sealed_path_fn("hb_sealedpath", "hy3/b7direct/sealed")
        new_canary = sealed_path_fn("hb_canary", "HYB7:direct")
    else:
        header = ("// hy3_teacher_leg.zag — CLASS 3 (teacher leg): the M2 taught-learner\n"
                  "// becomes the teacher (teacher_id=45) of a fresh learner.\n//\n"
                  "// Mechanical port of muse_teacher_leg.zag (MUSE-NATIVE). TEACHER: D2\n"
                  "// route on the frozen hy3 English corpus — all 240 ids, phase-2\n"
                  "// disproof, 4 per-category disconnects. LEARNER: fresh scaffold-\n"
                  "// and-release + 8 teaching slices with the frozen §B.7 flaw schedule\n"
                  "// (flaw-first, tid=45), clean teaching after — VERBATIM, value-agnostic.\n"
                  "// Pure Zag, zero RNG. N=5 byte-identical.\n")
        pairs = [
            ('@import("muse_corpus.zag")', '@import("hy3_corpus.zag")'),
            ('@import("muse_teach.zag")', '@import("hy3_teach.zag")'),
            ("MUSE_CORPUS_SHA256", "HY3_CORPUS_SHA256"),
            ('"MUSE_CORPUS,"', '"HY3_CORPUS,"'),
            ("TB_TID_MUSETAUGHT", "TB_TID_HY3TAUGHT"),
            ("muse_t_phase1", "hy3_t_phase1"),
            ("muse_t_phase2", "hy3_t_phase2"),
            ("mc_sealedpath", "hc_sealedpath"),
            ("mc_canary", "hc_canary"),
            ("mc_hex", "hc_hex"),
            ("mc_state_digest", "hc_state_digest"),
            ("mc_audit_empty", "hc_audit_empty"),
            ("mc_recall_ok", "hc_recall_ok"),
            ('"mc_teacher_teach_eps"', '"hc_teacher_teach_eps"'),
            ('"mc_teacher_disconnects",disconn,6', '"hc_teacher_disconnects",disconn,4'),
            ('"mc_teacher_learn_gate"', '"hc_teacher_learn_gate"'),
            ('"mc_teacher_holds_curriculum"', '"hc_teacher_holds_curriculum"'),
            ('"mc_learner_t0_empty_n"', '"hc_learner_t0_empty_n"'),
            ('"mc_learner_t0_audit_empty"', '"hc_learner_t0_audit_empty"'),
            ('"mc_scaffold_placed"', '"hc_scaffold_placed"'),
            ('"mc_scaffold_added"', '"hc_scaffold_added"'),
            ('"mc_disconnect_audited"', '"hc_disconnect_audited"'),
            ('"mc_slice_stim_placed"', '"hc_slice_stim_placed"'),
            ('"mc_slice_emit_ok"', '"hc_slice_emit_ok"'),
            ('"mc_slice_teacher_blocked"', '"hc_slice_teacher_blocked"'),
            ('"mc_slice_manifest_n"', '"hc_slice_manifest_n"'),
            ('"mc_slice_tripwire_fired"', '"hc_slice_tripwire_fired"'),
            ('"mc_slice_manifest_init"', '"hc_slice_manifest_init"'),
            ('"mc_slice_leak"', '"hc_slice_leak"'),
            ('"mc_slice_hnm12"', '"hc_slice_hnm12"'),
            ('"mc_final_mastery_192"', '"hc_final_mastery_192"'),
            ('"mc_teacher_blocked_total"', '"hc_teacher_blocked_total"'),
            ("MUSEC_TEACH_DIGEST", "HY3C_TEACH_DIGEST"),
            ("MUSEC_TEACH", "HY3C_TEACH"),
            ("MUSEC_SLICE", "HY3C_SLICE"),
            ("MUSEC_RUN", "HY3C_RUN"),
            ("MUSEC_DIGEST", "HY3C_DIGEST"),
            ("MUSEC_COMPLETE", "HY3C_COMPLETE"),
            ("MUSEC_FAIL", "HY3C_FAIL"),
            (".last20=0,.last21=0,", ".last55=0,.last45=0,"),
            ("// ================= TEACHER: the M2 taught-learner (tid=21) =================",
             "// ================= TEACHER: the M2 taught-learner (tid=45) ================="),
            ("// FLAW-FIRST: the teacher administers the flaw exam (tid=21).",
             "// FLAW-FIRST: the teacher administers the flaw exam (tid=45)."),
        ]
        new_sealed = sealed_path_fn("hc_sealedpath", "hy3/teacherleg/sealed")
        new_canary = sealed_path_fn("hc_canary", "HYCT:teacher45")
    s = header + s[i:]
    s = rep(s, pairs)
    # replace the sealed-path and canary byte functions wholesale
    # (names already renamed by rep(); look up the NEW names)
    sealed_name = "hb_sealedpath" if kind == "B" else "hc_sealedpath"
    canary_name = "hb_canary" if kind == "B" else "hc_canary"
    for new_name, new_fn in (sealed_name, new_sealed), (canary_name, new_canary):
        f0 = s.index(f"fn {new_name}(")
        f1 = s.index("\n}\n", f0) + 3
        # also consume a trailing // comment line documenting the old bytes
        nl = s.index("\n", f1)
        if s[f1:nl].lstrip().startswith("//"):
            f1 = nl + 1
        s = s[:f0] + new_fn + "\n" + s[f1:]
    assert_no_muse_code(s, f"driver {kind}")
    assert "last20" not in s and "last21" not in s
    return s

# ---------------------------------------------------------------- main

STATIC_Q1 = ["q1_types.zag", "q1_tape.zag", "q1_tripwire.zag",
             "q1_flawscore.zag", "q1_learner.zag", "q1_world.zag"]

def main():
    # shared teaching library
    write(os.path.join(SHARED, "hy3_teach.zag"),
          port_teach(os.path.join(MUSE, "shared", "muse_teach.zag")))

    for leg, mainsrc in (("legA", None), ("legB", None), ("legC", None)):
        srcdir = os.path.join(HERE, leg, "src")
        os.makedirs(srcdir, exist_ok=True)
        # t5_traps.zag + t5_arms.zag: verbatim (use t5_truth/t5_plant_claim
        # only as abstract values — value-agnostic)
        for zf in ("t5_traps.zag", "t5_arms.zag"):
            shutil.copy(os.path.join(MUSE, "legA", "src", zf),
                        os.path.join(srcdir, zf))
        # substrate (legB layout: flat substrate/ dir)
        sub = os.path.join(MUSE, "legB", "src", "substrate")
        dst = os.path.join(srcdir, "substrate")
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(sub, dst)
        print(f"copied substrate -> {dst}", flush=True)

    # legA main
    write(os.path.join(HERE, "legA", "src", "hy3_trial.zag"),
          port_trial(os.path.join(MUSE, "legA", "src", "muse_trial.zag")))

    # legB / legC: q1 machinery + drivers
    for leg in ("legB", "legC"):
        srcdir = os.path.join(HERE, leg, "src")
        for q in STATIC_Q1:
            if q == "q1_types.zag":
                write(os.path.join(srcdir, q),
                      port_q1_types(os.path.join(MUSE, leg, "src", q)))
            elif q == "q1_proposal.zag":
                pass  # handled below
            else:
                shutil.copy(os.path.join(MUSE, leg, "src", q),
                            os.path.join(srcdir, q))
        write(os.path.join(srcdir, "q1_proposal.zag"),
              port_q1_proposal(os.path.join(MUSE, leg, "src", "q1_proposal.zag")))
        # the drivers import hy3_teach.zag from src dir: copy shared in
        shutil.copy(os.path.join(SHARED, "hy3_teach.zag"),
                    os.path.join(srcdir, "hy3_teach.zag"))
        print(f"copied hy3_teach.zag -> {srcdir}", flush=True)

    write(os.path.join(HERE, "legB", "src", "hy3_b7_direct.zag"),
          port_driver(os.path.join(MUSE, "legB", "src", "muse_b7_direct.zag"), "B"))
    write(os.path.join(HERE, "legC", "src", "hy3_teacher_leg.zag"),
          port_driver(os.path.join(MUSE, "legC", "src", "muse_teacher_leg.zag"), "C"))
    print("assembly complete", flush=True)


if __name__ == "__main__":
    main()
