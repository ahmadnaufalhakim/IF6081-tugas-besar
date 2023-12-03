import os

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(CURR_DIR, "..", "dataset")
DATA_DIR = os.path.join(CURR_DIR, "..", "data")
DATA_LOCAL_DIR = os.path.join(DATA_DIR, "local")
DATA_LOCAL_LANG_DIR = os.path.join(DATA_LOCAL_DIR, "lang")

NEWLINE = '\n'

with open(os.path.join(DATASET_DIR, "lexicon.csv")) as f_lex_csv, open(os.path.join(DATA_LOCAL_LANG_DIR, "lexicon.txt"), 'w') as f_lex_txt :
  # Include silence and out-of-vocabulary phone model
  f_lex_txt.write(f"!SIL SIL\n")
  f_lex_txt.write(f"<OOV> SPN\n")

  next(f_lex_csv)
  lines = f_lex_csv.readlines()
  for i, line in enumerate(lines) :
    row = line.split(',')
    word = row[1].strip().upper()
    phonemes_list = row[2:]
    for phonemes in phonemes_list :
      phonemes = ' '.join(phonemes.split()).strip().upper()
      if phonemes != '' :
        f_lex_txt.write(f"{word.strip().upper()} {' '.join(phonemes.split()).strip().upper()}{NEWLINE}")