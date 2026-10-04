#!/bin/bash
# TNN LANE ISOLATION HELPER
#
# WHY THIS EXISTS
#   Wave 1 dispatched ~6 workers that all ran `git checkout -b` inside the SAME
#   working directory. They thrashed each other's branches: preregs landed on
#   other lanes' branches, branches were moved under active work, and two
#   workers had to rebuild their history. Charter section 9 requires isolated
#   worktrees with no shared-index races. This script makes that automatic.
#
# USAGE
#   lane.sh new  <lane-name>   -> creates branch lane/<lane-name> + worktree
#                                  prints the worktree path; cd there
#   lane.sh list               -> lists active lanes
#   lane.sh rm   <lane-name>   -> remove worktree (branch is kept)
#
# Each lane gets its own worktree, its own index, and its own working tree.
# Concurrency-safe as long as each worker only ever runs git INSIDE its own
# worktree path.

set -eu
REPO=/Users/Shared/micah/Documents/TNN/TNN
WTROOT=/Users/Shared/micah/Documents/TNN/.worktrees
BASE=${TNN_BASE_REF:-504641745}

mkdir -p "$WTROOT"

cmd=${1:-}
name=${2:-}

case "$cmd" in
  new)
    [ -n "$name" ] || { echo "usage: lane.sh new <name>" >&2; exit 2; }
    br="lane/$name"
    wt="$WTROOT/$name"
    if [ -e "$wt" ]; then
      echo "lane.sh: worktree already exists: $wt"
      echo "$wt"
      exit 0
    fi
    git -C "$REPO" worktree add -q -b "$br" "$wt" "$BASE" 2>/dev/null \
      || git -C "$REPO" worktree add -q "$wt" "$br"
    echo "lane.sh: created $br at $wt (base $BASE)"
    echo "$wt"
    ;;
  list)
    git -C "$REPO" worktree list
    ;;
  rm)
    [ -n "$name" ] || { echo "usage: lane.sh rm <name>" >&2; exit 2; }
    git -C "$REPO" worktree remove --force "$WTROOT/$name" 2>/dev/null || true
    echo "lane.sh: removed worktree for $name (branch lane/$name kept)"
    ;;
  *)
    echo "usage: lane.sh {new|list|rm} [name]" >&2
    exit 2
    ;;
esac
