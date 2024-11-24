# Sahibinden.com Web Scraper

Bu proje, Sahibinden.com web sitesinden araç ilan verilerini toplamak için Python tabanlı bir web kazıyıcı(scrape) sağlar. Selenium tarayıcı otomasyonu ve PostgreSQL veri saklama için kullanılmaktadır.

---

## Özellikler

- **Otomatik Veri Çekme**: Sahibinden.com'da gezinir, filtre uygular ve araç ilanlarını çeker.
- **Veri Depolama**: Çekilen verileri PostgreSQL veritabanına kaydeder.
- **Özelleştirilebilir Filtreler**: Araç modeli, yıl aralığı, şanzıman türü ve motor hacmine göre filtreleme yapabilir.

---

## Gereksinimler

- `Python 3.x`
- `Chrome`
- `PostreSQL`

---

### Python Kütüphaneleri

Kullanılan python kütüphaneleri.

- `selenium`
- `undetected_chromedriver`
- `psycopg2`

---

### PostgreSQL
Bu projede PostreSQL kullanılmaktadır, internetten kurulum sağlayabilirsiniz.

1. `postgres` adlı bir veritabanı oluşturun (veya bağlantı ayarlarını scriptte düzenleyin).
2. Varsayılan script bilgileri:
    - Host: `localhost`
    - Port: `5432`
    - Kullanıcı: `postgres`
    - Şifre: `1234`

---

## Kullanım

1. Depoyu klonlayın:
```bash
git clone https://github.com/0Baris/sahibinden-scraper.git
cd sahibinden-scraper
pip install -r requirements.txt

```

2. main.py'de filtreleri özelleştirin:
```python
arama = "Volkswagen Golf"  # Gerekli arama anahtar kelimesi
yıl_min = "2012"         # Opsiyonel minimum yıl
yıl_max = ""            # Opsiyonel maksimum yıl
motor_hacmi = ""            # Opsiyonel motor hacmi
vites = "Otomatik"          # Opsiyonel şanzıman türü ("Manuel" veya "Otomatik" olarak ayarlanabilir.)
```

3. Dosyayı çalıştırın:
```bash
python main.py
```

4. Veriler PostgreSQL veritabanınızdaki `sahibinden` tablosuna kaydedilecektir.

---

## İletişim

Herhangi bir geri bildiriminiz veya sorununuz varsa lütfen bariscem@proton.me adresinden bana ulaşabilirsiniz.
