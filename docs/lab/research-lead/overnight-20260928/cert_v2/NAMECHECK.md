# NAMECHECK.md: Cert Harness v2 Worker (CERT-V2)

Step 0 (toolchain guard, mandatory): safebin activated at session start
via the mandated setup loop. `which python3 python` returned NOTHING
(guard-check-done; forbidden interpreters do not resolve in
$HOME/safebin). PATH restricted to $HOME/safebin for every command in
this session. Any forbidden executable invocation would be an automatic
PROCESS-FAIL. No Python, C, or other interpreter was invoked at any
point; all new code is shell (wrappers) plus pure-Zag drivers.

Worker: Cert Harness v2 Worker, spawned 2026-10-02 ~09:07 PDT.
Mission: fold the CERT-SWEEP adaptations into certify_base v2
(auto ev_query detection, scratch-only main trim, base/adapter/
mechanism-experiment classification with NOT APPLICABLE verdicts),
re-run v2 against all 5 sweep targets with identical verdicts,
optionally certify xio_core2 as host+adapter against a trial base.
Deliverables in this directory: NAMECHECK.md (this file), REPORT.md,
the v2 harness (certify_base_v2, cert_driver.zag, cert_driver_noevq.zag),
the host+adapter cert (cert_hostadapter.sh, cert_adapter_driver.zag),
run outputs. Verdict target: CERT-V2-COMPLETE.
