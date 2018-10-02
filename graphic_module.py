from tkinter import *
from PIL import Image, ImageTk


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("GUI")
        # Allow the widget to take all window
        self.pack(fill=BOTH, expand=1)

        # Button
        quitButton = Button(self, text="Exit", command=self.client_exit)
        quitButton.place(x=0, y=0)

        # Menu
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # commands
        file = Menu(menu)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)

        edit = Menu(menu)
        edit.add_command(label='Undo')
        edit.add_command(label='Weight', command=self.showImg)
        edit.add_command(label='Show Text', command=self.showText)
        menu.add_cascade(label="Edit", menu=edit)

    def showImg(self):
        load = Image.open('Weight/Weight parallel plot.png')
        render = ImageTk.PhotoImage(load)

        img = Label(self, image=render)
        img.image = render
        img.place(x=0,  y=0)

    def showText(self):
        text = Label(self, text="bleh", font=("Helvetica", 56))
        text.pack()
        text.place(x=30, y=50)

    def client_exit(self):
        exit()

root = Tk()

root.geometry("800x539")

app = Window(root)
root.mainloop()
