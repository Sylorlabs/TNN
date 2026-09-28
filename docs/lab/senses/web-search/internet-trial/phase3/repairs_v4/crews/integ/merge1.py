#!/usr/bin/env python3
"""Assemble crews/integ/r12_v4.zag from the four verified crew files.

Merge plan (see INTEGRATION_REPORT.md):
- Base: hellhole/r12_v3.zag utilities (byte-identical across crews).
- Lexicons: b1's lex_strong/deny_prefix + b1's new lex_barrier/lex_cmp/lex_cog/lex_evid
             + b3's lex_verb/psyn_has additions + b3's lex_worse + b4's lex_hedge.
- New helpers: all of b1's neg helpers, b3's causal helpers, b2's numeric block,
  b4's cqht helpers (no name collisions).
- neg_scope: b1's rewrite + b3's has_cexp / subject-focus guards.
- competitor: b3's (subjA param).
- scan_text / r12_classify: merged (custom).
- reason_str: merged (tag*16+reason; 7 temporal, 8 comparative, 9 quantifier,
  10 numeric-mismatch). process_line/main: b4's.
"""
import re, hashlib, sys

def get_fns(path):
    src = open(path).read()
    fns = {}
    order = []
    for m in re.finditer(r'^fn (\w+)\(', src, re.M):
        name = m.group(1)
        start = m.start()
        i = src.index('{', m.end() - 1)
        depth = 0
        j = i
        while True:
            c = src[j]
            if c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    break
            j += 1
        fns[name] = src[start:j + 1]
        order.append(name)
    return fns, order

V3, _ = get_fns('/home/hatch/workspace/scratch-hellhole/hellhole/r12_v3.zag')
B1, _ = get_fns('/home/hatch/workspace/scratch-hellhole/crews/b1/r12_neg.zag')
B2, o2 = get_fns('/home/hatch/workspace/scratch-hellhole/crews/b2/r12_con.zag')
B3, _ = get_fns('/home/hatch/workspace/scratch-hellhole/crews/b3/r12_cau.zag')
B4, o4 = get_fns('/home/hatch/workspace/scratch-hellhole/crews/b4/r12_cqht.zag')

out = []

def emit(text):
    out.append(text)

HEADER = """// r12_v4.zag -- R1/R2 repaired stance classifier, hell-hole V4 INTEGRATED.
//
// Merges four independently verified fix crews (all pure Zag, zero RNG):
//   B1 negation    (crews/b1/r12_neg.zag): neg_scope rewrite, deny-lexicon
//        true stems, none-subject deny, reporting-verb fallback, no-evidence
//        generalization, lhedge/whether endorsement guards.
//   B2 contrastive (crews/b2/r12_con.zag): numeric_guard (constrained:
//        unit-aware temp, same-quantity/entity gates, name filter, 5% approx
//        tolerance, concession rule); abstain is pass-through.
//   B3 causal      (crews/b3/r12_cau.zag): causal-verb predicates, mech_aff,
//        cause_deny, prevent_aff, ant_pol, polarity-aware DENY (cneg),
//        opp_outcome_deny, short-stem list, trailing-e bridge.
//   B4 cqht        (crews/b4/r12_cqht.zag): conditionals, quantifiers, hedging,
//        temporal, comparatives; return encoding tag*16+reason.
//
// Interface: argv[1] = TSV file with lines  idx \\t claim \\t title \\t snippet
// Output per line:  idx SP tag SP reason \\n
//   tag: 0=IRRELEVANT/NEUTRAL, 1=AFFIRM, 2=DENY
//   reason: gate | deny-lex | antonym | neg-scope | competing-subject
//           | endorse | neutral | temporal | comparative | quantifier
//           | numeric-mismatch
//
// Deterministic, zero RNG, pure Zag. Compiled with the pinned toolchain:
//   ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 --no-zagd
//
// znc gotchas honored (see ~/AGENTS.md): no `as []i32` indexed tables
// (u8 arenas + LE helpers instead), no slice ==, no argc gate, all slices
// far below the 2^25 limit, no deep else-nesting, no large-struct tricks.
"""

# ---------------------------------------------------------------- header ---
emit(HEADER)

# ------------------------------------------------- section 1: v3 utils ----
for n in ['z_alloc', 'z_free', 'z_cstr', 'read_all', 'z_eq', 'z_has',
          'z_starts', 'z_cplen', 'z_cplen_range', 'z_isupper1', 'z_isdig',
          'z_isvowel', 'z_isspace', 'a_put', 'a_get', 'lower_copy', 'ew',
          'in_stems']:
    emit(V3[n])

# ------------------------------------------------- section 2: lexicons ----
emit("// ==================== lexicons ====================")
for n in ['lex_stop']:
    emit(V3[n])
emit(B3['lex_verb'])          # b3: +expand/float/freeze/happen/melt/occur/result/sink...
for n in ['lex_reporting', 'lex_neg']:
    emit(V3[n])
emit(B1['lex_strong'])        # b1: +contradict/denie/deny/disput/reject
for n in ['lex_weak', 'lex_super', 'lex_conjskip', 'lex_whaux', 'lex_filler',
          'lex_be', 'lex_have']:
    emit(V3[n])
for n in ['lex_barrier', 'lex_cmp', 'lex_cog', 'lex_evid']:  # b1 new
    emit(B1[n])
emit(B3['lex_worse'])         # b3 new
emit(B4['lex_hedge'])         # b4 new

# ------------------------------------------- section 3: shared helpers ----
emit("// ==================== shared helpers ====================")
emit(V3['in_list'])
emit(B1['deny_prefix'])       # b1: +deny/reject/disput/contradict
emit(B3['psyn_has'])          # b3: +float/sink/result/expand/occur/melt/freeze
for n in ['has_superlative', 'is_wc', 'z_toks', 'z_stem', 'z_clauses',
          'z_blank']:
    emit(V3[n])

# ---------------------------------------------- section 4: b1 neg helpers -
emit("// ==================== B1 negation helpers ====================")
for n in ['neg_marker_at', 'has_barrier', 'find_word', 'next_content',
          'strip_eq', 'antonym', 'antonym_tail', 'veto_idiom',
          'matrix_deny']:
    emit(B1[n])

# ------------------------------------------- section 5: b3 causal helpers -
emit("// ==================== B3 causal helpers ====================")
for n in ['is_negw', 'subj_idx', 'has_cexp', 'has_word_after',
          'claim_causal', 'claim_neg', 'ant_idx', 'cause_deny',
          'prevent_aff', 'postpi_deny', 'causal_verb', 'mech_aff',
          'opp_outcome_deny']:
    emit(B3[n])

# ant_pol with extended signature (merged neg_scope needs
# firstA/subjA/pred/cadj)
ant_pol = B3['ant_pol']
ant_pol = ant_pol.replace(
    "fn ant_pol(clause:[]u8,tokC:[]u8,nct:i32,stemC:[]u8,cstmC:[]u8,stemA:[]u8,cstemA:[]u8,ncs:i32,need:i32,nclm:i32,framed:i32,cneg:i32,tmp:[]u8)i32{",
    "fn ant_pol(clause:[]u8,tokC:[]u8,nct:i32,stemC:[]u8,cstmC:[]u8,stemA:[]u8,cstemA:[]u8,ncs:i32,need:i32,nclm:i32,framed:i32,cneg:i32,firstA:[]u8,subjA:[]u8,pred:[]u8,cadj:[]u8,tmp:[]u8)i32{")
ant_pol = ant_pol.replace(
    "let aneg:i32=neg_scope(clause,tokC,nct,ai,stemC,cstmC,stemA,cstemA,ncs,tmp);",
    "let aneg:i32=neg_scope(clause,tokC,nct,ai,stemC,cstmC,stemA,cstemA,ncs,firstA,subjA,pred,cadj,tmp);")
emit(ant_pol)

# -------------------------------------------- section 6: b2 numeric block -
emit("// ==================== B2 numeric guard ====================")
for n in o2:
    if n in B2 and n not in V3:
        emit(B2[n])

# ---------------------------------------------- section 7: b4 cqht helpers
emit("// ==================== B4 CQHT helpers ====================")
for n in o4:
    if n in B4 and n not in V3 and n != 'lex_hedge':
        if n in ('neg_scope', 'competitor', 'scan_text', 'r12_classify',
                 'reason_str', 'process_line', 'main'):
            continue
        emit(B4[n])

# --------------------------------------- section 8: merged neg_scope -----
emit("// ==================== merged neg_scope ====================")
# B1's rewrite + B3's has_cexp guard + B3's subject-focus guard.
ns = B1['neg_scope']
old_wheth = """    // "whether" after pi hedges pre-pi markers away (proposition unknown).
    let wheth:i32=find_word(clause,tokC,nct,"whether",pi+1,tmp);"""
new_wheth = """    // "whether" after pi hedges pre-pi markers away (proposition unknown).
    let wheth:i32=find_word(clause,tokC,nct,"whether",pi+1,tmp);
    // B3-CAU guards: (ce) a "because of" adjunct after pi means a
    // pre-predicate marker scopes the explanation, not the proposition;
    // (sj/snc) a marker directly before a non-claim subject belongs to an
    // upstream chain link, not this predicate.
    let sj:i32=subj_idx(clause,tokC,nct,pi,tmp);
    let snc:i32=0;
    if(sj>=0){
        let gso:i32=a_get(cstmC,2*sj);
        let gsl:i32=a_get(cstmC,2*sj+1);
        if(in_stems(stemC[gso..gso+gsl],stemA,cstemA,ncs)==0){snc=1;}
    }
    let ce:i32=has_cexp(clause,tokC,nct,pi,tmp);"""
assert old_wheth in ns
ns = ns.replace(old_wheth, new_wheth)
old_pre = """        if(j<pi){
            if(wheth>=0){j=j+1;continue;}
            let t:i32=find_word(clause,tokC,nct,"that",j+1,tmp);"""
new_pre = """        if(j<pi){
            if(wheth>=0){j=j+1;continue;}
            if(ce==1){j=j+1;continue;}
            if(sj>=0 && j==sj-1 && snc==1){j=j+1;continue;}
            let t:i32=find_word(clause,tokC,nct,"that",j+1,tmp);"""
assert old_pre in ns
ns = ns.replace(old_pre, new_pre)
# V4-INTEG: "not X but <claim-complement>" is a correction affirming the
# claim ("not at eleven but at noon" vs claim "at noon"): veto the denial.
# (B1's crew never saw this shape; B2's oracle marks it AFFIRM.)
old_cop = """                if(strip_eq(cadj,"dis",st2)==1){return 1;}
            }
            return 1;
        }"""
new_cop = """                if(strip_eq(cadj,"dis",st2)==1){return 1;}
            }
            let bb:i32=find_word(clause,tokC,nct,"but",j+1,tmp);
            if(bb>j){
                let bq:i32=bb+1;
                while(bq<nct){
                    let bso:i32=a_get(cstmC,2*bq);
                    let bsl:i32=a_get(cstmC,2*bq+1);
                    if(z_eq(stemC[bso..bso+bsl],cadj)==1){return 0;}
                    bq=bq+1;
                }
            }
            return 1;
        }"""
assert old_cop in ns
ns = ns.replace(old_cop, new_cop)
emit(ns)

# --------------------------------------- section 9: b3 competitor --------
emit("// ==================== competitor (B3) ====================")
emit(B3['competitor'])

# ----------------------------- section 10: v3 tail helpers ---------------
for n in ['is_interrog', 'claim_numbers', 'has_claim_value']:
    emit(V3[n])

print("mechanical sections assembled:", len(out), "functions")
print("sha of mechanical part:", hashlib.sha256("\n".join(out).encode()).hexdigest()[:16])
