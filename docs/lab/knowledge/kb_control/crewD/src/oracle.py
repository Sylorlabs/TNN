#!/usr/bin/env python3
"""Crew D oracle: canonical model, verify-output parser, chunk-diff K1 rule,
phase hash chain. Deterministic; no RNG."""
import hashlib
import os
import re

from fixtures import record_sha


# ---------------------------------------------------------------- model
class Model:
    """Canonical expected state: id -> {key,text,kind,deleted}."""

    def __init__(self):
        self.facts = {}

    def put(self, fid, key, text, kind=1):
        self.facts[fid] = {"key": key, "text": text, "kind": kind,
                           "deleted": False}

    def revise(self, fid, text):
        f = self.facts[fid]
        assert not f["deleted"]
        f["text"] = text

    def delete(self, fid):
        self.facts[fid]["deleted"] = True

    def live_ids(self):
        return sorted(i for i, f in self.facts.items() if not f["deleted"])

    def expected_sha(self, fid):
        f = self.facts[fid]
        return record_sha(f["kind"], fid, f["key"], f["text"])


# ---------------------------------------------------------------- verify parse
SLOT_RE = re.compile(
    r"^SLOT id=(\d+) off=(\d+) kind=(\d+) keylen=(\d+) textlen=(\d+) sha=([0-9a-f]{64})$")
VERIFY_RE = re.compile(
    r"^VERIFY n=(\d+) live=(\d+) deleted=(\d+) chunk_corrupt=(\d+) "
    r"offset_mismatches=(\d+) unreadable=(\d+) digest=([0-9a-f]{64}) (OK|FAIL)$")


def parse_verify(text):
    slots = {}
    summary = None
    for line in text.splitlines():
        m = SLOT_RE.match(line)
        if m:
            fid = int(m.group(1))
            slots[fid] = {"off": int(m.group(2)), "kind": int(m.group(3)),
                          "keylen": int(m.group(4)), "textlen": int(m.group(5)),
                          "sha": m.group(6)}
            continue
        m = VERIFY_RE.match(line)
        if m:
            summary = {"n": int(m.group(1)), "live": int(m.group(2)),
                       "deleted": int(m.group(3)),
                       "chunk_corrupt": int(m.group(4)),
                       "offset_mismatches": int(m.group(5)),
                       "unreadable": int(m.group(6)),
                       "digest": m.group(7), "ok": m.group(8) == "OK"}
    assert summary is not None, "no VERIFY line in output"
    return slots, summary


# ---------------------------------------------------------------- chunk K1 rule
def snapshot_chunks(store_dir):
    """{name: (sha256, bytes)} for every blob chunk file, sorted by name."""
    snaps = {}
    for name in sorted(os.listdir(store_dir)):
        if name.startswith("blob_") and name.endswith(".dat"):
            with open(os.path.join(store_dir, name), "rb") as fh:
                data = fh.read()
            snaps[name] = (hashlib.sha256(data).hexdigest(), data)
    return snaps


def chunk_diff_violations(pre, post):
    """Universal append-only K1 rule.

    For every chunk present before the op: post bytes must equal pre bytes,
    except that in the last pre-existing chunk, differences are allowed only
    where the pre byte was 0x00 (growth into zero padding). New chunk files
    are allowed. Returns a list of violation dicts (empty = clean).
    """
    viol = []
    names = sorted(set(pre) | set(post))
    last_pre = sorted(pre)[-1] if pre else None
    for name in names:
        if name not in pre:
            continue  # new chunk file: allowed growth
        if name not in post:
            viol.append({"chunk": name, "type": "chunk_deleted"})
            continue
        _, a = pre[name]
        _, b = post[name]
        if len(a) != len(b):
            viol.append({"chunk": name, "type": "size_changed",
                         "pre_len": len(a), "post_len": len(b)})
            n = min(len(a), len(b))
        else:
            n = len(a)
        bad = []
        for i in range(n):
            if a[i] != b[i]:
                if name == last_pre and a[i] == 0:
                    continue  # growth into zero padding
                bad.append(i)
                if len(bad) >= 8:
                    break
        if bad:
            # count all violating bytes
            total = sum(1 for i in range(n)
                        if a[i] != b[i] and not (name == last_pre and a[i] == 0))
            viol.append({"chunk": name, "type": "bytes_changed_in_live_data",
                         "first": bad[0], "count": total,
                         "sample": bad})
    return viol


# ---------------------------------------------------------------- hash chain
class HashChain:
    def __init__(self, seed: bytes):
        self.state = hashlib.sha256(seed).hexdigest()

    def step(self, phase_id: str, evidence: bytes) -> str:
        self.state = hashlib.sha256(
            (self.state + "|" + phase_id + "|").encode() + evidence
        ).hexdigest()
        return self.state


def sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            b = fh.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest()
