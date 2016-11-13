# Include the Dropbox SDK
import first_GUI
import dropbox
import threading
import pystray
from pystray import Menu as menu, MenuItem as item
from time import sleep
from PIL import Image, ImageDraw
import tkMessageBox
from Tkinter import Tk
import os
import urllib3
import util

app_key = 'das84cyxu58cofs'
app_secret = 'tqz6sbwibg5bb5v'
delta_time = 5
global last_sinc_time
last_sinc_time=0

path_file_local='C:/Users/anton/Documents/Prova/prova.txt'
path_file_remote='/Prova/prova.txt'

# Main Program

#se il file da caricare non esiste, il programma viene interrotto
try:
    f = open(path_file_local)
    f.close()
except IOError:
    tk = Tk()
    tk.withdraw()
    tkMessageBox.showinfo(title="Error", message="Il file da caricare non e' stato trovato")
    os._exit(0)


hasKey=False
while(hasKey != True):
    try:
        f = open('key.txt','rb')
        hasKey = True
    except:
        # prima configurazione
        flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
        authorize_url = flow.start()
        first_GUI.showFirstConfig(authorize_url)
        f = open('code.txt', 'rb')
        code= f.readline();
        f.close();
        try:
            access_token, user_id = flow.finish(code)
            f = open('key.txt', 'w+')
            f.writelines(access_token)
            f.close()
        except dropbox.rest.ErrorResponse:
            tk = Tk()
            tk.withdraw()
            tkMessageBox.showinfo(title="Error",
                                  message="Chiave errata, riavvia il programma e effettua di nuovo la configurazione ")
            os.remove('key.txt')
            os.remove('code.txt')
            exit(0)
        except urllib3.exceptions.MaxRetryError:
            tk = Tk()
            tk.withdraw()
            tkMessageBox.showinfo(title="Error", message="Non sei collegato alla rete! ")
            exit(0)
        except Exception, e:
            tk = Tk()
            tk.withdraw()
            tkMessageBox.showinfo(title="Error", message=e.message)
            exit(0)

access_token = f.readline()
f.close();

def uploadFile():
    now_time = util.get_now_time_minutes()
    if (now_time - last_sinc_time)>=delta_time:
        try:
            client = dropbox.client.DropboxClient(access_token)
            print 'linked account: ', client.account_info()
            f = open(path_file_local, 'rb')
            try:
                client.file_delete(path_file_remote)
            except dropbox.rest.ErrorResponse:
                pass
            response = client.put_file(path_file_remote, f)
            print 'uploaded: ', response
            f.close();
            global last_sinc_time
            last_sinc_time = now_time
        except dropbox.rest.ErrorResponse, e:
            tk = Tk()
            tk.withdraw()
            tkMessageBox.showinfo(title="Error",
                              message=e.error_msg)

            os._exit(0)
        except urllib3.exceptions.MaxRetryError:
            tk = Tk()
            tk.withdraw()
            tkMessageBox.showinfo(title="Error", message="Non sei collegato alla rete! ")
            os._exit(0)
        '''except IOError:
            tk = Tk()
            tk.withdraw()
            tkMessageBox.showinfo(title="Error", message="Il file da caricare non e' stato trovato")
            os._exit(0)
        except Exception, e:
            tk = Tk()
            tk.withdraw()
            tkMessageBox.showinfo(title="Error", message=e.message)
            os._exit(0)
'''
# thread in esecuzione fin quando e' in esecuzione anche il mainThread
def periodicUpload():
    while True:
        for i in threading.enumerate():
            if i.name == 'MainThread':
                if i.is_alive():
                    uploadFile()
                    sleep(5)
                else:
                    exit(0)

def setup(icon):
    icon.visible = True


def stop(icon):
    icon.stop()


icon = pystray.Icon('Dropbox Periodical Uploader')
# Generate an image
width = 50;
height = 50;
color1 = '#0066ff'
image = Image.new('RGB', (width, height), color1)
dc = ImageDraw.Draw(image)
icon.icon=image
icon.title='Dropbox Periodical Uploader'
icon.menu=menu(item("Exit", stop, default=True))
uploader = threading.Thread(name='PeriodicUploader',target=periodicUpload)
uploader.start()
icon.run(setup)
