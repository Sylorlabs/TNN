from pathlib import Path
import re,json,subprocess,hashlib,os
r=Path('/mnt/data/r32_epistemic');src=r/'tnn_r32_epistemic_chunking.zag';z=r/'znc'
out={'eligible':(r/'R32_NATIVE_LATEST_PASS.flag').exists() and z.exists() and src.exists()}
if out['eligible']:
 s=src.read_text();s2,n=re.subn(r'fn\s+main\s*\(\s*\)\s*i32', 'fn source_gate_main()i32', s, count=1)
 out['renamed_main']=n
 harness=r'''

fn main()i32 {
    let predicted:[]i32=new i32(8);let noise:[]i32=new i32(4);let cost:[]i32=new i32(4);
    let group:[]i32=new i32(4);let seen:[]i32=new i32(2);let features:[]i32=new i32(R32_EQUIV_FEATURES);
    let weights:[]i32=new i32(R32_EQUIV_FEATURES);let i:i32=0;while(i<R32_EQUIV_FEATURES){weights[i]=1;i=i+1;}
    i=0;while(i<4){noise[i]=100;cost[i]=100+i*50;group[i]=i/2;i=i+1;}seen[0]=0;seen[1]=0;
    // Resolvable: at least one affordable observation strongly separates candidates.
    predicted[0]=100;predicted[1]=200;predicted[2]=300;predicted[3]=400;
    predicted[4]=700;predicted[5]=220;predicted[6]=310;predicted[7]=410;
    let obs:i32=-1;let gain_res:i32=r32_best_affordable_separation(0,1,4,predicted,noise,cost,400,seen,group,2,&obs);
    r32_equivalence_features(250,750,500,300,100,700,gain_res,features);
    let decision_res:i32=r32_equivalence_decide(features,weights,0,500,150,100,100);
    // Underdetermined: all affordable observation predictions are identical.
    i=0;while(i<4){predicted[i]=100+i*10;predicted[4+i]=predicted[i];i=i+1;}
    let gain_amb:i32=r32_best_affordable_separation(0,1,4,predicted,noise,cost,400,seen,group,2,&obs);
    r32_equivalence_features(0,1000,500,300,100,700,gain_amb,features);
    let decision_amb:i32=r32_equivalence_decide(features,weights,0,500,150,100,100);
    metric("native_resolvable_gain_positive",bool_i32(gain_res>150));
    metric("native_resolvable_continue",bool_i32(decision_res==0));
    metric("native_underdetermined_gain_zero",bool_i32(gain_amb==0));
    metric("native_underdetermined_unknown",bool_i32(decision_amb==-1));
    metric("native_source_gate_retained",bool_i32(source_gate_main()==0));
    if(gain_res>150 && decision_res==0 && gain_amb==0 && decision_amb==-1){_zag_println("R32_NATIVE_EPISTEMIC_HARNESS=PASS");return 0;}
    _zag_println("R32_NATIVE_EPISTEMIC_HARNESS=FAIL");return 1;
}
'''
 h=r/'r32_native_epistemic_harness.zag';h.write_text(s2+harness)
 b=r/'r32_native_epistemic_harness'
 q=subprocess.run([str(z),str(h),'-o',str(b)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=1200)
 out['compile']={'rc':q.returncode,'stdout':q.stdout.decode('utf-8','replace')[:5000],'stderr':q.stderr.decode('utf-8','replace')[:20000],'binary_exists':b.exists()}
 if b.exists():
  out['binary_sha256']=hashlib.sha256(b.read_bytes()).hexdigest();os.chmod(b,0o755)
  rr=subprocess.run([str(b)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=300)
  out['run']={'rc':rr.returncode,'stdout':rr.stdout.decode('utf-8','replace'),'stderr':rr.stderr.decode('utf-8','replace')}
  out['pass']=rr.returncode==0 and 'R32_NATIVE_EPISTEMIC_HARNESS=PASS' in out['run']['stdout']
 else:out['pass']=False
else:
 out['pass']=False;out['reason']='Verified native compiler gate unavailable.'
(r/'R32_NATIVE_EPISTEMIC_HARNESS_STATUS.json').write_text(json.dumps(out,indent=2))
