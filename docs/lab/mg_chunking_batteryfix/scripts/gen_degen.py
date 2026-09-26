#!/usr/bin/env python3
"""Generate run/battery3.zag — the permanent degenerate-input regression battery.
41 cases per PREREG_DEGEN.md. Modelled on battery2.zag's structure."""
import os

CASES = [
    # (tag, question, text, exp)
    ("D00", "how many e's in ", "", "0"),
    ("D01", "what is the 1st letter of ", "", "?"),
    ("D02", "write  backwards", "", ""),
    ("D03", "how many words in ", "", "0"),
    ("D04", "how many letters in ", "", "0"),
    ("D05", "does  contain z", "", "no"),
    ("D06", "what is the first word of ", "", "?"),
    ("D07", "what is the first letter of ", "", "?"),
    ("D08", "what is the last letter of ", "", "?"),
    ("D09", "how many e's in the word after the in ", "", "?"),
    ("D10", "how many letters in the word after the in ", "", "?"),
    ("D11", "what is the 1st letter of the word after the in ", "", "?"),
    ("D12", "write the word after quick backwards in ", "", "?"),
    ("D13", "what is the first letter of the word after the in ", "", "?"),
    ("D14", "what is the last letter of the word after the in ", "", "?"),
    ("D15", "what is the last word of ", "", "?"),
    ("D16", "does the word after the contain z in ", "", "?"),
    ("D17", "how many sentences in ", "", "0"),
    ("D18", "what is the 1st sentence of ", "", "?"),
    ("D19", "what is the 2nd word of the 1st sentence of ", "", "?"),
    ("D20", "what is the letter after the 2nd letter of fox in ", "", "?"),
    ("D21", "what is the 1st letter of the 2nd word of the last word of ", "", "?"),
    ("D22", "ponder the void", "", ""),
    ("D23", "what is the 1st letter of x", "x", "x"),
    ("D24", "what is the 5th letter of x", "x", "x"),
    ("D25", "what is the last letter of x", "x", "x"),
    ("D26", "how many e's in x", "x", "0"),
    ("D27", "write x backwards", "x", "x"),
    ("D28", "how many words in    ", "   ", "0"),
    ("D29", "what is the 1st letter of    ", "   ", " "),
    ("D30", "what is the first word of    ", "   ", ""),
    ("D31", "what is the 99th letter of abc", "abc", "c"),
    ("D32", "what is the 0th letter of abc", "abc", "a"),
    ("D33", "what is the 1st letter of the last word of abc", "abc", "a"),
    ("D34", "what is the 2nd letter of the last word of ", "", "?"),
    ("D35", "", "abc", ""),
    ("D36", "how many lines in \n", "\n", "0"),
    ("D37", "how many sentences in a", "a", "1"),
    ("D38", "what is the first word of  ", " ", ""),
    ("D39", "what is the 100th word of the 1st sentence of abc", "abc", "?"),
    ("D40", "what is the -1th letter of abc", "abc", "a"),
]
assert len(CASES) == 41, len(CASES)

def zsrc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")

def zdisp(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\\\n")

L = []
L.append("// battery3.zag — DEGENERATE-INPUT regression battery (2026-09-26).")
L.append("// 41 degenerate cases per PREREG_DEGEN.md: empty text x every kind,")
L.append("// single-char text, all-whitespace text, past-end/zero/negative")
L.append("// positions, empty question. Bar: answer or refuse cleanly, no panics.")
L.append("// Runs through the production tnn_intake only, like battery1/2.")
L.append('@import("./intake.zag")')
L.append("")
L.append("fn unpack_correct(p:i64) i64 { return p-(p/2)*2; }")
L.append("fn unpack_native(p:i64) i64 { let q1:i64=p/2; return q1-(q1/2)*2; }")
L.append("fn unpack_fb(p:i64) i64 { let q2:i64=p/4; return q2-(q2/2)*2; }")
L.append("")
L.append("fn main() void {")
L.append('    let out:[]u8=nio_alloc(1048576);')
L.append('    let at:i64=0;')
L.append('    let scr:[]u8=nio_alloc(4096);')
L.append('    let soff:[]u8=nio_alloc(256);')
L.append('    let slen:[]u8=nio_alloc(256);')
L.append('    let zlog:[]u8=nio_alloc(8192);')
L.append('    let zn:i64=0;')
L.append('    let woffs:[]u8=nio_alloc(256);')
L.append('    let wlens:[]u8=nio_alloc(256);')
L.append('    let revbuf:[]u8=nio_alloc(4096);')
L.append('    let abuf:[]u8=nio_alloc(4096);')
L.append('    let know:[]u8=nio_alloc(2048);')
L.append('    know_init(know);')
L.append('    tnn_place_knowledge(know);')
L.append('    let whyb:[]u8=nio_alloc(4096);')
L.append('    let flushed:i64=0;')
L.append('    at=ob_raw(out,at,"# DEGEN-RUN v1: 41 degenerate cases through the production intake");')
L.append('    at=ob_nl(out,at);')
L.append('    let lc:i64=0; let lnat:i64=0; let lfb:i64=0;')
for i, (tag, q, t, exp) in enumerate(CASES):
    L.append(f'    // {tag}: q={q!r} t={t!r} exp={exp!r}')
    L.append(f'    at=ob_raw(out,at,"W {i:02d} [{tag}] q=\\"");')
    L.append(f'    at=ob_raw(out,at,"{zdisp(q)}");')
    L.append(f'    at=ob_raw(out,at,"\\" t=\\"");')
    L.append(f'    at=ob_raw(out,at,"{zdisp(t)}");')
    L.append(f'    at=ob_raw(out,at,"\\" exp=\\"");')
    L.append(f'    at=ob_raw(out,at,"{zdisp(exp)}");')
    L.append(f'    at=ob_raw(out,at,"\\"");')
    L.append(f'    at=ob_nl(out,at);')
    L.append(f'    zn=0;')
    L.append(f'    let p{i}:i64=tnn_intake({i},"{zsrc(q)}","{zsrc(t)}","{zsrc(exp)}",out,&at,scr,soff,slen,zlog,&zn,woffs,wlens,revbuf,abuf,whyb,know);')
    L.append(f'    lc=lc+unpack_correct(p{i});')
    L.append(f'    lnat=lnat+unpack_native(p{i});')
    L.append(f'    lfb=lfb+unpack_fb(p{i});')
    L.append(f'    nio_write_all(1,out[flushed..at]); flushed=at;')
L.append('    at=ob_raw(out,at,"# DEGEN SUMMARY correct=");')
L.append('    at=ob_i64(out,at,lc,scr);')
L.append('    at=ob_raw(out,at," native=");')
L.append('    at=ob_i64(out,at,lnat,scr);')
L.append('    at=ob_raw(out,at," fallback=");')
L.append('    at=ob_i64(out,at,lfb,scr);')
L.append('    at=ob_nl(out,at);')
L.append('    nio_write_all(1,out[flushed..at]); flushed=at;')
L.append('}')

out = os.path.expanduser("~/workspace/batteryfix/run/battery3.zag")
with open(out, "w") as f:
    f.write("\n".join(L) + "\n")
print(f"wrote {out} ({len(CASES)} cases)")
