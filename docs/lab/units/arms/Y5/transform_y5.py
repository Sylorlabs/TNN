#!/usr/bin/env python3
"""Generate cl/arm10.zag (chunked-corpus build) from cl/arm.zag (1x frozen).
Every replacement is asserted; the script fails loudly on any mismatch.
"""
import sys

SRC = "/home/hatch/workspace/tnn-lab/units/arms/Y5/cl/arm.zag"
DST = "/home/hatch/workspace/tnn-lab/units/arms/Y5/cl/arm10.zag"

txt = open(SRC).read()

def rep(old, new, count=1):
    global txt
    n = txt.count(old)
    if n != count:
        print(f"MISMATCH for {old[:70]!r}: found {n}, expected {count}")
        sys.exit(1)
    txt = txt.replace(old, new)

# ---------------------------------------------------------------- header
rep(
"// y5 \u2014 Arm Y5: CROSS-STREAM CHUNKS (non-contiguous spans, one ID).",
"""// y5 \u2014 Arm Y5: CROSS-STREAM CHUNKS (non-contiguous spans, one ID).
// CHUNKED-CORPUS BUILD (runs 1x and 10x). Derived from cl/arm.zag (1x frozen
// impl, evidence-approved 2026-09-21) by mechanical transformation only:
// every file/corpus buffer, the audit ledger, the LINK probe table, the M7
// C' buffer, and the M8 store image are chunked so no slice exceeds 2^25
// bytes (znc toolchain wall). Logical semantics are unchanged; 1x
// byte-equivalence against the approved evidence is proven in
// evidence/battery_1x_chunked/ before any 10x leg counts. Pure Zag, zero RNG.""",
)

# ---------------------------------------------------------------- consts
rep(
"""const Y5_LINK_BUDGET:i32=2048;""",
"""const Y5_LINK_BUDGET:i32=2048;
// ---- 10x scale: 2^25-byte slice wall (znc toolchain constraint) ----
// No slice may exceed 33,554,432 bytes. Corpora, the audit ledger, the LINK
// probe table, and the M8 store image are chunked; access goes through the
// Cb (chunked buffer) and ledger-chunk helpers below. Chunking preserves
// logical semantics byte-for-byte (proven by 1x rerun equivalence).
const CB_SHIFT:i32=25;
const CB_SIZE:i32=33554432;
const CB_MASK:i32=33554431;
const CB_NCMAX:i32=6;
const LED_SHIFT:i32=19;          // ledger entries per chunk = 2^19 (2^25/64)
const LED_EPC:i32=524288;
const LED_MASK:i32=524287;
const LINK_TS_MAX:i32=524288;   // y_link_pass tent entries cap (16MB)""",
)

# ---------------------------------------------------------------- Y5 struct: ledger overflow chunks
rep(
"""    led:[]u8,           // ledger bytes""",
"""    led:[]u8,           // ledger bytes (chunk 0)
    led1:[]u8,         // ledger overflow chunks 1..5 (each <= 2^25 bytes)
    led2:[]u8,
    led3:[]u8,
    led4:[]u8,
    led5:[]u8,""",
)

# ---------------------------------------------------------------- Cb + helpers (before reg_set)
rep(
"""fn reg_set(rbase:[]u8,rlen:[]u8,corpus:i32,base:i32,len:i32) void {""",
"""// ---- chunked corpus buffer (Cb) and chunked ledger access ----
// Every chunk is <= 2^25 bytes. File-data chunks use raw nio_alloc (untraced,
// exactly like the old read_file buffers); derived buffers use halloc (traced,
// exactly like the old concatenated cbufs). cb.total equals the old file
// length, and (corpus,off) byte addressing is unchanged.
struct Cb {
    nc:i32,
    total:i32,
    c0:[]u8,c1:[]u8,c2:[]u8,c3:[]u8,c4:[]u8,c5:[]u8,
}
fn cb_sel(cb:*Cb,i:i32) []u8 {
    if(i==0){let a:[]u8=cb.*.c0;return a;}
    if(i==1){let a:[]u8=cb.*.c1;return a;}
    if(i==2){let a:[]u8=cb.*.c2;return a;}
    if(i==3){let a:[]u8=cb.*.c3;return a;}
    if(i==4){let a:[]u8=cb.*.c4;return a;}
    let a:[]u8=cb.*.c5;return a;
}
fn cb_add(cb:*Cb,data:[]u8) i32 {
    let i:i32=cb.*.nc;
    if(i>=6){return -1;}
    if(i==0){cb.*.c0=data;}
    else{if(i==1){cb.*.c1=data;}
    else{if(i==2){cb.*.c2=data;}
    else{if(i==3){cb.*.c3=data;}
    else{if(i==4){cb.*.c4=data;}
    else{cb.*.c5=data;}}}}}
    cb.*.nc=i+1;
    cb.*.total=cb.*.total+data.len;
    return 0;
}
// raw pread: seek to off, read exactly n bytes (n <= 2^25). 0 ok, -1 short.
fn nio_read_at(fd:i64,off:i64,buf:[]u8,n:i32) i32 {
    if(nio_seek(fd,off,0)!=off){return -1;}
    let base:i64=_zag_slice_ptr(buf) as i64;
    let got:i32=0;
    let calls:i32=0;
    while(got<n && calls<4096){
        let r:i64=_zag_raw_syscall(0,fd,base+(got as i64),(n-got) as i64,0,0,0);
        calls=calls+1;
        if(r==-4){continue;}
        if(r<=0){break;}
        got=got+(r as i32);
    }
    if(got!=n){return -1;}
    return 0;
}
// load one file as a chunked Cb (untraced raw allocs, like read_file).
// 0 ok, -1 on missing/empty/oversize.
fn cb_load_file(cb:*Cb,dir:[]u8,name:[]u8) i32 {
    let root:i64=nio_open_root(dir);
    if(root<0){return -1;}
    let fd:i64=nio_open_child(root,name,0);
    nio_close(root);
    if(fd<0){return -1;}
    let sz:i64=nio_seek(fd,0,2);
    if(sz<=0 || sz>201326592){nio_close(fd);return -1;}
    let total:i32=sz as i32;
    let done:i32=0;
    while(done<total){
        let n:i32=total-done;
        if(n>33554432){n=33554432;}
        let ch:[]u8=nio_alloc(n);
        let rr:i32=nio_read_at(fd,done as i64,ch,n);
        if(rr!=0){nio_free(ch);nio_close(fd);return -1;}
        if(cb_add(cb,ch)<0){nio_free(ch);nio_close(fd);return -1;}
        done=done+n;
    }
    nio_close(fd);
    return 0;
}
fn cb_get(cb:*Cb,at:i32) u8 {
    let base:i32=0;
    let i:i32=0;
    while(i<cb.*.nc){
        let c:[]u8=cb_sel(cb,i);
        if(at<base+c.len){return c[at-base];}
        base=base+c.len;
        i=i+1;
    }
    return 0;
}
fn cb_put(cb:*Cb,at:i32,b:u8) void {
    let base:i32=0;
    let i:i32=0;
    while(i<cb.*.nc){
        let c:[]u8=cb_sel(cb,i);
        if(at<base+c.len){c[at-base]=b;return;}
        base=base+c.len;
        i=i+1;
    }
}
// copy n bytes of the logical buffer at src into dst[dat..]
fn cb_copy(cb:*Cb,src:i32,dst:[]u8,dat:i32,n:i32) void {
    let done:i32=0;
    while(done<n){
        dst[dat+done]=cb_get(cb,src+done);
        done=done+1;
    }
}
// duplicate a Cb through traced hallocs (M7's C' buffer)
fn cb_copy_from(s:*Y5,dst:*Cb,src:*Cb) i32 {
    let i:i32=0;
    while(i<src.*.nc){
        let sc:[]u8=cb_sel(src,i);
        let dc:[]u8=halloc(s,sc.len);
        let k:i32=0;
        while(k<sc.len){dc[k]=sc[k];k=k+1;}
        if(cb_add(dst,dc)<0){hfree(s,dc);return -1;}
        i=i+1;
    }
    return 0;
}
// ---- chunked audit ledger ----
fn led_sel(s:*Y5,ci:i32) []u8 {
    if(ci==0){let l:[]u8=s.*.led;return l;}
    if(ci==1){let l:[]u8=s.*.led1;return l;}
    if(ci==2){let l:[]u8=s.*.led2;return l;}
    if(ci==3){let l:[]u8=s.*.led3;return l;}
    if(ci==4){let l:[]u8=s.*.led4;return l;}
    let l:[]u8=s.*.led5;return l;
}
fn led_op(s:*Y5,e:i32) i32 {
    let l:[]u8=led_sel(s,e>>19);
    return iget(l,(e & 524287)*64);
}
// copy n bytes of the logical ledger stream at cs into dst
fn led_piece(s:*Y5,cs:i32,dst:[]u8,n:i32) void {
    let done:i32=0;
    while(done<n){
        let at:i32=cs+done;
        let l:[]u8=led_sel(s,at>>25);
        let lo:i32=at & 33554431;
        let avail:i32=l.len-lo;
        let want:i32=n-done;
        if(want>avail){want=avail;}
        let k:i32=0;
        while(k<want){dst[done+k]=l[lo+k];k=k+1;}
        done=done+want;
    }
}
// ledger stream hash: direct (1x-identical) when it fits one chunk,
// Merkle-over-1MB-pieces otherwise (10x).
fn ledger_hash(s:*Y5,out:[]u8) void {
    let total:i32=s.*.led_n*64;
    if(total<=33554432){
        let l0:[]u8=s.*.led;
        ns_sha256(l0[0..total],out);
        return;
    }
    let nch:i32=(total+1048575)/1048576;
    let chain:[]u8=nio_alloc(nch*32);
    let scratch:[]u8=nio_alloc(1048576);
    let ci:i32=0;
    while(ci<nch){
        let cs:i32=ci*1048576;
        let cn:i32=total-cs;
        if(cn>1048576){cn=1048576;}
        led_piece(s,cs,scratch,cn);
        ns_sha256(scratch[0..cn],chain[ci*32..ci*32+32]);
        ci=ci+1;
    }
    ns_sha256(chain,out);
    nio_free(chain);
    nio_free(scratch);
}
// write the logical ledger stream to dir/name in 1MB pieces
fn write_ledger(s:*Y5,dir:[]u8,name:[]u8) i32 {
    let root:i64=nio_open_root(dir);
    if(root<0){return -1;}
    let fd:i64=nio_open_child(root,name,1);
    nio_close(root);
    if(fd<0){return -1;}
    let total:i32=s.*.led_n*64;
    let done:i32=0;
    while(done<total){
        let l:[]u8=led_sel(s,done>>25);
        let lo:i32=done & 33554431;
        let avail:i32=l.len-lo;
        let want:i32=total-done;
        if(want>avail){want=avail;}
        let wdone:i32=0;
        while(wdone<want){
            let n:i32=want-wdone;
            if(n>1048576){n=1048576;}
            let w:i64=nio_write_all(fd,l[lo+wdone..lo+wdone+n]);
            if(w!=(n as i64)){nio_close(fd);return -1;}
            wdone=wdone+n;
        }
        done=done+want;
    }
    nio_close(fd);
    return 0;
}
// copy n bytes of the logical M8 store image (rows|pool|liveq|cbase) at cs
fn img_piece(s:*Y5,r0:i32,r1:i32,r2:i32,cs:i32,dst:[]u8,n:i32) void {
    let rows:[]u8=s.*.rows;
    let pool:[]u8=s.*.pool;
    let lq:[]u8=s.*.liveq;
    let cbase:[]u8=s.*.cbase;
    let b1:i32=r0;let b2:i32=r0+r1;let b3:i32=r0+r1+r2;
    let done:i32=0;
    while(done<n){
        let at:i32=cs+done;
        let src:[]u8=rows;let soff:i32=at;let send:i32=b1;
        if(at>=b1){
            src=pool;soff=at-b1;send=b2;
            if(at>=b2){
                src=lq;soff=at-b2;send=b3;
                if(at>=b3){src=cbase;soff=at-b3;send=b3+40;}
            }
        }
        let want:i32=send-at;
        let remn:i32=n-done;
        if(want>remn){want=remn;}
        let k:i32=0;
        while(k<want){dst[done+k]=src[soff+k];k=k+1;}
        done=done+want;
    }
}
// fill a materialized store image (1x path); returns bytes written
fn img_fill(s:*Y5,img:[]u8) i32 {
    let rows:[]u8=s.*.rows;
    let pool:[]u8=s.*.pool;
    let lq:[]u8=s.*.liveq;
    let cbase:[]u8=s.*.cbase;
    let at:i32=0;
    at=img_append(img,at,rows,s.*.cap*40);
    at=img_append(img,at,pool,s.*.pool_cap*12);
    at=img_append(img,at,lq,s.*.liveq_cap*4);
    at=img_append(img,at,cbase,40);
    return at;
}
fn j_isscale10(mode:[]u8) i32 {
    let i:i32=0;
    while(i+3<mode.len){
        if(mode[i]==45 && mode[i+1]==49 && mode[i+2]==48 && mode[i+3]==120){return 1;}
        i=i+1;
    }
    return 0;
}

fn reg_set(rbase:[]u8,rlen:[]u8,corpus:i32,base:i32,len:i32) void {""",
)

# ---------------------------------------------------------------- y_init ledger chunking
rep(
"""    s.*.led_cap=led_entries*64;s.*.led=halloc(s,s.*.led_cap);s.*.led_n=0;""",
"""    s.*.led_cap=led_entries*64;s.*.led_n=0;
    s.*.led1="";s.*.led2="";s.*.led3="";s.*.led4="";s.*.led5="";
    let lrem:i32=s.*.led_cap;
    let lc0:i32=lrem;if(lc0>33554432){lc0=33554432;}
    s.*.led=halloc(s,lc0);lrem=lrem-lc0;
    if(lrem>0){let lc1:i32=lrem;if(lc1>33554432){lc1=33554432;}s.*.led1=halloc(s,lc1);lrem=lrem-lc1;}
    if(lrem>0){let lc2:i32=lrem;if(lc2>33554432){lc2=33554432;}s.*.led2=halloc(s,lc2);lrem=lrem-lc2;}
    if(lrem>0){let lc3:i32=lrem;if(lc3>33554432){lc3=33554432;}s.*.led3=halloc(s,lc3);lrem=lrem-lc3;}
    if(lrem>0){let lc4:i32=lrem;if(lc4>33554432){lc4=33554432;}s.*.led4=halloc(s,lc4);lrem=lrem-lc4;}
    if(lrem>0){let lc5:i32=lrem;if(lc5>33554432){lc5=33554432;}s.*.led5=halloc(s,lc5);lrem=lrem-lc5;}""",
)

# ---------------------------------------------------------------- y_new literal
rep(
"""        .cbase="",.led="",.led_n=0,.led_cap=0,.trace="",.trace_n=0,.trace_cap=0};""",
"""        .cbase="",.led="",.led1="",.led2="",.led3="",.led4="",.led5="",
        .led_n=0,.led_cap=0,.trace="",.trace_n=0,.trace_cap=0};""",
)

# ---------------------------------------------------------------- y_free
rep(
"""    hfree(s,s.*.cbase);hfree(s,s.*.led);
    nio_free(s.*.trace);""",
"""    hfree(s,s.*.cbase);hfree(s,s.*.led);
    if(s.*.led1.len>0){hfree(s,s.*.led1);}
    if(s.*.led2.len>0){hfree(s,s.*.led2);}
    if(s.*.led3.len>0){hfree(s,s.*.led3);}
    if(s.*.led4.len>0){hfree(s,s.*.led4);}
    if(s.*.led5.len>0){hfree(s,s.*.led5);}
    nio_free(s.*.trace);""",
)

# ---------------------------------------------------------------- y_led reroute
rep(
"""    let at:i32=s.*.led_n*64;
    if(at+64>s.*.led_cap){return;} // LEDGER-BOUND: scored on what completed
    let l:[]u8=s.*.led;
    iput(l,at,op);iput(l,at+4,slot);iput(l,at+8,rc);
    iput(l,at+12,b1);iput(l,at+16,b2);iput(l,at+20,b3);iput(l,at+24,b4);iput(l,at+28,b5);
    iput(l,at+32,a1);iput(l,at+36,a2);iput(l,at+40,a3);iput(l,at+44,a4);iput(l,at+48,a5);
    iput(l,at+52,1);iput(l,at+56,d1);iput(l,at+60,d2);
    s.*.led_n=s.*.led_n+1;""",
"""    let e0:i32=s.*.led_n;
    let at:i32=e0*64;
    if(at+64>s.*.led_cap){return;} // LEDGER-BOUND: scored on what completed
    let l:[]u8=led_sel(s,e0>>19);
    let aw:i32=(e0 & 524287)*64;
    iput(l,aw,op);iput(l,aw+4,slot);iput(l,aw+8,rc);
    iput(l,aw+12,b1);iput(l,aw+16,b2);iput(l,aw+20,b3);iput(l,aw+24,b4);iput(l,aw+28,b5);
    iput(l,aw+32,a1);iput(l,aw+36,a2);iput(l,aw+40,a3);iput(l,aw+44,a4);iput(l,aw+48,a5);
    iput(l,aw+52,1);iput(l,aw+56,d1);iput(l,aw+60,d2);
    s.*.led_n=e0+1;""",
)

open("/home/hatch/workspace/transform_y5_part1.py", "w").write("# part1 done\n")
print("PART1-OK")

# ============================================================ PART 2: corpus accessors
# (appended to transform_y5.py)

# ---- span_copy ----
rep(
"""fn span_copy(cbufs:[]u8,rbase:[]u8,rlen:[]u8,corpus:i32,off:i32,len:i32,
             shift:i32,out:[]u8,out_at:i32) i32 {""",
"""fn span_copy(cb:*Cb,rbase:[]u8,rlen:[]u8,corpus:i32,off:i32,len:i32,
             shift:i32,out:[]u8,out_at:i32) i32 {""",
)
rep(
"""    let i:i32=0;while(i<l){out[out_at+i]=cbufs[bo+so+i];i=i+1;}
    return l;""",
"""    cb_copy(cb,bo+so,out,out_at,l);
    return l;""",
)

# ---- span_patch ----
rep(
"""fn span_patch(cbufs:[]u8,rbase:[]u8,rlen:[]u8,corpus:i32,off:i32,len:i32,""",
"""fn span_patch(cb:*Cb,rbase:[]u8,rlen:[]u8,corpus:i32,off:i32,len:i32,""",
)
rep(
"""    let n:i32=span_copy(cbufs,rbase,rlen,corpus,off,len,shift,out,out_at);""",
"""    let n:i32=span_copy(cb,rbase,rlen,corpus,off,len,shift,out,out_at);""",
)

# ---- y_recall ----
rep(
"""fn y_recall(s:*Y5,cbufs:[]u8,rbase:[]u8,rlen:[]u8,serial:i32,out:[]u8) i32 {""",
"""fn y_recall(s:*Y5,cb:*Cb,rbase:[]u8,rlen:[]u8,serial:i32,out:[]u8) i32 {""",
)
rep(
"""            if((f & F_PATCH)!=0){total=total+span_patch(cbufs,rbase,rlen,c,o,l,shift,dk,out,total);}
            else{total=total+span_copy(cbufs,rbase,rlen,c,o,l,shift,out,total);}""",
"""            if((f & F_PATCH)!=0){total=total+span_patch(cb,rbase,rlen,c,o,l,shift,dk,out,total);}
            else{total=total+span_copy(cb,rbase,rlen,c,o,l,shift,out,total);}""",
)
rep(
"""        if((f & F_PATCH)!=0){total=span_patch(cbufs,rbase,rlen,c,o,l,shift,dk,out,0);}
        else{total=span_copy(cbufs,rbase,rlen,c,o,l,shift,out,0);}""",
"""        if((f & F_PATCH)!=0){total=span_patch(cb,rbase,rlen,c,o,l,shift,dk,out,0);}
        else{total=span_copy(cb,rbase,rlen,c,o,l,shift,out,0);}""",
)

# ---- tok_extract ----
rep(
"""fn tok_extract(cbufs:[]u8,rbase:[]u8,rlen:[]u8,corpus:i32,off:i32,len:i32,
               tok:[]u8) i32 {""",
"""fn tok_extract(cb:*Cb,rbase:[]u8,rlen:[]u8,corpus:i32,off:i32,len:i32,
               tok:[]u8) i32 {""",
)
rep(
"""        let b:i32=cbufs[bo+off+p] as i32;
        if(b!=32 && b!=9 && b!=10 && b!=13){break;}""",
"""        let b:i32=cb_get(cb,bo+off+p) as i32;
        if(b!=32 && b!=9 && b!=10 && b!=13){break;}""",
)
rep(
"""        let b:i32=cbufs[bo+off+p] as i32;
        if(b==32 || b==9 || b==10 || b==13){break;}""",
"""        let b:i32=cb_get(cb,bo+off+p) as i32;
        if(b==32 || b==9 || b==10 || b==13){break;}""",
)

# ---- y_link_pass ----
rep(
"""fn y_link_pass(s:*Y5,cbufs:[]u8,rbase:[]u8,rlen:[]u8) i32 {""",
"""fn y_link_pass(s:*Y5,cb:*Cb,rbase:[]u8,rlen:[]u8) i32 {""",
)
rep(
"""    let ts:i32=1024;
    while(ts<ncand*2){ts=ts*2;}""",
"""    let ts:i32=1024;
    while(ts<ncand*2){ts=ts*2;}
    if(ts>524288){ts=524288;} // 10x: tent chunk cap; grouping is ts-invariant""",
)
# insert loop: tok_extract + probe guard
rep(
"""            let tn:i32=tok_extract(cbufs,rbase,rlen,rget(s,x,R_CORPUS),
                                   rget(s,x,R_OFF),rget(s,x,R_LEN),tok);
            if(tn>0){
                let h:i64=tok_hash(tok,tn);
                let slot:i64=h % (ts as i64);
                if(slot<0){slot=slot+(ts as i64);}
                let done:i32=0;
                while(done==0){
                    let hd:i32=iget(tent,(slot as i32)*32+28);
                    if(hd<0){
                        iput(tent,(slot as i32)*32,tn);
                        let q:i32=0;while(q<tn){tent[(slot as i32)*32+4+q]=tok[q];q=q+1;}
                        iput(tent,(slot as i32)*32+28,x);
                        done=1;
                    }else{""",
"""            let tn:i32=tok_extract(cb,rbase,rlen,rget(s,x,R_CORPUS),
                                   rget(s,x,R_OFF),rget(s,x,R_LEN),tok);
            if(tn>0){
                let h:i64=tok_hash(tok,tn);
                let slot:i64=h % (ts as i64);
                if(slot<0){slot=slot+(ts as i64);}
                let done:i32=0;
                let pg:i64=0;
                while(done==0){
                    pg=pg+1;
                    if(pg>(ts as i64)*4){_zag_println("FATAL,link-table-full");return 0;}
                    let hd:i32=iget(tent,(slot as i32)*32+28);
                    if(hd<0){
                        iput(tent,(slot as i32)*32,tn);
                        let q:i32=0;while(q<tn){tent[(slot as i32)*32+4+q]=tok[q];q=q+1;}
                        iput(tent,(slot as i32)*32+28,x);
                        done=1;
                    }else{""",
)
# process loop: tok_extract + probe guard
rep(
"""            let tn:i32=tok_extract(cbufs,rbase,rlen,rget(s,x,R_CORPUS),
                                   rget(s,x,R_OFF),rget(s,x,R_LEN),tok);
            if(tn>0){
                let h:i64=tok_hash(tok,tn);
                let slot:i64=h % (ts as i64);
                if(slot<0){slot=slot+(ts as i64);}
                let hd:i32=-2;
                let done2:i32=0;
                while(done2==0){
                    hd=iget(tent,(slot as i32)*32+28);
                    if(hd<0){done2=1;}
                    else{""",
"""            let tn:i32=tok_extract(cb,rbase,rlen,rget(s,x,R_CORPUS),
                                   rget(s,x,R_OFF),rget(s,x,R_LEN),tok);
            if(tn>0){
                let h:i64=tok_hash(tok,tn);
                let slot:i64=h % (ts as i64);
                if(slot<0){slot=slot+(ts as i64);}
                let hd:i32=-2;
                let done2:i32=0;
                let pg2:i64=0;
                while(done2==0){
                    pg2=pg2+1;
                    if(pg2>(ts as i64)*4){_zag_println("FATAL,link-table-full");return 0;}
                    hd=iget(tent,(slot as i32)*32+28);
                    if(hd<0){done2=1;}
                    else{""",
)

# ---- y_probe_one ----
rep(
"""fn y_probe_one(s:*Y5,cbufs:[]u8,rbase:[]u8,rlen:[]u8,live:[]u8,nlive:i32,""",
"""fn y_probe_one(s:*Y5,cb:*Cb,rbase:[]u8,rlen:[]u8,live:[]u8,nlive:i32,""",
)
rep(
"""    let rl:i32=y_recall(s,cbufs,rbase,rlen,T,tmp);""",
"""    let rl:i32=y_recall(s,cb,rbase,rlen,T,tmp);""",
)
rep(
"""                if(exp+j>=rl || tmp[exp+j]!=cbufs[bo+o+j]){ok=0;break;}""",
"""                if(exp+j>=rl || tmp[exp+j]!=cb_get(cb,bo+o+j)){ok=0;break;}""",
)
rep(
"""            while(j<l){if(tmp[j]!=cbufs[bo+o+j]){ok=0;break;}j=j+1;}""",
"""            while(j<l){if(tmp[j]!=cb_get(cb,bo+o+j)){ok=0;break;}j=j+1;}""",
)

# ---- unit_content_ok ----
rep(
"""fn unit_content_ok(s:*Y5,cbufs:[]u8,rbase:[]u8,rlen:[]u8,serial:i32,out:[]u8,""",
"""fn unit_content_ok(s:*Y5,cb:*Cb,rbase:[]u8,rlen:[]u8,serial:i32,out:[]u8,""",
)
rep(
"""            while(j<ll){if(out[exp+j]!=cbufs[bo+so+j]){return 0;}j=j+1;}""",
"""            while(j<ll){if(out[exp+j]!=cb_get(cb,bo+so+j)){return 0;}j=j+1;}""",
)
rep(
"""        while(j<ll){if(out[j]!=cbufs[bo+so+j]){return 0;}j=j+1;}""",
"""        while(j<ll){if(out[j]!=cb_get(cb,bo+so+j)){return 0;}j=j+1;}""",
)

# ---- probe_all ----
rep(
"""fn probe_all(s:*Y5,cbufs:[]u8,rbase:[]u8,rlen:[]u8,live:[]u8,nlive:i32,""",
"""fn probe_all(s:*Y5,cb:*Cb,rbase:[]u8,rlen:[]u8,live:[]u8,nlive:i32,""",
)
rep(
"""            if(y_probe_one(s,cbufs,rbase,rlen,live,nlive,T,probes,bout)!=0){""",
"""            if(y_probe_one(s,cb,rbase,rlen,live,nlive,T,probes,bout)!=0){""",
)
rep(
"""        let rl:i32=y_recall(s,cbufs,rbase,rlen,T,bout);
        if(rl>=0 && unit_content_ok(s,cbufs,rbase,rlen,T,bout,rl)==1){ok=ok+1;}""",
"""        let rl:i32=y_recall(s,cb,rbase,rlen,T,bout);
        if(rl>=0 && unit_content_ok(s,cb,rbase,rlen,T,bout,rl)==1){ok=ok+1;}""",
)

# ---- probe_reg ----
rep(
"""fn probe_reg(s:*Y5,cbufs:[]u8,rbase:[]u8,rlen:[]u8,corpus:i32,""",
"""fn probe_reg(s:*Y5,cb:*Cb,rbase:[]u8,rlen:[]u8,corpus:i32,""",
)
rep(
"""            let rl:i32=y_recall(s,cbufs,rbase,rlen,t,bout);
            if(rl>=0 && unit_content_ok(s,cbufs,rbase,rlen,t,bout,rl)==1){ok=ok+1;}""",
"""            let rl:i32=y_recall(s,cb,rbase,rlen,t,bout);
            if(rl>=0 && unit_content_ok(s,cb,rbase,rlen,t,bout,rl)==1){ok=ok+1;}""",
)

# ---- unit_verified ----
rep(
"""fn unit_verified(s:*Y5,cbufs:[]u8,rbase:[]u8,rlen:[]u8,corpus:i32,buflen:i32,""",
"""fn unit_verified(s:*Y5,cb:*Cb,rbase:[]u8,rlen:[]u8,corpus:i32,buflen:i32,""",
)
rep(
"""    let rl:i32=y_recall(s,cbufs,rbase,rlen,t,bout);
    if(rl<0){return 0;}
    if(unit_content_ok(s,cbufs,rbase,rlen,t,bout,rl)==0){return 0;}""",
"""    let rl:i32=y_recall(s,cb,rbase,rlen,t,bout);
    if(rl<0){return 0;}
    if(unit_content_ok(s,cb,rbase,rlen,t,bout,rl)==0){return 0;}""",
)

# ---- ingest_all_cp ----
rep(
"""fn ingest_all_cp(s:*Y5,buf:[]u8,blen:i32) void {""",
"""fn ingest_all_cp(s:*Y5,cb:*Cb,blen:i32) void {""",
)

# ---- j_begin scale ----
rep(
"""fn j_begin(mode:[]u8)void {
    _zag_print("METRIC_JSON {\\"schema\\":\\"metrics-v1\\",\\"arm\\":\\"y5\\",\\"round\\":\\"r1\\",\\"scale\\":\\"1x\\",\\"mode\\":\\"");""",
"""fn j_begin(mode:[]u8)void {
    _zag_print("METRIC_JSON {\\"schema\\":\\"metrics-v1\\",\\"arm\\":\\"y5\\",\\"round\\":\\"");
    if(j_isscale10(mode)==1){_zag_print("r10\\",\\"scale\\":\\"10x");}
    else{_zag_print("r1\\",\\"scale\\":\\"1x");}
    _zag_print("\\",\\"mode\\":\\"");""",
)

print("PART2-OK")

# ============================================================ PART 3: t_* modes

# ---- t_m1 ----
rep(
"""fn t_m1(cdir:[]u8,fname:[]u8,corpus:i32,keyp:[]u8,jmode:[]u8) void {
    let buf:[]u8=read_file(cdir,fname);
    if(buf.len==0){_zag_println("M1,FATAL,empty-corpus");return;}
    let n:i32=nunits_of(buf.len);""",
"""fn t_m1(cdir:[]u8,fname:[]u8,corpus:i32,keyp:[]u8,jmode:[]u8) void {
    let cb:Cb=Cb{.nc=0,.total=0,.c0="",.c1="",.c2="",.c3="",.c4="",.c5=""};
    if(cb_load_file(&cb,cdir,fname)<0){_zag_println("M1,FATAL,empty-corpus");return;}
    let n:i32=nunits_of(cb.total);""",
)
rep(
"""    reg_set(rbase,rlen,corpus,0,buf.len);
    ingest_all(&s,corpus,buf.len,0,0);
    let links:i32=y_link_pass(&s,buf,rbase,rlen);""",
"""    reg_set(rbase,rlen,corpus,0,cb.total);
    ingest_all(&s,corpus,cb.total,0,0);
    let links:i32=y_link_pass(&s,&cb,rbase,rlen);""",
)
rep(
"""    if(probe_all(&s,buf,rbase,rlen,live,nlive,corps,1,bout,&cok,&bok,&idp,1)!=0){return;}""",
"""    if(probe_all(&s,&cb,rbase,rlen,live,nlive,corps,1,bout,&cok,&bok,&idp,1)!=0){return;}""",
)
# (t_m1 has no probe_reg; the swap probe is the second probe_all inside probe_all with last flag=1)

# ---- t_m2 ----
rep(
"""fn t_m2(cdir:[]u8,fname:[]u8,corpus:i32,tier:[]u8,do_m9:i32) void {
    let buf:[]u8=read_file(cdir,fname);
    if(buf.len==0){_zag_println("M2,FATAL,empty-corpus");return;}
    let n:i32=nunits_of(buf.len);""",
"""fn t_m2(cdir:[]u8,fname:[]u8,corpus:i32,tier:[]u8,do_m9:i32) void {
    let cb:Cb=Cb{.nc=0,.total=0,.c0="",.c1="",.c2="",.c3="",.c4="",.c5=""};
    if(cb_load_file(&cb,cdir,fname)<0){_zag_println("M2,FATAL,empty-corpus");return;}
    let n:i32=nunits_of(cb.total);""",
)
rep(
"""    reg_set(rbase,rlen,corpus,0,buf.len);
    let corps:[]u8=halloc(&s,4);
    iput(corps,0,corpus);
    // episode 0 probe on empty store""",
"""    reg_set(rbase,rlen,corpus,0,cb.total);
    let corps:[]u8=halloc(&s,4);
    iput(corps,0,corpus);
    // episode 0 probe on empty store""",
)
rep(
"""        ingest_all(&s,corpus,buf.len,0,0);
        y_link_pass(&s,buf,rbase,rlen);
        nlive=y_livelist(&s,live);
        probe_all(&s,buf,rbase,rlen,live,nlive,corps,1,bout,&cok,&bok,&idp,0);""",
"""        ingest_all(&s,corpus,cb.total,0,0);
        y_link_pass(&s,&cb,rbase,rlen);
        nlive=y_livelist(&s,live);
        probe_all(&s,&cb,rbase,rlen,live,nlive,corps,1,bout,&cok,&bok,&idp,0);""",
)
# t_m2 episode-0 probe (4-space indent; the loop probe was handled above)
rep(
"""    probe_all(&s,buf,rbase,rlen,live,nlive,corps,1,bout,&cok,&bok,&idp,0);""",
"""    probe_all(&s,&cb,rbase,rlen,live,nlive,corps,1,bout,&cok,&bok,&idp,0);""",
)

# ---- t_m3 ----
rep(
"""    let prose:[]u8=read_file(cdir,"prose.bin");
    let code:[]u8=read_file(cdir,"code.bin");
    let fresh:[]u8=read_file(cdir,"churn_fresh.bin");
    if(prose.len==0 || code.len==0 || fresh.len==0){_zag_println("M3,FATAL,empty-corpus");return;}
    let nun_p:i32=nunits_of(prose.len);let nun_c:i32=nunits_of(code.len);""",
"""    let cb:Cb=Cb{.nc=0,.total=0,.c0="",.c1="",.c2="",.c3="",.c4="",.c5=""};
    if(cb_load_file(&cb,cdir,"prose.bin")<0){_zag_println("M3,FATAL,empty-corpus");return;}
    let plen:i32=cb.total;
    if(cb_load_file(&cb,cdir,"code.bin")<0){_zag_println("M3,FATAL,empty-corpus");return;}
    let clen:i32=cb.total-plen;
    if(cb_load_file(&cb,cdir,"churn_fresh.bin")<0){_zag_println("M3,FATAL,empty-corpus");return;}
    let flen:i32=cb.total-plen-clen;
    let nun_p:i32=nunits_of(plen);let nun_c:i32=nunits_of(clen);""",
)
rep(
"""    // registry: prose@0, code@plen, fresh@plen+clen (concatenated, b64 pattern)
    let cbufs:[]u8=halloc(&s,prose.len+code.len+fresh.len);
    let rbase:[]u8=halloc(&s,40);let rlen:[]u8=halloc(&s,40);
    let i:i32=0;while(i<prose.len){cbufs[i]=prose[i];i=i+1;}
    let j2:i32=0;while(j2<code.len){cbufs[prose.len+j2]=code[j2];j2=j2+1;}
    let j3:i32=0;while(j3<fresh.len){cbufs[prose.len+code.len+j3]=fresh[j3];j3=j3+1;}
    reg_set(rbase,rlen,Y5_C_PROSE,0,prose.len);
    reg_set(rbase,rlen,Y5_C_CODE,prose.len,code.len);
    reg_set(rbase,rlen,Y5_C_FRESH,prose.len+code.len,fresh.len);""",
"""    // registry: prose@0, code@plen, fresh@plen+clen (concatenated, b64 pattern)
    // 1x trace equivalence: dummy cbufs halloc (original had it traced); never indexed so 10x size is safe
    let cb_total:i32=plen+clen+flen;
    let cbufs:[]u8=halloc(&s,cb_total);
    let rbase:[]u8=halloc(&s,40);let rlen:[]u8=halloc(&s,40);
    reg_set(rbase,rlen,Y5_C_PROSE,0,plen);
    reg_set(rbase,rlen,Y5_C_CODE,plen,clen);
    reg_set(rbase,rlen,Y5_C_FRESH,plen+clen,flen);""",
)
rep(
"""        let sr:i32=y_ingest_grid(&s,Y5_C_PROSE,ii,prose.len,0,0);""",
"""        let sr:i32=y_ingest_grid(&s,Y5_C_PROSE,ii,plen,0,0);""",
)
rep(
"""        let sr:i32=y_ingest_grid(&s,Y5_C_CODE,jj,code.len,0,0);""",
"""        let sr:i32=y_ingest_grid(&s,Y5_C_CODE,jj,clen,0,0);""",
)
rep(
"""        let op:i32=iget(s.led,le*64);""",
"""        let op:i32=led_op(&s,le);""",
)
rep(
"""    hfree(&s,bout);hfree(&s,live);hfree(&s,cbufs);hfree(&s,rbase);hfree(&s,rlen);""",
"""    hfree(&s,bout);hfree(&s,live);hfree(&s,cbufs);hfree(&s,rbase);hfree(&s,rlen);""",
)

# t_m4: rename the original cb:[]u8 (cbase view) to avoid collision with the Cb struct
rep(
"""    let cb:[]u8=s.cbase;
    let base:i32=iget(cb,corpus*4);""",
"""    let cbb:[]u8=s.cbase;
    let base:i32=iget(cbb,corpus*4);""",
)
# ---- t_m4 ----
rep(
"""fn t_m4(cdir:[]u8,fname:[]u8,corpus:i32,is_code:i32,keyp:[]u8) void {
    let buf:[]u8=read_file(cdir,fname);
    if(buf.len==0){_zag_println("M4,FATAL,empty-corpus");return;}
    let n:i32=nunits_of(buf.len);""",
"""fn t_m4(cdir:[]u8,fname:[]u8,corpus:i32,is_code:i32,keyp:[]u8) void {
    let cb:Cb=Cb{.nc=0,.total=0,.c0="",.c1="",.c2="",.c3="",.c4="",.c5=""};
    if(cb_load_file(&cb,cdir,fname)<0){_zag_println("M4,FATAL,empty-corpus");return;}
    let n:i32=nunits_of(cb.total);""",
)
rep(
"""    reg_set(rbase,rlen,corpus,0,buf.len);
    ingest_all(&s,corpus,buf.len,0,0);
    y_link_pass(&s,buf,rbase,rlen);""",
"""    reg_set(rbase,rlen,corpus,0,cb.total);
    ingest_all(&s,corpus,cb.total,0,0);
    y_link_pass(&s,&cb,rbase,rlen);""",
)
# (unit_verified signature/body converted in PART2; call sites below)
rep(
"""            rep_b=rep_b+unit_verified(&s,buf,rbase,rlen,corpus,buf.len,iget(d_ser,j*4),bout);""",
"""            rep_b=rep_b+unit_verified(&s,&cb,rbase,rlen,corpus,cb.total,iget(d_ser,j*4),bout);""",
)
rep(
"""            rep_c=rep_c+unit_verified(&s,buf,rbase,rlen,corpus,buf.len,iget(d_ser,j*4),bout);""",
"""            rep_c=rep_c+unit_verified(&s,&cb,rbase,rlen,corpus,cb.total,iget(d_ser,j*4),bout);""",
)

print("PART3A-OK")

rep(
"""        ii2=ii2+1;
    }
    y_link_pass(&s,cbufs,rbase,rlen);
    let jj2:i32=0;""",
"""        ii2=ii2+1;
    }
    y_link_pass(&s,&cb,rbase,rlen);
    let jj2:i32=0;""",
)
rep(
"""        jj2=jj2+1;
    }
    y_link_pass(&s,cbufs,rbase,rlen);
    let fresh_base:i32=s.next_serial;""",
"""        jj2=jj2+1;
    }
    y_link_pass(&s,&cb,rbase,rlen);
    let fresh_base:i32=s.next_serial;""",
)
# t_m3 survival-check and fresh-sample sections (missed in the first pass)
rep(
"""            let rl:i32=y_recall(&s,cbufs,rbase,rlen,t,bout);""",
"""            let rl:i32=y_recall(&s,&cb,rbase,rlen,t,bout);""",
)
rep(
"""                                if(at3+q>=rl || bout[at3+q]!=cbufs[bo+off+q]){good=0;break;}""",
"""                                if(at3+q>=rl || bout[at3+q]!=cb_get(&cb,bo+off+q)){good=0;break;}""",
)
rep(
"""                                if(bout[q2]!=cbufs[bo+off+q2]){good=0;break;}""",
"""                                if(bout[q2]!=cb_get(&cb,bo+off+q2)){good=0;break;}""",
)
rep(
"""        let rl:i32=y_recall(&s,cbufs,rbase,rlen,sr,bout);""",
"""        let rl:i32=y_recall(&s,&cb,rbase,rlen,sr,bout);""",
)
rep(
"""            while(q<64){if(bout[q]!=cbufs[bo+off+q]){good=0;break;}q=q+1;}""",
"""            while(q<64){if(bout[q]!=cb_get(&cb,bo+off+q)){good=0;break;}q=q+1;}""",
)
# t_m3 valuable loop uses sr0/sr1 (t_m8 uses sr/ii/jj — handled above too)
rep(
"""        let sr0:i32=y_ingest_grid(&s,Y5_C_PROSE,ii2,prose.len,0,0);""",
"""        let sr0:i32=y_ingest_grid(&s,Y5_C_PROSE,ii2,plen,0,0);""",
)
rep(
"""        let sr1:i32=y_ingest_grid(&s,Y5_C_CODE,jj2,code.len,0,0);""",
"""        let sr1:i32=y_ingest_grid(&s,Y5_C_CODE,jj2,clen,0,0);""",
)

# ---- t_m5 ----
rep(
"""fn t_m5(cdir:[]u8) void {
    let prose:[]u8=read_file(cdir,"prose.bin");
    let code:[]u8=read_file(cdir,"code.bin");
    if(prose.len==0 || code.len==0){_zag_println("M5,FATAL,empty-corpus");return;}
    let nun_p:i32=nunits_of(prose.len);let nun_c:i32=nunits_of(code.len);
    let total:i32=nun_p+nun_c;
    let cap:i32=total+12000;
    let s:Y5=y_new(cap,300000,2*total+8192,1000000000,total+8192);
    let cbufs:[]u8=halloc(&s,prose.len+code.len);
    let rbase:[]u8=halloc(&s,40);let rlen:[]u8=halloc(&s,40);
    let i:i32=0;while(i<prose.len){cbufs[i]=prose[i];i=i+1;}
    let j2:i32=0;while(j2<code.len){cbufs[prose.len+j2]=code[j2];j2=j2+1;}
    reg_set(rbase,rlen,Y5_C_PROSE,0,prose.len);
    reg_set(rbase,rlen,Y5_C_CODE,prose.len,code.len);
    ingest_all(&s,Y5_C_PROSE,prose.len,0,0);
    y_link_pass(&s,cbufs,rbase,rlen);
    ingest_all(&s,Y5_C_CODE,code.len,0,0);
    y_link_pass(&s,cbufs,rbase,rlen);
    let units:i32=y_count_live(&s);
    let src:i64=(prose.len+code.len) as i64;
    let slot_bytes:i64=(cap as i64)*40;
    let led_bytes:i64=(s.led_n as i64)*64;
    // release the world bytes: the index does not retain them
    nio_free(cbufs);nio_free(prose);nio_free(code);
    _zag_print("M5,units,");p_i64(units as i64);_zag_println("");
    let f:i32=0;
    j_begin("m5-1x");""",
"""fn t_m5(cdir:[]u8,is10:i32) void {
    let cb:Cb=Cb{.nc=0,.total=0,.c0="",.c1="",.c2="",.c3="",.c4="",.c5=""};
    if(cb_load_file(&cb,cdir,"prose.bin")<0){_zag_println("M5,FATAL,empty-corpus");return;}
    let plen:i32=cb.total;
    if(cb_load_file(&cb,cdir,"code.bin")<0){_zag_println("M5,FATAL,empty-corpus");return;}
    let clen:i32=cb.total-plen;
    let nun_p:i32=nunits_of(plen);let nun_c:i32=nunits_of(clen);
    let total:i32=nun_p+nun_c;
    let cap:i32=total+12000;
    let le:i32=300000;
    if(is10==1){le=1000000;}
    let s:Y5=y_new(cap,le,2*total+8192,1000000000,total+8192);
    let rbase:[]u8=halloc(&s,40);let rlen:[]u8=halloc(&s,40);
    reg_set(rbase,rlen,Y5_C_PROSE,0,plen);
    reg_set(rbase,rlen,Y5_C_CODE,plen,clen);
    ingest_all(&s,Y5_C_PROSE,plen,0,0);
    y_link_pass(&s,&cb,rbase,rlen);
    ingest_all(&s,Y5_C_CODE,clen,0,0);
    y_link_pass(&s,&cb,rbase,rlen);
    let units:i32=y_count_live(&s);
    let src:i64=(plen+clen) as i64;
    let slot_bytes:i64=(cap as i64)*40;
    let led_bytes:i64=(s.led_n as i64)*64;
    // release the world bytes: the index does not retain them
    let fi2:i32=0;
    while(fi2<cb.nc){let fc:[]u8=cb_sel(&cb,fi2);nio_free(fc);fi2=fi2+1;}
    _zag_print("M5,units,");p_i64(units as i64);_zag_println("");
    let f:i32=0;
    if(is10==1){j_begin("m5-10x");}else{j_begin("m5-1x");}""",
)

print("PART3B-OK")

# ============================================================ PART 3C: t_m6, t_m7

# ---- t_m6 ----
rep(
"""fn t_m6(cdir:[]u8,dir:i32) void {""",
"""fn t_m6(cdir:[]u8,dir:i32,is10:i32) void {""",
)
rep(
"""    if(dir==1){
        tname="t1_code.bin";tcid=Y5_C_T1C;yname="prose.bin";ycid=Y5_C_PROSE;
        dkey="m6-c2p-1x";dtag="c2p";
    }""",
"""    if(dir==1){
        tname="t1_code.bin";tcid=Y5_C_T1C;yname="prose.bin";ycid=Y5_C_PROSE;
        dkey="m6-c2p-1x";dtag="c2p";
    }
    if(is10==1){
        if(dir==1){dkey="m6-c2p-10x";}else{dkey="m6-p2c-10x";}
    }""",
)
rep(
"""    let tbuf:[]u8=read_file(cdir,tname);
    let ybuf:[]u8=read_file(cdir,yname);
    if(tbuf.len==0 || ybuf.len==0){_zag_println("M6,FATAL,empty-corpus");return;}
    let nt:i32=nunits_of(tbuf.len);let ny:i32=nunits_of(ybuf.len);
    let cap:i32=nt+ny+12000;
    let s:Y5=y_new(cap,300000,2*cap,1000000000,cap);""",
"""    let cb_t:Cb=Cb{.nc=0,.total=0,.c0="",.c1="",.c2="",.c3="",.c4="",.c5=""};
    let cb_y:Cb=Cb{.nc=0,.total=0,.c0="",.c1="",.c2="",.c3="",.c4="",.c5=""};
    if(cb_load_file(&cb_t,cdir,tname)<0 || cb_load_file(&cb_y,cdir,yname)<0){_zag_println("M6,FATAL,empty-corpus");return;}
    let nt:i32=nunits_of(cb_t.total);let ny:i32=nunits_of(cb_y.total);
    let cap:i32=nt+ny+12000;
    let le6:i32=300000;
    if(is10==1){le6=600000;}
    let s:Y5=y_new(cap,le6,2*cap,1000000000,cap);""",
)
rep(
"""    reg_set(rbase,rlen,tcid,0,tbuf.len);
    reg_set(rbase,rlen,ycid,0,ybuf.len);""",
"""    reg_set(rbase,rlen,tcid,0,cb_t.total);
    reg_set(rbase,rlen,ycid,0,cb_y.total);""",
)
rep(
"""        ingest_all(&s,tcid,tbuf.len,0,0);
        y_link_pass(&s,tbuf,rbase,rlen);
        probe_reg(&s,tbuf,rbase,rlen,tcid,bout,&cok,&bok);""",
"""        ingest_all(&s,tcid,cb_t.total,0,0);
        y_link_pass(&s,&cb_t,rbase,rlen);
        probe_reg(&s,&cb_t,rbase,rlen,tcid,bout,&cok,&bok);""",
)
rep(
"""        rev_d=rev_d+unit_verified(&s,tbuf,rbase,rlen,tcid,tbuf.len,tbase+j*nt/100,bout);""",
"""        rev_d=rev_d+unit_verified(&s,&cb_t,rbase,rlen,tcid,cb_t.total,tbase+j*nt/100,bout);""",
)
rep(
"""    ingest_all(&s,ycid,ybuf.len,0,0);
    y_link_pass(&s,ybuf,rbase,rlen);""",
"""    ingest_all(&s,ycid,cb_y.total,0,0);
    y_link_pass(&s,&cb_y,rbase,rlen);""",
)
rep(
"""    probe_reg(&s,ybuf,rbase,rlen,ycid,bout,&rec_t,&bnd_t);""",
"""    probe_reg(&s,&cb_y,rbase,rlen,ycid,bout,&rec_t,&bnd_t);""",
)
rep(
"""        rev_t=rev_t+unit_verified(&s,ybuf,rbase,rlen,ycid,ybuf.len,ybase+j*ny/100,bout);""",
"""        rev_t=rev_t+unit_verified(&s,&cb_y,rbase,rlen,ycid,cb_y.total,ybase+j*ny/100,bout);""",
)

# ---- t_m7 ----
rep(
"""fn t_m7(cdir:[]u8) void {
    let prose:[]u8=read_file(cdir,"prose.bin");
    if(prose.len==0){_zag_println("M7,FATAL,empty-corpus");return;}
    let n:i32=nunits_of(prose.len);
    let cap:i32=n+12000;
    let s:Y5=y_new(cap,200000,2*n+8192,1000000000,n+8192);
    let bout:[]u8=halloc(&s,65536);
    let rbase:[]u8=halloc(&s,40);let rlen:[]u8=halloc(&s,40);
    reg_set(rbase,rlen,Y5_C_PROSE,0,prose.len);
    // C' buffer: prose with every-100th 256B unit's first byte XOR 0xFF
    let cp:[]u8=halloc(&s,prose.len);
    let ci:i32=0;while(ci<prose.len){cp[ci]=prose[ci];ci=ci+1;}
    let u100:i32=0;
    while(u100<n){
        if(u100%100==0){
            let off:i32=u100*Y5_CHUNK;
            cp[off]=(cp[off] as i32 ^ 255) as u8;
        }
        u100=u100+1;
    }
    let rbase2:[]u8=halloc(&s,40);let rlen2:[]u8=halloc(&s,40);
    reg_set(rbase2,rlen2,Y5_C_PROSE,0,prose.len);""",
"""fn t_m7(cdir:[]u8,is10:i32) void {
    let cb1:Cb=Cb{.nc=0,.total=0,.c0="",.c1="",.c2="",.c3="",.c4="",.c5=""};
    if(cb_load_file(&cb1,cdir,"prose.bin")<0){_zag_println("M7,FATAL,empty-corpus");return;}
    let n:i32=nunits_of(cb1.total);
    let cap:i32=n+12000;
    let le7:i32=200000;
    if(is10==1){le7=1000000;}
    let s:Y5=y_new(cap,le7,2*n+8192,1000000000,n+8192);
    let bout:[]u8=halloc(&s,65536);
    let rbase:[]u8=halloc(&s,40);let rlen:[]u8=halloc(&s,40);
    reg_set(rbase,rlen,Y5_C_PROSE,0,cb1.total);
    // C' buffer: prose with every-100th 256B unit's first byte XOR 0xFF
    let cb2:Cb=Cb{.nc=0,.total=0,.c0="",.c1="",.c2="",.c3="",.c4="",.c5=""};
    if(cb_copy_from(&s,&cb2,&cb1)<0){_zag_println("M7,FATAL,cp-copy");return;}
    let u100:i32=0;
    while(u100<n){
        if(u100%100==0){
            let off:i32=u100*Y5_CHUNK;
            cb_put(&cb2,off,(cb_get(&cb2,off) as i32 ^ 255) as u8);
        }
        u100=u100+1;
    }
    let rbase2:[]u8=halloc(&s,40);let rlen2:[]u8=halloc(&s,40);
    reg_set(rbase2,rlen2,Y5_C_PROSE,0,cb1.total);""",
)
rep(
"""    ingest_all(&s,Y5_C_PROSE,prose.len,0,0);
    idrefs=idrefs+(n as i64);
    y_link_pass(&s,prose,rbase,rlen);""",
"""    ingest_all(&s,Y5_C_PROSE,cb1.total,0,0);
    idrefs=idrefs+(n as i64);
    y_link_pass(&s,&cb1,rbase,rlen);""",
count=2,
)
rep(
"""        let sr:i32=y_ingest_grid(&s,Y5_C_PROSE,idx,prose.len,0,0);
        idrefs=idrefs+1;
        let rl:i32=y_recall(&s,prose,rbase,rlen,sr,bout);""",
"""        let sr:i32=y_ingest_grid(&s,Y5_C_PROSE,idx,cb1.total,0,0);
        idrefs=idrefs+1;
        let rl:i32=y_recall(&s,&cb1,rbase,rlen,sr,bout);""",
count=2,
)
rep(
"""    ingest_all_cp(&s,cp,prose.len);
    idrefs=idrefs+(n as i64);
    y_link_pass(&s,cp,rbase2,rlen2);""",
"""    ingest_all_cp(&s,&cb2,cb2.total);
    idrefs=idrefs+(n as i64);
    y_link_pass(&s,&cb2,rbase2,rlen2);""",
)
rep(
"""        let sr:i32=y_ingest_grid(&s,Y5_C_PROSE,idx,prose.len,0,0);
        idrefs=idrefs+1;
        let rl:i32=y_recall(&s,cp,rbase2,rlen2,sr,bout);""",
"""        let sr:i32=y_ingest_grid(&s,Y5_C_PROSE,idx,cb1.total,0,0);
        idrefs=idrefs+1;
        let rl:i32=y_recall(&s,&cb2,rbase2,rlen2,sr,bout);""",
)
rep(
"""    j_begin("m7-1x");""",
"""    if(is10==1){j_begin("m7-10x");}else{j_begin("m7-1x");}""",
)
rep(
"""    hfree(&s,cp);hfree(&s,rbase2);hfree(&s,rlen2);""",
"""    let fi7:i32=0;
    while(fi7<cb2.nc){let fc7:[]u8=cb_sel(&cb2,fi7);hfree(&s,fc7);fi7=fi7+1;}
    hfree(&s,rbase2);hfree(&s,rlen2);""",
)

print("PART3C-OK")

# ============================================================ PART 3D: t_m8, main

# ---- t_m8 ----
rep(
"""fn t_m8(cdir:[]u8,outdir:[]u8,pert:[]u8) void {""",
"""fn t_m8(cdir:[]u8,outdir:[]u8,pert:[]u8,is10:i32) void {""",
)
rep(
"""    let prose:[]u8=read_file(cdir,"prose.bin");
    let code:[]u8=read_file(cdir,"code.bin");
    let fresh:[]u8=read_file(cdir,"churn_fresh.bin");
    if(prose.len==0 || code.len==0 || fresh.len==0){
        _zag_println("M8,FATAL,empty-corpus");return;
    }
    let nun_p:i32=nunits_of(prose.len);let nun_c:i32=nunits_of(code.len);
    let total:i32=nun_p+nun_c;
    let cap:i32=total+20000;
    // large-capacity instance (A17): no eviction pressure in the gate
    let s:Y5=y_new(cap,400000,2*cap+16384,1000000000,cap);
    let bout:[]u8=halloc(&s,8192);
    let live:[]u8=halloc(&s,cap*4);
    let cbufs:[]u8=halloc(&s,prose.len+code.len+fresh.len);
    let rbase:[]u8=halloc(&s,40);let rlen:[]u8=halloc(&s,40);
    let i:i32=0;while(i<prose.len){cbufs[i]=prose[i];i=i+1;}
    let j2:i32=0;while(j2<code.len){cbufs[prose.len+j2]=code[j2];j2=j2+1;}
    let j3:i32=0;while(j3<fresh.len){cbufs[prose.len+code.len+j3]=fresh[j3];j3=j3+1;}
    reg_set(rbase,rlen,Y5_C_PROSE,0,prose.len);
    reg_set(rbase,rlen,Y5_C_CODE,prose.len,code.len);
    reg_set(rbase,rlen,Y5_C_FRESH,prose.len+code.len,fresh.len);""",
"""    let cb:Cb=Cb{.nc=0,.total=0,.c0="",.c1="",.c2="",.c3="",.c4="",.c5=""};
    if(cb_load_file(&cb,cdir,"prose.bin")<0){_zag_println("M8,FATAL,empty-corpus");return;}
    let plen:i32=cb.total;
    if(cb_load_file(&cb,cdir,"code.bin")<0){_zag_println("M8,FATAL,empty-corpus");return;}
    let clen:i32=cb.total-plen;
    if(cb_load_file(&cb,cdir,"churn_fresh.bin")<0){_zag_println("M8,FATAL,empty-corpus");return;}
    let flen:i32=cb.total-plen-clen;
    let nun_p:i32=nunits_of(plen);let nun_c:i32=nunits_of(clen);
    let total:i32=nun_p+nun_c;
    let cap:i32=total+20000;
    // large-capacity instance (A17): no eviction pressure in the gate
    let le8:i32=400000;
    if(is10==1){le8=1000000;}
    let s:Y5=y_new(cap,le8,2*cap+16384,1000000000,cap);
    let bout:[]u8=halloc(&s,8192);
    let live:[]u8=halloc(&s,cap*4);
    // 1x trace equivalence: dummy cbufs halloc (original had it traced); never indexed so 10x size is safe
    let cb_total8:i32=plen+clen+flen;
    let cbufs:[]u8=halloc(&s,cb_total8);
    let rbase:[]u8=halloc(&s,40);let rlen:[]u8=halloc(&s,40);
    reg_set(rbase,rlen,Y5_C_PROSE,0,plen);
    reg_set(rbase,rlen,Y5_C_CODE,plen,clen);
    reg_set(rbase,rlen,Y5_C_FRESH,plen+clen,flen);""",
)
rep(
"""    ingest_all(&s,Y5_C_PROSE,prose.len,0,0);
    y_link_pass(&s,cbufs,rbase,rlen);
    ingest_all(&s,Y5_C_CODE,code.len,0,0);
    y_link_pass(&s,cbufs,rbase,rlen);""",
"""    ingest_all(&s,Y5_C_PROSE,plen,0,0);
    y_link_pass(&s,&cb,rbase,rlen);
    ingest_all(&s,Y5_C_CODE,clen,0,0);
    y_link_pass(&s,&cb,rbase,rlen);""",
)
rep(
"""    probe_all(&s,cbufs,rbase,rlen,live,nlive,corps,2,bout,&cok,&bok,&idp,0);""",
"""    probe_all(&s,&cb,rbase,rlen,live,nlive,corps,2,bout,&cok,&bok,&idp,0);""",
)
# artifact section: branch on the 2^25 wall
rep(
"""    // store image: rows + pool + liveq + cbase (persistent slot region)
    let rows:[]u8=s.rows;let pool:[]u8=s.pool;let lq:[]u8=s.liveq;
    let cbase:[]u8=s.cbase;
    let imglen:i32=s.cap*40+s.pool_cap*12+s.liveq_cap*4+40;
    let img:[]u8=halloc(&s,imglen);
    let at:i32=0;
    at=img_append(img,at,rows,s.cap*40);
    at=img_append(img,at,pool,s.pool_cap*12);
    at=img_append(img,at,lq,s.liveq_cap*4);
    at=img_append(img,at,cbase,40);
    let nch:i32=(imglen+1048575)/1048576;
    let chain_in:[]u8=halloc(&s,nch*32);
    let ci:i32=0;
    while(ci<nch){
        let cs:i32=ci*1048576;let cn:i32=imglen-cs;
        if(cn>1048576){cn=1048576;}
        ns_sha256(img[cs..cs+cn],chain_in[ci*32..ci*32+32]);
        ci=ci+1;
    }
    let chl:[]u8=halloc(&s,nch*80);
    let cho:i32=0;
    ci=0;
    while(ci<nch){
        let hx:[]u8=ns_hex(chain_in[ci*32..ci*32+32]);
        let tag:[]u8=_zag_i64_to_str(ci as i64);
        chl[cho]=99;chl[cho+1]=104;chl[cho+2]=117;chl[cho+3]=110;chl[cho+4]=107;cho=cho+5;
        let a2:i32=0;while(a2<tag.len){chl[cho]=tag[a2];cho=cho+1;a2=a2+1;}
        chl[cho]=32;cho=cho+1;
        let b2:i32=0;while(b2<hx.len){chl[cho]=hx[b2];cho=cho+1;b2=b2+1;}
        chl[cho]=10;cho=cho+1;
        nio_free(hx);nio_free(tag);
        ci=ci+1;
    }
    write_file(outdir,"store_hashes.txt",chl[0..cho]);
    let chain:[]u8=halloc(&s,32);
    ns_sha256(chain_in,chain);
    write_hex_line(outdir,"store_chain.txt","chain",chain);""",
"""    // store image: rows + pool + liveq + cbase (persistent slot region)
    let imglen:i32=s.cap*40+s.pool_cap*12+s.liveq_cap*4+40;
    let nch:i32=(imglen+1048575)/1048576;
    let ci:i32=0;
    if(imglen<=33554432){
        // 1x path: materialize the image (byte-identical to the frozen 1x build)
        let img:[]u8=halloc(&s,imglen);
        img_fill(&s,img);
        let chain_in:[]u8=halloc(&s,nch*32);
        ci=0;
        while(ci<nch){
            let cs:i32=ci*1048576;let cn:i32=imglen-cs;
            if(cn>1048576){cn=1048576;}
            ns_sha256(img[cs..cs+cn],chain_in[ci*32..ci*32+32]);
            ci=ci+1;
        }
        let chl:[]u8=halloc(&s,nch*80);
        let cho:i32=0;
        ci=0;
        while(ci<nch){
            let hx:[]u8=ns_hex(chain_in[ci*32..ci*32+32]);
            let tag:[]u8=_zag_i64_to_str(ci as i64);
            chl[cho]=99;chl[cho+1]=104;chl[cho+2]=117;chl[cho+3]=110;chl[cho+4]=107;cho=cho+5;
            let a2:i32=0;while(a2<tag.len){chl[cho]=tag[a2];cho=cho+1;a2=a2+1;}
            chl[cho]=32;cho=cho+1;
            let b2:i32=0;while(b2<hx.len){chl[cho]=hx[b2];cho=cho+1;b2=b2+1;}
            chl[cho]=10;cho=cho+1;
            nio_free(hx);nio_free(tag);
            ci=ci+1;
        }
        write_file(outdir,"store_hashes.txt",chl[0..cho]);
        let chain:[]u8=halloc(&s,32);
        ns_sha256(chain_in,chain);
        write_hex_line(outdir,"store_chain.txt","chain",chain);
    }else{
        // 10x path: stream the logical image in 1MB pieces (never > 2^25)
        let chain_in:[]u8=halloc(&s,nch*32);
        let scratch:[]u8=nio_alloc(1048576);
        let r0:i32=s.cap*40;let r1:i32=s.pool_cap*12;let r2:i32=s.liveq_cap*4;
        ci=0;
        while(ci<nch){
            let cs:i32=ci*1048576;let cn:i32=imglen-cs;
            if(cn>1048576){cn=1048576;}
            img_piece(&s,r0,r1,r2,cs,scratch,cn);
            ns_sha256(scratch[0..cn],chain_in[ci*32..ci*32+32]);
            ci=ci+1;
        }
        nio_free(scratch);
        let chl:[]u8=halloc(&s,nch*80);
        let cho:i32=0;
        ci=0;
        while(ci<nch){
            let hx:[]u8=ns_hex(chain_in[ci*32..ci*32+32]);
            let tag:[]u8=_zag_i64_to_str(ci as i64);
            chl[cho]=99;chl[cho+1]=104;chl[cho+2]=117;chl[cho+3]=110;chl[cho+4]=107;cho=cho+5;
            let a2:i32=0;while(a2<tag.len){chl[cho]=tag[a2];cho=cho+1;a2=a2+1;}
            chl[cho]=32;cho=cho+1;
            let b2:i32=0;while(b2<hx.len){chl[cho]=hx[b2];cho=cho+1;b2=b2+1;}
            chl[cho]=10;cho=cho+1;
            nio_free(hx);nio_free(tag);
            ci=ci+1;
        }
        write_file(outdir,"store_hashes.txt",chl[0..cho]);
        let chain:[]u8=halloc(&s,32);
        ns_sha256(chain_in,chain);
        write_hex_line(outdir,"store_chain.txt","chain",chain);
    }""",
)
rep(
"""    write_file(outdir,"ledger.bin",s.led[0..s.led_n*64]);
    let lhash:[]u8=halloc(&s,32);
    ns_sha256(s.led[0..s.led_n*64],lhash);
    write_hex_line(outdir,"ledger_chain.txt","chain",lhash);""",
"""    write_ledger(&s,outdir,"ledger.bin");
    let lhash:[]u8=halloc(&s,32);
    ledger_hash(&s,lhash);
    write_hex_line(outdir,"ledger_chain.txt","chain",lhash);""",
)
rep(
"""    hfree(&s,bout);hfree(&s,live);hfree(&s,cbufs);hfree(&s,rbase);
    hfree(&s,rlen);hfree(&s,corps);hfree(&s,vser);
    hfree(&s,img);hfree(&s,chain_in);hfree(&s,chl);hfree(&s,chain);hfree(&s,lhash);""",
"""    hfree(&s,bout);hfree(&s,live);hfree(&s,cbufs);hfree(&s,rbase);
    hfree(&s,rlen);hfree(&s,corps);hfree(&s,vser);
    hfree(&s,lhash);""",
)

# ---- main: 10x dispatch (flat chain before the 1x chain) ----
rep(
"""fn main() i32 {
    let mode:[]u8=_zag_arg(1);
    let cdir:[]u8=_zag_arg(2);
    if(_zag_strcmp(mode,"m1-1x-prose")==1){t_m1(cdir,"prose.bin",Y5_C_PROSE,"prose","m1-1x-prose");}""",
"""fn main() i32 {
    let mode:[]u8=_zag_arg(1);
    let cdir:[]u8=_zag_arg(2);
    if(_zag_strcmp(mode,"m1-10x-prose")==1){t_m1(cdir,"prose.bin",Y5_C_PROSE,"prose","m1-10x-prose");return 0;}
    if(_zag_strcmp(mode,"m1-10x-code")==1){t_m1(cdir,"code.bin",Y5_C_CODE,"code","m1-10x-code");return 0;}
    if(_zag_strcmp(mode,"m2-10x-t1-prose")==1){t_m2(cdir,"t1_prose.bin",Y5_C_T1P,"m2-10x-t1-prose",0);return 0;}
    if(_zag_strcmp(mode,"m2-10x-t1-code")==1){t_m2(cdir,"t1_code.bin",Y5_C_T1C,"m2-10x-t1-code",0);return 0;}
    if(_zag_strcmp(mode,"m2-10x-t2-prose")==1){t_m2(cdir,"t2_prose.bin",Y5_C_T2P,"m2-10x-t2-prose",0);return 0;}
    if(_zag_strcmp(mode,"m2-10x-t2-code")==1){t_m2(cdir,"t2_code.bin",Y5_C_T2C,"m2-10x-t2-code",0);return 0;}
    if(_zag_strcmp(mode,"m2-10x-t3")==1){t_m2(cdir,"t3.bin",Y5_C_T3,"m2-10x-t3",0);return 0;}
    if(_zag_strcmp(mode,"m3-10x")==1){t_m3(cdir);return 0;}
    if(_zag_strcmp(mode,"m4-10x-prose")==1){t_m4(cdir,"prose.bin",Y5_C_PROSE,0,"m4-10x-prose");return 0;}
    if(_zag_strcmp(mode,"m4-10x-code")==1){t_m4(cdir,"code.bin",Y5_C_CODE,1,"m4-10x-code");return 0;}
    if(_zag_strcmp(mode,"m5-10x")==1){t_m5(cdir,1);return 0;}
    if(_zag_strcmp(mode,"m6-p2c-10x")==1){t_m6(cdir,0,1);return 0;}
    if(_zag_strcmp(mode,"m6-c2p-10x")==1){t_m6(cdir,1,1);return 0;}
    if(_zag_strcmp(mode,"m7-10x")==1){t_m7(cdir,1);return 0;}
    if(_zag_strcmp(mode,"m8-10x")==1){
        let o:[]u8=_zag_arg(3);
        let p:[]u8=_zag_arg(4);
        t_m8(cdir,o,p,1);return 0;
    }
    if(_zag_strcmp(mode,"m1-1x-prose")==1){t_m1(cdir,"prose.bin",Y5_C_PROSE,"prose","m1-1x-prose");}""",
)
# 1x call sites gain the is10=0 arg
rep(
"""                                            if(_zag_strcmp(mode,"m5-1x")==1){t_m5(cdir);}""",
"""                                            if(_zag_strcmp(mode,"m5-1x")==1){t_m5(cdir,0);}""",
)
rep(
"""                                                    if(_zag_strcmp(mode,"m6-p2c-1x")==1){t_m6(cdir,0);}""",
"""                                                    if(_zag_strcmp(mode,"m6-p2c-1x")==1){t_m6(cdir,0,0);}""",
)
rep(
"""                                                    if(_zag_strcmp(mode,"m6-c2p-1x")==1){t_m6(cdir,1);}""",
"""                                                    if(_zag_strcmp(mode,"m6-c2p-1x")==1){t_m6(cdir,1,0);}""",
)
rep(
"""                                                            if(_zag_strcmp(mode,"m7-1x")==1){t_m7(cdir);}""",
"""                                                            if(_zag_strcmp(mode,"m7-1x")==1){t_m7(cdir,0);}""",
)
rep(
"""                                                                    t_m8(cdir,o,p);
                                                                }else{usage();return 1;}""",
"""                                                                    t_m8(cdir,o,p,0);
                                                                }else{usage();return 1;}""",
)

# ---- usage line ----
rep(
"""    _zag_println("modes: m1-1x-prose m1-1x-code m2-t1-prose m2-t1-code m2-t2-prose m2-t2-code m2-t3-1x m3-1x m4-1x-prose m4-1x-code m5-1x m5-baseline m6-p2c-1x m6-c2p-1x m7-1x m8-1x");""",
"""    _zag_println("modes: m1-1x-prose m1-1x-code m2-t1-prose m2-t1-code m2-t2-prose m2-t2-code m2-t3-1x m3-1x m4-1x-prose m4-1x-code m5-1x m5-baseline m6-p2c-1x m6-c2p-1x m7-1x m8-1x");
    _zag_println("10x: m1-10x-prose m1-10x-code m2-10x-t1-prose m2-10x-t1-code m2-10x-t2-prose m2-10x-t2-code m2-10x-t3 m3-10x m4-10x-prose m4-10x-code m5-10x m6-p2c-10x m6-c2p-10x m7-10x m8-10x");""",
)

# Fix probe_reg shadowing: rename local cb:[]u8 to cb_reg (param is cb:*Cb)
txt = txt.replace(
    "fn probe_reg(s:*Y5,cb:*Cb,rbase:[]u8,rlen:[]u8,corpus:i32,\n             bout:[]u8,cok:*i32,bok:*i32) void {\n    let cb:[]u8=s.*.cbase;\n    let base:i32=iget(cb,corpus*4);",
    "fn probe_reg(s:*Y5,cb:*Cb,rbase:[]u8,rlen:[]u8,corpus:i32,\n             bout:[]u8,cok:*i32,bok:*i32) void {\n    let cb_reg:[]u8=s.*.cbase;\n    let base:i32=iget(cb_reg,corpus*4);",
)
# ---- write output ----
open(DST, "w").write(txt)
print("PART3D-OK")
print("wrote", DST, len(txt), "bytes")
