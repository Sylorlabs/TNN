// ================= V-QUAR-M merge gate =================
// The merge binary is the ONLY binary that may read the Q partition, and the
// ONLY function that may do so is qread_claim below (the single Q accessor).
// All other read sites go through the instrumented wrappers, which REFUSE
// Q-partition paths (audited REFUSED). qread_claim bypasses the wrappers via
// qraw_read_path and emits its own QAUDIT line, so a merge run's audit log shows
// exactly one QAUDIT per adjudicated claim and no AUDIT|MERGE|Q lines.
//
// Claim file format (glue-written): QC|<qid>|<cid>|<claim>|<query>
// Merge semantics (frozen): stateless per claim; strict-G4 re-verification
// only (the frozen verdict_core, loud=0). MERGE|1 iff strict installs AND the
// installed answer is byte-equal to the quarantined claim. The only
// machine-visible output is the verdict bit: MERGE|<qid>|<0|1>.
// =========================================================

// the single Q accessor: refuses non-Q paths; audited; content-free
fn qread_claim(path:[]u8,qid:[]u8,ok:*i32)[]u8 {
    if(qa_part(path)!=1){
        let line:[]u8=nio_alloc(192);
        if(line.len>0){
            let n:i32=0;
            let tag:[]u8="QAUDIT|MERGE|NOTQ|";
            let i:i32=0;
            while(i<tag.len){line[n]=tag[i]; n=n+1; i=i+1;}
            qa_hex16(qa_fnv(path),line,n);
            n=n+16;
            line[n]=10; n=n+1;
            qa_write_line(line,n);
            nio_free(line);
        }
        ok[0]=0;
        return "";
    }
    let b:[]u8=qraw_read_path(path,ok);
    if(ok[0]==1){
        let line2:[]u8=nio_alloc(192);
        if(line2.len>0){
            let n2:i32=0;
            let tag2:[]u8="QAUDIT|MERGE|Q|";
            let i2:i32=0;
            while(i2<tag2.len){line2[n2]=tag2[i2]; n2=n2+1; i2=i2+1;}
            qa_hex16(qa_fnv(path),line2,n2);
            n2=n2+16;
            line2[n2]=124; n2=n2+1;
            qa_hex16(qa_fnv(b),line2,n2);
            n2=n2+16;
            line2[n2]=10; n2=n2+1;
            qa_write_line(line2,n2);
            nio_free(line2);
        }
    }
    return b;
}

// split the QC line: returns 1 on success; claim/query are slices of cbuf
fn qparse(cbuf:[]u8,qid:[]u8,cid:*i32,claim:*i32,claiml:*i32,qstr:*i32,qstrl:*i32)i32 {
    // QC|<qid>|<cid>|<claim>|<query>
    let pos:i32=0;
    let ls:i32=0;
    let ll:i32=0;
    if(next_line(cbuf,&pos,&ls,&ll)!=1){return 0;}
    let ln:i32=ll;
    if(ln>0 && cbuf[ls+ln-1]==13){ln=ln-1;}
    let p0:i32=ls;
    // field 0: QC
    let f:i32=0;
    while(f<ln && cbuf[p0+f]!=124){f=f+1;}
    if(f!=2 || cbuf[p0]!=81 || cbuf[p0+1]!=67){return 0;}
    // field 1: qid must match
    let q1s:i32=p0+f+1;
    let q1e:i32=q1s;
    while(q1e<ls+ln && cbuf[q1e]!=124){q1e=q1e+1;}
    if(q1e-q1s!=qid.len){return 0;}
    if(bsub_eq(cbuf,q1s,qid,0,qid.len)!=1){return 0;}
    // field 2: cid (kept for the audit trail; not used in verification)
    let c2s:i32=q1e+1;
    let c2e:i32=c2s;
    while(c2e<ls+ln && cbuf[c2e]!=124){c2e=c2e+1;}
    cid[0]=c2s;
    // field 3: claim (may contain '|'; the query is after the LAST '|')
    // find last '|' in the line
    let le:i32=ls+ln-1;
    while(le>c2e && cbuf[le]!=124){le=le-1;}
    if(le<=c2e){return 0;}
    claim[0]=c2e+1;
    claiml[0]=le-(c2e+1);
    qstr[0]=le+1;
    qstrl[0]=ls+ln-(le+1);
    return 1;
}

fn cmd_merge(sd:[]u8,nfp:[]u8,ppath:[]u8,cpath:[]u8,qid:[]u8)i32 {
    let cok:i32=0;
    let cbuf:[]u8=qread_claim(cpath,qid,&cok);
    if(cok==0){nio_free(cbuf); return 2;}
    let cido:i32=0;
    let clmo:i32=0;
    let clml:i32=0;
    let qso:i32=0;
    let qsl:i32=0;
    if(qparse(cbuf,qid,&cido,&clmo,&clml,&qso,&qsl)==0){
        nio_free(cbuf);
        return 2;
    }
    let claim:[]u8=cbuf[clmo..clmo+clml];
    let qstr:[]u8=cbuf[qso..qso+qsl];
    // frozen strict re-verification over P-partition inputs only
    let dt:[]u8=nio_alloc(16384);
    let dp:i32=0;
    let dn:i32=0;
    load_installed(sd,dt,&dp,&dn);
    let ok:i32=0;
    let buf:[]u8=read_path(ppath,&ok);
    if(ok==0){nio_free(cbuf); nio_free(dt); return 2;}
    let nok:i32=0;
    let need:[]u8=read_path(nfp,&nok);
    let kwstr:[]u8="";
    if(nok==1){
        let g2:i32=nio_equal(dget(dt,dn,"QUERY-MODE"),"keywords");
        if(g2==1){kwstr=kw_query(trim(need),1,dget(dt,dn,"DROP"));}
        else{kwstr=lower_copy(trim(need));}
        nio_free(need);
    }
    let pa:[]u8=nio_alloc(8192);
    let papos:i32=0;
    let pt:[]u8=nio_alloc(64*8);
    let tt:[]u8=nio_alloc(64*8);
    let st:[]u8=nio_alloc(2048*12);
    let np:i32=0;
    let nst:i32=0;
    parse_pages(buf,&np,pa,&papos,pt,tt,st,&nst,64,2048);
    let o_ans:[]u8=nio_alloc(4096);
    let o_ansn:i32=0;
    let o_widx:[]u8=nio_alloc(64*4);
    let o_wn:i32=0;
    let o_provs:i32=0;
    let o_claims:i32=0;
    let o_fl:[]u8=nio_alloc(64*4);
    let o_fln:i32=0;
    let got:i32=verdict_core(buf,np,pa,pt,tt,st,nst,qstr,"FACT","",kwstr,dt,dn,0,0,
        o_ans,&o_ansn,o_widx,&o_wn,&o_provs,&o_claims,o_fl,&o_fln);
    let m:i32=0;
    if(got==1 && o_ansn==clml && bsub_eq(o_ans,0,claim,0,clml)==1){
        m=1;
    }
    _zag_print("MERGE|");
    _zag_print(qid);
    _zag_print("|");
    _zag_println(i64s(m as i64));
    nio_free(kwstr);
    nio_free(cbuf);
    nio_free(buf);
    nio_free(pa);
    nio_free(pt);
    nio_free(tt);
    nio_free(st);
    nio_free(o_ans);
    nio_free(o_widx);
    nio_free(o_fl);
    nio_free(dt);
    return 0;
}
