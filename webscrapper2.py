"""From downloaded HTML's, gets titles of each page"""

from time import time
from datetime import datetime
import json
from os.path import join

import pandas as pd
from bs4 import BeautifulSoup

#Connect to "database"
df = pd.read_excel("news_sites_and_title_class.xlsx")

def get_titles(limit_n_of_titles=2):
    """Read the HTML files downloaded with get_html and searches for titles and their links.
Everything found is added in the dictionary ALL_TITLES and dumped in a timestamped JSON file, grouped by source (news site)"""
    ALL_TITLES = {}
    ALL_TITLES['header'] = {}

    for index, row in df.iterrows(): #for each site we have referenced
        URL = row['URL']

        with open(join("HTML", f"{row['Name']}.html"), 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')

        #Here we read the column from the Excel file that defines the attribute and value for the titles on this specific page.
        all_titles_in_soup = soup.find_all(attrs={f"{row['titles_type']}": f"{row['titles_id']}"})[:limit_n_of_titles]
        print(f"Titles found for {row['Name']} : {len(all_titles_in_soup)}")

        all_titles_and_urls = []

        #here we just get the URL for each title
        for tag in all_titles_in_soup:
            try :
                link = tag.find_parent('a', href=True)["href"]
            except TypeError:
                try :
                    link = tag.find('a', href=True)["href"]
                except TypeError:
                    link = str()

            title_and_url = (tag.text.strip(), URL+link) #title_and_url is simply a tuple of the TITLE and the URL
            all_titles_and_urls.append(title_and_url)

        ALL_TITLES[row['Name']] = all_titles_and_urls #and we associate each list to the site's Name
        ALL_TITLES['header'][row['Name']] = len(all_titles_in_soup)#add a header containing summary information, currently only the number of articles

        #Write to JSON file with timestamp
        now = datetime.now()
        now = now.strftime("%Y%m%d_%H%M")


    with open(join('JSON', f'titles_{now}.json'), 'w+', encoding='utf-8') as file:
            json.dump(ALL_TITLES, file, indent=2)
            print(f'{file.name} written')


"""c = 0
for i in ALL_TITLES_list:
        if c < 10:
                print(i.text)
                print(i.find("a", href=True)["href"])
                print("====================")
        else:
                pass
        c += 1"""

if __name__ == '__main__':
    get_titles()
