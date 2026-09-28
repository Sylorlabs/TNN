# CREW A — SPEED log (2026-09-25)
binary: 7f6e0ceab59ad8a65d7a3a1500021b52934f3f41f81d34588284307e5745071f
toolchain: 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
machine: 2 cores; AMD EPYC 9D64 88-Core Processor
               total        used        free      shared  buff/cache   available
Mem:               7           3           0           0           4           3
load: 5.30 4.98 2.49 7/429 5525
=== S1 matrix timing (sequential, quiet machine) ===
OK s1_v20 A/B/C identical :: 339497145 219586069 175892845 
OK s1_v26 A/B/C identical :: 245686377 210993402 308110941 
OK s10_v20 A/B/C identical :: 1595946237 1542467061 1608173119 
OK s10_v26 A/B/C identical :: 1905843545 2121140966 1506690076 
OK s100_v20 A/B/C identical :: 16505667070 19480788017 81535394486 
OK s100_v26 A/B/C identical :: 80492652104 80646829483 96320378628 
GATE-XCHECK s1 v20 == adopted m20 OK
GATE-XCHECK s10 v20 == adopted m20 OK
GATE-XCHECK s100 v20 == adopted m20 OK
=== S3 chunked tail (s1 -> 50 chunks x 20 items) ===
1000 items_ordered.txt
overhead_ns: 374427427 492191855 370283126 380071722 171446320 422176760 206283491 451893323 455560316 682105937 
chunk runs done
=== S2 deliberation steps (v26 trace; v20 by source) ===
trace-run output == scored s1_v26_A OK
L1: 1000
117:    let d1prior:i64=950000;  // millionths, used when nopool && tp==0
119:    let know:i32=0;          // 0 = d1prior at tp==0; 1 = K-A; 2 = K-B; 3 = K-C
126:    else if(variant==23){nopool=1;d1prior=500000;} // m20_ind (light T4)
263:                                if(gsel==1 && corr==1 && cl_mil<d1prior){cl_mil=d1prior;}
265:                                cl_mil=d1prior;
309:                            // d1prior at exactly this step; below unchanged.
337:                                else {cl_mil=d1prior;}
TIMING DONE 2026-09-25T18:35:35Z
