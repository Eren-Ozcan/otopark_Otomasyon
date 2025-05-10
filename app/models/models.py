from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(db.Model):
    __tablename__ = 'adminler'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Musteri(db.Model):
    __tablename__ = 'musteriler'
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(50))
    soyad = db.Column(db.String(50))
    telefon = db.Column(db.String(20), unique=True)

    # Kullanıcı olarak giriş yapılabilmesi için:
    plaka = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Arac(db.Model):
    __tablename__ = 'araclar'
    id = db.Column(db.Integer, primary_key=True)
    plaka = db.Column(db.String(20), unique=True, nullable=False)
    marka = db.Column(db.String(50))
    model = db.Column(db.String(50))
    musteri_id = db.Column(db.Integer, db.ForeignKey('musteriler.id'))


class GirisCikisKayit(db.Model):
    __tablename__ = 'giris_cikis_kayit'
    id = db.Column(db.Integer, primary_key=True)
    arac_id = db.Column(db.Integer, db.ForeignKey('araclar.id'))
    giris_zamani = db.Column(db.DateTime)
    cikis_zamani = db.Column(db.DateTime)


class Abonelik(db.Model):
    __tablename__ = 'abonelikler'
    id = db.Column(db.Integer, primary_key=True)    
    musteri_id = db.Column(db.Integer, db.ForeignKey('musteriler.id'))
    baslangic_tarihi = db.Column(db.Date)
    bitis_tarihi = db.Column(db.Date)
    abonelik_tipi = db.Column(db.String(50))


class Odeme(db.Model):
    __tablename__ = 'odemeler'
    id = db.Column(db.Integer, primary_key=True)
    kayit_id = db.Column(db.Integer, db.ForeignKey('giris_cikis_kayit.id'))
    tutar = db.Column(db.Float)
    odeme_zamani = db.Column(db.DateTime)
    odeme_tipi = db.Column(db.String(50))
