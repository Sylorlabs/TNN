# Genuineness proofs

Raw execution outputs proving each plant's variation path is genuine
(all runs: `<plant-binary> <state1.bin> <input.bin>`, harness prints
64 bytes as hex).

- `pNN_r1.txt`, `pNN_r2.txt`, `pNN_r3.txt` (NN = 01–05, 10–13, 15, 16):
  three runs each; the three outputs are pairwise distinct —
  getrandom / clock_gettime / urandom bytes genuinely flow into the output.
- `p01_r{1,2,3}.txt`: deterministic per binary by design; bytes 0–3 are
  `65 5f 56 5c` = `7f 45 4c 46` (ELF magic of the plant's own binary) XOR
  the fixtures — real `/proc/self/exe` bytes in the output.
- `pNN_r1.txt` (NN = 06–09, 14, 19, 20): single runs; uninit/freed heap
  bytes observably flow into the output (tails/prefixes differ from the
  initialized pattern — see REDTEAM_REPORT.md §5).
- `p17_r1.txt`, `p18_r1.txt`: byte-exact match to an independent Python
  simulation of the documented hash functions (all 64 slots occupied,
  slot-order iteration) — real tables, not stubs.
- `p14_r2.txt`: second run of plant14, byte-identical to `p14_r1.txt`
  (deterministic use-after-free read on this platform).
