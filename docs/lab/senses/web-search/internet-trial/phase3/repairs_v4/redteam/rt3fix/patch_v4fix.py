#!/usr/bin/env python3
"""Transform g_intent6_v4.zag -> g_intent6_v4fix.zag (pure source-level patch)."""
import sys

SRC = '/home/hatch/workspace/scratch-hellhole/redteam/rt3fix/g_intent6_v4fix.zag'
HELPERS = '/home/hatch/workspace/scratch-hellhole/redteam/rt3fix/v4fix_helpers.zag'
src = open(SRC).read()

def rep(old, new, count=1):
    global src
    assert src.count(old) == count, "pattern count %d != %d for: %r" % (src.count(old), count, old[:80])
    src = src.replace(old, new)

# ---- 1. Stemmer fix: dropped-e branch must run when the full-stem match
# ---- failed too (it was nested inside `if(k==stem.len)`).
old_stem = """            if(k==stem.len){
                let e:i32=j_inflect_end(hay,i+stem.len);
                if(e>=0){return e;}
                if(lastc==101){
                    let m:i32=0;
                    while(m<stem.len-1){if(hay[i+m]!=stem[m]){break;}m=m+1;}
                    if(m==stem.len-1){
                        let e2:i32=j_inflect_ing(hay,i+stem.len-1);
                        if(e2>=0){return e2;}
                    }
                }
                if(j_is_cons(lastc)!=0){"""
new_stem = """            if(k==stem.len){
                let e:i32=j_inflect_end(hay,i+stem.len);
                if(e>=0){return e;}
                if(j_is_cons(lastc)!=0){"""
rep(old_stem, new_stem)

old_dd = """                if(j_is_cons(lastc)!=0){
                    if(i+stem.len<hay.len){
                        if(hay[i+stem.len]==lastc){
                            let e3:i32=j_inflect_deding(hay,i+stem.len+1);
                            if(e3>=0){return e3;}
                        }
                    }
                }
            }
        }
        i=i+1;"""
new_dd = """                if(j_is_cons(lastc)!=0){
                    if(i+stem.len<hay.len){
                        if(hay[i+stem.len]==lastc){
                            let e3:i32=j_inflect_deding(hay,i+stem.len+1);
                            if(e3>=0){return e3;}
                        }
                    }
                }
            }
            if(lastc==101){
                let m:i32=0;
                while(m<stem.len-1){if(hay[i+m]!=stem[m]){break;}m=m+1;}
                if(m==stem.len-1){
                    let e2:i32=j_inflect_ing(hay,i+stem.len-1);
                    if(e2>=0){return e2;}
                }
            }
        }
        i=i+1;"""
rep(old_dd, new_dd)

# ---- 2. Insert helpers before fn g_classify.
helpers = open(HELPERS).read()
rep('fn g_classify(text:[]u8,url:[]u8,codes:[]u8,markers:[]u8)i32 {',
    helpers + '\nfn g_classify(text:[]u8,url:[]u8,codes:[]u8,markers:[]u8)i32 {')

# ---- 3. Iron guard: "iron deficiency" is sincere health context.
rep('if(j_has_stem(t,"iron")!=0){n_A_IRON=n_A_IRON+1;g_markers_append(markers,"iron");}',
    'if(j_has_stem(t,"iron")!=0){if(j_has_word(t,"iron deficiency")==0){if(j_has_word(t,"iron-deficiency")==0){n_A_IRON=n_A_IRON+1;g_markers_append(markers,"iron");}}}')

# ---- 4. Compute just before the contra chain.
rep('    let contra:i32=0;',
    '    let just:i32=j_justify(t);\n    let contra:i32=0;')

# ---- 5. Special-case rules 36-39 FIRST (they also match the general pattern).
rep('if(contra==0){if(n_F_SKY>=1&&n_F_FOOD>=1&&n_F_MADEOF>=1){contra=36;g_codes_append(codes,"P_DA5D");}}',
    'if(contra==0){if(j_da5d_shape(t)!=0){contra=36;g_codes_append(codes,"P_DA5D");}}')
rep('if(contra==0){if(n_F_HABIT>=1&&n_F_LONGEV>=1){contra=37;g_codes_append(codes,"R_IRONY");}}',
    'if(contra==0){if(n_F_HABIT>=1&&n_F_LONGEV>=1&&j_cessation(t)==0&&j_you(t)==0){contra=37;g_codes_append(codes,"R_IRONY");}}')
rep('if(contra==0){if(n_F_DUAL>=1&&n_F_ABSTRACT>=1&&n_F_ENACT>=1){contra=38;g_codes_append(codes,"R_PUN1");}}',
    'if(contra==0){if(just!=0&&n_F_DUAL>=1&&n_F_ABSTRACT>=1&&n_F_ENACT>=1&&j_two_clause(t)!=0){contra=38;g_codes_append(codes,"R_PUN1");}}')
rep('if(contra==0){if(n_F_DISTRUST>=1&&n_F_MAKEUP>=1&&n_F_UNIV>=1){contra=39;g_codes_append(codes,"R_PUN2");}}',
    'if(contra==0){if(n_F_DISTRUST>=1&&j_pun2_pivot(t)!=0){contra=39;g_codes_append(codes,"R_PUN2");}}\n'
    '    if(contra==0){if(j_qa_shape(t)!=0){contra=40;g_codes_append(codes,"N_QA");g_markers_append(markers,"qa");}}\n'
    '    if(contra==0){if(j_deny_shape(t)!=0){contra=41;g_codes_append(codes,"N_DENY");g_markers_append(markers,"deny");}}\n'
    '    if(contra==0){if(j_bar_shape(t)!=0){contra=42;g_codes_append(codes,"N_BAR");g_markers_append(markers,"bar");}}\n'
    '    if(contra==0){if(j_neg_shape(t)!=0){contra=43;g_codes_append(codes,"N_NEG");g_markers_append(markers,"neg");}}')

# ---- 6. Gate remaining contra rules 1-35 on just (37/39 deliberately exempt).
src = src.replace('if(contra==0){if(n_F_HABIT', 'if(contra==0){if(PROTECT37n_F_HABIT')
src = src.replace('if(contra==0){if(n_F_DISTRUST', 'if(contra==0){if(PROTECT39n_F_DISTRUST')
n = src.count('if(contra==0){if(n_')
assert n == 35, "expected 35 remaining rules, found %d" % n
src = src.replace('if(contra==0){if(n_', 'if(contra==0){if(just!=0&&n_')
src = src.replace('if(contra==0){if(PROTECT37n_F_HABIT', 'if(contra==0){if(n_F_HABIT')
src = src.replace('if(contra==0){if(PROTECT39n_F_DISTRUST', 'if(contra==0){if(n_F_DISTRUST')

# ---- 7. Decision section: satire insult veto, trope two-clause gate.
# Trope as secondary tag: purpose infinitive corroborates an already-
# established joke (contra!=0); alone it is not enough (kills A05-style).
rep('    if(ns>=2){ev=3;g_codes_append(codes,"R_SATIRE");}',
    '    if(ns>=2){if(j_insult(t)==0){ev=3;g_codes_append(codes,"R_SATIRE");}}')
rep('        if(nt>=1){ev=2;g_codes_append(codes,"R_TROPE");}',
    '        if(nt>=1){if(j_two_clause(t)!=0){ev=2;g_codes_append(codes,"R_TROPE");}else{if(contra!=0){if(j_purpose_to(t)!=0){ev=2;g_codes_append(codes,"R_TROPE");}}}}')

# ---- 8. New structural rules 44-46 (attempted-X, conspiratorial quote,
# twisted proverb).
rep('    if(contra==0){if(j_neg_shape(t)!=0){contra=43;g_codes_append(codes,"N_NEG");g_markers_append(markers,"neg");}}',
    '    if(contra==0){if(j_neg_shape(t)!=0){contra=43;g_codes_append(codes,"N_NEG");g_markers_append(markers,"neg");}}\n'
    '    if(contra==0){if(j_whisper_shape(t)!=0){contra=45;g_codes_append(codes,"N_WHISPER");g_markers_append(markers,"whisper");}}')

# ---- 9. Pun rules 47-51: idiom + literal-context activation.
rep('    if(contra==0){if(j_whisper_shape(t)!=0){contra=45;g_codes_append(codes,"N_WHISPER");g_markers_append(markers,"whisper");}}',
    '    if(contra==0){if(j_whisper_shape(t)!=0){contra=45;g_codes_append(codes,"N_WHISPER");g_markers_append(markers,"whisper");}}\n'
    '    if(contra==0){if(j_pun_grow(t)!=0){contra=47;g_codes_append(codes,"N_PUN_GROW");g_markers_append(markers,"pun_grow");}}\n'
    '    if(contra==0){if(j_pun_over(t)!=0){contra=48;g_codes_append(codes,"N_PUN_OVER");g_markers_append(markers,"pun_over");}}\n'
    '    if(contra==0){if(j_pun_jump(t)!=0){contra=49;g_codes_append(codes,"N_PUN_JUMP");g_markers_append(markers,"pun_jump");}}\n'
    '    if(contra==0){if(j_pun_line(t)!=0){contra=50;g_codes_append(codes,"N_PUN_LINE");g_markers_append(markers,"pun_line");}}\n'
    '    if(contra==0){if(j_pun_comeout(t)!=0){contra=51;g_codes_append(codes,"N_PUN_OUT");g_markers_append(markers,"pun_out");}}')

open(SRC, 'w').write(src)
print("patched OK")
