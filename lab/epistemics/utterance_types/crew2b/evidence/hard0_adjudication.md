# Evidence: HARD0 scan adjudication

**Scanner:** `tnn-lab/epistemics/utterance_types/redteam_h7/hard0_scan.py`
**Target:** `tnn-lab/epistemics/utterance_types/crew2/learner` (1 file: `h7_main.zag`)
**Result:** `files=1 hits=5 OVERALL=HITS-NEED-ADJUDICATION`

## The 5 hits — all false positives

```
HIT h7_main.zag:993:KEYWORD_LIST_SHAPE:if(load_set(root,fname("tr",t,".txt",fnbuf),ppool,&pu,pent,&pn,64)<0){ _zag_print("ERR tr\n"); return; }
HIT h7_main.zag:1001:KEYWORD_LIST_SHAPE:if(load_set(root,fname("pa",t,".txt",fnbuf),ppool,&pu,pent,&pn,64)<0){ _zag_print("ERR pa\n"); return; }
HIT h7_main.zag:1009:KEYWORD_LIST_SHAPE:if(load_set(root,fname("no",t,".txt",fnbuf),ppool,&pu,pent,&pn,64)<0){ _zag_print("ERR no\n"); return; }
HIT h7_main.zag:1017:KEYWORD_LIST_SHAPE:if(load_set(root,fname("sinc",t,".txt",fnbuf),ppool,&pu,pent,&qn,64)<0){ _zag_print("ERR sinc\n"); return; }
HIT h7_main.zag:1101:KEYWORD_LIST_SHAPE:if(load_set(root,fname("no",t2,".txt",fnbuf),qpool,&qpu,qent,&qn,64)<0){ _zag_print("ERR xno\n"); return; }
```

Each hit is an `if(load_set(...) < 0)` **file-loading error check** for
curriculum probe files (`tr`, `pa`, `no`, `sinc`). The scanner's
`KEYWORD_LIST_SHAPE` pattern matched `if(` adjacent to string literals, but:

- No utterance-type keyword list exists anywhere in the source.
- No type name (`sarcasm`, `joke`, `hypothetical`, `quotation`, `roleplay`)
  appears in any control-flow condition.
- No regexes over utterance types; no per-type branches in `predict()`,
  `learn_exemplar()`, `calibrate()`, or `score_set()`.

**Adjudication: HARD0 CLEAN.** The 5 hits are file-I/O guards, not
type-specific logic. No waiver needed; no source change made.
