
import fdb
import csv
import os
from pathlib import Path
from ftplib import FTP

# familia = 'REL_CASIO_COLLECTION'

# con = fdb.connect(dsn='192.168.1.252:W:\\STECCS_MGV.FDB',
#                   user='sysdba',
#                   password='masterkey',
#                   charset='UTF8')

# cur = con.cursor()
# result = cur.execute("SELECT A.CODIGO_ARTICULO FROM ARTICULOS A JOIN ALMACENES AL ON (AL.CODIGO_ARTICULO = A.CODIGO_ARTICULO)  WHERE A.FAMILIA = '{}' AND AL.ALMACEN = '02' AND A.CODIGO_ARTICULO = 'A168WA-1YES' ORDER BY CODIGO_ARTICULO".format(familia))
# modelos_db = cur.fetchall()


modelos = ['A168WA-1YES','A168WEC-1EF']

# for model in modelos_db:
#     modelos.append(model[0])

# for model in modelos:
#     cur.execute("UPDATE ARTICULOS SET PRE4 = 'WEB' WHERE CODIGO_ARTICULO = '{}'".format(model))
#     con.commit()
ftp = FTP('ftp.mgvwatch.com')
rutaRelojes = "\\\\192.168.1.254\\G\\MGV\\SIRO\\Marketing\\Fotografias Articulos\\fotos casio kevin\\collection"

ftp.login(user='kevin@mgvwatch.com', passwd='KiNd138877')
ftp.cwd('/public_html/upload')
# ftp.retrlines('LIST')
relojesSinFoto = []


for model in modelos:
    if os.path.exists(Path(rutaRelojes + "\\" + model + ".jpg")):
        filename = model + '.jpg'
        print("La foto del modelo {} ha sido encontrada".format(model))
        ftp.storbinary('STOR '+ filename, open(Path(rutaRelojes + "\\" + model + ".jpg"), 'rb'))
        relojesSinFoto.append(model)
    else:
        relojesSinFoto.append(model)

ftp.quit()
# con.commit()
# con.close()
# print(modelos)

with open('faltanfotos.txt', 'w') as archivo:
    archivo.writelines("%s\n" % reloj for reloj in relojesSinFoto)
