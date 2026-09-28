#!/usr/bin/env python3
"""Oracle v2: independent Python implementation of the frozen RICH-COMPREHENSION
mechanism (Worker A's PREREG2.md; also documented in ARCHITECTURE.md).

Reads the same converted .txt inputs as the Zag binary and must produce a
byte-identical run log (INSTALL/CORROBORATE/CONTRADICT/QUARANTINE/DENIAL/
DERIVED/EXTRACT-FAIL/PROBE/SUMMARY/DIGEST/LEDGER/VERIFY/RESULT lines).

Serialization choices (ledger entry layout, key field, digest) mirror the Zag
implementation exactly. Deterministic: no RNG, no dict-order dependence.
"""
import hashlib
import struct
import sys

# ---------------------------------------------------------------- verbatim v1
STOP = {"the", "an", "of", "in", "is", "are", "was", "were", "be", "been",
        "what", "which", "that", "this", "these", "those", "it", "its", "do",
        "does", "did", "have", "has", "had", "there", "and", "or", "to", "for",
        "with", "at", "by", "from", "as", "on", "how", "many", "much", "when",
        "where", "s"}

CARD = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
        "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
        "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
        "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
        "twenty": 20, "thirty": 30}
ORD = {"first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5,
       "sixth": 6, "seventh": 7, "eighth": 8, "ninth": 9, "tenth": 10,
       "eleventh": 11, "twelfth": 12, "thirteenth": 13, "fourteenth": 14,
       "fifteenth": 15, "sixteenth": 16, "seventeenth": 17, "eighteenth": 18,
       "nineteenth": 19, "twentieth": 20, "thirtieth": 30}
NUMW = {**CARD, **ORD}


def tokenize_raw(text):
    """Raw-case tokens: maximal [A-Za-z0-9] runs, in order."""
    toks, cur = [], []
    for ch in text:
        if ("0" <= ch <= "9") or ("a" <= ch <= "z") or ("A" <= ch <= "Z"):
            cur.append(ch)
        else:
            if cur:
                toks.append("".join(cur))
                cur = []
    if cur:
        toks.append("".join(cur))
    return toks


def stem(w):
    if w.endswith("ies"):
        return w[:-3] + "y"
    if w.endswith("ication"):
        return w[:-7] + "ish"
    if w.endswith("ished"):
        return w[:-5] + "ish"
    if w.endswith("ic") and len(w) > 5:
        return w[:-2]
    if w.endswith("ed") and len(w) > 4:
        return w[:-2]
    if w.endswith(("ches", "shes", "sses", "xes", "zes")):
        return w[:-2]
    if w.endswith("s") and len(w) > 3 and not w.endswith("ss"):
        return w[:-1]
    return w


def digit_val(tok):
    import re
    m = re.fullmatch(r"(\d+)(st|nd|rd|th)?", tok)
    return int(m.group(1)) if m else None


class Vocab:
    def __init__(self):
        self.ids = {}

    def intern(self, form):
        if form not in self.ids:
            self.ids[form] = len(self.ids)
        return self.ids[form]


# ------------------------------------------------------- frozen v2 constants
EMPTY_ID = 0xFFFFFFFF
PHRASES = [["alphabet", "position"], ["letter", "count"], ["publish", "year"],
           ["come", "after"], ["come", "before"]]
PHRASE_NAMES = ["alphabet_position", "letter_count", "publication_year",
                "comes_after", "comes_before"]
HEDGE = {"think", "believe", "probably", "maybe", "perhap", "might", "could",
         "seem", "allegedly", "reportedly", "possibly", "likely", "rumor"}
NEG = {"not", "never", "no"}
VERBISH = {"isn", "don", "can", "won"}
PRONOUNS = {"it", "its", "this", "that", "these", "those"}
VERBS_2D = {"has", "have", "is", "are", "was", "were"}
ATT_NAMES = ["asserted", "hedged", "negated", "derived"]
KIND_INSTALL, KIND_CORROB, KIND_CONTRA = 1, 2, 3
KIND_QUAR, KIND_DENIAL, KIND_DERIVED = 4, 5, 6


def split_sentences(text):
    parts, cur = [], []
    for ch in text:
        if ch in ".?!":
            s = "".join(cur).strip()
            if s:
                parts.append(s)
            cur = []
        else:
            cur.append(ch)
    s = "".join(cur).strip()
    if s:
        parts.append(s)
    return parts


class Sentence:
    """Tokenized + classified sentence; mirrors the Zag token tables."""

    def __init__(self, vocab, text):
        self.vocab = vocab
        self.text = text
        self.raw = tokenize_raw(text)
        self.low = [t.lower() for t in self.raw]
        # per-token: (kind, value_or_None, stem_or_None, stem_uid_or_None, raw_uid)
        self.toks = []
        for t in self.low:
            raw_uid = vocab.intern(t)
            dv = digit_val(t)
            if dv is not None:
                self.toks.append(("digit", dv, None, None, raw_uid))
                continue
            if t in NUMW:
                self.toks.append(("numword", NUMW[t], None, None, raw_uid))
                continue
            if t in STOP:
                self.toks.append(("stop", None, None, None, raw_uid))
                continue
            st = stem(t)
            suid = vocab.intern(st)
            self.toks.append(("content", None, st, suid, raw_uid))
        # content token indices in order
        self.cpos = [i for i, k in enumerate(self.toks) if k[0] == "content"]

    def stemmed_at(self, i):
        return self.toks[i][2]

    def stem_uid_at(self, i):
        return self.toks[i][3]


def phrase_scan(sent, min_tokidx=-1):
    """Earliest-start phrase match over the stemmed content-token sequence;
    ties broken by frozen phrase list order. Returns (phidx, tok_start, tok_end)
    or (None, None, None)."""
    best = None
    for ci, ti in enumerate(sent.cpos):
        if ti <= min_tokidx:
            continue
        for phidx, ph in enumerate(PHRASES):
            ok = True
            for k, pw in enumerate(ph):
                if ci + k >= len(sent.cpos):
                    ok = False
                    break
                if sent.stemmed_at(sent.cpos[ci + k]) != pw:
                    ok = False
                    break
            if ok:
                cand = (ti, phidx)
                if best is None or cand < best:
                    best = cand
    if best is None:
        return None, None, None
    ti, phidx = best
    ci = sent.cpos.index(ti)
    return phidx, ti, sent.cpos[ci + len(PHRASES[phidx]) - 1]


def tag_entity(vocab, sent, prev):
    """Returns (ent_tokens, eid, canon, coref). prev = (eid, canon, stem_uids) or None."""
    low = sent.low
    # 2a: double-quoted span
    q1 = sent.text.find('"')
    if q1 >= 0:
        q2 = sent.text.find('"', q1 + 1)
        if q2 > q1:
            # token offsets in the sentence string
            offs = []
            i = 0
            for t in sent.raw:
                j = sent.text.find(t, i)
                offs.append((j, j + len(t)))
                i = j + len(t)
            span = [low[k] for k, (a, b) in enumerate(offs) if a > q1 and b <= q2]
            if span:
                canon = " ".join(span)
                return span, vocab.intern(canon), canon, False
    # 2b: single uppercase letter
    for k, t in enumerate(sent.raw):
        if len(t) == 1 and "A" <= t <= "Z":
            return [low[k]], vocab.intern(low[k]), low[k], False
    # 2c: [relation phrase] ... "of" X -> X. The parenthetical example
    # ("the alphabet position of M" -> M) is authoritative: the entity FOLLOWS
    # "of", which follows the phrase. First phrase occurrence (same as relation
    # tagging); first "of" after the phrase end; first <=4 content tokens after;
    # if none, the first word-token (stopwords allowed, digits never -- a digit
    # is the value, not the entity). If any link of that chain is missing, 2c
    # does not fire (fall through).
    phidx, ts, te = phrase_scan(sent)
    if phidx is not None:
        of_idx = next((k for k in range(te + 1, len(low)) if low[k] == "of"), None)
        if of_idx is not None:
            after = [low[k] for k in range(of_idx + 1, len(low))
                     if sent.toks[k][0] == "content"][:4]
            if not after:
                after = [low[k] for k in range(of_idx + 1, len(low))
                         if sent.toks[k][0] != "digit"][:1]
            if after:
                canon = " ".join(after)
                return after, vocab.intern(canon), canon, False
    # 2d: leading content tokens before has/have/is/are/was/were (max 4)
    v_idx = next((k for k, t in enumerate(low) if t in VERBS_2D), None)
    if v_idx is not None:
        lead = [low[k] for k in range(v_idx) if sent.toks[k][0] == "content"][:4]
        if lead:
            canon = " ".join(lead)
            return lead, vocab.intern(canon), canon, False
    # rule 6: coref (only when 2a-2d yielded EMPTY)
    trig = any(t in PRONOUNS for t in low)
    if not trig:
        for k in range(len(low) - 1):
            if low[k] == "the" and low[k + 1] in ("word", "letter"):
                trig = True
                break
    if trig and prev is not None and prev[0] != EMPTY_ID:
        return prev[2], prev[0], prev[1], True
    return [], EMPTY_ID, "EMPTY", False


def tag_relation(vocab, sent, ent_tokens):
    """Returns (relkind, sorted_uid_list, ph_tok_start, ph_tok_end).
    relkind 0..4 = frozen phrase, 5 = open."""
    phidx, ts, te = phrase_scan(sent)
    if phidx is not None:
        ci = sent.cpos.index(ts)
        uids = sorted(sent.stem_uid_at(sent.cpos[ci + k]) for k in range(len(PHRASES[phidx])))
        return phidx, uids, ts, te
    ent_stems = {stem(t) for t in ent_tokens}
    seen, uids = set(), []
    for ti in sent.cpos:
        st = sent.stemmed_at(ti)
        if st in ent_stems:
            continue
        u = sent.stem_uid_at(ti)
        if u not in seen:
            seen.add(u)
            uids.append(u)
    return 5, sorted(uids), None, None


def scan_value(sent):
    # frozen reading: the value token recorded in the role trace is the token
    # that determined the value (last digit-token if any, else last
    # number-word) -- not merely the last number-like token scanned.
    lastdig = lastword = None
    dtok = wtok = ""
    for k, (kind, v, st, suid, ruid) in enumerate(sent.toks):
        if kind == "digit":
            lastdig, dtok = v, sent.low[k]
        elif kind == "numword":
            lastword, wtok = v, sent.low[k]
    if lastdig is not None:
        return True, lastdig, dtok
    if lastword is not None:
        return True, lastword, wtok
    return False, 0, ""


def scan_attitude(sent):
    neg = hedge = False
    for k, (kind, v, st, suid, ruid) in enumerate(sent.toks):
        if kind != "content":
            continue
        if st in NEG:
            neg = True
        elif st == "t" and k > 0 and sent.low[k - 1] in VERBISH:
            neg = True
        elif st in HEDGE:
            hedge = True
    if neg:
        return 2
    if hedge:
        return 1
    return 0


def rel_hash(uids):
    return hashlib.sha256(b"".join(struct.pack("<I", u) for u in uids)).digest()


class Learner:
    def __init__(self):
        self.vocab = Vocab()
        # v1 first-seen interning: nothing is pre-interned. The alphabet/position
        # hash is resolved lazily at inference time.
        self.alphapos_hash = None
        self.asserted = []   # dicts: eid, relhash, relids, value, status(0/1), fid, seq
        self.quar = []       # eid, relhash, value, fid
        self.denial = []     # eid, relhash, value, fid
        self.comes = []      # (fid, xeid, xcanon, yeid, ycanon, direction)
        self.ledger_prev = bytes(32)
        self.seq = 0
        self.lg = []         # per-seq records for chain re-verification
        self.lines = []
        self.n = {"install": 0, "corrob": 0, "contra": 0, "quar": 0,
                  "denial": 0, "derived": 0, "fail": 0}

    # -- ledger --
    def trace(self, eid, relids, vtok, att, coref, extra=""):
        r = ",".join(str(u) for u in relids)
        return f"ent={eid}|rel={r}|val={vtok}|att={att}|coref={int(coref)}{extra}"

    def ledger_add(self, kind, fid, eid, relhash, value, att, trace):
        tb = trace.encode()
        entry = (self.ledger_prev + struct.pack("<Q", self.seq)
                 + struct.pack("<I", fid) + struct.pack("B", kind)
                 + struct.pack("<I", eid) + relhash
                 + struct.pack("<q", value) + struct.pack("B", att)
                 + struct.pack("<I", len(tb)) + tb)
        digest = hashlib.sha256(entry).digest()
        self.lg.append((kind, fid, eid, relhash, value, att, tb))
        self.ledger_prev = digest
        sq = self.seq
        self.seq += 1
        return sq

    def find_asserted(self, eid, relhash):
        for i, r in enumerate(self.asserted):
            if r["eid"] == eid and r["relhash"] == relhash:
                return i
        return -1

    def keystr(self, eid, relhash):
        return f"{eid}:{relhash[:4].hex()}"

    # -- install --
    def install(self, fid, s_idx, sent, ent_tokens, eid, canon, relkind,
                relids, value, vtok, att, coref):
        rh = rel_hash(relids)
        ks = self.keystr(eid, rh)
        rname = PHRASE_NAMES[relkind] if relkind < 5 else "open"
        aname = ATT_NAMES[att]
        tr = self.trace(eid, relids, vtok, att, coref)
        if att == 1:
            if not any(q["eid"] == eid and q["relhash"] == rh for q in self.quar):
                self.quar.append({"eid": eid, "relhash": rh, "value": value, "fid": fid})
            sq = self.ledger_add(KIND_QUAR, fid, eid, rh, value, att, tr)
            self.lines.append(f"QUARANTINE id={fid} sent={s_idx} entity={canon} "
                              f"relation={rname} reln={len(relids)} value={value} key={ks} seq={sq}")
            self.n["quar"] += 1
            return
        if att == 2:
            if not any(d["eid"] == eid and d["relhash"] == rh for d in self.denial):
                self.denial.append({"eid": eid, "relhash": rh, "value": value, "fid": fid})
            sq = self.ledger_add(KIND_DENIAL, fid, eid, rh, value, att, tr)
            self.lines.append(f"DENIAL id={fid} sent={s_idx} entity={canon} "
                              f"relation={rname} reln={len(relids)} value={value} key={ks} seq={sq}")
            self.n["denial"] += 1
            return
        i = self.find_asserted(eid, rh)
        if i < 0:
            self.asserted.append({"eid": eid, "relhash": rh, "relids": list(relids),
                                  "value": value, "status": 0, "fid": fid, "seq": self.seq})
            sq = self.ledger_add(KIND_INSTALL, fid, eid, rh, value, att, tr)
            self.lines.append(f"INSTALL id={fid} sent={s_idx} entity={canon} "
                              f"relation={rname} reln={len(relids)} attitude={aname} "
                              f"value={value} key={ks} seq={sq}")
            self.n["install"] += 1
            return
        row = self.asserted[i]
        if row["status"] == 0 and row["value"] == value:
            sq = self.ledger_add(KIND_CORROB, fid, eid, rh, value, att, tr)
            self.lines.append(f"CORROBORATE id={fid} sent={s_idx} key={ks} "
                              f"attitude={aname} seq={sq}")
            self.n["corrob"] += 1
            return
        if row["status"] == 0:
            row["status"] = 1
            sq = self.ledger_add(KIND_CONTRA, fid, eid, rh, value, att, tr)
            self.lines.append(f"CONTRADICT id={fid} sent={s_idx} key={ks} "
                              f"attitude={aname} old={row['value']} new={value} seq={sq}")
            self.n["contra"] += 1
            return
        # already contradicted: no-op

    def process_sentence(self, fid, s_idx, sent, prev, is_probe=False):
        ent_tokens, eid, canon, coref = tag_entity(self.vocab, sent, prev)
        relkind, relids, ts, te = tag_relation(self.vocab, sent, ent_tokens)
        ok, value, vtok = scan_value(sent)
        att = scan_attitude(sent)
        new_prev = (eid, canon, list(ent_tokens))
        if is_probe:
            return {"eid": eid, "canon": canon, "relkind": relkind, "relids": relids}
        if relkind in (3, 4) and att == 0 and ts is not None:
            # target entity: first <=4 content tokens after the phrase
            ci = sent.cpos.index(ts)
            ys = []
            for kk in range(ci + len(PHRASES[relkind]), len(sent.cpos)):
                ys.append(sent.low[sent.cpos[kk]])
                if len(ys) == 4:
                    break
            if ys:
                ycanon = " ".join(ys)
                yeid = self.vocab.intern(ycanon)
                self.comes.append((fid, eid, canon, yeid, ycanon,
                                   1 if relkind == 3 else -1))
        if not ok:
            self.lines.append(f"EXTRACT-FAIL id={fid} sent={s_idx}")
            self.n["fail"] += 1
            return {"prev": new_prev}
        self.install(fid, s_idx, sent, ent_tokens, eid, canon, relkind,
                     relids, value, vtok, att, coref)
        return {"prev": new_prev}

    def train_item(self, fid, text):
        prev = None
        for s_idx, s in enumerate(split_sentences(text)):
            sent = Sentence(self.vocab, s)
            r = self.process_sentence(fid, s_idx, sent, prev)
            prev = r["prev"]

    def inference(self):
        if self.alphapos_hash is None:
            self.alphapos_hash = rel_hash(sorted(
                self.vocab.intern(s) for s in ("alphabet", "position")))
        for _ in range(10000):
            changed = False
            for fid, xeid, xcanon, yeid, ycanon, direction in self.comes:
                i = self.find_asserted(yeid, self.alphapos_hash)
                if i < 0 or self.asserted[i]["status"] != 0:
                    continue
                n = self.asserted[i]["value"]
                v = n + direction
                rh = self.alphapos_hash
                relids = sorted(self.vocab.intern(s) for s in ("alphabet", "position"))
                tr = self.trace(xeid, relids, "derived", 3, False,
                                f"|rule={'comes_after' if direction == 1 else 'comes_before'}"
                                f"|prem={yeid}:{n}")
                j = self.find_asserted(xeid, rh)
                if j < 0:
                    self.asserted.append({"eid": xeid, "relhash": rh, "relids": relids,
                                          "value": v, "status": 0, "fid": fid, "seq": self.seq})
                    sq = self.ledger_add(KIND_DERIVED, fid, xeid, rh, v, 3, tr)
                    self.lines.append(f"DERIVED id={fid} rule="
                                      f"{'comes_after' if direction == 1 else 'comes_before'} "
                                      f"entity={xcanon} prem={yeid}:{n} value={v} seq={sq}")
                    self.n["derived"] += 1
                    changed = True
                else:
                    row = self.asserted[j]
                    if row["status"] == 0 and row["value"] == v:
                        sq = self.ledger_add(KIND_CORROB, fid, xeid, rh, v, 3, tr)
                        self.lines.append(f"CORROBORATE id={fid} sent=-1 key="
                                          f"{self.keystr(xeid, rh)} attitude=derived seq={sq}")
                        self.n["corrob"] += 1
                    elif row["status"] == 0:
                        row["status"] = 1
                        sq = self.ledger_add(KIND_CONTRA, fid, xeid, rh, v, 3, tr)
                        self.lines.append(f"CONTRADICT id={fid} sent=-1 key="
                                          f"{self.keystr(xeid, rh)} attitude=derived "
                                          f"old={row['value']} new={v} seq={sq}")
                        self.n["contra"] += 1
                        changed = True
            if not changed:
                break

    # -- probe --
    @staticmethod
    def jaccard(a, b):
        sa, sb = set(a), set(b)
        inter = len(sa & sb)
        union = len(sa | sb)
        if union == 0:
            return 0, 1  # defined as 0
        return inter, union

    def probe(self, pid, probe_text, expect):
        sent = Sentence(self.vocab, probe_text)
        r = self.process_sentence(pid, 0, sent, None, is_probe=True)
        eid, canon, relkind, relids = r["eid"], r["canon"], r["relkind"], r["relids"]
        rh = rel_hash(relids)
        rname = PHRASE_NAMES[relkind] if relkind < 5 else "open"
        verdict, vval, ties = None, 0, 0
        i = self.find_asserted(eid, rh)
        if i >= 0 and self.asserted[i]["status"] == 0:
            verdict, vval, ties = f"VALUE:{self.asserted[i]['value']}", self.asserted[i]["value"], 1
        elif i >= 0:
            verdict, ties = "CONTRADICTION", 0
        elif any(q["eid"] == eid and q["relhash"] == rh for q in self.quar):
            verdict, ties = "HEDGED", 0
        elif any(d["eid"] == eid and d["relhash"] == rh for d in self.denial):
            verdict, ties = "UNKNOWN", 0
        else:
            cands = [f for f in self.asserted
                     if f["status"] == 0 and (eid == EMPTY_ID or f["eid"] == eid)]
            best = None  # (inter, union, -fid)
            ntie = 0
            for f in cands:
                inter, union = self.jaccard(relids, f["relids"])
                if eid == EMPTY_ID and not (union > 0 and 2 * inter >= union):
                    continue
                key = (inter, union, f["fid"])
                if best is None or inter * best[1] > best[0] * union or \
                   (inter * best[1] == best[0] * union and f["fid"] < best[2]):
                    best = (inter, union, f["fid"])
                    ntie = 1
                    bv = f["value"]
                elif inter * best[1] == best[0] * union:
                    ntie += 1
            if best is None:
                verdict, ties = "UNKNOWN", 0
            else:
                verdict, vval, ties = f"VALUE:{bv}", bv, ntie
        exp = str(expect)
        want = f"VALUE:{exp}" if exp.lstrip("-").isdigit() else exp
        ok = 1 if verdict == want else 0
        self.lines.append(f"PROBE id={pid} verdict={verdict} expected={exp} ok={ok} "
                          f"entity={canon} relation={rname} reln={len(relids)} "
                          f"attitude=ignored ties={ties}")
        return verdict, vval, ok

    def digest(self, verdicts):
        vb = b""
        for code, val in verdicts:
            vb += struct.pack("B", code)
            if code == 0:
                vb += struct.pack("<q", val)
        return hashlib.sha256(vb + self.ledger_prev).hexdigest()

    def verify_chain(self):
        prev = bytes(32)
        for seq, (kind, fid, eid, relhash, value, att, tb) in enumerate(self.lg):
            entry = (prev + struct.pack("<Q", seq)
                     + struct.pack("<I", fid) + struct.pack("B", kind)
                     + struct.pack("<I", eid) + relhash
                     + struct.pack("<q", value) + struct.pack("B", att)
                     + struct.pack("<I", len(tb)) + tb)
            prev = hashlib.sha256(entry).digest()
        return 1 if prev == self.ledger_prev else 0


def run(source, inpdir):
    L = Learner()
    train = [l.rstrip("\n").split("\t", 1) for l in open(f"{inpdir}/train_{source}.txt")]
    test = [l.rstrip("\n").split("\t", 3) for l in open(f"{inpdir}/test_{source}.txt")]
    false_ids = {int(l.strip()) for l in open(f"{inpdir}/false_ids_{source}.txt")}
    for fid_s, text in train:
        L.train_item(int(fid_s), text)
    L.inference()
    verdicts, oks = [], []
    for pid_s, pv_s, probe, expect in test:
        v, val, ok = L.probe(int(pid_s), probe, expect)
        code = {"VALUE": 0, "CONTRADICTION": 1, "HEDGED": 2, "UNKNOWN": 3}[v.split(":")[0]]
        verdicts.append((code, val))
        oks.append((int(pid_s), ok))
    full = sum(o for _, o in oks)
    clean = sum(o for p, o in oks if p not in false_ids)
    ncl = len(test) - len(false_ids)
    d1 = L.digest(verdicts)
    d2 = L.digest(verdicts)
    chok = L.verify_chain()
    n = L.n
    L.lines.append(f"SUMMARY ninstall={n['install']} ncorroborate={n['corrob']} "
                   f"ncontradict={n['contra']} nquarantine={n['quar']} ndenial={n['denial']} "
                   f"nderived={n['derived']} nfail={n['fail']} nprobe={len(test)} "
                   f"full={full}/{len(test)} clean={clean}/{ncl}")
    L.lines.append(f"DIGEST {d1}")
    L.lines.append(f"DIGEST2 {d2}")
    L.lines.append(f"LEDGER {L.ledger_prev.hex()}")
    L.lines.append(f"VERIFY chain={chok} dmatch={1 if d1 == d2 else 0}")
    ok_all = chok == 1 and d1 == d2
    L.lines.append(f"RESULT {'PASS' if ok_all else 'FAIL'}")
    return L


if __name__ == "__main__":
    src = sys.argv[1]
    indir = sys.argv[2] if len(sys.argv) > 2 else "/home/hatch/workspace/richcomp/inputs"
    L = run(src, indir)
    print(f"PROSE-LEARN2 source={src}")
    print("\n".join(L.lines))
