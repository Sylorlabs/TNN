#!/bin/sh
# fe_build.sh -- assemble fe_full_ctl.zag and fe_full_trt.zag.
# The pinned znc rejects duplicate fn definitions, so redefined base
# functions are stripped from the base copy before concatenation.
export PATH="$HOME/safebin"
F=~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/formal_errors
strip_fns() {
  awk -v pat="^fn ($3)\\(" '
    $0 ~ pat { skip=1; next; }
    /^fn / { skip=0; }
    { if (!skip) print; }
  ' "$1" > "$2"
}
strip_fns "$F/fe_base.zag" "$F/fe_base_nomain.zag" "main"
cat "$F/fe_base_nomain.zag" "$F/fe_audit.zag" "$F/fe_driver.zag" > "$F/fe_full_ctl.zag"
strip_fns "$F/fe_base.zag" "$F/fe_base_stripped.zag" "main|t2_trial|t2_exec"
strip_fns "$F/fe_audit.zag" "$F/fe_audit_nofearm.zag" "fe_arm"
cat "$F/fe_base_stripped.zag" "$F/fe_audit_nofearm.zag" "$F/fe_patch.zag" "$F/fe_driver.zag" > "$F/fe_full_trt.zag"
echo "assembled ctl=$(wc -l < "$F/fe_full_ctl.zag") trt=$(wc -l < "$F/fe_full_trt.zag")"
echo "dup check ctl:"
grep -c "^fn t2_trial(\|^fn t2_exec(\|^fn main(\|^fn fe_arm(" "$F/fe_full_ctl.zag"
echo "dup check trt:"
grep -c "^fn t2_trial(\|^fn t2_exec(\|^fn main(\|^fn fe_arm(" "$F/fe_full_trt.zag"
