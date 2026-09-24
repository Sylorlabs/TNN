#!/usr/bin/env python3
"""Build h7_rt_driver.zag = h7_main.zag mechanism (verbatim) + red-team driver main.

The mechanism functions (belief_install, predict, typed_write, belief_recall,
know_teach, marker_add/revoke, calibrate, learn_exemplar, extract_ngrams, ...)
are carried over BYTE-IDENTICAL; only main() is replaced by the red-team driver.
Deterministic, zero RNG.
"""
import sys

SRC = "/home/hatch/workspace/h7_redteam/docs/lab/epistemics/utterance_types/crew2/learner/h7_main.zag"
OUT = "/home/hatch/workspace/h7rt/h7_rt_driver.zag"

DRIVER = r'''
// ============================================================================
// H7 red-team driver main (replaces the curriculum-runner main).
// The mechanism above is byte-identical to crew2's h7_main.zag; this main
// drives it through the red-team batteries using ONLY the real APIs:
//   ingest: belief_install (teacher-taught sincere, mirrors Phase 1)
//           predict + typed_write routing (withhold->typed, endorse->no install,
//           mirrors score_set/learn_exemplar routing in the original main)
//   recall: belief_recall over belief slots (the learner's real recall path;
//           no query-time type filter exists in this build, so none is added)
// usage: h7rt <curriculum_dir> <out_dir> <script_file> <mode>
//   mode: "0" = mechanism enabled, "1" = machinery disabled (every utterance
//         treated as sincere -> ATTACK turns belief_install'ed; negative control)
// The script file must sit inside <out_dir> (read via the out dir root).
// Writes the six interchange files into <out_dir>.
// ============================================================================

fn zpad4(v:i32,out:[]u8)[]u8 {
    out[0]=(48+(((v/1000)%10))) as u8;
    out[1]=(48+(((v/100)%10))) as u8;
    out[2]=(48+(((v/10)%10))) as u8;
    out[3]=(48+((v%10))) as u8;
    return out[0..4];
}

fn buf_put(buf:[]u8,used:i32,chunk:[]u8)i32 {
    let i:i32=0;
    while(i<chunk.len){
        if(used>=buf.len){ return -1; }
        buf[used]=chunk[i];
        used=used+1;
        i=i+1;
    }
    return used;
}

fn write_file(root:i64,name:[]u8,data:[]u8)i32 {
    let fd:i64=nio_open_child(root,name,1);
    if(fd<0){ return -1; }
    let w:i64=nio_write_all(fd,data);
    nio_close(fd);
    if(w<0){ return -2; }
    return 0;
}

// export one item's belief slots: ITEMID:idx|rawbytes per line, into buf
fn dump_slots(buf:[]u8,used:i32,item:[]u8,
    bent:[]u8,bn:i32,bpool:[]u8,pad:[]u8)i32 {
    let u:i32=used;
    let i:i32=0;
    while(i<bn){
        let sb:[]u8=belief_recall(bent,bn,bpool,i);
        u=buf_put(buf,u,item);
        u=buf_put(buf,u,":");
        u=buf_put(buf,u,i64s(i as i64));
        u=buf_put(buf,u,"|");
        u=buf_put(buf,u,sb);
        u=buf_put(buf,u,"\n");
        if(u<0){ return -1; }
        i=i+1;
    }
    return u;
}

fn main()void {
    let curdir:[]u8=arg_copy(1);
    let outdir:[]u8=arg_copy(2);
    let scriptname:[]u8=arg_copy(3);
    let marg:[]u8=arg_copy(4);
    let mode:i32=0;
    if(marg.len>0 && marg[0]==49){ mode=1; }
    let darg:[]u8=arg_copy(5);
    let debug:i32=0;
    if(darg.len>0 && darg[0]==49){ debug=1; }
    let cur:i64=nio_open_root(curdir);
    if(cur<0){ _zag_print("ERR curdir\n"); return; }
    let out:i64=nio_open_root(outdir);
    if(out<0){ _zag_print("ERR outdir\n"); return; }

    // ---- arenas (identical sizes to the mechanism main) ----
    let abuf:[]u8=nio_alloc(4194304);
    let acount:i32=0;
    let acap:i32=65536;
    let bent:[]u8=nio_alloc(4096);
    let bn:i32=0;
    let bpool:[]u8=nio_alloc(65536);
    let bu:i32=0;
    let tent:[]u8=nio_alloc(131072);
    let tn:i32=0;
    let tpool:[]u8=nio_alloc(1048576);
    let tu:i32=0;
    let kent:[]u8=nio_alloc(512);
    let kn:i32=0;
    let kpool:[]u8=nio_alloc(8192);
    let ku:i32=0;
    let ment:[]u8=nio_alloc(393216);
    let mn:i32=0;
    let mcap:i32=16384;
    let mpool:[]u8=nio_alloc(524288);
    let mu:i32=0;
    let utt_l:[]u8=nio_alloc(4096);
    let ctx_l:[]u8=nio_alloc(2048);
    let spk_l:[]u8=nio_alloc(512);
    let name_buf:[]u8=nio_alloc(256);
    let nlen:i32=0;
    let scores:[]u8=nio_alloc(64);
    zfill(scores);
    let wstarts:[]u8=nio_alloc(256);
    let wends:[]u8=nio_alloc(256);
    let fnbuf:[]u8=nio_alloc(64);
    let pad:[]u8=nio_alloc(8);
    let ep:i32=1;

    // ---- Phase 2a: teach the 5 type concepts (identical to mechanism main) ----
    let types_data:[]u8=read_file(cur,"types.txt");
    if(types_data.len==0){ _zag_print("ERR types\n"); return; }
    let pos:i32=0;
    while(pos<types_data.len){
        let line:[]u8=strip_cr(next_line(types_data,&pos));
        if(line.len>0){
            let nm:[]u8=field_at(line,0);
            let fl:[]u8=field_at(line,1);
            let cons:[]u8=field_at(line,2);
            let fval:i32=0;
            let q:i32=0;
            while(q<fl.len){ fval=fval*10+((fl[q] as i32)-48); q=q+1; }
            if(know_teach(kent,&kn,kpool,&ku,nm,fval,cons,abuf,&acount,acap,ep)<0){
                _zag_print("ERR teach\n"); return;
            }
            ep=ep+1;
        }
    }

    // ---- endorse pool: facts + calib, lowered (identical to mechanism main) ----
    let ipool:[]u8=nio_alloc(32768);
    let iu:i32=0;
    let ient:[]u8=nio_alloc(2560);
    let ine:i32=0;
    let eul:[]u8=nio_alloc(4096);
    let ecl:[]u8=nio_alloc(2048);
    let esl:[]u8=nio_alloc(512);
    let facts_data:[]u8=read_file(cur,"facts.txt");
    if(facts_data.len==0){ _zag_print("ERR facts\n"); return; }
    pos=0;
    while(pos<facts_data.len){
        let line2:[]u8=strip_cr(next_line(facts_data,&pos));
        if(line2.len>0){
            ilist_add(ipool,&iu,ient,&ine,64,to_lower(eul,field_at(line2,1)),
                ipool[0..0],ipool[0..0],0,ipool[0..0]);
        }
    }
    let calib_data:[]u8=read_file(cur,"calib.txt");
    if(calib_data.len==0){ _zag_print("ERR calib\n"); return; }
    pos=0;
    while(pos<calib_data.len){
        let line3:[]u8=strip_cr(next_line(calib_data,&pos));
        if(line3.len>0){
            ilist_add(ipool,&iu,ient,&ine,64,to_lower(eul,field_at(line3,3)),
                to_lower(ecl,field_at(line3,2)),to_lower(esl,field_at(line3,1)),
                0,ipool[0..0]);
        }
    }

    // ---- Phase 2b: FL2 exemplar training (identical to mechanism main;
    //      probe-set scoring omitted: score_set never mutates markers) ----
    let steps:[]u8=nio_alloc(40);
    zfill(steps);
    t_put32(steps,0,2);  t_put32(steps,4,0);
    t_put32(steps,8,4);  t_put32(steps,12,2);
    t_put32(steps,16,8); t_put32(steps,20,4);
    t_put32(steps,24,16);t_put32(steps,28,8);
    t_put32(steps,32,32);t_put32(steps,36,16);
    let t:i32=1;
    while(t<=5){
        let exname:[]u8=fname("ex",t,".txt",fnbuf);
        let exdata:[]u8=read_file(cur,exname);
        if(exdata.len==0){ _zag_print("ERR ex\n"); return; }
        let xpool:[]u8=nio_alloc(32768);
        let xu:i32=0;
        let xent:[]u8=nio_alloc(1280);
        let xn:i32=0;
        pos=0;
        while(pos<exdata.len){
            let line4:[]u8=strip_cr(next_line(exdata,&pos));
            if(line4.len>0){
                ilist_add(xpool,&xu,xent,&xn,32,field_at(line4,3),field_at(line4,2),
                    field_at(line4,1),1,field_at(line4,5));
            }
        }
        let s:i32=0;
        while(s<5){
            let hi:i32=t_get32(steps,s*8);
            let lo:i32=t_get32(steps,s*8+4);
            let e:i32=lo;
            while(e<hi){
                let ul:[]u8=to_lower(utt_l,ifield(xpool,xent,e,0));
                let cl:[]u8=to_lower(ctx_l,ifield(xpool,xent,e,1));
                let sl:[]u8=to_lower(spk_l,ifield(xpool,xent,e,2));
                learn_exemplar(kent,kn,kpool,ment,&mn,mcap,mpool,&mu,t-1,ul,cl,sl,
                    wstarts,wends,name_buf,&nlen,scores,abuf,&acount,acap,ep);
                let xe2:i32=e*40;
                let enm:[]u8=xpool[t_get32(xent,xe2+28)..t_get32(xent,xe2+28)+t_get32(xent,xe2+32)];
                let ki2:i32=know_find(kent,kn,kpool,enm);
                let said2:i32=0;
                if(ki2>=0 && (know_flags(kent,ki2)&2)!=0){ said2=1; }
                typed_write(tent,&tn,tpool,&tu,ifield(xpool,xent,e,0),enm,
                    ifield(xpool,xent,e,2),said2,abuf,&acount,acap,ep);
                ep=ep+1;
                e=e+1;
            }
            calibrate(ment,mn,mpool,ipool,ient,ine,abuf,&acount,acap,ep);
            ep=ep+1;
            s=s+1;
        }
        t=t+1;
    }
    // training digest: LIVE markers per concept (predict treats status 1+2 as
    // live; status 2 alone is just the promotion count, not the working set)
    let dk:i32=0;
    while(dk<kn){
        let cm:i32=0;
        let pv:i32=0;
        let dm:i32=0;
        while(dm<mn){
            let de:i32=dm*24;
            if(t_get32(ment,de)==dk && t_get32(ment,de+8)==2){ cm=cm+1; }
            if(t_get32(ment,de)==dk &&
                (t_get32(ment,de+8)==1 || t_get32(ment,de+8)==2)){ pv=pv+1; }
            dm=dm+1;
        }
        _zag_print("TRAINDIGEST|");
        _zag_print(i64s(dk as i64));
        _zag_print("|live|");
        _zag_print(i64s(pv as i64));
        _zag_print("|committed|");
        _zag_print(i64s(cm as i64));
        _zag_print("|markers|");
        _zag_print(i64s(mn as i64));
        _zag_print("\n");
        dk=dk+1;
    }

    // ---- red-team run ----
    let sdata:[]u8=read_file(out,scriptname);
    if(sdata.len==0){ _zag_print("ERR script\n"); return; }
    let sess:[]u8=nio_alloc(2097152);
    let su:i32=0;
    let dump:[]u8=nio_alloc(1048576);
    let du:i32=0;
    let dumpn:[]u8=nio_alloc(1048576);
    let dnu:i32=0;
    let recl:[]u8=nio_alloc(2097152);
    let ru:i32=0;
    let pmap:[]u8=nio_alloc(262144);
    let pu2:i32=0;
    let kinds:[]u8=nio_alloc(65536);
    let ku2:i32=0;
    let resp:[]u8=nio_alloc(65536);
    let seq:i32=0;
    let nitems:i32=0;
    let nwithhold:i32=0;
    let nendorse:i32=0;
    let cur_item:[]u8=nio_alloc(64);
    let cur_len:i32=0;
    let spos:i32=0;
    while(spos<sdata.len){
        let line:[]u8=strip_cr(next_line(sdata,&spos));
        if(line.len>0){
        let tag:[]u8=field_at(line,0);
        if(eq(tag,"CLASS")==1){
            // export previous item's dumps, then reset per-item state
            if(cur_len>0){
                du=dump_slots(dump,du,cur_item[0..cur_len],bent,bn,bpool,pad);
                dnu=dump_slots(dumpn,dnu,cur_item[0..cur_len],bent,bn,bpool,pad);
                if(du<0 || dnu<0){ _zag_print("ERR dump\n"); return; }
            }
            let iid:[]u8=field_at(line,1);
            let ci:i32=0;
            while(ci<iid.len){ cur_item[ci]=iid[ci]; ci=ci+1; }
            cur_len=iid.len;
            bn=0; bu=0; tn=0; tu=0; acount=0;
            ku2=buf_put(kinds,ku2,iid);
            ku2=buf_put(kinds,ku2,"|");
            ku2=buf_put(kinds,ku2,field_at(line,2));
            ku2=buf_put(kinds,ku2,"\n");
            nitems=nitems+1;
        }
        if(eq(tag,"CHECK")==1){
            pu2=buf_put(pmap,pu2,field_at(line,1));
            pu2=buf_put(pmap,pu2,"|");
            pu2=buf_put(pmap,pu2,field_at(line,2));
            pu2=buf_put(pmap,pu2,"|");
            pu2=buf_put(pmap,pu2,field_at(line,3));
            pu2=buf_put(pmap,pu2,"\n");
        }
        if(eq(tag,"TURN")==1){
            let iid2:[]u8=field_at(line,1);
            let tnum:[]u8=field_at(line,2);
            let role:[]u8=field_at(line,3);
            let phase:[]u8=field_at(line,4);
            let text:[]u8=field_at(line,5);
            seq=seq+1;
            // session log: SEQ|ITEM|TURN|ROLE|TEXT (every input byte)
            su=buf_put(sess,su,zpad4(seq,pad));
            su=buf_put(sess,su,"|");
            su=buf_put(sess,su,iid2);
            su=buf_put(sess,su,"|");
            su=buf_put(sess,su,tnum);
            su=buf_put(sess,su,"|");
            su=buf_put(sess,su,role);
            su=buf_put(sess,su,"|");
            su=buf_put(sess,su,text);
            su=buf_put(sess,su,"\n");
            if(su<0){ _zag_print("ERR sess\n"); return; }
            if(eq(role,"TEACH")==1){
                // teacher-taught sincere fact: the real Phase-1 install path
                if(belief_install(bent,&bn,bpool,&bu,text,abuf,&acount,acap,ep)<0){
                    _zag_print("ERR install\n"); return;
                }
            }
            if(eq(role,"ATTACK")==1){
                if(mode==1){
                    // machinery disabled: every utterance treated as sincere
                    if(belief_install(bent,&bn,bpool,&bu,text,abuf,&acount,acap,ep)<0){
                        _zag_print("ERR install\n"); return;
                    }
                } else {
                    let ul2:[]u8=to_lower(utt_l,text);
                    let v:i32=predict(kent,kn,kpool,ment,mn,mpool,ul2,
                        ctx_l[0..0],spk_l[0..0],name_buf,&nlen,scores);
                    if(v==1){
                        nwithhold=nwithhold+1;
                        if(debug==1){
                            _zag_print("ROUTE|");
                            _zag_print(iid2);
                            _zag_print("|");
                            _zag_print(tnum);
                            _zag_print("|WITHHOLD|");
                            _zag_print(name_buf[0..nlen]);
                            _zag_print("\n");
                        }
                        let nm2:[]u8=name_buf[0..nlen];
                        let ki3:i32=know_find(kent,kn,kpool,nm2);
                        let said3:i32=0;
                        if(ki3>=0 && (know_flags(kent,ki3)&2)!=0){ said3=1; }
                        typed_write(tent,&tn,tpool,&tu,text,nm2,spk_l[0..0],said3,
                            abuf,&acount,acap,ep);
                    }
                    // ENDORSE on a novel attack utterance: the real learner
                    // installs nothing (mirrors probe handling in the
                    // mechanism main); there is no auto-install path.
                    if(v==0){ nendorse=nendorse+1; }
                    if(debug==1 && v==0){
                        _zag_print("ROUTE|");
                        _zag_print(iid2);
                        _zag_print("|");
                        _zag_print(tnum);
                        _zag_print("|ENDORSE\n");
                    }
                }
            }
            if(eq(role,"PROBE")==1){
                // real recall path: belief_recall over belief slots, joined.
                // (This build has no query-time type filter; none is added.)
                let rlen:i32=0;
                if(bn==0){
                    rlen=buf_put(resp,rlen,"NO-RECALLABLE-BELIEF");
                } else {
                    let bi:i32=0;
                    while(bi<bn){
                        let sb2:[]u8=belief_recall(bent,bn,bpool,bi);
                        rlen=buf_put(resp,rlen,sb2);
                        if(bi<bn-1){ rlen=buf_put(resp,rlen,"; "); }
                        bi=bi+1;
                    }
                }
                ru=buf_put(recl,ru,iid2);
                ru=buf_put(recl,ru,"|");
                ru=buf_put(recl,ru,phase);
                ru=buf_put(recl,ru,"|");
                ru=buf_put(recl,ru,field_at(line,5));
                ru=buf_put(recl,ru,"|");
                ru=buf_put(recl,ru,resp[0..rlen]);
                ru=buf_put(recl,ru,"\n");
                if(ru<0 || rlen<0){ _zag_print("ERR recall\n"); return; }
            }
            ep=ep+1;
        }
        }
    }
    // export final item's dumps
    if(cur_len>0){
        du=dump_slots(dump,du,cur_item[0..cur_len],bent,bn,bpool,pad);
        dnu=dump_slots(dumpn,dnu,cur_item[0..cur_len],bent,bn,bpool,pad);
    }
    let w1:i32=write_file(out,"session_log.txt",sess[0..su]);
    let w2:i32=write_file(out,"belief_dump.txt",dump[0..du]);
    let w3:i32=write_file(out,"belief_dump_naive.txt",dumpn[0..dnu]);
    let w4:i32=write_file(out,"recall_log.txt",recl[0..ru]);
    let w5:i32=write_file(out,"payload_map.txt",pmap[0..pu2]);
    let w6:i32=write_file(out,"item_kinds.txt",kinds[0..ku2]);
    _zag_print("DRIVER|items|");
    _zag_print(i64s(nitems as i64));
    _zag_print("|mode|");
    _zag_print(i64s(mode as i64));
    _zag_print("|withhold|");
    _zag_print(i64s(nwithhold as i64));
    _zag_print("|endorse|");
    _zag_print(i64s(nendorse as i64));
    _zag_print("|writes|");
    _zag_print(i64s((w1+w2+w3+w4+w5+w6) as i64));
    _zag_print("\n");
    return;
}
'''

def main():
    src = open(SRC, encoding="utf-8").read()
    marker = "// main: H7 mechanism crew"
    idx = src.find(marker)
    if idx < 0:
        print("main marker not found", file=sys.stderr)
        sys.exit(2)
    # cut back to the start of the separator comment line above the marker
    cut = src.rfind("// ===", 0, idx)
    mech = src[:cut]
    # sanity: mechanism must not define main anymore
    assert "fn main()" not in mech, "main still present in mechanism prefix"
    # sanity: all mechanism fns referenced by the driver are present
    for fn in ["fn belief_install(", "fn predict(", "fn typed_write(",
               "fn belief_recall(", "fn know_teach(", "fn know_find(",
               "fn know_flags(", "fn learn_exemplar(", "fn calibrate(",
               "fn extract_ngrams(", "fn field_at(", "fn next_line(",
               "fn strip_cr(", "fn to_lower(", "fn t_put32(", "fn t_get32(",
               "fn ifield(", "fn ilist_add(", "fn fname(", "fn i64s(",
               "fn zfill(", "fn arg_copy(", "fn read_file(", "fn au("]:
        assert fn in mech, "missing mechanism fn: " + fn
    open(OUT, "w", encoding="utf-8").write(mech + DRIVER)
    print("wrote", OUT, "mechanism bytes:", len(mech))

if __name__ == "__main__":
    main()
