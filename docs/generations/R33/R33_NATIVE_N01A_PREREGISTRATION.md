# R33-N01A corrective native supervision preregistration

Identity `r33-native-n01a-direct-child-v2`. Engineering correction of N01, not
fresh scientific evidence, a reused primary or a full runtime certificate.
Read the retained [independent criticism](R33_NATIVE_N01_REVIEW.md) and
[worker design](R33_NATIVE_N01A_DESIGN.md). The latter describes its original
compile-only BUILD01; main-agent additions below are in selected BUILD02.

Exact schedule: native parent `n01a supervise` performs66 assertions and launches
four actual children: normal exit0 with57-character label; deliberately unguarded
child terminated by parent-owned100ms deadline and reaped withSIGKILL9;
output-flood child terminated by native hard1024-byte file limit withSIGXFSZ25;
and nonexistent executable observed as child exit127. Invalid58/64-character
labels and partial output admission must not start children. Native assertions
also cover exclusive run-root creation/repeated refusal, directory/nonregular
refusal, traversal, exact empty outputs, retained partial artifacts and closes.

Main-agent additions after worker BUILD01: fail-fatal parent guard20s;
persist wall_ms/cpu_us/peakRSS in PROCESSV2 records; classifySIGXFSZ as an
output-limit event; assert unguarded wall>=100ms and<5000ms/RSS present; execute
the flood falsifier. The child hard output cap is installed before execve.

The full `Research/R33_NATIVE_N01A_RUN_PRIMARY_V1` tree, including native child
logs, is the declared write envelope. Native `mkdir` admits that absent root.
An external reservation and launch logs live at the specifically named sibling
`R33_NATIVE_N01A_RESERVATION.json`, `R33_NATIVE_N01A_LAUNCH.stdout` and
`R33_NATIVE_N01A_LAUNCH.host.stderr`, because shell redirection cannot create a
file inside an intentionally nonexistent native-admitted root. Those logs are
subsequently copied into the run root as operational artifact packaging.
No other write root or accepted-state access is admitted.

Freeze selected sources/imports, binary, compiler, protocol and prior review
before this sole primary. N01 remains frozen with its scope deviation. Success
requires66 matching CHECK rows, N01A_FAILURES0, exact terminal marker, parent
exit0 and the four registered child outcomes. All results, including unexpected
failures, must be retained. No Python implementation, supervisor or test runs.

The guarantee is bounded direct-child supervision only. No descendants are
created, no descendant-tree containment or hostile-code sandbox is certified,
and no real symlink falsifier is included. A final reap may rely on normal kernel
process termination; the finite fixture is not proof against a kernel hang.
The guard's hard-limit installation is fail-fatal, not atomically reversible.
Journal recovery, grants, sensory gates, native brain migration and learning
still require their separate evidence. R27 remains canonical60423/restarts0.
