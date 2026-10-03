# Interactive survey: wave-20260929-0821pdt

Question: does a runnable interactive TNN exist on this branch for
red-teamed probe chats, beyond the frozen probe instruments?

Range surveyed: d2fdf1225ec973e1e07082af6b067fd1525cb643 (0521pdt
run-start pin) .. d24eda8bdc34dee54aace6451b193754e96784ab (this
wave's run-start tip). This range contains the morning research-lead
session commits, including 17 new .zag files under
docs/lab/research-lead/overnight-20260928/ (bridge_learn,
causal/causal_learn, causal/causal_world, causal/baselines,
genbias_test, integ_learn, pi_adversary/*, rep_v2/fdcr_learn,
route_learn, sem_l3/*, stress_learn, unified_learn).

Entry-point scan (git show at the tip, word-boundary grep for
stdin, _zag_arg, repl over all 17 files): the only hits are
_zag_arg(1)/_zag_arg(2) file-path arguments in causal_learn.zag,
causal_world.zag, baselines.zag, and fdcr_learn.zag (obs/probe file
inputs to batch instruments). Zero stdin-read chat loops, zero REPL
loops, zero interactive chat entry points. git diff --stat over src/
and units/ in the range: zero changed files.

Conclusion: NONE loop-owned and none new in the range. The frozen
probe instruments (tnn_chat.zag, tnn_chat_decline.zag, holding a
stdin line loop over the 38-fact KB) remain the only chat-capable
instruments on this branch, and they are batch probe instruments,
certified by the FIT lane, not a general interactive TNN. Micah's
frontier dirs were surveyed read-only; nothing there was modified.

Method limit: a code-text scan over the surveyed range only; not
evidence that interactive TNN is impossible in principle.
