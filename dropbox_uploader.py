import dropbox
from configurator import Configurator
import graphic_util
import urllib3
import os

''' classe adibita all'ottenimento dell'access_token e al caricamento di file e directory su Dropbox '''

class DropboxUploader:

    app_key = 'das84cyxu58cofs'
    app_secret = 'tqz6sbwibg5bb5v'

    def __init__(self):
        self.config = Configurator()
        self.flow = None
        # setto le informazioni dell'applicazione registrata su Dropbox
        if self.config.get_app_key() == '':
            self.config.set_app_key(self.app_key)
        if self.config.get_app_secret() == '':
            self.config.set_app_secret(self.app_secret)

    def get_authorize_URL(self):
        self.flow = dropbox.client.DropboxOAuth2FlowNoRedirect(self.app_key, self.app_secret)
        authorize_url = self.flow.start()
        return authorize_url

    def set_code(self,code):
        self.config.set_code(code)

    def obtain_access_token(self):
        try:
            access_token, user_id = self.flow.finish(self.config.get_code())
            self.config.set_key(access_token)
        except dropbox.rest.ErrorResponse:
            graphic_util.show_error_msg("Codice errato, effettua di nuovo la configurazione ")
            self.config.set_code('')
            self.config.set_key('')
        except urllib3.exceptions.MaxRetryError:
            graphic_util.show_error_msg("Non sei collegato alla rete! ")
            exit(0)
        except Exception, e:
            graphic_util.show_error_msg(e.message)
            exit(0)

    def test_connection(self, access_token):
        dropbox.client.DropboxClient(access_token)

    def has_valid_access_token(self):
        if self.config.get_key() == '':
            return False
        try:
            self.test_connection(self.config.get_key())
            return True
        except dropbox.rest.ErrorResponse:
            graphic_util.show_error_msg("Codice errato, effettua di nuovo la configurazione ")
            self.config.set_code('')
            self.config.set_key('')
            return False
        except urllib3.exceptions.MaxRetryError:
            graphic_util.show_error_msg("Non sei collegato alla rete! ")
            exit(0)
        except Exception, e:
            graphic_util.show_error_msg(e.message)
            exit(0)

    def upload_file(self, path_file_local, path_file_remote):
        try:
            client = dropbox.client.DropboxClient(self.config.get_key())
            f = open(path_file_local, 'rb')
            try:
                client.file_delete(path_file_remote)
            except dropbox.rest.ErrorResponse:
                #l'eccezione indica che il file da rimuovere non esiste, non ha importanza
                pass
            response = client.put_file(path_file_remote, f)
            print 'uploaded: ', response
            f.close();
        except dropbox.rest.ErrorResponse, e:
            graphic_util.show_error_msg(e.message)
            os._exit(0)
        except urllib3.exceptions.MaxRetryError:
            graphic_util.show_error_msg("Non sei collegato alla rete! ")
            os._exit(0)
        except IOError:
            graphic_util.show_error_msg("Il file da caricare non e' stato trovato ")
            os._exit(0)
        except Exception, e:
            graphic_util.show_error_msg(e.message)
            os._exit(0)

    def upload_directory(self, path_dir_local, path_dir_remote):
        try:
            client = dropbox.client.DropboxClient(self.config.get_key())

            #carico tutti i file trovati
            for root, dirnames, filenames in os.walk(path_dir_local):
                for filename in filenames:
                    if not filename.endswith('.ldb') :
                        abs_local_path = os.path.join(root, filename).replace('\\', '/')
                        rel_local_path = os.path.relpath(abs_local_path, path_dir_local).replace('\\', '/')
                        path_file_remote = path_dir_remote+'/'+rel_local_path

                        #provo a leggere il file locale
                        try:
                            f = open(abs_local_path, 'rb')
                            try:
                                client.file_delete(path_file_remote)
                            except dropbox.rest.ErrorResponse:
                                # l'eccezione indica che il file da rimuovere non esiste, non ha importanza
                                pass

                            #carico il file
                            response = client.put_file(path_file_remote, f)
                            print 'uploaded: ', response
                            f.close();

                        except dropbox.rest.ErrorResponse, e:
                            graphic_util.show_error_msg(e.message)

                        except urllib3.exceptions.MaxRetryError:
                            graphic_util.show_error_msg("Non sei collegato alla rete! ")
                            os._exit(0)

                        except IOError:
                            graphic_util.show_error_msg("Il file da caricare non e' stato trovato ")

                        except Exception, e:
                            graphic_util.show_error_msg(e.message)
                            os._exit(0)

        except dropbox.rest.ErrorResponse, e:
            graphic_util.show_error_msg(e.message)
            os._exit(0)
        except urllib3.exceptions.MaxRetryError:
            graphic_util.show_error_msg("Non sei collegato alla rete! ")
            os._exit(0)
        except IOError:
            graphic_util.show_error_msg("Il file da caricare non e' stato trovato ")
            os._exit(0)
        except Exception, e:
            graphic_util.show_error_msg(e.message)
            os._exit(0)