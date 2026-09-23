# T3-ANOMALY — RUNLOG

**Track:** T3-ANOMALY · **Coordinator:** Tier-3 coordinator (direct execution)
**Frozen prereg:** `crossref/PREREG_TIER3_WAVE2.md` @ `ac4a96c0b1f149d2f7338888de52b0607c4e7bbf`
**Checklist extraction:** programmatic — regex over the frozen file for the
T3-ANOMALY test list + frozen rule. 4 tests + rule extracted; no
transcription from memory.

## 2026-09-23 ~18:20–18:45 UTC — execution

- **Fixture:** local bare repo with 30×5 MB urandom blobs (151 MB total),
  `git update-server-info`, served over loopback HTTP
  (`python3 -m http.server 18923`) from the repo root so the clone URL
  is `http://localhost:18923/`. Real `git-remote-http` child processes.
  Scratch: `~/workspace/scratch-crossref/T3/ANOMALY/ctl/`
  (NOT committed — contains 151 MB fixture + http server).
- **Test 1 (orphan vs recreated dir):** started clone, waited 4 s
  (mid-transfer), `kill -9` the parent `git`; confirmed orphaned
  `git-remote-http` alive (reparented, ppid≠1 chain via `git
  remote-http` shim); recreated `victim/` with sentinel files;
  waited 10 s. Orphan exited on its own. **Sentinels byte-intact —
  no deletion.** (Two earlier attempts in this session failed on
  operator error: a self-matching `pgrep -f` that SIGKILLed my own
  shell, and a wrong URL path `/remote.git` → 404; both corrected,
  neither affects the result.)
- **Test 2 (late-rm interleaving):** session A recreates+populates
  immediately; session B `sleep 6 && rm -rf wt && mkdir wt`.
  **3/3 trials: populated tree wiped.** Positive control confirmed.
- **Test 3 (timestamps):** grepped all 28 RUNLOGs. Timestamped wipes:
  SENSESINT ~05:19 UTC, SELFTEST ~05:21 UTC, JOKE ~05:30 UTC
  (2026-09-23; JOKE logged as ~22:30 PDT 2026-09-22). HELLHOLE wipe
  has no precise timestamp in its RUNLOG ("once disappeared after
  successful reads"). Tier-2 closeout's reboot figure: ~05:47 UTC
  (uptime-derived). **All timestamped wipes precede the reboot by
  17–28 min; 11-minute cluster 05:19–05:30.**
- **Test 4 (script audit):** `grep -rn "rm -rf"` over all 28 crew dirs
  (RUNLOGs + on-disk scripts). One literal safe `rm -rf clean` in
  RUNLOGs; variable-form `rm -rf $R` only in
  `CERT/crew/rerun_all_source.sh` (+HTD1 copy) under `set -u` against
  fixed path `~/workspace/certrebuild/work/reruns`; remainder are old
  committed lab harness scripts. **Clean.**
- Wrote VERDICT.md (HYPOTHESIS-CONFIRMED, refined: late-`rm -rf`
  from overlapping retries is the deletion agent; zombie writes ruled
  out; SENSESINT empty-dir variant gets its own verdict line —
  same mechanism, observation between late rm and re-clone of the
  nested `clean/tnn` path).

## Notes

- Fixture + server left running in scratch (not committed). Kill the
  http.server (port 18923) when done with the track.
- No RNG, no network beyond localhost, no repo writes outside the T3
  track dir.
