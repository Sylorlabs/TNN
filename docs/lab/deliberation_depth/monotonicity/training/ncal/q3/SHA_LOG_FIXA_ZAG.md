# SHA LOG — FIX-A pure-Zag port

## A. Fixture-generator byte-identity proof (Python vs Zag)

Reference Python outputs generated from `q3/fixbuild.py` before deletion.

| Input | FIX | Python SHA-256 | Zag SHA-256 | Identical |
|---|---|---|---|---|
| necc_s1.tsv | A | 19a55e961f15f5cbe7e9002faa234f03affa9fbe2d8b9f57f3ef284d3c75eda1 | 19a55e961f15f5cbe7e9002faa234f03affa9fbe2d8b9f57f3ef284d3c75eda1 | YES |
| necc_s1.tsv | B | 13872571f2e432ee5c21abf337d1617df067212f7bd5d4c85d994eae4a2eff49 | 13872571f2e432ee5c21abf337d1617df067212f7bd5d4c85d994eae4a2eff49 | YES |
| necc_s1.tsv | C | 561c2b2ac9e24328071a9f45e6fe5661e16873badf74e23aa22d5162c2044880 | 561c2b2ac9e24328071a9f45e6fe5661e16873badf74e23aa22d5162c2044880 | YES |
| necc_s1.tsv | D | 3cf206da5d4a4a543c41391bcfd3184ad475a450ea7be32584d787c544dd5f19 | 3cf206da5d4a4a543c41391bcfd3184ad475a450ea7be32584d787c544dd5f19 | YES |
| necc_s10.tsv | A | 1d8d05c42d3c017aa98eeb9212aa6e2f6c4b4cf6a9d5f6a21a998838d539fd42 | 1d8d05c42d3c017aa98eeb9212aa6e2f6c4b4cf6a9d5f6a21a998838d539fd42 | YES |
| necc_s100.tsv | A | 1a29be570ba3fe83adb6c66b5500a515cf1eb8a8a58c59d70f14081c541e41a5 | 1a29be570ba3fe83adb6c66b5500a515cf1eb8a8a58c59d70f14081c541e41a5 | YES |

FIX-A s1: 8,506 rows. FIX-A s10: 85,060 rows. FIX-A s100: 850,600 rows
(33,273,050 bytes — exercises the streaming output path).

## B. Scale battery: m11 + pure-Zag FIX-A fixtures (3× reruns)

Driver: frozen m11 (`nec_scale_big.zag` rebuilt from source with the pinned
toolchain; rebuilt binary byte-identical to the Q2 binary on trap_t1).

| Scale | Rep | Driver-output SHA-256 |
|---|---|---|
| s1 | A | ee4fbafd74c823c4f2e8a1270f322070928eaae059bb7dab866d484e0605364d |
| s1 | B | ee4fbafd74c823c4f2e8a1270f322070928eaae059bb7dab866d484e0605364d |
| s1 | C | ee4fbafd74c823c4f2e8a1270f322070928eaae059bb7dab866d484e0605364d |
| s10 | A | 873e67f40aaa27ba0b33743672cfa0aad9a445c209e4e14f23bfbbf5411dcadc |
| s10 | B | 873e67f40aaa27ba0b33743672cfa0aad9a445c209e4e14f23bfbbf5411dcadc |
| s10 | C | 873e67f40aaa27ba0b33743672cfa0aad9a445c209e4e14f23bfbbf5411dcadc |
| s100 | A | d86bcb5268df1e24a37c2b5709abb598ba07a8946cb1a3d2f73ea3601ce2acd7 |
| s100 | B | d86bcb5268df1e24a37c2b5709abb598ba07a8946cb1a3d2f73ea3601ce2acd7 |
| s100 | C | d86bcb5268df1e24a37c2b5709abb598ba07a8946cb1a3d2f73ea3601ce2acd7 |

9/9: three byte-identical reruns per scale. All match the Q3
Python-fixture reference SHAs (`SHA_LOG_Q3.md`).

## C. Probe batteries (T1–T4 audit; FIX-A-augmented, Zag-generated)

| Battery | Fixture SHA-256 | Driver A/B |
|---|---|---|
| trap_t1 + FIX-A (480 rows) | 0a72c04d201dd7fcd30ee1277690cc6ca1a602a9f2e772203c05a47000c16b43 | 47214c56…89aad identical |
| trap_t3 + FIX-A (1280 rows) | cb4eb263eab7ca391b2fafd558bdbcea329c9de7aa61bc71956275f0d27a9c71 | d68dfbd6…59d159 identical |
| necc_s1 + FIX-A (8506 rows) | 19a55e961f15f5cbe7e9002faa234f03affa9fbe2d8b9f57f3ef284d3c75eda1 | ee4fbafd…5364d identical |

## D. Source pinned

- `q3/fixbuild.zag`: SHA-256
  `0086932eaa72aa7c839ae05854d1ddff0e686b4050c1fde4f0047c46895d06a4`
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Mechanism source `nec_scale_big.zag`: SHA-256
  `51c26c1da14848a6302133f31e11c5004ab394e4e70e06901679335b6f17a316`
