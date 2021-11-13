### 

# 1 To be Solved
1- If I go to scan barcode through text I cannot use after the navigation drawer

2- The speech to text should be changed, as it has a bad performance when it comes to understand human voices

3- The load_video function when it has found a barcode it stores it in self.food_item, but it
has not yet been display to the chat screen.

# 2 Main App
The .kv files handle the styling and structure of each screen page, but the classes shown in main.py handle the backend of the application, such as listen to the user when the microphone is pressed. 

Note that the messages the app displays are not safe messages, they have been stored in demo_users/users.py and loaded into the application at run time by load_past_msg(self)

class MainApp(MDApp): loads the app,as well ass the messsages 

## Chat Screen Classes
class Message(MDBoxLayout): Stores the value of each message, in order for the ChatScreen.kv to handle the styling of such message 

class ChatScreen(Screen): It handles the process of sending message when the icon send is pressed, getting the audio from the user when the microphone icon is pressed, as well as processing the message (what needs to be called in order to preform the request of the user).

## Navigation Drawer Classes
class ContentNavigationDrawer(BoxLayout): No need to be implemented, it is a placeholder to link .kv file with a .py file

class WindowManager(ScreenManager): No need to be implemented, it is a placeholder to link .kv file with a .py file

## Barcode Camera Classes
class BarcodeScreen(Screen): No need to be implemented, it is a placeholder to link .kv file with a .py file

class ZBarCam(MDBoxLayout): Camera in charge of scanning the barcode

## Instruction Classes
class InstructionsScreen(Screen): Not yet implemented; It is a place holder for when Instructions.kv starts being implemented

## Scan Document Classes
class ScanDocumentScreen (Screen): Not yet implemented, it is a place holder for when ScanDocument.kv starts being implemented

# 3 Screens (.kv files)

## main.kv
Registers all the different screens that the application can switch between, as well as the main navigation bar

## Instructions.kv
The goal of this page is to write the set of instructions on how to use the app, as well as the different capabilities of the app.

## NaviationDrawer.kv
It handles the navigation bar of the application. It allows for screen switching. 
When switching between screens it will call the function unschedule_video to make sure the camera is not on regardless if the document has finished scanning. 

This kv file also contains the Screen styling for the <BarcodeScreen>, as well as the camera <ZBarCam> for that screen; Both found at the bottom of the file

## ScanDocument.kv
The goal of this page is to scan a document using an aligment algorithm to help the individual. After this, it will look for specific ways to divide the document into different sections. 

## ChatScreen.kv
It contains a Message class handling the styling of the messages.
<TextField@MDCard> represent the input bar, in which either the user can type the command, or use the microphone icon to specify the command.
  
# 4 Github Repos that could be helpful
1 - https://github.com/Sahil-pixel/Kivy-Android-Face-Detection/blob/main/main.py
  
2 - https://github.com/cutehaddy/WhatsApp-Redesign/tree/main/Whatsapp%20Clone/kvs/pages

3 - https://github.com/kivy-garden/zbarcam
  
4 - https://github.com/tito/android-zbar-qrcode
  
