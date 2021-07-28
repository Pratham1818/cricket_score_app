from bs4 import BeautifulSoup
import requests
from tkinter import *

root = Tk()
root.geometry("900x600")
root.resizable(0,0)

f1 = Frame(root)
f1.pack()

lst = Listbox(f1,width=500)
lst.pack()

url = 'https://www.cricbuzz.com/live-cricket-scores/30555/2nd-test-india-tour-of-australia-2020-21'
result= requests.get(url)
soup = BeautifulSoup(result.text,'html.parser')

commenterys = soup.find_all('div',{'class':'cb-col cb-col-100'})
for i in commenterys:
    if i != None:
        lst.insert(END,i.text)

# key_stats = soup.find('div',{'class':'cb-col cb-col-33 cb-key-st-lst'})
# lst.insert(0,key_stats.text)

live_score = soup.find_all('div',{'class':'cb-col cb-col-67 cb-scrs-wrp'})
for i in live_score:
    lst.insert(0,i.text)
    lst.configure(font='lucida 10 bold')
    # print(i.text)


root.mainloop()