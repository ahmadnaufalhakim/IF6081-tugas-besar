#!/bin/bash

# Aliasing python to python3
alias python="python3"

# Execute path.sh and cmd.sh to set Kaldi path configurations
. ./path.sh || exit 1
. ./cmd.sh || exit 1

# Number of parallel jobs - 1 is perfect for a small dataset
nj=1
# Language model order (n-gram quantity)
lm_order=2

# Safety mechanism (possible running thiis script with modified arguments)
. utils/parse_options.sh || exit 1
[[ $# -ge 1 ]] && { echo "Wrong arguments!"; exit 1; }

# Removing all previously automatically created data (by Kaldi)
rm -rf exp mfcc
rm -rf data/train/spk2utt data/train/cmvn.scp data/train/feats.scp data/train/split1
rm -rf data/test/spk2utt data/test/cmvn.scp data/test/feats.scp data/test/split1
rm -rf data/local/lang data/lang data/local/tmp data/local/dict/lexiconp.txt
# Removing all previously automatically created data (by self-made python scripts)
rm -rf data/local/train data/local/test
rm -rf data/local/dict data/local/corpus

# Recreate Kaldi required data
echo
echo "##########################################"
echo "#     RECREATING KALDI REQUIRED DATA     #"
echo "##########################################"
echo
## Recreate all data/train and data/test files for acoustic training data
echo "Recreating data/train and data/test files .."
python3 scripts/prepare-data-train-and-test.py
## Pre-process all the wav files (equalize the sampling frequency)
echo "Equalize all wav files' sampling frequency .."
python3 scripts/equalize-wav-sample-frequency.py
## Recreate all data/local/dict and data/local/corpus files for language modeling data
echo "Recreating data/local/dict and data/local/corpus files .."
python3 scripts/prepare-data-local-dict.py
python3 scripts/prepare-data-local-corpus.py

# Preparing acoustic data
echo
echo "###################################"
echo "#     PREPARING ACOUSTIC DATA     #"
echo "###################################"
echo
## Sort train and test data using Kaldi script
utils/validate_data_dir.sh data/train
utils/fix_data_dir.sh data/train
utils/validate_data_dir.sh data/test
utils/fix_data_dir.sh data/test
## Making spk2utt files
utils/utt2spk_to_spk2utt.pl data/train/utt2spk > data/train/spk2utt
utils/utt2spk_to_spk2utt.pl data/test/utt2spk > data/test/spk2utt

# Features extraction
echo
echo "###############################"
echo "#     FEATURES EXTRACTION     #"
echo "###############################"
echo
## Making feats.scp files
mfcc_dir=mfcc
steps/make_mfcc.sh --nj $nj --cmd "$train_cmd" data/train exp/make_mfcc/train $mfcc_dir
steps/make_mfcc.sh --nj $nj --cmd "$train_cmd" data/test exp/make_mfcc/test $mfcc_dir
## Making cmvn.scp files
steps/compute_cmvn_stats.sh data/train exp/make_mfcc/train $mfcc_dir
steps/compute_cmvn_stats.sh data/test exp/make_mfcc/test $mfcc_dir

# Preparing language data
echo
echo "###################################"
echo "#     PREPARING LANGUAGE DATA     #"
echo "###################################"
echo
## Prepare language data using Kaldi script
utils/prepare_lang.sh data/local/dict "<OOV>" data/local/lang data/lang

# Language model creation (lm.arpa)
echo
echo "##########################################"
echo "#     N-GRAM LANGUAGE MODEL CREATION     #"
echo "#             MAKING lm.arpa             #"
echo "##########################################"
echo
## Check SRILM ngram-count binary file existence
loc=`which ngram-count`;
echo "Checking SRILM\'s ngram-count binary location .."
if [ -z $loc ]; then
    if uname -a | grep 64 >/dev/null; then
        sdir=$KALDI_ROOT/tools/srilm/bin/i686-m64
    else
        sdir=$KALDI_ROOT/tools/srilm/bin/i686
    fi
    if [ -f $sdir/ngram-count ]; then
        echo "Using SRILM language modelling tool from $sdir"
        export PATH=$PATH:$sdir
    else
        echo "SRILM toolkit is probably not installed.
                Instructions: tools/install_srilm.sh"
        exit 1
    fi
else
    echo "ngram-count binary detected."
    echo "Using SRILM language modelling tool from $loc"
fi
## Create language model based on the data/local/corpus/corpus.txt file
data_local_dir=data/local
mkdir -p $data_local_dir/tmp
ngram-count -order $lm_order -write-vocab $data_local_dir/tmp/vocab-full.txt -wbdiscount -text $data_local_dir/corpus/corpus.txt -lm $data_local_dir/tmp/lm.arpa || exit 1
echo "Created vocab-full.txt and lm.arpa language model file in $data_local_dir/tmp"

# Making a weighted finite-state transducer
echo
echo "########################"
echo "#     MAKING G.fst     #"
echo "########################"
echo
lang_dir=data/lang
arpa2fst --disambig-symbol=#0 --read-symbol-table=$lang_dir/words.txt $data_local_dir/tmp/lm.arpa $lang_dir/G.fst

# Monophone training
echo
echo "##############################"
echo "#     MONOPHONE TRAINING     #"
echo "##############################"
echo
steps/train_mono.sh --nj $nj --cmd "$train_cmd" data/train data/lang exp/mono || exit 1

# Monophone decoding
echo
echo "##############################"
echo "#     MONOPHONE DECODING     #"
echo "##############################"
echo
utils/mkgraph.sh data/lang exp/mono exp/mono/graph || exit 1
steps/decode.sh --config conf/decode.config --nj $nj --cmd "$decode_cmd" --scoring-opts "--min-lmwt 10 --max-lmwt 20" exp/mono/graph data/test exp/mono/decode

# Monophone alignment (required for delta based triphone training)
echo
echo "###############################"
echo "#     MONOPHONE ALIGNMENT     #"
echo "###############################"
echo
steps/align_si.sh --nj $nj --cmd "$train_cmd" data/train data/lang exp/mono exp/mono_ali || exit 1

# Triphone training (delta based)
echo
echo "#################################"
echo "#     TRI1 (delta) TRAINING     #"
echo "#################################"
echo
steps/train_deltas.sh --nj $nj --cmd "$train_cmd" 2000 10000 data/train data/lang exp/mono_ali exp/tri1 || exit 1

# Triphone (delta based) decoding
echo
echo "#################################"
echo "#     TRI1 (delta) DECODING     #"
echo "#################################"
echo
utils/mkgraph.sh data/lang exp/tri1 exp/tri1/graph || exit 1
steps/decode.sh --config conf/decode.config --nj $nj --cmd "$decode_cmd" --scoring-opts "--min-lmwt 10 --max-lmwt 20" exp/tri1/graph data/test exp/tri1/decode

# Triphone (delta based) alignment (required for (delta+delta_delta) based triphone training)
echo
echo "##################################"
echo "#     TRI1 (delta) ALIGNMENT     #"
echo "##################################"
echo
steps/align_si.sh --nj $nj --cmd "$train_cmd" data/train data/lang exp/tri1 exp/tri1_ali || exit 1

# Triphone training (delta+delta_delta based)
echo
echo "#############################################"
echo "#     TRI1 (delta+delta_delta) TRAINING     #"
echo "#############################################"
echo
steps/train_deltas.sh --nj $nj --cmd "$train_cmd" 2500 15000 data/train data/lang exp/tri1_ali exp/tri2 || exit 1

# Triphone (delta+delta_delta based) decoding
echo
echo "#############################################"
echo "#     TRI1 (delta+delta_delta) DECODING     #"
echo "#############################################"
echo
utils/mkgraph.sh data/lang exp/tri2 exp/tri2/graph || exit 1
steps/decode.sh --config conf/decode.config --nj $nj --cmd "$decode_cmd" --scoring-opts "--min-lmwt 10 --max-lmwt 20" exp/tri2/graph data/test exp/tri2/decode

# Triphone (delta+delta_delta based) alignment (required for (delta + delta_delta) based triphone training)
echo
echo "##############################################"
echo "#     TRI1 (delta+delta_delta) ALIGNMENT     #"
echo "##############################################"
echo
steps/align_si.sh --nj $nj --cmd "$train_cmd" data/train data/lang exp/tri2 exp/tri2_ali || exit 1

echo
echo "===== run.sh script is finished ====="
echo