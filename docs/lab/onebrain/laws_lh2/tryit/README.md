# Try-it: the 9 composition laws, runnable

This is a small self-contained demo of the nine Fable composition laws — the
governance layer that sits over the repaired one-brain organs. It runs a fixed
battery of 5 scenarios through the real laws dispatch (the same code that
passed 37/37 long-horizon checks), prints what happens in plain language plus
the raw check lines so you can verify it, and confirms the run is
bit-for-bit deterministic.

## Run it (on the lab VM)

Run these in a terminal **on the lab VM** (e.g. over SSH) — not on the Mac.
Copy-paste this block:

```
cd ~/workspace/ob_laws_lh2/tryit
./run_tryit.sh
```

If the script fails, the manual fallback is:

```
cd ~/workspace/ob_laws_lh2/tryit
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 build try_laws.zag -o try_laws.bin
./try_laws.bin
```

(The build takes ~30 seconds; the run takes a couple of seconds. The laws
sources are vendored copies in this directory, byte-identical to
`~/workspace/ob_laws_lh2/shared/`.)

## What success looks like

The last two lines of output must be exactly:

```
TRYIT: 5/5 scenarios behaved as expected — ALL OK
DETERMINISM: 3/3 byte-identical
```

## What each scenario proves

1. **Honest request accepted (law 1):** a properly signed cross-organ request
   is authenticated and executed — install, then force-pin, then promote,
   with the promote audited as succeeded.
2. **Tampered request refused (law 1):** a message altered after signing is
   refused *before* anything executes — nothing runs, the queue drains, and
   the attempt is written to the ledger.
3. **Real collision, bounded and escalated (laws 2, 4, 7):** a promote that
   collides with a pending revoke over a pinned claim is refused, citing the
   revoke's receipt; tied weights trigger exactly 10 rounds of deliberation,
   then a complete escalation entry naming both sides.
4. **Corroboration (law 6):** five sources sharing one root count as a single
   source, so promotion is refused; five genuinely independent sources are
   accepted.
5. **Revision chain (law 9):** the append-only log verifies intact, a single
   flipped byte is detected (and the bad entry is named), and a legitimate
   new entry appended afterwards still verifies.

## Same files in the repo

`docs/lab/onebrain/laws_lh2/tryit/` on branch `tnn-native-lab`,
commit `REPO_SHA_PLACEHOLDER`.

## Troubleshooting

- `BUILD_FAIL`: make sure the `~/workspace/toolchain` symlink exists (it
  points at `~/workspace/tnn-lab/toolchain`, which the laws sources import
  via a relative path). Re-create with
  `ln -s ~/workspace/tnn-lab/toolchain ~/workspace/toolchain`.
- `DETERMINISM FAIL`: the three runs disagreed — do not trust the result;
  report it instead of re-running until it passes.
