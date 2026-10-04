# NAMECHECK wave-20261002-0521pdt ARENA

## Step 0 (mandatory first, worker toolchain guard)
- Ran docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh: exit 0.
- Exported PATH="$HOME/safebin" (36 tools: coreutils, git, pinned znc).
- `which python3` returns nothing (not in PATH).
- `which python` returns nothing (not in PATH).
- Pinned znc verified: /home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1
- PURE ZAG ONLY for all computational research operations this wave.
- Miscompile workaround active: no `as *i32` + q[0..n] slice construction; u8-cell loop idiom with ig/is helpers.
- Forbidden executable invocation = automatic PROCESS-FAIL for current scientific wave.

## Step 3: Log (wave execution)

- 2026-10-02 ~05:26 PDT: Step 0 toolchain guard recorded. Safebin
  active, python3 and python absent. Lane directory created.
- Surveyed 0221pdt ARENA state: C9FIX generator PARTIAL (G4 seed
  order), PREREG_CAUSAL frozen but never evaluated,
  PREREG_ABSTENTION frozen but never run. causal_contestant.zag
  implements the two-stage protocol (do/do_out stats W
  15000..15028, discrim handler, zero chain literals in logic).
- Found D5 (deeper than the reported G4 issue): the turns.jsonl
  replay path rebuilds every C9 question as discrim|<true>|<alt>
  unconditionally, ignoring the seeded coin flip; battery.json
  honors it (actual draws under frozen seed: 1,1,0, not the
  reported 1,1,1). The 0221pdt "seed luck" diagnosis is
  falsified by artifact evidence.
- bc049ef67: froze PREREG_C9D5FIX.md alone (E1-E3: dflip array,
  flip recording, flip-ordered replay; seed unchanged).
- ee0e78ae7: C9D5FIX implementation + GEN-PASS eval. fixrun2/
  validated G1-G8: 3/3 byte-identical; true_listed_first=2/3;
  battery/turns C9 questions string-identical; old exploit 0/3;
  check tool recovers 3/3.
- C9 causal sealed eval (frozen PREREG_CAUSAL fdaa5c0a4):
  discovered fixrun1 is unscorable (frozen scorer DIVERGENCE: q
  mismatch, independent D5 confirmation) and the frozen scorer
  panics on 291-turn worlds (256-entry turn buffers). Built
  arena_512 (frozen logic, buffers 256->512, diff-verified,
  cross-validated byte-identical results.json on 131-turn
  world). Ran on fixrun2 with disclosed deviation.
- CAUSAL-PASS (K1-K7): v6 baseline 54/68=0.794 on fixrun2;
  causal candidate 57/68=0.838 (3/3 runs), C9 3/3, zero
  regressions, 3/3 byte-identical stripped streams; ablation
  per-capability identical to v6 (C9 0/3); order-swap invariant
  (replies unchanged, true chain x3). Files committed (swept
  into sibling commit d22862d07; content intact).
- e9c03e2b7: bare-prompt abstention test ABSTAIN-FAIL (A1/A2
  fail, A3 pass). DEFRECALL (binary byte-identical to sealed)
  enumerates the roster on bare whattime and bare invent;
  abstention boundary is structural (bare vs parameterized),
  not semantic. C15 scope bounded to roster-request prompts.
- ca4ed3320: froze PREREG_TRANSFER_C8C12.md alone (T1-T5).
- 620f99f91: C8/C12 surface-transfer TRANSFER-PASS. INQ 58/68
  (C8 4/4), REMAP 60/68 (C12 6/6) on fixrun2, byte-identical
  rebuilds, 3/3 determinism, profiles identical to frozen
  world. C9GEN instrument note written (candidate for
  governance; no adoption asserted).
- REDTEAM_SELF.md: self red team of all results (gaming,
  harness coupling, knowledge-vs-architecture).
- Toolchain: safebin PATH throughout; `which python3` /
  `which python` return nothing at lane start and end. New
  AGENTS.md second-miscompile lesson noted; mitigated by
  stdout byte verification (3/3 byte-identical streams
  everywhere). No forbidden executable invoked: no
  PROCESS-FAIL.
- Git: commits local only, pathspec-only, never pushed. No
  frozen kill bar weakened. One transparent protocol
  deviation disclosed (C9 substrate/scorer).
