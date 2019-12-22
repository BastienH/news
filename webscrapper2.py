#Gets all titles from URL and prints to new file

import os.path
pjoin = os.path.join

import requests_html as req
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import pandas as pd

from time import time
from bs4 import BeautifulSoup


import sys
sys.path.insert(1, r"C:\Users\NG8203C\Desktop\CodeBase\Scripts")
from secret import proxies


#Connect to "database"
df = pd.read_excel("news_sites_and_title_class.xlsx")


#Setup sites connection
headers = {"USER_AGENT" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"}
session = req.HTMLSession()

all_titles = {}

def get_html():
    for index, row in df.iterrows():
        start = time()        
        URL = row['URL']        
        #Connection
        r = session.get(URL, proxies=proxies, verify=False)
        time4request = time() - start
        print(f"connection to {URL} executed in : {round(time4request, 4)}")

        soup = BeautifulSoup(r.content, "html.parser")
        soup = soup.prettify()

        with open(pjoin("HTML", f"{row['Name']}.html"), 'a+', encoding='utf-8') as f:
            f.write(soup)

def parse_html():
    for index, row in df.iterrows():
        URL = row['URL']
        
        with open(pjoin("HTML", f"{row['Name']}.html"), 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')

        #Here we read the column from the Excel file that defines the attribute and value for the titles on this specific page.
        urlsTitle_List = soup.find_all(attrs={f"{row['titles_type']}": f"{row['titles_id']}"})
        print(f"Titles found for {row['Name']} : {len(urlsTitle_List)}")

        urlTitleLink_List = []
        
        for tag in urlsTitle_List:
            try :
                link = tag.find_parent('a', href=True)["href"]
            except TypeError:
                try :
                    link = tag.find('a', href=True)["href"]
                except TypeError:
                    link = str()
                
            relation = (tag.text.strip(), URL+link)
            urlTitleLink_List.append(relation)

        all_titles[row['Name']] = urlTitleLink_List
        
        print(f"All titles in {row['Name']} : ", all_titles[row['Name']])

parse_html()

"""c = 0
for i in all_titles_list:
        if c < 10:
                print(i.text)
                print(i.find("a", href=True)["href"])
                print("====================")
        else:
                pass
        c += 1"""



	
