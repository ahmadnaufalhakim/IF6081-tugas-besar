import os

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CURR_DIR, "..", "data")
DATA_LOCAL_DIR = os.path.join(DATA_DIR, "local")
DATA_LOCAL_LANG_DIR = os.path.join(DATA_LOCAL_DIR, "lang")

NEWLINE = '\n'

with open(os.path.join(DATA_LOCAL_LANG_DIR, "lexicon.txt")) as f_lex_txt, open(os.path.join(DATA_LOCAL_LANG_DIR, "nonsilence_phones.txt"), 'w') as f_nonsil_phns :
  phones = set()
  # Skip first two lines that represents silence and out-of-vocabulary phone model
  next(f_lex_txt)
  next(f_lex_txt)

  # Collect all unique phones in the lexicon file
  for line in f_lex_txt :
    phonemes = line.split()[1:]
    phones.update(phonemes)

  # Write all non-silence phones to data/local/lang/nonsilence_phones.txt
  for i, phone in enumerate(sorted(phones)) :
    f_nonsil_phns.write(f"{phone}{NEWLINE}")
