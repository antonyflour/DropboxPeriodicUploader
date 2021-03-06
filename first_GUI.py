from tkinter import *
from tkinter import messagebox

def showFirstConfig(authorize_url, uploader):
    length = len(authorize_url) + 30
    root = Tk()

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            exit(0)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.wm_title('Dropbox Periodical Uploader - Prima configurazione')
    ent1 = Entry(root, state='readonly', width=length)
    ent1.grid(row=0)
    var = StringVar()
    var.set("Segui le seguenti istruzioni:")
    ent1.config(textvariable=var, relief='flat')

    ent2 = Entry(root, state='readonly', width=length)
    ent2.grid(row=1)
    var = StringVar()
    var.set("1.         Collegati al sito: " + authorize_url)
    ent2.config(textvariable=var, relief='flat')

    ent3 = Entry(root, state='readonly', width=length)
    ent3.grid(row=2)
    var = StringVar()
    var.set("2.         Autorizza l'applicazione")
    ent3.config(textvariable=var, relief='flat')

    ent4 = Entry(root, state='readonly', width=length)
    ent4.grid(row=3)
    var = StringVar()
    var.set("4.         Copia il codice che e' comparso")
    ent4.config(textvariable=var, relief='flat')

    ent5 = Entry(root, state='readonly', width=length)
    ent5.grid(row=4)
    var = StringVar()
    var.set("5.         Incollalo nella casella e clicca su OK")
    ent5.config(textvariable=var, relief='flat')

    ent5 = Entry(root, state='readonly', width=30)
    ent5.grid(row=5, column=0)
    var = StringVar()
    var.set("Incolla qui il codice")
    ent5.config(textvariable=var, relief='flat')

    ent6 = Entry(root, width=length - 30)
    ent6.grid(row=5, column=1)

    def saveKey():
        if(len(ent6.get())>10):
            uploader.set_code(ent6.get())
            root.destroy()

        else:
            messagebox.showinfo(title="Error",
                                      message="Chiave non corretta, riprova")

    b1 = Button(root, text='OK', command=saveKey)
    b1.grid(row=7)
    root.mainloop()


