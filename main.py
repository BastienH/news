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
os.environ['KIVY_HOME'] = os.path.dirname(__file__) # To run on Windows
from getpass import getuser
if getuser == 'bast':
    os.environ['KIVY_HOME'] = os.path.dirname('/Applications/Kivy.app/') # To run on Mac

os.environ['KIVY_TEXT'] = 'pil'


import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout   # one of many layout structures
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, StringProperty, NumericProperty

from download_html import get_html
import webscrapper2
from database import *

data, header = open_recent_data()

class TheMain(App):
        """Contains all common elements to all pages :
        ScreenManager, style, credits, Header(togglable)"""
        def build(self):
                sm = ScreenManager()
                sm.add_widget(FrontPage(name="FrontPage"))
                sm.add_widget(SummaryPage(name="SummaryPage"))
                sm.add_widget(SitesStatusPage(name="SitesStatusPage"))
                #sm.add_widget(ArticleBehavior)
                return sm

class FrontPage(GridLayout, Screen):
        """Entry point to the app :
        Get the latest article from the favorite news site, or random?
        Shows if sites are up/down/changed/lastSync"""

        search_input = ObjectProperty(None)
        search_button = ObjectProperty(None)
        summary_button = ObjectProperty(None)
        sites_status_button = ObjectProperty(None)
        refresh_button = ObjectProperty(None)

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

        def changer(self, *args, target=None):
                print(f"changing to {target} ")
                self.manager.current = str(target)

        def refresh_all(self, *args):
                print("refreshing")
                #get_html()
                import get_titles
                data, header = open_recent_data()
                #SummaryPage.clear_widgets(SummaryPage)
                SummaryPage.load_titles_to_page(SummaryPage)
                print("refreshed")

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

        front_page_button = ObjectProperty(None)

        def __init__(self, **kwargs):
                super(SummaryPage, self).__init__(**kwargs)
                self.cols = 1
                self.load_titles_to_page(self)

        def load_titles_to_page(self, *args):
                self.scroll_view = ScrollView()
                self.TitlesLayout = GridLayout(cols = 1,
                                          #rows = 50,
                                          #spacing = 25,
                                          size_hint=(1,None),
                                          )

                #display all titles available for all sites
                index = 0
                data, _ = open_recent_data()
                for site in data.keys():
                        #create a label for each title found
                        for i, d in enumerate(data[site]):
                                if d == "":
                                        continue
                                name = f'{i}'
                                text = f'[ref={d[1]}]{d[0]}[/ref]'
                                self.reference = Label(text=text,
                                                       markup=True,
                                                       on_ref_press=self.browser,
                                                       #text_size = TitlesLayout.size,
                                                       #halign = 'left',
                                                       #valign = 'center',
                                                       #strip = True,
                                                       )
                                self.TitlesLayout.add_widget(self.reference, index=index)
                                index +=1
                                print(self.reference.text, index, sep="\t")
                #self.load_titles_to_page()
                #self.TitlesLayout.bind(minimum_height=self.setter('height'))

                #Back to "Menu"/Front Page
                self.menu_btn = Button(text="Front Page")
                self.menu_btn.bind(on_press=lambda x: self.changer(target="FrontPage"))
                self.TitlesLayout.add_widget(self.menu_btn)
                self.scroll_view.add_widget(self.TitlesLayout)
                #self.add_widget(self.scroll_view)


        def changer(self, *args, target=None):
                print(f"changing to {target} ")
                self.manager.current = str(target)

        def browser(self, *args):
                import webbrowser
                webbrowser.open(args[1])


class UpdateSource(Button):
        def __init__(self, source, **kwargs):
                source = self.source


class SitesStatusPage(GridLayout, Screen):
        """ here we try to mix up grids with 1 and 2 cols.
        Each Site Button should display the site name and a refresh button next to it"""
        def __init__(self, **kwargs):
                super(SitesStatusPage, self).__init__(**kwargs)

                self.cols = 2
                configured_sites = data.keys()
                self.sites = []
                self.refresh_btns = []
                for site in configured_sites:
                        #Add "ButtonGrid"
                        self.site_box = GridLayout()
                        self.site_box.cols = 2

                        #Add site name
                        name = site
                        text = f'[ref={site}]{site}[/ref]'
                        self.site_box.reference = Label(text=text, markup=True, on_ref_press=self.browser)

                        #Add refresh button to each reference -currently adds a general refresh button
                        self.site_box.reference.refresh_site_status_btn = Button()
                        self.site_box.reference.refresh_site_status_btn.refresh_logo = Image(source=os.path.join("icon", "refresh_logo.png"))
                        self.site_box.reference.refresh_site_status_btn.add_widget(self.site_box.reference.refresh_site_status_btn.refresh_logo)
                        self.site_box.reference.refresh_site_status_btn.bind(on_press=lambda x: self.refresh_site_status(site=site))

                        self.site_box.reference.add_widget(self.site_box.reference.refresh_site_status_btn)
                        self.add_widget(self.site_box.reference)

        def changer(self, *args, target=None):
                print(f"changing to {target} ")
                self.manager.current = str(target)

        def browser(self, *args):
                import webbrowser
                webbrowser.open(args[1])

        def refresh_site_status(self, *args, site=""):
                print(f"refreshing {site}")

if __name__ == "__main__":
    TheMain().run()
