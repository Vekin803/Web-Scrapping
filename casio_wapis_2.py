# import os
# from pathlib import Path
from requests_html import HTMLSession

# # rutaDiscoDuro = "\\\\192.168.1.254\\W\\Multimedia\\Casio\\Relojes"
# item = "A158WEA-1EF"


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

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
urls = {"https://www.css2.casio.de/servicewapis/_details.php?watch=BAX-100-1AER&stamp=&language=es","https://www.css2.casio.de/servicewapis/_details.php?watch=A168WG-9EF&stamp=&language=es"}

driver = webdriver.Chrome()
for url in urls :
    # driver = webdriver.Chrome()
    driver.get(url)
    session = HTMLSession()
    r = session.get(driver.current_url, verify=False)
    html = r.html
    print(html.text)

driver.quit()

