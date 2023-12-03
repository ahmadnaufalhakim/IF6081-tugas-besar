import os
import random
import string
random.seed(6081)

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(CURR_DIR, "..", "dataset")
AUDIO_DIR = os.path.join(DATASET_DIR, "Audio")
TRANSCRIPT_DIR = os.path.join(DATASET_DIR, "Label")
DATA_DIR = os.path.join(CURR_DIR, "..", "data")
TRAIN_DIR = os.path.join(DATA_DIR, "train")
TEST_DIR = os.path.join(DATA_DIR, "test")

def split_data(dir_path, test_ratio=.2) :
  # Get all file names in the directory
  all_files = [file for file in os.listdir(dir_path) if file.endswith('.wav')]
  # Sort the file paths alphabetically
  all_files.sort()
  # Calculate the number of files for testing
  num_test_files = int(len(all_files) * test_ratio)
  # Randomly select files for testing
  test_files = random.sample(all_files, num_test_files)
  # Sort the test files alphabetically
  test_files.sort(
    # key=lambda file_name: file_name[0]
  )
  # Create a list of training files
  train_files = [file for file in all_files if file not in test_files]
  # Sort the training files alphabetically
  train_files.sort(
    # key=lambda file_name: file_name[0]
  )
  return train_files, test_files

def remove_punctuation(input_string):
  input_string = input_string.replace('-', ' ')
  # Make a translation table that maps all punctuation characters to None
  translator = str.maketrans("", "", string.punctuation)
  # Apply the translation table to the input string
  result = input_string.translate(translator)
  return ' '.join(result.split())

if not os.path.exists(DATA_DIR) :
  os.mkdir(DATA_DIR)
if not os.path.exists(TRAIN_DIR) :
  os.mkdir(TRAIN_DIR)
if not os.path.exists(TEST_DIR) :
  os.mkdir(TEST_DIR)

speaker_ids = sorted(
  os.listdir(AUDIO_DIR),
  # key=lambda dir_name: (dir_name[0], int(dir_name.split('-')[-1]))
)

with open(os.path.join(TRAIN_DIR, "spk2gender"), 'w') as f_train_spk2gender,  \
     open(os.path.join(TRAIN_DIR, "wav.scp"), 'w') as f_train_wav_scp,        \
     open(os.path.join(TRAIN_DIR, "text"), 'w') as f_train_text,              \
     open(os.path.join(TRAIN_DIR, "utt2spk"), 'w') as f_train_utt2spk,        \
     open(os.path.join(TEST_DIR, "spk2gender"), 'w') as f_test_spk2gender,    \
     open(os.path.join(TEST_DIR, "wav.scp"), 'w') as f_test_wav_scp,          \
     open(os.path.join(TEST_DIR, "text"), 'w') as f_test_text,                \
     open(os.path.join(TEST_DIR, "utt2spk"), 'w') as f_test_utt2spk :
  for speaker_id in speaker_ids :
    train_files, test_files = split_data(os.path.join(AUDIO_DIR, speaker_id))

    if "Female" in speaker_id :
      gender = 'f'
    elif "Male" in speaker_id :
      gender = 'm'

    # Write spk2gender file
    f_train_spk2gender.write(f"{speaker_id} {gender}\n")
    f_test_spk2gender.write(f"{speaker_id} {gender}\n")

    for file_name in train_files :
      # Write wav.scp file
      utterance_id = f"{speaker_id}-{file_name.strip('.wav')}"
      f_train_wav_scp.write(f"{utterance_id} {os.path.join(AUDIO_DIR, speaker_id, file_name)}\n")
      # Write utt2spk file
      f_train_utt2spk.write(f"{utterance_id} {speaker_id}\n")
      # Write text file
      with open(os.path.join(TRANSCRIPT_DIR, speaker_id, f"{file_name.strip('.wav')}.txt")) as f_transcript :
        lines = f_transcript.readlines()
        if len(lines) > 1 : print(f"WARNING! {f'{utterance_id}.txt'} has more than one line of transcript")
        f_train_text.write(f"{utterance_id} {remove_punctuation(lines[0]).strip().upper()}\n")

    for file_name in test_files :
      # Write wav.scp file
      utterance_id = f"{speaker_id}-{file_name.strip('.wav')}"
      f_test_wav_scp.write(f"{utterance_id} {os.path.join(AUDIO_DIR, speaker_id, file_name)}\n")
      # Write utt2spk file
      f_test_utt2spk.write(f"{utterance_id} {speaker_id}\n")
      # Write text file
      with open(os.path.join(TRANSCRIPT_DIR, speaker_id, f"{file_name.strip('.wav')}.txt")) as f_transcript :
        lines = f_transcript.readlines()
        if len(lines) > 1 : print(f"WARNING! {f'{utterance_id}.txt'} has more than one line of transcript")
        f_test_text.write(f"{utterance_id} {remove_punctuation(lines[0]).strip().upper()}\n")
    # print(root)
    # print((train_files, test_files))
    # print(len(train_files), len(test_files))
    # print()