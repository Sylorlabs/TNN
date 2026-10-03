#!/bin/sh
# kindswap.sh -- DOMAIN-BLINDNESS Variant B kind-label polarity swap.
# Transcribed verbatim from PREREG.md Section 5 (frozen procedure).
# Applies ON TOP of Variant A outputs.
set -e
export PATH="$HOME/safebin"
# pkind return swap, scoped to the fn pkind body only.
sed '/^fn pkind/,/^}/ { s/return 1;/return K/; s/return 2;/return 1;/; s/return K/return 2;/; }' \
  ref_uc_base.zag > db_base_kswap.zag
# kin/kout swap in the four uni_solve calls (token unique to those calls).
sed 's/5003,1,2,/5003,2,1,/g' db_new.zag > db_new_kswap.zag
# Audits: exactly the intended lines changed, nothing else.
d1=$(diff ref_uc_base.zag db_base_kswap.zag | grep -c '^[<>]')
if [ "$d1" != "4" ]; then echo "AUDIT FAIL: base diff lines=$d1 (want 4)"; exit 1; fi
d2=$(diff db_new.zag db_new_kswap.zag | grep -c '^[<>]')
if [ "$d2" != "8" ]; then echo "AUDIT FAIL: driver diff lines=$d2 (want 8)"; exit 1; fi
echo "AUDIT OK kindswap"
echo "--- pkind after swap:"
sed -n '/^fn pkind/,/^}/p' db_base_kswap.zag
