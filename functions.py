import psycopg2
from selenium.common import StaleElementReferenceException


def veri_cek(ilan_model,ilan_basligi,ilan_kilometre,ilan_fiyati,ilan_tarihi,ilan_sehir):
    """
    Sahibinden sitesinden verilerin çekilmesi ve dataframe oluşturulma aşaması burada gerçekleşir.
    :return:
    """

    connect = psycopg2.connect(host="localhost", dbname = "postgres",
                               user = "postgres", password = "1234",
                               port = 5432
                               )

    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS sahibinden(
        id SERIAL PRIMARY KEY,
        baslik VARCHAR(150),
        model VARCHAR(100),
        kilometre INT,
        fiyat INT,
        adres VARCHAR(150),
        tarih VARCHAR(50)
        
    )
    
    """)


    ### Listelere tek tek contentleri ekleme
    for i in range(min(len(ilan_model), len(ilan_basligi), len(ilan_kilometre), len(ilan_fiyati), len(ilan_tarihi), len(ilan_sehir))):
         try:
            obje = {}
            obje['İlan Başlığı'] = ilan_basligi[i].text.strip()
            obje['Model'] = ilan_model[i].text.strip()
            obje['Kilometre'] = ilan_kilometre[i].text.strip().replace('.', '')
            obje['Fiyat'] = ilan_fiyati[i].text[:-3].strip().replace('.', '')
            obje['Adres'] = ilan_tarihi[i].text.strip().replace('\n', ' ')
            obje['Tarih'] = ilan_sehir[i].text.strip().replace('\n', ' ')

            if all(obje.values()):
                cursor.execute("""
                INSERT INTO sahibinden (baslik, model, kilometre, fiyat, adres, tarih)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (obje['İlan Başlığı'], obje['Model'], obje['Kilometre'], obje['Fiyat'], obje['Adres'], obje['Tarih']))
         except StaleElementReferenceException:
             print("Hatalı işlem!")



    connect.commit()
    cursor.close()
    connect.close()

    """
    
    database = pd.DataFrame(items)

    try:
        ### Reklam satırlarının silinmesi
        database = database.dropna(how="any")

        ### Medyan,minimum ve maximum değerlerinin alınabilmesi için veri tipi değiştirilmesi
        database['Kilometre'] = pd.to_numeric(database['Kilometre'].replace('', np.nan), errors='coerce')

        ### Database mevcut olan 'TL' değerenin değiştirilmesi.
        database['Fiyat'] = database['Fiyat'].str.replace('TL', '', regex=False)
        database['Fiyat'] = database['Fiyat'].str.replace('.', '').str.strip()
        database['Fiyat'] = pd.to_numeric(database['Fiyat'], errors='coerce')

        ### Database'de mevcut olan Adresteki karakterleri temizleme.
        database['Adres'] = database['Adres'].str.replace('\n', ' ', regex=False)

        ### Database'de mevcut olan Tarihteki karakterleri temizleme.
        database['Tarih'] = database['Tarih'].str.replace('\n', ' ', regex=False)

    finally:
    """

    return print("Tamamlandı!")

if __name__ == "__main__":
    print("Fonksiyonlar başarıyla içeri aktarıldı.")