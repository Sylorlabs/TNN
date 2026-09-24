# Trace format (TRACE.tsv): TRACE|<item_id>|<stepno>|<op>|<ptr>|<quoted>
# ops: recall (ptr + what the step CLAIMS the entry says), infer (quoted =
#   rule tag), conclude (quoted = resulting claim), assume (quoted =
#   the assumption). ptr "-" = no store pointer.
# For CONF/GOLD/SMUGGLE/CALIB the traces are HONEST records of (bad or good)
# reasoning: recall quotes are exact; the infer rule tag names the (possibly
# sloppy) inference. The fork must catch invalid licensing, not dishonest
# quoting. For ALIBI/POINTER the quotes/pointers are FABRICATED by the
# harness: the fork must re-resolve against STORE.tsv and catch the lie.
# RECUR traces cite GENERATOR-provenance entries that genuinely say the
# false thing: the fork must distrust generator-authored entries.
