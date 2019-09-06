import fdb


# Conectando a la BBDD
con = fdb.connect(dsn='192.168.1.252:W:\\STECCS_MGV.FDB',
                  user='sysdba',
                  password='masterkey',
                  charset='UTF8')


# Sacar los datos de la BBDD
cursor = con.cursor()
result = cursor.execute("SELECT CODIGO_ARTICULO, DESCRIPCION_ARTICULO FROM ARTICULOS WHERE FAMILIA = 'FOR_CASIO_CORREA' AND (FICHERO_IMAGEN = '' OR FICHERO_IMAGEN IS NULL)")
straps = [row[0] for row in result]
con.close()


# Generar el TXT con las referencias de las correas
with open('straps.txt', 'w') as f:
    for strap in straps:
        f.write(strap + '\n')