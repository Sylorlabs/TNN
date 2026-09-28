#!/usr/bin/env python3
"""Strip browser-open citation markers from fetched page text (LI-1 glue).

Fidelity transform (frozen for this run, documented here):
  The fetch tool wraps linked/cited spans in markers of the form
    OPEN idx DAGGER DISPLAY CLOSE               -> DISPLAY
    OPEN idx DAGGER DISPLAY DAGGER DOMAIN CLOSE  -> DISPLAY
  where OPEN=U+3010, CLOSE=U+3011, DAGGER=U+2020. The transform replaces each
  marker span with its DISPLAY text (the page's visible text). Everything else
  is byte-identical: blank lines, punctuation, leading/trailing spaces, the
  Images: footnote, raw markdown links. No bytes invented; only the marker
  chrome itself (OPEN/idx/DAGGER wrappers and DAGGER DOMAIN suffix) is removed.
  Adjacent spacing is preserved exactly as rendered (no space insertion).

Usage: strip_markers.py <rawfile> "<title>" <outfile>
  rawfile: page text as rendered by browser.open (blank lines preserved,
           no tool header/footer wrapper lines)
  Writes:  "TITLE: <title>\n" + transformed text (+ trailing newline ensured).

Exits nonzero with MARKER_REMAINDER if any marker bracket survives.
Zero RNG. Deterministic: same input bytes -> same output bytes.
"""
import re
import sys


def strip_markers(text):
    # U+3010 OPEN, U+2020 DAGGER, U+3011 CLOSE; escapes keep source ASCII-clean.
    pat = re.compile(
        '\u3010[^\u2020\u3011]+\u2020([^\u2020\u3011]+)(?:\u2020[^\u3011]*)?\u3011'
    )
    return pat.sub(r'\1', text)


def main():
    rawfile, title, outfile = sys.argv[1], sys.argv[2], sys.argv[3]
    with open(rawfile, encoding='utf-8') as f:
        text = f.read()
    out = strip_markers(text)
    if '\u3010' in out or '\u3011' in out:
        sys.exit('MARKER_REMAINDER')
    blob = 'TITLE: ' + title + '\n' + out
    if not blob.endswith('\n'):
        blob += '\n'
    with open(outfile, 'w', encoding='utf-8') as f:
        f.write(blob)
    print('OK %s %d bytes' % (outfile, len(blob.encode('utf-8'))))


if __name__ == '__main__':
    main()
