from selenium.common import TimeoutException, StaleElementReferenceException

import functions
import undetected_chromedriver as uc
import time

### İstenilen araba.

## Zorunlu
arama = "Volkswagen Golf"
## Opsiyonel

yıl_min = "2012"
yıl_max = ""
motor_hacmi = ""
vites = "Otomatik"

### Ayarlar
driver = uc.Chrome()
driver.set_window_size(1600, 900)
driver.get("https://www.sahibinden.com")
zaman = time.sleep

zaman(2)
## Çerezleri Kabul etme
cookie = driver.find_element(by="xpath", value='//*[@id="onetrust-accept-btn-handler"]')
cookie.click()

## Arama kutusu
driver.find_element(by="xpath", value="//*[@id='searchText']").send_keys(arama)
driver.find_element(by="xpath", value="//*[@id='searchSuggestionForm']/button").click()
zaman(2)

## Sayfadaki araba sayısının 20'den 50'ye çıkarılması
sonuc_Arttır = driver.find_element(by="xpath", value='//*[@id="searchResultsSearchForm"]/div[1]/div[*]/div[3]/div[2]/ul/li[2]/a')
sonuc_Arttır.click()
zaman(2)

## Filtreleme başlangıcı
driver.find_element(by="xpath", value='//*[@id="searchCategoryContainer"]/div/div/ul/li[1]/a').click()
zaman(2)

## Yıl filtreleri.
if yıl_min:
    driver.find_element(by="xpath", value='//*[@id="searchResultLeft-a5"]/dl/dd/div/input[1]').send_keys(yıl_min)
if yıl_max:
    driver.find_element(by="xpath", value='//*[@id="searchResultLeft-a5"]/dl/dd/div/input[2]').send_keys(yıl_max)

### Spesifik vites seçimi.
vites = vites.lower()
if vites == "manuel":
    driver.execute_script("window.scrollBy(0, 200);")
    vites_Secim = driver.find_element(by="css selector", value='.js-attribute.facetedCheckbox[title="Manuel"]').click()
elif vites == "otomatik":
    driver.execute_script("window.scrollBy(0, 200);")
    vites_Secim = driver.find_element(by="css selector", value='.js-attribute.facetedCheckbox[title="Otomatik"]').click()
else:
    pass

zaman(1)

### Filtreleme sonucu için butona tıklanması.
filtre_button = (driver.find_element(by="xpath", value='//*[@id="searchResultLeft-a5"]/dl/dd/div/button')
                 .click())
zaman(2)


### Verilerin çekilmesi için while döngüsü.
while True:
    try:
        ## Satırların css veya xpath adresleri.
        marka = driver.find_element(by="xpath", value='//*[@id="search_cats"]/ul/li[3]/div/a')
        model_motor = driver.find_elements(by="css selector", value='.searchResultsTagAttributeValue')
        ilan_basligi = driver.find_elements(by="css selector", value='.searchResultsTitleValue')
        renk_km_yil = driver.find_elements(by="css selector", value='.searchResultsAttributeValue')
        ilan_fiyati = driver.find_elements(by="css selector", value='.searchResultsPriceValue')
        ilan_tarihi = driver.find_elements(by="css selector", value='.searchResultsDateValue')
        ilan_sehir = driver.find_elements(by="css selector", value='.searchResultsLocationValue')
        zaman(2)

        try:
            ## Döngünün sayfa başına ne kadar döneceğinin hesaplanması.
            min_len = min(len(model_motor), len(ilan_basligi), len(ilan_fiyati), len(ilan_tarihi), len(ilan_sehir))

            for i in range(min_len):
                ## Verilerin temizlenmesi ve kaydedilmesi.
                baslik = ilan_basligi[i].text.strip()
                model = model_motor[i * 2].text.strip()
                motor = model_motor[i * 2 + 1].text.strip()
                fiyat = ilan_fiyati[i].text[:-3].strip().replace('.', '')
                tarih = ilan_tarihi[i].text.strip().replace('\n', ' ')
                sehir = ilan_sehir[i].text.strip().replace('\n', ' ')
                yil = renk_km_yil[i * 3].text.strip()
                km = renk_km_yil[i * 3 + 1].text.strip().replace('.', '')
                renk = renk_km_yil[i * 3 + 2].text.strip()

                ## Eğer motor hacmi verisi mevcut ise uyumlu verilerin yoksa tüm verilerin yazdırılması
                if motor_hacmi:
                    if motor_hacmi in motor:
                        database = functions.veri_cek(marka.text , motor, renk, model, yil,  baslik, km, fiyat, tarih, sehir)
                    else:
                        continue
                else:
                    database = functions.veri_cek(marka.text, motor, renk, model, yil, baslik, km, fiyat, tarih, sehir)


            driver.find_element(by="css selector", value='.prevNextBut[title="Sonraki"]').click()

        except StaleElementReferenceException:
            continue

        zaman(1)
    except TimeoutException:
            print("Button element not found.")


### Bittiğinin anlaşılması adına ufak yazı.
print("Bitti")