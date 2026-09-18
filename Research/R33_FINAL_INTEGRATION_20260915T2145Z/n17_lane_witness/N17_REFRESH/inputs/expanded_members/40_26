from pathlib import Path
import re,json,subprocess,hashlib,os
r=Path('/mnt/data/r32_epistemic');src=r/'tnn_r32_epistemic_chunking.zag';z=r/'znc'
out={'eligible':(r/'R32_NATIVE_LATEST_PASS.flag').exists() and z.exists() and src.exists()}
if out['eligible']:
 s=src.read_text();s2,n=re.subn(r'fn\s+main\s*\(\s*\)\s*i32','fn source_gate_main()i32',s,count=1);out['renamed_main']=n
 harness=r'''

fn r32_native_noise(seed:i32,case_id:i32,step:i32,scale:i32)i32 @noalloc {
    let v:i32=mod_pos(mix(seed+case_id*17,step*101+case_id),2001)-1000;return v*scale/1000;
}
fn r32_native_two_score(observed:i32,pred0:i32,pred1:i32,noise:i32,out:[]i32)void @noalloc {
    let n:i32=max_i32(1,noise);out[0]=0-abs_i32(observed-pred0)*1000/n;out[1]=0-abs_i32(observed-pred1)*1000/n;
}
fn main()i32 {
    let N:i32=6000;let predicted:[]i32=new i32(8);let noise:[]i32=new i32(4);let cost:[]i32=new i32(4);
    let group:[]i32=new i32(4);let seen:[]i32=new i32(2);let local:[]i32=new i32(2);
    let fixed_correct:i32=0;let fixed_wrong:i32=0;let eq_correct:i32=0;let eq_unknown_good:i32=0;let eq_wrong:i32=0;let i:i32=0;
    noise[0]=160;noise[1]=180;noise[2]=220;noise[3]=200;cost[0]=80;cost[1]=100;cost[2]=140;cost[3]=300;
    group[0]=0;group[1]=0;group[2]=1;group[3]=1;
    while(i<N){let cond:i32=mod_pos(mix(901,i),4);let truth:i32=mod_pos(mix(777,i),2);let ambiguous:i32=0;let available_budget:i32=400;
        predicted[0]=100;predicted[1]=220;predicted[2]=340;predicted[3]=460;
        predicted[4]=700;predicted[5]=250;predicted[6]=360;predicted[7]=480;
        if(cond==1){ambiguous=1;predicted[4]=predicted[0];predicted[5]=predicted[1];predicted[6]=predicted[2];predicted[7]=predicted[3];}
        if(cond==2){group[0]=0;group[1]=0;group[2]=0;group[3]=0;}else{group[0]=0;group[1]=0;group[2]=1;group[3]=1;}
        if(cond==3){predicted[4]=predicted[0];predicted[5]=predicted[1];predicted[6]=predicted[2];predicted[7]=800;available_budget=220;ambiguous=1;}
        // Fixed baseline uses the first source and commits.
        let mean0:i32=predicted[truth*4];let obs0:i32=mean0+r32_native_noise(333,i,0,noise[0]);r32_native_two_score(obs0,predicted[0],predicted[4],noise[0],local);
        let fixed:i32=0;if(local[1]>local[0]){fixed=1;}if(ambiguous==0 && fixed==truth){fixed_correct=fixed_correct+1;}else{fixed_wrong=fixed_wrong+1;}
        // Equivalence policy examines the best affordable independent observation.
        seen[0]=0;seen[1]=0;let best_obs:i32=-1;let gain:i32=r32_best_affordable_separation(0,1,4,predicted,noise,cost,available_budget,seen,group,2,&best_obs);
        if(gain<=120){if(ambiguous==1){eq_unknown_good=eq_unknown_good+1;}else{eq_wrong=eq_wrong+1;}}
        else{let mean:i32=predicted[truth*4+best_obs];let ob:i32=mean+r32_native_noise(551,i,best_obs,noise[best_obs]);r32_native_two_score(ob,predicted[best_obs],predicted[4+best_obs],noise[best_obs],local);
            let pred:i32=0;if(local[1]>local[0]){pred=1;}if(ambiguous==0 && pred==truth){eq_correct=eq_correct+1;}else if(ambiguous==1){eq_wrong=eq_wrong+1;}else{eq_wrong=eq_wrong+1;}}
        i=i+1;
    }
    metric("native_quant_fixed_correct_permille",fixed_correct*1000/N);
    metric("native_quant_fixed_wrong_permille",fixed_wrong*1000/N);
    metric("native_quant_equivalence_correct_permille",eq_correct*1000/N);
    metric("native_quant_equivalence_unknown_good_permille",eq_unknown_good*1000/N);
    metric("native_quant_equivalence_wrong_permille",eq_wrong*1000/N);
    let eq_utility:i32=eq_correct+eq_unknown_good-eq_wrong;let fixed_utility:i32=fixed_correct-fixed_wrong;
    metric("native_quant_equivalence_beats_fixed",bool_i32(eq_utility>fixed_utility));
    if(eq_utility>fixed_utility && eq_unknown_good>0 && eq_correct>0){_zag_println("R32_NATIVE_QUANT_EPISTEMIC=PASS");return 0;}
    _zag_println("R32_NATIVE_QUANT_EPISTEMIC=FAIL");return 1;
}
'''
 h=r/'r32_native_quantitative_epistemic.zag';h.write_text(s2+harness);b=r/'r32_native_quantitative_epistemic'
 q=subprocess.run([str(z),str(h),'-o',str(b)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=1200)
 out['compile']={'rc':q.returncode,'stdout':q.stdout.decode('utf-8','replace')[:5000],'stderr':q.stderr.decode('utf-8','replace')[:30000],'binary_exists':b.exists()}
 if b.exists():
  os.chmod(b,0o755);out['binary_sha256']=hashlib.sha256(b.read_bytes()).hexdigest();rr=subprocess.run([str(b)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=300)
  out['run']={'rc':rr.returncode,'stdout':rr.stdout.decode('utf-8','replace'),'stderr':rr.stderr.decode('utf-8','replace')};out['pass']=rr.returncode==0 and 'R32_NATIVE_QUANT_EPISTEMIC=PASS' in out['run']['stdout']
 else:out['pass']=False
else:out['pass']=False;out['reason']='Verified native compiler gate unavailable.'
(r/'R32_NATIVE_QUANTITATIVE_EPISTEMIC_STATUS.json').write_text(json.dumps(out,indent=2))
