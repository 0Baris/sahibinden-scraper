import asyncio
import logging
import utils.database as database
import nodriver as uc
from bs4 import BeautifulSoup
import time 
# Basit bir şekilde anlık logları takip etmeyi sağlar.
logging.basicConfig(level=30)

async def main(arama, yıl_min=None, yıl_max=None, motor_hacmi=None, vites=None):
    """
    Tüm değerler string olarak kabul edilir, örnek kullanım sayfanın en altında mevcuttur herhangi bir hata ile karşılaşırsanız issue oluşturabilirsiniz.

    Args:
        arama: Aramak istediğiniz araç. (Renault Clio?)
        yıl_min: Minimum araç yılı (2016)
        yıl_max: Maksimum araç yılı (2016)
        motor_hacmi: Motor hacmi filtresi (1.5)
        vites: Vites tipi filtresi (Manuel)
    """

    driver = await uc.start()
    # sahibinden.com'u açar.
    tab = await driver.get('https://www.sahibinden.com')
    time.sleep(3)

    # Cookileri kabul etme.
    accept_cookies = await tab.find('Tüm Çerezleri Kabul Et', best_match=True)
    if accept_cookies:
        await accept_cookies.click()
    time.sleep(3)

    ## Arama kısmına arama verisini gönderir.
    search_box = await tab.select('#searchText')
    await search_box.send_keys(arama)
    await tab.sleep(5)
    time.sleep(2)
    
    ## Arama butonuna tıklar.
    search_button = await tab.select('button[type="submit"][value="Ara"]')
    await search_button.click()
    await tab.sleep(5)
    time.sleep(2)

    ## Arama kısmında ilk çıkan öneriye tıklanır.
    first_suggestion = await tab.select('li.first-child.ui-menu-item a')
    await first_suggestion.click()
    await tab.sleep(5)

    click_category = await tab.select('#searchCategoryContainer div div ul li:first-child a')
    await click_category.click()
    await tab.sleep(5)


    ## Sonuçları 50'ye çıkarır.
    results_dropdown = await tab.select('a.paging-size.Limit50Passive[title="50"]')
    await results_dropdown.click()
    await tab.sleep(2)

    # Filtre mevcutsa uygulanır.
    if any([yıl_min, yıl_max, motor_hacmi, vites]):
        # Yıl filtresi
        if yıl_min:
            year_min_input = await tab.select('input[name="a5_min"]')
            await year_min_input.send_keys(yıl_min)
            await tab.sleep(1)
        if yıl_max:
            year_max_input = await tab.select('input[name="a5_max"]')
            await year_max_input.send_keys(yıl_max)
            await tab.sleep(1)

        # Motor hacmi filtresi
        if motor_hacmi:
            # motor_hacmi ör: "1.5" veya "1301 - 1600 cm3"
            motor_hacmi = motor_hacmi.replace(" ", "")
            if motor_hacmi in ["1.3", "1300", "1300cm3", "1300cm3'ekadar"]:
                motor_checkbox = await tab.select('a[data-value="51977"].js-attribute.facetedCheckbox')
            elif motor_hacmi in ["1.5", "1.6", "1301-1600", "1301-1600cm3"]:
                motor_checkbox = await tab.select('a[data-value="1118042"].js-attribute.facetedCheckbox')
            elif motor_hacmi in ["1.8", "1601-1800", "1601-1800cm3"]:
                motor_checkbox = await tab.select('a[data-value="51979"].js-attribute.facetedCheckbox')
            elif motor_hacmi in ["2.0", "1801-2000", "1801-2000cm3"]:
                motor_checkbox = await tab.select('a[data-value="51980"].js-attribute.facetedCheckbox')
            else:
                motor_checkbox = None
            if motor_checkbox:
                await motor_checkbox.click()
                await tab.sleep(1)

        # Vites filtresi
        if vites:
            vites = vites.lower()
            if vites == "manuel":
                manuel_checkbox = await tab.select('a[data-value="32467"].js-attribute.facetedCheckbox')
                await manuel_checkbox.click()
                await tab.sleep(1)
            elif vites == "otomatik":
                otomatik_checkbox = await tab.select('a[data-value="32466"].js-attribute.facetedCheckbox')
                await otomatik_checkbox.click()
                await tab.sleep(1)

        # Filtreleri uygula butonuna tıkla (Yıl veya KM gibi alanlarda)
        filter_apply = await tab.select('button.js-manual-search-button')
        if filter_apply:
            await filter_apply.click()
            await tab.sleep(2)
    else:
        print("Filtre bulunamadı!")

    # Her sayfanın araç verilerini çekmek için döngü.
    while True:
        try:
            # Sayfanın html içeriğini alır.
            html_content = await tab.get_content()
            # print(html_content[500:2500])
            # Alınan html'i bs4'e yapıştırır
            soup = BeautifulSoup(html_content, 'html.parser')

            # Sayfada eşleşen veriler çekilir.
            # Her ilan satırını bul
            ilanlar = soup.select('tr.searchResultsItem[data-id]')
            for ilan in ilanlar:
                try:
                    # Resim URL'si
                    img_tag = ilan.select_one('td.searchResultsLargeThumbnail img')
                    resim_url = img_tag['src'] if img_tag and img_tag.has_attr('src') else "N/A"

                    # Marka, Model, Motor
                    tag_attrs = ilan.select('td.searchResultsTagAttributeValue')
                    marka = tag_attrs[0].text.strip() if len(tag_attrs) > 0 else "N/A"
                    model = tag_attrs[1].text.strip() if len(tag_attrs) > 1 else "N/A"
                    motor = tag_attrs[2].text.strip() if len(tag_attrs) > 2 else "N/A"

                    # Başlık
                    baslik_tag = ilan.select_one('td.searchResultsTitleValue a.classifiedTitle')
                    baslik = baslik_tag.text.strip() if baslik_tag else "N/A"

                    # Yıl, KM, Renk
                    attr_vals = ilan.select('td.searchResultsAttributeValue')
                    yil = attr_vals[0].text.strip() if len(attr_vals) > 0 else "N/A"
                    km = attr_vals[1].text.strip().replace('.', '') if len(attr_vals) > 1 else "N/A"
                    renk = attr_vals[2].text.strip() if len(attr_vals) > 2 else "N/A"

                    # Fiyat
                    fiyat_tag = ilan.select_one('td.searchResultsPriceValue div.classified-price-container span')
                    fiyat = fiyat_tag.text.strip().split(' ')[0].replace('.', '') if fiyat_tag else "N/A"

                    # Tarih
                    tarih_tag = ilan.select_one('td.searchResultsDateValue')
                    if tarih_tag:
                        spans = tarih_tag.select('span')
                        tarih = ' '.join([span.text.strip() for span in spans])
                    else:
                        tarih = "N/A"

                    # Şehir
                    sehir_tag = ilan.select_one('td.searchResultsLocationValue')
                    sehir = sehir_tag.text.strip().replace(" ", "/") if sehir_tag else "N/A"

                    # Motor hacmi filtresi kontrolü
                    if not motor_hacmi or motor_hacmi in motor:
                        try:
                            yil_int = int(yil) if yil != "N/A" else 0
                            km_int = int(km) if km != "N/A" else 0
                            fiyat_int = int(fiyat) if fiyat != "N/A" else 0
                            print(marka, motor, renk, model, yil_int, baslik, km_int, fiyat_int, tarih, sehir, resim_url)
                            database.veri_ekle(marka, motor, renk, model, yil_int, baslik, km_int, fiyat_int, tarih, sehir, resim_url)
                        except ValueError as e:
                            print(f"Veri dönüşüm hatası: {e}")
                            continue
                except Exception as e:
                    print(f"Bir ilan işlenirken hata oluştu: {e}")
                    continue

            # Sayfanın verileri alınıp işlendikten sonra sonraki sayfaya geçer
            next_button = await tab.select('.prevNextBut[title="Sonraki"]')
            if not next_button:
                print("Son sayfaya gelindi, işlem tamamlandı.")
                break
            await next_button.click()
            await tab.sleep(2)

        except Exception as e:
            print("Son sayfaya ulaşıldı veya bir hata oluştu:", str(e))
            break

    # Driver kapatılır.
    print("Bitti")
    driver.stop()