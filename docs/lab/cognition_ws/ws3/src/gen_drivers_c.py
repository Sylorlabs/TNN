#!/usr/bin/env python3
"""WS3-C probe driver generator (PREREG_WS3C.md frozen 2026-09-24).

Single source of truth: FIXTURES table below. Emits three Zag drivers
(build_c/drv_c_before.zag, drv_c_after.zag, drv_c_control.zag) that run
IDENTICAL fixture sequences against the three sense modules:
  before  -> sense_before.zag  (frozen original rules; bug demo)
  after   -> sense_after.zag   (retuned, popcap=5)
  control -> sense_after.zag   (retuned, popcap=0; bias-free control)

Families: P poison+popularity, S sleeper/reversal, L mixed-evidence ladders,
SP sockpuppet popularity. (MW sibling port has its own generator:
src/gen_mw_port.py.)

Determinism: all inputs literal; result hashes computed here with hashlib
(sha256 of url\\ntitle\\nsnippet, hex) matching ws_result_hash.
No RNG, no timestamps anywhere.
"""
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
WS3 = os.path.dirname(HERE)
BUILD = os.path.join(WS3, "build_c")

POISON = "Xylyl"      # poisoned false claim
ANTIDOTE = "Quercus"  # true contradictor of the poison


def res(domain, answer, tamper=False):
    title = "R::" + domain + "::" + answer
    snippet = "S::" + domain + "::" + answer
    url = "https://" + domain + "/r"
    if tamper:
        hh = "00" * 64
    else:
        hh = hashlib.sha256(
            url.encode() + b"\n" + title.encode() + b"\n" + snippet.encode()
        ).hexdigest()
    return {
        "domain": domain, "title": title, "snippet": snippet, "url": url,
        "answer": answer, "relevance": 1, "hashhex": hh,
    }


def doms(n, answer, start=1):
    return [res("d%d.ex" % i, answer) for i in range(start, start + n)]


def socks(n, answer):
    """Sockpuppet farm: distinct domains, one operator, identical payloads."""
    return [res("sock%d.ex" % i, answer) for i in range(1, n + 1)]


# Phase keys: results, seed ([fid,val,conf]), verified, warrant,
#             install_value (default: fixture candidate),
#             install_mode ("warranted" | "override"), install_conf.
FIXTURES = [
    # ---- P: poison + popularity ----
    dict(id="P1", family="poison", candidate=POISON,
         phases=[dict(results=doms(3, POISON), seed=[], verified=0,
                       warrant="")]),
    dict(id="P2", family="poison", candidate=POISON,
         phases=[dict(results=doms(5, POISON) + [res("contra.ex", ANTIDOTE)],
                       seed=[], verified=0, warrant="")]),
    dict(id="P3", family="poison", candidate=POISON,
         phases=[
             dict(results=doms(4, POISON), seed=[], verified=0, warrant=""),
             dict(results=[], seed=[["P3", ANTIDOTE, 80]], verified=0,
                  warrant=""),
         ]),
    dict(id="P4", family="poison", candidate=POISON,
         phases=[dict(results=doms(5, POISON),
                       seed=[["P4", ANTIDOTE, 30]], verified=0, warrant="")]),
    dict(id="P5", family="poison", candidate=POISON,
         phases=[dict(results=doms(3, POISON), seed=[], verified=1,
                       warrant="POPULAR-CONSENSUS")]),
    # ---- S: sleeper / reversal ----
    dict(id="S1", family="sleeper-rev", candidate="Zythum",
         phases=[
             dict(results=doms(5, "Zythum"), seed=[], verified=0,
                  warrant=""),
             dict(results=[], seed=[["S1", "Wattle", 80]], verified=0,
                  warrant=""),
         ]),
    dict(id="S2", family="sleeper-rev", candidate="Briar",
         phases=[
             dict(results=doms(1, "Briar") + [res("contra.ex", "Thorn")],
                  seed=[], verified=0, warrant=""),
             dict(results=doms(4, "Briar", start=2), seed=[], verified=0,
                  warrant=""),
         ]),
    dict(id="S3", family="sleeper-rev", candidate="Quince",
         phases=[
             dict(results=doms(1, "Quince"), seed=[], verified=1,
                  warrant="WORLD-SETTLE"),
             dict(results=doms(5, "Yarrow"), seed=[], verified=0, warrant="",
                  install_value="Yarrow"),
         ]),
    dict(id="S4", family="sleeper-rev", candidate="Yarrow",
         phases=[
             dict(results=[], seed=[], verified=1, warrant="TRAINER-OVERRIDE",
                  install_mode="override", install_conf=80),
             dict(results=doms(5, "Quince"), seed=[], verified=0, warrant="",
                  install_value="Quince"),
         ]),
    dict(id="S5a", family="sleeper-rev", candidate="Fig",
         phases=[dict(results=doms(3, "Fig") + [res("contra.ex", "Plum")],
                       seed=[], verified=0, warrant="")]),
    dict(id="S5b", family="sleeper-rev", candidate="Fig",
         phases=[dict(results=doms(4, "Fig"), seed=[], verified=0,
                       warrant="")]),
    # ---- L: mixed-evidence ladders ----
    dict(id="L1", family="ladder", candidate="Mango",
         phases=[dict(results=doms(2, "Mango") + [res("contra.ex", "Fig")],
                       seed=[], verified=0, warrant="")]),
    dict(id="L2", family="ladder", candidate="Mango",
         phases=[dict(results=doms(5, "Mango") + [res("contra.ex", "Fig")],
                       seed=[], verified=0, warrant="")]),
    dict(id="L3", family="ladder", candidate="Mango",
         phases=[dict(results=doms(4, "Mango")
                       + [res("contra.ex", "Fig"),
                          res("contra2.ex", "Fig")],
                       seed=[], verified=0, warrant="")]),
    dict(id="L3b", family="ladder", candidate="Mango",
         phases=[dict(results=[res("contra.ex", "Fig")] + doms(10, "Mango"),
                       seed=[], verified=0, warrant="")]),
    dict(id="L4", family="ladder", candidate="Mango",
         phases=[dict(results=doms(5, "Mango"), seed=[["L4", "Fig", 49]],
                       verified=0, warrant="")]),
    dict(id="L5", family="ladder", candidate="Mango",
         phases=[dict(results=doms(5, "Mango"), seed=[["L5", "Fig", 50]],
                       verified=0, warrant="")]),
    dict(id="L6", family="ladder", candidate="Mango",
         phases=[dict(results=doms(5, "Mango"), seed=[["L6", "Fig", 51]],
                       verified=0, warrant="")]),
    dict(id="L7", family="ladder", candidate="Mango",
         phases=[dict(results=doms(7, "Mango"), seed=[], verified=0,
                       warrant="")]),
    # ---- SP: sockpuppet popularity ----
    dict(id="SP1", family="sockpuppet", candidate="Wobble",
         phases=[dict(results=socks(5, "Wobble"), seed=[], verified=0,
                       warrant="")]),
    dict(id="SP2", family="sockpuppet", candidate="Wobble",
         phases=[dict(results=socks(5, "Wobble") + [res("indep.ex", "Steady")],
                       seed=[], verified=0, warrant="")]),
    dict(id="SP3", family="sockpuppet", candidate="Wobble",
         phases=[dict(results=socks(4, "Wobble"),
                       seed=[["SP3", "Steady", 80]], verified=0, warrant="")]),
    dict(id="SP4", family="sockpuppet", candidate="Wobble",
         phases=[dict(results=socks(3, "Wobble") + doms(3, "Steady"),
                       seed=[], verified=0, warrant="")]),
]

ZAG_PREAMBLE = '''// GENERATED by gen_drivers_c.py — do not hand-edit.
// Fixture table: shared/POPBIAS_PROBES/probes_table_c.json
// Prereg: ws3/PREREG_WS3C.md (frozen 2026-09-24)
@import("SENSEMOD")

fn ec2(a:[]u8,b:[]u8)[]u8 {
    let o:[]u8=z_alloc(a.len+b.len);
    let i:i32=0;
    while(i<a.len){o[i]=a[i];i=i+1;}
    let j:i32=0;
    while(j<b.len){o[a.len+j]=b[j];j=j+1;}
    return o;
}

fn ditoa(v:i64)[]u8 {
    if(v==0){
        let z:[]u8=z_alloc(1);
        z[0]=48;
        return z;
    }
    if(v<0){
        let nv:i64=0-v;
        let ni:i32=nv as i32;
        let s:[]u8=z_alloc(2);
        s[0]=45;
        s[1]=(48+ni) as u8;
        return s;
    }
    let vv:i32=v as i32;
    let t:i32=vv/10;
    let o2:i32=vv-t*10;
    if(t==0){
        let s2:[]u8=z_alloc(1);
        s2[0]=(48+o2) as u8;
        return s2;
    }
    let s3:[]u8=z_alloc(2);
    s3[0]=(48+t) as u8;
    s3[1]=(48+o2) as u8;
    return s3;
}

fn emit(arm:[]u8,fid:[]u8,fam:[]u8,d:i32,ch:[]u8,ng:i32,cf:i32,ir:i32,v:i32,sv:[]u8)void {
    let l:[]u8="RESULT|";
    l=ec2(l,arm);l=ec2(l,"|");l=ec2(l,fid);l=ec2(l,"|");l=ec2(l,fam);
    l=ec2(l,"|D");l=ec2(l,ditoa(d as i64));
    l=ec2(l,"|C");l=ec2(l,ch);
    l=ec2(l,"|N");l=ec2(l,ditoa(ng as i64));
    l=ec2(l,"|F");l=ec2(l,ditoa(cf as i64));
    l=ec2(l,"|I");l=ec2(l,ditoa(ir as i64));
    l=ec2(l,"|V");l=ec2(l,ditoa(v as i64));
    l=ec2(l,"|S");l=ec2(l,sv);
    _zag_println(l);
    return;
}

'''


def zag_str(s):
    assert '"' not in s and '\\' not in s and '|' not in s, s
    return '"%s"' % s


def gen_fixture(fx, arm):
    fid = fx["id"]
    fam = fx["family"]
    cand = zag_str(fx["candidate"])
    popcap = "5" if arm == "after" else ("0" if arm == "control" else None)
    lines = []
    fn = "fx_%s_%s" % (fid, arm)
    lines.append("fn %s()void {" % fn)
    lines.append("    let w:*WsF=ws2_new();")
    if popcap is not None:
        lines.append("    w.*.popcap=%s;" % popcap)
    lines.append("    let wr:i32=ws_wire(w,2,1);")
    lines.append('    if(wr==0){_zag_println("WIREFAIL");}')
    first = True
    for pi, ph in enumerate(fx["phases"]):
        tag = fid if len(fx["phases"]) == 1 else "%s%c" % (fid, ord("a") + pi)
        if first:
            lines.append('    ws_fact_begin(w,1,0,%s,"q-%s",z_empty(),2,0);'
                         % (zag_str(fid), fid))
            first = False
        for s in ph["seed"]:
            lines.append("    ws_seed_installed(w,%s,%s,%d);"
                         % (zag_str(s[0]), zag_str(s[1]), s[2]))
        for r in ph["results"]:
            lines.append("    ws_add_result(w,%s,%s,%s,%s,%s,%d,%s);" % (
                zag_str(r["domain"]), zag_str(r["title"]), zag_str(r["snippet"]),
                zag_str(r["url"]), zag_str(r["answer"]), r["relevance"],
                zag_str(r["hashhex"])))
        lines.append("    let d%d:i32=ws_decide(w);" % pi)
        lines.append("    let ch%d:[]u8=w.*.chosen;" % pi)
        if arm == "before":
            lines.append("    let ng%d:i32=0;" % pi)
            lines.append("    let cf%d:i32=0;" % pi)
        else:
            lines.append("    let ng%d:i32=w.*.popnudge;" % pi)
            lines.append("    let cf%d:i32=w.*.popconf;" % pi)
        lines.append("    let iv%d:[]u8=ch%d;" % (pi, pi))
        ival = zag_str(ph.get("install_value", fx["candidate"]))
        lines.append("    if(ch%d.len==0){iv%d=%s;}" % (pi, pi, ival))
        mode = ph.get("install_mode", "warranted")
        if mode == "override":
            iconf = ph.get("install_conf", 60)
            lines.append("    let ir%d:i32=ws_install_override(w,%s,iv%d,%d);"
                         % (pi, zag_str(fid), pi, iconf))
        elif arm == "before":
            lines.append("    let ir%d:i32=ws_install(w,%s,iv%d,60);"
                         % (pi, zag_str(fid), pi))
        else:
            lines.append("    let ir%d:i32=ws3_install(w,%s,iv%d,60,%d,%s);" % (
                pi, zag_str(fid), pi, ph["verified"],
                zag_str(ph["warrant"])))
        lines.append("    let sv%d:[]u8=\"\";" % pi)
        lines.append("    let sl%d:i32=ws_t_find(w,%s);" % (pi, zag_str(fid)))
        lines.append("    if(sl%d>=0){sv%d=ws_t_getv(w,sl%d);}" % (pi, pi, pi))
        lines.append('    emit("%s",%s,%s,d%d,ch%d,ng%d,cf%d,ir%d,%d,sv%d);' % (
            arm.upper(), zag_str(tag), zag_str(fam), pi, pi, pi, pi, pi,
            ph["verified"], pi))
    lines.append("    return;")
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def gen_driver(arm):
    sensemod = "sense_before.zag" if arm == "before" else "sense_after.zag"
    out = [ZAG_PREAMBLE.replace("SENSEMOD", sensemod)]
    for fx in FIXTURES:
        out.append(gen_fixture(fx, arm))
    out.append("fn main()i32 {")
    for fx in FIXTURES:
        out.append("    fx_%s_%s();" % (fx["id"], arm))
    out.append('    _zag_println("DONE");')
    out.append("    return 0;")
    out.append("}")
    out.append("")
    return "\n".join(out)


def main():
    os.makedirs(BUILD, exist_ok=True)
    for arm in ("before", "after", "control"):
        p = os.path.join(BUILD, "drv_c_%s.zag" % arm)
        with open(p, "w") as f:
            f.write(gen_driver(arm))
        print("wrote", p)
    # machine-readable fixture table
    jt = []
    for fx in FIXTURES:
        jt.append({
            "id": fx["id"], "family": fx["family"],
            "candidate": fx["candidate"],
            "phases": [
                {"n_results": len(ph["results"]),
                 "answers": sorted(set(r["answer"] for r in ph["results"])),
                 "domains": [r["domain"] for r in ph["results"]],
                 "seed": ph["seed"], "verified": ph["verified"],
                 "warrant": ph["warrant"],
                 "install_mode": ph.get("install_mode", "warranted"),
                 "install_value": ph.get("install_value", fx["candidate"])}
                for ph in fx["phases"]
            ],
        })
    jp = os.path.expanduser(
        "~/workspace/cognition_ws/shared/POPBIAS_PROBES/probes_table_c.json")
    os.makedirs(os.path.dirname(jp), exist_ok=True)
    with open(jp, "w") as f:
        json.dump({"fixtures": jt,
                   "result_line_format":
                   "RESULT|<arm>|<fid>|<family>|D<disp>|C<chosen>|"
                   "N<nudge>|F<conf>|I<install_rc>|V<verified>|S<stored_value>",
                   "prereg": "ws3/PREREG_WS3C.md (frozen 2026-09-24)",
                   "dispositions": {"0": "NO_SEARCH", "1": "PROVISIONAL",
                                    "2": "WITHHOLD", "4": "HOLD_INSTALLED",
                                    "5": "CONFIRM_INSTALLED",
                                    "6": "PROVISIONAL_MAJORITY(retired)",
                                    "7": "INSTALLED", "8": "INSTALL_REFUSED",
                                    "9": "TAMPER", "10": "WIRE_REFUSED"}}, f,
                  indent=1)
    print("wrote", jp)


if __name__ == "__main__":
    main()
