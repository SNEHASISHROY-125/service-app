import kivy.clock
from kivymd.uix.progressbar import MDProgressBar
import asyncio
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
import threading , time

KV = '''
ScreenManager:
    id: screen_manager
    BookApointmentScreen:
    LoginScreen:
    SignupScreen:
    MenuScreen:
    MyAppointmentsScreen:
    WelcomeScreen:
    HomeScreen:
    VerifyOTPScreen:

<WelcomeScreen@Screen>:
    name: 'welcome'
    MDLabel:
        text: "Welcome to the Welcome Page!"
        halign: 'center'
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
    MDRaisedButton:
        text: "Go to Signup"
        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
        on_release: app.root.current = 'signup'

<LoginScreen@Screen>:
    name: 'login'
    MDTextField:
        id: email
        hint_text: "Email"
        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
        size_hint_x: None
        width: 300
    MDRaisedButton: 
        text: "Login"
        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
        on_release: app.login()

<VerifyOTPScreen@Screen>:
    name: 'verify_otp'
    MDTextField:
        id: otp
        hint_text: "ENTER OTP SENT TO YOUR EMAIL"
        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
        size_hint_x: None
        width: 300
    MDRaisedButton:
        text: "Verify OTP"
        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
        on_release: app.verify_otp()
    
<SignupScreen@Screen>:
    name: 'signup'
    MDTextField:
        id: username
        hint_text: "Username"
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        size_hint_x: None
        width: 300
    MDTextField:
        id: email
        hint_text: "Email"
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint_x: None
        width: 300
    MDRaisedButton:
        text: "Signup"
        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
        on_release: app.signup()
    MDRaisedButton:
        text: "Go to Home"
        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
        on_release: app.signup()

<HomeScreen@Screen>:
    name: 'home'
    BoxLayout:
        orientation: 'vertical'
        MDLabel:
            text: "Welcome to the Home Page!"
            halign: 'center'
            pos_hint: {'center_x': 0.5, 'center_y': 0.9}
        MDProgressBar:
            id: progress_bar
            value: 0
            max: 100
            pos_hint: {'center_x': 0.5, 'center_y': 0.8}
            size_hint_x: 0.8
            size_hint_y: None
            height: dp(30)

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(100)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            spacing: dp(20)
            MDIconButton:
                icon: "moon-waning-crescent"
                user_font_size: "64sp"
                on_release: app.on_image_click("Image 1")
            MDIconButton:
                icon: "pencil"
                user_font_size: "64sp"
                on_release: print(app.root.get_screen('menu').ids.top_app_bar.left_action_items)
            MDIconButton:
                icon: "image3.png"
                user_font_size: "64sp"
                on_release: app.on_image_click("Image 3")
        MDRaisedButton:
            text: "Go to Login"
            pos_hint: {'center_x': 0.5, 'center_y': 0.1}
            on_release: app.switch_to_login()

<MenuScreen@Screen>:
    name: 'menu'
    BoxLayout:
        orientation: 'vertical'
        MDTopAppBar: 
            id: top_app_bar
            anchor_title: "left"
            title: "Menu Screen"
            left_action_items: [["arrow-left", lambda x: app.switch_to_home()]]
            right_action_items: [["account-circle-outline", lambda x: app.switch_to_login()]]
            elevation: 10
        
        BoxLayout:
            orientation: 'vertical'
            padding: dp(10)
    
    
            MDBoxLayout:
                orientation: 'vertical'
                padding: dp(10)
                spacing: dp(10)
                
                md_bg_color: 0.9, 0.7, 0.9, 1
                radius: [15, 15, 15, 15]
            
                MDBoxLayout:
                    orientation: 'horizontal'
                    
                    spacing: dp(10)
            
                    MDSmartTile:
                        radius: 24
                        box_radius: [0, 0, 24, 24]
                        box_color: 1, 1, 1, .3
                        source: "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2F2.bp.blogspot.com%2F-8DL1_7b-4h4%2FUhNloO6amvI%2FAAAAAAAAAcU%2Fj-ZgMSBMmg4%2Fs1600%2Flord%2Bkrishna%2Bfull%2Bscreen%2Bwallpaper.jpg&f=1&nofb=1&ipt=8360efe24ba6ad51243d6ddcd7de06f98374a6e83945c8e44a35146aa3ca7a77&ipo=images"
                        pos_hint: {"center_x": .5, "center_y": .5}
                        on_release: app.root.current = 'book_apointment'
                        
                        MDLabel:
                            text: "Hare krishna"
                            halign: 'center'
                            bold: True
                            color: 1, 1, 1, 1
                        
                    MDSmartTile:
                        radius: 24
                        box_radius: [0, 0, 24, 24]
                        box_color: 1, 1, 1, .2
                        source: "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2F2.bp.blogspot.com%2F-8DL1_7b-4h4%2FUhNloO6amvI%2FAAAAAAAAAcU%2Fj-ZgMSBMmg4%2Fs1600%2Flord%2Bkrishna%2Bfull%2Bscreen%2Bwallpaper.jpg&f=1&nofb=1&ipt=8360efe24ba6ad51243d6ddcd7de06f98374a6e83945c8e44a35146aa3ca7a77&ipo=images"
                        pos_hint: {"center_x": .5, "center_y": .5}
                        
                    
                
                MDBoxLayout:
                    orientation: 'horizontal'
                    
                    spacing: dp(10)
            
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

<BookApointmentScreen@Screen>:
    name: 'book_apointment'
    

    MDTopAppBar:
        pos_hint: {'top': 1}
        title: "Book Apointment"
        left_action_items: [["arrow-left", lambda x: app.switch_to_home()]]

    
    MDFloatLayout:
        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
        size_hint: 0.8, 0.8
        md_bg_color: 0.9, 0.7, 0.9, 1
        radius: [30, 30, 15, 15]
        orientation: 'vertical'
        
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(20)
            spacing: dp(20)
            
            pos_hint: {'center_x': 0.5, 'center_y': 0.75}

            
            MDTextField:
                id: issue_desc
                hint_text: "Tell us a little about your issue"
                multiline: True
                max_text_length: 250
                mode: "rectangle"
                helper_text: "we need to know what you are facing"
                helper_text_mode: "on_error"
                size_hint_y: None
                height: dp(150)
                
            MDTextField:
                id: user_location
                hint_text: "Your home Location/Address"
                max_text_length: 50
                mode: "rectangle"
                helper_text: "we need to know where you are"
                helper_text_mode: "on_focus"

            MDTextField:
                id: user_phone
                hint_text: "Your phone number"
                max_text_length: 10
                mode: "rectangle"
                helper_text: "our team will contact you"
                helper_text_mode: "on_focus"

            
                
            MDRaisedButton:
                text: "Book Apointment"
                on_release: app.book_appointments({'complaint-id': '#56608' ,'attd-name': 'NAME_', 'time': '12:00 PM', 'status': 'pending'})

<MyAppointmentsScreen@Screen>:
    name: 'my_apointments'
    BoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "My Appointment"
            left_action_items: [["arrow-left", lambda x: app.switch_to_home()]]
            right_action_items: [["account-circle-outline",]]
            elevation: 10

        ScrollView:
            do_scroll_x: False
            MDList:
                id: appointments_list

                TwoLineAvatarIconListItem:
                    text: "Two-line item with avatar"
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

from kivymd.uix.list import TwoLineAvatarIconListItem , IconLeftWidget , IconRightWidget
import threading
from kivy.clock import Clock
import kivy.app
from kivymd.toast import toast

global _appointments_data
_appointments_data = {}  # appointments data to load | server response writes here | 
global _modal 
_modal = None   # modal view | loading screen
global con_local
con_local = None # local database connection to save app data
global server_url 
server_url = "https://chat-app.fudemy.me/" # server url
global email
email = None
global user_id
user_id = None
global _current_screen
_current_screen = 'home'

# def import_dependencies():
import s_requests as s_r
import sql_local as sq_local

class MainApp(MDApp):
    
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "A700"
        
        return Builder.load_string(KV)
    
    # def on_start(self):
        # # self.root.current = 'welcome'
        # print(_modal)
        # # kivy.clock.Clock.schedule_once(lambda:import_dependencies(), 0.1)
        # # import dependencies
        # import sql_local as sq_local
        # # check if the local database exists
        # # import_dependencies()
        # global con_local
        # con_local = sq_local.check_db_exists('app.db')
        # # initialize the local-database
        # # sq_local.initialize_db(con_local) ...
        # # if the app is running for the first time
        # if sq_local.query_data(con_local, 'select app_first_run from settings')[0][0] == 1:
        #     # set the app_first_run to False
        #     sq_local.update_data(con_local, 'settings', {'app_first_run': 0},condition={'id': 1})
        #     # take the user to the welcome screen
        #     kivy.clock.Clock.schedule_once(lambda dt: setattr(self.root, 'current', 'welcome'), 2.5)
        #     # self.root.current = 'welcome'
        # else:
        #     # get the app theme and set it
        #     app_theme = sq_local.query_data(con_local, 'SELECT app_theme FROM settings')[0][0]
        #     self.theme_cls.theme_style = app_theme
        #     app_theme = None
        #     # take the user to the menu screen
        #     kivy.clock.Clock.schedule_once(lambda dt: setattr(self.root, 'current', 'menu'), 2.5)
        #     # self.root.current = 'menu'

    def on_stop(self):
        # close the local database connection
        global con_local
        if con_local:
            con_local.close()
        print('App closed')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_loading_widget()
        
    # def login(self):
    #     username = self.root.get_screen('signin').ids.username.text
    #     password = self.root.get_screen('signin').ids.password.text
    #     if username == "admin" and password == "admin":  # Simple check for demonstration
    #         self.root.current = 'home'
    #     else:
    #         print("Invalid credentials")

    def switch_to_home(self):
        self.root.current = 'home'

    def switch_to_login(self):
        self.root.current = 'signup'
    
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
            global server_url
            # _ = s_r.make_query("http://localhost:8000/login", data={"email": "user@example.com"})
            _ = requests.post(url=server_url+'login', params={"email": email}).json()
            try:
                if _['code'] == 'exists-check-email':
                    # save the user data to the local database
                    # import sql_local as sq_local
                    conn_ = sq_local.create_connection('app.db')
                    sq_local.update_data(conn_, 'users', {'user_id': _['user_id'],'email': email}, {'id': 1})
                    # take the user to the verify OTP screen
                    global user_id
                    user_id = _['user_id']
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
        import requests
        global server_url
        # make a query to the server | signin
        # load modal
        _modal.open()
        def _make_query():
            name = self.root.get_screen('signup').ids.username.text
            email = self.root.get_screen('signup').ids.email.text
            _ = requests.post(url=server_url+'login_or_signup', json={"username": name, "email": email}).json()
            try:
                if _['code'] == 'check-email':
                    # save the user data to the local database
                    # import sql_local as sq_local
                    conn_ = sq_local.create_connection('app.db')
                    sq_local.update_data(conn_, 'users', {'user_id': _['user_id'],'email': email}, {'id': 1})
                    # close the connection
                    conn_.close()
                    global user_id
                    user_id = _['user_id']
                    # take the user to the login screen
                    Clock.schedule_once(lambda dt: setattr(self.root, 'current', 'verify_otp'), 1)
                elif _['detail'] == "Email already exists":
                    # take the user to the login screen
                    Clock.schedule_once(lambda dt: toast("Email already exists", duration=1.5), 0)
                    Clock.schedule_once(lambda dt: setattr(self.root, 'current', 'login'), 1)
            except Exception as e:
                print(f"Exception occurred: {e}")
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
            global user_id
            global _current_screen
            # loading screen
            otp = int(self.root.get_screen('verify_otp').ids.otp.text)
            _ = requests.post(url=server_url+'verify_otp', params={"user_id": user_id, "otp_": otp}).json()
            # close the modal
            _modal.dismiss()
            try:
                # print(_)
                if _['code'] == 'success':
                    # take the user to the login screen
                    Clock.schedule_once(lambda dt: toast("OTP verified", duration=1.5), 0)
                    Clock.schedule_once(lambda dt: setattr(self.root, 'current', _current_screen), 1)
            except Exception as e:
                if _['detail'] == 'Invalid OTP':
                    print("Invalid OTP detected")
                    print(_['detail'])
                    Clock.schedule_once(lambda dt: toast("Invalid OTP", duration=1.5), 0)
                elif _['detail'] == 'Invalid user_id':
                    Clock.schedule_once(lambda dt: toast("Invalid user_id", duration=1.5), 0)
                elif _['detail'] == 'OTP expired':
                    Clock.schedule_once(lambda dt: toast("OTP expired", duration=1.5), 0)
                    # display to the user that the otp has expired
                else:
                    print(_['detail'])
                # print(f"Exception occurred: {e}")
        
        threading.Thread(target=_make_query).start()

    def update_progress_bar(self, dt):
        progress_bar = self.root.get_screen('home').ids.progress_bar
        if progress_bar.value < 100:
            progress_bar.value += 10
        else:
            # self.root.current = 'menu'
            Clock.unschedule(self.update_progress_bar)
            print("Progress bar complete")

    def background_task(self):
        # Clock.schedule_interval(lambda k: self.root.current 'menu' if self.root.get_screen('home').ids.progress_bar.value == 100 else print(k), 0.1)
        for _ in range(10):
            Clock.schedule_once(self.update_progress_bar, 0.3)
            asyncio.run(asyncio.sleep(0.5))  # Simulate a long-running task
            # time.sleep(0.5)
        # else:self.root.current = 'menu'
        if self.root.get_screen('home').ids.progress_bar.value == 100:
            print(self.root.get_screen('home').ids.progress_bar.value)
            Clock.schedule_once(lambda dt: setattr(self.root, 'current', 'menu'), 0.001)

    def on_image_click(self, image_name):
        print(f"{image_name} clicked")
        threading.Thread(target=self.background_task).start()

    def book_appointments(self,appointment:dict):
        #transition into APPOINTMENTS SCREEN
        self.root.current = 'my_apointments'
        #load the spinner | LOADING SCREEN

        #make a POST request to the server
        # ...
        # loading screen
        _modal.open()
        #add appointment to MDList
        _appointments_data.update(appointment)
        threading.Thread(target=lambda : Clock.schedule_once(self.render_appointments,0.1)).start()
        # threading.Thread(target=self.dummy).start()

    # APP ONLY DEVELOPMENT
    def render_appointments(self,dt):
        # query the server for appointments
        import requests
        issue_ = str(self.root.get_screen('book_apointment').ids.issue_desc.text)
        location_ = str(self.root.get_screen('book_apointment').ids.user_location.text)
        phone_ = str(self.root.get_screen('book_apointment').ids.user_phone.text)
        #
        global res_
        res_ = None
        global user_id
        if not user_id:
            Clock.schedule_once(lambda dt: toast("User not logged in", duration=.5), 0)
            # Clock.schedule_once(lambda dt: _modal.dismiss(), 0)
            # return
        def _make_query():
            global res_
            user_id = 'a772963d-f7ac-4a42-a0ed-9ca04c74f41a'
            res_ = requests.post(server_url + "report_issue", json={"issue": issue_, "location": location_, "phone": phone_, "user_id": user_id}).json()
            print(res_)
            try:
                if res_["detail"] == "No available service engineers" :
                    Clock.schedule_once(lambda dt: toast("No available service engineers\ntry agin in few minutes", duration=1.5), 0)
                elif res_["detail"] == "Invalid user_id":
                    print("Invalid user_id")
                    Clock.schedule_once(lambda dt: toast("Invalid user_id", duration=2.5), 2)
            except Exception as e:
                print(e)
                _appointments_data['complaint-id'] = res_['complaintid']
            #
            threading.Thread(target=Clock.schedule_once(_add_appointments,0.1)).start()
        def _add_appointments(dt):
            appointments = _appointments_data
            # the root MDList to add appointments to
            appointments_list = self.root.get_screen('my_apointments').ids.appointments_list
            # appointments = {'complaint-id': '#56608' ,'attd-name': 'NAME_', 'time': '12:00 PM', 'status': 'pending'}
            appointments_list.add_widget(
                TwoLineAvatarIconListItem(
                    IconLeftWidget(
                        icon="clock"
                    ),
                    IconRightWidget(
                        icon="chevron-right"
                    ),
                    text=_appointments_data['complaint-id'],
                    secondary_text=_appointments_data['status'],
                )
            )
            # relese-resources
            appointments_list = None
            # appointments = None
            print("Appointments added\n",res_,phone_)
            threading.Thread(target=self.close_).start()

        # 1. make a query to the server
        threading.Thread(target=_make_query).start()
        # 2. add appointments to the MDList

    def close_(self):
        time.sleep(5)
        _modal.dismiss()


    def _init_loading_widget(self):
        ''' Initialize the loading widget '''
        # init the modal view
        from kivy.uix.modalview import ModalView
        from kivymd.uix.spinner import MDSpinner
        global _modal
        _modal  =   ModalView(size_hint=(.5, .5), auto_dismiss=True, background='', background_color=[0, 0, 0, 0])
        _modal.add_widget(MDSpinner(size_hint=(None, None), size=(46, 46), pos_hint={'center_x': .5, 'center_y': .5},active=True))  # Load and play the GIF


        

MainApp().run()