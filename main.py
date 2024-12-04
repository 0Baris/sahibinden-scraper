from selenium.common import TimeoutException, StaleElementReferenceException, NoSuchElementException
import functions
import undetected_chromedriver as uc
import time

def sahibinden_arama(arama, yıl_min=None, yıl_max=None, motor_hacmi=None, vites=None):
    """
    Sahibinden'de arama yaparak filtrelere göre ilanları çeker.

    Args:
        arama (str): Arama yapılacak kelime.
        yıl_min (str, optional): Minimum yıl filtresi.
        yıl_max (str, optional): Maksimum yıl filtresi.
        motor_hacmi (str, optional): Motor hacmi filtresi.
        vites (str, optional): Vites tipi ("Manuel" veya "Otomatik").
    """

    ### Ayarlar
    driver = uc.Chrome()
    driver.set_window_size(1600, 900)

    ## Başlangıç
    driver.get("https://www.sahibinden.com")
    zaman = time.sleep
    zaman(2)

    ## Çerezleri kabul etme
    cookie = driver.find_element(by="xpath", value='//*[@id="onetrust-accept-btn-handler"]')
    cookie.click()

    ## Arama kutusu
    driver.find_element(by="xpath", value="//*[@id='searchText']").send_keys(arama)
    driver.find_element(by="xpath", value="//*[@id='searchSuggestionForm']/button").click()
    zaman(2)

    ## Sayfadaki araba sayısının 20'den 50'ye çıkarılması
    sonuc_arttir = driver.find_element(by="xpath", value='//*[@id="searchResultsSearchForm"]/div[1]/div[*]/div[3]/div[2]/ul/li[2]/a')
    sonuc_arttir.click()
    zaman(2)

    ## Filtreleme başlangıcı
    driver.find_element(by="xpath", value='//*[@id="searchCategoryContainer"]/div/div/ul/li[1]/a').click()
    zaman(2)

    ## Yıl filtreleri
    if yıl_min:
        driver.find_element(by="xpath", value='//*[@id="searchResultLeft-a5"]/dl/dd/div/input[1]').send_keys(yıl_min)
    if yıl_max:
        driver.find_element(by="xpath", value='//*[@id="searchResultLeft-a5"]/dl/dd/div/input[2]').send_keys(yıl_max)

    ### Spesifik vites seçimi
    if vites:
        vites = vites.lower()
        driver.execute_script("window.scrollBy(0, 200);")
        if vites == "manuel":
            driver.find_element(by="css selector", value='.js-attribute.facetedCheckbox[title="Manuel"]').click()
        elif vites == "otomatik":
            driver.find_element(by="css selector", value='.js-attribute.facetedCheckbox[title="Otomatik"]').click()

    zaman(1)

    ### Filtreleme sonucu için butona tıklanması
    filtre_button = driver.find_element(by="xpath", value='//*[@id="searchResultLeft-a5"]/dl/dd/div/button')
    filtre_button.click()
    zaman(2)

    ### Verilerin çekilmesi için while döngüsü
    while True:
        try:
            marka = driver.find_element(by="xpath", value='//*[@id="search_cats"]/ul/li[3]/div/a')
            model_motor = driver.find_elements(by="css selector", value='.searchResultsTagAttributeValue')
            ilan_basligi = driver.find_elements(by="css selector", value='.searchResultsTitleValue')
            renk_km_yil = driver.find_elements(by="css selector", value='.searchResultsAttributeValue')
            ilan_fiyati = driver.find_elements(by="css selector", value='.searchResultsPriceValue')
            ilan_tarihi = driver.find_elements(by="css selector", value='.searchResultsDateValue')
            ilan_sehir = driver.find_elements(by="css selector", value='.searchResultsLocationValue')
            zaman(2)

            ## Döngünün sayfa başına ne kadar döneceğinin hesaplanması
            min_len = min(len(model_motor), len(ilan_basligi), len(ilan_fiyati), len(ilan_tarihi), len(ilan_sehir))

            for i in range(min_len):
                ## Verilerin temizlenmesi ve kaydedilmesi
                baslik = ilan_basligi[i].text.strip()
                model = model_motor[i * 2].text.strip() if len(model_motor) > i * 2 else "N/A"
                motor = model_motor[i * 2 + 1].text.strip() if len(model_motor) > i * 2 + 1 else "N/A"
                fiyat = ilan_fiyati[i].text[:-3].strip().replace('.', '')
                tarih = ilan_tarihi[i].text.strip().replace('\n', ' ')
                sehir = ilan_sehir[i].text.strip().replace('\n', ' ')
                yil = renk_km_yil[i * 3].text.strip() if len(renk_km_yil) > i * 3 else "N/A"
                km = renk_km_yil[i * 3 + 1].text.strip().replace('.', '') if len(renk_km_yil) > i * 3 + 1 else "N/A"
                renk = renk_km_yil[i * 3 + 2].text.strip() if len(renk_km_yil) > i * 3 + 2 else "N/A"

                ## Eğer motor hacmi verisi mevcut ise uyumlu verilerin yoksa tüm verilerin yazdırılması
                if motor_hacmi:
                    if motor_hacmi in motor:
                        functions.veri_cek(marka.text, motor, renk, model, yil, baslik, km, fiyat, tarih, sehir)
                    else:
                        continue
                else:
                    functions.veri_cek(marka.text, motor, renk, model, yil, baslik, km, fiyat, tarih, sehir)

            driver.find_element(by="css selector", value='.prevNextBut[title="Sonraki"]').click()

        except StaleElementReferenceException:
            continue

        except TimeoutException:
            print("Sonraki buton bulunamadı, işlem tamamlandı.")
            break

        except NoSuchElementException:
            print("Son sayfaya ulaşıldı.")
            break

        zaman(1)

    print("Bitti")

### arama (string): Arama yapılacak kelime.
### yıl_min (string, opsiyonel): Minimum yıl filtresi.
### yıl_max (string, opsiyonel): Maksimum yıl filtresi.
### motor_hacmi (string, opsiyonel): Motor hacmi filtresi.
### vites (string, opsiyonel): Vites tipi ("Manuel" veya "Otomatik").

## sahibinden_arama(arama, yıl_min, yıl_max, motor_hacmi, vites)

# Örnek kullanım
sahibinden_arama(
    arama="Volkswagen Golf",
    yıl_min="2016",
    yıl_max="2016",
    vites="Otomatik"
)
