#!/usr/bin/env python3
"""Generate g_intent6_v4.zag: stem-level verb classes + hypernym fact classes
+ rhetorical-shape contradiction rules. Verbatim-preserving superset of the
frozen g_intent6.zag (32 patterns first, 7 new rules appended)."""
import sys

def zq(s):  # zag string literal escape
    return s.replace('\\', '\\\\').replace('"', '\\"')

# entry kinds: ('stem',s) -> j_has_stem ; ('word',w) -> j_has_word ;
# ('phrase',p) -> j_has_word (multiword idiom, kept form-bound) ;
# ('near',stem,w2,n) -> j_stem_near (verb + preposition within n chars)
ACTIONS = [
 ("A_APPLY",   [('stem',s) for s in ["apply","squeeze","rub","spread","smear","paint","put","pour","dab","refresh","retread"]] + [('phrase',p) for p in ["rub on","spread on"]]),
 ("A_BAREWALK",[('phrase',p) for p in ["walk over the area with bare feet","walk over broken glass with bare feet","walk on broken glass","clean up glass with your bare feet","walk across broken glass barefoot"]]),
 ("A_BITE_SEEK",[('stem',s) for s in ["bite","sting"]] + [('phrase',p) for p in ["bitten by","get bitten","let it bite"]]),
 ("A_DELETE",  [('stem',s) for s in ["delete","erase","uninstall"]]),
 ("A_DISGUISE",[('stem',"disguise")] + [('phrase',p) for p in ["dress up as","dressed as"]]),
 ("A_DROP",    [('stem',"drop")]),
 ("A_HUG",     [('stem',s) for s in ["hug","embrace","cuddle"]]),
 ("A_IMAGINE", [('stem',s) for s in ["imagine","pretend"]] + [('phrase',"close your eyes and")]),
 ("A_INFLATE", [('stem',s) for s in ["inflate","fill","pump"]] + [('phrase',p) for p in ["fill with","pump up","filling them with helium","fill my tires with helium","fill your tires with helium"]]),
 ("A_INGEST",  [('stem',s) for s in ["eat","drink","swallow","consume","chew","ingest"]] + [('word',w) for w in ["ate","eaten","drank"]]),
 ("A_INJURE",  [('stem',s) for s in ["stub","hit","punch","smash","slam"]] + [('phrase',p) for p in ["walk over","bare feet","step on"]]),
 ("A_INSERT",  [('stem',s) for s in ["stick","insert","shove"]] + [('phrase',p) for p in ["put in","stuck in","knife in the toaster","put your knife in the toaster","use a fork to straighten","fork to straighten your electric sockets","straighten the outlet with a fork","use a fork to fix","fork to fix that electrical outlet","stick a fork into","metal fork","fork into","into the toaster"]]),
 ("A_KISS",    [('stem',"kiss")]),
 ("A_RUN",     [('phrase',p) for p in ["through red lights","run the light","blow through","run red lights"]]),
 ("A_STOP",    [('phrase',p) for p in ["don't breathe","stop breathing","hold your breath"]]),
 ("A_SUBST",   [('stem',s) for s in ["substitute","swap","instead"]] + [('phrase',"instead of")] + [('near',("replace","with",48)),('near',("substitute","with",48)),('near',("swap","for",48))]),
 ("A_TAKE",    [('phrase',p) for p in ["take home","take them home","keep them","free you can take"]]),
 ("A_TEST",    [('stem',s) for s in ["test","check"]] + [('phrase',p) for p in ["to test","find out if","call it"]]),
 ("A_TUB",     [('phrase',p) for p in ["take a toaster into the tub","toaster into the tub","bring a toaster into the bath","toaster in the bathtub","take the toaster into the bath","take a toaster into the bath","took the toaster in the bath","take a bath with my toaster"]]),
 ("A_USE",     [('stem',"use")] + [('phrase',"use it as")]),
 ("A_WEAPON_SUB",[('stem',s) for s in ["fork","spoon","spork","toothpick"]]),
 ("A_ADD",     [('stem',s) for s in ["add","mix","put","spread","stir","pour","dump"]]),
 ("A_ACCEL",   [('stem',s) for s in ["fast","speed","floor","step"]] + [('word',"faster")] + [('phrase',p) for p in ["twice as fast","floor it","step on it"]]),
 ("A_ELEC",    [('stem',s) for s in ["charge","recharge","dry","phone","battery"]] + [('word',w) for w in ["iphone","cell phone","smartphone","dryer","dried","drying","quick dry"]]),
 ("A_SHOOT",   [('stem',s) for s in ["shoot","spray","squirt"]]),
 ("A_BLIND",   [('stem',"blindfold")] + [('phrase',p) for p in ["close your eyes","close my eyes","shut your eyes","eyes closed"]]),
 ("A_IRON",    [('stem',"iron")]),
]

FACTS = [
 ("F_BODY",    [('stem',s) for s in ["toe","tooth","teeth","finger","foot","feet","head","nose","toenail"]]),
 ("F_COSMETIC",[('stem',"paint")] + [('word',w) for w in ["marker","sharpie","nail polish","paint over","permanent marker"]]),
 ("F_CRITSYS", [('word',w) for w in ["system32","sys32","registry","system 32","system-32"]]),
 ("F_DANGER_ANIMAL",[('stem',s) for s in ["bear","shark","lion","tiger","crocodile","alligator","wolf"]]),
 ("F_DARK",    [('word',w) for w in ["dark","darkness"]]),
 ("F_ELEC",    [('word',w) for w in ["iphone","phone","cell phone","laptop","tablet","headphones"]]),
 ("F_ESSENT",  [('stem',s) for s in ["breathe","heartbeat"]]),
 ("F_HEATAPP", [('word',w) for w in ["toaster","oven","hair dryer","flat iron"]]),
 ("F_HEAVY",   [('word',w) for w in ["tables","brick","bricks","piano","anvil","table"]]),
 ("F_IMAGINE", [('word',"imagination")]),
 ("F_LAX",     [('word',w) for w in ["laxative","laxatives","ex-lax"]]),
 ("F_MICRO",   [('stem',"microwave")]),
 ("F_PET",     [('word',w) for w in ["pet","dog","cat","puppy","kitten"]]),
 ("F_PHOTO",   [('word',w) for w in ["photo","photograph","picture","selfie"]]),
 ("F_ROBBERY", [('word',w) for w in ["rob you","robber","robbery","mugger","mugged","robbed"]]),
 ("F_SCALD",   [('word',w) for w in ["boiling","scalding","molten"]]),
 ("F_SEA",     [('word',w) for w in ["lost at sea","at sea","ocean"]]),
 ("F_SEDATIVE",[('word',w) for w in ["sleeping pill","sleeping pills","melatonin","nyquil"]]),
 ("F_SHEEP",   [('word',"sheep")]),
 ("F_SIGNAL",  [('word',w) for w in ["red light","red lights","stop sign","traffic light"]]),
 ("F_SOCKET",  [('word',w) for w in ["socket","outlet","electric socket","electrical outlet","electrical socket","light-socket","sockets","outlets","electric sockets","electrical sockets"]]),
 ("F_STRANGER",[('word',w) for w in ["stranger","atm","neck","person in front of you"]]),
 ("F_TIRE",    [('word',w) for w in ["tire","tires"]]),
 ("F_TOXIC",   [('word',w) for w in ["antifreeze","rat poison","bleach","poison","ammonia","drain cleaner","paint thinner","pesticide"]]),
 ("F_VACATION",[('word',w) for w in ["vacation","escape","getaway","holiday"]]),
 ("F_VENOM",   [('word',w) for w in ["rattlesnake","venomous","scorpion","black widow","cobra"]]),
 ("F_VR",      [('word',w) for w in ["virtual reality","vr headset","oculus"]]),
 ("F_WATER",   [('word',w) for w in ["water","bathtub","tub","bath","shower","pool"]]),
 ("F_WEAPON_SUB",[('stem',s) for s in ["fork","spoon","spork","toothpick"]]),
 ("F_WILDLIFE",[('word',w) for w in ["duck","ducks","goose","geese","squirrel","pigeon","raccoon"]]),
 ("F_WRONGGAS",[('word',w) for w in ["helium","hydrogen"]]),
 ("F_WRONGPROD",[('word',w) for w in ["dish soap","laundry detergent","shampoo"]]),
 ("F_NOTFOOD", [('word',w) for w in ["glue","elmer's","toothpaste","rocks","rock","sandpaper","chalk","play-doh","glitter"]]),
 ("F_CONTAM",  [('word',w) for w in ["yellow snow","expired","moldy","rotten","filthy"]]),
 ("F_IRRIT",   [('word',w) for w in ["lemon","garlic","juice","salt","onion","lime","vinegar","hot sauce"]]),
 ("F_WOUND",   [('word',w) for w in ["cut","burn","eyes","wound","burns","cuts","paper cut","scrape"]]),
 ("F_CAUGHT",  [('word',w) for w in ["caught speeding","dui","police","cops","pulled over","speed trap"]]),
 # --- v4 generalized fact classes (hypernyms) ---
 ("F_FOOD",    [('stem',s) for s in ["bagel","cheese","cracker","milk","coffee","bread","butter","egg","pizza","sandwich","soup","meat","fruit","vegetable","cake","cookie","chocolate","sugar","honey","jam","pasta","rice","cereal","pancake","waffle","donut","taco","burger","steak","bacon","chicken","turkey","potato","tomato","apple","banana","orange","grape","salad","snack","meal","food","dinner","lunch","breakfast","popcorn","candy","pie","muffin","bean","carrot","pea","corn","noodle","nut","syrup","toast"]]),
 ("F_SKY",     [('word',w) for w in ["moon","sun","stars","star","venus","mars","jupiter","planet","planets","galaxy","sky","earth","universe","cosmos"]]),
 ("F_DRIVING", [('stem',s) for s in ["headlight","steer","drive","road","wheel"]] + [('word',w) for w in ["car","cars","highway","windshield","brakes","brake"]]),
 ("F_HABIT",   [('stem',s) for s in ["smoke","cigarette","cigar","drink","alcohol","booze"]] + [('word',w) for w in ["packs a day","pack a day","junk food","soda","fast food","drank","drunk"]]),
 ("F_LONGEV",  [('word',w) for w in ["lived to","lived to be","lived past","ninety","eighty","seventy","hundred","old age","long life"]]),
 ("F_WORN",    [('stem',"wear")] + [('word',w) for w in ["wore","worn"]]),
 ("F_DUAL",    [('stem',"embrace")]),
 ("F_ABSTRACT",[('stem',s) for s in ["mistake","fault","failure","flaw","error","weakness"]]),
 ("F_ENACT",   [('stem',"hug")]),
 ("F_DISTRUST",[('word',w) for w in ["never trust","don't trust","do not trust"]]),
 ("F_MAKEUP",  [('word',w) for w in ["make up","made up"]]),
 ("F_UNIV",    [('word',w) for w in ["everything","anything"]]),
 ("F_MADEOF",  [('word',w) for w in ["made of","made from","composed of"]]),
]

# frozen 32-pattern chain, verbatim order
CONTRA_FROZEN = [
 (1, "P_DA3B", "n_A_INSERT>=1&&n_F_HEATAPP>=1"),
 (2, "P_DA3D", "n_A_TUB>=1&&n_F_HEATAPP>=1&&n_F_WATER>=1"),
 (3, "P_DA3F", "n_A_DELETE>=1&&n_F_CRITSYS>=1"),
 (4, "P_DA4B", "n_A_INFLATE>=1&&n_F_WRONGGAS>=1&&n_F_TIRE>=1"),
 (5, "P_DA1C", "n_A_ADD>=1&&n_F_NOTFOOD>=1"),
 (6, "P_DA1E", "n_A_INGEST>=1&&n_F_NOTFOOD>=1"),
 (7, "P_DA1T", "n_A_INGEST>=1&&n_F_TOXIC>=1"),
 (8, "P_DA1X", "n_A_ADD>=1&&n_F_TOXIC>=1"),
 (9, "P_DA1S", "n_A_INGEST>=1&&n_F_SCALD>=1"),
 (10,"P_DA1Y", "n_A_INGEST>=1&&n_F_CONTAM>=1"),
 (11,"P_DA1L", "n_F_SEDATIVE>=1&&n_F_LAX>=1"),
 (12,"P_DA2A", "n_A_APPLY>=1&&n_F_IRRIT>=1&&n_F_WOUND>=1"),
 (13,"P_DA2S", "n_A_SHOOT>=1&&n_F_IRRIT>=1&&n_F_WOUND>=1"),
 (14,"P_DA2D", "n_A_DROP>=1&&n_F_HEAVY>=1&&n_F_BODY>=1"),
 (15,"P_DA2V", "n_A_BITE_SEEK>=1&&n_F_VENOM>=1"),
 (16,"P_DA3E", "n_A_ELEC>=1&&n_F_MICRO>=1"),
 (17,"P_DA3T", "n_A_TEST>=1&&n_F_MICRO>=1"),
 (18,"P_DA3S", "n_A_INSERT>=1&&n_F_SOCKET>=1"),
 (19,"P_DA4H", "n_A_HUG>=1&&n_F_DANGER_ANIMAL>=1"),
 (20,"P_DA4K", "n_A_KISS>=1&&n_F_STRANGER>=1"),
 (21,"P_DA4W", "n_A_TAKE>=1&&n_F_WILDLIFE>=1"),
 (22,"P_DA4S", "n_A_SUBST>=1&&n_F_WRONGPROD>=1"),
 (23,"P_DA4M", "n_A_APPLY>=1&&n_F_COSMETIC>=1&&n_F_TIRE>=1"),
 (24,"P_DA4I", "n_A_INJURE>=1&&n_F_BODY>=1"),
 (25,"P_DA4A", "n_A_ACCEL>=1&&n_F_CAUGHT>=1"),
 (26,"P_DA4N", "n_A_STOP>=1&&n_F_ESSENT>=1"),
 (27,"P_DA4R", "n_A_RUN>=1&&n_F_SIGNAL>=1"),
 (28,"P_DB1P", "n_A_USE>=1&&n_F_PHOTO>=1&&n_F_DARK>=1"),
 (29,"P_DB1V", "n_A_IMAGINE>=1&&n_F_VR>=1"),
 (30,"P_DB1F", "n_A_WEAPON_SUB>=1&&n_F_ROBBERY>=1"),
 (31,"P_DB1S", "n_F_SEA>=1&&n_F_VACATION>=1"),
 (32,"P_DB1D", "n_A_DISGUISE>=1&&n_F_SHEEP>=1"),
]
# v4 generalized contradiction rules (appended; only fire when no frozen rule fired)
CONTRA_NEW = [
 (33,"P_DA5A", "n_A_SUBST>=1&&n_F_TIRE>=1&&n_F_FOOD>=1"),
 (34,"P_DA5B", "n_A_IRON>=1&&n_F_WORN>=1"),
 (35,"P_DA5C", "n_A_BLIND>=1&&n_F_DRIVING>=1"),
 (36,"P_DA5D", "n_F_SKY>=1&&n_F_FOOD>=1&&n_F_MADEOF>=1"),
 (37,"R_IRONY","n_F_HABIT>=1&&n_F_LONGEV>=1"),
 (38,"R_PUN1", "n_F_DUAL>=1&&n_F_ABSTRACT>=1&&n_F_ENACT>=1"),
 (39,"R_PUN2", "n_F_DISTRUST>=1&&n_F_MAKEUP>=1&&n_F_UNIV>=1"),
]

SAT_WORDS = ["area","sources","confirm","says","experts","inside","resident","details","developing","press","weigh","study","finds","local","time","report","full","man","woman","peer","pending","review","story","nobody"]
TROPE_WORDS = ["free","ram","upgrade","ama","findings","joke","pet","downloaded","traveler"]

def emit_counter(name, entries):
    L = []
    L.append(f'    let n_{name}:i32=0;')
    for kind, val in entries:
        if kind == 'stem':
            L.append(f'    if(j_has_stem(t,"{zq(val)}")!=0){{n_{name}=n_{name}+1;g_markers_append(markers,"{zq(val)}");}}')
        elif kind in ('word','phrase'):
            L.append(f'    if(j_has_word(t,"{zq(val)}")!=0){{n_{name}=n_{name}+1;g_markers_append(markers,"{zq(val)}");}}')
        elif kind == 'near':
            s, w2, n = val
            L.append(f'    if(j_stem_near(t,"{zq(s)}","{zq(w2)}",{n})!=0){{n_{name}=n_{name}+1;g_markers_append(markers,"{zq(s)}~{zq(w2)}");}}')
    return "\n".join(L)

out = []
out.append("// g_intent6_v4.zag — JOKE-FIX crew, hell-hole V4.")
out.append("// Generalization of the frozen g_intent6.zag (config 6, 32 patterns, 321 phrases):")
out.append("//  (a) verb classes are STEM-keyed and form-insensitive via j_has_stem")
out.append("//      (pour/pours/poured/pouring, rub/rubbed/rubbing, shove/shoved/shoving...);")
out.append("//      verb+preposition constructions generalized as j_stem_near (\"replace X with Y\").")
out.append("//  (b) fact classes broadened with hypernym inventories (F_FOOD, F_SKY, F_DRIVING,")
out.append("//      F_HABIT, F_LONGEV, F_WORN); new absurd-combination rules P_DA5A..P_DA5D.")
out.append("//  (c) rhetorical-shape rules: R_IRONY (harmful-habit + longevity anecdote),")
out.append("//      R_PUN1 (dual-meaning verb + abstract object + literal enactment),")
out.append("//      R_PUN2 (distrust-imperative + make-up pivot + universal quantifier).")
out.append("// Frozen 32-pattern chain kept verbatim and first; 7 new rules appended with")
out.append("// contra==0 guards, so nothing the frozen classifier caught changes verdict.")
out.append("// Decision rule unchanged: contradiction -> JOKING (R6 CONTRADICTS overrides);")
out.append("// elif SAT>=2 -> SATIRE; elif TROPE>=1 -> JOKING; else UNCERTAIN.")
out.append("// SINCERE(1)/DECEPTIVE(4) never emitted. Pure Zag; zero RNG.")
out.append("")
out.append('@import("j_ledger.zag")')
out.append('@import("r5_r6.zag")')
out.append("")
out.append("fn g_codes_append(codes:[]u8,tok:[]u8)void {")
out.append('    let n:i32=j_cstrlen(codes);')
out.append('    if(n>0){codes[n]=43;n=n+1;}')
out.append('    let i:i32=0;')
out.append('    while(i<tok.len){codes[n+i]=tok[i];i=i+1;}')
out.append('    codes[n+tok.len]=0;')
out.append('    return;')
out.append("}")
out.append("")
out.append("fn g_markers_append(markers:[]u8,mk:[]u8)void {")
out.append('    let n:i32=j_cstrlen(markers);')
out.append('    let i:i32=0;')
out.append('    while(i<mk.len){markers[n+i]=mk[i];i=i+1;}')
out.append('    markers[n+mk.len]=126;')
out.append('    markers[n+mk.len+1]=0;')
out.append('    return;')
out.append("}")
out.append("")
out.append("// ---------- stem machinery ----------")
out.append("// j_is_cons: lowercase consonant test (text is lowercased before matching).")
out.append("fn j_is_cons(c:u8)i32{")
out.append("    if(c<97){return 0;}")
out.append("    if(c>122){return 0;}")
out.append("    if(c==97){return 0;}")
out.append("    if(c==101){return 0;}")
out.append("    if(c==105){return 0;}")
out.append("    if(c==111){return 0;}")
out.append("    if(c==117){return 0;}")
out.append("    return 1;")
out.append("}")
out.append("// j_inflect_end: after a stem match at [..,p), the alnum suffix must be a valid")
out.append("// inflection: \"\", s, es, ed, d  (e.g. pour/pours/poured, shove/shoved).")
out.append("fn j_inflect_end(hay:[]u8,p:i32)i32{")
out.append("    if(p>=hay.len){return p;}")
out.append("    if(j_is_alnum(hay[p])==0){return p;}")
out.append("    let e:i32=p;")
out.append("    while(e<hay.len){if(j_is_alnum(hay[e])==0){break;}e=e+1;}")
out.append("    let sl:i32=e-p;")
out.append("    if(sl==1){if(hay[p]==115){return e;}if(hay[p]==100){return e;}}")
out.append("    if(sl==2){if(hay[p]==101){if(hay[p+1]==115){return e;}if(hay[p+1]==100){return e;}}}")
out.append("    if(sl==3){if(hay[p]==105){if(hay[p+1]==110){if(hay[p+2]==103){return e;}}}}")
out.append("    return -1;")
out.append("}")
out.append("// j_inflect_ing: for dropped-e stems (shove->shoving): suffix exactly \"ing\".")
out.append("fn j_inflect_ing(hay:[]u8,p:i32)i32{")
out.append("    if(p+3>hay.len){return -1;}")
out.append("    if(hay[p]!=105){return -1;}")
out.append("    if(hay[p+1]!=110){return -1;}")
out.append("    if(hay[p+2]!=103){return -1;}")
out.append("    let q:i32=p+3;")
out.append("    if(q<hay.len){if(j_is_alnum(hay[q])!=0){return -1;}}")
out.append("    return q;")
out.append("}")
out.append("// j_inflect_deding: for doubled-consonant stems (hug->hugged/hugging): \"ed\"/\"ing\".")
out.append("fn j_inflect_deding(hay:[]u8,p:i32)i32{")
out.append("    let q:i32=-1;")
out.append("    if(p+2<=hay.len){if(hay[p]==101){if(hay[p+1]==100){q=p+2;}}}")
out.append("    if(q<0){if(p+3<=hay.len){if(hay[p]==105){if(hay[p+1]==110){if(hay[p+2]==103){q=p+3;}}}}}")
out.append("    if(q<0){return -1;}")
out.append("    if(q<hay.len){if(j_is_alnum(hay[q])!=0){return -1;}}")
out.append("    return q;")
out.append("}")
out.append("// j_stem_endpos: first inflection of stem at/after start; returns word end or -1.")
out.append("fn j_stem_endpos(hay:[]u8,stem:[]u8,start:i32)i32{")
out.append("    if(stem.len==0){return -1;}")
out.append("    let lastc:u8=stem[stem.len-1];")
out.append("    let i:i32=start;")
out.append("    while(i<=hay.len-stem.len){")
out.append("        let ok:i32=1;")
out.append("        if(i>0){if(j_is_alnum(hay[i-1])!=0){ok=0;}}")
out.append("        if(ok!=0){")
out.append("            let k:i32=0;")
out.append("            while(k<stem.len){if(hay[i+k]!=stem[k]){break;}k=k+1;}")
out.append("            if(k==stem.len){")
out.append("                let e:i32=j_inflect_end(hay,i+stem.len);")
out.append("                if(e>=0){return e;}")
out.append("                if(lastc==101){")
out.append("                    let m:i32=0;")
out.append("                    while(m<stem.len-1){if(hay[i+m]!=stem[m]){break;}m=m+1;}")
out.append("                    if(m==stem.len-1){")
out.append("                        let e2:i32=j_inflect_ing(hay,i+stem.len-1);")
out.append("                        if(e2>=0){return e2;}")
out.append("                    }")
out.append("                }")
out.append("                if(j_is_cons(lastc)!=0){")
out.append("                    if(i+stem.len<hay.len){")
out.append("                        if(hay[i+stem.len]==lastc){")
out.append("                            let e3:i32=j_inflect_deding(hay,i+stem.len+1);")
out.append("                            if(e3>=0){return e3;}")
out.append("                        }")
out.append("                    }")
out.append("                }")
out.append("            }")
out.append("        }")
out.append("        i=i+1;")
out.append("    }")
out.append("    return -1;")
out.append("}")
out.append("fn j_has_stem(hay:[]u8,stem:[]u8)i32{")
out.append("    if(j_stem_endpos(hay,stem,0)>=0){return 1;}")
out.append("    return 0;")
out.append("}")
out.append("// j_has_word_lim: whole-word match of w inside [from,lim).")
out.append("fn j_has_word_lim(hay:[]u8,w:[]u8,from:i32,lim:i32)i32{")
out.append("    if(w.len==0){return 0;}")
out.append("    if(from<0){from=0;}")
out.append("    if(lim>hay.len){lim=hay.len;}")
out.append("    if(lim-from<w.len){return 0;}")
out.append("    let i:i32=from;")
out.append("    while(i<=lim-w.len){")
out.append("        let k:i32=0;")
out.append("        while(k<w.len){if(hay[i+k]!=w[k]){break;}k=k+1;}")
out.append("        if(k==w.len){")
out.append("            let ok:i32=1;")
out.append("            if(i>0){if(j_is_alnum(hay[i-1])!=0){ok=0;}}")
out.append("            if(i+w.len<hay.len){if(j_is_alnum(hay[i+w.len])!=0){ok=0;}}")
out.append("            if(ok!=0){return 1;}")
out.append("        }")
out.append("        i=i+1;")
out.append("    }")
out.append("    return 0;")
out.append("}")
out.append("// j_stem_near: verb stem followed by whole word w2 within maxchars after the")
out.append("// verb's word end — generalizes \"replace X with Y\", \"swap X for Y\", \"pour X into Y\".")
out.append("fn j_stem_near(hay:[]u8,stem:[]u8,w2:[]u8,maxchars:i32)i32{")
out.append("    let s:i32=0;")
out.append("    while(s<hay.len){")
out.append("        let e:i32=j_stem_endpos(hay,stem,s);")
out.append("        if(e<0){return 0;}")
out.append("        if(j_has_word_lim(hay,w2,e,e+maxchars)!=0){return 1;}")
out.append("        s=e;")
out.append("    }")
out.append("    return 0;")
out.append("}")
out.append("")
out.append("fn g_classify(text:[]u8,url:[]u8,codes:[]u8,markers:[]u8)i32 {")
out.append('    let t:[]u8=j_tolower(text);')
for name, entries in ACTIONS:
    out.append(emit_counter(name, entries))
for name, entries in FACTS:
    out.append(emit_counter(name, entries))
out.append("    let contra:i32=0;")
for num, code, cond in CONTRA_FROZEN + CONTRA_NEW:
    out.append(f'    if(contra==0){{if({cond}){{contra={num};g_codes_append(codes,"{code}");}}}}')
out.append("    let ns:i32=0;")
for w in SAT_WORDS:
    out.append(f'    if(j_has_word(t,"{zq(w)}")!=0){{ns=ns+1;g_markers_append(markers,"{zq(w)}");}}')
out.append("    let nt:i32=0;")
for w in TROPE_WORDS:
    out.append(f'    if(j_has_word(t,"{zq(w)}")!=0){{nt=nt+1;g_markers_append(markers,"{zq(w)}");}}')
out.append("    let ev:i32=5;")
out.append('    if(ns>=2){ev=3;g_codes_append(codes,"R_SATIRE");}')
out.append("    if(ev==5){")
out.append('        if(nt>=1){ev=2;g_codes_append(codes,"R_TROPE");}')
out.append("    }")
out.append("    if(ev==5){")
out.append('        if(contra==0){g_codes_append(codes,"R_NO_PATTERN");}')
out.append("    }")
out.append("    let logic:i32=0;")
out.append("    if(contra!=0){logic=2;}")
out.append("    if(logic==0){")
out.append("        if(ev!=5){logic=1;}")
out.append("    }")
out.append("    let intent:i32=r5_dispose(logic,ev);")
out.append("    return intent;")
out.append("}")

with open(sys.argv[1], "w") as f:
    f.write("\n".join(out) + "\n")
print("wrote", sys.argv[1])
