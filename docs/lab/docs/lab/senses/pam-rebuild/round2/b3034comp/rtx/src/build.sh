#!/bin/bash
# RT-X build script. Materializes build dirs from byte-verified committed
# sources + derived files, then compiles with the pinned toolchain.
# Imports resolve relative to CWD (znc rule), so each binary builds in its
# own directory. Binaries are NOT committed.
set -e
ZNC=/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
RT=/home/hatch/workspace/rtx
FRZ=/home/hatch/workspace/b3034comp/extract/frozen
SRC=/home/hatch/workspace/b3034comp/src

sha() { sha256sum "$1" | cut -d' ' -f1; }

# pinned SHAs (prereg section 9)
[ "$(sha $FRZ/drive3034_ad0e1ddd.zag)" = "1b1eb68ab4d0b704546b75ee0a6a7207cb7dcd59b6b6c53b5850d4b991e410b4" ] || { echo "driver SHA FAIL"; exit 1; }
[ "$(sha $FRZ/b303134_common_6e74ce54.zag)" = "79257900bc1ccb1518ff0d286615a4f8ce90bb02c9dfcb724b50ca26af286218" ] || { echo "common SHA FAIL"; exit 1; }
[ "$(sha $SRC/R33_NATIVE_IO_V1.zag)" = "e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8" ] || { echo "io SHA FAIL"; exit 1; }
echo "pristine SHAs OK"

# 1. pristine (unmodified) driver
mkdir -p $RT/b_pristine
cp $FRZ/drive3034_ad0e1ddd.zag $RT/b_pristine/
cp $FRZ/b303134_common_6e74ce54.zag $RT/b_pristine/b303134_common.zag
cp $SRC/R33_NATIVE_IO_V1.zag $RT/b_pristine/
cd $RT/b_pristine && $ZNC drive3034_ad0e1ddd.zag -o $RT/bin/drive3034_pristine

# 2. rtx_x (X-classes + OLD replay) against the main-rename lib
mkdir -p $RT/b_x
cp $SRC/R33_NATIVE_IO_V1.zag $RT/b_x/
cp $FRZ/b303134_common_6e74ce54.zag $RT/b_x/b303134_common.zag
cp $RT/derived/drive3034_lib.zag $RT/b_x/
cp $RT/rtx_x.zag $RT/b_x/
cd $RT/b_x && $ZNC rtx_x.zag -o $RT/bin/rtx_x

# 3. ablate pass 1
mkdir -p $RT/b_a1
cp $SRC/R33_NATIVE_IO_V1.zag $RT/b_a1/
cp $FRZ/b303134_common_6e74ce54.zag $RT/b_a1/b303134_common.zag
cp $RT/derived/drive3034_ablate_p1.zag $RT/b_a1/
cp $RT/rtx_ablate_p1.zag $RT/b_a1/
cd $RT/b_a1 && $ZNC rtx_ablate_p1.zag -o $RT/bin/rtx_ablate_p1

# 4. ablate pass 2 (bind_ok nopped)
mkdir -p $RT/b_a2
cp $SRC/R33_NATIVE_IO_V1.zag $RT/b_a2/
cp $RT/derived/b303134_common_ablate_p2.zag $RT/b_a2/
cp $RT/derived/drive3034_ablate_p2.zag $RT/b_a2/
cp $RT/rtx_ablate_p2.zag $RT/b_a2/
cd $RT/b_a2 && $ZNC rtx_ablate_p2.zag -o $RT/bin/rtx_ablate_p2

echo "BUILD OK"
ls -la $RT/bin/
