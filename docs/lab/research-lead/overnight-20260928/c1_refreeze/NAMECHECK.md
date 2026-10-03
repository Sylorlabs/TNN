# C1 Clean Re-freeze: NAMECHECK

Step 0: Toolchain guard (strict, zero tolerance).

- Ran `which python3 python` against a filtered PATH before any work.
- Result: `python3` exists at `/usr/bin/python3` (also `python3.12`).
  System binary; surgical removal from the OS not possible.
- Mitigation applied: created a safe-bin directory of symlinks to all
  executable tools in /usr/bin, /bin, /usr/local/bin EXCEPT anything
  matching *python*, *pypy*, *conda*, *pip*, plus node/nodejs/deno/bun
  removed (JavaScript is also a forbidden research language).
- Every shell command in this session begins with
  `export PATH="<safebin>"`.
- Verified: with the restricted PATH, `which python3 python node nodejs`
  returns nothing (exit 1).
- Perl/awk symlinks remain in the bin but are NOT used for research
  logic in this session; only grep/cut/tr/wc/diff for inspection.
- Commitment: no forbidden executable will be invoked for any purpose
  in this wave, including inspection aids. Any invocation = PROCESS-FAIL.

Incident log:
- 2026-09-30 ~20:45 UTC: /tmp was wiped by the runtime, destroying the
  original safe bin (/tmp/c1_refreeze_safebin) and killing the background
  drive at 22/60 runs. No Python was invoked; the wipe was environmental.
- Safe bin recreated at ~/workspace/c1_refreeze_safebin (persistent).
  Drive resumed with skip-if-done logic for the remaining 38 runs.
- The /tmp/c1_refreeze_verify rebuild directory was also lost, but the
  byte-identical rebuild verification (sha256 match) was already recorded
  before the wipe.

Owned path: docs/lab/research-lead/overnight-20260928/c1_refreeze/
Task: cleanly re-freeze the C1 pure-Zag driver re-derivation
(commit d5984f313) after the prior wave's Python process incident.
