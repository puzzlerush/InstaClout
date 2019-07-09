from tkinter import *
from PIL import Image, ImageTk
import threading
from followerbot import check_directory, start_bot
from test import getuserlist

def submit(event):
    login_username, login_password, follower_list, start_follow, end_follow, duration, timeout, ratio = [entry.get() for entry in entries]
    def callback():
        start_bot(login_username, login_password, int(duration), follower_list, int(start_follow), int(end_follow), int(timeout), int(ratio))
    t = threading.Thread(target=callback)
    t.start()
def get_users(event):
    login_username, login_password, account, follower_num, timeout = entryusername.get(), entrypassword.get(), entryaccount.get(), entrynum.get(), entrytimeout.get()
    def callback():
        getuserlist(login_username, login_password, account, int(follower_num), int(timeout))
    t = threading.Thread(target=callback)
    t.start()

root = Tk()
root.title('InstaClout')
root.iconbitmap('favicon.ico')
root.geometry('640x360')
root.resizable(0,0)

image = Image.open('sad.png')
image = image.resize((200, 200), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(image)
label = Label(image=photo)
label.image = photo
label.place(x=100, y=0, relwidth=1, relheight=1)

labeltext = ['Username: ', 'Password: ', 'Userlist: ', 'List start index: ', 'List end index: ', 'Duration: ', 'Timeout: ', 'Ratio: ']
entryusername, entrypassword, entryfollowerlist, entrystart, entryend, entryduration, entrytimeout, entryratio = Entry(root), Entry(root, show = '*'), Entry(root), Entry(root), Entry(root), Entry(root), Entry(root), Entry(root)
entries =[entryusername, entrypassword, entryfollowerlist, entrystart, entryend, entryduration, entrytimeout, entryratio] 

for i in range(len(labeltext)):
    label = Label(root, text = labeltext[i])
    label.grid(row = i, sticky = E, padx = 16, pady = 8)
    entries[i].grid(row = i, column = 1, padx = 2, pady = 8)
    x = i + 1
   
button1 = Button(root, text='Submit')
button1.bind('<Button-1>', submit)
button1.grid(row = x, column = 1)

labeltext2 = ['Account: ', 'Number of users: ']
entryaccount, entrynum = Entry(root), Entry(root)
entries2 = [entryaccount, entrynum]

for i in range(len(labeltext2)):
    label2 = Label(root, text = labeltext2[i])
    label2.grid(row = i, column = 2, padx = 16, pady = 8)
    entries2[i].grid(row = i, column = 3, padx = 2, pady = 8)
    
button1 = Button(root, text='Get users')
button1.bind('<Button-1>', get_users)
button1.grid(row = x, column = 3)

default_text = open('defaults.txt', 'r')
defaults_list = default_text.read().split('\n')
for i in range(len(entries)):
    entries[i].insert(END, defaults_list[i].split('=')[1])

check_directory()
root.mainloop()
