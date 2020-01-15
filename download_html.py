"""Downloads the HTML of all sites referenced"""

from bs4 import BeautifulSoup
from datetime import datetime
from os.path import join
import pandas as pd
from time import time


import sys
#sys.path.insert(1, r"C:\Users\NG8203C\Desktop\CodeBase\Scripts")
#from secret import proxies
import requests_html as req
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


#Connect to "database"
df = pd.read_excel("news_sites_and_title_class.xlsx")


#Setup sites connection
headers = {"USER_AGENT" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"}
session = req.HTMLSession()

def get_html():
    for index, row in df.iterrows():
        start = time()        
        URL = row['URL']        
        #Connection
        #r = session.get(URL, proxies=proxies, verify=False)
        #We try to connect to the site
        try:
            r = session.get(URL, verify=False)
        #If it doesn't work, we just go to the next site.
        except ConnectionError as r:
            continue

        time4request = time() - start
        print(f"connection to {URL} executed in : {round(time4request, 4)}")

        soup = BeautifulSoup(r.content, "html.parser")
        soup = soup.prettify()

        with open(join("HTML", f"{row['Name']}.html"), 'a+', encoding='utf-8') as f:
            f.write(soup)

