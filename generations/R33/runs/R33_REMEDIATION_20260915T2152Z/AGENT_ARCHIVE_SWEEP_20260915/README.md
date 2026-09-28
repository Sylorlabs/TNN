# N17 / R25 / R26 exact archive recovery lane

Run `../run_exact_archive_sweep.zsh` from a native execution window.

The sweep enumerates local TNN tar/zip archives, lists candidate historical R25/R26 source/state/policy/manifest members, streams candidate bytes directly to SHA-256 without executing or deserializing them, and records exact matches to the three currently known historical hashes.

Admission is exact-hash only. Similar names, shadow states, witness receipts, and reconstructed artifacts do not close the historical verifier-equivalence rows by themselves.
