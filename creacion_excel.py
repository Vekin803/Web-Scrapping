
import psycopg2
from pathlib import Path
import time
import xlsxwriter



#Conectar con base de datos de intranet para sacar los datos de las funciones de los relojes
conn = psycopg2.connect(host='192.168.1.252', database='casio', user='postgres', password='Mgv17Watch')
cur = conn.cursor()

#Consulta para sacar los datos de cada modelo
cur.execute("""
SELECT 
    r.referencia,
    r.modulo,
    r.tipo_reparacion,
    r.pila,
    r.categoria
FROM public.reloj r
""")
modelos = cur.fetchall()

#Loop entre los modelos para crear el diccionario de cada modelo con sus caracteristicas y funciones
modelos_dict = {}

for model in modelos:
    funciones = {}
    modelos_dict[model[0]] = {'modulo': model[1], 'tipo': model[2], 'pila': model[3], 'categoria': model[4]}
    cur.execute("""
        SELECT         
            f.nombre,
            f.descripcion,
            f.img_name
        FROM public.reloj r
        JOIN public.reloj_funcion rf ON r.id = rf.id_reloj
        JOIN public.funcion f ON f.id = rf.id_funcion
        WHERE r.referencia = '{}'
        """.format(model[0]))
    funcion = cur.fetchall()
    for func in funcion:
        funciones[func[0]] = [func[1], func[2]]
    modelos_dict[model[0]]['funciones'] = funciones

# print(modelos_dict['GD-100-1AER'])


# # Creando el archivo y la hoja
timestr = time.strftime("%Y%m%d%H%M%S")
archivo = xlsxwriter.Workbook(Path('\\\\192.168.1.254\\G\\MGV\\SIRO\\Informacion_wapis\\Excel_Wapis_' + timestr + '.xlsx'))
hoja = archivo.add_worksheet()

# # Añadiendo estilos
bold = archivo.add_format({'bold': True})

# # Añadiendo los titulos de las columnas
hoja.write('A1', 'Referencia', bold)
hoja.write('B1', 'Modulo', bold)
hoja.write('C1', 'Tipo', bold)
hoja.write('D1', 'Pila', bold)
hoja.write('E1', 'Categoria', bold)
hoja.write('F1', 'Funciones', bold)

row = 1
col = 0

for modelo in modelos_dict:
    hoja.write(row, col, modelo)
    col += 1
    hoja.write(row, col, modelos_dict[modelo]['modulo'])
    col += 1
    hoja.write(row, col, modelos_dict[modelo]['tipo'])
    col += 1
    hoja.write(row, col, modelos_dict[modelo]['pila'])
    col += 1
    hoja.write(row, col, modelos_dict[modelo]['categoria'])
    col += 1
    for func in modelos_dict[modelo]['funciones']:
        if modelos_dict[modelo]['funciones'][func][1] != '':
            hoja.write(row, col, modelos_dict[modelo]['funciones'][func][1])
            col += 1
            if modelos_dict[modelo]['funciones'][func][0] != '':
                hoja.write(row, col, func + ': ' + modelos_dict[modelo]['funciones'][func][0])
                col += 1
            else:
                hoja.write(row, col, func)
                col += 1
        else:
            pass
    row += 1
    col = 0

archivo.close()
