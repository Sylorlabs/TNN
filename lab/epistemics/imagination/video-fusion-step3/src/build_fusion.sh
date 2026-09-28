#!/bin/bash
# Assemble fusion.zag from step-2 base + fusion organ chunks, then compile.
set -e
cd ~/workspace/video-fusion/src
head -1582 composer_base.zag > fusion.zag
cat chunks/fz1.zag chunks/fz2.zag chunks/fz3.zag chunks/fz4.zag >> fusion.zag
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
    if (_zag_strcmp(a1, "stillingest") == 1) {
        let rc:i64 = do_stillingest(a2, a3, a4);
        _zag_print("stillingest_rc=");
        _zag_println(_zag_i64_to_str(rc));
        if (rc == 0) { return 0; }
        return 1;
    }
    if (_zag_strcmp(a1, "stillrecall") == 1) {
        let rc:i64 = do_stillrecall(a2, a3);
        _zag_print("stillrecall_rc=");
        _zag_println(_zag_i64_to_str(rc));
        if (rc == 0) { return 0; }
        return 1;
    }
    if (_zag_strcmp(a1, "compose") == 1) {
        let rc:i64 = do_compose(a2, a3, a4, a5);
        _zag_print("compose_rc=");
        _zag_println(_zag_i64_to_str(rc));
        if (rc == 0) { return 0; }
        return 1;
    }
    if (_zag_strcmp(a1, "render") == 1) {
        let rc:i64 = do_render(a2, a3, parse_i64(a4), a5);
        _zag_print("render_rc=");
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
    _zag_println("usage: composer selftest | ingest|recall|stillingest|stillrecall|compose|render|fuse ...");
    return 99;
}
'''
open('fusion.zag','a').write(main)
PYEOF
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 fusion.zag -o fusion_bin --no-analyze
echo "BUILD_OK"
