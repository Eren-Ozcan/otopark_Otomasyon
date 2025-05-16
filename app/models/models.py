from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship

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
    plaka = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))

    araclar = relationship(
        'Arac',
        back_populates='musteri',
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    abonelikler = relationship(
        'Abonelik',
        back_populates='musteri',
        cascade='all, delete-orphan',
        passive_deletes=True
    )

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
    musteri_id = db.Column(
        db.Integer,
        db.ForeignKey('musteriler.id', ondelete='CASCADE'),
        nullable=False
    )

    musteri = relationship('Musteri', back_populates='araclar')
    kayitlar = relationship(
        'GirisCikisKayit',
        back_populates='arac',
        cascade='all, delete-orphan',
        passive_deletes=True
    )


class GirisCikisKayit(db.Model):
    __tablename__ = 'giris_cikis_kayit'
    id = db.Column(db.Integer, primary_key=True)
    arac_id = db.Column(
        db.Integer,
        db.ForeignKey('araclar.id', ondelete='CASCADE'),
        nullable=False
    )
    giris_zamani = db.Column(db.DateTime)
    cikis_zamani = db.Column(db.DateTime)

    arac = relationship('Arac', back_populates='kayitlar')
    odemeler = relationship(
        'Odeme',
        back_populates='kayit',
        cascade='all, delete-orphan',
        passive_deletes=True
    )


class Abonelik(db.Model):
    __tablename__ = 'abonelikler'
    id = db.Column(db.Integer, primary_key=True)
    musteri_id = db.Column(
        db.Integer,
        db.ForeignKey('musteriler.id', ondelete='CASCADE'),
        nullable=False
    )
    baslangic_tarihi = db.Column(db.Date)
    bitis_tarihi = db.Column(db.Date)
    abonelik_tipi = db.Column(db.String(50))

    musteri = relationship('Musteri', back_populates='abonelikler')


class Odeme(db.Model):
    __tablename__ = 'odemeler'
    id = db.Column(db.Integer, primary_key=True)
    kayit_id = db.Column(
        db.Integer,
        db.ForeignKey('giris_cikis_kayit.id', ondelete='CASCADE'),
        nullable=False
    )
    tutar = db.Column(db.Float)
    odeme_zamani = db.Column(db.DateTime)
    odeme_tipi = db.Column(db.String(50))

    kayit = relationship('GirisCikisKayit', back_populates='odemeler')
