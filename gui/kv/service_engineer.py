# from kivymd.tools.hotreload.app import MDApp   # hotreload-app
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.factory import Factory
import os

#
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import BooleanProperty, StringProperty , ListProperty , DictProperty
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.pickers import MDColorPicker
from typing import Union
import threading
from kivymd.uix.card import MDCard
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.list import TwoLineAvatarIconListItem , IconLeftWidget, IconRightWidget
# from kivymd.uix.textfield.textfield #import MDTextField
# kivy_garden

# from kivymd.app import MDApp

from kivy_garden.mapview import MapView
from os import path
import sys

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))




KV_DIR = os.path.join(os.path.dirname(__file__), "kv")

class CustomTwoLineAvatarIconListItem(TwoLineAvatarIconListItem):
    icon_left = StringProperty('android')
    icon_right = StringProperty('android')

class CustomRecycleView(MDRecycleView):
    pass 

class MainApp(MDApp):
    ##
    images = [
"https://images.pexels.com/photos/3389613/pexels-photo-3389613.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
]
    image_list = ListProperty(images)
    email = StringProperty()
    phone = StringProperty()
    last_screen = StringProperty()

    # engineer
    is_logged_in = BooleanProperty(False)
    mapsource = [22.5626, 88.363]
    totalearnings = StringProperty('200k')
    complaints_list = ListProperty([
        {'icon_left': 'alert-circle-outline','icon_right': 'chevron-right' ,'text': 'Complaint 1', 'secondary_text': 'Complaint 1 description'},
        {'icon_left': 'alert-circle-outline','icon_right': 'chevron-right' ,'text': 'Complaint 2', 'secondary_text': 'Complaint 2 description'},

       ] )
    up = [
		{'icon_left': 'alert-circle-outline', 'icon_right': 'chevron-right', 'text': 'Complaint 3', 'secondary_text': 'Complaint 3 description'},
		{'icon_left': 'alert-circle-outline', 'icon_right': 'chevron-right', 'text': 'Complaint 4', 'secondary_text': 'Complaint 4 description'},
        {'icon_left': 'alert-circle-outline', 'icon_right': 'chevron-right', 'text': 'Complaint 5', 'secondary_text': 'Complaint 5 description'},
        {'icon_left': 'alert-circle-outline', 'icon_right': 'chevron-right', 'text': 'Complaint 6', 'secondary_text': 'Complaint 6 description'},
	]
    

    # def build_app(self):  # hotreload-build
    def build(self):

        self._init_loading_widget()
        self.theme_cls.theme_style = "Light"
        return Builder.load_file('kv/engineer.kv')
    def on_start(self):
        self.clear_card()
        self.root.get_screen('engineer').ids.recycle_view.data = self.complaints_list
        print(self.root.get_screen('engineer').ids)
    
    def clear_card(self):
        if not app.is_logged_in:
            card = self.root.get_screen('engineer').ids
            # clear the card
            card.job_address.text = 'N/A'
            card.job_customer.text = 'N/A'
            card.job_service.text = 'N/A'
            card.job_time.text = 'N/A'

    def update(self):
        self.root.get_screen('engineer').ids.recycle_view.data = self.up
        print('updated')

    def _init_loading_widget(self):
        ''' Initialize the loading widget '''
        # init the modal view
        from kivy.uix.modalview import ModalView
        from kivymd.uix.spinner import MDSpinner
        global _modal
        _modal  =   ModalView(size_hint=(.8, .8), auto_dismiss=False, background='', background_color=[0, 0, 0, 0])
        _modal.add_widget(MDSpinner(line_width=dp(5.25), size_hint=(None, None), size=(120, 120), pos_hint={'center_x': .5, 'center_y': .5}, active=True))  # Load and play the GIF
    
app = MainApp()
app.run()
