# H7R NAMECHECK (wave-20261001-2321pdt)

Lane: H7R (contradiction-driven re-derivation re-attempt; replacement worker).
Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab. Commits local only, never push.

## Step 0: worker toolchain guard (mandatory, first)

Ran, in order:
`cd ~/workspace/tnn-rsi && sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh && export PATH="$HOME/safebin"`

Exact verification output:
```
safebin: /home/hatch/safebin
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
SAFEBIN_SETUP_DONE
which python3 exit: 1
```
`which python3` printed nothing (exit 1). `which python` likewise absent per setup
script verify lines. `which znc` resolves to /home/hatch/safebin/znc.
Branch confirmed: tnn-native-lab.

Pure Zag only for all computational research operations in this lane. Shell only:
invoke znc, run binaries, git ops, move/copy files. Any forbidden-interpreter
invocation is PROCESS-FAIL: disclose immediately, cleanly re-freeze if the result
matters.

## Commit order self-check (prereg discipline)

1. H7R_PREREG.md frozen and committed ALONE (no implementation in the same commit).
2. World tables + consumer + driver committed strictly after the prereg freeze.
3. Sealed run executed only after both commits; no source edits between run 1 and
   runs 2-3 (byte-identical rerun check).
