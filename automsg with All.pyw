import time,pickle,sys
from threading import Thread
from tkinter import *
from tkinter.ttk import *
import stocks


with open(".env","rb") as f:
    data = pickle.load(f)

root = Tk()
root.title("AutoGrinder")
# root.geometry("607x282+200+200")

def quit_func():
    search_eve_stop()
    hunt_stop()
    hl_stop()
    logger.remove_if_blank()
    root.destroy()
    sys.exit(0)
root.protocol("WM_DELETE_WINDOW",quit_func)


style = Style()
style.configure(".",font=("Times New Roman",16,"bold"))


fr_bu = Frame(root)
fr_donate = Frame(root)

donate = Button(fr_donate,text="Donate:")
donate.pack(side="left",fill="x",padx=5)

def change(e):
    global url,url_hl,url_sto,header,logger

    logger = stocks.Logger(user.get()+"_log.log")
    sys.stdout = sys.stderr = logger

    active = data[user.get()]

    url = active["url"]
    url_hl = active["url_hl"]
    url_sto = active["url_sto"]
    header = active["header"]

user = Combobox(fr_bu,value=["removed"],state="readonly")
user.current(0)
user.grid(columnspan=2,sticky="news")
user.bind("<<ComboboxSelected>>",change)
change(None)


shop = Text(root,width=38,height=15)
shop.insert("1.0",">"*15+"STOCKS"+"<"*15)


fr_donate.pack(side="bottom",fill="x",pady=2)
if "windows" not in root.winfo_server().lower():
    src_l = Scrollbar(root,command=shop.yview)
    shop.configure(yscrollcommand=src_l.set)
    src_l.pack(side='right',fill='y')
shop.pack(side="right",fill="y",expand=True)
fr_bu.pack(fill="both",expand=True)

#__ Nothing __
def search_dr():
    shop.insert("end", f"""\n{'-'*30}\n{
        time.asctime( time.localtime(time.time()) )}\n{'-'*30}""")

#__ should make class __
def hunt_start():
    pm  = stocks.random.choice(   ['f','c',"k",'r'] )
    pls = ["pls pm", pm ,'pls beg', '']
    stocks.send(url,header,4,*pls)
    stocks.send(url,header,1, *["pls hunt"])
    stocks.do_type(url,header)
    stocks.send(url,header,1,*["pls fish"])
    stocks.do_type(url,header)

    global hunt_id
    hunt_id = root.after(53_000,Thread(target=hunt_start).start )

def hunt():
    Thread(target=hunt_start).start()
    # hunt_start()
    pls_hunt.configure(text="Stop Hunt",command=hunt_stop)
def hunt_stop():
    try:
        global hunt_id
        root.after_cancel(hunt_id)
    except NameError:
        shop.insert("end", """\nerror in stopping Hunt:
Wait... let it complete typing before stopping
(arround 8s from start)""")
    else:
        pls_hunt.configure(text="Start Hunt",command=hunt)
        del hunt_id


#__ This requires 1 class __

def hl_start():
    Thread(target=stocks.hl, args=(url_hl,header) ).start()
    global hl_id
    hl_id = root.after(33_400,Thread(target=hl_start).start )

def hl():
    # Thread(target=hl_start).start()
    hl_start()
    pls_hl.configure(text="Stop HL",command=hl_stop)
def hl_stop():
    try:
        global hl_id
        root.after_cancel(hl_id)
    except NameError:
        shop.insert("end", "\nerror in stopping HL:\nWait... let it type once before stopping\n(arround 2.2s from start)")
    else:
        pls_hl.configure(text="Start HL",command=hl)
        del hl_id


#__ Which has start-stop __
def search_eve_start():
    Thread(target=stocks.event, args=(url,header) ).start()
    Thread(target=stocks.event, args=(url_hl,header) ).start()
    #Thread(target=stocks.event, args=(url_sto,header) ).start()
    search_events.configure(text="  Stop  Events  ",command=search_eve_stop)
def search_eve():
    stocks.enableEvent()
    search_eve_start()
def search_eve_stop():
    stocks.stopEvent()
    search_events.configure(text=" Search Events  ",command=search_eve)


def stock():
    shop_stock.configure(text="Loding stock...")
    t1 = Thread(target=stocks.stock_inv, args=(url_sto,header,user.get()) )
    t1.start()
    def load():
        t1.join()
        try:
            with open(user.get()+"_Stocks.txt") as f:
                shop.insert("end",f.read()+"-"*30)
            shop_stock.configure(text="Load Stocks")
        except FileNotFoundError:
            return stock()
    root.after(24000,load)

def clear():
    shop.delete("1.0","end")
    shop.insert("1.0",">"*15+"STOCKS"+"<"*15)

def load_existing():
    try:
        with open(user.get()+"_Stocks.txt") as f:
            shop.insert("end",f.read()+"-"*30)
    except FileNotFoundError:pass



lottery = stocks.lottery()
lott_time = 1
def start_lot():
    global lott_after,lott_time
    lott_after = root.after(60_000,start_lot)

    lott_time -= 1
    lott.configure(text=f"{lott_time} Min Left")

    if lott_time == 0:
        Thread(target=lottery).start()
        lott_time = 60

def draw_lot():
    global lott_after
    lott.configure(text="Stop Lottery",command=stop_lot)
    start_lot()

def stop_lot():
    global lott_after,lott_time
    root.after_cancel(lott_after)
    lott.configure(text=f"Stopped {lott_time}M",command=draw_lot)
    # lott_timer.configure(text=f"Stopped {lott_time}M")
    lott_time += 1


pls_hunt = Button(fr_bu,text="Start Hunt",command=hunt)
search_dragons = Button(fr_bu,text="Write Time",width=13,command=search_dr)
search_events = Button(fr_bu,text=" Search Events  ",command=search_eve)
pls_hl = Button(fr_bu,text="Start HL",command=hl)
shop_stock = Button(fr_bu,text="Load Stocks",command=stock)
clear = Button(fr_bu,text="Clear -->",command=clear)
lott = Button(fr_bu,text="Draw Lottery",command=draw_lot)
# lott_timer = Label(fr_bu,text=" Start ",justify="center")



pls_hunt.grid(row = 1,column =0,pady=4)
search_dragons.grid(row = 1,column =1,pady=4)
pls_hl.grid(row = 2,column =0,pady=1)
search_events.grid(row = 2,column =1,pady=1)
shop_stock.grid(row = 3,column =0,columnspan=2,sticky="news",pady=5,padx=2)
clear.grid(row = 4,columnspan=2,sticky="news",padx=2)
lott.grid(row = 5,column = 0,sticky="news",pady = 2, padx = 4)
# lott_timer.grid(row = 5,column=1,sticky="news",pady=2, padx=2)

Button(fr_bu,text='existing stock',command=load_existing
).grid(row=5,column=1,sticky="news",pady=2, padx=2)


def donate_any():
    user = data[donner.get()]
    amt,itm,tag,cmds = amount.get(),item.get(),data[recive.get()],list()
    if "all" in [amt,itm]:
        with open(donner.get()+"_Stocks.txt") as f:
            inv = {i.strip().split()[0]:int(i.strip().split()[1]) for i in f.readlines()[1:] }


    if itm == "all" and amt == "all":
        cmds = [f"pls gift {inv[i]} {i} <@{tag}>" for i in inv if i not in ("fishingpole","huntingrifle","laptop")]
        Thread(target=stocks.send,args=(user["url"],user["header"],21,*cmds)).start()
    elif amt == "all":
        stocks.send(user["url"],user["header"],1,f"pls gift {inv[itm]} {itm} <@{tag}>")
    else:
        stocks.send(user["url"],user["header"],1,f"pls gift {amt} {itm} <@{tag}>")

    root.after(21*len(cmds)*1000,lambda:shop.insert("end","\nDonations Complete\n") )

def load_stock(e=None):
    try:
        with open(donner.get()+"_Stocks.txt") as f:
            item.configure(values = ["all"]+[i.strip().split()[0] for i in f.readlines()[1:] ] )
    except FileNotFoundError:
        with open(donner.get()+"_Stocks.txt","w") as f:
            f.write("\n")

donate.configure(command=donate_any)


donner = Combobox(fr_donate,value = ["removed"],state = "readonly")
donner.current(0)
donner.bind("<<ComboboxSelected>>",load_stock)

item = Combobox(fr_donate,value= ["all"]+stocks.items,state="readonly")
item.current(0)
amount = Combobox(fr_donate,width=6,value=["all"])
amount.current(0)
recive = Combobox(fr_donate,width=6,value=["tagA",'tagH',"tagE"],state="readonly")
recive.current(0)


recive.pack(side="right",padx=2)
amount.pack(side="right",padx=2)
item.pack(side="right",padx=2)
donner.pack(side="right",padx=2)


# style.theme_use("xpnative")
root.mainloop()
