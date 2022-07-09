from android import basarili, noadded, pip_, bilgi, soru, logo, clabtoken 
import asyncio
import sys
import time
import random   

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError, PasswordHashInvalidError, PhoneNumberInvalidError
from telethon.network import ConnectionTcpAbridged
from telethon.sessions import StringSession

try:
   import requests
   import bs4
except:
   pip_("requests")
   pip_("bs4")
finally:
    import requests
    import bs4
# Original Source https://github.com/LonamiWebs/Telethon/master/telethon_examples/interactive_telegram_client.py #
loop = asyncio.get_event_loop()

class InteractiveTelegramClient(TelegramClient):
    def __init__(self, session_user_id, api_id, api_hash,
                 telefon=None, proxy=None):
        super().__init__(
            session_user_id, api_id, api_hash,
            connection=ConnectionTcpAbridged,
            proxy=proxy
        )
        self.found_media = {}
        bilgi('@CerceynLab String Alıcıya Hoş Geldiniz')
        bilgi('[i] Telegramın Sunucularına Bağlanılıyor...')
        try:
            loop.run_until_complete(self.connect())
        except IOError:
            noadded('[!] Bağlanılırken bir hata oluştu. Yeniden deneniyor...')
            loop.run_until_complete(self.connect())

        if not loop.run_until_complete(self.is_user_authorized()):
            if telefon == None:
               user_phone = input('[?] Telefon Numaranız (Örnek: +90xxxxxxxxxx): ')
            else:
               user_phone = telefon
            try:
                loop.run_until_complete(self.sign_in(user_phone))
                self_user = None
            except PhoneNumberInvalidError:
                noadded("[!] Geçersiz Bir Numara Girdiniz Örnekte Gibi Giriniz. Örnek: +90xxxxxxxxxx")
                exit(1)
            except ValueError:
               noadded("[!] Geçersiz Bir Numara Girdiniz Örnekte Gibi Giriniz. Örnek: +90xxxxxxxxxx")
               exit(1)

            while self_user is None:
                code = input('[?] Telegramdan Gelen Beş (5) Haneli Kodu Giriniz: ')
                try:
                    self_user =\
                        loop.run_until_complete(self.sign_in(code=code))
                except PhoneCodeInvalidError:
                    print("[!] Kodu Yanlış Yazdınız. Lütfen Tekrar Deneyiniz. [Fazla Deneme Yapmak Ban Yemenize Neden Olur]")
                except SessionPasswordNeededError:
                    pw = input('[i] İki aşamalı doğrulama tespit edildi. '
                                 '[?] Şifrenizi Yazınız: ')
                    try:
                        self_user =\
                            loop.run_until_complete(self.sign_in(password=pw))
                    except PasswordHashInvalidError:
                        noadded("[!] 2 Aşamalı Şifrenizi Yanlış Yazdınız. Lütfen Tekrar Deneyiz. [Fazla Deneme Yapmak Ban Yemenize Neden Olur]")
test_key = 'MyKey4TestingYnP'
if __name__ == '__main__':
   logo(True)
   bilgi("[1] OtoMatik API ID/HASH Alıcı")
   bilgi("[2] String Alıcı")
   bilgi("[3] CLab-AccountToken Oluşturucu")
   try:
      secim = int(input("[?] Seçim Yapın: "))
   except:
      noadded("[!] Lütfen Sadece Rakam Giriniz!")
      exit(1)
   if secim == 3:
      api_id = soru("Hesabınızın API ID'i:")
      try:
        check_api = int(api_id)
      except Exception:
        hata("🛑 API ID Hatalı ! 🛑")
      api_hash = soru("Hesabınızın API HASH'i:")
      if not len(api_hash) >= 30:
        hata("🛑 API HASH Hatalı ! 🛑")
      stringsession = soru("Hesabınızın String'i:")
      if not len(api_hash) >= 30:
        hata("🛑 String Hatalı ! 🛑")
      text = "{}|{}|{}".format(api_id, api_hash, stringsession)
      Token = clabtoken(f"CLab&&{text}&&{test_key}",False)
      bilgi("[i] CLab-AccountToken Aşağıdadır:")
      print(Token)
   elif secim == 2:
      API_ID = soru('[?] API ID\'iniz [Hazır Key\'leri Kullanmak İçin Boş Bırakınız]: ')
      if API_ID == "":
         print("[i] Hazır Keyler Kullanılıyor...")
         API_ID = 4
         API_HASH = "014b35b6184100b085b0d0572f9b5103"
      else:
         API_HASH = input('[?] API HASH\'iniz: ')
      client = InteractiveTelegramClient(StringSession(), API_ID, API_HASH)
      stringsession=client.session.save()
      print("[i] String Keyiniz Aşağıdadır!\n\n" + stringsession)
      text = "{}|{}|{}".format(API_ID, API_HASH, stringsession)
      Token = clabtoken(f"CLab&&{text}&&{test_key}",False)
      bilgi("[i] CLab-AccountToken Aşağıdadır:")
      print(Token)
   elif secim == 1:
      numara = soru("[?] Telefon Numaranız: ")
      try:
         rastgele = requests.post("https://my.telegram.org/auth/send_password", data={"phone": numara}).json()["random_hash"]
      except:
         noadded("[!] Kod Gönderilemedi. Telefon Numaranızı Kontrol Ediniz.")
         exit(1)
      
      sifre = input("[?] Telegram'dan Gelen Kodu Yazınız: ")
      try:
         cookie = requests.post("https://my.telegram.org/auth/login", data={"phone": numara, "random_hash": rastgele, "password": sifre}).cookies.get_dict()
      except:
         noadded("[!] Büyük İhtimal Kodu Yanlış Yazdınız. Lütfen Scripti Yeniden Başlatın.")
         exit(1)
      app = requests.post("https://my.telegram.org/apps", cookies=cookie).text
      soup = bs4.BeautifulSoup(app, features="html.parser")

      if soup.title.string == "Create new application":
         bilgi("[i] Uygulamanız Yok. Oluşturuluyor...")
         hashh = soup.find("input", {"name": "hash"}).get("value")
         AppInfo = {
            "hash": hashh,
            "app_title":"Cerceyn UserBot",
            "app_shortname": "Cerceynus" + str(random.randint(9, 99)) + str(time.time()).replace(".", ""),
            "app_url": "",
            "app_platform": "android",
            "app_desc": ""
         }
         app = requests.post("https://my.telegram.org/apps/create", data=AppInfo, cookies=cookie).text
         print(app)
         bilgi("[i] Uygulama başarıyla oluşturuldu!")
         bilgi("[i] API ID/HASH alınıyor...")
         newapp = requests.get("https://my.telegram.org/apps", cookies=cookie).text
         newsoup = bs4.BeautifulSoup(newapp, features="html.parser")

         g_inputs = newsoup.find_all("span", {"class": "form-control input-xlarge uneditable-input"})
         app_id = g_inputs[0].string
         api_hash = g_inputs[1].string
         basarili("[i] Bilgiler Getirildi! Lütfen Bunları Not Ediniz.\n\n")
         bilgi(f"[i] API ID: {app_id}")
         bilgi(f"[i] API HASH: {api_hash}")
         try:
            stringonay = int(input("[?] String Almak İster Misiniz? [Evet için 1 Yazınız]: "))
         except:
            print("[!] Lütfen Sadece Sayı Yazınız!")

         if stringonay == 1:
            client = InteractiveTelegramClient(StringSession(), app_id, api_hash, numara)
            bilgi("[i] String Keyiniz Aşağıdadır!\n\n\n" + client.session.save())
            text = "{}|{}|{}".format(app_id, api_hash, stringsession)
            Token = clabtoken(f"CLab&&{text}&&{test_key}",False)
            bilgi("[i] CLab-AccountToken Aşağıdadır:")
            print(Token)
         else:
            bilgi("[i] Script Durduruluyor...")
            exit(1)
      elif  soup.title.string == "App configuration":
         print("[i] Halihazır da Uygulama Oluşturmuşsunuz. API ID/HASH Çekiliyor...")
         g_inputs = soup.find_all("span", {"class": "form-control input-xlarge uneditable-input"})
         app_id = g_inputs[0].string
         api_hash = g_inputs[1].string
         print("[i] Bilgiler Getirildi! Lütfen Bunları Not Ediniz.\n\n")
         print(f"[i] API ID: {app_id}")
         print(f"[i] API HASH: {api_hash}")
         try:
            stringonay = int(input("[?] String Almak İster Misiniz? [Evet için 1 Yazınız]: "))
         except:
            noadded("[!] Lütfen Sadece Sayı Yazınız!")
            raise IndexError("Lütfen Sadece Sayı Yazınız!")

         if stringonay == 1:
            client = InteractiveTelegramClient(StringSession(), app_id, api_hash, numara)
            stringsession=client.session.save()
            print("[i] String Keyiniz Aşağıdadır!\n\n" + stringsession)
            text = "{}|{}|{}".format(app_id, api_hash, stringsession)
            Token = clabtoken(f"CLab&&{text}&&{test_key}",False)
            bilgi("[i] CLab-AccountToken Aşağıdadır:")
            print(Token)
         else:
            noadded("[i] Script Durduruluyor...")
            exit(1)
      else:
         noadded("[!] Bir Hata Oluştu.")
         exit(1)
   else:
      noadded("[!] Bilinmeyen seçim.")
