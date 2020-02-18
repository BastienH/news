"""From downloaded HTML's, gets titles of each page"""

from time import time
from datetime import datetime
import json
from os.path import join

import pandas as pd
from bs4 import BeautifulSoup


class dissect_HTML:
    """
    Extract the required data from an HTML
    Read the HTML files downloaded with get_html and
    Everything found is added in the dictionary ALL_TITLES and dumped in a timestamped JSON file, grouped by source (news site)
    """
    def __init__(self, path, HTML_attributes_source, titles_limit=None):
        self.path = path
        self.soup = str()
        self.HTML_attributes = pd.read_excel(HTML_attributes_source)
        self.titles_limit = titles_limit
        self.ALL_TITLES = {}
        self.ALL_TITLES['header'] = {}


    def get_titles_for_site(self, attributes):
        """
        """
        URL = attributes['URL']
        Name = attributes['Name']
        title_type = attributes['titles_type']
        title_id = attributes['titles_id']
        title_text = attributes['title_text']
        title_text2 = attributes['title_text2']

        self.make_soup(Name)
        assert self.soup != str(), 'No soup to get titles from'

        #Read the column from the sources file that defines the attribute and value for the titles on this specific page.
        title_attrs = {title_type: title_id}
        print(title_attrs)

        all_titles_in_soup = self.soup.find_all(attrs=title_attrs)[:self.titles_limit]
        all_titles_in_soup = [t.strip() for t in all_titles_in_soup]


        #Make sure we get just the title
        for index, title in enumerate(all_titles_in_soup):
            #if several line space in the title_tag's text, we assume we have too many tags inside,
            #so we use the one defined in the source file.
            if '\n\n\n' in title.text:
                print(title.prettify())
                text = title.find_all(title_text)
                if text == []:
                    text = title.find_all(title_text2)

                all_titles_in_soup[index] = text
                print(all_titles_in_soup[index])

        print(f"Titles found for {Name} : {len(all_titles_in_soup)}")

        #Get the URL for each title
        all_titles_and_urls = []
        for tag in all_titles_in_soup:
            path_to_title = self.get_path_for_title(tag)
            title_and_url = (tag.text.strip(), URL+path_to_title) #title_and_url is simply a tuple of the TITLE and the URL
            all_titles_and_urls.append(title_and_url)


        self.ALL_TITLES[Name] = all_titles_and_urls #and we associate each list to the site's Name
        self.ALL_TITLES['header'][Name] = len(all_titles_in_soup)#add a header containing summary information, currently only the number of articles

    def make_soup(self, name):
        path_to_html = join(self.path, name + '.html')
        with open(path_to_html, 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')
        self.soup = soup

    def clean_title(title):
        pass

    def get_path_for_title(tag):
        try :
            path = tag.find_parent('a', href=True)["href"]
        except TypeError:
            try :
                path = tag.find('a', href=True)["href"]
            except TypeError:
                path = str()
        return path

    def get_titles_for_all(self):
        """
        searches for titles and their paths.
        """
        for index, attributes in self.HTML_attributes.iterrows(): #for each site we have referenced
            self.get_titles_for_site(attributes)
        return self.ALL_TITLES



if __name__ == "__main__":
    #Write to JSON file with timestamp
    now = datetime.now()
    now = now.strftime("%Y%m%d_%H%M")

    dissect = dissect_HTML("HTML", "news_sites_and_title_class.xlsx", titles_limit = 2)
    dissect.get_titles_for_all()
    ALL_TITLES = dissect.get_titles_for_all()

    with open(join('JSON', f'titles_{now}.json'), 'w+', encoding='utf-8') as file:
            json.dump(ALL_TITLES, file, indent=2)
            print(f'{file.name} written')
