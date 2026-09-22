# B-T1 repaired-module retest — run manifest (crew3, 2026-09-21/22)

Battery: repaired `arms_bin_repaired` (built 2026-09-21 from
`units/r0/impl/arms/arms.zag` with pinned znc `znc_linux_x86_64_abed8aa1`),
11 arms × {pg100.txt, sqlite3.c} × N=2. Every pair required byte-identical
(r1==r2 via `cmp -s`). The 10 non-grounded arms additionally hash-checked
against the frozen closeout goldens (`closeout/RUN_MANIFEST.md`).

Corpora (verified 2026-09-21):
- pg100.txt: sha256 3cf4b3d44ee14cff4e14e78e2ad3318eff76f3f7f2afc3cee6bb925879110a37 (5,638,480 B)
- sqlite3.c: sha256 b1dd5d74ec7f29055a6684fa06fb3c2f6821c87dd38f9a458dfd2e8a1db28189 (9,515,341 B)

## r1 sha256 + pair equality

| arm__corpus | sha256 (r1) | r1==r2 | closeout golden |
|---|---|---|---|
| predictive_surprise__pg100 | 79d25904f2db5534cb8acad468f03b7253681250f2b692e55a9d79fccac197c8 | yes | MATCH |
| predictive_surprise__sqlite3c | 5d30be791d4d7e41e51fa9b172d080d91eebe55c6abd700095f130ff0f1d358d | yes | MATCH |
| fixed_window_4__pg100 | 416b9a5b6276887382c502d0eb6614dc60e3fc43c0d272ddc70daa748f1ba272 | yes | MATCH |
| fixed_window_4__sqlite3c | 55bf1070245c59d69248e55f34532754a42d210ace390c5f8ddc8c6475dee992 | yes | MATCH |
| fixed_window_8__pg100 | 5bd3a4154967a152b5cafde0b576400714d5ab570c0ce70561ee0dc391a4cd2d | yes | MATCH |
| fixed_window_8__sqlite3c | 8fb4e4de9f7100dc26d736c608172f2720762ca402bf656c54bef7d4938449a4 | yes | MATCH |
| fixed_window_16__pg100 | 888e73a742ea42ad5195f9df86a4acd5e48413c7c4918eb234111f5d0e1d62ac | yes | MATCH |
| fixed_window_16__sqlite3c | 4418330f96710df9bfe4a76efcde03be8dd9f42ad06d32d85e3cf3298d0d1e08 | yes | MATCH |
| fixed_window_64__pg100 | f888b99b371bcef7b926931d981ff50d145041922c44f217ad29a40552bc8f27 | yes | MATCH |
| fixed_window_64__sqlite3c | 94210c4d4480f584c7316fb4af682bdcd337a5f16052407b5ae0e75729327e2e | yes | MATCH |
| adaptive_mdl__pg100 | 3ca691bc0a8dfeec98c65b3b9428965786727cd85124a971a2e0a0a238094240 | yes | MATCH |
| adaptive_mdl__sqlite3c | 68394d26d9dcc3cd7e2c6aec058eb4147920ad3fa9ab290eb6ee69f656976ca7 | yes | MATCH |
| adaptive_mdl_8__pg100 | 33e2e517f17aff798f1cefcc19b8ff6efd0a5de110da8981c4489c77e342de28 | yes | MATCH |
| adaptive_mdl_8__sqlite3c | cab9644146d72357348eb8f6f506b0a9ff9bd1fc3f41334aa9cf40068fed9dd1 | yes | MATCH |
| hierarchical_mdl__pg100 | 94d58c865b52fd3f4ee670529b6747227baac29963fe1512df64e01b0b06ad0f | yes | MATCH |
| hierarchical_mdl__sqlite3c | e99e945d31c92239f3e3935b98d1ff08d270fca9a789fa92bc4045a33a2f87b1 | yes | MATCH |
| raw_micro__pg100 | a599775b1bdbb2433737bb71361cf5719bb5c9216885d5e8666c06a574c8f0ee | yes | MATCH |
| raw_micro__sqlite3c | 4d79135e542507ede19e946f55ccc91ffc1f2a908c87d69d396cd2226fce464a | yes | MATCH |
| random_chunks__pg100 | 7b64a5dc40ab03cf7d987dfb768100ccd026ebc43e505d4da292c39250e1bede | yes | MATCH |
| random_chunks__sqlite3c | 79aaaca84aa112f754fb1e5a0e8c8a09eb92462ab1a8737b90ee26445364ed68 | yes | MATCH |
| grounded_adaptive_mdl__pg100 | d5455e201fd6fa038f07882b5447ad4e815ffc09704508410212aa613970688a | yes | n/a (was CRASHED) |
| grounded_adaptive_mdl__sqlite3c | 57f61024da08cc5f01436816bd34b9db634ca2a215f2671ed9b6b40f8ee018a1 | yes | n/a (was CRASHED) |

Battery log: `BATTERY.log` (this directory). Full per-run OK/MISMATCH lines
with golden hashes are recorded there. Battery completed 2026-09-22 with
`done fail=0` (all 11 arms × 2 corpora verified; grounded verified separately,
recorded in BATTERY.log with SKIP on restarts).

Note: `.seg` run outputs are NOT committed (65–130 MB each for grounded).
Hashes above + the battery log constitute the reproducibility record; the
closeout goldens cover the 10 non-grounded arms.
