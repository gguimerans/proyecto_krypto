import sqlite3


class manejarDB:
    def __init__(self, dbpath):
        self.path = dbpath
        self.conn = None
        self.cursor = None

    def consultaBD(self, query, params=()):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()

        c.execute(query, params)
        conn.commit()

        filas = c.fetchall()

        conn.close()


        if len(filas) == 0:
            return filas

        columnNames = []
        for columnName in c.description:
            columnNames.append(columnName[0])

        listaDeDiccionarios = []

        for fila in filas:
            d = {}
            for ix, columnName in enumerate(columnNames):
                d[columnName] = fila[ix]
            listaDeDiccionarios.append(d)

        return listaDeDiccionarios

    def consultaBDFetchOne(self, query, params=()):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()

        c.execute(query, params)
        conn.commit()

        fila = c.fetchone()

        conn.close()

        return fila    


class queriesDB:
    def __init__(self, DBFILE):
        self.db = manejarDB(DBFILE)

    def getMovimientosCrypto(self):
        return self.db.consultaBD("SELECT date, time, from_currency, from_quantity, to_currency, to_quantity, (from_quantity/to_quantity) as precio_unitario FROM tabla_movimientos;")  

    def getSaldoEuros(self):
        return self.db.consultaBDFetchOne("""SELECT M2.importe_from - M.importe_to as saldoEuros
                FROM
                (SELECT coalesce(sum(to_quantity), 0) as importe_to
                FROM tabla_movimientos
                WHERE to_currency = 'EUR') as M,
                (SELECT coalesce(sum(from_quantity), 0) as importe_from
                FROM tabla_movimientos
                WHERE from_currency = 'EUR') as M2;"""
            )

    def getEurosInvertidos(self):
        return self.db.consultaBDFetchOne("""SELECT coalesce(sum(from_quantity), 0)
                FROM tabla_movimientos 
                WHERE from_currency = 'EUR';"""
            )    

    def getconsultaToAll(self):
        return self.db.consultaBD("""SELECT coalesce(sum(to_quantity), 0) as importe_destino, to_currency
                FROM tabla_movimientos
                WHERE to_currency != 'EUR'
                GROUP BY to_currency;"""
            )

    def getconsultaFromAll(self):
        return self.db.consultaBD("""SELECT coalesce(sum(from_quantity), 0) as importe_origen, from_currency
                FROM tabla_movimientos
                WHERE from_currency != 'EUR'
                GROUP BY from_currency;"""
            )
            
    def insertaCompra(self, params):
        return self.db.consultaBD("INSERT INTO tabla_movimientos (date, time, from_currency, from_quantity, to_currency, to_quantity) VALUES (?,?,?,?,?,?);", params)

