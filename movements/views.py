from movements import app
from movements.forms import MovementForm
from flask import render_template, request, url_for, redirect 
from datetime import date, datetime
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from tools.dbaccess import queriesDB
import json

DBFILE = app.config["DBFILE"]
queries = queriesDB(DBFILE)


def getListaCryptos():
    consultaToAll = queries.getconsultaToAll()

    consultaFromAll = queries.getconsultaFromAll()

    listaCrypto = consultaToAll

    if consultaToAll:
        if consultaFromAll:
            for registroTo in consultaToAll:
                monedaTo = registroTo["to_currency"]
                for registroFrom in consultaFromAll:
                    monedaFrom = registroFrom["from_currency"]
                    if monedaTo == monedaFrom:
                        registroTo["importe_destino"] -= registroFrom["importe_origen"]
                        break

    return listaCrypto

def cargaMonedasDisponibles(select):
    listaCrypto = getListaCryptos()
    
    monedasDisponibles = ["EUR"]
    if listaCrypto:
        for registro in listaCrypto:
            if registro["importe_destino"] > 0:
                monedasDisponibles += [registro["to_currency"]]
    
    select.choices = monedasDisponibles


@app.route("/", methods=["GET", "POST"])
def movimientosCrypto():
    movimientos = queries.getMovimientosCrypto()
    return render_template("movimientos.html", movimientos=movimientos)

@app.route("/compra", methods=["GET", "POST"])
def compraCrypto():

    form = MovementForm()
    cargaMonedasDisponibles(form.from_currency)

    if request.method == "POST":
        now = datetime.now()
        fecha = now.strftime('%Y-%m-%d')
        hora = now.strftime("%H:%M:%S")
        if form.validate():           
            queries.insertaCompra((fecha, hora, form.from_currency.data, form.from_quantity.data, form.to_currency.data, form.to_quantity.data))
            return redirect(url_for("movimientosCrypto"))
        else:
            return render_template("compra.html", form=form)           

    return render_template("compra.html", form=form)
    


@app.route("/estado", methods=["GET", "POST"])
def statusCrypto():
    
    #Consulta de saldo de Euros     
    consultaSaldo = queries.getSaldoEuros()

    saldoEuros = 0

    if consultaSaldo:
        saldoEuros = consultaSaldo[0]

    #Consulta de total de Euros invertidos
    consultaTotal = queries.getEurosInvertidos()

    totalEuros = 0

    if consultaTotal:
        totalEuros = consultaTotal[0]

    #Consulta listado de cryptomonedas y sus valores
    listaCrypto = getListaCryptos()

    #Consulta saldo Cryptomonedas: pendiente conexión con API para hacer conversión real (saldoCryptoenEuros)   
    saldoCrypto = 0
    for registroCrypto in listaCrypto:    
        saldoCrypto += registroCrypto[0]

    saldoCryptoenEuros = saldoCrypto

    #Valor actual: cálculo de Total de euros invertidos + Saldo de euros invertidos (ganancia/perdida) + Valor de euros de nuestras cryptos (inversión atrapada)
    valorActual = totalEuros + saldoEuros + saldoCryptoenEuros

    return render_template("estado.html", totalEuros=totalEuros, valorActual=valorActual)