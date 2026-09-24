# RUNLOG — KB-Control Crew A reproducer runs

**Binary:** `kb_repro.zag` → `kb_repro` (native, pinned toolchain
`znc_linux_x86_64_abed8aa1`)
**Binary SHA256:** `1d9b861edbaf574c0b0d0410dff0883c45f07a144065487ac2402d9d079a8f0f`
**Method:** two runs from clean outdirs (`run1/`, `run2/`), stdout captured to
`evidence_runN.log`. Zero RNG; no timestamps in output.

## Run 1

- outdir: `run1/` (clean)
- exit: rc=0
- `evidence_run1.log` SHA256: `e335718a0074ca8797651689eaa0525ca7c0a5119fdb2985af76e7192663e753`
- chunk images:
  - `chunk_000000.dat`: `29d268e75abf9b0c9a72741a3d2c6b077c575438a800b5461f157a6964c7de3c`
  - `chunk_000001.dat`: `ff603f36209c3cf55f183deb37fba8611f9df5200f461d07978fa8e02d61273c`
  - `chunk_000002.dat`: `9b020e1a4a6e179758ca35beb5ea599ddc95824b3ab6c9c9a15adaaa6b3fd659`

## Run 2 (hash-chained)

- outdir: `run2/` (clean)
- exit: rc=0
- `evidence_run2.log` SHA256: `e335718a0074ca8797651689eaa0525ca7c0a5119fdb2985af76e7192663e753`
- chain: run 2's log is byte-identical to run 1's log, which carries SHA256
  `e335718a…fdb2985af76e7192663e753`; this entry binds run 2 to that digest.
- chunk images: all three byte-identical to run 1 (SHAs above).

## Byte-identity verdict

`sha256sum` equal on both evidence logs and on all three chunk images across
runs. A2 (prereg) SATISFIED.

## Evidence transcript (both runs)

```
KB-REPRO geometry CHUNK=4096 N=100 KLEN=8 TLEN=90 RECLEN=109
ingest nfiles=3 total=10900 recs=100 pad_per_rollover=63
census wrong_pre=0/37 wrong_post=63/63
walk_true_geometry parsed=100/100 bad=0
revise id=5 rc=0 rused_buggy=2708 rused_true=2834 undercount=126 new_off_recorded=10900
revise id=50 via recorded offset: REFUSED id_mismatch (fail closed)
verify id=5 new text at true_off=10900 OK
verify id=99 at true_off=10917 MISSING (header destroyed)
clobber first=2708 last=2833 count=125
verify id=98 tail damaged: yes (17 text bytes)
verdict D1=REPRODUCED D2=REPRODUCED
```

Note on `count=125` vs span 126: the clobber span is exactly the predicted
126 bytes `[2708,2834)`; one byte position (2719) coincidentally holds `0x6B`
('k') in both the old and new content, so 125 bytes differ. See ROOTCAUSE_A.md.
