# IF6081-tugas-besar
Kaldi recipe for IF6081 Speech Recognition final assignment

## Directories info
- `app`

Contains the source code for the interface of the ASR system

- `conf`

Contains the configuration files used for this project (feature extraction, decoding configuration, etc.)

- `data`

Contains data used for training and testing, language modelling, and whatnot

- `doc/att`

Contains attachments used for the assignment's report

- `exp`

Contains the final acoustic model, decoding graph, and training logs

- `local`

Contains the scoring shell script (as of now is just a symbolic link to Kaldi's scoring script)

- `mfcc`

Contains the MFCC features for the audio for each training and testing dataset

- `scripts`

Contains helper scripts (in Shell and Python) for data preparation in `data` directory

- `src`, `steps`, and `utils`

Contains the source code, steps and utils scripts of Kaldi library (as of now is just a symbolic link to Kaldi's source code, steps and utils scripts)