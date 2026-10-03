# Determinism Manifest — M3 Retry

Two complete runs per arm (D/N/A). Recursive diff of run1 vs run2 per arm: byte-identical.

| Arm | run1 files | run2 files | Diff result |
|-----|------------|------------|-------------|
| D | 27 | 27 | IDENTICAL |
| N | 27 | 27 | IDENTICAL |
| A | 27 | 27 | IDENTICAL |

All runs completed with "run complete" (no panics, no errors).

SHA-256 of run1 output manifests (for verification):
## D run1
7499bdd1bbf2ddfe3c17d3cdd5b350575cf97449cbf1412d31a7c722cd0c3741  chat_S1.txt
076c7089e48f29a9b275280212e3df31322ec558ba544ca2b198abfefecb5759  chat_S2.txt
4b26eedec9831f2b1efe9aaa16fed2e5c7951021f3250174cadab6f73ca58fb7  chat_S3.txt
2036523392884f88bdf94eb1a7fc7381203492f415cebdcebf67be43dc7d985e  chat_S4.txt
d0e86e6955687da284b7bbc390f20ac1e2b003f240bfa59aab294d44e4865a13  chat_S5.txt
## N run1
7499bdd1bbf2ddfe3c17d3cdd5b350575cf97449cbf1412d31a7c722cd0c3741  chat_S1.txt
076c7089e48f29a9b275280212e3df31322ec558ba544ca2b198abfefecb5759  chat_S2.txt
4b26eedec9831f2b1efe9aaa16fed2e5c7951021f3250174cadab6f73ca58fb7  chat_S3.txt
2036523392884f88bdf94eb1a7fc7381203492f415cebdcebf67be43dc7d985e  chat_S4.txt
d0e86e6955687da284b7bbc390f20ac1e2b003f240bfa59aab294d44e4865a13  chat_S5.txt
## A run1
7499bdd1bbf2ddfe3c17d3cdd5b350575cf97449cbf1412d31a7c722cd0c3741  chat_S1.txt
076c7089e48f29a9b275280212e3df31322ec558ba544ca2b198abfefecb5759  chat_S2.txt
4b26eedec9831f2b1efe9aaa16fed2e5c7951021f3250174cadab6f73ca58fb7  chat_S3.txt
2036523392884f88bdf94eb1a7fc7381203492f415cebdcebf67be43dc7d985e  chat_S4.txt
d0e86e6955687da284b7bbc390f20ac1e2b003f240bfa59aab294d44e4865a13  chat_S5.txt
