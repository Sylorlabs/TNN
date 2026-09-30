# Step 0 name-check

The standing-rules sections at the top of the repo-root LOOP_STATE.md apply
to this task as follows: (1) PURE ZAG ONLY is a literal red line; this
prereg is pure markdown, and all subsequent work (generator, runs, diag)
will be pure Zag binaries plus shell sequencing, zero Python. (2)
Shell-only byte checks: dash checks run via the shell-only check_no_dash.sh
snippet, never python3. (3) Frozen-bar discipline: this prereg is committed
alone before any implementation; the freeze will be committed alone before
world generation; seeds come from /dev/urandom after the freeze. (4)
Commits stay local with explicit pathspecs on the owned path
docs/lab/research-lead/overnight-20260928/c1_fe_family/ only; git status
inspected before every commit; never touch a live .git/index.lock. Fork
testing and the image-judge rule do not apply.
