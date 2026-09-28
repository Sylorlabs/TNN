#!/usr/bin/env python3
"""Generate Phase-1 promotion sources from the frozen fork mg_chunk.zag.

intake.zag     = live text-intake organ (fork's deliberative D machinery,
                 renamed tnn_*; fixed arms REMOVED; no main).
negcontrol.zag = retired fixed arms C/W/S, nc_-prefixed, frozen behavior,
                 extended classifier (new kinds -> arms fail, documented).
battery1.zag   = test harness: 24-question battery through the live path
                 plus the retired arms as negative controls.
"""
import re, sys

FORK = "/home/hatch/workspace/mg_chunking/mg_chunk.zag"
OUT = "/home/hatch/workspace/chunking_promote"
src = open(FORK).read()

MARKERS = [
    "little-endian accessors",
    "output buffer",
    "byte-string helpers",
    "chunk primitives",
    "question kinds",
    "magnifying-glass zoom",
    "deliberative chunking choice",
    "answer-line emitter",
    "deliberative arm D",
    "fixed arm C",
    "fixed arm W",
    "fixed arm S",
    "summary",
    "per-question runner",
]
# split src into dict marker -> section text (section starts at its marker line)
secs = {}
idx = [src.find("// ---------- " + m) for m in MARKERS]
for i, m in enumerate(MARKERS):
    assert idx[i] >= 0, m
    end = idx[i+1] if i+1 < len(MARKERS) else src.find("fn main() i32 {")
    secs[m] = src[idx[i]:end]

INTAKE_HEADER = """// intake.zag — TNN LIVE TEXT-INTAKE ORGAN (promoted 2026-09-26).
//
// Micah ruling 2026-09-26 ~09:49 PDT: promote the magnifying-glass chunking
// fork as TNN's live text-intake path. intake(question, text) answers via
// the deliberative chunker: TNN chooses HOW to chunk (CHAR / WORD /
// WORD>CHAR / WORD?CHARSCAN), every choice recorded with a reason, zoom
// trace emitted. The zoom trace IS the deliberation record (n5_zoom
// precedent: mg_zoom(qid, parent, roff, rlen, depth, why)).
//
// LIVE-PATH CONTRACT:
//   * The ONLY entry point is tnn_intake(...). It always emits the
//     chunking choice + reason + zoom trace (the trace contract is never
//     relaxed: no silent chunking).
//   * The fixed arms (C/W/S) are RETIRED from the live path per Micah's
//     ruling ("that's the arms' fault for failing when TNN got it right,
//     so obviously don't use fixed arms that answered H"). They survive
//     ONLY in negcontrol.zag as negative controls for tests. This file
//     does not import them, does not call them, does not know them.
//   * Zero RNG. Deterministic: byte-identical reruns.
//
// Promoted from the frozen fork docs/lab/mg_chunking (commit
// 1de59c334aea10907cdc34545c7a3e97a868c6d2); deliberative machinery
// renamed d_* -> tnn_*, behavior unchanged.
@import("./R33_NATIVE_IO_V1.zag")

"""

NC_HEADER = """// negcontrol.zag — RETIRED FIXED ARMS. NEGATIVE CONTROL ONLY.
//
// *** NOT PART OF THE LIVE PATH. ***
//
// Per Micah's ruling 2026-09-26 ~09:49 PDT the fixed chunking arms
// (C = fixed character chunks, W = fixed word chunks, S = fixed 4-byte
// spans) are RETIRED from TNN's text-intake path: on the q22 sub-span trap
// ("what is the 2nd letter of fox") C and S answered "h" — a different
// question than asked — and W only survived via a recorded sub-word
// fallback escape hatch (18 fallbacks across the battery).
//
// They are kept in the codebase for ONE purpose: as negative controls in
// test harnesses (battery1.zag, battery2.zag), proving the live path
// beats them and that their known failures persist. NEVER import this
// file from live intake code. NEVER call nc_c_answer / nc_w_answer /
// nc_s_answer from any production path.
//
// Behavior is FROZEN at the fork's arms (byte-for-byte semantics on the
// original 24 questions). The classifier is extended with the Phase-2
// nested kinds (10-17) so the controls run the expanded battery: the
// frozen arms cannot parse the nested forms and fail them, which is
// itself the documented control outcome (fixed arms cannot adapt).
@import("./R33_NATIVE_IO_V1.zag")

"""

# ---------- intake.zag ----------
parts = [INTAKE_HEADER]
for m in ["little-endian accessors", "output buffer", "byte-string helpers",
          "chunk primitives", "question kinds", "magnifying-glass zoom",
          "deliberative chunking choice", "answer-line emitter"]:
    parts.append(secs[m])
dsec = secs["deliberative arm D"]
dsec = dsec.replace("fn d_answer(", "fn tnn_intake(")
dsec = dsec.replace("// ---------- deliberative arm D ----------",
                    "// ---------- live intake: deliberative chunking ----------\n"
                    "// tnn_intake is the ONLY live entry point. It never falls back:\n"
                    "// it magnifies instead, and the zoom trace is the deliberation\n"
                    "// record. native=1 always.")
dsec = dsec.replace('emit_result("D",', 'emit_result("INTAKE",')
dsec = dsec.replace('"D qid="', '"INTAKE qid="')
parts.append(dsec)
# summary: keep summ_add + skind_name, drop arm_name
summ = secs["summary"]
summ = summ[:summ.find("fn arm_name")]
parts.append("// ---------- summary helpers (harness use) ----------\n" + summ)
intake = "".join(parts)
intake = intake.replace("fn d_choose(", "fn tnn_choose(")
intake = intake.replace("fn d_why(", "fn tnn_why(")
intake = intake.replace("fn d_locate(", "fn tnn_locate(")
intake = intake.replace("d_choose(kind,t)", "tnn_choose(kind,t)")
intake = intake.replace("d_why(kind,c)", "tnn_why(kind,c)")
intake = intake.replace("d_locate(qid,q,t,", "tnn_locate(qid,q,t,")
intake = intake.replace('"D zoom qid="', '"INTAKE zoom qid="')
open(OUT + "/intake.zag", "w").write(intake)

# ---------- negcontrol.zag ----------
NC_IDS = ["w_u32le", "r_u32le", "ob_raw", "ob_i64", "ob_nl",
          "find_sub", "has_sub", "beq", "parse_digits",
          "enum_words", "scan_count", "count_words_bytes", "find_word",
          "reverse_into", "parse_target_letter", "parse_pos_n", "parse_after", "parse_between",
          "pack_stats", "emit_result",
          "c_answer", "w_answer", "s_answer"]
def prefix_code(code):
    # prefix whole-word occurrences of NC_IDS with nc_; also fix the
    # string tags "C"/"W"/"S" in emit_result calls -> "NC-C" etc.
    for i in sorted(NC_IDS, key=len, reverse=True):
        code = re.sub(r"\b" + i + r"\b", "nc_" + i, code)
    code = code.replace('emit_result("C",', 'emit_result("NC-C",')
    code = code.replace('emit_result("W",', 'emit_result("NC-W",')
    code = code.replace('emit_result("S",', 'emit_result("NC-S",')
    return code

nc_parts = [NC_HEADER]
for m in ["little-endian accessors", "output buffer"]:
    nc_parts.append(prefix_code(secs[m]))
# byte-string helpers: drop has_byte (unused by arms); keep rest
helpers = secs["byte-string helpers"]
helpers = helpers[:helpers.find("fn has_byte")] + helpers[helpers.find("fn beq"):]
nc_parts.append(prefix_code(helpers))
nc_parts.append(prefix_code(secs["chunk primitives"]))
# parse fns from question-kinds section (drop classify/kind_name/skind: hand-written below)
kinds = secs["question kinds"]
kinds_pre = kinds[:kinds.find("fn classify(")]
parse_fns = kinds[kinds.find("fn parse_target_letter"):]
nc_parts.append(prefix_code(kinds_pre))
nc_parts.append(prefix_code(parse_fns))
# handwritten extended classifier
nc_parts.append(r"""
// ---------- extended classifier (superset of the fork's) ----------
// New nested kinds 10-17 (Phase-2 traps). The frozen arms below have no
// branches for these kinds: they leave the answer empty and fail. That is
// the documented negative-control outcome — fixed arms cannot adapt to
// question forms they were not built for.
// Kinds: 1 LETTER_COUNT, 2 POSITION_N, 3 REVERSE, 4 WORD_COUNT, 5 LENGTH,
// 6 CONTAINS, 7 FIRST_WORD, 8 POS_FIRST, 9 POS_LAST,
// 10 LETTER_COUNT_WORD, 11 LENGTH_WORD, 12 POSITION_WORD, 13 REVERSE_WORD,
// 14 FIRST_LETTER_WORD, 15 LAST_LETTER_WORD, 16 LAST_WORD, 17 CONTAINS_WORD
fn nc_classify(q:[]u8) i64 {
    if (nc_has_sub(q,"how many words in")==1) { return 4; }
    if (nc_has_sub(q,"how many letters in")==1) {
        if (nc_has_sub(q," word of ")==1) { return 11; }
        return 5;
    }
    if (nc_has_sub(q,"'s in")==1) {
        if (nc_has_sub(q," word of ")==1) { return 10; }
        return 1;
    }
    if (nc_has_sub(q,"backwards")==1) {
        if (nc_has_sub(q," word of ")==1) { return 13; }
        return 3;
    }
    if (nc_has_sub(q,"first letter of the")==1) {
        if (nc_has_sub(q," word of ")==1) { return 14; }
    }
    if (nc_has_sub(q,"last letter of the")==1) {
        if (nc_has_sub(q," word of ")==1) { return 15; }
    }
    if (nc_has_sub(q,"first word of")==1) { return 7; }
    if (nc_has_sub(q," word of ")==1) {
        if (nc_has_sub(q,"contain ")==1) { return 17; }
    }
    if (nc_has_sub(q,"last word of")==1) { return 16; }
    if (nc_has_sub(q,"contain ")==1) { return 6; }
    if (nc_has_sub(q,"first letter of")==1) { return 8; }
    if (nc_has_sub(q,"last letter of")==1) { return 9; }
    if (nc_has_sub(q,"letter of")==1) {
        if (nc_has_sub(q," word of ")==1) { return 12; }
        return 2;
    }
    return 0;
}
fn nc_kind_name(k:i64) []u8 {
    if (k==1) { return "LETTER_COUNT"; }
    if (k==2) { return "POSITION"; }
    if (k==3) { return "REVERSE"; }
    if (k==4) { return "WORD_COUNT"; }
    if (k==5) { return "LENGTH"; }
    if (k==6) { return "CONTAINS"; }
    if (k==7) { return "FIRST_WORD"; }
    if (k==8) { return "POS_FIRST"; }
    if (k==9) { return "POS_LAST"; }
    if (k==10) { return "LETTER_COUNT_WORD"; }
    if (k==11) { return "LENGTH_WORD"; }
    if (k==12) { return "POSITION_WORD"; }
    if (k==13) { return "REVERSE_WORD"; }
    if (k==14) { return "FIRST_LETTER_WORD"; }
    if (k==15) { return "LAST_LETTER_WORD"; }
    if (k==16) { return "LAST_WORD"; }
    return "CONTAINS_WORD";
}
""")
nc_parts.append(prefix_code(secs["answer-line emitter"]))
for m in ["fixed arm C", "fixed arm W", "fixed arm S"]:
    arm = secs[m]
    # drop the section header comment lines, keep code; add frozen note
    arm = re.sub(r"// ---------- fixed arm.*?\n(//.*\n)+", "", arm, count=1)
    nc_parts.append("// RETIRED — negative control only. Frozen fork behavior.\n" + prefix_code(arm))
nc_src = "".join(nc_parts)
# strip unused w_i64le/r_i64le (would collide with intake.zag's; arms don't use them)
nc_src = re.sub(r"fn w_i64le\(b:\[\]u8, o:i64, v:i64\) void \{.*?\n\}\n", "", nc_src, flags=re.S)
nc_src = re.sub(r"fn r_i64le\(b:\[\]u8, o:i64\) i64 \{.*?\n\}\n", "", nc_src, flags=re.S)
open(OUT + "/negcontrol.zag", "w").write(nc_src)
print("wrote intake.zag (%d lines), negcontrol.zag (%d lines)" % (
    intake.count("\n"), "".join(nc_parts).count("\n")))
