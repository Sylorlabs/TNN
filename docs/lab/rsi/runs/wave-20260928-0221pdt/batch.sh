#!/bin/sh
# batch.sh -- wave-20260928-0221pdt fork battery over all 56 named entries.
# Live entries first (newly enumerated 2321pdt archive, task-pinned local tip),
# then the fixture set. Faithful frozen driver; pure shell only.
# Pinned-commit discipline: every extraction is by run-start-pinned SHA
# (never by live ref), so mid-battery lane commits are inert.
set -u
export R="$HOME/workspace/tnn-rsi" SCR="$HOME/workspace/fb0221" HARNESS="$HOME/workspace/fb0221/fork_battery"
export ZNC_PIN=498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
export PROBE_PIN=3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919
export B1_RUN_PIN=5dfe3c161096819c8c0dd6057c4df9944ddd884f57b9a513b47e7655d53c6066
export B2_BIN_PIN=75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2
run() { "$SCR/run_one.sh" "$1" "$2"; }

# --- live first: newly enumerated archive (task run-start pin 43f339e60),
#     and local-tnn-native-lab tested at the task-pinned commit ---
run arch-wave-20260927-2321pdt 43f339e60dad44bf5ceccef83962248b7a434256
run local-tnn-native-lab 43f339e60dad44bf5ceccef83962248b7a434256

# --- local archive branches, plain names (fixture, unchanged SHAs) ---
run arch-20260923-2321pdt 3aa59360d3f4849358817fae945aab942882ab92
run arch-20260924-0221pdt aab82c574098e8f85d909bfddeac368588f76f72
run arch-20260924-0521pdt 9f681e2719ea45916da19cad15965717bffa82af
run arch-20260924-1121pdt b66c6aeabfff03ceca9194386d98b61574ff4601
run arch-20260924-1421pdt c5f0383e2713aa91166b01a1a15229937cea4b3f
run arch-20260924-1721pdt 088a1914efb308f8a5d8f168f1f9878cf7a4fca8
run arch-20260926-2021pdt 5ba241235482610f1c8f538d97ca0462164b4014
run arch-20260927-0221pdt 463b115b69e280da0d7f6da15c6ded2f3f610809
run arch-20260927-0521pdt 80c40a7afc0231493e0f1f46540a6dbe60c60c3f
run arch-20260927-1421pdt 8929cdd93df7efeb8b67320d5a7d67e2d6bed467

# --- local archive branches, wave-prefixed (fixture, unchanged SHAs) ---
run arch-wave-20260924-1721pdt d24bb4b502022efc675dda80e0e97436acc09278
run arch-wave-20260924-2321pdt e33b5ddbdcb6cf5290c2fb3272d1dd8fb6c86155
run arch-wave-20260925-0221pdt 058ee02a8a31efc66fb8e92293d399752ce33a6f
run arch-wave-20260925-0521pdt 0ee06268e9118d1812f7a1e1b85ad384f79a583a
run arch-wave-20260925-0821pdt 393007563d27b931c8af59ad9d9fedc336fbed1d
run arch-wave-20260925-1121pdt 60a0579973fa64c80ec2501afc1f5d3080b9b8ba
run arch-wave-20260925-1421pdt 2e2c65fb294e85348d4329ca1e55caf8f6c258a9
run arch-wave-20260926-0521pdt 4328a8350d987a65c4e86e4973dbe45c9d5f6cd5
run arch-wave-20260926-0821pdt 4bbbca69cecd9c47602e125545b137380e8bab1a
run arch-wave-20260926-1121pdt 746ff60ba16d18c36db2ccd4394cbb9db9d6266d
run arch-wave-20260926-1421pdt a222f8f178049b9aeee3b053328c59e9b6fd813d
run arch-wave-20260926-1721pdt a4d4ff7cd4eb3ad7fbed08da7e0fb8282f32844a
run arch-wave-20260926-2321pdt 004616f657165191c0d0e89d91fc10a99edd2d6e
run arch-wave-20260927-0821pdt e9373dad1aca4a694cf39d023e7756312e125ba7
run arch-wave-20260927-1121pdt 4805f5363a0dba762abf2d35e8ab8284abce6731
run arch-wave-20260927-1721pdt 4042f15bf40b1c73a516ba5eda2a412033db9f6d
run arch-wave-20260927-2021pdt baf48e4744c3c075e3fc70a383f0a77efec83ad7

# --- experimental branches, pinned commits (fixture; tested read-only) ---
run exp1 1010a63c3c1cc3f3724f6cf0ca55decc08207a2d
run exp2 a2a36e6571b2cf716df151c6ad8b8ffa07c6d3e4
run exp-sensory c368b8e1ffecec2f9061011f5d7c0e3e68675e0a

# --- debate backup (fixture) ---
run wave-debate-session-1-backup 3947dca1a77c00818575dbc7476556c8278b8b7b

# --- remote heads (fixture; pins captured at run start, read-only ls-remote) ---
run origin-tnn-native-lab-rt bedf8b4aab0110e3c115fb1bca3903551a32577e
run origin-tnn-native-lab-live bedf8b4aab0110e3c115fb1bca3903551a32577e
run rh-tnn-native-lab-live-tip b257c02cc68b7a1f079dee28611cccd93b6efc9d
run rh-main 27a4271f208247a1e9c24cca35468c298b6cd29d
run rh-fs-gr1 23f6c0f9012887448a83edbe9060b73e13d5a7a5
run rh-r2-7 2d99d183f693145c53213639990a3474ff786b69
run rh-reorg-phase-0-1 9914322267e1358e5542a23c72ec51d1a9ae43df
run rh-wg-freeze f875b34179f570ba1ad555262cd401ddc4a52848
run rh-pull-1-head 5802fec8401f28b4036b0dd5ebb23905610cab57
run rh-pull-2-head 4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba
run rh-pull-3-head 9914322267e1358e5542a23c72ec51d1a9ae43df

# --- worktrees (fixture, pinned commits, read-only) ---
run wt-forktest-main 293602fb1d4a2fd5d680a3376463d61b0572006b
run wt-forktest-r2-7 a0e7f8ba2bf0e32ec5b989cae0838fdcd14d33a5
run wt-forktest-reorg 9914322267e1358e5542a23c72ec51d1a9ae43df
run wt-forktest-tnn-native-lab bd30978748fa83bbea6e423a7074cf32b7304291
run wt-forktest-tnn-native-lab-remote cea8db22f53ed1294aff5324aa143bd6d1df845e
run wt-forktest-debate-backup 3947dca1a77c00818575dbc7476556c8278b8b7b
run wt-forktest-wg-freeze f875b34179f570ba1ad555262cd401ddc4a52848
run wt-wave3-probe bd30978748fa83bbea6e423a7074cf32b7304291
run wt-wave3-senses bd30978748fa83bbea6e423a7074cf32b7304291
run wt-wave3-trades bd30978748fa83bbea6e423a7074cf32b7304291
run wt-exp1 1010a63c3c1cc3f3724f6cf0ca55decc08207a2d
run wt-exp2 a2a36e6571b2cf716df151c6ad8b8ffa07c6d3e4
run wt-exp-sensory c368b8e1ffecec2f9061011f5d7c0e3e68675e0a
