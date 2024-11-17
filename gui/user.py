'''
User-UI
'''
from kivymd.app import MDApp
from kivymd.uix.list import TwoLineAvatarIconListItem, OneLineAvatarListItem, IconLeftWidget, IconRightWidget
from kivymd.uix.dialog import MDDialog
import kivymd.utils.asynckivy as ak
from kivymd.uix.button import MDFlatButton
from kivy.lang import Builder
from kivymd.toast import toast as tst
from kivy.utils import platform
import threading
from kivy.properties import StringProperty

def toast(text:str, duration=1.0):
    if platform == 'android':
        tst(text, duration)
    else:
        tst(text, duration=duration)


class Item(OneLineAvatarListItem):
    # divider = None
    source = StringProperty()

class TwoLineAvatarIconListItem(TwoLineAvatarIconListItem):
    # divider = None
    source = StringProperty()
    complaint_id = StringProperty()

class FAPP(MDApp):
    user_id: str = "0ef59067-6cc5-447a-8d4c-21e50577958d"

    def build(self):
        return Builder.load_file('gui/user.kv')
    
    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label,):
        screen = self.root.get_screen('services')
        if instance_tab.name == 'appointments_tab':
            screen.ids.top_app_bar.title = "My Appointments"
        else:
            screen.ids.top_app_bar.title = "All Services"
        print(instance_tab.name)
    
    def render_appointment(self , *args):
        import requests
        from kivy.clock import Clock
        from kivymd.toast import toast
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
            engineers_list = self.root.get_screen("services").ids.appointments_list
            print(engineers_list.children)
            #
            # engineers_list.clear_widgets()
            # print(engineers_list.children)
            # Logic to match list items with the engineers
            if len(engineers_list.children) < len(_complaints['complaint_list']):
                for i in range(len(_complaints['complaint_list']) - len(engineers_list.children)):
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

    def book_appointment(self, data:dict,*args):
        print(data)
        global _modal
        _modal.open()
        def _query():
            # check data is not empty
          
            if not data['issue_desc'] or not data['user_location'] or not data['user_phone']:
                return
            import requests
            from kivy.clock import Clock
            import time
            server_url = "https://chat-app.fudemy.me/"
            global _complaints
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
            if _complaints:
                Clock.schedule_once(lambda dt: toast('your appointment booked',1),0.1)
                Clock.schedule_once(lambda x: self.render_appointment(), 0.1)
                #
                Clock.schedule_once(lambda x: setattr(self.root , 'current' ,'services') , .1)
                Clock.schedule_once(lambda x: setattr(self.root.get_screen('services').ids.top_app_bar , 'title' , "All Services"), .1)
                _modal.dismiss()
        threading.Thread(target=_query).start()

    def on_start(self):
        # 1
        self._init_loading_widget()
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

    def _init_loading_widget(self):
        ''' Initialize the loading widget '''
        # init the modal view
        from kivy.uix.modalview import ModalView
        from kivymd.uix.spinner import MDSpinner
        global _modal
        _modal  =   ModalView(size_hint=(.5, .5), auto_dismiss=False, background='', background_color=[0, 0, 0, 0])
        _modal.add_widget(MDSpinner(size_hint=(None, None), size=(46, 46), pos_hint={'center_x': .5, 'center_y': .5},active=True))  # Load and play the GIF
    


FAPP().run()