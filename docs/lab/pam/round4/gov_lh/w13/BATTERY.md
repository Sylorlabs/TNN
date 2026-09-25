# W13-GOVLH battery log (crew 3, 2026-09-24)

Pinned toolchain: ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
Streams (gen_lease_govlh.py, frozen §2/§5 formula):
- w13_stream_base_10x.txt: 100500 events, sha256=0bdb86fea256ef5480420d014ef503180d4030d1c1d994781e882c9c35b1eb26
- w13_stream_adv_10x.txt:  101500 events, sha256=f926b6d50dd71a4bcc797b0ea1525e33301dc7b214001ea0962a72f9b504d772
- w13_stream_base_100x.txt: 1005000 events, sha256=01cd189a7191946b15f334da8e91276664a73d7ce112715ba49221f2c006aca5
- w13_stream_adv_100x.txt:  1015000 events, sha256=4f48e02f5848cacca6fb4763bc26dc2e6a0079ee32f2735cc417fefcf96e8fda

Binaries (SHA-256):
- w13f_lease: 7f7443200ea8fc277c873674bba367abc91d7f2473b85245b1a6a13725840b67
- w13a_lease: a9af6c6a2e8622fdbff075db1ccc117b5fa8cbe71099c5d1df3f58302571927b
- w13b_lease: 915bd34eda630546d7ff6ed98cc3f44537ab04349cf1f2b435d5ccdc456c5e17

## 10x results (all K2 byte-identical r1/r2, 0 scorer mismatches)

| cfg | stdout sha | LIVE | K1 | K1-adv | K6 | K4 | K5 | result |
|-----|-----------|------|----|--------|----|----|----|--------|
| f_base | 8dd7d7bee38b9827dfcd2fab15185f98932467be627f7348c35e9905dc67d8a1 | 66500/100000=66.50% | 0 | 0/0 | 2 | 1 | all | HOLD |
| a_base | b74494e9d06fa0cc7aae8f1ecf40ecba25e2486d9bdfefe328befd5006716fb0 | 100000/100000=100% | 0 | 0/0 | 2 | 1 | all | SURVIVE |
| b_base | c3b3a00746f958e61d14863369e2ec5820ccc847a39f2970066569b17b5ebf3c | 100000/100000=100% | 0 | 0/0 | 2 | 1 | all | SURVIVE |
| f_adv | 9421a17d2767ecb2b1414c20ae919cf8a3f379c8ffed93aeb38d64490141237b | 66513/100000=66.51% | 0 | 667/1000 (both=167 m1only=333 m2only=0 none=0) | 2 | 1 | all | DEAD (K1-adv) |
| a_adv | 09d3190f4bf5345e2e2aeca9114e34337b689e798a19e9b06ff32cb5def0e95b | 100000/100000=100% | 0 | 1000/1000 (both=500) | 2 | 1 | all | DEAD (K1-adv) |
| b_adv | 906ba15df5acc40337935f11ca15e2b8d72633bf2059cf21b2f14ddc7aa6040f | 100000/100000=100% | 0 | 1000/1000 (both=500) | 2 | 1 | all | DEAD (K1-adv) |

F-COLLAPSE: A/B C-lines byte-identical on base-10x (27db176f...) and adv-10x (2ff82d2b...).
D-GOVLH-1 (live-vs-snapshot ACTIVE divergence): base 33500/100500, adv 33820/101500.

## 100x results (all K2 byte-identical r1/r2, 0 scorer mismatches)

| cfg | stdout sha | LIVE | K1 | K1-adv | K6 | K4 | K5 | result |
|-----|-----------|------|----|--------|----|----|----|--------|
| f_base | c1b9c96647f9a3216b390b55273a5542fa8dfb35b3d259ff7c16bcfebd1ca375 | 665000/1000000=66.50% | 0 | 0/0 | 2 | 1 | all | HOLD |
| a_base | 3b891840b111fa48070015ad1174af093db1d4d251be0c54307b916401cdde18 | 1000000/1000000=100% | 0 | 0/0 | 2 | 1 | all | SURVIVE |
| b_base | 3fb67def9287eb5c1887732c90ccf36eb06720ed13f02a1355fc1fb796d62eb1 | 1000000/1000000=100% | 0 | 0/0 | 2 | 1 | all | SURVIVE |
| f_adv | 732a8cebc55fa7113ebb4c884d8a357ac92286ff0d0e86eb0ec22555b523bb7f | 665722/1000000=66.57% | 0 | 6667/10000 (both=1667 m1only=3333) | 2 | 1 | all | DEAD (K1-adv) |
| a_adv | ec3c7cb1cdfe1b0277482df47f6d1e4c615f699421d254442fd90a45da6112d3 | 1000000/1000000=100% | 0 | 10000/10000 (both=5000) | 2 | 1 | all | DEAD (K1-adv) |
| b_adv | df0b9cd8b56730769e684caad88e499e115d6e9c739a474efe4dcbd5a6b29287 | 1000000/1000000=100% | 0 | 10000/10000 (both=5000) | 2 | 1 | all | DEAD (K1-adv) |

F-COLLAPSE at 100x ADV: A/B C-lines byte-identical (dfdafae7…).
Battery complete 2026-09-25 ~00:30 UTC. Note: a daemon restart at ~00:12 UTC
killed the in-flight a/b_adv_100x r2 runs; r2 legs were re-run cleanly and
K2-verified against pre-restart r1 SHAs (no r1 was re-run, SHAs unchanged).

F-COLLAPSE at 100x: A/B logs differ ONLY in the header line (diff: 1 line);
all 3,015,000 G/C/L data lines byte-identical. (The a/b .gz size delta —
6.3MB vs 22.3MB — is a gzip phase-alignment artifact from the 5-byte header
length difference, not a content difference.)
D-GOVLH-1 at 100x BASE: 335000/1005000. Staleness hist exactly
{0:335000, 1:335000, 2:335000}.
