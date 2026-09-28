# MATH R4 batteries

Frozen prereg: docs/lab/math_logic/round4/PREREG_MATH_R4.md (commit 84ed45077a554f9897ec55c2ca1430273c79eb69).

Contents:
- chain_nl/ : 20 raw-NL chain problems (5 per domain: number_theory, geometry, logic_puzzles, causal_temporal), each requiring 5-20 derivation steps. Public files carry NO verdicts, solutions, or traces.
- chain50_nl/ : 6 raw-NL long-chain problems requiring 50-160 steps. Public files carry the problem only.
- para_inv/ : 12 paraphrase pairs + 12 nonce-word variants (public problems only). PARA_ENTAIL.json records the statement alignment and numeric signatures (no verdicts).
- knowledge/ : KNOWLEDGE_STORE_NL.md (R4 wording) and KNOWLEDGE_AUDIT_R3_R4.md (full R3->R4 wording audit of all 25 items).
- sealed/ : sealed solutions, reference traces, nonce maps, skeletons, and MANIFEST.sha256. Engine crews must not read this directory.

Verification: run `python3 verify_battery.py <battery_dir> <source_dir>` (byte-identical
rebuild + all checks). The builder (gen_battery.py) is deterministic Python over
hand-authored data (zero RNG); byte-identical rerun is verified, not assumed.
Sealed-solution isolation: w_sealed() exits 3 on any non-sealed/ write; the verifier tests this.
Determinism: pure deterministic construction, zero RNG; rerun must be byte-identical.
