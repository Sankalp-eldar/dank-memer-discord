import requests,time,random
from item_calc import items

def send(url,header,delay,*args):
    for i in args[:-1]:
        payload = {"content": i}
        requests.post(url,data = payload,headers = header)
        time.sleep(delay)
    if args[-1]:
        requests.post(url,data = {"content": args[-1]},headers = header)

def hl(url,header):
    send(url,header,1, *("pls hl",) )
    ch = random.choice(["l","h"])
    time.sleep(4)
    try:
        data = requests.get(url,headers = header).json()[0]
        hint = int(data['embeds'][0]['description'].split("*")[2])
    except (IndexError,ValueError):
        send(url,header,1,ch)
    else:
        if hint < 28:ch = "h"
        elif hint > 80:ch = "l"
        send(url,header,1,ch)


def stock_inv(url,header,user):
    res = dict()
    stop = 5

    payload = {"content": "pls inv"}
    requests.post(url,data = payload,headers = header)
    time.sleep(4)
    data = requests.get(url,headers = header).json()[0]
    stop = int(data['embeds'][0]['footer']['text'][-1])+1


    for i in range(2,stop):
        payload = {"content": "pls inv "+str(i)}
        requests.post(url,data = payload,headers = header)
        time.sleep(3)
    time.sleep(3)

    for i in requests.get(url,headers = header).json()[:(stop-1)]:
        data = i['embeds'][0]
        data = data['fields'][0]
        data = data['value'].split("\n\n")
        a = [ x.split(" ─ ",maxsplit=1) for x in data ]
        res.update( {j.split("`")[1].lower():int(j.split("\n")[0].replace(",","")) for h,j in a } )



    text = [f'{i} {res[i]}\n' for i in res]# if i in items]

    with open(user+"_Stocks.txt", "w") as f:
        f.writelines(["\n"]+text)




Event_loop = True
def stopEvent():
    global Event_loop
    Event_loop = False
def enableEvent():
    global Event_loop
    Event_loop = True
def event(url,headers):
    global Event_loop
    while Event_loop:
        try:
            data = requests.get(url,headers = headers).json()[:4]
        except TypeError:
            print('event error at:',time.localtime(time.time() ))
            import pickle
            data = requests.get(url,headers=headers).json()
            with open('type.dat','wb') as f:
                pickle.dump(data,f)
            time.sleep(9)
            continue
        for i in range(len(data)):
            if "event" in data[i]["content"].lower():
                c = data[abs(i-1)]["content"].lower()
                if "type" in c:
                    # c = "".join(c.replace("\ufeff","").translate({ord("`"):""}).split("type ")[1:])
                    c = c.replace("\ufeff","").split("type ")[1].split("`")[1]
                    requests.post(url, data = {"content":c}, headers=headers)
                    break
        time.sleep(9)

def do_type(url, headers):
    time.sleep(4)
    data = requests.get(url,headers = headers).json()[:2]
    for i in data:
        c = i["content"].lower()
        if "type" in c:
            # c = "".join(c.replace("\ufeff","").translate({ord("`"):""}).split("type ")[-1])
            c = c.replace("\ufeff","").split("`")[1]
            requests.post(url, data = {"content":c}, headers=headers)
            time.sleep(1)
            break


class lottery:

    def __init__(self):
        import pickle

        with open(".env","rb") as f:
            data = pickle.load(f)

        self.url = data["dank"]
        self.users = data["..."]['header'],data["...2"]['header'],data["...3"]['header']


    def __call__(self):

        for i in self.users:
            send(self.url,i,6, "pls lottery","yes" )

class Logger:

    def __init__(self,file):
        self.f = file
        with open(self.f,'w') as f:
            pass

    def write(self,content):
        with open(self.f,'a') as f:
            f.write(str(content))
    def flush(self,content=None):
        if content is not None:
            with open(self.f,'a') as f:
                f.write(str(content))
    def remove_if_blank(self):
        import os
        f = open(self.f)
        if not f.read():
            f.close();os.remove(self.f)
        f.close()

