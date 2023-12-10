#!/bin/bash

# Get directory name of this script
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Execute path.sh and cmd.sh to set Kaldi path configurations
. path.sh || exit 1
. cmd.sh || exit 1

# Enable openfst
export PATH=$KALDI_ROOT/tools/openfst/bin:$PATH

draw-tree $SCRIPT_DIR/data/lang/phones.txt exp/mono/tree | dot -Gsize=48,50.5 -Tps | ps2pdf - $SCRIPT_DIR/doc/att/mono-tree.pdf

draw-tree $SCRIPT_DIR/data/lang/phones.txt exp/tri1/tree | dot -Gsize=720,722.5 -Tps | ps2pdf - $SCRIPT_DIR/doc/att/tri1-tree.pdf