from ftplib import FTP

host = "videoftptut.bplaced.net"
user = "videoftptut"
password = "neural123"

def retrieve_ftp():
    with open('text.txt', 'wb') as f:
        ftp.retrbinary("RETR " + "mytest.txt", f.write, 1024)


def send_ftp():
    with open('myupload.txt', 'rb') as f:
        ftp.storbinary("STOR " + "upload.txt", f)


with FTP(host) as ftp:

    ftp.login(user=user, passw=password)
    print(ftp.getwelcome())

    '''use functions'''

    ftp.quit()

