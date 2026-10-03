#!/usr/bin/env python3
"""Offline independent channel for the fork-D write-once evidence partition.

Deterministic for a fixed seed. Signs honest EXT atom lists into
signature-chained EXT partitions and emits genesis.zag (pinned genesis
public keys) for the pure-Zag verifier.

Scheme (frozen, AMENDMENT_01_PARTITION.md §2, seed handling per
AMENDMENT_02_SEED.md):
  WOTS w=16: 64 message nibbles + 3 checksum nibbles = 67 chains.
  sk(tag,idx,j) = SHA256(SEED || tag || idx_be4 || j_byte)
  tip(sk)       = SHA256^15(sk)
  pk(tag,idx)   = SHA256(tip_0 || ... || tip_66)
  m(tag,idx)    = SHA256(tag || atom || pknext_raw || prev_raw)
  sig_j         = SHA256^{15-d_j}(sk_j)
  prev_{i+1}    = SHA256(prev_raw || atom || pknext_raw || sig_raw)

The private SEED is EXTERNALLY HELD (Amendment 02): it is read from the
file named by the FORKD_CHANNEL_SEED environment variable, or from
~/.forkd_channel_seed. It is NEVER committed, embedded, or printed.
Signing commands refuse to run without it. Verification-only commands
(attest mirror, genpart, genesis emission of PUBLIC keys) need no seed.

Usage:
  channel.py sign <tag> <atoms.txt> <extpart>     # atoms: 5-field lines
  channel.py genpart <tag> <atoms.txt> <genpart>  # unsigned GEN partition
  channel.py genesis <tags...> > genesis.zag     # emit pinned genesis pins
  channel.py attest <tag> <extpart>               # verify (mirror, no seed)
"""
import hashlib
import os
import sys

NCHAINS = 67


def _load_seed() -> bytes:
    p = os.environ.get("FORKD_CHANNEL_SEED")
    if not p:
        p = os.path.expanduser("~/.forkd_channel_seed")
    with open(p, "rb") as f:
        seed = f.read().strip()
    if len(seed) < 16:
        raise SystemExit("channel seed too short (need >= 16 bytes)")
    return seed


_SEED = None


def SEED() -> bytes:
    global _SEED
    if _SEED is None:
        _SEED = _load_seed()
    return _SEED


def H(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()


def Hpow(b: bytes, n: int) -> bytes:
    for _ in range(n):
        b = H(b)
    return b


def sk(tag: str, idx: int, j: int) -> bytes:
    return H(SEED() + tag.encode() + idx.to_bytes(4, "big") + bytes([j]))


def tips(tag: str, idx: int):
    return [Hpow(sk(tag, idx, j), 15) for j in range(NCHAINS)]


def pk(tag: str, idx: int) -> bytes:
    return H(b"".join(tips(tag, idx)))


def digits_of(digest: bytes):
    ds = []
    for byte in digest:
        ds.append(byte >> 4)
        ds.append(byte & 15)
    cksum = sum(15 - d for d in ds)
    ds.append((cksum >> 8) & 15)
    ds.append((cksum >> 4) & 15)
    ds.append(cksum & 15)
    return ds


def sign_entry(tag: str, idx: int, atom: str, pknext: bytes, prev: bytes) -> bytes:
    m = H(tag.encode() + atom.encode() + pknext + prev)
    ds = digits_of(m)
    assert len(ds) == NCHAINS
    return b"".join(Hpow(sk(tag, idx, j), 15 - ds[j]) for j in range(NCHAINS))


def verify_entry(tag: str, idx: int, atom: str, pknext: bytes, prev: bytes,
                 sig: bytes, auth_pk: bytes) -> bool:
    """Mirror of the Zag verifier — kept in lockstep for cross-checking."""
    if len(sig) != NCHAINS * 32:
        return False
    m = H(tag.encode() + atom.encode() + pknext + prev)
    ds = digits_of(m)
    tps = []
    for j in range(NCHAINS):
        tps.append(Hpow(sig[j * 32:(j + 1) * 32], ds[j]))
    return H(b"".join(tps)) == auth_pk


def sign_partition(tag: str, atoms: list) -> list:
    """-> list of ENTRY lines (without header)."""
    lines = []
    prev = bytes(32)
    for idx, atom in enumerate(atoms):
        pknext = pk(tag, idx + 1)
        sig = sign_entry(tag, idx, atom, pknext, prev)
        q, s, pol, r, o = atom.split("|")
        lines.append(
            f"ENTRY|{tag}|{q}|{s}|{pol}|{r}|{o}|{prev.hex()}|{pknext.hex()}|{sig.hex()}")
        prev = H(prev + atom.encode() + pknext + sig)
    return lines, prev


def gen_partition(tag: str, atoms: list) -> list:
    lines = []
    prev = bytes(32)
    for atom in atoms:
        q, s, pol, r, o = atom.split("|")
        lines.append(f"GENENTRY|{tag}|{q}|{s}|{pol}|{r}|{o}|{prev.hex()}")
        prev = H(prev + atom.encode())
    return lines, prev


def attest_ext(tag: str, lines: list, genesis_pk: bytes):
    """Full re-verification (Python mirror of forkd2 attest)."""
    auth = genesis_pk
    prev = bytes(32)
    atoms = []
    for idx, ln in enumerate(lines):
        p = ln.split("|")
        if len(p) != 10 or p[0] != "ENTRY" or p[1] != tag:
            return False, f"entry {idx}: malformed"
        atom = "|".join(p[2:7])
        prev_h, pknext_h, sig_h = p[7], p[8], p[9]
        try:
            prev_b = bytes.fromhex(prev_h)
            pknext_b = bytes.fromhex(pknext_h)
            sig_b = bytes.fromhex(sig_h)
        except ValueError:
            return False, f"entry {idx}: bad hex"
        if prev_b != prev:
            return False, f"entry {idx}: prev mismatch"
        if not verify_entry(tag, idx, atom, pknext_b, prev_b, sig_b, auth):
            return False, f"entry {idx}: sig invalid"
        atoms.append(atom)
        prev = H(prev_b + atom.encode() + pknext_b + sig_b)
        auth = pknext_b
    return True, atoms


def main():
    cmd = sys.argv[1]
    if cmd == "keygen":
        tag = sys.argv[2]
        print(f"{tag} genesis pk: {pk(tag, 0).hex()}")
    elif cmd == "sign":
        tag, atoms_f, out_f = sys.argv[2], sys.argv[3], sys.argv[4]
        atoms = [l.strip() for l in open(atoms_f) if l.strip()]
        lines, tip = sign_partition(tag, atoms)
        with open(out_f, "w") as f:
            f.write(f"PART|{tag}|{len(lines)}\n")
            f.write("\n".join(lines) + "\n")
        ok, _ = attest_ext(tag, lines, pk(tag, 0))
        assert ok, "self-attestation failed"
        print(f"signed {len(lines)} entries tag={tag} tip={tip.hex()[:16]}..")
    elif cmd == "genpart":
        tag, atoms_f, out_f = sys.argv[2], sys.argv[3], sys.argv[4]
        atoms = [l.strip() for l in open(atoms_f) if l.strip()]
        lines, tip = gen_partition(tag, atoms)
        with open(out_f, "w") as f:
            f.write(f"PART|{tag}|gen|{len(lines)}\n")
            f.write("\n".join(lines) + "\n")
        print(f"gen partition {len(lines)} entries tag={tag}")
    elif cmd == "genesis":
        tags = sys.argv[2:]
        print("// genesis.zag — pinned genesis public keys, emitted by channel.py.")
        print("// DO NOT HAND-EDIT. Regenerate via: channel.py genesis <tags...>")
        for tag in tags:
            print(f"fn genesis_pk_{tag}()[]u8 {{")
            print(f"    return \"{pk(tag, 0).hex()}\";")
            print("}")
            print()
        print("fn genesis_lookup(tag:[]u8)[]u8 {")
        for tag in tags:
            print(f"    if(seq(tag,\"{tag}\")==1){{return genesis_pk_{tag}();}}")
        print("    return \"\";")
        print("}")
    elif cmd == "selftest":
        # WOTS round-trip + tamper detection, pure Python.
        tag = "selftest"
        atoms = ["UNIT|cat|POS|IS_A|mammal", "UNIT|mammal|POS|IS_A|animal"]
        lines, _ = sign_partition(tag, atoms)
        ok, _ = attest_ext(tag, lines, pk(tag, 0))
        assert ok, "round-trip failed"
        # tamper: flip one sig hex char
        p = lines[1].split("|")
        s = p[9]
        p[9] = ("0" if s[0] != "0" else "1") + s[1:]
        ok2, why = attest_ext(tag, [lines[0], "|".join(p)], pk(tag, 0))
        assert not ok2, "tampered sig verified!"
        # reorder
        ok3, _ = attest_ext(tag, [lines[1], lines[0]], pk(tag, 0))
        assert not ok3, "reordered chain verified!"
        # wrong-seed forgery
        SEED2 = b"attacker-seed"
        def sk2(idx, j):
            return H(SEED2 + tag.encode() + idx.to_bytes(4, "big") + bytes([j]))
        m = H(tag.encode() + atoms[0].encode() + pk(tag, 1) + bytes(32))
        ds = digits_of(m)
        forged = b"".join(Hpow(sk2(0, j), 15 - ds[j]) for j in range(NCHAINS))
        fl = f"ENTRY|{tag}|{'|'.join(atoms[0].split('|'))}|{'00'*32}|{pk(tag,1).hex()}|{forged.hex()}"
        ok4, _ = attest_ext(tag, [fl], pk(tag, 0))
        assert not ok4, "forged entry verified!"
        print("channel selftest: round-trip OK; sig-flip, reorder, forgery all rejected")
    else:
        sys.exit(f"unknown cmd {cmd}")


if __name__ == "__main__":
    main()
