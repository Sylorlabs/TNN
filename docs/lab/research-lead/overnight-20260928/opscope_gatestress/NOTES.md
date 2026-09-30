# OpScope Gate-Stress Attack - NOTES.md

Worker: OpScope Gate-Stress Attacker (subagent, depth 1).
Spawned: 2026-09-30 PDT by parent coordinator.
Task: stress the OpScope K=2 DELETION gate with sealed NEG variants where a
positional confound clears the count bars; test whether the K=2-configured
discovery gate discriminates correctly.
Owned path: docs/lab/research-lead/overnight-20260928/opscope_gatestress/
Pinned znc: /home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
Committed target: commit c60bfbe7a (OPSCOPE-R1R4-PASS). Prereg K=2: 51c54e262.

## Step 0: standing-rules name-check (written 2026-09-30, before any Step 1 work)

Checked rules, by name:

(1) PURE ZAG ONLY. Pure Zag and shell only. Variant generation, analysis,
    byte checks all in Zag or shell. Never author Python. Authoring Python is
    a violation; disclosure does not cure it. Byte checks via shell only.
(2) IMAGE JUDGE. Wave-level rule about sensory judgment. Not applicable to
    this sealed gate-stress attack (no images rendered or judged). Noted, not
    binding here.
(3) EVERY FORK TESTED. Wave-level rule about fork coverage. Not applicable
    (this attack does not fork the learner; it attacks the committed source).
    Noted, not binding here.
(4) PURE-ZAG SCOPE (fixture/variant provisioning). Fixture/variant
    provisioning for this attack is loop work and must be Zag-only. All
    variant world generation will be in Zag. No Python fixtures.
(5) SHELL-ONLY BYTE CHECKS. Byte checks via the shell-only checker
    docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh,
    never python3.

Binding on this worker: (1), (4), (5). (2) and (3) acknowledged as wave-level,
not applicable to this sealed attack.

Additional standing constraints honored: no em dashes in loop docs; prereg
before implementation (verify git merge-base --is-ancestor); never weaken a
frozen bar (K=2 stays; prior K=3 FAIL untouched); commits local with explicit
pathspecs only; inspect git status before every commit; never remove a live
.git/index.lock (wait and retry); never touch
docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md;
attacker discipline: copies only, never modify sealed/frozen files,
rebuild-from-source OK; verdict vocabulary GATE-STRESS-[PASS/FAIL];
AGENTS.md toolchain lesson (2026-09-30): never use `as *i32` + q[0..n] slice
construction inside functions (pinned znc miscompiles); use u8-backed cells
with little-endian pack/unpack helpers. The committed sources already follow
this idiom; my new Zag code will too.

Name-check complete. Step 1 (pilot) may proceed.
