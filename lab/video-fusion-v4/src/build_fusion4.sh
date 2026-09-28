#!/bin/bash
# Assemble fusion4.zag from step-3 base + fz1-3 + v4a-e chunks, then compile.
set -e
cd ~/workspace/video-fusion-v4/src
head -1582 composer_base.zag > fusion4.zag
cat chunks/fz1.zag chunks/fz2.zag chunks/fz3.zag chunks/fz4.zag >> fusion4.zag
cat chunks/v4a.zag chunks/v4b.zag chunks/v4c.zag chunks/v4d.zag chunks/v4e.zag >> fusion4.zag
python3 - << 'PYEOF'
main = '''fn main() i32 {
    let a1:[]u8 = _zag_arg(1);
    if (_zag_strcmp(a1, "selftest") == 1) { return selftest(); }
    let a2:[]u8 = _zag_arg(2);
    let a3:[]u8 = _zag_arg(3);
    let a4:[]u8 = _zag_arg(4);
    let a5:[]u8 = _zag_arg(5);
    if (_zag_strcmp(a1, "ingest") == 1) {
        let rc:i64 = do_ingest(a2, a3, a4);
        _zag_print("ingest_rc=");
        _zag_println(_zag_i64_to_str(rc));
        if (rc == 0) { return 0; }
        return 1;
    }
    if (_zag_strcmp(a1, "recall") == 1) {
        let rc:i64 = do_recall(a2, a3);
        _zag_print("recall_rc=");
        _zag_println(_zag_i64_to_str(rc));
        if (rc == 0) { return 0; }
        return 1;
    }
    if (_zag_strcmp(a1, "fuse") == 1) {
        let rc:i64 = do_fuse(a2, a3, a4, a5);
        _zag_print("fuse_rc=");
        _zag_println(_zag_i64_to_str(rc));
        if (rc == 0) { return 0; }
        return 1;
    }
    if (_zag_strcmp(a1, "fuse4") == 1) {
        let rc:i64 = do_fuse4(a2, a3, a4, a5);
        _zag_print("fuse4_rc=");
        _zag_println(_zag_i64_to_str(rc));
        if (rc == 0) { return 0; }
        return 1;
    }
    _zag_println("usage: composer4 selftest | ingest|recall|fuse|fuse4 ...");
    return 99;
}
'''
open('fusion4.zag','a').write(main)
PYEOF
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 fusion4.zag -o fusion4_bin --no-analyze
echo "BUILD_OK"
