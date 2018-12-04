import fdb
from casio_wapis_2 import casio
# from rhythm_b2b import rhythm

# # Conectando a la BBDD
con = fdb.connect(dsn='192.168.1.252:W:\STECCS_MGV_TEST.FDB',
                  user='sysdba',
                  password='masterkey',
                  charset='UTF8')

# # Sacar los datos de la BBDD
cursor = con.cursor()
marca = input('Seleccione la marca de la que quiere conseguir los datos(1=Casio, 2=Rhythm) ')
# familia = input('De que familia CASIO quieres sacar los datos? ')
# result = cursor.execute("SELECT CODIGO_ARTICULO FROM ARTICULOS WHERE FAMILIA = '{}'".format(familia))
result = cursor.execute("SELECT CODIGO_ARTICULO FROM ARTICULOS WHERE CODIGO_ARTICULO = 'A158WEA-1EF'")
items = [row[0] for row in result]
con.close()




for item in items:

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

