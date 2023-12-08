import os
from asr import ASR

# Constants
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(CURR_DIR, "input")
TMP_DIR = os.path.join(CURR_DIR, "tmp")
if not os.path.exists(TMP_DIR) :
  os.mkdir(TMP_DIR)

if not os.path.exists(INPUT_DIR) :
  print("input directory does not exist. Creating input directory ..")
  os.mkdir(INPUT_DIR)
  print("Please put your audio wav file input in the input directory")
  exit(1)

files = os.listdir(INPUT_DIR)
if len(files) == 0 :
  print("Please put your audio wav file input in the input directory")
  exit(1)

asr = ASR("tri2")
for file in sorted(files) :
  filename = os.path.basename(file).split('.')[0]
  tmp_scp_path = os.path.join(TMP_DIR, f"{filename}.scp")
  wav_path = os.path.join(INPUT_DIR, f"{file}")
  with open(tmp_scp_path, 'w') as f_tmp_scp :
    f_tmp_scp.write(f"{filename} {wav_path}\n")
  print(asr.decode(tmp_scp_path))
  os.remove(tmp_scp_path)
