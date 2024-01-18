from tkinter import *
import random
from PIL import ImageTk, Image

dictionary = {}
fileread = open('picList.txt', "r")
x = fileread.read().split("\n")
for i in x:
    a,b = i.split(";")
    dictionary[a] = b

class FourPics1word(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("400x500")
        self.title("Four Pics One Word")
        self.resizable(False, False)
        self.configure(bg="#CBC3E3")
        playerInfo = open("playerInfo.txt", 'r')
        x,y = playerInfo.read().split(';')
        self.fourpicLevel = x
        self.string = "Level:" + self.fourpicLevel
        self.coins = int(y)
        self.answer = {}
        playerInfo.close()
        coinfile = "coin5.png"
        coin = Image.open(coinfile)
        coin = ImageTk.PhotoImage(coin)
        self.topFrame = Frame(self, background="sky blue", height=57, width=500, relief= RAISED)
        self.levelLabel = Label(self.topFrame, text=self.string, font="Arial 30", bg="sky blue")
        self.coinLabel = Label(self.topFrame, text=self.coins, font="Arial 30 bold", bg="sky blue")
        self.coinshow = Label(self.topFrame, bg="sky blue")
        self.topFrame.grid(row=0, column=0)
        self.levelLabel.place(x=0, y=0)
        self.coinLabel.place(x=325, y=0)
        self.coinshow.configure(image=coin)
        self.coinshow.image = coin
        self.coinshow.place(x=265,y=-2)
        self.fourpicfile = dictionary[self.fourpicLevel]+".png"
        fourpic = Image.open(self.fourpicfile)
        fourpic = fourpic.resize((250,250))
        fourpic = ImageTk.PhotoImage(fourpic)
        self.pictureFrame = Frame(self, bg="dark grey", width=250,height=250)
        self.fourpicshow = Label(self.pictureFrame, image=fourpic)
        self.fourpicshow.image = fourpic
        self.fourpicshow.place(x=0,y=0)
        self.pictureFrame.place(x=80, y=63)
        self.buttons = Frame(self, height=85, width=280, bg="pink")
        self.buttons.place(x=65, y=387)
        self.hintbutton = Button(self, text="HINT", bg="yellow", relief=RAISED, height=2, width=4, command=self.hint) 
        self.hintbutton.place(x=355,y=390)
        self.passbutton = Button(self, text="PASS", bg="green", relief=RAISED, height=2, width=4, command=self.passbtn)
        self.passbutton.place(x=355,y=434)
        self.level()

    def changeLevel(self):
        self.fourpicLevel = int(self.fourpicLevel)
        self.fourpicLevel+=1
        if self.fourpicLevel >=len(dictionary)+1:
            win = Tk()
            win.title("Finish Window")
            label = Label(win, text="You won the game!", font="Arial 25 bold", ).pack()
            win.mainloop()
            self.fourpicLevel = 1
            self.coins =100
        self.fourpicLevel = str(self.fourpicLevel)
        self.string = "Level:" + self.fourpicLevel
        fourpicfile = dictionary[self.fourpicLevel]+".png"
        fourpic = Image.open(fourpicfile)
        fourpic = fourpic.resize((250,250))
        fourpic = ImageTk.PhotoImage(fourpic)
        self.fourpicshow.configure(image=fourpic)
        self.fourpicshow.image = fourpic
        self.fourpicshow.place(x=0,y=0)
        self.levelLabel.configure(text=self.string)
        self.coinLabel.configure(text=self.coins)
        self.hintbutton.configure(bg='yellow', command=self.hint)
        self.level()

    def passbtn(self):
        if self.fourpicLevel == 50:
            self.passbutton.configure(command=lambda: None)
        if self.coins !=0:
            self.coins -=10
            self.changeLevel()
            self.passbutton.configure(command=self.passbtn)
        else:
            self.coinLabel.configure(text=self.coins)
            self.passbutton.configure(command=self.nocoins)

    def nocoins(self):
        self.coinLabel.configure(fg="red")
        self.hintbutton.configure(bg="red", command=lambda:None)

    def level(self):
        self.count = 0
        self.hintCount = 0
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.letters = []
        self.lettersBtns = []
        self.lettersRef = []
        self.answerDict = {}
        self.hintDict = {}
        for i in range(0,len(dictionary[self.fourpicLevel])):
            self.answer[i] = "_"
        count = 0
        for i in dictionary[self.fourpicLevel].upper():
            self.letters.append(i)
            self.lettersBtns.append(i)
            self.lettersRef.append(i)
            self.answerDict[count] = i
            self.hintDict[count] = "_"
            count +=1
        self.answerFrame = Frame(self, bg="#CBC3E3", height = 42, width=140)
        self.answerFrame.place(x=80,y=325)
        c = 0
        for i in range(0,len(self.lettersBtns)):
            self.lettersBtns[i] = Label(self.answerFrame,bg="grey", text=" ", font="Arial 10 bold", height=2, width=4, relief=RAISED)
            self.lettersBtns[i].grid(row=0, column=c)
            c+=1
        for a in range(len(self.alphabet)-1):
            b = self.alphabet[random.randint(0,len(self.alphabet)-1)]
            if b in self.letters:
                continue
            else:
                if len(self.letters) == 12:
                    break
                else:
                    self.letters.append(b)
                    self.lettersRef.append(b)
        self.coinLabel.configure(fg="Black")
        self.passbutton.configure(command=self.passbtn)
        self.hintbutton.configure(bg="yellow", command=self.hint)
        self.letters.sort()
        self.lettersRef.sort()
        self.randomLetters()

    def randomLetters(self):
        self.numbers = []
        r = 0
        c = 0
        for i in range(12):
            self.numbers.append(i)
            self.letters[i] = Button(self.buttons, text=self.lettersRef[i], bg= "light green", font= "arial 11 bold", height=2,activebackground = 'beige',activeforeground = 'blue', width=4, relief=RAISED,cursor='circle', command=lambda a = i: self.answerAdd(a))
            self.letters[i].grid(row=r, column=c)
            c += 1
            if c == 6:
                r=2
                c=0

    def tryAgain(self):
        for i in self.hintDict:
            self.lettersBtns[i].config(bg="red", text=self.hintDict[i])
            self.answer[i] = self.hintDict[i]
            
    def checkAns(self):
        if self.answer != self.answerDict:
            self.tryAgain()
            self.randomLetters()
            for i in range(0,len(dictionary[self.fourpicLevel])-1):
                if self.answer[i] == '_':
                    self.count = i
                    break
            if self.count == len(dictionary[self.fourpicLevel]):
                self.count -= 1
        if self.answer == self.answerDict:
            self.coins += 10
            for i in range(0,len(dictionary[self.fourpicLevel])):
                self.lettersBtns[i].destroy()
            self.hintDict.clear()
            self.answerDict.clear()
            self.changeLevel()

    def answerAdd(self, a):
        if self.answer[self.count] != "_":
            self.count += 1
        if self.count != len(dictionary[self.fourpicLevel]):
            self.answer[self.count] = self.lettersRef[a]
            self.lettersBtns[self.count].config(text=self.lettersRef[a],bg = 'khaki')
            self.letters[a].config(text=" ", bg="#CBC3E3", command= lambda: None, relief = FLAT) 
            self.count += 1
            if self.count == len(dictionary[self.fourpicLevel]):
                self.checkAns()

    def hint(self):
        if self.coins < 1:
            self.nocoins()
        if self.coins > 0:
            if self.count != len(self.answerDict)-1 :
                self.answer[self.count] = self.answerDict[self.count]
                self.hintDict[self.count] = self.answerDict[self.count]
                self.coins-=2
                self.lettersBtns[self.count].config(text=self.answerDict[self.count],bg = 'khaki')
                self.coinLabel.configure(text=self.coins)
                d = self.lettersRef.index(self.answerDict[self.count])
                self.letters[int(d)].config(text=" ", bg="#CBC3E3",relief = FLAT, command= lambda: None) 
                self.count += 1
        if self.count == len(self.answerDict)-1:
            self.hintbutton.config(bg='red', command=lambda: None)

    def fileHandling(self):
        writeFile = open("playerInfo.txt", 'w')
        if self.fourpicLevel == len(dictionary)-1:
            self.fourpicLevel = 1
            self.coins = 100
        writeFile.write(self.fourpicLevel +";"+str(self.coins))
        writeFile.close()

root = FourPics1word()
root.mainloop()
root.fileHandling()