#!/usr/bin/env python3
"""Generate adversarial variant corpora for H3 fixes (prereg §3 + amendments)."""
import os, shutil

OUT = os.path.expanduser('~/workspace/h4_deep_audit/h3fixes/variants')
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT, exist_ok=True)

def write_variant(cid, pages):
    """pages: list of (title, framing, [sentences])"""
    d = os.path.join(OUT, cid)
    os.makedirs(d, exist_ok=True)
    for i, (title, framing, sents) in enumerate(pages, 1):
        with open(os.path.join(d, 'p%d.txt' % i), 'w', encoding='utf-8') as f:
            f.write('TITLE: %s\n' % title)
            f.write('FRAMING: %s\n' % framing)
            for s in sents:
                f.write(s + '\n')

T = "Adversarial probe"
F = "Probe framing:"

# ---- F1 variants ----
# V1a: novel translation (unregistered Spanish novel sentence) -> NOVEL install
write_variant('F1-V1a', [
    (T, F, ["Los gatos vuelan silenciosamente por la noche."]),
    (T, F, ["Los gatos vuelan silenciosamente por la noche."]),
    (T, F, ["Los gatos vuelan silenciosamente por la noche."]),
])
# V1b: English paraphrase of K1 (not in table) -> NOVEL install
write_variant('F1-V1b', [
    (T, F, ["Search tools align terms."]),
    (T, F, ["Search tools align terms."]),
    (T, F, ["Search tools align terms."]),
])
# V1d: duplicate registration (same ES sentence twice in table) -> EMPTY
# (uses standard table; the dup is in the table file itself - tested via table gen)

# ---- F2 variants ----
# V2a: triple negation (odd parity) -> NOVEL
write_variant('F2-V2a', [
    (T, F, ["It is not the case that it is not true that it is false that all of it is just text on a page."]),
    (T, F, ["It is not the case that it is not true that it is false that all of it is just text on a page."]),
    (T, F, ["It is not the case that it is not true that it is false that all of it is just text on a page."]),
])
# V2b: unknown wrapper -> NOVEL
write_variant('F2-V2b', [
    (T, F, ["It is rumored that all of it is just text on a page."]),
    (T, F, ["It is rumored that all of it is just text on a page."]),
    (T, F, ["It is rumored that all of it is just text on a page."]),
])
# V2c: negated novel -> NOVEL
write_variant('F2-V2c', [
    (T, F, ["It is not true that cats fly silently at night."]),
    (T, F, ["It is not true that cats fly silently at night."]),
    (T, F, ["It is not true that cats fly silently at night."]),
])
# V2d: shell around novel core -> NOVEL
write_variant('F2-V2d', [
    (T, F, ["It is not the case that the claim that cats fly silently at night is false."]),
    (T, F, ["It is not the case that the claim that cats fly silently at night is false."]),
    (T, F, ["It is not the case that the claim that cats fly silently at night is false."]),
])

# ---- F3 variants ----
P1a = "Search engines match words."
P1b = "Pick out the words that carry the meaning and leave the rest behind."
# V3a: three-way split of P1 -> EMPTY
write_variant('F3-V3a', [
    (T, F, ["Search engines match words,", "so pick out the words", "that carry the meaning and leave the rest behind."]),
    (T, F, ["Search engines match words,", "so pick out the words", "that carry the meaning and leave the rest behind."]),
    (T, F, ["Search engines match words,", "so pick out the words", "that carry the meaning and leave the rest behind."]),
])
# V3b: cross-page halves -> NOVEL (fork is same-page only)
write_variant('F3-V3b', [
    (T, F, [P1a]),
    (T, F, [P1b]),
    (T, F, [P1a, P1b]),
])
# V3c: reordered halves -> NOVEL
write_variant('F3-V3c', [
    (T, F, [P1b, P1a]),
    (T, F, [P1b, P1a]),
    (T, F, [P1b, P1a]),
])
# V3d: interleaved novel between halves -> NOVEL
write_variant('F3-V3d', [
    (T, F, [P1a, "Cats fly silently at night.", P1b]),
    (T, F, [P1a, "Cats fly silently at night.", P1b]),
    (T, F, [P1a, "Cats fly silently at night.", P1b]),
])

# ---- F4b variants ----
# V4a: multi-rename (two nonces in K1 template) -> EMPTY
write_variant('F4b-V4a', [
    (T, F, ["VEXMOR engines match ZORBLAX, so pick out the words that carry the meaning and leave the rest behind."]),
    (T, F, ["VEXMOR engines match ZORBLAX, so pick out the words that carry the meaning and leave the rest behind."]),
    (T, F, ["VEXMOR engines match ZORBLAX, so pick out the words that carry the meaning and leave the rest behind."]),
])
# V4b: nonce-shaped common words (uppercase IT/IS that are in vocab) -> NOVEL
# "IT IS" are nonce-shaped (uppercase) but in K vocab, so no match.
write_variant('F4b-V4b', [
    (T, F, ["IT IS not the case that the claim is false."]),
    (T, F, ["IT IS not the case that the claim is false."]),
    (T, F, ["IT IS not the case that the claim is false."]),
])
# V4c: rename+paraphrase -> NOVEL
write_variant('F4b-V4c', [
    (T, F, ["VEXMOR search tools align terms effectively."]),
    (T, F, ["VEXMOR search tools align terms effectively."]),
    (T, F, ["VEXMOR search tools align terms effectively."]),
])
# V4d: template novel (nonce in novel content) -> NOVEL
write_variant('F4b-V4d', [
    (T, F, ["VEXMOR engines harvest moonlight on BRUNDIC-ALPHA."]),
    (T, F, ["VEXMOR engines harvest moonlight on BRUNDIC-ALPHA."]),
    (T, F, ["VEXMOR engines harvest moonlight on BRUNDIC-ALPHA."]),
])

# ---- F5 variants ----
K1 = "Search engines match words, so pick out the words that carry the meaning and leave the rest behind."
# V5a: fullwidth ASCII "Search" -> EMPTY
write_variant('F5-V5a', [
    (T, F, ["\uFF33\uFF45\uFF41\uFF52\uFF43\uFF48 engines match words, so pick out the words that carry the meaning and leave the rest behind."]),
    (T, F, ["\uFF33\uFF45\uFF41\uFF52\uFF43\uFF48 engines match words, so pick out the words that carry the meaning and leave the rest behind."]),
    (T, F, ["\uFF33\uFF45\uFF41\uFF52\uFF43\uFF48 engines match words, so pick out the words that carry the meaning and leave the rest behind."]),
])
# V5b: Cyrillic Es + "earch" -> EMPTY
write_variant('F5-V5b', [
    (T, F, ["\u0405earch engines match words, so pick out the words that carry the meaning and leave the rest behind."]),
    (T, F, ["\u0405earch engines match words, so pick out the words that carry the meaning and leave the rest behind."]),
    (T, F, ["\u0405earch engines match words, so pick out the words that carry the meaning and leave the rest behind."]),
])
# V5c: mixed-script (Cyrillic a in "match") -> EMPTY
write_variant('F5-V5c', [
    (T, F, ["Search engines m\u0430tch words, so pick out the words that carry the meaning and leave the rest behind."]),
    (T, F, ["Search engines m\u0430tch words, so pick out the words that carry the meaning and leave the rest behind."]),
    (T, F, ["Search engines m\u0430tch words, so pick out the words that carry the meaning and leave the rest behind."]),
])
# V5d: math bold S (U+1D400) -> NOVEL (safe-direction, not folded)
write_variant('F5-V5d', [
    (T, F, ["\U0001D400earch engines match words, so pick out the words that carry the meaning and leave the rest behind."]),
    (T, F, ["\U0001D400earch engines match words, so pick out the words that carry the meaning and leave the rest behind."]),
    (T, F, ["\U0001D400earch engines match words, so pick out the words that carry the meaning and leave the rest behind."]),
])
# V5e: German ß / Chinese -> NOVEL
write_variant('F5-V5e', [
    (T, F, ["Search engines match words\u00DF, so pick out the words that carry the meaning and leave the rest behind."]),
    (T, F, ["Search engines match words\u00DF, so pick out the words that carry the meaning and leave the rest behind."]),
    (T, F, ["Search engines match words\u00DF, so pick out the words that carry the meaning and leave the rest behind."]),
])
# V5f: canonical decomposition (e + combining acute vs precomposed) -> NOVEL (no NFC)
write_variant('F5-V5f', [
    (T, F, ["Search engines match words, so pick out the words that carry the meaning and leave the rest behind caf\u0065\u0301."]),
    (T, F, ["Search engines match words, so pick out the words that carry the meaning and leave the rest behind caf\u0065\u0301."]),
    (T, F, ["Search engines match words, so pick out the words that carry the meaning and leave the rest behind caf\u0065\u0301."]),
])
# V5g: soft hyphen in "engines" -> EMPTY
write_variant('F5-V5g', [
    (T, F, ["Search en\u00ADgines match words, so pick out the words that carry the meaning and leave the rest behind."]),
    (T, F, ["Search en\u00ADgines match words, so pick out the words that carry the meaning and leave the rest behind."]),
    (T, F, ["Search en\u00ADgines match words, so pick out the words that carry the meaning and leave the rest behind."]),
])
# V5h: math alphanumeric boundary (another math char) -> NOVEL
write_variant('F5-V5h', [
    (T, F, ["Search \U0001D41A\u006Egines match words, so pick out the words that carry the meaning and leave the rest behind."]),
    (T, F, ["Search \U0001D41A\u006Egines match words, so pick out the words that carry the meaning and leave the rest behind."]),
    (T, F, ["Search \U0001D41A\u006Egines match words, so pick out the words that carry the meaning and leave the rest behind."]),
])
# V5i: mixed-script skeleton (Cyrillic o in "words") -> EMPTY
write_variant('F5-V5i', [
    (T, F, ["Search engines match w\u043Erds, so pick out the words that carry the meaning and leave the rest behind."]),
    (T, F, ["Search engines match w\u043Erds, so pick out the words that carry the meaning and leave the rest behind."]),
    (T, F, ["Search engines match w\u043Erds, so pick out the words that carry the meaning and leave the rest behind."]),
])

print("Variants written to", OUT)
import subprocess
r = subprocess.run(['ls', OUT], capture_output=True, text=True)
print(r.stdout)
