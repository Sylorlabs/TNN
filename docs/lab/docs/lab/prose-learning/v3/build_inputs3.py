#!/usr/bin/env python3
"""Build v3 inputs: dense-phrasing championship train sets (3 wordings/fact)
+ fixed NEG battery. Deterministic. Every generated wording is verified:
value-scan == probe_value, single sentence, != original.

Reads v2 championship JSONs from ../../prose-learning/inputs/.
Writes v3/inputs3/{train,test,false_ids}_<s>.txt and sub-battery txt files.
"""
import json, os, re, sys, hashlib

INPD = os.path.expanduser('~/workspace/tnn-lab/prose-learning/inputs')
IN2 = os.path.expanduser('~/workspace/tnn-lab/prose-learning/v2/inputs2')
OUTD = os.path.expanduser('~/workspace/tnn-lab/prose-learning/v3/inputs3')
SRC = ['grok', 'sol', 'step', 'muse-native']

CARD = {"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,
        "nine":9,"ten":10,"eleven":11,"twelve":12,"thirteen":13,"fourteen":14,
        "fifteen":15,"sixteen":16,"seventeen":17,"eighteen":18,"nineteen":19,
        "twenty":20,"thirty":30}
ORD = {"first":1,"second":2,"third":3,"fourth":4,"fifth":5,"sixth":6,"seventh":7,
       "eighth":8,"ninth":9,"tenth":10,"eleventh":11,"twelfth":12,"thirteenth":13,
       "fourteenth":14,"fifteenth":15,"sixteenth":16,"seventeenth":17,
       "eighteenth":18,"nineteenth":19,"twentieth":20,"thirtieth":30}
NUMW = {**CARD, **ORD}

def tokens(text):
    return re.findall(r'[A-Za-z0-9]+', text)

def value_scan(text):
    """v2 value rule: last digit-token wins, else last number-word, else None."""
    last_digit = None
    last_word = None
    for t in tokens(text):
        m = re.fullmatch(r'(\d+)(st|nd|rd|th)?', t)
        if m:
            last_digit = int(m.group(1))
        elif t.lower() in NUMW:
            last_word = NUMW[t.lower()]
    return last_digit if last_digit is not None else last_word

def single_sentence(t):
    return not re.search(r'[.?!]', t.rstrip('.').rstrip())

def clean_article(e):
    for a in ('The ', 'A ', 'An ', 'Each '):
        if e.startswith(a):
            return a.lower() + e[len(a):]
    return e[0].lower() + e[1:] if e else e

# ---------------------------------------------------------------- extractors
def extract_alpha(t, n):
    m = re.search(r'(?<![A-Za-z])([A-Z])(?![A-Za-z])', t)
    if not m:
        return None
    L = m.group(1)
    return [f"{L} has an alphabet position of {n}.",
            f"The alphabet position of {L} is {n}.",
            f"The letter {L} stands at alphabet position {n}."]

def extract_wordlen(t, n):
    m = re.search(r'"([^"]+)"', t) or re.search(r'\u201c([^\u201d]+)\u201d', t)
    if m:
        w = m.group(1)
    else:
        m2 = re.search(r'[Ww]ord (\w+) has', t)
        if m2:
            w = m2.group(1)
        else:
            m3 = re.match(r'^The letter count of (\w+) is \d+\.$', t)
            if not m3:
                return None
            w = m3.group(1)
    return [f'The word "{w}" has a letter count of {n}.',
            f'The letter count of "{w}" is {n}.',
            f'"{w}" contains {n} letters.']

def extract_pubyear(t, n):
    m = (re.match(r'^(.*?) has a publication year of \d+\.$', t)
         or re.match(r'^The publication year of (.*?) is \d+\.$', t)
         or re.match(r'^(.*?) was published in \d+\.$', t))
    if not m:
        return None
    T = m.group(1)
    return [f"{T} has a publication year of {n}.",
            f"The publication year of {T} is {n}.",
            f"{T} was published in {n}."]

def open_frames(U, E, N):
    """Three canonical frames given unit-phrase U, entity E (or None), value N."""
    if E is None:
        return [f"The count of {U} is {N}.",
                f"There are {N} {U} in total.",
                f"The number of {U} stands at {N}."]
    Ec = clean_article(E)
    return [f"The count of {U} in {Ec} is {N}.",
            f"There are {N} {U} in {Ec}.",
            f"{E} has {N} {U}."]

def unit_from_entity(E):
    """Derive a unit noun from an entity like 'The labors of Hercules'."""
    e = E
    m = re.search(r'^(?:The |A |An )?(\w+) of ', e)
    if m:
        return m.group(1).lower(), re.sub(r'^(?:The |A |An )?(\w+) of ', '', e)
    m = re.search(r'^(?:The |A |An )?(\w+) in ', e)
    if m:
        return m.group(1).lower(), re.sub(r'^(?:The |A |An )?(\w+) in ', '', e)
    w = e.split()
    last = w[-1].lower().rstrip('.')
    return last, None  # None -> caller treats as redundant -> E=None frames

def extract_open(t, n):
    m = re.match(r'^The (?:count|number) of (.+?) (in|of) (.*?) (?:is|stands at) (\d+)\.$', t)
    if m:
        return open_frames(m.group(1), m.group(3), n)
    m = re.match(r'^The (?:count|number) of (.*?) (?:is|stands at) (\d+)\.$', t)
    if m:
        return open_frames(m.group(1), None, n)
    m = re.match(r'^Records give the number of (.+?) in (.*?) as (\d+)\.$', t)
    if m:
        return open_frames(m.group(1), m.group(2), n)
    m = re.match(r'^Records give the number of (.*?) as (\d+)\.$', t)
    if m:
        return open_frames(m.group(1), None, n)
    m = re.match(r'^(.*?) has a count of (\d+) (\S+)\.$', t)
    if m:
        return open_frames(m.group(3), m.group(1), n)
    m = re.match(r'^(.*?) has (\d+) (.+?)( on the (?:field|court))?\.$', t)
    if m:
        E, N2, U, tail = m.group(1), m.group(2), m.group(3), m.group(4) or ''
        assert int(N2) == n, (t, n)
        Ec = clean_article(E)
        return [f"The count of {U} in {Ec}{tail} is {n}.",
                f"There are {n} {U} in {Ec}{tail}.",
                f"{E}{tail} has {n} {U}."]
    m = re.match(r'^There are (\d+) (.*?) in (.*?)\.$', t)
    if m:
        return open_frames(m.group(2), m.group(3), n)
    m = re.match(r'^There are (\d+) (.*?) of (.*?)\.$', t)
    if m:
        return open_frames(m.group(2), m.group(3), n)
    m = re.match(r'^There are (\d+) (.*?)\.$', t)
    if m:
        return open_frames(m.group(2), None, n)
    m = re.match(r'^(.*?) (?:consists of|contains) (\d+) (.*?)\.$', t)
    if m:
        return open_frames(m.group(3), m.group(1), n)
    m = re.match(r'^([A-Z]) is the (\d+)(?:st|nd|rd|th) letter of (.*?)\.$', t)
    if m:
        return extract_alpha(t, n)
    m = re.match(r'^The word (\w+) has (\d+) letters\.$', t)
    if m:
        return extract_wordlen(t, n)
    m = re.match(r'^"([^"]+)" contains (\d+) letters\.$', t)
    if m:
        return extract_wordlen(t, n)
    m = re.match(r'^(.*?) have a count of (\d+)\.$', t)
    if m:
        E = m.group(1)
        U, E2 = unit_from_entity(E)
        if E2 is None:
            # redundant (unit == head noun): use E=None frames with U
            return open_frames(U, None, n)
        return open_frames(U, E2, n)
    m = re.match(r'^(.*?) have (\d+) (.*?)\.$', t)
    if m:
        return open_frames(m.group(3), m.group(1), n)
    return None

def categorize(t):
    tl = t.lower()
    if 'alphabet position' in tl:
        return 'alpha'
    if 'letter count' in tl:
        return 'wordlen'
    if 'publication year' in tl or 'published' in tl:
        return 'pubyear'
    return 'open'

def paraphrases(t, n):
    cat = categorize(t)
    if cat == 'alpha':
        cands = extract_alpha(t, n)
    elif cat == 'wordlen':
        cands = extract_wordlen(t, n)
    elif cat == 'pubyear':
        cands = extract_pubyear(t, n)
    else:
        cands = extract_open(t, n)
    return cands

# ---------------------------------------------------------------- build
def main():
    os.makedirs(OUTD, exist_ok=True)
    report = []
    for s in SRC:
        train = json.loads(open(f'{INPD}/train_{s}.jsonl').read().strip())
        test = json.loads(open(f'{INPD}/test_{s}.jsonl').read().strip())
        false_facts = set(int(x) for x in open(f'{INPD}/false_ids_{s}.txt'))
        pv = {o['id']: o['probe_value'] for o in test}
        tmap = {o['id']: o.get('sentence', o.get('text', '')) for o in train}
        n_full = 0
        n_fallback = 0
        fallback_ids = []
        with open(f'{OUTD}/train_{s}.txt', 'w') as f:
            for fid in range(240):
                orig = tmap[fid]
                n = pv[fid]
                assert n is not None, (s, fid)
                cands = paraphrases(orig, n)
                wordings = [orig]
                if cands:
                    for c in cands:
                        if c != orig and c not in wordings:
                            if value_scan(c) == n and single_sentence(c):
                                wordings.append(c)
                        if len(wordings) == 3:
                            break
                if len(wordings) == 3:
                    n_full += 1
                else:
                    n_fallback += 1
                    fallback_ids.append(fid)
                    while len(wordings) < 3:
                        wordings.append(orig)  # documented fallback: repeat
                for w_i, w in enumerate(wordings):
                    f.write(f"{fid*3+w_i}\t{w}\n")
        # test: unchanged probes, original ids
        with open(f'{OUTD}/test_{s}.txt', 'w') as f:
            for o in test:
                pv_s = o['probe_value']
                exp = o.get('expect', pv_s)
                f.write(f"{o['id']}\t{pv_s}\t{o['probe']}\t{exp}\n")
        # false ids: all 3 train ids per false fact
        with open(f'{OUTD}/false_ids_{s}.txt', 'w') as f:
            for fid in sorted(false_facts):
                for w_i in range(3):
                    f.write(f"{fid*3+w_i}\n")
        report.append((s, n_full, n_fallback, fallback_ids))
    for s, nf, nb, fb in report:
        print(f"{s}: {nf}/240 facts with 3 distinct wordings, {nb} fallback (repeat original): {fb[:12]}{'...' if len(fb)>12 else ''}")

    # ---- fixed NEG battery
    neg_test = [json.loads(l) for l in open(f'{IN2}/sub_neg_test.jsonl')]
    neg_train = [json.loads(l) for l in open(f'{IN2}/sub_neg_train.jsonl')]
    fixed = 0
    for o in neg_test:
        if o['id'] == 18:
            o['probe'] = 'How many members are in the "Beatles"?'
            fixed += 1
        elif o['id'] == 19:
            o['probe'] = 'How many members are in the "Jackson 5"?'
            fixed += 1
    probes = [o['probe'] for o in neg_test]
    assert len(set(probes)) == len(probes), "duplicate probe strings remain!"
    os.makedirs(f'{OUTD}/negfix', exist_ok=True)
    with open(f'{OUTD}/negfix/sub_neg_train.jsonl', 'w') as f:
        for o in neg_train:
            f.write(json.dumps(o) + '\n')
    with open(f'{OUTD}/negfix/sub_neg_test.jsonl', 'w') as f:
        for o in neg_test:
            f.write(json.dumps(o) + '\n')
    print(f"NEG battery rebuilt: {fixed} probes rephrased, {len(neg_test)} probes all-unique strings")

    def loadjl(path):
        return [json.loads(l) for l in open(path)]

    # ---- convert sub-batteries (v2 frozen + negfix) to txt
    for name in ['sub_para', 'sub_contr', 'sub_hedge', 'sub_multi', 'sub_core', 'sub_distr']:
        tr = loadjl(f'{IN2}/{name}_train.jsonl')
        te = loadjl(f'{IN2}/{name}_test.jsonl')
        with open(f'{OUTD}/{name}_train.txt', 'w') as f:
            for r in tr:
                text = r.get('text', r.get('sentence', '')).replace('\t', ' ')
                f.write(f"{r['id']}\t{text}\n")
        with open(f'{OUTD}/{name}_test.txt', 'w') as f:
            for r in te:
                pv_s = r['probe_value']
                exp = r.get('expect', pv_s)
                f.write(f"{r['id']}\t{pv_s}\t{r['probe']}\t{exp}\n")
    for name in ['sub_neg']:
        tr = loadjl(f'{OUTD}/negfix/{name}_train.jsonl')
        te = loadjl(f'{OUTD}/negfix/{name}_test.jsonl')
        with open(f'{OUTD}/{name}_train.txt', 'w') as f:
            for r in tr:
                text = r.get('text', r.get('sentence', '')).replace('\t', ' ')
                f.write(f"{r['id']}\t{text}\n")
        with open(f'{OUTD}/{name}_test.txt', 'w') as f:
            for r in te:
                pv_s = r['probe_value']
                exp = r.get('expect', pv_s)
                f.write(f"{r['id']}\t{pv_s}\t{r['probe']}\t{exp}\n")
    print("sub-battery txt files written")
    # checksums
    for fn in sorted(os.listdir(OUTD)):
        p = os.path.join(OUTD, fn)
        if os.path.isfile(p):
            h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
            print(f"sha256 {fn} {h}")

if __name__ == '__main__':
    main()
