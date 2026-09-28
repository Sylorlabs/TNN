#!/usr/bin/env bash
# Convert v3c 6-col outputs to analyzer legs + run frozen bars_full.py.
set -e
export TMPDIR=~/workspace/tmp_commit
J=~/workspace/nec_v3b/job3
A=$J/analysis
W=$J/work
cd $W
for spec in "26 s1 s10 s100" "27 s1 s10 s100" "28 s1"; do
  set -- $spec; v=$1; shift
  for s in "$@"; do
    tag=v${v}_${s}
    legs=legs_${tag}
    python3 $A/to_analyzer.py ${tag}_A.tsv $legs v$v
  done
done
infile() { # scale -> 6/7-col input path
  case $1 in
    s1)   echo "$W/necc_input.tsv" ;;
    s10)  echo ~/workspace/nec_v2d/work/necc_input_s10.tsv ;;
    s100) echo ~/workspace/nec_v2d/work/necc_input_s100.tsv ;;
  esac
}
for spec in "26 s1 s10 s100" "27 s1 s10 s100" "28 s1"; do
  set -- $spec; v=$1; shift
  for s in "$@"; do
    tag=v${v}_${s}
    echo "########## v$v $s ##########"
    python3 $A/bars_full.py legs_${tag} v$v ${tag}_A.tsv "$(infile $s)"
  done
done
echo "done"
