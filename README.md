# AI-Prom-Date

Yes I did bring her to prom.

## Demo from the actual Prom Venue

https://github.com/KephaSher/AI-Prom-Date/assets/87000244/ae9f491b-9106-4a91-b592-335f036d74c2

![demo](https://github.com/KephaSher/AI-Prom-Date/assets/87000244/815d518f-a5be-4201-89ac-ae13333f5511)

This program only supports OS X, but Windows probably works the same with some minor tweaks.

The tutorial video will come soon...

To install, follow the steps:

## Initialize python virtual environment
1. Open terminal, find a suitable directory (could be just the repo directory) and type `python -m venv NAME_HERE`. Activate it by typing `source NAME_HERE/bin/activate`.
2. Install `requirements.txt` with ```pip install -r requirements.txt```.

## VTube Studios setup
1. Install [VTube Studios](https://denchisoft.com/) (You'll need a Steam account for this).
2. Click the cog on the top left, scroll down until you see the Start API button. Toggle that switch. The designated port should be 8001.
   <img width="1091" alt="Screenshot 2024-05-09 at 2 13 41 PM" src="https://github.com/KephaSher/AI-Prom-Date/assets/87000244/f2ea32c3-82cb-4b9f-99b8-73ee086292c8">
3. This program is designed so that certain emotions corresponds to certain hotkey actions of your model. The map could be found in `vtube.py` in the `MAP` dictionary on line 12. You should configure the hotkeys so that the names of the hotkeys matches the one given in the `MAP` variable. To change hotkey names, open VTube Studios and go to the fourth icon on the top bar.
<img width="1091" alt="Screenshot 2024-05-09 at 2 25 01 PM" src="https://github.com/KephaSher/AI-Prom-Date/assets/87000244/5291357f-8c34-4c4e-ba87-64c311240d97">


## Set up OpenAI
1. Get your OpenAI API setup by going [here](https://platform.openai.com/api-keys). You'll need to create an account for OpenAI, and then create your key.
2. Go to `chat.py` line 16, and paste your API key into that variable. 

## Initializing Google Cloud Text to Speech
1. First create an account and then make a new project [here](https://console.cloud.google.com/welcome/new?hl=en). 
2. Start a new project from this page by clicking the top left project icon
   <img width="1275" alt="Screenshot 2024-05-09 at 12 36 11 PM" src="https://github.com/KephaSher/AI-Prom-Date/assets/87000244/0cc8e4e3-7857-4118-9ee0-3348ad0ad05f">
3. Go to API & Services for this new project and enable the API.
  <img width="1275" alt="Screenshot 2024-05-09 at 12 37 13 PM" src="https://github.com/KephaSher/AI-Prom-Date/assets/87000244/3f855662-2b6b-4c5e-9f01-0e540d390771">
4. Go to IAM & Admin and click on Service Accounts, you should then be able to download your API JSON file here.
<img width="1275" alt="Screenshot 2024-05-09 at 12 38 01 PM" src="https://github.com/KephaSher/AI-Prom-Date/assets/87000244/74d050a2-bae3-4f33-b745-255a14f67ff7">
<img width="1275" alt="Screenshot 2024-05-09 at 12 38 15 PM" src="https://github.com/KephaSher/AI-Prom-Date/assets/87000244/9814f253-670a-4394-9bb7-8b6b86ceb0f1">
5. After clicking on your project link, click on the KEY tab and get your API.
 
6. Replace the `REPLACE_THIS.json` file in this repo with the new json credentials you've just downloaded.

## Setting up Loopback
1. Loopback is avaliable on their official [website](https://rogueamoeba.com/loopback/)
2. Download the app, and pipe the audio input from terminal (or whatever you're running your program from) to VTubeStudios. To do that, create a new device and a new output channel and link your terminal up with the output device, and then link that to your monitor. My example:
   <img width="1188" alt="Screenshot 2024-05-09 at 2 04 42 PM" src="https://github.com/KephaSher/AI-Prom-Date/assets/87000244/0ad2a2d5-675f-4a37-8c4f-f80d14b4c367">
3. Next, click the cog in VTube Studios, and configure your VTube Studios so that it recieves audio input from the Loopback device you created:
<img width="1108" alt="Screenshot 2024-05-09 at 2 08 10 PM" src="https://github.com/KephaSher/AI-Prom-Date/assets/87000244/e13ee365-157b-40ec-833a-adff4f09e736">
4. To make your model's mouth move with audio input, go to the character setting (the third icon to the right on the top bar), and find the following setting and change it to what is shown:
 <img width="331" alt="Screenshot 2024-05-09 at 2 09 07 PM" src="https://github.com/KephaSher/AI-Prom-Date/assets/87000244/2192680c-c68e-4663-afdf-3d79cf464a9f">

## Get OBS to stream VTube Studios and add captions
1. Download OBS
2. Under Sources, click the add button to create Screen Capture. In the Properties section of this screen capture, choose Window Capture and select VTube Studios (which needs to be open of course) <img width="1164" alt="Screenshot 2024-07-21 at 1 14 13 PM" src="https://github.com/user-attachments/assets/d7bba578-9c26-4d59-9801-f4ed8a6a0ac1">

3. To add captions, click the add buton this time choosing Text (Freetype 2). For its properties, select "From file" for the Text Input Mode. The text file to choose from is the `output.txt` file in this repo. <img width="1164" alt="Screenshot 2024-07-21 at 1 14 41 PM" src="https://github.com/user-attachments/assets/5a5b477f-754a-4275-a68e-91fc02b623ac">

4. Right click on the Text object under sources, and click "Transform > Edit Transform". For Bounding Box Type, select Scale to inner bounds. You can also adjust the size of the caption box here. <img width="1164" alt="Screenshot 2024-07-21 at 1 15 52 PM" src="https://github.com/user-attachments/assets/7d729f2a-6fa2-4422-b28c-25650e45c222"> <img width="1164" alt="Screenshot 2024-07-21 at 1 16 00 PM" src="https://github.com/user-attachments/assets/33654a7c-a565-4760-8200-39bafaef5461">


5. Move the captions to a pleasant position.
6. To project to a monitor (or to simply full screen), right click Scene under the "Scene section", and click "Full Screen Projector (Scene), and your monitors should pop up there. <img width="1164" alt="Screenshot 2024-07-21 at 1 16 07 PM" src="https://github.com/user-attachments/assets/b8f34564-8d41-44cc-bf52-bea138c15038">

## Instructions for running the program

1. Ensure you are in the correct virtual environment.
2. Run `setup.py`.

There are 2 additional flags you can apply. They both default to False.

   ```python3 setup.py --enable_video=True```
   
runs the program with video enabled, so she can see you and recognize your emotions. Her perceived emotion will be used to augment her speech. Make sure you    have a functional webcam. Warning: this option is very GPU intensive.

```python3 setup.py --enable_vtube=True```

runs the program with VTube Studios actions enabled. This means that she'll be able to perform certain actions, like bobbing her head, when she feels a certain emotion. If you select this option, there will be a pop-up on your VTube Studios application. Just click OK and you should see updates in the command line, meaning it's properly running.

3. To quit, say `Quit`. Once she picks up everything should quit. If not, you can always kill the processes with `ps aux | grep [...]` with whatever program you just ran.

## Debugging info and other important information

I have color coded a lot of logging/update information for ease of tracking the program while running. These are:
- Orange: messages from `main.py`. You'll be able to see what she picked up from your speech. <img width="646" alt="Screenshot 2024-07-21 at 1 44 49 PM" src="https://github.com/user-attachments/assets/87fff53b-5e9d-42bf-8ee4-1e306c434a16"> Note that **the first message is always meant as a test message and discarded**
- Green: Update ticks from `vtube.py`. Due to my incompetence, I have no idea how to maintain a websocket connection for more than half a minute without sending out requests. That's why I send a message, through a websocket, to Vtube Studios every 2 seconds (just to be safe). Aside from this annoying logging information, you should also get a response whenever she decides to perform an emotion: `[INFO] Received hotkey request`.
- Blue: Updates the video feed. There will be updates on her saving her perceived emotion to a file: `[INFO] Wrote emotion [...] to 'emotion.txt' at time [...]'`
- Purple: Updates on the status of synthesized speech and captions. The captions are updated live as she speaks.
- Cyan: Only for the setup file. Tells you if everything's been initialized.
- Red: All errors are coded red.

An important thing to note is how the audio reception works. Once you start speaking, the program decides your sentence is finished if there's been a period of silence for more than 2 seconds. In other words, you can't pause for long, otherwise the things you said after that pause will be neglected. There's actually a flag that controls this in `main.py` called `--phrase_timeout` and `--record_timeout` (you need to change both), which defaults to 2. You can change this in the code at line 99 of `main.py`. 
