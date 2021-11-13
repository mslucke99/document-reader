# Installation

## Step 1: Create a virtual environment
```
python -m pip install --upgrade pip setuptools virtualenv
python -m virtualenv kivy_venv
```
## Step 2: Activate the environment
```
source kivy_venv/Scripts/activate
```
## Step 3: Install kivy
```
python -m pip install kivy[base]kivy_examples
pip install kivymd

```

## Step 4: Install Dependencies
```
pip install zbarcam
pip install opencv-python
pip install pyzbar
pip intall numpy 

pip install SpeechRecognition
pip install gtts
pip install pyttsx3
pip install PyAudio
pip install playsound

pip install beautifulsoup4
pip install lxml 
pip install requests 

```
(Note that you may need to manually download pyaudio executable since the pip command contains errors)


## Step 5: Move all the files into the kivy_venv folder

# Run the App
```
python kivy_venv\app.py
```

# Explore the app
1- Type "scan barcode" and press the send icon

2- Press the microphone icon and say "scan barcode"

3- Use the navigation bar to switch between screens
