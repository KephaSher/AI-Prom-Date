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
2. Under Sources, click the add button to create Screen Capture. In the Properties section of this screen capture, choose Window Capture and select VTube Studios (which needs to be open of course)
3. To add captions, click the add buton this time choosing Text (Freetype 2). For its properties, select "From file" for the Text Input Mode. The text file to choose from is the `output.txt` file in this repo.
4. Right click on the Text object under sources, and click "Transform > Edit Transform". For Bounding Box Type, select Scale to inner bounds. You can also adjust the size of the caption box here.
5. Move the captions to a pleasant position.
6. To project to a monitor (or to simply full screen), right click Scene under the "Scene section", and click "Full Screen Projector (Scene), and your monitors should pop up there.
