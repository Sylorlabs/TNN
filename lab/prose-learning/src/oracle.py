#!/usr/bin/env python3
"""Oracle: exact implementation of the frozen PROSE-LEARNING pipeline (PREREG.md).

Used to validate the Zag binary's outputs. Serialization choices (ledger entry
layout, key_hash, digest) mirror the Zag implementation exactly.
"""
import hashlib, json, re, struct, sys

STOP = {"the","an","of","in","is","are","was","were","be","been","what","which",
"that","this","these","those","it","its","do","does","did","have","has","had",
"there","and","or","to","for","with","at","by","from","as","on","how","many",
"much","when","where","s"}

CARD = {"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,
"nine":9,"ten":10,"eleven":11,"twelve":12,"thirteen":13,"fourteen":14,
"fifteen":15,"sixteen":16,"seventeen":17,"eighteen":18,"nineteen":19,
"twenty":20,"thirty":30}
ORD = {"first":1,"second":2,"third":3,"fourth":4,"fifth":5,"sixth":6,"seventh":7,
"eighth":8,"ninth":9,"tenth":10,"eleventh":11,"twelfth":12,"thirteenth":13,
"fourteenth":14,"fifteenth":15,"sixteenth":16,"seventeenth":17,"eighteenth":18,
"nineteenth":19,"twentieth":20,"thirtieth":30}
NUMW = {**CARD, **ORD}

def tokenize(text):
    return re.findall(r"[a-z0-9]+", text.lower())

def stem(w):
    if w.endswith("ies"): return w[:-3] + "y"
    if w.endswith("ication"): return w[:-7] + "ish"
    if w.endswith("ished"): return w[:-5] + "ish"
    if w.endswith("ic") and len(w) > 5: return w[:-2]
    if w.endswith("ed") and len(w) > 4: return w[:-2]
    if w.endswith(("ches","shes","sses","xes","zes")): return w[:-2]
    if w.endswith("s") and len(w) > 3 and not w.endswith("ss"): return w[:-1]
    return w

def digit_val(tok):
    m = re.fullmatch(r"(\d+)(st|nd|rd|th)?", tok)
    return int(m.group(1)) if m else None

class Vocab:
    def __init__(self): self.ids = {}
    def intern(self, form):
        if form not in self.ids: self.ids[form] = len(self.ids)
        return self.ids[form]

def pipeline(vocab, text):
    """Returns (link, key_sorted, value_or_None, trace)."""
    toks = tokenize(text)
    link, key = [], set()
    ndig = nword = 0
    lastdig = lastword = None
    for t in toks:
        uid = vocab.intern(t)
        link.append(uid)
        dv = digit_val(t)
        if dv is not None:
            ndig += 1; lastdig = dv; continue
        if t in NUMW:
            nword += 1; lastword = NUMW[t]; continue
        if t in STOP: continue
        key.add(vocab.intern(stem(t)))
    value = lastdig if ndig else (lastword if nword else None)
    return link, sorted(key), value, (len(toks), ndig, nword)

def key_hash(key):
    return hashlib.sha256(b"".join(struct.pack("<I", u) for u in key)).digest()

def run(source, inpdir):
    vocab = Vocab()
    train = [l.rstrip("\n").split("\t", 1) for l in open(f"{inpdir}/train_{source}.txt")]
    test = [l.rstrip("\n").split("\t", 2) for l in open(f"{inpdir}/test_{source}.txt")]
    false_ids = {int(l.strip()) for l in open(f"{inpdir}/false_ids_{source}.txt")}
    facts = []  # (fact_id, key, value)
    ledger_prev = bytes(32)
    seq = 0
    terminal = None
    extract_ok = 0
    installed = {}
    for fid_s, sent in train:
        fid = int(fid_s)
        link, key, value, tr = pipeline(vocab, sent)
        if value is not None:
            extract_ok += 1
            kh = key_hash(key)
            entry = hashlib.sha256(ledger_prev + struct.pack("<Q", seq)
                                   + struct.pack("<I", fid) + kh
                                   + struct.pack("<Q", value)).digest()
            ledger_prev = entry
            terminal = entry
            facts.append((fid, key, value))
            installed[fid] = value
            seq += 1
    # probes
    answers, corrects, ties_list = [], [], []
    for pid_s, pv_s, probe in test:
        pid, pv = int(pid_s), int(pv_s)
        _, key, _, _ = pipeline(vocab, probe)
        best = None; best_id = None; ntie = 0
        kset = set(key)
        for fid, fkey, fval in facts:
            fset = set(fkey)
            inter = len(kset & fset); union = len(kset | fset)
            if best is None or inter * best[1] > best[0] * union:
                best = (inter, union); best_id = fid; ntie = 1
            elif inter * best[1] == best[0] * union:
                ntie += 1  # tie: keep lowest fact id (facts in id order)
        ans = dict((f[0], f[2]) for f in facts)[best_id]
        answers.append(ans)
        corrects.append(1 if ans == pv else 0)
        ties_list.append((pid, ntie, best_id))
    full = sum(corrects)
    clean = sum(c for (pid_s, _, _), c in zip(test, corrects) if int(pid_s) not in false_ids)
    # absorption: installed value == train sentence's stated value on false ids
    # (stated value = value scan of the train sentence; fresh vocab since the
    # scan does not depend on unit ids)
    stated = {}
    for fid_s, sent in train:
        v = pipeline(Vocab(), sent)[2]  # fresh vocab; value scan only
        stated[int(fid_s)] = v
    absorb = sum(1 for i in false_ids if installed.get(i) is not None and installed.get(i) == stated[i])
    digest = hashlib.sha256(b"".join(struct.pack("<Q", a) for a in answers) + terminal).hexdigest()
    return {
        "extract_ok": extract_ok, "full": full, "clean": clean,
        "absorb": absorb, "digest": digest,
        "ledger": terminal.hex(), "ties": ties_list,
        "answers": answers, "corrects": corrects, "installed": installed,
    }

if __name__ == "__main__":
    src = sys.argv[1]
    r = run(src, "/home/hatch/workspace/prose-learning/inputs")
    print(f"extract_ok={r['extract_ok']}/240 full={r['full']}/240 clean={r['clean']}/228 absorb={r['absorb']}/12")
    print(f"digest={r['digest']}")
    print(f"ledger={r['ledger']}")
    amb = [(p, n, b) for p, n, b in r["ties"] if n > 1]
    print(f"ambiguous_probes={len(amb)}")
    for p, n, b in amb[:40]:
        print(f"  probe {p}: {n}-way tie, winner fact {b}")
