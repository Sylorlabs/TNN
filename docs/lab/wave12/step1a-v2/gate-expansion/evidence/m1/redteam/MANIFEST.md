# M1 Red-Team Manifest (blind)

**Method under test:** M1 seccomp capability sandbox (Arm C gate-expansion).
**Red-team lead:** blind subagent, 2026-09-25.
**Blinding:** the red team never saw M1's source, binaries, filter bytes, launcher, or test results. The method crew must not have seen these plants before this freeze.
**Toolchain (pinned):** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
**Build:** `znc <plant>.zag -o <plant>` (pure Zag, no imports).
**Kernel calibrated on:** 7.0.0-38-generic (vvar layout verified empirically on this host; plants that parse the vvar page locate it via `/proc/self/maps` and discover live fields empirically, so they are not hardcoded to one layout).

## Miss definition (frozen)

After this freeze, the method crew runs each plant under the frozen M1 launcher.
A plant is a **MISS** iff it **exits 0 AND its stdout varies across 3 sandboxed runs**.
Miss rate > 0 kills this M1 version.

## Plant table

| # | File | SHA-256 (source) | Category | Mechanism (one line) | Unsandboxed variance proof (SHA-256 of stdout, two runs) |
|---|------|------------------|----------|----------------------|----------------------------------------------------------|
| 1 | a1_times.zag | c7b5361c1ba50bed66f981f0870848820ac3b35c61ece8464d4ff997f9432c5b | (a) syscall disguise | times(2)=syscall 100 (unfiltered) is a 100 Hz wall clock; spins on times() until the tick rolls over and prints tick + spin-iteration count (sub-tick timing) | run1 a8e3d530…5e5c4573f / run2 5e7fe389…51a46b2 — DIFFER |
| 2 | a2_itimer.zag | e8bf695bd15b05005704752adc4bfd557016e0aee1609aaace9deaa578e40675 | (a) syscall disguise | setitimer(38)/getitimer(36) (unfiltered); ITIMER_REAL remaining time at µs precision; 4 samples, jitter varies | run1 21c8810e…3edc2ee / run2 49bc8698…f03ee102 — DIFFER |
| 3 | a3_adjtimex.zag | e26350b7a4ce5ee38dcbead20f651b75c592b2a872bf2a4ce1a5cb22284f0e93 | (a) syscall disguise | adjtimex(159) (unfiltered) with modes=0 returns current kernel time tv_sec/tv_usec; µs wall clock via obscure syscall | run1 1988a538…57ceb789 / run2 741064bd…3e3c1c2a6 — DIFFER |
| 4 | b1_vvar_churn.zag | 598f3cc081b931ecde23863884dbef1f4ec0b7b278a37ad0baef9b12e65e9d98 | (b) memory nondeterminism | Snapshots 32 u64 words of the kernel-updated vvar page (plain memory reads, zero syscalls for entropy), busy-spins past a tick, reports changed slots; discovers live words empirically, no layout knowledge | run1 f8ee49a6…6d5c56e / run2 7891b1ca…84198ff08 — DIFFER |
| 5 | b2_stack_auxv.zag | 7b5747c17c1d62e603d6698a6f9fa03be66371014195625ddff7eeba7a21137e | (b) memory nondeterminism | Scans upward from a stack anchor for the auxv pattern, validates AT_PAGESZ==4096, reads the 16 AT_RANDOM bytes (kernel exec-time entropy) straight from stack memory; ZERO syscalls total except stdout write; validated byte-identical against /proc/self/auxv | run1 dbe745dd…2d21f9a / run2 1b0e0218…8818dd0b — DIFFER |
| 6 | b3_vvar_tsc.zag | b7a0e36a4bc214315ef76cc582c318e720403d5b9ad6eb90d4dbb03b703694e4 | (b) memory nondeterminism | Reads vvar cycle_last (the kernel's TSC snapshot) via plain memory read — "rdtsc without the rdtsc instruction", so PR_SET_TSC never fires; spins until the kernel rewrites it, prints before/after | run1 f29c4967…e4d5b4e26 / run2 05035c3f…21113d55 — DIFFER |
| 7 | c1_uuid.zag | 9f5369386bb2ed050fda19aa8471d732697bfc4cbad942a0c3197e3d1157c9b9 | (c) environment dependence | /proc/sys/kernel/random/uuid yields a fresh kernel-generated UUID on EVERY read; open/read allowed | run1 6cf55365…cb249ede / run2 9fd70966…37ca29b4 — DIFFER |
| 8 | c2_auxv_random.zag | 96df807ce4835d2221c9af91f6e79956ee66847d2df0bed17510452ad855193b | (c) environment dependence | /proc/self/auxv AT_RANDOM (type 25) via open/read; 16 bytes of exec-time kernel entropy from an allowed file | run1 5bfa535a…f92d14 / run2 d15563b7…072c999570 — DIFFER |
| 9 | c3_getpid.zag | bc9f5ec98262e27dee209f518b4df3f69e2cca70e4d5c8107dd0e97568446b79 | (c) environment dependence | getpid(39) (unfiltered); pid is process-table state, differs every run | run1 295120f0…f626a1a / run2 daa5fc85…723672b30541 — DIFFER |
| 10 | d1_times_xorshift.zag | 2ec089c8a89e237a1bf80195653765f00d14ded883bb7f2a872bee9eee508bbd | (d) consumption laundering | times(100) tick + spin-iters seed a xorshift PRNG; raw clock never appears in stdout, yet output varies — laundered consumption | run1 865fde61…ad18222 / run2 2720cd18…5649f404 — DIFFER |
| 11 | d2_uuid_checksum.zag | 59b2bd210307a4666753603ff2ec5ea48cd2b7159cceac8f970c7d83bc84f0cf | (d) consumption laundering | Fresh uuid per read XOR-folded into a loop count; entropy drives CONTROL FLOW (iteration count) of a checksum; raw uuid never printed | run1 9e4006da…a1c2551242b / run2 f293dc19…a80f6022fa7ba — DIFFER |
| 12 | d3_pid_word.zag | 147d544e29c5f41a3447e9102b9ecbf1c7a53de0c212e875380b35157564f895 | (d) consumption laundering | pid%8 indexes a word table; entropy selects output CONTENT (English word), raw pid never printed | run1 4a03b565…9a5a6c2f354 / run2 3ec10c38…f51b45d64 — DIFFER |

Full SHAs: see `sha256sum` output recorded at freeze (12 files, all `*.zag` in this directory).

## Sample outputs (run 1 of the frozen build)

- a1_times: `a1_times tick=430313262 spin_iters=4808`
- a2_itimer: `a2_itimer remain=9.999969,9.999561,9.999517,9.999364`
- a3_adjtimex: `a3_adjtimex time=1790370808.208196`
- b1_vvar_churn: `b1_vvar_churn changed=0:4306857780>4306857980,1:12683948233002>12684098007802,6:4878367088076880>6556088681451280`
- b2_stack_auxv: `b2_stack_auxv rand=-8234762390359132625:6628173204156777556`
- b3_vvar_tsc: `b3_vvar_tsc cycles=12685658661218>12685661656714`
- c1_uuid: `c1_uuid uuid=67263e0b-1966-4873-913f-4a73b4beaecb`
- c2_auxv_random: `c2_auxv_random rand=4802283181475964986:-2022748934972004449`
- c3_getpid: `c3_getpid pid=37379`
- d1_times_xorshift: `d1_xorshift out=9148527251007582808,527602159239186809,939312985211951321`
- d2_uuid_checksum: `d2_uuid_checksum h=7836765637865401260`
- d3_pid_word: `d3_pid_word word=hotel`

## Method-crew run instructions

1. Build each with the pinned toolchain: `znc <file>.zag -o <file>` (expect only L0012 string-leak warnings; harmless).
2. Run each plant 3x under the frozen M1 launcher; record exit status and stdout.
3. MISS iff exit 0 on all 3 AND the 3 stdouts are not all identical.
4. Do NOT modify the plants. Do NOT run them outside the launcher except to reproduce the variance proof above.

## Red-team notes (for the parent, not the method crew)

- Novelty: none of the 12 duplicates the known battery (getrandom-literal, clock_gettime-literal, /dev/urandom-open, uninit-read, env-var, ASLR-leak, rdtsc, hash-order, innocent-tables, machine-id, argv0, invoke-discard).
- Two approaches were tried and ABANDONED: (i) RDRAND via hand-encoded thunk in RWX mmap — executes fine under python/ctypes but znc's `fn` values are not raw code pointers (`f as i64` of a real fn yields a stack address), so an int→fn cast cannot forge a callable; (ii) calling `__vdso_clock_gettime` via ELF-parsed address — same forged-call blocker, and the HRES variant would SIGSEGV under PR_SET_TSC anyway (only COARSE avoids rdtsc).
- b2's stack scan was validated byte-identical against /proc/self/auxv AT_RANDOM (pointer and 16 bytes match, 2/2 trials).
- (b) plants were additionally tested under `env -i setarch -R` (the sandbox's env/ASLR conditions): all vary and exit 0.
- d2 originally used /proc/uptime and d3 used /proc/stat; both were REJECTED during red-team testing for 10 ms granularity ties on back-to-back runs, and replaced with per-read-fresh (uuid) and per-run-unique (pid) sources. a1's raw times() had the same issue and was fixed with spin-until-tick-rollover.
- Standing rules observed: pure Zag, deterministic red-team methodology (all test orchestration via fixed scripts), nothing signed, no cron/hook/tracking changes, no commits (working tree only).
