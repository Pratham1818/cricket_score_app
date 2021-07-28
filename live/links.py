from bs4 import BeautifulSoup
import requests

url = 'https://www.cricbuzz.com/cricket-match/live-scores'

result = requests.get(url)
soup = BeautifulSoup(result.text,'html.parser')
matches = soup.find_all('div',{'class':'cb-mtch-lst cb-col cb-col-100 cb-tms-itm'})
match_links = {}
for i in matches:
    team_name = i.find('h3').text
    link = i.find('nav')
    link = link.find('a',{'title':'Scorecard'})
    if link != None:
        link = link.get('href')
        link = 'https://www.cricbuzz.com' + link
        match_links[team_name] = (link)

print(match_links)