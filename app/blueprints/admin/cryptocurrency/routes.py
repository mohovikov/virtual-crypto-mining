from flask import flash, jsonify, redirect, render_template, request, url_for
from flask.typing import ResponseReturnValue

from app import services
from app.extensions import db
from app.forms import admin_forms as forms
from app.blueprints.admin.cryptocurrency import cryptocurrency
from app.models.crypto_price_history import CryptoPriceHistory


@cryptocurrency.route("/")
def all():
    return render_template(
        "admin/cryptocurrency/all.html",
        cryptocurrencies = services.get_all_cryptocurrencies()
    )

@cryptocurrency.route("/add", methods=["GET", "POST"])
def add():
    form = forms.ManageCryptocurrencyForm()

    if form.validate_on_submit():
        success, message, category = services.create_cryptocurrency(form)

        if not success:
            flash(message, category)
        flash(message, category)
        return redirect(url_for('admin.cryptocurrency.all'))

    return render_template(
        "admin/cryptocurrency/add.html",
        form = form
    )

@cryptocurrency.route("<int:crypto_id>/edit", methods=["GET", "POST"])
def edit(crypto_id):
    form = forms.ManageCryptocurrencyForm()
    data = services.get_cryptocurrency(crypto_id)

    if not data:
        flash("Такой криптовалюты не существует", "warning")
        return redirect(url_for('admin.cryptocurrency.all'))
    
    if form.validate_on_submit():
        submit, message, category = services.edit_cryptocurrency(data, form)

        if not submit:
            flash(message, category)
        flash(message, category)
        return redirect(url_for('admin.cryptocurrency.all'))

    return render_template(
        "admin/cryptocurrency/edit.html",
        cryptocurrency = data,
        form = form
    )

@cryptocurrency.route("<int:crypto_id>/update-price")
def update_price(crypto_id) -> ResponseReturnValue:
    message, category = services.update_price_cryptocurrency(crypto_id)

    flash(message, category)
    return redirect(request.referrer or url_for('admin.cryptocurrency.all'))

@cryptocurrency.route("/<int:crypto_id>/history")
def history(crypto_id: int):
    history = (
        db.session.query(CryptoPriceHistory)
        .filter_by(crypto_id=crypto_id)
        .order_by(CryptoPriceHistory.created_at.desc())
        .limit(50)
        .all()
    )

    # Формируем список для JSON
    data = [
        {"timestamp": h.created_at.isoformat(), "price": float(h.price)}
        for h in reversed(history)
    ]

    return jsonify(data)