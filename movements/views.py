from movements import app
from movements.forms import MovementForm
from flask import render_template, request, url_for, redirect 
from datetime import date, datetime
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from tools.dbaccess import queriesDB
import json
from tools.apicomm import CryptoAPI

DBFILE = app.config["DBFILE"]
queries = queriesDB(DBFILE)

API_URL = app.config["API_URL"]
API_KEY = app.config["API_KEY"]
manejaAPI = CryptoAPI(API_URL, API_KEY)


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

    return listaCrypto


def getPrecioUnitarioCrypto(params):
    data = manejaAPI.consultaApi(params)
    return data["data"]["quote"][params[2]]["price"]


@app.route("/", methods=["GET"])
def movimientosCrypto():
    movimientos = queries.getMovimientosCrypto()
    return render_template("movimientos.html", movimientos=movimientos)

@app.route("/compra", methods=["GET", "POST"])
def compraCrypto():

    try:
        form = MovementForm()
        listaCrypto = cargaMonedasDisponibles(form.from_currency)

        if request.method == "POST":

            #Si se pulsa Aceptar se esta confirmando la compra, por lo que no hace falta pasar la validación del formulario
            if form.submit.data:
                now = datetime.now()
                fecha = now.strftime('%Y-%m-%d')
                hora = now.strftime("%H:%M:%S")
                #Recuperamos los valores de pantalla de confirmacion
                monedaOrigen = form.monedaOrigen.data
                monedaDestino = form.monedaDestino.data
                importeOrigen = form.importeOrigen.data
                importeDestino = form.importeDestino.data
                queries.insertaCompra((fecha, hora, monedaOrigen, importeOrigen, monedaDestino, importeDestino))
                return redirect(url_for("movimientosCrypto"))
            
            elif form.validate():

                if form.calc.data:
                    monedaActual = "EUR"
                    #Reseteamos los campos de la ventana de confirmacion
                    form.monedaOrigen.data = form.monedaDestino.data = form.importeOrigen.data = form.importeDestino.data = form.precio_unitario.data = ""
                    #validamos que tenemos importe suficiente para convertir en la moneda seleccionada (EUR ilimitados)
                    monedaActual = form.from_currency.data
                    if (monedaActual != 'EUR'):
                        saldoMonedaActual = float(request.form[monedaActual])
                        if form.from_quantity.data > saldoMonedaActual:
                            form.from_quantity.errors.append("no hay saldo suficiente de la moneda seleccionada: %d%s" %(saldoMonedaActual, monedaActual))                            
                            raise Exception("Error por saldo insuficiente")
                    
                    #Consultamos el precio unitario de la crypto llamando a la API
                    precioUnitario = getPrecioUnitarioCrypto((1, monedaActual, form.to_currency.data))
                    form.precio_unitario.data = precioUnitario
                    if precioUnitario > 0:
                        #Calculamos el importe en la nueva moneda
                        form.to_quantity.data = form.from_quantity.data * precioUnitario
                        #Asignamos los valores a los hidden
                        form.monedaOrigen.data = form.from_currency.data
                        form.monedaDestino.data = form.to_currency.data
                        form.importeOrigen.data = form.from_quantity.data
                        form.importeDestino.data = form.to_quantity.data
                        form.precioUnitario.data = form.precio_unitario.data
                    
            return render_template("compra.html", form=form,  cryptosDisponibles=listaCrypto)

        else:
            return render_template("compra.html", form=form, cryptosDisponibles=listaCrypto)
        
    except Exception as e:
        print("Error en el submit del formulario: {}". format(type(e).__name__, e))
        return render_template("compra.html", form=form, cryptosDisponibles=listaCrypto)


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
    saldoCryptoenEuros = 0
    if listaCrypto:
        for registroCrypto in listaCrypto:
            if registroCrypto["importe_destino"] > 0:
                saldoCryptoenEuros += getPrecioUnitarioCrypto((registroCrypto["importe_destino"], registroCrypto["to_currency"], "EUR"))


    #Valor actual: cálculo de Total de euros invertidos + Saldo de euros invertidos (ganancia/perdida) + Valor de euros de nuestras cryptos (inversión atrapada)
    valorActual = totalEuros + saldoEuros + saldoCryptoenEuros

    return render_template("estado.html", totalEuros=totalEuros, valorActual=valorActual)