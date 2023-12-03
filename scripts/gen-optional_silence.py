import os

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CURR_DIR, "..", "data")
DATA_LOCAL_DIR = os.path.join(DATA_DIR, "local")
DATA_LOCAL_LANG_DIR = os.path.join(DATA_LOCAL_DIR, "lang")

with open(os.path.join(DATA_LOCAL_LANG_DIR, "optional_silence.txt"), 'w') as f_sil_phns :
  f_sil_phns.write(f"SIL\n")