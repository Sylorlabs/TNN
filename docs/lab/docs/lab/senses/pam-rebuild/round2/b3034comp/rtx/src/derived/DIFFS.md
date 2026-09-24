# RT-X derived-source diffs (mechanical, script-applied)

## drive3034_ad0e1ddd.zag -> drive3034_lib.zag

```diff
--- 
+++ 
@@ -537,7 +537,7 @@
 }
 
 // ---------- main ----------
-fn main() void {
+fn comp_main_unused() void {
     let ob:[]u8 = nio_alloc(65536);
     let pos:i32 = 0;
     pos = ob_puts(ob, pos, "B3034COMP drive3034 | prereg d9e72746 | pure Zag, zero RNG\n");
```

## drive3034_lib.zag -> drive3034_ablate_p1.zag

```diff
--- 
+++ 
@@ -38,20 +38,17 @@
     let temporal_ok:i32 = 1;
     let h0:i64 = cont_hash(id, label, conf, meas, extra);
     let e:i64 = 0;
-    while(e < 3) {
-        if(e < (maxv as i64)) {
+    while(e < 1) {
+        if(1 == 1) {
             let tv:i64 = tick; tick = tick + 1;
             let bit:i32 = 0;
             if(corrupt == 1) { bit = verdict_bit_corrupt(id, label, conf, meas, extra); }
             else { bit = verdict_bit(1, id, label, conf, meas, extra, seed); }
             let bnd:i64 = verdict_bound(1, id, label, conf, meas, extra, seed);
             let td:i64 = tick; tick = tick + 1;
-            if(tv < t_present) { temporal_ok = 0; }
-            if(td < tv) { temporal_ok = 0; }
             if(bit == 0) { all1 = 0; }
             if(bind_ok(1, bnd, id, label, conf, meas, extra, seed) == 0) { all1 = 0; }
             let he:i64 = cont_hash(id, label, conf, meas, extra);
-            if(he != h0) { all1 = 0; }
         }
         e = e + 1;
     }
```

## drive3034_ablate_p1.zag -> drive3034_ablate_p2.zag

```diff
--- 
+++ 
@@ -1,5 +1,5 @@
 @import("R33_NATIVE_IO_V1.zag")
-@import("b303134_common.zag")
+@import("b303134_common_ablate_p2.zag")
 
 // drive3034.zag — C-3034 composition: H-PAM-30's full-pin verdict gate as the
 // admission surface + H-PAM-34's interleave/delay-line protocol as the
```

## b303134_common.zag -> b303134_common_ablate_p2.zag

```diff
--- 
+++ 
@@ -133,9 +133,7 @@
 // binding check: recompute from the PRESENTED percept, compare to the attached
 // verdict object's bound. P-class arm replays a bound computed over X with Y.
 fn bind_ok(pin:i32, attached:i64, id:i64, label:i64, conf:i64, meas:i64, extra:i64, seed:i64) i32 {
-    let re:i64 = verdict_bound(pin, id, label, conf, meas, extra, seed);
-    if(re == attached) { return 1; }
-    return 0;
+    return 1;
 }
 
 // ---------- sinks ----------
```

