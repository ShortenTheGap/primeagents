#!/usr/bin/env bash
# Worked example: a PER-ITERATION verifier — checks that the one item this
# iteration just handled reached its final, correct state.
#
# The loop passes the current item's identity in as arguments (here: the path to
# the artifact the iteration was supposed to produce, and an optional marker file
# + token that should now be present). The verifier is deterministic — it reads
# files and compares, it never asks a model whether the work "looks done".
#
# This is distinct from the GOAL predicate (see verify_example.sh, "0 items
# left"): a per-iteration verifier gates ONE attempt; the goal predicate decides
# whether the whole loop may stop.
#
# Usage: verify_item_example.sh <artifact_path> [<marker_file> <marker_token>]
# Exit:  0 = this item passed · 1 = it did not (iterate / retry) · 2 = misuse
set -euo pipefail

if [ "$#" -ne 1 ] && [ "$#" -ne 3 ]; then
  echo "usage: $0 <artifact_path> [<marker_file> <marker_token>]" >&2
  exit 2
fi

artifact="$1"

# 1. the artifact this iteration produced must exist and be non-empty
if [ ! -s "$artifact" ]; then
  echo "FAIL: artifact missing or empty: $artifact" >&2
  exit 1
fi

# 2. optional: a marker (e.g. the source line flipped to done) must now be present
if [ "$#" -eq 3 ]; then
  marker_file="$2"; marker_token="$3"
  if [ ! -f "$marker_file" ]; then
    echo "FAIL: marker file missing: $marker_file" >&2
    exit 1
  fi
  if ! grep -qF -- "$marker_token" "$marker_file"; then
    echo "FAIL: marker token not found in $marker_file: $marker_token" >&2
    exit 1
  fi
fi

echo "PASS: item verified ($artifact)"
exit 0
