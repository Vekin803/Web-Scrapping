import psycopg2
from requests_html import HTMLSession
import os
from pathlib import Path
import urllib.request
import urllib
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
        

        # Coger el div general
        bigdiv = html.find('div.rahmen')


        try:
            os.mkdir(item)
        except:
            print("La carpeta del articulo {} ya existe".format(item))

        try:
            os.mkdir(Path(item + '/funciones'))
        except:
            print("La carpeta para las funciones del articulo {} ya existe".format(item))

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
            img_name = img_url.replace('http://wapis.casio-europe.com/bilderordner/pictoidbilder/', '')
            img_name_func = img_name.replace('.jpg', '')
            func_path = item + '/funciones/' + img_name 
            try:
                func_file = open(Path(func_path), 'wb')
                data2 = session.get(img_url)
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
        #     try:
        #         func_file.write(urllib.request.urlopen(src_img).read())
        #     except:
        #         print("La imagen de la función {} ya existe".format(alt_img))
        #     func_file.close()


        # print(modelo)
        return modelo
    else:
        return None

# casio(item)