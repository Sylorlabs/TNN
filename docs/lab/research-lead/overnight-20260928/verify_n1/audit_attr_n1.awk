# audit_attr_n1.awk -- frozen attribution audit for VERIFY-N1 logs.
# Usage: awk -f audit_attr_n1.awk <runlog>
# Checks (PREREG.md section 7):
#   1. every ATTR line satisfies arr - sched == 1 (frozen delay N=1);
#   2. a DEPLOY line exists at step sched with the same tag AND the same k;
#   3. no ATTR-BAD and no ATTR-COUNT-BAD line exists.
# Exit 0 + "ATTR-AUDIT PASS" iff all hold; else exit 1 + "ATTR-AUDIT FAIL".
/^DEPLOY / {
  s = 0; tg = -1; kk = -1;
  for (i = 1; i <= NF; i++) {
    if ($i ~ /^step=/)  { s  = substr($i, 6) + 0; }
    if ($i ~ /^tag=/)   { tg = substr($i, 5) + 0; }
    if ($i ~ /^k=/)     { kk = substr($i, 3) + 0; }
  }
  dep[s] = tg;
  depk[s] = kk;
  next;
}
/^ATTR / {
  a = 0; s = -1; tg = -1; kk = -1;
  for (i = 1; i <= NF; i++) {
    if ($i ~ /^arr=/)   { a  = substr($i, 5) + 0; }
    if ($i ~ /^sched=/) { s  = substr($i, 7) + 0; }
    if ($i ~ /^tag=/)   { tg = substr($i, 5) + 0; }
    if ($i ~ /^k=/)     { kk = substr($i, 3) + 0; }
  }
  nattr++;
  if (a - s != 1) { bad++; }
  if (!(s in dep)) { bad++; }
  else if (dep[s] != tg) { bad++; }
  else if (depk[s] != kk) { bad++; }
  next;
}
/^ATTR-BAD/ { bad++; next; }
/^ATTR-COUNT-BAD/ { bad++; next; }
END {
  if (nattr == 0) { bad++; }
  if (bad == 0) { print "ATTR-AUDIT PASS nattr=" nattr; exit 0; }
  print "ATTR-AUDIT FAIL bad=" bad " nattr=" nattr; exit 1;
}
