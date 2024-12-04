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

2. main.py'de **sahibinden_arama** fonksiyonunu özelleştirin:

##### `sahibinden_arama(arama, yıl_min, yıl_max, motor_hacmi, vites)`

```python
arama = "Volkswagen Golf"  # Arama yapmak istediğiniz kelime veya model adı.
yıl_min = "2012"           # Opsiyonel: Minimum yıl.
yıl_max = ""               # Opsiyonel: Maksimum yıl.
motor_hacmi = ""           # Opsiyonel: Motor hacmi filtresi (örnek: "1.6").
vites = "Otomatik"         # Opsiyonel: Şanzıman türü ("Manuel" veya "Otomatik").
```

3. Dosyayı çalıştırın:
```bash
python main.py
```

4. Veriler PostgreSQL veritabanınızdaki `sahibinden` tablosuna kaydedilecektir.

---

## İletişim

Herhangi bir geri bildiriminiz veya sorununuz varsa bariscem@proton.me adresinden bana ulaşabilirsiniz.
