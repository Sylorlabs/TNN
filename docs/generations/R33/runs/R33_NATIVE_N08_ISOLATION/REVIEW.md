# N08 main-agent engineering review before exposure

Two new native executables separate the test supervisor/OS adapter from the
adverse worker. No worker source includes controller keys or protected canary
contents. Exact inline policy generation is in the supervisor; only five
allowlisted mode strings reach it. No profile path, executable or arbitrary
argument can be supplied by worker data. No failure path launches unrestricted
code. Stdin is /dev/null; environment empty; all descriptor numbers3..63 are
closed before Apple's loader runs. The64-descriptor hard ceiling is inherited.

Policy grants only public system-library reads, one exact input, the frozen
worker executable and that child's two capture files. The symlink alias is not
an additional readable input. Worker probes target disposable synthetic fixtures
only; original canary preimage is retained. An unexpected successful fork exits
immediately and is reaped; this remains a failing outcome. Signal0 tests only
permission checking, not signal delivery or arbitrary process-memory access.

The declared OS-policy dependency is Apple's installed /usr/bin/sandbox-exec;
its SHA256 is abc5bb136d6b5cce8fa85d789f78e3326c51ca60cae637b2064adfb67a1dcd9a.
Installed macOS reports26.6.2/build25G83, uid501. Apple calls this launcher
deprecated in the installed manual, and policy syntax private/changeable in
bsd.sb. This experiment neither treats the helper as a newly authored evaluator
nor claims a portable long-term security interface. All new logic is Zag.

Both native builds settled at exit0, with exact pairwise equality. Controller
SHA25662bbc5215c0e8719b7ad2ea6219a1a37e6e946646a8648bc64a18468206bbee1;
worker SHA256e86a016bbd948dfb359d36c589c80c38c429ce37c156951eb31e825622d1cf97.
BUILD01 controller elapsed0.62s/maxRSS27,115,520bytes; worker0.19s/maxRSS10,665,984.
No worker or fixture has executed. Native counters only credit successful worker
count records; an incomplete or failed worker does not gain the planned count.

No original-source search was repeated. One combined read was rejected before
dispatch; a narrower authority/manual/environment read succeeded. There is no
claim of access granted by a blocked request. Main-agent engineering review is
not an independent review, production grant or full protected-runtime certificate.
The exact prospective tests decide only this bounded OS-confined worker lane.
