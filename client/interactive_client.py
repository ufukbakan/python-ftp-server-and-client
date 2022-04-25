from ftplib import FTP
from functools import partial
from pathlib import Path

ui = "1"
host = "localhost"
port = 2121
username = "anonymous" # ufuk
pwd = "" # 123456
downloadsFolder = Path(__file__).parent.absolute().joinpath(".\\Downloads")
currentFolder = Path(__file__).parent.absolute()


def satirYazdir(bytes):
    print(bytes.decode("utf-8"))


def dosyayaYazdir(dosya, bytes):
    dosya.write(bytes)


def printMainMenu():
    print("===========")
    print("0. Çıkış")
    print("1. Sunucu adı gir")
    print("2. Sunucu port gir")
    print("3. Kullanıcı adı gir")
    print("4. Kullanıcı şifresi gir")
    print("5. Konfigürasyonu göster")
    print("6. FTP Sunucusuna bağlan")
    print("===========")


def printFTPMenu():
    print("=======")
    print("0: Çıkış")
    print("1: Dosya/Dizin listele")
    print("2: Dizin değiştir")
    print("3: Dosya indir")
    print("4: Dosya yükle")
    print("5: Dosya/Dizin yeniden adlandır")
    print("6: Dosya sil")
    print("7. Dizin oluştur")
    print("8. Dizin sil")
    print("9. Dosya oku")
    print("=======")


def handleFTPMenuInput(ftp):
    global ui
    if ui == '1':
        # VEYA ftp.dir() komutuyla gerçekleştirilebilir
        print(ftp.retrlines("LIST", print))
    elif ui == '2':
        ui = input("Geciş yapmak istediğiniz dizini girin: ")
        ftp.cwd(ui)
    elif ui == '3':
        filename = input("İndirmek istediğiniz dosya adını girin: ")
        retr_command = "RETR " + filename
        relative_filename = ".\\"+filename
        file = open(downloadsFolder.joinpath(relative_filename), "wb")
        yazCallback = partial(dosyayaYazdir, file)
        ftp.retrbinary(retr_command, yazCallback)
        print("Tamamlandı")

    elif ui == '4':
        filename = input("Yüklemek istediğiniz dosya adını girin: ")
        stor_command = "STOR " + filename
        relative_filename = ".\\"+filename
        file = open(currentFolder.joinpath(relative_filename), "rb")
        ftp.storbinary(stor_command, file)
        print("Tamamlandı")

    elif ui == '5':
        oldname = input("İsmini değiştirmek istediğiniz dosyayı girin: ")
        newname = input("Yeni ismi girin: ")
        ftp.rename(oldname, newname)
        print("Tamamlandı")

    elif ui == '6':
        file = input("Silmek istediğiniz dosyanın adını girin: ")
        ftp.delete(file)
        print("Tamamlandı")

    elif ui == '7':
        folder = input("Oluşturmak istediğiniz dizin adını girin: ")
        ftp.mkd(folder)
        print("Tamamlandı")

    elif ui == '8':
        folder = input("Silmek istediğiniz dizin adını girin: ")
        ftp.rmd(folder)
        print("Tamamlandı")

    elif ui == '9':
        filename = input("Okumak istediğiniz dosya adını girin: ")
        retr_command = "RETR " + filename
        relative_filename = ".\\"+filename
        ftp.retrbinary(retr_command, satirYazdir)
        print("Tamamlandı")


def ftpLoop(ftp):
    global ui
    while (ui != '0'):
        printFTPMenu()
        ui = input("Seçiminizi girin: ")
        try:
            handleFTPMenuInput(ftp)
        except Exception as e:
            print(e)
    ftp.quit()
    ui = -1


def handleMainMenuInput():
    global host, port, username, pwd, ui
    if ui == '1':
        host = input()
    elif ui == '2':
        port = int(input())
    elif ui == '3':
        username = input()
    elif ui == '4':
        pwd = input()
    elif ui == '5':
        print("%s:%d usr:%s pwd:%s" % (host, port, username, pwd))
    elif ui == '6':
        ftp = FTP()
        ftp.encoding = "UTF-8"
        ftp.connect(host, port)
        ftp.login(username, pwd)
        print(ftp.getwelcome())  # ftp serverdaki banner mesajını getirir
        print("Bulunduğunuz dizin", ftp.pwd())
        ftpLoop(ftp)


while ui != "0":
    printMainMenu()
    ui = input("Seçeneğinizi girin: ")
    handleMainMenuInput()
