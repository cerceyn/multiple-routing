from traceback import format_exc
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest
from .events import register as clabtetikleyici 
from telethon.events import NewMessage as bberc
from telethon.errors import PeerIdInvalidError
from telethon.sessions import StringSession
from telethon import TelegramClient
from subprocess import PIPE, Popen
from rich import print as rprint
from telethon import types
from time import sleep
from android import *
import asyncio, os
import base64

loop = asyncio.get_event_loop()

def n():
    console.print("\n")
def log(text,renk=None):
    if renk:
        console.log(f"[{renk}]{text}[/{renk}]")
    else:
        console.log(f"{text}")
Token="MTc4Mzc1MjY5ODpBQUUzajlkQ0toSW9kZU5GSTZ3aHEtYkFTd3lPWHBLWXgtWQ=="
try:
    bot = TelegramClient('bot',api_id=6, api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e")
except Exception:
    hata(f"Bir sorunla karşılaştık! Bu hatayı geliştiriciye bildirin:\n{format_exc()}")
async def botagir():
    global bot
    bilgi("Şimdi hesabını tanımam lazım.")
    api_hash=0
    stringsession=None
    api_id = soru("Hesabınızın API ID'i veya CLab-AccountToken:")
    if api_id.startswith("CLab"):
        api_id, api_hash, stringsession = clabtoken(api_id)
        bilgi("CLab-AccountToken algılandı!")
    else:
        try:
            int(api_id)
        except Exception:
            hata("🛑 API ID Hatalı ! 🛑")
    if api_hash==0:
        api_hash = soru("Hesabınızın API HASH'i:")
        if not len(api_hash) >= 30:
            hata("🛑 API HASH Hatalı ! 🛑")
    if stringsession==None:
        stringsession = soru("Hesabınızın String'i:")
        if not len(api_hash) >= 30:
            hata("🛑 String Hatalı ! 🛑")

    try:
        bot = TelegramClient(
        StringSession(stringsession),
        api_id=api_id,
        api_hash=api_hash,
        lang_code="tr")
        basarili(api_hash + " için client oluşturuldu !")
    except Exception as e:
        hata(api_hash + f" için client oluşturulamadı ! 🛑 Hata: {str(e)}")

    return bot

async def setdirectory(pprint=True):
    sep = os.sep
    li = os.getcwd().split(sep)
    if pprint:bilgi(li[-1])
    passed("Dizin ayarlanıyor")
    if os.name=="nt":
        os.chdir("c://")
    elif "home" in li: #termux
        while True:
            if not li[-1] == "home": #termux
                os.chdir(os.pardir)
            else:
                break
    else:
        hata("403 Forbidden | Geçersiz işletim sistemi!")
    li = os.getcwd().split(sep)
    if pprint:rprint(li)
    oathh="{}{}m-r".format(os.getcwd(),sep)
    try: os.makedirs(oathh)
    except FileExistsError: pass
    return oathh

def getdirectory(oathh,file):
    oathh="{main}{sep}{file}".format(main=oathh,sep=os.sep,file=file)
    rprint(oathh)
    return oathh
async def setchannel(isp=0,pprint=True,forceadd=""):
    global eklenecek; eklenecek=True
    oathh=await setdirectory(pprint)

    if isp == 0:
                error=False
                with open(getdirectory(oathh,"main.txt"),"w") as f:
                    if forceadd == "":
                        neolsun=soru("🍀 Ana kanal ne olsun? Lütfen id'i yazın!")
                        onayl = onay(f"Ana kanal '{neolsun}' olsun mu ?")
                        try:
                            neolsunn = int(neolsun)
                        except ValueError:
                            noadded("Lütfen bir kanal id yazın!");error=True
                   
                        if neolsun.startswith("-100") and onayl:
                            f.write(neolsun);basarili("✅ İşlem başarıyla tamamlandı!")
                        elif onayl==False:
                            return await setchannel (isp, False, forceadd)
                        else:
                            log("Hatalı kanal id'si!","red");error=True
                    else: f.write(adds+forceadd);basarili("✅ Force ({}) başarıyla tamamlandı!".format(forceadd))
                if error:
                    if os.path.isfile(getdirectory(oathh,"main.txt")): os.remove(getdirectory(oathh,"main.txt"))
                    return await setchannel (isp, False, forceadd)
                eklenecek=False
                return getdirectory(oathh,"main.txt")
    elif isp == 1:
                error=False
                if os.path.isfile(getdirectory(oathh,"channel.txt")):adds="\n"
                else:adds=""
                try:
                    with open(getdirectory(oathh,"channel.txt"),"r") as f:
                        channelsss=f.read().split('\n')
                except FileNotFoundError: channelsss=[]
                with open(getdirectory(oathh,"channel.txt"),"a") as f:
                    if forceadd == "":
                        neolsun=soru("🍀 Eklenecek yan kanal ne olsun? Lütfen id'i yazın!")
                        onayl = onay(f"Yan kanallara '{neolsun}' eklensin mi ?")
                        try:
                            int(neolsun)
                        except ValueError:
                            noadded("Lütfen bir kanal id yazın!");error=True
                        if neolsun in channelsss:noadded("Bu kadar zaten daha önceden eklenmiş!")
                        elif neolsun.startswith("-100") and onayl:
                            f.write(adds+neolsun);basarili("✅ İşlem başarıyla tamamlandı!")
                        elif onayl==False:
                            return await setchannel (isp,False, forceadd)
                        else:
                            log("Hatalı kanal id'si!","red");error=True
                    else: f.write(adds+forceadd);basarili("✅ Force ({}) başarıyla tamamlandı!".format(forceadd))
                if error:
                    if os.path.isfile(getdirectory(oathh,"channel.txt")): os.remove(getdirectory(oathh,"channel.txt"))
                    return await setchannel (isp, False, forceadd)
                eklenecek=False
                return getdirectory(oathh,"channel.txt")

async def getchannel (isp=0,pprint=True):
    oathh=await setdirectory(pprint)
    if isp == 0:
                if os.path.isfile(getdirectory(oathh,"main.txt")):
                    with open(getdirectory(oathh,"main.txt"),"r") as f:
                        file = f.read()
                    if not file.split('\n')[0].startswith("-100"):
                        await setchannel (isp,False); return await getchannel (isp,False)
                    return file.split('\n')[0]
                else:
                    await setchannel (isp,False); return await getchannel (isp,False)
    elif isp == 1:
                if os.path.isfile(getdirectory(oathh,"channel.txt")):
                    with open(getdirectory(oathh,"channel.txt"),"r") as f:
                        file = f.read()
                    if not file.split('\n')[0].startswith("-100"):
                        await setchannel (isp,False); return await getchannel (isp,False)
                    return file.split('\n')
                else:
                    await setchannel (isp,False); return await getchannel (isp,False)
    return None

async def forchannel(bot,channelpath,message):
    bilgi ("Perceived: ")
    onemli(channelpath)
    basarilic=0
    mesj = await bot.get_messages(message.chat_id, ids=message.id)
    bilgi("Kopyalanacak mesaj hazır!")
    for chnl in channelpath:
        if chnl == "":continue 
        if chnl.startswith("-100"):
            bilgi("Şuraya mesaj gönderilmeye çalışılıyor..: {}".format(chnl))
            try:
                chat=await bot.get_entity(int(chnl))
                await bot.send_message(chat.id,mesj)
                log("Mesaj {} kanalına gönderildi!".format(chat.id),"green")
                basarilic+=1
            except PeerIdInvalidError:
                noadded("Kanal ID'si({}) hatalı, lütfen bunu silin!".format (chnl))
            except Exception as e:
                noadded("✖️ Yan kanallardan '{}' mesaj atılmadı! Hata: {}".format(chnl,str(e)))
        else:
            try:
                chat=await bot.get_entity(int(chnl)) #types.PeerChannel(int(chnl))
                await bot.send_message(chat,mesj)
                log("Mesaj {} kanalına gönderildi!".format(chat.id),"green")
                basarilic+=1
            except Exception as e:
                noadded("✖️ Yan kanallardan '{}' mesaj atılmadı! Hata: {}".format(chnl,str(e)))
    return basarilic

mainpath= ""
channelpath=""
async def main ():
    statusz="ads"
    if os.name!="nt": os.system("clear")
    else: os.system("cls")
    while True:
        logo(True)
        if statusz=="ads":ads("Free trial bitiş süresi: 31 gün",.5); statusz=None
        elif statusz:
            passed(statusz);statusz=None
        passed("İşlemler:\n\n🍀 1:Botu başlat!\n🍀 2:Ana Kanal Ayarla veya Değiştir!\n🍀 3:Yan Kanal Ekle!\n🍀 4:Çıkış")
        try:
            islem = soru_("Yapacağınız işlemi seçin [1-4]?")
        except:
            await disconn ()
        if islem=="1":
            global bot, mainpath, channelpath 
            mainpath= await getchannel (0)
            channelpath= await getchannel (1)
            bot = await botagir()
            n()
            log("💨💨 Şimdi botunuz çalışıyor ve yan kanallarda birşey paylaşılmasını bekliyor...","green")
            statusz="Bottan çıkış yapıldı!"
            with console.status("[bold thistle1]⌛ Bot çalışıyor, durdurmak için Ctrl C yapın!") as status:
                try:
                    await bot.run_until_disconnected()
                except KeyboardInterrupt:
                    pass #raise KeyboardInterrupt("Çıkış!")
            await disconn ()
        elif islem=="2":
            statusz="Ana kanal işlemlerinden çıkıldı!"
            await setchannel ()
            onayl = onay("Başka bir işlem yapmak ister misiniz?")
            if onayl:continue
            else:break
        elif islem=="3":
            statusz="Yan kanal işlemlerinden çıkıldı!"
            await setchannel (1)
            onayl = onay("Başka bir işlem yapmak ister misiniz?")
            if onayl:continue
            else: break
        elif islem=="4":
            break
        if islem not in ["1","2","3","4"]:
            statusz= "Hatalı işlem seçimi!"; continue 
    log("Çıkış isteğiniz gerçekleşiyor...","yellow1")
    await disconn()

@clabtetikleyici(bot=bot,incoming=True, pattern="^.start",disable_edited=True)
async def muutf(m):
    await m.reply("Running...⚡")

@clabtetikleyici(bot=bot,incoming=True, pattern="^.maingroup(?: |$)(.*)",disable_edited=True)
async def muutf(m):
    #string = m.pattern_match.group(1)
    await m.reply("🆔: {}".format(mainpath))

@clabtetikleyici(bot=bot,incoming=True, pattern="^.channels(?: |$)(.*)",disable_edited=True)
async def muutf(m):
    await m.respond("📋: {}".format(str(channelpath)))
    text=""
    for i in channelpath:
        text+="🆔: {}\n".format(i)
    await m.respond("{}".format(text))


@clabtetikleyici(bot=bot,incoming=True,groups_only=True,disable_edited=True)
async def muutf(m):
    if str(m.chat_id) in channelpath:
   
        onemli("🔄 Yeni bir post tespit edildi,gönderiliyor...")

        mesj = await bot.get_messages(m.chat_id, ids=m.id)
        bilgi("Kopyalanacak mesaj hazır!")
        try:
            await bot.send_message(mainpath,mesj);onemli("✅ İşlem tamamlandı! Hedef post iletildi!")
        except Exception as e:
            noadded(f"{m.chat_id} kaynağından ana group hedefine iletilememe hatası: {str(e)}")

        #else:
        #await m.reply("✉️: {}".format(str(m)))
     
        
    else:
        bilgi(f"Şuradan bir mesaj algılandım🌀: {m.chat_id}")
eklenecek=False

@clabtetikleyici(bot=bot,incoming=True,groups_only=False,disable_edited=True,trigger_on_fwd=True)
async def muutf(m):
    if m.fwd_from and m.views:
        await m.reply("🆔: <i>Kanal ID:</i> {}".format(m.fwd_from.from_id))


"""
@bot.on(bberc(incoming=True))
async def handler(event):
    await event.reply("b "+ event.text)
"""
async def disconn():
    try:
        await bot.disconnect()
        hata("Bottan çıkış yapıldı!","red")
    except:
        pass

if __name__ == "__main__":
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        n()
        loop.run_until_complete(disconn())
        hata("Güle güle!")






