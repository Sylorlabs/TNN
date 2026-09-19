#!/bin/sh
set -u
E=/tmp/r33_finish_recovery_20260915_b/compiler_probe
S=/Users/Shared/micah/Documents/TNN/TNN/Research/R33_CONTINUING_LIFE_V1
C=/Users/Shared/micah/Documents/zag/znc
for pair in v68:outer_learner_packet_bridge_v68_tests v73:zag_checkpoint_sliceparam_repro_v73 v71:zag_checkpoint_module_repro_v71; do
 n=${pair%%:*}; f=${pair#*:}
 rm -f "$E/$n.projected.zag" "$E/$n.provenance.tsv"
 "$C" "$S/$f.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/$n.direct" > "$E/$n.direct.build.stdout" 2> "$E/$n.direct.build.stderr"
 echo $? > "$E/$n.direct.build.exit"
 "$E/$n.direct" > "$E/$n.direct.stdout" 2> "$E/$n.direct.stderr"
 echo $? > "$E/$n.direct.exit"
 "$E/project" "$S/$f.zag" "$E/$n.projected.zag" "$E/$n.provenance.tsv" > "$E/$n.projection.stdout" 2> "$E/$n.projection.stderr"
 echo $? > "$E/$n.projection.exit"
 "$C" "$E/$n.projected.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/$n.projected" > "$E/$n.projected.build.stdout" 2> "$E/$n.projected.build.stderr"
 echo $? > "$E/$n.projected.build.exit"
 "$E/$n.projected" > "$E/$n.projected.stdout" 2> "$E/$n.projected.stderr"
 echo $? > "$E/$n.projected.exit"
done
