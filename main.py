from dropbox_uploader import DropboxUploader
from tray import TrayIcon
import os
import graphic_util
import first_GUI
import threading
from time import sleep
import util
import urllib3

#Main del programma

path_local= 'C:/Users/anton/Documents/Prova'
path_remote= '/Prova'

delta_time = 1
last_sinc_time=0


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
        while mainThread.is_alive():
            now_time = util.get_now_time_minutes()
            #verifico che sia scaduto il delta time (intervallo di sincronizzazione)
            if (now_time - last_sinc_time) >= delta_time:
                try:
                    #se il path punta ad un file
                    if os.path.isfile(path_local):
                        #carico un file
                        uploader.upload_file(path_local, path_remote)

                    #se punta ad una directory
                    else:
                        #carico tutti i file all'interno della directory, rispettando l'albero delle directory
                        uploader.upload_directory(path_local, path_remote)

                    #aggiorno il time dell'ultima sincronizzazione
                    global last_sinc_time
                    last_sinc_time = now_time

                #se il caricamento fallisce per mancanza di connessione mi metto in attesa di avere connessione
                except urllib3.exceptions.MaxRetryError:
                    graphic_util.show_error_msg("Attendo che tu sia collegato alla rete! ")
                    while not uploader.has_connection():
                        if not mainThread.is_alive():
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
tray_icon = TrayIcon(False)
tray_icon.show()
