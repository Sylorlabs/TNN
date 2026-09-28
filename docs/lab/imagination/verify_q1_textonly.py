#!/usr/bin/env python3
"""Q1 text-only control: lookup-only baseline over q1_procedures.txt.

The baseline may answer a question ONLY if its expected answer appears
VERBATIM in the procedure text (digits, or number words zero..twenty
normalized to digits). Anything requiring aggregation over elements
(counts, max/min, relations, pairs, chain following, contour, intervals)
is unanswerable by lookup -> "unknown" -> wrong.

Scored against the same expected-answer set as verify_imag.py.
Frozen guard: procedure text without the partition must score < 12/36.
"""
import re, sys
sys.path.insert(0, '/home/hatch/workspace/tnn-lab/imagination')
import verify_imag as V

# NOTE: 'one' is deliberately excluded: in these texts it occurs only as a
# pronoun ("a low-mid one", "that one"), never as the numeral 1. Counting it
# would credit answers the text does not state. 'zero' never occurs.
WORDS = {'zero':0,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,
         'eight':8,'nine':9,'ten':10,'eleven':11,'twelve':12,'thirteen':13,
         'fourteen':14,'fifteen':15,'sixteen':16,'seventeen':17,'eighteen':18,
         'nineteen':19,'twenty':20}

def load_procedures(path):
    texts = {}
    mode = scene = None
    buf = []
    def flush():
        if mode is not None and buf:
            texts[(mode, scene)] = ' '.join(buf)
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('# '):
                continue
            m = re.match(r'## MODE (\d) \(.*\) — scene (\d+)', line)
            if m:
                flush()
                mode, scene, buf = int(m.group(1)), int(m.group(2)), []
            elif line.startswith('#'):
                continue
            else:
                buf.append(line)
    flush()
    return texts

def numbers_in(text):
    nums = set()
    for d in re.findall(r'\b\d+\b', text):
        nums.add(int(d))
    for w in re.findall(r'[a-z]+', text.lower()):
        if w in WORDS:
            nums.add(WORDS[w])
    return nums

def main():
    texts = load_procedures('/home/hatch/workspace/tnn-lab/imagination/q1_procedures.txt')
    assert len(texts) == 24, f"expected 24 paragraphs, got {len(texts)}"
    for mode in (0, 1):
        exp = V.expected(mode)
        ok = tot = 0
        hits = []
        for (scene, qid), ans in sorted(exp.items()):
            nums = numbers_in(texts[(mode, scene)])
            if isinstance(ans, tuple):
                answered = all(a in nums for a in ans)
            else:
                answered = ans in nums
            tot += 1
            if answered:
                ok += 1
                hits.append(((scene, qid), ans))
        mname = 'MACHINE' if mode == 0 else 'HUMAN'
        print(f"{mname}: text-only lookup baseline {ok}/{tot} (bar: <12/36)")
        for (s, q), a in hits:
            print(f"   hit: scene {s} q{q} answer={a} appears verbatim")
    print("guard: <12/36 per mode")

if __name__ == '__main__':
    main()
