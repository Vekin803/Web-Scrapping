import fdb
# from rhythm_b2b import rhythm

# Conectando a la BBDD
con = fdb.connect(dsn='192.168.1.252:W:\\STECCS_MGV.FDB',
                  user='sysdba',
                  password='masterkey',
                  charset='UTF8')

# Sacar los datos de la BBDD
cursor = con.cursor()
marca = input('Seleccione la marca de la que quiere conseguir los datos(1=Casio, 2=Rhythm) ')
familia = input('De que familia CASIO quieres sacar los datos? ')
result = cursor.execute("SELECT CODIGO_ARTICULO FROM ARTICULOS WHERE FAMILIA = '{}'".format(familia))
# result = cursor.execute("SELECT CODIGO_ARTICULO FROM ARTICULOS WHERE CODIGO_ARTICULO = 'HDC-700-1AVEF'")
items = [row[0] for row in result]
# items = ['A158WEA-1EF', 'A168WG-9EF']
con.close()

# print(items)
# print(len(items))

from casio_wapis import casio

for it in items:
    item = it.strip()
    if marca == '1':
        modelo = casio(item)
    # elif marca == '2':
        # modelo = rhythm(item)

    if modelo:
        print("Se han recogido los datos del modelo {} correctamente".format(item))
    else:
        print("El modelo {} no existe en el WAPIS".format(item))

print('Ha finalizado la recolección de datos')


# for watch in listado:
#     for item in watch.keys():
#         print(item, watch[item])

