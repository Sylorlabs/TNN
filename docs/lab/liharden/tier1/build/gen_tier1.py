#!/usr/bin/env python3
"""Build tier1.zag: hostnorm.zag (base, minus main) + corrob.zag verdict
machinery (unique fns; corrob's pid_less renamed to pid_less_idx) +
Tier-1 adaptations + new main. Build-time script only; not in any decision path.
"""
HN = '/home/hatch/workspace/liharden/glue/hostnorm.zag'
CB = '/home/hatch/workspace/liharden/corrob/build/corrob.zag'
OUT = '/home/hatch/workspace/liharden/tier1/build/tier1.zag'

hn_lines = open(HN).read().split('\n')
cb_text = open(CB).read()

# hostnorm base: everything before its main
mi = next(i for i, l in enumerate(hn_lines) if l.startswith('fn main()'))
base = '\n'.join(hn_lines[:mi]).rstrip() + '\n'

# rename corrob's pid_less (signature conflicts with hostnorm's pid_less)
cb_text = cb_text.replace('fn pid_less(', 'fn pid_less_idx(')
cb_text = cb_text.replace('pid_less(pa,pt,v,', 'pid_less_idx(pa,pt,v,')
assert 'fn pid_less(' not in cb_text
assert cb_text.count('pid_less_idx(pa,pt,v,') == 1


def split_fns(text):
    fns, cur_name, cur = [], None, []
    for l in text.split('\n'):
        if l.startswith('fn '):
            if cur_name is not None:
                fns.append((cur_name, '\n'.join(cur)))
            cur_name = l[3:].split('(')[0]
            cur = [l]
        elif cur_name is not None:
            cur.append(l)
    if cur_name is not None:
        fns.append((cur_name, '\n'.join(cur)))
    return fns


# drop byte-identical shared helpers + corrob's main
DROP = {'i64s', 'p32', 'g32', 'bsub', 'bsub_eq', 'next_line', 'read_file',
        'read_path', 'main'}

TIE_BLOCK = '''    if(w>=0){
        // HL-3: any tie for the largest cluster withholds (never first-seen-install)
        let tiec:i32=0;
        let c5:i32=0;
        while(c5<ncl){
            if(g32(cc,c5*4)==wc){tiec=tiec+1;}
            c5=c5+1;
        }
        if(tiec>1){
            let tidx:[]u8=nio_alloc(64*4);
            let tn2:i32=0;
            c5=0;
            while(c5<ncl){
                if(g32(cc,c5*4)==wc){
                    let m6:i32=0;
                    while(m6<wc){
                        p32(tidx,tn2*4,g32(cm,c5*256+m6*4));
                        tn2=tn2+1;
                        m6=m6+1;
                    }
                }
                c5=c5+1;
            }
            _zag_println("ANSWER|UNCHECKABLE");
            _zag_print("GATE|TIE|");
            sort_page_idx(pa,pt,tidx,tn2);
            print_pids(pa,pt,tidx,tn2);
            _zag_println("");
            nio_free(tidx);
            nio_free(buf);
            nio_free(pa);
            nio_free(pt);
            nio_free(ha);
            nio_free(ht);
            nio_free(tt);
            nio_free(st);
            nio_free(qlow);
            nio_free(qt);
            nio_free(cidx);
            nio_free(ca);
            nio_free(ct);
            nio_free(cpg);
            nio_free(keep);
            nio_free(cona);
            nio_free(conu);
            nio_free(ck);
            nio_free(cc);
            nio_free(cm);
            return 0;
        }
    }
'''


def apply_adaptations(body):
    body = body.replace(
        '// cluster kept candidates by byte equality; winner = largest, tie -> first (canonical)',
        '// cluster kept candidates by byte equality; winner = largest, tie -> WITHHOLD (HL-3 no-tie-install)')
    anchor = '        nio_free(cm);\n        return 0;\n    }\n    let widx:[]u8=nio_alloc(64*4);'
    assert anchor in body, 'tie anchor not found'
    body = body.replace(anchor,
        '        nio_free(cm);\n        return 0;\n    }\n' + TIE_BLOCK + '    let widx:[]u8=nio_alloc(64*4);', 1)
    old_q = '    let verdict_ok:i32=0;\n    if(wc>=2 && nh>=2){verdict_ok=1;}'
    assert old_q in body, 'quorum anchor not found'
    body = body.replace(old_q,
        '    let qneed:i32=2;\n'
        '    if(mode==3){qneed=3;}\n'
        '    let verdict_ok:i32=0;\n'
        '    if(wc>=qneed && nh>=qneed){verdict_ok=1;}', 1)
    old_g = '            if(wc<2){'
    assert old_g in body, 'gate anchor not found'
    body = body.replace(old_g, '            if(wc<qneed){', 1)
    # add-on gates: ch2 furniture discount (before CORROB-1D), ch1 polarity veto (before install)
    old_q2 = '    let verdict_ok:i32=0;\n    if(wc>=qneed && nh>=qneed){verdict_ok=1;}'
    assert old_q2 in body, 'quorum anchor 2 not found'
    body = body.replace(old_q2,
        '    let verdict_ok:i32=0;\n'
        '    let furn_hit:i32=0;\n'
        '    let pol_veto:i32=0;\n'
        '    if(wc>=qneed && nh>=qneed){verdict_ok=1;}\n' + ADDON_CH2, 1)
    old_inst = '    if(verdict_ok==1){\n        _zag_print("ANSWER|");'
    assert old_inst in body, 'install anchor not found'
    body = body.replace(old_inst, ADDON_CH1 + '    if(verdict_ok==1){\n        _zag_print("ANSWER|");', 1)
    old_w = '            _zag_println("ANSWER|UNCHECKABLE");\n            if(wc<qneed){'
    assert old_w in body, 'withhold anchor not found'
    body = body.replace(old_w,
        '            _zag_println("ANSWER|UNCHECKABLE");\n'
        '            if(pol_veto==1){\n'
        '                _zag_print("GATE|POLARITY|");\n'
        '                print_pids(pa,pt,widx,wc);\n'
        '                _zag_println("");\n'
        '            }else if(furn_hit==1){\n'
        '                _zag_print("GATE|FURNITURE|");\n'
        '                print_pids(pa,pt,widx,wc);\n'
        '                _zag_println("");\n'
        '            }else if(wc<qneed){', 1)
    return body


# add-on gate sources (WALL-RED C3, BEYOND ch1/ch2); loaded before use
import os as _os
_BUILD = _os.path.dirname(OUT)
with open(_os.path.join(_BUILD, 'addon_gates.zag')) as f:
    ADDON_FNS = f.read()
with open(_os.path.join(_BUILD, 'snippet_ch1.zag')) as f:
    ADDON_CH1 = f.read()
with open(_os.path.join(_BUILD, 'snippet_ch2.zag')) as f:
    ADDON_CH2 = f.read()

kept = []
for name, body in split_fns(cb_text):
    if name in DROP:
        continue
    if name == 'run_verdict':
        body = apply_adaptations(body)
    kept.append(body.rstrip())
sec = '\n\n'.join(kept)

# add-on gates: new functions before contra_pair; C3 call inside contra_pair
anchor_cp = 'fn contra_pair(a:[]u8,b:[]u8)i32 {'
assert anchor_cp in sec, 'contra_pair anchor not found'
sec = sec.replace(anchor_cp, ADDON_FNS + '\n' + anchor_cp, 1)
old_c3 = '    if(num_contra(a,b)==1){return 1;}\n    return 0;'
assert old_c3 in sec, 'contra_pair tail anchor not found'
sec = sec.replace(old_c3,
    '    if(num_contra(a,b)==1){return 1;}\n    if(c3_slot_dissent(a,b)==1){return 1;}\n    return 0;', 1)

for need in ['normalize(', 'tokenize(', 'contra_pair(', 'parse_pages_h(',
             'best_for_page(', 'print_pids(', 'sort_page_idx(', 'expand_neg(',
             'frame_vals(', 'page_body(', 'distinct_hosts(', 'pid_less_idx(',
             'GATE|TIE|', 'qneed', 'c3_slot_dissent(', 'GATE|POLARITY|',
             'GATE|FURNITURE|']:
    assert need in sec, 'missing ' + need
print('kept corrob fns:', len(kept))

MAIN = '''
// ---------- tier1 driver ----------
// Modes: norm | pages (=ingest) | verdict (HL-1..HL-4, quorum 2) |
//        verdict3 (HL-5, quorum >=3 distinct registrable domains).
// The verdict H| key is the eTLD+1 registrable-domain origin emitted by
// `pages`; empty/missing H| fails closed (never counts toward quorum).
fn main()i32 {
    let lit:[]u8=psl_literal();
    let psl:[]u8=nio_alloc(256*12);
    let cft:[]u8=nio_alloc(128*8);
    let scratch:[]u8=nio_alloc(16384);
    let arena:[]u8=nio_alloc(65536);
    if(psl.len==0 || cft.len==0 || scratch.len==0 || arena.len==0){
        _zag_println("ERR alloc");
        return 2;
    }
    let psln:i32=psl_init(psl);
    let cfn:i32=conf_init(cft);
    let m:[]u8=_zag_arg(1);
    let rc:i32=2;
    if(nio_equal(m,"norm")==1){
        let fp:[]u8=_zag_arg(2);
        if(fp.len>0){rc=cmd_norm(fp,scratch,arena,psl,psln,lit,cft,cfn);}
        else{_zag_println("usage: tier1 norm <urlfile>");}
    }else{
        if(nio_equal(m,"pages")==1 || nio_equal(m,"ingest")==1){
            let inf:[]u8=_zag_arg(2);
            let outf:[]u8=_zag_arg(3);
            if(inf.len>0 && outf.len>0){rc=cmd_pages(inf,outf,scratch,arena,psl,psln,lit,cft,cfn);}
            else{_zag_println("usage: tier1 pages <infile> <outfile>");}
        }else{
            if(nio_equal(m,"verdict")==1){
                let pp:[]u8=_zag_arg(2);
                let qy:[]u8=_zag_arg(3);
                if(pp.len>0 && qy.len>0){rc=run_verdict(pp,qy,"",0);}
                else{_zag_println("usage: tier1 verdict <pages> <query>");}
            }else{
                if(nio_equal(m,"verdict3")==1){
                    let pp2:[]u8=_zag_arg(2);
                    let qy2:[]u8=_zag_arg(3);
                    if(pp2.len>0 && qy2.len>0){rc=run_verdict(pp2,qy2,"",3);}
                    else{_zag_println("usage: tier1 verdict3 <pages> <query>");}
                }else{
                    _zag_println("usage: tier1 norm|pages|ingest|verdict|verdict3");
                }
            }
        }
    }
    nio_free(psl);
    nio_free(cft);
    nio_free(scratch);
    nio_free(arena);
    return rc;
}
'''

HDR = '''// tier1.zag — LI-HARDEN Tier-1 unified pipeline (T1-BUILD crew).
// Pure Zag. Zero RNG. Deterministic: same input bytes -> same output bytes.
// Base: glue/hostnorm.zag (HL-1 canonical WHATWG URL parser + host
// normalization; HL-2 eTLD+1 via pinned PSL emitted on H| lines) verbatim
// minus its main. Verdict: corrob/build/corrob.zag CORROB-1 machinery
// (HL-3 canonical pid-sort; HL-4 C1/C2 contradiction veto; report-only
// diversity) verbatim except two Tier-1 adaptations:
//   (a) tie for largest cluster -> WITHHOLD with GATE|TIE (HL-3
//       no-tie-install; CORROB-1 installed canonical-first),
//   (b) verdict3 mode: quorum >=3 pages AND >=3 distinct registrable-domain
//       keys (HL-5). Adopted only if the throughput guard battery passes.
// CORROB-1D/1M code paths (mode 1/2) are present but unreachable in tier1.
//
// Add-on gates (measured candidates, default-on; each with a differential
// kill fixture and a 12/12 honest regression battery):
//   C3  functional-slot proper-noun dissent (WALL-RED crack 1): same frozen
//       slot frame (capital/president/atomic-number/closest-planet/
//       tallest-mountain/largest-city), same entity, different filler ->
//       contradiction. Numeric/negation shapes defer to C1/C2.
//   ch1 assertion-polarity veto (BEYOND): a non-claim sentence sharing >=2
//       content words with the winning claim that carries a polarity flipper
//       (false/hoax/...) or antonym predicate vetoes the install.
//   ch2 furniture-coupled repetition discount (BEYOND; safer HL-10): a
//       non-claim furniture-marked sentence repeated across >=2 distinct
//       hosts discounts its pages' votes before the quorum check.
'''
open(OUT, 'w').write(HDR + base + '\n// ---------- corrob verdict machinery (HL-3, HL-4) ----------\n' + sec + '\n' + MAIN)
print('wrote', OUT)
