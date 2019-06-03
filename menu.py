import tkinter as tk
from game import init_game
import json

RESOLUTION = ("800", "600")
DECOR = "assets/sprites/nuclear_mini.png"
DECOR_W = 50
DECOR_H = 50


class App(tk.Frame):
    DF = 1
    BG = "assets/sprites/bg_1.png"

    def __init__(self, master):
        super().__init__(master)
        self.root = master
        self.pack()
        self.create()
        with open("settings.txt", "w") as f:
            f.write(str(App.DF)+"\n")
            f.write(App.BG)

    def generate_decor(self):
        self.main_photo_r = tk.PhotoImage(file=DECOR)
        for i in range(1, 7):
            self.im1 = tk.Label(self.root, image=self.main_photo_r,
                           width=DECOR_W, height=DECOR_H, bd=0)
            self.im1.place(anchor="center", x=3*DECOR_W, y=10*i+i*DECOR_H)
        self.main_photo_l = tk.PhotoImage(file=DECOR)
        for i in range(1, 7):
            self.im2 = tk.Label(self.root, image=self.main_photo_l,
                                width=DECOR_W, height=DECOR_H, bd=0)
            self.im2.place(anchor="center", x=int(RESOLUTION[0]) - 3 * DECOR_W, y=10 * i + i * DECOR_H)
        self.lbcop = tk.Label(self.root, text="Copyright © 2016. ABSL studio. All rights reserved.",
                              fg="yellow", bg="black", font=("Times", 10))
        self.lbcop.place(x=0, y=int(RESOLUTION[1])-20)

    def create(self):
        self.lb = tk.Label(self.root, text="Nuclear Shield",
                           width=20, height=2, bd=0,
                           fg="yellow", bg="black",
                           font="Times 20")
        self.lb.pack()
        self.btn_ng = tk.Button(self.root, text="New game", command=lambda: init_game(),
                                width=20, height=2, bd=8,
                                fg="yellow", bg="black", activebackground="yellow",
                                font="Times 13", relief="ridge")
        self.btn_ng.pack()
        self.btn_settings = tk.Button(self.root, text="Setings", command=lambda: self.settings(),
                                      width=20, height=2, bd=8,
                                      fg="yellow", bg="black", activebackground="yellow",
                                      font="Times 13", relief="ridge")

        self.btn_settings.pack()
        self.btn_rec = tk.Button(self.root, text="Records", command=lambda: self.records(),
                                 width=20, height=2, bd=8,
                                 fg="yellow", bg="black", activebackground="yellow",
                                 font="Times 13", relief="ridge")
        self.btn_rec.pack()
        self.btn_about = tk.Button(self.root, text="About", command=lambda: self.about(),
                                   width=20, height=2, bd=8,
                                   fg="yellow", bg="black", activebackground="yellow",
                                   font="Times 13", relief="ridge")
        self.btn_about.pack()
        self.btn_quit = tk.Button(self.root, text="Quit", command=lambda: self.root.quit(),
                                  width=20, height=2, bd=8,
                                  fg="yellow", bg="black", activebackground="yellow",
                                  font="Times 13", relief="ridge")
        self.btn_quit.pack()
        self.generate_decor()

    @staticmethod
    def update_df(df):
        App.DF = df
        with open("settings.txt", "r") as f:
            var = f.readlines()
        with open("settings.txt", "w") as f:
            f.write(str(df) + "\n")
            f.write(var[1])

    @staticmethod
    def update_bg(bg):
        App.BG = bg
        with open("settings.txt", "r") as f:
            var = f.readlines()
        with open("settings.txt", "w") as f:
            f.write(var[0])
            f.write(bg)

    def settings(self):
        self.modes = [("Easy", 0), ("Medium", 1), ("Hard", 2), ("Unreal", 3)]
        self.backgroundes = [("City 1", "assets/sprites/bg_1.png"),
                             ("City 2", "assets/sprites/bg_2.jpg"),
                             ("City 3", "assets/sprites/bg_3.png")]
        self.root1 = tk.Toplevel()
        self.root1.title("Settings")
        self.root1.resizable(0, 0)
        image = tk.Image("photo", file="assets/sprites/settings.png")
        self.root1.wm_iconphoto(False, image)
        self.root1.geometry("360x260")
        self.root1.configure(background="white")
        self.lb1 = tk.Label(self.root1, text = "Difficulty: ", bg="white")
        self.lb1.pack()
        self.var1 = tk.IntVar()
        self.var1.set(App.DF)  # initialize
        for text, value in self.modes:
            self.rbtn = tk.Radiobutton(self.root1, text=text, bg="white",
                                       command=lambda: App.update_df(self.var1.get()),
                                       variable=self.var1, value=value)
            self.rbtn.pack(anchor="w")
        self.lb2 = tk.Label(self.root1, text="Background: ", bg="white")
        self.lb2.pack()
        self.var2 = tk.StringVar()
        self.var2.set(App.BG)  # initialize
        for text, value in self.backgroundes:
            self.rbtn = tk.Radiobutton(self.root1, text=text, bg="white",
                                       command=lambda: App.update_bg(self.var2.get()),
                                       variable=self.var2, value=value)
            self.rbtn.pack(anchor="w")

        self.btn1 = tk.Button(self.root1, text="Ok", command=lambda: self.root1.destroy(),
                              width=10, height=1, bd=5,
                              fg="yellow", bg="black", activebackground="yellow",
                              font="Times 13", relief="ridge")
        self.btn1.pack()

    def about(self):
        self.root2 = tk.Toplevel()
        self.root2.title("About")
        self.root2.resizable(0, 0)
        image = tk.Image("photo", file="assets/sprites/info.png")
        self.root2.wm_iconphoto(False, image)
        self.root2.geometry("360x400")
        self.root2.configure(background="white")
        self.var1 = tk.StringVar()
        self.lb3 = tk.Label(self.root2, textvariable=self.var1,
                            bg="white", width=42)
        self.var1.set("ABOUT GAME: \n"
                      "Help the shield protect lonely town.\n"
                      "Collect $ 300,000!\n"
                      "This can be done in several ways:\n"
                      "1) \n"
                      "2) \n"
                      "3) \n")
        self.lb3.pack()
        self.lb4 = tk.Label(self.root2, text="CREDITS: ", bg="white")
        self.lb4.pack()
        self.listbox = tk.Listbox(self.root2,  bg="black",width=30, relief="ridge", bd=5,fg="yellow")
        self.listbox.pack()
        self.listbox.insert("end", "Project manadger: ABS_Lord\n")
        self.listbox.insert("end", "Programming: ABS_Lord\n")
        self.listbox.insert("end", "Designer: ABS_Lord\n")
        self.listbox.insert("end", "Music: ABS_Lord\n")
        self.listbox.insert("end", "Original story: ABS_Lord\n")
        self.listbox.pack()
        self.lb5 = tk.Label(self.root2, text="Copyright © 2016. ABSL studio. All rights reserved.", bg="white")
        self.lb5.pack()
        self.btn2 = tk.Button(self.root2, text="Ok", command=lambda: self.root2.destroy(),
                              width=10, height=1, bd=5,
                              fg="yellow", bg="black", activebackground="yellow",
                              font="Times 13", relief="ridge")
        self.btn2.pack()

    def records(self):
        with open("records.json", "r") as f:
            self.global_records = json.load(f)
        self.root3 = tk.Toplevel()
        self.root3.resizable(0,0)
        self.root3.title("Records")
        image = tk.Image("photo", file="assets/sprites/records.png")
        self.root3.wm_iconphoto(False, image)
        self.root3.geometry("360x240")
        self.root3.configure(background="white")
        self.var3 = tk.StringVar()
        self.lb6 = tk.Label(self.root3, text="RECORDS: ", textvariable=self.var3,
                            bg="white", width=42, font=("Times", 14))
        self.var3.set("RECORDS: \n\n" + "1: " + str(self.global_records["1"]) + "\n" +
                      "2: " + str(self.global_records["2"]) + "\n" +
                      "3: " + str(self.global_records["3"]) + "\n")
        self.lb6.pack()
        self.btn3 = tk.Button(self.root3, text="Ok", command=lambda: self.root3.destroy(),
                              width=10, height=1, bd=5,
                              fg="yellow", bg="black", activebackground="yellow",
                              font="Times 13", relief="ridge")
        self.btn3.pack()



def init_menu():
    root = tk.Tk()
    root.resizable(0, 0)
    root.title("Nuclear Shield")
    image = tk.Image("photo", file="assets/sprites/icon.png")
    root.wm_iconphoto(False, image)
    root.geometry(RESOLUTION[0] + "x" + RESOLUTION[1])
    root.configure(background="black")
    App(root)
    root.mainloop()

