#!/usr/bin/env python3
"""Verify E1 retrieval: every key in eval_keys.bin must be found by bquery
with status 0 and byte-identical text to facts.bin.
Memory-efficient: retains only the 1,000 requested keys from facts.bin.

Usage: verify_e1.py <facts.bin> <eval_keys.bin> <eval_res.bin>
bquery result record: [1B status][4B id LE][4B text_len LE][text]
eval_keys record: [2B key_len BE][key]
facts record: [1B kind][2B key_len BE][4B text_len BE][key][text]
"""
import struct, sys

def main():
    facts_p, keys_p, res_p = sys.argv[1], sys.argv[2], sys.argv[3]

    # Load the 1,000 eval keys first.
    want = set()
    keys = []
    with open(keys_p, "rb") as f:
        while True:
            h = f.read(2)
            if len(h) < 2:
                break
            kl = struct.unpack(">H", h)[0]
            k = f.read(kl)
            keys.append(k)
            want.add(k)
    print(f"eval keys: {len(keys)}", flush=True)

    # Scan facts.bin, retaining only wanted keys (facts.bin is sorted;
    # first occurrence wins, matching merge keep-first).
    facts = {}
    with open(facts_p, "rb") as f:
        while want:
            hdr = f.read(7)
            if len(hdr) < 7:
                break
            klen = struct.unpack(">H", hdr[1:3])[0]
            tlen = struct.unpack(">I", hdr[3:7])[0]
            key = f.read(klen)
            if key in want:
                facts[key] = f.read(tlen)
                want.discard(key)
            else:
                f.seek(tlen, 1)
    print(f"facts retained: {len(facts)}", flush=True)

    n_ok = n_found = n_textmatch = 0
    fails = []
    with open(res_p, "rb") as f:
        for i, key in enumerate(keys):
            hdr = f.read(9)
            if len(hdr) < 9:
                fails.append((i, key, "truncated result"))
                break
            status = hdr[0]
            rid = struct.unpack("<i", hdr[1:5])[0]
            tl = struct.unpack("<I", hdr[5:9])[0]
            text = f.read(tl) if tl else b""
            if status == 0:
                n_found += 1
                if key in facts and facts[key] == text:
                    n_textmatch += 1
                    n_ok += 1
                else:
                    fails.append((i, key, "text mismatch"))
            else:
                fails.append((i, key, f"status={status}"))
    print(f"E1: {n_ok}/{len(keys)} full pass "
          f"(found={n_found}, text_match={n_textmatch})")
    for i, k, why in fails[:10]:
        print(f"  FAIL key#{i} {k[:60]!r}: {why}")
    if fails:
        raise SystemExit(f"E1 FAILED: {len(fails)} failures")
    print("E1 PASS")

if __name__ == "__main__":
    main()
