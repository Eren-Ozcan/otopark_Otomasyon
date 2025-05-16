# 🚗 Otopark Otomasyon Sistemi

Modern, esnek ve güvenli bir **Flask** tabanlı otopark yönetim platformu. Küçük ve orta ölçekli işletmeler için müşteriler, araçlar, giriş/çıkış kayıtları, abonelikler ve ödemeler tek çatı altında yönetilir.

---

## ✨ Özellikler

- **Admin Paneli**  
  - Güçlü CRUD (Oluştur/Görüntüle/Güncelle/Sil) işlemleri  
  - Müşteri, Araç, Giriş/Çıkış, Abonelik ve Ödeme yönetimi  
  - Test veri ekleme arayüzü  

- **Müşteri Self-Service**  
  - “Plaka ile Giriş” ile kişisel panel  
  - Kendi araç, abonelik ve ödeme geçmişini görüntüleme  
  - Kolay oturum kapatma  

- **Güvenlik**  
  - Scrypt ile tek yönlü parola hash’leme  
  - Fernet ile reversible (geri çözülebilir) şifre saklama  
  - Oturum bazlı yetkilendirme  

- **Temiz UI & Responsive Tasarım**  
  - Modern renk paleti ve gölgeler  
  - Grid tabanlı dashboard kartları  
  - Tüm cihazlarda uyumlu form ve tablo düzeni  

---

## 🛠️ Teknolojiler

- **Backend:** Python · Flask · Flask-SQLAlchemy  
- **Veritabanı:** PostgreSQL (yada SQLite/MySQL)  
- **Şifreleme:** Werkzeug Scrypt · Cryptography (Fernet)  
- **Frontend:** Jinja2 · HTML5 · CSS3 (Custom Properties, Grid, Flexbox)  

---

## 🚀 Kurulum & Çalıştırma

1. **Projeyi klonlayın**  
   ```bash
   git clone https://github.com/Eren-Ozcan/otopark_Otomasyon.git
   cd otopark_Otomasyon


Sanal ortam oluşturun

bash
Kopyala
Düzenle
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows


Bağımlılıkları yükleyin

bash
Kopyala
Düzenle
pip install -r requirements.txt
Çevresel değişkenleri tanımlayın

SECRET_KEY (Flask gizli anahtarı)

FERNET_KEY (Fernet için Base64 anahtar)

DATABASE_URL (örn. postgresql://user:pass@localhost/otopark_db)

Veritabanını hazırlayın

bash
Kopyala
Düzenle
flask db upgrade        # Eğer Alembic migration kullanıyorsanız
Uygulamayı başlatın

bash
Kopyala
Düzenle
flask run
Ardından http://127.0.0.1:5000/ adresini ziyaret edin.


📂 Proje Yapısı

csharp
Kopyala
Düzenle
otopark_Otomasyon/
├── app/
│   ├── __init__.py        # Uygulama fabrikası
│   ├── models.py          # ORM modelleri & ilişkiler
│   ├── routes/
│   │   ├── auth.py        # Giriş/çıkış rotaları
│   │   └── main.py        # Admin & CRUD rotaları
│   └── templates/         # Jinja2 şablonları
├── static/
│   └── style.css          # Ortak CSS & responsive düzen
├── config.py              # Ayarlar & gizli anahtarlar
├── requirements.txt       # Python paketleri
└── run.py                 # Sunucu başlatıcı


📝 Kullanım Notları

Admin Girişi: /login

Plaka Girişi: /plaka-login

Dashboard: /

Müşteriler: /customers

Araçlar: /vehicles

Giriş/Çıkış: /entry_exit

Abonelikler: /subscriptions

Ödemeler: /payments

Test Veri Ekleme: /add-sample-data

👩‍💻 Geliştirici
Eren ÖZCAN
(https://github.com/Eren-Ozcan)
Buse ÇAKAL
[https://github.com/busecakal]