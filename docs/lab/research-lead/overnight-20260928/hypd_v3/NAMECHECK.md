# D-v3 Builder: Step 0 Name-Check

I have read the standing-rules block at the top of `LOOP_STATE.md`
(the four sections: Standing owner rules 2026-09-23, fork testing,
pure-Zag red line scope, shell-only byte checks 2026-09-30).

Rules that apply to my work and how I will honor them:

1. **PURE ZAG ONLY** (owner red line, 2026-09-23; scope ruling
   2026-09-23): no Python anywhere in my work — not in the
   implementation, not in glue, not in analysis, not in verifiers,
   not in harnesses, not in byte checks. I will write only Zag and
   shell. All analysis of run output will be done with shell tools
   (grep, awk, sort, sha256sum) or not at all.

2. **Shell-only byte checks** (2026-09-30): the no-dash documentation
   check will use only
   `docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh`.
   I will not reach for python3 for any byte check.

3. **Shared-branch discipline**: my owned path is
   `docs/lab/research-lead/overnight-20260928/hypd_v3/` only. Every
   `git add` and `git commit` will use explicit pathspecs limited to
   that path. I will run `git status --porcelain` before every commit
   and confirm no other worker's files are staged. I will never touch
   `docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md`
   (verified with an empty diff at the end). If I encounter a live
   `.git/index.lock`, I will wait and retry; I will never remove it.

4. **Fork testing** is a wave-level rule owned by the coordinator, not
   by this build task; I will not interfere with it.

No other standing rule in the block assigns me work. Proceeding.
