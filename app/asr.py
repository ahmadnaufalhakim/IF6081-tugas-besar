import os
from kaldi.asr import GmmLatticeFasterRecognizer
from kaldi.decoder import LatticeFasterDecoderOptions
from kaldi.feat.mfcc import Mfcc, MfccOptions
from kaldi.feat.functions import compute_deltas, DeltaFeaturesOptions
from kaldi.feat.window import FrameExtractionOptions
from kaldi.transform.cmvn import Cmvn
from kaldi.util.table import SequentialWaveReader

# Constants (Directories)
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
CONF_DIR = os.path.join(CURR_DIR, "..", "conf")
EXP_DIR = os.path.join(CURR_DIR, "..", "exp")
def MODEL_DIR(am_model_type) :
  return os.path.join(EXP_DIR, am_model_type)

# Constants (for Kaldi decoding process)
## Decoder options
decoder_opts = LatticeFasterDecoderOptions()
decoder_opts.beam = 13
decoder_opts.max_active = 7000
## Frame extraction options
frame_opts = FrameExtractionOptions()
frame_opts.samp_freq = 44100
frame_opts.allow_downsample = True
## MFCC feature extraction options
mfcc_opts = MfccOptions()
mfcc_opts.use_energy = False
mfcc_opts.frame_opts = frame_opts

class ASR() :
  def __init__(self, am_model_type) -> None:
    if am_model_type not in ["mono", "tri1", "tri2"] :
      raise ValueError("invalid am_model_type, must be either \"mono\", \"tri1\", or \"tri2\"")
    # Construct recognizer
    self.asr = GmmLatticeFasterRecognizer.from_files(
      model_rxfilename=f"{MODEL_DIR(am_model_type)}_ali/final.mdl",
      graph_rxfilename=f"{MODEL_DIR(am_model_type)}/graph/HCLG.fst",
      symbols_filename=f"{MODEL_DIR(am_model_type)}/graph/words.txt",
      decoder_opts=decoder_opts
    )
    # Construct feature extraction pipeline
    self.feat_pipeline = self.make_feat_pipeline(Mfcc(mfcc_opts))

  def make_feat_pipeline(self, base, opts=DeltaFeaturesOptions()) :
    def feat_pipeline(wav_file) :
      feats = base.compute_features(wav_file.data()[0], wav_file.samp_freq, 1.0)
      cmvn = Cmvn(base.dim())
      cmvn.accumulate(feats=feats)
      cmvn.apply(feats=feats)
      return compute_deltas(opts, feats)
    return feat_pipeline

  def decode(self, scp_file) :
    result = ''
    rspec = "scp:"
    for key, wav in SequentialWaveReader(rspecifier=f"{rspec}{scp_file}") :
      feats = self.feat_pipeline(wav)
      out = self.asr.decode(feats)
      result = f"{key} {out['text']}"
    return result