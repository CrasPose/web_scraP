import time
import re
import pyodbc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException


iller_ve_ilceler = {
    "Adana": ["Seyhan","Yüreğir","Çukurova","Sarıçam","Aladağ","Ceyhan","Feke","İmamoğlu","Karaisalı","Karataş","Kozan","Pozantı","Saimbeyli","Tufanbeyli","Yumurtalık"],
    "Adıyaman": ["Merkez","Besni","Çelikhan","Gerger","Gölbaşı","Kahta","Samsat","Sincik","Tut"],
    "Afyonkarahisar": ["Merkez","Başmakçı","Bayat","Bolvadin","Çay","Çobanlar","Dazkırı","Dinar","Emirdağ","Evciler","Hocalar","İhsaniye","İscehisar","Kızılören","Sandıklı","Sinanpaşa","Sultandağı","Şuhut"],
    "Ağrı": ["Merkez","Diyadin","Doğubayazıt","Eleşkirt","Hamur","Patnos","Taşlıçay","Tutak"],
    "Aksaray": ["Merkez","Ağaçören","Eskil","Gülağaç","Güzelyurt","Ortaköy","Sarıyahşi"],
    "Amasya": ["Merkez","Göynücek","Gümüşhacıköy","Hamamözü","Merzifon","Suluova","Taşova"],
    "Ankara": ["Altındağ","Ayaş","Bala","Beypazarı","Çamlıdere","Çankaya","Çubuk","Elmadağ","Etimesgut","Evren","Gölbaşı","Güdül","Haymana","Kalecik","Kahramankazan","Keçiören","Kızılcahamam","Mamak","Nallıhan","Polatlı","Pursaklar","Sincan","Şereflikoçhisar","Yenimahalle"],
    "Antalya": ["Aksu","Alanya","Demre","Döşemealtı","Elmalı","Finike","Gazipaşa","Gündoğmuş","İbradı","Kaş","Kemer","Kepez","Konyaaltı","Korkuteli","Kumluca","Manavgat","Muratpaşa","Serik"],
    "Ardahan": ["Merkez","Çıldır","Damal","Göle","Hanak","Posof"],
    "Artvin": ["Merkez","Ardanuç","Arhavi","Borçka","Hopa","Murgul","Şavşat","Yusufeli"],
    "Aydın": ["Merkez","Bozdoğan","Buharkent","Çine","Didim","Efeler","Germencik","İncirliova","Karacasu","Karpuzlu","Koçarlı","Köşk","Kuşadası","Kuyucak","Nazilli","Söke","Sultanhisar","Yenipazar"],
    "Balıkesir": ["Altıeylül","Ayvalık","Balya","Bandırma","Bigadiç","Burhaniye","Dursunbey","Edremit","Erdek","Gömeç","Gönen","Havran","İvrindi","Karesi","Kepsut","Manyas","Marmara","Savaştepe","Sındırgı","Susurluk"],
    "Bartın": ["Merkez","Amasra","Kurucaşile","Ulus"],
    "Batman": ["Merkez","Beşiri","Gercüş","Hasankeyf","Kozluk","Sason"],
    "Bayburt": ["Merkez","Aydıntepe","Demirözü"],
    "Bilecik": ["Merkez","Bozüyük","Gölpazarı","İnhisar","Osmaneli","Pazaryeri","Söğüt","Yenipazar"],
    "Bingöl": ["Merkez","Adaklı","Genç","Karlıova","Kığı","Solhan","Yayladere","Yedisu"],
    "Bitlis": ["Merkez","Adilcevaz","Ahlat","Güroymak","Hizan","Mutki","Tatvan"],
    "Bolu": ["Merkez","Dörtdivan","Gerede","Göynük","Kıbrıscık","Mengen","Mudurnu","Seben","Yeniçağa"],
    "Burdur": ["Merkez","Ağlasun","Altınyayla","Bucak","Çavdır","Çeltikçi","Gölhisar","Karamanlı","Kemer","Tefenni","Yeşilova"],
    "Bursa": ["Büyükorhan","Gemlik","Gürsu","Harmancık","İnegöl","İznik","Karacabey","Keles","Kestel","Mudanya","Mustafakemalpaşa","Nilüfer","Orhaneli","Orhangazi","Osmangazi","Yenişehir","Yıldırım"],
    "Çanakkale": ["Merkez","Ayvacık","Bayramiç","Biga","Bozcaada","Çan","Eceabat","Ezine","Gelibolu","Gökçeada","Lapseki","Yenice"],
    "Çankırı": ["Merkez","Çerkeş","Eldivan","Ilgaz","Kızılırmak","Kurşunlu","Orta","Şabanözü","Yapraklı"],
    "Çorum": ["Merkez","Alaca","Bayat","Boğazkale","Dodurga","İskilip","Kargı","Laçin","Mecitözü","Oğuzlar","Ortaca","Sungurlu","Uğurludağ"],
    "Denizli": ["Merkez","Acıpayam","Babadağ","Baklan","Bekilli","Beyağaç","Bozkurt","Buldan","Çal","Çameli","Çardak","Çivril","Güney","Honaz","Kale","Sarayköy","Serinhisar","Tavas"],
    "Diyarbakır": ["Merkez","Bağlar","Bismil","Dicle","Ergani","Hani","Hazro","Kayapınar","Kocaköy","Kulp","Lice","Silvan","Sur","Çermik","Çınar","Çüngüş"],
    "Düzce": ["Merkez","Akçakoca","Çilimli","Cumayeri","Gölyaka","Gümüşova","Kaynaşlı","Yığılca"],
    "Edirne": ["Merkez","Enez","Havsa","İpsala","Keşan","Lalapaşa","Meriç","Süloğlu","Uzunköprü"],
    "Elazığ": ["Merkez","Ağın","Alacakaya","Arıcak","Baskil","Karakoçan","Keban","Maden","Palu","Sivrice"],
    "Erzincan": ["Merkez","Çayırlı","İliç","Kemah","Kemaliye","Refahiye","Tercan","Üzümlü"],
    "Erzurum": ["Merkez","Aşkale","Aziziye","Çat","Hınıs","Horasan","İspir","Karayazı","Narman","Olur","Pasinler","Pazaryolu","Şenkaya","Tekman","Tortum","Uzundere"],
    "Eskişehir": ["Merkez","Alpu","Beylikova","Çifteler","Günyüzü","Han","İnönü","Mahmudiye","Mihalgazi","Mihalıççık","Sarıcakaya","Seyitgazi","Sivrihisar"],
    "Gaziantep": ["Merkez","Araban","İslahiye","Karkamış","Nizip","Oğuzeli","Yavuzeli"],
    "Giresun": ["Merkez","Alucra","Bulancak","Çamoluk","Çanakçı","Dereli","Doğankent","Espiye","Eynesil","Güce","Keşap","Piraziz","Şebinkarahisar","Tirebolu","Yağlıdere"],
    "Gümüşhane": ["Merkez","Kelkit","Köse","Kürtün","Şiran","Torul"],
    "Hakkari": ["Merkez","Çukurca","Şemdinli","Yüksekova"],
    "Hatay": ["Merkez","Antakya","Arsuz","Defne","Dörtyol","Erzin","Hassa","İskenderun","Kırıkhan","Payas","Reyhanlı","Samandağ","Yayladağı"],
    "Iğdır": ["Merkez","Aralık","Karakoyunlu","Tuzluca"],
    "Isparta": ["Merkez","Aksu","Atabey","Eğirdir","Gelendost","Gönen","Keçiborlu","Senirkent","Sütçüler","Şarkikaraağaç","Uluborlu","Yalvaç","Yenişarbademli"],
    "İstanbul": ["Adalar","Arnavutköy","Ataşehir","Avcılar","Bağcılar","Bahçelievler","Bakırköy","Başakşehir","Bayrampaşa","Beşiktaş","Beykoz","Beylikdüzü","Beyoğlu","Büyükçekmece","Çatalca","Çekmeköy","Esenler","Esenyurt","Eyüpsultan","Fatih","Gaziosmanpaşa","Güngören","Kadıköy","Kağıthane","Kartal","Küçükçekmece","Maltepe","Pendik","Sancaktepe","Sarıyer","Silivri","Sultanbeyli","Sultangazi","Şile","Şişli","Tuzla","Ümraniye","Üsküdar","Zeytinburnu"],
    "İzmir": ["Merkez","Aliağa","Balçova","Bayındır","Bayraklı","Bergama","Beydağ","Bornova","Buca","Çeşme","Çiğli","Dikili","Foça","Gaziemir","Güzelbahçe","Karabağlar","Karşıyaka","Kemalpaşa","Kınık","Kiraz","Konak","Menderes","Menemen","Narlıdere","Ödemiş","Seferihisar","Selçuk","Tire","Torbalı","Urla"],
    "Kahramanmaraş": ["Merkez","Afşin","Andırın","Dulkadiroğlu","Ekinözü","Elbistan","Göksun","Nurhak","Onikişubat","Pazarcık","Türkoğlu"],
    "Karabük": ["Merkez","Eflani","Eskipazar","Ovacık","Safranbolu","Yenice"],
    "Karaman": ["Merkez","Ayrancı","Başyayla","Ermenek","Kazımkarabekir","Sarıveliler"],
    "Kars": ["Merkez","Akyaka","Arpaçay","Digor","Kağızman","Sarıkamış","Selim","Susuz"],
    "Kastamonu": ["Merkez","Abana","Araç","Azdavay","Bozkurt","Cide","Çatalzeytin","Daday","Devrekani","İnebolu","İhsangazi","Küre","Taşköprü","Tosya","Pınarbaşı","Şenpazar","Doğanyurt"],
    "Kayseri": ["Merkez","Akkışla","Bünyan","Develi","Felahiye","İncesu","Kocasinan","Melikgazi","Özvatan","Pınarbaşı","Sarıoğlan","Sarız","Talas","Tomarza","Yahyalı","Yeşilhisar"],
    "Kırıkkale": ["Merkez","Bahşılı","Balışeyh","Delice","Karakeçili","Keskin","Sulakyurt","Yahşihan"],
    "Kırklareli": ["Merkez","Babaeski","Demirköy","Kofçaz","Lüleburgaz","Pehlivanköy","Pınarhisar","Vize"],
    "Kırşehir": ["Merkez","Akpınar","Akçakent","Boztepe","Çiçekdağı","Kaman","Mucur"],
    "Kocaeli": ["Merkez","Başiskele","Çayırova","Derince","Dilovası","Gebze","Gölcük","Kandıra","Karamürsel","Kartepe","Körfez"],
    "Konya": ["Merkez","Akşehir","Altınekin","Beyşehir","Bozkır","Cihanbeyli","Çeltik","Derebucak","Doğanhisar","Emirgazi","Ereğli","Güneysınır","Hadim","Halkapınar","Hüyük","Ilgın","Kadınhanı","Karapınar","Karatay","Kulu","Meram","Sarayönü","Selçuklu","Seydişehir","Taşkent","Tuzlukçu","Yalıhüyük","Yunak"],
    "Kütahya": ["Merkez","Altıntaş","Aslanapa","Çavdarhisar","Domaniç","Dumlupınar","Emet","Gediz","Hisarcık","Pazarlar","Şaphane","Simav","Tavşanlı"],
    "Malatya": ["Merkez","Akçadağ","Arapgir","Arguvan","Battalgazi","Darende","Doğanşehir","Doğanyol","Hekimhan","Kuluncak","Pütürge","Yeşilyurt","Yazıhan"],
    "Manisa": ["Merkez","Ahmetli","Akhisar","Alaşehir","Demirci","Gölmarmara","Gördes","Kırkağaç","Köprübaşı","Salihli","Sarıgöl","Saruhanlı","Selendi","Soma","Şehzadeler","Turgutlu","Yunusemre"],
    "Mardin": ["Merkez","Dargeçit","Derik","Kızıltepe","Mazıdağı","Midyat","Nusaybin","Ömerli","Savur"],
    "Mersin": ["Merkez","Akdeniz","Anamur","Aydıncık","Bozyazı","Çamlıyayla","Erdemli","Gülnar","Mezitli","Mut","Silifke","Tarsus","Toroslar","Yenişehir"],
    "Muğla": ["Merkez","Bodrum","Dalaman","Datça","Fethiye","Kavaklıdere","Marmaris","Menteşe","Milas","Menteşe","Ortaca","Ula","Yatağan"],
    "Muş": ["Merkez","Bulanık","Hasköy","Korkut","Malazgirt","Varto"],
    "Nevşehir": ["Merkez","Avanos","Derinkuyu","Gülşehir","Hacıbektaş","Kozaklı","Ürgüp"],
    "Niğde": ["Merkez","Altunhisar","Bor","Çamardı","Ulukışla"],
    "Ordu": ["Merkez","Akkuş","Altınordu","Aybastı","Çamaş","Çatalpınar","Fatsa","Gölköy","Gülyalı","Gürgentepe","İkizce","Kabadüz","Kabataş","Korgan","Kumru","Mesudiye","Perşembe","Ulubey","Ünye"],
    "Osmaniye": ["Merkez","Bahçe","Düziçi","Kadirli","Sumbas","Toprakkale"],
    "Rize": ["Merkez","Ardeşen","Çamlıhemşin","Çayeli","Fındıklı","Hemşin","İkizdere","Kalkandere","Pazar"],
    "Sakarya": ["Merkez","Adapazarı","Akyazı","Arifiye","Erenler","Ferizli","Geyve","Hendek","Karapürçek","Karasu","Kaynarca","Kocaali","Pamukova","Sapanca","Serdivan","Söğütlü","Taraklı"],
    "Samsun": ["Merkez","Alaçam","Asarcık","Atakum","Bafra","Canik","Çarşamba","Havza","Kavak","Ladik","Ondokuzmayıs","Salıpazarı","Tekkeköy","Terme","Vezirköprü","Yakakent"],
    "Siirt": ["Merkez","Baykan","Eruh","Kurtalan","Pervari","Şirvan","Tillo"],
    "Sinop": ["Merkez","Ayancık","Boyabat","Dikmen","Durağan","Erfelek","Gerze","Saraydüzü","Türkeli"],
    "Sivas": ["Merkez","Akıncılar","Altınyayla","Divriği","Doğanşar","Gölova","Gürün","Hafik","İmranlı","Kangal","Koyulhisar","Suşehri","Şarkışla","Ulaş","Yıldızeli","Zara"],
    "Şanlıurfa": ["Merkez","Akçakale","Birecik","Bozova","Ceylanpınar","Eyyübiye","Halfeti","Haliliye","Harran","Hilvan","Karaköprü","Siverek","Suruç","Viranşehir"],
    "Şırnak": ["Merkez","Beytüşşebap","Cizre","Güçlükonak","İdil","Silopi","Uludere"],
    "Tekirdağ": ["Merkez","Çerkezköy","Çorlu","Hayrabolu","Malkara","Marmaraereğlisi","Muratlı","Saray","Süleymanpaşa","Şarköy"],
    "Tokat": ["Merkez","Almus","Artova","Başçiftlik","Erbaa","Niksar","Pazar","Reşadiye","Sulusaray","Turhal","Yeşilyurt","Zile"],
    "Trabzon": ["Merkez","Akçaabat","Araklı","Arsin","Beşikdüzü","Çarşıbaşı","Çaykara","Dernekpazarı","Düzköy","Hayrat","Köprübaşı","Maçka","Of","Ortahisar","Sürmene","Şalpazarı","Tonya","Vakfıkebir","Yomra"],
    "Tunceli": ["Merkez","Çemişgezek","Hozat","Mazgirt","Nazımiye","Ovacık","Pertek","Pülümür"],
    "Uşak": ["Merkez","Banaz","Eşme","Karahallı","Sivaslı","Ulubey"],
    "Van": ["Merkez","Bahçesaray","Başkale","Çatak","Erciş","Gevaş","Gürpınar","İpekyolu","Muradiye","Özalp","Saray","Tuşba"],
    "Yalova": ["Merkez","Altınova","Armutlu","Çınarcık","Çiftlikköy","Termal"],
    "Yozgat": ["Merkez","Akdağmadeni","Aydıncık","Boğazlıyan","Çayıralan","Çekerek","Kadışehri","Saraykent","Sorgun","Şefaatli","Yenifakılı","Yerköy"],
    "Zonguldak": ["Merkez","Alaplı","Çaycuma","Devrek","Ereğli","Gökçebey"]
}

# ================== SQL Server Bağlantısı ==================
conn = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=DESKTOP-OBGL57I\\SQLEXPRESS;"  # kendi server adını yaz
    "Database=web_scrap;"
    "Trusted_Connection=yes;"
)
cursor = conn.cursor()

# ================== Selenium Ayarları ==================
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# ================== Duplicate Kontrol ==================
kaydedilenler = set()

def temizle_text(txt):
    return re.sub(r'\s+', ' ', txt.strip()) if txt else None

def kaydet_veri(isim, adres, phone, il, ilce, kaynak):
    key = (isim, adres, phone, il, ilce)
    if key in kaydedilenler or not isim:
        return
    kaydedilenler.add(key)
    cursor.execute(
        "INSERT INTO Petshop (City, District, Name, Address, Phone, Source) VALUES (?, ?, ?, ?, ?, ?)",
        (il, ilce, isim, adres, phone, kaynak)
    )
    conn.commit()
    print(f"[+] {il} / {ilce} → {isim} eklendi. (Tel: {phone})")

# ================== Google Maps Scraper ==================
def scrape_google_maps(il, ilce):
    arama_terimi = f"{ilce} {il} petshop"
    print(f"\n=== {il.upper()} - {ilce.upper()} ===")
    print(f"[Google Maps] {arama_terimi} aranıyor...")

    driver.get("https://www.google.com/maps/")
    time.sleep(3)

    try:
        arama_kutusu = driver.find_element(By.ID, "searchboxinput")
        arama_kutusu.clear()
        arama_kutusu.send_keys(arama_terimi)
        arama_kutusu.send_keys(Keys.RETURN)
        time.sleep(7)
    except NoSuchElementException:
        print("Google arama kutusu bulunamadı.")
        return

    kayit_sayisi_once = 0
    scroll_deneme = 0

    while True:
        kartlar = driver.find_elements(By.XPATH, '//div[contains(@class, "Nv2PK")]')
        if not kartlar:
            break

        for kart in kartlar:
            try:
                # İsim ve adres
                isim = kart.find_element(By.XPATH, './/a[contains(@class, "hfpxzc")]').get_attribute('aria-label')
                adres_el = kart.find_element(By.XPATH, './/div[contains(@class,"W4Efsd")]/span[2]')
                adres = temizle_text(adres_el.text) if adres_el else None

                # Kartı tıklayıp detay panelini aç
                try:
                    kart.click()
                    time.sleep(5)  # panelin yüklenmesini bekle
                except:
                    pass

                # Telefon numarasını detay panelden al
                try:
                    phone_el = driver.find_element(By.XPATH, '//button[contains(@aria-label,"Telefon:")]//div[contains(@class,"Io6YTe")]')
                    phone = phone_el.text.strip()
                except Exception:
                    phone = None

                kaydet_veri(isim, adres, phone, il, ilce, "Google Maps")

            except Exception as e:
                print(f"[!] Bir kart işlenemedi: {e}")
                continue

        # Scroll
        try:
            scrollable_div = driver.find_element(By.XPATH, '//div[@role="feed"]')
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
            time.sleep(3)
        except:
            break

        # Yeni kayıt kontrolü
        if len(kaydedilenler) == kayit_sayisi_once:
            scroll_deneme += 1
            if scroll_deneme >= 3:
                break
        else:
            kayit_sayisi_once = len(kaydedilenler)
            scroll_deneme = 0

# ================== Ana Döngü ==================
try:
    for il, ilceler in iller_ve_ilceler.items():
        print(f"\n\n******** {il.upper()} İLİNİN PETSHOPLARI ********")
        for ilce in ilceler:
            print(f"\n--- {il.upper()} / {ilce.upper()} başlıyor ---")
            scrape_google_maps(il, ilce)
            print(f"--- {il.upper()} / {ilce.upper()} bitti ---")

    print("\n✅ Tüm il ve ilçeler için scraping tamamlandı.")

finally:
    driver.quit()
    conn.close()