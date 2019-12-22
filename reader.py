"""Here we make a cross platform application to read articles from any determined source
This includes : 
a Front-Page, with a highligh article (La Une) 

some "KPI"
A search
Reading : a Menu to access all articles currently up
Monitoring : a check to see which sites are up and which are down
Communication : a way to send an communication to all these sites... an email?
"""
import os
os.environ['KIVY_HOME'] = os.path.dirname(__file__)

import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout   # one of many layout structures
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, StringProperty, NumericProperty

from database import data



class TheMain(App):
        """Contains all common elements to all pages : 
        ScreenManager, style, credits, Header(togglable)"""
        def build(self):
                sm = ScreenManager()
                sm.add_widget(FrontPage(name="FrontPage"))
                sm.add_widget(SummaryPage(name="SummaryPage"))
                #sm.add_widget(ArticleBehavior)
                return sm

class FrontPage(GridLayout, Screen):
        """Entry point to the app :
        Get the latest article from the favorite news site, or random?
        Shows if sites are up/down/changed/lastSync"""
        
        search_input = ObjectProperty(None)
        search_button = ObjectProperty(None)
        summary_button = ObjectProperty(None)
        
        def __init__(self, **kwargs):
                super(FrontPage, self).__init__(**kwargs)

                """self.cols = 1

                self.add_widget(Label(text='Custom News'))

                self.add_widget(Label(text='La Une'))

                self.summary = Button(text='Summary')
                self.summary.bind(on_press=self.changer)
                self.add_widget(self.summary)

                self.add_widget(Label()) #Empty

                self.search = Button(text="Search")
                self.search.bind(on_press=self.search_function)
                self.search = TextInput(multiline=False)
                self.add_widget(self.search)

                self.add_widget(Label(text='Status'))
                """
        def search(self, search_input, *args):
                self.search_button.text = "Got searched"
                print(self.search_input.text)
        
        def changer(self, *args):
                print("changing")
                self.manager.current = 'SummaryPage'

"""class ArticleBehavior(ButtonBehavior):
        def __init__(self, **kwargs):
                super(ArticleBehavior, self).__init__(**kwargs)
                self.source = 'atlas://data/images/defaulttheme/checkbox_off'

        def on_press(self):
                self.source = 'atlas://data/images/defaulttheme/checkbox_on'

        def on_release(self):
                self.source = 'atlas://data/images/defaulttheme/checkbox_off'"""


class SummaryPage(GridLayout, Screen):
        """the list of articles scrapped.
        With option to group by ['Source', 'Keyword', 'Date', 'Author?']
        That's like a table 
        ["Source", "Datetime",
        "Title", "Image", 
        "Extract"],
        [Next] """
        def __init__(self, **kwargs):
                super(SummaryPage, self).__init__(**kwargs)
                
                self.cols = 1
                
                for i, d in enumerate(data["Lundi.am"][:10]):
                        name = f'{i}'
                        text = f'[ref={d[1]}]{d[0]}[/ref]'
                        self.reference = Label(text=text, markup=True, on_ref_press=self.browser)
                        self.add_widget(self.reference)        
       

        def changer(self, *args):
                print("changed")
                self.manager.current = "FrontPage"

        def browser(self, *args):
                import webbrowser
                webbrowser.open(args[1])



class UpdateSource(Button):
        def __init__(self, source, **kwargs):
                source = self.source


if __name__ == "__main__":
    TheMain().run()
