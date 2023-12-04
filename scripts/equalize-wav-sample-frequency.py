import librosa
import os
import soundfile as sf

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(CURR_DIR, "..", "dataset")
AUDIO_DIR = os.path.join(DATASET_DIR, "Audio")

speakers = os.listdir(AUDIO_DIR)
for speaker in speakers :
  wavs = os.listdir(os.path.join(AUDIO_DIR, speaker))
  for wav in wavs :
    file_path = os.path.join(AUDIO_DIR, speaker, wav)
    y, sr = librosa.load(file_path, sr=None)
    target_sr = 44100
    if sr == target_sr :
      continue
    y_resampled = librosa.resample(y, orig_sr=sr, target_sr=target_sr)
    sf.write(file_path, y_resampled, target_sr)