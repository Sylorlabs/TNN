# P7 KB Profile Summary

## Configuration
- Binary: kbp (pending fork) with HOLD OFF, empty pending
- Battery: 40 clusters, frozen KB battery
- Arms: K (knowledge=True), N (knowledge=False)
- Passes: 2 per arm

## Results
- Arm K pass 1: installs=20, withholds=20 (gates: NO_CORROBORATION=8, KB_CONTRADICTION=12)
- Arm K pass 2: identical
- Arm N pass 1: installs=8, withholds=32 (gates: NO_CORROBORATION=32)
- Arm N pass 2: identical

## Determinism (KB5)
All 6 files byte-identical across passes (both arms):
- run_kb.log: IDENTICAL
- knowledge_ledger.txt: IDENTICAL
- refusal_ledger.txt: IDENTICAL

## SHAs
Arm K:
- run_kb.log: 865ddc3cfd2cb3b9419f7799d17c351afd4a46b106267b215c1b652404c0f641
- knowledge_ledger.txt: 9ab11074db030eaf906b575c6fabd628d45c27d9aa27e85a30cd661d32f773cf
- refusal_ledger.txt: a4e721f22573659024dfc23c32a51395f82d253e21117a84e9701e47dcaa9061

Arm N:
- run_kb.log: a43f7953788718eb3c139beec4f1b73759d1d124c03d7ff456a8fa3508734cf0
- knowledge_ledger.txt: cb0a69546ff7b714c92687ffc13d2bc79fc6c937e7815b98b5a272f62e6667e1
- refusal_ledger.txt: d1560b62ae944339882126f95872337bce0f471a79ab6d3fabedd398a89b4433
