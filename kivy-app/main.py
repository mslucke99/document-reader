from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.app import App
from kivymd.app import MDApp

#MOBILE PHONE SIZE - for development 
from kivy.core.window import Window
Window.size = (300,500)

## TOOLBAR IMPORTS
from kivy.lang import Builder




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
    Widget:
        id:proxy
        Camera:
            id:camera
            play:True
            resolution: root.resolution
            allow_stretch: True
            keep_ratio: True
  
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
                        id: proxy
                   
                        

        MDNavigationDrawer:
            id: nav_drawer
            ContentNavigationDrawer:
                id: content_drawer
                screen_manager: screen_manager
                nav_drawer:nav_drawer
                
"""



#IMPORTS FRO NAVIGATION DRAWER
from kivy.properties import StringProperty, ListProperty
from kivymd.uix.list import OneLineIconListItem
from kivy.properties import ObjectProperty
from kivymd.uix.list import MDList
from kivymd.theming import ThemableBehavior
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.uix.anchorlayout import AnchorLayout

import time



class ZBarCam(AnchorLayout):
    resolution = ListProperty([640, 480])
    def _setup(self):
        camera = self.ids['camera']
        camera.play = True
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")



# NAVIGATION DRAWER = MAIN 
class ContentNavigationDrawer(BoxLayout):
    pass

class MyApp(MDApp):
    def build(self):
        screen = Builder.load_string(navigation_helper)
        return screen

if __name__ == '__main__':
    MyApp().run()