import time,pickle,sys
from threading import Thread
from tkinter import *
from tkinter.ttk import *
import stocks


with open(".env","rb") as f:
    data = pickle.load(f)

root = Tk()
root.title("AutoGrinder")
root.geometry("600x250+200+200")

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


donate = Button(root,text="Donate to ...")
fr_bu = Frame(root)

def change(e):
    global url,url_hl,url_sto,header,logger

    logger = stocks.Logger(user.get()+"_log.log")
    sys.stdout = sys.stderr = logger

    active = data[user.get()]

    url = active["url"]
    url_hl = active["url_hl"]
    url_sto = active["url_sto"]
    header = active["header"]

user = Combobox(fr_bu,value=["whyyyyy"],state="readonly")
user.current(0)
user.grid(columnspan=2,sticky="news")
user.bind("<<ComboboxSelected>>",change)
change(None)


shop = Text(root,width=38)
shop.insert("1.0",">"*15+"STOCKS"+"<"*15)
donate.pack(side="bottom",fill="x",pady=2)
shop.pack(side="right",fill="y",expand=True)
fr_bu.pack(fill="both",expand=True)

#__ Nothing __
def search_dr():
    shop.insert("end", f"""\n{'-'*30}\n{
        time.asctime( time.localtime(time.time()) )}\n{'-'*30}""")

#__ should make class __
def hunt_start():
    pm  = stocks.random.choice(   ['f','c',"k",'r'] )
    pls = ["pls pm", pm ]
    stocks.send(url,header,3,*pls)
    stocks.send(url,header,1, *["pls hunt"])
    stocks.do_type(url,header)
    stocks.send(url,header,1,*["pls fish"])
    stocks.do_type(url,header)

    global hunt_id
    hunt_id = root.after(60_500,Thread(target=hunt_start).start )

def hunt():
    Thread(target=hunt_start).start()
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
    hl_id = root.after(22_400,Thread(target=hl_start).start )

def hl():
    Thread(target=hl_start).start()
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
        with open(user.get()+"_Stocks.txt") as f:
            shop.insert("end",f.read()+"-"*30)
        shop_stock.configure(text="Load Stocks")
    root.after(24000,load)

def clear():
    shop.delete("1.0","end")
    shop.insert("1.0",">"*15+"STOCKS"+"<"*15)

pls_hunt = Button(fr_bu,text="Start Hunt",command=hunt)
search_dragons = Button(fr_bu,text="Write Time",width=13,command=search_dr)
search_events = Button(fr_bu,text=" Search Events  ",command=search_eve)
pls_hl = Button(fr_bu,text="Start HL",command=hl)
shop_stock = Button(fr_bu,text="Load Stocks",command=stock)
clear = Button(fr_bu,text="Clear -->",command=clear)

pls_hunt.grid(row = 1,column =0,pady=4)
search_dragons.grid(row = 1,column =1,pady=4)
pls_hl.grid(row = 2,column =0,pady=1)
search_events.grid(row = 2,column =1,pady=1)
shop_stock.grid(row = 3,column =0,columnspan=2,sticky="news",pady=15,padx=2)
clear.grid(row = 4,columnspan=2,sticky="news",padx=2)


def donateE():
    try:
        with open(user.get()+"_Stocks.txt") as f:
            # items = [i.strip().rsplit(maxsplit=1)[0].split(" (") for i in f.readlines()[1:]]
            items = [i.strip().split() for i in f.readlines()[1:]]
    except FileNotFoundError:
        return shop.insert("end","\nClick 'load stock' first.\n")
    if not items or user.get() == '...':return

    # cmds = [f"pls gift {i[1]} {i[0].replace(' ','')} {data['tagH']}" for i in items if i[0].split()[-1].lower() not in ("laptop","pole","rifle")]
    cmds = [f"pls gift {i[1]} {i[0]} {data['tagH']}" for i in items if i[0] not in ("fishingpole","huntingrifle","laptop")]

    Thread(target=stocks.send ,args=(url,header,21, *cmds)).start()

    root.after(21*len(cmds)*1000,lambda:shop.insert("end","\nDonations Complete\n") )

donate.configure(command=donateE)


root.mainloop()
