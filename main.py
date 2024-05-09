import argparse
import numpy as np
import speech_recognition as sr
import whisper
import torch

from datetime import datetime, timedelta
from queue import Queue
from time import sleep
from time import time
from chat import Chat
from colors import *
import vlc

# seconds before emotion is invalid
EMOTION_THRES = 5

def process_session(text: str):
    # quit the program when the user says quit. Otherwise you'd have to quit by killing the process manually
    if text.strip().lower() == "quit" or text.strip().lower() == "quit.":
        f = open("action.txt", "w")
        f.write("quit\n")
        f.close()
        print(f"{orange}[INFO] Saving transcriptions...")

        # Save the transcription into a text file when quitting
        f = open("transcription.txt", "a")
        f.write("time " + str(time()) + "\n")
        for line in transcription:
            f.write(line + "\n")
        f.write("\n\n")
        print(f"{orange}[INFO] Quitting main.py...{reset}")
        quit()
    else:
        try: 
            # Append the user's current emotion to the message
            emotions = open("emotion.txt", "r").readline().split(' ')
            if len(emotions) > 2:
                time_past = float(emotions[2][:-1])
                if time() - time_past > EMOTION_THRES:
                    text = text + ' (You see that I am ' + emotions[0] + ' )'
                    print(f"{orange}[INFO] Emotion appended to message{reset}")
        except Exception as e:
            print(f"{red}[ERROR]{reset} Failed to fetch emotion.txt")

        print(f"{orange}[INFO] Processsing Responses...{reset}")
        message = chat.chat_normal(text)

    print(f"{orange}[INFO] Processing message emotional content...{reset}")
    response_emotion = chat.get_emotion(message)

    try:
        # Send an action to VTS
        f = open("action.txt", "w")
        f.write(response_emotion)
        f.close()
        print(f"{orange}[INFO] Action written to 'action.txt{reset}")
    except Exception as e:
        print("\033[91m[ERROR]\033[00m Failed to find 'action.txt'")
    
    # Play the response
    chat.tts_improved(message)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="small", help="Model to use",
                        choices=["tiny", "base", "small", "medium", "large"])
    parser.add_argument("--energy_threshold", default=1000,
                        help="Energy level for mic to detect.", type=int)
    parser.add_argument("--record_timeout", default=2,
                        help="How real time the recording is in seconds.", type=float)
    parser.add_argument("--phrase_timeout", default=2,
                        help="How much empty space between recordings before we "
                             "consider it a new line in the transcription.", type=float)
    args = parser.parse_args()

    global chat
    print(f"{orange}[INFO] Initializing Chat class...{reset}")

    # You can change the prompt here.
    chat = Chat(sysmessage=open("prompt1.txt").read())

    print(f"{orange}[INFO] Initializing Chat class successful{reset}")


    # The last time a recording was retrieved from the queue.
    phrase_time = None
    # Thread safe Queue for passing data from the threaded recording callback.
    data_queue = Queue()
    # We use SpeechRecognizer to record our audio because it has a nice feature where it can detect when speech ends.
    recorder = sr.Recognizer()
    recorder.energy_threshold = args.energy_threshold
    # Definitely do this, dynamic energy compensation lowers the energy threshold dramatically to a point where the SpeechRecognizer never stops recording.
    recorder.dynamic_energy_threshold = False

    print(f"{orange}[INFO] Sourcing microphone...{reset}")
    try:
        source = sr.Microphone(sample_rate=16000)
        print(f"{orange}[INFO] Successfully sourced microphone{reset}")
    except Exception as e:
        print("\033[91m[ERROR]\033[00m Failed to source microphone")

    # Load / Download model
    model = args.model
    if args.model != "large":
        model = model + ".en"
    audio_model = whisper.load_model(model)

    record_timeout = args.record_timeout
    phrase_timeout = args.phrase_timeout

    global transcription
    transcription = ['']

    with source:
        recorder.adjust_for_ambient_noise(source)

    def record_callback(_, audio:sr.AudioData) -> None:
        """
        Threaded callback function to receive audio data when recordings finish.
        audio: An AudioData containing the recorded bytes.
        """
        # Grab the raw bytes and push it into the thread safe queue.
        data = audio.get_raw_data()
        data_queue.put(data)

    # Create a background thread that will pass us raw audio bytes.
    # We could do this manually but SpeechRecognizer provides a nice helper.
    recorder.listen_in_background(source, record_callback, phrase_time_limit=record_timeout)
    print(f"{orange}[INFO] Recorder set up{reset}")

    # Cue the user that we're ready to go.
    print(f"{orange}[INFO] Model loaded.\n {reset}")

    phrase_time = datetime.utcnow()
    while True:
        try:
            now = datetime.utcnow()
            # Pull raw recorded audio from the queue.
            if not data_queue.empty():
                print(f"{orange} [INFO] Audio Received {reset}")

                phrase_complete = False
                # If enough time has passed between recordings, consider the phrase complete.
                # Clear the current working audio buffer to start over with the new data.
                if phrase_time and now - phrase_time > timedelta(seconds=phrase_timeout):
                    phrase_complete = True
                # This is the last time we received new audio data from the queue.
                
                phrase_time = now

                # Combine audio data from queue
                audio_data = b''.join(data_queue.queue)
                data_queue.queue.clear()
                
                # Convert in-ram buffer to something the model can use directly without needing a temp file.
                # Convert data from 16 bit wide integers to floating point with a width of 32 bits.
                # Clamp the audio stream frequency to a PCM wavelength compatible default of 32768hz max.
                audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

                # Read the transcription.
                result = audio_model.transcribe(audio_np, fp16=torch.cuda.is_available())
                text = result['text'].strip()

                # If we detected a pause between recordings, add a new item to our transcription.
                # Otherwise edit the existing one.
                if phrase_complete:
                    if len(text.strip()) == 0: 
                        print(f"{orange}[INFO] Empty message received, discarding...{reset}")
                        sleep(0.25)
                        continue
                    
                    transcription.append(text)
                    print(f"{orange}[INFO] Processing: " + text + reset)
                    # you have to wait 2 seconds before speaking your next sentence, and it has to be clear without stumbles, otherwise
                    # it gets pushed to the other case and you get no response.
                    # note that if you speak while the program speaks, it still counts
                    process_session(text)

                    # clear all the audio recorded when the program is talking. Might remove later...
                    print(f"{orange}[INFO] Clearing Audio queue...{reset}")
                    data_queue.queue.clear()
                    sleep(0.25)
                else:
                    transcription[-1] += " " + text
                    print(f"{orange}[INFO] Discarding: " + transcription[-1] + reset)

            else:
                # Infinite loops are bad for processors, must sleep.
                sleep(0.25)
        except KeyboardInterrupt:
            break



if __name__ == "__main__":
    main()
