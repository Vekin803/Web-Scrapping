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
            func_list = []
            img_td = func.find('td')[1]
            img_attrs = img_td.attrs
            img_html_split = img_attrs['style'].split(';')
            img_url_split = img_html_split[3].split(')')
            img_url = img_url_split[0].replace('background:url(', '')
            img_name = img_url.replace('http://wapis.casio-europe.com/bilderordner/pictoidbilder/', '')
            img_name_func = img_name.replace('.jpg', '')
            funciones['img_name_func'] = img_name_func
            func_path = item + '/funciones/' + img_name 
            funciones['func_path'] = func_path
            try:
                data2 = session.get(img_url)
                func_b64 = base64.b64encode(data2.content)
                func_file = open(Path(func_path), 'wb')
                func_file.write(data2.content)
                func_file.close()
            except:
                print('No hay foto de funcion')
                func_b64 = ''
            print(img_name_func)
            funciones['func_b64'] = func_b64
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
                func_list.extend((desc,img_name_func,img_url,func_b64))
                funciones[titulo] = func_list
            else:
                titulo = titulo_func_b.text
                desc = desc_func_final
                func_list.extend((desc,img_name_func,img_url,func_b64))
                funciones[titulo] = func_list
        print(funciones['Iluminación de la pantalla'][0])
        return modelo
    else:
        return None

# casio(item)