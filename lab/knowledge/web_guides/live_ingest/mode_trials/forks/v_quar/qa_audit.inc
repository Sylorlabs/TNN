// ================= V-QUAR read-audit instrumentation =================
// Every successful file read is logged to fd 2 (stderr) as one line:
//   AUDIT|<binid>|<part>|<slot16>|<content16>
// binid: per-binary constant substituted by gen_sources.py ("PROD","TRAIN","MERGE").
// part: "Q" iff the read path contains the substring "quarantine", else "P".
// slot16: lowercase hex of FNV-1a-64 over the path bytes.
// content16: lowercase hex of FNV-1a-64 over the content bytes.
// Content-free: only hashes leave the instrument. Deterministic: no
// timestamps, PIDs, or addresses; the glue attributes lines to runs by file.
// Q-partition reads are REFUSED here (audited as REFUSED, ok=0). The sole
// exception is qread_claim in the MERGE binary, which bypasses these wrappers
// via qraw_read_path and emits its own QAUDIT line (see qa_merge.inc).
// ==========================================================================

fn qa_bin()[]u8 {
    return "@BINID@";
}

fn qa_part(path:[]u8)i32 {
    let q:[]u8="quarantine";
    if(path.len<q.len){return 0;}
    let i:i32=0;
    while(i+q.len<=path.len){
        let j:i32=0;
        while(j<q.len && path[i+j]==q[j]){j=j+1;}
        if(j==q.len){return 1;}
        i=i+1;
    }
    return 0;
}

fn qa_fnv(b:[]u8)u64 {
    let h:u64=(1469598103934665603 as u64)*(10 as u64)+(7 as u64);
    let p:u64=1099511628211 as u64;
    let i:i32=0;
    while(i<b.len){
        h=(h ^ (b[i] as u64))*p;
        i=i+1;
    }
    return h;
}

fn qa_hex16(v:u64,out:[]u8,at:i32)void {
    let k:i32=0;
    while(k<16){
        let m:u64=v & (15 as u64);
        let n:i32=m as i32;
        let c:u8=(48+n) as u8;
        if(n>=10){c=(87+n) as u8;}
        out[at+15-k]=c;
        v=v >> (4 as u64);
        k=k+1;
    }
    return;
}

fn qa_write_line(line:[]u8,n:i32)void {
    _zag_raw_syscall(1,2,_zag_slice_ptr(line) as i64,n as i64,0,0,0);
    return;
}

fn qa_emit(path:[]u8,content:[]u8)void {
    let line:[]u8=nio_alloc(192);
    if(line.len==0){return;}
    let n:i32=0;
    let tag:[]u8="AUDIT|";
    let i:i32=0;
    while(i<tag.len){line[n]=tag[i]; n=n+1; i=i+1;}
    let b:[]u8=qa_bin();
    i=0;
    while(i<b.len){line[n]=b[i]; n=n+1; i=i+1;}
    line[n]=124; n=n+1;
    let ps:[]u8="P";
    if(qa_part(path)==1){ps="Q";}
    i=0;
    while(i<ps.len){line[n]=ps[i]; n=n+1; i=i+1;}
    line[n]=124; n=n+1;
    qa_hex16(qa_fnv(path),line,n);
    n=n+16;
    line[n]=124; n=n+1;
    qa_hex16(qa_fnv(content),line,n);
    n=n+16;
    line[n]=10; n=n+1;
    qa_write_line(line,n);
    nio_free(line);
    return;
}

fn qa_refuse(path:[]u8)void {
    let line:[]u8=nio_alloc(192);
    if(line.len==0){return;}
    let n:i32=0;
    let tag:[]u8="AUDIT|";
    let i:i32=0;
    while(i<tag.len){line[n]=tag[i]; n=n+1; i=i+1;}
    let b:[]u8=qa_bin();
    i=0;
    while(i<b.len){line[n]=b[i]; n=n+1; i=i+1;}
    let mid:[]u8="|Q|REFUSED|";
    i=0;
    while(i<mid.len){line[n]=mid[i]; n=n+1; i=i+1;}
    qa_hex16(qa_fnv(path),line,n);
    n=n+16;
    line[n]=10; n=n+1;
    qa_write_line(line,n);
    nio_free(line);
    return;
}

fn read_file(dir:[]u8,name:[]u8,ok:*i32)[]u8 {
    if(qa_part(dir)==1 || qa_part(name)==1){
        let pl0:i32=dir.len+1+name.len;
        let p0:[]u8=nio_alloc(pl0+1);
        if(p0.len>0){
            let i0:i32=0;
            while(i0<dir.len){p0[i0]=dir[i0]; i0=i0+1;}
            p0[dir.len]=47;
            let j0:i32=0;
            while(j0<name.len){p0[dir.len+1+j0]=name[j0]; j0=j0+1;}
            qa_refuse(p0[0..pl0]);
            nio_free(p0);
        }
        ok[0]=0;
        return "";
    }
    let b:[]u8=qraw_read_file(dir,name,ok);
    if(ok[0]==1){
        let pl:i32=dir.len+1+name.len;
        let p2:[]u8=nio_alloc(pl+1);
        if(p2.len>0){
            let i2:i32=0;
            while(i2<dir.len){p2[i2]=dir[i2]; i2=i2+1;}
            p2[dir.len]=47;
            let j2:i32=0;
            while(j2<name.len){p2[dir.len+1+j2]=name[j2]; j2=j2+1;}
            qa_emit(p2[0..pl],b);
            nio_free(p2);
        }
    }
    return b;
}

fn read_path(path:[]u8,ok:*i32)[]u8 {
    if(qa_part(path)==1){
        qa_refuse(path);
        ok[0]=0;
        return "";
    }
    let b:[]u8=qraw_read_path(path,ok);
    if(ok[0]==1){
        qa_emit(path,b);
    }
    return b;
}
