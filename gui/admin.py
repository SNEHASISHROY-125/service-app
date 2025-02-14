import threading
import gc
from kivy.clock import Clock
from kivymd.toast import toast
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar
# from kivymd.uix.bottomnavigation.bottomnavigation
import random
from kivymd.uix.fitimage import FitImage
from kivymd.uix.list import TwoLineAvatarIconListItem , IconLeftWidget , IconRightWidget
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty

# from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarListItem
from kivy.properties import BooleanProperty, ObjectProperty

from kivy.config import Config
Config.set('kivy', 'pause_on_minimize', '1')

from kivymd.toast import toast as tst
from kivy.utils import platform

def toast(text:str, duration=1.0):
    if platform == 'android':
        tst(text, duration)
    else:
        tst(text, duration=duration)

'''
admin dashboard
'''
source_ = random.choice(
    [
        "https://images.news18.com/ibnlive/uploads/2024/05/untitled-design-2024-05-06t172011.884-2024-05-346a6a8bc708ce85866cf99c6560cdeb.jpg?impolicy=website&width=360&height=270",
        "https://wp.inews.co.uk/wp-content/uploads/2024/10/comp-1730130269.png?resize=640,360&strip=all&quality=90",
        "https://media1.popsugar-assets.com/files/thumbor/ZBYCnxskaB7r0JZR6fgIlE8hLTA=/fit-in/1584x1056/top/filters:format_auto():upscale()/2024/11/05/759/n/1922441/tmp_s9n0N8_b15ab770b39bdf02_GettyImages-2114215250.jpg"
    ]
)

KV = '''
MDScreenManager:
    AdminDashboardScreen:

<Item>

    ImageLeftWidget:
        source: root.source

<TwoLineAvatarIconListItem>
    complaint_id: root.complaint_id


<AdminDashboardScreen@MDScreen>:
    name: "admin_dashboard"

    BoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "Admin Dashboard"
            pos_hint: {"top": 1}

        MDBottomNavigation:
            on_switch_tabs: print(999)
            MDBottomNavigationItem:
                name: 'screen 1'
                text: 'service engineers'
                icon: "face-agent"

                MDScreen:
                    FitImage:
                        size_hint: 1, 1
                        pos_hint: {"center_x": .5, "center_y": .5}
                        source: "{}".format(app.s_)
                        opacity: .4
                        #radius: dp(24)

                    RefreshScrollView: 
                        do_scroll_x: False
                        
                        MDBoxLayout:
                            orientation: 'vertical'
                            size_hint: 1, None
                            
                            height: self.minimum_height
                            size_hint_y: None

                            MDList:
                                id: engineers_list

                                TwoLineAvatarIconListItem:
                                    text: "Two-line item with avatar"
                                    theme_text_color: "Custom"
                                    text_color: app.theme_cls.primary_color
                                    secondary_text: "Secondary text here"

                                    IconLeftWidget:
                                        icon: "clock"

                                    IconRightWidget:
                                        icon: "chevron-right"
                                
                                TwoLineAvatarIconListItem:
                                    text: "Two-line item with avatar"
                                    secondary_text: "Secondary text here"

                                    IconLeftWidget:
                                        icon: "close-circle-outline"

                                    IconRightWidget:
                                        icon: "chevron-right"
                            
                    MDFloatingActionButton:
                        icon: "plus"
                        pos_hint: {"center_x": .7, "center_y": .1}
                        on_release: app.add_engineer()


            MDBottomNavigationItem:
                name: 'screen 2'
                text: 'complaints'
                icon: 'gmail'

                MDScreen:
                   
                    FitImage:
                        size_hint: 1, 1
                        pos_hint: {"center_x": .5, "center_y": .5}
                        source: "{}".format(app.s_)
                        opacity: .4
                        #radius: dp(24)

                    RefreshScrollView_Complaints:
                        do_scroll_x: False
                        MDList:
                            id: complaints_list

                            TwoLineAvatarIconListItem:
                                text: "Two-line item with avatar"
                                theme_text_color: "Custom"
                                text_color: app.theme_cls.primary_color
                                secondary_text: "Secondary text here"

                                IconLeftWidget:
                                    icon: "clock"

                                IconRightWidget:
                                    icon: "chevron-right"
                            
                            TwoLineAvatarIconListItem:
                                text: "Two-line item with avatar"
                                secondary_text: "Secondary text here"

                                IconLeftWidget:
                                    icon: "close-circle-outline"

                                IconRightWidget:
                                    icon: "chevron-right"
'''

global server_url
server_url = "https://chat-app.fudemy.me/" # server url

class Item(OneLineAvatarListItem):
    # divider = None
    source = StringProperty()

class TwoLineAvatarIconListItem(TwoLineAvatarIconListItem):
    # divider = None
    source = StringProperty()
    complaint_id = StringProperty()

class PullToRefreshBehavior:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._start_touch_y = None

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self._start_touch_y = touch.y
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self._start_touch_y and self._start_touch_y - touch.y > 350:
        # if self._start_touch_y and touch.y - self._start_touch_y > 150:  # Adjust the threshold as needed
            self.refresh()
        self._start_touch_y = None
        return super().on_touch_up(touch)

    def refresh(self):
        print("Pulled down to refresh!")
        # Add your refresh logic here

global _APP

class RefreshScrollView(PullToRefreshBehavior, ScrollView):
    refreshing = BooleanProperty(False)
    spinner = ObjectProperty(None)
    global _modal
    global _APP

    def refresh(self):
        print("Pulled down to refresh!")
        _modal.open()
        # Add your refresh logic here
        Clock.schedule_once(_APP.refresh_engineers, .3)  # Simulate a delay
        # threading.Thread(target=self.run_background_task).start()  # Run the background task in a separate thread

    def run_background_task(self):
        try:
            _APP.render_engineers()
        except Exception as e:
            print(e)

class RefreshScrollView_Complaints(PullToRefreshBehavior, ScrollView):
    refreshing = BooleanProperty(False)
    spinner = ObjectProperty(None)
    global _modal
    global _APP

    def refresh(self):
        print("Pulled down to refresh!")
        _modal.open()
        # Add your refresh logic here
        Clock.schedule_once(_APP.render_complaints, .3)  # Simulate a delay
        # threading.Thread(target=self.run_background_task).start()  # Run the background task in a separate thread

import time, requests

class AdminDashboardApp(MDApp):
    s_ = source_
    dialog = None
    _dialog = None
    global _modal_issue
    _modal_issue = None
    global _modal_confirm

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "A700" 
        return Builder.load_string(KV)
    
    def _init_loading_widget(self):
        ''' Initialize the loading widget '''
        # init the modal view
        from kivy.uix.modalview import ModalView
        from kivymd.uix.spinner import MDSpinner
        global _modal
        _modal  =   ModalView(size_hint=(.5, .5), auto_dismiss=False, background='', background_color=[0, 0, 0, 0])
        _modal.add_widget(MDSpinner(size_hint=(None, None), size=(46, 46), pos_hint={'center_x': .5, 'center_y': .5},active=True))  # Load and play the GIF
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # modal
        # global _modal_issue
        # # _modal_issue  =   ModalView(size_hint=(.5, .5), auto_dismiss=True, background='', background_color=[1, 1, 1, .5],border=[20,0,0,20])
        # _modal_issue = MDDialog(
        #         title="Set backup account",
        #         type="custom",
        #         content_cls=MDBoxLayout(
        #             MDTextField(
        #                 hint_text="",
        #             ),
        #             orientation="vertical",
        #             spacing="12dp",
        #             size_hint_y=None,
        #             height="120dp",
        #         ),
        #         buttons=[
        #             MDFlatButton(
        #                 text="CANCEL",
        #                 theme_text_color="Custom",
        #                 text_color=self.theme_cls.primary_color,
        #                 on_release=lambda x: _modal_issue.dismiss()
        #             ),
        #             MDFlatButton(
        #                 text="OK",
        #                 theme_text_color="Custom",
        #                 text_color=self.theme_cls.primary_color,
                 
        #             ),
        #         ],
        #     )
        def on_pre_dismiss(instance):
            # _modal.remove_widget(image)
            _modal_issue.clear_widgets()
        
        # _modal_issue.bind(on_pre_dismiss=on_pre_dismiss)

    
    def render_complaints(self, *args):
        # self.root.ids.refresh_scroll.refreshing = False
        # self.root.ids.refresh_scroll.spinner.active = False  # Stop the spinner
        # self.root.ids.refresh_scroll.spinner.opacity = 0  # Hide the spinner
        # make query to get all engineers
        def _query():
            import requests
            from kivy.clock import Clock
            from kivymd.toast import toast
            import time
            server_url = "http://chat-app.fudemy.me/"
            global _complaints
            try:
                print(server_url)
                time.sleep(1) # simulate a delay | blocks main thread
                _complaints = requests.get(url=server_url+"get_all", params={"table_name": "issues"}).json()
                print(_complaints)
            except Exception as e:
                Clock.schedule_once(lambda dt: toast('You are offlline',1),0.5)
                Clock.schedule_once(lambda dt: _modal.dismiss() ,1)
                return
            # if response contains issues ->
            if _complaints:
                Clock.schedule_once(lambda x:_add_complaints(), 0.1)
        def _add_complaints():
            global _modal
            global _dialog
            def not_none(x): 
                    if not x :
                        print(x)
                        return 'not-availale'
                    else: return x

            def _close_complaint(_instance,_complaint_id,_code):
                global _modal
                Clock.schedule_once(lambda x:_modal.open(),0.1)
                _modal_issue.dismiss()
                print('from CLOSE-COMPLAINT ',_instance,_complaint_id,_code)
                # print(_modal_issue.children[0].children[0].children[0].children[0].text)
                def _query():
                    server_url = "http://chat-app.fudemy.me/"
                    global _complaints
                    try:
                        print(server_url)
                        time.sleep(1) # simulate a delay | blocks main thread
                        _complaints = requests.delete(url=server_url+f"close_complaint/{_complaint_id}", params={"code": _code}).json()
                        print(_complaints)
                    except Exception as e:
                        Clock.schedule_once(lambda dt: toast('You are offlline', 1),0.5)
                        Clock.schedule_once(lambda dt: _modal.dismiss() ,1)
                        return
                    _modal.dismiss()
                    try:
                        # if response contains issues ->
                        if _complaints["code"] == "success": 
                            Clock.schedule_once(lambda dt: toast('complaint closed',1),0.5)
                            # refresh the complaints
                            self.render_complaints()
                            # Clock.schedule_once(lambda x:_add_complaints(), 0.1)
                        elif _complaints["detail"] == "Complaint not found":
                            Clock.schedule_once(lambda dt: toast("Complaint not found" , 1), 0.5)
                    except Exception as e:
                        print(e)
                        Clock.schedule_once(lambda dt: toast("Error closing complaint" , 1), 0.5)
                threading.Thread(target=_query).start()
            
            def _show_dialog(_issue_data):
                self._dialog.title = f"Complaint {_issue_data['complaintid']}"
                _items_list = self._dialog.children[0].children[2].children[0].children
                print(self._dialog.children[0].children[2].children[0].children[0].source)
                _payments_receipt = _items_list[0]
                _payments_receipt.source = "https://img.icons8.com/stickers/50/cash-in-hand.png"
                _location = _items_list[1]
                _location.source = "https://img.icons8.com/arcade/64/marker.png"
                _esttime = _items_list[2]
                _esttime.source = "https://img.icons8.com/external-flaticons-flat-flat-icons/64/external-time-100-most-used-icons-flaticons-flat-flat-icons-2.png"
                _user_id = _items_list[3]
                _user_id.source = "https://img.icons8.com/cotton/100/guest-male.png"
                _phone = _items_list[4]
                _phone.source = "https://img.icons8.com/pulsar-gradient/48/ringer-volume.png"
                _name = _items_list[5]
                _name.source = "https://img.icons8.com/3d-fluency/94/worker-male--v1.png"
                _status = _items_list[6]
                _complaintid = _items_list[7]
                _complaintid.source = "https://img.icons8.com/emoji/48/id-button-emoji.png" # "https://img.icons8.com/pulsar-color/48/instagram-verification-badge.png"
                _issue = _items_list[8]
                _issue.source = "https://img.icons8.com/external-gradients-pongsakorn-tan/64/external-audit-gdpr-gradients-pongsakorn-tan.png"
                #  set status icon
                _status.source="https://img.icons8.com/3d-fluency/94/sand-clock-1.png" if _issue_data['status'] == 'open' else "https://img.icons8.com/color/240/ok--v1.png" if _issue_data['status'] == 'closed' else "https://img.icons8.com/keek/100/delete-sign.png"
                # set values
                _payments_receipt.text = not_none(str(_issue_data['payments_receipt']))
                _location.text = not_none(_issue_data['location'])
                _esttime.text = not_none(_issue_data['esttime'])
                _user_id.text = not_none(_issue_data['user_id'])
                _phone.text = not_none(str(_issue_data['phone']))
                _name.text = not_none(_issue_data['name'])
                _status.text = not_none(_issue_data['status'])
                _complaintid.text = not_none(str(_issue_data['complaintid']))
                _issue.text = not_none(_issue_data['issue'])
                # print(_payments_receipt,'\n',_location.text,'\n',_esttime,'\n',_user_id,'\n',_phone,'\n',_name,'\n',_status,'\n',_complaintid,'\n',_issue)
                # release resorces
                for i in [_payments_receipt, _location, _esttime, _user_id, _phone, _name, _status, _complaintid, _issue]:
                    i = None
                    # i = None
                # print(_dialog.children[0].children[2].children[0].children[1].text)
                self._dialog.open()
            # 
            engineers_list = self.root.get_screen("admin_dashboard").ids.complaints_list
            print(engineers_list.children)
            #
            # engineers_list.clear_widgets()
            # print(engineers_list.children)
            # Logic to match list items with the engineers
            if len(engineers_list.children) < len(_complaints['data']):
                for i in range(len(_complaints['data']) - len(engineers_list.children)):
                    engineers_list.add_widget(TwoLineAvatarIconListItem(
                        IconLeftWidget(
                        ),
                        IconRightWidget(
                        ),
                        text="Two-line item with avatar",secondary_text="Secondary text here",theme_text_color="Custom",text_color=self.theme_cls.primary_color
                        )
                    )
                    print('added new to list')

            for i in engineers_list.children:
                index = engineers_list.children.index(i)
                print(index)
                i.theme_text_color = "Custom"
                i.text_color = self.theme_cls.primary_color
                print(_complaints['data'][index])
                i.text = _complaints['data'][index]['issue']
                i.secondary_text = str(_complaints['data'][index]['complaintid'])

                rightwidget = i.children[0].children
                rightwidget[0].icon = "chevron-right"
                rightwidget[0].theme_text_color = "Custom"
                rightwidget[0].text_color = self.theme_cls.primary_color
                rightwidget[0].on_release = lambda data=_complaints['data'][index]: _show_dialog(data)

                leftwidget = i.children[1].children
                leftwidget[0].icon = "clock" if _complaints['data'][index]['status'] == 'open' else "check-circle-outline" if _complaints['data'][index]['status'] == 'closed' else "close-circle-outline"
                global _modal_issue
                #
                # _instance = i
                # _complaint_id = _complaints['data'][index]['complaintid']
                # _code = _modal_issue.content_cls.children[0].text if _modal_issue.content_cls.children[0].text else 'CANCELED'
                i.complaint_id = _complaints['data'][index]['complaintid']
                # _modal_issue.buttons[1].on_release = lambda _instance=i, complaint_id=_complaints['data'][index]['complaintid'], _code=_modal_issue.content_cls.children[0].text if _modal_issue.content_cls.children[0].text else 'CANCELED': _close_complaint(_instance, complaint_id, _code)
                leftwidget[0].on_release = lambda _instance=i,_issue=_complaints['data'][index]['issue'] : open_modal_issue(_instance,_issue=_issue)

                def open_modal_issue(_instance,_issue):
                    # _modal_issue.children[0].children[0].children[0].children[0].on_release = lambda index=i.index:print(index)
                    _modal_issue.title = f'Do you want to close the complaint ?\n{_issue[:20]}...'
                    _modal_issue.children[0].children[0].children[0].children[0].on_release = lambda _instance=_instance, _complaint_id=_instance.complaint_id, : _close_complaint(_instance=_instance, _complaint_id=_complaint_id, _code=_modal_issue.content_cls.children[0].text if _modal_issue.content_cls.children[0].text else 'CANCELED')
                    _modal_issue.open()

            #     engineers_list.add_widget(OneLineListItem(text=f"Item {i}"))

            _modal.dismiss()
        # _query()
        Clock.schedule_once(lambda x:threading.Thread(target=_query).start(),0.5)

    # def render_engineers(self):
    #     # self.root.get_screen("admin_dashboard").ids.engineers_list
    #     def _query():
    #         import requests
    #         from kivy.clock import Clock
    #         from kivymd.toast import toast
    #         global _engineers
    #         try:
    #             _engineers = requests.get(url=server_url+"get_all", params={"table_name": "service_engineers"}).json()
    #             print(_engineers)
    #         except Exception as e:
    #             Clock.schedule_once(lambda dt: toast('You are offlline'),0.5)
    #             Clock.schedule_once(lambda dt: _modal.dismiss() ,1)
    #             return
    #         # if response contains issues ->
    #         if _engineers:
    #             Clock.schedule_once(_add_complaints, 0.1)


    #     def _add_complaints(dt):
    #         # appointments = _appointments_data
    #         # the root MDList to add appointments to
    #         global _engineers
    #         global _modal
    #         def bind_list_item(x):
    #             # print(x.text)
    #             # scroll_view = ScrollView(
    #             #     do_scroll_x= False
    #             #     )
    #             # list_item = TwoLineAvatarIconListItem(text=x['issue'], secondary_text=x['complaintid'])
    #             # scroll_view.add_widget(list_item)
    #             # _modal_issue.add_widget(scroll_view)

    #             def not_none(x): 
    #                 if not x :
    #                     print(x)
    #                     return 'not-availale'
    #                 else: return x
    #             # dialog
    #             m_  =   MDDialog(
    #                 title=x['status'],
    #                 type="simple",
    #                 items=[
    #                     Item(text=not_none(x['issue']), theme_text_color="Custom", text_color=self.theme_cls.primary_color, source="https://cdn.iconscout.com/icon/free/png-256/doctor-1851563-1569282.png"),
    #                     Item(text=not_none(x['complaintid']), theme_text_color="Custom", text_color=self.theme_cls.primary_color, source="https://cdn.iconscout.com/icon/free/png-256/doctor-1851563-1569282.png"),
    #                     Item(text=not_none(x['status']), theme_text_color="Custom", text_color=self.theme_cls.primary_color, source="https://img.icons8.com/color/240/ok--v1.png"),
    #                     Item(text=not_none(x['name']), theme_text_color="Custom", text_color=self.theme_cls.primary_color, source="https://cdn.iconscout.com/icon/free/png-256/doctor-1851563-1569282.png"),
    #                     Item(text=not_none(str(x['phone'])), theme_text_color="Custom", text_color=self.theme_cls.primary_color, source="https://cdn.iconscout.com/icon/free/png-256/doctor-1851563-1569282.png"),
    #                     Item(text=not_none(x['user_id']), theme_text_color="Custom", text_color=self.theme_cls.primary_color, source="https://cdn.iconscout.com/icon/free/png-256/doctor-1851563-1569282.png"),
    #                     Item(text=not_none(x['esttime']), theme_text_color="Custom", text_color=self.theme_cls.primary_color, source="https://cdn.iconscout.com/icon/free/png-256/doctor-1851563-1569282.png"),
    #                     Item(text=not_none(x['location']), theme_text_color="Custom", text_color=self.theme_cls.primary_color, source="https://cdn.iconscout.com/icon/free/png-256/doctor-1851563-1569282.png"),
    #                     Item(text=not_none(x['payments_receipt']), theme_text_color="Custom", text_color=self.theme_cls.primary_color, source="https://cdn.iconscout.com/icon/free/png-256/doctor-1851563-1569282.png"),
    #                 ],
    #                 buttons=[
    #                     MDFlatButton(
    #                         text="CLOSE",
    #                         theme_text_color="Custom",
    #                         text_color=self.theme_cls.primary_color,
    #                         on_release=lambda x: m_.dismiss()
    #                     ),
    #                 ],
    #             )
                
    #             #
    #             global _modal
    #             m_.bind(on_open=lambda x:_modal.dismiss())
    #             m_.bind(on_pre_dismiss=lambda x : m_.clear_widgets())
    #             # m_.bind(on_pre_dismiss=lambda x: clr(m=m_))
    #             m_.open()

    #         appointments_list = self.root.get_screen("admin_dashboard").ids.engineers_list
    #         # appointments = {'complaint-id': '#56608' ,'attd-name': 'NAME_', 'time': '12:00 PM', 'status': 'pending'}
    #         # remove all widgets from the list
    #         appointments_list.clear_widgets()
    #         self.clear_widgets(appointments_list)  # Clear existing items

    #         ## 
    #         global _issue_widget_list
    #         _issue_widget_list = [] 
    #         for i in _engineers['data']:
    #             print(i)
    #             # icon
    #             if i['availability'] == True: icon_ = "home"
    #             elif i['availability'] == False: icon_ = "briefcase"
    #             else: icon_ = "home"
    #             # elif i['status'] == 'canceled': icon_ = "close-circle-outline"
    #             icon = "account-hard-hat"
    #             _issue_widget = TwoLineAvatarIconListItem(
    #                     IconLeftWidget(
    #                         icon=icon,

    #                         theme_text_color="Custom",
    #                         text_color='green' if i['availability'] else 'orange'
    #                     ),
    #                     IconRightWidget(
    #                         icon=icon_,
    #                         theme_text_color="Custom",
    #                         text_color= 'green' if i['availability'] else 'orange',
    #                         on_press=lambda x: threading.Thread(target=_modal.open()).start(),
    #                         # on_release=lambda x,i=i: bind_list_item(i),
    #                     ),
    #                     text= i['name'],
    #                     secondary_text= str('busy with a complaint' if not i['availability'] else 'available'),
    #                     theme_text_color="Custom",
    #                     text_color = self.theme_cls.primary_color,
    #                 )
    #             # bind the on_press event
    #             _issue_widget.bind(on_release=lambda x: print(x.text,x))
    #             # add the widget to the list
    #             appointments_list.add_widget(_issue_widget, index=0)
    #             # relese-resources
    #             # _issue_widget.clear_widgets()
    #             _issue_widget_list.append(_issue_widget)
    #             _issue_widget = None
            
    #         # relese-resources
    #         appointments_list = None
    #         print(_issue_widget_list, len(_issue_widget_list) , len(_engineers['data']))
    #         # Force garbage collection
    #         gc.collect()    
    #         # print("Appointments added\n",res_,phone_)
    #         Clock.schedule_once(lambda dt: _modal.dismiss() ,1)
    #     # 
    #     threading.Thread(target=_query).start()

    def clear_widgets(self, container):
        # Remove widgets from the container
        [container.remove_widget(widget) for widget in container.children[:]]
            
        # Force garbage collection
        gc.collect()

    # add engineers
    def add_engineer(self):
        # dialog
        if not self.dialog:
            self.dialog= MDDialog(
            title="Add Engineer",
            type="custom",
            content_cls=MDBoxLayout(
            MDTextField(
                hint_text="Engineer Name",
                # id="engineer_name"
            ),
            MDBoxLayout(
                MDLabel(
                    text="Set Availability"),
                MDSwitch(
                    # id="availability",
                    # active=True,
                    pos_hint={"center_x": 0.5},
                    ),
                orientation="horizontal",
            ),
            orientation="vertical",
            spacing="12dp",
            size_hint_y=None,
            height="120dp"
            ),
            buttons=[
            MDFlatButton(
                text="CANCEL",
                on_release=lambda x: self.dialog.dismiss()
            ),
            MDFlatButton(
                text="ADD",
                # on_release=self.add_engineer_to_list
                # mdswitch
                # on_release=lambda x: print(self.dialog.children[0].children[2].children[0].children[0].children[0])
                on_release=lambda x: add_engineer_to_list(name_=self.dialog.children[0].children[2].children[0].children[1].text)
            ),
            ],
        )
        self.dialog.open()
        # Force garbage collection
        gc.collect()

        def add_engineer_to_list( name_,*args):
            #
            self.dialog.dismiss()
            import requests
            try:
                _engineers = requests.post(url=server_url+"add_engineer", json={"name": str(name_), "availability": True}).json()
                print(_engineers)
            except Exception as e:
                Clock.schedule_once(lambda dt: toast('You are offlline',1),0.5)
                Clock.schedule_once(lambda dt: _modal.dismiss() ,1)
                return
            
            global _modal
            _modal.open()
            if _engineers['code'] == 'success':
                Clock.schedule_once(lambda dt: toast('engineer added sucessfully',1),0.5)
                # add to the list
                _modal.open()
                Clock.schedule_once(self.refresh_engineers, .3)  # Simulate a delay
                # self.refresh_engineers()

    def on_start(self):
        self._init_loading_widget()
        # 1
        _modal.open()
        Clock.schedule_once(self.refresh_engineers, .1)  # Simulate a delay
        # 4
        global _modal_issue
        # _modal_issue  =   ModalView(size_hint=(.5, .5), auto_dismiss=True, background='', background_color=[1, 1, 1, .5],border=[20,0,0,20])
        _modal_issue = MDDialog(
                title="Set backup account",
                type="custom",
                content_cls=MDBoxLayout(
                    MDTextField(
                        hint_text="",
                    ),
                    orientation="vertical",
                    spacing="12dp",
                    size_hint_y=None,
                    height="120dp",
                ),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: _modal_issue.dismiss()
                    ),
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        
                    ),
                ],
            )
        # 2
        _modal.open()
        self.render_complaints()
        # 3
        self._dialog = MDDialog(
                    title='status',
                    type="simple",
                    items=[
                        Item(text='issue', theme_text_color="Custom", text_color=self.theme_cls.primary_color, source="https://cdn.iconscout.com/icon/free/png-256/doctor-1851563-1569282.png"),
                        Item(text='complaintid', theme_text_color="Custom", text_color=self.theme_cls.primary_color, source="https://cdn.iconscout.com/icon/free/png-256/doctor-1851563-1569282.png"),
                        Item(text='status', theme_text_color="Custom", text_color=self.theme_cls.primary_color, source="https://img.icons8.com/color/240/ok--v1.png"),
                        Item(text='name', theme_text_color="Custom", text_color=self.theme_cls.primary_color, source="https://cdn.iconscout.com/icon/free/png-256/doctor-1851563-1569282.png"),
                        Item(text='phone', theme_text_color="Custom", text_color=self.theme_cls.primary_color, source="https://cdn.iconscout.com/icon/free/png-256/doctor-1851563-1569282.png"),
                        Item(text='user_id', theme_text_color="Custom", text_color=self.theme_cls.primary_color, source="https://cdn.iconscout.com/icon/free/png-256/doctor-1851563-1569282.png"),
                        Item(text='esttime', theme_text_color="Custom", text_color=self.theme_cls.primary_color, source="https://cdn.iconscout.com/icon/free/png-256/doctor-1851563-1569282.png"),
                        Item(text='location', theme_text_color="Custom", text_color=self.theme_cls.primary_color, source="https://cdn.iconscout.com/icon/free/png-256/doctor-1851563-1569282.png"),
                        Item(text='payments_receipt', theme_text_color="Custom", text_color=self.theme_cls.primary_color, source="https://cdn.iconscout.com/icon/free/png-256/doctor-1851563-1569282.png"),
                    ],
                    buttons=[
                        MDFlatButton(
                            text="CLOSE",
                            theme_text_color="Custom",
                            text_color=self.theme_cls.primary_color,
                            on_release=lambda x: self._dialog.dismiss()
                        ),
                    ],
                )
        # self._dialog.open()
        # 5
        # bind if the user enters a 6 digit password that matches 869421 then dissmiss the modal
        def validate_password():
            global _modal_confirm
            print(_modal_confirm.content_cls.children[0].text , type(_modal_confirm.content_cls.children[0].text))

            if str(_modal_confirm.content_cls.children[0].text) == str(369421):
                Clock.schedule_once(lambda dt: toast("Login sucess",1),0.1)
                _modal_confirm.dismiss()
            else:
                Clock.schedule_once(lambda dt: toast("Incorrect password",1),0.1)
        global _modal_confirm
        # _modal_issue  =   ModalView(size_hint=(.5, .5), auto_dismiss=True, background='', background_color=[1, 1, 1, .5],border=[20,0,0,20])
        _modal_confirm = MDDialog(
                title='Enter Admin Password',
                type="custom",
                auto_dismiss=False,
                content_cls=MDBoxLayout(
                    MDTextField(
                        hint_text="",
                        max_text_length=6,
                    ),
                    orientation="vertical",
                    spacing="12dp",
                    size_hint_y=None,
                    height="120dp",
                ),
                buttons=[
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: validate_password()
                    ),
                ],
            )
        _modal_confirm.open()
        
        # Force garbage collection
        gc.collect()

    def on_pause(self):
        # Save any necessary state data or suspend operations here.
        return True  # Return True to indicate we’re handling the pause.

    def on_resume(self):
        # Restore any data or state when the app resumes.
        # Force a redraw
        self.root.canvas.ask_update()
    
    def refresh_engineers(self, dt):
        # self.root.ids.refresh_scroll.refreshing = False
        # self.root.ids.refresh_scroll.spinner.active = False  # Stop the spinner
        # self.root.ids.refresh_scroll.spinner.opacity = 0  # Hide the spinner
        # make query to get all engineers
        def _query():
            import requests
            from kivy.clock import Clock
            from kivymd.toast import toast
            import time
            server_url = "http://chat-app.fudemy.me/"
            global _engineers
            try:
                print(server_url)
                time.sleep(1) # simulate a delay | blocks main thread
                _engineers = requests.get(url=server_url+"get_all", params={"table_name": "service_engineers"}).json()
                print(_engineers)
            except Exception as e:
                Clock.schedule_once(lambda dt: toast('You are offlline',1),0.5)
                Clock.schedule_once(lambda dt: _modal.dismiss() ,1)
                return
            # if response contains issues ->
            if _engineers:
                print('from refresh_engineers',_engineers)
                Clock.schedule_once(lambda x:_add_engineers(), 0.1)
        
        def delete_engineer(_name:str,_instance):
            global _modal_issue
            _modal_issue.dismiss()
            global _modal
            Clock.schedule_once(lambda x:_modal.open(),0.1)
            print(_name)
            # clear the list-instance-widget
            _instance.text = ''
            _instance.secondary_text = ''
            _instance.children[0].children[0].icon = ''
            _instance.children[1].children[0].icon = ''
            # unbind the on_release event
            _instance.children[0].children[0].on_release = lambda : None
            _instance.children[1].children[0].on_release = lambda : None
            #
            _instance.parent.remove_widget(_instance)
            # make query to get all engineers
            def _query():
                import requests
                from kivy.clock import Clock
                from kivymd.toast import toast
                import time
                server_url = "http://chat-app.fudemy.me/"
                global _engineers
                try:
                    print(server_url)
                    time.sleep(1) # simulate a delay | blocks main thread
                    _engineers = requests.delete(url=server_url+"delete_engineer", params={"engineer_name": _name}).json()
                    print(_engineers)
                except Exception as e:
                    Clock.schedule_once(lambda dt: toast('You are offlline',1),0.5)
                    Clock.schedule_once(lambda dt: _modal.dismiss() ,1)
                    _modal.dismiss()
                    return
                # if response contains issues ->
                if _engineers["code"] == "success":
                    Clock.schedule_once(lambda dt: toast('Engineer Deleted Sucessfully',1),0.5)
                    Clock.schedule_once(lambda dt:self.refresh_engineers(dt=dt), 0.1)
            threading.Thread(target=_query).start()

        def _add_engineers():
            global _modal
            # 
            engineers_list = self.root.get_screen("admin_dashboard").ids.engineers_list
            print(engineers_list.children)
            #
            # engineers_list.clear_widgets()
            # print(engineers_list.children)
            # Logic to match list items with the engineers
            if len(engineers_list.children) < len(_engineers['data']):
                for i in range(len(_engineers['data']) - len(engineers_list.children)):
                    engineers_list.add_widget(TwoLineAvatarIconListItem(
                        IconLeftWidget(
                        ),
                        IconRightWidget(
                        ),
                        text="Two-line item with avatar",secondary_text="Secondary text here",theme_text_color="Custom",text_color=self.theme_cls.primary_color
                        )
                    )
                    print('added new to list')

            try:
                for i in engineers_list.children:
                    print(engineers_list.children.index(i))
                    i.theme_text_color = "Custom"
                    i.text_color = self.theme_cls.primary_color
                    i.text = _engineers['data'][engineers_list.children.index(i)]['name']
                    i.secondary_text = str('busy with a complaint' if not _engineers['data'][engineers_list.children.index(i)]['availability'] else 'available')
                    #
                    rightwidget = i.children[0].children
                    rightwidget[0].icon = "home" if _engineers['data'][engineers_list.children.index(i)]['availability'] else "briefcase"
                    rightwidget[0].theme_text_color = "Custom"
                    rightwidget[0].text_color = 'green' if _engineers['data'][engineers_list.children.index(i)]['availability'] else 'orange'
                    # rightwidget[0].on_release = lambda : _modal.open()
                    #
                    leftwidget = i.children[1].children
                    leftwidget[0].icon = "face-agent"
                    leftwidget[0].theme_text_color = "Custom"
                    leftwidget[0].text_color = 'green' if _engineers['data'][engineers_list.children.index(i)]['availability'] else 'orange'
                    leftwidget[0].on_release = lambda _instance = i, x=_engineers['data'][engineers_list.children.index(i)]['name'] : open_modal_engineer(_name=x,_instance=_instance)
                
                def open_modal_engineer(_instance,_name):
                    # _modal_issue.children[0].children[0].children[0].children[0].on_release = lambda index=i.index:print(index)
                    _modal_issue.title = f'Do you want to delete engineer ?\n{_name[:20]}...'
                    _modal_issue.children[0].children[0].children[0].children[0].on_release = lambda name=_name : delete_engineer(_name=name,_instance=_instance)
                    _modal_issue.open()

                    # print(i.text,i.secondary_text,i.children[1].children)
            except Exception as e:
                print(e)
            #     engineers_list.add_widget(OneLineListItem(text=f"Item {i}"))

            _modal.dismiss()
        # _query()
        Clock.schedule_once(lambda x:threading.Thread(target=_query).start(),0.5)
        # Force garbage collection
        gc.collect()
    


_APP = AdminDashboardApp()

if __name__ == "__main__":
    _APP.run()