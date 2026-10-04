# NAMECHECK.md - lane INDEX, wave-20261002-1121pdt

Lane: index. Branch: lane-index-20261002-1121pdt (from tnn-native-lab).
Worktree: ~/workspace/tnn-rsi-work/wave-20261002-1121pdt/index/

## Step 0: toolchain guard (recorded first, per governance)

Setup output (literal):
```
safebin: /home/hatch/safebin
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
```

Post-export PATH="$HOME/safebin" evidence:
- `which python3` -> rc=1, resolves to NOTHING (PASS)
- `which znc` -> /home/hatch/safebin/znc (PASS)

Guard: ACTIVE. All Zag invocations in this lane use ~/safebin/znc.
Any python3/python invocation by this lane is automatic PROCESS-FAIL
with measurements quarantined; only clean safebin reproduction promotes.

## Standing rules acknowledged (wave NAMECHECK.md)

1. PURE ZAG ONLY. 2. Guard as above. 3. Fork enumeration for the
frozen battery. 4. Image judging rules. 5. Prereg commit-order
self-check before any verdict. 6. Debate group transcript.
7. PROPOSE/TEST/RED-TEAM/VERDICT per candidate; free lunches first.
8. No em-dashes in loop docs; verify with check_no_dash.sh.
9. Frozen lanes honored; kill bars frozen before implementation,
never moved. 10. Red lines: no spend, no publish, no outsiders,
no bookings, no irreversible commitments, never git push,
never Google Drive.

Technical: pinned znc defects (no _zag_print for dynamic content;
no as *i32 + q[0..n]; as []f64 no .len rescale; WAV 2-byte getter;
hoist conditions, nesting <= 3; capacity plan < 1024 nodes;
ma_base.zag not self-contained, supply minimal ev_query).
No writes into scaling_5000_fixed or scaling_10000 live-run dirs.
Commits pathspec-limited to lane dirs only.

Task (queue item 12): (a) t2_revise_graph coverage, frozen prereg
with kill bars committed BEFORE implementation; (b) soak storms
(fixed seeds, byte-identical reruns) on the eviction hook to
trigger the index-cycle panic and the eviction latency cliff;
measure and characterize; (c) pure-Zag index validator checking
index invariants after every storm (no cycles, bounds respected);
any invariant violation is a KILL with evidence.
