# H-EXP2 v2 STEP 6 alternative explanation attack: NAMECHECK

## Step 0: toolchain guard
- setup_safebin.sh not present at ~/docs/lab/research-lead/overnight-20260928/safebin_setup/ (dir does not exist).
- Pre-provisioned safebin at ~/safebin used instead: 41 entries including pinned znc.
- PATH exported to $HOME/safebin only. `which python3` returns nothing. `which python` returns nothing.
- VERDICT: guard PASS. Pure Zag only from here.
