#!/bin/sh
# setup_safebin.sh
#
# Builds $HOME/safebin: a restricted PATH directory containing only the
# allowed toolchain (git, the pinned znc compiler, coreutils). python3 and
# python are deliberately absent, so any accidental invocation fails loudly
# with "command not found" instead of silently contaminating a wave.
#
# Idempotent: safe to re-run. Shell only. Invokes no Python.
#
# Usage:
#   sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
#   export PATH="$HOME/safebin"
#
# After exporting PATH, verify with:
#   command -v python3 python   # must print nothing

set -u

SAFEBIN="$HOME/safebin"
ZNC_PINNED="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"

# Allowed tools, resolved from the system. znc is handled separately (pinned binary).
TOOLS="awk basename cat chmod cmp cp cut date diff dirname echo find git grep head ls mkdir mv od printf rm sed sha256sum sleep sort stat tail tee timeout touch tr uname uniq wc xargs"

mkdir -p "$SAFEBIN"

linked=0
missing=""

for t in $TOOLS; do
    src=""
    for d in /usr/bin /bin; do
        if [ -x "$d/$t" ]; then
            src="$d/$t"
            break
        fi
    done
    if [ -n "$src" ]; then
        ln -sf "$src" "$SAFEBIN/$t"
        linked=$((linked + 1))
    else
        missing="$missing $t"
    fi
done

# Pinned znc compiler (absolute repo path, never a PATH-resolved copy).
if [ -x "$ZNC_PINNED" ]; then
    ln -sf "$ZNC_PINNED" "$SAFEBIN/znc"
    linked=$((linked + 1))
    znc_status="OK ($ZNC_PINNED)"
else
    znc_status="MISSING ($ZNC_PINNED not executable)"
fi

echo "safebin: $SAFEBIN"
echo "linked: $linked tools"
echo "znc: $znc_status"
if [ -n "$missing" ]; then
    echo "missing from system (skipped):$missing"
fi

# Verification: python3 and python must NOT resolve under the safebin PATH.
# Use the shell builtin `command -v` so the check itself needs no external tool.
OLD_PATH="$PATH"
PATH="$SAFEBIN"
py3="$(command -v python3 2>/dev/null || true)"
py="$(command -v python 2>/dev/null || true)"
PATH="$OLD_PATH"

fail=0
if [ -n "$py3" ]; then
    echo "FAIL: python3 resolves to $py3 under safebin PATH"
    fail=1
else
    echo "verify: python3 absent from safebin PATH (OK)"
fi
if [ -n "$py" ]; then
    echo "FAIL: python resolves to $py under safebin PATH"
    fail=1
else
    echo "verify: python absent from safebin PATH (OK)"
fi

# Sanity: the tools a builder needs most must resolve.
for need in git znc sh; do
    :
done
if [ ! -x "$SAFEBIN/git" ]; then
    echo "FAIL: git missing from safebin"
    fail=1
fi
if [ ! -x "$SAFEBIN/znc" ]; then
    echo "FAIL: znc missing from safebin"
    fail=1
fi

if [ "$fail" -eq 0 ]; then
    echo "SAFEBIN-READY: $SAFEBIN ($linked tools, no python)"
    exit 0
else
    echo "SAFEBIN-BROKEN: see failures above"
    exit 1
fi
