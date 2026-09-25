# CREW B — COST log (2026-09-25)
binary: 7f6e0ceab59ad8a65d7a3a1500021b52934f3f41f81d34588284307e5745071f (213837 bytes)
nec_v3c.zag: c3fed78f7ff29f2683ed42807bb7c00acd6d8850cf26546a016192203ac7c95e
schema_kc.zag: b6aa3327ff72df5e75029cb3d66058dcdb53ebd5f1d58da9d941539a1dfdf8ab (38271 bytes)
=== C1 per-item ledger (white-box source inspection) ===
142:    let ibuf:[]u8=nio_alloc(buf_bytes);
148:    // Ledger: 35*16 = 560 bytes, zeroed by nio_alloc
149:    let ld:[]u8=nio_alloc(35*16);
153:    let slots:[]u8=nio_alloc((max_items as i64)*64);
155:    let confs:[]u8=nio_alloc((max_items as i64)*8);
158:    let pcp:[]u8=nio_alloc((max_items as i64)*8);
160:    let ptp:[]u8=nio_alloc((max_items as i64)*8);
162:    let htab:[]u8=nio_alloc(htsize*8);
slots per-item bytes: 64
confs per-item bytes: 8
pcp per-item bytes: 8
ptp per-item bytes: 8
C1 total per-item ledger bytes = 64+8+8+8 = 88
135:    let max_items:i32=nec_max_items(scale);
48:// htab: htsize entries, each 8 bytes (i64 slot index, -1 = empty).
138:    let htsize:i64=2;
139:    while(htsize < (max_items as i64)*2){htsize=htsize*2;}
140:    let htmask:i64=htsize-1;
=== C2 schema footprint (static) ===
558
fn kc_l2(f1:i32, f5:i32, tot:*i64, rate:*i64)i32 {
    if(f1==100 && f5==125){tot.*=10;rate.*=0;return 1;}
fn kc_l3(dep:i32, tot:*i64, rate:*i64)i32 {
    if(dep==1){tot.*=1000;rate.*=802000;return 1;}
C2 data-equivalent: L1 312*40=12480 + L2 246*32=7872 + L3 7*24=168 = 20520 B
m20 schema footprint: 0 B (d1prior is a compiled constant, no table)
=== C4 deliberation depth distribution (input property) ===
   1000 1
   1000 2
   1000 4
   1000 8
   1000 16
    120 32
    120 64
depth 16: 1000 rows
depth 1: 1000 rows
depth 2: 1000 rows
depth 32: 120 rows
depth 4: 1000 rows
depth 64: 120 rows
depth 8: 1000 rows
waiting for speed timing_done.flag ...
=== C2 RSS delta (v26 - v20), /usr/bin/time -v, 3x each ===
rss_s1_v20 KB: 
=== C2 RSS (python resource.ru_maxrss, KB), 2x per leg ===
rss_s1_v20 11536 11400
rss_s1_v26 11664 11524
rss_s10_v20 17740 17672
rss_s10_v26 17716 17732
rss_s100_v20 73972 73916
rss_s100_v26 73804 73920
RSS-run v20 s1 == scored output OK
RSS-run v26 s100 == scored output OK
=== C3 output bytes per item (from scored outputs) ===
s1 v20: 172991 bytes
s1 v26: 176600 bytes
s10 v20: 2096710 bytes
s10 v26: 2132800 bytes
s100 v20: 22015100 bytes
s100 v26: 22376000 bytes
=== C5 projection (1M items x 100 obs = 100M rows) ===
INTERLEAVED s10 validation (5 alternating pairs, ns):
COST DONE 2026-09-25T18:48:25Z
=== C5 projection (1M items x 100 obs = 100M rows) — corrected run ===
INTERLEAVED s10 validation (5 alternating pairs, drift-cancelling):
  v20 median 12.61s | v26 median 9.66s | median ratio v26/v20 = 0.766
per-row wall medians (ns), sequential legs:
  v20: s1 41905.7 | s10 30457.0 | s100 37177.1
  v26: s1 46886.7 | s10 36371.1 | s100 153906.2 (CONTENTION-POLLUTED)
v20 PROJECTION from s10 medians: wall 3046s = 0.85h; ledger 0.088GB; output 4.00GB (40.01 B/row)
v26 PROJECTION from s10 medians: wall 3637s = 1.01h; ledger 0.088GB; output 4.07GB (40.70 B/row)
Reading: the +19% sequential-median gap at s10 is INSIDE the noise band —
the interleaved (drift-cancelling) median ratio is 0.77 (v26 faster). The two
methods bracket 1.0: no measurable per-row wall difference. Projection walls
are effectively equal within noise; ledger identical; output +1.7% for v26
(7-char '1000000' confs vs 6-char '950000' — audit-byte formatting, not mechanism).
Assumptions: linear extrapolation from s10 medians; arena allocator constant;
single-threaded; no page-cache/GC effects; schema shared (not per-item).
RSS model: measured base + 88 B/item + schema (static 20,520 B data-equiv / ~+126KB resident at s1, ~0 at s10+).
COST DONE (corrected) 2026-09-25T18:49:37Z
