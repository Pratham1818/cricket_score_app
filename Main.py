from tkinter import *
import json
import requests
from bs4 import BeautifulSoup
from PIL import Image,ImageTk
import tkinter.messagebox as msgbox
from tkinter import ttk
import webbrowser

#variables for app and link and html parser
screen_width = 900
screen_height = 600
menubutton_x = screen_width/2 - 100
menubutton_y = 80
pos_x = 10
pos_y = 60
# main window
root = Tk()
root.geometry("900x600")
root.resizable(0,0)
root.iconbitmap('Data\icon.ico')
root.title('Cric Scorer')

#importing images
bg_img = Image.open('Data\\background.png').resize((screen_width,screen_height))
bg_img = ImageTk.PhotoImage(bg_img)

bg_live = Image.open('Data\\bg2.png').resize((screen_width,screen_height+100))
bg_live = ImageTk.PhotoImage(bg_live)

bg_frame = Image.open('Data\\bg3.png').resize((700,400))
bg_frame = ImageTk.PhotoImage(bg_frame)

startbtn_img = Image.open('Data\Frame.png')
startbtn_img = ImageTk.PhotoImage(startbtn_img)
livematchimg = Image.open('Data\Live match.png').resize((180,70))
livematchimg = ImageTk.PhotoImage(livematchimg)
upcomingimg = Image.open('Data\\Upcoming Match.png').resize((180,70))
upcomingimg = ImageTk.PhotoImage(upcomingimg)
previousimg = Image.open('Data\previous match.png').resize((180,70))
previousimg = ImageTk.PhotoImage(previousimg)
    
def start_data(): 

    startbtn.destroy()
    livematchbtn = Button(root,text='Livematch',image=livematchimg)
    livematchbtn.bind('<Button-1>',matches_result_nd_live)
    livematchbtn.place(x=menubutton_x,y=menubutton_y)

    upcoming_matchbtn = Button(root,image=upcomingimg,command=fixtuers_match)
    upcoming_matchbtn.place(x=menubutton_x,y=menubutton_y+100)

    previous_matchbtn = Button(root,text='match result',image=previousimg)
    previous_matchbtn.place(x=menubutton_x,y=menubutton_y+200)
    previous_matchbtn.bind('<Button-1>',matches_result_nd_live)

def search():
    try:
        #Fixtuers Matches data
        match = match_lst.get(ANCHOR)
        data = fixtuers
        data = data[match]
        print(data)
        team1 = data['Team 1']
        team2 = data['Team 2']
        date = data['Date']
        summary = data['Match Info']

        search_root = Toplevel(root)
        search_root.title(match)
        search_root.iconbitmap('Data\icon.ico')
        search_root.geometry('580x380')
        search_root.config(bg='black')
        search_root.resizable(0,0)

        scrlbary = Scrollbar(search_root)
        scrlbary.pack(side=LEFT,fill=Y)
        scrlbarx = Scrollbar(search_root,orient=HORIZONTAL)
        scrlbarx.pack(side=BOTTOM,fill=X)

        search_list = Listbox(search_root,width=50,font="lucida 15 bold",bg='black',fg='white',yscrollcommand=scrlbary.set,xscrollcommand=scrlbarx.set)
        search_list.place(x=20,y=10)
        scrlbary.config(command=search_list.yview)
        scrlbarx.config(command=search_list.xview)

        while True:
            search_list.insert(END,"Teams:")
            search_list.insert(END,f"{team1} Vs {team2}")
            search_list.insert(END,"________________________________________________________________________")
            search_list.insert(END,"Match Date:")
            search_list.insert(END,date)
            search_list.insert(END,"________________________________________________________________________")
            search_list.insert(END,"Summary:")
            search_list.insert(END,summary)
            search_list.insert(END,"________________________________________________________________________")
            break
        
    except Exception as e:
        print(e)
        msgbox.showerror(title="Error",message="There Was Sonmenthing Problem. We Can not connact with Database!!")
     
def matches_result_nd_live(event):
    btn = event.widget.cget(("text"))
    match_links = {}
    live_team = []
    pading = 15
    result_root = Toplevel(root)
    result_root.geometry('900x600')
    result_root.resizable(0,0)
    result_root.iconbitmap('Data\icon.ico')

    bg = Label(result_root,image=bg_live)
    bg.place(x=0,y=0)
    url = 'https://www.cricbuzz.com/cricket-match/live-scores'
    if btn == 'match result':
        url = 'https://www.cricbuzz.com/cricket-match/live-scores/recent-matches'
    result = requests.get(url)
    soup = BeautifulSoup(result.text,'html.parser')
    matches = soup.find_all('div',{'class':'cb-mtch-lst cb-col cb-col-100 cb-tms-itm'})

    for i in matches:
        team = i.find('h3').text
        match_type = i.find('span',{'class':'text-gray'}).text
        team_name = team + match_type
        link = i.find('nav')
        link = link.find('a',{'title':'Scorecard'})
        if link != None:
            link = link.get('href')
            link = 'https://www.cricbuzz.com' + link
            live_team.append(team_name)
            match_links[team_name] = (link)


    def matches_btn(event):
        # live match window
        live_root = Toplevel(result_root)
        live_root.geometry("900x600")
        live_root.resizable(0,0)
        team = event.widget.cget(("text"))
        live_root.title(team+' Match Report')
        bg = Label(live_root,image=bg_img).place(x=0,y=0)

        # match data fatching from website
        match_url = match_links[team]
        result = requests.get(match_url)
        soup = BeautifulSoup(result.text,'html.parser')

        # style for table
        style = ttk.Style()
        style.theme_use('alt')
        style.configure('Treeview',font='calberia 10 bold',rowheight=25)
        style.configure('Treeview.Heading',font='lucida 15 bold')
        #match information function
        def match_info():
            frame = Frame(live_root,borderwidth=10,relief=SUNKEN,width=720,bg='black',height=400)
            label = Label(frame,image=bg_frame).place(x=0,y=0)
            frame.place(x=10,y=100)
            frame.pack_propagate(0)
                
            details = soup.find_all('div',{'class':'cb-nav-main cb-col-100 cb-col cb-bg-white'})

            head_lst = []
            details_lst = []

            scrlbar_y = Scrollbar(frame)
            scrlbar_y.pack(fill=Y,side=LEFT)

            scrlbar_x = Scrollbar(frame,orient=HORIZONTAL)
            scrlbar_x.pack(fill=X,side=BOTTOM)
            innings = event.widget.cget(("text"))

            tree = ttk.Treeview(frame,yscrollcommand=scrlbar_y.set,xscrollcommand=scrlbar_x.set)
            scrlbar_y.config(command=tree.yview)
            scrlbar_x.config(command=tree.xview)

            try:
                #if match completed
                live_stat = soup.find('div',{'class':'cb-col cb-scrcrd-status cb-col-100 cb-text-complete'}).text
                head_lst.append("Live Stats Of Match:")
                details_lst.append(live_stat)

            except Exception as e:
                # if match is playing
                live_stat = soup.find('div',{'class':'cb-col cb-scrcrd-status cb-col-100 cb-text-live'}).text
                head_lst.append("Live Stats Of Match:")
                details_lst.append(live_stat.strip())

            for i in details:
                detail = i.find('div',{'class':'cb-nav-subhdr cb-font-12'})
                details_lst.append(detail.text)

            head_lst.append("Seriese")
                
            data = soup.find_all('div',{'class':'cb-col cb-col-100'})

            for data in data:
                head = data.find_all('div',{'class':'cb-col cb-col-27'})
                for head in head:
                    if head != None:
                        head_lst.append(head.text)

                details = data.find_all('div',{'class':'cb-col cb-col-73'})
                for details in details:
                    details = details.text
                    details = details.replace("  ","")
                    details_lst.append(details)

            tree['columns'] = ("1st","2nd")

            tree.column("#0",width=0)
            tree.column("1st",anchor=W,minwidth=150,width=150)
            tree.column("2nd",anchor=W,minwidth=700,width=700)

            tree.heading("#0",text="")
            tree.heading("1st",text="",anchor=CENTER)
            tree.heading("2nd",text="",anchor=CENTER)

            for i in range(len(head_lst)):
                tree.insert('',END,i,values=(head_lst[i],details_lst[i]))
            # tree.place(x=20,y=0)
            tree.pack()
        #Batsman 1st innings funcion
        def Batting_scorecard(event):
            frame = Frame(live_root,borderwidth=10,relief=SUNKEN,width=720,bg='black',height=400)
            label = Label(frame,image=bg_frame).place(x=0,y=0)
            frame.place(x=10,y=100)
            frame.pack_propagate(0)

            scrlbar_y = Scrollbar(frame)
            scrlbar_y.pack(fill=Y,side=LEFT)

            scrlbar_x = Scrollbar(frame,orient=HORIZONTAL)
            scrlbar_x.pack(fill=X,side=BOTTOM)
            innings = event.widget.cget(("text"))

            tree = ttk.Treeview(frame,yscrollcommand=scrlbar_y.set,xscrollcommand=scrlbar_x.set)
            scrlbar_y.config(command=tree.yview)
            scrlbar_x.config(command=tree.xview)
        
            players = []
            wicket = []
            runs = []
            balls = []
            try:
                live_stat = soup.find('div',{'class':'cb-col cb-scrcrd-status cb-col-100 cb-text-complete'}).text
            except Exception as e:
                live_stat = soup.find('div',{'class':'cb-col cb-scrcrd-status cb-col-100 cb-text-live'}).text

            stats = Label(frame,text=live_stat,font="calberia 15 bold",bg='black',fg='white').pack(anchor=NW)

            data = soup.find_all('div',{'id':'innings_1'})
            if innings == 'Innings 2 Batsman':
                data = soup.find_all('div',{'id':'innings_2'})

            for main_data in data:
                score = main_data.find('div',{'class':'cb-col cb-col-100 cb-scrd-hdr-rw'}).text
                score_label = Label(frame,text=score,font="calberia 15 bold",bg='black',fg='white').pack(pady=5,anchor=NW)
                a = main_data.find_all('div',{'class':'cb-col cb-col-100 cb-scrd-itms'})
                for player_data in a:
                    player_name = player_data.find('div',{'class':'cb-col cb-col-27 text-bold'})
                    player_name2 = player_data.find('div',{'class':'cb-col cb-col-27'})
                    if player_name != None:
                        players.append(player_name.text)
                    if player_name2 != None:
                        players.append(player_name2.text)
                    
                for wickets in a:
                    wickets = wickets.find('div',{'class':'cb-col cb-col-33'})
                    if wickets != None:
                        wicket.append(wickets.text)
                    if wickets == None:
                        wicket.append("")
                    
                for plyer_run in a:
                    plyer_run = plyer_run.find('div',{'class':'cb-col cb-col-8 text-right text-bold'})
                    if plyer_run != None:
                        runs.append(plyer_run.text)
                        
                for plyer_balls in a:
                    plyer_balls = plyer_balls.find('div',{'class':'cb-col cb-col-8 text-right'})
                    if plyer_balls != None:
                        balls.append(plyer_balls.text)
            length = len(players)
            try:
                if 'Yet to Bat' in players[length-1]:
                    players = players[:length-1]
            except Exception as e:
                pass
            try:
                if 'Did not' in players[length-1]:
                    players = players[:length-1]
            except Exception as e:
                pass
            tree['columns'] = ("Batsman","wicket","Runs","Balls")

            tree.column("#0",width=0)
            tree.column("Batsman",anchor=W,minwidth=200,width=200)
            tree.column("wicket",anchor=W,minwidth=250,width=250)
            tree.column("Runs",anchor=CENTER,minwidth=125,width=125)
            tree.column("Balls",anchor=CENTER,minwidth=125,width=125)

            tree.heading("#0",text="")
            tree.heading("Batsman",text="Batsman",anchor=CENTER)
            tree.heading("wicket",text="",anchor=CENTER)
            tree.heading("Runs",text="Runs",anchor=CENTER)
            tree.heading("Balls",text="Balls",anchor=CENTER)

            for i in range(len(players)):
                tree.insert('',END,i,values=(players[i],wicket[i],runs[i],balls[i]))
            tree.pack()

        #Bowling scorcard function
        def bowling_scorecard(event):
            frame = Frame(live_root,borderwidth=10,relief=SUNKEN,width=720,bg='black',height=400)
            frame.place(x=10,y=100)
            label = Label(frame,image=bg_frame).place(x=0,y=0)
            frame.pack_propagate(0)
                
            scrlbar_y = Scrollbar(frame)
            scrlbar_y.pack(fill=Y,side=LEFT)

            scrlbar_x = Scrollbar(frame,orient=HORIZONTAL)
            scrlbar_x.pack(fill=X,side=BOTTOM)
            innings = event.widget.cget(("text"))

            tree = ttk.Treeview(frame,yscrollcommand=scrlbar_y.set,xscrollcommand=scrlbar_x.set)
            scrlbar_y.config(command=tree.yview)
            scrlbar_x.config(command=tree.xview)
                
            innings = event.widget.cget(("text"))
            #bowling data
            name_lst = []
            wickets_lst = []
            stats2 = []
            try:
                live_stat = soup.find('div',{'class':'cb-col cb-scrcrd-status cb-col-100 cb-text-complete'}).text
            except Exception as e:
                live_stat = soup.find('div',{'class':'cb-col cb-scrcrd-status cb-col-100 cb-text-live'}).text

            stats = Label(frame,text=live_stat,font="calberia 15 bold",bg='black',fg='white').pack(pady=8,anchor=NW)

            data = soup.find_all('div',{'id':'innings_1'})

            if innings == 'Innings 2 Bowling':
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
            tree.column("player name",anchor=W,minwidth=500,width=500)
            tree.column("Wicket",anchor=W,minwidth=200,width=200)

            tree.heading("#0",text="")
            tree.heading("player name",text="Bowler",anchor=CENTER)
            tree.heading("Wicket",text="Wickets",anchor=CENTER)

            for i in range(len(name_lst)):
                tree.insert('',END,i,values=(name_lst[i],wickets_lst[i]))

            tree.pack()
        def live_commentery():
            frame = Frame(live_root,borderwidth=10,relief=SUNKEN,width=720,bg='black',height=400)
            frame.place(x=10,y=100)
            label = Label(frame,image=bg_frame).place(x=0,y=0)
            frame.pack_propagate(0)
                
            scrlbar_y = Scrollbar(frame)
            scrlbar_y.pack(fill=Y,side=LEFT)

            scrlbar_x = Scrollbar(frame,orient=HORIZONTAL)
            scrlbar_x.pack(fill=X,side=BOTTOM)

        #all buttons 
        info_btn = Button(live_root,text="Match Info",font='calbria 10 bold',command=match_info)
        info_btn.pack(side="left",anchor=NW,padx=10,pady=30)

        inings1_batsman_btn = Button(live_root,text="Innings 1 Batting",font='calbria 10 bold')
        inings1_batsman_btn.pack(side="left",anchor=NW,padx=10,pady=30)
        inings1_batsman_btn.bind("<Button-1>",Batting_scorecard)

        inings1_bowler_btn = Button(live_root,text="Innings 1 Bowling",font='calbria 10 bold')
        inings1_bowler_btn.pack(side="left",anchor=NW,padx=10,pady=30)
        inings1_bowler_btn.bind("<Button-1>",bowling_scorecard)

        inings2_batsman_btn = Button(live_root,text="Innings 2 Batsman",font='calbria 10 bold')
        inings2_batsman_btn.pack(side="left",anchor=NW,padx=10,pady=30)
        inings2_batsman_btn.bind("<Button-1>",Batting_scorecard)

        inings2_bowler_btn = Button(live_root,text="Innings 2 Bowling",font='calbria 10 bold')
        inings2_bowler_btn.pack(side="left",anchor=NW,padx=10,pady=30)
        inings2_bowler_btn.bind("<Button-1>",bowling_scorecard)

        commentery_btn = Button(live_root,text="Live Commentery",font='calbria 10 bold')
        commentery_btn.pack(side="left",anchor=NW,padx=10,pady=30)
    #live matches list buttons

    for i in live_team:
        btn = Button(result_root,text=i,font='calbria 15 bold',width=80,bg='silver')
        btn.bind("<Button-1>",matches_btn)
        btn.pack(pady=pading,anchor=NW,padx=30)

def fixtuers_match():
    fixtuers_root = Toplevel(root)
    fixtuers_root.geometry('800x560')
    fixtuers_root.title("Fixtuers Matches")
    fixtuers_root.resizable(0,0)
    fixtuers_root.iconbitmap('Data\icon.ico')

    bg = Label(fixtuers_root,image=bg_img).pack()
    detail = Label(fixtuers_root,text='To Watch More Details Select The Match And click Search Button',font='lucida 15 bold',bg='red',width=59,relief=SUNKEN)
    detail.place(x=35,y=465)

    fram_list = Frame(fixtuers_root)
    fram_list.place(x=35,y=70)

    global match_lst
    scroly = Scrollbar(fram_list)
    scroly.pack(fill=Y,side=RIGHT)
    scrlbarx = Scrollbar(fram_list,orient=HORIZONTAL)
    scrlbarx.pack(side=BOTTOM,fill=X)

    match_lst = Listbox(fram_list,width=65,height=15,font="lucida 15 bold",bg='black',fg='white',yscrollcommand=scroly.set,xscrollcommand=scrlbarx.set)
    scroly.config(command=match_lst.yview)
    scrlbarx.config(command=match_lst.xview)
    match_lst.pack()

    # global fixtuers
    url = 'https://www.icc-cricket.com/mens-schedule/list'
    result = requests.get(url)
    soup = BeautifulSoup(result.text,'html.parser')

    dates = soup.find_all('time',{'class':'match-block__date match-block__date--local'})
    date_lst = []
    for i in dates:
        date = i.text
        date_lst.append(date)

    data = soup.find_all('div',{'class':'match-block__team-container'})
    matches = []
    for i in data:
        match = i.find('div',{'class':'match-block__summary'})
        if match != None:
            matches.append(match.text)

    length = len(date_lst)

    for i in range(length):
        match_lst.insert(END,date_lst[i])
        match_lst.insert(END,matches[i])
        match_lst.insert(END,"________________________________________________________________________") 
    fixtuers_root.mainloop()

bg = Label(root,image=bg_img)
bg.pack()
startbtn = Button(root,image=startbtn_img,borderwidth=0,command=start_data)
startbtn.place(x=screen_width/2-80,y=screen_height/2-80)
creater = Label(root,text="Developer : Pratham Rathod",font='times 20 bold',fg='white',bg='black',relief=SUNKEN,borderwidth=5).place(x=0,y=0)
root.mainloop()
