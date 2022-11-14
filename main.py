import tkinter

from PIL import Image,ImageTk
import tkmacosx
from random import randint


root = tkinter.Tk()
root.title('Text Based Game')
root.geometry("900x500")
root.resizable(False, False)

class Player():
    def __init__(self):
        self.hp = 10
        self.shield = 3
        self.defense = 0
        self.speed = 7
        self.attack = 3
        self.coin = 10
        self.wave = 1
        self.count = 0

player = Player()

info = ['HP', 'Shield', 'Defense', 'Speed', 'Attack']


BLACK = '#000000'
WHITE = '#FFFFFF'

root.configure(bg=BLACK)

label_list = []

desc_var = tkinter.StringVar()

description = tkinter.Label(root, bg=BLACK, fg = WHITE, font=("Courier", 15),
                            highlightbackground=WHITE, highlightcolor= WHITE, highlightthickness=3,
                            textvariable=desc_var)
description.grid(row=9, column=1, rowspan=2, columnspan=4, padx=70, sticky="EWSN")

desc_var.set("Welcome to my text adventure game! Press Enter to continue.")
conversation = ["This is a turn-based game.",
                "In each turn, you can only attack once.",
                "But you can use items whenever you want to.",
                "Now enjoy the journey! Attack the monster by clicking the 'Attack' button."]

progress = 0
def continue_conversation(event=None):
    # while i != 2:
    #     continue_conversation()
    global progress
    print(progress)
    desc_var.set(conversation[progress])
    progress +=1

root.bind("<Return>", continue_conversation)



class MyButton(tkmacosx.Button):
    def __init__(self, root, text="", command=None):
        super().__init__(root, text=text, font=("Courier", 15),
                         bg=BLACK, fg=WHITE,
                         command=command,
                         highlightbackground=WHITE, highlightcolor= WHITE, highlightthickness=3,
                         padx=10, pady=7)

class MyLabel(tkinter.Label):
    def __init__(self, root, text="", fontsize=20):
        super().__init__(root, text=text, font = ("Courier", fontsize),
                          bg=BLACK, fg=WHITE, padx=10, pady=7)

class Monster:
    def __init__(self):
        self.hp = randint(int(3*(3**(player.wave/9)-0.6)),int(6*(2**(player.wave/6))))
        self.shield = randint(0,3)
        self.defense = randint(0,1)
        self.speed = randint(1,7)
        self.attack = randint(1,int(2+player.wave/5))

class Weapon:
    def __init__(self, name, attack):
        self.name = name
        self.attack = attack

class Consumable:
    def __init__(self, name, hp=0, attack=0, shield=0, defense=0, speed=0, cost=0):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.shield = shield
        self.defense = defense
        self.speed = speed
        self.cost = cost

player_item_list = [Consumable("Woden Shield", shield=3, cost=7), Consumable("Small HP Potion", hp=2, cost=5)]
titem_list = [Consumable("Iron Sword", attack=1, cost=10), Consumable("Gold Sword", attack=2, cost=15),
              Consumable("Woden Shield", shield=3, cost=7), Consumable("Iron Shield", shield=6, cost=12),
              Consumable("Small HP Potion", hp=2, cost=5), Consumable("Medium HP Potion", hp=5, cost=12)]


for i in range(5):
    label=MyLabel(root, text=info[i] + ": 0", fontsize=15)
    label.grid(row=i + 3, column=1)
    label_list.append(label)


monsterImage = tkinter.Label(root)
monsterImage.grid(row=3, column = 2, rowspan=4, columnspan=2)


def attack():

    if player.count == 1:
        desc_var.set("You can only attack once per round.")
        return

    deal_damage(player,monster, "Player", "monster")

    update_window()

    player.count += 1

    if monster.hp <= 0:
        desc_var.set("You defeat this monster!")
        reset()
        player.coin += 5
        player.wave += 1
        update_window()
        player.count = 0


def status():

    pvar = [player.hp, player.shield, player.defense, player.speed, player.attack]

    top = tkinter.Toplevel(root)
    top.configure(bg=BLACK)
    top.geometry("540x300")
    top.resizable(False, False)

    for i in range(5):
        MyLabel(top, text=info[i] + ": " + str(pvar[i]), fontsize=15).grid(row=i + 2, column=1)

    top.mainloop()


def item():

    top = tkinter.Toplevel(root)
    top.configure(bg=BLACK)
    top.geometry("540x300")
    top.resizable(False, False)

    for i in range(3):
        root.columnconfigure(i+1, weight=1, minsize=10)

    for i in range(4):
        root.rowconfigure(i + 1, weight=1, minsize=10)

    listbox = tkinter.Listbox(top);
    listbox.config(bg=BLACK, fg = WHITE, font=("Courier", 20))
    listbox.grid(row=1, column=1, rowspan=4, pady=10, padx=10)

    for i in range(len(player_item_list)):
        listbox.insert(i, player_item_list[i].name)

    def use_item():
        index = listbox.curselection()[0]
        item = player_item_list[index]

        player.attack += item.attack
        player.hp += item.hp
        player.defense += item.defense
        player.speed += item.speed
        player.shield += item.shield

        player_item_list.remove(item)
        listbox.delete(index)

    useButton = MyButton(top, text="Use", command=use_item)
    useButton.grid(row=2, column =3)

    shopButton = MyButton(top, text="Shop", command=shop)
    shopButton.grid(row=4,column=3)


    top.mainloop()


def p_pass():
    if player.count == 0:
        desc_var.set("You can still attack, are you sure you want to pass?")

    if player.count == 1:
        player.count = 0
        deal_damage(monster,player,"Monster", "player")
        if player.hp <= 0:
            desc_var.set("You are defeated!")


def deal_damage(attacker,defender, attackern, defendern):

    if attacker.speed < defender.speed:
        chance = defender.speed-attacker.speed
        if randint(1,10) <= chance:
            desc_var.set("Surprise! Dodge!")
            return

    damage = attacker.attack - defender.defense
    if defender.shield > 0 and damage <= defender.shield:
        desc_var.set(str(attackern) + " deal " + str(damage) + " damage to " + str(defendern) + "'s shield!")
        defender.shield -= damage

    elif defender.shield >= 0 and damage > defender.shield:
        defender.hp -= damage - defender.shield
        desc_var.set(str(attackern) + " deal " + str(damage - defender.shield) + " damage to the " + str(defendern)+"!")
        defender.shield = 0


def update_window():
    var = [monster.hp, monster.shield, monster.defense, monster.speed, monster.attack]

    for i in range(5):
        label_list[i].config(text=info[i] + ": " + str(var[i]))

    coinLabel.config(text = "Coins: " + str(player.coin))
    waveLabel.config(text = "Wave: " + str(player.wave))

def reset():
    global monster
    monster = Monster()
    # monsterindex = randint(1,2)
    imgindex = randint(1,5)

    image = Image.open(f"Monster/Monster {imgindex}.png")
    image = image.resize((200, 200), Image.ANTIALIAS)
    photoImg = ImageTk.PhotoImage(image)
    monsterImage.config(image=photoImg)
    monsterImage.image = photoImg


def shop():

    top = tkinter.Toplevel(root)
    top.configure(bg=BLACK)
    top.geometry("540x300")
    top.resizable(False, False)

    shoplistbox = tkinter.Listbox(top);
    shoplistbox.config(bg=BLACK, fg=WHITE, font=("Courier", 20))
    shoplistbox.grid(row=1, column=1, rowspan=4, pady=10, padx=10)
    for i in range(len(titem_list)):
        shoplistbox.insert(i, str(titem_list[i].name) + ": " + str(titem_list[i].cost) + "$")

    def buy():

        index = shoplistbox.curselection()[0]
        item =  titem_list[index]
        if player.coin >= item.cost:
            player_item_list.append(item)
            player.coin -= item.cost
            update_window()


    buyButton = MyButton(top, text="Buy", command=buy)
    buyButton.grid(row=2, column=2)



coinLabel = MyLabel(root,text = "Coins: " + str(player.coin))
coinLabel.grid(row=1,column=4)

waveLabel = MyLabel(root,text = "Wave: " + str(player.wave))
waveLabel.grid(row=1,column=1)

attackButton = MyButton(root, text="Attack",command=attack)
attackButton.grid(row=12, column=1)

statusButton = MyButton(root, text = "Status", command=status)
statusButton.grid(row=12, column=2)

itemButton = MyButton(root, text = "Item", command=item)
itemButton.grid(row=12, column=3)

passButton = MyButton(root, text = "Pass", command= p_pass)
passButton.grid(row=12, column=4)

root.rowconfigure(10, minsize=10)

for i in range (4):
    root.columnconfigure(i+1, weight=1)

for i in range(13):
    root.rowconfigure(i+1, minsize=10)
    root.rowconfigure(i+1, weight=1)


reset()
update_window()

root.mainloop()