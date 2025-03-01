# Sahibinden.com Web Scraper

Bu proje, Sahibinden.com web sitesinden araç ilan verilerini toplamak için Python tabanlı bir web kazıyıcı(scrape) sağlar. Nodriver tarayıcı otomasyonu ve SQLite3 veya Postresql veri saklama için kullanılmaktadır.

---

## Özellikler

- **Otomatik Veri Çekme**: Sahibinden.com'da gezinir, filtre uygular ve araç ilanlarını çeker.
- **Veri Depolama**: Çekilen veriler SQLite3 veya Postresql veritabanına kaydeder.
- **Özelleştirilebilir Filtreler**: Araç modeli, yıl aralığı, şanzıman türü ve motor hacmine göre filtreleme yapabilir.

---

## Gereksinimler

- `Python 3.x`
- `Chrome`
- `DB Browser?`
- `PostreSQL?`

---

### Python Kütüphaneleri

Kullanılan python kütüphaneleri.

- `nodriver`
- `undetected_chromedriver`
- `bs4`
- `psycopg2`

---

### PostgreSQL -- **İsteğe bağlı!** -- SQLite mevcuttur.
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
```
```bash
cd sahibinden-scraper
```
```bash
pip install -r requirements.txt
```

2. main.py'de **belirtilen yerleri** özelleştirin:

##### `main(arama, yıl_min, yıl_max, motor_hacmi, vites)`

```python
arama = "Volkswagen Golf"  # Arama yapmak istediğiniz kelime veya model adı.
yıl_min = "2012"           # Opsiyonel: Minimum yıl.
yıl_max = ""               # Opsiyonel: Maksimum yıl.
motor_hacmi = ""           # Opsiyonel: Motor hacmi filtresi (örnek: "1.6").
vites = "Otomatik"         # Opsiyonel: Şanzıman türü ("Manuel" veya "Otomatik").
```

3. Paylaşılan .env Dosyasını düzenleyin.
```bash
# Veritabanı tercihi "sqlite" veya "postgres" başka bir şey denemeyin hata alırsınız.
DB_TYPE=postgres

# SQLite veritabanı ismi.
SQLITE_DB_PATH=sahibinden.db

# PostreSQL yapılandırması.
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=veritabanı_ismi
POSTGRES_USER=kullanıcı_adı
POSTGRES_PASSWORD=sifre
```


4. Dosyayı çalıştırın:
```bash
python main.py
```

5. Veriler tercih ettiğiniz veritabanına kaydedilecektir.

---

## İletişim

Herhangi bir geri bildiriminiz veya sorununuz varsa bariscem@proton.me adresinden bana ulaşabilirsiniz.
