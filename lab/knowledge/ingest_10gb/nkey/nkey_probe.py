#!/usr/bin/env python3
"""Instrument the ~N chunk-key rejection: classify every tilde-keyed record
in dryrun_facts.dat and predict what each resolution variant would do.
Pure analysis - reads only, zero writes to the corpus.
"""
import struct, sys

FACTS = "/home/hatch/workspace/scratch_10gb_work/dryrun/dryrun_facts.dat"

def se_key_ok_current(key: bytes) -> bool:
    """Mirror of ig_se_key_ok (gate.zag:579): digits only after post id."""
    if len(key) < 8: return False
    if key[:3] != b"se:": return False
    i = 3
    while i < len(key) and key[i] != 58: i += 1
    if i <= 3: return False
    if i + 3 >= len(key): return False
    if key[i+1] not in (113, 97): return False
    if key[i+2] != 58: return False
    j = i + 3
    while j < len(key):
        if key[j] < 48 or key[j] > 57: return False
        j += 1
    return True

def se_key_ok_admit_tilde(key: bytes) -> bool:
    """Variant B: allow a single ~N suffix (N = 1+ digits) after the post id."""
    if len(key) < 8: return False
    if key[:3] != b"se:": return False
    i = 3
    while i < len(key) and key[i] != 58: i += 1
    if i <= 3: return False
    if i + 3 >= len(key): return False
    if key[i+1] not in (113, 97): return False
    if key[i+2] != 58: return False
    j = i + 3
    # digits, then optional ~digits tail
    while j < len(key) and 48 <= key[j] <= 57: j += 1
    if j == i + 3: return False  # need >=1 digit of post id
    if j == len(key): return True  # plain numeric id
    if key[j] != 126: return False  # '~'
    j += 1
    k = j
    while k < len(key) and 48 <= key[k] <= 57: k += 1
    return k > j and k == len(key)

def is_q(key: bytes) -> bool:
    i = 3
    while i < len(key) and key[i] != 58: i += 1
    return key[i+1] == 113

def g1_ok(key: bytes, text: bytes) -> bool:
    if not (1 <= len(key) <= 160): return False
    if not (20 <= len(text) <= 4096): return False
    if any(c < 32 or c == 127 or c == 10 for c in key): return False
    if b"\x00" in text: return False
    if any(c < 32 and c != 10 or c == 127 for c in text): return False
    return True

def main():
    n_total = 0
    tilde_recs = []  # (idx, kind, key, text)
    per_kind = {}
    per_site = {}
    with open(FACTS, "rb") as f:
        idx = 0
        while True:
            h = f.read(7)
            if len(h) < 7: break
            kind = h[0]
            klen, tlen = struct.unpack(">HI", h[1:7])
            key = f.read(klen); text = f.read(tlen)
            n_total += 1
            if b"~" in key:
                tilde_recs.append((idx, kind, key, text))
                per_kind[kind] = per_kind.get(kind, 0) + 1
                # site = between 2nd and 3rd colon
                try:
                    site = key.split(b":")[1]
                    per_site[site] = per_site.get(site, 0) + 1
                except Exception:
                    per_site[b"?"] = per_site.get(b"?", 0) + 1
            idx += 1
    print(f"total_records={n_total} tilde_keyed={len(tilde_recs)}")
    print(f"tilde per kind: {per_kind}")
    print(f"tilde per site (top): {sorted(per_site.items(), key=lambda x:-x[1])[:12]}")
    # classify under variant B admission
    b_would_install = 0
    b_q_nonnsep = 0   # question chunks that would still fail G3 (no \n\n)
    b_g1_fail = 0
    b_bad_shape = 0   # tilde key not matching ~N shape
    max_chunk = 0
    for idx, kind, key, text in tilde_recs:
        if kind != 6:
            continue
        if not se_key_ok_admit_tilde(key):
            b_bad_shape += 1
            continue
        if not g1_ok(key, text):
            b_g1_fail += 1
            continue
        if is_q(key) and b"\n\n" not in text:
            b_q_nonnsep += 1
            continue
        b_would_install += 1
        # chunk number
        try:
            m = int(key.rsplit(b"~", 1)[1])
            if m > max_chunk: max_chunk = m
        except Exception:
            pass
    n6 = per_kind.get(6, 0)
    print(f"kind6 tilde: {n6}")
    print(f"  variantB would install: {b_would_install}")
    print(f"  variantB still G3 (question chunk, no \\n\\n): {b_q_nonnsep}")
    print(f"  variantB G1 fail: {b_g1_fail}")
    print(f"  tilde key bad shape (not ~N): {b_bad_shape}")
    print(f"  max chunk index seen: {max_chunk}")
    # sanity: every tilde key currently fails ig_se_key_ok?
    cur_fail = sum(1 for _, k6, key, _ in tilde_recs if k6 == 6 and not se_key_ok_current(key))
    print(f"kind6 tilde keys failing CURRENT ig_se_key_ok: {cur_fail} / {n6}")
    # non-kind6 tilde keys: what are they?
    other = [(k, key[:40]) for _, k, key, _ in tilde_recs if k != 6][:10]
    print(f"non-kind6 tilde sample: {other}")

main()
