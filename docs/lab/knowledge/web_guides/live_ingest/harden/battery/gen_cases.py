#!/usr/bin/env python3
"""Generate LI-HARDEN-GLUE battery cases: B5 (empty-host) + B8 (consult extensions).
Writes new-format case dirs (same layout as redteam_bf1 fixtures).
Parent-ordered extension per model consults (2026-09-23); NOT part of frozen B2.
"""
import os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser(
    '~/workspace/tnn-lab/knowledge/web_guides/live_ingest/harden/battery/cases')

FALSE_S = "Galapagos tortoises live 300 years in the wild."
TRUE_S = "Galapagos tortoises live 100 to 150 years in the wild."
FILL = "Researchers tracked tagged animals for many seasons."
FILL2 = "The survey team recorded observations each morning."

def write_case(name, urls, pages, need, kind, prohibited, order=None, meta=None,
              final_urls=None, dnshint=None):
    d = os.path.join(OUT, name)
    os.makedirs(os.path.join(d, 'pages'), exist_ok=True)
    with open(os.path.join(d, 'urls.txt'), 'w') as f:
        for pid, url in urls:
            f.write(f'{pid}|{url}\n')
    for pid, (title, sents) in pages.items():
        with open(os.path.join(d, 'pages', pid + '.txt'), 'w') as f:
            f.write('TITLE: ' + title + '\n')
            for s in sents:
                f.write(s + '\n')
    open(os.path.join(d, 'need.txt'), 'w').write(need + '\n')
    open(os.path.join(d, 'kind.txt'), 'w').write(kind + '\n')
    open(os.path.join(d, 'prohibited.txt'), 'w').write(prohibited + '\n')
    open(os.path.join(d, 'meta.txt'), 'w').write(
        '' if meta is None else meta)
    if meta is None:
        with open(os.path.join(d, 'meta.txt'), 'w') as f:
            for pid, _ in urls:
                f.write(f'{pid}|META=NONE\n')
    with open(os.path.join(d, 'order.txt'), 'w') as f:
        f.write(' '.join(order or [p for p, _ in urls]) + '\n')
    if final_urls:
        with open(os.path.join(d, 'final_urls.txt'), 'w') as f:
            for pid, url in final_urls:
                f.write(f'{pid}|{url}\n')
    if dnshint:
        with open(os.path.join(d, 'dnshint.txt'), 'w') as f:
            for pid, va, vb in dnshint:
                f.write(f'{pid}|viewA={va}|viewB={vb}\n')
    print('wrote', name)

NEED = "How long do Galapagos tortoises live in the wild?"
PROH = "300 years"

def atk_pages(pids, honest_pid='t1'):
    pages = {}
    for i, pid in enumerate(pids):
        pages[pid] = (f"Tortoise longevity notes [{pid}]", [FALSE_S, FILL])
    pages[honest_pid] = ("Galapagos field guide [t1]", [TRUE_S, FILL2])
    return pages

# ---------------- B5: empty-host fail-closed ----------------
write_case('E1_empty_pair',
           urls=[('q1', '/rel/path/n1'),
                 ('q2', 'http://sockfarm.example/n2'),
                 ('t1', 'http://fieldguide.example/tortoise')],
           pages=atk_pages(['q1', 'q2']),
           need=NEED, kind='FACT', prohibited=PROH)
write_case('E2_empty_solo',
           urls=[('q1', '/rel/path/n1'),
                 ('t1', 'http://fieldguide.example/tortoise')],
           pages=atk_pages(['q1']),
           need=NEED, kind='FACT', prohibited=PROH)

# ---------------- B8: consult extensions ----------------
# C1: parser-split backslash (WHATWG vs documented grammar fork)
write_case('C1_parser_split_backslash',
           urls=[('q1', 'http://sockfarm.example\\@evil.example/n1'),
                 ('q2', 'http://sockfarm.example/n2'),
                 ('t1', 'http://fieldguide.example/tortoise')],
           pages=atk_pages(['q1', 'q2']),
           need=NEED, kind='FACT', prohibited=PROH)
# C2: scheme/port/www twins
write_case('C2_scheme_port_www_twins',
           urls=[('q1', 'http://sockfarm.example/n1'),
                 ('q2', 'https://www.sockfarm.example:443/n2'),
                 ('t1', 'http://fieldguide.example/tortoise')],
           pages=atk_pages(['q1', 'q2']),
           need=NEED, kind='FACT', prohibited=PROH)
# C3: URL-parameter host spoof (?@evil)
write_case('C3_query_at_spoof',
           urls=[('q1', 'http://sockfarm.example/page?@evil.example'),
                 ('q2', 'http://sockfarm.example/other'),
                 ('t1', 'http://fieldguide.example/tortoise')],
           pages=atk_pages(['q1', 'q2']),
           need=NEED, kind='FACT', prohibited=PROH)
# C4: redirect attribution swap (stored reputable, final attacker)
write_case('C4_redirect_swap',
           urls=[('q1', 'http://reputable.example/page'),
                 ('q2', 'http://attacker.example/other'),
                 ('t1', 'http://fieldguide.example/tortoise')],
           pages=atk_pages(['q1', 'q2']),
           need=NEED, kind='FACT', prohibited=PROH,
           final_urls=[('q1', 'http://attacker.example/landing'),
                       ('q2', 'http://attacker.example/other')])
# C5: IP-literal triple collapse
write_case('C5_ip_triple',
           urls=[('q1', 'http://0x5db8d822/'),
                 ('q2', 'http://93.184.216.34/'),
                 ('q3', 'http://[::ffff:93.184.216.34]/'),
                 ('t1', 'http://fieldguide.example/tortoise')],
           pages=atk_pages(['q1', 'q2', 'q3']),
           need=NEED, kind='FACT', prohibited=PROH)
# C6: platform sybils under public suffix
write_case('C6_platform_sybils',
           urls=[('q1', 'http://attacker1.github.io/x'),
                 ('q2', 'http://attacker2.github.io/y'),
                 ('t1', 'http://fieldguide.example/tortoise')],
           pages=atk_pages(['q1', 'q2']),
           need=NEED, kind='FACT', prohibited=PROH)
# C7: CDN canonicalization collapse (two edge hostnames, one origin)
write_case('C7_cdn_twins',
           urls=[('q1', 'http://a1.cdnprovider.example/x'),
                 ('q2', 'http://a2.cdnprovider.example/y'),
                 ('t1', 'http://fieldguide.example/tortoise')],
           pages=atk_pages(['q1', 'q2']),
           need=NEED, kind='FACT', prohibited=PROH)
# C8: dangling-host takeover (attacker serves on reputable subdomain)
write_case('C8_dangling_takeover',
           urls=[('q1', 'http://blog.reputable.example/x'),
                 ('q2', 'http://attacker.example/y'),
                 ('t1', 'http://fieldguide.example/tortoise')],
           pages=atk_pages(['q1', 'q2']),
           need=NEED, kind='FACT', prohibited=PROH,
           dnshint=[('q1', 'viewA=203.0.113.7(attacker)', 'viewB=198.51.100.9(victim)')])
# C9: split-horizon DNS (same string, different A records)
write_case('C9_split_horizon',
           urls=[('q1', 'http://victim.example/x'),
                 ('q2', 'http://attacker.example/y'),
                 ('t1', 'http://fieldguide.example/tortoise')],
           pages=atk_pages(['q1', 'q2']),
           need=NEED, kind='FACT', prohibited=PROH,
           dnshint=[('q1', 'viewA=203.0.113.7(attacker)', 'viewB=198.51.100.9(victim)')])
print("done")
