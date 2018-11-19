import psycopg2
from requests_html import HTMLSession
import os
import urllib

# item = 'GBD-800-1ER'

def casio(item):
    # Consiguiendo el HTML real
    session = HTMLSession()
    r = session.get("http://www.css2.casio.de/servicewapis/_details.php?watch={}&stamp=&language=es".format(item))
    html = r.html

    existe = html.find(containing='Recommended retail price EU', first=True)
    modelo = {}

    if existe:
        print('{}'.format(item))
        # Creando la carpeta
        try:
            os.mkdir(item)
        except:
            print("La carpeta del articulo {} ya existe".format(item))

        # Coger el div general
        bigdiv = html.find('div.rahmen')

        # Sacando imagen del modelos y de las funciones
            # Imagen del modelos
             # Generando la ruta para el archivo
        filename = "{}/{}.jpg".format(item,item)

             # Cogiendo el DIV derecho de la página
        side_r = html.find("div > img[alt={}]".format(item), first=True)

             # Selecccionando el link de la imágen
        img_link = side_r.attrs['src']

             # Creando el archivo de la imagen
        try:
            img_file = open(filename, 'wb')
            img_file.write(urllib.request.urlopen(img_link).read())
            img_file.close()
        except:
            print("La imagen del articulo {} no existe".format(item))


        # Recopilando los datos del modelo
             # Referencia
        ref = html.find('h1', first=True).text
        modelo['Referencia'] = ref

            # Tipo de reparación
        try:
            table_tipo = bigdiv[1].find('table > tr > td > table', first=True)
            b = table_tipo.find('td > b', first=True)
            tipo = b.text
            modelo['Tipo'] = tipo
        except:
            modelo['Tipo'] = '-'

            # Tipo de Pila
        td_pila = html.find('div > table > tr > td > div.rahmen > table > tr > td', containing='Tipo de pila')
        slash_pila = td_pila[1].html.split('<br/>')
        ref_pila = slash_pila[1].replace('</td>', '')
        modelo['Pila'] = ref_pila

            # Módulo
        table_modulo = bigdiv[2].find('table > tr > td')
        td_modulo = table_modulo[1].find('td', first=True)
        slash_modulo = td_modulo.html.split('<br/>')
        ref_modulo = slash_modulo[1].replace('</td>', '')
        modelo['Modulo'] = ref_modulo

            # Categoría
        table_cat = bigdiv[2].find('table > tr > td')
        slash_cat = table_cat[5].html.split('<br/>')
        cat = slash_cat[1].replace('</td>', '')
        modelo['Categoria'] = cat


            # Funciones
        funciones = {}
        div_func = bigdiv[4]
        table_func = div_func.find('table > tr > td > table > tr')
        for func in table_func:
            titulo_func_a = func.find('a > b', first=True)
            desc_func_a = func.find('div.unsichtbar > div', first=True)
            titulo_func_b = func.find('td > b', first=True)
            desc_slash_func = func.html.split('<br/>')
            desc_func_slashed = desc_slash_func[1]
            desc_func_n = desc_func_slashed.replace('\n', '')
            desc_func_final = desc_func_n.replace('\t', '')
            if titulo_func_a:
                titulo = titulo_func_a.text
                desc = desc_func_a.text
                funciones[titulo] = desc
            else:
                titulo = titulo_func_b.text
                desc = desc_func_final
                funciones[titulo] = desc


        conn = psycopg2.connect(host='localhost', database='casio', user='postgres', password='masterkey')
        cur = conn.cursor()
        cur.execute('INSERT INTO reloj (referencia, tipo_reparacion, pila, modulo, categoria, imagen) VALUES ( %s, %s, %s, %s, %s, %s) ON CONFLICT (referencia) DO UPDATE SET tipo_reparacion = EXCLUDED.tipo_reparacion, pila = EXCLUDED.pila, modulo = EXCLUDED.modulo, categoria = EXCLUDED.categoria, imagen = EXCLUDED.imagen RETURNING id', 
                    (modelo['Referencia'], modelo['Tipo'], modelo['Pila'], modelo['Modulo'], modelo['Categoria'], filename))
        conn.commit()
        id_modelo = cur.fetchone()[0]
        
        for func in funciones.keys():
            cur.execute('INSERT INTO funcion (nombre, descripcion, id_reloj) VALUES ( %s, %s, %s) ON CONFLICT (nombre, id_reloj) DO UPDATE SET descripcion = EXCLUDED.descripcion', 
                        (func, funciones[func], id_modelo))
        conn.commit()

             # Imagenes de funciones
        table_img_func = bigdiv[3]
        img_tags = table_img_func.find('img')
        try:
            os.mkdir(item + '/funciones')
        except:
            print("La carpeta para las funciones del articulo {} ya existe".format(item))

        for img in img_tags:
            alt_img = img.attrs['alt']
            src_img = img.attrs['src']
            func_filename = item + '/funciones/' + alt_img + '.jpg'
            cur.execute('INSERT INTO imagen_funcion (nombre, link, id_reloj) VALUES ( %s, %s, %s) ON CONFLICT (nombre, id_reloj) DO UPDATE SET link = EXCLUDED.link', 
                        (alt_img, func_filename, id_modelo))
            conn.commit()
            func_file = open(func_filename, 'wb')
            try:
                func_file.write(urllib.request.urlopen(src_img).read())
            except:
                print("La imagen de la función {} ya existe".format(alt_img))
            func_file.close()

        conn.close()

        # print(modelo)
        return modelo
    else:
        return None

# casio(item)