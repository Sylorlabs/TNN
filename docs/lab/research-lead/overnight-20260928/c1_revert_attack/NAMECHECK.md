# Step 0 name-check (C1 Law-Revert Attacker, 2026-09-30)

I read the standing-rules block at the top of LOOP_STATE.md. Four rules
govern this task. (1) PURE ZAG ONLY: I will write no Python anywhere in
this wave, not in generators, scorers, diagnostics, or /tmp scratch; all
analysis is Zag or shell. (2) Fork testing: a wave-level rule I honor by
staying on the single checked-out branch tnn-native-lab and running only
the pinned frozen contestant, never an untested fork. (3) Pure-Zag red
line scope: fixture provisioning is loop work, so world generation itself
is a frozen Zag binary fed by mechanically derived seeds, with the shell
only moving bytes. (4) Shell-only byte checks: dash checks run through
worker_snippets/check_no_dash.sh, never python3. This name-check is
written before any implementation begins.
