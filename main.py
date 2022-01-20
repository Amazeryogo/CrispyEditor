from fileinput import filename
from tkinter import *
from tkinter import filedialog
import json
import threading
import idlelib.colorizer as ic
import idlelib.percolator as ip
import re
import os

global file_name
file_name = "cache/Untitled.txt"

with open("config/config.json") as f:
    config = json.load(f)



font = config["font"]
size = config["size"]
text = config["text"]
background = config["background"]
textcolor = config["textcolor"]
tabsize = config["tabsize"]

global pysyntax
pysyntax = config["pysyntax"]


root = Tk()
root.geometry("1000x800")
title = "CrispyEditor"
root.title(title)
root.minsize(height=250, width=350)
root.maxsize(height=1000, width=1000)



# adding scrollbar
scrollbar = Scrollbar(root)

# packing scrollbar
scrollbar.pack(side=RIGHT,
			fill=Y)

font = (font,size)

# set default text
text_info = Text(root,
				yscrollcommand=scrollbar.set)
text_info.configure(font=font, bg=background, fg=textcolor)
text_info.insert(END, text)


def tab(arg):
    text_info.insert(END, " " * tabsize)
    return 'break'

text_info.bind("<Tab>", tab)
text_info.pack(fill=BOTH)

cdg = ic.ColorDelegator()
cdg.prog = re.compile(r'\b(?P<MYGROUP>tkinter)\b|' + ic.make_pat(), re.S)
cdg.idprog = re.compile(r'\s+(\w+)', re.S)
cdg.tagdefs['MYGROUP'] = {'foreground': '#7F7F7F', 'background': 'background'}
cdg.tagdefs['COMMENT'] = {'foreground': 'green', 'background': 'background'}
cdg.tagdefs['KEYWORD'] = {'foreground': '#007F00', 'background': 'background'}
cdg.tagdefs['BUILTIN'] = {'foreground': '#7F7F00', 'background': 'background'}
cdg.tagdefs['STRING'] = {'foreground': 'orange', 'background': 'background'}
cdg.tagdefs['DEFINITION'] = {'foreground': '#007F7F', 'background': 'background'}
cdg.tagdefs['FUNCTION'] = {'foreground': 'blue', 'background': 'background'}
cdg.tagdefs['VARIABLE'] = {'foreground': 'red', 'background': 'background'}
cdg.tagdefs['CLASS'] = {'foreground': 'blue', 'background': 'background'}


# configuring the scrollbar
scrollbar.config(command=text_info.yview)








def load_file(*args):
    global file_name
    file_name = filedialog.askopenfilename()
    text_info.delete(1.0,END)
    text_info.insert(END, open(file_name).read())
    with open('cache/openedfiles.txt','a') as f:
        f.write(file_name)
        f.write('\n')
        f.close()

    # if extension is .py turn syntax on
    if file_name.endswith(".py"):
        ip.Percolator(text_info).insertfilter(cdg)
    else:
        pass

def load_certian_file(file_name):
    try:
        text_info.delete(1.0,END)
        text_info.insert(END, open(file_name).read())
        with open('cache/openedfiles.txt','a') as f:
            f.write(file_name)
            f.write('\n')
            f.close()
        # if extension is .py turn syntax on
        if file_name.endswith(".py"):
            ip.Percolator(text_info).insertfilter(cdg)
        else:
            pass
    except IsADirectoryError:
        # insert the names of the files in the directory into the folder widget under the directory
        # find the directory's location in the folder widget
        # insert the names of the files in the directory into the folder widget under the directory
        dir_location = folder.get(folder.curselection())
        for file in os.listdir(file_name):
            folder.insert(dir_location, file)

def save_file():
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

def command_line(command):
    REPLYBOX.delete(1.0, END)
    if command == "cached":
        with open('cache/openedfiles.txt') as f:
            for line in f:
                REPLYBOX.insert(END, line)
    elif command =="ls":
        os.system("ls")
    elif command == "":
         # clear REPLYBOX
        REPLYBOX.delete(1.0, END)
    elif command == "clear":
        # clear REPLYBOX
        REPLYBOX.delete(1.0, END)
    elif command == "quit":
        root.destroy()
    elif command == "open":
        load_file()
    elif command == "save":
        save_file()
    elif command == "saveas":
        save_as()
    elif command == "new":
        new_file()
    elif command == "help":
        REPLYBOX.insert(END, "cached - list all cached files\n") #
        REPLYBOX.insert(END, "clear - clear REPLYBOX\n")#
        REPLYBOX.insert(END, "help - list commands\n") #
        REPLYBOX.insert(END, "quit - quit CrispyEditor\n")#
        REPLYBOX.insert(END, "save - save file\n")#
        REPLYBOX.insert(END, "saveas - save as file\n")#
        REPLYBOX.insert(END, "open - open file\n")#
    else:
        REPLYBOX.delete(1.0, END)
        # display os.system output in REPLYBOX
        command = command + "> cache/answer.txt"
        os.system(command)
        with open('cache/answer.txt') as f:
            for line in f:
                REPLYBOX.insert(END, line)
            f.close()
        os.system("rm cache/answer.txt")

# add a folder widget to show the files in the current directory
folder = Listbox(root, height=30, width=50)
folder.configure(font=font, bg=background, fg=textcolor)
folder.pack(side=LEFT, fill=X)
for file in os.listdir():
    filenamex = file
    folder.insert(END, filenamex)
    
    
    
# if a file is selected in the folder widget, load it
folder.bind("<<ListboxSelect>>", lambda event: load_certian_file(folder.get(folder.curselection())))


    
                
#Add a basic commandline to open settings and cached stuff 
COMMANDBOX = Entry(root)
COMMANDBOX.insert(END, "Write a command here")
COMMANDBOX.configure(font=font, bg=background, fg=textcolor)
COMMANDBOX.pack(side=BOTTOM, fill=X)
#add a widget that shows the commands given in COMMANDBOX
COMMANDBOX.bind("<Return>", lambda event: command_line(COMMANDBOX.get()))

REPLYBOX = Text(root, height=30, width=50)
REPLYBOX.insert(END, "CrispyCommandLine")
REPLYBOX.configure(font=font, bg=background, fg=textcolor)
REPLYBOX.pack(side=BOTTOM, fill=X)




#add a menu for saving and opening
menu_bar = Menu(root)
root.config(menu=menu_bar)
file_menu = Menu(menu_bar)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=load_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as)
file_menu.add_command(label="New", command=new_file)

#open the last file in cache/openedfiles.txt
with open('cache/openedfiles.txt') as f:
    try:
        # load the last file in cache/openedfiles.txt
            file_name = f.readlines()[-1]
            file_name = file_name.strip('\n')
            text_info.delete(1.0,END)
            text_info.insert(END, open(file_name).read())
            # if extension is .py turn syntax on
            if file_name.endswith(".py"):
                ip.Percolator(text_info).insertfilter(cdg)
            else:
                pass
            f.close()
    except IndexError:
        pass


root.mainloop()