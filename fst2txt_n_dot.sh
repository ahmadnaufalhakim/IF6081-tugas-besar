#!/bin/bash

# Get directory name of this script
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Execute path.sh and cmd.sh to set Kaldi path configurations
. path.sh || exit 1
. cmd.sh || exit 1

# Enable openfst
export PATH=$KALDI_ROOT/tools/openfst/bin:$PATH

# Generate readable representation for G.fst
fstprint --isymbols=data/lang/words.txt --osymbols=data/lang/words.txt $SCRIPT_DIR/data/lang/G.fst > $SCRIPT_DIR/doc/att/G.txt
fstdraw --portrait=true --isymbols=data/lang/words.txt --osymbols=data/lang/words.txt $SCRIPT_DIR/data/lang/G.fst > $SCRIPT_DIR/doc/att/G.dot
# Generate readable representation for L.fst
fstprint --isymbols=data/lang/words.txt --osymbols=data/lang/words.txt $SCRIPT_DIR/data/lang/L.fst > $SCRIPT_DIR/doc/att/L.txt
fstdraw --portrait=true --isymbols=data/lang/words.txt --osymbols=data/lang/words.txt $SCRIPT_DIR/data/lang/L.fst > $SCRIPT_DIR/doc/att/L.dot
# Generate readable representation for HCLG.fst
fstprint --isymbols=data/lang/words.txt --osymbols=data/lang/words.txt $SCRIPT_DIR/exp/mono/graph/HCLG.fst > $SCRIPT_DIR/doc/att/mono-graph-HCLG.txt
fstdraw --portrait=true --isymbols=data/lang/words.txt --osymbols=data/lang/words.txt $SCRIPT_DIR/exp/mono/graph/HCLG.fst > $SCRIPT_DIR/doc/att/mono-graph-HCLG.dot

# # Would take so much memory to draw, hence strongly suggest to not execute following commands!
# dot -Tpdf $SCRIPT_DIR/doc/att/G.dot > $SCRIPT_DIR/doc/att/G.pdf
# dot -Tpdf $SCRIPT_DIR/doc/att/L.dot > $SCRIPT_DIR/doc/att/L.pdf