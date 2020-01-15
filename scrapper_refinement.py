import pandas as pd
import json
import os.path
pjoin = os.path.join
from bs4 import BeautifulSoup

df = pd.read_excel("news_sites_and_title_class.xlsx")

ALL_TITLES = {}
ALL_TITLES['header'] = {}

for index, row in df.iterrows(): #for each site we have referenced
    URL = row['URL']
    
    with open(pjoin("HTML", f"{row['Name']}.html"), 'r', encoding='utf-8') as f:
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
