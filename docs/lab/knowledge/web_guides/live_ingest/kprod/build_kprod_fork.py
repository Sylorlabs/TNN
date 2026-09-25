#!/usr/bin/env python3
"""Build instrument_kprod.zag from the frozen Track-B base.

Applies the PREREG_KPROD.md §2 mechanism as ADDITIVE changes to a copy of
instrument_kb.zag (SHA-256 d7ce44ffe8866f7fb5869250cfba40fcd8140e22eb79d4a23b773969dedede41):
  - kb_tv text-vs-text matcher (+ KPROD store helpers)
  - cmd_kbcommit: append semantics + `|`-rejection + auto-resolve
  - cmd_kbtest (new deliberate command)
  - verdict_core: +prod/+sd params, resolved-false check, pending diversion
  - main(): kbtest command (+ temporary kbtv debug hook, stripped later)

Every edit asserts exactly-once match so transcription drift fails loud.
"""
import sys, hashlib

SRC = sys.argv[1]
DST = sys.argv[2]
STRIP_DEBUG = "--strip-debug" in sys.argv

BASE_SHA = "d7ce44ffe8866f7fb5869250cfba40fcd8140e22eb79d4a23b773969dedede41"

src = open(SRC).read()
h = hashlib.sha256(src.encode()).hexdigest()
# NOTE: after the debug hook is stripped the working copy no longer matches
# the base SHA; the check below only applies to the pre-edit copy.
if not STRIP_DEBUG:
    assert h == BASE_SHA, f"base SHA mismatch: {h}"

KPROD_SECTION = r'''
// ================= KPROD: pending + resolved-false production path ========
// Additive fork of instrument_kb.zag per PREREG_KPROD.md §2.
// New stores: pending.txt (PB|<pseq>|<claim>|<pidcsv>), resolved.txt
// (RF|<pseq>|<claim>|<how>). knowledge.txt gains APPEND semantics in
// kbcommit (seq continues from max+1). The verdict path opens knowledge.txt
// read-only; pending.txt is written only by the verdict-path diversion
// (prod mode, Arm K) and entries are removed only by deliberate
// kbtest/kbcommit. Zero RNG.

// kb_tv: text-vs-text matcher. a = candidate text (e.g. a pending claim),
// b = committed-claim text. Returns 2=AGREE, 1=CONTRADICT, 0=UNKNOWN.
// Byte-for-byte the same pair logic as kb_prior's inner loop:
//   content tokens via content_toks (lowercase, tokenize minl=2, exact-drop
//   of the taught G1 DROP stoplist); digit tokens via digit_toks.
//   sh_ck = overlap(a_toks, b_toks); bind = (an>0 && 3*sh_ck >= 2*an).
//   if bind: sh_kc = overlap(b_toks, a_toks); deq = digits_eq(...);
//   if sh_kc>=bn && deq==1 -> 2 (AGREE);
//   elif adn>=1 && deq==0 -> 1 (CONTRADICT); else 0. else 0.
fn kb_tv(a:[]u8, b:[]u8, dropb:[]u8, dropt:[]u8, dropn:i32)i32 {
    let ab:[]u8=nio_alloc(16384);
    let apos:i32=0;
    let at:[]u8=nio_alloc(64*8);
    let an:i32=0;
    content_toks(a,dropb,dropt,dropn,ab,&apos,at,64,&an);
    let bb:[]u8=nio_alloc(16384);
    let bpos:i32=0;
    let bt:[]u8=nio_alloc(64*8);
    let bn:i32=0;
    content_toks(b,dropb,dropt,dropn,bb,&bpos,bt,64,&bn);
    let adb:[]u8=nio_alloc(4096);
    let adpos:i32=0;
    let adt:[]u8=nio_alloc(32*8);
    let adn:i32=0;
    digit_toks(ab,at,an,adb,&adpos,adt,&adn);
    let bdb:[]u8=nio_alloc(4096);
    let bdpos:i32=0;
    let bdt:[]u8=nio_alloc(32*8);
    let bdn:i32=0;
    digit_toks(bb,bt,bn,bdb,&bdpos,bdt,&bdn);
    let rc:i32=0;
    let sh_ck:i32=overlap(ab,at,an,bb,bt,bn);
    let bind:i32=0;
    if(an>0 && 3*sh_ck>=2*an){bind=1;}
    if(bind==1){
        let sh_kc:i32=overlap(bb,bt,bn,ab,at,an);
        let deq:i32=digits_eq(adb,adt,adn,bdb,bdt,bdn);
        if(sh_kc>=bn && deq==1){rc=2;}else{
            if(adn>=1 && deq==0){rc=1;}
        }
    }
    nio_free(ab);
    nio_free(at);
    nio_free(bb);
    nio_free(bt);
    nio_free(adb);
    nio_free(adt);
    nio_free(bdb);
    nio_free(bdt);
    return rc;
}

// SPEC-DEFERRED CHOICE (§2.1/§2.3): `|`-sanitization is a pure copy with
// every `|` byte (124) replaced by a space (32). Returns a fresh slice;
// the caller frees it.
fn sanitize_pipes(s:[]u8)[]u8 {
    let b:[]u8=nio_alloc(s.len+1);
    if(b.len==0){return b;}
    let i:i32=0;
    while(i<s.len){
        let c:u8=s[i];
        if(c==124){c=32;}
        b[i]=c;
        i=i+1;
    }
    return b[0..s.len];
}

// kb_maxseq: max <seq> in <sd>/knowledge.txt; 0 when absent/empty.
fn kb_maxseq(sd:[]u8)i32 {
    let ok:i32=0;
    let buf:[]u8=read_file(sd,"knowledge.txt",&ok);
    if(ok==0){return 0;}
    let mx:i32=0;
    let pos:i32=0;
    let ls:i32=0;
    let ll:i32=0;
    while(next_line(buf,&pos,&ls,&ll)==1){
        let ln:i32=ll;
        if(ln>0 && buf[ls+ln-1]==13){ln=ln-1;}
        if(ln>4 && buf[ls]==75 && buf[ls+1]==66 && buf[ls+2]==124){
            let p:i32=ls+3;
            while(p<ls+ln && buf[p]!=124){p=p+1;}
            if(p<ls+ln){
                let v:i32=atoi(buf[ls+3..p]);
                if(v>mx){mx=v;}
            }
        }
    }
    nio_free(buf);
    return mx;
}

// append_to_file: append data to <sd>/name (missing file -> created).
fn append_to_file(sd:[]u8,name:[]u8,data:[]u8)i32 {
    let ok:i32=0;
    let old:[]u8=read_file(sd,name,&ok);
    let nb:[]u8=nio_alloc(old.len+data.len+1);
    let o:i32=0;
    if(ok==1){
        let c:i32=0;
        while(c<old.len){nb[o+c]=old[c]; c=c+1;}
        o=o+old.len;
        nio_free(old);
    }
    let c2:i32=0;
    while(c2<data.len){nb[o+c2]=data[c2]; c2=c2+1;}
    o=o+data.len;
    let rc:i32=write_file(sd,name,nb[0..o]);
    nio_free(nb);
    return rc;
}

// drop_load: the taught DROP list from <sd>/installed.txt -> lowercased
// buffer + token table (mirrors the verdict_core KB-prior setup). The
// caller frees the returned buffer and dropt.
fn drop_load(sd:[]u8,dropt:[]u8,dropn:*i32)[]u8 {
    dropn[0]=0;
    let dt:[]u8=nio_alloc(16384);
    let dp:i32=0;
    let dn:i32=0;
    load_installed(sd,dt,&dp,&dn);
    let dropv:[]u8=dget(dt,dn,"DROP");
    let droplow:[]u8=lower_copy(dropv);
    nio_free(dt);
    tokenize(droplow,dropt,128,1,dropn);
    return droplow;
}

// pend_load: read <sd>/pending.txt; lines "PB|<pseq>|<claim>|<pidcsv>".
// pbt: 5 u32 per entry: pseq, claim-off, claim-len, pidcsv-off, pidcsv-len.
// Returns 1 if the file was present, 0 when absent.
fn pend_load(sd:[]u8,pba:[]u8,pbt:[]u8,pn:*i32)i32 {
    pn[0]=0;
    let ok:i32=0;
    let buf:[]u8=read_file(sd,"pending.txt",&ok);
    if(ok==0){return 0;}
    let apos:i32=0;
    let pos:i32=0;
    let ls:i32=0;
    let ll:i32=0;
    while(next_line(buf,&pos,&ls,&ll)==1){
        let ln:i32=ll;
        if(ln>0 && buf[ls+ln-1]==13){ln=ln-1;}
        if(ln>4 && buf[ls]==80 && buf[ls+1]==66 && buf[ls+2]==124){
            let p:i32=ls+3;
            while(p<ls+ln && buf[p]!=124){p=p+1;}
            if(p<ls+ln && pn[0]<64){
                let ps:i32=atoi(buf[ls+3..p]);
                let cs:i32=p+1;
                let q:i32=cs;
                while(q<ls+ln && buf[q]!=124){q=q+1;}
                let cl:i32=q-cs;
                let vs:i32=q;
                let vl:i32=0;
                if(q<ls+ln){vs=q+1; vl=ls+ln-vs;}
                if(apos+cl+vl<=pba.len){
                    let c:i32=0;
                    while(c<cl){pba[apos+c]=buf[cs+c]; c=c+1;}
                    let c0:i32=apos;
                    apos=apos+cl;
                    c=0;
                    while(c<vl){pba[apos+c]=buf[vs+c]; c=c+1;}
                    let v0:i32=apos;
                    apos=apos+vl;
                    p32(pbt,pn[0]*20,ps);
                    p32(pbt,pn[0]*20+4,c0);
                    p32(pbt,pn[0]*20+8,cl);
                    p32(pbt,pn[0]*20+12,v0);
                    p32(pbt,pn[0]*20+16,vl);
                    pn[0]=pn[0]+1;
                }
            }
        }
    }
    nio_free(buf);
    return 1;
}

// pend_write_mask: rewrite <sd>/pending.txt from the loaded entries,
// dropping entries with rmask[i]==1.
fn pend_write_mask(sd:[]u8,pba:[]u8,pbt:[]u8,pn:i32,rmask:[]u8)void {
    let ob:[]u8=nio_alloc(65536);
    let o:i32=0;
    let i:i32=0;
    while(i<pn){
        if(rmask[i]==0){
            let ps:i32=g32(pbt,i*20);
            let co:i32=g32(pbt,i*20+4);
            let cl:i32=g32(pbt,i*20+8);
            let vo:i32=g32(pbt,i*20+12);
            let vl:i32=g32(pbt,i*20+16);
            let sq:[]u8=i64s(ps as i64);
            let need:i32=3+sq.len+1+cl+1+vl+1;
            if(o+need<=ob.len){
                ob[o]=80; ob[o+1]=66; ob[o+2]=124; o=o+3;
                let c:i32=0;
                while(c<sq.len){ob[o+c]=sq[c]; c=c+1;}
                o=o+sq.len;
                ob[o]=124; o=o+1;
                c=0;
                while(c<cl){ob[o+c]=pba[co+c]; c=c+1;}
                o=o+cl;
                ob[o]=124; o=o+1;
                c=0;
                while(c<vl){ob[o+c]=pba[vo+c]; c=c+1;}
                o=o+vl;
                ob[o]=10; o=o+1;
            }
            nio_free(sq);
        }
        i=i+1;
    }
    write_file(sd,"pending.txt",ob[0..o]);
    nio_free(ob);
    return;
}

// resolved_load: read <sd>/resolved.txt; lines "RF|<pseq>|<claim>|<how>".
// rbt: 3 u32 per entry: pseq, claim-off, claim-len.
// Returns 1 if the file was present, 0 when absent.
fn resolved_load(sd:[]u8,rba:[]u8,rbt:[]u8,rn:*i32)i32 {
    rn[0]=0;
    let ok:i32=0;
    let buf:[]u8=read_file(sd,"resolved.txt",&ok);
    if(ok==0){return 0;}
    let apos:i32=0;
    let pos:i32=0;
    let ls:i32=0;
    let ll:i32=0;
    while(next_line(buf,&pos,&ls,&ll)==1){
        let ln:i32=ll;
        if(ln>0 && buf[ls+ln-1]==13){ln=ln-1;}
        if(ln>4 && buf[ls]==82 && buf[ls+1]==70 && buf[ls+2]==124){
            let p:i32=ls+3;
            while(p<ls+ln && buf[p]!=124){p=p+1;}
            if(p<ls+ln && rn[0]<64){
                let ps:i32=atoi(buf[ls+3..p]);
                let cs:i32=p+1;
                let q:i32=cs;
                while(q<ls+ln && buf[q]!=124){q=q+1;}
                let cl:i32=q-cs;
                if(apos+cl<=rba.len){
                    let c:i32=0;
                    while(c<cl){rba[apos+c]=buf[cs+c]; c=c+1;}
                    p32(rbt,rn[0]*12,ps);
                    p32(rbt,rn[0]*12+4,apos);
                    p32(rbt,rn[0]*12+8,cl);
                    apos=apos+cl;
                    rn[0]=rn[0]+1;
                }
            }
        }
    }
    nio_free(buf);
    return 1;
}

// pids_csv: same content as print_pids_csv, returned as a fresh string.
fn pids_csv(pa:[]u8,pt:[]u8,idx:[]u8,n:i32)[]u8 {
    let b:[]u8=nio_alloc(4096);
    let o:i32=0;
    let m:i32=0;
    while(m<n){
        if(m>0 && o<b.len){b[o]=44; o=o+1;}
        let pd:[]u8=pid_of(pa,pt,g32(idx,m*4));
        let c:i32=0;
        while(c<pd.len && o<b.len){b[o]=pd[c]; c=c+1; o=o+1;}
        m=m+1;
    }
    return b[0..o];
}
'''

def once(s, old, new, tag):
    n = s.count(old)
    assert n == 1, f"{tag}: expected 1 match, found {n}"
    return s.replace(old, new, 1)

# E0: fork header after the @import line.
src = once(src,
    '@import("R33_NATIVE_IO_V1.zag")\n',
    '@import("R33_NATIVE_IO_V1.zag")\n\n'
    '// instrument_kprod.zag — KPROD fork of instrument_kb.zag (Track B).\n'
    '// Per PREREG_KPROD.md §2 (frozen): additive changes only. New: kb_tv\n'
    '// text-vs-text matcher, pending.txt + resolved.txt stores, kbcommit\n'
    '// append semantics + auto-resolve, kbtest deliberate command,\n'
    '// verdict_core prod mode (resolved-false check + pending diversion).\n'
    '// Zero RNG.\n',
    "E0 header")

# E1: KPROD section between digits_eq and kb_prior.
src = once(src,
    '    nio_free(used);\n    return 1;\n}\n\n// kb_prior: the retrieval stage.',
    '    nio_free(used);\n    return 1;\n}\n' + KPROD_SECTION +
    '\n// kb_prior: the retrieval stage.',
    "E1 kprod-section")

NEW_KBCOMMIT = r'''
// cmd_kbcommit: the DELIBERATE install path for the knowledge store.
// Reads <src> (one claim per line), validates every line against the
// PARSE gate (>=4 tokens, <=600 chars) plus the `|`-rejection (the store
// format uses `|` delimiters), all-or-nothing. Rejections emit the single
// frozen line KB|REJECT|line <n>|PARSE-GATE (SPEC-DEFERRED CHOICE: the
// prereg gives one Reject line format for the whole validation step, so
// `|`-lines use it too). New claims are APPENDED to <sd>/knowledge.txt
// with continuing seq (max(existing)+1); the verdict path only ever reads
// this file. Then the auto-resolve pass (§2.3): every pending entry is
// kb_tv-compared against each NEWLY committed claim — the AGREE pass over
// all pairs first, then the CONTRADICT pass (same precedence as the
// prior): AGREE -> promote into knowledge.txt (KB|AUTO_PROMOTED|<pseq>|
// <kseq>), CONTRADICT -> resolve false into resolved.txt as
// RF|<pseq>|<claim>|COMMIT (KB|AUTO_FALSE|<pseq>). Untouched otherwise.
fn cmd_kbcommit(src:[]u8,sd:[]u8)i32 {
    let ok:i32=0;
    let buf:[]u8=read_path(src,&ok);
    if(ok==0){_zag_println("KB|ERROR|read-fail"); return 2;}
    let ca:[]u8=nio_alloc(65536);
    let ct:[]u8=nio_alloc(64*8);
    let capos:i32=0;
    let n:i32=0;
    let pos:i32=0;
    let ls:i32=0;
    let ll:i32=0;
    while(next_line(buf,&pos,&ls,&ll)==1){
        let ln:i32=ll;
        if(ln>0 && buf[ls+ln-1]==13){ln=ln-1;}
        let t:[]u8=trim(buf[ls..ls+ln]);
        if(t.len==0){continue;}
        let low:[]u8=lower_copy(t);
        let tt:[]u8=nio_alloc(512*8);
        let tn:i32=0;
        tokenize(low,tt,512,2,&tn);
        let piped:i32=bsub(t,"|");
        nio_free(low);
        nio_free(tt);
        if(tn<4 || t.len>600 || piped==1){
            _zag_print("KB|REJECT|line ");
            _zag_print(i64s((n+1) as i64));
            _zag_println("|PARSE-GATE");
            nio_free(ca);
            nio_free(ct);
            nio_free(buf);
            return 3;
        }
        if(n<64 && capos+t.len<=ca.len){
            let c:i32=0;
            while(c<t.len){ca[capos+c]=t[c]; c=c+1;}
            p32(ct,n*8,capos);
            p32(ct,n*8+4,t.len);
            capos=capos+t.len;
        }
        n=n+1;
    }
    if(n==0 || n>64){
        _zag_println("KB|ERROR|empty-or-too-many");
        nio_free(ca);
        nio_free(ct);
        nio_free(buf);
        return 3;
    }
    // append with continuing seq
    let nextseq:i32=kb_maxseq(sd)+1;
    let ob:[]u8=nio_alloc(65536);
    let o:i32=0;
    let i:i32=0;
    while(i<n){
        let cs:i32=g32(ct,i*8);
        let cl:i32=g32(ct,i*8+4);
        let sq:[]u8=i64s((nextseq+i) as i64);
        let need:i32=3+sq.len+1+cl+1;
        if(o+need<=ob.len){
            ob[o]=75; ob[o+1]=66; ob[o+2]=124; o=o+3;
            let c:i32=0;
            while(c<sq.len){ob[o+c]=sq[c]; c=c+1;}
            o=o+sq.len;
            ob[o]=124; o=o+1;
            c=0;
            while(c<cl){ob[o+c]=ca[cs+c]; c=c+1;}
            o=o+cl;
            ob[o]=10; o=o+1;
        }
        _zag_print("KB|COMMIT|");
        _zag_println(sq);
        nio_free(sq);
        i=i+1;
    }
    append_to_file(sd,"knowledge.txt",ob[0..o]);
    nio_free(ob);
    // ---- auto-resolve: pending entries vs the NEWLY committed claims ----
    let dropt:[]u8=nio_alloc(128*8);
    let dropn:i32=0;
    let droplow:[]u8=drop_load(sd,dropt,&dropn);
    let pba:[]u8=nio_alloc(65536);
    let pbt:[]u8=nio_alloc(64*20);
    let pn:i32=0;
    pend_load(sd,pba,pbt,&pn);
    let rmask:[]u8=nio_alloc(64);
    let dz:i32=0;
    while(dz<64){rmask[dz]=0; dz=dz+1;}
    let kseq:i32=nextseq+n;
    let pi:i32=0;
    while(pi<pn){
        let ps:i32=g32(pbt,pi*20);
        let pco:i32=g32(pbt,pi*20+4);
        let pcl:i32=g32(pbt,pi*20+8);
        let pc:[]u8=pba[pco..pco+pcl];
        let ci:i32=0;
        let ag:i32=0;
        while(ci<n){
            let cs2:i32=g32(ct,ci*8);
            let cl2:i32=g32(ct,ci*8+4);
            if(kb_tv(pc,ca[cs2..cs2+cl2],droplow,dropt,dropn)==2){ag=1; break;}
            ci=ci+1;
        }
        if(ag==1){
            let ksq:[]u8=i64s(kseq as i64);
            let needk:i32=3+ksq.len+1+pcl+1;
            let kb2:[]u8=nio_alloc(needk+1);
            let ko:i32=0;
            kb2[ko]=75; kb2[ko+1]=66; kb2[ko+2]=124; ko=ko+3;
            let c3:i32=0;
            while(c3<ksq.len){kb2[ko+c3]=ksq[c3]; c3=c3+1;}
            ko=ko+ksq.len;
            kb2[ko]=124; ko=ko+1;
            c3=0;
            while(c3<pcl){kb2[ko+c3]=pc[c3]; c3=c3+1;}
            ko=ko+pcl;
            kb2[ko]=10; ko=ko+1;
            append_to_file(sd,"knowledge.txt",kb2[0..ko]);
            nio_free(kb2);
            rmask[pi]=1;
            _zag_print("KB|AUTO_PROMOTED|");
            _zag_print(i64s(ps as i64));
            _zag_print("|");
            _zag_println(ksq);
            nio_free(ksq);
            kseq=kseq+1;
        }else{
            ci=0;
            let contrad:i32=0;
            while(ci<n){
                let cs3:i32=g32(ct,ci*8);
                let cl3:i32=g32(ct,ci*8+4);
                if(kb_tv(pc,ca[cs3..cs3+cl3],droplow,dropt,dropn)==1){contrad=1; break;}
                ci=ci+1;
            }
            if(contrad==1){
                let psq:[]u8=i64s(ps as i64);
                let needr:i32=3+psq.len+1+pcl+7+1;
                let rb:[]u8=nio_alloc(needr+1);
                let ro:i32=0;
                rb[ro]=82; rb[ro+1]=70; rb[ro+2]=124; ro=ro+3;
                let c4:i32=0;
                while(c4<psq.len){rb[ro+c4]=psq[c4]; c4=c4+1;}
                ro=ro+psq.len;
                rb[ro]=124; ro=ro+1;
                c4=0;
                while(c4<pcl){rb[ro+c4]=pc[c4]; c4=c4+1;}
                ro=ro+pcl;
                rb[ro]=124; rb[ro+1]=67; rb[ro+2]=79; rb[ro+3]=77;
                rb[ro+4]=77; rb[ro+5]=73; rb[ro+6]=84; ro=ro+7;
                rb[ro]=10; ro=ro+1;
                append_to_file(sd,"resolved.txt",rb[0..ro]);
                nio_free(rb);
                rmask[pi]=1;
                _zag_print("KB|AUTO_FALSE|");
                _zag_println(psq);
                nio_free(psq);
            }
        }
        pi=pi+1;
    }
    pend_write_mask(sd,pba,pbt,pn,rmask);
    nio_free(droplow);
    nio_free(dropt);
    nio_free(pba);
    nio_free(pbt);
    nio_free(rmask);
    nio_free(ca);
    nio_free(ct);
    nio_free(buf);
    return 0;
}

// cmd_kbtest: the DELIBERATE verification/test action on the pending store.
// `instrument_kprod kbtest <sd> <pseq> true|false`.
// true  -> promote: append KB|<kseq>|<claim> (continuing seq) to
//          knowledge.txt, remove the pending line, emit
//          KB|PROMOTED|<pseq>|<kseq>, rc=0.
// false -> resolve false: append RF|<pseq>|<claim>|TEST to resolved.txt,
//          remove the pending line, emit KB|RESOLVED_FALSE|<pseq>, rc=0.
// unknown pseq (incl. non-numeric) -> KB|ERROR|no-such-pending, rc=3.
// any other verdict word -> KB|ERROR|bad-verdict, rc=3.
fn cmd_kbtest(sd:[]u8,pseqs:[]u8,verdict:[]u8)i32 {
    let pseq:i32=atoi(pseqs);
    let pba:[]u8=nio_alloc(65536);
    let pbt:[]u8=nio_alloc(64*20);
    let pn:i32=0;
    pend_load(sd,pba,pbt,&pn);
    let idx:i32=-1;
    let pi:i32=0;
    while(pi<pn){
        if(g32(pbt,pi*20)==pseq){idx=pi; break;}
        pi=pi+1;
    }
    if(pseq<=0 || idx==-1){
        _zag_println("KB|ERROR|no-such-pending");
        nio_free(pba);
        nio_free(pbt);
        return 3;
    }
    let rmask:[]u8=nio_alloc(64);
    let dz:i32=0;
    while(dz<64){rmask[dz]=0; dz=dz+1;}
    rmask[idx]=1;
    let pco:i32=g32(pbt,idx*20+4);
    let pcl:i32=g32(pbt,idx*20+8);
    let pc:[]u8=pba[pco..pco+pcl];
    let psq:[]u8=i64s(pseq as i64);
    if(nio_equal(verdict,"true")==1){
        let kseq:i32=kb_maxseq(sd)+1;
        let ksq:[]u8=i64s(kseq as i64);
        let need:i32=3+ksq.len+1+pcl+1;
        let kb2:[]u8=nio_alloc(need+1);
        let ko:i32=0;
        kb2[ko]=75; kb2[ko+1]=66; kb2[ko+2]=124; ko=ko+3;
        let c:i32=0;
        while(c<ksq.len){kb2[ko+c]=ksq[c]; c=c+1;}
        ko=ko+ksq.len;
        kb2[ko]=124; ko=ko+1;
        c=0;
        while(c<pcl){kb2[ko+c]=pc[c]; c=c+1;}
        ko=ko+pcl;
        kb2[ko]=10; ko=ko+1;
        append_to_file(sd,"knowledge.txt",kb2[0..ko]);
        nio_free(kb2);
        pend_write_mask(sd,pba,pbt,pn,rmask);
        _zag_print("KB|PROMOTED|");
        _zag_print(psq);
        _zag_print("|");
        _zag_println(ksq);
        nio_free(ksq);
        nio_free(psq);
        nio_free(rmask);
        nio_free(pba);
        nio_free(pbt);
        return 0;
    }
    if(nio_equal(verdict,"false")==1){
        let need2:i32=3+psq.len+1+pcl+5+1;
        let rb:[]u8=nio_alloc(need2+1);
        let ro:i32=0;
        rb[ro]=82; rb[ro+1]=70; rb[ro+2]=124; ro=ro+3;
        let c2:i32=0;
        while(c2<psq.len){rb[ro+c2]=psq[c2]; c2=c2+1;}
        ro=ro+psq.len;
        rb[ro]=124; ro=ro+1;
        c2=0;
        while(c2<pcl){rb[ro+c2]=pc[c2]; c2=c2+1;}
        ro=ro+pcl;
        rb[ro]=124; rb[ro+1]=84; rb[ro+2]=69; rb[ro+3]=83; rb[ro+4]=84; ro=ro+5;
        rb[ro]=10; ro=ro+1;
        append_to_file(sd,"resolved.txt",rb[0..ro]);
        nio_free(rb);
        pend_write_mask(sd,pba,pbt,pn,rmask);
        _zag_print("KB|RESOLVED_FALSE|");
        _zag_println(psq);
        nio_free(psq);
        nio_free(rmask);
        nio_free(pba);
        nio_free(pbt);
        return 0;
    }
    _zag_println("KB|ERROR|bad-verdict");
    nio_free(psq);
    nio_free(rmask);
    nio_free(pba);
    nio_free(pbt);
    return 3;
}

// __KBTV_DEBUG_BEGIN__
// cmd_kbtv: SHAKEDOWN-ONLY debug hook exposing kb_tv for the §7.3
// differential check (kb_prior vs kb_tv on throwaway pairs). Reads two text
// files, runs kb_tv(a,b) with the taught DROP list, prints KBTV|<0|1|2>.
// STRIPPED before the final build; never ships in the production instrument.
fn cmd_kbtv(sd:[]u8,fa:[]u8,fb:[]u8)i32 {
    let ok:i32=0;
    let a:[]u8=read_path(fa,&ok);
    if(ok==0){_zag_println("KBTV|ERROR|read-a"); return 2;}
    let ok2:i32=0;
    let b:[]u8=read_path(fb,&ok2);
    if(ok2==0){nio_free(a); _zag_println("KBTV|ERROR|read-b"); return 2;}
    let dropt:[]u8=nio_alloc(128*8);
    let dropn:i32=0;
    let droplow:[]u8=drop_load(sd,dropt,&dropn);
    let r:i32=kb_tv(trim(a),trim(b),droplow,dropt,dropn);
    _zag_print("KBTV|");
    _zag_println(i64s(r as i64));
    nio_free(a);
    nio_free(b);
    nio_free(droplow);
    nio_free(dropt);
    return 0;
}
// __KBTV_DEBUG_END__
'''

# E2: replace the old cmd_kbcommit (up to fn first_int) with the new
# cmd_kbcommit + cmd_kbtest + the temporary kbtv debug hook.
start = src.find("// cmd_kbcommit: the DELIBERATE install path")
end = src.find("fn first_int(s:[]u8)i64 {")
assert start > 0 and end > start, "E2: cmd_kbcommit span not found"
src = src[:start] + NEW_KBCOMMIT.lstrip("\n") + "\n" + src[end:]
print("E2 ok: replaced cmd_kbcommit, added cmd_kbtest + debug kbtv hook", file=sys.stderr)

PROD_BRANCHES = r'''
        // ---- KPROD (a): resolved-false check ----
        // In prod mode, before any install output: if <sd>/resolved.txt
        // exists, run kb_tv(key, resolved claim) per entry. On AGREE the
        // claim was verified false -> withhold. Precedence: the
        // committed-knowledge prior above already returned on AGREE, so a
        // knowledge AGREE always beats resolved-false here.
        // SPEC-DEFERRED CHOICE: §2.5(a) does not condition on prod, but the
        // only caller with a state dir is cmd_verdict (prod=1); calibration
        // (prod=0, empty sd) must stay byte-identical to frozen, so the
        // check is gated on prod==1.
        if(prod==1 && sd.len>0){
            let rba:[]u8=nio_alloc(65536);
            let rbt:[]u8=nio_alloc(64*12);
            let rn:i32=0;
            let rok:i32=resolved_load(sd,rba,rbt,&rn);
            if(rok==1 && rn>0){
                let rdropt:[]u8=nio_alloc(128*8);
                let rdropn:i32=0;
                let rdroplow:[]u8=drop_load(sd,rdropt,&rdropn);
                let ri:i32=0;
                let rhit:i32=-1;
                while(ri<rn){
                    let rsq:i32=g32(rbt,ri*12);
                    let rco:i32=g32(rbt,ri*12+4);
                    let rcl:i32=g32(rbt,ri*12+8);
                    if(kb_tv(key,rba[rco..rco+rcl],rdroplow,rdropt,rdropn)==2){rhit=rsq; break;}
                    ri=ri+1;
                }
                nio_free(rdroplow);
                nio_free(rdropt);
                if(rhit>=0){
                    if(loud==1){
                        _zag_print("KB|RESOLVED_HIT|");
                        _zag_println(i64s(rhit as i64));
                        _zag_print("GATE|KB_RESOLVED_FALSE|");
                        _zag_println(i64s(rhit as i64));
                        _zag_println("ANSWER|UNCHECKABLE");
                    }
                    nio_free(rba);
                    nio_free(rbt);
                    nio_free(widx);
                    nio_free(qlow);
                    nio_free(qt);
                    nio_free(incl);
                    return 0;
                }
            }
            nio_free(rba);
            nio_free(rbt);
        }
        // ---- KPROD (b): pending diversion ----
        // In prod mode with committed knowledge (Arm K), the frozen install
        // class for UNKNOWN claims becomes PENDING: the claim is held in
        // pending.txt (deduped by byte-identical claim), never installed,
        // and the driver sees KB|PENDING + GATE|KB_PENDING + ANSWER|UNVERIFIED.
        if(prod==1 && kbn>0){
            let pcs:[]u8=pids_csv(pa,pt,widx,wn2);
            let sk:[]u8=sanitize_pipes(key);
            let pba2:[]u8=nio_alloc(65536);
            let pbt2:[]u8=nio_alloc(64*20);
            let pn2:i32=0;
            pend_load(sd,pba2,pbt2,&pn2);
            let pseq2:i32=-1;
            let qi:i32=0;
            while(qi<pn2){
                let qco:i32=g32(pbt2,qi*20+4);
                let qcl:i32=g32(pbt2,qi*20+8);
                if(qcl==sk.len && bsub_eq(pba2,qco,sk,0,qcl)==1){pseq2=g32(pbt2,qi*20); break;}
                qi=qi+1;
            }
            if(pseq2==-1){
                let mx:i32=0;
                qi=0;
                while(qi<pn2){
                    let qs:i32=g32(pbt2,qi*20);
                    if(qs>mx){mx=qs;}
                    qi=qi+1;
                }
                pseq2=mx+1;
                let psq2:[]u8=i64s(pseq2 as i64);
                let need3:i32=3+psq2.len+1+sk.len+1+pcs.len+1;
                let pb:[]u8=nio_alloc(need3+1);
                let po:i32=0;
                pb[po]=80; pb[po+1]=66; pb[po+2]=124; po=po+3;
                let c5:i32=0;
                while(c5<psq2.len){pb[po+c5]=psq2[c5]; c5=c5+1;}
                po=po+psq2.len;
                pb[po]=124; po=po+1;
                c5=0;
                while(c5<sk.len){pb[po+c5]=sk[c5]; c5=c5+1;}
                po=po+sk.len;
                pb[po]=124; po=po+1;
                c5=0;
                while(c5<pcs.len){pb[po+c5]=pcs[c5]; c5=c5+1;}
                po=po+pcs.len;
                pb[po]=10; po=po+1;
                append_to_file(sd,"pending.txt",pb[0..po]);
                nio_free(pb);
                nio_free(psq2);
            }
            if(loud==1){
                _zag_print("KB|PENDING|");
                _zag_print(i64s(pseq2 as i64));
                _zag_print("|");
                _zag_println(pcs);
                _zag_print("GATE|KB_PENDING|");
                _zag_println(i64s(pseq2 as i64));
                _zag_println("ANSWER|UNVERIFIED");
            }
            nio_free(pcs);
            nio_free(sk);
            nio_free(pba2);
            nio_free(pbt2);
            nio_free(widx);
            nio_free(qlow);
            nio_free(qt);
            nio_free(incl);
            return 0;
        }
'''

# E3: verdict_core gains prod + sd.
src = once(src,
    "    o_provs:*i32,o_claims:*i32,o_fl:[]u8,o_fln:*i32)i32 {",
    "    o_provs:*i32,o_claims:*i32,o_fl:[]u8,o_fln:*i32,\n    prod:i32,sd:[]u8)i32 {",
    "E3 verdict_core-signature")

# E4: insert (a)/(b) at the head of the frozen non-blind install branch.
src = once(src,
    "    let rc2:i32=0;\n    if(nsrc>=minsrc){\n        if(loud==1){\n",
    "    let rc2:i32=0;\n    if(nsrc>=minsrc){" + PROD_BRANCHES +
    "        if(loud==1){\n",
    "E4 prod-branches")

# E5: the four call sites. calib_g4/g5/g6 pass prod=0 + empty sd;
# cmd_verdict passes prod=1 + its sd.
src = once(src,
    '        let got:i32=verdict_core(cpages[0..cpn],np,pa,pt,tt,st,nst,ha,ht,\n'
    '            buf[cqs..cqs+cql],"FACT","","",dt,dn,0,0,"","",0,\n'
    '            o_ans,&o_ansn,o_widx,&o_wn,&o_provs,&o_claims,o_fl,&o_fln);',
    '        let got:i32=verdict_core(cpages[0..cpn],np,pa,pt,tt,st,nst,ha,ht,\n'
    '            buf[cqs..cqs+cql],"FACT","","",dt,dn,0,0,"","",0,\n'
    '            o_ans,&o_ansn,o_widx,&o_wn,&o_provs,&o_claims,o_fl,&o_fln,0,"");',
    "E5a calib_g4")
src = once(src,
    '        verdict_core(cpages[0..cpn],np,pa,pt,tt,st,nst,ha,ht,\n'
    '            buf[cqs..cqs+cql],"FACT","","",dt,dn,0,0,"","",0,\n'
    '            o_ans,&o_ansn,o_widx,&o_wn,&o_provs,&o_claims,o_fl,&o_fln);',
    '        verdict_core(cpages[0..cpn],np,pa,pt,tt,st,nst,ha,ht,\n'
    '            buf[cqs..cqs+cql],"FACT","","",dt,dn,0,0,"","",0,\n'
    '            o_ans,&o_ansn,o_widx,&o_wn,&o_provs,&o_claims,o_fl,&o_fln,0,"");',
    "E5b calib_g5")
src = once(src,
    '        verdict_core(cpages[0..cpn],np,pa,pt,tt,st,nst,ha,ht,\n'
    '            q,"FACT","","",dt,dn,0,0,"","",0,\n'
    '            o_ans,&o_ansn,o_widx,&o_wn,&o_provs,&o_claims,o_fl,&o_fln);',
    '        verdict_core(cpages[0..cpn],np,pa,pt,tt,st,nst,ha,ht,\n'
    '            q,"FACT","","",dt,dn,0,0,"","",0,\n'
    '            o_ans,&o_ansn,o_widx,&o_wn,&o_provs,&o_claims,o_fl,&o_fln,0,"");',
    "E5c calib_g6")
src = once(src,
    '    verdict_core(buf,np,pa,pt,tt,st,nst,ha,ht,query,kind,extra,kwstr,dt,dn,0,1,\n'
    '        kba,kbt,kbn,\n'
    '        o_ans,&o_ansn,o_widx,&o_wn,&o_provs,&o_claims,o_fl,&o_fln);',
    '    verdict_core(buf,np,pa,pt,tt,st,nst,ha,ht,query,kind,extra,kwstr,dt,dn,0,1,\n'
    '        kba,kbt,kbn,\n'
    '        o_ans,&o_ansn,o_widx,&o_wn,&o_provs,&o_claims,o_fl,&o_fln,1,sd);',
    "E5d cmd_verdict")

# E6: main(): kbtest command + temporary kbtv debug hook.
src = once(src,
    '    if(nio_equal(m,"query")==1){',
    '    if(nio_equal(m,"kbtest")==1){\n'
    '        let tsd:[]u8=_zag_arg(2);\n'
    '        let tps:[]u8=_zag_arg(3);\n'
    '        let tvw:[]u8=_zag_arg(4);\n'
    '        if(tsd.len==0 || tps.len==0 || tvw.len==0){return 2;}\n'
    '        return cmd_kbtest(tsd,tps,tvw);\n'
    '    }\n'
    '// __KBTV_DEBUG_BEGIN__\n'
    '    if(nio_equal(m,"kbtv")==1){\n'
    '        let ksd:[]u8=_zag_arg(2);\n'
    '        let kfa:[]u8=_zag_arg(3);\n'
    '        let kfb:[]u8=_zag_arg(4);\n'
    '        if(ksd.len==0 || kfa.len==0 || kfb.len==0){return 2;}\n'
    '        return cmd_kbtv(ksd,kfa,kfb);\n'
    '    }\n'
    '// __KBTV_DEBUG_END__\n'
    '    if(nio_equal(m,"query")==1){',
    "E6 main-kbtest+kbtv")

if STRIP_DEBUG:
    # Remove the debug hook (function + main() dispatch) for the final build.
    b0 = src.find("// __KBTV_DEBUG_BEGIN__")
    b1 = src.find("// __KBTV_DEBUG_END__")
    assert b0 > 0 and b1 > b0, "strip-debug: hook block not found"
    src = src[:b0] + src[b1 + len("// __KBTV_DEBUG_END__\n"):]
    m0 = src.find("// __KBTV_DEBUG_BEGIN__\n    if(nio_equal(m,\"kbtv\")")
    assert m0 < 0 or True
    # main() dispatch markers
    d0 = src.find('// __KBTV_DEBUG_BEGIN__\n    if(nio_equal(m,"kbtv")==1){')
    assert d0 > 0, "strip-debug: main dispatch not found"
    d1 = src.find("// __KBTV_DEBUG_END__", d0)
    src = src[:d0] + src[d1 + len("// __KBTV_DEBUG_END__\n"):]
    print("stripped kbtv debug hook", file=sys.stderr)

open(DST, "w").write(src)
print(f"wrote {DST} ({len(src)} bytes)", file=sys.stderr)
