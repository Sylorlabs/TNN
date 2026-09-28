#!/usr/bin/env python3
"""Build task4/src/learner4.zag from loop/learner.zag + KB store fns.

learner4 = the tested loop learner (teach/gen/diagnose/gate/delib + all
patch machinery, verbatim) PLUS a store-driven battery generation path:
  gen <kb.dat> <spec>        (battery tier B1..B5 -> kb recall + slot fill)
  diagnose <kb.dat> <spec> <src> <evtype> <evidence>
"""
import os

WS = os.path.expanduser("~/workspace/tnn-lab")
SRC = os.path.join(WS, "coding/reflection/loop/learner.zag")
DST = os.path.join(WS, "coding/reflection/task4/src/learner4.zag")

KB_SECTION = r'''
// ============ KB store (task-4 battery recall) ============
// Store-driven generation: load kb.dat, score E-* entries against the
// spec description, fill {{slots}} from spec kv, emit the entry body.
// All coding decisions (which entry, which slot values) are made here,
// in the Zag learner. Emits KB-MISS:<reason> sentinels, never guesses.

fn kb_put64(b:[]u8, o:i64, v:i64)void {
    let i:i64=0;
    while(i<8){
        let sh:i64=i*8;
        b[o+i]=((v>>sh)&255) as u8;
        i=i+1;
    }
    return;
}

fn kb_get64(b:[]u8, o:i64)i64 {
    let v:i64=0;
    let k:i64=0;
    while(k<8){
        v=v|(((b[o+k] as i64)&255)<<(k*8));
        k=k+1;
    }
    return v;
}

fn fnv1a(data:[]u8)i64 {
    let h:i64=-3750763034362895579;
    let p:i64=1099511628211;
    let i:i64=0;
    while(i<data.len){
        h=h^(data[i] as i64);
        h=h*p;
        i=i+1;
    }
    return h;
}

fn e_hex(cx:*Cx, v:i64)void {
    let digits:[]u8="0123456789abcdef";
    let k:i64=0;
    while(k<16){
        let sh:i64=(15-k)*4;
        let nib:i64=(v>>sh)&15;
        e_ch(cx,digits[nib]);
        k=k+1;
    }
    return;
}

fn path_cstr(s:[]u8)*u8 {
    let p:*u8=_zag_malloc(s.len+1) as *u8;
    let i:i64=0;
    while(i<s.len){
        p[i]=s[i];
        i=i+1;
    }
    p[s.len]=0;
    return p;
}

fn read_all(path:[]u8, mem:*u8, cap:i64)i64 {
    let pp:*u8=path_cstr(path);
    let fd:i64=_zag_raw_syscall(2, pp as i64, 0, 0, 0, 0, 0);
    if(fd<0){return -1;}
    let total:i64=0;
    while(1==1){
        if(total>=cap){break;}
        let want:i64=cap-total;
        if(want>65536){want=65536;}
        let r:i64=_zag_raw_syscall(0, fd, (mem as i64)+total, want, 0, 0, 0);
        if(r<=0){break;}
        total=total+r;
    }
    let c:i64=_zag_raw_syscall(3, fd, 0, 0, 0, 0, 0);
    return total;
}

fn kb_et_get(tab:[]u8, e:i64, f:i64)i64 {
    return kb_get64(tab,e*64+f*8);
}

fn kb_parse(mem:*u8, n:i64, tab:[]u8) i64 {
    let img:[]u8=mem[0..n];
    if(n<13){return -1;}
    if(img[0]!=75){return -1;}
    if(img[1]!=66){return -1;}
    if(img[2]!=48){return -1;}
    if(img[3]!=49){return -1;}
    if(img[4]!=10){return -1;}
    let ec:i64=kb_get64(img,5);
    if(ec>256){return -1;}
    let off:i64=13;
    let e:i64=0;
    while(e<ec){
        let f:i64=0;
        while(f<4){
            let fl:i64=kb_get64(img,off);
            off=off+8;
            kb_put64(tab,e*64+f*2*8,off);
            kb_put64(tab,e*64+(f*2+1)*8,fl);
            off=off+fl;
            f=f+1;
        }
        e=e+1;
    }
    return ec;
}

fn kb_entry_id(tab:[]u8, img:[]u8, e:i64)[]u8 {
    let o:i64=kb_et_get(tab,e,0);
    let l:i64=kb_et_get(tab,e,1);
    return img[o..o+l];
}

fn kb_entry_kw(tab:[]u8, img:[]u8, e:i64)[]u8 {
    let o:i64=kb_et_get(tab,e,4);
    let l:i64=kb_et_get(tab,e,5);
    return img[o..o+l];
}

fn kb_entry_body(tab:[]u8, img:[]u8, e:i64)[]u8 {
    let o:i64=kb_et_get(tab,e,6);
    let l:i64=kb_et_get(tab,e,7);
    return img[o..o+l];
}

fn kb_find_entry(tab:[]u8, img:[]u8, ec:i64, id:[]u8)i64 {
    let e:i64=0;
    while(e<ec){
        if(s_eq(kb_entry_id(tab,img,e),id)==1){return e;}
        e=e+1;
    }
    return -1;
}

fn kb_entry_score(tab:[]u8, img:[]u8, e:i64, lowered:[]u8)i64 {
    let kw:[]u8=kb_entry_kw(tab,img,e);
    let score:i64=0;
    let ts:i64=0;
    while(ts<kw.len){
        let te:i64=ts;
        while(te<kw.len){
            if(kw[te]==44){break;}
            te=te+1;
        }
        let a:i64=ts;
        let b:i64=te;
        while(a<b){
            if(kw[a]!=32){break;}
            a=a+1;
        }
        while(b>a){
            if(kw[b-1]!=32){break;}
            b=b-1;
        }
        if(b>a){
            let term:[]u8=kw[a..b];
            if(s_find(lowered,term,0)>=0){score=score+1;}
        }
        ts=te+1;
    }
    return score;
}

fn kb_is_family(id:[]u8)i64 {
    if(id.len<2){return 0;}
    if(id[0]==69){
        if(id[1]==45){return 1;}
    }
    return 0;
}

fn is_battery_tier(tier:[]u8)i64 {
    if(tier.len<2){return 0;}
    if(tier[0]!=66){return 0;}
    if(tier[1]>=49){
        if(tier[1]<=53){return 1;}
    }
    return 0;
}

// resolve one slot name -> value slice. miss flag via ptr.
fn kb_slot_value(name:[]u8, spec:[]u8, tab:[]u8, img:[]u8, ec:i64, miss:*i64)[]u8 {
    let kp:*u8=_zag_malloc(name.len+2) as *u8;
    let kb:[]u8=kp[0..name.len+1];
    let i:i64=0;
    while(i<name.len){
        kb[i]=name[i];
        i=i+1;
    }
    kb[name.len]=61;
    if(s_find(spec,kb,0)>=0){
        let v:[]u8=spec_kv(spec,kb);
        return v;
    }
    miss.*=1;
    let mt:[]u8="";
    return mt;
}

fn gen_store(cx:*Cx, kbpath:[]u8, spec:[]u8)void {
    let memp:*u8=_zag_malloc(1048576) as *u8;
    let tabp:*u8=_zag_malloc(32768) as *u8;
    let tab:[]u8=tabp[0..32768];
    let n:i64=read_all(kbpath, memp, 1048576);
    if(n<0){
        e_raw(cx,"KB-MISS: cannot load knowledge store\n");
        return;
    }
    let img:[]u8=memp[0..n];
    let dg:i64=fnv1a(img);
    let ec:i64=kb_parse(memp, n, tab);
    if(ec<0){
        e_raw(cx,"KB-MISS: cannot parse knowledge store\n");
        return;
    }
    let bar:i64=s_find(spec,"|",0);
    let desc:[]u8=spec;
    if(bar>=0){desc=spec[0..bar];}
    let lowered:[]u8=s_lower(desc);
    let best:i64=-1;
    let bests:i64=0;
    let e:i64=0;
    while(e<ec){
        let id:[]u8=kb_entry_id(tab,img,e);
        if(kb_is_family(id)==1){
            let s:i64=kb_entry_score(tab,img,e,lowered);
            if(s>bests){
                bests=s;
                best=e;
            }
        }
        e=e+1;
    }
    if(best<0){
        e_raw(cx,"KB-MISS: no family entry matched spec\n");
        return;
    }
    let bid:[]u8=kb_entry_id(tab,img,best);
    let body:[]u8=kb_entry_body(tab,img,best);
    e_raw(cx,"// kb-recall family=");
    e_raw(cx,bid);
    e_raw(cx," digest=");
    e_hex(cx,dg);
    e_raw(cx,"\n");
    let miss:i64=0;
    let missname:[]u8="";
    let i:i64=0;
    while(i<body.len){
        if(body[i]==123){
            if(i+1<body.len){
                if(body[i+1]==123){
                    let j:i64=i+2;
                    let found:i64=0;
                    while(j+1<body.len){
                        if(body[j]==125){
                            if(body[j+1]==125){found=1;}
                        }
                        if(found==1){break;}
                        j=j+1;
                    }
                    if(found==0){miss=1;}
                    if(miss==0){
                        let name:[]u8=body[i+2..j];
                        missname=name;
                        let v:[]u8=kb_slot_value(name,spec,tab,img,ec,&miss);
                        if(miss==0){
                            e_raw(cx,v);
                        }
                        i=j+2;
                    }
                } else {
                    e_ch(cx,body[i]);
                    i=i+1;
                }
            } else {
                e_ch(cx,body[i]);
                i=i+1;
            }
        } else {
            e_ch(cx,body[i]);
            i=i+1;
        }
        if(miss==1){break;}
    }
    if(miss==1){
        cx.*.n=0;
        e_raw(cx,"KB-MISS: unresolvable slot {{");
        e_raw(cx,missname);
        e_raw(cx,"}}\n");
        return;
    }
    return;
}

'''

OLD_DO_GEN = '''fn do_gen()void {
    let spec:[]u8=_zag_arg(2);
    let installed:[]u8=_zag_arg(3);
    let demo:[]u8=_zag_arg(4);
    let card:[]u8=_zag_arg(5);
    // gate first: refuse banned requests before any generation
    let gr:i64=gate_hit(spec);
    if(gr!=0){
        _zag_print("REFUSED:G");
        _zag_print(_zag_i64_to_str(gr));
        _zag_print("\\n");
        return;
    }
    let c:Cx=cx_new(65536);
    let cx:*Cx=&c;
    let tier:[]u8=spec[0..2];
    if(s_eq(tier,"T1")==1){gen_t1(cx,spec,demo,installed);}
    else if(s_eq(tier,"T2")==1){gen_t2(cx,spec,demo,installed);}
    else if(s_eq(tier,"T4")==1){gen_t4(cx,spec,demo,installed,card);}
    else {e_raw(cx,"UNKNOWN_TIER\\n");}
'''

NEW_DO_GEN = '''fn do_gen()void {
    let kbpath:[]u8=_zag_arg(2);
    let spec:[]u8=_zag_arg(3);
    // gate first: refuse banned requests before any generation
    let gr:i64=gate_hit(spec);
    if(gr!=0){
        _zag_print("REFUSED:G");
        _zag_print(_zag_i64_to_str(gr));
        _zag_print("\\n");
        return;
    }
    let c:Cx=cx_new(300000);
    let cx:*Cx=&c;
    let tier:[]u8=spec[0..2];
    if(is_battery_tier(tier)==1){gen_store(cx,kbpath,spec);}
    else if(s_eq(tier,"T1")==1){gen_t1(cx,spec,"","");}
    else if(s_eq(tier,"T2")==1){gen_t2(cx,spec,"","");}
    else if(s_eq(tier,"T4")==1){gen_t4(cx,spec,"","","");}
    else {e_raw(cx,"UNKNOWN_TIER\\n");}
'''

OLD_REGEN = '''fn regen_from_spec(outc:*Cx, spec:[]u8, installed:[]u8, demo:[]u8, card:[]u8)i64 {
    outc.*.n=0;
    if(spec.len<2){return 0;}
    let tier:[]u8=spec[0..2];
    if(s_eq(tier,"T1")==1){gen_t1(outc,spec,demo,installed);}
    else if(s_eq(tier,"T2")==1){gen_t2(outc,spec,demo,installed);}
    else if(s_eq(tier,"T4")==1){gen_t4(outc,spec,demo,installed,card);}
    else {return 0;}'''

NEW_REGEN = '''fn regen_from_spec(outc:*Cx, spec:[]u8, kbpath:[]u8)i64 {
    outc.*.n=0;
    if(spec.len<2){return 0;}
    let tier:[]u8=spec[0..2];
    if(is_battery_tier(tier)==1){gen_store(outc,kbpath,spec);}
    else if(s_eq(tier,"T1")==1){gen_t1(outc,spec,"","");}
    else if(s_eq(tier,"T2")==1){gen_t2(outc,spec,"","");}
    else if(s_eq(tier,"T4")==1){gen_t4(outc,spec,"","","");}
    else {return 0;}'''

OLD_REGEN_TAIL = '''    if(s_has(out,"UNKNOWN_GOAL")==1){return 0;}
    if(s_has(out,"UNTAUGHT:")==1){return 0;}
    if(s_has(out,"NEED_CARD:")==1){return 0;}
    if(s_has(out,"UNKNOWN_TIER")==1){return 0;}
    if(s_has(out,"REFUSED:")==1){return 0;}
    return 1;
}'''

NEW_REGEN_TAIL = '''    if(s_has(out,"UNKNOWN_GOAL")==1){return 0;}
    if(s_has(out,"UNTAUGHT:")==1){return 0;}
    if(s_has(out,"NEED_CARD:")==1){return 0;}
    if(s_has(out,"UNKNOWN_TIER")==1){return 0;}
    if(s_has(out,"REFUSED:")==1){return 0;}
    if(s_has(out,"KB-MISS:")==1){return 0;}
    return 1;
}'''

OLD_DIAG_TEST_SIG = "fn diag_test(tr:*Cx, outc:*Cx, src:[]u8, ev:[]u8, spec:[]u8, installed:[]u8, demo:[]u8, card:[]u8, dr:*DRes)void {"
NEW_DIAG_TEST_SIG = "fn diag_test(tr:*Cx, outc:*Cx, src:[]u8, ev:[]u8, spec:[]u8, kbpath:[]u8, dr:*DRes)void {"

OLD_DIAG_TEST_REGEN = "if(regen_from_spec(outc,spec,installed,demo,card)==1){"
NEW_DIAG_TEST_REGEN = "if(regen_from_spec(outc,spec,kbpath)==1){"

OLD_DO_DIAGNOSE_HEAD = '''fn do_diagnose()void {
    let spec:[]u8=_zag_arg(2);
    let src:[]u8=_zag_arg(3);
    let evtype:[]u8=_zag_arg(4);
    let ev:[]u8=_zag_arg(5);
    let installed:[]u8=_zag_arg(6);
    let demo:[]u8=_zag_arg(7);
    let card:[]u8=_zag_arg(8);
'''
NEW_DO_DIAGNOSE_HEAD = '''fn do_diagnose()void {
    let kbpath:[]u8=_zag_arg(2);
    let spec:[]u8=_zag_arg(3);
    let src:[]u8=_zag_arg(4);
    let evtype:[]u8=_zag_arg(5);
    let ev:[]u8=_zag_arg(6);
'''

OLD_DIAG_TEST_CALL = "        diag_test(tr,outc,src,ev,spec,installed,demo,card,dr);"
NEW_DIAG_TEST_CALL = "        diag_test(tr,outc,src,ev,spec,kbpath,dr);"


def main():
    src = open(SRC).read()
    # 1. insert KB section before do_gen
    anchor = "fn do_gen()void {"
    assert src.count(anchor) == 1
    src = src.replace(anchor, KB_SECTION + anchor)
    # 2. replace do_gen head
    assert src.count(OLD_DO_GEN) == 1
    src = src.replace(OLD_DO_GEN, NEW_DO_GEN)
    # 3. regen_from_spec
    assert src.count(OLD_REGEN) == 1
    src = src.replace(OLD_REGEN, NEW_REGEN)
    assert src.count(OLD_REGEN_TAIL) == 1
    src = src.replace(OLD_REGEN_TAIL, NEW_REGEN_TAIL)
    # 4. diag_test signature + regen call
    assert src.count(OLD_DIAG_TEST_SIG) == 1
    src = src.replace(OLD_DIAG_TEST_SIG, NEW_DIAG_TEST_SIG)
    assert src.count(OLD_DIAG_TEST_REGEN) == 1
    src = src.replace(OLD_DIAG_TEST_REGEN, NEW_DIAG_TEST_REGEN)
    # 5. do_diagnose head + diag_test call
    assert src.count(OLD_DO_DIAGNOSE_HEAD) == 1
    src = src.replace(OLD_DO_DIAGNOSE_HEAD, NEW_DO_DIAGNOSE_HEAD)
    assert src.count(OLD_DIAG_TEST_CALL) == 1
    src = src.replace(OLD_DIAG_TEST_CALL, NEW_DIAG_TEST_CALL)
    # 6. header comment
    src = src.replace(
        "// learner.zag — CODING CREW (pure Zag, zero RNG).",
        "// learner4.zag — TASK-4 BATTERY learner (pure Zag, zero RNG).",
        1,
    )
    open(DST, "w").write(src)
    print("wrote", DST, len(src), "bytes")


if __name__ == "__main__":
    main()
