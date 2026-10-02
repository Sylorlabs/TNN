# NAMECHECK.md - lane ARENA, wave-20261002-1121pdt

Wave: wave-20261002-1121pdt. Branch: lane-arena-20261002-1121pdt.
Worktree: ~/workspace/tnn-rsi-work/wave-20261002-1121pdt/arena/.
Lane worker: ARENA.

## Step 0: toolchain guard (recorded first, before any other work)

Ran: `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
Output (literal):
```
safebin: /home/hatch/safebin
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
```
Then with `export PATH="$HOME/safebin"`:
- `which python3` printed NOTHING (no output at all; does not resolve).
- `which znc` printed `/home/hatch/safebin/znc`.

Guard result: PASS. All subsequent work runs under this safebin PATH.
Any forbidden-interpreter invocation = automatic PROCESS-FAIL of this
lane's wave, measurements quarantined.

## Provenance (what this lane inherits, all read-only until preregs freeze)

From prior lane branch lane-arena-20261002-0821pdt, path
docs/lab/rsi/runs/wave-20261002-0521pdt/ARENA/:
- v6_base.zag (refreeze devint1_contestant_v6.zag; 15-cap baseline,
  54/68 = 0.794 on fixrun2; zeros on C8/C9/C12/C15)
- transfer/inq_contestant.zag (INQ: active inquiry; C8 4/4 on fixrun2;
  TRANSFER-PASS T1)
- transfer/remap_contestant.zag (REMAP: remap tables; C12 6/6 on fixrun2;
  TRANSFER-PASS T2)
- causal_contestant.zag (CAUSAL: two-stage interventional protocol;
  C9 3/3 on fixrun2; CAUSAL-PASS K1-K7)
- abstention/defrecall_contestant.zag (DEFRECALL; ABSTAIN-FAIL on
  non-roster bare prompts; scope bounded to roster-request prompts)
- world_gen_c9d5fix.zag (D5-fixed generator; GEN-PASS)
- arena_512.zag (scorer; cross-validated byte-identical vs frozen scorer
  on the 131-turn world; differs ONLY in 256->512 turn-index sizes)
- fixrun2/ world (68 items, 291 turns, seed 71503461337030)
- run_sealed.sh (turn replay driver; bash process sequencing only)

Nothing is adopted from the above except through this wave's own frozen
preregs and fresh executions. Sources for builds are extracted via
`git show` from the recorded lineage commits, never from working files.

## Queue (this wave's lane task, item 7)

(a) Integrated contestant assembly: v6 + INQ + REMAP + CAUSAL in one
    binary, frozen prereg, byte-identical reruns, per-capability scores.
(b) Adversarial C8/C12 families: post-freeze variants designed to break
    the current INQ/REMAP approach.
(c) Multi-seed C9: causal mechanism across multiple seeds, byte-identical
    per seed, variance reported honestly.
(d) C15 abstention: bounded-scope measurement of the abstention
    boundary (no new semantic cases; genuine intent discrimination stays
    a new-frontier proposal).

## Standing rules acknowledged

PURE ZAG ONLY. No spend/publish/contact/purchase/commitment/push/Drive.
Commits pathspec-limited to this lane dir +
docs/lab/rsi/runs/wave-20261002-1121pdt/arena/. Never to tnn-native-lab.
No rebase, no reset. No writes into scaling_5000_fixed or scaling_10000.
No em-dashes in docs (verified with check_no_dash.sh). Prereg
commit-order self-check before any verdict. Red team every candidate.
FW1-FW9 is regression only. No LLM comparisons (no credential).
