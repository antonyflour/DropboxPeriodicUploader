from Tkinter import *
import tkMessageBox


def showFirstConfig(authorize_url):
    length = len(authorize_url) + 30
    root = Tk()

    def on_closing():
        if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
            exit(0)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.wm_title('Dropbox Periodical Uploader - Prima configurazione')
    ent1 = Entry(root, state='readonly', width=length)
    ent1.grid(row=0)
    var = StringVar()
    var.set("Segui le seguenti istruzioni:")
    ent1.config(textvariable=var, relief='flat')
    ent1.pack()

    ent2 = Entry(root, state='readonly', width=length)
    ent2.grid(row=1)
    var = StringVar()
    var.set("1.         Collegati al sito: " + authorize_url)
    ent2.config(textvariable=var, relief='flat')
    ent2.pack()

    ent3 = Entry(root, state='readonly', width=length)
    ent3.grid(row=2)
    var = StringVar()
    var.set("2.         Autorizza l'applicazione")
    ent3.config(textvariable=var, relief='flat')
    ent3.pack()

    ent4 = Entry(root, state='readonly', width=length)
    ent4.grid(row=3)
    var = StringVar()
    var.set("4.         Copia il codice che e' comparso")
    ent4.config(textvariable=var, relief='flat')
    ent4.pack()

    ent5 = Entry(root, state='readonly', width=length)
    ent5.grid(row=4)
    var = StringVar()
    var.set("5.         Incollalo nella casella e clicca su OK")
    ent5.config(textvariable=var, relief='flat')
    ent5.pack()

    ent5 = Entry(root, state='readonly', width=30)
    ent5.grid(row=5, column=0)
    var = StringVar()
    var.set("Incolla qui il codice")
    ent5.config(textvariable=var, relief='flat')
    ent5.pack(side='left')

    ent6 = Entry(root, width=length - 30)
    ent6.grid(row=5, column=1)
    ent6.pack()

    def saveKey():
        try:
            if(len(ent6.get())>10):
                f = open('code.txt','w+')
                f.writelines(ent6.get().split())
                f.close();
                root.destroy()

            else:
                tkMessageBox.showinfo(title="Error",
                                      message="Chiave non corretta, riprova")
        except:
            tkMessageBox.showinfo(title="Error", message="Problema nel salvataggio della chiave, procedura annullata")
            exit(0)
    b1 = Button(root, text='OK', command=saveKey)
    b1.grid(row=7)
    b1.pack(side='left')
    root.mainloop()


