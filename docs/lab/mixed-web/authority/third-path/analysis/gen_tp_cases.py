#!/usr/bin/env python3
"""Generate tp_cases.zag: 220 frozen envelopes as run functions + main.
Test-side data prep (harness), not decision logic. Reads tp_data.json
(extracted from frozen manifest_r3.txt, twin/latent formulas verified 0 mismatches).
"""
import json

data = json.load(open('/home/hatch/workspace/third-path/tp_data.json'))
qids = sorted(data.keys())
assert len(qids) == 220, len(qids)

doms = sorted({r[0] for v in data.values() for r in v['rows']})
anss = sorted({r[1] for v in data.values() for r in v['rows']})
did = {d: i for i, d in enumerate(doms)}
aid = {a: i for i, a in enumerate(anss)}

out = []
out.append('// tp_cases.zag — GENERATED from frozen manifest_r3.txt. Do not hand-edit.')
out.append('// 220 envelopes: Block U (180) + Block S/S8 (20) + Block G2 (20).')
out.append('@import("tp_trial.zag")')
out.append('')
out.append('// domain ids:')
for d, i in did.items():
    out.append(f'//   {i} = {d}')
out.append('// answer ids:')
for a, i in aid.items():
    out.append(f'//   {i} = {a}')
out.append('')

for q in qids:
    v = data[q]
    rows = v['rows']
    assert len(rows) == 4, (q, len(rows))
    assert rows[0][2] == '2026', (q, rows[0])
    prim = did[rows[0][0]]
    rel = -1 if v['rel'] in (None, 'None') else int(round(float(v['rel']) * 1000))
    gold = -1 if v['block'] == 'S' else aid[v['gold']]
    latent = -1 if v['block'] != 'S' else aid[v['latent']]
    out.append(f'fn run_TP_{q}(lg:*TpL) void {{')
    out.append('    let w:*TpW=tp_new();')
    out.append(f'    tp_begin(w,"{q}",{prim},{rel},{gold},{latent});')
    for d, a, y in rows:
        out.append(f'    tp_row(w,{did[d]},{aid[a]},{y});')
    out.append('    tp_decide(w,lg);')
    out.append('    return;')
    out.append('}')

out.append('')
out.append('fn main() i32 {')
out.append('    let lg:*TpL=tp_lg_new();')
for q in qids:
    out.append(f'    run_TP_{q}(lg);')
out.append('    _zag_print("H|T1|");_zag_println(ns_hex(lg.*.p0));')
out.append('    _zag_print("H|T2|");_zag_println(ns_hex(lg.*.p1));')
out.append('    _zag_print("H|T3|");_zag_println(ns_hex(lg.*.p2));')
out.append('    _zag_print("S|");_zag_print(tp_i32(lg.*.s0 as i32));_zag_print("|");')
out.append('    _zag_print(tp_i32(lg.*.s1 as i32));_zag_print("|");_zag_println(tp_i32(lg.*.s2 as i32));')
out.append('    _zag_print("C|1|");_zag_print(tp_i32(lg.*.n1));_zag_print("|2|");_zag_print(tp_i32(lg.*.n2));')
out.append('    _zag_print("|3|");_zag_print(tp_i32(lg.*.n3));_zag_print("|0|");_zag_println(tp_i32(lg.*.n0));')
out.append('    return 0;')
out.append('}')

with open('/home/hatch/workspace/tnn-lab/mixed-web/authority/third-path/src/tp_cases.zag', 'w') as f:
    f.write('\n'.join(out) + '\n')

# save id maps for the oracle/analysis
json.dump({'dom': did, 'ans': {v: k for k, v in aid.items()}},
          open('/home/hatch/workspace/third-path/idmaps.json', 'w'))
print('wrote tp_cases.zag with', len(qids), 'envelopes;', len(doms), 'domains;', len(anss), 'answers')
