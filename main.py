from tkinter import *
from tkinter import filedialog
import json


with open("config.json") as f:
    config = json.load(f)

font = config["font"]
size = config["size"]
text = config["text"]
background = config["background"]
textcolor = config["textcolor"]

root = Tk()
root.geometry("350x250")
root.title("CrispyEditor")
root.minsize(height=250, width=350)
root.maxsize(height=500, width=500)

# adding scrollbar
scrollbar = Scrollbar(root)

# packing scrollbar
scrollbar.pack(side=RIGHT,
			fill=Y)

font = (font,size)

text_info = Text(root,
				yscrollcommand=scrollbar.set)
text_info.configure(font=font,)
text_info.pack(fill=BOTH)

# configuring the scrollbar
scrollbar.config(command=text_info.yview)


def load_file():
    file_name = filedialog.askopenfilename()
    text_info.insert(END, open(file_name).read())

def save_file():
    file_name = filedialog.asksaveasfilename()
    file = open(file_name, "w")
    file.write(text_info.get(1.0, END))
    file.close()

def save_as():
    file_name = filedialog.asksaveasfilename()
    file = open(file_name, "w")
    file.write(text_info.get(1.0, END))
    file.close()

def new_file():
    text_info.delete(1.0, END)


#add a menu for saving and opening
menu_bar = Menu(root)
root.config(menu=menu_bar)
file_menu = Menu(menu_bar)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=load_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as)
file_menu.add_command(label="New", command=new_file)







root.mainloop()
