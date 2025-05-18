from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from app import db
from app.models.models import Musteri, Arac, GirisCikisKayit, Abonelik, Odeme
from datetime import datetime

main = Blueprint("main", __name__)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

@main.route("/")
@login_required
def index():
    musteri_sayisi = Musteri.query.count()
    arac_sayisi = Arac.query.count()
    kayit_sayisi = GirisCikisKayit.query.count()
    abonelik_sayisi = Abonelik.query.count()
    odeme_sayisi = Odeme.query.count()
    odeme_toplam = db.session.query(func.sum(Odeme.tutar)).scalar() or 0

    return render_template("index.html",
                           musteri_sayisi=musteri_sayisi,
                           arac_sayisi=arac_sayisi,
                           kayit_sayisi=kayit_sayisi,
                           abonelik_sayisi=abonelik_sayisi,
                           odeme_sayisi=odeme_sayisi,
                           odeme_toplam=odeme_toplam)

@main.route("/customers")
@login_required
def customers():
    # musteriler ve ilişkili araclar birlikte yükleniyor
    musteriler = Musteri.query.options(joinedload(Musteri.araclar)).all()
    return render_template("customers.html", musteriler=musteriler)

@main.route("/customers/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_customer(id):
    musteri = Musteri.query.options(joinedload(Musteri.araclar)).get_or_404(id)
    if request.method == "POST":
        # Temel müşteri alanları
        musteri.ad = request.form["ad"]
        musteri.soyad = request.form["soyad"]
        musteri.telefon = request.form["telefon"]

        # Plaka güncellemesi: eğer araç varsa ilkini al, yoksa yenisini oluştur
        yeni_plaka = request.form["plaka"]
        if musteri.araclar:
            arac = musteri.araclar[0]
            arac.plaka = yeni_plaka
        else:
            arac = Arac(plaka=yeni_plaka, musteri_id=musteri.id)
            db.session.add(arac)

        db.session.commit()
        flash("Müşteri ve plaka bilgisi güncellendi!", "success")
        return redirect(url_for("main.customers"))
    return render_template("edit_customer.html", musteri=musteri)


@main.route("/customers/delete/<int:id>", methods=["POST"])
@login_required
def delete_customer(id):
    musteri = Musteri.query.get_or_404(id)
    db.session.delete(musteri)
    db.session.commit()
    flash("Müşteri silindi.", "info")
    return redirect(url_for("main.customers"))

@main.route("/vehicles")
@login_required
def vehicles():
    araclar = Arac.query.all()
    return render_template("vehicles.html", araclar=araclar)

@main.route("/vehicles/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_vehicle(id):
    arac = Arac.query.get_or_404(id)
    if request.method == "POST":
        arac.plaka = request.form.get("plaka")
        arac.marka = request.form.get("marka")
        arac.model = request.form.get("model")
        db.session.commit()
        flash("Araç bilgisi güncellendi.", "success")
        return redirect(url_for("main.vehicles"))
    return render_template("edit_vehicle.html", arac=arac)

@main.route("/vehicles/delete/<int:id>", methods=["POST"])
@login_required
def delete_vehicle(id):
    arac = Arac.query.get_or_404(id)
    db.session.delete(arac)
    db.session.commit()
    flash("Araç silindi.", "success")
    return redirect(url_for("main.vehicles"))

@main.route("/entry_exit")
@login_required
def entry_exit():
    kayitlar = GirisCikisKayit.query.all()
    return render_template("entry_exit.html", kayitlar=kayitlar)

@main.route("/entry_exit/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_entry(id):
    kayit = GirisCikisKayit.query.get_or_404(id)
    if request.method == "POST":
        giris = request.form.get("giris_zamani")
        cikis = request.form.get("cikis_zamani") or None
        kayit.giris_zamani = datetime.fromisoformat(giris) if giris else None
        kayit.cikis_zamani = datetime.fromisoformat(cikis) if cikis else None
        db.session.commit()
        flash("Kayıt başarıyla güncellendi.", "success")
        return redirect(url_for("main.entry_exit"))
    return render_template("edit_entry.html", kayit=kayit)

@main.route("/entry_exit/delete/<int:id>", methods=["POST"])
@login_required
def delete_entry(id):
    kayit = GirisCikisKayit.query.get_or_404(id)
    db.session.delete(kayit)
    db.session.commit()
    flash("Kayıt başarıyla silindi.", "success")
    return redirect(url_for("main.entry_exit"))

@main.route("/subscriptions")
@login_required
def subscriptions():
    abonelikler = Abonelik.query.all()
    return render_template("subscriptions.html", abonelikler=abonelikler)

@main.route("/subscriptions/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_subscription(id):
    ab = Abonelik.query.get_or_404(id)
    if request.method == "POST":
        ab.baslangic_tarihi = request.form["baslangic_tarihi"]
        ab.bitis_tarihi = request.form["bitis_tarihi"]
        ab.abonelik_tipi = request.form["abonelik_tipi"]
        db.session.commit()
        flash("Abonelik güncellendi.", "success")
        return redirect(url_for("main.subscriptions"))
    return render_template("edit_subscription.html", abonelik=ab)

@main.route("/subscriptions/delete/<int:id>", methods=["POST"])
@login_required
def delete_subscription(id):
    ab = Abonelik.query.get_or_404(id)
    db.session.delete(ab)
    db.session.commit()
    flash("Abonelik silindi.", "success")
    return redirect(url_for("main.subscriptions"))

@main.route("/payments")
@login_required
def payments():
    odemeler = Odeme.query.all()
    return render_template("payments.html", odemeler=odemeler)

@main.route("/payments/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_payment(id):
    od = Odeme.query.get_or_404(id)
    if request.method == "POST":
        od.kayit_id     = request.form["kayit_id"]
        od.tutar        = float(request.form["tutar"])
        od.odeme_zamani = datetime.fromisoformat(request.form["odeme_zamani"])
        od.odeme_tipi   = request.form["odeme_tipi"]
        db.session.commit()
        flash("Ödeme güncellendi.", "success")
        return redirect(url_for("main.payments"))
    return render_template("edit_payment.html", odeme=od)

@main.route("/payments/delete/<int:id>", methods=["POST"])
@login_required
def delete_payment(id):
    od = Odeme.query.get_or_404(id)
    db.session.delete(od)
    db.session.commit()
    flash("Ödeme silindi.", "success")
    return redirect(url_for("main.payments"))

@main.route("/add-sample-data", methods=["GET", "POST"])
@login_required
def add_sample_data():
    if request.method == "POST":
        # Müşteri oluştur (plaka bilgisi araçta saklanacak)
        musteri = Musteri(
            ad=request.form.get("musteri_ad"),
            soyad=request.form.get("musteri_soyad"),
            telefon=request.form.get("musteri_telefon")
        )
        musteri.set_password(request.form.get("musteri_password"))
        db.session.add(musteri)
        db.session.flush()

        # Araç oluştur
        arac = Arac(
            plaka=request.form.get("musteri_plaka"),
            marka=request.form.get("arac_marka"),
            model=request.form.get("arac_model"),
            musteri_id=musteri.id
        )
        db.session.add(arac)
        db.session.flush()

        # Giriş/Çıkış kaydı
        giris = request.form.get("giris_zamani")
        cikis = request.form.get("cikis_zamani") or None
        giris_dt = datetime.fromisoformat(giris) if giris else None
        cikis_dt = datetime.fromisoformat(cikis) if cikis else None

        kayit = GirisCikisKayit(
            arac_id=arac.id,
            giris_zamani=giris_dt,
            cikis_zamani=cikis_dt
        )
        db.session.add(kayit)
        db.session.flush()

        # Abonelik
        if request.form.get("abonelik_baslangic") and request.form.get("abonelik_bitis"):
            abonelik = Abonelik(
                musteri_id=musteri.id,
                baslangic_tarihi=request.form.get("abonelik_baslangic"),
                bitis_tarihi=request.form.get("abonelik_bitis"),
                abonelik_tipi=request.form.get("abonelik_tipi")
            )
            db.session.add(abonelik)

        # Ödeme
        if request.form.get("odeme_tutar"):
            odeme = Odeme(
                kayit_id=kayit.id,
                tutar=float(request.form.get("odeme_tutar")),
                odeme_zamani=datetime.fromisoformat(request.form.get("odeme_zamani")) if request.form.get("odeme_zamani") else datetime.utcnow(),
                odeme_tipi=request.form.get("odeme_tipi")
            )
            db.session.add(odeme)

        db.session.commit()
        flash("Veriler başarıyla eklendi!", "success")
        return redirect(url_for("main.index"))

    return render_template("add_sample_data.html")
