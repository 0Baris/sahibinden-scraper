import psycopg2
import sqlite3
from typing import Dict, Any
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=30)

# Veritabanı yöneticisi.
class DatabaseHandler:
    def __init__(self, db_type: str = "sqlite"):
        """
        db_type: "sqlite" veya "postgres" olabilir.
        """
        
        self.db_type = db_type
        self.conn = None
        self.cursor = None

        try:
            if db_type == "sqlite":
                db_path = os.getenv('SQLITE_DB_PATH')
                if not db_path:
                    raise ValueError("SQLITE_DB_PATH environment variable is not set")
                self.conn = sqlite3.connect(db_path)
            elif db_type == "postgres":
                self.conn = psycopg2.connect(
                    host=os.getenv('POSTGRES_HOST'),
                    dbname=os.getenv('POSTGRES_DB'),
                    user=os.getenv('POSTGRES_USER'),
                    password=os.getenv('POSTGRES_PASSWORD'),
                    port=int(os.getenv('POSTGRES_PORT'))
                )
            else:
                raise ValueError(f"Desteklenmeyen veri tabanı tipi: {db_type}")

            self.cursor = self.conn.cursor()
            self._create_table()
        except Exception as e:
            print(f"Database connection error: {e}")
            raise
    
    def _create_table(self):
        """
        Veritabanı için tablo oluşturur, eğer yeni bir veri eklenicekse buradan ekleyip yeniden tablo oluşturabilirsiniz.
        """
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS sahibinden(
            id INTEGER PRIMARY KEY,
            baslik VARCHAR(150),
            marka VARCHAR(30),
            model VARCHAR(100),
            motor VARCHAR(75),
            renk VARCHAR(20),
            yil INT,
            kilometre INT,
            fiyat INT,
            tarih VARCHAR(100),
            adres VARCHAR(100),
            resim_url VARCHAR(300)
        )
        """)
    
    def add_data(self, data: Dict[str, Any]):
        """
        Verileri veri tabanına kayıt eder, eğer eşleşen araç varsa o araç atlanır.
        """
        try:
            # Veri mevcut mu diye kontrol eder.
            query = """
                SELECT 1 FROM sahibinden 
                WHERE baslik=%s AND motor=%s AND adres=%s
            """ if self.db_type == "postgres" else """
                SELECT 1 FROM sahibinden 
                WHERE baslik=? AND motor=? AND adres=?
            """
            self.cursor.execute(query, (data['başlık'], data['motor'], data['adres']))

            if not self.cursor.fetchone():
                insert_query = """
                    INSERT INTO sahibinden 
                    (baslik, marka, model, motor, renk, yil, kilometre, fiyat, tarih, adres, resim_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """ if self.db_type == "postgres" else """
                    INSERT INTO sahibinden 
                    (baslik, marka, model, motor, renk, yil, kilometre, fiyat, tarih, adres, resim_url)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                self.cursor.execute(insert_query, (
                    data['başlık'], data['marka'], data['model'],
                    data['motor'], data['renk'], data['yil'],
                    data['kilometre'], data['fiyat'],
                    data['tarih'], data['adres'], data['resim_url']
                ))
                self.conn.commit()
            else:
                print(f"Araç halihazırda kayıtlı: {data['başlık']}, {data['fiyat']}")
        except Exception as e:
                print(f"Hata: {e}")
                self.conn.rollback()

    def __del__(self):
        """
        Bağlantılar kapatılır.
        """
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

## Veri tabanına veri eklemek için kullanılacak fonksiyon. Yapacağınız değişikleri DatabaseHandler içinde "add_data" fonksiyonu içinde yapmalısınız.
def veri_ekle(marka, motor, renk, ilan_model, yil, ilan_basligi, 
             ilan_kilometre, ilan_fiyati, ilan_tarihi, ilan_sehir, resim_url):
    """
    Spesifik olarak dokunulmamasını tavsiye ederim fakat test için basit bir veri gönderebilirsiniz.
    """
    
    db_type = os.getenv('DB_TYPE')
    db = DatabaseHandler(db_type=db_type)
    
    data = {
        'başlık': ilan_basligi,
        'marka': marka,
        'model': ilan_model,
        'motor': motor,
        'renk': renk,
        'yil': yil,
        'kilometre': ilan_kilometre,
        'fiyat': ilan_fiyati,
        'tarih': ilan_tarihi,
        'adres': ilan_sehir,
        'resim_url': resim_url
    }
    
    db.add_data(data)

if __name__ == "__main__":
    print("Fonksiyonlar başarıyla içeri aktarıldı.")