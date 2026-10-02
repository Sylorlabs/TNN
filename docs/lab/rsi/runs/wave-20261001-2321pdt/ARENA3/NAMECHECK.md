# NAMECHECK: ARENA3 lane, wave-20261001-2321pdt

## Step 0 (toolchain guard, recorded first)

Date: 2026-10-01 23:37 PDT (wave wave-20261001-2321pdt)

Verification output (exact):

```
safebin: /home/hatch/safebin
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
--- safebin contents:
awk basename bash cat chmod cmp cp cut date diff dirname echo find git git-receive-pack git-upload-pack grep head ln ls mkdir mv od printf rm sed sh sha256sum sleep sort stat tail tee timeout touch tr uname uniq wc which xargs znc
--- which python3:
python3 NOT FOUND
--- which python:
python NOT FOUND
```

Worker PATH: `export PATH="$HOME/safebin"` is active for this lane.
Branch: tnn-native-lab. No python3 resolves: guard PASSES, work proceeds.
No forbidden interpreter invocation will occur; if one does, this wave is
automatically PROCESS-FAIL and will be disclosed in the final report.

## Lane log

- 2026-10-01 23:37 PDT: Step 0 recorded. Sibling lanes read: ARENA
  (inquiry, DONE, BUILD-PASS 0.853); ARENA2 directory empty, no prereg
  frozen, so per parent instruction this lane defaults to C12 transfer
  (assumption recorded in the prereg).
- Capability definitions taken from the sealed generator
  (competitive_arena/world_gen.zag) and the refreeze record
  (wave-20261001-1721pdt): C12 = 6 items, 3 x remap_prod and
  3 x remap_class, scored by exact reply match.
- Prereg PREREG_ARENA_TRANSFER.md committed alone at 829208f99.
- Implementation trx_contestant.zag (TRX: parse_remap with permutation
  validation; remap_prod and remap_class head handlers reusing the
  learned class-A/B templates; TRX_PROD_ON/TRX_CLASS_ON ablation flags)
  built on the INQ candidate source, committed at 9191e71de.
  Commit order verified: prereg 06:40:52 UTC strictly before
  implementation 06:43:17 UTC.
- Dev smoke test in /tmp (never sealed): all 9 cases pass (remapped
  prod answer, UNKNOWN on non-template input / invalid remap / no
  templates; yes/no class answers; zemprod/zemclass intact).
- Sealed evaluation: world_gen and arena rebuilt from committed sources,
  hashes match the refreeze record; turns.jsonl regenerated
  byte-identical to the sealed world; pre-run key hashed, never opened.
- 3/3 sealed runs: C12 6/6 = 1.000; total 64/68 = 0.941; zero regressions
  on the other 15 capabilities; byte-identical stripped reply streams and
  stderr traces.
- K6 ablations: prod-off 3/6, class-off 3/6 (61/68 = 0.897 each); both
  halves causal; no other capability disturbed.
- K5/K7/K8 audits: zero C12 literal strings in mechanism source; C7
  replies exactly UNKNOWN in all runs; +80/-0 lines, zero
  mode/bridge/router/admission/gate keywords.
- K9: L3 explicitly disclaimed (fails C0-A through C0-D).
- Verdict: BUILD-PASS. Lane end: `which python3` and `which python`
  print nothing; zero interpreter invocations; no PROCESS-FAIL.
- Nothing pushed; commits local only on tnn-native-lab. Sibling lane
  dirs (ARENA, ARENA2) untouched.
