# import os
# from pathlib import Path
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# # rutaDiscoDuro = "\\\\192.168.1.254\\W\\Multimedia\\Casio\\Relojes"
item = "A158WEA-1EF"


# # if os.path.exists(Path(rutaDiscoDuro + "\\" + item)):
# #     print("La carpeta del articulo {} ya existe".format(item))
# # else:
# #     os.mkdir(rutaDiscoDuro + "\\" + item)

# session = HTMLSession()
# r = session.get("https://www.css2.casio.de/servicewapis/_details.php?watch='{}'&stamp=&language=es".format(item), verify = False)
# html = r.html
# # existe = html.find(containing='Recommended retail price EU', first=True)
# html2 = html.render
# print(html)

url = "https://www.css2.casio.de/servicewapis/_details.php?watch=LA690WEM-7EF&stamp=&language=es"

driver = webdriver.Chrome()
# driver = webdriver.Chrome()
driver.get(url)
session = HTMLSession()
r = session.get(driver.current_url, verify=False)
html = r.html
existe = html.find(containing='Categoría')
ex_html = existe[2].html
cat = ex_html.split('<br/>')
categoria = cat[1].replace('</td></tr>','')
# cat = ex_html.split
# existe = html.find('div > div.rahmen > table > tbody > tr > td')
# print(dir(existe))
# print(type(existe))
# print(type(existe[0]))
if categoria:
    print(categoria)
else:
    print('No categoria')
    
driver.quit()

