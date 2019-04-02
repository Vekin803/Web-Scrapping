
import fdb
import csv

familia = 'REL_CASIO_COLLECTION'

con = fdb.connect(dsn='192.168.1.252:W:\\STECCS_MGV.FDB',
                  user='sysdba',
                  password='masterkey',
                  charset='UTF8')

cur = con.cursor()
result = cur.execute("SELECT A.CODIGO_ARTICULO FROM ARTICULOS A JOIN ALMACENES AL ON (AL.CODIGO_ARTICULO = A.CODIGO_ARTICULO)  WHERE A.FAMILIA = '{}' AND AL.ALMACEN = '02' ORDER BY CODIGO_ARTICULO".format(familia))
modelos_db = cur.fetchall()
con.close()

modelos = []

for model in modelos_db:
    modelos.append(model[0])

print(len(modelos))
