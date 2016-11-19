from dropbox_uploader import DropboxUploader
from tray import TrayIcon
import os
import graphic_util
import first_GUI
import threading
from time import sleep
import util


#Main del programma

path_local= 'C:/Users/anton/Documents/Prova/prova.txt'
path_remote= '/Prova/prova.txt'

delta_time = 1
last_sinc_time=0


uploader = DropboxUploader()
app_key = uploader.app_key
app_secret = uploader.app_secret

# se il percorso specificato non porta ne' ad un file ne' ad una cartella, si interrompe il programma
if not os.path.isfile(path_local) and not os.path.isdir(path_local):
    graphic_util.show_error_msg("Il file da caricare non e' stato trovato")
    exit(0)

# ottengo l'access_token
while not uploader.has_valid_access_token():
    authorize_url = uploader.get_authorize_URL()
    # nella GUI l'utente inserisce il codice di permission dell'applicazione che serve ad uploader per richiedere l'access_token
    first_GUI.showFirstConfig(authorize_url, uploader)
    uploader.obtain_access_token()

# thread in esecuzione fin quando e' in esecuzione anche il mainThread
def periodic_upload():
    #aspetto 10 secondi prima del tentativo di connessione (utile durante l'esecuzione automatica in startup)
    sleep(10)
    while True:
        for i in threading.enumerate():
            if i.name == 'MainThread':
                if i.is_alive():
                    now_time = util.get_now_time_minutes()
                    if (now_time - last_sinc_time) >= delta_time:
                        if os.path.isfile(path_local):
                            uploader.upload_file(path_local, path_remote)
                        else:
                            uploader.upload_directory(path_local, path_remote)
                        global last_sinc_time
                        last_sinc_time = now_time
                    sleep(5)
                else:
                    exit(0)


thread_uploader = threading.Thread(name='PeriodicUploader',target=periodic_upload)
thread_uploader.start()
tray_icon = TrayIcon(False)
tray_icon.show()


