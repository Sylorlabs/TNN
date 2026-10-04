#!/bin/sh
# verify_clh2.sh -- sealed evaluation checks for CLH2 (shell only).
# Prints PASS/FAIL per check. Exits nonzero on any FAIL.
LANE="/home/hatch/workspace/tnn-rsi/docs/lab/rsi/runs/wave-20261002-0521pdt/CONTLEARN"
cd "$LANE" || exit 1
fail=0
chk() { # chk <name> <expected> <actual>
  if [ "$2" = "$3" ]; then echo "PASS $1: $3"; else echo "FAIL $1: want [$2] got [$3]"; fail=1; fi
}
# ---- CP-R6 determinism: 3x byte-identical per binary ----
for m in TREAT CONTROL NOPHASE; do
  h1=$(sha256sum "transcript_${m}_r1.txt" | cut -d' ' -f1)
  h2=$(sha256sum "transcript_${m}_r2.txt" | cut -d' ' -f1)
  h3=$(sha256sum "transcript_${m}_r3.txt" | cut -d' ' -f1)
  if [ "$h1" = "$h2" ] && [ "$h2" = "$h3" ]; then echo "PASS determinism $m: $h1"; else echo "FAIL determinism $m: $h1 $h2 $h3"; fail=1; fi
  f1=$(grep -m1 "^FNV " "transcript_${m}_r1.txt"); f2=$(grep -m1 "^FNV " "transcript_${m}_r2.txt"); f3=$(grep -m1 "^FNV " "transcript_${m}_r3.txt")
  chk "fnv-$m" "$f1" "$f2"; chk "fnv-$m-r3" "$f1" "$f3"
done
# ---- stderr must be 0 bytes on all 9 runs ----
se=0
for m in TREAT CONTROL NOPHASE; do for r in 1 2 3; do
  if [ -s "stderr_${m}_r${r}.txt" ]; then se=1; echo "FAIL stderr $m r$r nonempty"; fi
done; done
if [ "$se" = 0 ]; then echo "PASS stderr: 0 bytes on all 9 runs"; else fail=1; fi
# ---- oracle lines, rep 1 of each binary (reps byte-identical) ----
t() { grep -m1 "^$2" "transcript_$1_r1.txt"; }
chk "TREAT REBIND_OK" "REBIND_OK 12/12" "$(t TREAT REBIND_OK)"
chk "TREAT REBIND_PROP_CITE" "REBIND_PROP_CITE 12/12" "$(t TREAT REBIND_PROP_CITE)"
chk "TREAT SURVIVE_OK" "SURVIVE_OK 6/6" "$(t TREAT SURVIVE_OK)"
chk "TREAT SURVIVE_ANSFACT" "SURVIVE_ANSFACT 6/6" "$(t TREAT SURVIVE_ANSFACT)"
chk "TREAT RETAIN_OK" "RETAIN_OK 6/6" "$(t TREAT RETAIN_OK)"
chk "TREAT INT2_OK" "INT2_OK 1/1" "$(t TREAT INT2_OK)"
chk "TREAT STORE3_OK" "STORE3_OK 6/6" "$(t TREAT STORE3_OK)"
chk "TREAT PRESSURE_OK" "PRESSURE_OK 96/96" "$(t TREAT PRESSURE_OK)"
chk "TREAT CAPGUARD" "CAP_GUARD_OK" "$(t TREAT CAP_GUARD_OK)"
chk "TREAT AUDIT" "AUDIT_PASS" "$(t TREAT AUDIT_PASS)"
chk "CONTROL REBIND_OK" "REBIND_OK 12/12" "$(t CONTROL REBIND_OK)"
chk "CONTROL REBIND_PROP_CITE" "REBIND_PROP_CITE 0/12" "$(t CONTROL REBIND_PROP_CITE)"
chk "CONTROL SURVIVE_OK" "SURVIVE_OK 6/6" "$(t CONTROL SURVIVE_OK)"
chk "CONTROL RETAIN_OK" "RETAIN_OK 6/6" "$(t CONTROL RETAIN_OK)"
chk "CONTROL INT2_OK" "INT2_OK 1/1" "$(t CONTROL INT2_OK)"
chk "CONTROL STORE3_OK" "STORE3_OK 6/6" "$(t CONTROL STORE3_OK)"
chk "CONTROL PRESSURE_OK" "PRESSURE_OK 96/96" "$(t CONTROL PRESSURE_OK)"
chk "CONTROL AUDIT" "AUDIT_PASS" "$(t CONTROL AUDIT_PASS)"
chk "NOPHASE NOPHASE_OK" "NOPHASE_OK 12/12" "$(t NOPHASE NOPHASE_OK)"
chk "NOPHASE NOPHASE_NOA" "NOPHASE_NOA 1/1" "$(t NOPHASE NOPHASE_NOA)"
chk "NOPHASE STORE3_OK" "STORE3_OK 6/6" "$(t NOPHASE STORE3_OK)"
chk "NOPHASE PRESSURE_OK" "PRESSURE_OK 96/96" "$(t NOPHASE PRESSURE_OK)"
chk "NOPHASE INT2_OK" "INT2_OK 1/1" "$(t NOPHASE INT2_OK)"
chk "NOPHASE AUDIT" "AUDIT_PASS" "$(t NOPHASE AUDIT_PASS)"
# CONTROL must contain zero PROPOSAL occurrences
chk "CONTROL zero PROPOSAL" "0" "$(grep -c "PROPOSAL" transcript_CONTROL_r1.txt)"
# ---- CP-R0 ordering on TREAT rep 1 ----
np=$(grep -o "PROPOSAL s=" transcript_TREAT_r1.txt | wc -l)
nm=$(grep -c "^MACHINERY " transcript_TREAT_r1.txt)
ns=$(grep -c "MACHINERY_SKIPPED" transcript_TREAT_r1.txt)
chk "TREAT PROPOSAL count" "24" "$np"
chk "TREAT MACHINERY count" "24" "$nm"
chk "TREAT MACHINERY_SKIPPED" "0" "$ns"
ord_ok=1
for s in 97001 97002 97003 97004 97005 97006; do
  pl=$(grep -n "PROPOSAL s=$s r=863 " transcript_TREAT_r1.txt | cut -d: -f1)
  ml=$(grep -n "^MACHINERY s=$s r=863 " transcript_TREAT_r1.txt | cut -d: -f1)
  pn=$(grep -o "PROPOSAL s=$s r=863 mech=1 node=[0-9]*" transcript_TREAT_r1.txt | grep -o "[0-9]*$")
  mn=$(grep "^MACHINERY s=$s r=863 " transcript_TREAT_r1.txt | grep -o "prop=[0-9]*" | grep -o "[0-9]*$")
  if [ -z "$pl" ] || [ -z "$ml" ] || [ "$pl" -ge "$ml" ] || [ "$pn" != "$mn" ]; then ord_ok=0; echo "ORDER-FAIL tail s=$s pl=$pl ml=$ml pn=$pn mn=$mn"; fi
done
for s in 97101 97102 97103 97104 97105 97106; do
  pl=$(grep -n "PROPOSAL s=$s r=866 " transcript_TREAT_r1.txt | cut -d: -f1)
  ml=$(grep -n "^MACHINERY s=$s r=866 " transcript_TREAT_r1.txt | cut -d: -f1)
  pn=$(grep -o "PROPOSAL s=$s r=866 mech=1 node=[0-9]*" transcript_TREAT_r1.txt | grep -o "[0-9]*$")
  mn=$(grep "^MACHINERY s=$s r=866 " transcript_TREAT_r1.txt | grep -o "prop=[0-9]*" | grep -o "[0-9]*$")
  if [ -z "$pl" ] || [ -z "$ml" ] || [ "$pl" -ge "$ml" ] || [ "$pn" != "$mn" ]; then ord_ok=0; echo "ORDER-FAIL head s=$s pl=$pl ml=$ml pn=$pn mn=$mn"; fi
done
if [ "$ord_ok" = 1 ]; then echo "PASS TREAT rebind ordering 12/12 with matching prop ids"; else echo "FAIL TREAT rebind ordering"; fail=1; fi
# ---- answer spot checks (content, not just oracle lines) ----
a1=$(grep -m1 "^MACHINERY s=97001 r=863 " transcript_TREAT_r1.txt | grep -o "ans=[0-9-]*")
chk "TREAT tail answer s=97001" "ans=96201" "$a1"
a2=$(grep -m1 "^MACHINERY s=97101 r=866 " transcript_TREAT_r1.txt | grep -o "ans=[0-9-]*")
chk "TREAT head answer s=97101" "ans=96101" "$a2"
a3=$(grep -m1 "^MACHINERY s=97001 r=863 " transcript_NOPHASE_r1.txt | grep -o "ans=[0-9-]*")
chk "NOPHASE tail answer s=97001" "ans=1" "$a3"
# ---- K3 regression: lo_driver 3x with stdin TREAT ----
for r in 1 2 3; do
  printf 'TREAT' | PATH="$HOME/safebin" bash -c "exec -c ../../wave-20261001-2321pdt/CONTLEARN/lo_driver" > /tmp/lo_r$r.txt 2>/tmp/lo_e$r.txt
  echo "lo_driver r$r rc=$?"
done
l1=$(sha256sum /tmp/lo_r1.txt | cut -d' ' -f1); l2=$(sha256sum /tmp/lo_r2.txt | cut -d' ' -f1); l3=$(sha256sum /tmp/lo_r3.txt | cut -d' ' -f1)
chk "K3 lo_driver identical" "$l1" "$l2"; chk "K3 lo_driver identical r3" "$l1" "$l3"
chk "K3 lo_driver hash" "1ff527fa97b36da25fd8163299773680e53ae47fba521fc2227b0bf7c39394d9" "$l1"
le=0; for r in 1 2 3; do if [ -s /tmp/lo_e$r.txt ]; then le=1; fi; done
if [ "$le" = 0 ]; then echo "PASS K3 stderr empty"; else echo "FAIL K3 stderr"; fail=1; fi
# ---- K1a: 9 spawns recorded; K1b: 3 builds, 0 during runs ----
chk "K1a spawns" "total_spawns=9 want=9" "$(tail -1 harness_clh2.log)"
chk "K1b builds" "3" "$(wc -l < znc_invocations_clh2.log)"
# ---- K2a: frozen hashes still hold after runs ----
h=$(sha256sum /home/hatch/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag | cut -d' ' -f1)
chk "K2a tnn2.zag" "a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd" "$h"
if [ "$fail" = 0 ]; then echo "ALL SEALED CHECKS PASS"; else echo "SEALED CHECKS FAILED"; fi
exit $fail
