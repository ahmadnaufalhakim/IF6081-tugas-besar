import os
import pyaudio
import threading
from tkinter import *
from tkinter import scrolledtext
import wave

from asr import ASR

# Constants
## PyAudio
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
SAMPLE_RATE = 44100
SECONDS = 5
## Directories
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
TMP_DIR = os.path.join(CURR_DIR, "tmp")
if not os.path.exists(TMP_DIR) :
  os.mkdir(TMP_DIR)

# Global variables
record_on = False
counter = 0
stop_event = threading.Event()

class GUI :
  def __init__(self) -> None:
    # PyAudio
    self.p = None
    self.stream = None
    self.frames = []
    self.filename = ''
    # Live microphone thread
    self.thread = None

    # ASR module
    self.asr = ASR("tri2")

    # Core code of the GUI
    ## Window
    self.window = Tk()
    self.window.title("Tugas Besar IF6081-Speech")
    self.window.geometry("1250x700")
    self.window.configure(background="#346beb")
    self.window.columnconfigure(0, weight=1)
    self.window.columnconfigure(1, weight=1)
    ## Transcription (label + scrolledtext)
    self.label_transcription = Label(
      self.window,
      text="Transcription", font=("Helvetica 14 underline"),
      fg="White",
      bg="#346beb"
    )
    self.label_transcription.grid(
      row=0, column=0,
      pady=20
    )
    self.scrolledtext_transcription = scrolledtext.ScrolledText(
      self.window,
      width=75, height=25,
      font="Helvetica 16",
    )
    self.scrolledtext_transcription.grid(
      row=1, column=0,
    )
    ## Counter (label)
    self.label_counter = Label(
      self.window,
      text="00:00", font=("Helvetica 36"),
      bg="#346beb"
    )
    self.label_counter.grid(
      row=1, column=1,
      columnspan=2
    )
    ## Microphone (label + buttons)
    self.label_microphone = Label(
      self.window,
      text="Microphone", font=("Helvetica 14 underline"),
      fg="White",
      bg="#346beb"
    )
    self.label_microphone.grid(
      row=0, column=1,
      columnspan=2
    )
    self.button_live_decoding = Button(
      self.window,
      text="Live decoding",
      command=self.live_decoding
    )
    self.button_live_decoding.grid(
      row=2, column=0,
      pady=20
    )
    self.button_exit = Button(
      self.window,
      text="Exit",
      width=10,
      command=self.exit_app
    )
    self.button_exit.grid(
      row=2, column=1,
      columnspan=2
    )

  def start_counter(self, label) :
    def count() :
      global counter
      if not record_on :
        return
      counter += 1
      m, s = (counter%3600)//60, (counter%3600)%60
      label.config(
        text="{:02d}:{:02d}".format(m, s), font="Helvetica 36 bold",
        fg="red"
      )
      label.after(1000, count)
    count()

  def live_decoding(self) :
    global record_on, stop_event
    def start_recording() :
      global counter
      counter = 0
      prev_counter = 0
      buffer_frames = []
      self.start_counter(self.label_counter)
      self.stream.start_stream()
      while not stop_event.is_set() :
        data = self.stream.read(CHUNK,)
        self.frames.append(data)
        buffer_frames.append(data)
        if not record_on :
          # print(stop_event)
          # self.frames.clear()
          self.stream.stop_stream()
          self.stream.close()
          self.stream = None
          self.p.terminate()
          break
        if prev_counter+SECONDS == counter :
          prev_counter = counter
          print(prev_counter)
          self.filename = "tmp"
          tmp_wav_path = os.path.join(TMP_DIR, f"{self.filename}.wav")
          if os.path.exists(tmp_wav_path) :
            os.remove(tmp_wav_path)
          wv = wave.open(tmp_wav_path, "wb")
          wv.setnchannels(CHANNELS)
          wv.setsampwidth(self.p.get_sample_size(FORMAT))
          wv.setframerate(SAMPLE_RATE)
          wv.writeframes(b''.join(buffer_frames))
          wv.close()

          tmp_scp_path = os.path.join(TMP_DIR, f"{self.filename}.scp")
          with open(tmp_scp_path, 'w') as f_tmp_scp :
            f_tmp_scp.write(f"{self.filename} {tmp_wav_path}\n")
          
          decode_str = self.asr.decode(tmp_scp_path)
          decode_str = f"{' '.join(decode_str.split()[1:])}{' ' if decode_str.split()[1:] else ''}"
          os.remove(tmp_scp_path)
          print(f"*{decode_str}*")
          buffer_frames.clear()
          self.scrolledtext_transcription.insert(END, decode_str)
    if not record_on :
      record_on = True
      stop_event.clear()
      self.scrolledtext_transcription.delete("1.0", END)
      self.button_live_decoding.configure(text="Stop decoding")
      self.frames.clear()
      self.p = pyaudio.PyAudio()
      self.stream = self.p.open(
        rate=SAMPLE_RATE,
        channels=CHANNELS,
        format=FORMAT,
        frames_per_buffer=CHUNK,
        input=TRUE
      )
      self.thread = threading.Thread(target=start_recording, daemon=True)
      self.thread.start()
    else :
      record_on = False
      stop_event.set()
      self.thread.join(3.0)
      self.button_live_decoding.configure(text="Live decoding")
      self.filename = "tmp"
      tmp_wav_path = os.path.join(TMP_DIR, f"{self.filename}.wav")
      if os.path.exists(tmp_wav_path) :
        os.remove(tmp_wav_path)
      wv = wave.open(tmp_wav_path, "wb")
      wv.setnchannels(CHANNELS)
      wv.setsampwidth(self.p.get_sample_size(FORMAT))
      wv.setframerate(SAMPLE_RATE)
      wv.writeframes(b''.join(self.frames))
      wv.close()

      
      self.label_counter.config(
        font="Helvetica 36",
        fg="black"
      )

  def exit_app(self) :
    self.window.quit()

if __name__=="__main__" :
  gui = GUI()
  gui.window.mainloop()