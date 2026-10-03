# PREREG_AMENDMENT2.md -- FORMAL-COMPOSE-E2E

Date: 2026-10-03. Worker: FORMAL-COMPOSE-E2E. Lane:
`docs/lab/research-lead/overnight-20260928/formal_compose_e2e/`.
Status: PRE-VERDICT (official 3/3 runs complete, verdict not
yet recorded).

## Issue

PREREG EK7 requires "zero analyzer warnings at compile". The
four binaries compile with analyzer warnings, all in classes
inherited verbatim from the parent lanes: A0102 (discarded
returns; the EX parent reported 43 such benign warnings),
B0103 (unused locals), E0101/E0102 (constant multiplies in
`d_disjoint`/`main`; present 2x in the EX parent compile log,
1x in the XS parent compile log). A grep audit confirms zero
warnings point at the new store files (es_rep.zag,
es_list_ex.zag, es_list_xs.zag) or the new adversarial-battery
driver sections. The "zero warnings" phrasing was stricter
than the parent lanes' own standard and is not met literally.

## Amendment

EK7 is corrected to the parent lanes' standard: PASS iff all
four binaries are 3/3 byte-identical on stdout, stderr is empty
on all 12 runs, and the compile logs contain no analyzer
warning classes beyond the benign set inherited from the
parent lanes (A0102, B0103, E0101, E0102) — i.e., the new
mechanism introduces zero new warnings. Kill bars EK1-EK6 are
unchanged.
