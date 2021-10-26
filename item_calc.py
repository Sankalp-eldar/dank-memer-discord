items = ["fish", "rarefish", "exoticfish", "legendaryfish",
 "skunk", "rabbit", "duck", "boar", "deer", "dragon"]
 # "fishingpole","huntingrifle","laptop"]

price = [ 4e3,   16e3   ,  1.3e5  ,  1.3e5  ,
      8e3  ,   8e3  ,  8e3   ,  2.5e4   ,  5e4   ,  1.3e5 ]

price_map = {i:j for i,j in zip(items,price)}

emote = {i:f':{i}:' for i in items}
emote['rarefish'] = ':tropical_fish:'
emote['exoticfish'] = ':blowfish:'
emote['legendaryfish'] = ':whale:'


advt_start = "**`SELLING`**\n\n"
"""**`TRADING ONLY`**

For pepet :trophy: **at** 43M

From following stocks and prices choose *creatures* you want,
total amount adding up to 43M ± 40k\n\n
"""
advt_end = "\n\nNon-negotiable"#"\n\nI can help with calculations"


def price_calc(user):

    with open(user+"_Stocks.txt") as f:
        item = [x.strip().split() for x in f.readlines()[1:]]
        item = {i:int(j) for i,j in item}

    res_l = dict()
    for i in item:
        if price_map.get(i):
            res_l.update({i: [item[i],price_map[i],
            f"{(item[i]*price_map[i])/1_000_000}M"]
            })
    return res_l



if __name__ == '__main__':
    import stocks
    from tkinter import *
    from tkinter.ttk import *
    root = Tk()
    root.title("Calc")

    style = Style()

    fr = Frame(root)
    fr.pack()



    ent_list = list()
    for i,val in enumerate(list(price_map)):
        Label(fr, text= val.capitalize()).grid(row = i, column = 0,pady=2,padx=2)
        x = Entry(fr)
        x.grid(row = i, column=1,pady=2,padx=2)
        ent_list.append(x)



    def total():
        amt = 0
        for i,val in enumerate(ent_list):
            amt += price[i]*int(    val.get() if val.get() else 0  )

        t.configure(text= f"{amt/1_000_000}M"   )

    Button(fr, text="Total:",command=total).grid(row = i+1,column = 0)
    t = Label(fr,text="Total amt...")
    t.grid(row = i+1,column = 1)

    def invert_totals():
        for i,val in enumerate(ent_list):
            x = val.get()
            if x:
                x = float(x)
                val.delete(0,"end")
                val.insert(0, x/price[i]   )

    def invert_coppy():
        res = list()
        for i,val in enumerate(ent_list):
            x = val.get()
            if x:
                j = items[i]
                try:
                    x = int(x)
                except ValueError:
                    x = round(float(x),2)
                if x == 0:continue
                a = avaliable[j]
                if a < x:
                    res.append(f"{emote[j]} Only {a} in stock at {price_map[j]*a/1_000_000}M")
                    continue
                res.append(f"{emote[j]}: {x}")
        if res:
            root.clipboard_clear()
            root.clipboard_append(" ".join(res))

    def clear():
        for i in ent_list:
            i.delete(0,"end")

    def load_stocks():

        with open("..."+"_Stocks.txt") as f:
            item = [x.strip().split() for x in f.readlines()[1:]]
            item = {i:int(j) for i,j in item}
        global avaliable
        avaliable = item

        for i,val in enumerate(list(price_map)):
            if item.get(val):
                ent_list[i].delete(0,"end")
                ent_list[i].insert(0,item.get(val))

    def advt():
        x = price_calc('...')

        res = list()
        for i in items:
            if x.get(i):
                res.append(
            f"{i.capitalize()} {emote[i]} **`at {int(x[i][1])//1000}k`** ea +tax (stock: {x[i][0]})"
            )

        root.clipboard_clear()
        root.clipboard_append(advt_start+"\n".join(res)+advt_end)


    Button(fr, text="Inverted totals",command=invert_totals
        ).grid(row = i+2, column = 0,sticky ="news",pady=5,padx=2)
    Button(fr, text="Coppy inverts",command=invert_coppy
        ).grid(row = i+2, column = 1,sticky ="news",pady=5,padx=2)

    Button(fr, text="Clear",command=clear
        ).grid(row = i+3, columnspan = 2 ,padx=2,sticky ="news",pady=5)

    Button(fr, text="Load stocks:",command=load_stocks
        ).grid(row = i+4,column = 0,sticky ="news",pady=2,padx=2)
    Button(fr, text="Coppy Advt.",command=advt
        ).grid(row =i+4,column = 1,sticky ="news",pady=2,padx=2)


    root.mainloop()
