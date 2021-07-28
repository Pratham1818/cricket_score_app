import requests
from bs4 import BeautifulSoup
from  tkinter import *
from tkinter import ttk

root = Tk()
tree = ttk.Treeview(root)

url = 'https://www.cricbuzz.com/live-cricket-scorecard/31643/aus-vs-ind-3rd-odi-india-tour-of-australia-2020-21'

result = requests.get(url)
soup = BeautifulSoup(result.text,'html.parser')

# class="cb-col cb-scrcrd-status cb-col-100 cb-text-live ng-scope"
#match info 
details = soup.find_all('div',{'class':'cb-nav-main cb-col-100 cb-col cb-bg-white'})
# cb-col cb-scrcrd-status cb-col-100 cb-text-live
for i in details:
    head = i.find('h1',{'class':'cb-nav-hdr cb-font-18 line-ht24'})
    print(head.text)
    detail = i.find('div',{'class':'cb-nav-subhdr cb-font-12'})
    print(detail.text)
    
live_stat = soup.find('div',{'class':'cb-col cb-scrcrd-status cb-col-100 cb-text-complete'})
print(live_stat)
head_lst = []
details_lst = []

data = soup.find_all('div',{'class':'cb-col cb-col-100'})
for data in data:
    head = data.find_all('div',{'class':'cb-col cb-col-27'})
    for head in head:
        if head != None:
            head_lst.append(head.text)

    details = data.find_all('div',{'class':'cb-col cb-col-73'})
    for details in details:
        details_lst.append(details.text)

tree['columns'] = ("1st","2nd")

tree.column("#0",width=0)
tree.column("1st",anchor=W,width=50)
tree.column("2nd",anchor=W)

tree.heading("#0",text="")
tree.heading("1st",text="",anchor=W)
tree.heading("2nd",text="",anchor=W)

for i in range(len(head_lst)):
    tree.insert('',END,i,values=(head_lst[i],details_lst[i]))

tree.pack(expand=True,fill=BOTH)

root.mainloop()