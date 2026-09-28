#!/bin/bash
# AU1 trial runner — trainer-auth binding (Wave-5, investigation 11).
# Orchestrates the full session twice; asserts preregistered expectations;
# requires byte-identical logs across both runs (J-A6).
set -u
HERE="$HOME/workspace/tnn-lab/wave5/trainer-auth"
BIN="/tmp/tnn-auth-bin/auth_trial"
SOCKDIR="/tmp/tnn-auth-test"
ZAG="$HERE/auth_trial.zag"
FAIL=0

as_user() { # uid, then command...
  local uid="$1"; shift
  setpriv --reuid "$uid" --regid "$uid" --clear-groups "$@"
}

wait_file() { # path, timeout_s
  local i=0
  while [ ! -e "$1" ] && [ "$i" -lt "$2" ]; do sleep 0.2; i=$((i+1)); done
  [ -e "$1" ]
}

run_once() {
  local run="$1"
  local logdir="$HERE/$run"
  mkdir -p "$logdir"; rm -f "$logdir"/*.log
  rm -rf "$SOCKDIR"; mkdir -p "$SOCKDIR"
  chown tnnsup:tnnsup "$SOCKDIR"; chmod 755 "$SOCKDIR"
  # AU2: the supervisor starts as root and drops privileges itself after
  # fork (parent -> 1000, TNN child -> 1003). The child cannot create
  # files in the sockdir, so its log is precreated here owned by it.
  : > "$SOCKDIR/child.log"
  chown tnnlearner:tnnlearner "$SOCKDIR/child.log"; chmod 644 "$SOCKDIR/child.log"

  # F-C theft target: a uid-1001 process guaranteed alive for the whole
  # session. Spawned BEFORE the supervisor so its pid is stable; recorded
  # in pid_9 for the child's fixed-target fd-theft cell (deterministic
  # attempt count, no /proc scan race).
  as_user 1001 /bin/sleep 120 &
  local decoy=$!
  echo "$decoy" > "$SOCKDIR/pid_9"
  chmod 644 "$SOCKDIR/pid_9" # the uid-1003 TNN child must be able to read it

  # AU2: supervisor starts privileged; it drops to tnnsup(1000) itself.
  "$BIN" sup > "$logdir/sup.log" 2>&1 &
  local suppid=$!
  wait_file "$SOCKDIR/ready" 25 || { echo "RUN $run: supervisor never ready"; kill "$suppid" "$decoy" 2>/dev/null; return 1; }

  as_user 1001 "$BIN" console legit1 > "$logdir/c_legit1.log" 2>&1
  wait_file "$SOCKDIR/redteam_done" 25 || { echo "RUN $run: redteam never finished"; kill "$suppid" "$decoy" 2>/dev/null; return 1; }
  as_user 1001 "$BIN" console master  > "$logdir/c_master.log" 2>&1
  as_user 1001 "$BIN" console rejoin  > "$logdir/c_rejoin.log" 2>&1
  as_user 1002 "$BIN" console overseer > "$logdir/c_overseer.log" 2>&1

  wait "$suppid"; local se=$?
  kill "$decoy" 2>/dev/null; wait "$decoy" 2>/dev/null
  cp "$SOCKDIR/child.log" "$logdir/child.log" 2>/dev/null
  echo "RUN $run: supervisor exit=$se"
  return 0
}

expect_grep() { # file, pattern, desc
  if grep -qE "$2" "$1"; then echo "  ok: $3";
  else echo "  FAIL: $3 (missing /$2/ in $1)"; FAIL=1; fi
}

check_run() {
  local logdir="$HERE/$1" run="$1"
  echo "== checks for $run =="
  # P1 legit trainer flow
  expect_grep "$logdir/c_legit1.log" "^C,legit1,register,0,-1$" "trainer register ok"
  expect_grep "$logdir/c_legit1.log" "^C,legit1,revoke_self,120,-1$" "trainer cannot revoke (120)"
  expect_grep "$logdir/c_legit1.log" "^C,legit1,install,0,0$" "force-install ok slot 0"
  expect_grep "$logdir/c_legit1.log" "^C,legit1,pin,0,-1$" "force-pin ok"
  # P2 learner + red team
  expect_grep "$logdir/sup.log" "^S,EUID,1000$" "supervisor dropped to uid 1000"
  expect_grep "$logdir/child.log" "^T,EUID,1003$" "TNN child dropped to uid 1003"
  expect_grep "$logdir/child.log" "^T,l_add,0,1$" "learner add ok slot 1"
  expect_grep "$logdir/child.log" "^T,fa_register,130,-1$" "F-A rogue register refused 130"
  expect_grep "$logdir/child.log" "^T,fa_pin_unregistered,132,-1$" "F-A pin on unregistered conn refused 132"
  expect_grep "$logdir/child.log" "^T,fb_force_on_ctl,133,-1$" "F-B force-shaped ctl traffic refused 133"
  expect_grep "$logdir/child.log" "^T,fc_fd_theft,32,0$" "F-C fd theft: 32 attempts, 0 successes"
  expect_grep "$logdir/child.log" "^T,fd_replay_noreg,132,-1$" "F-D replay w/o registration refused 132"
  expect_grep "$logdir/child.log" "^T,fe_kill_pinned,122,-1$" "F-E learner kill of pinned refused 122"
  expect_grep "$logdir/child.log" "^T,FORGE_FAILURES_EXPECTED,6,6$" "all 6 forgery attempts failed"
  expect_grep "$logdir/child.log" "^T,END,0$" "child clean exit"
  # P3 revocation
  expect_grep "$logdir/c_master.log" "^C,master,register,0,-1$" "master register ok"
  expect_grep "$logdir/c_master.log" "^C,master,revoke7,0,-1$" "revoke trainer 7 ok"
  # P4 revoked identity (F-F)
  expect_grep "$logdir/c_rejoin.log" "^C,rejoin,register,131,-1$" "F-F revoked re-register refused 131"
  expect_grep "$logdir/c_rejoin.log" "^C,rejoin,pin,132,-1$" "revoked conn pin refused 132"
  # P5 overseer
  expect_grep "$logdir/c_overseer.log" "^C,overseer,register,0,-1$" "overseer register ok"
  expect_grep "$logdir/c_overseer.log" "^C,overseer,pin_claim_mismatch,134,-1$" "claim mismatch refused 134"
  expect_grep "$logdir/c_overseer.log" "^C,overseer,install,0,2$" "overseer install ok slot 2"
  expect_grep "$logdir/c_overseer.log" "^C,overseer,pin,0,-1$" "overseer pin ok (Micah's law)"
  expect_grep "$logdir/c_overseer.log" "^C,overseer,unpin_revoked_pinner,0,-1$" "overseer unpins revoked pinner's pin (R4)"
  # supervisor final report
  expect_grep "$logdir/sup.log" "^AU_REFUSED,9$" "9 refused ops audited"
  expect_grep "$logdir/sup.log" "^AU_NOTES,1$" "1 red-team note"
  expect_grep "$logdir/sup.log" "^AU_MUTOK,1$" "no mutation on refusal (J-A2)"
  expect_grep "$logdir/sup.log" "^AU_J1,1$" "J-A1 ok-force entries role>=TRAINER + registered"
  expect_grep "$logdir/sup.log" "^AU_REPLAY,1$" "ledger replay reconstructs state (J-A4)"
  expect_grep "$logdir/sup.log" "^AU_PIN_PERSIST,1$" "pin persisted across revocation (R3)"
}

# static checks (J-A5): no RNG, no credential-like identifiers in the trial source
echo "== static checks =="
if grep -nE "rand|srand|random" "$ZAG"; then echo "FAIL: RNG-like token in source"; FAIL=1;
else echo "  ok: no rand/srand/random in trial source"; fi
if grep -nE "\b(token|secret|password|api_key|private_key)\b" "$ZAG" | grep -viE "bearer secret|no secret"; then echo "FAIL: credential-like identifier in source"; FAIL=1;
else echo "  ok: no credential-like identifiers in source"; fi

run_once run1 || FAIL=1
run_once run2 || FAIL=1

check_run run1
check_run run2

echo "== determinism (J-A6): diff run1 vs run2 =="
for f in sup.log child.log c_legit1.log c_master.log c_rejoin.log c_overseer.log; do
  if cmp -s "$HERE/run1/$f" "$HERE/run2/$f"; then echo "  ok: $f identical";
  else echo "  FAIL: $f differs"; FAIL=1; fi
done

if [ "$FAIL" = 0 ]; then echo "AU2: ALL CHECKS PASS"; else echo "AU2: FAILURES PRESENT"; fi
exit "$FAIL"
