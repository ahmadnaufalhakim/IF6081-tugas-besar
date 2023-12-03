import os
import string

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(CURR_DIR, "..", "dataset")
TRANSCRIPTION_DIR = os.path.join(DATASET_DIR, "Label")

def remove_punctuation(input_string):
  input_string = input_string.replace('-', ' ')
  # Make a translation table that maps all punctuation characters to None
  translator = str.maketrans("", "", string.punctuation)
  # Apply the translation table to the input string
  result = input_string.translate(translator)
  return result

unique_words = set()
i = 0
for root, dirs, files in os.walk(TRANSCRIPTION_DIR) :
  for file in files :
    if ".txt" in file :
      with open(os.path.join(root, file)) as f_txt :
        for line in f_txt :
          line = remove_punctuation(line).lower().strip()
          words = line.split()
          # Check in which file a certain word is spoken in the audio data
          if "macau" in words :
            print(file, words)
          unique_words.update(words)

# unique_words = sorted(list(unique_words))
# for word in unique_words :
#   print(word.upper())