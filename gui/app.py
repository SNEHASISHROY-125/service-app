from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFlatButton
# import kivymd.uix.

KV = '''
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
                box_color: 1, 1, 1, .2
                source: "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2F2.bp.blogspot.com%2F-8DL1_7b-4h4%2FUhNloO6amvI%2FAAAAAAAAAcU%2Fj-ZgMSBMmg4%2Fs1600%2Flord%2Bkrishna%2Bfull%2Bscreen%2Bwallpaper.jpg&f=1&nofb=1&ipt=8360efe24ba6ad51243d6ddcd7de06f98374a6e83945c8e44a35146aa3ca7a77&ipo=images"
                pos_hint: {"center_x": .5, "center_y": .5}
                
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
    
        
'''

class Example(MDApp):
    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

Example().run()