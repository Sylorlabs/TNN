# debate.zag — build & synthetic test log (2026-09-22)

Build: `znc debate.zag -o debate_bin` (cwd = src/, imports resolve there).
Warnings only (analyzer false positives on guarded `k<=eol` loops; L0010 on
pi64 is a false positive — nio_free releases the buffer).

## Synthetic tests (no trial data; all in scratch)

1. Tally bug caught & fixed: first build incremented S for every non-neutral
   record (S counted all votes). Fixed to increment S only on stance==1.
2. `opine` on 17-record synthetic file:
   - D1 S=2 R=5 V=7 p=285 -> REJECT 715 (correct)
   - D2 S=5 R=2 V=7 p=714 -> ACCEPT 714 (correct)
   - D3 S=1 R=1 V=2 (<6) -> SUSPEND 500 (correct)
   - D4/D5 no records -> SUSPEND 500 (correct)
3. `rubric` flip test: D2 ACCEPT + 6 debate REFUTES -> post SUSPEND 616,
   class=FLIP, trigger=D2X001..D2X006, verdict=EVIDENCE_DRIVEN (correct).
4. `chain` cross-checked against Python hashlib.sha256: byte-identical
   (entry0: 15c6b43d... match).
5. `verify` on 2-entry ledger: VERIFY OK 2. Two bugs caught & fixed en route:
   (a) read_file/unesc_line allocated n+1/w+1 bytes hashing heap garbage
   (agrees with AGENTS.md uninitialized-heap lesson); (b) verify copied
   prevhex into a 65-byte buffer so hexdecode64's len!=64 guard returned
   uninitialized memory.
6. Byte-identical reruns: opine 3/3 identical sha256; rubric 3/3 identical.

Binary `debate_bin` NOT committed (convention: no binaries).
