#!/usr/bin/env python3
"""R-35 repair: apply the full-64-bit tag binding to hpam3536_probe.zag.

Reads the ORIGINAL probe (b20ae9edf87da4aa...), applies exact string
replacements (auditable diff), writes hpam3536_r35.zag. Fails loudly if any
replacement target is not found exactly once.
"""
import sys

SRC = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/round_c/probe3536/hpam3536_probe.zag"
DST = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/r35/hpam3536_r35.zag"

with open(SRC) as f:
    s = f.read()

def sub_once(old, new):
    global s
    n = s.count(old)
    if n != 1:
        sys.exit(f"FATAL: pattern found {n}x (want 1): {old[:80]!r}")
    s = s.replace(old, new, 1)

# 1. header comment: record the repair
sub_once(
    "// hpam3536_probe.zag — Round-C cheap probes for H-PAM-35 and H-PAM-36.",
    "// hpam3536_r35.zag — R-35 REPAIR of hpam3536_probe.zag (b20ae9edf87da4aa).\n"
    "// Repair vs J-35: the capability tag now binds the FULL 64 bits of every\n"
    "// i64 field (put64i) at every mode-35 sink. Mode-36 paths untouched.\n"
    "// hpam3536_probe.zag — Round-C cheap probes for H-PAM-35 and H-PAM-36.",
)

# 2. add put64i after put32i
sub_once(
    """fn put32i(bs:[]u8, o:i32, v:i64) void {
    bs[o] = (v % 256) as u8;
    bs[o+1] = ((v / 256) % 256) as u8;
    bs[o+2] = ((v / 65536) % 256) as u8;
    bs[o+3] = ((v / 16777216) % 256) as u8;
    return;
}""",
    """fn put32i(bs:[]u8, o:i32, v:i64) void {
    bs[o] = (v % 256) as u8;
    bs[o+1] = ((v / 256) % 256) as u8;
    bs[o+2] = ((v / 65536) % 256) as u8;
    bs[o+3] = ((v / 16777216) % 256) as u8;
    return;
}
// R-35: full 64-bit LE decomposition of an i64 (proven put32i style:
// u8 arena + repeated % 256 / / 256; mint and verify use the same fn so
// binding is self-consistent by construction)
fn put64i(bs:[]u8, o:i32, v:i64) void {
    let k:i64 = v;
    let b:i32 = 0;
    while(b < 8) {
        bs[o + b] = (k % 256) as u8;
        k = k / 256;
        b = b + 1;
    }
    return;
}""",
)

# 3. tag_half: bind full 64 bits of every field (48-byte preimage)
sub_once(
    """// one half of the capability tag over content bytes || verdict || CAP || dom
fn tag_half(bs:[]u8, id:i64, conf:i64, meas:i64, label:i64, verdict:i64, cap:i64, dom:u8) u64 {
    put32i(bs, 0, id);
    put32i(bs, 4, conf);
    put32i(bs, 8, meas);
    put32i(bs, 12, label);
    put32i(bs, 16, verdict);
    put32i(bs, 20, cap);
    return fnv32(bs, 24, dom);
}""",
    """// R-35: one half of the capability tag over FULL-64 content bytes || verdict
// || CAP || dom (was: low-32 only via put32i — the J-35 hole)
fn tag_half(bs:[]u8, id:i64, conf:i64, meas:i64, label:i64, verdict:i64, cap:i64, dom:u8) u64 {
    put64i(bs, 0, id);
    put64i(bs, 8, conf);
    put64i(bs, 16, meas);
    put64i(bs, 24, label);
    put64i(bs, 32, verdict);
    put64i(bs, 40, cap);
    return fnv32(bs, 48, dom);
}""",
)

# 4. vec_tag_half (IF3 sink): full 64 bits (40-byte preimage)
sub_once(
    """fn vec_tag_half(bs:[]u8, v0:i64, v1:i64, v2:i64, v3:i64, cap:i64, dom:u8) u64 {
    put32i(bs, 0, v0);
    put32i(bs, 4, v1);
    put32i(bs, 8, v2);
    put32i(bs, 12, v3);
    put32i(bs, 16, cap);
    return fnv32(bs, 20, dom);
}""",
    """// R-35: full-64 binding for the IF3 vector sink
fn vec_tag_half(bs:[]u8, v0:i64, v1:i64, v2:i64, v3:i64, cap:i64, dom:u8) u64 {
    put64i(bs, 0, v0);
    put64i(bs, 8, v1);
    put64i(bs, 16, v2);
    put64i(bs, 24, v3);
    put64i(bs, 32, cap);
    return fnv32(bs, 40, dom);
}""",
)

# 5. premise_keyed (IF4 sink): full 64 bits (24-byte preimage)
sub_once(
    """fn premise_keyed(k:HighKey, bs:[]u8) i32 {
    put32i(bs, 0, k.k0);
    put32i(bs, 4, k.k1);
    put32i(bs, 8, 2654435769);
    let th:u64 = fnv32(bs, 12, 27);
    if(k.taghi != th) { return 0; }
    put32i(bs, 8, 2135587861);
    let tl:u64 = fnv32(bs, 12, 28);
    if(k.taglo != tl) { return 0; }
    return 1;
}""",
    """// R-35: full-64 binding for the IF4 keyed-premise sink
fn premise_keyed(k:HighKey, bs:[]u8) i32 {
    put64i(bs, 0, k.k0);
    put64i(bs, 8, k.k1);
    put64i(bs, 16, 2654435769);
    let th:u64 = fnv32(bs, 24, 27);
    if(k.taghi != th) { return 0; }
    put64i(bs, 16, 2135587861);
    let tl:u64 = fnv32(bs, 24, 28);
    if(k.taglo != tl) { return 0; }
    return 1;
}""",
)

# 6. m35 scratch buffer 32 -> 64 bytes (largest preimage is 48)
sub_once("let bs:[]u8 = nio_alloc(32);", "let bs:[]u8 = nio_alloc(64); // R-35: 48-byte preimages need 64")

with open(DST, "w") as f:
    f.write(s)
print("wrote", DST)
