from movements import app
from flask import render_template, request, url_for, redirect
import csv

@app.route("/")
def portada():
    fMovimientos = open("movements/data/BBDD.csv", "r")
    csvReader = csv.reader(fMovimientos, delimiter=",", quotechar="'")
    movimientos = list(csvReader)

    print (movimientos)

    return render_template("portada.html", datos=movimientos)

@app.route("/compra", methods=["GET", "POST"])
def compraCrypto():
    if request.method == "POST":
        fMovimientos = open("movements/data/BBDD.csv", "w+")
        csvWriter = csv.writer(fMovimientos, delimiter=",", quotechar="'")
        csvWriter.writerow([request.form.get("from"), request.form.get("to"), request.form.get("Q")])
        return redirect(url_for("portada"))
          

    return render_template("compra.html")