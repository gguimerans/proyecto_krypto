from movements import app
from flask import render_template, request, url_for, redirect
import csv
import sqlite3
from datetime import date, datetime

DBFILE = "movements/data/bbdd_crypto.db"

def consultaBD(query, params):
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()    

    c.execute(query, params)

    conn.commit()
    conn.close()

    return c.fetchall()

@app.route("/")
def movimientosCrypto():
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()
    c.execute("SELECT date, time, from_currency, from_quantity, to_currency, to_quantity, from_quantity/to_quantity FROM tabla_movimientos;")

    movimientos = c.fetchall()

    if not movimientos:
            conn.close()
            return render_template("sin_movimientos.html") 
    else:    
        conn.close()
        return render_template("movimientos.html", movimientos=movimientos) 
    
# pendiente cálculo de P.U.
@app.route("/compra", methods=["GET", "POST"])
def compraCrypto():
    monedas = ("EUR", "BTC", "ETH", "XRP", "LTC", "BCH", "BNB", "USDT", "EOS", "BSV", "XLM", "ADA", "TRX")

    if request.method == "POST":

        now = datetime.now()
        fecha = now.strftime('%Y-%m-%d')
        hora = now.strftime("%H:%M:%S")

        conn = sqlite3.connect(DBFILE)
        c = conn.cursor()

        c.execute("INSERT INTO tabla_movimientos (date, time, from_currency, from_quantity, to_currency, to_quantity) VALUES (?,?,?,?,?,?);",
                (
                    fecha, 
                    hora, 
                    request.form.get("fromMoneda"),
                    float(request.form.get("cantidadFrom")),
                    request.form.get("toMoneda"),
                    float(request.form.get("cantidadTo"))     
                )
        )    
            
        conn.commit()
        conn.close()

        return redirect(url_for("movimientosCrypto"))
          

    return render_template("compra.html", monedas=monedas)
    


@app.route("/estado", methods=["GET"])
def statusCrypto():
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()


#Consulta de saldo de Euros invertidos    
    c.execute("SELECT M.importe_destino - M2.importe_origen as saldoEuros "
                "FROM "
                "(SELECT coalesce(sum(to_quantity), 0) as importe_destino "
                "FROM tabla_movimientos "
                "WHERE to_currency = 'EUR') as M, "
                "(SELECT coalesce(sum(from_quantity), 0) as importe_origen "
                "FROM tabla_movimientos "
                "WHERE from_currency = 'EUR') as M2;"
            )

    consultaSaldo = c.fetchone()

    saldoEuros = 0

    if consultaSaldo:
        saldoEuros = consultaSaldo[0]

#Consulta de total de Euros invertidos
    c.execute("""SELECT coalesce(sum(from_quantity), 0)
                FROM tabla_movimientos 
                WHERE from_currency = 'EUR';"""
            )    
    consultaTotal = c.fetchone()

    totalEuros = 0

    if consultaTotal:
        totalEuros = consultaTotal[0]



#Consulta listado de cryptomonedas y sus valores
    c.execute("""SELECT coalesce(sum(to_quantity), 0) as importe_destino, to_currency
                FROM tabla_movimientos
                WHERE to_currency != 'EUR'
                GROUP BY to_currency;"""
            )
    consultaToAll = c.fetchall()

    c.execute("""SELECT coalesce(sum(from_quantity), 0) as importe_origen, from_currency
                FROM tabla_movimientos
                WHERE from_currency != 'EUR'
                GROUP BY from_currency;"""
            )
    consultaFromAll = c.fetchall()

    listaCrypto = []

    if consultaToAll:
        if consultaFromAll:
            for registroTo in consultaToAll:
                saldoCrypto = registroTo[0]
                monedaTo = registroTo[1]
                for registroFrom in consultaFromAll:
                    monedaFrom = registroFrom[1]
                    if monedaTo == monedaFrom:
                        saldoCrypto = registroTo[0] - registroFrom[0]
                        break
            
                listaCrypto.append((saldoCrypto, monedaTo))

    if consultaFromAll:
        if consultaToAll:
            for registroFrom in consultaFromAll:
                saldoCrypto = registroFrom[0]*(-1)
                monedaFrom = registroFrom[1]
                encontrado = False
                for registroTo in consultaToAll:
                    monedaTo = registroTo[1]
                    if monedaTo == monedaFrom:
                        encontrado=True
                        break 
                if encontrado == False:
                    listaCrypto.append((saldoCrypto, monedaFrom))
    
    
    #Consulta saldo Cryptomonedas: pendiente conexión con API para hacer conversión real (saldoCryptoenEuros)
    saldoCrypto = 0
    for registroCrypto in listaCrypto:    
        saldoCrypto += registroCrypto[0]

    saldoCryptoenEuros = saldoCrypto*2

    #Valor actual: cálculo de Total de euros invertidos + Saldo de euros invertidos (ganancia/perdida) + Valor de euros de nuestras cryptos (inversión atrapada)

    valorActual = totalEuros + saldoEuros + saldoCryptoenEuros

    conn.close()
    return render_template("estado.html", totalEuros=totalEuros, valorActual=valorActual)


