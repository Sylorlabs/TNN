#!/usr/bin/env python3
"""build_curriculum.py — deterministic Track B curriculum slice builder.

CORPUS PREP ONLY. This script never participates in any AI decision path: it
cuts byte slices, derives ground-truth unit inventories, and computes flaw
slot maps. No RNG, no wall-clock, no network, no locale dependence. Two runs
over the same corpus bytes produce byte-identical outputs (verified in
VERIFICATION.md).

Implements, verbatim:
  slicing   SLICE-V1  (OPERATIONALIZATION.md §1)
  inventory G-V1      (OPERATIONALIZATION.md §2)
  flaw slots FLAW-V1  (FLAW_PLACEMENT.md)

Usage:
  python3 build_curriculum.py --corpora-dir /tmp/tnn-corpora --out <dir>

Outputs under <out>:
  manifests/slices_manifest.json
  inventories/<slice_id>.json
  sealed/slot_maps/<slice_id>.json
"""
import argparse
import hashlib
import json
import os
import struct
import sys

# ---------------------------------------------------------------- pinned inputs
SHK_NAME = "pg100.txt"
SHK_LEN = 5638480
SHK_SHA256 = "3cf4b3d44ee14cff4e14e78e2ad3318eff76f3f7f2afc3cee6bb925879110a37"
SQL_NAME = "sqlite3.c"
SQL_LEN = 9515341
SQL_SHA256 = "b1dd5d74ec7f29055a6684fa06fb3c2f6821c87dd38f9a458dfd2e8a1db28189"

SIZE_LEGS = (("64K", 65536), ("256K", 262144), ("1M", 1048576))
K1X_CAP = 8          # max 1x slices per corpus per size leg (OPERATIONALIZATION §1)
HELD_OUT_FRAC = 0.10  # last 10% of each corpus reserved for M2 T1 (never sliced)
REC_BAR = 3          # recurrence bar for inventory (G-V1 step 5)
MIN_LEN = 2          # minimum candidate length (G-V1 step 2)
FLAWS_PER_SLICE = 12
TYPE_ORDER = (["wrong-span"] * 4 + ["false-confidence"] * 4
              + ["missing-grounding"] * 2 + ["plausible-false"] * 2)
assert len(TYPE_ORDER) == FLAWS_PER_SLICE

WALL = 1 << 25  # znc 2^25 slice-indexing wall: no buffer indexed above this


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# ------------------------------------------------------- G-V1 candidate scan
def is_letter(c: int) -> bool:
    return 0x41 <= c <= 0x5A or 0x61 <= c <= 0x7A


def is_id_start(c: int) -> bool:
    return c == 0x5F or is_letter(c)


def is_id_cont(c: int) -> bool:
    return is_id_start(c) or 0x30 <= c <= 0x39


def scan_prose(buf: bytes):
    """Maximal [A-Za-z] runs, len>=2. Returns list of (start, raw_bytes)."""
    out = []
    i, n = 0, len(buf)
    while i < n:
        if is_letter(buf[i]):
            j = i + 1
            while j < n and is_letter(buf[j]):
                j += 1
            if j - i >= MIN_LEN:
                out.append((i, bytes(buf[i:j])))
            i = j
        else:
            i += 1
    return out


def scan_code(buf: bytes):
    """C identifier runs outside comments/strings/char-literals, len>=2.

    Lexical approximation (not a full C parser): states CODE, LINE_COMMENT,
    BLOCK_COMMENT, STRING, CHAR with backslash escapes. Deterministic.
    """
    out = []
    i, n = 0, len(buf)
    state = 0  # 0=code 1=line 2=block 3=str 4=char
    start = -1
    while i < n:
        c = buf[i]
        if state == 0:
            if start >= 0 and not is_id_cont(c):
                if i - start >= MIN_LEN:
                    out.append((start, bytes(buf[start:i])))
                start = -1
            if c == 0x2F and i + 1 < n and buf[i + 1] == 0x2F:
                state = 1
                i += 2
                continue
            if c == 0x2F and i + 1 < n and buf[i + 1] == 0x2A:
                state = 2
                i += 2
                continue
            if c == 0x22:
                state = 3
                i += 1
                continue
            if c == 0x27:
                state = 4
                i += 1
                continue
            if start < 0 and is_id_start(c):
                start = i
        elif state == 1:  # // to newline
            if c == 0x0A:
                state = 0
        elif state == 2:  # /* to */
            if c == 0x2A and i + 1 < n and buf[i + 1] == 0x2F:
                state = 0
                i += 2
                continue
        elif state == 3:  # " ..."
            if c == 0x5C:
                i += 2
                continue
            if c == 0x22:
                state = 0
        elif state == 4:  # '...'
            if c == 0x5C:
                i += 2
                continue
            if c == 0x27:
                state = 0
        i += 1
    if start >= 0 and n - start >= MIN_LEN:
        out.append((start, bytes(buf[start:n])))
    return out


def canonical(unit: bytes, corpus: str) -> bytes:
    if corpus == "shakespeare":
        return unit.lower()  # ASCII-only by construction; bytes.lower is exact
    return unit


def build_inventory(slice_id: str, buf: bytes, corpus: str):
    """G-V1. Returns (entries, inventory_sha256_hex, n_occ, canon_counts).

    entries: list of dicts {u, count, first} sorted by (-count, u).
    canon_counts: dict canonical_unit_bytes -> total occurrence count
                  (for O(1) plausible-false zero-count checks).
    """
    assert len(buf) < WALL, "slice exceeds 2^25 wall"
    occ = scan_prose(buf) if corpus == "shakespeare" else scan_code(buf)
    counts = {}
    first = {}
    for (s, raw) in occ:
        k = canonical(raw, corpus)
        if k in counts:
            counts[k] += 1
        else:
            counts[k] = 1
            first[k] = s
    kept = [(k, counts[k], first[k]) for k in counts if counts[k] >= REC_BAR]
    kept.sort(key=lambda t: (-t[1], t[0]))
    entries = [{"u": k.decode("ascii"), "count": n, "first": f}
               for (k, n, f) in kept]
    # canonical hash serialization: u32LE(len)||bytes||u64LE(count)||u64LE(first)
    h = hashlib.sha256()
    for (k, n, f) in kept:
        h.update(struct.pack("<I", len(k)))
        h.update(k)
        h.update(struct.pack("<Q", n))
        h.update(struct.pack("<Q", f))
    return entries, h.hexdigest(), len(occ), counts


# ------------------------------------------------------- FLAW-V1 slot map
def flaw_uid(slice_id: str) -> bytes:
    # Flaw slots are a pure function of the slice id ONLY (B.7: "12 planted
    # flaws per curriculum slice"). All sessions on a slice — 1x or 10x —
    # plant the same 12 slots, so Crew 4 (arm-1 sessions) and every other
    # crew derive the identical map from the slice id alone. (A 10x leg is 10
    # repetitions of the same session content per the 1x->10x rule, not 10
    # different flaw sets.)
    return slice_id.encode("ascii")


def u64be(b: bytes) -> int:
    return struct.unpack(">Q", b)[0]


def build_slots(slice_id: str, buf: bytes, corpus: str, entries,
                canon_counts: dict):
    """FLAW-V1. Pure function of (slice_id, slice bytes). Returns 12 slots."""
    n_units = len(entries)
    assert n_units >= FLAWS_PER_SLICE, \
        "slice %s has %d units < 12 flaws" % (slice_id, n_units)
    unit_bytes = [e["u"].encode("ascii") for e in entries]
    firsts = [e["first"] for e in entries]
    uid = flaw_uid(slice_id)
    slots = []
    for j in range(FLAWS_PER_SLICE):
        ftype = TYPE_ORDER[j]
        h = hashlib.sha256(b"TNN-TB-FLAW-V1\x00" + uid
                           + bytes([j])).digest()
        idx = u64be(h[0:8]) % n_units
        u = unit_bytes[idx]
        o = firsts[idx]
        L = len(u)
        slot = {"j": j, "type": ftype, "unit_index": idx,
                "unit": u.decode("ascii")}
        if ftype == "wrong-span":
            mag = 1 + (u64be(h[8:16]) % 16)
            direction = 1 if (h[16] & 1) else -1
            ss = o + direction * mag
            if ss < 0:
                ss = 0
            if ss > len(buf) - L:
                ss = len(buf) - L
            slot["base_span"] = [o, o + L]
            slot["shifted_span"] = [ss, ss + L]
            slot["shift_applied"] = ss - o
        elif ftype in ("false-confidence", "missing-grounding"):
            slot["span"] = [o, o + L]
            if ftype == "false-confidence":
                slot["confidence"] = 255
                slot["grounding"] = []
            else:
                slot["grounding"] = []
        else:  # plausible-false
            alpha = (b"abcdefghijklmnopqrstuvwxyz" if corpus == "shakespeare"
                     else b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")
            mutated = None
            nonce = -1
            for nn in range(100000):
                pos = (h[17] + nn) % L
                ch = alpha[(h[18] + 7 * nn) % len(alpha)]
                cand = u[:pos] + bytes([ch]) + u[pos + 1:]
                if cand == u:
                    continue
                if canon_counts.get(cand, 0) == 0:
                    mutated = cand
                    nonce = nn
                    break
            assert mutated is not None, "no zero-count mutation for %r" % u
            slot["base_unit_index"] = idx
            slot["mutated_unit"] = mutated.decode("ascii")
            slot["nonce"] = nonce
        slots.append(slot)
    return slots


# ------------------------------------------------------------------- main
def load_corpus(d: str, name: str, want_len: int, want_sha: str) -> bytes:
    p = os.path.join(d, name)
    with open(p, "rb") as f:
        b = f.read()
    if len(b) != want_len or sha256(b) != want_sha:
        raise SystemExit(
            "CORPUS MISMATCH %s: got len=%d sha=%s; want len=%d sha=%s\n"
            "Re-fetch with fetch/*.sh and check PROVENANCE.md." %
            (name, len(b), sha256(b), want_len, want_sha))
    return b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpora-dir", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    corpora = [
        ("shakespeare", "SHK", SHK_NAME, SHK_LEN, SHK_SHA256),
        ("sqlite", "SQL", SQL_NAME, SQL_LEN, SQL_SHA256),
    ]
    bufs = {}
    for (corpus, _, name, want_len, want_sha) in corpora:
        bufs[corpus] = load_corpus(a.corpora_dir, name, want_len, want_sha)

    os.makedirs(os.path.join(a.out, "manifests"), exist_ok=True)
    os.makedirs(os.path.join(a.out, "inventories"), exist_ok=True)
    os.makedirs(os.path.join(a.out, "sealed", "slot_maps"), exist_ok=True)

    manifest_slices = []
    for (corpus, tag, _, _, csha) in corpora:
        buf = bufs[corpus]
        assert len(buf) < WALL
        eligible_end = int(len(buf) * (1.0 - HELD_OUT_FRAC))
        for (leg_name, S) in SIZE_LEGS:
            k = min(K1X_CAP, eligible_end // S)
            for i in range(k):
                s0, s1 = i * S, (i + 1) * S
                sbuf = buf[s0:s1]
                slice_id = "%s-%s-%04d" % (tag, leg_name, i)
                entries, inv_sha, n_occ, canon_counts = build_inventory(
                    slice_id, sbuf, corpus)
                inv_doc = {
                    "slice_id": slice_id,
                    "corpus": corpus,
                    "size_leg": leg_name,
                    "procedure": "G-V1",
                    "rec_bar": REC_BAR,
                    "min_len": MIN_LEN,
                    "candidate_occurrences": n_occ,
                    "unit_count": len(entries),
                    "units": entries,
                    "inventory_sha256": inv_sha,
                }
                with open(os.path.join(a.out, "inventories",
                                       slice_id + ".json"), "w") as f:
                    json.dump(inv_doc, f, sort_keys=True,
                              separators=(",", ":"), ensure_ascii=True)
                    f.write("\n")
                # slot maps: the same 12 FLAW-V1 slots for every session
                # on this slice (1x and all 10x reps)
                slot_doc = {"slice_id": slice_id,
                            "flaw_procedure": "FLAW-V1",
                            "slots": build_slots(slice_id, sbuf, corpus,
                                                 entries, canon_counts)}
                with open(os.path.join(a.out, "sealed", "slot_maps",
                                       slice_id + ".json"), "w") as f:
                    json.dump(slot_doc, f, sort_keys=True,
                              separators=(",", ":"), ensure_ascii=True)
                    f.write("\n")
                manifest_slices.append({
                    "slice_id": slice_id,
                    "corpus": corpus,
                    "corpus_sha256": csha,
                    "size_leg": leg_name,
                    "slice_bytes": S,
                    "byte_start": s0,
                    "byte_end": s1,
                    "held_out_start": eligible_end,
                    "slice_sha256": sha256(sbuf),
                    "inventory_sha256": inv_sha,
                    "inventory_units": len(entries),
                    "flaw_slots_per_session_variant": FLAWS_PER_SLICE,
                })

    manifest_slices.sort(key=lambda d: d["slice_id"])
    manifest = {
        "slicing_procedure": "SLICE-V1",
        "ground_truth_procedure": "G-V1",
        "flaw_slot_procedure": "FLAW-V1",
        "rec_bar": REC_BAR,
        "min_len": MIN_LEN,
        "k1x_cap": K1X_CAP,
        "held_out_rule": "slices from [0, floor(0.9*len)); last 10%% reserved M2 T1",
        "scale_rule": "10x = 10 reps per 1x slice (R0..R9), same bytes, same "
                      "inventory, same 12 flaw slots (FLAW-V1 is a pure function "
                      "of slice_id); never bigger slices",
        "corpora": {
            "shakespeare": {"file": SHK_NAME, "bytes": SHK_LEN,
                            "sha256": SHK_SHA256, "license": "public domain"},
            "sqlite": {"file": SQL_NAME, "bytes": SQL_LEN,
                       "sha256": SQL_SHA256, "license": "public domain"},
        },
        "size_legs_bytes": {n: s for (n, s) in SIZE_LEGS},
        "slice_count": len(manifest_slices),
        "slices": manifest_slices,
    }
    with open(os.path.join(a.out, "manifests",
                           "slices_manifest.json"), "w") as f:
        json.dump(manifest, f, sort_keys=True,
                  separators=(",", ":"), ensure_ascii=True)
        f.write("\n")
    print("slices: %d" % len(manifest_slices))
    print("manifest sha256:",
          sha256(open(os.path.join(a.out, "manifests",
                                   "slices_manifest.json"), "rb").read()))


if __name__ == "__main__":
    sys.exit(main())
