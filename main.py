from selenium.common import TimeoutException

import functions
import undetected_chromedriver as uc
import time

### İstenilen araba.
araba = "Renault Clio"
yıl_min = 2016
yıl_max = 2016

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
        ilan_model = driver.find_elements(by="xpath", value='//*[@id="searchResultsTable"]/tbody/tr[*]/td[3]')
        ilan_basligi = driver.find_elements(by="xpath", value='//*[@id="searchResultsTable"]/tbody/tr[*]/td[4]')
        ilan_kilometre = driver.find_elements(by="xpath", value='//*[@id="searchResultsTable"]/tbody/tr[*]/td[6]')
        ilan_fiyati = driver.find_elements(by="xpath", value='//*[@id="searchResultsTable"]/tbody/tr[*]/td[8]')
        ilan_tarihi = driver.find_elements(by="xpath", value='//*[@id="searchResultsTable"]/tbody/tr[*]/td[9]')
        ilan_sehir = driver.find_elements(by="xpath", value='//*[@id="searchResultsTable"]/tbody/tr[*]/td[10]')

        database = functions.veri_cek(ilan_model, ilan_basligi, ilan_kilometre, ilan_fiyati, ilan_tarihi, ilan_sehir)

        time.sleep(2)
        driver.find_element(by="css selector", value='.prevNextBut[title="Sonraki"]').click()
    except TimeoutException:
            print("Button element not found.")


### Bittiğinin anlaşılması adına ufak yazı.
print("Bitti")