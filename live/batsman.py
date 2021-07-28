import requests
from bs4 import BeautifulSoup
from  tkinter import *
from tkinter import ttk

root = Tk()
tree = ttk.Treeview(root)
# url = 'https://www.cricbuzz.com/live-cricket-scorecard/31643/aus-vs-ind-3rd-odi-india-tour-of-australia-2020-21'
url = 'https://www.cricbuzz.com/live-cricket-scorecard/30549/ausa-vs-inda-1st-practice-match-india-tour-of-australia-2020-21'
result = requests.get(url)
soup = BeautifulSoup(result.text,'html.parser')

#Innings 1 batsman data
players = []
wicket = []
runs = []
balls = []
data = soup.find_all('div',{'id':'innings_2'})
for main_data in data:
    score = main_data.find('div',{'class':'cb-col cb-col-100 cb-scrd-hdr-rw'})
    a = main_data.find_all('div',{'class':'cb-col cb-col-100 cb-scrd-itms'})
    # batsmans = main_data.find_all('div',{'class':'cb-col cb-col-27'})
    for player_data in a:
        player_name = player_data.find('div',{'class':'cb-col cb-col-27 text-bold'})
        player_name2 = player_data.find('div',{'class':'cb-col cb-col-27'})
        if player_name != None:
            players.append(player_name.text)
            # print(player_name.text)
        if player_name2 != None:
            players.append(player_name2.text)
            # print(player_name2.text)
    
    for wickets in a:
        wickets = wickets.find('div',{'class':'cb-col cb-col-33'})
        if wickets != None:
            wicket.append(wickets.text)
        if wickets == None:
            wicket.append("")
    
    for plyer_run in a:
        plyer_run = plyer_run.find('div',{'class':'cb-col cb-col-8 text-right text-bold'})
        if plyer_run != None:
            # print(plyer_run.text)
            runs.append(plyer_run.text)
        
    for plyer_balls in a:
        plyer_balls = plyer_balls.find('div',{'class':'cb-col cb-col-8 text-right'})
        if plyer_balls != None:
            balls.append(plyer_balls.text)
length = len(players)
# print(length)
print(len(players))
print(players[length-1])
if 'Did not' in players[length-1] or 'Yet to bat' in players[length-1]:
    players = players[:length-1]
    print('ju')
tree['columns'] = ("Batsman","wicket","Runs","Balls")

tree.column("#0",width=0)
tree.column("Batsman",anchor=W,width=50)
tree.column("wicket",anchor=W)
tree.column("Runs",anchor=W)
tree.column("Balls",anchor=W)

tree.heading("#0",text="")
tree.heading("Batsman",text="Batsman",anchor=W)
tree.heading("wicket",text="",anchor=W)
tree.heading("Runs",text="Runs",anchor=W)
tree.heading("Balls",text="Balls",anchor=W)

for i in range(len(players)):
    tree.insert('',END,i,values=(players[i],wicket[i],runs[i],balls[i]))

tree.pack(expand=True,fill=BOTH)

root.mainloop()