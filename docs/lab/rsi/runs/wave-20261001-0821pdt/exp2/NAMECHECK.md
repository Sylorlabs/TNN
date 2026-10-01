# NAMECHECK wave-20261001-0821pdt lane exp2-altexplain (H-EXP2 v2 step 6)

Step 0: toolchain guard activation.
Command: bash ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
Output: safebin: /home/hatch/safebin; linked: 36 tools; znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1); verify: python3 absent from safebin PATH (OK); verify: python absent from safebin PATH (OK); SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
Command: export PATH="$HOME/safebin"
Command: which python3
Output: NOT FOUND
Command: command -v python
Output: NOT FOUND
Command: which znc
Output: /home/hatch/safebin/znc
znc --version: znc 2026.07.0-dev (edition 2026)
All subsequent shell work in this lane runs with PATH restricted to /home/hatch/safebin.
All research logic in this lane is written and executed in pure Zag via znc. Shell is used only to invoke znc, run binaries, do git ops, and move/copy files.

Step 1: forbidden-executable audit (updated at wave end).
(no forbidden executable invoked; audit to be completed at wave end)
