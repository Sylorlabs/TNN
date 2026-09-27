#!/usr/bin/env python3
"""Attempt-3 clean-room premise-frame parser (deterministic, label-blind).

Reads ONLY:
  ~/workspace/epi_a3/blind/train_blind.tsv   (opaque ids T0001-T0448)
  ~/workspace/epi_a3/blind/heldout_blind.tsv (opaque ids H0001-H0192)
Emits: frames.tsv, vocab.tsv, addr.tsv, classmeta.tsv, antonym.tsv,
       idmap.tsv, massaddr.tsv  (all integer-coded, sorted, deterministic).

All linguistic tables below are GENERAL linguistic knowledge ( Evaluative
dimensions, antonym pairs, word-number map, verb lists, constructional
patterns ). No label information is used anywhere.
Provenance for each table is documented in TABLES.md.
"""
import re, sys, os, collections

WORK = os.path.dirname(os.path.abspath(__file__))
BLIND = os.path.expanduser("~/workspace/epi_a3/blind")

# --------------------------------------------------------------------------
# Table 1: word-number map (general linguistic knowledge)
# --------------------------------------------------------------------------
WORDNUM = {
    "zero":0,"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,
    "eight":8,"nine":9,"ten":10,"eleven":11,"twelve":12,"thirteen":13,
    "fourteen":14,"fifteen":15,"sixteen":16,"seventeen":17,"eighteen":18,
    "nineteen":19,"twenty":20,"thirty":30,"forty":40,"fifty":50,"sixty":60,
    "seventy":70,"eighty":80,"ninety":90,"hundred":100,"thousand":1000,
    "million":1000000,"billion":1000000000,"dozen":12,
}
# "baker's dozen" handled as a special phrase -> 13

# --------------------------------------------------------------------------
# Table 2: evaluative dimension lexicon: adjective -> dimension
# (dimension words, not topic words; general linguistic knowledge)
# --------------------------------------------------------------------------
DIM_OF_ADJ = {}
def _dim(dim, words):
    for w in words:
        DIM_OF_ADJ[w] = dim
_phys = [
    ("size", ["big","large","small","little","long","short","tall","high","low",
              "deep","shallow","wide","narrow","thick","thin","huge","tiny",
              "giant","massive","vast","enormous","minute"]),
    ("time", ["old","young","new","early","late","fast","slow","quick",
              "ancient","modern","brief"]),
    ("temp", ["hot","cold","warm","cool","freezing","boiling","chilly"]),
    ("weight", ["heavy","light","weighty","featherweight"]),
    ("distance", ["far","near","close","distant","remote"]),
    ("countdim", ["many","much","few","numerous","several","countless"]),
    ("sense", ["deaf","blind","mute"]),
]
_eval = [
    ("taste", ["tasty","delicious","yummy","bland","savory","sweet","bitter",
               "sour","salty","spicy","flavorful","tasteless"]),
    ("aesthetic", ["beautiful","ugly","pretty","gorgeous","handsome",
                   "attractive","hideous","elegant","graceful","stylish",
                   "catchy","melodious","vivid","drab","colorful","atmospheric",
                   "cinematic","moody","creative","artistic","poetic","stunning",
                   "breathtaking","exquisite","tasteful","gaudy","kitschy"]),
    ("value", ["important","valuable","worth","worthwhile","meaningful",
               "significant","essential","crucial","vital","overrated",
               "underrated","precious","priceless","treasured","cherished",
               "mattering","matters","mattered","pointless","trivial","respect"]),
    ("fun", ["fun","boring","dull","entertaining","amusing","enjoyable",
             "exciting","thrilling","tedious","interesting","fascinating",
             "captivating","gripping","dull","hilarious","dreary"]),
    ("moral", ["moral","ethical","right","wrong","evil","virtuous","noble",
               "courageous","brave","cowardly","honest","dishonest","kind",
               "cruel","fair","unfair","just","corrupt","decent","good","bad",
               "courage","cowardice","kindness","cruelty"]),
    ("general", ["great","best","worst","better","worse","excellent",
                 "terrible","awful","horrible","wonderful","fantastic",
                 "amazing","incredible","outstanding","superb","mediocre",
                 "lousy","dreadful","phenomenal","splendid","magnificent",
                 "brilliant","stupid","dumb","smart","clever","wise","foolish",
                 "nice","nasty","lovely","finest","greatest","finer"]),
    ("feeling", ["happy","sad","joyful","miserable","alive","calm","calming",
                 "soothing","stressful","relaxing","peaceful","anxious",
                 "lively","dramatic","intense","powerful","moving","touching",
                 "inspiring","depressing","uplifting","afraid","scary",
                 "frightening","comforting","lonely","nostalgic","romantic",
                 "melancholy","euphoric","blissful","serene","restful"]),
]
for _d, _ws in _phys + _eval:
    _dim(_d, _ws)
EVAL_DIMS = {"taste","aesthetic","value","fun","moral","general","feeling"}
# sound/taste/smell/feel/look sense verbs coerce sensory adjectives to
# aesthetic/taste/feeling dimensions (general linguistic knowledge)
SENSE_VERBS = {"sounds":"aesthetic","tastes":"taste","smells":"aesthetic",
               "feels":"feeling","looks":"aesthetic","sound":"aesthetic",
               "taste":"taste","smell":"aesthetic","feel":"feeling",
               "look":"aesthetic"}
ABSTRACT_NOUNS = {"form","kind","way","type","genre","style","sort","manner"}

# --------------------------------------------------------------------------
# Table 3: antonym pairs (general linguistic knowledge)
# --------------------------------------------------------------------------
ANTONYMS = [
    ("hot","cold"),("warm","cool"),("big","small"),("large","small"),
    ("big","little"),("long","short"),("tall","short"),("high","low"),
    ("deep","shallow"),("wide","narrow"),("thick","thin"),("heavy","light"),
    ("fast","slow"),("quick","slow"),("early","late"),("old","new"),
    ("young","old"),("old","young"),("new","old"),("light","dark"),
    ("bright","dim"),("bright","dark"),("near","far"),("close","far"),
    ("close","distant"),("rich","poor"),("wealthy","poor"),("strong","weak"),
    ("hard","soft"),("loud","quiet"),("loud","soft"),("clean","dirty"),
    ("full","empty"),("true","false"),("real","fake"),("alive","dead"),
    ("living","dead"),("awake","asleep"),("open","closed"),("open","shut"),
    ("safe","dangerous"),("safe","unsafe"),("easy","hard"),
    ("easy","difficult"),("simple","complex"),("happy","sad"),
    ("happy","unhappy"),("good","bad"),("better","worse"),("best","worst"),
    ("beautiful","ugly"),("pretty","ugly"),("honest","dishonest"),
    ("kind","cruel"),("kind","unkind"),("brave","cowardly"),
    ("smart","stupid"),("clever","stupid"),("wise","foolish"),
    ("right","wrong"),("correct","incorrect"),("legal","illegal"),
    ("moral","immoral"),("ethical","unethical"),("possible","impossible"),
    ("visible","invisible"),("natural","artificial"),
    ("natural","unnatural"),("wet","dry"),("smooth","rough"),
    ("sweet","sour"),("sweet","bitter"),("win","lose"),("love","hate"),
    ("like","dislike"),("remember","forget"),("create","destroy"),
    ("build","destroy"),("give","take"),("arrive","depart"),("come","go"),
    ("begin","end"),("start","finish"),("start","end"),("rise","fall"),
    ("increase","decrease"),("expand","contract"),("appear","disappear"),
    ("include","exclude"),("remember","forget"),("pass","fail"),
]

# --------------------------------------------------------------------------
# Table 4: verb lists (general linguistic knowledge)
# --------------------------------------------------------------------------
AUX = {"am","is","are","was","were","be","been","being","has","have","had",
       "having","do","does","did","done","doing","will","would","shall",
       "should","can","could","may","might","must","ought"}
LEX_VERBS = """connect connects connected wear wears wore worn cause causes caused
make makes made lead leads led generate generates generated produce produces produced
create creates created trigger triggers triggered raise raises raised lower lowers lowered
increase increases increased decrease decreases decreased shorten shortens shortened
give gives gave given prevent prevents prevented stop stops stopped flush flushes flushed
prove proves proved proven know knows knew known think thinks thought feel feels felt
believe believes believed say says said claim claims claimed show shows showed shown
find finds found discover discovers discovered invent invents invented write writes wrote written
compose composes composed paint paints painted build builds built found founds founded
complete completes completed end ends ended begin begins began begun start starts started
win wins won lose loses lost beat beats beaten assassinate assassinates assassinated
kill kills killed die dies died lie lies lay lain stand stands stood sit sits sat
live lives lived grow grows grew grown occur occurs occurred happen happens happened
take takes took taken last lasts lasted matter matters mattered mean means meant
expand expands expanded float floats floated freeze freezes froze frozen melt melts melted
need needs needed want wants wanted use uses used require requires required
sound sounds sounded look looks looked seem seems seemed become becomes became become
get gets got gotten turn turns turned go goes went gone come comes came come
run runs ran run work works worked help helps helped allow allows allowed
keep keeps kept hold holds held carry carries carried bring brings brought
send sends sent tell tells told ask asks asked call calls called name names named
consider considers considered remain remains remained stay stays stayed
appear appears appeared disappear disappears disappeared exist exists existed
belong belongs belonged contain contains contained include includes included
consist consists consisted represent represents represented serve serves served
form forms formed develop develops developed crack cracks cracked shave shaves shaved
touch touches touched eat eats ate eaten drink drinks drank drunk sleep sleeps slept
breathe breathes breathed shiver shivers shivered heal heals healed cure cures cured
vote votes voted elect elects elected rule rules ruled govern governs governed
fight fights fought attack attacks attacked defend defends defended
conquer conquers conquered explore explores explored sail sails sailed
fly flies flew flown drive drives drove driven walk walks walked swim swims swam swum
climb climbs climbed fall falls fell fallen rise rises rose risen sink sinks sank sunk
burn burns burned boil boils boiled cool cools cooled heat heats heated
weigh weighs weighed measure measures measured cost costs spend spends spent
save saves saved waste wastes wasted earn earns earned pay pays paid
buy buys bought sell sells sold own owns owned result results resulted
contribute contributes contributed separate separates separated taste tastes tasted
circle circles circled erase erases erased offer offers offered deliver delivers delivered
deserve deserves deserved shed drop drops dropped modify modifies modified
title titles titled""".split()
VERB_SET = AUX | set(LEX_VERBS)
VERB_LEMMA = {
    "am":"be","is":"be","are":"be","was":"be","were":"be","been":"be","being":"be",
    "has":"have","had":"have","having":"have",
    "does":"do","did":"do","done":"do","doing":"do",
}
# irregular past/participle -> base (general linguistic knowledge)
IRREG = {
    "wore":"wear","worn":"wear","taught":"teach","thought":"think",
    "felt":"feel","knew":"know","went":"go","gone":"go","took":"take",
    "taken":"take","gave":"give","given":"give","made":"make","led":"lead",
    "proved":"prove","proven":"prove","said":"say","found":"find",
    "wrote":"write","written":"write","built":"build","won":"win",
    "lost":"lose","beaten":"beat","died":"die","lay":"lie","lain":"lie",
    "stood":"stand","sat":"sit","lived":"live","grew":"grow","grown":"grow",
    "froze":"freeze","frozen":"freeze","sank":"sink","sunk":"sink",
    "rose":"rise","risen":"rise","fell":"fall","fallen":"fall",
    "flew":"fly","flown":"fly","drove":"drive","driven":"drive",
    "swam":"swim","swum":"swim","ate":"eat","eaten":"eat","drank":"drink",
    "drunk":"drink","slept":"sleep","chose":"choose","chosen":"choose",
    "broke":"break","broken":"break","spoke":"speak","spoken":"speak",
    "shone":"shine","drew":"draw","drawn":"draw","hung":"hang",
    "meant":"mean","dreamt":"dream","dreamed":"dream","shivered":"shiver",
    "burned":"burn","burnt":"burn","smelled":"smell","smelt":"smell",
    "spelled":"spell","spelt":"spell","learned":"learn","learnt":"learn",
    # regular -ed pasts (silent-e and doubled-consonant safe list)
    "ended":"end","completed":"complete","invented":"invent",
    "discovered":"discover","assassinated":"assassinate",
    "demonstrated":"demonstrate","connected":"connect","started":"start",
    "founded":"found","composed":"compose","painted":"paint",
    "created":"create","developed":"develop","expanded":"expand",
    "floated":"float","melted":"melt","needed":"need","wanted":"want",
    "used":"use","required":"require","seemed":"seem","turned":"turn",
    "called":"call","named":"name","considered":"consider",
    "remained":"remain","stayed":"stay","appeared":"appear",
    "disappeared":"disappear","existed":"exist","belonged":"belong",
    "contained":"contain","included":"include","consisted":"consist",
    "represented":"represent","served":"serve","formed":"form",
    "cracked":"crack","shaved":"shave","touched":"touch",
    "breathed":"breathe","healed":"heal","cured":"cure","voted":"vote",
    "elected":"elect","ruled":"rule","governed":"govern",
    "attacked":"attack","defended":"defend","conquered":"conquer",
    "explored":"explore","sailed":"sail","walked":"walk",
    "climbed":"climb","boiled":"boil","cooled":"cool","heated":"heat",
    "weighed":"weigh","measured":"measure","saved":"save","wasted":"waste",
    "earned":"earn","owned":"own","resulted":"result",
    "contributed":"contribute","located":"locate","situated":"situate",
    "shortened":"shorten","flushed":"flush","proven":"prove",
    "separated":"separate","tasted":"taste","circled":"circle","erased":"erase",
    "offered":"offer","delivered":"deliver","deserved":"deserve","dropped":"drop",
    "modified":"modify","titled":"title",
}
# role nouns for "The <role> of <E> is <V>" (closed class; general knowledge)
ROLE_NOUNS = {"capital","capitals","inventor","discoverer","author","founder",
    "composer","painter","creator","builder","designer","architect","maker",
    "writer","king","queen","president","leader","director","owner",
    "birthplace","headquarters","symbol","emblem","nickname","name","motto",
    "slogan","anthem","flag","seal"}
DEGREE_ADV = {"too","so","very","quite","rather","pretty","really",
              "extremely","incredibly","fairly","somewhat"}
def lemma_verb(w):
    if w in VERB_LEMMA: return VERB_LEMMA[w]
    if w in IRREG: return IRREG[w]
    if w in AUX: return w
    if w.endswith("ies") and len(w)>5:
        return w[:-3]+"y"
    if w.endswith("es") and len(w)>4:
        # sibilant stems take -es (passes->pass); silent-e bases take -s (rises->rise)
        if w.endswith(("ches","shes","xes","zes")):
            return w[:-2]
        stem_s=w[:-1]; stem_es=w[:-2]
        if stem_s.endswith(("se","ze")) and not stem_es.endswith(("ss","zz","sh","ch")):
            return stem_s
        return stem_es
    if w.endswith("s") and len(w)>4 and not w.endswith(("ss","us","is")):
        return w[:-1]
    return w
CAUSAL_VERBS = {"cause","make","lead","generate","produce","create","trigger",
                "raise","lower","increase","decrease","shorten","give","flush",
                "contribute","result"}
ORIGIN_VERBS = {"invent","discover","write","compose","paint","build","found",
                "create","develop"}  # passive use -> origin
DEONTIC_MODALS = {"should","ought","must"}
EXPERIENCER = {"think","thought","feel","felt","believe","believed","would"}

# attribute classes
ACLASS = ["location","date","count","composition","capability","origin","rank",
          "cause","property","possession","event","mechanism","attire",
          "relation","achievement","naming","role","purpose"]
QUANT_CLASSES = {"count","date"}
FUNC_CLASSES = {"capital","origin","role","naming"}  # + location when stative
STATIVE_PLACE_HEADS = {"be","lie","stand","sit"}
NONFUNC_PLACE_HEADS = {"live","grow","occur","happen","find"}

VKINDS = {"NUM":0,"CMP":1,"ADJ":2,"ENT":3,"PHR":4}
TYPES = {"FACTUAL":0,"EVALUATIVE":1,"DEONTIC":2,"CAUSAL":3}

DET = {"a","an","the","this","that","these","those","their","its","his","her",
       "my","your","our","its","some","any","each","every","all","no","such"}
STOP = DET | {"of","to","in","on","at","for","with","by","from","as","and","or",
              "but","than","then","so","too","very","quite","rather","just",
              "only","even","also","still","already","yet","not","never","no",
              "is","are","was","were","be","been","has","have","had","do",
              "does","did","will","would","can","could","should","may","might",
              "must","it","its","they","them","their","we","us","our","you",
              "he","him","his","she","her","i","me","my","who","whom","whose",
              "which","what","that","this","there","here","when","where","why",
              "how","if","because","while","although","though","until","unless",
              "about","above","across","after","against","along","among",
              "around","before","behind","below","beneath","beside","between",
              "beyond","during","except","into","like","near","off","over",
              "through","toward","under","up","upon","within","without","out"}
MONTHS = {"january","february","march","april","may","june","july","august",
          "september","october","november","december"}

# --------------------------------------------------------------------------
# text utilities
# --------------------------------------------------------------------------
def normalize_text(t):
    t = t.replace("\u2019","'").replace("\u2018","'").replace("\u201c",'"') \
         .replace("\u201d",'"').replace("\u2013","-").replace("\u2014","-")
    t = re.sub(r"\bcan\s*not\b","can not",t,flags=re.I)
    t = re.sub(r"\b(can)'t\b",r"\1 not",t,flags=re.I)
    t = re.sub(r"n't\b"," not",t)
    t = re.sub(r"\s+"," ",t).strip()
    return t

def tokenize(t):
    # keep words, numbers, internal apostrophes/hyphens
    return re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?|\d+(?:,\d+)*(?:\.\d+)?|[^\s\w]", t)

def lemmatize(w):
    if w in WORDNUM or w in DIM_OF_ADJ:
        return w
    if len(w) > 4 and w.endswith("ies"):
        return w[:-3]+"y"
    if len(w) > 3 and w.endswith("ses"):
        return w[:-2]
    if len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
        return w[:-1]
    return w

def strip_det(toks):
    i = 0
    while i < len(toks) and toks[i] in DET:
        i += 1
    return toks[i:]

def norm_phrase(toks):
    """lowercase, strip determiners, lemmatize, sort modifiers, head last."""
    toks = [t.lower() for t in toks]
    # split possessive clitics ("baker's" -> "baker")
    toks2=[]
    for t in toks:
        if t.endswith("'s") and len(t)>3:
            toks2.append(t[:-2])
        elif t.endswith("'") and len(t)>2:
            toks2.append(t[:-1])
        else:
            toks2.append(t)
    toks=toks2
    # merge single-letter sequences ("d","c" -> "dc")
    toks3=[]; buf=[]
    for t in toks+[""]:
        if len(t)==1 and t.isalpha():
            buf.append(t)
        else:
            if buf: toks3.append("".join(buf)); buf=[]
            if t: toks3.append(t)
    toks=toks3
    toks = with_pp_to_mod(toks)
    toks = strip_det(toks)
    # split on and/or, normalize each conjunct
    parts, cur = [], []
    for t in toks:
        if t in ("and","or"):
            if cur: parts.append(cur); cur=[]
        else:
            cur.append(t)
    if cur: parts.append(cur)
    out=[]
    for p in parts:
        p=[t for t in p if t not in ("'s",)]
        if not p: continue
        head = lemmatize(p[-1])
        mods = sorted(norm_adj(t) for t in p[:-1] if t not in STOP or t in DIM_OF_ADJ)
        out.append(" ".join(mods+[head]) if mods else head)
    return " and ".join(out)

# noun vocabulary (built from corpus, label-blind) for -ed stripping
NOUN_VOCAB = set()
def build_noun_vocab(items):
    for _id, text in items:
        for t in tokenize(text):
            w = t.lower()
            if w.isalpha() and len(w)>2:
                NOUN_VOCAB.add(lemmatize(w))

def norm_adj(w):
    w = w.lower()
    if w in DIM_OF_ADJ:
        return w
    # "horned" -> "horn" when stem is a known noun (handles "with horns" ~= "horned")
    if len(w)>4 and w.endswith("ed"):
        stem = w[:-2] if not w.endswith("eed") else w[:-1]
        if stem in NOUN_VOCAB:
            return stem
        if w.endswith("ied") and w[:-3]+"y" in NOUN_VOCAB:
            return w[:-3]+"y"
    return lemmatize(w)

def with_pp_to_mod(toks):
    """'helmets with horns' -> ['horn','helmets'] (with-PP noun becomes modifier,
    head noun stays last so norm_phrase heads match the no-PP form)."""
    mods=[]; out=[]
    i=0
    while i < len(toks):
        if toks[i].lower()=="with" and i+1 < len(toks):
            nxt=toks[i+1].lower()
            if nxt not in DET:
                mods.append(lemmatize(nxt))
                i+=2
                continue
        out.append(toks[i]); i+=1
    return mods+out

# --------------------------------------------------------------------------
# entity extraction
# --------------------------------------------------------------------------
COMMON_INITIAL = set("""
a an the this that these those it its he she they we you i my our your his her their
no not never every each all some many few most more less other such what when where
who why how and but or if then than so as at in on of to for with by from be is are
was were has have had do does did will would can could should may might must
there here swimming shivering cracking eating touching drinking
sleeping dreaming breathing walking running working talking thinking feeling being
having doing going coming getting making taking looking seeming becoming turning
long black white red blue green fresh poor rich young old new small large big great
good bad best better worst many much few several various certain real true false
only just even still already yet also either neither both half whole entire full
empty open closed hot cold warm cool dry wet loud quiet quick slow fast early late
high low deep wide narrow thick thin heavy light bright dark clean dirty strong weak
hard soft smooth rough sweet sour bitter salty spicy tiny huge vast enormous minute
ancient modern brief french english american chinese dutch greek roman
""".split())

def proper_nouns(toks):
    """toks: original-case tokens. Returns list of proper-noun phrases (lowercased)."""
    res=[]
    i=0
    n=len(toks)
    while i<n:
        w=toks[i]
        if w and w[0].isupper() and w.lower() not in ("i",):
            # candidate run
            j=i
            while j<n and toks[j] and (toks[j][0].isupper() or toks[j].lower() in ("of","the","de","van","von","st")):
                j+=1
            run=toks[i:j]
            # trim trailing lowercase glue
            while run and run[-1].lower() in ("of","the","de","van","von"):
                run=run[:-1]
            # split on and/or/&
            cur=[]
            for t in run:
                if t.lower() in ("and","or","&"):
                    if cur: res.append(" ".join(cur).lower()); cur=[]
                elif t.lower() not in ("of","the","de","van","von","st"):
                    cur.append(t)
                # keep "of the" inside multiword names
                elif cur:
                    cur.append(t)
            if cur: res.append(" ".join(cur).lower())
            i=j
        else:
            i+=1
    # drop pure-glue results
    return [r for r in res if re.search(r"[a-z]{2,}", r)]

def is_proper_initial(w, toks):
    """Is a clause-initial capitalized word a proper noun?"""
    wl=w.lower()
    if wl in COMMON_INITIAL: return False
    if wl.endswith("ing") and len(toks)>1: return False  # gerund subject
    return True

def extract_entities(orig_toks, low_toks, subj_span):
    ents=set()
    # proper nouns anywhere (non-initial runs)
    for pn in proper_nouns(orig_toks):
        ents.add(pn)
    # initial word check
    if orig_toks and orig_toks[0] and orig_toks[0][0].isupper():
        if is_proper_initial(orig_toks[0], orig_toks):
            ents.add(orig_toks[0].lower())
    # subject head noun + subject phrase
    sub=[t for t in subj_span if t.lower() not in DET]
    if sub:
        head=lemmatize(sub[-1].lower())
        if head not in STOP and len(head)>1:
            ents.add(head)
        ph=norm_phrase(sub)
        if ph and len(ph)>1:
            ents.add(ph)
    return sorted(ents)

# --------------------------------------------------------------------------
# clause -> premise frame(s)
# --------------------------------------------------------------------------
COMPARATIVES = {
    "bigger":"big","smaller":"small","larger":"large","longer":"long",
    "shorter":"short","higher":"high","lower":"low","taller":"tall",
    "faster":"fast","slower":"slow","earlier":"early","later":"late",
    "older":"old","younger":"young","newer":"new","greater":"great",
    "lesser":"less","stronger":"strong","weaker":"weak","happier":"happy",
    "sadder":"sad","easier":"easy","harder":"hard","warmer":"warm",
    "cooler":"cool","hotter":"hot","colder":"cold","brighter":"bright",
    "darker":"dark","cleaner":"clean","dirtier":"dirty","richer":"rich",
    "poorer":"poor","louder":"loud","quieter":"quiet","closer":"close",
    "farther":"far","further":"far","nearer":"near","kinder":"kind",
    "meaner":"mean","nicer":"nice","smarter":"smart","dumber":"dumb",
    "braver":"brave","fairer":"fair","rarer":"rare","simpler":"simple",
    "stranger":"strange","wilder":"wild","calmer":"calm","deeper":"deep",
    "wider":"wide","thicker":"thick","thinner":"thin","heavier":"heavy",
    "lighter":"light","sweeter":"sweet","fresher":"fresh","quicker":"quick",
    "better":"good","worse":"bad","best":"good","worst":"bad",
    "longest":"long","shortest":"short","largest":"large","smallest":"small",
    "biggest":"big","highest":"high","lowest":"low","tallest":"tall",
    "fastest":"fast","slowest":"slow","earliest":"early","latest":"late",
    "oldest":"old","youngest":"young","newest":"new","greatest":"great",
    "strongest":"strong","weakest":"weak","happiest":"happy","saddest":"sad",
    "easiest":"easy","hardest":"hard","warmest":"warm","coolest":"cool",
    "hottest":"hot","coldest":"cold","brightest":"bright","darkest":"dark",
    "cleanest":"clean","dirtiest":"dirty","richest":"rich","poorest":"poor",
    "loudest":"loud","quietest":"quiet","closest":"close","farthest":"far",
    "furthest":"far","nearest":"near","kindest":"kind","meanest":"mean",
    "nicest":"nice","smartest":"smart","bravest":"brave","fairest":"fair",
    "rarest":"rare","simplest":"simple","strangest":"strange",
    "wildest":"wild","calmest":"calm","deepest":"deep","widest":"wide",
    "thickest":"thick","thinnest":"thin","heaviest":"heavy",
    "lightest":"light","sweetest":"sweet","freshest":"fresh",
    "quickest":"quick",
}
SUPERLATIVES = {k for k in COMPARATIVES}
def base_adj(w):
    return COMPARATIVES.get(w.lower(), w.lower())

def find_verb(low):
    for i in range(1,len(low)):
        if low[i] in VERB_SET:
            return i
    return -1

def detect_neg(low):
    for t in low:
        if t in ("not","never","no"):
            return 1
    return 0

def parse_number_phrase(low, start):
    """Parse [number [percent]] at start; returns (value:int|None, next_i)."""
    i=start
    while i<len(low) and low[i] in ("only","about","around","approximately","almost","nearly","exactly","over","under"):
        i+=1
    if i>=len(low): return None,i
    t=low[i]
    v=None
    if re.fullmatch(r"\d+(?:,\d+)*", t):
        v=int(t.replace(",",""))
        i+=1
    elif t in WORDNUM:
        v=WORDNUM[t]; i+=1
        # "twenty one" style
        if i<len(low) and low[i] in WORDNUM and WORDNUM[low[i]]<10 and v>=20 and v%10==0:
            v+=WORDNUM[low[i]]; i+=1
    elif t=="baker's" and i+1<len(low) and low[i+1]=="dozen":
        v=13; i+=2
    if v is None: return None,start
    # scale words
    while i<len(low) and low[i] in ("hundred","thousand","million","billion"):
        v*=WORDNUM[low[i]]; i+=1
    if i<len(low) and low[i] in ("percent","percentage"):
        i+=1
    # BCE/CE
    if i<len(low) and low[i] in ("bce","bc"):
        v=-v; i+=1
    elif i<len(low) and low[i] in ("ce","ad"):
        i+=1
    return v,i

def is_date_tokens(low, i):
    # year-like or month or BCE/CE nearby
    if i>=len(low): return False
    t=low[i]
    if re.fullmatch(r"\d{3,4}", t): return True
    if t in MONTHS: return True
    if t in ("bce","bc","ce","ad","century"): return True
    return False

def comparative_at(low, i):
    """Detect comparative/superlative construction at position i.
    Returns (dim_word, kind, next_i) kind in MORE/LESS/MOST/LEAST or None."""
    t=low[i]
    if t in ("more","less"):
        d = "MORE" if t=="more" else "LESS"
        j=i+1
        dimw=None
        if j<len(low):
            w=low[j]
            if w in DIM_OF_ADJ or w in COMPARATIVES:
                dimw=base_adj(w); j+=1
            elif w not in STOP and w.isalpha():
                dimw=w; j+=1  # noun dimension e.g. "more courage"
        return dimw,d,j
    if t in ("most","least"):
        d="MORE" if t=="most" else "LESS"
        j=i+1; dimw=None
        if j<len(low) and (low[j] in DIM_OF_ADJ or low[j] in COMPARATIVES):
            dimw=base_adj(low[j]); j+=1
        return dimw,d,j
    if t in COMPARATIVES:
        # -er form: MORE/LESS by antonym direction? use dim table sign below
        return base_adj(t),"ER",i+1
    return None

def find_cmp(pred):
    """Find comparative/superlative in pred. Returns (idx, dimw, kind, nx) or None."""
    for i in range(len(pred)):
        t=pred[i]
        if t=="the" and i==0:
            continue
        c=comparative_at(pred,i)
        if c:
            dimw,kind,nx=c
            return (i,dimw,kind,nx)
    return None

def er_direction(base):
    LESS_BASES={"small","little","short","low","slow","late","young","cool",
                "cold","light","dark","dim","far","distant","poor","weak",
                "soft","quiet","dirty","empty","false","sad","unhappy","bad",
                "worse","ugly","thin","narrow","shallow"}
    return "LESS" if base in LESS_BASES else "MORE"

def dim_of(word, verb_lemma):
    if word in SENSE_VERBS and False:
        pass
    d=DIM_OF_ADJ.get(word)
    if d: return d
    return None

def parse_value(pred, head, sense_dim):
    """Returns (vkind, vcode_text, vnum)."""
    if not pred:
        return "PHR","",-1
    # "unable to X" / "able to X"
    if pred[0] in ("unable","able"):
        rest=pred[2:] if len(pred)>1 and pred[1]=="to" else pred[1:]
        return "PHR",norm_phrase(rest),-1
    # number first
    v,ni=parse_number_phrase(pred,0)
    if v is not None and ni>=len(pred)-1:
        return "NUM",str(v),v
    # comparative handled by caller for be; here generic
    return "PHR",norm_phrase(with_pp_to_mod(pred)),-1

def parse_be_complement(pred, neg, sense_dim, deontic):
    aclass="property"; adim=""; vkind="PHR"; vcode_text=""; vnum=-1
    vdir=0; vcmp=""; vadj=""; vent=""; ctype="FACTUAL"
    if not pred:
        return aclass,adim,vkind,vcode_text,vnum,vdir,vcmp,vadj,vent,ctype
    # comparative / superlative (find anywhere, skip leading "the")
    fc=find_cmp(pred)
    if fc:
        idx,dimw,kind,nx=fc
        # "the most honest kind": skip leading the handled earlier; pred[0] is most
        dim = dim_of(dimw,"") if dimw else None
        if sense_dim and dimw: dim=sense_dim
        # abstract noun after superlative -> value dimension
        restn=nx
        if restn<len(pred) and pred[restn] in ABSTRACT_NOUNS and dim not in EVAL_DIMS:
            dim="value"
        aclass="rank"; adim=dim or "general"
        if kind=="ER":
            vdir=-1 if er_direction(dimw or "")=="LESS" else 1
        else:
            vdir=1 if kind in ("MORE",) else -1
        # comparator: after "than" or the class noun
        cmp_toks=[]
        if "than" in pred:
            cmp_toks=pred[pred.index("than")+1:]
        else:
            cmp_toks=pred[nx:]
        vcmp=norm_phrase(cmp_toks) if cmp_toks else ""
        vkind="CMP"
        vcode_text=("more:" if vdir>0 else "less:")+adim+":"+vcmp
        if adim in EVAL_DIMS: ctype="EVALUATIVE"
        return aclass,adim,vkind,vcode_text,vnum,vdir,vcmp,vadj,vent,ctype
    # degree adverbs before the real complement ("too slow"); "able" stripped
    # so "able to vomit" matches "unable to vomit" (negation carries polarity)
    while pred and (pred[0] in DEGREE_ADV or pred[0]=="able" or
                    pred[0] in ("physically","mentally","generally","usually",
                                "often","simply","merely","just")):
        pred=pred[1:]
    if not pred:
        return aclass,adim,vkind,vcode_text,vnum,vdir,vcmp,vadj,vent,ctype
    # "more <noun> than" handled above (more/less branch)
    # PP location/date
    if pred[0] in ("in","at","on","near","from"):
        rest=pred[1:]
        if rest and is_date_tokens(rest,0):
            aclass="date"
            v,ni=parse_number_phrase(rest,0)
            if v is not None:
                vkind="NUM"; vcode_text=str(v); vnum=v
            else:
                vkind="PHR"; vcode_text=norm_phrase(rest)
        else:
            aclass="location"
            vkind,vcode_text,vnum=parse_value(rest,"be",sense_dim)
            vent=vcode_text
            vkind="ENT"
        return aclass,adim,vkind,vcode_text,vnum,vdir,vcmp,vadj,vent,ctype
    # number
    v,ni=parse_number_phrase(pred,0)
    if v is not None and ni>=len(pred)-1:
        aclass="count"; vkind="NUM"; vcode_text=str(v); vnum=v
        return aclass,adim,vkind,vcode_text,vnum,vdir,vcmp,vadj,vent,ctype
    # "a/an <noun>" composition; lone "a" is the letter A
    if pred[0] in ("a","an"):
        if len(pred)>1:
            aclass="composition"
            vkind="ENT"; vcode_text=norm_phrase(with_pp_to_mod(pred)); vent=vcode_text
        else:
            aclass="composition"
            vkind="PHR"; vcode_text="a"
        return aclass,adim,vkind,vcode_text,vnum,vdir,vcmp,vadj,vent,ctype
    # adjective predicate
    w0=norm_adj(pred[0])
    if w0 in DIM_OF_ADJ:
        d=DIM_OF_ADJ[w0]
        if sense_dim: d=sense_dim
        aclass="property"; adim=d; vkind="ADJ"; vcode_text=w0; vadj=w0
        if d in EVAL_DIMS: ctype="EVALUATIVE"
        return aclass,adim,vkind,vcode_text,vnum,vdir,vcmp,vadj,vent,ctype
    # default
    vkind,vcode_text,vnum=parse_value(pred,"be",sense_dim)
    return aclass,adim,vkind,vcode_text,vnum,vdir,vcmp,vadj,vent,ctype

def mkframe(ents,head,aclass,adim,vkind,vcode_text,vnum,vdir,vcmp,vadj,vent,
            neg,ctype,pred=None,low=None):
    return {"ents":ents,"head":head,"aclass":aclass,"adim":adim or "",
            "vkind":vkind,"vtext":vcode_text,"vnum":vnum,"vdir":vdir,
            "vcmp":vcmp,"vadj":vadj,"vent":vent,"neg":neg,"type":ctype}

# --------------------------------------------------------------------------
# part 3: driver — clause splitting, two-phase parse, coding, emission
# --------------------------------------------------------------------------
NEGWORDS = ("not","never","no","unable","cannot","can't","won't","don't",
            "doesn't","didn't","isn't","aren't","wasn't","weren't","haven't",
            "hasn't","hadn't","couldn't","wouldn't","shouldn't")

def split_clauses(text):
    text=normalize_text(text)
    # colon tail: "X: seven" -> keep tail appended for value extraction
    text=text.replace(" : ",": ").replace(" :",":")
    parts=[p.strip() for p in text.split(";")]
    clauses=[]
    # subordinate split: "I feel alive when the weather is dramatic".
    # guarded: not "a while", not "since <year>"
    SUBSPLIT=re.compile(r"(?<![Aa] )\s+(?:when|while|because)\s+|\s+since\s+(?!\d)",
                        re.IGNORECASE)
    SUBLEAD=re.compile(r"^(?:when|while|because|since|if)\s+", re.IGNORECASE)
    for p in parts:
        # ", not Y" / ", never Y" ellipsis -> separate clause
        m=re.split(r",\s+(?=not\s|never\s)",p)
        for x in m:
            for y in SUBSPLIT.split(x):
                y=SUBLEAD.sub("",y.strip(" .")).strip(" .")
                if y:
                    clauses.append(y)
    return clauses

def parse_item(text):
    frames=[]
    prev_sv=None
    for cl in split_clauses(text):
        orig_toks=tokenize(cl)
        low_all=[t.lower() for t in tokenize(cl)]
        low=[t for t in low_all if t not in (",",".","!","?",";",":","-","--",'"',"'")]
        # ellipsis inheritance: clause starts with not/never/no, no verb
        if low and low[0] in NEGWORDS and find_verb(low)<0 and prev_sv:
            low = prev_sv + low
            orig_toks = tokenize(" ".join(prev_sv)) + orig_toks
        fr=parse_clause_fixed(orig_toks, low)
        v=find_verb(low)
        if v>0:
            prev_sv=low[:v+1]
        frames.extend(fr)
    return frames

def parse_clause_fixed(orig_toks, low):
    """parse_clause with corrected NEG scope + general comparative path."""
    frames=[]
    if not low:
        return frames
    # experiencer
    exp_type=None
    rest=low
    rest_orig=orig_toks
    if len(low)>=2 and low[0]=="i" and low[1] in EXPERIENCER:
        exp_type="EVALUATIVE"
        rest=low[2:]
        if rest[:2]==["believe","in"]:
            rest=rest[2:]
        elif rest[:1]==["in"]:
            rest=rest[1:]
    deontic = any(t in DEONTIC_MODALS for t in rest)
    vi=find_verb(rest)
    if vi<0:
        ents=extract_entities(orig_toks, low, low[:min(3,len(low))])
        if not ents: ents=["unknown"]
        ftype="EVALUATIVE" if exp_type else ("DEONTIC" if deontic else "FACTUAL")
        fc0=find_cmp(rest)
        if fc0:
            # verbless experiencer superlative: "I feel most alive"
            ahead=low[1] if exp_type else "be"
            sdim=SENSE_VERBS.get(low[1]) if exp_type else None
            aclass,adim,vkind,vcode_text,vnum,vdir,vcmp,vadj,vent,ctype = \
                build_comparative(fc0, rest, sdim, ahead)
            frames.append(mkframe(ents,ahead,aclass,adim,vkind,vcode_text,
                                  vnum,vdir,vcmp,vadj,vent,0,ctype,rest,low))
        else:
            frames.append(mkframe(ents,"be","property",None,"PHR",
                                  norm_phrase(rest),-1,0,"","","",0,ftype,rest,low))
        return frames
    # NEG: negation word at or before verb+1 scopes the predicate
    neg=0
    for p,t in enumerate(rest):
        if t in NEGWORDS and p<=vi+1:
            neg=1; break
    # strip neg words for structural parse
    clean=[]
    for p,t in enumerate(rest):
        if t in NEGWORDS and p<=vi+1:
            continue
        clean.append(t)
    nneg_before=sum(1 for p,t in enumerate(rest) if t in NEGWORDS and p<vi)
    vi2=vi-nneg_before
    subj=clean[:vi2]
    verb_tok=clean[vi2]
    head=lemma_verb(verb_tok)
    # do-auxiliary: "did not prove" -> head=prove
    pred=clean[vi2+1:]
    if head=="do" and pred and pred[0] in VERB_SET and pred[0] not in AUX:
        head=lemma_verb(pred[0]); pred=pred[1:]
    # strip leading adverbs from the predicate ("already knew" -> "knew")
    while pred and pred[0] in ("already","just","even","still","also","often",
                               "usually","generally","simply","merely"):
        pred=pred[1:]
    # map orig toks roughly: use low-based entity extraction on clean
    ents=extract_entities(orig_toks, low, subj)
    if not ents: ents=["unknown"]
    sense_dim=SENSE_VERBS.get(verb_tok)

    aclass="event"; adim=""; vkind="PHR"; vcode_text=""
    vnum=-1; vdir=0; vcmp=""; vadj=""; vent=""
    ctype="FACTUAL"

    # role pattern (guarded: role word must be in ROLE_NOUNS, no proper-name part)
    role_frame=None
    if head=="be":
        m=re.match(r"^the (.+) of (.+)$"," ".join(subj))
        if m:
            role,entpart=m.group(1),m.group(2)
            rhead=lemmatize(role.split()[-1])
            if rhead in ROLE_NOUNS:
                role_frame=(role,entpart)
        if not role_frame:
            m2=re.match(r"^(.+)'s (.+)$"," ".join(subj))
            if m2:
                entpart,role=m2.group(1),m2.group(2)
                rhead=lemmatize(role.split()[-1])
                if rhead in ROLE_NOUNS:
                    role_frame=(role,entpart)
    # general comparative check (non-be verbs, incl. have)
    fc=find_cmp(pred) if pred else None

    if role_frame:
        role,entpart=role_frame
        aclass="role"; adim=lemmatize(role.split()[-1])
        for e in extract_entities(tokenize(entpart),[t.lower() for t in tokenize(entpart)],tokenize(entpart)):
            ents.append(e)
        ents=sorted(set(ents))
        vkind,vcode_text,vnum=parse_value(pred, head, sense_dim)
        vkind="ENT"; vent=vcode_text
    elif head in CAUSAL_VERBS:
        aclass="cause"
        vkind,vcode_text,vnum=parse_value(pred, head, sense_dim)
        ctype="CAUSAL"
    elif fc and head not in ("have",):
        aclass,adim,vkind,vcode_text,vnum,vdir,vcmp,vadj,vent,ctype = \
            build_comparative(fc, pred, sense_dim, head)
    elif head=="beat":
        aclass="rank"; adim="general"; vkind="CMP"; vdir=1
        vcmp=norm_phrase(pred); vcode_text="more:general:"+vcmp; ctype="EVALUATIVE"
    elif head=="be":
        aclass,adim,vkind,vcode_text,vnum,vdir,vcmp,vadj,vent,ctype = \
            parse_be_complement(pred, neg, sense_dim, deontic)
        if aclass=="count":
            # unit from subject head ("a baker's dozen is thirteen" -> 13:dozen)
            sh=""
            for t in reversed(subj):
                tt=t[:-2] if t.endswith("'s") else t
                if tt not in STOP and tt not in ("a","an","the"):
                    sh=lemmatize(tt); break
            vcode_text=str(vnum)+":"+sh
    elif head=="have":
        if fc:
            aclass,adim,vkind,vcode_text,vnum,vdir,vcmp,vadj,vent,ctype = \
                build_comparative(fc, pred, sense_dim, head)
        else:
            v,ni=parse_number_phrase(pred,0)
            if v is None:
                # trailing number ("... as humans: seven")
                for i,t in enumerate(pred):
                    vv,nn=parse_number_phrase(pred,i)
                    if vv is not None: v=vv; ni=i+nn; break
            if v is not None:
                aclass="count"; vkind="NUM"; vnum=v
                # counted noun disambiguates ("10 provinces" vs "3 territories")
                unit=""
                if ni<len(pred) and pred[ni] not in STOP and pred[ni] not in (
                        "in","of","total","about","around","over","under","per"):
                    unit=lemmatize(pred[ni])
                vcode_text=str(v)+":"+unit
            elif pred[:2]==["a","name"] or pred[:3]==["the","name","of"]:
                aclass="naming"; vkind,vcode_text,vnum=parse_value(pred[2:], head, sense_dim)
                vkind="ENT"; vent=vcode_text
            else:
                aclass="possession"; vkind,vcode_text,vnum=parse_value(pred, head, sense_dim)
    elif head in ORIGIN_VERBS:
        if pred and pred[0] in ("in","at","on") and len(pred)>1 and is_date_tokens(pred,1):
            aclass="date"
            v,ni=parse_number_phrase(pred,1)
            if v is not None: vkind="NUM"; vcode_text=str(v); vnum=v
            else: vkind="PHR"; vcode_text=norm_phrase(pred[1:])
        else:
            aclass="origin"; vkind,vcode_text,vnum=parse_value(pred, head, sense_dim)
    elif head=="wear":
        aclass="attire"; vkind,vcode_text,vnum=parse_value(pred, head, sense_dim)
    elif head=="connect":
        aclass="relation"; vkind,vcode_text,vnum=parse_value(pred, head, sense_dim)
    elif head in ("locate","situate"):
        aclass="location"; vkind,vcode_text,vnum=parse_value(pred, head, sense_dim)
    elif head=="win":
        aclass="achievement"; vkind,vcode_text,vnum=parse_value(pred, head, sense_dim)
    elif pred and pred[0] in ("in","at","on") and len(pred)>1 and is_date_tokens(pred,1):
        # "ended in 1945", "was completed in 1869": date PP on any verb
        aclass="date"
        v,ni=parse_number_phrase(pred,1)
        if v is not None: vkind="NUM"; vcode_text=str(v); vnum=v
        else: vkind="PHR"; vcode_text=norm_phrase(pred[1:])
    else:
        vkind,vcode_text,vnum=parse_value(pred, head, sense_dim)

    if exp_type: ctype="EVALUATIVE"
    elif deontic: ctype="DEONTIC"
    if ctype=="FACTUAL" and head=="be":
        for i,t in enumerate(pred):
            if t=="way" and i+1<len(pred) and pred[i+1]=="of":
                aclass="mechanism"; break
    if not vcode_text and vkind=="PHR":
        # intransitive / elliptical: value is the event itself ("apples float")
        vcode_text=head
    frames.append(mkframe(ents,head,aclass,adim or None,vkind,vcode_text,
                          vnum,vdir,vcmp,vadj,vent,neg,ctype,pred,low))
    return frames

VERB_DIM={"matter":"value"}

def build_comparative(fc, pred, sense_dim, head):
    idx,dimw,kind,nx=fc
    dim=dim_of(dimw,"") if dimw else None
    if sense_dim and dimw: dim=sense_dim
    if dim is None and head in VERB_DIM: dim=VERB_DIM[head]
    if nx<len(pred) and pred[nx] in ABSTRACT_NOUNS and dim not in EVAL_DIMS:
        dim="value"
    aclass="rank"; adim=dim or "general"
    if kind=="ER": vdir=-1 if er_direction(dimw or "")=="LESS" else 1
    else: vdir=1 if kind=="MORE" else -1
    cmp_toks=[]
    if "than" in pred: cmp_toks=pred[pred.index("than")+1:]
    else: cmp_toks=pred[nx:]
    vcmp=norm_phrase(cmp_toks) if cmp_toks else ""
    vkind="CMP"; vnum=-1; vadj=""; vent=""
    vcode_text=("more:" if vdir>0 else "less:")+adim+":"+vcmp
    ctype="EVALUATIVE" if adim in EVAL_DIMS else "FACTUAL"
    return aclass,adim,vkind,vcode_text,vnum,vdir,vcmp,vadj,vent,ctype

# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------
def load_items():
    items=[]
    for fn,prefix in (("train_blind.tsv","T"),("heldout_blind.tsv","H")):
        with open(os.path.join(BLIND,fn),encoding="utf-8") as f:
            for line in f:
                line=line.rstrip("\n")
                if line.startswith("id\t"): continue
                iid,text=line.split("\t",1)
                assert iid.startswith(prefix)
                items.append((iid,text))
    return items

def main():
    items=load_items()
    build_noun_vocab(items)
    # internal int ids: T0001->1..T0448->448, H0001->449..H0192->640
    idmap={}
    for iid,_ in items:
        if iid.startswith("T"): idmap[iid]=int(iid[1:])
        else: idmap[iid]=448+int(iid[1:])
    # phase 1: parse
    parsed={}
    for iid,text in items:
        parsed[iid]=parse_item(text)
    # phase 2: mass-addressability for rank dims (train mass, excl self)
    train_ids=[iid for iid,_ in items if iid.startswith("T")]
    dim_items=collections.defaultdict(set)  # dim -> set of train iids with rank:dim
    for iid in train_ids:
        for f in parsed[iid]:
            if f["aclass"]=="rank" and f["adim"]:
                dim_items[f["adim"]].add(iid)
    massaddr={}
    for iid,_ in items:
        for f in parsed[iid]:
            if f["aclass"]=="rank" and f["adim"] and f["adim"] not in EVAL_DIMS \
               and f["type"]=="FACTUAL":
                others=dim_items[f["adim"]]-{iid} if iid.startswith("T") else dim_items[f["adim"]]
                addressed=1 if others else 0
                massaddr[(iid,f["adim"])]=addressed
                if not addressed:
                    f["type"]="EVALUATIVE"  # mass-unaddressable dimension
    # item-level TYPE: any EVALUATIVE -> EVALUATIVE etc.
    item_type={}
    for iid,_ in items:
        ts=[f["type"] for f in parsed[iid]]
        if "EVALUATIVE" in ts: item_type[iid]="EVALUATIVE"
        elif "DEONTIC" in ts: item_type[iid]="DEONTIC"
        elif "CAUSAL" in ts: item_type[iid]="CAUSAL"
        else: item_type[iid]="FACTUAL"
    # ---- vocab coding ----
    voc=collections.OrderedDict()  # (ns,text)->code
    def code(ns,text):
        key=(ns,text)
        if key not in voc: voc[key]=len([k for k in voc if k[0]==ns])
        return voc[key]
    # ---- emit frames ----
    frows=[]
    for iid,_ in items:
        ii=idmap[iid]
        for pi,f in enumerate(parsed[iid]):
            ents=f["ents"][:6]
            while len(ents)<6: ents.append("")
            erow=[ii,pi,len([e for e in f["ents"][:6] if e])]
            erow+=["" if e=="" else code("ent",e) for e in ents]
            erow+=[code("ahead",f["head"]),code("aclass",f["aclass"]),
                   code("adim",f["adim"] or "-"),VKINDS[f["vkind"]],
                   code("val",f["vtext"]),f["vnum"],f["vdir"],
                   code("val",f["vcmp"]) if f["vcmp"] else -1,
                   code("adj",f["vadj"]) if f["vadj"] else -1,
                   code("ent",f["vent"]) if f["vent"] else -1,
                   f["neg"],TYPES[f["type"]],TYPES[item_type[iid]],
                   # functional attr: single entity per slot (prereg D2)
                   1 if (f["aclass"] in ("role","origin","naming") or
                         (f["aclass"]=="location" and f["head"] in STATIVE_PLACE_HEADS))
                   else 0]
            frows.append(erow)
            f["_erow"]=erow
    # ---- addressing index ----
    # inverted index: ent -> [(train_iid, pi, frow)]
    inv=collections.defaultdict(list)
    trows={}
    for iid in train_ids:
        for pi,f in enumerate(parsed[iid]):
            for e in f["ents"][:6]:
                if e: inv[e].append((iid,pi,f))
    arows=[]
    for iid,_ in items:
        ii=idmap[iid]
        for pi,f in enumerate(parsed[iid]):
            ah=code("ahead",f["head"]); ac=code("aclass",f["aclass"])
            seen=set()
            cands=[]
            for e in f["ents"][:6]:
                if not e: continue
                for (tid,tpj,tf) in inv.get(e,[]):
                    key=(tid,tpj)
                    if key in seen: continue
                    seen.add(key)
                    tah=code("ahead",tf["head"]); tac=code("aclass",tf["aclass"])
                    if tah==ah or tac==ac:
                        cands.append((tid,tpj,tf))
            cands.sort(key=lambda x:x[0])
            for tid,tpj,tf in cands:
                ti=idmap[tid]
                arows.append([ii,pi,ti,tpj,
                    code("ahead",tf["head"]),code("aclass",tf["aclass"]),
                    code("adim",tf["adim"] or "-"),VKINDS[tf["vkind"]],
                    code("val",tf["vtext"]),tf["vnum"],tf["vdir"],
                    code("val",tf["vcmp"]) if tf["vcmp"] else -1,
                    code("adj",tf["vadj"]) if tf["vadj"] else -1,
                    code("ent",tf["vent"]) if tf["vent"] else -1,
                    tf["neg"]])
    arows.sort()
    # ---- write files ----
    def w(path,rows):
        with open(os.path.join(WORK,path),"w",encoding="utf-8") as f:
            for r in rows:
                f.write("\t".join(str(x) for x in r)+"\n")
    w("frames.tsv",[r for r in frows])
    w("addr.tsv",arows)
    # vocab
    vrows=[]
    for (ns,text),c in voc.items():
        vrows.append([ns,c,text])
    vrows.sort(key=lambda r:(r[0],r[1]))
    w("vocab.tsv",vrows)
    # idmap
    w("idmap.tsv",sorted([[v,k] for k,v in idmap.items()]))
    # classmeta
    w("classmeta.tsv",sorted([[code("aclass",c),
        1 if c in QUANT_CLASSES else 0,
        1 if (c in FUNC_CLASSES or c=="location") else 0] for c in ACLASS]))
    # antonyms (adj codes)
    arows2=[]
    for a,b in ANTONYMS:
        arows2.append([code("adj",a),code("adj",b)])
    arows2.sort()
    w("antonym.tsv",arows2)
    # massaddr audit
    w("massaddr.tsv",sorted([[idmap[i],code("adim",d),v] for (i,d),v in massaddr.items()]))
    # ---- well-formedness report ----
    n_items=len(items)
    n_wf=sum(1 for iid,_ in items if parsed[iid] and all(
        f["ents"] and f["head"] and f["aclass"] and f["vtext"] is not None for f in parsed[iid]))
    print(f"items={n_items} wellformed_items={n_wf} frac={n_wf/n_items:.4f}")
    n_prem=sum(len(v) for v in parsed.values())
    print(f"premises={n_prem} addr_rows={len(arows)}")
    # addressing coverage (label-blind)
    cov=sum(1 for iid,_ in items if any(True for pi,f in enumerate(parsed[iid])
           for r in arows if r[0]==idmap[iid] and r[1]==pi and r[2]!=idmap[iid]))
    print(f"items_with_>=1_non-self_address={cov}")
    # type distribution (label-blind)
    tc=collections.Counter(item_type.values())
    print("item_types:",dict(tc))

if __name__=="__main__":
    main()
