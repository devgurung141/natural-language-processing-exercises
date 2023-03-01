import requests
import os
import json

from bs4 import BeautifulSoup


def get_blog_articles(url):
    
    '''takes in url, returns a list with a dictionary containing title and content of each article'''
    file = 'blog_articles.json'
    if os.path.exists(file):
        with open(file) as f:
            return json.load(f)
        
    headers = {'User-Agent': 'Codeup Data Science'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    article_links = soup.find_all('a', class_='more-link')
    lists = [] 
    
    for element in article_links:
        url = element['href']
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        dicts = {'title': soup.h1.text, 
                 'content':soup.find('div', class_ = 'entry-content').text}
        lists.append(dicts )
    with open(file, 'w') as f:
        json.dump(lists,f)
        
    return lists


def get_news_articles(topics):
    '''takes in a list of topic and return a list with category , title, and content'''
        
    file = 'news_articles.json'
    
    if os.path.exists(file):
        with open(file) as f:
            return json.load(f)
        
    base_url = 'https://inshorts.com/en/read/'
     
    lists = []

    for topic in topics:
        
        response = requests.get(base_url + topic)

        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find_all('span', itemprop='headline')

        content = soup.find_all('div', itemprop='articleBody')

        for i in range(len(title)):

            temp_dict = {'category': topic,
                         'title': title[i].text,
                         'content': content[i].text}

            lists.append(temp_dict)
            
    with open(file, 'w') as f:
        json.dump(lists,f)

    return lists   