#!/bin/sh
# Battery part 2: remaining configs with the rebuilt E-DE2 binary.
# fd_p1/fd_p2 already done (unaffected binary). e2a_p1 is redone with the
# rebuilt binary (SHA must match the old binary's fb211967...).
set -u
W=~/workspace/htd-1/builds/comp
RUNS=$W/runs
SNAP_PRISTINE=~/workspace/htd-1/builds/ref-baselines/runs/snapshot.bin
DUP1=~/workspace/htd-1/builds/ede4/dup_p1.txt
DUP2=~/workspace/htd-1/builds/ede4/dup_p2.txt
LOG=$RUNS/battery.log
echo "battery part2 start $(date -u +%FT%TZ) e2a_binary=ede2_bin_rebuild" >> "$LOG"

run_one() {
    tag=$1; shift
    r=$1; shift
    out=$RUNS/${tag}_r${r}.bin
    start=$(date +%s%N)
    "$@" > "$out.stdout" 2>&1
    rc=$?
    end=$(date +%s%N)
    ms=$(( (end - start) / 1000000 ))
    if [ $rc -ne 0 ]; then
        echo "FAIL rc=$rc tag=$tag r=$r" >> "$LOG"
        cat "$out.stdout" >> "$LOG"
        return 1
    fi
    sha=$(sha256sum "$out" | cut -d' ' -f1)
    echo "OK tag=$tag r=$r ms=$ms sha=$sha $(cat $out.stdout | tr '\n' '|')" >> "$LOG"
    rm -f "$out.stdout"
    echo "$sha  $tag r$r"
}

snap_run() {
    tag=$1; bin=$2; man=$3
    r=1
    while [ $r -le 5 ]; do
        wsnap=$RUNS/snap_work_${tag}_r${r}.bin
        cp "$SNAP_PRISTINE" "$wsnap"
        run_one "$tag" "$r" $bin "$wsnap" "$man" "$RUNS/${tag}_r${r}.bin" || return 1
        rm -f "$wsnap"
        r=$((r+1))
    done
}

E2R=~/workspace/htd-1/builds/ede2/ede2_bin_rebuild
E4=~/workspace/htd-1/builds/ede4/ede4_bin
CB=$W/comp_bin

snap_run e2a_p1 "$E2R a" "$DUP1" || exit 1
snap_run e2a_p2 "$E2R a" "$DUP2" || exit 1
snap_run e4n_p1 "$E4 narrow" "$DUP1" || exit 1
snap_run e4n_p2 "$E4 narrow" "$DUP2" || exit 1
snap_run comp_p1 "$CB" "$DUP1" || exit 1
snap_run comp_p2 "$CB" "$DUP2" || exit 1
echo "battery done $(date -u +%FT%TZ)" >> "$LOG"
