# Interactive-TNN merge survey, wave-20260927-1421pdt

Scope: merge range b08dc57f2..9beb0adea (the origin side merged at b876016e6, b876016e6^1 local, b876016e6^2 origin 9beb0adea).
New commits in range: 9beb0adea (hyptest sealed battery results), 9eacb1c48 (hyptest frozen prereg), 1638fe526 (upscale round 4 subtree attach), a1e6fc3b4 (upscale round 4 honest all-arm kill), 3cd24f11d (workbuddy round 2), fd1f1d0f0 (epistemics round 2 held-out run), d836ca7b7 (epistemics round 2 prereg amendment), 6a0bec5e5 (continual-learning benchmark v2 GO), a607ff549 (continual-learning cl-repair-v2).

New .zag sources in range: docs/lab/epistemic_native/round2/{ehelp,epistemic_r2}.zag; docs/lab/hyptest/build/hyptest.zag; docs/lab/image_upscale/generation_fix_round4/arm_p{1..4}/*.zag (azgen, azlayers, common_az); docs/lab/workbuddy/wb_dialogue.zag; docs/lab/workbuddy/round2/wb2_dialogue.zag.

## Findings

1. A new interactive chat/REPL entry point EXISTS in source, authored by Micah himself in commit 3cd24f11d (workbuddy round 2, origin side, his frontier line, CLOSED to the loop). wb_dialogue.zag (line 4102) and wb2_dialogue.zag (line 5894): argv[1]=="chat" mode, "persistent stdin/stdout conversation. One process = one session". Reads stdin via stdin_line(line, 4096) in a while loop, turns processed by do_turn, session-taught facts live in process memory only and evaporate on exit. Requires gaz.txt and kb.txt in the working directory (gaz_install/kb_install calls). Batch mode untouched.

2. No stdin reads in the new epistemic_r2/hyptest sources (their keyword hits are comment-only: "replicates gen_interp", "replaces"). No stdin reads in the new image_upscale generation_fix_round4 sources (hits are "replacement" in comments). hyptest battery ships shell scripts (run_dev.sh, build.sh, check_citations.sh) plus a Python fixture builder (docs/lab/hyptest/phenomena/sealed/build_phenomena.py): these are his lines' tooling, not loop instruments; loop did not invoke them.

3. Existing frozen probe instruments unchanged: docs/lab/rsi/fit_authority/tnn_chat.zag and tnn_chat_decline.zag untouched this merge range (name-match hits in the survey were pre-existing wave-record scratch files, not new in the range).

## Verdict

For red-teamed probe chats, no runnable interactive TNN exists this wave beyond the frozen probe instruments. The workbuddy chat mode is Micah's own unvetted frontier code (his line, CLOSED to the loop): the loop did not build, run, or certify it, and probe-certification of his frontier material is his decision, not a wave action. tnn_chat/tnn_chat_decline FIT pins stand (fresh FIT re-run due within 8 waves; stale count 1 of 8 entering this wave).
