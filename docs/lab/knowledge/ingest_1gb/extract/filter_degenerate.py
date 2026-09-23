#!/usr/bin/env python3
"""One-time remediation filter for wikt.bin (legacy 5M-page portion).

Removes records the frozen CAL/G3 gate can never accept, emitted by the
pre-fix wikt extractor (see PREREG_GAPS.md Gap 2):
  - kind 1 with len(text) < 4  (degenerate senses, e.g. text ".")
  - kind 2 whose key has an empty word segment after "wikt:en:"
    (ig_key_word wl<1 -> G3 reject)

The fixed extractor (wikt_slow.py parse_page) skips these at emission; this
filter cleans the portion extracted before the fix. Deterministic: record
order preserved, drops only.

Usage: filter_degenerate.py <in.bin> <out.bin>
Prints counts and SHA256 of the output.
"""
import struct, sys, hashlib

def main():
    inp, outp = sys.argv[1], sys.argv[2]
    with open(inp, "rb") as f:
        data = f.read()
    p, n = 0, len(data)
    kept, drop_k1, drop_k2 = 0, 0, 0
    h = hashlib.sha256()
    with open(outp, "wb") as out:
        while p < n:
            kind = data[p]
            klen = struct.unpack(">H", data[p+1:p+3])[0]
            tlen = struct.unpack(">I", data[p+3:p+7])[0]
            rec = data[p:p+7+klen+tlen]
            key = data[p+7:p+7+klen]
            drop = False
            if kind == 1 and tlen < 4:
                drop, drop_k1 = True, drop_k1 + 1
            elif kind == 2:
                ks = key.decode("utf-8", "replace")
                if ks.startswith("wikt:en:"):
                    ci = ks.find(":", 8)
                    if ci < 0 or ci == 8:
                        drop, drop_k2 = True, drop_k2 + 1
            if drop:
                pass
            else:
                out.write(rec)
                h.update(rec)
                kept += 1
            p += 7 + klen + tlen
    assert p == n, "truncated record at end of input"
    print(f"kept={kept} dropped_k1_short={drop_k1} dropped_k2_badkey={drop_k2}")
    print(f"sha256={h.hexdigest()}")

if __name__ == "__main__":
    main()
