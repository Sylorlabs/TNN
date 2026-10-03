# Step 0 Name-Check: C1 Smallest-Consistent-K Revision Worker

The standing-rules sections at the top of the repo-root LOOP_STATE.md apply to this revision experiment as follows:

(1) PURE ZAG ONLY is a literal red line. This is a revision experiment on a frozen contestant: I will modify only the Zag source (one line, the rotation tie-break), compile with the pinned znc, and run with shell only. No Python for any purpose: not in the implementation, not in the driver, not in analysis. All verification via shell, git, sha256sum, and cmp.

(2) Shell-only byte checks. All dash checks run via the shell-only `check_no_dash.sh` snippet at `docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh`. Never python3 for byte checks.

(3) Fork testing and image-judge rules are not applicable to this revision experiment.

(4) Commits stay local on branch tnn-native-lab with explicit pathspecs confined to `docs/lab/research-lead/overnight-20260928/c1_smallk/`. I will inspect `git status` before every commit and never touch other workers' files. The contaminated paper `TNN_RESEARCH_PAPER_20260929.md` is outside my owned path and will be left untouched (verified zero diff before and after). If I hit a live `.git/index.lock`, I will wait and retry; never remove it.

(5) Frozen history is immutable. I will never amend or rewrite any shared-branch commit. The F-E family sealed worlds from 6e03b2fa5 are reused byte-identical (hashes verified); they are not regenerated.

(6) Preregistration strictly precedes implementation. The PREREG is committed alone before any source modification exists.
