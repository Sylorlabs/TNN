# NAMECHECK_ADVERSARY: lane TNN3H5, wave-20261001-2021pdt

Independent adversary for the H5 sealed evaluation. I am a different
worker from the TNN3H5 builder and the TNN3H5-IMPL worker, with no shared
working state with either. I work from the frozen prereg PREREG_H5.md
(committed alone at 57aac4b81) and the coordinator rulings Q1-Q4 only.

## Step 0: adversary toolchain guard (mandatory, recorded at startup)

1. Ran: `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
   from /home/hatch/workspace/tnn-rsi.
   Result: SAFEBIN-READY, /home/hatch/safebin, 36 tools, znc OK
   (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1),
   verify: python3 absent from safebin PATH (OK), python absent (OK).
2. `export PATH="$HOME/safebin"`; then `which python3` printed NOTHING
   (exit 1) and `which python` printed NOTHING (exit 1). Guard satisfied.
3. PURE ZAG ONLY for this lane: no Python for glue, analysis, verifiers,
   harnesses, or fixture provisioning. Shell invokes only the pinned znc,
   built binaries, git read-only ops (log/show/status/diff/hash-object),
   and file moves/copies. Any forbidden executable invocation is automatic
   PROCESS-FAIL and will be reported honestly.
4. Working copy: /home/hatch/workspace/tnn-rsi, branch tnn-native-lab.
   No push (never). No git reset --hard, no rebase. No commits by this
   worker; the coordinator commits. Writes only inside
   docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H5/ as new files:
   NAMECHECK_ADVERSARY.md, SEALED_WORLDS.md, SEALED_EVAL.md, and the
   sealed/ directory (world drivers). The builder has no read path to
   sealed/ per the coordinator Q4 ruling.
5. Documentation rule observed: no em-dashes in anything written in this lane.
6. Determinism standard: 3/3 byte-identical reruns per sealed world,
   compared by SHA-256 of full stdout (behavioral lines plus canonical
   full state dump).

Recorded: 2026-10-01 20:45 PDT, adversary worker session 95a8108a
(subagent lane TNN3H5-ADVERSARY, depth 2/2).

## Step 0b: frozen binary verification (before any sealed run)

- Expected SHA-256 (from the task and IMPLEMENTATION.md):
  344ac89fb338ddbf46bea6be4c526d99410ea643278ab91fb06d76b7e33c4eb7
- Measured with `sha256sum` on
  docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H5/tnn3_h5.bin:
  344ac89fb338ddbf46bea6be4c526d99410ea643278ab91fb06d76b7e33c4eb7
  MATCH. Proceeding; any mismatch would have been BLOCKED.

## Independence statement

Sealed worlds are designed post-freeze (after commit 57aac4b81,
2026-10-02 03:30:27 UTC) from the prereg section 4 family requirements
only. Key ranges 51xxx-54xxx are disjoint from the builder dev ranges
(7xxx/8xxx and the small dev keys), from FW1-FW9 (3xxxx), and from the
1421pdt battery (43xxx). I read the frozen implementation source to build
correct drivers (event interface, white-box layouts); world CONTENT
(keys, relations, values, event orderings, distractor placement) is my own
adversarial design, not derived from the builder dev worlds. Per the
coordinator tasking for this lane, the prereg 4.3 "no knowledge of the
implementation" clause is superseded by the Q4 adversary assignment as
communicated in my task; this is recorded transparently here.
