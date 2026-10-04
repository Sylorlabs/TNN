# NAMECHECK_S7_EXEC (HPIREV2 step-7 sealed OOD execution, wave-20261001-2021pdt)

Role: executor. This worker is the EXECUTOR of the frozen step-7 battery
only. The worlds were designed by the independent adversary (lane
HPIREV2-S7-ADV, commit dea2694d1) and certified V1-V4 by the independent
certifier (lane HPIREV2-S7-RT, commit 53e92c8ce, CERT_S7_V1V4.md). This
worker designed no world and certified nothing; it read the prereg, the
manifest, and the certification to execute them.

## Step 0: Worker toolchain guard (per Micah's governance ruling 2026-09-30)

- Safebin activated: ran
  docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
  from the working copy /home/hatch/workspace/tnn-rsi. Output: 36 tools
  linked, znc OK (pinned znc_linux_x86_64_abed8aa1), python3 and python
  absent from safebin PATH, SAFEBIN-READY.
- Verification: `export PATH="$HOME/safebin"` then `which python3` printed
  nothing (exit code 1). No python3 resolves in this worker's PATH.
- PURE ZAG ONLY for all research logic: shell invokes only the pinned znc
  compiler, runs compiled binaries, git read-only ops, sha256sum, and file
  moves/copies. No python, perl, ruby, node, gcc, or other interpreter or
  compiler was invoked at any stage. Any forbidden executable invocation
  would be automatic PROCESS-FAIL; none occurred.
- Working copy: /home/hatch/workspace/tnn-rsi, branch tnn-native-lab.
  NEVER push. No git reset --hard, no rebase. No git commit (coordinator
  commits). Writes confined to
  docs/lab/rsi/runs/wave-20261001-2021pdt/HPIREV2/ and only these new files:
  NAMECHECK_S7_EXEC.md, SEALED_S7_EXEC.md, s7_exec.zag, s7_exec_bin,
  s7_world_*.txt transcripts, s7_run_times.txt, s7_stage_check.txt.
  The sealed world files, the manifest SEALED_S7_WORLDS.md, the frozen
  prereg, and the frozen mechanism source were never modified.
- Determinism: 3/3 byte-identical reruns required per world (K-OOD-W4).
- Documentation rule observed: no em-dashes and no en-dashes anywhere in
  this file or any file written by this worker (byte-checked at the end).

## Frozen references used

- Frozen step-7 prereg: PREREG_PI_REV2_STEP7.md, committed alone at
  201ed5a05 (commit-order self-check: git log shows exactly that commit).
- Frozen mechanism source:
  docs/lab/rsi/runs/wave-20260929-2321pdt/pi_rev2/proc_revise2.zag,
  committed at 847a8f10f. Working-tree sha256 verified against the
  committed blob before building:
  dd3cb02dbd883243e350a89e328e570c35e2dc7a71f49f4e3aa51f0603a99a12
  (match, see SEALED_S7_EXEC.md section 1).
- Certification: CERT_S7_V1V4.md (53e92c8ce): all 4 families CERTIFY,
  no world voided. Two errata applied: (1) manifest C_FW.txt sha256 typo;
  load-time verification used the actual file hash
  8d6f3362dc476447f1e07402e97958a654fe76558114adcad4ef7af40bd3fbf8
  recorded in the cert; the manifest file itself was not edited.
  (2) Family C note typo "uuuuuuuu" should read "vvvvvvvv"; the V2
  misprediction conclusion is unaffected.
- Certified predictions (bounding matrix): Family A full PASS expected;
  Family B expected honest W1 fail on RW only (single-conflict bound);
  Family C PASS; Family D PASS.

## Executor method (disclosure)

The frozen binary hardcodes its fixtures in main and accepts only one
adversary byte, so it cannot be pointed at sealed world files. The
executor therefore built s7_exec.zag as: lines 1-606 of proc_revise2.zag
copied byte-verbatim (all machinery: benum, dsearch, loadseq, extract_seq,
predict, observe, diagnose, build_test, specialize; verified by diff),
plus a new main that stages one family's sealed pairs as literals,
selected by argv[1] (a/b/c/d), and runs the prereg's per-world order:
V0/V1/V2/V3 prechecks, train v1w, present FW, frozen revision
(diagnose, build_test, alt dsearch on FW alone, specialize), score
against EW (W1, W2), present RW after revision ACTIVE (W3). The code
path is identical for all four families; only the staged literals
differ. No world-specific branching, no new semantic cases, no modes,
no bridges. The frozen mechanism source file is byte-identical before
and after (K-ARCH1).

No em-dashes or en-dashes appear in this file.
