# Frozen-source / rebuild hashes — 2026-09-21 rerun

## certifier (thin-certifier/certifier/)
- `thincert.zag`:        9b55fa2f158d98c31b4011c09f2f2a4394e740d9fa95450cad2ad5bdea9bbbd3
- `run_thincert.sh`:     b5bfff3d2d3f4fd94b99ec844f269d5161a3596ac7fa898665f1af5fe0eee343

## rebuilt certifier binary (two independent builds, byte-identical)
- `thincert_b1`/`thincert_b2`: d5e4de746a790b234726a3bcd5043bbfb7487fea203f7005e88b8c8012f2d3ca
  (matches pinned/recorded hash; binaries removed before commit)

## repbuild clean binary (fresh rebuild from frozen source)
- `variation.bin`:       75cf2006ca044081caad740afbf29b239a38dc9bb3214e477830912bd943a83c
  (matches recorded BIN; binary removed before commit)

## fresh plant binaries (pinned toolchain)
- dirty2_clock:          8396d8bf8ee209595da3be250e5d6e21a964c6f1f9cb271dfb900d658041b694 (matches record)
- dirty3_uninit:         faf161608b6f6e60c9a220f507f05f7e24ab7ca97aeb16efa433fd (matches record)
- dirty5_ptrleak:        6116425cf92783ec23707e5dd8c435c47d53c51b694e5546542bb1e7e31dc706 (matches record)
- dirty1_urandom:        NOT BUILDABLE with pinned toolchain — recorded BIN 5f70bf18…
                          is not reproducible from frozen sources (calls nonexistent
                          nio_open_readonly and _zag_rand, probed UNKNOWN on this toolchain)

## replay fresh 64+1 build
- `real_substrate_sha256`:  e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8
- `adv_template_sha256`:    eb801d7ed210095844bbb4895069a173873fe2bcf2bb16c4a323d762d7e8333d
- `driver_sha256`:           5c04a8ac53b0729cbc4f930da4045454f378217bebf8abc4430c225c66cd2101
- `driver_zeroing_sha256`:  69973d603e6c4da269c2269e64d8ec931c3329396c7255d78c4b069e22f86fdf
