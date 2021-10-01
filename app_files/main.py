
# LIST of styling sheets use
import kivy
from kivymd.app import MDApp 
from kivy.lang import Builder 
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import BooleanProperty, DictProperty, ListProperty, NumericProperty, ObjectProperty, OptionProperty, StringProperty
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.picker import MDThemePicker
from kivy.uix.scrollview import ScrollView
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.label import MDLabel
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.clock import Clock

# from user.py in demo_user folder import the list with all the messages stored
from demo_users.user import user_chat

#Import for barcode decoder
import time
import pyzbar.pyzbar as zbar
import cv2

# speech text
from audio.speechRecog import get_command

#Import food item Objects and web scraping functions 
# Functions created by me and that are found in the barcode folder
from barcode.foodObjects import *
from barcode.webScraping import web_scrapping

# Load the screen styling to the main app
Builder.load_file('Screens/ChatScreen.kv')
Builder.load_file('Screens/Instructions.kv')
Builder.load_file("Screens/ScanDocument.kv")
Builder.load_file("Screens/NavigationDrawer.kv")

Window.size = (320, 600)



#INSTRUCT SCREEN
class InstructionsScreen(Screen):
    '''
    Not yet implemented; It is a place holder for when Instructions.kv
     starts being implemented
    '''
    pass
# Scan Document
class ScanDocumentScreen (Screen):
    '''
    Not yet implemented; It is a place holder for when Instructions.kv
     starts being implemented
    '''
    pass

# BARCODE CAMERA 
class BarcodeScreen(Screen):
    '''
    No need to be implemented, it is a placeholder to link .kv 
    file with this .py file
    '''
    pass

class ZBarCam(MDBoxLayout):
    '''
    class that handles the scanning of a barcode
    '''
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        #Img element
        self.image = Image()
        self.add_widget(self.image)

        #Video Capture
        self.capture = cv2.VideoCapture(0)
        self.frames_per_sec = 1.0/30.0

        #Limit on camera open
        self.startTime =  time.time()

        self.clock = None
        self.food_item = None

    def schedule_video(self):
        '''
        Every time the Scan Barcode page is opened, the video will load at a 
        determined amout of frames per second by calling the load_video method,
        and thereby start recording
        '''
        self.clock = Clock.schedule_interval(self.load_video, self.frames_per_sec)

    def unschedule_video(self):
        '''
        Makes sure than when switching screens the video is off and the camera
        is not actively looking for a barcode
        '''
        print("unschedule_video")
        if self.clock == None:
            return
        else:
            Clock.unschedule(self.clock)
            self.clock = None

    def decode_barcode(self,barcodes):
        '''Tries to find the data from a barcode'''
        for barcode in barcodes:
            bc = (barcode.data)
            #bc = re.findall("\d+", str(bc))
            bc = ("".join(filter(str.isdigit, str(bc))))
            print("BARCODE: ",bc)
            return bc

    def load_video(self, *args):
        '''
        Every frames/sec this method will be called and a picture will be taken.
        This picture will be updated to the screen and used to determine if a barcode
        was present. If a barcode was found, the camera will stop recording and the barcode´s 
        information will be scrapped from an external database

        Note that this method uses the functions created in the files found in the barcode folder
        '''
        ## TIME LIMIT OF 1 MINUTE TO FIND BARCODE
        timeElapsed = int (time.time() - self.startTime)
        if (timeElapsed > 60):
            Clock.unschedule(self.clock)
            #self.parent.parent.parent.current = "main_screen"
            return -1

        ## READ IMG
        success,frame = self.capture.read()
        ## Find barcodes and send it to be deocded
        if success:
            barcodes = zbar.decode(frame)
            if barcodes != []:
                #send it to be decoded
                decoded_bar = self.decode_barcode(barcodes)
                self.food_item = web_scrapping(decoded_bar)
                print("FOOD ITEM",self.food_item)

                #Stop using video and go back to main page
                Clock.unschedule(self.clock)
                self.clock = None
                return self.food_item

            ## Load new picture to video
            self.img = frame
            buffer = cv2.flip(frame,0).tostring()
            texture = Texture.create(size=(frame.shape[1],frame.shape[0]),colorfmt='bgr')
            texture.blit_buffer(buffer,colorfmt='bgr',bufferfmt='ubyte')
            self.image.texture = texture
        else: 
            print("CAMERA ERRROR")

# NAVIGATION DRAWER = MAIN 
class ContentNavigationDrawer(BoxLayout):
    '''
    No need to be implemented, it is a placeholder to link .kv 
    file with this .py file
    '''
    pass

class WindowManager(ScreenManager):
    '''
    No need to be implemented, it is a placeholder to link .kv 
    file with this .py file. It is a window manager to manage
    switching between sceens.
    '''
    pass


#CHAT SCREEN
class Message(MDBoxLayout):
    content = StringProperty()
    user = StringProperty()

class ChatScreen(Screen):
    '''A screen that display messages with a user.'''
    text = StringProperty()
    image = ObjectProperty()
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def process_message(self,message):
        if("scan barcode" in message.lower()):
            self.parent.screens[1].ids.camera.schedule_video()
            self.parent.switch_to(self.parent.screens[1])

        elif ("show instructions" in message.lower()):
            self.parent.switch_to(self.parent.screens[3])

        elif("scan document" in message.lower()):
            self.parent.switch_to(self.parent.screens[2])
        

    def get_audio(self,*args):  
        print("LISTENING")
        txt = get_command()
        print("MESSAGE: ", txt)
        if (txt != None):
            self.msg = Message()
            self.msg.content = txt
            self.msg.user = "you"
            self.ids["msglist"].add_widget(self.msg)
            self.process_message(txt)

    def send_message(self,*args):
        
        msg = self.ids["txtfield"].ids["textinput"]

        if (msg.text):
            self.msg = Message()
            self.msg.content = msg.text
            self.msg.user = "you"
            self.ids["msglist"].add_widget(self.msg)

        #process message sent 
        self.process_message(msg.text)

        #replace placeholdren 
        msg.text = ""
        msg.hint_text="Type a message"

        #update user chat storage


#MAIN APP
class MainApp(MDApp):

    def build(self):
        screen = Builder.load_file("Screens/main.kv")
        self.manager = screen.ids["screen_manager"]
        self.nav_drawer = screen.ids["nav_drawer"]
        self.user_chat = user_chat

        #call function to update
        self.load_past_msg()
        return screen

    def load_past_msg(self):
        '''
        It gets the messages found in the list in demo_users/user.py
        and displays then in the chat screen by turning them into Message 
        objects
        '''
        screen = self.manager.screens[0]
        for messages in user_chat:
            old_msg,user = messages.split(";")
            self.msg = Message()
            self.msg.content = old_msg
            self.msg.user = user
            #add it to the list of messages
            screen.ids["msglist"].add_widget(self.msg)


MainApp().run()