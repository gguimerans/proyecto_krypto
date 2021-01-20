from movements import app
from flask import render_template, request, url_for, redirect
import csv
import sqlite3
from datetime import date, datetime

@app.route("/")
def portada():
    conn = sqlite3.connect("movements/data/bbdd_crypto.db")
    c = conn.cursor()
    c.execute("SELECT date, time, from_currency, from_quantity, to_currency, to_quantity, from_quantity/to_quantity FROM tabla_movimientos;")

    movimientos = c.fetchall()

    conn.close()

    return render_template("portada.html", movimientos=movimientos) 

    

@app.route("/compra", methods=["GET", "POST"])
def compraCrypto():
    monedas = ("EUR", "BTC", "ETH", "XRP", "LTC", "BCH", "BNB", "USDT", "EOS", "BSV", "XLM", "ADA", "TRX")

    if request.method == "POST":

        now = datetime.now()
        fecha = now.strftime('%Y/%m/%d')
        hora = now.strftime("%H:%M:%S")

        conn = sqlite3.connect("movements/data/bbdd_crypto.db")
        c = conn.cursor()

        c.execute("INSERT INTO tabla_movimientos (date, time, from_currency, from_quantity, to_currency, to_quantity) VALUES (?,?,?,?,?,?);",
                (
                    fecha, hora, 
                    request.form.get("fromMoneda"),
                    float(request.form.get("cantidadFrom")),
                    request.form.get("toMoneda"),
                    float(request.form.get("cantidadTo"))     
                )
        )    
            
        conn.commit()
        conn.close()

        return redirect(url_for("portada"))
          

    return render_template("compra.html", monedas=monedas)

@app.route("/status", methods=["GET"])
def statusCrypto():
    return render_template("estado.html")