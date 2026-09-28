#!/usr/bin/env python3
"""verify_hints_tape.py — W3 arm-4 TST-1 tape verifier (frozen PREREG_FREEZE.md §4, B.1/B.4).
Asserts, from the tape alone:
  - framing: [u8 type][u32 le len][payload], event sequence [1,2,5*N,9]
  - header: magic 'TST1', version 1, arm_id 4, prereg_hash == pinned freeze sha256
  - NO type-3 TEACHER_MSG events anywhere (arm 4 emits HINT only; no §P)
  - HINT payload decodes: u8 region_count==1, u64 start, u64 end, u8 flags in {0,1}
  - start < end, region within stimulus bounds, region != any GT unit span (never a word)
  - tape chain: chain_{n+1} = sha256(chain_n || etype || len_le32 || payload),
    seed 32 zero bytes; footer chain matches; footer event_count matches
Exit 0 on PASS, nonzero with the failed assertion otherwise.
"""
import hashlib, struct, sys

PINNED_FREEZE = bytes.fromhex(
    "c7a9d57e3ac4d8ff48f4396c47eec9fedbfacb894584a31779a91a64deeef879")
GT_UTILS = []  # (start,end,util) loaded from the gt file when --gt given

def load_gt(path):
    units = []
    stim_len = None
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            p = line.split()
            if p[0] == 'GT1':
                stim_len = int(p[1])
            elif p[0] == 'U':
                units.append((int(p[1]), int(p[2]), int(p[3])))
    return stim_len, units

def frames(path):
    t = open(path, 'rb').read()
    out, off = [], 0
    while off < len(t):
        etype = t[off]
        ln = struct.unpack('<I', t[off+1:off+5])[0]
        pay = t[off+5:off+5+ln]
        assert len(pay) == ln, f"truncated payload at frame {len(out)}"
        out.append((etype, ln, pay))
        off += 5 + ln
    return out

def main():
    tape, gt = sys.argv[1], sys.argv[2]
    stim_len, units = load_gt(gt)
    fr = frames(tape)
    fails = []
    def chk(name, cond, detail=""):
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")
        if not cond:
            fails.append(name)

    types = [e for e, _, _ in fr]
    chk("t4.tape.nonempty", len(fr) >= 4, f"frames={len(fr)}")
    chk("t4.tape.event_sequence",
        types[0] == 1 and types[1] == 2 and types[-1] == 9 and
        all(t == 5 for t in types[2:-1]) and len(types) > 3,
        f"types={types}")
    chk("t4.tape.no_teacher_msg", 3 not in types, "no type-3 TEACHER_MSG")

    # header
    pay = fr[0][2]
    magic = pay[0:4]; ver = struct.unpack('<H', pay[4:6])[0]
    sess = struct.unpack('<Q', pay[6:14])[0]
    arm = struct.unpack('<I', pay[14:18])[0]
    pr = pay[22:54]
    chk("t4.header.magic", magic == b"TST1", magic.hex())
    chk("t4.header.version", ver == 1, f"v={ver}")
    chk("t4.header.arm_id", arm == 4, f"arm={arm}")
    chk("t4.header.prereg_hash_pinned", pr == PINNED_FREEZE, pr.hex())
    chk("t4.header.session_id", sess == 1, f"session={sess}")

    # stimulus ref
    pay2 = fr[1][2]
    r0 = struct.unpack('<Q', pay2[8:16])[0]; r1 = struct.unpack('<Q', pay2[16:24])[0]
    chk("t4.stimulus.bounds", r0 == 0 and r1 == stim_len, f"[{r0},{r1}) stim_len={stim_len}")

    # hints
    nhints = 0
    unit_spans = {(s, e) for s, e, _ in units}
    for i, (etype, ln, p) in enumerate(fr):
        if etype != 5:
            continue
        nhints += 1
        rc = p[0]; s = struct.unpack('<Q', p[1:9])[0]; e = struct.unpack('<Q', p[9:17])[0]
        fl = p[17]
        chk(f"t4.hint[{nhints}].wire_len", ln == 18, f"len={ln}")
        chk(f"t4.hint[{nhints}].region_count", rc == 1, f"rc={rc}")
        chk(f"t4.hint[{nhints}].ordered_bounds", s < e, f"[{s},{e})")
        chk(f"t4.hint[{nhints}].within_stimulus", e <= stim_len, f"end={e} stim={stim_len}")
        chk(f"t4.hint[{nhints}].flags", fl in (0, 1), f"flags={fl}")
        chk(f"t4.hint[{nhints}].never_a_word", (s, e) not in unit_spans, f"[{s},{e})")
    chk("t4.hints.count_bounded", 0 < nhints <= 16, f"nhints={nhints}")

    # chain + footer: footer chain covers all frames except the footer itself;
    # footer layout: u64 final_memory_hash @0, 32-byte chain @8, u64 event_count @40
    chain = bytes(32)
    for etype, ln, p in fr[:-1]:
        raw = bytes([etype]) + struct.pack('<I', ln) + p
        chain = hashlib.sha256(chain + raw).digest()
    fpay = fr[-1][2]
    fchain = fpay[8:40]
    fcount = struct.unpack('<Q', fpay[40:48])[0]
    chk("t4.chain.recomputed", fchain == chain, fchain.hex()[:16] + "...")
    chk("t4.footer.event_count", fcount == len(fr) - 1, f"count={fcount} frames={len(fr)}")

    print("T345_RESULT," + ("PASS" if not fails else "FAIL") + f",fails={len(fails)}")
    return 1 if fails else 0

if __name__ == "__main__":
    sys.exit(main())
