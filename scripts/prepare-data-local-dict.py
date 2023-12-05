import os

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(CURR_DIR, "..", "dataset")

DATA_DIR = os.path.join(CURR_DIR, "..", "data")
if not os.path.exists(DATA_DIR) : os.mkdir(DATA_DIR)
DATA_LOCAL_DIR = os.path.join(DATA_DIR, "local")
if not os.path.exists(DATA_LOCAL_DIR) : os.mkdir(DATA_LOCAL_DIR)
DATA_LOCAL_DICT_DIR = os.path.join(DATA_LOCAL_DIR, "dict")
if not os.path.exists(DATA_LOCAL_DICT_DIR) : os.mkdir(DATA_LOCAL_DICT_DIR)

NEWLINE = '\n'

# Write data/local/dict/lexicon.txt (REQUIRES dataset/lexicon.csv)
with open(os.path.join(DATASET_DIR, "lexicon.csv")) as f_lex_csv, open(os.path.join(DATA_LOCAL_DICT_DIR, "lexicon.txt"), 'w') as f_lex_txt :
  # Include silence and out-of-vocabulary phone model
  f_lex_txt.write(f"!SIL SIL\n")
  f_lex_txt.write(f"<OOV> SPN\n")
  # Skip header
  next(f_lex_csv)

  for line in f_lex_csv :
    row = line.split(',')
    word = row[1].strip().upper()
    phonemes_list = row[2:]
    for phonemes in phonemes_list :
      phonemes = ' '.join(phonemes.split()).strip().upper()
      if phonemes != '' :
        f_lex_txt.write(f"{word.strip().upper()} {' '.join(phonemes.split()).strip().upper()}{NEWLINE}")

# Write data/local/dict/nonsilence_phones.txt
with open(os.path.join(DATA_LOCAL_DICT_DIR, "lexicon.txt")) as f_lex_txt, open(os.path.join(DATA_LOCAL_DICT_DIR, "nonsilence_phones.txt"), 'w') as f_nonsil_phns :
  phones = set()
  # Skip first two lines that represents silence and out-of-vocabulary phone model
  next(f_lex_txt)
  next(f_lex_txt)
  # Collect all unique phones in the lexicon file
  for line in f_lex_txt :
    phonemes = line.split()[1:]
    phones.update(phonemes)
  # Write all non-silence phones to data/local/dict/nonsilence_phones.txt
  for i, phone in enumerate(sorted(phones)) :
    f_nonsil_phns.write(f"{phone}{NEWLINE}")

# Write data/local/dict/optional_silence.txt and data/local/dict/silence_phones.txt
with open(os.path.join(DATA_LOCAL_DICT_DIR, "optional_silence.txt"), 'w') as f_opt_sil, \
     open(os.path.join(DATA_LOCAL_DICT_DIR, "silence_phones.txt"), 'w') as f_sil_phns :
  f_opt_sil.write(f"SIL{NEWLINE}")
  f_sil_phns.write(f"SIL{NEWLINE}")
  f_sil_phns.write(f"SPN{NEWLINE}")