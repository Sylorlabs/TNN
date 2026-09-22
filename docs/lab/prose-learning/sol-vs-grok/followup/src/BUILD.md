# Build note — followup sources

The four followup contenders are new files in this directory:
`sg_verify.zag`, `sg_coref1.zag`, `sg_coref2.zag`, `sg_gated.zag`.

Each does `@import("sg_parse.zag")`, which the znc toolchain resolves
relative to the CURRENT WORKING DIRECTORY (not the source file). To build,
mirror the duel's frozen layout into this directory first:

    cd prose-learning/sol-vs-grok/followup/src
    cp ../../sg_parse.zag ../../R33_NATIVE_SHA256_V2.zag \
       ../../R33_NATIVE_IO_V1.zag .
    cp ../../src/sg_sol.zag ../../src/sg_grok.zag .
    ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
    for s in sg_verify sg_coref1 sg_coref2 sg_gated sg_sol sg_grok; do
        $ZNC build $s.zag -o /path/to/$s
    done

`sg_parse.zag`, `R33_NATIVE_*.zag`, `sg_sol.zag`, `sg_grok.zag` are
byte-identical to the duel's frozen files (verified at freeze time) and are
not duplicated in this commit. `followup/gen/` likewise reuses the duel's
`gen/battery.py`, `gen/check_sg.py`, `gen/score_sg.py`, `gen/validate_sg.zag`
unchanged; only `cfg_followup.py`, `mk_followup.py`, `score_fup.py` are new.
