__author__ = 'AvbrehtL14'
from tkinter import *
#from tkinter.filedialog import *

class tkmlin:
    def __init__(self,master):
        self.master = master
        self.master.minsize(width=600, height=600)

root = Tk()
root.wm_title('Nine Man\'s Morris')
okno = tkmlin(root)
root.mainloop()