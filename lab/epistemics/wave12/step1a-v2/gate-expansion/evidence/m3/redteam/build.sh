#!/bin/bash
# build.sh — compile all 12 red-team plants with the pinned znc toolchain and
# prove run-to-run stdout variance (validity rule). Run from the redteam dir.
# Extern-shim plants (a2, b2) link their C shims via --dynamic --needed;
# run those binaries with LD_LIBRARY_PATH=.  b1 needs cwd=redteam for @import.
set -u
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
mkdir -p bin
pass=0; fail=0
build_plain() { # $1=src $2=out
  $ZNC "$1" -o "bin/$2" 2>bin/"$2".build.log || { echo "BUILD-FAIL $1"; tail -3 bin/"$2".build.log; return 1; }
}
build_dyn() { # $1=src $2=out $3=libbase (e.g. a2wall)
  cc -shared -fPIC -o "bin/lib$3.so" "${3}_shim.c" 2>/dev/null || { echo "SHIM-FAIL $3"; return 1; }
  cp "bin/lib$3.so" "bin/lib$3.so.1"
  (cd bin && $ZNC "../$1" --dynamic --needed "lib$3.so.1" -o "$2" 2>"$2".build.log) || { echo "BUILD-FAIL $1"; tail -3 bin/"$2".build.log; return 1; }
}
check() { # $1=binary $2=expected_bytes ("any" ok) $3=dyn?
  local b="$1" exp="$2" dyn="${3:-}"
  local pfx=""; [ -n "$dyn" ] && pfx="LD_LIBRARY_PATH=bin"
  # shellcheck disable=SC2086
  env $pfx "bin/$b" > bin/"$b".run1 2>/dev/null; local r1=$?
  env $pfx "bin/$b" > bin/"$b".run2 2>/dev/null; local r2=$?
  local s1 s2 len1
  s1=$(sha256sum bin/"$b".run1 | cut -d' ' -f1)
  s2=$(sha256sum bin/"$b".run2 | cut -d' ' -f1)
  len1=$(wc -c < bin/"$b".run1)
  if [ $r1 -ne 0 ] || [ $r2 -ne 0 ]; then echo "RUN-FAIL $b rc=$r1/$r2"; fail=$((fail+1)); return; fi
  if [ "$exp" != any ] && [ "$len1" -ne "$exp" ]; then echo "LEN-FAIL $b got=$len1 want=$exp"; fail=$((fail+1)); return; fi
  if [ "$s1" = "$s2" ]; then echo "NOVAR $b sha=$s1 (no run-to-run variance!)"; fail=$((fail+1)); return; fi
  echo "VALID $b len=$len1 sha1=${s1:0:16} sha2=${s2:0:16}"; pass=$((pass+1))
}

build_plain a1_gettimeofday_heap.zag a1 && check a1 8
build_dyn   a2_extern_shim.zag       a2 a2wall && check a2 8 dyn
build_plain a3_table_lookup.zag      a3 && check a3 16
build_plain b1_main.zag              b1 && check b1 8
build_dyn   b2_extern_retval.zag     b2 b2wall && check b2 8 dyn
build_plain b3_raw_syscalls.zag      b3 && check b3 8
build_plain c1_straightline.zag      c1 && check c1 16
build_plain c2_fixedloop.zag         c2 && check c2 16
build_plain c3_constbranch.zag       c3 && check c3 8
build_plain d1_flood.zag             d1 && check d1 1000000
build_plain d2_nofooter.zag          d2 && check d2 8
build_plain d3_sites.zag             d3 && check d3 8
echo "valid=$pass failed=$fail"
