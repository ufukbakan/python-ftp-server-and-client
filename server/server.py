# pip install pyftpdlib
from pyftpdlib import authorizers
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pathlib import Path

currentPath = Path(__file__).parent.absolute().__str__()

myAuthorizer = authorizers.DummyAuthorizer()

#add_user(kullanıcı adı (str), şifre (str), ev dizini (str), yetkiler (str), giriş mesajı (str), çıkış mesajı (str))
# ufuk kullanıcısına okuma ve yazma yetkileri :
myAuthorizer.add_user("ufuk", "123456", currentPath+"\\home\\ufuk".__str__(), "elradfmw", "Giriş Başarılı", "Çıkış Yapıldı")
"""
Yekiler :

Read permissions:
"e" = change directory (CWD, CDUP commands)
"l" = list files (LIST, NLST, STAT, MLSD, MLST, SIZE commands)
"r" = retrieve file from the server (RETR command)

Write permissions:
"a" = append data to an existing file (APPE command)
"d" = delete file or directory (DELE, RMD commands)
"f" = rename file or directory (RNFR, RNTO commands)
"m" = create directory (MKD command)
"w" = store a file to the server (STOR, STOU commands)
"M" = change file mode / permission (SITE CHMOD command) New in 0.7.0
"T" = change file modification time (SITE MFMT command) New in 1.5.3

"""
#add_anonymous(ev dizini, **kwargs)
# anonim kullanıcıya hiçbir yetki verme :
myAuthorizer.add_anonymous(currentPath+"\\home\\anonymous".__str__(), perm="")


myHandler = FTPHandler
myHandler.timeout = 0
myHandler.banner = "FTP Server'a hoş geldiniz"
myHandler.authorizer = myAuthorizer


myFTPServer = FTPServer(("localhost", 2121), myHandler)
myFTPServer.serve_forever()