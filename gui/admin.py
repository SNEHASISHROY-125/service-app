import threading
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
from kivy.uix.modalview import ModalView
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty

# from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarListItem


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
                        #radius: dp(24)

                    ScrollView: 
                        do_scroll_x: False
                        
                        MDBoxLayout:
                            orientation: 'vertical'
                            size_hint: 1, None
                            spacing: dp(10)
                            padding: dp(10)
                            height: self.minimum_height
                            size_hint_y: None

                            MDBoxLayout:
                                orientation: 'vertical'
                                size_hint: 1, None
                                spacing: dp(10)
                                padding: dp(10)
                        
                                
                                MDBoxLayout:
                                    orientation: 'horizontal'
                                    size_hint: 1, None
                                    spacing: dp(10)
                                    padding: dp(10)
                            
                                    MDFlatButton:
                                        text: 'Button 1'
                                        size_hint: 0.5, 1
                                        md_bg_color: 1, .5, 0.9, 1
                                        on_release: 
                                    MDFlatButton:
                                        text: 'Button 1'
                                        size_hint: 0.5, 1
                                        md_bg_color: .3, 1, 0.9, 1
                                        on_release: 
                                
                                MDBoxLayout:
                                    orientation: 'horizontal'
                                    size_hint: 1, None
                                    spacing: dp(10)
                                    padding: dp(10)

                                    MDFlatButton:
                                        text: 'Button 1'
                                        size_hint: 0.5, 1
                                        md_bg_color: 1, .5, 0.9, 1
                                        on_release:
                                    MDFlatButton:
                                        text: 'Button 1'
                                        size_hint: 0.5, 1
                                        md_bg_color: .3, 1, 0.9, 1
                                MDBoxLayout:
                                    orientation: 'horizontal'
                                    size_hint: 1, None
                                    spacing: dp(10)
                                    padding: dp(10)

                                    MDFlatButton:
                                        text: 'Button 1'
                                        size_hint: 0.5, 1
                                        md_bg_color: 1, .5, 0.9, 1
                                        on_release:
                                    MDFlatButton:
                                        text: 'Button 1'
                                        size_hint: 0.5, 1
                                        md_bg_color: .3, 1, 0.9, 1

                                    
                        


            MDBottomNavigationItem:
                name: 'screen 2'
                text: 'Twitter'
                icon: 'twitter'

                MDScreen:
                   
                    FitImage:
                        size_hint: 1, 1
                        pos_hint: {"center_x": .5, "center_y": .5}
                        source: "{}".format(app.s_)
                        #radius: dp(24)

                    ScrollView:
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

class AdminDashboardApp(MDApp):
    s_ = source_
    def build(self):
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

    
    def render_complaints(self):
        def _query():
            import requests
            from kivy.clock import Clock
            from kivymd.toast import toast
            global _issue
            try:
                _issue = requests.get(url=server_url+"get_all", params={"table_name": "issues"}).json()
                print(_issue)
            except Exception as e:
                Clock.schedule_once(lambda dt: toast('You are offlline'),0.5)
                Clock.schedule_once(lambda dt: _modal.dismiss() ,1)
                return
            # if response contains issues ->
            if _issue:
                threading.Thread(target=Clock.schedule_once(_add_complaints,0.1)).start()


        def _add_complaints(dt):
            # appointments = _appointments_data
            # the root MDList to add appointments to
            global _issue
            global _modal
            def bind_list_item(x):
                # print(x.text)
                # scroll_view = ScrollView(
                #     do_scroll_x= False
                #     )
                # list_item = TwoLineAvatarIconListItem(text=x['issue'], secondary_text=x['complaintid'])
                # scroll_view.add_widget(list_item)
                # _modal_issue.add_widget(scroll_view)

                def not_none(x): 
                    if not x :
                        print(x)
                        return 'not-availale'
                    else: return x
                # dialog
                m_  =   MDDialog(
                    title=x['status'],
                    type="simple",
                    items=[
                        Item(text=not_none(x['issue']), theme_text_color="Custom", text_color=self.theme_cls.primary_color, source="https://cdn.iconscout.com/icon/free/png-256/doctor-1851563-1569282.png"),
                        Item(text=not_none(x['complaintid']), theme_text_color="Custom", text_color=self.theme_cls.primary_color, source="https://cdn.iconscout.com/icon/free/png-256/doctor-1851563-1569282.png"),
                        Item(text=not_none(x['status']), theme_text_color="Custom", text_color=self.theme_cls.primary_color, source="https://img.icons8.com/color/240/ok--v1.png"),
                        Item(text=not_none(x['name']), theme_text_color="Custom", text_color=self.theme_cls.primary_color, source="https://cdn.iconscout.com/icon/free/png-256/doctor-1851563-1569282.png"),
                        Item(text=not_none(str(x['phone'])), theme_text_color="Custom", text_color=self.theme_cls.primary_color, source="https://cdn.iconscout.com/icon/free/png-256/doctor-1851563-1569282.png"),
                        Item(text=not_none(x['user_id']), theme_text_color="Custom", text_color=self.theme_cls.primary_color, source="https://cdn.iconscout.com/icon/free/png-256/doctor-1851563-1569282.png"),
                        Item(text=not_none(x['esttime']), theme_text_color="Custom", text_color=self.theme_cls.primary_color, source="https://cdn.iconscout.com/icon/free/png-256/doctor-1851563-1569282.png"),
                        Item(text=not_none(x['location']), theme_text_color="Custom", text_color=self.theme_cls.primary_color, source="https://cdn.iconscout.com/icon/free/png-256/doctor-1851563-1569282.png"),
                        Item(text=not_none(x['payments_receipt']), theme_text_color="Custom", text_color=self.theme_cls.primary_color, source="https://cdn.iconscout.com/icon/free/png-256/doctor-1851563-1569282.png"),
                    ],
                    buttons=[
                        MDFlatButton(
                            text="CLOSE",
                            theme_text_color="Custom",
                            text_color=self.theme_cls.primary_color,
                            on_release=lambda x: m_.dismiss()
                        ),
                    ],
                )
                
                #
                global _modal
                m_.bind(on_open=lambda x:_modal.dismiss())
                m_.bind(on_pre_dismiss=lambda x : m_.clear_widgets())
                # m_.bind(on_pre_dismiss=lambda x: clr(m=m_))
                m_.open()

            appointments_list = self.root.get_screen("admin_dashboard").ids.complaints_list
            # appointments = {'complaint-id': '#56608' ,'attd-name': 'NAME_', 'time': '12:00 PM', 'status': 'pending'}
            # remove all widgets from the list
            appointments_list.clear_widgets()
            for i in _issue['data']:
                print(i)
                # icon
                if i['status'] == 'open': icon_ = "clock"
                elif i['status'] == 'closed': icon_ = "check-circle-outline"
                elif i['status'] == 'canceled': icon_ = "close-circle-outline"
                _issue_widget = TwoLineAvatarIconListItem(
                        IconLeftWidget(
                            icon=icon_,
                            theme_text_color="Custom",
                            text_color=self.theme_cls.primary_color
                        ),
                        IconRightWidget(
                            icon="chevron-right",
                            theme_text_color="Custom",
                            text_color=self.theme_cls.primary_color,
                            on_press=lambda x: threading.Thread(target=_modal.open()).start(),
                            on_release=lambda x,i=i: bind_list_item(i),
                        ),
                        text= i['issue'],
                        theme_text_color="Custom",
                        text_color = self.theme_cls.primary_color,
                        secondary_text= i['complaintid'],
                    )
                # bind the on_press event
                _issue_widget.bind(on_release=lambda x: print(x.text,x))
                # add the widget to the list
                appointments_list.add_widget(_issue_widget, index=0)
            
            # relese-resources
            appointments_list = None
            # _issue = None
            # print("Appointments added\n",res_,phone_)
            Clock.schedule_once(lambda dt: _modal.dismiss() ,1)
        # 
        threading.Thread(target=_query).start()

    def on_start(self):
        self._init_loading_widget()
        _modal.open()
        self.render_complaints()
        # threading.Thread(target=self.render_complaints).start()
    def on_stop(self):
        pass

    def on_pause(self):
        pass

    def on_resume(self):
        pass
    

if __name__ == "__main__":
    AdminDashboardApp().run()