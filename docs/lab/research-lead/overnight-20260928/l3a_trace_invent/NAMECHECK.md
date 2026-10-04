# Step 0 name-check (L3A-TRACE builder, 2026-09-30)

Rules from LOOP_STATE.md that apply to this task and how I will honor them:

1. Standing owner rules, PURE ZAG ONLY. No Python anywhere: not glue, not analysis,
not verifiers, not harnesses, not fixture provisioning. I will honor this by writing
only Zag source compiled with the pinned znc binary, doing all analysis with shell
tools (grep, diff, sha256sum), and never authoring or executing Python at any step.
2. Standing rule: shell-only byte checks (2026-09-30). I will check loop documents for
em/en dash bytes only with docs/lab/research-lead/overnight-20260928/worker_snippets/
check_no_dash.sh, never with python3. Disclosure does not cure use.
3. Standing owner rule: fork testing. Every fork gets tested; for this single-machine
battery that means 3/3 byte-identical deterministic reruns, verified with sha256sum.
4. Loop documentation style: no em dashes, enforced by the shell-only snippet above.
5. Task-level constraints from the brief: commits local, owned pathspec only
(docs/lab/research-lead/overnight-20260928/l3a_trace_invent/), never touch the
contaminated research paper, never remove a live .git/index.lock (wait and retry),
prereg committed alone and strictly before implementation (merge-base verified).

Name-check complete. Proceeding to prereg freeze.
