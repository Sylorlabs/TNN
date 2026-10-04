# matrix.awk -- verdict matrix of the standing battery over the engine panel.
# Input matrix.txt: ARM|SITE|VERDICT
# Prints one row per site and counts sites with an identical verdict on all 10
# engines. A site that passes on every engine in the panel separates nothing.
FS="|"
BEGIN { split("pre fix M1 M2 M3 M4 M5 M6 M7 M8", nm, " ") ; NP = 10 }
{
  arm = $1; site = $2; ver = $3
  if (!(site in seen)) { seen[site] = 1; order[++m] = site }
  V[site, arm] = (ver == "PASS")
}
END {
  printf "%-34s", "SITE"
  for (i = 1; i <= NP; i++) printf " %-4s", nm[i]
  printf "  nPASS\n"
  all = 0; allpre = 0
  for (i = 1; i <= m; i++) {
    k = order[i]; line = sprintf("%-34s", k); np = 0
    for (j = 1; j <= NP; j++) { p = V[k, nm[j]] + 0; if (p) np = np + 1
      line = line sprintf(" %-4s", (p ? "ok" : "F")) }
    printf "%s   %d\n", line, np
    if (np == NP) { all = all + 1; if (V[k, "pre"]) allpre = allpre + 1 }
  }
  printf "\nsites with the SAME verdict on all 10 engines      = %d of %d\n", all, m
  printf "  ... of those, PASS on E_PRE (all 8 defects live)  = %d\n", allpre
}
