from dropbox import DropboxOAuth2FlowNoRedirect
import dropbox
from configurator import Configurator
import graphic_util
import urllib3
import os
import requests

''' classe adibita all'ottenimento dell'access_token e al caricamento di file e directory su Dropbox '''

class DropboxUploader:

    app_key = ''
    app_secret = ''

    def __init__(self):
        self.config = Configurator()
        self.flow = None
        # setto le informazioni dell'applicazione registrata su Dropbox
        if self.config.get_app_key() == '':
            self.config.set_app_key(self.app_key)
        if self.config.get_app_secret() == '':
            self.config.set_app_secret(self.app_secret)

    def get_authorize_URL(self):
        self.flow = DropboxOAuth2FlowNoRedirect(self.app_key, self.app_secret)
        authorize_url = self.flow.start()
        return authorize_url.strip()

    def set_code(self,code):
        self.config.set_code(code)

    def obtain_access_token(self):
        try:
            oauth_result = self.flow.finish(self.config.get_code())
            self.config.set_key(oauth_result.access_token)
        except requests.exceptions.HTTPError:
            graphic_util.show_error_msg("Codice errato, effettua di nuovo la configurazione ")
            self.config.set_code('')
            self.config.set_key('')
        except urllib3.exceptions.MaxRetryError:
            graphic_util.show_error_msg("Non sei collegato alla rete! ")
            exit(0)
        except Exception as e:
            graphic_util.show_error_msg(e)
            exit(0)

    def has_connection(self):
        try:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            http = urllib3.PoolManager()
            url = 'https://www.dropbox.com'
            response = http.request('GET', url)
            return True
        except urllib3.exceptions.MaxRetryError:
            return False


    def has_valid_access_token(self):
        if self.config.get_key() == '':
            return False
        try:
            client = dropbox.Dropbox(self.config.get_key())
            client.users_get_current_account()
            return True
        except dropbox.rest.ErrorResponse as e:
            graphic_util.show_error_msg("Codice errato, effettua di nuovo la configurazione [dropbox_uploader.py line 57]" + e.message)
            self.config.set_code('')
            self.config.set_key('')
            return False
        except Exception as e:
            graphic_util.show_error_msg("[dropbox_uploader.py line65]"+ e.message)
            exit(0)

    def upload_file(self, path_file_local, path_file_remote):
        try:
            client = dropbox.Dropbox(self.config.get_key())
            with open(path_file_local, 'rb') as f:
                data = f.read()
            mode = dropbox.files.WriteMode.overwrite
            resp = client.files_upload(data, path_file_remote, mode, mute=True)
        except dropbox.exceptions.ApiError as e:
            graphic_util.show_error_msg(e)
            os._exit(0)
        except IOError as e:
            graphic_util.show_error_msg(e)
            os._exit(0)
        except Exception as e:
            graphic_util.show_error_msg(e)
            os._exit(0)

