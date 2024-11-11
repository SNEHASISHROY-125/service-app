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
                text: 'Mail'
                icon: 'gmail'
                badge_icon: "numeric-1"

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
                            spacing: dp(10)
                            padding: dp(10)
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
                text: 'Twitter'
                icon: 'twitter'

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

class PullToRefreshBehavior:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._start_touch_y = None

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self._start_touch_y = touch.y
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self._start_touch_y and self._start_touch_y - touch.y > 50:
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


class AdminDashboardApp(MDApp):
    s_ = source_
    dialog = None
    _dialog = None
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
        _modal  =   ModalView(size_hint=(.5, .5), auto_dismiss=True, background='', background_color=[0, 0, 0, 0])
        _modal.add_widget(MDSpinner(size_hint=(None, None), size=(46, 46), pos_hint={'center_x': .5, 'center_y': .5},active=True))  # Load and play the GIF
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # modal
        global _modal_issue
        # _modal_issue  =   ModalView(size_hint=(.5, .5), auto_dismiss=True, background='', background_color=[1, 1, 1, .5],border=[20,0,0,20])
        _modal_issue = MDDialog(
                title="Set backup account",
                type="simple",
                items=[
                ],
            )
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
                Clock.schedule_once(lambda dt: toast('You are offlline'),0.5)
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
            
            def _show_dialog(_issue_data):
                self._dialog.title = f"Complaint {_issue_data['complaintid']}"
                _items_list = self._dialog.children[0].children[2].children[0].children
                print(self._dialog.children[0].children[2].children[0].children[0].source)
                _payments_receipt = _items_list[0]
                _location = _items_list[1]
                _esttime = _items_list[2]
                _user_id = _items_list[3]
                _phone = _items_list[4]
                _name = _items_list[5]
                _status = _items_list[6]
                _complaintid = _items_list[7]
                _issue = _items_list[8]
                #  set status icon
                _status.source="https://cdn.iconscout.com/icon/free/png-256/doctor-1851563-1569282.png" if _issue_data['status'] == 'open' else "https://img.icons8.com/color/240/ok--v1.png" if _issue_data['status'] == 'closed' else "https://img.icons8.com/color/240/close-sign.png"
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
                print(engineers_list.children.index(i))
                i.theme_text_color = "Custom"
                i.text_color = self.theme_cls.primary_color
                print(_complaints['data'][engineers_list.children.index(i)])
                i.text = _complaints['data'][engineers_list.children.index(i)]['issue']
                i.secondary_text = str( _complaints['data'][engineers_list.children.index(i)]['complaintid'])
                #
                rightwidget = i.children[0].children
                rightwidget[0].icon = "chevron-right"
                rightwidget[0].theme_text_color = "Custom"
                rightwidget[0].text_color = self.theme_cls.primary_color
                rightwidget[0].on_release = lambda data=_complaints['data'][engineers_list.children.index(i)] : _show_dialog(data)

                #
                leftwidget = i.children[1].children
                leftwidget[0].icon = "clock" if _complaints['data'][engineers_list.children.index(i)]['status'] == 'open' else "check-circle-outline" if _complaints['data'][engineers_list.children.index(i)]['status'] == 'closed' else "close-circle-outline"
                # print(i.text,i.secondary_text,i.children[1].children)

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
                Clock.schedule_once(lambda dt: toast('You are offlline'),0.5)
                Clock.schedule_once(lambda dt: _modal.dismiss() ,1)
                return
            
            global _modal
            _modal.open()
            if _engineers['code'] == 'success':
                # add to the list
                _modal.open()
                Clock.schedule_once(self.refresh_engineers, .3)  # Simulate a delay
                # self.refresh_engineers()

    def on_start(self):
        self._init_loading_widget()
        # 1
        _modal.open()
        Clock.schedule_once(self.refresh_engineers, .1)  # Simulate a delay
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
        self._dialog.open()
        # Force garbage collection
        gc.collect()
    def on_stop(self):
        pass

    def on_pause(self):
        pass

    def on_resume(self):
        pass
    
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
                Clock.schedule_once(lambda dt: toast('You are offlline'),0.5)
                Clock.schedule_once(lambda dt: _modal.dismiss() ,1)
                return
            # if response contains issues ->
            if _engineers:
                Clock.schedule_once(lambda x:_add_engineers(), 0.1)
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
                rightwidget[0].on_release = lambda : _modal.open()
                #
                leftwidget = i.children[1].children
                leftwidget[0].icon = "account-hard-hat"
                leftwidget[0].theme_text_color = "Custom"
                leftwidget[0].text_color = 'green' if _engineers['data'][engineers_list.children.index(i)]['availability'] else 'orange'

                # print(i.text,i.secondary_text,i.children[1].children)

            #     engineers_list.add_widget(OneLineListItem(text=f"Item {i}"))

            _modal.dismiss()
        # _query()
        Clock.schedule_once(lambda x:threading.Thread(target=_query).start(),0.5)
        # Force garbage collection
        gc.collect()
    


_APP = AdminDashboardApp()

if __name__ == "__main__":
    _APP.run()