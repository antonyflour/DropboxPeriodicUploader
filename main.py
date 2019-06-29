from dropbox_uploader import DropboxUploader
import os
import graphic_util
import first_GUI
import threading
from time import sleep
import util
import urllib3
import os, shutil
import pystray
from pystray import MenuItem, Menu
from PIL import Image


#Main del programma

# path_local= 'C:/Users/admin/eDT Consulting'
# path_remote= '/Backup/Negozio-Facile-2.0_backup.zip'
# path_zip = 'C:/Users/admin/Negozio-Facile-2.0_backup'
path_local= 'C:/Users/admin/prova'
path_remote= '/Backup/prova_backup.zip'
path_zip = 'C:/Users/admin/prova_backup'
extension = ".zip"
delta_time = 1

last_sinc_time=0
_FINISH = False


uploader = DropboxUploader()
app_key = uploader.app_key
app_secret = uploader.app_secret

# se il percorso specificato non porta ne' ad un file ne' ad una cartella, si interrompe il programma
if not os.path.isfile(path_local) and not os.path.isdir(path_local):
    graphic_util.show_error_msg("Il file da caricare non e' stato trovato")
    exit(0)

def getMainThread():
    for i in threading.enumerate():
        if i.name == 'MainThread':
            return i

# thread in esecuzione fin quando e' in esecuzione anche il mainThread
def periodic_upload():
    mainThread = getMainThread()
    while(mainThread.is_alive() and not uploader.has_connection()):
        sleep(5)

    if not mainThread.is_alive():
        exit(0)

    else:
        # ottengo l'access_token
        while not uploader.has_valid_access_token():
            authorize_url = uploader.get_authorize_URL()
            # nella GUI l'utente inserisce il codice di permission dell'applicazione che serve ad uploader per richiedere l'access_token
            first_GUI.showFirstConfig(authorize_url, uploader)
            uploader.obtain_access_token()

        #inizio il caricamento
        while(not _FINISH):
            # rimuovo il file zip se gia esiste
            if os.path.exists(path_zip+extension):
                os.remove(path_zip+extension)

            #comprimo la cartella da caricare in un unico archivio zip
            shutil.make_archive(path_zip, 'zip', root_dir=path_local, base_dir=path_local)

            now_time = util.get_now_time_minutes()
            global last_sinc_time
            #verifico che sia scaduto il delta time (intervallo di sincronizzazione)
            if (now_time - last_sinc_time) >= delta_time:
                try:
                    #carico il file zip
                    uploader.upload_file(path_zip+extension, path_remote)

                    #aggiorno il time dell'ultima sincronizzazione
                    last_sinc_time = now_time

                #se il caricamento fallisce per mancanza di connessione mi metto in attesa di avere connessione
                except urllib3.exceptions.MaxRetryError:
                    graphic_util.show_error_msg("Attendo che tu sia collegato alla rete! ")
                    while not uploader.has_connection():
                        if _FINISH:
                            # se il main non e' piu' attivo, termino anche il processo di caricamento
                            exit(0)
                        else:
                            sleep(5)

                    graphic_util.show_error_msg("Riprendo il caricamento")

            #sospendo il processo per 5 secondi
            sleep(5)

#avvio il caricamento in un altro thread; il thread principale viene usato dalla tray icon
thread_uploader = threading.Thread(name='PeriodicUploader',target=periodic_upload)
thread_uploader.start()

#creo l'icona
TRAY_TOOLTIP = 'Dropbox Periodic Uploader'
TRAY_ICON = 'icon.png'

def stop():
    global _FINISH
    _FINISH = True
    icon.stop()

menu = Menu((MenuItem('Exit', stop)))
image = Image.open(TRAY_ICON)

icon = pystray.Icon(TRAY_TOOLTIP, image, TRAY_TOOLTIP, menu)
icon.run()
