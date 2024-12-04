import psycopg2


def veri_cek(marka, motor, renk, ilan_model, yil, ilan_basligi, ilan_kilometre, ilan_fiyati, ilan_tarihi, ilan_sehir):
    """
    Sahibinden sitesinden çekilen veriler ile database oluşturulma aşaması burada gerçekleşir.
    :return:
    """

    ## Veritabanı bağlantısı.
    connect = psycopg2.connect(host="localhost", dbname = "postgres",
                               user = "postgres", password = "1234",
                               port = 5432
                               )

    ## Veritabanında işlem yapabilmek için cursor.
    cursor = connect.cursor()

    ## Veritabanı tablosu mevcut değilse oluşturulması.
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

    ## Veritabanına gelen verilerin aktarılması.
    try:
        ## Gelen verilerden sözlük oluşturulması.
        obje = {}
        obje['İlan Başlığı'] = ilan_basligi
        obje['Marka'] = marka
        obje['Model'] = ilan_model
        obje['Motor'] = motor
        obje['Renk'] = renk
        obje['Yıl'] = yil
        obje['Kilometre'] = ilan_kilometre
        obje['Fiyat'] = ilan_fiyati
        obje['İlan Tarihi'] = ilan_tarihi
        obje['Adres'] = ilan_sehir

        ## Veritabanındaki anlık verilerin her döngüde yenilenmesi.
        cursor.execute("SELECT baslik, motor, adres, kilometre,tarih  FROM sahibinden")
        mevcut_veriler = cursor.fetchall()

        ## Veritabanında gönderilen aracın verileri mevcut ise, verinin atlanması ve sonraki aracın verilerinin eklenmesi.
        yeni_veri = (obje['İlan Başlığı'], obje['Motor'], obje['Adres'], obje['Kilometre'], obje['İlan Tarihi'])
        if yeni_veri in mevcut_veriler:
                print("Veri atlandı")
        else:
            cursor.execute("""
                        INSERT INTO sahibinden 
                        (baslik, marka, motor, model, renk, yil, kilometre, fiyat, tarih, adres)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                    obje['İlan Başlığı'],
                    obje['Marka'],
                    obje['Motor'],
                    obje['Model'],
                    obje['Renk'],
                    obje['Yıl'],
                    obje['Kilometre'],
                    obje['Fiyat'],
                    obje['İlan Tarihi'],
                    obje['Adres']
                ))

            connect.commit()

    ## Hata yönetimi.
    except Exception as e:
        print(f"Veri aktarılamadı hata kodu: {e}")
        connect.rollback()

    ## İşlemlerin bitmesi ve veritabanı bağlantısının kapatılması.
    finally:
        cursor.close()
        connect.close()

    return

if __name__ == "__main__":
    print("Fonksiyonlar başarıyla içeri aktarıldı.")
