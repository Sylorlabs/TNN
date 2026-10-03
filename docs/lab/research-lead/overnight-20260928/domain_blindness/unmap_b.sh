#!/bin/sh
# unmap_b.sh -- frozen inverse output mapping, Variant B (PREREG 5).
# Variant A inverse, then kind-mask polarity swap-back via placeholders.
# stdin -> stdout.
export PATH="$HOME/safebin"
./unmap_a.sh | sed -e 's/inmask=2/inmask=T/; s/inmask=1/inmask=2/; s/inmask=T/inmask=1/' \
                   -e 's/outmask=2/outmask=T/; s/outmask=1/outmask=2/; s/outmask=T/outmask=1/'
