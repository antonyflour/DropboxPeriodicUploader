from tkinter import Tk
from tkinter import messagebox

def show_error_msg(msg):
    tk = Tk()
    tk.withdraw()
    messagebox.showinfo(title="Error", message=msg)
    tk.destroy()