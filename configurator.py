import os
class Configurator:
    ''' classe che gestisce il file di configurazione'''

    file_name = 'config.conf'

    def __init__(self):
        self.data = {'app_key':'','app_secret':'','code':'','key':''}
        if not os.path.isfile(self.file_name):
            file = open(self.file_name, 'w+')
            file.close()
        self.data['app_key'] = self._read_value_field(self.file_name, 'app_key')
        self.data['app_secret'] = self._read_value_field(self.file_name, 'app_secret')
        self.data['code']=self._read_value_field(self.file_name,'code')
        self.data['key']=self._read_value_field(self.file_name,'key')

    def print_data(self):
        print self.data

    def _read_value_field(self, file_name, field):
        field = field + '='
        file = open(file_name,'r')
        lines = file.readlines()
        file.close()
        for str in lines:
            if field in str:
                return str[len(field):].replace('\n','')
        return ''


    def get_app_key(self):
        return self.data.get('app_key')

    def get_app_secret(self):
        return self.data.get('app_secret')

    def get_code(self):
        return self.data.get('code')

    def get_key(self):
        return self.data.get('key')

    def set_app_key(self, app_key):
        self.data['app_key']=app_key
        self._write_data()

    def set_app_secret(self, app_secret):
        self.data['app_secret']=app_secret
        self._write_data()

    def set_code(self, code):
        self.data['code']=code
        self._write_data()

    def set_key(self, key):
        self.data['key']=key
        self._write_data()

    def _write_data(self):
        file = open(self.file_name,'w+')
        for str in self.data:
            file.write(str + '=' + self.data.get(str)+'\n')
        file.close()


