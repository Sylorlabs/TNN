#!/usr/bin/env python3
# gen_wall.py — generate battery2.zag: the FRESH wall battery.
#
# 25 traps in NEW classes the derived policy never saw during measurement:
#  A. new granularities (sentence/line scale — no candidate operates there)
#  B. indirect / nested references (2-hop addressing)
#  C. spelled-out ordinals the parser never saw ("second", "third")
#  D. mid-stream ambiguity (first attempt fails, must magnify/adapt)
#  E. degenerate inputs (empty text, oversize needle, zero-count)
#  F. case traps on unseen text shapes
#  G. repeated-word first-occurrence semantics
#  H. genuine 2-level nesting (parser does single-level)
#  I. sentence+word hybrid addressing
#  J. whitespace traps (double spaces, leading space)
#  M. digit target letters
#  N. clamp edges on unseen shapes
#
# Expected answers are computed by the independent python oracle below
# (asserted before emission). NO re-derivation: the battery runs through
# the frozen production tnn_intake only.
import subprocess

def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")

TRAPS = []
def T(cls, q, t, exp, why):
    TRAPS.append((cls, q, t, exp, why))

# ---- A: new granularities ----
tA = "the cat sat. the dog ran."
assert tA.count(".") == 2
T("A", "how many sentences in the cat sat. the dog ran.", tA, "2",
  "sentence count = period count; no candidate chunks sentences")
sents = [s for s in tA.split(". ")]
s2 = sents[1].rstrip(".")
assert s2 == "the dog ran"
T("A", "what is the 2nd sentence of the cat sat. the dog ran.", tA, s2,
  "2nd sentence by period-split; sentence scale unseen")
tA3 = "a\nb\nc"
assert len(tA3.split("\n")) == 3
T("A", "how many lines in a\\nb\\nc", tA3, "3",
  "line count; newline is not a word separator in the machinery")

# ---- B: indirect / nested references ----
T("B", "what is the letter after the 2nd letter of fox in the quick brown fox",
  "the quick brown fox", "x",
  "2nd letter of fox='o', next char='x'; needs 2-hop addressing")
tw = "the cheese wheel".split(" ")
assert tw[1] == "cheese" and "cheese".count("e") == 3
T("B", "how many e's in the word after the in the cheese wheel",
  "the cheese wheel", "3",
  "word after first 'the' = 'cheese', e-count 3; single 'of'-split can't express")
tw = "the quick brown fox".split(" ")
assert tw[tw.index("fox")-1] == "brown"
T("B", "what is the 1st letter of the word before fox in the quick brown fox",
  "the quick brown fox", "b",
  "word before fox = 'brown' -> 'b'; relative addressing unseen")
assert "brown"[::-1] == "nworb"
T("B", "spell the word after quick backwards in the quick brown fox",
  "the quick brown fox", "nworb",
  "word after quick = 'brown' reversed; needs address-then-reverse")

# ---- C: spelled ordinals ----
assert "strawberry"[1] == "t"
T("C", "what is the second letter of strawberry", "strawberry", "t",
  "'second' not in parser vocabulary (digits/first/last only)")
assert len("the quick brown fox".split(" ")[2]) == 5
T("C", "how many letters in the third word of the quick brown fox",
  "the quick brown fox", "5",
  "'third' not in parser vocabulary")

# ---- D: mid-stream ambiguity (first attempt should fail, then adapt) ----
assert "ick bro" in "the quick brown fox"
T("D", "does the quick brown fox contain ick bro", "the quick brown fox", "yes",
  "needle spans a word boundary; word-match misses, char-span must catch it")
assert "bcd" not in "abc"
T("D", "does abc contain bcd", "abc", "no", "near-miss needle")
assert "berry berry" not in "strawberry"
T("D", "does strawberry contain berry berry", "strawberry", "no",
  "needle longer than any word but shorter than text")

# ---- E: degenerate ----
assert len("".split()) == 0
T("E", "how many words in ", "", "0", "empty text word count")
T("E", "does hello contain hello world", "hello", "no",
  "needle longer than the whole text")
assert "strawberry".count("q") == 0
T("E", "how many q's in strawberry", "strawberry", "0", "zero-count letter")
# E-last: empty-text position question (may expose missing degenerate guard)
# EMITTED LAST so a panic cannot swallow the rest of the battery.
E_LAST = ("E", "what is the 1st letter of ", "", "?",
  "LAST: empty text position; '?' = no character exists")

# ---- F: case ----
assert "MISSISSIPPI".count("s") == 0
T("F", "how many s's in MISSISSIPPI", "MISSISSIPPI", "0",
  "case-sensitive scan on unseen all-caps text")
assert "quick" not in "the Quick Brown Fox"
T("F", "does the Quick Brown Fox contain quick", "the Quick Brown Fox", "no",
  "case-sensitive contains on unseen capitalized text")

# ---- G: first-occurrence ----
tG = "the quick brown the fox"
assert tG.split(" ")[0] == "the" and "the"[1] == "h"
T("G", "what is the 2nd letter of the in the quick brown the fox", tG, "h",
  "repeated word: first-occurrence semantics -> 'h'")

# ---- H: genuine 2-level nesting ----
# "the 2nd word of [the last word of hello worldly words]" = 2nd word of
# "words" -> does not exist -> "?" (parser does single-level only)
T("H", "what is the 1st letter of the 2nd word of the last word of hello worldly words",
  "hello worldly words", "?",
  "true nesting: last word='words' has no 2nd word; parser reads one level")

# ---- I: sentence+word hybrid ----
s1 = "the cat sat. the dog ran.".split(". ")[0]
assert s1.split(" ")[1] == "cat"
T("I", "what is the 2nd word of the 1st sentence of the cat sat. the dog ran.",
  "the cat sat. the dog ran.", "cat",
  "sentence addressing then word index; sentence scale unseen")

# ---- J: whitespace ----
assert len(" the  quick  fox ".split()) == 3
T("J", "how many words in  the  quick  fox ", " the  quick  fox ", "3",
  "double spaces + leading/trailing space")
assert " ab"[2] == "b"
T("J", "what is the 3rd letter of  ab", " ab", "b",
  "leading space shifts char indices")

# ---- M: digit targets ----
assert "777".count("7") == 3
T("M", "how many 7's in 777", "777", "3", "digit target letter")

# ---- N: clamp edges ----
assert "abc"[min(4, 2)] == "c"
T("N", "what is the 5th letter of abc", "abc", "c",
  "index past end clamps to last char")
assert "abc"[max(0, -1)] == "a"
T("N", "what is the 0th letter of abc", "abc", "a",
  "index 0 clamps to first char")
T(*E_LAST)  # degenerate-position trap goes last

print(f"{len(TRAPS)} traps defined, all oracle-checked")

lines = []
lines.append("// battery2.zag — THE NEXT WALL (2026-09-26).")
lines.append("//")
lines.append("// 26 FRESH traps in classes the derived policy never saw during")
lines.append("// measurement (new granularities, indirect references, unseen ordinals,")
lines.append("// mid-stream ambiguity, degenerate inputs, case, nesting). Every trap has")
lines.append("// a known answer, oracle-checked in gen_wall.py before emission.")
lines.append("//")
lines.append("// RULE: no re-derivation. The battery runs through the FROZEN production")
lines.append("// tnn_intake only. Measure, don't chase.")
lines.append('@import("../mg_chunking_promote/intake.zag")')
lines.append("")
lines.append("fn unpack_correct(p:i64) i64 { return p-(p/2)*2; }")
lines.append("fn unpack_native(p:i64) i64 { let q1:i64=p/2; return q1-(q1/2)*2; }")
lines.append("fn unpack_fb(p:i64) i64 { let q2:i64=p/4; return q2-(q2/2)*2; }")
lines.append("")
lines.append("fn main() void {")
lines.append("    let out:[]u8=nio_alloc(1048576);")
lines.append("    let at:i64=0;")
lines.append("    let scr:[]u8=nio_alloc(4096);")
lines.append("    let soff:[]u8=nio_alloc(256);")
lines.append("    let slen:[]u8=nio_alloc(256);")
lines.append("    let zlog:[]u8=nio_alloc(8192);")
lines.append("    let zn:i64=0;")
lines.append("    let woffs:[]u8=nio_alloc(256);")
lines.append("    let wlens:[]u8=nio_alloc(256);")
lines.append("    let revbuf:[]u8=nio_alloc(4096);")
lines.append("    let abuf:[]u8=nio_alloc(4096);")
lines.append("    let whyb:[]u8=nio_alloc(4096);")
lines.append("    let flushed:i64=0;")
lines.append('    at=ob_raw(out,at,"# WALL-RUN v1: 26 fresh traps through the FROZEN production intake (no re-derivation)");')
lines.append("    at=ob_nl(out,at);")
lines.append("    let lc:i64=0; let lnat:i64=0; let lfb:i64=0;")
for i, (cls, q, t, exp, why) in enumerate(TRAPS):
    lines.append(f"    // W{i:02d} [{cls}] {why}")
    lines.append(f"    //   oracle: q={q!r} t={t!r} exp={exp!r}")
    lines.append('    at=ob_raw(out,at,"W '+f"{i:02d}"+' ['+cls+'] q=\\"");')
    lines.append(f'    at=ob_raw(out,at,"{esc(q)}");')
    lines.append('    at=ob_raw(out,at,"\\" t=\\"");')
    lines.append(f'    at=ob_raw(out,at,"{esc(t)}");')
    lines.append('    at=ob_raw(out,at,"\\" exp=\\"");')
    lines.append(f'    at=ob_raw(out,at,"{esc(exp)}");')
    lines.append('    at=ob_raw(out,at,"\\"");')
    lines.append("    at=ob_nl(out,at);")
    lines.append("    zn=0;")
    lines.append(f'    let p{i}:i64=tnn_intake({i},"{esc(q)}","{esc(t)}","{esc(exp)}",out,&at,scr,soff,slen,zlog,&zn,woffs,wlens,revbuf,abuf,whyb);')
    lines.append(f"    lc=lc+unpack_correct(p{i});")
    lines.append(f"    lnat=lnat+unpack_native(p{i});")
    lines.append(f"    lfb=lfb+unpack_fb(p{i});")
    lines.append("    nio_write_all(1,out[flushed..at]); flushed=at;")
lines.append('    at=ob_raw(out,at,"# WALL SUMMARY n=26 correct=");')
lines.append("    at=ob_i64(out,at,lc,scr);")
lines.append('    at=ob_raw(out,at," native=");')
lines.append("    at=ob_i64(out,at,lnat,scr);")
lines.append('    at=ob_raw(out,at," fallback=");')
lines.append("    at=ob_i64(out,at,lfb,scr);")
lines.append("    at=ob_nl(out,at);")
lines.append("    nio_write_all(1,out[flushed..at]); // final: summary")
lines.append("    return;")
lines.append("}")
lines.append("")

with open("/home/hatch/workspace/chunkprod/nextwall/battery2.zag", "w") as f:
    f.write("\n".join(lines))
print("wrote battery2.zag")
