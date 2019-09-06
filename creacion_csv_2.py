
import fdb
import psycopg2
import csv
import os
from pathlib import Path
from ftplib import FTP

# familia = 'REL_CASIO_COLLECTION'

 # Preparación para usar el FTP
ftp = FTP('ftp.mgvwatch.com')
rutaRelojes = "\\\\192.168.1.254\\G\\MGV\\SIRO\\Marketing\\Fotografias Articulos\\fotos casio kevin\\collection"

 # Conexion a la base de datos de Elite
connect = fdb.connect(dsn='192.168.1.252:W:\\STECCS_MGV.FDB',
                  user='sysdba',
                  password='masterkey',
                  charset='UTF8')
            
#Conectar con base de datos de intranet para sacar los datos de las funciones de los relojes
conn = psycopg2.connect(host='192.168.1.252', database='casio', user='postgres', password='Mgv17Watch')
cur = conn.cursor()

cursor = connect.cursor()
# result_model = cursor.execute("SELECT A.CODIGO_ARTICULO FROM ARTICULOS A JOIN ALMACENES AL ON (AL.CODIGO_ARTICULO = A.CODIGO_ARTICULO)  WHERE AL.ALMACEN = '02' AND A.PRE4 != 'WEB' ORDER BY CODIGO_ARTICULO")
# modelos_db = cursor.fetchall()
modelos_db = 'A168WA-1YES'

modelos = []

for model in modelos_db:
    modelos.append(model[0])

modelos_dict = {}

for model in modelos:
    result = cursor.execute("SELECT DESCRIPCION_ARTICULO, FAMILIA, PRECIO_CON_IVA, COSTE, CODIGO_BARRAS FROM ARTICULOS WHERE CODIGO_ARTICULO = '{}'".format(model))
    items = cursor.fetchall()[0]

    if items[1] == 'REL_CASIO_COLLECTION':
        categoria = '6_5_4'
        proveedor = 'Casio'
        marca = 'Casio'
        etiquetas = 'reloj_casio_collection'
    elif items[1] == 'REL_CASIO_BABYG':
        categoria = '16_5_4'
        proveedor = 'Casio'
        marca = 'Casio'
        etiquetas = 'reloj_casio_babyg'
    elif items[1] == 'REL_CASIO_DESPERTADO'
        categoria = '20_5_4'
        proveedor = 'Casio'
        marca = 'Casio'
        etiquetas = 'reloj_casio_despertador'
    elif items[1] == 'REL_CASIO_EDIFICE'
        categoria = '14_5_4'
        proveedor = 'Casio'
        marca = 'Casio'
        etiquetas = 'reloj_casio_edifice'
    elif items[1] == 'REL_CASIO_GSHOCK'
        categoria = '15_5_4'
        proveedor = 'Casio'
        marca = 'Casio'
        etiquetas = 'reloj_casio_gshock'
    elif items[1] == 'REL_CASIO_PROTREK'
        categoria = '17_5_4'
        proveedor = 'Casio'
        marca = 'Casio'
        etiquetas = 'reloj_casio_protrek'
    elif items[1] == 'REL_CASIO_WAVECEPTOR'
        categoria = '18_5_4'
        proveedor = 'Casio'
        marca = 'Casio'
        etiquetas = 'reloj_casio_waveceptor'


    # precio_iva = items[2] 
    # coste = items[3]
    # ean13 = items[4]
    # descripcion = items[0]
    # url_img = 'https://www.mgvwatch.com/upload/' + model + '.jpg'

     # Sacando las funciones de cada modelo   
    cur.execute("""
        SELECT 
            f.nombre as FUNCION,
            f.descripcion as DESCRIPCION
        FROM public.reloj r
        JOIN public.reloj_funcion rf ON r.id = rf.id_reloj
        JOIN public.funcion f ON f.id = rf.id_funcion
        WHERE r.referencia = '{}'
        """.format(model))
    funcion = cur.fetchall()

    funciones = ""

    for i, func in enumerate(funcion, start=1):
        if i < len(funcion):
            funciones += func[0] + ":" + func[1] + ":" + "1:0_"
        else:
            funciones += func[0] + ":" + func[1] + ":" + "1:0"
    

    modelos_dict[model] = {'Activo': 1,
                           'Modelo': model,
                           'Categoria': categoria,
                           'Precio IVA': items[2],
                           'ID Impuesto': 1,
                           'Coste': items[3],
                           'Referencia': model,
                           'Ref proveedor': model,
                           'Proveedor': marca,
                           'EAN13': items[4],
                           'Cantidad': 0,
                           'Descripcion': items[0],
                           'Etiquetas': etiquetas,
                           'Meta titulo':model,
                           'Meta keywords': etiquetas,
                           'Meta descripcion': items[0],
                           'URL': 'https://www.mgvwatch.com/upload/' + model + '.jpg',
                           'Caracteristicas': funciones}

# print(modelos_dict['W-S210H-1AVEF'])


#Crear el CSV con todos los datos de cada reloj
with open('prestashop.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['Activo', 'Modelo', 'Categoria', 'Precio IVA', 'ID Impuesto', 'Coste', 'Referencia', 'Ref proveedor', 'Proveedor', 'Marca', 'EAN13', 'Cantidad', 'Descripcion', 'Etiquetas', 'Meta-titulo', 'Meta-keywords', 'Meta-descripcion', 'Url imagen', 'Caracteristicas'])
    for modelo in modelos_dict:
        spamwriter.writerow([modelos_dict[modelo]['Activo'],
                             modelos_dict[modelo]['Modelo'],
                             modelos_dict[modelo]['Categoria'],
                             modelos_dict[modelo]['Precio IVA'],
                             modelos_dict[modelo]['ID Impuesto'],
                             modelos_dict[modelo]['Coste'],
                             modelos_dict[modelo]['Referencia'],
                             modelos_dict[modelo]['Ref proveedor'],
                             modelos_dict[modelo]['Proveedor'],
                             modelos_dict[modelo]['EAN13'],
                             modelos_dict[modelo]['Cantidad'],
                             modelos_dict[modelo]['Descripcion'],
                             modelos_dict[modelo]['Etiquetas'],
                             modelos_dict[modelo]['Meta titulo'],
                             modelos_dict[modelo]['Meta keywords'],
                             modelos_dict[modelo]['Meta descripcion'],
                             modelos_dict[modelo]['URL'],
                             modelos_dict[modelo]['Caracteristicas']])


# for model in modelos:
#     cursor.execute("UPDATE ARTICULOS SET PRE4 = 'WEB' WHERE CODIGO_ARTICULO = '{}'".format(model))
#     connect.commit()

conn.close()
connect.close()