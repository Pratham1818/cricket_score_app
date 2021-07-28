import requests
from bs4 import BeautifulSoup
import pandas as pd
from  tkinter import *
from tkinter import ttk

root = Tk()
tree = ttk.Treeview(root)

url = 'https://www.cricbuzz.com/live-cricket-scorecard/31643/aus-vs-ind-3rd-odi-india-tour-of-australia-2020-21'
result = requests.get(url)
soup = BeautifulSoup(result.text,'html.parser')

#bowling data
name_lst = []
wickets_lst = []
stats2 = []
data = soup.find_all('div',{'id':'innings_2'})
for main_data in data:
    #players_name 
    names = main_data.find_all('div',{'class':'cb-col cb-col-40'})
    for player_name in names:
        player_name = player_name.find('a')
        if player_name != None:
            name_lst.append(player_name.text)

    stats = main_data.find_all('div',{'class':'cb-col cb-col-100 cb-ltst-wgt-hdr'})
    stats2.append(stats[1])
    for i in stats2:
        wicket = i.find_all('div',{'class':'cb-col cb-col-8 text-right text-bold'})
        for a in wicket:
            wickets_lst.append(a.text)

tree['columns'] = ("player name","Wicket")

tree.column("#0",width=0)
tree.column("player name",anchor=W,width=50)
tree.column("Wicket",anchor=W)

tree.heading("#0",text="")
tree.heading("player name",text="Bowler",anchor=W)
tree.heading("Wicket",text="Wickets",anchor=W)

for i in range(len(name_lst)):
    tree.insert('',END,i,values=(name_lst[i],wickets_lst[i]))

tree.pack(expand=True,fill=BOTH)

root.mainloop()