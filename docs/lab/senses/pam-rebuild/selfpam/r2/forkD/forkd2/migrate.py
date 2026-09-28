#!/usr/bin/env python3
"""Migrate fork-D label-based corpora to write-once partitions.

For each corpus: split store.txt into EXT/GEN atom lists (labels STRIPPED —
the partition is the provenance now), sign the EXT list with the channel,
chain the GEN list, rewrite the manifest as manifest2
(case|draft|extpart|genpart|delib|expected). Copies drafts/ and delib/.

Deterministic. No RNG.
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from channel import sign_partition, gen_partition, H, pk

FORKD = os.path.expanduser("~/workspace/tnn-native-lab-work/docs/lab/senses/pam-rebuild/selfpam/r2/forkD/corpora")
RT = os.path.expanduser("~/workspace/tnn-native-lab-work/docs/lab/senses/pam-rebuild/selfpam/r2/redteam/runs/reattack_cd/forkD_attack")
REGEN = os.path.expanduser("~/workspace/selfpam_forkd/build_orig/regen/all")
OUT = os.path.expanduser("~/workspace/selfpam_forkd/forkd2/corpora2")


def split_store(store_path):
    ext, gen = [], []
    for ln in open(store_path):
        ln = ln.strip()
        if not ln:
            continue
        assert ln.endswith("|EXT") or ln.endswith("|GEN"), ln
        if ln.endswith("|EXT"):
            ext.append(ln[:-4])
        else:
            gen.append(ln[:-4])
    return ext, gen


def write_part(path, header, lines):
    with open(path, "w") as f:
        f.write(header + "\n")
        for ln in lines:
            f.write(ln + "\n")


def migrate_corpus(tag, store_path, drafts_dir, delib_dir, manifest_path,
                   outdir, new_expected=None):
    """new_expected: dict case->expected overriding the manifest (launder)."""
    os.makedirs(outdir, exist_ok=True)
    ext, gen = split_store(store_path)
    elines, _ = sign_partition(tag, ext)
    glines, _ = gen_partition(tag, gen)
    write_part(os.path.join(outdir, "extpart.txt"),
               f"PART|{tag}|{len(elines)}", elines)
    write_part(os.path.join(outdir, "genpart.txt"),
               f"PART|{tag}|gen|{len(glines)}", glines)
    for sub in ("drafts", "delib"):
        src = drafts_dir if sub == "drafts" else delib_dir
        dst = os.path.join(outdir, sub)
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    n = 0
    with open(os.path.join(outdir, "manifest2.txt"), "w") as mf:
        for ln in open(manifest_path):
            ln = ln.strip()
            if not ln:
                continue
            case, draft, _store, delib, exp = ln.split("|")
            if new_expected and case in new_expected:
                exp = new_expected[case]
            mf.write(f"{case}|{draft}|extpart.txt|genpart.txt|{delib}|{exp}\n")
            n += 1
    print(f"{tag}: {len(ext)} EXT signed, {len(gen)} GEN chained, {n} cases")
    return ext, elines


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    # Builder corpora c1..c6 (regenerated drafts/delib, byte-identical manifests).
    for k in ["c1", "c2", "c3", "c4", "c5", "c6"]:
        migrate_corpus(
            k,
            os.path.join(FORKD, k, "store.txt"),
            os.path.join(REGEN, k, "drafts"),
            os.path.join(REGEN, k, "delib"),
            os.path.join(FORKD, k, "manifest.txt"),
            os.path.join(OUT, k))

    # Red-team M2 flip pairs (a=base INSTALL, b=flip WITHHOLD).
    for tag, sub in [("m2a", "a"), ("m2b", "b")]:
        migrate_corpus(
            tag,
            os.path.join(RT, "m2", sub, "store.txt"),
            os.path.join(RT, "m2", sub, "drafts"),
            os.path.join(RT, "m2", sub, "delib"),
            os.path.join(RT, "m2", sub, "manifest.txt"),
            os.path.join(OUT, tag))

    # Red-team M4 trace alibis.
    migrate_corpus(
        "m4",
        os.path.join(RT, "m4", "store.txt"),
        os.path.join(RT, "m4", "drafts"),
        os.path.join(RT, "m4", "delib"),
        os.path.join(RT, "m4", "manifest.txt"),
        os.path.join(OUT, "m4"))

    # Red-team M5 genuine generator-authored recursion.
    migrate_corpus(
        "m5",
        os.path.join(RT, "m5", "store.txt"),
        os.path.join(RT, "m5", "drafts"),
        os.path.join(RT, "m5", "delib"),
        os.path.join(RT, "m5", "manifest.txt"),
        os.path.join(OUT, "m5"))

    # Launder case: the 72 honest EXT entries are signed; the 6 attacker
    # zorp entries are FORGED (well-formed lengths, garbage signatures).
    # Old world: INSTALL. New world must fail closed -> WITHHOLD.
    outdir = os.path.join(OUT, "launder")
    os.makedirs(outdir, exist_ok=True)
    ext, gen = split_store(os.path.join(RT, "m5", "launder", "store.txt"))
    honest = [a for a in ext if "|zorp|" not in a and "|qux|" not in a
              and "|wug|" not in a]
    forged_atoms = [a for a in ext if a not in honest]
    assert len(honest) == 72 and len(forged_atoms) == 6, (len(honest), len(forged_atoms))
    elines, _ = sign_partition("launder", honest)
    # chain tip after the honest entries (public value; attacker can compute)
    prev = bytes(32)
    for ln in elines:
        q = ln.split("|")
        atom = "|".join(q[2:7])
        prev = H(prev + atom.encode() + bytes.fromhex(q[8]) + bytes.fromhex(q[9]))
    for i, atom in enumerate(forged_atoms):
        q, s, pol, r, o = atom.split("|")
        # garbage signature, well-formed length; unauthorized pknext
        fl = (f"ENTRY|launder|{q}|{s}|{pol}|{r}|{o}|{prev.hex()}|"
              f"{pk('launder', 900 + i).hex()}|{'ab' * 2144}")
        elines.append(fl)
        prev = H(prev + atom.encode() + bytes.fromhex(pk('launder', 900 + i).hex())
                 + bytes.fromhex("ab" * 2144))
    glines, _ = gen_partition("launder", gen)
    write_part(os.path.join(outdir, "extpart.txt"),
               f"PART|launder|{len(elines)}", elines)
    write_part(os.path.join(outdir, "genpart.txt"),
               f"PART|launder|gen|{len(glines)}", glines)
    for sub, src in (("drafts", os.path.join(RT, "m5", "launder", "drafts")),
                     ("delib", os.path.join(RT, "m5", "launder", "delib"))):
        dst = os.path.join(outdir, sub)
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    with open(os.path.join(outdir, "manifest2.txt"), "w") as mf:
        for ln in open(os.path.join(RT, "m5", "launder", "manifest.txt")):
            ln = ln.strip()
            if not ln:
                continue
            case, draft, _s, delib, _e = ln.split("|")
            mf.write(f"{case}|{draft}|extpart.txt|genpart.txt|{delib}|WITHHOLD\n")
    print(f"launder: {len(honest)} EXT signed + {len(forged_atoms)} FORGED, "
          f"{len(gen)} GEN chained; M5L-001 expected WITHHOLD")

    # Tamper corpus ct/: byte-flip, reorder, fully-forged chain.
    ctdir = os.path.join(OUT, "ct")
    os.makedirs(ctdir, exist_ok=True)
    c1ext, c1gen = split_store(os.path.join(FORKD, "c1", "store.txt"))
    base_lines, _ = sign_partition("ct", c1ext)
    base_gen, _ = gen_partition("ct", c1gen)
    write_part(os.path.join(ctdir, "genpart.txt"),
               f"PART|ct|gen|{len(base_gen)}", base_gen)
    os.makedirs(os.path.join(ctdir, "drafts"), exist_ok=True)
    os.makedirs(os.path.join(ctdir, "delib"), exist_ok=True)
    open(os.path.join(ctdir, "drafts", "CT.txt"), "w").write("The cat is a mammal.\n")
    open(os.path.join(ctdir, "delib", "CT.txt"), "w").write(
        "PREMISES:\nUNIT|cat|POS|IS_A|mammal\nSTEPS:\n"
        "LOOKUP||UNIT|cat|POS|IS_A|mammal||UNIT|cat|POS|IS_A|mammal\n"
        "CONCLUSIONS:\nUNIT|cat|POS|IS_A|mammal\n")
    hdr = f"PART|ct|{len(base_lines)}"
    # CT-SIGFLIP: flip one hex char in entry 5's signature
    p = base_lines[5].split("|")
    s = p[9]
    p[9] = ("0" if s[0] != "0" else "1") + s[1:]
    tampered = base_lines[:5] + ["|".join(p)] + base_lines[6:]
    write_part(os.path.join(ctdir, "extpart_sigflip.txt"), hdr, tampered)
    # CT-REORDER: swap entries 3 and 4
    reo = base_lines[:3] + [base_lines[4], base_lines[3]] + base_lines[5:]
    write_part(os.path.join(ctdir, "extpart_reorder.txt"), hdr, reo)
    # CT-FORGE: fully attacker-forged single-entry partition (own keychain)
    from channel import sk, digits_of, H as _H
    aidx, aj = 5000, 0
    ask = [_H(b"attacker-seed-ct" + b"ct" + aidx.to_bytes(4, "big") + bytes([j]))
           for j in range(67)]
    atips = []
    for j in range(67):
        t = ask[j]
        for _ in range(15):
            t = _H(t)
        atips.append(t)
    apknext = _H(b"".join(atips))
    m = _H(b"ct" + b"UNIT|cat|POS|IS_A|mammal" + apknext + bytes(32))
    ds = digits_of(m)
    asig_parts = []
    for j in range(67):
        t = ask[j]
        for _ in range(15 - ds[j]):
            t = _H(t)
        asig_parts.append(t)
    asig = b"".join(asig_parts)
    fl = ("ENTRY|ct|UNIT|cat|POS|IS_A|mammal|" + "00" * 32 + "|" +
          apknext.hex() + "|" + asig.hex())
    write_part(os.path.join(ctdir, "extpart_forge.txt"), "PART|ct|1", [fl])
    with open(os.path.join(ctdir, "manifest2.txt"), "w") as mf:
        mf.write("CT-SIGFLIP|drafts/CT.txt|extpart_sigflip.txt|genpart.txt|delib/CT.txt|WITHHOLD\n")
        mf.write("CT-REORDER|drafts/CT.txt|extpart_reorder.txt|genpart.txt|delib/CT.txt|WITHHOLD\n")
        mf.write("CT-FORGE|drafts/CT.txt|extpart_forge.txt|genpart.txt|delib/CT.txt|WITHHOLD\n")
    print("ct: 3 tamper cases (sigflip, reorder, forge)")

    print("migration complete ->", OUT)


if __name__ == "__main__":
    main()
