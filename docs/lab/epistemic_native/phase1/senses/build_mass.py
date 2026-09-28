#!/usr/bin/env python3
# SENSE (mechanical, judgment-free build step): tokenization + constructional
# feature codes + lexical retrieval index over the 448-item train mass.
# NO epistemic judgment here: no labels, no verdicts, no truth assessment.
# Output: mass.bin (binary, parsed by the Zag deliberation) + mass_meta.txt.
# Deterministic: fixed iteration order, no RNG, no hashing.
import re, struct, sys, hashlib

SRC = '/home/hatch/workspace/epi_a3/blind/train_blind.tsv'
OUT_BIN = '/home/hatch/workspace/epistemic_native/impl/phase1/senses/mass.bin'
OUT_META = '/home/hatch/workspace/epistemic_native/impl/phase1/senses/mass_meta.txt'

STOP = set("""a an the and or but of to in on for with is are was were be been being
it its this that these those as at by from has have had he she they we you i my
our their his her him them us yours mine theirs ours not no never n't s t d ll m
re ve do does did will would can could shall should may might must ought than
then so such very just only also too more most less least own same other another
each every all any both few many much such nor if when where which who whom whose
what how why because until while""".split())

NEG_RAW = {"not","no","never","n't","cannot","without","don't","doesn't","isn't",
"aren't","wasn't","weren't","haven't","hadn't","wouldn't","shouldn't","couldn't",
"can't","won't","ain't"}

NUMW = {"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,
"nine":9,"ten":10,"eleven":11,"twelve":12,"thirteen":13,"fourteen":14,
"fifteen":15,"sixteen":16,"seventeen":17,"eighteen":18,"nineteen":19,"twenty":20,
"thirty":30,"forty":40,"fifty":50,"sixty":60,"seventy":70,"eighty":80,
"ninety":90,"hundred":100,"thousand":1000}

EXP_RAW = {"feel","feels","felt","think","thinks","thought","love","loves","loved",
"like","likes","liked","prefer","prefers","preferred","believe","believes",
"believed","enjoy","enjoys","enjoyed","hate","hates","hated","want","wants",
"wanted","hope","hopes","hoped","wish","wishes","wished"}

ER_EXCL = {"other","either","never","ever","over","under","after","before",
"water","later","outer","inner","better","worse"}

def raw_toks(s):
    s = s.lower()
    parts = re.findall(r"[a-z0-9']+", s)
    out = []
    for p in parts:
        p = p.strip("'")
        if p: out.append(p)
    return out

def stem(w):
    # Tiny deterministic stemmer. MUST match the Zag port exactly.
    if len(w) > 4:
        if w.endswith("ies"):
            w = w[:-3] + "y"
        elif w.endswith("es") and not w.endswith("sses"):
            w = w[:-2]
        elif w.endswith("s") and not w.endswith("ss"):
            w = w[:-1]
    if len(w) > 5 and w.endswith("ed"):
        w = w[:-2]
    if len(w) > 6 and w.endswith("ing"):
        w = w[:-3]
    return w

def analyze(text):
    rt = raw_toks(text)
    st = [stem(w) for w in rt]
    content = [w for w in st if w not in STOP]
    # constructional patterns (syntax-level only), on RAW lowercased tokens.
    # (Raw, not stemmed, so the Zag port is a direct transliteration.)
    pat = 0
    # SUP: superlative syntax
    sup = False
    for t in rt:
        if t in ("best","worst"): sup = True
    for i in range(len(rt)):
        if rt[i] == "the":
            for j in range(i+1, min(len(rt), i+7)):
                if rt[j] in ("most","least"): sup = True
                if len(rt[j]) > 4 and rt[j].endswith("est"): sup = True
    if sup: pat |= 1
    # COMP: comparative syntax (... than)
    comp = False
    for j in range(len(rt)):
        if rt[j] == "than":
            for i in range(max(0, j-8), j):
                if rt[i] in ("more","less","better","worse"): comp = True
                if (len(rt[i]) > 3 and rt[i].endswith("er")
                        and rt[i] not in ER_EXCL):
                    comp = True
    if comp: pat |= 2
    # DEON: deontic modals
    if any(t in ("should","must","ought") for t in rt): pat |= 4
    # 1PEXP: first-person experiencer
    for i in range(len(rt)-1):
        if rt[i] in ("i","my") and rt[i+1] in EXP_RAW:
            pat |= 8
            break
    neg = 1 if any(t in NEG_RAW for t in rt) else 0
    nums = set()
    for t in rt:
        if re.fullmatch(r"\d+", t):
            try: nums.add(int(t))
            except: pass
        elif t in NUMW:
            nums.add(NUMW[t])
    return content, pat, neg, sorted(nums)

def main():
    items = []
    with open(SRC, 'rb') as f:
        data = f.read().decode('utf-8')
    lines = data.split('\n')
    assert lines[0].strip() == 'id\ttext', lines[0][:40]
    for ln in lines[1:]:
        if not ln.strip(): continue
        iid, text = ln.split('\t', 1)
        items.append((iid, text))
    assert len(items) == 448, len(items)

    recs = []
    index = {}  # token -> list of item idx
    for idx, (iid, text) in enumerate(items):
        content, pat, neg, nums = analyze(text)
        recs.append((iid, text, content, pat, neg, nums))
        for t in content:
            index.setdefault(t, []).append(idx)

    buf = bytearray()
    buf += b'EPI1'
    buf += struct.pack('<I', len(recs))
    # item records
    for (iid, text, content, pat, neg, nums) in recs:
        ib = iid.encode('utf-8'); tb = text.encode('utf-8')
        buf += struct.pack('<I', len(ib)) + ib
        buf += struct.pack('<I', len(tb)) + tb
        buf += struct.pack('<I', len(content))
        for t in content:
            bb = t.encode('utf-8')
            buf += struct.pack('<I', len(bb)) + bb
        buf += struct.pack('<I', pat)
        buf += struct.pack('<I', neg)
        buf += struct.pack('<I', len(nums))
        for v in nums:
            buf += struct.pack('<i', v)
    # inverted index (sorted tokens for determinism)
    toks_sorted = sorted(index.keys())
    buf += struct.pack('<I', len(toks_sorted))
    for t in toks_sorted:
        bb = t.encode('utf-8')
        posts = index[t]
        buf += struct.pack('<I', len(bb)) + bb
        buf += struct.pack('<I', len(posts))
        for p in posts:
            buf += struct.pack('<I', p)

    with open(OUT_BIN, 'wb') as f:
        f.write(bytes(buf))
    h = hashlib.sha256(bytes(buf)).hexdigest()
    with open(OUT_META, 'w') as f:
        f.write("mass.bin sha256: %s\n" % h)
        f.write("items: %d\n" % len(recs))
        f.write("distinct content tokens: %d\n" % len(toks_sorted))
        f.write("source: %s\n" % SRC)
        pc = {}
        for r in recs:
            pc[r[3]] = pc.get(r[3], 0) + 1
        f.write("pattern-flag histogram: %s\n" % sorted(pc.items()))
    print("wrote %s (%d bytes) sha256=%s" % (OUT_BIN, len(buf), h))
    print("items=%d distinct_tokens=%d" % (len(recs), len(toks_sorted)))

if __name__ == '__main__':
    main()
