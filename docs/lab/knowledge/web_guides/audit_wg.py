#!/usr/bin/env python3
"""WG-1 audit: webg.zag must contain no guide/corpus/task content literals.
Usage: audit_wg.py ; exits nonzero on violation."""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'webg.zag')
ALLOWED = {'QUERY', 'ANSWER', 'CLAIM', 'PROV', 'FLAG', 'LEARN', 'OPEN', 'UNCHECKED',
           'INJECTION', 'DISPUTE', 'INSTALLED', 'REJECTED', 'VOID', 'NONE', 'NO-GUIDES',
           'SEL-REASON', 'D|', 'I|', 'Q|', 'R|', 'P|', 'S|', 'W|',
           # protocol vocabulary (mode names / flag values), not taught knowledge:
           'keywords', 'max-overlap', 'always', 'on', 'yes',
           'QUERY-MODE', 'DROP', 'SELECT-N', 'CLAIM-BY', 'MIN-SOURCES',
           'PROVENANCE', 'SCAN-INJECTION', 'INJECT-WORDS', 'SKIP-DUPE-TITLES',
           'TRUST-FIRST', 'OBEY-PAGES'}

def collect_strings():
    strs = set()
    # corpus sentences + titles + pids
    cdir = os.path.join(HERE, 'corpus', 'pages')
    for fn in sorted(os.listdir(cdir)):
        if fn.endswith('.txt'):
            strs.add(fn[:-4])  # pid
            with open(os.path.join(cdir, fn)) as f:
                for l in f:
                    l = l.strip()
                    if l and not l.startswith('TITLE:'):
                        strs.add(l)
                    elif l.startswith('TITLE:'):
                        t = l.split('TITLE:', 1)[1].strip()
                        if len(t) > 12:
                            strs.add(t)
    # task needs + expected answers + entity phrases
    bdir = os.path.join(HERE, 'batteries')
    for fn in sorted(os.listdir(bdir)):
        if fn.endswith('.txt'):
            with open(os.path.join(bdir, fn)) as f:
                for l in f:
                    if l.startswith('TASK|'):
                        p = l.rstrip('\n').split('|')
                        strs.add(p[2])  # need
                        if p[3] != 'UNCHECKABLE':
                            strs.add(p[3])  # expected
                        if len(p) > 6 and p[6] != '-':
                            for e in p[6].split(';'):
                                strs.add(e)
    # guide content: principle/worked/calibration text, directive values
    gdir = os.path.join(HERE, 'guides')
    for fn in sorted(os.listdir(gdir)):
        if fn.endswith('.txt'):
            with open(os.path.join(gdir, fn)) as f:
                for l in f:
                    l = l.rstrip('\n')
                    if l.startswith('D|'):
                        p = l.split('|')
                        if len(p) > 2 and p[2]:
                            for v in p[2].replace('|', ' ').split():
                                if len(v) > 3:
                                    strs.add(v)
                    elif l and not any(l.startswith(k) for k in
                                       ('MODULE:', 'TITLE:', 'PRINCIPLE:', 'WORKED:', 'DIRECTIVES:',
                                        'CALIBRATION:', 'CNEED:', 'CQUERY:', 'CRESULTS:', 'CPAGE:',
                                        'CPAGES:', 'EXPECT-', 'W|')):
                        if len(l) > 20:
                            strs.add(l)
    return strs

def main():
    with open(SRC) as f:
        src = f.read()
    bad = []
    for s in collect_strings():
        if s in ALLOWED:
            continue
        # match as a whole word/phrase (no word char adjacent on either side),
        # case-insensitive; skip tiny generic words. Plain substring matching
        # false-positives on English prose in comments (e.g. "ignore" inside
        # "(rc ignored)"); \b alone breaks on trailing punctuation, so use
        # explicit word-char lookarounds instead.
        if len(s) < 6:
            continue
        if re.search(r'(?<!\w)' + re.escape(s) + r'(?!\w)', src, flags=re.IGNORECASE):
            bad.append(s[:80])
    if bad:
        print(f'AUDIT FAIL: {len(bad)} forbidden strings in webg.zag:')
        for b in bad[:20]:
            print('  ' + b)
        sys.exit(1)
    print('AUDIT PASS: no guide/corpus/task literals in webg.zag')

if __name__ == '__main__':
    main()
