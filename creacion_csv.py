
import fdb
import psycopg2
import csv

modelo = 'LA690WEA-1EF'


 # Conexion a la base de datos de Elite
connect = fdb.connect(dsn='192.168.1.252:W:\\STECCS_MGV.FDB',
                  user='sysdba',
                  password='masterkey',
                  charset='UTF8')

cursor = connect.cursor()
result = cursor.execute("SELECT DESCRIPCION_ARTICULO, FAMILIA, PRECIO_CON_IVA, COSTE, CODIGO_BARRAS FROM ARTICULOS WHERE CODIGO_ARTICULO = '{}'".format(modelo))
items = cursor.fetchall()[0]
connect.close()


descripcion = items[0]

if items[1] == 'REL_CASIO_COLLECTION':
    categoria = '6_5_4'
    proveedor = 'Casio'
    marca = 'Casio'
    etiquetas = 'reloj_casio_collection'


precio_iva = items[2]
coste = items[3]
ean13 = items[4]
url_img = 'https://www.mgvwatch.com/upload/' + modelo + '.jpg'


 #Conectar con base de datos de intranet para sacar los datos de las funciones de los relojes
conn = psycopg2.connect(host='192.168.1.252', database='casio', user='postgres', password='Mgv17Watch')
cur = conn.cursor()
cur.execute("""
SELECT 
    f.nombre as FUNCION,
    f.descripcion as DESCRIPCION
FROM public.reloj r
JOIN public.reloj_funcion rf ON r.id = rf.id_reloj
JOIN public.funcion f ON f.id = rf.id_funcion
WHERE r.referencia = '{}'
""".format(modelo))
funcion = cur.fetchall()
conn.close()

funciones = ""

for i, func in enumerate(funcion, start=1):
    if i < len(funcion):
        funciones += func[0] + ":" + func[1] + ":" + "1:0_"
    else:
        funciones += func[0] + ":" + func[1] + ":" + "1:0"




 #Crear el CSV con todos los datos de cada reloj
with open('presta.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['Activo', 'Modelo', 'Categoria', 'Precio IVA', 'ID Impuesto', 'Coste', 'Referencia', 'Ref proveedor', 'Proveedor', 'Marca', 'EAN13', 'Cantidad', 'Descripcion', 'Etiquetas', 'Meta-titulo', 'Meta-keywords', 'Meta-descripcion', 'Url imagen', 'Caracteristicas'])
    spamwriter.writerow([1, modelo, categoria, precio_iva, 1, coste, modelo, modelo, proveedor, marca, ean13, 0, descripcion, etiquetas, modelo, etiquetas, descripcion, url_img, funciones])
