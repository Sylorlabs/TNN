#!/usr/bin/env python3
"""Generate the three V-QUAR instrument sources from the frozen webg.zag.

Deterministic textual edits, fully reviewable via diff:
  webg_prod.zag  = frozen + read-audit instrumentation (BINID=PROD)
  webg_train.zag = frozen + read-audit (BINID=TRAIN) + V-PARA quarantine path
  webg_merge.zag = frozen + read-audit (BINID=MERGE) + merge gate + qread_claim

Edits (applied in order):
  E1. Insert qa_audit.inc after the @import line (@BINID@ substituted).
  E2. Rename frozen `fn read_file(` -> `fn qraw_read_file(`,
      frozen `fn read_path(` -> `fn qraw_read_path(` (definitions only; call sites
      now resolve to the instrumented wrappers in qa_audit.inc).
  E3. (TRAIN) Insert qa_para.inc after the audit block; hook cmd_verdict so
      qp_quarantine runs iff the strict verdict did not install.
  E4. (MERGE) Insert qa_merge.inc after the audit block; add the `merge`
      command branch to main().
"""
import sys

FROZEN = "/home/hatch/workspace/scratch-li-forkbase/webg.zag"
HERE = "/home/hatch/workspace/scratch-li-f3/vquar"

IMPORT_LINE = '@import("R33_NATIVE_IO_V1.zag")'

VERDICT_HOOK_OLD = """    verdict_core(buf,np,pa,pt,tt,st,nst,query,kind,extra,kwstr,dt,dn,0,1,
        o_ans,&o_ansn,o_widx,&o_wn,&o_provs,&o_claims,o_fl,&o_fln);
    nio_free(kwstr);"""
VERDICT_HOOK_NEW = """    let vrc:i32=verdict_core(buf,np,pa,pt,tt,st,nst,query,kind,extra,kwstr,dt,dn,0,1,
        o_ans,&o_ansn,o_widx,&o_wn,&o_provs,&o_claims,o_fl,&o_fln);
    if(vrc==0){
        qp_quarantine(buf,np,pa,pt,st,nst,query,o_fl,o_fln,sd);
    }
    nio_free(kwstr);"""

MERGE_BRANCH_OLD = """        return cmd_verdict(sd4,nfp,pp,kd,qy,ex2);
    }
    return 2;
}"""
MERGE_BRANCH_NEW = """        return cmd_verdict(sd4,nfp,pp,kd,qy,ex2);
    }
    if(nio_equal(m,"merge")==1){
        let sd5:[]u8=_zag_arg(2);
        let nfp5:[]u8=_zag_arg(3);
        let pp5:[]u8=_zag_arg(4);
        let cp5:[]u8=_zag_arg(5);
        let qid5:[]u8=_zag_arg(6);
        if(sd5.len==0 || pp5.len==0 || cp5.len==0 || qid5.len==0){return 2;}
        return cmd_merge(sd5,nfp5,pp5,cp5,qid5);
    }
    return 2;
}"""


def extract_fn(src, name):
    """Extract a top-level `fn name(` ... matching-`}` block; returns
    (block, src_without_block)."""
    start = src.index("fn " + name + "(")
    i = src.index("{", start)
    depth = 0
    j = i
    while True:
        if src[j] == "{":
            depth += 1
        elif src[j] == "}":
            depth -= 1
            if depth == 0:
                break
        j += 1
    block = src[start:j + 1]
    rest = src[:start] + src[j + 1:]
    return block, rest


def build(binid, extra_inc=None):
    src = open(FROZEN).read()
    # E2: rename the frozen raw-reader definitions and MOVE them to just
    # after the @import line, before any wrapper/accessor that calls them.
    # (znc miscompiles the forward reference qread_claim -> read_path0 in
    # the full-size binary: the call lands in the wrapper instead.)
    assert src.count("fn read_file(") == 1, src.count("fn read_file(")
    assert src.count("fn read_path(") == 1, src.count("fn read_path(")
    raw_file, src = extract_fn(src, "read_file")
    raw_path, src = extract_fn(src, "read_path")
    raw_file = raw_file.replace("fn read_file(", "fn qraw_read_file(", 1)
    raw_path = raw_path.replace("fn read_path(", "fn qraw_read_path(", 1)
    # The raw readers must call EACH OTHER raw, not via the wrappers:
    # qraw_read_path's body calls read_file(...) -> must be qraw_read_file.
    # (All other frozen call sites intentionally resolve to the wrappers.)
    raw_path = raw_path.replace("read_file(", "qraw_read_file(")
    raw_file = raw_file.replace("read_path(", "qraw_read_path(")
    # E1: insert raw readers + audit instrumentation after the @import line.
    audit = open(HERE + "/qa_audit.inc").read().replace("@BINID@", binid)
    assert src.count(IMPORT_LINE) == 1
    src = src.replace(IMPORT_LINE,
                      IMPORT_LINE + "\n" + raw_file + "\n\n" + raw_path + "\n" + audit, 1)
    if extra_inc:
        inc = open(HERE + "/" + extra_inc).read()
        # insert after the end of the audit include = end of the second
        # wrapper (read_path); anchor on its closing lines.
        anchor = "    return b;\n}\n"
        pos = src.index(IMPORT_LINE) + len(IMPORT_LINE)
        first = src.index(anchor, pos) + len(anchor)
        second = src.index(anchor, first) + len(anchor)
        src = src[:second] + "\n" + inc + src[second:]
    if binid == "TRAIN":
        assert src.count(VERDICT_HOOK_OLD) == 1
        src = src.replace(VERDICT_HOOK_OLD, VERDICT_HOOK_NEW, 1)
    if binid == "MERGE":
        assert src.count(MERGE_BRANCH_OLD) == 1
        src = src.replace(MERGE_BRANCH_OLD, MERGE_BRANCH_NEW, 1)
    return src


def main():
    plans = [("PROD", "webg_prod.zag", None),
             ("TRAIN", "webg_train.zag", "qa_para.inc"),
             ("MERGE", "webg_merge.zag", "qa_merge.inc")]
    for binid, fname, inc in plans:
        out = build(binid, inc)
        with open(HERE + "/" + fname, "w") as f:
            f.write(out)
        print("wrote", fname, len(out), "bytes")


if __name__ == "__main__":
    main()
