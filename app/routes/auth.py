from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models.models import Admin, Musteri, Arac, GirisCikisKayit, Abonelik, Odeme

auth = Blueprint("auth", __name__)

# ------------------ Admin Giriş ------------------
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            session["admin_id"] = admin.id
            session["admin_logged_in"] = True
            flash("Giriş başarılı!", "success")
            return redirect(url_for("main.index"))
        else:
            flash("Geçersiz kullanıcı adı veya şifre!", "danger")
    
    return render_template("admin_login.html")

# ------------------ Plaka Giriş ------------------
@auth.route("/plaka-login", methods=["POST"])
def plaka_login():
    plaka = request.form.get("plaka")
    password = request.form.get("password")

    if not plaka or not password:
        flash("Plaka ve şifre zorunludur!", "danger")
        return redirect(url_for("auth.login"))

    musteri = Musteri.query.filter_by(plaka=plaka).first()

    if musteri and musteri.check_password(password):
        session["plaka"] = plaka
        session["plaka_giris"] = True
        return redirect(url_for("auth.plaka_bilgileri", plaka=plaka))
    else:
        flash("Geçersiz plaka veya şifre!", "danger")
        return redirect(url_for("auth.login"))

# ------------------ Plaka Bilgi Sayfası ------------------
@auth.route("/plaka-bilgileri/<plaka>")
def plaka_bilgileri(plaka):
    if not session.get("plaka_giris") or session.get("plaka") != plaka:
        flash("Yetkisiz erişim!", "danger")
        return redirect(url_for("auth.login"))

    arac = Arac.query.filter_by(plaka=plaka).first()
    musteri = Musteri.query.get(arac.musteri_id) if arac else None
    kayitlar = GirisCikisKayit.query.filter_by(arac_id=arac.id).all() if arac else []
    abonelikler = Abonelik.query.filter_by(musteri_id=arac.musteri_id).all() if arac else []
    odemeler = Odeme.query.filter(Odeme.kayit_id.in_([k.id for k in kayitlar])).all() if kayitlar else []

    return render_template("plaka_Bilgileri.html", arac=arac, musteri=musteri, kayitlar=kayitlar,
                           abonelikler=abonelikler, odemeler=odemeler)

# ------------------ Admin Çıkış ------------------
@auth.route("/logout")
def logout():
    session.clear()
    flash("Çıkış yapıldı.", "info")
    return redirect(url_for("auth.login"))

# ------------------ Kullanıcı Çıkış (Plaka) ------------------
@auth.route("/user_logout")
def user_logout():
    session.pop("plaka", None)
    session.pop("plaka_giris", None)
    flash("Kullanıcı çıkışı yapıldı.", "info")
    return redirect(url_for("auth.login"))
