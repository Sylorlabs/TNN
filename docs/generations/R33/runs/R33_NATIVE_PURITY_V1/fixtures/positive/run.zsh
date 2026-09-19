#!/bin/zsh
set -eu
COMP=/Users/Shared/micah/Documents/Zag/znc
"$COMP" source.zag --target macos-arm64 -o native-bin
./native-bin

