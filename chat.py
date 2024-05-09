import os
from pathlib import Path
from openai import OpenAI 
from audioplayer import AudioPlayer
import time
from time import sleep
from google.cloud import texttospeech_v1beta1 as texttospeech
import vlc
from colors import *

# Place the path to your JSON credential file into an environment variable
# example: os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/Users/kephasher/Documents/girl/chatbot-xxx.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "PLACE PATH HERE"

# It's bad practice to put your api key inside the running program but I'm too lazy to care
openai_key = "PLACE API KEY HERE"

class Chat:
    def __init__(self, sysmessage=""):
        # `sysmessage` is the system prompt for the chatbot
        self.sysmessage = sysmessage
        self.messages = [ {"role": "system", "content": sysmessage} ]

        # Connect to clients
        try:
            self.cloud_client = texttospeech.TextToSpeechClient()
            print("[INFO] Google Cloud Text To Speech Client initialized")
        except Exception as e:
            print("\033[91m[ERROR]\033[00m Failed to initialize Google Cloud Client")

        try:
            self.openai_client = OpenAI(api_key=openai_key) 
            print("[INFO] OpenAI Client initialized")
        except Exception as e:
            print("\033[91m[ERROR]\033[00m Failed to initialize OpenAI Client")

    def chat_normal(self, message):
        if message:
            self.messages.append(
                {"role": "user", "content": message},
            )
            chat = self.openai_client.chat.completions.create(model="gpt-3.5-turbo", messages=self.messages, temperature=1.0)

        reply = chat.choices[0].message.content
        self.messages.append({"role": "assistant", "content": reply})
        return reply
    
    # this method uses Openai API
    def tts(self, message: str):
        speech_file_path = Path(__file__).parent / "output.mp3"
        response = self.openai_client.audio.speech.create(
            model="tts-1",
            voice="nova", # change voice here
            input=message
        )

        count = 0
        current = 0
        x = message.split()
        for i in range(len(x)):
            count += 1
            current += 1
            with open("output.txt", "a", encoding="utf-8") as out:
                out.write(x[i] + " ")
            if count % 13 == 0:
                with open("output.txt", "a", encoding="utf-8") as out:
                    out.write("\n")
        open("output.txt", "a", encoding="utf-8").write("\n")

        print("[INFO] Captions Written through OpenAI Client")

        response.stream_to_file(speech_file_path)
        AudioPlayer(str(Path(__file__).parent / "output.mp3")).play(block=True)
        open("output.txt", "w").close()
    
    # This method uses google cloud text to speech API
    def tts_improved(self, message: str):
        DELAY = 0.01
        input_text = texttospeech.SynthesisInput(text=message)

        # Note: the voice can also be specified by name.
        # Names of voices can be retrieved with client.list_voices().

        # English
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Neural2-H", # change voice here
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )


        # If you want a sexy french guy
        # voice = texttospeech.VoiceSelectionParams(
        #     language_code = "fr-FR", 
        #     name = "fr-FR-Polyglot-1",
        #     ssml_gender=texttospeech.SsmlVoiceGender.MALE
        # )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=1
        )

        # Configure SSML text file
        response = message
        ssml_text = '<speak>'
        response_counter = 0
        mark_array = []
        for s in response.split(' '):
            ssml_text += f'<mark name="{response_counter}"/>{s}'
            mark_array.append(s)
            response_counter += 1
        ssml_text += '</speak>'

        input_text = texttospeech.SynthesisInput(ssml = ssml_text)

        request = texttospeech.SynthesizeSpeechRequest(
            input=input_text,
            voice=voice,
            audio_config=audio_config,
            enable_time_pointing=[texttospeech.SynthesizeSpeechRequest.TimepointType.SSML_MARK]
        )

        try:
            response = self.cloud_client.synthesize_speech(request)
            print("[INFO] Successfully synthesized speech")
        except Exception as e:
            print(e)
            print("\033[91m[ERROR]\033[00m Could not synthesize audio, clearing output file and returning...")
            open('output.txt', 'w').close()
            return
        
        # The response's audio_content is binary.
        with open("output.mp3", "wb") as out:
            out.write(response.audio_content)

        audio_file = os.path.dirname(__file__) + '/output.mp3'
        media = vlc.MediaPlayer(audio_file)
        media.play()

        print("[INFO] Writting Captions through Cloud Client")

        count = 0
        current = 0
        for i in range(len(response.timepoints)):
            count += 1
            current += 1
            with open("output.txt", "a", encoding="utf-8") as out:
                out.write(mark_array[int(response.timepoints[i].mark_name)] + " ")
            if i != len(response.timepoints) - 1:
                total_time = response.timepoints[i + 1].time_seconds
                sleep(max(0, total_time - response.timepoints[i].time_seconds - DELAY))
            if current == 25:
                    open('output.txt', 'w', encoding="utf-8").close()
                    current = 0
                    count = 0
            elif count % 8 == 0:
                with open("output.txt", "a", encoding="utf-8") as out:
                    out.write("\n")
        sleep(2)

        open('output.txt', 'w').close()

    # Analyze emotion of a given input
    def get_emotion(self, message):
        response = self.openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "system",
            "content": f"You will be provided with a response from a conversation, and your task is to classify its sentiment as [happy, neutral, sad, suprised, fear, anger]. ONLY OUTPUT ONE WORD FROM THE LIST"
            },
            {
            "role": "user",
            "content": message
            }
        ],
        temperature=0.1,
        max_tokens=64,
        top_p=1
        )

        return response.choices[0].message.content

if __name__ == '__main__':
    # Testing code

    from time import time
    x = time()
    prompt = open("prompt1.txt").read()
    c = Chat(sysmessage=prompt)
    res = c.chat_normal(input("talk to her: "))   
    print("-"*50)
    print(f"message: {res}")
    c.tts(res)
    print(f"emotion: {c.get_emotion(res)}")
    print(f"time used: {time() - x}")

