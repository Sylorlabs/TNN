# N08A corrective pre-exposure review

The N08 worker crash is an actual dyld bootstrap abort, not evidence of a failed
native test. The reviewed Apple bootstrap-only policy adds required cryptex
read/mapping/ancestor access and loader syscalls. The broad system.sb was read
for comparison but is not imported. The narrow dyld-support.sb copy exactly
matches its observed SHA25606215a5d32689aefe395c29710e182eb54ba22162f50df8b4842290f8a19bf1c.
The controller imports that frozen local path, not an unpinned changing system
policy. The selected OS sandbox executable and system version remain N08 pins.

Relative to N08, only experiment/source/run identities and this bootstrap import
change. Worker low-level markers and15-check expectations remain deliberately
identical regression controls. No sandbox permission for protected user data,
networking, process creation or arbitrary execution is added. Existing negative
results and source bytes are untouched; no old primary is rerun.

Two new build pairs settled exit0 and are byte-identical. Selected controller
ebd0bbfc04fea66641c8008c35dd88d90450bdc70491fd0b47aef0ec6fedfa89;
worker2389229bde626dfdcf936f5d81e681c9910647b35a4caa7d6566ab7fde15e7d0.
No fixture has run. This is main-agent engineering review only, not independent
approval, a real human grant, training or a complete security/runtime verdict.
