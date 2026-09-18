"""Synthetic-only native checks; no scientific world generator entry is executed."""
from pathlib import Path

root = Path(".scratch/e51aj")
source = (root/"SOURCE.zag").read_text()
marker = "fn main()i32 {"
if source.count(marker) != 1:
    raise SystemExit("non-unique main")
main = r'''
fn main()i32 {
    let failures:i32=0;
    if(e51aj_schedule_gate()!=1){ failures=failures+1; }
    if(e51aj_sample(1,0,540)!=540 || e51aj_sample(1,1,540)!=0 || e51aj_sample(2,1,0)!=270 || e51aj_sample(3,31,1079)!=539){ failures=failures+1; }
    let records:[]i32=zalloc_i(2*E50_RECORD_N); e45_zero(records,2*E50_RECORD_N);
    records[0]=13; records[32]=27; records[33]=29; records[34]=987654;
    records[E50_RECORD_N]=31; records[E50_RECORD_N+32]=37; records[E50_RECORD_N+33]=41;
    let pair:[]i32=zalloc_i(128); e45_zero(pair,128);
    if(e51aj_feature_pair(records,0,0,pair,0)!=1 || e51aj_feature_pair(records,1,1,pair,64)!=1){ failures=failures+1; }
    if(pair[0]!=13 || pair[3]!=27 || pair[5]!=29 || pair[64]!=31 || pair[96]!=13 || pair[99]!=27){ failures=failures+1; }
    let f:i32=0; while(f<32){ if(pair[32+f]!=0){ failures=failures+1; } f=f+1; }
    let arm:i32=0; while(arm<5){ if(e51aj_column(pair,1,33,arm)!=13){ failures=failures+1; } arm=arm+1; }
    let before:i32=e51aj_hash(pair,0,128); records[34]=-987654;
    if(e51aj_feature_pair(records,0,0,pair,0)!=1 || e51aj_hash(pair,0,128)!=before){ failures=failures+1; }
    let x:[]i32=zalloc_i(128); e45_zero(x,128); x[0]=1000; x[64]=-1000;
    let targets:[]i32=zalloc_i(4); e45_zero(targets,4); targets[0]=1000; targets[2]=-1000;
    let w:[]i32=zalloc_i(65); let rw:[]i32=zalloc_i(65); e45_zero(w,65); e45_zero(rw,65); w[32]=123; rw[32]=123;
    let u:i32=0; let ru:i32=0; let il:i64=0; let fl:i64=0; let ril:i64=0; let rfl:i64=0;
    if(e51aj_fit(x,targets,w,0,3,0,0,0,2,&u,&il,&fl)!=1 || e51aj_fit(x,targets,rw,0,3,0,0,1,2,&ru,&ril,&rfl)!=1){ failures=failures+1; }
    if(w[32]!=123 || fl!=0 || il!=2000000 || ru!=u || rfl!=fl || ril!=il){ failures=failures+1; }
    f=0; while(f<65){ if(w[f]!=rw[f]){ failures=failures+1; } f=f+1; }
    let frozen:i32=e51aj_hash(w,0,65);
    if(e51aj_fit(x,targets,w,0,3,0,0,0,2,&u,&il,&fl)!=1 || il!=0 || fl!=0 || u!=0 || e51aj_hash(w,0,65)!=frozen){ failures=failures+1; }
    if(e51aj_fit(x,targets,w,0,3,0,0,0,0,&u,&il,&fl)!=0 || e51aj_hash(w,0,65)!=frozen){ failures=failures+1; }
    zfree(records); zfree(pair); zfree(x); zfree(targets); zfree(w); zfree(rw);
    e45_print_pair("e51aj_synthetic_failures",failures);
    if(failures==0){ _zag_println("E51AJ_SYNTHETIC_SELFTESTS_PASS=1"); }
    return failures;
}
'''
out = root/"preflight"
out.mkdir(exist_ok=True)
(out/"SELFTEST.zag").write_text(source.split(marker,1)[0]+main)
(out/"tnn_r32_e45_investigation_core.zag").write_bytes((root/"tnn_r32_e45_investigation_core.zag").read_bytes())
print("E51AJ synthetic-only source created")
