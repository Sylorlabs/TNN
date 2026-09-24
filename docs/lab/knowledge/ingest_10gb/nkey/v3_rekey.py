#!/usr/bin/env python3
"""V3: honest BIG-offset re-key of kind-6 ~N chunk keys.
se:<site>:<q|a>:<id>~<n> -> se:<site>:<q|a>:<10^12 + id*10000 + n>
Injective while id < 10^12 and n < 10000. Provenance recoverable:
id = (k-10^12)//10000, n = (k-10^12)%10000.
Streaming: chunks buffered per (site,qa) group, flushed after the group's
genuine records (transformed keys sort after all genuine keys in group).
Usage: v3_rekey.py <in.dat> <out.dat>
"""
import struct, sys

BIG = 10**12
K = 10000

def xform(key: bytes):
    # returns (group, newkey) or (None, key) if not a kind-6 chunk key
    if not key.startswith(b"se:"):
        return None, key
    try:
        _, site, qa, rest = key.split(b":", 3)
    except ValueError:
        return None, key
    if qa not in (b"q", b"a") or b"~" not in rest:
        return None, key
    ids, ns = rest.split(b"~", 1)
    if not ids.isdigit() or not ns.isdigit():
        return None, key
    idi, ni = int(ids), int(ns)
    assert idi < BIG, f"id too big: {idi}"
    assert ni < K, f"chunk index too big: {ni}"
    newkey = b"se:" + site + b":" + qa + b":" + str(BIG + idi * K + ni).encode()
    assert len(newkey) <= 160
    return (site, qa), newkey

def main():
    inp, outp = sys.argv[1], sys.argv[2]
    n = nx = 0
    max_id = max_n = 0
    anomalies = 0
    cur_group = None
    buf = []  # (newkey, rec) for current group
    with open(inp, "rb") as f, open(outp, "wb") as o:
        while True:
            h = f.read(7)
            if len(h) < 7:
                break
            kind = h[0]
            klen, tlen = struct.unpack(">HI", h[1:7])
            key = f.read(klen); text = f.read(tlen)
            n += 1
            if kind == 6 and b"~" in key:
                group, newkey = xform(key)
                if group is None:
                    anomalies += 1
                    o.write(bytes([kind]) + h[1:7] + key + text)
                    continue
                if group != cur_group:
                    for nk, rec in sorted(buf):
                        o.write(rec)
                    buf = []
                    cur_group = group
                newrec = bytes([kind]) + struct.pack(">H", len(newkey)) + h[3:7] + newkey + text
                buf.append((newkey, newrec))
                nx += 1
                idi = int(key.rsplit(b":", 1)[1].split(b"~")[0])
                ni = int(key.rsplit(b"~", 1)[1])
                max_id = max(max_id, idi); max_n = max(max_n, ni)
            else:
                if cur_group is not None and not (kind == 6):
                    # kind changed away from 6: flush (groups are contiguous)
                    for nk, rec in sorted(buf):
                        o.write(rec)
                    buf = []
                    cur_group = None
                o.write(bytes([kind]) + h[1:7] + key + text)
        for nk, rec in sorted(buf):
            o.write(rec)
    print(f"total={n} rekeyed={nx} anomalies={anomalies} max_id={max_id} max_n={max_n}")

main()
