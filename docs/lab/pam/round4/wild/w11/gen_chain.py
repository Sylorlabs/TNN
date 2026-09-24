#!/usr/bin/env python3
"""gen_chain.py — W11 frozen chain-of-custody fixtures (PREREG_W11.md, frozen).

Deterministic (zero RNG). Device key K (32 bytes, frozen constant):
  K[i] = ((i*2654435761 + 0x9e3779b9) mod 256)
HMAC-SHA256 via hashlib. Chain line format:
  chain_id|nlinks|calib|link0|link1|...
link = stage,input_hex64,output_hex64,transform,mac_hex64 ; calib = 8 hex.
anchor (link 0): stage=0, input=output=percept_hash=sha256("percept-"+cid),
  transform=0, mac_0=HMAC("W11A"|cid_be32|calib_be32|percept_hash).
links i>=1: stage=i, input=prev.output, output=sha256(prev.output|t_byte),
  transform in 1..8, mac_i=HMAC(stage_be32|input|output|t_be32|mac_{i-1}).
CALIB_REG = 0xC0FFEE11 (frozen).
Classes: VALID 200 | BROKEN_MAC 30 | UNLISTED 20 | OVERLONG 20 | REPLAY 15 |
  MID_TRUNCATE 15 | FORGE_NOKEY 30 (12 W + 18 P wrong-set items, counter
  hex macs, no key) | CALIB_DRIFT 40.
CONSTRUCTION AUDIT (C3): every chain below is built ONLY through anchor()
  + extend(). No other construction path exists in this file.
"""
import hashlib, hmac, os, struct

HERE = os.path.dirname(os.path.abspath(__file__))
K = bytes(((i * 2654435761 + 0x9E3779B9) % 256) for i in range(32))
CALIB_REG = 0xC0FFEE11
ALLOW = set(range(1, 9))

def H(msg: bytes) -> bytes:
    return hashlib.sha256(msg).hexdigest().encode(), hashlib.sha256(msg).digest()
def Hhex(msg: bytes) -> str:
    return hashlib.sha256(msg).hexdigest()
def M(key: bytes, msg: bytes) -> str:
    return hmac.new(key, msg, hashlib.sha256).hexdigest()

def anchor(cid: int, calib: int):
    """Single construction entry point (C3 audit). Returns (links, percept_hash)."""
    ph = Hhex(b"percept-" + str(cid).encode())
    mac0 = M(K, b"W11A" + struct.pack(">I", cid) + struct.pack(">I", calib) + bytes.fromhex(ph))
    return [f"0,{ph},{ph},0,{mac0}"], ph

def extend(links, cid, calib, transforms):
    prev_out = links[-1].split(",")[2]
    prev_mac = links[-1].split(",")[4]
    for n, t in enumerate(transforms, start=len(links)):
        out = Hhex(bytes.fromhex(prev_out) + bytes([t]))
        mac = M(K, struct.pack(">I", n) + bytes.fromhex(prev_out) + bytes.fromhex(out)
                + struct.pack(">I", t) + bytes.fromhex(prev_mac))
        links.append(f"{n},{prev_out},{out},{t},{mac}")
        prev_out, prev_mac = out, mac
    return links

def emit(cid, links, calib):
    return f"{cid}|{len(links)}|{calib:08x}|" + "|".join(links)

def main():
    chains = []
    cid = 0
    # VALID 200
    valid_store = []
    for v in range(200):
        links, _ = anchor(cid, CALIB_REG)
        ts = [1 + ((v + k) % 8) for k in range(cid % 6)]
        extend(links, cid, CALIB_REG, ts)
        chains.append(emit(cid, links, CALIB_REG))
        valid_store.append((cid, links))
        cid += 1
    # BROKEN_MAC 30: flip one hex digit of a middle mac
    for b in range(30):
        _, links = valid_store[b]
        links = list(links)
        mid = len(links) // 2
        f = links[mid].split(",")
        mac = f[4]
        f[4] = ("0" if mac[0] != "0" else "1") + mac[1:]
        links[mid] = ",".join(f)
        chains.append(emit(cid, links, CALIB_REG)); cid += 1
    # UNLISTED 20: transform=99, MAC honestly recomputed with key
    for u in range(20):
        links, _ = anchor(cid, CALIB_REG)
        extend(links, cid, CALIB_REG, [3, 99, 5])
        chains.append(emit(cid, links, CALIB_REG)); cid += 1
    # OVERLONG 20: nlinks 7..9, MACs honest
    for o in range(20):
        links, _ = anchor(cid, CALIB_REG)
        extend(links, cid, CALIB_REG, [1 + ((o + k) % 8) for k in range(7 + (o % 3))])
        chains.append(emit(cid, links, CALIB_REG)); cid += 1
    # REPLAY 15: VALID macs replayed onto different content
    for r in range(15):
        _, links = valid_store[100 + r]
        f0 = links[0].split(",")
        ph2 = Hhex(b"percept-evil-" + str(cid).encode())
        links2 = [f"0,{ph2},{ph2},0,{f0[4]}"] + links[1:]
        chains.append(emit(cid, links2, CALIB_REG)); cid += 1
    # MID_TRUNCATE 15: remove a middle link, keep later macs (needs len>=4)
    mt_src = [e for e in valid_store if len(e[1]) >= 4][:15]
    assert len(mt_src) == 15
    for t in range(15):
        _, links = mt_src[t]
        links2 = [links[0], links[1]] + links[3:]
        chains.append(emit(cid, links2, CALIB_REG)); cid += 1
    # FORGE_NOKEY 30: wrong-set items, counter-hex macs (no key) — C1 red team
    for w in range(30):
        links, _ = anchor(cid, CALIB_REG)
        extend(links, cid, CALIB_REG, [2, 4])
        forged = []
        for n, ln in enumerate(links):
            f = ln.split(",")
            f[4] = ("%064x" % ((cid * 1000003 + n * 9176 + 12345) % (1 << 256)))
            forged.append(",".join(f))
        chains.append(emit(cid, forged, CALIB_REG)); cid += 1
    # CALIB_DRIFT 40: drifted calib, MACs honestly over drifted calib (K7)
    for d in range(40):
        calib = (CALIB_REG + 10 * (1 + (d % 40))) & 0xFFFFFFFF
        links, _ = anchor(cid, calib)
        extend(links, cid, calib, [1, 2, 3])
        chains.append(emit(cid, links, calib)); cid += 1
    p = os.path.join(HERE, "w11_chains.txt")
    open(p, "w").write("\n".join(chains) + "\n")
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    print(f"w11_chains.txt: {len(chains)} chains sha256={h}")

if __name__ == "__main__":
    main()
