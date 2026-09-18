from pathlib import Path
import re,json,subprocess,hashlib,os
r=Path('/mnt/data/r32_epistemic');src=r/'tnn_r32_epistemic_chunking.zag';z=r/'znc'
out={'eligible':(r/'R32_NATIVE_LATEST_PASS.flag').exists() and z.exists() and src.exists()}
if out['eligible']:
 s=src.read_text();s2,n=re.subn(r'fn\s+main\s*\(\s*\)\s*i32','fn source_gate_main()i32',s,count=1);out['renamed_main']=n
 harness=r'''

fn main()i32 {
    let seq:[]i32=new i32(12);seq[0]=4;seq[1]=7;seq[2]=4;seq[3]=9;seq[4]=2;seq[5]=3;
    seq[6]=4;seq[7]=7;seq[8]=4;seq[9]=9;seq[10]=5;seq[11]=6;
    let p_hash:[]i32=new i32(R31_PROPOSAL_MAX);let p_len:[]i32=new i32(R31_PROPOSAL_MAX);
    let p_data:[]i32=new i32(R31_PROPOSAL_MAX*R31_CHUNK_LEN_MAX);let p_seen:[]i32=new i32(R31_PROPOSAL_MAX);
    let p_sum:[]i32=new i32(R31_PROPOSAL_MAX);let p_n:[]i32=new i32(R31_PROPOSAL_MAX);let p_count:i32=0;
    let pass:i32=0;while(pass<8){r31_observe_stream(seq,700,6,p_hash,p_len,p_data,p_seen,p_sum,p_n,&p_count);pass=pass+1;}
    let c_len:[]i32=new i32(R31_CHUNK_MAX);let c_data:[]i32=new i32(R31_CHUNK_MAX*R31_CHUNK_LEN_MAX);
    let c_use:[]i32=new i32(R31_CHUNK_MAX);let c_utility:[]i32=new i32(R31_CHUNK_MAX);let c_count:i32=0;
    r31_promote_chunks(p_len,p_data,p_seen,p_sum,p_n,p_count,c_len,c_data,c_use,c_utility,&c_count,3,500);
    let ids:[]i32=new i32(32);let starts:[]i32=new i32(32);let lens:[]i32=new i32(32);let nids:i32=0;
    r31_segment(seq,c_len,c_data,c_use,c_count,ids,starts,lens,&nids,32);
    let rebuilt:[]i32=new i32(32);let rebuilt_n:i32=0;r31_reconstruct(ids,lens,nids,c_len,c_data,rebuilt,&rebuilt_n,32);
    let exact:i32=1;let i:i32=0;if(rebuilt_n!=seq.len){exact=0;}
    while(i<seq.len && i<rebuilt_n){if(seq[i]!=rebuilt[i]){exact=0;}i=i+1;}
    let score_good:i32=r31_dual_evidence_score(800,750,700,600);
    let score_bad:i32=r31_dual_evidence_score(800,200,700,600);
    let reopen:i32=r31_should_retrieve_raw(200,850,400,500);
    metric("native_chunks_recruited",bool_i32(c_count>0));
    metric("native_chunk_roundtrip_exact",exact);
    metric("native_chunk_compression",bool_i32(nids<seq.len));
    metric("native_dual_raw_dominates_bad_chunk",bool_i32(score_bad>=400));
    metric("native_raw_reopened_on_low_trust",reopen);
    if(c_count>0 && exact==1 && nids<seq.len && score_bad>=400 && reopen==1){_zag_println("R32_NATIVE_DUAL_ROUTE_HARNESS=PASS");return 0;}
    _zag_println("R32_NATIVE_DUAL_ROUTE_HARNESS=FAIL");return 1;
}
'''
 h=r/'r32_native_dual_route_harness.zag';h.write_text(s2+harness);b=r/'r32_native_dual_route_harness'
 q=subprocess.run([str(z),str(h),'-o',str(b)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=1200)
 out['compile']={'rc':q.returncode,'stdout':q.stdout.decode('utf-8','replace')[:5000],'stderr':q.stderr.decode('utf-8','replace')[:20000],'binary_exists':b.exists()}
 if b.exists():
  os.chmod(b,0o755);out['binary_sha256']=hashlib.sha256(b.read_bytes()).hexdigest();rr=subprocess.run([str(b)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=300)
  out['run']={'rc':rr.returncode,'stdout':rr.stdout.decode('utf-8','replace'),'stderr':rr.stderr.decode('utf-8','replace')};out['pass']=rr.returncode==0 and 'R32_NATIVE_DUAL_ROUTE_HARNESS=PASS' in out['run']['stdout']
 else:out['pass']=False
else:out['pass']=False;out['reason']='Verified native compiler gate unavailable.'
(r/'R32_NATIVE_DUAL_ROUTE_HARNESS_STATUS.json').write_text(json.dumps(out,indent=2))
