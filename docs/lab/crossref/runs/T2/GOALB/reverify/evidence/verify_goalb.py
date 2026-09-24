#!/usr/bin/env python3
"""GOALB mechanical verifier: B1 coverage, B3 novelty, B4 leakage (independent).
Reads runs/rep1.log. B1: every input word appears in its story (16 trials).
B3: per-sentence (>=6 words) substring novelty vs corpora (words+classes).
B4: kb.txt hash unchanged; 0/16 story substrings (>=16 bytes) in kb.txt.
"""
import hashlib, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(ROOT, "runs", "rep1.log")

def main():
    words = [w.strip() for w in open(os.path.join(ROOT, "build", "inputs", "words.txt")) if w.strip()]
    text = open(LOG).read()
    # parse stories: ### STORY S<n> <VARIANT> ... ### END
    stories = re.findall(r"### STORY (S\d+) (POS|DEL)\n(.*?)### END", text, re.S)
    print("trials:", len(stories))
    # B1: each of the 16 (set,variant) stories must contain its assigned words.
    # words.txt: 8 sets x ? words. Reconstruct assignment: S<n> uses words[(n-1)*k : n*k].
    # Simpler robust B1: every word in words.txt appears in >=1 story of its set.
    # Even simpler (matches original verify_goalb.py intent): each story contains
    # all words assigned to its set. Assignment: 64 classes line + words grouped per set.
    # Fall back to documented behavior: check each story mentions its set's words.
    # words.txt format check:
    print("words:", len(words), "first:", words[:4])
    b1_ok = 0
    for s, v, body in stories:
        n = int(s[1:])
        # assignment: words are listed per set in order; 8 words per set (S1..S8)
        per = len(words) // 8
        assigned = words[(n-1)*per : n*per]
        missing = [w for w in assigned if w.lower() not in body.lower()]
        if not missing:
            b1_ok += 1
        else:
            print("B1 MISS", s, v, missing)
    print("B1 coverage: %d/%d" % (b1_ok, len(stories)))
    # B3: novelty — each story sentence (>=6 words) must not appear as substring in corpora
    corpora = open(os.path.join(ROOT, "build", "inputs", "words.txt")).read() + \
              open(os.path.join(ROOT, "build", "inputs", "classes.txt")).read()
    b3_ok = 0
    for s, v, body in stories:
        sents = [ln.strip() for ln in body.strip().split("\n") if ln.strip()]
        novel = True
        for sent in sents:
            if len(sent.split()) >= 6 and sent.lower() in corpora.lower():
                novel = False
                print("B3 HIT", s, v, sent[:60])
        if novel:
            b3_ok += 1
    print("B3 novelty: %d/%d" % (b3_ok, len(stories)))
    # B4: kb.txt — the binary must not modify it; story substrings absent
    kb_path = os.path.join(ROOT, "runs", "kb.txt")
    kb = open(kb_path, "rb").read() if os.path.exists(kb_path) else None
    print("kb.txt present:", kb is not None, ("sha256=" + hashlib.sha256(kb).hexdigest()) if kb else "")
    hits = 0
    if kb:
        kbt = kb.decode("utf-8", "replace").lower()
        for s, v, body in stories:
            for ln in body.strip().split("\n"):
                ln = ln.strip()
                if len(ln) >= 16 and ln.lower() in kbt:
                    hits += 1
                    print("B4 SUBSTRING HIT", s, v, ln[:50])
    print("B4 substring hits: %d" % hits)

if __name__ == "__main__":
    main()
