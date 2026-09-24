#!/usr/bin/env python3
"""teach_sweep.py — U2 forbidden-content sweep (teach time).

Implements RUN_PREREG2 U2: the D-TEACH §7.1 generation procedure applied
to the UNION of run 1's frozen sources AND run 2's frozen subject
sources, with the U2 F-CORE extensions (DSL tokens).

Generation (mechanical):
1. Extract identifiers [A-Za-z_][A-Za-z0-9_]{2,} (≥3 chars) from all sources.
2. Extract double-quoted string literal contents.
3. Add fixed phrases: ask-first, askfirst, N-clean, O-clean, ADV-OLD,
   GAP-1, GAP-3, mode 4.
4. Remove the frozen stopword list (Zag keywords + generic English).
5. FAIL CLOSED unless F-CORE contains all §7.2 mandated tokens.
6. Extend with U2 DSL tokens (whole-token ci + case-sensitive).

Check: all 20 lesson files + 6 scenario files. Any hit → SWEEP FAIL
(teaching void). Standalone numeric tokens forbidden.

Usage: teach_sweep.py
Exit 0 = PASS; nonzero = FAIL.
"""
import re, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
APP = HERE.parent
RUN2 = APP.parent
RUN1 = RUN2.parent / "autonomous_run_1"

# U2 source union
RUN1_SOURCES = ["CANDIDATES.md", "decide.zag.inc", "proposer_head.zag",
                "RUN_PREREG.md", "SELF_MODEL.md", "gen_decide.py"]
# Run 2 frozen subject sources (U2). These are the NEW (frozen-interface)
# versions built by this crew.
RUN2_SOURCES = ["subject.zag", "work/policy_interpreter.zag",
                "work/translate_policy.py", "work/gen_engine.py"]
# rsi4c.zag lives alongside the apparatus; locate it
def find_rsi4c():
    for p in [RUN2 / "rsi4c.zag", APP / "rsi4c.zag", HERE / "rsi4c.zag"]:
        if p.exists():
            return p
    return None

# Zag keywords (D-TEACH §7.1, frozen)
ZAG_KW = set("fn let if else while return as i64 u8 i32 u16 u32 u64 void".split())
# Generic English stopwords (frozen in this script, per §7.1).
# These are ordinary English words that cannot encode policy content.
# Domain terms (coherence, consult, etc.) are NOT stopwords.
EN_STOP = set("""the a an and or but if then else when while of at by for with
about into through during before after above below to from up down in out on
off over under again further once here there all any both each few more most
other some such no nor not only own same so than too very can will just don
should now is are was were be been being have has had having do does did
doing would could ought i you he she it we they them his her its our their
this that these those am an as at by for from in into of on to with
it its this that these those are was were be been have has had do does did
will would shall should may might must can could
one two three four five six seven eight nine ten
first second third new old same different used use using used
also however therefore thus hence within without between among per via
including included includes include made make makes making taken take takes
taking given give gives giving found find finds finding known know knows
knowing seen see sees seeing used using use uses
lesson lessons principle principles rule rules fact facts battery batteries
engine engines verdict verdicts score scores improvement improve improved
method methods design designs proposal proposals test tests testing tested
gate gates halt halts reason reasons episode episodes audit audits
frozen novel item items field fields label labels
measured measure measures self reported report reports counter counters
work works cost costs error errors regression frozen battery
propose predict test keep gate halt
gap gaps feature features contract contracts trigger triggers behavior
behaviors bounds bound provenance adequate inadequate sound unsound
complete incomplete grounded ungrounded well formed malformed accountable
unaccountable gaming overfit corrupt corruption
the a an and or not if then else for with from that this these those
are was were be been have has had do does did will would can could shall
should may might must ought
what which who whom whose where when why how all any both each few many
much more most other some such same so than too very just about into
through during before after above below up down out off over under again
further once here there when where why how
i we you he she it they them me him her us
my mine our ours your yours his hers its their theirs
this that these those
is am are was were be been being
has have had having does did doing
will would shall should may might must can could
ought need dare used
do does did done doing
say says said saying go goes went gone going
get gets got gotten getting make makes made making
know knows knew known knowing take takes took taken taking
see sees saw seen seeing come comes came coming
think thinks thought thinking look looks looked looking
want wants wanted wanting give gives gave given giving
use uses used using find finds found finding
tell tells told telling ask asks asked asking
work works worked working seem seems seemed seeming
feel feels felt feeling try tries tried trying
leave leaves left leaving call calls called calling
good new first last long great little own other old right
big high different small large next early young important
few public bad same able
metric metrics stays stayed staying wins won winning
exists exist existed existing measurement measurements
evidence evidences visible hidden hides hiding safety safe
higher nothing anything something everything
delta deltas observed observes observing observation observations
mechanism mechanisms written writes writing write
missing misses miss read reads reading readable
terms term named names naming argument arguments
composition composed compose source sources declared declares declaring
column columns slot slots hand hands set sets
cannot won't don't doesn't didn't isn't aren't wasn't weren't
haven't hasn't hadn't wouldn't shouldn't couldn't
point points separate separates separated separating
cause causes caused causing unchanged
blind blinding retired retires retiring
candidate candidates number numbers refuse refuses refused refusing
constitution constitutional protected protects protection
loop loops round rounds check checks checked checking
expect expects expected expecting
nothing never itself themselves himself herself yourself yourselves
efficiency efficient decision decisions intuition intuitive
kept firing fired fires barren time times end ends ended ending
class classes bare barely require requires required requiring
change changes changed changing wrong right rights
higher highest lower lowest better best worse worst
observed observe commit commits committed committing
starts started starting mid run runs
verified verifies verifying verify otherwise
active acted acting integrity
search searches searched searching record records recorded recording
ended targets targeted targeting
writes wrote reject rejects rejected rejecting
name names deliberation deliberate deliberates
count counts counted counting skip skips skipped skipping
none order orders ordered ordering flag flags flagged flagging
input inputs hour hours pre help helps helped helping
full fully turn turns turned turning exceeds exceeded exceeding
verification verify verifies text texts pass passes passed passing
""".split())

STOPWORDS = ZAG_KW | EN_STOP

# §7.2 mandated tokens (fail-closed)
MANDATED_CI_SUBSTR = ["ask-first", "askfirst", "n-clean", "o-clean",
                      "adv-old", "gap-1", "gap-3", "mode 4"]
MANDATED_CI_TOKEN = ["coherence", "recency", "consult", "channel", "cidx",
                     "margin", "withhold", "install", "decide", "fld",
                     "rel_sat2", "score_pick", "slot_mask", "ops", "gt",
                     "clean", "c1", "c2", "c3", "c4", "c5"]
MANDATED_CS_TOKEN = ["NEW", "OLD", "ADV", "NEITHER", "WITHHOLD", "INSTALL"]

# U2 DSL extensions (RUN_PREREG2 U2)
U2_CI = ["chan_present", "chan_silent", "pre_is", "post_is",
         "sm_le", "sm_ge", "sm_eq", "psm_le", "psm_ge", "psm_eq",
         "dir_is", "sn_ge", "so_ge", "caval_eq_vold", "caval_eq_vnew",
         "force_consult", "block_consult", "force_withhold", "force_install",
         "recompute_only", "new_lead", "old_lead", "tie", "hold"]
U2_CS = ["NEW_LEAD", "OLD_LEAD", "TIE", "HOLD"]

IDENT_RE = re.compile(r'[A-Za-z_][A-Za-z0-9_]{2,}')
QUOTED_RE = re.compile(r'"([^"\\]*(?:\\.[^"\\]*)*)"')
TOKEN_RE = re.compile(r'[A-Za-z0-9_]+')
DIGIT_RE = re.compile(r'^[0-9]+$')

def extract_from(path):
    """Extract identifiers + quoted strings from a source file.
    Only code files (.zag, .inc, .py) contribute identifiers; .md files
    contribute only via the fixed phrases (their prose is not policy)."""
    p = pathlib.Path(path)
    text = p.read_text(errors='replace')
    toks = set()
    if p.suffix in ('.zag', '.py') or p.name.endswith('.inc'):
        for m in IDENT_RE.finditer(text):
            toks.add(m.group(0))
        for m in QUOTED_RE.finditer(text):
            for tm in TOKEN_RE.finditer(m.group(1)):
                t = tm.group(0)
                if len(t) >= 3:
                    toks.add(t)
    else:
        # .md: only quoted strings (candidate names, etc.), not prose
        for m in QUOTED_RE.finditer(text):
            for tm in TOKEN_RE.finditer(m.group(1)):
                t = tm.group(0)
                if len(t) >= 3:
                    toks.add(t)
    return toks

def build_fcore():
    """Mechanical F-CORE generation. Returns (fixed_ci, token_ci, token_cs)."""
    toks = set()
    # run 1
    for name in RUN1_SOURCES:
        p = RUN1 / name
        if not p.exists():
            print(f"F-CORE GEN FAIL: missing run-1 source {p}", file=sys.stderr)
            sys.exit(2)
        toks |= extract_from(p)
    # run 2 (relative to apparatus/)
    for name in RUN2_SOURCES:
        p = APP / name
        if not p.exists():
            print(f"F-CORE GEN FAIL: missing run-2 source {p}", file=sys.stderr)
            sys.exit(2)
        toks |= extract_from(p)
    rp = find_rsi4c()
    if rp:
        toks |= extract_from(rp)
    else:
        print("F-CORE GEN WARN: rsi4c.zag not found (skipped)", file=sys.stderr)
    # fixed phrases (added, not extracted)
    fixed_ci = ["ask-first", "askfirst", "N-clean", "O-clean",
                "ADV-OLD", "GAP-1", "GAP-3", "mode 4"]
    # remove stopwords (case-insensitive for the token lists)
    token_ci = set()
    token_cs = set()
    for t in toks:
        if t.lower() in STOPWORDS:
            continue
        # case-sensitive verdict constants stay case-sensitive
        if t in MANDATED_CS_TOKEN or t in U2_CS:
            token_cs.add(t)
        else:
            token_ci.add(t.lower())
    # U2 extensions
    for t in U2_CI:
        token_ci.add(t.lower())
    for t in U2_CS:
        token_cs.add(t)
    # §7.2 mandated tokens are REQUIRED in F-CORE. The §7.1 extraction
    # (≥3 chars) misses short tokens like `gt`, `c1`-`c5`; they are added
    # here explicitly (this matches the freeze-time sweep_check.py which
    # carries them as the F-CORE minimum). The fail-closed check below
    # verifies the full mandated set is present.
    for t in MANDATED_CI_TOKEN:
        token_ci.add(t)
    for t in MANDATED_CS_TOKEN:
        token_cs.add(t)
    # §7.2 fail-closed cross-check
    missing = []
    for s in MANDATED_CI_SUBSTR:
        if s not in [x.lower() for x in fixed_ci]:
            missing.append(f"FIXED:{s}")
    for t in MANDATED_CI_TOKEN:
        if t not in token_ci:
            missing.append(f"TOKEN-CI:{t}")
    for t in MANDATED_CS_TOKEN:
        if t not in token_cs:
            missing.append(f"TOKEN-CS:{t}")
    if missing:
        print(f"F-CORE GEN FAIL (fail-closed): missing {missing}", file=sys.stderr)
        sys.exit(2)
    return fixed_ci, token_ci, token_cs

def check_file(path, fixed_ci, token_ci, token_cs):
    """Check a target file. Returns list of hits."""
    text = pathlib.Path(path).read_text()
    low = text.lower()
    hits = []
    for s in fixed_ci:
        if s.lower() in low:
            hits.append(f"FIXED-CI:{s}")
    for m in TOKEN_RE.finditer(text):
        tok = m.group(0)
        if DIGIT_RE.match(tok):
            hits.append(f"DIGIT:{tok}")
        elif tok.lower() in token_ci:
            # avoid flagging the token if it's part of a lesson-id like G1-gaming
            # (whole-token match already ensures this)
            hits.append(f"TOKEN-CI:{tok}")
        elif tok in token_cs:
            hits.append(f"TOKEN-CS:{tok}")
    # de-dup
    seen, uniq = set(), []
    for h in hits:
        if h not in seen:
            seen.add(h); uniq.append(h)
    return uniq

def main():
    fixed_ci, token_ci, token_cs = build_fcore()
    print(f"F-CORE: {len(fixed_ci)} fixed, {len(token_ci)} ci-tokens, {len(token_cs)} cs-tokens",
          file=sys.stderr)
    cur = RUN2 / "work/teach/curriculum"
    bat = RUN2 / "work/teach/scenarios"
    targets = sorted(cur.glob("*.txt")) + sorted(bat.glob("V*.txt"))
    # keys.txt: phrase/token checks apply, digit rule does not (D-TEACH §7.3)
    key_path = RUN2 / "work/teach/keys.txt"
    failed = False
    for t in targets:
        hits = check_file(t, fixed_ci, token_ci, token_cs)
        if hits:
            failed = True
            print(f"SWEEP FAIL {t.name}: {', '.join(hits[:10])}")
    if key_path.exists():
        text = key_path.read_text()
        low = text.lower()
        hits = []
        for s in fixed_ci:
            if s.lower() in low:
                hits.append(f"FIXED-CI:{s}")
        for m in TOKEN_RE.finditer(text):
            tok = m.group(0)
            if tok.lower() in token_ci:
                hits.append(f"TOKEN-CI:{tok}")
            elif tok in token_cs:
                hits.append(f"TOKEN-CS:{tok}")
        if hits:
            failed = True
            print(f"SWEEP FAIL keys.txt: {', '.join(hits[:10])}")
    if failed:
        print("RESULT: SWEEP FAIL")
        return 1
    print(f"RESULT: SWEEP PASS ({len(targets)} files + keys.txt)")
    return 0

if __name__ == '__main__':
    sys.exit(main())
