import os
import re
import json
import time
import base64
import requests
import logging
from urllib.request import urlopen

from datetime import datetime
from bs4 import BeautifulSoup
from datetime import datetime

def get_html(url):
    res = requests.get(url)
    if res.status_code == 200:
        return res.content
    else:
        return None

def jst_str2ts_epoch_milli(jst, format="%Y-%m-%d %H:%M:%S"):
    dt = datetime.strptime(jst + "+0900", format + "%z")
    ts = dt.timestamp() * 1000
    return ts
    
def extract_recent_link(html):
    soup = BeautifulSoup(html, 'html.parser')
    novels = soup.findAll('div', class_='section novels content-block')
    links = [n.find('h2', class_='title').find('a').get('href') for n in novels]
    return links
    
    
def remove_duplicated_link(links, lastkey, default=False):
    idx = links.index(lastkey) if lastkey in links else default
    return links[:idx]
    
    
def lambda_handler(event, context):
    url = event['url']
    lastkey = event['lastkey']
    html = get_html(url).decode('utf-8')
    links = extract_recent_link(html)
    links = remove_duplicated_link(links, lastkey, len(links))
    if len(links) > 0:
        lastkey = links[0]
    return {
        'statusCode': 200,
        'pkey': event['pkey'],
        'skey': event['skey'],
        'lastkey': lastkey,
        'links': links
    }
