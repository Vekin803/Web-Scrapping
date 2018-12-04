import psycopg2
from requests_html import HTMLSession
import os
from pathlib import Path
# import urllib.request
# import urllib
import base64

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

             # Selecccionando el link de la imágen y el codificando en base64
        img_link = side_r.attrs['src']
        data = session.get(img_link)
        img_b64 = base64.b64encode(data.content)
        
             # Crear la imagen a partir del base64 
        # fh = open("imageToSave.png", "wb")
        # fh.write(base64.b64decode(imgcode))
        # fh.close()

             # Creando el archivo de la imagen
        try:
            img_file = open(Path(filename), 'wb')
            img_file.write(data.content)
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
            img_td = func.find('td')[1]
            img_attrs = img_td.attrs
            img_html_split = img_attrs['style'].split(';')
            img_url_split = img_html_split[3].split(')')
            img_url = img_url_split[0].replace('background:url(', '')
            funciones['img_url'] = img_url
            data2 = session.get(img_url)
            func_b64 = base64.b64encode(data2.content)
            funciones['func_b64'] = func_b64
            img_name = img_url.replace('http://wapis.casio-europe.com/bilderordner/pictoidbilder/', '')
            img_name_func = img_name.replace('.jpg', '')
            func_path = item + '/funciones/' + img_name 
            funciones['func_path'] = func_path
            try:
                func_file = open(Path(func_path), 'wb')
                func_file.write(data2.content)
                func_file.close()
            except:
                print('No hay foto de funcion')
            print(img_name_func)
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


        conn = psycopg2.connect(host='192.168.1.252', database='casio', user='postgres', password='Mgv17Watch')
        cur = conn.cursor()
        cur.execute('INSERT INTO reloj (referencia, tipo_reparacion, pila, modulo, categoria, img_url, img_blob) VALUES ( %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (referencia) DO UPDATE SET tipo_reparacion = EXCLUDED.tipo_reparacion, pila = EXCLUDED.pila, modulo = EXCLUDED.modulo, categoria = EXCLUDED.categoria, img_url = EXCLUDED.img_url, img_blob = EXCLUDED.img_blob RETURNING id', 
                    (modelo['Referencia'], modelo['Tipo'], modelo['Pila'], modelo['Modulo'], modelo['Categoria'], filename, img_b64))
        conn.commit()
        id_modelo = cur.fetchone()[0]
        
        for func in funciones.keys():
            cur.execute('INSERT INTO funcion (nombre, descripcion, img_name, img_url, img_blob) VALUES ( %s, %s, %s, %s, %s) ON CONFLICT (nombre) DO UPDATE SET descripcion = EXCLUDED.descripcion, img_name = EXCLUDED.img_name, img_url = EXCLUDED.img_url, img_blob = EXCLUDED.img_blob RETURNING id', 
                        (func, funciones[func], funciones['img_name_func'], funciones['func_path'], funciones['func_b64']))
            id_funcion = cur.fetchone()[0]
            conn.commit()
            cur.execute('INSERT INTO reloj_funcion (id_reloj, id_funcion) VALUES ( %s, %s) ON CONFLICT (id_reloj, id_funcion) DO NOTHING', (id_modelo, id_funcion))
            conn.commit()
        # conn.commit()

        #      # Imagenes de funciones
        # table_img_func = bigdiv[3]
        # img_tags = table_img_func.find('img')
        # try:
        #     os.mkdir(item + '/funciones')
        # except:
        #     print("La carpeta para las funciones del articulo {} ya existe".format(item))

        # for img in img_tags:
        #     alt_img = img.attrs['alt']
        #     src_img = img.attrs['src']
        #     func_filename = item + '/funciones/' + alt_img + '.jpg'
        #     cur.execute('INSERT INTO imagen_funcion (nombre, link, id_reloj) VALUES ( %s, %s, %s) ON CONFLICT (nombre, id_reloj) DO UPDATE SET link = EXCLUDED.link', 
        #                 (alt_img, func_filename, id_modelo))
        #     conn.commit()
        #     func_file = open(func_filename, 'wb')
        #     try:
        #         func_file.write(urllib.request.urlopen(src_img).read())
        #     except:
        #         print("La imagen de la función {} ya existe".format(alt_img))
        #     func_file.close()

        conn.close()

        # print(modelo)
        return modelo
    else:
        return None

# casio(item)