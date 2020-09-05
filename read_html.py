from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
import pkl_functions

def parse_html(URL):
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def read_RUV():
    filename = 'RUV.pkl'
    #pkl_functions.create_pkl(filename, {"data_frame": pd.DataFrame({"url":[],"dated":[],"title":[],"text":[]})})
    ruv_df = pkl_functions.read_pkl(filename)
    URL ='https://www.ruv.is/english?page='    
    for i in range(20):
        n = ruv_df.shape[0]
        soup = parse_html(URL + str(i))
        content = soup.find("div",{"id": "content"}).find("div",{"class":"view-content"})
        links_sources = content.findAll("strong",{"class":"article-summary-link"})
        for link_source in links_sources:
            new_url = 'https://www.ruv.is' + link_source.find("a").get("href")
            if new_url not in ruv_df['url'].to_list():
                new_soup = parse_html(new_url)
                new_content = new_soup.find("div",{"id": "mini-panel-body_and_author"})
                title = new_content.find("h1",{"class":"line-height1"}).text.strip()
                published = new_soup.find("div",{"class":"publish-time"}).text.strip().split()[0]
                dated = datetime.strptime(published, '%d.%m.%Y')
                field_items = new_soup.find("div",{"class":"region-two-66-33-first"}).findAll("div",{"class":"field-items"})
                text = ''
                for item in field_items:
                    text += item.text.replace("Click to follow RÚV English on Facebook.", "").strip() + "\n"
                article_df = pd.DataFrame({"url":[new_url],"dated":[dated],"title":[title],"text":[text]})
                ruv_df = pd.concat([ruv_df, article_df], ignore_index = False)
        ruv_df = ruv_df.reset_index(drop = True)
        pkl_functions.update_pkl(ruv_df, filename)
        if ruv_df.shape[0] - n == 0:
            break
        
if __name__ == "__main__":
    read_RUV()
            
    
