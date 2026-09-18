"""Generate native synthetic self-tests; never call an experiment entry point."""
from pathlib import Path

source = Path(".scratch/e51ah/tnn_r32_e51ah_grounded_preservation_replay.zag").read_text()
marker = "fn main()i32 {"
if source.count(marker) != 1:
    raise SystemExit("expected one native main entry point")
# All native functions precede main in this frozen assembly lineage.
prefix = source.split(marker, 1)[0]
checks = [
    "e51ah_select_replay_arm(0,0)==-1",
    "e51ah_select_replay_arm(1,0)==3",
    "e51ah_select_replay_arm(0,1)==4",
    "e51ah_select_replay_arm(1,1)==3",
    "e51ah_validation_class(4200,1200,4000,1200,0)==1",
    "e51ah_validation_class(4100,1200,4000,1200,0)==2",
    "e51ah_validation_class(4100,1100,4000,1200,100)==3",
    "e51ah_validation_class(3900,1200,4000,1100,100)==3",
    "e51ah_validation_class(4100,1200,4000,1200,1)==0",
    "e51ah_validation_class(4000,1200,4000,1200,1)==0",
]
main = "fn main()i32 {\n    let failures:i32=0;\n"
for condition in checks:
    main += f"    if(!({condition})){{ failures=failures+1; }}\n"
main += """
    let records:[]i32=zalloc_i(2*E50_RECORD_N);
    let t0:[]i32=zalloc_i(2); let t1:[]i32=zalloc_i(2);
    let repeated:[]i32=zalloc_i(5*E50_RECORD_N);
    let rt0:[]i32=zalloc_i(5); let rt1:[]i32=zalloc_i(5);
    e45_zero(records,2*E50_RECORD_N); e45_zero(repeated,5*E50_RECORD_N);
    records[0]=11; records[E50_RECORD_N]=22;
    t0[0]=3; t0[1]=5; t1[0]=-3; t1[1]=-5;
    let trace:i32=0;
    e51ah_repeat_critical(records,t0,t1,2,repeated,rt0,rt1,5,&trace);
    let i:i32=0;
    while(i<5){
        let s:i32=e45_mod(i,2);
        if(repeated[i*E50_RECORD_N]!=records[s*E50_RECORD_N] || rt0[i]!=t0[s] || rt1[i]!=t1[s]){ failures=failures+1; }
        i=i+1;
    }
    if(e51ah_record_isolation(repeated,5)!=1){ failures=failures+1; }
    e51ah_repeat_critical(records,t0,t1,0,repeated,rt0,rt1,5,&trace);
    if(trace!=8209 || repeated[0]!=11){ failures=failures+1; }
    zfree(records); zfree(t0); zfree(t1); zfree(repeated); zfree(rt0); zfree(rt1);
    if(failures!=0){ _zag_println("E51AH_SYNTHETIC_SELFTESTS_FAILED"); return 1; }
    _zag_println("E51AH_SYNTHETIC_SELFTESTS_PASS=1");
    return 0;
}
"""
scratch = Path(".scratch/e51ah/preflight")
scratch.mkdir(parents=True, exist_ok=True)
(scratch / "NATIVE_SELFTEST.zag").write_text(prefix + main)
(scratch / "tnn_r32_e45_investigation_core.zag").write_bytes(
    Path("Research/tnn_r32_e45_investigation_core.zag").read_bytes())
print("Generated synthetic-only native entry point: no E50/E51 experiments invoked.")
