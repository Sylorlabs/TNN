# NAMECHECK wave-20261001-1721pdt lane HEXP2 (H-EXP2 v2 step-6 attack execution)

Step 0: toolchain guard activation.
Command: bash ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
Output: linked: 36 tools; znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1); verify: python3 absent from safebin PATH (OK); verify: python absent from safebin PATH (OK); SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
Command: export PATH="$HOME/safebin"
Command: which python3
Output: NOT FOUND (exit 1)
All subsequent shell work in this lane runs with PATH restricted to /home/hatch/safebin.
No programs are written in this lane: subjects are used as frozen binaries per the prereg; no znc compilation is performed. Shell is used only to invoke the frozen binaries and the frozen shell loops, and to move/copy files. Zero Python anywhere.
Forbidden-executable audit: none invoked.

Frozen subject binaries (sha256, recorded at execution start):
- S-argmax expseq_bin: sha256 recorded in EXECUTION_RECORD.md
- S-first/S-enum altexp_bin: sha256 recorded in EXECUTION_RECORD.md
- expworld_bin (0221 and 0821 dirs): byte-identical, sha256 0301125c9308d4b6a157dc5dd9f91afb60a3cb9406654725244c3a7a5625579b
Frozen prereg: dc83844dee90c404b4e00c6acf34db1ea7fe29ef (ancestor of working-copy HEAD; prereg-first-commit strictly precedes all evaluation work).
Sealed law hashes verified before execution: law_WC.txt 4fb807b0..., law_WD.txt ff2ee02e..., law_WT.txt b3ae9ae9... (all match freeze record).
