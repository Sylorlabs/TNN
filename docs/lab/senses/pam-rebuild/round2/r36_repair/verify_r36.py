#!/usr/bin/env python3
"""Independent verification of the R-36 M-36 retest outcome.

1. Recompute seed = SHA256(transcript) in Python; must match the probe's
   r36_seed_hex for both modes (validates the Zag ns_sha256 path).
2. Reimplement the FNV/wstep/honest_* mechanism in Python; recompute the
   attacker's offline chain (seed 305419896/2596069104) and the harness chain
   (transcript seed); count expected installs. Must be 0/120.
"""
import hashlib

PREREG_SHA = "506fc0927100e76b3d1c00874dfe42239c6bef63"
MATERIAL = "bd1b7914f731ac24c0823828702f642ef45807fe90b230f81fe13444f554ee73"

M32 = 0xFFFFFFFF


def transcript(mode):
    t = b"R36.SEED.v1\x00" + PREREG_SHA.encode() + b"\x00" + mode.encode() \
        + b"\x00" + b"120\x00" + MATERIAL.encode() + b"\x00"
    return t


def fnv32(bs, dom):
    h = 2166136261
    h = ((h ^ dom) * 16777619) & M32
    for b in bs:
        h = ((h ^ b) * 16777619) & M32
    return h


def put32u(bs, o, v):
    v &= M32
    bs[o] = v & 0xFF
    bs[o + 1] = (v >> 8) & 0xFF
    bs[o + 2] = (v >> 16) & 0xFF
    bs[o + 3] = (v >> 24) & 0xFF


def wstep(whi, wlo, dom):
    bs = bytearray(16)
    put32u(bs, 0, whi)
    put32u(bs, 4, wlo)
    put32u(bs, 8, 608135816)
    put32u(bs, 12, 2242054355)
    return fnv32(bs, dom)


def honest_wc(whi, wlo):
    m = 2001
    p32 = 4294967296 % m
    r = (((whi % m) * (p32 % m)) + (wlo % m)) % m
    return 700 + r


def honest_wm(whi, wlo):
    wmid = (whi * 2048) + (wlo // 2097152)
    return wmid % 100001


# 1. seed check
for mode, expect in (("batt", "5b5a7f647a81704deadcef33323fdd4dba313ab9f9f5fefa8dd0df4be662c1c4"),
                     ("m36", "5059e67abcaee33f511bfb70a5c1d165797aeacd35284935771fa558253f40f6")):
    d = hashlib.sha256(transcript(mode)).digest()
    got = d.hex()
    print(f"mode={mode} python_seed={got}")
    assert got == expect, f"SEED MISMATCH for {mode}"
print("seed derivation: Python SHA256 matches probe ns_sha256 for both modes")

# 2. M-36 outcome check
d = hashlib.sha256(transcript("m36")).digest()
shi = int.from_bytes(d[0:8], "little")
slo = int.from_bytes(d[8:16], "little")

awhi, awlo = 305419896, 2596069104
A = []
t = 0
while t < 120:
    A.append((awhi, awlo))
    awhi, awlo = wstep(awhi, awlo, 1), wstep(awhi, awlo, 2)
    t += 1

hwhi, hwlo = shi, slo
installs = 0
t = 0
while t < 120:
    tw, tl = A[t]
    conf, meas = honest_wc(tw, tl), honest_wm(tw, tl)
    wc, wm = honest_wc(hwhi, hwlo), honest_wm(hwhi, hwlo)
    if abs(conf - wc) <= 5 and abs(meas - wm) <= 20:
        installs += 1
        print(f"  trial {t}: INSTALL (unexpected)")
    hwhi, hwlo = wstep(hwhi, hwlo, 1), wstep(hwhi, hwlo, 2)
    t += 1
print(f"python-expected m36 installs: {installs}/120")
assert installs == 0, "expected 0 installs"
print("M-36 retest outcome independently confirmed: 0/120 (attacker chain targets the wrong world)")
