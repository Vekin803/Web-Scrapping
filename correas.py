import requests
import time
from pathlib import Path

straps =[]

with open('straps.txt', 'r') as f:
    for line in f:
        straps.append(line.strip())



base_url = 'https://www.casioindiashop.com/product_images/enlarge-image/'
local = "\\\\192.168.1.254\\W\\Multimedia\\Correas\\"
extension = '.jpg'


for strap in straps:
    straps.remove(strap)
    with open('straps.txt', 'w') as f:
        for s in straps:
            f.write(s + '\n')
    file_name = local + strap + extension
    p = Path(file_name)
    if p.is_file() is not True:
        url = base_url + strap + extension    
        r = requests.get(url)
        header = r.headers
        if header['Content-type'] == 'image/jpeg':
            imagen = r.content
            with open(file_name, 'wb') as file:
                file.write(imagen)
        time.sleep(5)
    else:
        pass
    