import psycopg2


def veri_cek(marka, motor, renk, ilan_model, yil, ilan_basligi, ilan_kilometre, ilan_fiyati, ilan_sehir,ilan_tarihi):
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
        marka VARCHAR(30),
        model VARCHAR(100),
        motor VARCHAR(75),
        renk VARCHAR(20),
        yil INT,
        kilometre INT,
        fiyat INT,
        tarih VARCHAR(100),
        adres VARCHAR(100)
        
    )
    
    """)


    try:
        obje = {}
        obje['İlan Başlığı'] = ilan_basligi
        obje['Marka'] = marka
        obje['Model'] = ilan_model
        obje['Motor'] = motor
        obje['Renk'] = renk
        obje['Yıl'] = yil
        obje['Kilometre'] = ilan_kilometre
        obje['Fiyat'] = ilan_fiyati
        obje['Adres'] = ilan_tarihi
        obje['Tarih'] = ilan_sehir

        cursor.execute("""
                           INSERT INTO sahibinden (baslik, marka, motor, model, renk, yil, kilometre, fiyat, adres, tarih)
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                           """, (
                                        obje['İlan Başlığı'], obje['Marka'], obje['Motor'], obje['Model'], obje['Renk'], obje['Yıl'], obje['Kilometre'],
                                            obje['Fiyat'], obje['Adres'], obje['Tarih']))

    except Exception as e:
        print(f"Veri aktarılamadı hata kodu: {e}")

    connect.commit()
    cursor.close()
    connect.close()

    return

if __name__ == "__main__":
    print("Fonksiyonlar başarıyla içeri aktarıldı.")