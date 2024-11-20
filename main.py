from selenium.common import TimeoutException, StaleElementReferenceException

import functions
import undetected_chromedriver as uc
import time

### İstenilen araba.
araba = "Renault Clio"
yıl_min = 2016
yıl_max = 2016
motor_hacmi = "1.5"

driver = uc.Chrome()
driver.get("https://www.sahibinden.com")


### Arama kutusuna yazıların gönderilmesi.
driver.find_element(by="xpath", value="//*[@id='searchText']").send_keys(araba)
time.sleep(5)

### Arama kutusuna tıklanma.
search_bar = (driver.find_element(by="xpath", value="//*[@id='searchSuggestionForm']/button")
              .click())
time.sleep(3)

### Tarayıcı çerezlerini kabul etme.
cookie = (driver.find_element(by="xpath", value="//*[@id='onetrust-accept-btn-handler']")
          .click())
time.sleep(3)

### Tarayıcı çerezlerini kabul etme.
otomobil_clicker = (driver.find_element(by="xpath", value='//*[@id="searchCategoryContainer"]/div/div/ul/li[1]/a')
                    .click())
time.sleep(3)

## Yıl Ayarlama
min_val = (driver.find_element(by="xpath", value='//*[@id="searchResultLeft-a5"]/dl/dd/div/input[1]')
           .send_keys(yıl_min))
max_val = (driver.find_element(by="xpath", value='//*[@id="searchResultLeft-a5"]/dl/dd/div/input[2]')
           .send_keys(yıl_max))

### FİLTRELEME SONU!!!
filtre_button = (driver.find_element(by="xpath", value='//*[@id="searchResultLeft-a5"]/dl/dd/div/button')
                 .click())

time.sleep(5)

### Sayfayı 20 sonuçtan 50 sonuca çıkartma.
sonuc_Arttır = (
    driver.find_element(by="xpath", value='//*[@id="searchResultsSearchForm"]/div[1]/div[*]/div[3]/div[2]/ul/li[2]/a')
    .click())
time.sleep(3)


### Sırasıyla her bir satırın verileri.
while True:
    try:
        ilan_model = driver.find_elements(by="css selector", value='.searchResultsTagAttributeValue')
        ilan_basligi = driver.find_elements(by="css selector", value='.searchResultsTitleValue')
        renk_km_yil = driver.find_elements(by="css selector", value='.searchResultsAttributeValue')
        ilan_fiyati = driver.find_elements(by="css selector", value='.searchResultsPriceValue')
        ilan_tarihi = driver.find_elements(by="css selector", value='.searchResultsDateValue')
        ilan_sehir = driver.find_elements(by="css selector", value='.searchResultsLocationValue')

        time.sleep(2)

        try:
            min_len = min(len(ilan_model), len(ilan_basligi), len(ilan_fiyati), len(ilan_tarihi), len(ilan_sehir))

            for i in range(min_len):
                baslik = ilan_basligi[i].text.strip()
                model = ilan_model[i].text.strip()
                fiyat = ilan_fiyati[i].text[:-3].strip().replace('.', '')
                tarih = ilan_tarihi[i].text.strip().replace('\n', ' ')
                sehir = ilan_sehir[i].text.strip().replace('\n', ' ')
                yil = renk_km_yil[i * 3].text.strip()
                km = renk_km_yil[i * 3 + 1].text.strip().replace('.', '')
                renk = renk_km_yil[i * 3 + 2].text.strip()

                if motor_hacmi in model:

                    database = functions.veri_cek(model, baslik, km, fiyat, tarih, sehir)
                else:
                    continue

            driver.find_element(by="css selector", value='.prevNextBut[title="Sonraki"]').click()

        except StaleElementReferenceException:
            continue

        time.sleep(1)
    except TimeoutException:
            print("Button element not found.")


### Bittiğinin anlaşılması adına ufak yazı.
print("Bitti")