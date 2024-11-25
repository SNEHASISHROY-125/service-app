'''
User-UI
'''
from kivymd.app import MDApp
from kivymd.uix.list import TwoLineAvatarIconListItem, OneLineAvatarListItem, IconLeftWidget, IconRightWidget
from kivymd.uix.dialog import MDDialog
import kivymd.utils.asynckivy as ak
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivy.uix.scrollview import ScrollView
import sql_local as sq_local
from kivy.lang import Builder
from kivymd.toast import toast as tst
from kivy.utils import platform
from kivy.clock import Clock
import threading
from kivy.properties import StringProperty
from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty
from kivy.metrics import dp


from kivy.config import Config
Config.set('kivy', 'pause_on_minimize', '1')
from kivy.core.window import Window
# Set the window size
Window.size = (800, 600)

def toast(text:str, duration=1.0):
    if platform == 'android':
        tst(text, duration)
    else:
        tst(text, duration=duration)

# "https://icons8.com/illustrations/author/ARh4OKrFtdfC" discount.png
images = [
"https://images.pexels.com/photos/3389613/pexels-photo-3389613.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
]

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

global FAPP

class RefreshScrollView(PullToRefreshBehavior, ScrollView):
    refreshing = BooleanProperty(False)
    spinner = ObjectProperty(None)
    global _modal
    global FAPP

    def refresh(self):
        print("Pulled down to refresh!")
        _modal.open()
        # Add your refresh logic here
        Clock.schedule_once(FAPP.render_appointment, .3)  # Simulate a delay
        # threading.Thread(target=self.run_background_task).start()  # Run the background task in a separate thread

    def run_background_task(self):
        try:
            FAPP.render_engineers()
        except Exception as e:
            print(e)

class APP(MDApp):
    user_id: str = '' #"0ef59067-6cc5-447a-8d4c-21e50577958d"
    server_url = "https://chat-app.fudemy.me/"
    current_screen = ''
    switch_tab = ''
    user_name = ''
    image_list = images
    email = ''

    def build(self):
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.primary_hue = "A700" 
        return Builder.load_file('gui/user.kv')
    
    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label,):
        screen = self.root.get_screen('services')
        if instance_tab.name == 'appointments_tab':
            screen.ids.top_app_bar.title = "My Appointments"
        elif instance_tab.name == 'hot_deals_tab':
            screen.ids.top_app_bar.title = "Hot Deals"
        else:
            screen.ids.top_app_bar.title = "All Services"
        print(instance_tab.name)

    def toast(self,text:str, duration=1.0):
        if platform == 'android':
            tst(text, duration)
        else:
            tst(text, duration=duration) 
    
    def render_appointment(self , *args):
        import requests
        from kivy.clock import Clock
        # from kivymd.toast import toast
        import time
        global _modal
        _modal.open()
        # self.root.ids.refresh_scroll.refreshing = False
        # self.root.ids.refresh_scroll.spinner.active = False  # Stop the spinner
        # self.root.ids.refresh_scroll.spinner.opacity = 0  # Hide the spinner
        # make query to get all complaints
        def _query():
            #
            server_url = "http://chat-app.fudemy.me/"
            if not self.user_id or self.user_id == 'xyz':
                Clock.schedule_once(lambda dt: toast('You are not logged in',1),0.1)
                Clock.schedule_once(lambda dt: toast('log in to see your appointments',1),0.5)
                Clock.schedule_once(lambda dt: _modal.dismiss() ,1)
                print(self.user_id)
                return
            global _complaints
            try:
                print(server_url)
                time.sleep(1) # simulate a delay | blocks main thread
                _complaints = requests.get(url=server_url+f"complaint/{self.user_id}/complaint_id").json()
                print(_complaints)
            except Exception as e:
                Clock.schedule_once(lambda dt: toast('You are offlline',1),0.5)
                Clock.schedule_once(lambda dt: _modal.dismiss() ,1)
                return
            # if response contains no issues ->
            try:
                if _complaints["detail"] == "No complaints found for the user":
                    Clock.schedule_once(lambda dt: toast('No complaints found',1),0.5)
                    Clock.schedule_once(lambda dt: _modal.dismiss() ,1)
                    return
            except Exception as e: print(e)
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
                            self.render_appointment()
                            # Clock.schedule_once(lambda x:_add_complaints(), 0.1)
                        elif _complaints["detail"] == "Complaint not found":
                            Clock.schedule_once(lambda dt: toast("Complaint not found" , 1), 0.5)
                    except Exception as e:
                        print(e)
                        Clock.schedule_once(lambda dt: toast("Error closing complaint" , 1), 0.5)
                threading.Thread(target=_query).start()
            
            def _show_dialog(_issue_data):
                self._dialog.title = f"Complaint {_issue_data[4]}"
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
                _status.source="https://img.icons8.com/3d-fluency/94/sand-clock-1.png" if _issue_data[8] == 'open' else "https://img.icons8.com/color/240/ok--v1.png" if _issue_data[8] == 'closed' else "https://img.icons8.com/keek/100/delete-sign.png"
                # set values
                _payments_receipt.text = not_none(str(_issue_data[9]))
                _location.text = not_none(_issue_data[2])
                _esttime.text = not_none(_issue_data[5])
                _user_id.text = not_none(_issue_data[7])
                _phone.text = not_none(str(_issue_data[3]))
                _name.text = not_none(_issue_data[6])
                _status.text = not_none(_issue_data[8])
                _complaintid.text = not_none(str(_issue_data[4]))
                _issue.text = not_none(_issue_data[1])
                # print(_payments_receipt,'\n',_location.text,'\n',_esttime,'\n',_user_id,'\n',_phone,'\n',_name,'\n',_status,'\n',_complaintid,'\n',_issue)
                # release resorces
                for i in [_payments_receipt, _location, _esttime, _user_id, _phone, _name, _status, _complaintid, _issue]:
                    i = None
                    # i = None
                # print(_dialog.children[0].children[2].children[0].children[1].text)
                self._dialog.open()
            # 
            engineers_list = self.root.get_screen("services").ids.appointments_list
            print(engineers_list.children)
            #
            # engineers_list.clear_widgets()
            # print(engineers_list.children)
            # Logic to match list items with the engineers
            if len(engineers_list.children) < len(_complaints['complaints_list']):
                for i in range(len(_complaints['complaints_list']) - len(engineers_list.children)):
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
                # 
                i.theme_text_color = "Custom"
                i.text_color = self.theme_cls.primary_color
                print(_complaints['complaints_list'][index])
                i.text = _complaints['complaints_list'][index][1]
                i.secondary_text = str(_complaints['complaints_list'][index][4])

                rightwidget = i.children[0].children
                rightwidget[0].icon = "chevron-right"
                rightwidget[0].theme_text_color = "Custom"
                rightwidget[0].text_color = self.theme_cls.primary_color
                rightwidget[0].on_release = lambda data=_complaints['complaints_list'][index]: _show_dialog(data)

                leftwidget = i.children[1].children
                leftwidget[0].icon = "clock" if _complaints['complaints_list'][index][8] == 'open' else "check-circle-outline" if _complaints['complaints_list'][index][8] == 'closed' else "close-circle-outline"
                global _modal_issue
                #
                # _instance = i
                # _complaint_id = _complaints['data'][index]['complaintid']
                # _code = _modal_issue.content_cls.children[0].text if _modal_issue.content_cls.children[0].text else 'CANCELED'
                i.complaint_id = _complaints['complaints_list'][index][4]
                # _modal_issue.buttons[1].on_release = lambda _instance=i, complaint_id=_complaints['data'][index]['complaintid'], _code=_modal_issue.content_cls.children[0].text if _modal_issue.content_cls.children[0].text else 'CANCELED': _close_complaint(_instance, complaint_id, _code)
                leftwidget[0].on_release = lambda _instance=i,_issue=_complaints['complaints_list'][index][1] : open_modal_issue(_instance,_issue=_issue)

                def open_modal_issue(_instance,_issue):
                    # _modal_issue.children[0].children[0].children[0].children[0].on_release = lambda index=i.index:print(index)
                    _modal_issue.title = f'Do you want to close the complaint ?\n{_issue[:20]}...'
                    _modal_issue.children[0].children[0].children[0].children[0].on_release = lambda _instance=_instance, _complaint_id=_instance.complaint_id, : _close_complaint(_instance=_instance, _complaint_id=_complaint_id, _code=_modal_issue.content_cls.children[0].text if _modal_issue.content_cls.children[0].text else 'CANCELED')
                    _modal_issue.open()

            #     engineers_list.add_widget(OneLineListItem(text=f"Item {i}"))

            _modal.dismiss()
        # _query()
        Clock.schedule_once(lambda x:threading.Thread(target=_query).start(),0.5)

    def book_appointment(self, data:dict,*args):
        print(data)
        global _modal
        _modal.open()
        def _query():
            import requests
            from kivy.clock import Clock
            import time
            # check wheather user has any ongoing | open appointment
            global _complaints
            _complaints = requests.get(url=self.server_url+f"complaint/{self.user_id}/complaint_id").json()
            try:
                if _complaints["detail"] =="No complaints found for the user": pass
            except Exception as e: print(e)
            if _complaints:
                for i in _complaints['complaints_list']:
                    print(i[8])
                    if i[8] == 'open':
                        Clock.schedule_once(lambda dt: toast('You have an ongoing appointment',1),0.2)
                        self.switch_tab = 'appointments_tab'
                        Clock.schedule_once(lambda dt: self.switch_to_tab(),.5)
                        Clock.schedule_once(lambda dt: _modal.dismiss() ,1)
                        return
            # check data is not empty
            if not data['issue_desc'] or not data['user_location'] or not data['user_phone']:
                return
            server_url = "https://chat-app.fudemy.me/"
            try:
                print(server_url)
                time.sleep(1) # simulate a delay | blocks main thread
                _complaints = requests.post(url=server_url+"report_issue", json={"issue": data['issue_desc'], "location": data['user_location'], "phone": data['user_phone'], "user_id": self.user_id}).json()
                print(_complaints)
            except Exception as e:
                Clock.schedule_once(lambda dt: toast('You are offlline',1),0.1)
                Clock.schedule_once(lambda dt: _modal.dismiss() ,1)
                return
            # if response contains issues ->
            try:
                if _complaints['complaintid']:
                    Clock.schedule_once(lambda dt: toast('your appointment booked',1),0.1)
                    Clock.schedule_once(lambda x: self.render_appointment(), 0.1)
                    #
                    Clock.schedule_once(lambda x: setattr(self.root , 'current' ,'services') , .1)
                    Clock.schedule_once(lambda x: setattr(self.root.get_screen('services').ids.top_app_bar , 'title' , "All Services"), .1)
                    _modal.dismiss()
            except Exception as e:
                if _complaints["detail"] == "No available service engineers":
                    Clock.schedule_once(lambda dt: toast('Our engineers are busy right now',1),0.1)
                    Clock.schedule_once(lambda dt: toast('try again later',1.5),1.5)
                    _modal.dismiss()

        threading.Thread(target=_query).start()
    
        # login
    def login(self):
        # import s_requests as s_r
        # username = self.root.get_screen('signup').ids.username.text
        # password = self.root.get_screen('signup').ids.password.text
        email = self.root.get_screen('login').ids.email.text
        # loadingscreen | modal
        _modal.open()
        # root = lambda: setattr(self.root, 'current', 'login')
        # make a query to the server | signup
        def _make_query():
            import requests
            
            # _ = s_r.make_query("http://localhost:8000/login", data={"email": "user@example.com"})
            try:
                _ = requests.post(url=self.server_url+'login', params={"email": email}).json()
            except Exception as e:
                print(e)
                Clock.schedule_once(lambda dt: toast('You are offlline'),0.5)
                Clock.schedule_once(lambda dt: _modal.dismiss() ,1)
                return
            try:
                if _['code'] == 'exists-check-email':
                    # save the user data to the local database
                    # import sql_local as sq_local
                    conn_ = sq_local.create_connection('app.db')
                    r_=sq_local.update_data(conn_, 'users', {'user_id': _['user_id'],'email': email}, {'id': 1})
                    # take the user to the verify OTP screen
                    # global user_id
                    self.user_id = _['user_id']
                    print(self.user_id,'\n',r_)
                    Clock.schedule_once(lambda dt: toast("Email already exists\ncheck email for otp", duration=2.5), 0)
                    Clock.schedule_once(lambda dt: setattr(self.root, 'current', 'verify_otp'), 1)
                    # Clock.schedule_once(lambda dt: setattr(self.root, 'current', 'home'), 1)
                elif _['code'] == 'not_exist':
                    # take the user to the login screen
                    Clock.schedule_once(lambda dt: toast("Email does not exist", duration=1.5), 0)
                    Clock.schedule_once(lambda dt: setattr(self.root, 'current', 'signup'), 1)
            except Exception as e:
                try:
                    if _['detail'] == 'Username already exists':...
                        # toast("Username already exists",duration=1.5)
                except Exception as e:
                    print(e)
            finally:
                _modal.dismiss()
                # print(_,'from login')
        threading.Thread(target=_make_query).start()
        # if username and password:
        #     print(f"Username: {username}, Password: {password}")
        #     self.root.current = 'login'
        # else:
        #     print("Please enter valid details")
        
    # signup
    def signup(self):
        print('form signup ',self.email)
        # set the email
        self.root.get_screen('login').ids.email.text = self.email
        import requests
        global server_url
        # make a query to the server | signin
        # load modal
        _modal.open()
        def _make_query():
            name = self.root.get_screen('signup').ids.username.text
            email = self.root.get_screen('signup').ids.email.text
            try:
                _ = requests.post(url=self.server_url+'login_or_signup', json={"username": name, "email": email}).json()
            except Exception as e:
                Clock.schedule_once(lambda dt: toast('You are offlline'),0.5)
                Clock.schedule_once(lambda dt: _modal.dismiss() ,1)
                return
            try:
                if 'code' in _:
                    if _['code'] == 'check-email':
                        # save the user data to the local database
                        # import sql_local as sq_local
                        conn_ = sq_local.create_connection('app.db')
                        sq_local.update_data(conn_, 'users', {'user_id': _['user_id'],'email': email}, {'id': 1})
                        # close the connection
                        conn_.close()
                        # global user_id
                        self.user_id = _['user_id']
                        # take the user to the login screen
                        Clock.schedule_once(lambda dt: toast("OTP sent", duration=1.5), 1)
                        Clock.schedule_once(lambda dt: setattr(self.root, 'current', 'verify_otp'), 1)
                elif 'detail' in _:
                    if _['detail'] == "Email already exists":
                        # take the user to the login screen
                        Clock.schedule_once(lambda dt: toast("Email already exists", duration=1.5), 1)
                        Clock.schedule_once(lambda dt: setattr(self.root, 'current', 'login'), 1)
            except Exception as e:
                print(f"Exception occurred: {e}")
                Clock.schedule_once(lambda dt: toast("EXCEPTION ",e[:10], duration=1.5), 1)

            finally:
                print(_)
                _modal.dismiss()
        
        threading.Thread(target=_make_query).start()

    # verify otp
    def verify_otp(self):
        import requests
        global server_url
        # make a query to the server | verify otp
        _modal.open()
        def _make_query():
            # global user_id
            global _current_screen
            # loading screen
            otp = int(self.root.get_screen('verify_otp').ids.otp.text)
            try:
                _ = requests.post(url=self.server_url+'verify_otp', params={"user_id": self.user_id, "otp_": otp}).json()
            except Exception as e:
                Clock.schedule_once(lambda dt: toast('You are offlline'),0.5)
                # close the modal
                Clock.schedule_once(lambda dt: _modal.dismiss() ,1)
                return
            try:
                # print(_)
                if _['code'] == 'success':
                    # take the user to the login screen
                    Clock.schedule_once(lambda dt: toast("OTP verified", duration=1.5), 0)
                    # 1
                    self.render_appointment()
                    Clock.schedule_once(lambda dt: setattr(self.root, 'current', 'book_apointment'), 1)
            except Exception as e:
                if _['detail'] == 'Invalid OTP':
                    print("Invalid OTP detected")
                    print(_['detail'])
                    _modal.dismiss()
                    Clock.schedule_once(lambda dt: toast("Invalid OTP", duration=1.5), 0)
                elif _['detail'] == 'Invalid user_id':
                    Clock.schedule_once(lambda dt: toast("Invalid user_id", duration=1.5), 0)
                    _modal.dismiss()
                elif _['detail'] == 'OTP expired':
                    Clock.schedule_once(lambda dt: toast("OTP expired", duration=1.5), 0)
                    _modal.dismiss()
                    # display to the user that the otp has expired
                else:
                    print(_['detail'])
                    _modal.dismiss()
                # print(f"Exception occurred: {e}")
        
        threading.Thread(target=_make_query).start()

    # 

    def on_start(self):
        # 1
        self._init_loading_widget()
        # 2
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
        # 3 ...
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
        # 5
        # import dependencies
        import sql_local as sq_local
        # check if the local database exists
        # import_dependencies()
        global con_local
        con_local = sq_local.check_db_exists('app.db')
        # initialize the local-database
        sq_local.initialize_db(con_local)
        # if the app is running for the first time
        if sq_local.query_data(con_local, 'select app_first_run from settings')[0][0] == 1:
            # set the app_first_run to False
            sq_local.update_data(con_local, 'settings', {'app_first_run': 0},condition={'id': 1})
            # take the user to the welcome screen
            Clock.schedule_once(lambda dt: setattr(self.root, 'current', 'welcome'), 2.5)
            # self.root.current = 'welcome'
        else:
            # get the app theme and set it
            app_theme = sq_local.query_data(con_local, 'SELECT app_theme FROM settings')[0][0]
            self.theme_cls.theme_style = app_theme
            app_theme = None
            # get user_id
            _uid = sq_local.query_data(con_local, 'SELECT user_id FROM users')[0][0]
            self.user_id = _uid if not _uid=='xyz' else ''
            self.user_name = sq_local.query_data(con_local, 'SELECT email FROM users')[0][0]
            # take the user to the menu screen
            # Clock.schedule_once(lambda dt: setattr(self.root, 'current', 'login'), 2.5)
            # self.root.current = 'menu'

        # 6
        self.render_appointment() if self.user_id else toast('You are not logged in',1)

    def on_pause(self):
        # Save any necessary state data or suspend operations here.
        return True  # Return True to indicate we’re handling the pause.

    def on_resume(self):
        # Restore any data or state when the app resumes.
        # Force a redraw
        self.root.canvas.ask_update()

    def _init_loading_widget(self):
        ''' Initialize the loading widget '''
        # init the modal view
        from kivy.uix.modalview import ModalView
        from kivymd.uix.spinner import MDSpinner
        global _modal
        _modal  =   ModalView(size_hint=(.5, .5), auto_dismiss=False, background='', background_color=[0, 0, 0, 0])
        _modal.add_widget(MDSpinner(line_width=dp(5.25), size_hint=(None, None), size=(80, 80), pos_hint={'center_x': .5, 'center_y': .5}, active=True))  # Load and play the GIF
    

# app instance
FAPP = APP()
FAPP.run()