from ftplib import FTP


class FTPservice():
    retr = 'RETR '
    stor = 'STOR '

    def __init__(self, ftp_address='127.0.0.1'):
        self.ftp = FTP(ftp_address)
        self.ftp.login()

    def dowload_file(self, file_name, file_path_download='temp/', file_source_on_server=''):
        my_file = open(file_path_download + file_name, 'wb')
        self.ftp.retrbinary(self.retr + file_source_on_server + file_name, my_file.write, 1024)

    def upload_file(self, file_name, user_directory, file_path):
        file_to_upload = open(file_path, 'rb')
        self.ftp.storbinary(self.stor+user_directory + "\\" + file_name, file_to_upload)
        file_to_upload.close()

    def update_file(self, file_name, file_source_on_client='', file_source_on_server=''):
        self.delete_file(self, file_name, file_source_on_server)
        self.upload_file(self, file_name, file_source_on_client)

    def delete_file(self, file_name, file_source=''):
        self.ftp.delete(file_source + file_name)

    def list_files(self):
        print()
        self.ftp.retrlines('LIST')

    def create_user_directory(self, user):
        try:
            self.ftp.mkd(user)
        except:
            pass
