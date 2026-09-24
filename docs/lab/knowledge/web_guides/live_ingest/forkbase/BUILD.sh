#!/usr/bin/env bash
# LI fork-base build + fidelity proof.
# Compiles frozen webg.zag with the PINNED toolchain, asserts the binary is
# byte-identical to the frozen instrument binary, then runs the minimal
# driver twice over the novel-facts fixture corpus and asserts both passes
# are byte-identical to the frozen measurement artifacts (expected/).
set -euo pipefail
cd "$(dirname "$0")"

ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
FROZEN_BIN="$HOME/workspace/tnn-lab/knowledge/web_guides/webg"

echo "== 1. compile webg.zag with pinned toolchain =="
"$ZNC" webg.zag -o webg

echo "== 2. assert binary byte-identical to frozen instrument binary =="
cmp webg "$FROZEN_BIN"
echo "OK: compiled webg == frozen webg (byte-identical)"

echo "== 3. run minimal driver twice over fixture corpus =="
python3 run_forkbase.py fixtures_novel/manifest_fixtures.txt fixtures_novel/snap fb_pass1
python3 run_forkbase.py fixtures_novel/manifest_fixtures.txt fixtures_novel/snap fb_pass2

echo "== 4. assert pass1 == frozen measurement artifacts (expected/) =="
for f in knowledge_ledger.txt refusal_ledger.txt run_li.log; do
  cmp "fb_pass1/$f" "expected/$f"
  echo "OK: fb_pass1/$f == expected/$f"
done

echo "== 5. assert determinism: pass1 == pass2 =="
for f in knowledge_ledger.txt refusal_ledger.txt run_li.log; do
  cmp "fb_pass1/$f" "fb_pass2/$f"
  echo "OK: fb_pass1/$f == fb_pass2/$f"
done

echo
echo "FORK-BASE BUILD PASSED: binary faithful, driver reproduces the frozen"
echo "measurement byte-identically and is deterministic across two runs."
