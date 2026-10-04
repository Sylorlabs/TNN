# INTERACTIVE_SURVEY_1121.md

Wave: wave-20260929-1121pdt. Run-start pin: 5f86e6cb2eaedb115235e4af52684a44b7c6eb36.
Survey range: d24eda8bdc34dee54aace6451b193754e96784ab..5f86e6cb2eaedb115235e4af52684a44b7c6eb36
(the 0821pdt tip to the 1121pdt run-start tip; HEAD was static at the pin when the survey ran).

Method: git diff --diff-filter=A --name-only over the range filtered to .zag, plus a
--diff-filter=M check for modified .zag files; each new file grepped for stdin reads
and REPL patterns (stdin, readln, read_line, getline, repl, chat, prompt, interactive)
and its usage header read.

Result: NONE new interactive candidates.

New .zag files (2 added, 0 modified, both 220 lines, byte-identical to each other):
- docs/lab/rsi/runs/wave-20260929-0821pdt/impl/exp_learn.zag
- docs/lab/rsi/runs/wave-20260929-0821pdt/evidence/build_host/exp_learn.zag

What they are: exp_learn.zag is the discriminating-experiment invention program from
the 0821pdt H-EXP work. Usage is `exp_learn <hyp1.txt> <hyp2.txt>`; it parses two
hypothesis files, enumerates action sequences of length 1..3 over actions 0..5,
simulates each under both hypotheses, and emits the shortest discriminating sequence
or the exact WITHHOLD line. There is no stdin read loop, no REPL, no chat prompt,
and no interactive entry point. It is an experiment-invention instrument, not a
conversational one.

Conclusion: the frozen probe instruments remain the only chat-capable instruments on
this branch. No runnable interactive TNN exists on tnn-native-lab at the run-start
tip for red-teamed probe chats beyond what was already instrumented at 0821pdt.

No em-dashes used in this document.
