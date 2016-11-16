from Tkinter import Tk
import tkMessageBox

def show_error_msg(msg):
    tk = Tk()
    tk.withdraw()
    tkMessageBox.showinfo(title="Error", message=msg)
    tk.destroy()