# SHA-256 manifest — production intake v2 (learned policy), 2026-09-26

Unchanged upstream files (not re-listed): R33_NATIVE_IO_V1.zag, negcontrol.zag,
gen_phase1.py.

```
5a4e6789df98ba013dcaa06ff865604e93b887ed666827d82ec5db1db760b1bc  intake.zag
ffabd23b525769dd21c35d9762633ca75412ecb476969749aff46f880091a5c6  battery1.zag
9b322d077ad93af0b448ce6af9e0ec829c30b3b5ed6c8e248b1ed3b04cf1e8ee  build.sh
da76d2dd0b0ae39f5945bb579888a404919b0fc063b1f9765f73c040f56343f9  regress_degen.zag
2f224d7620264e49c407f4f6dbb1c5a710f37ba883be797f12285560c78e13ca  build_regress.sh
4026a3675fc3f024ba69714b9e541131fe565076898237aa9e9de36e9927c955  VERDICT.md
0a34116398fcd22b313c785c1d1037d712a444f18b3925ce49ac29316a41d268  evidence/RUN_LIVE1.out
0a34116398fcd22b313c785c1d1037d712a444f18b3925ce49ac29316a41d268  evidence/RUN_LIVE2.out
8880c82e8cc99ac3a6a8671dd1daba779b9b2e766012e5f19068655a0064b3fb  evidence/DEGEN1.out
8880c82e8cc99ac3a6a8671dd1daba779b9b2e766012e5f19068655a0064b3fb  evidence/DEGEN2.out
```

Regression: 57/57 correct, 57/57 native, 0 fallbacks; reruns byte-identical.
Degenerate-input regression: 6/6 correct, 6/6 native, 0 fallbacks; reruns byte-identical.
