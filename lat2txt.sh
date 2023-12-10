#!/bin/bash

# Get directory name of this script
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Execute path.sh and cmd.sh to set Kaldi path configurations
. path.sh || exit 1
. cmd.sh || exit 1

# Example of generating visualization of decoding lattice graph
lattice-copy "ark:gunzip -c $SCRIPT_DIR/exp/mono/decode/lat.1.gz|" ark,t:- > $SCRIPT_DIR/doc/att/mono-decode-lat.1.gz-int.txt
lattice-copy "ark:gunzip -c $SCRIPT_DIR/exp/mono/decode/lat.1.gz|" ark,t:- | utils/int2sym.pl -f 3 data/lang/words.txt > $SCRIPT_DIR/doc/att/mono-decode-lat.1.gz-sym.txt
sed -n 387,393p $SCRIPT_DIR/doc/att/mono-decode-lat.1.gz-int.txt | lattice-to-fst --rm-eps=true --acoustic-scale=1.0 --lm-scale=1.0 ark,t:- ark,t:- | tail -n+2 | fstcompile | fstdraw --portrait=true --osymbols=data/lang/words.txt | dot -Tpdf > $SCRIPT_DIR/doc/att/mono-decode-lat.1.gz-sym1.pdf