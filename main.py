import time
import undetected_chromedriver as uc
import pandas as pd
import sqlite3

connect = sqlite3.connect('sahibinden.db')
driver = uc.Chrome()
driver.get("https://www.sahibinden.com")

### İstenilen araba.
araba = "Skoda Superb"
yıl_min = 2016
yıl_max = 2022

### Arama kutusuna yazıların gönderilmesi.
(driver.find_element(by="xpath", value="//*[@id='searchText']")
 .send_keys(araba))
time.sleep(5)

### Arama kutusuna tıklanma.
search_bar = (driver.find_element(by="xpath",value="//*[@id='searchSuggestionForm']/button")
              .click())
time.sleep(3)

### Tarayıcı çerezlerini kabul etme.
cookie = (driver.find_element(by="xpath",value="//*[@id='onetrust-accept-btn-handler']")
          .click())
time.sleep(3)

### Tarayıcı çerezlerini kabul etme.
otomobil_clicker = (driver.find_element(by="xpath",value='//*[@id="searchCategoryContainer"]/div/div/ul/li[1]/a')
                    .click())
time.sleep(3)

###### FİLTRELEME AŞAMASI ######

## Yıl Ayarlama
min_val = (driver.find_element(by="xpath", value='//*[@id="searchResultLeft-a5"]/dl/dd/div/input[1]')
           .send_keys(yıl_min))
max_val = (driver.find_element(by="xpath", value='//*[@id="searchResultLeft-a5"]/dl/dd/div/input[2]')
           .send_keys(yıl_max))

### FİLTRELEME SONU!!!
filtre_button = (driver.find_element(by="xpath",value='//*[@id="searchResultLeft-a5"]/dl/dd/div/button')
                 .click())

time.sleep(5)


### Sayfa 20 sonuçtan 50 sonuca çıkartma.
sonuc_Arttır = (driver.find_element(by="xpath", value='//*[@id="searchResultsSearchForm"]/div[1]/div[*]/div[3]/div[2]/ul/li[2]/a')
                .click())
time.sleep(3)

### Sırasıyla her bir satırın verileri.
ilan_model = driver.find_elements(by="xpath", value='//*[@id="searchResultsTable"]/tbody/tr[*]/td[4]')
ilan_basligi = driver.find_elements(by="xpath", value='//*[@id="searchResultsTable"]/tbody/tr[*]/td[5]')
ilan_kilometre = driver.find_elements(by="xpath", value='//*[@id="searchResultsTable"]/tbody/tr[*]/td[7]')
ilan_fiyati = driver.find_elements(by="xpath", value='//*[@id="searchResultsTable"]/tbody/tr[*]/td[8]')
ilan_tarihi = driver.find_elements(by="xpath", value='//*[@id="searchResultsTable"]/tbody/tr[*]/td[9]')
ilan_sehir = driver.find_elements(by="xpath", value='//*[@id="searchResultsTable"]/tbody/tr[*]/td[10]')

### Başlangıç listeleri
model_list = []
baslik_list = []
kilometre_list = []
fiyat_list = []
adres_list = []
tarih_list = []

### Listelere tek tek contentleri ekleme
for model in ilan_model:
    model_list.append(model.text)
for baslik in ilan_basligi:
    baslik_list.append(baslik.text)
for kilometre in ilan_kilometre:
    kilometre_list.append(kilometre.text)
for fiyat in ilan_fiyati:
    fiyat_list.append(fiyat.text)
for adres in ilan_sehir:
    adres_list.append(adres.text)
for tarih in ilan_tarihi:
    tarih_list.append(tarih.text)

### Database oluşturma aşaması.
database = pd.DataFrame((zip(baslik_list, model_list, kilometre_list, fiyat_list, adres_list, tarih_list)),
                        columns=['İlan Başlığı','Model','Kilometre', 'Fiyat', 'Adres', 'Tarih'])

### Database filtreleme işlemleri.

database.to_sql('sahibinden', connect, if_exists='replace', index=False)
database.to_csv('sahibinden.csv', index=False)

database = database.dropna(how="any")

database['Kilometre'] = database['Kilometre'].astype(float)

### Database mevcut olan 'TL' değerenin değiştirilmesi.
database['Fiyat'] = database['Fiyat'].str.replace('TL', '')
database['Fiyat'] = database['Fiyat'].str.replace('.', '').str.strip()
database['Fiyat'] = database['Fiyat'].astype(float)

### Database'de mevcut olan Adresteki karakterleri temizleme.
database['Adres'] = database['Adres'].str.replace('\n', ' ')

### Database'de mevcut olan Tarihteki karakterleri temizleme.
database['Tarih'] = database['Tarih'].str.replace('\n', ' ')

database.to_sql('sahibinden', connect, if_exists='replace', index=False)
database.to_csv('sahibinden.csv', index=False)

### Bittiğinin anlaşılması adına ufak yazı.
print("Bitti")