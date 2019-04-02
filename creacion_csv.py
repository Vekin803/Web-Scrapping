
import fdb
import psycopg2
import csv

familia = 'REL_CASIO_COLLECTION'


 # Conexion a la base de datos de Elite
connect = fdb.connect(dsn='192.168.1.252:W:\\STECCS_MGV.FDB',
                  user='sysdba',
                  password='masterkey',
                  charset='UTF8')

cursor = connect.cursor()

result_model = cursor.execute("SELECT A.CODIGO_ARTICULO FROM ARTICULOS A JOIN ALMACENES AL ON (AL.CODIGO_ARTICULO = A.CODIGO_ARTICULO)  WHERE A.FAMILIA = '{}' AND AL.ALMACEN = '02' ORDER BY CODIGO_ARTICULO".format(familia))
modelos_db = cursor.fetchall()

modelos = []

for model in modelos_db:
    modelos.append(model[0])


for model in modelos:
    result = cursor.execute("SELECT DESCRIPCION_ARTICULO, FAMILIA, PRECIO_CON_IVA, COSTE, CODIGO_BARRAS FROM ARTICULOS WHERE CODIGO_ARTICULO = '{}'".format(model))
    items = cursor.fetchall()[0]



    descripcion = items[0]

    if items[1] == 'REL_CASIO_COLLECTION':
        categoria = '6_5_4'
        proveedor = 'Casio'
        marca = 'Casio'
        etiquetas = 'reloj_casio_collection'


    precio_iva = items[2]
    coste = items[3]
    ean13 = items[4]
    url_img = 'https://www.mgvwatch.com/upload/' + model + '.jpg'


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
    """.format(model))
    funcion = cur.fetchall()
    conn.close()

    funciones = ""

    for i, func in enumerate(funcion, start=1):
        if i < len(funcion):
            funciones += func[0] + ":" + func[1] + ":" + "1:0_"
        else:
            funciones += func[0] + ":" + func[1] + ":" + "1:0"


    #Crear el CSV con todos los datos de cada reloj
    with open('presta.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Activo', 'Modelo', 'Categoria', 'Precio IVA', 'ID Impuesto', 'Coste', 'Referencia', 'Ref proveedor', 'Proveedor', 'Marca', 'EAN13', 'Cantidad', 'Descripcion', 'Etiquetas', 'Meta-titulo', 'Meta-keywords', 'Meta-descripcion', 'Url imagen', 'Caracteristicas'])
        spamwriter.writerow([1, model, categoria, precio_iva, 1, coste, model, model, proveedor, marca, ean13, 0, descripcion, etiquetas, model, etiquetas, descripcion, url_img, funciones])

connect.close()