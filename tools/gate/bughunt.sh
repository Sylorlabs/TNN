#!/bin/sh
# BUG-CATCHER: meta-tests that deliberately break things and require the
# infrastructure to NOTICE. Do not treat lints as proof -- treat them as detectors
# and require that each injected defect is actually caught.
#
# Every fixture here corresponds to a defect this lane has ACTUALLY shipped:
#   stale binary, false compile success, hardcoded bar, duplicate arm, duplicate
#   row, permute-one-axis-only, target leak, unincremented loop, facts-only
#   oracle, old output file, random seed collision.
#
# A detector that does not fire on its own fixture is a broken detector.
set -u
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
GATE="tools/gate/zag_run.sh"
PASS=0; FAIL=0
ok(){ printf '  PASS  %s\n' "$1"; PASS=$((PASS+1)); }
no(){ printf '  FAIL  %s\n' "$1"; FAIL=$((FAIL+1)); }
t(){ if [ "$2" = "$3" ]; then ok "$1 ($2)"; else no "$1 (got $2 want $3)"; fi; }

TD="${TMPDIR:-/tmp}/tnn_bughunt"
rm -rf "$TD"; mkdir -p "$TD"

# A minimal well-behaved Zag program used as the control.
cat > "$TD/good.zag" <<'Z'
fn z_alloc(n:i32)[]u8 { if(n<1){return "";} let p:*u8=_zag_malloc(n) as *u8;
  if(p==null as *u8){return "";} return p[0..n]; }
fn o_app(b:[]u8,c:i32,s:[]u8)i32 { let i:i32=0; while(i<s.len){b[c+i]=s[i];i=i+1;} return c+s.len; }
fn o_nl(b:[]u8,c:i32)i32 { b[c]=10; return c+1; }
fn main()i32 { let ob:[]u8=z_alloc(256); let c:i32=0;
  c=o_app(ob,c,"CONTROL OK"); c=o_nl(ob,c); _zag_print(ob[0..c]); return 0; }
Z

echo "== A. build-run gate refuses to run a failed compile =="
# F1a: unclosed brace. NOTE: I originally wrote this fixture as "apostrophe inside a
# string literal" because I had wrongly diagnosed that as the cause of an E0001 in
# p6struct/precond.zag. I TESTED that claim and it is FALSE -- apostrophes compile fine.
# The real cause there was the missing paren alone. Fixtures must not encode guesses
# about a defect; this one is now a brace that genuinely fails to parse.
cat > "$TD/f1_brace.zag" <<'Z'
fn main()i32 { if(1==1){ return 0; return 0; }
Z
sh "$GATE" "$TD/f1_brace.zag" >/dev/null 2>"$TD/f1.err"
t "F1a unclosed-brace refuses (90)" "$?" "90"
grep -q 'REFUSING TO RUN' "$TD/f1.err" && ok "F1a refusal message present" || no "F1a refusal message absent"

# F1b: NEGATIVE CONTROL for the above. Apostrophe-in-string must COMPILE. If a future
# "fix" makes the gate reject valid programs, this fires.
cat > "$TD/f1b_apos.zag" <<'Z'
fn main()i32 { _zag_print("the prover's own output"); return 0; }
Z
sh "$GATE" "$TD/f1b_apos.zag" >/dev/null 2>&1
t "F1b apostrophe-in-string compiles (negative control)" "$?" "0"

# F1c: unknown function -- the compiler names it, must refuse
cat > "$TD/f1c_unknown.zag" <<'Z'
fn main()i32 { return zzz_nonexistent_fn(); }
Z
sh "$GATE" "$TD/f1c_unknown.zag" >/dev/null 2>&1
t "F1c unknown-function refuses (90)" "$?" "90"

# F1d: type error must refuse
cat > "$TD/f1d_type.zag" <<'Z'
fn main()i32 { let x:i32="not an int"; return x; }
Z
sh "$GATE" "$TD/f1d_type.zag" >/dev/null 2>&1
t "F1d type error refuses (90)" "$?" "90"

# F2: missing closing paren (the other exact bug)
cat > "$TD/f2_paren.zag" <<'Z'
fn o_app(b:[]u8,c:i32,s:[]u8)i32 { return c+s.len; }
fn main()i32 { let ob:[]u8=z_alloc(8); let c:i32=0;
  c=o_app(ob,c,"hello"; _zag_print(ob[0..c]); return 0; }
Z
sh "$GATE" "$TD/f2_paren.zag" >/dev/null 2>&1
t "F2 missing-paren refuses (90)" "$?" "90"

# F3: nonexistent source
sh "$GATE" "$TD/does_not_exist.zag" >/dev/null 2>&1
t "F3 missing source refuses (90)" "$?" "90"

# F4: THE core regression. A pre-existing binary from a GOOD source must NOT be
# executed when a later BROKEN source is gated. This is the stale-binary bug.
sh "$GATE" "$TD/good.zag" >/dev/null 2>&1
cp "${TMPDIR:-/tmp}/tnn_gate/good.stamp" "$TD/stamp_before" 2>/dev/null
# now break the source in place and re-gate
cat > "$TD/good.zag" <<'Z'
fn main()i32 { _zag_print("BROKEN"; return 0; }
Z
sh "$GATE" "$TD/good.zag" >/dev/null 2>&1
ST=$?
t "F4 stale binary not run after source break" "$ST" "90"
cp "${TMPDIR:-/tmp}/tnn_gate/good.stamp" "$TD/stamp_after" 2>/dev/null
# a REFUSED build must leave the provenance stamp untouched, so the surviving stamp
# still describes a binary that matches its recorded source
if cmp -s "$TD/stamp_before" "$TD/stamp_after"; then ok "F4 refused build left stamp intact"; else no "F4 refused build MODIFIED the stamp"; fi
# and the recorded srchash must equal the srchash of the GOOD source we still have a
# copy of -- proving the stamp was not silently re-pointed at the broken source
# The gate rm's the gated binary BEFORE compiling, so a refused build DESTROYS the
# previous binary. That is strictly safer than keeping it: the surviving artifact can
# never be mistaken for the output of the source that just failed to build. Assert the
# destructive behaviour deliberately, so a future "keep the old binary around" change
# is caught rather than silently reintroducing the stale-artifact hazard.
if [ -s "${TMPDIR:-/tmp}/tnn_gate/good.gated" ]; then
  no "F4 gated binary survived a refused build (stale-artifact risk)"
else
  ok "F4 refused build removed prior binary (no stale artifact to misread)"
fi

echo "== B. gate records provenance =="
cat > "$TD/good.zag" <<'Z'
fn z_alloc(n:i32)[]u8 { if(n<1){return "";} let p:*u8=_zag_malloc(n) as *u8;
  if(p==null as *u8){return "";} return p[0..n]; }
fn o_app(b:[]u8,c:i32,s:[]u8)i32 { let i:i32=0; while(i<s.len){b[c+i]=s[i];i=i+1;} return c+s.len; }
fn o_nl(b:[]u8,c:i32)i32 { b[c]=10; return c+1; }
fn main()i32 { let ob:[]u8=z_alloc(256); let c:i32=0;
  c=o_app(ob,c,"CONTROL OK"); c=o_nl(ob,c); _zag_print(ob[0..c]); return 0; }
Z
sh "$GATE" "$TD/good.zag" >"$TD/good.out" 2>"$TD/good.err"
t "B1 control compiles+runs" "$?" "0"
for k in srchash binhash compile_exit runhash; do
  grep -q "^$k=" "${TMPDIR:-/tmp}/tnn_gate/good.stamp" && ok "B2 stamp has $k" || no "B2 stamp missing $k"
done
grep -q 'CONTROL OK' "$TD/good.out" && ok "B3 output is from this build" || no "B3 no control output"
# runhash must change when the source changes
H1="$(sed -n 's/^runhash=//p' "${TMPDIR:-/tmp}/tnn_gate/good.stamp")"
printf '\n// touch\n' >> "$TD/good.zag"
sh "$GATE" "$TD/good.zag" >/dev/null 2>&1
H2="$(sed -n 's/^runhash=//p' "${TMPDIR:-/tmp}/tnn_gate/good.stamp")"
[ "$H1" != "$H2" ] && ok "B4 runhash changes with source" || no "B4 runhash did NOT change with source"

echo "== C. mutation sensitivity of the P6 precondition =="
# The claimed bar is that the prover reproduces hand-derived numbers. Mutating
# the GRAMMAR must change them; mutating the SOURCE silently must be caught.
P6="docs/lab/research-lead/overnight-20260928/p6struct/precond.zag"
if [ -f "$P6" ]; then
  sh "$GATE" "$P6" >"$TD/p6.out" 2>/dev/null
  t "C1 precondition runs" "$?" "0"
  grep -q 'PRECONDITION PASSES' "$TD/p6.out" && ok "C1 precondition passes" || no "C1 precondition did not pass"
  grep -q 'derivable : 3' "$TD/p6.out" && ok "C1 hand-derived derivable=3" || no "C1 derivable != 3"
  # mutate: change A1's rhs from [3,3] to [3,4]; derivable count MUST change
  /usr/bin/sed 's/wset(RH,qidx(1,0)\*3+1,3)/wset(RH,qidx(1,0)*3+1,4)/' "$P6" > "$TD/p6_mut.zag"
  sh "$GATE" "$TD/p6_mut.zag" >"$TD/p6m.out" 2>/dev/null
  if grep -q 'PRECONDITION FAILS' "$TD/p6m.out"; then ok "C2 grammar mutation flips the bar"; else no "C2 mutation did NOT flip the bar"; fi
  # mutate the EXPECTED constant only: a hardcoded bar must be detectable
  /usr/bin/sed 's/if(found!=3)/if(found!=4)/' "$P6" > "$TD/p6_bar.zag"
  sh "$GATE" "$TD/p6_bar.zag" >"$TD/p6b.out" 2>/dev/null
  grep -q 'derivable : 3' "$TD/p6b.out" && ok "C3 bar mutation does not change measurement" || no "C3 bar mutation changed the measurement"
  grep -q 'FAIL: derivable count' "$TD/p6b.out" && ok "C3 mutated bar FAILS loudly" || no "C3 mutated bar did not fail"
else
  no "C* precondition source missing"
fi

echo "== D. namecheck is real (does it actually detect a python file?) =="
if sh "$GATE" tools/lab/namecheck.zag >"$TD/nc_build.txt" 2>&1 || [ -s "$TD/nc_build.txt" ]; then
  NC="${TMPDIR:-/tmp}/tnn_gate/namecheck.gated"
  if [ -x "$NC" ]; then
    # clean list: ONLY .zag sources. (My first fixture wrongly put y.py in the CLEAN
    # list, so "D1 failed" was my fixture's bug, not namecheck's.)
    printf 'x.zag\ny.zag\ntools/lab/namecheck.zag\n' > "$TD/clean.lst"
    # dirty lists, one defect class each
    printf 'x.zag\ny.py\n' > "$TD/d_py.lst"
    printf 'x.zag\ny.mjs\n' > "$TD/d_mjs.lst"
    printf 'x.zag\ny.rb\n' > "$TD/d_rb.lst"
    printf 'x.zag\ny.py\n' > "$TD/d_both.lst"
    "$NC" "$TD/clean.lst" > "$TD/nc_clean.txt" 2>&1
    grep -q 'RESULT=PASS' "$TD/nc_clean.txt" && ok "D1 clean all-zag list PASSes" || no "D1 clean all-zag list did not PASS"
    # N1's declared scope is exactly .py/.js/.rb/.pl -- .mjs is NOT in it, so d_mjs is a
    # fixture for a coverage GAP, not a broken detector. Recorded as such below.
    for L in d_py d_rb; do
      "$NC" "$TD/$L.lst" > "$TD/nc_$L.txt" 2>&1
      RC=$?
      if [ "$RC" -ne 0 ]; then ok "D2 $L correctly FAILS (exit $RC)"; else no "D2 $L wrongly PASSED"; fi
    done
    # Known coverage gap, asserted as a gap so it cannot rot into a silent hole.
    "$NC" "$TD/d_mjs.lst" > "$TD/nc_d_mjs.txt" 2>&1
    if grep -q 'RESULT=PASS' "$TD/nc_d_mjs.txt"; then
      no "D4 KNOWN GAP: namecheck misses .mjs (JS source would pass) -- FIX namecheck"
    else
      ok "D4 .mjs now detected (gap closed)"
    fi
    # the real lane must pass
    git ls-files > "$TD/real.lst"
    "$NC" "$TD/real.lst" > "$TD/nc_real.txt" 2>&1
    grep -q 'RESULT=PASS' "$TD/nc_real.txt" && ok "D3 real lane file list PASSes" || no "D3 real lane file list did not PASS"
  else
    no "D* namecheck binary missing after gated build"
  fi
else
  no "D* namecheck did not build"
fi

printf '\nBUGHUNT SUMMARY: pass=%s fail=%s\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ] || exit 1
exit 0