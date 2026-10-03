#!/usr/bin/env python3
"""Surgical edits turning sense_h2.zag into sense_r24.zag:
- import gcheck.zag
- per task fn: accept (gbuf, gn), run the independent-evidence self check,
  prog = self-result, progF = F-verdict (diagnostic), pred = (self==PASS),
  judgment = F verdict (no runner-up flip), program=R2-4/...
- main: split R24A dual-span fixtures; legacy single-span -> G absent.
"""
import re, sys

P = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/forks/R2-4/src/sense_r24.zag"
src = open(P).read()

def rep(old, new, count=1):
    global src
    n = src.count(old)
    assert n == count, "expected %d of %r, found %d" % (count, old[:60], n)
    src = src.replace(old, new)

# 1. import + header
rep('@import("lut.zag")', '@import("lut.zag")\n@import("gcheck.zag")')
rep("// sense_h2.zag — PAM fork H2: EXECUTABLE PERCEPT PROGRAMS.",
    "// sense_r24.zag — PAM fork R2-4: EXECUTABLE PERCEPT PROGRAMS + self-flag.")
rep("// CLI: sense_h2 <task> <fixture-path>   (same fixture formats as INTERFACE.md)",
    "// CLI: sense_r24 <task> <fixture-path>  (R24A dual-span or legacy formats)")
rep('pos = ob_kv(ob, pos, "approach", "H2");',
    'pos = ob_kv(ob, pos, "approach", "R2-4");', count=2)  # main + fail

# 2. signatures
rep("fn task_colordisc(buf:[]u8, n:i32, ob:[]u8, pos:i32, op:[]u8, lut:[]u8) i32 {",
    "fn task_colordisc(buf:[]u8, n:i32, ob:[]u8, pos:i32, op:[]u8, lut:[]u8, gbuf:[]u8, gn:i32) i32 {")
rep("fn task_colorconst(buf:[]u8, n:i32, ob:[]u8, pos:i32, op:[]u8, lut:[]u8) i32 {",
    "fn task_colorconst(buf:[]u8, n:i32, ob:[]u8, pos:i32, op:[]u8, lut:[]u8, gbuf:[]u8, gn:i32) i32 {")
for fn in ["task_shapetrans", "task_motiondir", "task_pitchdisc", "task_timbredisc"]:
    rep("fn %s(buf:[]u8, n:i32, ob:[]u8, pos:i32, op:[]u8) i32 {" % fn,
        "fn %s(buf:[]u8, n:i32, ob:[]u8, pos:i32, op:[]u8, gbuf:[]u8, gn:i32) i32 {" % fn)

# 3. remove runner-up flips: judgment = F verdict, always
rep("    let judge:i64 = hh;\n    if(r == 1) { judge = 1 - hh; }",
    "    let judge:i64 = hh;", count=2)  # colordisc, colorconst
rep("    if(r == 1) { judge = shape_runner(ravg, hh); }", "    // R2-4: no runner-up flip; judgment stays the F verdict")
rep("    let judge:i64 = hh;\n    if(r == 1) {\n        judge = 0;\n        if(dA != hh) { judge = dA; }\n        else {\n            if(dB != hh) { judge = dB; }\n        }\n    }",
    "    let judge:i64 = hh;  // R2-4: no span-vote override; judgment stays the F verdict")
rep("    if(r == 1) { judge = pitch_runner(d, fA, fB, hh); }", "    // R2-4: no runner-up flip; judgment stays the F verdict")
rep("    if(r == 1) { judge = timbre_runner(r12, hh); }", "    // R2-4: no runner-up flip; judgment stays the F verdict")

# 4. gcheck call blocks, one per task fn, inserted after resolve()
def gblock(call, evtext):
    return ("    let r:i32 = resolve(t1, t2d, t2c, t3, p1);\n"
            "    // R2-4 independent-evidence self check on the disjoint G span\n"
            "    let gev:[]u8 = nio_alloc(32);\n"
            "    let sres:i32 = 2;\n"
            "    let gt1:i64 = 0;\n"
            "    let gag:i64 = 0;\n"
            "    let gst:i64 = 0;\n"
            "    let gmv:i64 = 0;\n"
            "    if(gev.len != 0 && gn > 0) {\n"
            "        sres = " + call + ";\n"
            "        gt1 = t_get64(gev, 0);\n"
            "        gag = t_get64(gev, 8);\n"
            "        gst = t_get64(gev, 16);\n"
            "        gmv = t_get64(gev, 24);\n"
            "    }\n"
            "    nio_free(gev);\n"
            "    let gpred:i64 = 0;\n"
            "    if(sres == 0) { gpred = 1; }\n")

calls = {
    "colordisc":  "gcheck_colordisc(gbuf, gn, hh, op, lut, gev)",
    "colorconst": "gcheck_colorconst(gbuf, gn, hh, op, gev)",
    "shapetrans": "gcheck_shape(gbuf, gn, hh, op, gev)",
    "motiondir":  "gcheck_motion(gbuf, gn, hh, op, gev)",
    "pitchdisc":  "gcheck_pitch(gbuf, gn, fA, fB, hh, sr, op, gev)",
    "timbredisc": "gcheck_timbre(gbuf, gn, f0, hh, sr, op, gev)",
}
# insert into each task fn body: find its resolve line and expand
for fn, call in calls.items():
    m = re.search(r"(fn task_%s\(.*?^})" % fn, src, re.M | re.S)
    assert m, fn
    body = m.group(1)
    old = "    let r:i32 = resolve(t1, t2d, t2c, t3, p1);\n"
    assert body.count(old) == 1, fn
    body = body.replace(old, gblock(call, ""))
    src = src.replace(m.group(1), body)

# 5. emit: prog=self-result, add progF, pred=gpred
rep('pos = ob_kv(ob, pos, "prog", res_str(r));',
    'pos = ob_kv(ob, pos, "prog", res_str(sres));\n    pos = ob_kv(ob, pos, "progF", res_str(r));', count=6)
rep('pos = ob_kint(ob, pos, "pred", p1 as i64);',
    'pos = ob_kint(ob, pos, "pred", gpred);', count=6)

# 6. program= rename + G evidence + self_result before |result=
rep("program=H2/colordisc", "program=R2-4/colordisc")
rep("program=H2/colorconst", "program=R2-4/colorconst")
rep("program=H2/shapetrans", "program=R2-4/shapetrans")
rep("program=H2/motiondir", "program=R2-4/motiondir")
rep("program=H2/pitchdisc", "program=R2-4/pitchdisc")
rep("program=H2/timbredisc", "program=R2-4/timbredisc")

evtexts = {
    "colordisc":  '|G=selfcheck:de=',
    "colorconst": '|G=selfcheck:dist=',
    "shapetrans": '|G=selfcheck:mrg=',
    "motiondir":  '|G=selfcheck:mag=',
    "pitchdisc":  '|G=selfcheck:mratio=',
    "timbredisc": '|G=selfcheck:cent=',
}
for fn, tag in evtexts.items():
    m = re.search(r"(fn task_%s\(.*?^})" % fn, src, re.M | re.S)
    body = m.group(1)
    old = '    pos = ob_add(ob, pos, "|result=");\n'
    assert body.count(old) == 1, fn
    if fn == "colordisc":
        mval = '_zag_i64_to_str((gmv + 50) / 100)'
    else:
        mval = '_zag_i64_to_str(gmv)'
    new = ('    pos = ob_add(ob, pos, "' + tag + '");\n'
           '    pos = ob_add(ob, pos, ' + mval + ');\n'
           '    pos = ob_add(ob, pos, ",t1=");\n'
           '    pos = ob_add(ob, pos, _zag_i64_to_str(gt1));\n'
           '    pos = ob_add(ob, pos, ",agree=");\n'
           '    pos = ob_add(ob, pos, _zag_i64_to_str(gag));\n'
           '    pos = ob_add(ob, pos, ",strong=");\n'
           '    pos = ob_add(ob, pos, _zag_i64_to_str(gst));\n'
           '    pos = ob_add(ob, pos, "|self_result=");\n'
           '    pos = ob_add(ob, pos, res_str(sres));\n'
           '    pos = ob_add(ob, pos, "|result=");\n')
    body = body.replace(old, new)
    src = src.replace(m.group(1), body)

open(P, "w").write(src)
print("edits ok")

# 7. main(): split R24A dual-span fixtures; legacy single-span -> G absent
src = open(P).read()
old_main = '''    let ob:[]u8 = nio_alloc(4096);
    let pos:i32 = 0;
    pos = ob_kv(ob, pos, "approach", "R2-4");
    pos = ob_kv(ob, pos, "task", task);
    let rc:i32 = -1;
    if(_zag_strcmp(task, "colordisc") == 1) { rc = task_colordisc(buf, n as i32, ob, pos, op, lut); }
    if(_zag_strcmp(task, "colorconst") == 1) { rc = task_colorconst(buf, n as i32, ob, pos, op, lut); }
    if(_zag_strcmp(task, "shapetrans") == 1) { rc = task_shapetrans(buf, n as i32, ob, pos, op); }
    if(_zag_strcmp(task, "pitchdisc") == 1) { rc = task_pitchdisc(buf, n as i32, ob, pos, op); }
    if(_zag_strcmp(task, "timbredisc") == 1) { rc = task_timbredisc(buf, n as i32, ob, pos, op); }
    if(_zag_strcmp(task, "motiondir") == 1) { rc = task_motiondir(buf, n as i32, ob, pos, op); }
    nio_free(buf);'''
new_main = '''    let ob:[]u8 = nio_alloc(8192);
    let pos:i32 = 0;
    pos = ob_kv(ob, pos, "approach", "R2-4");
    pos = ob_kv(ob, pos, "task", task);
    // R24A dual-span split: F = verdict span, G = disjoint holdout span.
    // Legacy single-span fixtures: G absent -> self-result UNRESOLVED.
    let fbuf:[]u8 = buf[0..n as i32];
    let fnn:i32 = n as i32;
    let gbuf:[]u8 = buf[0..0];
    let gn:i32 = 0;
    if(n >= 8 && t_get32(buf, 0) == 1093939794) {
        let flen:i64 = r24_flen(buf, n);
        if(flen <= 0 || 8 + flen > n || r24_tcode(task) != t_get32(buf, 4)) {
            nio_free(buf);
            nio_free(lut);
            return fail(task, "bad-r24a");
        }
        fbuf = buf[8..(8 + flen) as i32];
        fnn = flen as i32;
        gbuf = buf[(8 + flen) as i32..n as i32];
        gn = (n - 8 - flen) as i32;
    }
    let rc:i32 = -1;
    if(_zag_strcmp(task, "colordisc") == 1) { rc = task_colordisc(fbuf, fnn, ob, pos, op, lut, gbuf, gn); }
    if(_zag_strcmp(task, "colorconst") == 1) { rc = task_colorconst(fbuf, fnn, ob, pos, op, lut, gbuf, gn); }
    if(_zag_strcmp(task, "shapetrans") == 1) { rc = task_shapetrans(fbuf, fnn, ob, pos, op, gbuf, gn); }
    if(_zag_strcmp(task, "pitchdisc") == 1) { rc = task_pitchdisc(fbuf, fnn, ob, pos, op, gbuf, gn); }
    if(_zag_strcmp(task, "timbredisc") == 1) { rc = task_timbredisc(fbuf, fnn, ob, pos, op, gbuf, gn); }
    if(_zag_strcmp(task, "motiondir") == 1) { rc = task_motiondir(fbuf, fnn, ob, pos, op, gbuf, gn); }
    nio_free(buf);'''
assert src.count(old_main) == 1
src = src.replace(old_main, new_main)
open(P, "w").write(src)
print("main ok")
