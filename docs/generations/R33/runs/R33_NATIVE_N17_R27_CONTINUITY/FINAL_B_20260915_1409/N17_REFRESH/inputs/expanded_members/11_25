"""Generate synthetic-only native checks. No experimental entry point is called."""
from pathlib import Path

root = Path(".scratch/e51ai")
source = (root / "SOURCE.zag").read_text()
marker = "fn main()i32 {"
if source.count(marker) != 1:
    raise SystemExit("Non-unique main")
main = r'''
fn main()i32 {
    let failures:i32=0;
    let records:[]i32=zalloc_i(2*E50_RECORD_N); e45_zero(records,2*E50_RECORD_N);
    records[0]=13; records[32]=27; records[33]=29; records[34]=987654;
    records[E50_RECORD_N]=31; records[E50_RECORD_N+32]=37; records[E50_RECORD_N+33]=41;
    let pair:[]i32=zalloc_i(128); e45_zero(pair,128);
    if(e51ai_feature_pair(records,0,0,pair,0)!=1){ failures=failures+1; }
    if(e51ai_feature_pair(records,1,1,pair,64)!=1){ failures=failures+1; }
    if(pair[0]!=13 || pair[3]!=27 || pair[5]!=29 || pair[64]!=31 || pair[96]!=13 || pair[99]!=27){ failures=failures+1; }
    let f:i32=0; while(f<32){ if(pair[32+f]!=0){ failures=failures+1; } f=f+1; }
    if(e51ai_column(pair,1,33,1)!=13 || e51ai_column(pair,1,33,2)!=0){ failures=failures+1; }
    if(e51ai_sample(3,0,600)!=60 || e51ai_sample(3,1,600)!=217 || e51ai_sample(3,4,540)!=928){ failures=failures+1; }
    let block:i32=0;
    while(block<32){
        let p:i32=0;
        while(p<1080){
            let row:i32=e51ai_sample(3,block,p);
            if(row<0 || row>=2160){ failures=failures+1; }
            if(block<4 && row/540>block){ failures=failures+1; }
            p=p+1;
        }
        block=block+1;
    }
    let x:[]i32=zalloc_i(128); e45_zero(x,128); x[0]=1000; x[64]=-1000;
    let targets:[]i32=zalloc_i(4); e45_zero(targets,4); targets[0]=1000; targets[2]=-1000;
    let w:[]i32=zalloc_i(65); let rw:[]i32=zalloc_i(65); e45_zero(w,65); e45_zero(rw,65);
    // An inactive coordinate must survive; resetting would silently break longevity.
    w[32]=123; rw[32]=123;
    let u:i32=0; let ru:i32=0; let il:i64=0; let fl:i64=0; let ril:i64=0; let rfl:i64=0;
    if(e51ai_fit(x,targets,w,0,2,0,0,0,2,&u,&il,&fl)!=1){ failures=failures+1; }
    if(e51ai_fit(x,targets,rw,0,2,0,0,1,2,&ru,&ril,&rfl)!=1){ failures=failures+1; }
    if(w[32]!=123 || fl!=0 || il!=2000000 || ru!=u || rfl!=fl || ril!=il){ failures=failures+1; }
    f=0; while(f<65){ if(w[f]!=rw[f]){ failures=failures+1; } f=f+1; }
    let frozen:i32=e51ai_hash(w,0,65);
    if(e51ai_fit(x,targets,w,0,2,0,0,0,2,&u,&il,&fl)!=1 || il!=0 || fl!=0 || u!=0){ failures=failures+1; }
    if(e51ai_hash(w,0,65)!=frozen){ failures=failures+1; }
    if(e51ai_fit(x,targets,w,0,2,0,0,0,0,&u,&il,&fl)!=0 || e51ai_hash(w,0,65)!=frozen){ failures=failures+1; }
    zfree(records); zfree(pair); zfree(x); zfree(targets); zfree(w); zfree(rw);
    e45_print_pair("e51ai_synthetic_failures",failures);
    if(failures==0){ _zag_println("E51AI_SYNTHETIC_SELFTESTS_PASS=1"); }
    return failures;
}
'''
out = root / "preflight"
out.mkdir(exist_ok=True)
(out / "SELFTEST.zag").write_text(source.split(marker, 1)[0] + main)
(out / "tnn_r32_e45_investigation_core.zag").write_bytes((root / "tnn_r32_e45_investigation_core.zag").read_bytes())
print("Synthetic-only test source created")
