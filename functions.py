import psycopg2


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

    ### Listelere tek tek contentleri eklem
    try:
        obje = {}
        obje['İlan Başlığı'] = ilan_basligi
        obje['Model'] = ilan_model
        obje['Kilometre'] = ilan_kilometre
        obje['Fiyat'] = ilan_fiyati
        obje['Adres'] = ilan_tarihi
        obje['Tarih'] = ilan_sehir

        cursor.execute("""
                    INSERT INTO sahibinden (baslik, model, kilometre, fiyat, adres, tarih)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (obje['İlan Başlığı'], obje['Model'], obje['Kilometre'], obje['Fiyat'], obje['Adres'], obje['Tarih']))

    except Exception as e:
        print(f"Veri aktarılamadı hata kodu: {e}")

    connect.commit()
    cursor.close()
    connect.close()

    return

if __name__ == "__main__":
    print("Fonksiyonlar başarıyla içeri aktarıldı.")