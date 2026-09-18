#!/bin/sh
cd /Users/Shared/micah/Documents/TNN/TNN || exit 99
E=Research/R33_NATIVE_N19_RUNTIME_BOUNDARY/INDEPENDENT_V3_FRESH
ln -s final/ops "$E/root_symlink"
printf 'COMMAND %s/n19 case-host-abi %s/root_symlink\n' "$E" "$E"
"$E/n19" case-host-abi "$E/root_symlink"
printf 'EXIT %s\n' "$?"
printf 'COMMAND %s/n19 case-probe-existing %s/root_symlink append.bin\n' "$E" "$E"
"$E/n19" case-probe-existing "$E/root_symlink" append.bin
printf 'EXIT %s\n' "$?"
printf 'COMMAND shasum -a 256 -c canonical_raw.sha256\n'
shasum -a 256 -c "$E/canonical_raw.sha256"
printf 'EXIT %s\n' "$?"
