# NAMECHECK.md: wave-20261001-2321pdt, lane BATTERY

Worker: BATTERY (v3 design + validation; post-freeze sealed adversarial battery).
Date: 2026-10-01/02.

## Step 0 (toolchain guard, mandatory first)

Executed before any other work:

```
cd ~/workspace/tnn-rsi && sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh && export PATH="$HOME/safebin"
```

Verification output (exact):
- `safebin: /home/hatch/safebin`
- `linked: 36 tools`
- `znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)`
- `verify: python3 absent from safebin PATH (OK)`
- `verify: python absent from safebin PATH (OK)`
- `SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)`
- `which python3` prints nothing (exit=1)
- `which python` prints nothing (exit=1)

Toolchain: safebin only (36 tools: coreutils, git, pinned znc). No Python
anywhere in this lane. All research logic (world generators, drivers,
scorers, inspectors, controls) is Zag compiled with the pinned znc.
Shell is used only for byte checks, file transport, and hash manifests.
Any forbidden-interpreter invocation is automatic PROCESS-FAIL.

## Adversary independence attestation

(i) This worker has not authored mechanism-build or mechanism-repair code
in the previous two waves. (ii) The frozen mechanism source was read for
adversarial design (white-box adversarial intent is permitted). (iii) All
writes are inside docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY/.

## Provenance

- Battery v2: 9/9 VALIDATED in wave-20261001-2021pdt (prereg
  PREREG_BATTERY_V2.md, validation VALIDATION_RUN.md, amendment
  AMENDMENT_M2W2.md for the M2-W2 fresh-state protocol).
- The 6 triviality-review corrections (wave-20261001-1721pdt,
  TRIVIALITY/TRIVIALITY_REVIEW.md section 6) are applied as design
  invariants in Battery v3. Correction 3 is applied completely this
  time: the v2 K-S11v2(d) restatement was still looser than the
  evidence-counting intent (v2 validation prediction miss 1); v3
  tightens the bar text to require both-phase licensed evidence.
- The v2 M2-W2 fresh-state baseline protocol (frozen amendment) is base
  protocol in v3, not an amendment.
