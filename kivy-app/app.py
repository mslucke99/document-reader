#Imports kivy functionalities
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.clock import Clock

#Import for barcode decoder
import time
import cv2
import pyzbar.pyzbar as zbar

#Import food item Objects and web scraping functions
from barcode.foodObjects import *
from barcode.webScraping import web_scrapping

#MOBILE PHONE SIZE - for development 
from kivy.core.window import Window
Window.size = (300,500)

navigation_helper = """

<ContentNavigationDrawer>:
    orientation:'vertical'
    padding: "8dp"
    spacing: "8dp"

    ScrollView:
        MDList:
            OneLineIconListItem:
                text: "Instructions"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "instructions_screen"
                IconLeftWidget:
                    icon: 'star'
                    theme_text_color: "Custom"

            OneLineIconListItem:
                text: "Scan Document"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "document_screen"
                IconLeftWidget:
                    icon: 'folder'
                    theme_text_color: "Custom"

            OneLineIconListItem:
                text: "Scan Food Item"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "barcode_screen"
                IconLeftWidget:
                    icon: 'barcode'
                    theme_text_color: "Custom"

<ZBarCam>:
    size: root.width, root.height
    orientation:'vertical'
    Image:
        width: 100
        allow_stretch: True

Screen:
    MDNavigationLayout:

        ScreenManager:
            id: screen_manager
            Screen:
                name: "main_screen"
                BoxLayout:
                    orientation: 'vertical'
                    MDToolbar:
                        title: "Navigation Drawer"
                        elevation: 10
                        left_action_items: [['menu', lambda x: nav_drawer.set_state('toggle')]]
                    Widget:

            Screen:
                name: 'instructions_screen'
                BoxLayout:
                    orientation: 'vertical'
                    MDToolbar:
                        title: "App Instructions"
                        elevation: 10
                        left_action_items: [['menu', lambda x: nav_drawer.set_state('toggle')]]
                    Widget:


            Screen:
                name: 'document_screen'
                BoxLayout:
                    orientation: 'vertical'
                    MDToolbar:
                        title: "Document Scanner"
                        elevation: 10
                        left_action_items: [['menu', lambda x: nav_drawer.set_state('toggle')]]
                    Widget:

            Screen:
                name: 'barcode_screen'
                BoxLayout:
                    orientation: 'vertical'
                    MDToolbar:
                        title: "Barcode Scanner"
                        elevation: 10
                        left_action_items: [['menu', lambda x: nav_drawer.set_state('toggle')]]
                    ZBarCam:
                   
                        

        MDNavigationDrawer:
            id: nav_drawer
            ContentNavigationDrawer:
                id: content_drawer
                screen_manager: screen_manager
                nav_drawer:nav_drawer
                
"""


# BARCODE CAMERA 
class ZBarCam(MDBoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        #Img element
        self.image = Image()
        self.add_widget(self.image)

        #Video Capture
        self.capture = cv2.VideoCapture(0)
        frames_per_sec = 1.0/30.0

        #Limit on camera open
        self.startTime =  time.time()

        #Update image every frames/sec
        self.clock = Clock.schedule_interval(self.load_video, frames_per_sec)

    def decode_barcode(self,barcodes):
        for barcode in barcodes:
            bc = (barcode.data)
            #bc = re.findall("\d+", str(bc))
            bc = ("".join(filter(str.isdigit, str(bc))))
            return bc

    def load_video(self, *args):
        ## TIME LIMIT OF 1 MINUTE TO FIND BARCODE
        timeElapsed = int (time.time() - self.startTime)
        if (timeElapsed > 60):
            Clock.unschedule(self.clock)
            self.parent.parent.parent.current = "main_screen"
            return -1

        ## READ IMG
        success,frame = self.capture.read()

        ## Find barcodes and send it to be deocded
        if success:
            barcodes = zbar.decode(frame)
            if barcodes != []:
                #send it to be decoded
                decoded_bar = self.decode_barcode(barcodes)
                food_item = web_scrapping(decoded_bar)
                print(food_item)

                #Stop using video and go back to main page
                Clock.unschedule(self.clock)
                self.parent.parent.parent.current = "main_screen"
                return food_item

        ## Load new picture to video
        self.img = frame
        buffer = cv2.flip(frame,0).tostring()
        texture = Texture.create(size=(frame.shape[1],frame.shape[0]),colorfmt='bgr')
        texture.blit_buffer(buffer,colorfmt='bgr',bufferfmt='ubyte')
        self.image.texture = texture


# NAVIGATION DRAWER = MAIN 
class ContentNavigationDrawer(BoxLayout):
    pass

class MyApp(MDApp):
    def build(self):
        screen = Builder.load_string(navigation_helper)
        return screen

if __name__ == '__main__':
    MyApp().run()