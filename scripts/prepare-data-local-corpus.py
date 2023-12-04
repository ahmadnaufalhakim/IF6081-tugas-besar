import os
import string

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(CURR_DIR, "..", "dataset")
TRANSCRIPTION_DIR = os.path.join(DATASET_DIR, "Label")

DATA_DIR = os.path.join(CURR_DIR, "..", "data")
if not os.path.exists(DATA_DIR) : os.mkdir(DATA_DIR)
DATA_LOCAL_DIR = os.path.join(DATA_DIR, "local")
if not os.path.exists(DATA_LOCAL_DIR) : os.mkdir(DATA_LOCAL_DIR)
DATA_LOCAL_CORPUS_DIR = os.path.join(DATA_LOCAL_DIR, "corpus")
if not os.path.exists(DATA_LOCAL_CORPUS_DIR) : os.mkdir(DATA_LOCAL_CORPUS_DIR)

NEWLINE = '\n'

def remove_punctuation(input_string):
  input_string = input_string.replace('-', ' ')
  # Make a translation table that maps all punctuation characters to None
  translator = str.maketrans("", "", string.punctuation)
  # Apply the translation table to the input string
  result = input_string.translate(translator)
  return ' '.join(result.split())

# Read all transcriptions from dataset/Label
unique_sentences = set()
for root, dirs, files in os.walk(TRANSCRIPTION_DIR) :
  for file in files :
    if ".txt" in file :
      with open(os.path.join(root, file)) as f_txt :
        for line in f_txt :
          line = remove_punctuation(line).upper().strip()
          unique_sentences.add(line)

# Write data/local/corpus/corpus.txt
with open(os.path.join(DATA_LOCAL_CORPUS_DIR, "corpus.txt"), 'w') as f_corpus :
  for sentence in sorted(unique_sentences) :
    f_corpus.write(f"{sentence}{NEWLINE}")