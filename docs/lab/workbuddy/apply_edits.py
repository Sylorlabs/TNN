#!/usr/bin/env python3
"""Reconstruct the WB-LEARN workbuddy source from frozen round-4 dialogue.zag.

Applies, in one pass, the five native-mechanism edits developed 2026-09-27:
  A. WB-LEARN block before fn do_turn:
     is_teach_shape (declarative-shape gate), session_teach (session facts
     via the same ingestion as KB facts), stdin_line, is_mem_scaffold,
     tok_in_span, mem_answer (content-word + tell/ask selection).
     Placed BEFORE do_turn but mem_answer is defined AFTER is_teach_shape
     (all calls backward -- znc miscompiles forward references into a
     globally corrupt binary; see lesson below).
     The original mem_answer is removed (D).
  B. 4b hook in section 4 of do_turn: unparsed declarative turns are taught
     as session facts ("Noted.").
  C. chat branch in main: argv[1]=="chat" runs a persistent stdin/stdout
     session; one process = one session; batch mode untouched.
  D. Original mem_answer removed (redefined in the WB block).
  E. is_teach_shape imperative exclusions (task verbs are not teachings).

Usage: apply_edits.py <path-to-dialogue.zag>
Rewrites the file in place.
"""
import sys

SRC = sys.argv[1]
s = open(SRC).read()

def rep(old, new, name):
    global s
    assert s.count(old) == 1, f'anchor not unique/found for {name}: count={s.count(old)}'
    s = s.replace(old, new)
    print('applied', name, flush=True)

WB = '''// ================= WB-LEARN: session teaching (2026-09-27) ================
// A declarative user turn the assertion path cannot parse is taught as a
// SESSION fact through the SAME ingestion as KB facts (proc_sentence +
// gaz_scan + extract_unit + 40-byte fm record). Session facts live in fm
// after the KB facts with fids 100000+, so retrieval, G6, negation, yes/no
// and provenance all consult them with zero changes. Session scope only:
// the process owns them; a new process starts with KB facts alone (no
// persistence -- the grow-with-me prereg governs cross-session learning).
// This is a general mechanism (any declarative sentence), not a per-item
// patch: the shape test below is grammatical mood (declarative vs
// interrogative/imperative), never content.

// is_teach_shape: 1 iff the turn reads as a declarative statement.
// Excludes interrogatives (wh-words, auxiliary inversion -- the same class
// cmp_yesno detects) and leading imperatives (requests, not teachings).
fn is_teach_shape(ubuf:[]u8,uo:i32,ul:i32)i32 {
    if(ul<=0){ return 0; }
    if(starts_with(ubuf,uo,ul,"who ",4)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"what ",5)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"when ",5)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"where ",6)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"why ",4)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"how ",4)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"which ",6)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"whom ",5)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"whose ",6)==1){ return 0; }
    if(cmp_yesno(ubuf,uo,ul)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"tell ",5)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"give ",5)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"show ",5)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"list ",5)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"explain ",8)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"describe ",9)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"summarize ",10)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"draft ",6)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"write ",6)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"name ",5)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"review ",7)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"check ",6)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"audit ",6)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"verify ",7)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"find ",5)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"identify ",9)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"compare ",8)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"analyze ",8)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"analyse ",8)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"assess ",7)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"evaluate ",9)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"critique ",9)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"edit ",5)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"fix ",4)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"create ",7)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"make ",5)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"generate ",9)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"produce ",8)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"provide ",8)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"suggest ",8)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"recommend ",10)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"outline ",8)==1){ return 0; }
    if(starts_with(ubuf,uo,ul,"plan ",5)==1){ return 0; }
    return 1;
}

// session_teach: ingest one lowercased teaching sentence as a session fact.
// Mirrors kb_install's per-fact block exactly. Returns 1 on install,
// 0 when an arena has no room (principled capacity: physical arena bounds,
// not a tuned constant).
fn session_teach(fm:[]u8,ftx:[]u8,ftl:[]u8,fea:[]u8,vbytes:[]u8,vent:[]u8,linka:[]u8,keya:[]u8,gnames:[]u8,ge:[]u8,gord:[]u8,tmp:[]u8,kid:[]u8,trb:[]u8,st:[]u8,out:[]u8,eout:[]u8,sbuf:[]u8,so:i32,sl:i32)i32 {
    let nf:i32=g32(fm,0) as i32;
    if(8+(nf+1)*40>8192){ return 0; }
    if((g32(ftx,0) as i32)+sl>8192){ return 0; }
    if((g32(fea,0) as i32)+256>4096){ return 0; }
    let si:i32=0;
    let fx:i32=0;
    while(fx<nf){
        if((g32(fm,8+fx*40) as i32)>=100000){ si=si+1; }
        fx=fx+1;
    }
    let fid:i32=100000+si;
    let to:i32=g32(ftx,0) as i32;
    copy_bytes(ftx,to,sbuf,so,sl);
    let lc:i32=0;
    while(lc<sl){ ftl[to+lc]=sbuf[so+lc]; lc=lc+1; }
    p32(ftx,0,to+sl);
    p32(ftl,0,to+sl);
    p32(linka,0,8);
    zero40(st);
    proc_sentence(vbytes,vent,sbuf,so,sl,tmp,kid,linka,keya,trb,st,out);
    let ko:i32=g32(out,8) as i32;
    let kl:i32=g32(out,12) as i32;
    let val:i64=g64(out,16) as i32;
    let eo:i32=g32(fea,0) as i32;
    let ne:i32=gaz_scan(gnames,ge,gord,ftl,to,sl,eout,-1);
    let k2:i32=0;
    while(k2<ne){ p32(fea,eo+k2*4,g32(eout,k2*4)); k2=k2+1; }
    p32(fea,0,eo+ne*4);
    let ro:i32=8+nf*40;
    p32(fm,ro,fid); p32(fm,ro+4,ko); p32(fm,ro+8,kl); p32(fm,ro+12,val);
    p32(fm,ro+16,to); p32(fm,ro+20,sl); p32(fm,ro+24,eo); p32(fm,ro+28,ne);
    let uu:i64=extract_unit(ftx,ftl,to,sl,val);
    p32(fm,ro+32,(uu>>32) as i32); p32(fm,ro+36,(uu & 4294967295) as i32);
    p32(fm,0,nf+1);
    return 1;
}

// stdin_line: read one line from fd 0 into buf (max bytes). Returns the
// length, or -1 on EOF (no bytes read at all). Strips a trailing CR.
fn stdin_line(buf:[]u8,max:i32)i32 {
    let n:i32=0;
    let any:i32=0;
    let one:[]u8=nio_alloc(1);
    let go:i32=1;
    while(go==1){
        let r:i64=_zag_raw_syscall(0,0,(_zag_slice_ptr(one) as i64),1,0,0,0);
        if(r==-4){ go=1; }
        else {
            if(r<=0){ go=0; }
            else {
                any=1;
                let c:u8=one[0];
                if(c==10){ go=0; }
                else {
                    if(n<max){ buf[n]=c; n=n+1; }
                }
            }
        }
    }
    nio_free(one);
    if(any==0){ return -1; }
    if(n>0 && buf[n-1]==13){ n=n-1; }
    return n;
}

// is_mem_scaffold: 1 iff the token is memory-discourse scaffolding rather
// than a content word the user is asking about. Closed grammatical class:
// stopwords plus the memory verbs/markers. General, never content.
fn is_mem_scaffold(sb:[]u8,so:i32,sl:i32)i32 {
    if(is_stop(sb,so,sl)==1){ return 1; }
    if(beq(sb,so,sl,"tell")==1){ return 1; }
    if(beq(sb,so,sl,"told")==1){ return 1; }
    if(beq(sb,so,sl,"ask")==1){ return 1; }
    if(beq(sb,so,sl,"asked")==1){ return 1; }
    if(beq(sb,so,sl,"say")==1){ return 1; }
    if(beq(sb,so,sl,"said")==1){ return 1; }
    if(beq(sb,so,sl,"remember")==1){ return 1; }
    if(beq(sb,so,sl,"recall")==1){ return 1; }
    if(beq(sb,so,sl,"about")==1){ return 1; }
    if(beq(sb,so,sl,"my")==1){ return 1; }
    if(beq(sb,so,sl,"question")==1){ return 1; }
    if(beq(sb,so,sl,"mention")==1){ return 1; }
    if(beq(sb,so,sl,"mentioned")==1){ return 1; }
    return 0;
}
// tok_in_span: token-exact search of lit[lo,lo+ll) inside buf[bo,bo+bl).
fn tok_in_span(buf:[]u8,bo:i32,bl:i32,lit:[]u8,lo:i32,ll:i32)i32 {
    let i:i32=0;
    while(i<bl){
        while(i<bl && is_alnum(buf[bo+i])==0){ i=i+1; }
        if(i<bl){
            let ts:i32=i;
            while(i<bl && is_alnum(buf[bo+i])==1){ i=i+1; }
            if(i-ts==ll && beq2(buf,bo+ts,lit,lo,ll)==1){ return 1; }
        }
    }
    return 0;
}
// mem_answer (2026-09-27, WB-LEARN): placed after is_teach_shape so every
// call is backward. Adds content-word selection -- "what did i tell you
// about FI1?" selects the most recent user turn containing a content word
// instead of blindly quoting the last turn -- with a tell/say vs ask shape
// preference (teachings for "tell me", questions for "ask me").
fn mem_answer(resp:[]u8,ubuf:[]u8,uo:i32,ul:i32,hist:[]u8,histb:[]u8)void {
    let n:i32=g32(hist,0) as i32;
    let c:i32=0;
    let hx:i32=0;
    while(hx<n-1){
        if((g32(hist,4+hx*12) as i32)==0){ c=c+1; }
        hx=hx+1;
    }
    if(c==0){
        let nm:[]u8="You haven't asked anything before this.";
        rput(resp,nm,0,nm.len);
        return;
    }
    let sel:i32=c-1;
    let done:i32=0;
    if(tok_has(ubuf,uo,ul,"first")==1){ sel=0; done=1; }
    if(done==0 && tok_has(ubuf,uo,ul,"last")==1){ done=1; }
    if(done==0 && tok_has(ubuf,uo,ul,"previous")==1){ done=1; }
    if(done==0 && tok_has(ubuf,uo,ul,"latest")==1){ done=1; }
    if(done==0){
        let on:i32=mem_ord(ubuf,uo,ul);
        if(on>0 && on<=c){ sel=on-1; done=1; }
    }
    if(done==0){
        let want_teach:i32=0;
        if(tok_has(ubuf,uo,ul,"tell")==1){ want_teach=1; }
        if(tok_has(ubuf,uo,ul,"told")==1){ want_teach=1; }
        if(tok_has(ubuf,uo,ul,"say")==1){ want_teach=1; }
        if(tok_has(ubuf,uo,ul,"said")==1){ want_teach=1; }
        let found:i32=0;
        let pass:i32=0;
        while(pass<2 && found==0){
            let qi:i32=0;
            while(qi<ul && found==0){
                while(qi<ul && is_alnum(ubuf[uo+qi])==0){ qi=qi+1; }
                if(qi<ul){
                    let qs:i32=qi;
                    while(qi<ul && is_alnum(ubuf[uo+qi])==1){ qi=qi+1; }
                    let ql:i32=qi-qs;
                    if(is_mem_scaffold(ubuf,uo+qs,ql)==0){
                        let hx2:i32=n-2;
                        while(hx2>=0 && found==0){
                            if((g32(hist,4+hx2*12) as i32)==0){
                                let ho2:i32=g32(hist,4+hx2*12+4) as i32;
                                let hl2:i32=g32(hist,4+hx2*12+8) as i32;
                                let shape_ok:i32=0;
                                if(pass==1){ shape_ok=1; }
                                else {
                                    if(is_teach_shape(histb,ho2,hl2)==want_teach){ shape_ok=1; }
                                }
                                if(shape_ok==1 && tok_in_span(histb,ho2,hl2,ubuf,uo+qs,ql)==1){
                                    let s2:i32=0;
                                    let h3:i32=0;
                                    while(h3<hx2){
                                        if((g32(hist,4+h3*12) as i32)==0){ s2=s2+1; }
                                        h3=h3+1;
                                    }
                                    sel=s2; found=1;
                                }
                            }
                            hx2=hx2-1;
                        }
                    }
                }
            }
            pass=pass+1;
        }
        if(found==1){ done=1; }
    }
    let seen:i32=0;
    let row:i32=-1;
    hx=0;
    while(hx<n-1){
        if((g32(hist,4+hx*12) as i32)==0){
            if(seen==sel){ row=hx; }
            seen=seen+1;
        }
        hx=hx+1;
    }
    if(row<0){ row=n-2; }
    let ho:i32=g32(hist,4+row*12+4) as i32;
    let hl:i32=g32(hist,4+row*12+8) as i32;
    let pre:[]u8="You asked: ";
    rput(resp,pre,0,pre.len);
    rput(resp,histb,ho,hl);
    return;
}

'''

# Edit A: WB-LEARN block before fn do_turn
rep('''//           (one-turn) dim@56 (write-only) turn@60 ---
fn do_turn(''',
'''//           (one-turn) dim@56 (write-only) turn@60 ---
''' + WB + '''fn do_turn(''', 'A: WB-LEARN block')

# Edit B: 4b hook in section 4
rep('''            p32(pv,32,0);
            return -1;
        }
    }
    // ---- 5. default: reference resolution + v1 retrieval ----''',
'''            p32(pv,32,0);
            return -1;
        }
        // ---- 4b. WB-LEARN: session teaching ----
        // A declarative turn the assertion path cannot parse (unknown
        // entity or relation shape) is taught as a session fact through
        // session_teach -- the same ingestion KB facts get. It becomes
        // retrievable, withhold-gated, and negatable like any taught fact,
        // for the rest of this session only.
        if(is_teach_shape(ubuf,uo,ul)==1){
            let okw:i32=session_teach(fm,ftx,ftl,fea,vbytes,vent,linka,keya,gnames,ge,gord,tmp,kid,trb,st,out,eout,ubuf,uo,ul);
            rclr(resp);
            if(okw==1){ rput(resp,"Noted.",0,6); }
            else { rput(resp,"My session notes are full.",0,25); }
            let nea2:i32=gaz_scan(gnames,ge,gord,ubuf,uo,ul,eout,-1);
            push_ents(sal,eout,nea2);
            p32(pv,0,-1); p32(pv,4,-1); p32(pv,8,-1); p32(pv,28,1);
            p32(pv,32,0);
            p32(novelf,0,0);
            return -1;
        }
    }
    // ---- 5. default: reference resolution + v1 retrieval ----''', 'B: 4b hook')

# Edit C: chat branch in main
rep('''    pr("KB "); prn(nf as i64); pr(" ENT "); prn(g32(ge,0) as i64); prl("");
    let bat:[]u8=read_all("battery.txt");''',
'''    pr("KB "); prn(nf as i64); pr(" ENT "); prn(g32(ge,0) as i64); prl("");
    // ---- WB-LEARN: interactive chat mode (2026-09-27) ----
    // argv[1]=="chat": persistent stdin/stdout conversation. One process =
    // one session: history, salience, and session-taught facts live in
    // process memory and evaporate on exit (no cross-session persistence).
    // Batch mode below is untouched.
    let a1:[]u8=_zag_arg(1);
    if(a1.len==4 && beq(a1,0,4,"chat")==1){
        p32(sal,0,0); p32(top,0,0); p32(uc,0,0); p32(hist,0,0); p32(pqb,0,8); p32(histb,0,8);
        p32(pv,0,-1); p32(pv,28,1); p32(pv,64,0);
        let last_fid_c:i32=-1;
        let turn_c:i32=0;
        let line:[]u8=nio_alloc(4096);
        let go_c:i32=1;
        while(go_c==1){
            let ll:i32=stdin_line(line,4096);
            if(ll<0){ go_c=0; }
            else {
                if(ll>0){
                    turn_c=turn_c+1;
                    let k5:i32=0;
                    while(k5<ll){ ubuf[k5]=to_low(line[k5]); k5=k5+1; }
                    hist_add(hist,histb,0,ubuf,0,ll);
                    last_fid_c=do_turn(ubuf,0,ll,turn_c,sal,top,uc,pv,pqb,fm,fea,ftx,ftl,keya,kid,vbytes,vent,linka,tmp,trb,st,out,gnames,ge,gord,resp,hist,histb,eout,eout2,bout,qbuf,abuf,nbuf,novelf,last_fid_c,fout);
                    let rl3:i32=g32(resp,0) as i32;
                    hist_add(hist,histb,1,resp,4,rl3);
                    pr("A ");
                    prlen(resp[4..4+rl3],rl3);
                    prl("");
                }
            }
        }
        nio_free(line);
        return;
    }
    let bat:[]u8=read_all("battery.txt");''', 'C: chat branch')

# Edit D: remove original mem_answer (redefined in the WB block)
start = s.index('fn mem_answer(resp:[]u8,ubuf:[]u8,uo:i32,ul:i32,hist:[]u8,histb:[]u8)void {')
endmark = '// --- F1-COMPARE (2026-09-23): general comparison engine ---'
end = s.index(endmark)
s = s[:start] + s[end:]
print('applied D: removed original mem_answer, redefined in WB block', flush=True)

open(SRC, 'w').write(s)
print('OK, final size', len(s), flush=True)
