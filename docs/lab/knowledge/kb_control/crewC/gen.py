#!/usr/bin/env python3
"""Crew C fixture generator: deterministic KB store images + episode specs.
Zero RNG: every parameter derives from the episode index by fixed formulas.
"""
import os
import struct
import sys

IMG_SIZE = 4096
MAGIC = 0x4B424331
HEADER = 12
SLOTREC = 16

# situation bits (must match kbc.zag)
SB_HOFF, SB_HUSED, SB_BOUND, SB_SEQ, SB_DEL, SB_REFUSE = 1, 2, 4, 8, 16, 32


def align8(n):
    return n + ((-n) % 8)


def payload_bytes(slot_id, idx, ln, variant=0):
    return bytes((slot_id * 37 + j * 11 + idx * 5 + variant * 101) % 256 for j in range(ln))


def build_store(slot_payloads):
    """slot_payloads: list of (id, bytes, live). Returns (img bytearray, table dict)."""
    n = len(slot_payloads)
    img = bytearray(IMG_SIZE)
    struct.pack_into('<III', img, 0, MAGIC, n, 0)
    tbase = HEADER
    off = tbase + n * SLOTREC
    table = {}
    for k, (sid, pay, live) in enumerate(slot_payloads):
        ln = len(pay)
        struct.pack_into('<IIII', img, tbase + k * SLOTREC, sid, off, ln, live)
        struct.pack_into('<II', img, off, sid, ln)
        img[off + 8:off + 8 + ln] = pay
        pad = align8(8 + ln) - (8 + ln)
        # padding bytes already zero
        table[sid] = (off, ln, live)
        off = off + 8 + ln + pad
    struct.pack_into('<I', img, 8, off)  # blob_end
    return img, table


def compute_sit(table, blob_end, hints, hint_used, chunk, seq_idx, opdel, target, newlen):
    sit = 0
    for sid, ho in hints.items():
        if sid in table and table[sid][0] != ho:
            sit |= SB_HOFF
    if hint_used != blob_end:
        sit |= SB_HUSED
    if seq_idx > 0:
        sit |= SB_SEQ
    if opdel:
        sit |= SB_DEL
    refuse = False
    if target not in table or table[target][2] != 1:
        refuse = True
    elif not opdel and newlen is not None and newlen > table[target][1]:
        refuse = True
    if refuse:
        sit |= SB_REFUSE
    if target in table and table[target][2] == 1:
        off, ln, _ = table[target]
        recend = off + 8 + ln
        if blob_end - recend < 32:
            sit |= SB_BOUND
        if chunk > 0 and (off // chunk) != ((recend - 1) // chunk):
            sit |= SB_BOUND
    return sit


def write_spec(path, *, ep, op, slot, newlen=None, payload_hex=None,
               hint_used, hints, seq_idx, seq_total, chunk, sit, must_refuse):
    with open(path, 'w') as f:
        f.write(f"EP {ep}\n")
        f.write(f"CHUNK {chunk}\n")
        if op == 'revise':
            f.write(f"OP revise {slot} {newlen}\n")
            f.write(f"PAYLOAD {payload_hex}\n")
        else:
            f.write(f"OP delete {slot}\n")
        f.write(f"HINT_USED {hint_used}\n")
        for sid in sorted(hints):
            f.write(f"HINT {sid} {hints[sid]}\n")
        f.write(f"SEQ {seq_idx} {seq_total}\n")
        f.write(f"SIT {sit}\n")
        f.write(f"MUST_REFUSE {must_refuse}\n")


# ---------------- episode families ----------------
# Each returns a list of op dicts: {op, slot, newlen?, payload?, must_refuse}
# plus hint overrides. Hints default to the true table (of the CURRENT image
# for seq op 0; pre-sequence table for seq ops >0 to model staleness).

def base_slots(idx, nslots, chunk):
    slots = []
    for i in range(nslots):
        sid = 100 + i
        ln = 8 + (idx * 13 + i * 29) % 120
        slots.append((sid, payload_bytes(sid, idx, ln), 1))
    return slots


def fam_clean(idx, chunk):
    nslots = 4 + (idx * 7) % 9
    slots = base_slots(idx, nslots, chunk)
    t = idx % nslots
    sid, pay, _ = slots[t]
    oldlen = len(pay)
    newlen = max(1, oldlen - (1 + (idx % 5)))
    if idx % 3 == 0:
        return slots, [{'op': 'delete', 'slot': sid, 'must_refuse': 0}], {}
    return slots, [{'op': 'revise', 'slot': sid, 'newlen': newlen,
                    'payload': payload_bytes(sid, idx, newlen, variant=1),
                    'must_refuse': 0}], {}


def fam_t1(idx, chunk, novel=False):
    # stale hint_off on the target slot
    nslots = 4 + (idx * 7) % 9
    slots = base_slots(idx, nslots, chunk)
    t = idx % nslots
    sid = slots[t][0]
    deltas = [40, 48] if novel else [8, 16, 24]
    delta = deltas[idx % len(deltas)]
    if (idx // len(deltas)) % 2 == 0:
        delta = -delta
    oldlen = len(slots[t][1])
    newlen = max(1, oldlen - (1 + (idx % 5)))
    ops = [{'op': 'revise', 'slot': sid, 'newlen': newlen,
            'payload': payload_bytes(sid, idx, newlen, variant=1),
            'must_refuse': 0, 'hint_delta': delta}]
    return slots, ops, {}


def fam_t2(idx, chunk, novel=False):
    # boundary: last slot; hint_used padding-blind; hint_off[last] shifted.
    # total inter-record padding = 126 (train) / 70 (heldout).
    nslots = 10 if novel else 18
    pad_each = 7
    slots = []
    for i in range(nslots):
        sid = 100 + i
        ln = 1 + 8 * ((idx + i) % 16)  # == 1 mod 8 -> 7 pad bytes each
        slots.append((sid, payload_bytes(sid, idx, ln), 1))
    sid = 100 + nslots - 1
    oldlen = len(slots[-1][1])
    newlen = max(1, oldlen - 3)
    total_pad = nslots * pad_each
    ops = [{'op': 'revise', 'slot': sid, 'newlen': newlen,
            'payload': payload_bytes(sid, idx, newlen, variant=1),
            'must_refuse': 0, 't2': total_pad}]
    return slots, ops, {}


def fam_t4(idx, chunk, novel=False):
    # delete non-last slot; hint_used understates blob_end (padding-blind)
    nslots = 5 + (idx * 7) % 8
    slots = base_slots(idx, nslots, chunk)
    t = idx % (nslots - 1)  # not last
    sid = slots[t][0]
    pt = [40, 56][idx % 2] if novel else [16, 24, 32][idx % 3]
    ops = [{'op': 'delete', 'slot': sid, 'must_refuse': 0, 'used_short': pt}]
    return slots, ops, {}


def fam_t5(idx, chunk):
    nslots = 4 + (idx * 7) % 9
    slots = base_slots(idx, nslots, chunk)
    v = idx % 3
    if v == 0:
        # revise with newlen > oldlen
        t = idx % nslots
        sid = slots[t][0]
        oldlen = len(slots[t][1])
        ops = [{'op': 'revise', 'slot': sid, 'newlen': oldlen + 8,
                'payload': payload_bytes(sid, idx, oldlen + 8, variant=1),
                'must_refuse': 1}]
    elif v == 1:
        # delete an already-dead slot
        t = idx % nslots
        sid, pay, _ = slots[t]
        slots[t] = (sid, pay, 0)
        ops = [{'op': 'delete', 'slot': sid, 'must_refuse': 1}]
    else:
        # wild hint (OOB)
        t = idx % nslots
        sid = slots[t][0]
        oldlen = len(slots[t][1])
        newlen = max(1, oldlen - 2)
        ops = [{'op': 'revise', 'slot': sid, 'newlen': newlen,
                'payload': payload_bytes(sid, idx, newlen, variant=1),
                'must_refuse': 0, 'wild_hint': True}]
    return slots, ops, {}


def fam_t3(idx, chunk):
    # adversarial sequence: delete (shifts offsets) then revises; hints frozen pre-seq
    nslots = 6 + (idx * 5) % 7
    slots = base_slots(idx, nslots, chunk)
    k = 2 + (idx % 3)  # 2..4 ops
    d0 = idx % (nslots - 1)  # delete target not last
    dsid = slots[d0][0]
    ops = [{'op': 'delete', 'slot': dsid, 'must_refuse': 0}]
    j = 1
    si = (idx + 3) % nslots
    while len(ops) < k:
        sid = slots[si % nslots][0]
        if sid != dsid:
            oldlen = len(slots[si % nslots][1])
            newlen = max(1, oldlen - (1 + (idx + j) % 5))
            ops.append({'op': 'revise', 'slot': sid, 'newlen': newlen,
                        'payload': payload_bytes(sid, idx + j, newlen, variant=1),
                        'must_refuse': 0})
            j += 1
        si += 1
    return slots, ops, {'seq_stale_hints': True}


# ---------------- driver ----------------
def episode_plan(idx, regime):
    """Returns (family_fn_kwargs, chunk)."""
    if regime == 'train':
        if idx < 60:      # P0 basics
            r = idx % 10
            fam = 't1' if r < 4 else ('t5' if r == 4 else 'clean')
        elif idx < 120:   # P1 boundaries
            r = (idx - 60) % 10
            fam = 't2' if r < 3 else ('t1' if r < 5 else ('t5' if r == 5 else 'clean'))
        elif idx < 180:   # P2 multi-chunk
            r = (idx - 120) % 10
            fam = 't4' if r < 3 else ('t2' if r == 3 else ('t1' if r == 4 else 'clean'))
        else:             # P3 adversarial sequences
            r = (idx - 180) % 10
            fam = 't3' if r < 4 else ('t4' if r < 6 else ('t2' if r == 6 else 'clean'))
        chunk = [256, 512][idx % 2]
    elif regime == 'heldout':
        r = (idx - 1000) % 10
        fam = (['t1', 't1', 't2', 't2', 't4', 't4', 't3', 't3', 't5', 'clean'])[r]
        chunk = [384, 768][idx % 2]
    elif regime == 'retention':
        r = (idx - 2000) % 10
        fam = (['t1', 't2', 't4', 't3', 'clean', 'clean', 'clean', 'clean', 'clean', 't5'])[r]
        chunk = [256, 512][idx % 2]
    else:
        raise ValueError(regime)
    novel = (regime == 'heldout')
    return fam, chunk, novel


FAMS = {'clean': fam_clean, 't1': fam_t1, 't2': fam_t2, 't4': fam_t4,
        't5': fam_t5, 't3': fam_t3}


def read_table(img):
    magic, n, blob_end = struct.unpack_from('<III', img, 0)
    assert magic == MAGIC
    table = {}
    for k in range(n):
        sid, off, ln, live = struct.unpack_from('<IIII', img, HEADER + k * SLOTREC)
        table[sid] = (off, ln, live)
    return table, blob_end


def write_op_spec(outdir, j, op, img_path, frozen_hints, hint_used_fn, chunk, ep_base, seq_total):
    """Write spec j for an op against the CURRENT image; hints stay frozen."""
    with open(img_path, 'rb') as f:
        img = f.read()
    table, blob_end = read_table(img)
    hints = dict(frozen_hints)
    hint_used = hint_used_fn(j, blob_end)
    newlen = op.get('newlen')
    sit = compute_sit(table, blob_end, hints, hint_used, chunk, j,
                      1 if op['op'] == 'delete' else 0, op['slot'], newlen)
    sp = os.path.join(outdir, f'spec{j}.txt')
    write_spec(sp, ep=ep_base + j, op=op['op'], slot=op['slot'],
               newlen=newlen,
               payload_hex=op['payload'].hex() if op.get('payload') else None,
               hint_used=hint_used, hints=hints, seq_idx=j,
               seq_total=seq_total, chunk=chunk, sit=sit,
               must_refuse=op['must_refuse'])
    return sp


def build_episode(idx, regime, outdir):
    fam, chunk, novel = episode_plan(idx, regime)
    if fam in ('t1', 't2', 't4'):
        slots, ops, extra = FAMS[fam](idx, chunk, novel)
    else:
        slots, ops, extra = FAMS[fam](idx, chunk)
    img, table = build_store(slots)
    blob_end = struct.unpack_from('<I', img, 8)[0]
    os.makedirs(outdir, exist_ok=True)
    img0_path = os.path.join(outdir, 'img0.bin')
    with open(img0_path, 'wb') as f:
        f.write(img)
    # frozen hints: pre-sequence truth for T3, else per-op truth (same thing for j=0)
    frozen_hints = {sid: off for sid, (off, ln, live) in table.items()}

    def hint_used_fn(j, cur_blob_end):
        op = ops[j]
        if op.get('t2'):
            return cur_blob_end - op['t2'] if j == 0 else cur_blob_end - op['t2']
        if op.get('used_short'):
            return cur_blob_end - op['used_short']
        return cur_blob_end

    # trap hint overrides that are defined relative to the frozen (img0) table
    frozen_overrides = {}
    op0 = ops[0]
    if 'hint_delta' in op0:
        frozen_overrides[op0['slot']] = frozen_hints[op0['slot']] + op0['hint_delta']
    if op0.get('wild_hint'):
        frozen_overrides[op0['slot']] = IMG_SIZE + 64
    if op0.get('t2'):
        total_pad = op0['t2']
        sid = op0['slot']
        oldlen = table[sid][1]
        frozen_overrides[sid] = (blob_end - total_pad) - 8 - oldlen
    for sid, ho in frozen_overrides.items():
        frozen_hints[sid] = ho

    # hint_used may also be overridden relative to img0's blob_end (freeze it)
    frozen_hint_used = hint_used_fn(0, blob_end)

    def hint_used_fn2(j, cur_blob_end):
        return frozen_hint_used

    sp0 = write_op_spec(outdir, 0, ops[0], img0_path, frozen_hints, hint_used_fn2,
                        chunk, idx * 10, len(ops))
    meta = {'ops': ops, 'chunk': chunk, 'fam': fam, 'seq_total': len(ops),
            'frozen_hints': dict(frozen_hints),
            'frozen_hint_used': frozen_hint_used}
    return sp0, img0_path, meta


def geom_key(idx, regime):
    fam, chunk, novel = episode_plan(idx, regime)
    if fam in ('t1', 't2', 't4'):
        _, ops, _ = FAMS[fam](idx, chunk, novel)
    else:
        _, ops, _ = FAMS[fam](idx, chunk)
    op = ops[0]
    lie = 'none'
    if 'hint_delta' in op:
        lie = f"t1d{op['hint_delta']}"
    elif 't2' in op:
        lie = f"t2p{op['t2']}"
    elif 'used_short' in op:
        lie = f"t4s{op['used_short']}"
    elif op.get('wild_hint'):
        lie = 't5wild'
    return (fam, chunk, lie, novel)


if __name__ == '__main__':
    # overlap assertion: train vs heldout geometry must be disjoint
    train_keys = {geom_key(i, 'train') for i in range(260)}
    held_keys = {geom_key(i, 'heldout') for i in range(1000, 1060)}
    overlap = train_keys & held_keys
    # novel flag differs by construction; check the rest too
    train_core = {(f, c, l) for (f, c, l, n) in train_keys}
    held_core = {(f, c, l) for (f, c, l, n) in held_keys}
    print("train keys:", len(train_keys), "heldout keys:", len(held_keys))
    print("core overlap (must be empty):", held_core & train_core)
    assert not (held_core & train_core), "GEOMETRY OVERLAP between train and heldout"
    print("OK: heldout geometries are novel")
