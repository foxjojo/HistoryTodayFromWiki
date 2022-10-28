from distutils.spawn import spawn
from importlib.resources import files
from os import write
import requests
import bs4
import io
import sys
import csv
import time
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52',

}
error = open("error.txt", "w", encoding="utf-8-sig")

csvfile = open('history.csv', 'w', newline='', encoding="utf-8-sig")
spamwriter = csv.writer(csvfile)


def GetAllDayUrl():
    # class="nowraplinks collapsible autocollapse navbox-inner"
    html = requests.get(
        "https://zh.wikipedia.org/wiki/10%E6%9C%8827%E6%97%A5", headers=headers)

    bs = bs4.BeautifulSoup(html.text, 'html.parser')
    data = bs.find_all('div', style="padding:0em 0.25em")
    for div in data:
        for li in div.find_all('li'):
            if li.a != None and li.a.has_attr('href') and li.a.has_attr('title'):
                url = 'https://zh.wikipedia.org' + li.a['href']
                day = li.a['title']
                print(day+url)
                GetOneDayData(url, day)
    csvfile.close()
    error.close()


def GetOneDayData(url, day):
    time.sleep(2)
    try:

        html = requests.get(url, headers=headers)
        html.encoding = 'utf-8'
        bs = bs4.BeautifulSoup(html.text, 'html.parser')
        # data = bs.find(
        #    'div', class_="mw-parser-output").find_all(['h2', 'h3', 'ul'], recursive=False)
        data = bs.find('div', id="bodyContent").find(
            'div', class_="mw-body-content mw-content-ltr").div
        data = data.find_all(['h2', 'h3', 'ul'], recursive=False)
        h2 = ''
        h3 = ''
        ul = ''
        i = 1
        for item in data:
            if item.name == 'h2':
                h2 = item.get_text()
                # print(item.get_text())
            if item.name == 'h3':
                h3 = item.get_text()
                # print(item.get_text())
            if item.name == 'ul':
                for li in item.find_all('li'):
                    ul = li.get_text()
                    desc = day + h2+' '+h3+' '+ul
                    i = 2
                    print(desc)
                    spamwriter.writerow([day, h2, h3, ul])
        if i == 1:
            print('错误'+url)
            error.write(url+'\n')
            error.flush()
    except:
        print('错误'+url)
        error.write(url+'\n')


GetAllDayUrl()
